# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structural-subsumption/. The authors are listed in prov/DQ8M2F.jsonl.
"""Structural subsumption for FL-: bring both concepts to a normal form, then compare the parts.

FL- has concept names, top, conjunction, value restriction (all r.C) and unqualified existential
restriction (some r.top). Concepts are the tuples of dl.py. The normal form of a concept is a tree:
each node holds a set of concept names, a set of roles r with some r.top, and at most one child for
each role r, which holds the merged fillers of all value restrictions on r. Children whose subtree
is empty are removed, because all r.top is equivalent to top.
"""

from typing import Optional

from dl import TOP, Concept, Interpretation


class NotFLMinus(ValueError):
    """Raised for a concept that is not in FL-."""


class Normal:
    """A node of the normal form tree."""

    __slots__ = ("names", "roles", "child")

    def __init__(self) -> None:
        self.names: set[str] = set()  # N: concept names that hold here
        self.roles: set[str] = set()  # E: roles r with some r.top here
        self.child: dict[str, "Normal"] = {}  # V: for role r, the merged value restriction on r

    def is_empty(self) -> bool:
        return not self.names and not self.roles and not self.child

    def show(self) -> str:
        parts = sorted(self.names) + ["∃" + r for r in sorted(self.roles)]
        parts += ["∀" + r + "." + self.child[r].show() for r in sorted(self.child)]
        if not parts:
            return "⊤"
        return parts[0] if len(parts) == 1 else "(" + " ⊓ ".join(parts) + ")"


def is_fl_minus(c: Concept) -> bool:
    op = c[0]
    if op in ("top", "atom"):
        return True
    if op == "and":
        return is_fl_minus(c[1]) and is_fl_minus(c[2])
    if op == "some":
        return c[2] == TOP
    if op == "all":
        return is_fl_minus(c[2])
    return False


def _insert(x: Normal, c: Concept) -> None:
    op = c[0]
    if op == "atom":
        x.names.add(c[1])  # @line L5
    elif op == "some":
        x.roles.add(c[1])  # @line L6
    elif op == "and":
        _insert(x, c[1])  # @line L7
        _insert(x, c[2])
    elif op == "all":
        if c[1] not in x.child:  # @line L8
            x.child[c[1]] = Normal()
        _insert(x.child[c[1]], c[2])


def _prune(x: Normal) -> None:
    for r in list(x.child):
        _prune(x.child[r])
        if x.child[r].is_empty():
            del x.child[r]


def normalize(c: Concept) -> Normal:
    """The normal form of an FL- concept."""
    if not is_fl_minus(c):
        raise NotFLMinus(repr(c))
    root = Normal()  # @line L1
    _insert(root, c)  # @line L2
    _prune(root)  # @line L3
    return root  # @line L4


def subsumes_normal(c: Normal, d: Normal) -> bool:
    """SUBSUMES(c, d): True when the concept with normal form c is subsumed by the one with normal form d."""
    if not d.names <= c.names or not d.roles <= c.roles:  # @line L9
        return False
    for r, dr in d.child.items():  # @line L10
        if r not in c.child or not subsumes_normal(c.child[r], dr):  # @line L11
            return False
    return True  # @line L12


def subsumes(c: Concept, d: Concept) -> bool:
    """True when c is subsumed by d (every model puts c inside d). Both must be FL- concepts."""
    return subsumes_normal(normalize(c), normalize(d))


class _Builder:
    def __init__(self) -> None:
        self.n = 0
        self.conc: dict[str, set] = {}
        self.roles: dict[str, set] = {}

    def new(self, x: Normal) -> int:
        e = self.n
        self.n += 1
        for a in x.names:
            self.conc.setdefault(a, set()).add(e)
        return e

    def edge(self, r: str, u: int, v: int) -> None:
        self.roles.setdefault(r, set()).add((u, v))

    def tree(self, x: Normal) -> int:
        """An element in the concept of x: one successor for each role of x.roles."""
        e = self.new(x)
        for r in sorted(x.roles):
            self.edge(r, e, self.tree(x.child.get(r, Normal())))
        return e

    def counter(self, c: Normal, d: Normal) -> int:
        """An element in the concept of c but not in the concept of d. Needs: c is not subsumed by d."""
        if not d.names <= c.names or not d.roles <= c.roles:
            return self.tree(c)
        r = next(r for r in sorted(d.child) if not subsumes_normal(c.child.get(r, Normal()), d.child[r]))
        e = self.new(c)
        for s in sorted(c.roles):
            if s != r:
                self.edge(s, e, self.tree(c.child.get(s, Normal())))
        # The one r-successor is in the concept of c.child[r] but not in the one of d.child[r].
        self.edge(r, e, self.counter(c.child.get(r, Normal()), d.child[r]))
        return e


def counter_model(c: Concept, d: Concept) -> Optional[Interpretation]:
    """None when c is subsumed by d. Otherwise a finite tree model where element 0 is in c and not in d."""
    nc, nd = normalize(c), normalize(d)
    if subsumes_normal(nc, nd):
        return None
    b = _Builder()
    b.counter(nc, nd)
    return Interpretation(list(range(b.n)), b.conc, b.roles)
