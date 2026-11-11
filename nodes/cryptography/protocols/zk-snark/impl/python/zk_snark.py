# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zk-snark/. The authors are listed in prov/QH7EWC.jsonl.
"""The arithmetization step of a pairing-based zk-SNARK: R1CS to QAP.

This file does NOT implement a SNARK. There are no pairings, no trusted
setup, no encrypted evaluation and no zero knowledge here. It implements the
first half of the pipeline that Pinocchio and Groth16 use:

  1. A rank-1 constraint system (R1CS): vectors a_j, b_j, c_j per constraint,
     satisfied by s when <a_j, s> * <b_j, s> = <c_j, s> for each j.
  2. A quadratic arithmetic program (QAP): interpolate each column over the
     points 1..m, so that s satisfies the R1CS if and only if
     t(X) = (X - 1)...(X - m) divides A_s(X) B_s(X) - C_s(X).
  3. The check at one random point tau (Schwartz-Zippel), which is what the
     SNARK does "in the exponent" with pairings.

The field is the scalar field of the BN254 curve (alt_bn128), the field of
Groth16 proofs in Ethereum. The example is x^3 + x + 5 = 35, from Vitalik
Buterin's 2016 introduction.

For study only. Use a reviewed proof system library such as arkworks,
libsnark or gnark for real proofs.
"""

import secrets

R = 21888242871839275222246405745257275088548364400416034343698204186575808495617


# ------------------------------------------------------------ polynomials mod R
# A polynomial is a list of coefficients, lowest degree first.
def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p, q, mod=R):
    n = max(len(p), len(q))
    return trim([((p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)) % mod for i in range(n)])


def pscale(p, c, mod=R):
    return trim([a * c % mod for a in p])


def psub(p, q, mod=R):
    return padd(p, pscale(q, mod - 1, mod), mod)


def pmul(p, q, mod=R):
    if not p or not q:
        return []
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] = (out[i + j] + a * b) % mod
    return trim(out)


def pdivmod(num, den, mod=R):
    """Long division: num = quot * den + rem with deg rem < deg den."""
    num, den = trim(num), trim(den)
    inv = pow(den[-1], -1, mod)
    quot = [0] * max(len(num) - len(den) + 1, 0)
    rem = list(num)
    for i in range(len(quot) - 1, -1, -1):
        coef = rem[i + len(den) - 1] * inv % mod
        quot[i] = coef
        for j, d in enumerate(den):
            rem[i + j] = (rem[i + j] - coef * d) % mod
    return trim(quot), trim(rem)


def peval(p, x, mod=R):
    acc = 0
    for a in reversed(p):
        acc = (acc * x + a) % mod
    return acc


def lagrange(ys, mod=R):
    """The polynomial of degree < m through (1, ys[0]), ..., (m, ys[m-1])."""
    m = len(ys)
    xs = list(range(1, m + 1))
    out = []
    for i, yi in enumerate(ys):
        if yi % mod == 0:
            continue
        basis, denom = [1], 1
        for j, xj in enumerate(xs):
            if j != i:
                basis = pmul(basis, [(-xj) % mod, 1], mod)
                denom = denom * (xs[i] - xj) % mod
        out = padd(out, pscale(basis, yi * pow(denom, -1, mod) % mod, mod), mod)
    return out


def vanishing(m, mod=R):
    t = [1]
    for j in range(1, m + 1):
        t = pmul(t, [(-j) % mod, 1], mod)
    return t


# ------------------------------------------------------------ R1CS and QAP
# Variables: [one, x, out, sym1, y, sym2]
VARIABLES = ["one", "x", "out", "sym1", "y", "sym2"]
# x * x = sym1;  sym1 * x = y;  (y + x) * 1 = sym2;  (sym2 + 5) * 1 = out
A_ROWS = [
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [5, 0, 0, 0, 0, 1],
]
B_ROWS = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
]
C_ROWS = [
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0],
]
WITNESS = [1, 3, 35, 9, 27, 30]


def dot(u, v, mod=R):
    return sum(a * b for a, b in zip(u, v)) % mod


def r1cs_satisfied(A, B, C, s, mod=R):
    return all(dot(a, s, mod) * dot(b, s, mod) % mod == dot(c, s, mod) for a, b, c in zip(A, B, C))


def qap_columns(rows, mod=R):
    """One polynomial per variable: column i interpolated over the points 1..m."""
    n = len(rows[0])
    return [lagrange([row[i] for row in rows], mod) for i in range(n)]


class QAP:
    def __init__(self, A, B, C, mod=R):
        self.mod = mod
        self.m = len(A)
        self.A = qap_columns(A, mod)                               # @line L1
        self.B = qap_columns(B, mod)
        self.C = qap_columns(C, mod)
        self.t = vanishing(self.m, mod)                            # @line L2

    def combine(self, cols, s):
        out = []
        for poly, si in zip(cols, s):
            out = padd(out, pscale(poly, si % self.mod, self.mod), self.mod)
        return out

    def polys(self, s):
        """A_s, B_s, C_s and P = A_s B_s - C_s."""
        a = self.combine(self.A, s)                                # @line L3
        b = self.combine(self.B, s)
        c = self.combine(self.C, s)
        return a, b, c, psub(pmul(a, b, self.mod), c, self.mod)    # @line L4

    def quotient(self, s):
        """(h, remainder) of P / t. The remainder is zero iff s satisfies the R1CS."""
        *_, p = self.polys(s)
        return pdivmod(p, self.t, self.mod)                        # @line L5

    def check_at(self, s, h, tau):
        """The SNARK's check, here in the clear: A(tau) B(tau) - C(tau) = h(tau) t(tau)."""
        a, b, c, _ = self.polys(s)
        lhs = (peval(a, tau, self.mod) * peval(b, tau, self.mod) - peval(c, tau, self.mod)) % self.mod
        return lhs == peval(h, tau, self.mod) * peval(self.t, tau, self.mod) % self.mod  # @line L6


def random_point(mod=R):
    return secrets.randbelow(mod)
