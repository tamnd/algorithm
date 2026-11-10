# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-tree-clocks/. The authors are listed in prov/MXR7AF.jsonl.

"""Interval tree clocks (Almeida, Baquero and Fonte 2008).

A stamp is a pair (id, event). An id is 0, 1 or a pair (l, r) of ids; it
stands for a subset of the unit interval: 1 is all of it, 0 is none of it,
and (l, r) is l on the left half and r on the right half. An event tree is
an integer n or a triple (n, l, r); it stands for a function on the unit
interval: n is constant, and (n, l, r) is n plus l on the left half and n
plus r on the right half. Operations: fork, join, event and peek. Costs are
linear in the sizes of the trees involved. Recursion depth is the tree depth.
"""

import random

Id = int | tuple
Ev = int | tuple
Stamp = tuple[Id, Ev]

GROW_PENALTY = 1000  # the large constant N of grow: expanding a leaf costs more than any path


# ---- ids ----

def norm_id(i: Id) -> Id:
    """(0, 0) -> 0 and (1, 1) -> 1, assuming normal children."""
    if i == (0, 0):
        return 0
    if i == (1, 1):
        return 1
    return i


def split(i: Id) -> tuple[Id, Id]:
    """Split an id into two disjoint ids whose union is i."""
    if i == 0:
        return (0, 0)
    if i == 1:
        return ((1, 0), (0, 1))
    l, r = i
    if l == 0:
        r1, r2 = split(r)
        return ((0, r1), (0, r2))
    if r == 0:
        l1, l2 = split(l)
        return ((l1, 0), (l2, 0))
    return ((l, 0), (0, r))


def sum_id(i1: Id, i2: Id) -> Id:
    """The union of two disjoint ids."""
    if i1 == 0:
        return i2
    if i2 == 0:
        return i1
    if i1 == 1 or i2 == 1:
        raise ValueError("ids overlap")
    return norm_id((sum_id(i1[0], i2[0]), sum_id(i1[1], i2[1])))


# ---- event trees ----

def ev_min(e: Ev) -> int:
    if isinstance(e, int):
        return e
    return e[0] + min(ev_min(e[1]), ev_min(e[2]))


def ev_max(e: Ev) -> int:
    if isinstance(e, int):
        return e
    return e[0] + max(ev_max(e[1]), ev_max(e[2]))


def lift(e: Ev, m: int) -> Ev:
    return e + m if isinstance(e, int) else (e[0] + m, e[1], e[2])


def sink(e: Ev, m: int) -> Ev:
    return e - m if isinstance(e, int) else (e[0] - m, e[1], e[2])


def norm_ev(e: Ev) -> Ev:
    """Normalize the root of an event tree whose children are normal."""
    if isinstance(e, int):
        return e
    n, l, r = e
    if isinstance(l, int) and isinstance(r, int) and l == r:
        return n + l
    m = min(ev_min(l), ev_min(r))
    return (n + m, sink(l, m), sink(r, m))


def leq(e1: Ev, e2: Ev) -> bool:
    """The function of e1 is at most the function of e2 everywhere."""
    if isinstance(e1, int):
        return e1 <= (e2 if isinstance(e2, int) else e2[0])  # @line L6
    n1, l1, r1 = e1
    if isinstance(e2, int):
        return n1 <= e2 and leq(lift(l1, n1), e2) and leq(lift(r1, n1), e2)  # @line L7
    n2, l2, r2 = e2
    return n1 <= n2 and leq(lift(l1, n1), lift(l2, n2)) and leq(lift(r1, n1), lift(r2, n2))  # @line L8


def join_ev(e1: Ev, e2: Ev) -> Ev:
    """The pointwise maximum of two event trees, normalized."""
    if isinstance(e1, int) and isinstance(e2, int):
        return max(e1, e2)
    if isinstance(e1, int):
        e1 = (e1, 0, 0)
    if isinstance(e2, int):
        e2 = (e2, 0, 0)
    if e1[0] > e2[0]:
        e1, e2 = e2, e1
    n1, l1, r1 = e1
    n2, l2, r2 = e2
    d = n2 - n1
    return norm_ev((n1, join_ev(l1, lift(l2, d)), join_ev(r1, lift(r2, d))))


def fill(i: Id, e: Ev) -> Ev:
    """Raise e inside the region of i as far as possible without inventing a new value."""
    if i == 0:
        return e
    if i == 1:
        return ev_max(e)
    if isinstance(e, int):
        return e
    il, ir = i
    n, el, er = e
    if il == 1:
        er2 = fill(ir, er)
        return norm_ev((n, max(ev_max(el), ev_min(er2)), er2))
    if ir == 1:
        el2 = fill(il, el)
        return norm_ev((n, el2, max(ev_max(er), ev_min(el2))))
    return norm_ev((n, fill(il, el), fill(ir, er)))


def grow(i: Id, e: Ev) -> tuple[Ev, int]:
    """Add 1 inside the region of i at the cheapest place. Return (new tree, cost)."""
    if i == 1 and isinstance(e, int):
        return (e + 1, 0)
    if isinstance(e, int):
        e2, c = grow(i, (e, 0, 0))
        return (e2, c + GROW_PENALTY)
    il, ir = i
    n, el, er = e
    if il == 0:
        er2, cr = grow(ir, er)
        return ((n, el, er2), cr + 1)
    if ir == 0:
        el2, cl = grow(il, el)
        return ((n, el2, er), cl + 1)
    el2, cl = grow(il, el)
    er2, cr = grow(ir, er)
    if cl < cr:
        return ((n, el2, er), cl + 1)
    return ((n, el, er2), cr + 1)


# ---- stamps ----

class IntervalTreeClock:
    """A stamp (id, event) with the four operations of the fork-event-join model."""

    def __init__(self, i: Id = 1, e: Ev = 0) -> None:
        """The seed stamp is (1, 0)."""
        self.i = i
        self.e = e

    def fork(self) -> "IntervalTreeClock":
        """Split the id; self keeps one half, the result gets the other. The event is shared."""
        i1, i2 = split(self.i)  # @line L1
        self.i = i1
        return IntervalTreeClock(i2, self.e)

    def join(self, other: "IntervalTreeClock") -> None:
        """Merge other into self: union of ids, maximum of events."""
        self.i = sum_id(self.i, other.i)  # @line L2
        self.e = join_ev(self.e, other.e)

    def event(self) -> None:
        """Record a new event. Precondition: the id is not 0."""
        if self.i == 0:
            raise ValueError("an anonymous stamp cannot record events")
        f = fill(self.i, self.e)  # @line L3
        if f != self.e:  # @line L4
            self.e = f
        else:
            self.e = norm_ev_full(grow(self.i, self.e)[0])  # @line L5

    def peek(self) -> "IntervalTreeClock":
        """An anonymous copy (0, event), as carried by a message."""
        return IntervalTreeClock(0, self.e)

    def leq(self, other: "IntervalTreeClock") -> bool:
        return leq(self.e, other.e)


# ---- helpers for tests ----

def norm_ev_full(e: Ev) -> Ev:
    """Normalize an arbitrary event tree bottom up."""
    if isinstance(e, int):
        return e
    return norm_ev((e[0], norm_ev_full(e[1]), norm_ev_full(e[2])))


def norm_id_full(i: Id) -> Id:
    """Normalize an arbitrary id tree bottom up."""
    if isinstance(i, int):
        return i
    return norm_id((norm_id_full(i[0]), norm_id_full(i[1])))


def depth(t: int | tuple) -> int:
    if isinstance(t, int):
        return 0
    return 1 + max(depth(c) for c in t[-2:])


def id_cells(i: Id, d: int) -> list[int]:
    """The id as a 0/1 list over 2^d equal cells of the unit interval. Precondition: depth(i) <= d."""
    if isinstance(i, int):
        return [i] * (1 << d)
    return id_cells(i[0], d - 1) + id_cells(i[1], d - 1)


def ev_cells(e: Ev, d: int) -> list[int]:
    """The event function as a list over 2^d equal cells. Precondition: depth(e) <= d."""
    if isinstance(e, int):
        return [e] * (1 << d)
    return [e[0] + x for x in ev_cells(e[1], d - 1) + ev_cells(e[2], d - 1)]


def is_normal_ev(e: Ev) -> bool:
    if isinstance(e, int):
        return e >= 0
    n, l, r = e
    if not (is_normal_ev(l) and is_normal_ev(r)):
        return False
    if isinstance(l, int) and isinstance(r, int) and l == r:
        return False
    return n >= 0 and min(ev_min(l), ev_min(r)) == 0


def is_normal_id(i: Id) -> bool:
    if isinstance(i, int):
        return i in (0, 1)
    return is_normal_id(i[0]) and is_normal_id(i[1]) and i not in ((0, 0), (1, 1))


def random_event_tree(rng: random.Random, d: int) -> Ev:
    """A random event tree of depth at most d, not necessarily normal."""
    if d == 0 or rng.random() < 0.4:
        return rng.randint(0, 3)
    return (rng.randint(0, 3), random_event_tree(rng, d - 1), random_event_tree(rng, d - 1))
