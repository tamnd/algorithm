# SPDX-License-Identifier: MIT
# Test helper of the description logic pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small reference decision procedure for ALC concept satisfiability with a general TBox.

The tests use it as an independent oracle. It is the plain tableau: depth first, a label is a set
of concepts in negation normal form, every node gets the concept nnf(not C or D) of each inclusion
C subsumed by D, and a new node is not made when its label is a subset of the label of an ancestor
(subset blocking, which is sound for ALC). Disjunctions are split in a fixed order with no
heuristics, so the node count shows how much search the plain method does.
"""

from typing import Iterator, Sequence

from dl import BOTTOM, GCI, Concept, conj, disj, neg, nnf


class Counter:
    def __init__(self) -> None:
        self.nodes = 0  # labels that were completed and expanded
        self.branches = 0  # completions tried, clash-free or not


def _completions(s: frozenset, cnt: Counter) -> Iterator[frozenset]:
    lab: set = set()
    stack = list(s)
    while stack:
        c = stack.pop()
        if c in lab:
            continue
        lab.add(c)
        if c[0] == "and":
            stack.append(c[1])
            stack.append(c[2])
    cnt.branches += 1
    if BOTTOM in lab or any(c[0] == "not" and c[1] in lab for c in lab):
        return
    pending = sorted(repr(c) for c in lab if c[0] == "or" and c[1] not in lab and c[2] not in lab)
    if not pending:
        yield frozenset(lab)
        return
    c = next(c for c in lab if repr(c) == pending[0])
    yield from _completions(frozenset(lab | {c[1]}), cnt)
    yield from _completions(frozenset(lab | {c[2]}), cnt)


def _sat(label: frozenset, ancestors: tuple, tc: frozenset, cnt: Counter) -> bool:
    cnt.nodes += 1
    for lab in _completions(label, cnt):
        path = ancestors + (lab,)
        ok = True
        for c in sorted((c for c in lab if c[0] == "some"), key=repr):
            child = frozenset({c[2]} | {d[2] for d in lab if d[0] == "all" and d[1] == c[1]}) | tc
            if tc and any(child <= a for a in path):
                continue  # blocked: the ancestor's label serves as the successor
            if not _sat(child, path, tc, cnt):
                ok = False
                break
        if ok:
            return True
    return False


def satisfiable_count(c: Concept, tbox: Sequence[GCI] = ()) -> tuple[bool, Counter]:
    """Decide whether c is satisfiable with respect to the TBox; also return the work counter."""
    tc = frozenset(nnf(disj(neg(x), y)) for x, y in tbox)
    cnt = Counter()
    return _sat(frozenset({nnf(c)}) | tc, (), tc, cnt), cnt


def satisfiable(c: Concept, tbox: Sequence[GCI] = ()) -> bool:
    return satisfiable_count(c, tbox)[0]


def subsumes(c: Concept, d: Concept, tbox: Sequence[GCI] = ()) -> bool:
    """True when c is subsumed by d with respect to the TBox."""
    return not satisfiable(conj(c, neg(d)), tbox)
