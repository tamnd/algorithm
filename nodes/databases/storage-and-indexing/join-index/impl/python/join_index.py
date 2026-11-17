# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/join-index/. The authors are listed in prov/8DK147.jsonl.

"""Join index (Valduriez 1987) for the equi-join R.a = S.b.

The join index is the set of pairs (rid of r, rid of s) with r.a = s.b. It is
kept in two copies: one grouped by the rid of R and one by the rid of S, as
two B+ trees would keep it. Each relation also has an index from a join
value to the rids that hold it, which the updates use to find new pairs.

Record ids are given in insert order, and a deleted rid is not used again,
so the tuple with rid i lies on page i // per_page of its heap file.

The join with the index reads the pairs in rid-of-R order (ceil(P / q)
pages for P pairs and q pairs per page), fetches each page of R that holds a
matching tuple once, sorts the partial results on the rid of S in memory,
and fetches each page of S that holds a matching tuple once.
"""

from math import ceil
from typing import Optional

Row = tuple


class JoinIndex:
    """Join index of R and S on r[r_col] == s[s_col]."""

    def __init__(self, r_col: int, s_col: int, per_page: int = 4, pairs_per_page: int = 8) -> None:
        if per_page < 1 or pairs_per_page < 1:
            raise ValueError("page capacities must be at least 1")
        self.r_col, self.s_col = r_col, s_col
        self.per_page, self.pairs_per_page = per_page, pairs_per_page
        self.r: dict[int, Row] = {}
        self.s: dict[int, Row] = {}
        self._next_r = self._next_s = 0
        self.r_by_value: dict[object, set[int]] = {}
        self.s_by_value: dict[object, set[int]] = {}
        self.by_r: dict[int, set[int]] = {}
        self.by_s: dict[int, set[int]] = {}
        self.size = 0

    def _link(self, rid: int, sid: int) -> None:
        self.by_r.setdefault(rid, set()).add(sid)
        self.by_s.setdefault(sid, set()).add(rid)
        self.size += 1

    def insert_r(self, row: Row) -> int:
        """Add a tuple to R and a pair for each matching tuple of S. Returns its rid."""
        rid, self._next_r = self._next_r, self._next_r + 1  # @line L1
        self.r[rid] = row
        v = row[self.r_col]
        self.r_by_value.setdefault(v, set()).add(rid)
        for sid in self.s_by_value.get(v, ()):  # @line L2
            self._link(rid, sid)
        return rid

    def insert_s(self, row: Row) -> int:
        """Add a tuple to S and a pair for each matching tuple of R. Returns its rid."""
        sid, self._next_s = self._next_s, self._next_s + 1
        self.s[sid] = row
        v = row[self.s_col]
        self.s_by_value.setdefault(v, set()).add(sid)
        for rid in self.r_by_value.get(v, ()):
            self._link(rid, sid)
        return sid

    def delete_r(self, rid: int) -> Row:
        """Remove a tuple of R and all its pairs. Raises KeyError if rid is absent."""
        row = self.r.pop(rid)  # @line L3
        bucket = self.r_by_value[row[self.r_col]]
        bucket.discard(rid)
        if not bucket:
            del self.r_by_value[row[self.r_col]]
        for sid in self.by_r.pop(rid, set()):  # @line L4
            self.by_s[sid].discard(rid)
            if not self.by_s[sid]:
                del self.by_s[sid]
            self.size -= 1
        return row

    def delete_s(self, sid: int) -> Row:
        """Remove a tuple of S and all its pairs. Raises KeyError if sid is absent."""
        row = self.s.pop(sid)
        bucket = self.s_by_value[row[self.s_col]]
        bucket.discard(sid)
        if not bucket:
            del self.s_by_value[row[self.s_col]]
        for rid in self.by_s.pop(sid, set()):
            self.by_r[rid].discard(sid)
            if not self.by_r[rid]:
                del self.by_r[rid]
            self.size -= 1
        return row

    def pairs(self) -> set[tuple[int, int]]:
        return {(rid, sid) for rid, sids in self.by_r.items() for sid in sids}

    def matches_of_r(self, rid: int) -> set[int]:
        """The rids of S that join with the tuple rid of R (a semijoin lookup)."""
        return set(self.by_r.get(rid, ()))

    def join(self) -> tuple[list[Row], int]:
        """Compute R join S from the index. Returns the rows r + s and the page I/Os."""
        ordered = sorted(self.pairs())  # @line L5
        ios = ceil(len(ordered) / self.pairs_per_page)
        last: Optional[int] = None
        partial = []
        for rid, sid in ordered:  # @line L6
            page = rid // self.per_page
            if page != last:
                ios += 1
                last = page
            partial.append((sid, self.r[rid]))
        partial.sort(key=lambda t: t[0])  # @line L7
        last = None
        out = []
        for sid, r in partial:  # @line L8
            page = sid // self.per_page
            if page != last:
                ios += 1
                last = page
            out.append(r + self.s[sid])
        return out, ios  # @line L9

    def check_invariant(self) -> None:
        want = {(rid, sid) for rid, r in self.r.items() for sid, s in self.s.items()
                if r[self.r_col] == s[self.s_col]}
        assert self.pairs() == want
        assert {(rid, sid) for sid, rids in self.by_s.items() for rid in rids} == want
        assert self.size == len(want)
        assert all(self.by_r.values()) and all(self.by_s.values())
