# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-particle-filter/. The authors are listed in prov/7NZNER.jsonl.

"""Local particle filter: an analysis step with local weights and local resampling.

The state has n grid points on a ring. An observation o measures one grid
point pos_o with the value y_o and the error variance r_o. Particle i
gets at grid point j the local log weight

    log w_i(j) = -1/2 sum_o rho(dist(j, pos_o)) (y_o - x_i[pos_o])^2 / r_o,

where rho is a taper that is 1 at distance 0 and 0 far away, as in the
observation localization of the LETKF. At each grid point the weights are
normalized and resampled with systematic resampling. One offset u is used
at all grid points, so neighboring points with similar weights pick the
same particles. Component j of the new particle i is component j of the
old particle that grid point j picks.

With radius None the taper is 1 everywhere, all grid points have the same
weights and pick the same particles, and the step is the analysis step of
the global bootstrap particle filter with systematic resampling.
"""

import math


def gaspari_cohn(r, c):
    """Return the Gaspari-Cohn fifth order taper at distance r for the half-width c (zero beyond 2c)."""
    z = abs(r) / c
    if z <= 1.0:
        return -0.25 * z**5 + 0.5 * z**4 + 0.625 * z**3 - (5.0 / 3.0) * z**2 + 1.0
    if z <= 2.0:
        return z**5 / 12.0 - 0.5 * z**4 + 0.625 * z**3 + (5.0 / 3.0) * z**2 - 5.0 * z + 4.0 - 2.0 / (3.0 * z)
    return 0.0


def taper(d, radius):
    """Return rho(d): 1 for radius None, the indicator of d = 0 for radius 0, else Gaspari-Cohn."""
    if radius is None:
        return 1.0
    if radius == 0:
        return 1.0 if d == 0 else 0.0
    return gaspari_cohn(d, radius)


def ring_distance(j, k, n):
    """Return the distance between the grid points j and k on a ring of n points."""
    d = abs(j - k) % n
    return min(d, n - d)


def normalize(logw):
    """Return the normalized weights exp(logw) / sum, shifted by the maximum to avoid underflow."""
    top = max(logw)
    w = [math.exp(v - top) for v in logw]
    s = sum(w)
    return [v / s for v in w]


def systematic_resample(w, u):
    """Return N indices: index i is the particle whose cumulative weight interval holds (i + u) / N."""
    N = len(w)
    out = []
    c = w[0]
    k = 0
    for i in range(N):
        t = (i + u) / N
        while t > c and k < N - 1:
            k += 1
            c += w[k]
        out.append(k)
    return out


def local_weights(particles, obs, radius):
    """Return W with W[j] the normalized local weights of all particles at grid point j."""
    n = len(particles[0])
    N = len(particles)
    misfit = [[(y - x[pos]) ** 2 / r for pos, y, r in obs] for x in particles]
    W = []
    for j in range(n):
        rho = [taper(ring_distance(j, pos, n), radius) for pos, y, r in obs]
        near = [o for o in range(len(obs)) if rho[o] > 0.0]
        logw = [-0.5 * sum(rho[o] * misfit[i][o] for o in near) for i in range(N)]
        W.append(normalize(logw))
    return W


def local_pf_analysis(particles, obs, radius, u):
    """Return the new particles of one local particle filter analysis with the offset u in [0, 1)."""
    n = len(particles[0])  # @line L1
    N = len(particles)
    W = local_weights(particles, obs, radius)  # @line L2
    new = [[0.0] * n for _ in range(N)]  # @line L3
    for j in range(n):  # @line L4
        pick = systematic_resample(W[j], u)  # @line L5
        for i in range(N):  # @line L6
            new[i][j] = particles[pick[i]][j]  # @line L7
    return new  # @line L8


def local_particle_filter(particles, step, observations, radius, rng):
    """Cycle forecast and analysis. observations[k] is the list of (pos, y, r) at time k = 1, 2, ...

    step(x, rng) is one stochastic model step. Return the list of particle sets after each analysis.
    """
    history = []
    for obs in observations:
        particles = [step(x, rng) for x in particles]
        particles = local_pf_analysis(particles, obs, radius, rng.random())
        history.append(particles)
    return history
