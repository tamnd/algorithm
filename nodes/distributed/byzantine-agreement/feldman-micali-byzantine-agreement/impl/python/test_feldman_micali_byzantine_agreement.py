# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feldman-micali-byzantine-agreement/. The authors are listed in prov/P7QJJH.jsonl.

import itertools
import random

from feldman_micali_byzantine_agreement import check, mean_iterations, run

STRATEGIES = ("silent", "random", "equivocate", "mirror", "split")


def test_validity_in_one_iteration():
    for n, t in ((4, 1), (7, 2), (10, 3)):
        for b in (0, 1):
            for strat in STRATEGIES:
                faulty = set(range(n - t, n))
                res = run(n, t, faulty, strat, [b] * n, seed=1)
                assert check(res, list(range(n - t)), [b] * n) == []
                assert res["decisions"] == {i: b for i in range(n - t)}
                assert res["iterations"] == 1 and res["rounds"] == 2


def test_agreement_all_traitor_sets_at_the_bound():
    for n, t, seeds in ((4, 1, range(10)), (7, 2, range(3))):
        for faulty in itertools.combinations(range(n), t):
            for strat in STRATEGIES:
                for coin in ("ideal", "weak"):
                    for seed in seeds:
                        rng = random.Random(seed)
                        inputs = [rng.randrange(2) for _ in range(n)]
                        res = run(n, t, set(faulty), strat, inputs, seed=seed, coin=coin)
                        honest = [i for i in range(n) if i not in faulty]
                        assert check(res, honest, inputs) == [], (n, faulty, strat, coin, seed)


def test_constant_expected_iterations_measured():
    # Ideal coin: unanimity with probability >= 1/2 per iteration, so at most
    # 3 iterations (6 rounds plus the coins) in expectation.
    for strat in STRATEGIES:
        assert mean_iterations(10, 3, strat, 300) <= 3.2
    split = mean_iterations(10, 3, "split", 300)
    assert 2.5 <= split <= 3.2, split
    # A coin that is common only with probability 1/2: at most 4 + 1 = 5.
    assert mean_iterations(10, 3, "split", 300, coin="weak") <= 5.3


def test_a_predictable_coin_lets_the_adversary_block():
    res = run(10, 3, {7, 8, 9}, "split", [1] * 5 + [0] * 5, coin="predicted", max_iters=60)
    assert res["iterations"] is None and res["decisions"] == {}
    res = run(4, 1, {3}, "split", [1, 1, 0, 0], coin="predicted", max_iters=60)
    assert res["iterations"] is None


def test_fails_just_below_the_bound():
    # n = 3t: the faulty process echoes each honest value back, and the two
    # honest processes decide differently in the first iteration.
    res = run(3, 1, {2}, "mirror", [0, 1, 0])
    assert "agreement" in check(res, [0, 1], [0, 1, 0])
    assert res["decisions"] == {0: 0, 1: 1}
    res = run(6, 2, {4, 5}, "mirror", [0, 0, 1, 1, 0, 0])
    assert "agreement" in check(res, [0, 1, 2, 3], [0, 0, 1, 1, 0, 0])
