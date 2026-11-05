# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-sampling-lsh/. The authors are listed in prov/PZGBBJ.jsonl.

import random
from collections.abc import Sequence


def hamming(x: int, y: int) -> int:
    """Return the number of bit positions where x and y differ."""
    return (x ^ y).bit_count()


class BitSamplingLSH:
    """LSH for the Hamming distance on d-bit integers, keyed by k sampled bits in each of L tables.

    Build: O(nLk) time, O(nL) space. Query: O(Lk) time for the keys and at most 3L
    distance computations of O(d / w) word operations each.
    """

    def __init__(
        self,
        points: Sequence[int],
        d: int,
        k: int,
        L: int,
        rng: random.Random | None = None,
        positions: list[list[int]] | None = None,
    ) -> None:
        if d < 1 or k < 1 or L < 1:
            raise ValueError("d, k and L must be at least 1")
        rng = rng if rng is not None else random.Random()
        self.points = list(points)
        self.L = L
        self.pos: list[list[int]] = []
        self.tables: list[dict[tuple[int, ...], list[int]]] = []
        for j in range(L):  # @line L1
            if positions is not None:
                idx = list(positions[j])
            else:
                idx = [rng.randrange(d) for _ in range(k)]  # @line L2
            self.pos.append(idx)
            table: dict[tuple[int, ...], list[int]] = {}
            for i, x in enumerate(self.points):
                table.setdefault(self.key(j, x), []).append(i)  # @line L3
            self.tables.append(table)

    def key(self, j: int, x: int) -> tuple[int, ...]:
        """Return the bits of x at the k sampled positions of table j."""
        return tuple((x >> i) & 1 for i in self.pos[j])

    def query(self, q: int, c: float, r: float) -> int | None:
        """Return the index of a point within Hamming distance c*r of q, or None."""
        count = 0  # @line L4
        for j in range(self.L):  # @line L5
            for i in self.tables[j].get(self.key(j, q), []):
                count += 1  # @line L6
                if hamming(q, self.points[i]) <= c * r:
                    return i
                if count >= 3 * self.L:  # @line L7
                    return None
        return None  # @line L8
