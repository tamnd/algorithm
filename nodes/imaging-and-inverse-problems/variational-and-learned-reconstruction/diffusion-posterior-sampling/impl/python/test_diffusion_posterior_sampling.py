# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-posterior-sampling/. The authors are listed in prov/K0GFYT.jsonl.

import math
import random

from diffusion_posterior_sampling import (
    dps,
    gaussian_score,
    guidance_gradient,
    linear_alpha_bars,
    linear_dps_moments,
    schedule,
    tweedie,
)

N = 100
AB = linear_alpha_bars(N, 1e-3, 0.2)
BETAS = [schedule(AB, t)[2] for t in range(1, N + 1)]


def identity(x):
    return list(x)


def likelihood_steps(sig2, extra=None):
    """beta_t / (2 (sig2 + extra_t) sqrt(1 - beta_t)), the step of the reverse SDE."""
    out = []
    for t, bt in enumerate(BETAS, start=1):
        e = 0.0 if extra is None else extra(t)
        out.append(bt / (2.0 * (sig2 + e) * math.sqrt(1.0 - bt)))
    return out


def test_schedule_and_last_step():
    assert abs(AB[0] - 0.999) < 1e-15 and AB[-1] < 1e-4
    for t in range(2, N + 1):
        assert abs(schedule(AB, t)[0] - (1.0 - schedule(AB, t)[2]) * AB[t - 2]) < 1e-15
    # With one step and no guidance the output is the Tweedie estimate.
    score, vjp = gaussian_score([0.6], [2.0])
    x = dps([0.0], identity, identity, score, vjp, [0.6], 0.0, random.Random(0),
            normalize=False, x_start=[1.5])
    v = 0.6 * 2.0 + 0.4
    assert abs(x[0] - math.sqrt(0.6) * 2.0 / v * 1.5) < 1e-12


def test_tweedie_is_the_posterior_mean_for_a_gaussian_prior():
    prior = [0.5, 3.0]
    score, _ = gaussian_score(AB, prior)
    for t in (1, 10, 50, 100):
        ab = AB[t - 1]
        x = [0.7, -1.3]
        got = tweedie(x, score(x, t), ab)
        for j in range(2):
            exact = math.sqrt(ab) * prior[j] / (ab * prior[j] + 1.0 - ab) * x[j]
            assert abs(got[j] - exact) < 1e-12


def test_guidance_gradient_matches_finite_differences():
    rng = random.Random(3)
    n, m = 3, 2
    u = [[rng.gauss(0.0, 0.5) for _ in range(n)] for _ in range(n)]
    w = [[rng.gauss(0.0, 0.5) for _ in range(n)] for _ in range(n)]
    a = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(m)]
    y = [0.4, -0.9]

    def score(x, t):
        h = [math.tanh(sum(wr[j] * x[j] for j in range(n))) for wr in w]
        return [-x[i] + sum(u[i][k] * h[k] for k in range(n)) for i in range(n)]

    def score_vjp(x, t, v):
        h = [math.tanh(sum(wr[j] * x[j] for j in range(n))) for wr in w]
        q = [(1.0 - h[k] ** 2) * sum(u[i][k] * v[i] for i in range(n)) for k in range(n)]
        return [-v[j] + sum(w[k][j] * q[k] for k in range(n)) for j in range(n)]

    def apply_a(x):
        return [sum(r[j] * x[j] for j in range(n)) for r in a]

    def apply_at(r):
        return [sum(a[i][j] * r[i] for i in range(m)) for j in range(n)]

    ab, t = 0.4, 7

    def objective(x):
        x0 = tweedie(x, score(x, t), ab)
        return sum((p - q) ** 2 for p, q in zip(apply_a(x0), y))

    x = [0.3, -0.5, 1.2]
    g, _ = guidance_gradient(x, t, ab, tweedie(x, score(x, t), ab), y,
                             apply_a, apply_at, score_vjp)
    h = 1e-6
    for j in range(n):
        xp, xm = list(x), list(x)
        xp[j] += h
        xm[j] -= h
        assert abs((objective(xp) - objective(xm)) / (2 * h) - g[j]) < 1e-6


def test_monte_carlo_matches_the_exact_law_of_the_sampler():
    score, vjp = gaussian_score(AB, [1.0])
    steps = likelihood_steps(0.25)
    mean, var = linear_dps_moments(1.0, 1.0, AB, 1.0, steps)
    assert abs(mean - 0.98458) < 1e-5 and abs(var - 0.09976) < 1e-5
    rng = random.Random(1)
    count = 1500
    xs = [dps([1.0], identity, identity, score, vjp, AB, steps, rng,
              normalize=False, n=1)[0] for _ in range(count)]
    m = sum(xs) / count
    v = sum((x - m) ** 2 for x in xs) / (count - 1)
    assert abs(m - mean) < 4.0 * math.sqrt(var / count)
    assert abs(v - var) < 5.0 * var * math.sqrt(2.0 / count)


def test_dps_is_not_the_exact_posterior():
    # Prior N(0, 1), A = 1, noise variance 0.25, y = 1: posterior N(0.8, 0.2).
    long_ab = linear_alpha_bars(1000, 1e-4, 0.02)
    long_b = [schedule(long_ab, t)[2] for t in range(1, 1001)]
    dps_steps = [b / (0.5 * math.sqrt(1.0 - b)) for b in long_b]
    mean, var = linear_dps_moments(1.0, 1.0, long_ab, 1.0, dps_steps)
    assert abs(mean - 0.98197) < 1e-5 and abs(var - 0.12167) < 1e-5
    # The same sampler with the exact p(y | x_t), whose variance is
    # 0.25 + Var(x_0 | x_t) = 0.25 + 1 - alpha_bar_t, is close to the posterior.
    exact_steps = [b / (2.0 * (1.25 - long_ab[t]) * math.sqrt(1.0 - b))
                   for t, b in enumerate(long_b)]
    mean_e, var_e = linear_dps_moments(1.0, 1.0, long_ab, 1.0, exact_steps)
    assert abs(mean_e - 0.8) < 1e-4 and abs(var_e - 0.2) < 0.005


def test_normalized_step_on_a_noiseless_inpainting_problem():
    # Prior N(0, I_2), observe the first entry exactly: y = 1.
    score, vjp = gaussian_score(AB, [1.0, 1.0])
    apply_a = lambda x: [x[0]]
    apply_at = lambda r: [r[0], 0.0]
    rng, free = random.Random(4), random.Random(4)
    for _ in range(200):
        x = dps([1.0], apply_a, apply_at, score, vjp, AB, 0.1, rng, n=2)
        z = dps([1.0], apply_a, apply_at, score, vjp, AB, 0.0, free, n=2)
        # The step has length about 2 zeta, so the error does not go below it.
        assert abs(x[0] - 1.0) < 0.21
        # The unobserved entry gets no guidance and follows the prior sampler.
        assert x[1] == z[1]


def test_one_call_of_each_operator_per_step():
    calls = {"score": 0, "vjp": 0, "a": 0, "at": 0}
    score, vjp = gaussian_score(AB, [1.0])

    def counted(name, f):
        def g(*args):
            calls[name] += 1
            return f(*args)
        return g

    dps([0.5], counted("a", identity), counted("at", identity), counted("score", score),
        counted("vjp", vjp), AB, 0.3, random.Random(2), n=1)
    assert calls == {"score": N, "vjp": N, "a": N, "at": N}
