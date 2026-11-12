# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-random-load-balancing/. The authors are listed in prov/BWGAF8.jsonl.

import random
from fractions import Fraction

import pytest

from weighted_random_load_balancing import AliasPicker, WeightedRandom, chi_square

# upper 0.001 points of the chi-square distribution, degrees of freedom 1 to 9
CHI2_999 = [10.828, 13.816, 16.266, 18.467, 20.515, 22.458, 24.322, 26.124, 27.877]


def test_example_intervals() -> None:
    wr = WeightedRandom([5, 1, 3, 1])
    assert wr.p == [0, 5, 6, 9, 10]
    assert [wr.locate(r) for r in range(10)] == [0, 0, 0, 0, 0, 1, 2, 2, 2, 3]


def test_every_r_exactly_once() -> None:
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 8)
        w = [rng.choice([0, 1, 2, 3, 10]) for _ in range(n)]
        if sum(w) == 0:
            continue
        wr = WeightedRandom(w)
        counts = [0] * n
        for r in range(sum(w)):
            i = wr.locate(r)
            # oracle: a linear scan of the running sum
            acc, want = 0, None
            for j, x in enumerate(w):
                acc += x
                if acc > r:
                    want = j
                    break
            assert i == want
            counts[i] += 1
        assert counts == w  # so P(i) = w[i] / W exactly


def test_alias_exact_distribution() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(1, 8)
        w = [rng.randint(0, 9) for _ in range(n)]
        if sum(w) == 0:
            continue
        a = AliasPicker(w)
        assert a.exact_distribution() == [Fraction(x, sum(w)) for x in w]


def test_chi_square_fit() -> None:
    w = [5, 1, 3, 1, 10]
    for picker in (WeightedRandom(w), AliasPicker(w)):
        for seed in (1, 2, 3):
            rng = random.Random(seed)
            counts = [0] * len(w)
            for _ in range(100000):
                counts[picker.pick(rng)] += 1
            assert chi_square(counts, w) < CHI2_999[len(w) - 2]


def test_zero_weight_never_picked() -> None:
    rng = random.Random(3)
    wr, a = WeightedRandom([0, 2, 0, 1]), AliasPicker([0, 2, 0, 1])
    picks = {wr.pick(rng) for _ in range(2000)} | {a.pick(rng) for _ in range(2000)}
    assert picks == {1, 3}


def test_bad_weights() -> None:
    for w in ([], [0, 0], [1, -1]):
        with pytest.raises(ValueError):
            AliasPicker(w)
    for w in ([0, 0], [1, -1]):
        with pytest.raises(ValueError):
            WeightedRandom(w)
