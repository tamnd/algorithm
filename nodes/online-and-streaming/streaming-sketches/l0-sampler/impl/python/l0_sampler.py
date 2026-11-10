# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l0-sampler/. The authors are listed in prov/QSH7SV.jsonl.
"""An L0 sampler: a linear sketch that returns a nonzero coordinate of x.

The vector x has n coordinates 1..n and receives turnstile updates (i, d).
Each copy of the sampler hashes the coordinates with a k-wise independent
polynomial hash h into [0, P). Level j holds the coordinates with
h(i) < P / 2^j, so the levels are nested and level j keeps about a 2^-j
fraction. Each level keeps a 1-sparse recovery structure (A, B, C):

    A = sum of x_i,  B = sum of i x_i,  C = sum of x_i z^i mod P.

If the vector restricted to a level has one nonzero coordinate, the three
numbers reveal it; if it has more, the test rejects except with probability
at most n / P over the random z.
"""

from __future__ import annotations

import math
import random

P = (1 << 61) - 1  # a Mersenne prime, used for the hash and the fingerprint

ZERO = "zero"
MANY = "many"
EMPTY = "empty"
FAIL = "fail"


def decode(a: int, b: int, c: int, n: int, z: int, q: int = P):
    """The 1-sparse test. Returns ZERO, MANY, or (i, value)."""
    if a == 0 and b == 0 and c == 0:  # @line L3
        return ZERO
    if a != 0 and b % a == 0:  # @line L4
        i = b // a
        if 1 <= i <= n and c == (a * pow(z, i, q)) % q:
            return (i, a)
    return MANY  # @line L5


class OneSparse:
    """The counters (A, B, C) of one level, for a fixed fingerprint base z."""

    __slots__ = ("a", "b", "c")

    def __init__(self) -> None:
        self.a = 0
        self.b = 0
        self.c = 0


class L0Sampler:
    """copies x (levels + 1) one-sparse structures; a linear sketch of x in Z^n."""

    def __init__(self, n: int, delta: float, rng: random.Random, k: int = 8) -> None:
        self.n = n
        self.levels = max(1, math.ceil(math.log2(max(n, 2)))) + 2
        # a copy fails with probability at most 17/32 (see the proof), so this many copies give delta
        self.copies = max(1, math.ceil(math.log(1 / delta) / math.log(32 / 17)))
        # each copy: hash coefficients (degree k - 1) and a fingerprint base z
        self.hashes = [[rng.randrange(P) for _ in range(k)] for _ in range(self.copies)]
        self.zs = [rng.randrange(1, P) for _ in range(self.copies)]
        self.cells = [[OneSparse() for _ in range(self.levels + 1)] for _ in range(self.copies)]

    def _hash(self, c: int, i: int) -> int:
        v = 0
        for coef in self.hashes[c]:
            v = (v * i + coef) % P
        return v

    def level_of(self, c: int, i: int) -> int:
        """The deepest level j <= L with h(i) < P / 2^j."""
        h = self._hash(c, i)
        j = 0
        while j < self.levels and h < P >> (j + 1):
            j += 1
        return j

    def update(self, i: int, d: int) -> None:
        """x_i += d."""
        if not 1 <= i <= self.n:
            raise ValueError("coordinate out of range")
        for c in range(self.copies):
            top = self.level_of(c, i)  # @line L1
            fp = (d * pow(self.zs[c], i, P)) % P
            for j in range(top + 1):  # @line L2
                cell = self.cells[c][j]
                cell.a += d
                cell.b += i * d
                cell.c = (cell.c + fp) % P

    def add(self, other: "L0Sampler", sign: int = 1) -> None:
        """Linearity: self becomes the sketch of x + sign * y. Both must share the seeds."""
        assert self.hashes == other.hashes and self.zs == other.zs
        for c in range(self.copies):
            for mine, theirs in zip(self.cells[c], other.cells[c]):
                mine.a += sign * theirs.a
                mine.b += sign * theirs.b
                mine.c = (mine.c + sign * theirs.c) % P

    def copy_empty(self) -> "L0Sampler":
        """A sketch of the zero vector with the same seeds."""
        twin = object.__new__(L0Sampler)
        twin.n, twin.levels, twin.copies = self.n, self.levels, self.copies
        twin.hashes, twin.zs = self.hashes, self.zs
        twin.cells = [[OneSparse() for _ in range(self.levels + 1)] for _ in range(self.copies)]
        return twin

    def query(self):
        """Return (i, x_i) for a nonzero x_i, EMPTY if x = 0, or FAIL."""
        for c in range(self.copies):  # @line L6
            all_zero = True
            for j in range(self.levels, -1, -1):  # @line L7
                cell = self.cells[c][j]
                r = decode(cell.a, cell.b, cell.c, self.n, self.zs[c])
                if r == ZERO:
                    continue
                all_zero = False
                if r != MANY:  # @line L8
                    return r
                break
            if all_zero:  # @line L9
                return EMPTY
        return FAIL  # @line L10

    def check_invariant(self, x: dict | None = None) -> None:
        """Shapes and ranges; with the true vector x, every counter matches its definition."""
        assert len(self.cells) == self.copies
        for c in range(self.copies):
            assert len(self.cells[c]) == self.levels + 1
            for cell in self.cells[c]:
                assert 0 <= cell.c < P
            if x is None:
                continue
            for j, cell in enumerate(self.cells[c]):
                part = {i: v for i, v in x.items() if v and self.level_of(c, i) >= j}
                assert cell.a == sum(part.values())
                assert cell.b == sum(i * v for i, v in part.items())
                assert cell.c == sum(v * pow(self.zs[c], i, P) for i, v in part.items()) % P
