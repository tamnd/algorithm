# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-flux-balance-analysis/. The authors are listed in prov/4C9MZV.jsonl.
"""Dynamic flux balance analysis by the static optimization approach.

The state is the biomass X (g/L) and the concentrations z of extracellular
species (mmol/L). At each time step of length dt:
1. each uptake reaction j of species k gets the upper bound
   min(vmax_j z_k / (Km_j + z_k), z_k / (X dt)), so that the step cannot use
   more than what is in the medium;
2. one FBA problem (max v_bio subject to S v = 0, lb <= v <= ub) gives the
   fluxes v in mmol/gDW/h and the growth rate mu = v_bio in 1/h;
3. the state moves by one explicit Euler step: X += dt mu X and
   z_k += dt (E v)_k X, where E maps the exchange fluxes to the medium.

update="exponential" is the variant of Varma and Palsson: X is multiplied by
exp(mu dt) and z_k changes by (E v)_k X (exp(mu dt) - 1) / mu. It is exact
when v stays constant over the step. With it, z_k is cut at 0.

The LP of each step is solved exactly by sy3lp.py on the exact rational
value of the float bounds; the state itself is in float.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import List, Sequence, Tuple

from sy3lp import solve_lp


def dfba(S: Sequence[Sequence], lb: Sequence, ub: Sequence, bio: int,
         E: Sequence[Sequence], uptakes: Sequence[Tuple[int, int, float, float]],
         X0: float, z0: Sequence[float], dt: float, steps: int,
         update: str = "euler"):
    """Run the static optimization approach for steps steps of length dt.

    E[k][j] is the change of medium species k per unit flux of reaction j
    and per unit biomass. uptakes holds (j, k, vmax, Km) for each uptake
    reaction j of species k. Returns a list of (t, X, z, v); v is the flux
    vector used for the step that starts at t (None in the last record or
    when the LP is infeasible, which ends the run).
    """
    c = [0] * len(lb)
    c[bio] = 1
    zeros = [0] * len(S)
    t, X, z = 0.0, float(X0), [float(x) for x in z0]  # @line L1
    out: List[tuple] = []
    for _ in range(steps):  # @line L2
        hi = list(ub)
        for j, k, vmax, km in uptakes:  # @line L3
            s = max(z[k], 0.0)
            bound = vmax * s / (km + s) if km + s > 0 else 0.0
            if X > 0:
                bound = min(bound, s / (X * dt))
            hi[j] = Fraction(bound)
        res = solve_lp(c, A_eq=S, b_eq=zeros, lb=lb, ub=hi, maximize=True)  # @line L4
        if res.status != "optimal":  # @line L5
            out.append((t, X, list(z), None))
            return out
        v = [float(x) for x in res.x]
        mu = v[bio]
        out.append((t, X, list(z), v))
        rates = [sum(E[k][j] * v[j] for j in range(len(v))) for k in range(len(z))]
        if update == "euler":  # @line L6
            z = [zk + dt * rk * X for zk, rk in zip(z, rates)]
            X = X + dt * mu * X
        else:
            g = math.expm1(mu * dt) / mu if mu != 0 else dt
            z = [max(zk + rk * X * g, 0.0) for zk, rk in zip(z, rates)]
            X = X * math.exp(mu * dt)
        t += dt  # @line L7
    out.append((t, X, list(z), None))
    return out  # @line L8


# The overflow network of the page. Internal metabolites: A (substrate),
# O (oxygen), E (energy), P (by-product). Reactions:
# 0 EX_A: -> A (uptake of the medium substrate s, Monod bound)
# 1 EX_O: -> O, at most O_MAX
# 2 RESP: A + O -> 2 E
# 3 FERM: A -> E + P
# 4 EX_P: P -> (secretion into the medium)
# 5 BIO: 5 A + 5 E -> biomass (flux = growth rate in 1/h)
O_MAX = 1
VMAX, KM = 10.0, 1.0
S_OV = [
    [1, 0, -1, -1, 0, -5],  # A
    [0, 1, -1, 0, 0, 0],    # O
    [0, 0, 2, 1, 0, -5],    # E
    [0, 0, 0, 1, -1, 0],    # P
]
LB_OV = [0, 0, 0, 0, 0, 0]
UB_OV = [None, O_MAX, None, None, None, None]
BIO_OV = 5
# Medium species: 0 = substrate s, 1 = by-product p.
E_OV = [
    [-1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
]
UPTAKES_OV = [(0, 0, VMAX, KM)]


def overflow_rates(u: float, o_max: float = O_MAX):
    """Closed form of the FBA optimum of the overflow network at uptake u.

    Returns (mu, secretion of P). Respiration only if u <= 3 o_max.
    """
    if u <= 3 * o_max:
        return 2 * u / 15, 0.0
    return (u + o_max) / 10, (u - 3 * o_max) / 2
