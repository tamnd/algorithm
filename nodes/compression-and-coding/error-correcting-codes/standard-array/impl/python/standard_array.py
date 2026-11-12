# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/standard-array/. The authors are listed in prov/YCM9KR.jsonl.

"""The standard array (Slepian 1956) of a linear code over GF(q), q prime.

Vectors are rows (tuples of integers in 0..q-1). Row 0 lists the codewords
c_0 = 0, c_1, ..., c_{M-1} in the order of their messages. Each later row is
a coset l + C, written as l + c_0, l + c_1, ..., l + c_{M-1}, where the coset
leader l is the first unused vector in the order: weight first, then the
vector read as a number with the first position most significant, from large
to small. So the leader of each row has the least weight in its coset.
"""

from itertools import product

Vector = tuple[int, ...]


def weight(v: Vector) -> int:
    return sum(1 for x in v if x)


def vector_order(n: int, q: int) -> list[Vector]:
    """All of GF(q)^n by weight, then in decreasing lexicographic order."""
    vs = list(product(range(q), repeat=n))
    return sorted(vs, key=lambda v: (weight(v), tuple(-x for x in v)))


class StandardArray:
    """A table of the q^(n - k) cosets of a linear code.

    Representation: rows[i][j] = leader_i + c_j, and where[v] = (i, j) for each
    vector v. Memory: q^n vectors of length n. Build time: Θ(q^n n).
    """

    def __init__(self, g: list[list[int]], q: int = 2) -> None:
        """Build the array of the code spanned by the rows of g (full rank, q prime)."""
        self.q = q
        self.k, self.n = len(g), len(g[0])
        self.codewords: list[Vector] = [
            tuple(sum(m[i] * g[i][j] for i in range(self.k)) % q for j in range(self.n))
            for m in product(range(q), repeat=self.k)
        ]
        self.rows: list[list[Vector]] = [list(self.codewords)]  # @line L1
        self.where: dict[Vector, tuple[int, int]] = {c: (0, j) for j, c in enumerate(self.codewords)}
        total = q ** (self.n - self.k)
        for v in vector_order(self.n, q):  # @line L2
            if v not in self.where:  # @line L3
                leader = v  # @line L4
                row = [tuple((a + b) % q for a, b in zip(leader, c)) for c in self.codewords]  # @line L5
                i = len(self.rows)
                for j, x in enumerate(row):  # @line L6
                    self.where[x] = (i, j)
                self.rows.append(row)
            if len(self.rows) == total:  # @line L7
                break

    def leader(self, i: int) -> Vector:
        """The coset leader of row i (the entry under the zero codeword)."""
        return self.rows[i][0]

    def locate(self, r: Vector) -> tuple[int, int]:
        """Row and column of r. Cost: one dictionary lookup."""
        return self.where[tuple(r)]

    def decode(self, r: Vector) -> Vector:
        """The codeword at the head of the column that holds r."""
        i, j = self.locate(r)  # @line L8
        return self.codewords[j]  # @line L9

    def check_invariant(self) -> None:
        """Rows partition GF(q)^n, each row is a coset, each leader has least weight."""
        q, n = self.q, self.n
        assert len(self.rows) == q ** (n - self.k)
        assert len(self.where) == q**n
        for i, row in enumerate(self.rows):
            lead = row[0]
            assert weight(lead) == min(weight(x) for x in row)
            for j, x in enumerate(row):
                assert x == tuple((a + b) % q for a, b in zip(lead, self.codewords[j]))
                assert self.where[x] == (i, j)
