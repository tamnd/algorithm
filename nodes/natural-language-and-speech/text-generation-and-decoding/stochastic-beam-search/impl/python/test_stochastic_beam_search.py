# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-beam-search/. The authors are listed in prov/G3YHYE.jsonl.

import itertools
import math
import random
from collections import Counter

from nlslog import NEG_INF, log_normalize, safe_log
from stochastic_beam_search import EOS, gumbel, log1mexp, shift, stochastic_beam_search

M1 = {
    (): {"a": 0.5, "b": 0.4, EOS: 0.1},
    ("a",): {"a": 0.4, "b": 0.3, EOS: 0.3},
    ("b",): {"a": 0.05, "b": 0.05, EOS: 0.9},
}
M1_CACHE = {}


def m1(prefix):
    key = tuple(prefix)
    if key not in M1_CACHE:
        probs = M1.get(key, {"a": 0.0, "b": 0.0, EOS: 1.0})
        M1_CACHE[key] = {w: safe_log(p) for w, p in probs.items()}
    return M1_CACHE[key]


def random_model(seed, vocab, n):
    cache = {}

    def model(prefix):
        if prefix not in cache:
            if len(prefix) >= n - 1:
                cache[prefix] = {w: (0.0 if w == EOS else NEG_INF) for w in vocab}
            else:
                rng = random.Random(f"{seed}|{' '.join(prefix)}")
                raw = [math.log(rng.random() ** 2 + 1e-3) for _ in vocab]
                cache[prefix] = dict(zip(vocab, log_normalize(raw)))
        return cache[prefix]

    return model


def exhaustive(model, n):
    out = []

    def rec(prefix, s):
        for w, lp in model(tuple(prefix)).items():
            if lp == NEG_INF:
                continue
            if w == EOS:
                out.append((tuple(prefix + [w]), s + lp))
            elif len(prefix) + 1 < n:
                rec(prefix + [w], s + lp)

    rec([], 0.0)
    return out


def ordered_probability(ps):
    """Probability that sampling without replacement draws ps[0], ps[1], ... first."""
    prob, left = 1.0, 1.0
    for p in ps:
        prob *= p / left
        left -= p
    return prob


def test_m1_has_seven_outputs() -> None:
    probs = {y: math.exp(s) for y, s in exhaustive(m1, 3)}
    assert len(probs) == 7
    assert math.isclose(math.fsum(probs.values()), 1.0)
    b, aa = ("b", EOS), ("a", "a", EOS)
    assert math.isclose(ordered_probability([probs[b], probs[aa]]), 0.1125)
    pair = ordered_probability([probs[b], probs[aa]]) + ordered_probability([probs[aa], probs[b]])
    assert math.isclose(pair, 0.2025)


def test_k1_is_a_sample_from_the_model() -> None:
    rng = random.Random(7)
    probs = {y: math.exp(s) for y, s in exhaustive(m1, 3)}
    draws = 20000
    counts = Counter(tuple(stochastic_beam_search(m1, 3, 1, rng)[0][0]) for _ in range(draws))
    for y, p in probs.items():
        assert abs(counts[y] / draws - p) < 0.01


def test_k2_ordered_pairs() -> None:
    rng = random.Random(11)
    probs = {y: math.exp(s) for y, s in exhaustive(m1, 3)}
    draws = 20000
    counts = Counter()
    for _ in range(draws):
        out = stochastic_beam_search(m1, 3, 2, rng)
        assert len(out) == 2 and out[0][0] != out[1][0]
        assert out[0][2] >= out[1][2]
        counts[(tuple(out[0][0]), tuple(out[1][0]))] += 1
    for y1, y2 in itertools.permutations(probs, 2):
        want = ordered_probability([probs[y1], probs[y2]])
        assert abs(counts[(y1, y2)] / draws - want) < 0.01


def test_k3_sets_on_a_random_model() -> None:
    model = random_model(5, ["a", "b", EOS], 3)
    probs = {y: math.exp(s) for y, s in exhaustive(model, 3)}
    assert len(probs) == 7
    rng = random.Random(3)
    draws = 10000
    counts = Counter(
        frozenset(tuple(y) for y, _, _ in stochastic_beam_search(model, 3, 3, rng)) for _ in range(draws)
    )
    for s in itertools.combinations(probs, 3):
        want = sum(ordered_probability([probs[y] for y in perm]) for perm in itertools.permutations(s))
        assert abs(counts[frozenset(s)] / draws - want) < 0.015


def test_large_k_returns_everything_once() -> None:
    for seed in range(20):
        model = random_model(seed, ["a", "b", "c", EOS], 4)
        everything = dict(exhaustive(model, 4))
        out = stochastic_beam_search(model, 4, len(everything) + 5, random.Random(seed))
        assert len(out) == len(everything)
        assert {tuple(y) for y, _, _ in out} == set(everything)
        for y, phi, _ in out:
            assert math.isclose(phi, everything[tuple(y)])


def test_shift_keeps_order_and_sets_the_maximum() -> None:
    rng = random.Random(2)
    for _ in range(500):
        target = rng.uniform(-5, 5)
        gs = [gumbel(rng.uniform(-6, 0), rng) for _ in range(rng.randrange(1, 6))]
        z = max(gs)
        shifted = [shift(target, z, g) for g in gs]
        assert max(shifted) == target
        for i in range(len(gs)):
            assert shifted[i] <= target
            for j in range(len(gs)):
                if gs[i] < gs[j]:
                    assert shifted[i] <= shifted[j]
        for g, s in zip(gs, shifted):
            direct = -math.log(math.exp(-target) - math.exp(-z) + math.exp(-g))
            assert math.isclose(s, direct, rel_tol=1e-9, abs_tol=1e-9)


def test_log1mexp() -> None:
    for a in (-1e-12, -1e-5, -0.3, -0.69):
        assert math.isclose(log1mexp(a), math.log(-math.expm1(a)), rel_tol=1e-12)
    for a in (-0.7, -2.0, -10.0):
        assert math.isclose(math.exp(log1mexp(a)) + math.exp(a), 1.0, rel_tol=1e-14)
    # For a very negative a, log(1 - e^a) is about -e^a; the naive form rounds to 0.
    assert math.isclose(log1mexp(-40.0), -math.exp(-40.0), rel_tol=1e-12)
    assert math.log(1.0 - math.exp(-40.0)) == 0.0
    assert log1mexp(0.0) == NEG_INF


def test_long_outputs_stay_in_log_space() -> None:
    steps = 1300
    vocab = ["a", "b", EOS]

    def model(prefix):
        if len(prefix) >= steps:
            return {"a": NEG_INF, "b": NEG_INF, EOS: 0.0}
        return {"a": math.log(0.5), "b": math.log(0.5), EOS: NEG_INF}

    out = stochastic_beam_search(model, steps + 1, 3, random.Random(4))
    assert len({tuple(y) for y, _, _ in out}) == 3
    for y, phi, _ in out:
        assert len(y) == steps + 1
        assert math.isclose(phi, steps * math.log(0.5))
        assert math.exp(phi) == 0.0
    assert vocab[-1] == EOS
