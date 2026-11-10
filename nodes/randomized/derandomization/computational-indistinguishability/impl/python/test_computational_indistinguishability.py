# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/computational-indistinguishability/. The authors are listed in prov/SBVWAV.jsonl.

import random
from fractions import Fraction
from itertools import product

from computational_indistinguishability import (
    accept_prob,
    advantage,
    best_test,
    hybrid_gaps,
    output_dist,
    prg_hybrids,
    product_hybrids,
    statistical_distance,
    uniform,
    yao_predictor_success,
)


def g_example(s):
    a, b = s
    return (a | b, a & b, a ^ b)


def majority(z):
    return 1 if 2 * sum(z) > len(z) else 0


def random_gen(rng, d, m):
    table = {s: tuple(rng.randrange(2) for _ in range(m)) for s in product((0, 1), repeat=d)}
    return lambda s: table[tuple(s)]


def random_test(rng, m):
    accept = {z for z in product((0, 1), repeat=m) if rng.randrange(2)}
    return lambda z: 1 if tuple(z) in accept else 0


def test_worked_example() -> None:
    hybrids = prg_hybrids(g_example, 2, 3)
    probs = [accept_prob(majority, h) for h in hybrids]
    assert probs == [Fraction(1, 2), Fraction(5, 8), Fraction(1, 2), Fraction(3, 4)]
    gaps = hybrid_gaps(majority, hybrids)
    assert gaps == [Fraction(1, 8), Fraction(-1, 8), Fraction(1, 4)]
    assert sum(gaps) == advantage(majority, output_dist(g_example, 2), uniform(3)) == Fraction(1, 4)
    assert yao_predictor_success(g_example, 2, 3, majority, 3) == Fraction(3, 4)
    assert yao_predictor_success(g_example, 2, 3, majority, 2) == Fraction(3, 8)


def test_end_hybrids() -> None:
    hybrids = prg_hybrids(g_example, 2, 3)
    assert hybrids[0] == uniform(3)
    assert hybrids[-1] == output_dist(g_example, 2)
    for h in hybrids:
        assert sum(h.values()) == 1


def test_telescoping_and_some_large_gap() -> None:
    rng = random.Random(7)
    for _ in range(500):
        d = rng.randrange(1, 4)
        m = rng.randrange(1, 5)
        gen = random_gen(rng, d, m)
        test = random_test(rng, m)
        hybrids = prg_hybrids(gen, d, m)
        gaps = hybrid_gaps(test, hybrids)
        total = advantage(test, output_dist(gen, d), uniform(m))
        assert sum(gaps) == total
        assert max(abs(g) for g in gaps) * m >= abs(total)


def test_predictor_matches_gap() -> None:
    rng = random.Random(11)
    for _ in range(200):
        d = rng.randrange(1, 4)
        m = rng.randrange(1, 5)
        gen = random_gen(rng, d, m)
        test = random_test(rng, m)
        probs = [accept_prob(test, h) for h in prg_hybrids(gen, d, m)]
        for i in range(1, m + 1):
            want = Fraction(1, 2) + probs[i] - probs[i - 1]
            assert yao_predictor_success(gen, d, m, test, i) == want


def test_statistical_distance_is_best_advantage() -> None:
    rng = random.Random(3)
    for m in (1, 2):
        tests = [lambda z, t=t, m=m: (t >> int("".join(map(str, z)) or "0", 2)) & 1 for t in range(2 ** (2**m))]
        for _ in range(100):
            gen = random_gen(rng, 2, m)
            p, q = output_dist(gen, 2), uniform(m)
            best = max(abs(advantage(t, p, q)) for t in tests)
            assert best == statistical_distance(p, q)
            assert advantage(best_test(p, q), p, q) == statistical_distance(p, q)


def test_many_samples_hybrid() -> None:
    rng = random.Random(5)
    for _ in range(100):
        gen = random_gen(rng, 2, 2)
        p, q = output_dist(gen, 2), uniform(2)
        k = rng.randrange(1, 4)
        hybrids = product_hybrids(p, q, k)
        assert hybrids[0] == product_hybrids(q, q, k)[0]
        sd_k = statistical_distance(hybrids[-1], hybrids[0])
        assert sd_k <= k * statistical_distance(p, q)
        test = random_test(rng, 2 * k)
        gaps = hybrid_gaps(test, hybrids)
        assert sum(gaps) == advantage(test, hybrids[-1], hybrids[0])
        assert max(abs(g) for g in gaps) <= statistical_distance(p, q)


def test_identical_distributions() -> None:
    u = uniform(3)
    assert statistical_distance(u, u) == 0
    assert advantage(majority, u, u) == 0
