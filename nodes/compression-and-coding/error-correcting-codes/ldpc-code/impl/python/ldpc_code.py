# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ldpc-code/. The authors are listed in prov/JDSJ23.jsonl.

"""Low-density parity-check codes: Gallager's regular construction, degree
distributions, the design rate, and density evolution on the BEC.

A parity-check matrix H is a list of rows of 0 and 1; codewords are rows c
with H c^T = 0 over GF(2). Degree distributions are edge-perspective dicts
{degree: fraction of edges}: lambda(x) = sum lambda_i x^(i - 1) for the
variable nodes and rho(x) = sum rho_j x^(j - 1) for the check nodes.
"""

import random
from typing import Dict, List, Sequence

Dist = Dict[int, float]


def gallager_regular(n: int, dv: int, dc: int, rng: random.Random) -> List[List[int]]:
    """Gallager's (n, dv, dc) construction: dv bands of n / dc rows. Band 0
    has row i covering columns i dc .. i dc + dc - 1; each other band is a
    random column permutation of band 0. Needs dc | n."""
    if n % dc:
        raise ValueError("dc must divide n")
    rows = n // dc
    band = [[1 if i * dc <= j < (i + 1) * dc else 0 for j in range(n)] for i in range(rows)]
    h = [row[:] for row in band]
    for _ in range(dv - 1):
        perm = list(range(n))
        rng.shuffle(perm)
        h += [[row[perm[j]] for j in range(n)] for row in band]
    return h


def integral(dist: Dist) -> float:
    """The integral from 0 to 1 of sum_i d_i x^(i - 1), that is sum_i d_i / i."""
    return sum(f / i for i, f in dist.items())


def design_rate(lam: Dist, rho: Dist) -> float:
    """r = 1 - (integral of rho) / (integral of lambda)."""
    return 1 - integral(rho) / integral(lam)


def node_to_edge(node: Dist) -> Dist:
    """From node fractions {degree: fraction of nodes} to edge fractions."""
    tot = sum(d * f for d, f in node.items())
    return {d: d * f / tot for d, f in node.items()}


def poly(dist: Dist, x: float) -> float:
    return sum(f * x ** (i - 1) for i, f in dist.items())


def de_bec(eps: float, lam: Dist, rho: Dist, iterations: int) -> float:
    """Density evolution of belief propagation on BEC(eps): the erasure
    probability of a variable-to-check message after the iterations,
    x_(l+1) = eps lambda(1 - rho(1 - x_l)), x_0 = eps."""
    x = eps
    for _ in range(iterations):
        x = eps * poly(lam, 1 - poly(rho, 1 - x))
    return x


def bec_threshold(lam: Dist, rho: Dist, tol: float = 1e-7, iterations: int = 20000) -> float:
    """The largest eps for which density evolution goes to 0, by bisection."""
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if de_bec(mid, lam, rho, iterations) < 1e-10:
            lo = mid
        else:
            hi = mid
    return lo


def bec_threshold_fixed_point(lam: Dist, rho: Dist, grid: int = 200000) -> float:
    """The same threshold as inf over x in (0, 1] of x / lambda(1 - rho(1 - x))."""
    return min(x / poly(lam, 1 - poly(rho, 1 - x)) for x in (i / grid for i in range(1, grid + 1)))


def gf2_null_space(h: Sequence[Sequence[int]]) -> List[List[int]]:
    """A basis of the codewords: Gaussian elimination over GF(2)."""
    n = len(h[0])
    rows = [sum(b << j for j, b in enumerate(r)) for r in h]
    pivots: List[int] = []
    red: List[int] = []
    for r in rows:
        for p, q in zip(pivots, red):
            if (r >> p) & 1:
                r ^= q
        if r:
            p = (r & -r).bit_length() - 1
            for i in range(len(red)):
                if (red[i] >> p) & 1:
                    red[i] ^= r
            pivots.append(p)
            red.append(r)
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        v = 1 << f
        for p, q in zip(pivots, red):
            if (q >> f) & 1:
                v |= 1 << p
        basis.append([(v >> j) & 1 for j in range(n)])
    return basis
