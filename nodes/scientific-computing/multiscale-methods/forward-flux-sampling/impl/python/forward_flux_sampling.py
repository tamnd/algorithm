# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-flux-sampling/. The authors are listed in prov/0GTKCK.jsonl.
"""Forward flux sampling, direct version (Allen, Warren and ten Wolde 2005).

An order parameter lam(x) and interfaces lam_0 < lam_1 < ... < lam_n
separate the state A (in_a(x) is True, and lam < lam_0 there) from the
state B (lam >= lam_n). The rate constant from A to B is

    k_AB = Phi_A0 * P(lam_1 | lam_0) * ... * P(lam_n | lam_(n-1)),

where Phi_A0 is the flux of first crossings of lam_0 by trajectories that
come from A, per unit of time spent in the region of A (the time since the
last visit to A rather than to B), and P(lam_(i+1) | lam_i) is the
probability that a trajectory at its first crossing of lam_i reaches
lam_(i+1) before it returns to A.

The flux and the first point set come from one long run in the region of
A. Each later stage fires trial runs from points picked at random in the
set of the previous stage, and keeps the end points of the runs that reach
the next interface. Only forward simulation is needed, so the dynamics
need not be reversible or in equilibrium.
"""

from typing import Callable


def forward_flux_sampling(x0, step: Callable, lam: Callable, in_a: Callable, interfaces, rng,
                          n_flux_steps: int, n_trials: int, max_trial_steps: int = 10**6):
    """Estimate k_AB per unit of time step.

    Returns (rate, flux, probabilities, work): the rate estimate, the flux
    estimate, the list of the n estimated crossing probabilities, and the
    number of dynamics steps used. Time is counted in steps.
    """
    lam_0, lam_b = interfaces[0], interfaces[-1]
    x = x0
    in_region_a, armed = True, True
    time_a, crossings = 0, 0
    points = []
    work = 0
    for _ in range(n_flux_steps):                                       # @line L1
        x = step(x, rng)
        work += 1
        if lam(x) >= lam_b:
            in_region_a = False
        elif in_a(x):
            in_region_a, armed = True, True
        if in_region_a:
            time_a += 1
            if armed and lam(x) >= lam_0:
                crossings += 1
                points.append(x)
                armed = False
    flux = crossings / time_a if time_a else 0.0
    probabilities = []
    if not points:
        return 0.0, flux, probabilities, work
    for i in range(len(interfaces) - 1):                                # @line L2
        target = interfaces[i + 1]
        reached = []
        for _ in range(n_trials):
            y = rng.choice(points)                                      # @line L3
            steps = 0
            while lam(y) < target and not in_a(y):                      # @line L4
                if steps == max_trial_steps:
                    raise RuntimeError("forward_flux_sampling: a trial run did not end")
                y = step(y, rng)
                steps += 1
            work += steps
            if lam(y) >= target:
                reached.append(y)                                       # @line L5
        p = len(reached) / n_trials                                     # @line L6
        probabilities.append(p)
        if p == 0.0:
            return 0.0, flux, probabilities, work
        points = reached
    rate = flux
    for p in probabilities:
        rate *= p
    return rate, flux, probabilities, work                              # @line L7
