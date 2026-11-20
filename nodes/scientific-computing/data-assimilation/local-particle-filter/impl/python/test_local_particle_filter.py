# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-particle-filter/. The authors are listed in prov/7NZNER.jsonl.

import math
import random

from local_particle_filter import (
    local_particle_filter,
    local_pf_analysis,
    local_weights,
    normalize,
    systematic_resample,
)


def global_bootstrap_analysis(particles, obs, u):
    """Reference: global weights from all observations, then systematic resampling of whole particles."""
    logw = [-0.5 * sum((y - x[pos]) ** 2 / r for pos, y, r in obs) for x in particles]
    w = normalize(logw)
    N = len(particles)
    out = []
    for i in range(N):
        t = (i + u) / N
        k = 0
        while k < N - 1 and sum(w[: k + 1]) < t:
            k += 1
        out.append(list(particles[k]))
    return out


def test_page_example():
    # Particles (0, 0) and (1, 1), y = (1, 0), r = 1/2, radius 0 and u = 0.45: the new particles are (0, 0) and (1, 0).
    obs = [(0, 1.0, 0.5), (1, 0.0, 0.5)]
    W = local_weights([[0.0, 0.0], [1.0, 1.0]], obs, 0)
    small = math.exp(-1.0) / (1.0 + math.exp(-1.0))
    assert abs(W[0][0] - small) < 1e-12 and abs(W[1][1] - small) < 1e-12
    new = local_pf_analysis([[0.0, 0.0], [1.0, 1.0]], obs, 0, 0.45)
    assert new == [[0.0, 0.0], [1.0, 0.0]]


def test_systematic_resampling_against_inverse_cdf():
    rng = random.Random(2)
    for _ in range(200):
        N = rng.randint(1, 12)
        w = normalize([rng.gauss(0, 2) for _ in range(N)])
        u = rng.random()
        pick = systematic_resample(w, u)
        for i, k in enumerate(pick):
            t = (i + u) / N
            ref = next((m for m in range(N) if sum(w[: m + 1]) >= t), N - 1)
            assert k == ref
        for m in range(N):
            assert math.floor(N * w[m]) - 1e-9 <= pick.count(m) <= math.ceil(N * w[m]) + 1e-9


def test_infinite_radius_is_global_bootstrap_filter():
    rng = random.Random(9)
    n, N = 6, 15
    particles = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
    obs = [(j, rng.gauss(0, 1), 0.7) for j in (0, 2, 3, 5)]
    for u in (0.0, 0.31, 0.77):
        assert local_pf_analysis(particles, obs, None, u) == global_bootstrap_analysis(particles, obs, u)


def test_local_weighted_mean_matches_kalman_filter():
    # Independent N(0, 1) components, each observed with r = 1/2: the posterior mean is y / 1.5 at every point.
    rng = random.Random(4)
    n, N = 6, 4000
    particles = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
    y = [rng.gauss(0, 1.2) for _ in range(n)]
    W = local_weights(particles, [(j, y[j], 0.5) for j in range(n)], 0)
    for j in range(n):
        mean = sum(W[j][i] * particles[i][j] for i in range(N))
        assert abs(mean - y[j] / 1.5) < 0.05


def run_twin(radius, seeds):
    a, q, R = 0.9, 0.5, 0.5
    n, N, T = 40, 50, 20

    def step(x, rng):
        return [a * v + math.sqrt(q) * rng.gauss(0, 1) for v in x]

    pf = kf = 0.0
    for s in seeds:
        rng, trng = random.Random(7 + s), random.Random(70 + s)
        truth = [trng.gauss(0, 1) for _ in range(n)]
        observations, states = [], []
        for _ in range(T):
            truth = [a * v + math.sqrt(q) * trng.gauss(0, 1) for v in truth]
            states.append(truth)
            observations.append([(j, truth[j] + math.sqrt(R) * trng.gauss(0, 1), R) for j in range(n)])
        history = local_particle_filter([[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)], step, observations, radius, rng)
        m, v = [0.0] * n, [1.0] * n
        for k in range(T):
            m = [a * x for x in m]
            v = [a * a * x + q for x in v]
            g = [x / (x + R) for x in v]
            m = [mi + gi * (o[1] - mi) for mi, gi, o in zip(m, g, observations[k])]
            v = [(1 - gi) * x for gi, x in zip(g, v)]
            if k >= 5:
                mean = [sum(p[j] for p in history[k]) / N for j in range(n)]
                pf += math.sqrt(sum((mean[j] - states[k][j]) ** 2 for j in range(n)) / n)
                kf += math.sqrt(sum((m[j] - states[k][j]) ** 2 for j in range(n)) / n)
    return pf / kf


def test_cycled_twin_local_tracks_kalman_filter_global_does_not():
    # 40 independent AR(1) components, 50 particles: a measurement, not a theorem.
    assert run_twin(0, range(3)) < 1.1
    assert run_twin(None, range(3)) > 1.8


def test_weight_collapse_grows_with_dimension_only_for_global_weights():
    N = 100
    result = {}
    for n in (10, 40, 160):
        g_max = l_max = 0.0
        for s in range(10):
            rng = random.Random(1000 * n + s)
            particles = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
            obs = [(j, rng.gauss(0, 1) + rng.gauss(0, 1), 1.0) for j in range(n)]
            g = normalize([-0.5 * sum((y - x[p]) ** 2 / r for p, y, r in obs) for x in particles])
            W = local_weights(particles, obs, 2)
            g_max += max(g) / 10
            l_max += sum(max(w) for w in W) / n / 10
        result[n] = (g_max, l_max)
    assert result[10][0] < result[40][0] < result[160][0]
    assert result[160][0] > 0.7
    assert all(l < 0.15 for _, l in result.values())
