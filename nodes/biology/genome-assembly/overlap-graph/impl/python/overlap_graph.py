# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overlap-graph/. The authors are listed in prov/QXKQRZ.jsonl.

from typing import Dict, List, Sequence, Tuple


def suffix_prefix_overlap(a: str, b: str) -> int:
    """Length of the longest proper suffix of a that is a proper prefix of b. Cost: O(|a| * |b|)."""
    for k in range(min(len(a), len(b)) - 1, 0, -1):
        if a[len(a) - k:] == b[:k]:
            return k
    return 0


class OverlapGraph:
    """Overlap graph of a list of reads with minimum overlap length ell.

    Vertex i is reads[i]. There is an arc (i, j), i != j, with weight w when the longest
    proper suffix of reads[i] that is a proper prefix of reads[j] has length w >= ell.
    Precondition: ell >= 1. Build cost: O(n * L * log m + P) time, where n is the total
    length, L the longest read, m the number of reads and P the number of triples (i, j, k)
    with a suffix-prefix match of length k >= ell.
    """

    def __init__(self, reads: Sequence[str], ell: int) -> None:
        if ell < 1:
            raise ValueError("the minimum overlap must be at least 1")
        self.reads: List[str] = list(reads)
        self.ell = ell
        m = len(self.reads)
        self.out: List[Dict[int, int]] = [dict() for _ in range(m)]
        self.inc: List[Dict[int, int]] = [dict() for _ in range(m)]
        # @line L1
        order = sorted(range(m), key=lambda q: self.reads[q])
        keys = [self.reads[q] for q in order]
        # @line L2
        for i, r in enumerate(self.reads):
            # @line L3
            for k in range(len(r) - 1, ell - 1, -1):
                # @line L4
                u = r[len(r) - k:]
                # @line L5
                lo, hi = self._prefix_range(keys, u)
                # @line L6
                for p in range(lo, hi):
                    j = order[p]
                    if j == i or len(self.reads[j]) <= k or j in self.out[i]:
                        continue
                    # @line L7
                    self.out[i][j] = k
                    self.inc[j][i] = k

    @staticmethod
    def _prefix_range(keys: List[str], u: str) -> Tuple[int, int]:
        """Half-open range of the sorted keys that start with u, by two binary searches."""
        k = len(u)
        lo, hi = 0, len(keys)
        while lo < hi:
            mid = (lo + hi) // 2
            if keys[mid] < u:
                lo = mid + 1
            else:
                hi = mid
        start = lo
        hi = len(keys)
        while lo < hi:
            mid = (lo + hi) // 2
            if keys[mid][:k] > u:
                hi = mid
            else:
                lo = mid + 1
        return start, lo

    def num_vertices(self) -> int:
        return len(self.reads)

    def num_arcs(self) -> int:
        return sum(len(d) for d in self.out)

    def weight(self, i: int, j: int) -> int:
        """Weight of the arc (i, j), or 0 when there is no arc. O(1) expected time."""
        return self.out[i].get(j, 0)

    def out_arcs(self, i: int) -> List[Tuple[int, int]]:
        """Arcs leaving i as (j, w), by decreasing w, then increasing j."""
        return sorted(self.out[i].items(), key=lambda e: (-e[1], e[0]))

    def in_arcs(self, j: int) -> List[Tuple[int, int]]:
        """Arcs entering j as (i, w), by decreasing w, then increasing i."""
        return sorted(self.inc[j].items(), key=lambda e: (-e[1], e[0]))

    def spell(self, path: Sequence[int]) -> str:
        """String spelled by a path of arcs: the first read, then each next read without its overlap."""
        if not path:
            return ""
        parts = [self.reads[path[0]]]
        for a, b in zip(path, path[1:]):
            if b not in self.out[a]:
                raise ValueError("not a path of the overlap graph")
            parts.append(self.reads[b][self.out[a][b]:])
        return "".join(parts)

    def check_invariant(self) -> None:
        """Arcs are exactly the pairs with longest proper overlap >= ell; in and out lists agree."""
        m = len(self.reads)
        for i in range(m):
            for j in range(m):
                w = suffix_prefix_overlap(self.reads[i], self.reads[j]) if i != j else 0
                if i != j and w >= self.ell:
                    assert self.out[i].get(j) == w, (i, j)
                    assert self.inc[j].get(i) == w, (i, j)
                else:
                    assert j not in self.out[i] and i not in self.inc[j], (i, j)
