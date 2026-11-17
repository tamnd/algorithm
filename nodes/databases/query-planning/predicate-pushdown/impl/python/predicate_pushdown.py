# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predicate-pushdown/. The authors are listed in prov/75V2SP.jsonl.
"""Predicate pushdown on relational algebra trees, with bag semantics.

A tree is one of
  Rel(name, schema)            a stored relation
  Sel(preds, child)            selection by a conjunction of predicates
  Proj(attrs, child)           projection that keeps duplicates
  Join(preds, left, right)     inner join (no predicates: cross product)
  LeftJoin(preds, left, right) left outer join; right is null-supplying
A row is a dict from attribute name to value; attribute names are unique
across relations. A padded value is None, and a predicate that reads None is
false (the SQL rule that WHERE drops unknown).

push_down(tree) returns an equivalent tree in which each predicate sits as low
as the algebraic laws allow. The cost is O(size of tree * number of predicates).
"""

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, FrozenSet, List, Tuple, Union

Row = Dict[str, Any]


@dataclass(frozen=True)
class Pred:
    attrs: FrozenSet[str]
    fn: Callable[[Row], bool] = field(compare=False)
    name: str = ""

    def __call__(self, row: Row) -> bool:
        if any(row[a] is None for a in self.attrs):
            return False
        return bool(self.fn(row))


@dataclass(frozen=True)
class Rel:
    name: str
    schema: Tuple[str, ...]


@dataclass(frozen=True)
class Sel:
    preds: Tuple[Pred, ...]
    child: "Tree"


@dataclass(frozen=True)
class Proj:
    attrs: Tuple[str, ...]
    child: "Tree"


@dataclass(frozen=True)
class Join:
    preds: Tuple[Pred, ...]
    left: "Tree"
    right: "Tree"


@dataclass(frozen=True)
class LeftJoin:
    preds: Tuple[Pred, ...]
    left: "Tree"
    right: "Tree"


Tree = Union[Rel, Sel, Proj, Join, LeftJoin]


def schema(t: Tree) -> FrozenSet[str]:
    if isinstance(t, Rel):
        return frozenset(t.schema)
    if isinstance(t, Sel):
        return schema(t.child)
    if isinstance(t, Proj):
        return frozenset(t.attrs)
    return schema(t.left) | schema(t.right)


def _wrap(preds: List[Pred], t: Tree) -> Tree:
    return Sel(tuple(preds), t) if preds else t


def push_down(t: Tree, preds: Tuple[Pred, ...] = ()) -> Tree:
    """Place the predicates `preds` (which come from above t) and those
    inside t as low as possible. Returns an equivalent tree."""
    if isinstance(t, Rel):  # @line L1
        return _wrap(list(preds), t)  # @line L2
    if isinstance(t, Sel):  # @line L3
        return push_down(t.child, preds + t.preds)  # @line L4
    if isinstance(t, Proj):  # @line L5
        # Each predicate above a projection reads only projected attributes.
        return Proj(t.attrs, push_down(t.child, preds))  # @line L6
    ls, rs = schema(t.left), schema(t.right)
    if isinstance(t, Join):  # @line L7
        all_preds = list(preds) + list(t.preds)
        lp = [p for p in all_preds if p.attrs <= ls]  # @line L8
        rp = [p for p in all_preds if p.attrs <= rs and not p.attrs <= ls]
        keep = [p for p in all_preds if not (p.attrs <= ls or p.attrs <= rs)]  # @line L9
        return Join(tuple(keep), push_down(t.left, tuple(lp)), push_down(t.right, tuple(rp)))  # @line L10
    # Left outer join: a WHERE predicate may go to the preserved (left) side
    # only; an ON predicate may go to the null-supplying (right) side only.
    above = [p for p in preds if not p.attrs <= ls]  # @line L11
    lp = [p for p in preds if p.attrs <= ls]
    rp = [p for p in t.preds if p.attrs <= rs and not p.attrs <= ls]
    on = [p for p in t.preds if not (p.attrs <= rs and not p.attrs <= ls)]
    inner = LeftJoin(tuple(on), push_down(t.left, tuple(lp)), push_down(t.right, tuple(rp)))
    return _wrap(above, inner)  # @line L12


def evaluate(t: Tree, db: Dict[str, List[Row]], stats: Counter = None) -> List[Row]:
    """Evaluate t on db. stats counts the rows that each join produces."""
    if stats is None:
        stats = Counter()
    if isinstance(t, Rel):
        return [dict(r) for r in db[t.name]]
    if isinstance(t, Sel):
        return [r for r in evaluate(t.child, db, stats) if all(p(r) for p in t.preds)]
    if isinstance(t, Proj):
        return [{a: r[a] for a in t.attrs} for r in evaluate(t.child, db, stats)]
    left, right = evaluate(t.left, db, stats), evaluate(t.right, db, stats)
    out = []
    pad = {a: None for a in schema(t.right)}
    for l in left:
        matched = False
        for r in right:
            row = {**l, **r}
            if all(p(row) for p in t.preds):
                out.append(row)
                matched = True
        if isinstance(t, LeftJoin) and not matched:
            out.append({**l, **pad})
    stats["join rows"] += len(out)
    return out


def bag(rows: List[Row]) -> Counter:
    return Counter(tuple(sorted(r.items())) for r in rows)
