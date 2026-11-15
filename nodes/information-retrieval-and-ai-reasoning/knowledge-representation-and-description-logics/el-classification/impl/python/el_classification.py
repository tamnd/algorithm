# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/el-classification/. The authors are listed in prov/JW3S50.jsonl.
"""Classification of an EL TBox with bottom by completion rules (Baader, Brandt and Lutz 2005).

Concepts are the tuples of dl.py, built from top, bottom, concept names, conjunction and existential
restriction. The TBox is a list of general concept inclusions (C, D). The algorithm first puts the
TBox in normal form, with fresh names that start with "_", then saturates the sets S(X) of
subsumers of each name X and the relations R(r) with five completion rules.
"""

from collections import deque
from typing import Optional, Sequence

from dl import BOTTOM, TOP, GCI, Concept, Interpretation, names

TOPN = "⊤"  # the name used for top inside the completion
BOTN = "⊥"  # the name used for bottom inside the completion


class NotEL(ValueError):
    """Raised for a concept that is not in EL with bottom."""


def is_el(c: Concept) -> bool:
    op = c[0]
    if op in ("top", "bottom", "atom"):
        return True
    if op == "and":
        return is_el(c[1]) and is_el(c[2])
    if op == "some":
        return is_el(c[2])
    return False


def simplify(c: Concept) -> Concept:
    """Remove top from conjunctions, and turn every part that contains bottom in a conjunction or an
    existential restriction into bottom. The result is equivalent to c."""
    op = c[0]
    if op == "and":
        a, b = simplify(c[1]), simplify(c[2])
        if BOTTOM in (a, b):
            return BOTTOM
        if a == TOP:
            return b
        if b == TOP:
            return a
        return ("and", a, b)
    if op == "some":
        f = simplify(c[2])
        return BOTTOM if f == BOTTOM else ("some", c[1], f)
    return c


class Normalizer:
    """Builds the normal form. Each axiom is one of
    ("sub", A, B)        A subsumed by B
    ("conj", A1, A2, B)  A1 and A2 subsumed by B
    ("ex_r", A, r, B)    A subsumed by some r.B
    ("ex_l", r, A, B)    some r.A subsumed by B
    where A, A1, A2 are names or top and B is a name, top or bottom."""

    def __init__(self) -> None:
        self.axioms: list[tuple] = []
        self.fresh = 0

    def _new(self) -> str:
        self.fresh += 1
        return f"_N{self.fresh}"

    @staticmethod
    def _base(c: Concept) -> Optional[str]:
        if c == TOP:
            return TOPN
        if c == BOTTOM:
            return BOTN
        if c[0] == "atom":
            return c[1]
        return None

    def left(self, c: Concept) -> str:
        """A name X with c subsumed by X, by new axioms that follow the structure of c."""
        b = self._base(c)
        if b is not None:
            return b
        x = self._new()
        if c[0] == "and":
            self.axioms.append(("conj", self.left(c[1]), self.left(c[2]), x))
        else:
            self.axioms.append(("ex_l", c[1], self.left(c[2]), x))
        return x

    def right(self, c: Concept) -> str:
        """A name X with X subsumed by c, by new axioms that follow the structure of c."""
        b = self._base(c)
        if b is not None:
            return b
        x = self._new()
        if c[0] == "and":
            self.axioms.append(("sub", x, self.right(c[1])))
            self.axioms.append(("sub", x, self.right(c[2])))
        else:
            self.axioms.append(("ex_r", x, c[1], self.right(c[2])))
        return x

    def add(self, c: Concept, d: Concept) -> None:
        c, d = simplify(c), simplify(d)
        if c == BOTTOM or d == TOP:
            return  # holds in every interpretation
        self.axioms.append(("sub", self.left(c), self.right(d)))


def normalize(tbox: Sequence[GCI]) -> list[tuple]:
    nz = Normalizer()
    for c, d in tbox:
        if not (is_el(c) and is_el(d)):
            raise NotEL(repr((c, d)))
        nz.add(c, d)
    return nz.axioms


class Completion:
    """The saturated sets S(X) and relations R(r) of a normalized TBox."""

    def __init__(self, axioms: Sequence[tuple], extra_names: Sequence[str] = ()) -> None:
        self.axioms = list(axioms)
        nm = {TOPN} | set(extra_names)
        sub: dict[str, list] = {}
        conj: dict[str, list] = {}
        ex_r: dict[str, list] = {}
        ex_l: dict[tuple, list] = {}
        for ax in self.axioms:
            if ax[0] == "sub":
                sub.setdefault(ax[1], []).append(ax[2])
                nm |= {ax[1], ax[2]}
            elif ax[0] == "conj":
                conj.setdefault(ax[1], []).append((ax[2], ax[3]))
                conj.setdefault(ax[2], []).append((ax[1], ax[3]))
                nm |= {ax[1], ax[2], ax[3]}
            elif ax[0] == "ex_r":
                ex_r.setdefault(ax[1], []).append((ax[2], ax[3]))
                nm |= {ax[1], ax[3]}
            else:
                ex_l.setdefault((ax[1], ax[2]), []).append(ax[3])
                nm |= {ax[2], ax[3]}
        nm.discard(BOTN)
        self.names = sorted(nm)
        self.S: dict[str, set] = {x: set() for x in self.names}
        self.R: dict[str, set] = {}
        self.pred: dict[str, set] = {x: set() for x in self.names}  # pairs (r, W) with (W, X) in R(r)
        self.steps = 0  # rule applications that added something
        queue: deque = deque()

        def add(x: str, a: str) -> None:
            if a not in self.S[x]:
                self.S[x].add(a)
                self.steps += 1
                queue.append((x, a))

        def add_edge(r: str, x: str, y: str) -> None:
            pairs = self.R.setdefault(r, set())
            if (x, y) in pairs:
                return
            pairs.add((x, y))  # @line L8
            self.steps += 1
            self.pred[y].add((r, x))
            for a in list(self.S[y]):
                for b in ex_l.get((r, a), ()):
                    add(x, b)  # @line L9
            if BOTN in self.S[y]:
                add(x, BOTN)  # @line L10

        for x in self.names:
            add(x, x)  # @line L1
            add(x, TOPN)
        while queue:  # @line L2
            x, a = queue.popleft()  # @line L3
            for b in sub.get(a, ()):
                add(x, b)  # @line L4
            for a2, b in conj.get(a, ()):
                if a2 in self.S[x]:
                    add(x, b)  # @line L5
            for r, b in ex_r.get(a, ()):
                add_edge(r, x, b)  # @line L6
            for r, w in list(self.pred[x]):
                for b in ex_l.get((r, a), ()):
                    add(w, b)  # @line L7
                if a == BOTN:
                    add(w, BOTN)  # @line L7

    def subsumes(self, a: str, b: str) -> bool:
        """True when the name a is subsumed by the name b (or b is top)."""
        if b == TOPN:
            return True
        return b in self.S[a] or BOTN in self.S[a]  # @line L11

    def unsatisfiable(self, a: str) -> bool:
        return BOTN in self.S[a]

    def canonical_model(self) -> Optional[Interpretation]:
        """The model built from S and R: one element for each name X without bottom in S(X), the
        names of S(X) hold at it, and the edges are those of R. None if the TBox has no model."""
        if BOTN in self.S[TOPN]:
            return None
        live = [x for x in self.names if BOTN not in self.S[x]]
        ids = {x: k for k, x in enumerate(live)}
        conc: dict[str, set] = {}
        for x in live:
            for a in self.S[x]:
                if a not in (TOPN, BOTN):
                    conc.setdefault(a, set()).add(ids[x])
        roles = {r: {(ids[x], ids[y]) for x, y in pairs if x in ids and y in ids} for r, pairs in self.R.items()}
        return Interpretation(list(range(len(live))), conc, roles)

    def element(self, a: str) -> int:
        """The element of the canonical model for the name a."""
        live = [x for x in self.names if BOTN not in self.S[x]]
        return live.index(a)


def complete(tbox: Sequence[GCI]) -> Completion:
    """Normalize the TBox and saturate it. Every concept name of the TBox gets a set S."""
    cn, _ = names([c for gci in tbox for c in gci])
    return Completion(normalize(tbox), cn)


def classify(tbox: Sequence[GCI]) -> dict[str, set[str]]:
    """For each concept name A of the TBox, the set of concept names B of the TBox with A subsumed by B.
    An unsatisfiable name is subsumed by every name."""
    cn, _ = names([c for gci in tbox for c in gci])
    comp = Completion(normalize(tbox), cn)
    return {a: {b for b in cn if comp.subsumes(a, b)} for a in cn}


def subsumes(tbox: Sequence[GCI], c: Concept, d: Concept) -> bool:
    """True when c is subsumed by d with respect to the TBox, for EL concepts c and d.
    Uses fresh names Q and P with Q subsumed by c and d subsumed by P."""
    q, p = ("atom", "_Q"), ("atom", "_P")
    comp = complete(list(tbox) + [(q, c), (d, p)])
    return comp.subsumes("_Q", "_P")
