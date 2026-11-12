# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wake-sleep-algorithm/. The authors are listed in prov/08MB4F.jsonl.

import itertools
import math
import random

from wake_sleep_algorithm import (avg_log_likelihood, elbo, hidden_states, init_params, log_marginal, log_p_joint, log_q,
                                  sleep_delta, wake_delta, wake_sleep)

# Two bars: the left pair and the right pair of four pixels, each on or off independently.
DATA = [(1, 1, 0, 0), (0, 0, 1, 1), (1, 1, 1, 1), (0, 0, 0, 0)]
VISIBLE = list(itertools.product((0, 1), repeat=4))
# A generative model that does not fit DATA, with explaining away between the two hidden units.
GEN = ([0.0, 0.0], [-1.5, -1.5, -1.5, -1.5], [[3.0, 3.0], [3.0, 3.0], [0.0, 0.0], [0.0, 0.0]])


def flat(params):
    out = []
    for p in params:
        for x in p:
            out.extend(x if isinstance(x, list) else [x])
    return out


def rec_of(x):
    return (x[:2], [x[2:6], x[6:10]])


def gen_of(x):
    return (x[:2], x[2:6], [x[6 + 2 * i:8 + 2 * i] for i in range(4)])


def numeric_grad(f, x, e=1e-6):
    g = []
    for k in range(len(x)):
        xp, xm = x[:], x[:]
        xp[k] += e
        xm[k] -= e
        g.append((f(xp) - f(xm)) / (2 * e))
    return g


def expected_sleep_gradient(gen, rec):
    """sum over (h, v) of p(h, v) times the sleep update: the gradient of E_p[log q(h | v)]."""
    g = [0.0] * 10
    for v in VISIBLE:
        for h in hidden_states(2):
            w = math.exp(log_p_joint(gen, v, h))
            g = [a + w * b for a, b in zip(g, flat(sleep_delta(rec, h, v)))]
    return g


def elbo_gradient(gen, rec):
    """The exact gradient of the average ELBO over DATA in the recognition parameters."""
    g = [0.0] * 10
    for v in DATA:
        for h in hidden_states(2):
            lq = log_q(rec, h, v)
            w = math.exp(lq) * (log_p_joint(gen, v, h) - lq) / len(DATA)
            g = [a + w * b for a, b in zip(g, flat(sleep_delta(rec, h, v)))]
    return g


def test_enumerated_log_likelihood_improves():
    rng = random.Random(0)
    gen, rec = init_params(2, 4, rng)
    start = avg_log_likelihood(gen, DATA)
    gen, rec = wake_sleep(DATA, 2, 20000, rng, init=(gen, rec))
    end = avg_log_likelihood(gen, DATA)
    assert round(start, 4) == -2.7761 and round(end, 4) == -1.4544
    assert end > -1.5 and end <= -math.log(4)  # -log 4 is the best possible value
    bound = sum(elbo(gen, rec, v) for v in DATA) / len(DATA)
    assert round(bound, 4) == -1.4802 and bound <= end
    # The model found the two bars: each hidden unit drives one pair of pixels.
    W = gen[2]
    assert W[0][0] > 5 and W[1][0] > 5 and W[2][1] > 5 and W[3][1] > 5
    assert max(abs(W[0][1]), abs(W[1][1]), abs(W[2][0]), abs(W[3][0])) < 1


def test_likelihood_improves_on_other_seeds():
    for seed in range(1, 6):
        rng = random.Random(seed)
        gen, rec = init_params(2, 4, rng)
        start = avg_log_likelihood(gen, DATA)
        gen, _ = wake_sleep(DATA, 2, 20000, rng, init=(gen, rec))
        assert avg_log_likelihood(gen, DATA) > start + 1.2


def test_wake_update_is_the_gradient_of_the_expected_complete_log_likelihood():
    rng = random.Random(4)
    gen, rec = init_params(2, 4, rng, scale=1.0)
    for v in DATA:
        expected = [0.0] * 14
        for h in hidden_states(2):
            w = math.exp(log_q(rec, h, v))
            expected = [a + w * b for a, b in zip(expected, flat(wake_delta(gen, v, h)))]

        def f(x):
            return sum(math.exp(log_q(rec, h, v)) * log_p_joint(gen_of(x), v, h) for h in hidden_states(2))
        assert max(abs(a - b) for a, b in zip(expected, numeric_grad(f, flat(gen)))) < 1e-7
        # The entropy of q does not depend on the generative model, so this is also the ELBO gradient.
        fd = numeric_grad(lambda x: elbo(gen_of(x), rec, v), flat(gen))
        assert max(abs(a - b) for a, b in zip(expected, fd)) < 1e-7


def test_sleep_update_is_the_gradient_of_the_expected_recognition_log_likelihood():
    rng = random.Random(5)
    _, rec = init_params(2, 4, rng, scale=1.0)

    def f(x):
        r = rec_of(x)
        return sum(math.exp(log_p_joint(GEN, v, h)) * log_q(r, h, v) for v in VISIBLE for h in hidden_states(2))
    fd = numeric_grad(f, flat(rec))
    assert max(abs(a - b) for a, b in zip(expected_sleep_gradient(GEN, rec), fd)) < 1e-7
    assert max(abs(a - b) for a, b in zip(elbo_gradient(GEN, rec), numeric_grad(
        lambda x: sum(elbo(GEN, rec_of(x), v) for v in DATA) / len(DATA), flat(rec)))) < 1e-7


def test_sleep_phase_does_not_maximize_the_elbo():
    sleep_x, elbo_x = [0.0] * 10, [0.0] * 10
    for _ in range(3000):
        sleep_x = [a + 0.5 * b for a, b in zip(sleep_x, expected_sleep_gradient(GEN, rec_of(sleep_x)))]
        elbo_x = [a + 0.5 * b for a, b in zip(elbo_x, elbo_gradient(GEN, rec_of(elbo_x)))]
    assert max(map(abs, expected_sleep_gradient(GEN, rec_of(sleep_x)))) < 1e-8
    assert max(map(abs, elbo_gradient(GEN, rec_of(elbo_x)))) < 1e-8
    at_sleep = sum(elbo(GEN, rec_of(sleep_x), v) for v in DATA) / len(DATA)
    at_best = sum(elbo(GEN, rec_of(elbo_x), v) for v in DATA) / len(DATA)
    loglik = avg_log_likelihood(GEN, DATA)
    assert (round(at_sleep, 4), round(at_best, 4), round(loglik, 4)) == (-3.0847, -3.0701, -3.0161)
    assert at_sleep < at_best < loglik
    assert all(log_marginal(GEN, v) <= 0 for v in DATA)
