# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perfectly-matched-layer/. The authors are listed in prov/D5V4KY.jsonl.
"""A graded perfectly matched layer for the one-dimensional Yee scheme.

Equations (units with eps = mu = c = 1): E_t + sigma E = H_x, H_t + sigma H = E_x.
With the same sigma in both equations the layer has the impedance of free
space, so in the continuous problem a wave enters it without reflection and
decays as exp(-integral of sigma). The grid has E at x_i = i dx, i = 0..n,
and H at x_{i+1/2}; E = 0 at both ends (a perfect conductor behind the layer).
"""

import math


def sigma_max_for(R, depth, m):
    """Peak conductivity that gives the reflection R of the continuous layer."""
    # @line L1: sigma_max from the target reflection, the depth D and the grading m
    return -(m + 1) * math.log(R) / (2 * depth)


def theoretical_reflection(sigma_max, depth, m, cos_theta=1.0):
    """R = exp(-2 cos(theta) integral_0^D sigma), for sigma = sigma_max (d / D)^m."""
    return math.exp(-2 * cos_theta * sigma_max * depth / (m + 1))


def profiles(n, npml, dx, sigma_max, m):
    """sigma at the E points and at the H points, graded into the layers at both ends."""
    D = npml * dx

    def depth(x):
        return max(npml * dx - x, x - (n - npml) * dx, 0.0)

    # @line L2: sigma(d) = sigma_max (d / D)^m at depth d inside the layer
    sE = [sigma_max * (depth(i * dx) / D) ** m if depth(i * dx) > 0 else 0.0
          for i in range(n + 1)]
    sH = [sigma_max * (depth((i + 0.5) * dx) / D) ** m if depth((i + 0.5) * dx) > 0 else 0.0
          for i in range(n)]
    return sE, sH


def pml_step(E, H, sE, sH, dx, dt):
    n = len(H)
    for i in range(n):
        s = sH[i] * dt / 2
        # @line L3: lossy H update (sigma averaged in time)
        H[i] = ((1 - s) * H[i] + dt / dx * (E[i + 1] - E[i])) / (1 + s)
    for i in range(1, n):
        s = sE[i] * dt / 2
        # @line L4: lossy E update
        E[i] = ((1 - s) * E[i] + dt / dx * (H[i] - H[i - 1])) / (1 + s)
    # @line L5: a conductor behind the layer
    E[0] = E[n] = 0.0


def simulate(n, npml, dx, dt, steps, sigma_max, m, pulse):
    """Run a right-moving pulse E = f(x - t), H = -f(x - t) and return E at the end."""
    sE, sH = profiles(n, npml, dx, sigma_max, m)
    E = [pulse(i * dx) for i in range(n + 1)]
    H = [-pulse((i + 0.5) * dx + dt / 2) for i in range(n)]
    E[0] = E[n] = 0.0
    for _ in range(steps):
        pml_step(E, H, sE, sH, dx, dt)
    return E


def reflection(npml, sigma_max, m, interior=200, dx=1.0, lam=0.5, width=6.0):
    """Largest reflected |E| in the interior, relative to a unit pulse.

    The reference is the same scheme on a domain so long at both ends that
    no wave reaches them, so numerical dispersion cancels in the difference.
    """
    dt = lam * dx
    x0 = (npml + interior / 2) * dx
    travel = interior / 2 + 2 * npml + interior / 4          # out, through the layer, back
    steps = int(travel / lam)
    n = interior + 2 * npml
    E = simulate(n, npml, dx, dt, steps, sigma_max, m,
                 lambda x: math.exp(-((x - x0) / width) ** 2))
    L = int(steps * lam) + 4 * int(width)                    # extra cells at each end
    E_ref = simulate(n + 2 * L, 0, dx, dt, steps, 0.0, 0,
                     lambda x: math.exp(-((x - x0 - L * dx) / width) ** 2))
    lo, hi = npml, npml + interior
    return max(abs(E[i] - E_ref[i + L]) for i in range(lo, hi + 1))
