# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lennard-jones-potential/. The authors are listed in prov/3RCYBF.jsonl.

import math
from typing import Optional

Point = list[float]


def phi(r: float, eps: float = 1.0, sigma: float = 1.0) -> float:
    """The full Lennard-Jones pair energy 4 eps ((sigma/r)^12 - (sigma/r)^6)."""
    x = (sigma / r) ** 6
    return 4 * eps * (x * x - x)


def pair_force(r: float, eps: float = 1.0, sigma: float = 1.0) -> float:
    """f(r) = -dphi/dr = 24 eps (2 (sigma/r)^12 - (sigma/r)^6) / r; positive means repulsive."""
    x = (sigma / r) ** 6
    return 24 * eps * (2 * x * x - x) / r


def pair(r: float, rc: Optional[float], variant: str = "truncated", eps: float = 1.0, sigma: float = 1.0) -> tuple[float, float]:
    """Energy and force magnitude of one pair at distance r.

    variant is "full" (no cutoff), "truncated" (zero beyond rc),
    "shifted" (phi(r) - phi(rc) inside rc) or "shifted-force"
    (phi(r) - phi(rc) - (r - rc) phi'(rc) inside rc).
    """
    if variant == "full":
        return phi(r, eps, sigma), pair_force(r, eps, sigma)
    if rc is None or r >= rc:  # @line L3
        if rc is None:
            raise ValueError("this variant needs a cutoff")
        return 0.0, 0.0  # @line L3
    x = (sigma / r) ** 6  # @line L4
    u = 4 * eps * (x * x - x)  # @line L5
    f = 24 * eps * (2 * x * x - x) / r  # @line L5
    if variant == "shifted":
        u -= phi(rc, eps, sigma)  # @line L6
    elif variant == "shifted-force":
        fc = pair_force(rc, eps, sigma)
        u += -phi(rc, eps, sigma) + (r - rc) * fc  # @line L6
        f -= fc  # @line L6
    elif variant != "truncated":
        raise ValueError("unknown variant")
    return u, f


def energy_forces(
    positions: list[Point],
    rc: Optional[float] = None,
    variant: str = "full",
    box: Optional[float] = None,
    eps: float = 1.0,
    sigma: float = 1.0,
) -> tuple[float, list[Point]]:
    """Total energy and the force on each atom, by the direct loop over pairs.

    With box set, distances use the minimum image in a cubic periodic box,
    and the cutoff must be at most box / 2.
    """
    if box is not None and (rc is None or rc > box / 2):
        raise ValueError("a periodic box needs a cutoff of at most half the box")
    n = len(positions)
    dim = len(positions[0]) if n else 3
    u_total = 0.0  # @line L1
    forces = [[0.0] * dim for _ in range(n)]  # @line L1
    for i in range(n):  # @line L2
        for j in range(i + 1, n):  # @line L2
            d = [positions[i][a] - positions[j][a] for a in range(dim)]
            if box is not None:
                d = [x - box * round(x / box) for x in d]
            r = math.sqrt(sum(x * x for x in d))  # @line L3
            u, f = pair(r, rc, variant, eps, sigma)
            u_total += u  # @line L7
            for a in range(dim):
                forces[i][a] += f * d[a] / r  # @line L7
                forces[j][a] -= f * d[a] / r  # @line L7
    return u_total, forces  # @line L8


def tail_energy_per_atom(rho: float, rc: float, eps: float = 1.0, sigma: float = 1.0) -> float:
    """U_tail / N = (8/3) pi rho eps sigma^3 ((1/3)(sigma/rc)^9 - (sigma/rc)^3), for g(r) = 1 beyond rc."""
    x = sigma / rc
    return (8 / 3) * math.pi * rho * eps * sigma ** 3 * (x ** 9 / 3 - x ** 3)


def tail_pressure(rho: float, rc: float, eps: float = 1.0, sigma: float = 1.0) -> float:
    """P_tail = (16/3) pi rho^2 eps sigma^3 ((2/3)(sigma/rc)^9 - (sigma/rc)^3), for g(r) = 1 beyond rc."""
    x = sigma / rc
    return (16 / 3) * math.pi * rho * rho * eps * sigma ** 3 * (2 * x ** 9 / 3 - x ** 3)


def reduced_time_unit(sigma_m: float, eps_over_kb: float, mass_kg: float) -> float:
    """tau = sigma sqrt(m / eps) in seconds."""
    kb = 1.380649e-23
    return sigma_m * math.sqrt(mass_kg / (eps_over_kb * kb))
