# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flux-variability-analysis/. The authors are listed in prov/3ZQX3G.jsonl.
"""Flux variability analysis with exact linear programs.

A network has n metabolites and m reactions, with the n x m stoichiometric
matrix S, the flux bounds lb and ub (None is infinite) and the objective c.
FVA first solves the FBA problem max c v, S v = 0, lb <= v <= ub, for the
optimum z. Then for each reaction j it solves two LPs, the minimum and the
maximum of v_j over the set

    S v = 0,  lb <= v <= ub,  c v >= t,  with t = z - (1 - f) |z|.

f = 1 gives the optimal face of the FBA problem. f < 1 keeps every flux
vector whose objective is within the fraction 1 - f of the optimum. Each LP
is solved exactly by the simplex method of sy3lp.py.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple

from sy3lp import frac, solve_lp

Range = Tuple[Optional[Fraction], Optional[Fraction]]


def fva(S: Sequence[Sequence], lb: Sequence, ub: Sequence, c: Sequence,
        fraction=1, reactions: Optional[Sequence[int]] = None):
    """Return (z, ranges): the FBA optimum and the range of each flux.

    ranges[k] = (lo, hi) for reaction reactions[k] (all reactions by
    default). lo is None if v_j is unbounded below over the set, and hi is
    None if it is unbounded above. Raises ValueError if the FBA problem is
    infeasible or unbounded.
    """
    m = len(c)
    zeros = [0] * len(S)
    base = solve_lp(c, A_eq=S, b_eq=zeros, lb=lb, ub=ub, maximize=True)  # @line L1
    if base.status != "optimal":
        raise ValueError("the FBA problem is " + base.status)
    z = base.value
    f = frac(fraction)
    t = z - (1 - f) * abs(z)  # @line L2
    A_le = [[-frac(x) for x in c]]
    b_le = [-t]
    out: List[Range] = []
    for j in (range(m) if reactions is None else reactions):  # @line L3
        e = [0] * m
        e[j] = 1
        lo = solve_lp(e, A_eq=S, b_eq=zeros, A_le=A_le, b_le=b_le,  # @line L4
                      lb=lb, ub=ub)
        hi = solve_lp(e, A_eq=S, b_eq=zeros, A_le=A_le, b_le=b_le,  # @line L5
                      lb=lb, ub=ub, maximize=True)
        out.append((lo.value if lo.status == "optimal" else None,  # @line L6
                    hi.value if hi.status == "optimal" else None))
    return z, out  # @line L7


def blocked_reactions(S, lb, ub):
    """Reactions with v_j = 0 in every steady state: FVA with c = 0."""
    _, ranges = fva(S, lb, ub, [0] * len(lb))
    return [j for j, (lo, hi) in enumerate(ranges) if lo == 0 and hi == 0]


# The toy network N of the flux-balance-analysis page.
NAMES = ["EX_A", "RESP1", "RESP2", "FERM", "EX_P", "BIO"]
S_N = [
    [1, -1, -1, -1, 0, -1],  # A
    [0, 2, 2, 1, 0, -1],     # E
    [0, 0, 0, 1, -1, 0],     # P
]
LB_N = [0, 0, 0, 0, 0, 0]
UB_N = [10, None, None, None, None, None]
C_N = [0, 0, 0, 0, 0, 1]
