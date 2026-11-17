# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-view-maintenance/. The authors are listed in prov/V5APR5.jsonl.
"""Incremental maintenance of a nonrecursive view by delta rules, with the
counting algorithm of Gupta, Mumick and Subrahmanian (1993).

Relations are bags with signed multiplicities: a Counter that maps a tuple
(a sorted tuple of (attribute, value) pairs) to an integer. A database is a
dict from relation names to such Counters, and an update is a dict of
signed deltas (+1 inserts a copy, -1 deletes one).

Expressions: Rel(name), Select(pred, e), Project(attrs, e), Join(e1, e2)
(natural join on the shared attributes) and Union(e1, e2) (bag sum).
The delta rules, for the old database D and the update dD:
  d(R)          = dD[R]
  d(sigma_p E)  = sigma_p(dE)
  d(pi_A E)     = pi_A(dE)
  d(E1 + E2)    = dE1 + dE2
  d(E1 join E2) = dE1 join E2  +  E1 join dE2  +  dE1 join dE2   (E1, E2 old)
so that E(D + dD) = E(D) + dE exactly, multiplicities included.

The counting view stores, for each tuple of the view, its number of
derivations (its bag multiplicity). The set view holds the tuples with a
positive count: a deletion removes a tuple only when its count drops to 0.
"""

from collections import Counter
from dataclasses import dataclass
from typing import Callable, Dict, FrozenSet, Tuple, Union as U

Row = Tuple[Tuple[str, object], ...]
Bag = Counter
Db = Dict[str, Bag]


def row(**kv: object) -> Row:
    return tuple(sorted(kv.items()))


@dataclass(frozen=True)
class Rel:
    name: str


@dataclass(frozen=True)
class Select:
    pred: Callable[[dict], bool]
    child: "Expr"


@dataclass(frozen=True)
class Project:
    attrs: FrozenSet[str]
    child: "Expr"


@dataclass(frozen=True)
class Join:
    left: "Expr"
    right: "Expr"


@dataclass(frozen=True)
class Union:
    left: "Expr"
    right: "Expr"


Expr = U[Rel, Select, Project, Join, Union]


def bag_add(x: Bag, y: Bag) -> Bag:
    out = Counter(x)
    for t, m in y.items():
        out[t] += m
    return Counter({t: m for t, m in out.items() if m != 0})


def select(pred: Callable[[dict], bool], b: Bag) -> Bag:
    return Counter({t: m for t, m in b.items() if pred(dict(t))})


def project(attrs: FrozenSet[str], b: Bag) -> Bag:
    out: Bag = Counter()
    for t, m in b.items():
        out[tuple((a, v) for a, v in t if a in attrs)] += m
    return Counter({t: m for t, m in out.items() if m != 0})


def join(x: Bag, y: Bag) -> Bag:
    """Natural join of signed bags: multiplicities multiply. Hash on the
    shared attributes of each pair of tuples' schemas."""
    out: Bag = Counter()
    if not x or not y:
        return out
    ax = {a for t in x for a, _ in t}
    ay = {a for t in y for a, _ in t}
    shared = sorted(ax & ay)
    index: Dict[tuple, list] = {}
    for t, m in y.items():
        d = dict(t)
        index.setdefault(tuple(d[a] for a in shared), []).append((d, m))
    for t, m in x.items():
        d = dict(t)
        for d2, m2 in index.get(tuple(d[a] for a in shared), []):
            out[tuple(sorted({**d, **d2}.items()))] += m * m2
    return Counter({t: m for t, m in out.items() if m != 0})


def evaluate(e: Expr, db: Db) -> Bag:
    if isinstance(e, Rel):
        return Counter({t: m for t, m in db.get(e.name, Counter()).items() if m != 0})
    if isinstance(e, Select):
        return select(e.pred, evaluate(e.child, db))
    if isinstance(e, Project):
        return project(e.attrs, evaluate(e.child, db))
    if isinstance(e, Join):
        return join(evaluate(e.left, db), evaluate(e.right, db))
    return bag_add(evaluate(e.left, db), evaluate(e.right, db))


def relations(e: Expr) -> FrozenSet[str]:
    if isinstance(e, Rel):
        return frozenset([e.name])
    if isinstance(e, (Select, Project)):
        return relations(e.child)
    return relations(e.left) | relations(e.right)


def delta(e: Expr, db: Db, d: Db) -> Bag:
    """dE such that E(db + d) = E(db) + dE. Old subexpressions are evaluated
    only when the other side of a join has a nonzero delta."""
    if not any(d.get(r) for r in relations(e)):
        return Counter()
    if isinstance(e, Rel):  # @line L1
        return Counter({t: m for t, m in d.get(e.name, Counter()).items() if m != 0})
    if isinstance(e, Select):  # @line L2
        return select(e.pred, delta(e.child, db, d))
    if isinstance(e, Project):  # @line L3
        return project(e.attrs, delta(e.child, db, d))
    if isinstance(e, Union):  # @line L4
        return bag_add(delta(e.left, db, d), delta(e.right, db, d))
    d1, d2 = delta(e.left, db, d), delta(e.right, db, d)  # @line L5
    out: Bag = Counter()
    if d1:
        out = bag_add(out, join(d1, evaluate(e.right, db)))  # @line L6
    if d2:
        out = bag_add(out, join(evaluate(e.left, db), d2))
    if d1 and d2:
        out = bag_add(out, join(d1, d2))
    return out


def apply_update(db: Db, d: Db) -> Db:
    out = {k: Counter(v) for k, v in db.items()}
    for name, dr in d.items():
        out[name] = bag_add(out.get(name, Counter()), dr)
    return out


class CountingView:
    """A materialized view under set semantics, with a derivation count per
    tuple (the counting algorithm)."""

    def __init__(self, e: Expr, db: Db) -> None:
        self.e = e
        self.db = {k: Counter(v) for k, v in db.items()}
        self.count: Bag = evaluate(e, self.db)

    def rows(self) -> set:
        return {t for t, c in self.count.items() if c > 0}

    def maintain(self, d: Db) -> Tuple[set, set]:
        """Apply the update d; return (tuples inserted into the set view,
        tuples deleted from it)."""
        dv = delta(self.e, self.db, d)  # @line L7
        inserted, deleted = set(), set()
        for t, m in dv.items():  # @line L8
            old = self.count.get(t, 0)
            new = old + m  # @line L9
            if old <= 0 < new:  # @line L10
                inserted.add(t)
            elif new <= 0 < old:
                deleted.add(t)
            if new == 0:  # @line L11
                self.count.pop(t, None)
            else:
                self.count[t] = new
        self.db = apply_update(self.db, d)  # @line L12
        return inserted, deleted
