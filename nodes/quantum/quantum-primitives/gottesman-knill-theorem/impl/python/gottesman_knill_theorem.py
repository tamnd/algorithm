# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gottesman-knill-theorem/. The authors are listed in prov/V5TKK8.jsonl.
"""A stabilizer tableau simulator in the style of Aaronson and Gottesman (CHP).

The state of n qubits is stored as 2n Pauli rows plus one scratch row. Rows 0..n-1 are the
destabilizers, rows n..2n-1 generate the stabilizer group of the state. Row i is the operator
(-1)^r[i] * P_{n-1} (x) ... (x) P_0, where qubit j has the letter I, X, Z or Y when
(bit j of x[i], bit j of z[i]) is (0, 0), (1, 0), (0, 1) or (1, 1). Qubit 0 is the least
significant bit, and the rightmost letter of a word acts on qubit 0.

Cost: O(n) bit operations per gate (O(1) word operations on the 2n rows when n fits in a word,
counted here per row), and O(n^2) per measurement. Space O(n^2) bits.
"""

import random


def _g(x1: int, z1: int, x2: int, z2: int) -> int:
    """The exponent of i in P1 P2 for one-qubit Paulis P1 = (x1, z1), P2 = (x2, z2), Y = (1, 1)."""
    if x1 == 0 and z1 == 0:
        return 0
    if x1 == 1 and z1 == 1:
        return z2 - x2
    if x1 == 1:
        return z2 * (2 * x2 - 1)
    return x2 * (1 - 2 * z2)


class Tableau:
    def __init__(self, n: int) -> None:
        """The state |0...0>: destabilizers X_j, stabilizers Z_j."""
        if n < 1:
            raise ValueError("need at least one qubit")
        self.n = n
        self.x = [0] * (2 * n + 1)
        self.z = [0] * (2 * n + 1)
        self.r = [0] * (2 * n + 1)
        for j in range(n):
            self.x[j] = 1 << j
            self.z[n + j] = 1 << j

    def copy(self) -> "Tableau":
        t = Tableau.__new__(Tableau)
        t.n, t.x, t.z, t.r = self.n, list(self.x), list(self.z), list(self.r)
        return t

    def _check(self, *qs: int) -> None:
        if len(set(qs)) != len(qs) or not all(0 <= q < self.n for q in qs):
            raise ValueError("bad qubit index")

    # Gates. Each one updates all 2n rows; the sign rule comes from U P U^dagger.

    def h(self, a: int) -> None:
        self._check(a)
        m = 1 << a
        for i in range(2 * self.n):
            xa, za = self.x[i] & m, self.z[i] & m
            if xa and za:
                self.r[i] ^= 1  # H Y H = -Y
            self.x[i] = (self.x[i] & ~m) | za
            self.z[i] = (self.z[i] & ~m) | xa

    def s(self, a: int) -> None:
        self._check(a)
        m = 1 << a
        for i in range(2 * self.n):
            if self.x[i] & m and self.z[i] & m:
                self.r[i] ^= 1  # S Y S^dagger = -X
            if self.x[i] & m:
                self.z[i] ^= m

    def cnot(self, c: int, t: int) -> None:
        self._check(c, t)
        for i in range(2 * self.n):
            xc, zc = (self.x[i] >> c) & 1, (self.z[i] >> c) & 1
            xt, zt = (self.x[i] >> t) & 1, (self.z[i] >> t) & 1
            self.r[i] ^= xc & zt & (xt ^ zc ^ 1)
            self.x[i] ^= xc << t
            self.z[i] ^= zt << c

    def apply(self, gate: tuple) -> None:
        if gate[0] == "H":
            self.h(gate[1])
        elif gate[0] == "S":
            self.s(gate[1])
        elif gate[0] == "CNOT":
            self.cnot(gate[1], gate[2])
        else:
            raise ValueError("not a Clifford generator: " + str(gate[0]))

    # Measurement.

    def _rowsum(self, h: int, i: int) -> None:
        """Row h becomes row i times row h, with the exact sign."""
        e = 2 * self.r[h] + 2 * self.r[i]
        for j in range(self.n):
            e += _g((self.x[i] >> j) & 1, (self.z[i] >> j) & 1, (self.x[h] >> j) & 1, (self.z[h] >> j) & 1)
        if e % 4 not in (0, 2):
            raise AssertionError("rows do not commute")
        self.r[h] = 0 if e % 4 == 0 else 1
        self.x[h] ^= self.x[i]
        self.z[h] ^= self.z[i]

    def is_deterministic(self, a: int) -> bool:
        """True when a Z measurement of qubit a has a fixed outcome."""
        self._check(a)
        return all(not (self.x[p] >> a) & 1 for p in range(self.n, 2 * self.n))

    def measure(self, a: int, rng: random.Random | None = None, forced: int | None = None) -> tuple[int, bool]:
        """Measure qubit a in the computational basis. Returns (outcome, deterministic).

        A random outcome is taken from forced if given, else from rng. A forced value is
        ignored when the outcome is deterministic.
        """
        self._check(a)
        n = self.n
        m = 1 << a
        p = next((q for q in range(n, 2 * n) if self.x[q] & m), None)
        if p is not None:
            for i in range(2 * n):
                # row p - n anticommutes with row p, and it is overwritten below
                if i != p and i != p - n and self.x[i] & m:
                    self._rowsum(i, p)
            self.x[p - n], self.z[p - n], self.r[p - n] = self.x[p], self.z[p], self.r[p]
            if forced is not None:
                b = forced
            else:
                b = (rng or random.Random()).randrange(2)
            self.x[p], self.z[p], self.r[p] = 0, m, b
            return b, False
        s = 2 * n
        self.x[s] = self.z[s] = self.r[s] = 0
        for i in range(n):
            if self.x[i] & m:
                self._rowsum(s, i + n)
        return self.r[s], True

    # Reading the state.

    def row_word(self, i: int) -> tuple[int, str]:
        """(sign, word) of row i."""
        letters = []
        for q in range(self.n - 1, -1, -1):
            letters.append("IZXY"[2 * ((self.x[i] >> q) & 1) + ((self.z[i] >> q) & 1)])
        return (-1 if self.r[i] else 1), "".join(letters)

    def stabilizers(self) -> list[tuple[int, str]]:
        return [self.row_word(i) for i in range(self.n, 2 * self.n)]

    def destabilizers(self) -> list[tuple[int, str]]:
        return [self.row_word(i) for i in range(self.n)]


def simulate(n: int, circuit: list[tuple], rng: random.Random) -> list[int]:
    """Run a circuit of H, S, CNOT and ("M", q) steps from |0...0>. Returns the outcomes in order."""
    t = Tableau(n)
    out = []
    for g in circuit:
        if g[0] == "M":
            out.append(t.measure(g[1], rng)[0])
        else:
            t.apply(g)
    return out
