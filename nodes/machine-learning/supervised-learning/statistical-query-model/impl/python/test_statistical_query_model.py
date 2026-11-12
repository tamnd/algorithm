# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-query-model/. The authors are listed in prov/ASCCKX.jsonl.

import math
import random
from itertools import product

from statistical_query_model import (AdversarialOracle, NoisySampleOracle, SampleOracle, adversary_answer,
                                     conjunction, error, expectation, fourier_coefficient, learn_conjunction,
                                     literal_value, parity, points, surviving_parities)


def random_conjunction(d: int, rng: random.Random) -> tuple[int, ...]:
    vs = rng.sample(range(d), rng.randint(0, min(3, d)))
    return tuple(sorted(2 * v + rng.getrandbits(1) for v in vs))


def test_learner_against_adversarial_oracles() -> None:
    rng = random.Random(1)
    for trial in range(60):
        d = rng.randint(2, 6)
        p = [rng.choice((0.5, rng.uniform(0.02, 0.98))) for _ in range(d)]
        lits = random_conjunction(d, rng)
        c = conjunction(lits)
        eps = rng.choice((0.05, 0.1, 0.3))
        for sign in (1, -1, 0):
            o = AdversarialOracle(c, p, sign, seed=trial)
            h = learn_conjunction(o, d, eps)
            assert o.calls == 2 * d
            assert set(lits) <= set(h)
            hc = conjunction(h)
            assert all(c(x) == 1 for x, w in points(p) if hc(x) == 1)  # no false positives
            assert error(hc, c, p) <= eps + 1e-12


def test_sample_oracle_is_within_tolerance() -> None:
    rng = random.Random(2)
    d, p = 4, [0.3, 0.5, 0.7, 0.9]
    c = conjunction((0, 5))
    queries = [lambda x, y, j=j: float(literal_value(j, x) == 0 and y == 1) for j in range(2 * d)]
    o = SampleOracle(c, p, len(queries), 0.05, rng)
    assert o.sample_size(0.05) == math.ceil(math.log(2 * 8 / 0.05) / (2 * 0.05 ** 2))
    for chi in queries:
        assert abs(o.stat(chi, 0.05) - expectation(chi, c, p)) <= 0.05


def test_noise_identity_is_exact() -> None:
    rng = random.Random(3)
    d, p, eta = 3, [0.2, 0.5, 0.6], 0.3
    c = conjunction((1, 4))
    for _ in range(20):
        table = {(x, y): rng.random() for x in product((0, 1), repeat=d) for y in (0, 1)}
        chi = lambda x, y: table[(x, y)]
        noisy = sum(w * ((1 - eta) * chi(x, c(x)) + eta * chi(x, 1 - c(x))) for x, w in points(p))
        s = sum(w * (chi(x, 0) + chi(x, 1)) for x, w in points(p))
        assert abs((noisy - eta * s) / (1 - 2 * eta) - expectation(chi, c, p)) < 1e-12


def test_learning_from_noisy_examples() -> None:
    d, eps, eta = 3, 0.5, 0.2
    p = [0.5, 0.9, 0.5]
    lits = (0, 3)
    c = conjunction(lits)
    o = NoisySampleOracle(c, p, eta, 2 * d, 0.1, random.Random(4))
    h = learn_conjunction(o, d, eps)
    assert set(lits) <= set(h)
    assert error(conjunction(h), c, p) <= eps


def test_parity_answers_differ_by_half_a_fourier_coefficient() -> None:
    rng = random.Random(5)
    d = 4
    xs = list(product((0, 1), repeat=d))
    for _ in range(10):
        table = {(x, y): rng.random() for x in xs for y in (0, 1)}
        chi = lambda x, y: table[(x, y)]
        h = lambda x: chi(x, 1) - chi(x, 0)
        a = adversary_answer(chi, d)
        total = 0.0
        for s in product((0, 1), repeat=d):
            hs = fourier_coefficient(h, s, d)
            truth = sum(chi(x, parity(s)(x)) for x in xs) / len(xs)
            assert abs(truth - (a - hs / 2)) < 1e-12
            total += hs * hs
        assert abs(total - sum(h(x) ** 2 for x in xs) / len(xs)) < 1e-12  # Parseval


def test_each_query_rules_out_few_parities() -> None:
    rng = random.Random(6)
    d, tau = 5, 0.1
    xs = list(product((0, 1), repeat=d))
    queries = []
    for _ in range(6):
        table = {(x, y): rng.random() for x in xs for y in (0, 1)}
        queries.append(lambda x, y, t=table: t[(x, y)])
    for _ in range(4):
        t = tuple(rng.getrandbits(1) for _ in range(d))
        queries.append(lambda x, y, t=t: float(y == parity(t)(x)))
    queries.append(lambda x, y: float(y == x[0]))
    for chi in queries:
        assert 2 ** d - len(surviving_parities([chi], tau, d)) <= 1 / (4 * tau * tau)
    alive = surviving_parities(queries, tau, d)
    assert len(alive) >= 2 ** d - len(queries) / (4 * tau * tau)
    assert len(alive) >= 2  # so some parity is still possible and the learner errs on one of two
