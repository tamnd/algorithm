# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-fourier-transform/. The authors are listed in prov/E4WS9H.jsonl.

"""Sparse DFT by aliasing and peeling (an exact, verified form of FFAST).

The length n is a product of pairwise coprime factors f_1, ..., f_d. Stage i
reads x at the positions t*(n/f_i) + s for t < f_i and a few shifts s, and a
DFT of length f_i sorts the spectrum into f_i buckets by k mod f_i. Buckets
holding one frequency are decoded (the residues of k come from the shifts
n/f_j, the Chinese remainder theorem gives k) and subtracted everywhere.
X_k = sum_j x_j w**(j*k); over C, w = exp(-2*pi*i/n).
"""

from __future__ import annotations

import cmath
import math
from typing import Callable, Sequence


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * math.pi * r / n)


def crt(residues: Sequence[int], moduli: Sequence[int]) -> int:
    """The k in [0, prod moduli) with k = residues[i] mod moduli[i]."""
    k, m = 0, 1
    for r, f in zip(residues, moduli):
        # solve k + m*u = r (mod f)
        u = (r - k) * pow(m, -1, f) % f
        k, m = k + m * u, m * f
    return k


class _Field:
    """Arithmetic over C (p is None) or over Z/pZ, with the n-th root w."""

    def __init__(self, n: int, w: int | None, p: int | None, tol: float) -> None:
        self.n, self.p, self.tol = n, p, tol
        if p is not None:
            if w is None or pow(w, n, p) != 1 or any(pow(w, n // q, p) == 1 for q in _primes(n)):
                raise ValueError("w must be a principal n-th root of unity modulo p")
            self.w = w

    def root(self, e: int) -> complex | int:
        """w**e."""
        if self.p is None:
            return _unit(-e, self.n)
        return pow(self.w, e % self.n, self.p)

    def norm(self, v: complex | int) -> complex | int:
        return v % self.p if self.p is not None else v

    def scale(self, num: int, den: int) -> complex | int:
        """num/den in the field."""
        if self.p is None:
            return num / den
        return num * pow(den, -1, self.p) % self.p

    def is_zero(self, v: complex | int) -> bool:
        return abs(v) <= self.tol if self.p is None else v % self.p == 0


def _primes(n: int) -> list[int]:
    out, q = [], 2
    while q * q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


def sparse_dft(
    sample: Callable[[int], complex | int],
    factors: Sequence[int],
    K: int,
    T: int | None = None,
    w: int | None = None,
    p: int | None = None,
    tol: float = 1e-7,
) -> tuple[dict[int, complex | int], bool, int]:
    """Recover the spectrum of x (at most K nonzero X_k) from few samples.

    sample(j) returns x_j for 0 <= j < n = prod(factors); the factors must be
    pairwise coprime. T is the largest consecutive shift used to verify a
    bucket; T >= K makes every reported coefficient provably correct (exact
    arithmetic). Returns (coefficients, success, number of samples read).
    """
    factors = list(factors)
    n = math.prod(factors)
    for a in range(len(factors)):
        for b in range(a + 1, len(factors)):
            if math.gcd(factors[a], factors[b]) != 1:
                raise ValueError("the factors must be pairwise coprime")
    if T is None:
        T = K
    F = _Field(n, w, p, tol)
    d = len(factors)
    shifts = sorted(set(range(T + 1)) | {n // f for f in factors})  # @line L1
    # Z[i][s][b] = sum_t x_(t*n/f + s) * w_f**(t*b) = (f/n) sum_(k = b mod f) X_k w**(-s*k)
    Z: list[dict[int, list]] = []
    reads = 0
    for f in factors:  # @line L2
        step = n // f
        wf = [F.root(step * e) for e in range(f)]
        per_shift = {}
        for s in shifts:
            z = [sample((t * step + s) % n) for t in range(f)]
            reads += f
            per_shift[s] = [F.norm(sum(z[t] * wf[(t * b) % f] for t in range(f))) for b in range(f)]
        Z.append(per_shift)
    if F.p is None:  # tolerance relative to the largest bucket value
        big = max((abs(v) for st in Z for row in st.values() for v in row), default=0.0)
        F.tol = tol * max(big, 1.0)
    # tables for reading k mod f_j from the ratio w_(f_j)**(-r)
    tables = []
    for f in factors:
        tables.append([F.root(-(n // f) * r) for r in range(f)])
    found: dict[int, complex | int] = {}  # @line L3
    budget = K  # a K-sparse input needs at most K peels; this also bounds bad inputs
    progress = True
    while progress and budget > 0:  # @line L4
        progress = False
        for i, f in enumerate(factors):  # @line L5
            for b in range(f):
                z0 = Z[i][0][b]
                if F.is_zero(z0):
                    continue
                residues = []
                for j, g in enumerate(factors):  # @line L6
                    if j == i:
                        residues.append(b)
                        continue
                    zs = Z[i][n // g][b]
                    r = _match(F, tables[j], zs, z0)
                    if r is None:
                        break
                    residues.append(r)
                if len(residues) < d:
                    continue
                k = crt(residues, factors)  # @line L7
                v = F.norm(z0 * (n // f))
                coef = F.scale(f, n)
                ok = all(  # @line L8
                    F.is_zero(Z[i][s][b] - coef * v * F.root(-s * k)) for s in shifts
                )
                if not ok:
                    continue
                found[k] = F.norm(found.get(k, 0) + v)  # @line L9
                for l, g in enumerate(factors):
                    cg = F.scale(g, n)
                    for s in shifts:
                        row = Z[l][s]
                        row[k % g] = F.norm(row[k % g] - cg * v * F.root(-s * k))
                progress = True
                budget -= 1
                if budget == 0:
                    break
            if budget == 0:
                break
    success = all(F.is_zero(v) for st in Z for row in st.values() for v in row)  # @line L10
    if F.p is None:
        found = {k: v for k, v in found.items() if abs(v) > F.tol}
    else:
        found = {k: v for k, v in found.items() if v % F.p}
    return found, success, reads  # @line L11


def _match(F: _Field, table: list, zs, z0) -> int | None:
    """The r with zs = table[r] * z0, or None."""
    if F.p is not None:
        for r, t in enumerate(table):
            if (zs - t * z0) % F.p == 0:
                return r
        return None
    best = min(range(len(table)), key=lambda r: abs(zs - table[r] * z0))
    return best if abs(zs - table[best] * z0) <= F.tol else None
