# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flux-balance-analysis/. The authors are listed in prov/TC2TH5.jsonl.
"""Flux balance analysis as one exact linear program.

A network has n metabolites and m reactions. S is the n x m stoichiometric
matrix (a list of n rows of length m), lb and ub are the flux bounds (None
means minus or plus infinity) and c is the objective vector, usually the unit
vector of the biomass reaction. FBA solves

    maximize c v  subject to  S v = 0,  lb <= v <= ub.

fba() writes this LP in the standard form min d y, A y = b, y >= 0, and
solves it with the exact two-phase simplex method with Bland's rule of
sy3lp.py. All arithmetic is in Fraction.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Optional, Sequence

from sy3lp import frac, simplex_standard


class FBAResult:
    """status is 'optimal', 'infeasible' or 'unbounded'.

    For 'optimal', v is one optimal flux vector and z = c v the optimum.
    """

    def __init__(self, status: str, v: Optional[List[Fraction]] = None,
                 z: Optional[Fraction] = None):
        self.status = status
        self.v = v
        self.z = z

    def __repr__(self) -> str:
        return f"FBAResult({self.status!r}, {self.v!r}, {self.z!r})"


def fba(S: Sequence[Sequence], lb: Sequence, ub: Sequence,
        c: Sequence) -> FBAResult:
    """Maximize c v subject to S v = 0 and lb <= v <= ub, exactly."""
    m = len(c)
    # Each flux is v_j = off_j + sum of sign * y_k over its columns k, y >= 0.
    off: List[Fraction] = []  # @line L1
    cols: List[List[tuple]] = []
    ny = 0
    for j in range(m):
        if lb[j] is not None and ub[j] is not None and frac(lb[j]) > frac(ub[j]):
            return FBAResult("infeasible")
        if lb[j] is not None:
            off.append(frac(lb[j]))
            cols.append([(ny, 1)])
            ny += 1
        elif ub[j] is not None:
            off.append(frac(ub[j]))
            cols.append([(ny, -1)])
            ny += 1
        else:
            off.append(Fraction(0))
            cols.append([(ny, 1), (ny + 1, -1)])
            ny += 2
    caps = [j for j in range(m) if lb[j] is not None and ub[j] is not None]
    N = ny + len(caps)
    A: List[List[Fraction]] = []  # @line L2
    b: List[Fraction] = []
    for row in S:
        r = [Fraction(0)] * N
        shift = Fraction(0)
        for j in range(m):
            a = frac(row[j])
            if a != 0:
                shift += a * off[j]
                for k, s in cols[j]:
                    r[k] += a * s
        A.append(r)
        b.append(-shift)
    for t, j in enumerate(caps):  # @line L3
        r = [Fraction(0)] * N
        r[cols[j][0][0]] = Fraction(1)
        r[ny + t] = Fraction(1)
        A.append(r)
        b.append(frac(ub[j]) - frac(lb[j]))
    d = [Fraction(0)] * N  # @line L4
    for j in range(m):
        for k, s in cols[j]:
            d[k] -= frac(c[j]) * s
    res = simplex_standard(A, b, d)  # @line L5
    if res.status != "optimal":  # @line L6
        return FBAResult(res.status)
    v = [off[j] + sum(s * res.x[k] for k, s in cols[j]) for j in range(m)]  # @line L7
    z = sum(frac(cj) * vj for cj, vj in zip(c, v))
    return FBAResult("optimal", v, z)  # @line L8


def knockout_bounds(lb: Sequence, ub: Sequence, knocked: Sequence[int]):
    """Bounds of a mutant: each reaction in knocked gets lb = ub = 0."""
    lb2, ub2 = list(lb), list(ub)
    for j in knocked:
        lb2[j] = 0
        ub2[j] = 0
    return lb2, ub2


# The toy network N of the page. Metabolites: A, E (energy), P (product).
# Reactions: EX_A (uptake of A, at most 10), RESP1 and RESP2 (A -> 2 E, two
# parallel routes), FERM (A -> E + P), EX_P (secretion of P), BIO (A + E -> ).
NAMES = ["EX_A", "RESP1", "RESP2", "FERM", "EX_P", "BIO"]
S_N = [
    [1, -1, -1, -1, 0, -1],  # A
    [0, 2, 2, 1, 0, -1],     # E
    [0, 0, 0, 1, -1, 0],     # P
]
LB_N = [0, 0, 0, 0, 0, 0]
UB_N = [10, None, None, None, None, None]
C_N = [0, 0, 0, 0, 0, 1]
