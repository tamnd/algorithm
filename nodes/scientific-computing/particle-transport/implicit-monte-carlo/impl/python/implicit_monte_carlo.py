# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-monte-carlo/. The authors are listed in prov/CX3297.jsonl.
"""Implicit Monte Carlo (Fleck and Cummings) for grey radiation in one zone.

The zone is infinite and uniform, so space and direction drop out. The
radiation energy density E_r and the material temperature T obey

    dE_r/dt     = c sigma (a T^4 - E_r),
    c_v dT/dt   = c sigma (E_r - a T^4),

and E_r + c_v T is constant. One IMC step of size dt freezes the
temperature-dependent data at the start of the step and uses the Fleck
factor

    beta = 4 a T^3 / c_v,   f = 1 / (1 + beta c sigma dt).

During the step the material emits f c sigma a T^4 per unit time. A
radiation particle collides at rate c sigma; at a collision it is
absorbed with probability f, and with probability 1 - f it goes on as if
scattered ("effective scattering"). Particles that reach the end of the
step go to census. The material energy changes by the absorbed energy
minus the emitted energy, so the total energy is conserved exactly.

Since this zone has no space or direction, the census can be merged into
equal-weight particles without loss; a code with space cannot do that.
"""

import math


def uniform_open(rng) -> float:
    return 1.0 - rng.random()


def imc_step(temp, census, dt, n_emit, rng, a=1.0, c=1.0, sigma=1.0, cv=1.0, n_census=None):
    """One IMC step. census is a list of particle energies.

    Returns (new temperature, new census list, info dict).
    """
    beta = 4.0 * a * temp ** 3 / cv  # @line L1
    f = 1.0 / (1.0 + beta * c * sigma * dt)
    e_emit = f * c * sigma * a * temp ** 4 * dt  # @line L2
    particles = [(w, dt) for w in census]
    if n_emit > 0 and e_emit > 0.0:
        w = e_emit / n_emit
        particles += [(w, dt * (1.0 - rng.random())) for _ in range(n_emit)]  # time left after birth
    e_abs = 0.0
    out = []
    for w, t_left in particles:  # @line L3
        while True:  # @line L4
            d_coll = -math.log(uniform_open(rng)) / sigma
            if d_coll >= c * t_left:  # @line L5
                out.append(w)
                break
            t_left -= d_coll / c  # @line L6
            if rng.random() < f:  # @line L7
                e_abs += w
                break
            continue  # @line L8 (effective scattering: the particle goes on)
    new_temp = temp + (e_abs - e_emit) / cv  # @line L9
    if n_census is not None and len(out) > n_census:  # @line L10
        total = sum(out)
        out = [total / n_census] * n_census
    info = {"f": f, "emitted": e_emit, "absorbed": e_abs, "launched_w2": sum(w * w for w, _ in particles)}
    return new_temp, out, info


def expected_census(e_r, temp, dt, a=1.0, c=1.0, sigma=1.0, cv=1.0):
    """Exact mean radiation energy after one IMC step (the step's own linear model)."""
    beta = 4.0 * a * temp ** 3 / cv
    f = 1.0 / (1.0 + beta * c * sigma * dt)
    x = f * c * sigma * dt
    return e_r * math.exp(-x) + a * temp ** 4 * (1.0 - math.exp(-x))


def equilibrium_temperature(total, a=1.0, cv=1.0):
    """Solve a T^4 + c_v T = total by bisection."""
    lo, hi = 0.0, max(total / cv, (total / a) ** 0.25)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if a * mid ** 4 + cv * mid < total:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
