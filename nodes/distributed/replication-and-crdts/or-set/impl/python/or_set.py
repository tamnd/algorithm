# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/or-set/. The authors are listed in prov/DDH0TH.jsonl.

"""Two observed-remove sets.

ORSet is the op-based OR-Set of Shapiro et al. 2011 (RR-7506 Specification 15).
Each add makes a unique tag. A remove carries the tags of the element that
the source has observed, and every replica deletes exactly those tags. An add
that the remove did not observe keeps its tag, so a concurrent add wins.
Delivery must be causal, so that a remove arrives after the adds it names.

OptORSet is the optimized state-based OR-Set of Bieniusa et al. 2012
(arXiv 1210.3368). It keeps no tombstones. A tag is a dot (i, c), the c-th
add of replica i, and a version vector V records which dots a replica has
seen. In a merge, a dot that is missing on one side was removed there if that
side's vector covers it, and was not yet seen there otherwise.
"""

import itertools
from collections.abc import Hashable

Tag = tuple[int, int]  # (replica id, counter)


class ORSet:
    """One replica of the op-based OR-Set."""

    def __init__(self, rid: int) -> None:
        self.rid = rid
        self.counter = itertools.count(1)
        self.s: set[tuple[Hashable, Tag]] = set()  # @line L1

    def lookup(self, e: Hashable) -> bool:
        return any(x == e for x, _ in self.s)  # @line L2

    def prepare_add(self, e: Hashable) -> tuple[str, Hashable, frozenset[Tag]]:
        tag = (self.rid, next(self.counter))  # @line L3
        return ("add", e, frozenset([tag]))

    def prepare_remove(self, e: Hashable) -> tuple[str, Hashable, frozenset[Tag]]:
        if not self.lookup(e):
            raise ValueError("remove needs the element in the set at the source")
        r = frozenset(t for x, t in self.s if x == e)  # @line L4
        return ("rem", e, r)

    def effect(self, op: tuple[str, Hashable, frozenset[Tag]]) -> None:
        kind, e, tags = op
        if kind == "add":
            (t,) = tags
            self.s.add((e, t))  # @line L5
        else:
            self.s -= {(e, t) for t in tags}  # @line L6

    def elements(self) -> frozenset:
        return frozenset(x for x, _ in self.s)

    def check_invariant(self) -> None:
        tags = [t for _, t in self.s]
        assert len(tags) == len(set(tags)), "a tag belongs to one add only"


class OptORSet:
    """One replica of the optimized OR-Set without tombstones, n replicas, id i."""

    def __init__(self, n: int, i: int) -> None:
        self.n, self.me = n, i
        self.e: set[tuple[Hashable, int, int]] = set()  # (element, counter, replica)
        self.v: list[int] = [0] * n

    def lookup(self, x: Hashable) -> bool:
        return any(y == x for y, _, _ in self.e)

    def add(self, x: Hashable) -> None:
        self.v[self.me] += 1
        c = self.v[self.me]
        self.e = {t for t in self.e if not (t[0] == x and t[2] == self.me)}
        self.e.add((x, c, self.me))

    def remove(self, x: Hashable) -> None:
        self.e = {t for t in self.e if t[0] != x}

    def merge(self, other: "OptORSet | tuple[frozenset, tuple[int, ...]]") -> None:
        be, bv = (other.e, other.v) if isinstance(other, OptORSet) else other
        m = self.e & set(be)
        m |= {t for t in self.e - set(be) if t[1] > bv[t[2]]}  # b has not seen it yet
        m |= {t for t in set(be) - self.e if t[1] > self.v[t[2]]}  # we have not seen it yet
        latest: dict[tuple[Hashable, int], int] = {}
        for x, c, i in m:
            latest[(x, i)] = max(c, latest.get((x, i), 0))
        self.e = {(x, c, i) for x, c, i in m if latest[(x, i)] == c}
        self.v = [max(a, b) for a, b in zip(self.v, bv)]

    def state(self) -> tuple[frozenset, tuple[int, ...]]:
        return (frozenset(self.e), tuple(self.v))

    def elements(self) -> frozenset:
        return frozenset(x for x, _, _ in self.e)

    def check_invariant(self) -> None:
        for x, c, i in self.e:
            assert 1 <= c <= self.v[i]
        keys = [(x, i) for x, _, i in self.e]
        assert len(keys) == len(set(keys)), "at most one dot per element and replica"
