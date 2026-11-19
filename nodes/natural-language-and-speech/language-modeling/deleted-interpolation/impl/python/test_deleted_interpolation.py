# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deleted-interpolation/. The authors are listed in prov/S7TPCG.jsonl.

import itertools
import math
import random

import pytest

from deleted_interpolation import (
    BOS,
    EOS,
    Components,
    deleted_interpolation,
    fit_weights,
    heldout_interpolation,
)

# three held-out tokens, with (bigram, unigram) probabilities
HAND = {"b": [[0.5, 0.25], [0.0, 0.125], [1.0, 0.5]]}
TOY = [s.split() for s in ["a b", "a c", "b c", "a b c", "c a b"]]


def test_hand_example() -> None:
    lam, trace = fit_weights(HAND, max_iter=1)
    assert math.isclose(lam["b"][0], 4 / 9)
    lam, trace = fit_weights(HAND, max_iter=2)
    assert math.isclose(lam["b"][0], 16 / 39)
    # the log likelihood is log((1 + l)/4) + log((1 - l)/8) + log((1 + l)/2), largest at l = 1/3
    lam, trace = fit_weights(HAND, max_iter=3000, tol=0.0)
    assert abs(lam["b"][0] - 1 / 3) < 1e-6
    assert math.isclose(sum(lam["b"]), 1.0)


def random_rows(rng: random.Random, k: int, size: int) -> list[list[float]]:
    rows = []
    for _ in range(size):
        p = [rng.choice([0.0, rng.random()]) for _ in range(k - 1)]
        p.append(rng.uniform(0.05, 0.3))  # the uniform component is never zero
        rows.append(p)
    return rows


def test_em_never_decreases_the_likelihood() -> None:
    rng = random.Random(1)
    for _ in range(30):
        k = rng.randrange(2, 5)
        rows = {"b": random_rows(rng, k, rng.randrange(1, 30))}
        lam, trace = fit_weights(rows, max_iter=60, tol=-1.0)
        for x, y in zip(trace, trace[1:]):
            assert y >= x - 1e-9
        assert math.isclose(sum(lam["b"]), 1.0) and min(lam["b"]) >= 0


def test_em_reaches_the_grid_optimum() -> None:
    rng = random.Random(2)
    for _ in range(20):
        rows = random_rows(rng, 2, 20)
        lam, trace = fit_weights({"b": rows}, max_iter=5000, tol=1e-14)
        best = max(
            sum(math.log(g * p[0] + (1 - g) * p[1]) for p in rows) for g in (i / 1000 for i in range(1000))
        )
        got = sum(math.log(lam["b"][0] * p[0] + lam["b"][1] * p[1]) for p in rows)
        assert got >= best - 1e-6


def test_fixed_point_condition() -> None:
    """At the optimum, the mean of p_j / z is 1 for every component with positive weight, and at most 1 otherwise."""
    rng = random.Random(3)
    rows = random_rows(rng, 3, 40)
    lam, _ = fit_weights({"b": rows}, max_iter=5000, tol=1e-15)
    lam = lam["b"]
    for j in range(3):
        g = sum(p[j] / sum(l * q for l, q in zip(lam, p)) for p in rows) / len(rows)
        if lam[j] > 1e-3:
            assert abs(g - 1) < 1e-3
        else:
            assert g <= 1 + 1e-3


def test_components_use_the_longest_seen_history() -> None:
    comp = Components(TOY, 3, {"a", "b", "c", EOS})
    b, p = comp("b", ("c", "a"))
    assert b == (2, 1) and p == [1.0, 3 / 4, 4 / 17, 1 / 4]
    b, p = comp("b", ("b", "a"))  # "b a" never seen, "a" seen 4 times
    assert b == (1, 3) and p == [3 / 4, 4 / 17, 1 / 4]


def test_rows_sum_to_one() -> None:
    rng = random.Random(9)
    words = ["a", "b", "c", "d"]
    for trial in range(40):
        n = rng.randrange(1, 4)
        corpus = [[rng.choice(words[:3]) for _ in range(rng.randrange(0, 6))] for _ in range(rng.randrange(3, 9))]
        if trial % 2:
            m = deleted_interpolation(corpus, n, parts=rng.randrange(2, 4), vocab=words)
        else:
            m = heldout_interpolation(corpus[1:], corpus[:1], n, vocab=words)
        for lam in m.weights.values():
            assert math.isclose(sum(lam), 1.0) and min(lam) >= 0
        for h in itertools.product([BOS] + words, repeat=n - 1):
            d = m.distribution(h)
            assert math.isclose(sum(d.values()), 1.0, abs_tol=1e-12)
            assert all(p > 0 for p in d.values())


def test_unseen_test_tokens_get_mass() -> None:
    m = deleted_interpolation(TOY, 2, parts=2, vocab={"a", "b", "c", "d"})
    ll = m.log_likelihood([["d", "a"], ["c", "c"]])
    assert math.isfinite(ll)
    assert m.prob("d", ["a"]) > 0


def test_errors() -> None:
    with pytest.raises(ValueError):
        deleted_interpolation(TOY, 2, parts=1)
    with pytest.raises(ValueError):
        deleted_interpolation(TOY[:1], 2, parts=2)
    with pytest.raises(ValueError):
        deleted_interpolation(TOY, 2, vocab={"a"})
    with pytest.raises(ValueError):
        deleted_interpolation(TOY, 2, vocab={"a", "b", "c", BOS})
    m = deleted_interpolation(TOY, 2)
    with pytest.raises(KeyError):
        m.prob("z", ["a"])
