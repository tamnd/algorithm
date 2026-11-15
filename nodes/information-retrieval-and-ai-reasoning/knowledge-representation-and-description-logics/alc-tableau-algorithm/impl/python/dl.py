# SPDX-License-Identifier: MIT
# Shared helper of the description logic pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""ALC concepts as syntax trees, negation normal form, and evaluation in a finite interpretation.

A concept is a tuple:
    TOP = ("top",)            BOTTOM = ("bottom",)
    ("atom", "A")             ("not", C)
    ("and", C, D)             ("or", C, D)
    ("some", "r", C)          ("all", "r", C)
A TBox is a sequence of general concept inclusions (C, D), read C is subsumed by D.
An interpretation has a nonempty finite domain, a set for each concept name and a set of pairs
for each role name. Names that an interpretation does not list are empty.
This file holds only the syntax and the semantics. No reasoning algorithm goes here.
"""

from itertools import product
from typing import Iterable, Iterator, Sequence

Concept = tuple
GCI = tuple[Concept, Concept]

TOP: Concept = ("top",)
BOTTOM: Concept = ("bottom",)


def atom(name: str) -> Concept:
    return ("atom", name)


def neg(c: Concept) -> Concept:
    return ("not", c)


def conj(*cs: Concept) -> Concept:
    """The conjunction of the arguments, nested to the right. conj() is TOP."""
    if not cs:
        return TOP
    out = cs[-1]
    for c in reversed(cs[:-1]):
        out = ("and", c, out)
    return out


def disj(*cs: Concept) -> Concept:
    """The disjunction of the arguments, nested to the right. disj() is BOTTOM."""
    if not cs:
        return BOTTOM
    out = cs[-1]
    for c in reversed(cs[:-1]):
        out = ("or", c, out)
    return out


def exists(r: str, c: Concept) -> Concept:
    return ("some", r, c)


def forall(r: str, c: Concept) -> Concept:
    return ("all", r, c)


def nnf(c: Concept) -> Concept:
    """Negation normal form: an equivalent concept with negation only in front of concept names."""
    op = c[0]
    if op in ("top", "bottom", "atom"):
        return c
    if op in ("and", "or"):
        return (op, nnf(c[1]), nnf(c[2]))
    if op in ("some", "all"):
        return (op, c[1], nnf(c[2]))
    d = c[1]  # op == "not"
    dop = d[0]
    if dop == "top":
        return BOTTOM
    if dop == "bottom":
        return TOP
    if dop == "atom":
        return c
    if dop == "not":
        return nnf(d[1])
    if dop == "and":
        return ("or", nnf(neg(d[1])), nnf(neg(d[2])))
    if dop == "or":
        return ("and", nnf(neg(d[1])), nnf(neg(d[2])))
    if dop == "some":
        return ("all", d[1], nnf(neg(d[2])))
    return ("some", d[1], nnf(neg(d[2])))  # dop == "all"


def is_nnf(c: Concept) -> bool:
    op = c[0]
    if op in ("top", "bottom", "atom"):
        return True
    if op == "not":
        return c[1][0] == "atom"
    if op in ("and", "or"):
        return is_nnf(c[1]) and is_nnf(c[2])
    return is_nnf(c[2])


def subconcepts(c: Concept) -> set[Concept]:
    """All subconcepts of c, c included."""
    out = {c}
    op = c[0]
    if op == "not":
        out |= subconcepts(c[1])
    elif op in ("and", "or"):
        out |= subconcepts(c[1]) | subconcepts(c[2])
    elif op in ("some", "all"):
        out |= subconcepts(c[2])
    return out


def size(c: Concept) -> int:
    """The number of constructors and names in c."""
    op = c[0]
    if op in ("top", "bottom", "atom"):
        return 1
    if op == "not":
        return 1 + size(c[1])
    if op in ("and", "or"):
        return 1 + size(c[1]) + size(c[2])
    return 2 + size(c[2])


def role_depth(c: Concept) -> int:
    """The largest number of nested role restrictions in c."""
    op = c[0]
    if op in ("top", "bottom", "atom"):
        return 0
    if op == "not":
        return role_depth(c[1])
    if op in ("and", "or"):
        return max(role_depth(c[1]), role_depth(c[2]))
    return 1 + role_depth(c[2])


def names(cs: Iterable[Concept]) -> tuple[list[str], list[str]]:
    """The sorted concept names and role names that occur in the given concepts."""
    cn: set[str] = set()
    rn: set[str] = set()
    for c in cs:
        for s in subconcepts(c):
            if s[0] == "atom":
                cn.add(s[1])
            elif s[0] in ("some", "all"):
                rn.add(s[1])
    return sorted(cn), sorted(rn)


def show(c: Concept) -> str:
    """The concept in the usual notation, with full parentheses."""
    op = c[0]
    if op == "top":
        return "⊤"
    if op == "bottom":
        return "⊥"
    if op == "atom":
        return c[1]
    if op == "not":
        return "¬" + show(c[1])
    if op == "and":
        return "(" + show(c[1]) + " ⊓ " + show(c[2]) + ")"
    if op == "or":
        return "(" + show(c[1]) + " ⊔ " + show(c[2]) + ")"
    q = "∃" if op == "some" else "∀"
    return q + c[1] + "." + show(c[2])


class Interpretation:
    """A finite interpretation. domain is a nonempty list; concepts maps a name to a set of elements;
    roles maps a name to a set of pairs of elements."""

    def __init__(self, domain: Sequence, concepts: dict, roles: dict) -> None:
        if not domain:
            raise ValueError("the domain of an interpretation is not empty")
        self.domain = list(domain)
        self.concepts = {a: frozenset(s) for a, s in concepts.items()}
        self.roles = {r: frozenset(p) for r, p in roles.items()}
        self._succ: dict[str, dict] = {}

    def successors(self, r: str, x) -> list:
        if r not in self._succ:
            m: dict = {y: [] for y in self.domain}
            for (u, v) in self.roles.get(r, ()):
                m[u].append(v)
            self._succ[r] = m
        return self._succ[r][x]

    def __repr__(self) -> str:
        return f"Interpretation({self.domain!r}, {self.concepts!r}, {self.roles!r})"


def evaluate(c: Concept, i: Interpretation) -> frozenset:
    """The extension of c in the interpretation i, by the semantics of ALC."""
    op = c[0]
    if op == "top":
        return frozenset(i.domain)
    if op == "bottom":
        return frozenset()
    if op == "atom":
        return i.concepts.get(c[1], frozenset())
    if op == "not":
        return frozenset(i.domain) - evaluate(c[1], i)
    if op == "and":
        return evaluate(c[1], i) & evaluate(c[2], i)
    if op == "or":
        return evaluate(c[1], i) | evaluate(c[2], i)
    ext = evaluate(c[2], i)
    if op == "some":
        return frozenset(x for x in i.domain if any(y in ext for y in i.successors(c[1], x)))
    return frozenset(x for x in i.domain if all(y in ext for y in i.successors(c[1], x)))


def is_model_of_tbox(i: Interpretation, tbox: Iterable[GCI]) -> bool:
    """True when i satisfies every inclusion C subsumed by D of the TBox."""
    return all(evaluate(c, i) <= evaluate(d, i) for c, d in tbox)


def interpretations(concept_names: Sequence[str], role_names: Sequence[str], max_size: int) -> Iterator[Interpretation]:
    """Every interpretation of the given names over the domains [0], [0, 1], ..., [0, ..., max_size - 1].
    There are sum over n of 2^(n * |concept_names| + n^2 * |role_names|) of them."""
    for n in range(1, max_size + 1):
        dom = list(range(n))
        pairs = [(x, y) for x in dom for y in dom]
        cbits = list(product((False, True), repeat=n * len(concept_names)))
        rbits = list(product((False, True), repeat=n * n * len(role_names)))
        for rb in rbits:
            roles = {r: {pairs[k] for k in range(n * n) if rb[j * n * n + k]} for j, r in enumerate(role_names)}
            for cb in cbits:
                conc = {a: {x for x in dom if cb[j * n + x]} for j, a in enumerate(concept_names)}
                yield Interpretation(dom, conc, roles)
