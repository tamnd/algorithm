# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ripple-join/. The authors are listed in prov/NQMZP0.jsonl.

import itertools
import random
from fractions import Fraction

from ripple_join import exact_variance, ripple_join

KEY = lambda t: t[0]
PRICE = lambda r, s: r[2]
ONE = lambda r, s: 1


def exact(r_rows, s_rows, value):
    return sum(value(r, s) for r in r_rows for s in s_rows
               if r[0] is not None and s[0] is not None and r[0] == s[0])


R_EX = [(1, "r1", 3), (2, "r2", 5), (1, "r3", 2), (3, "r4", 4)]
S_EX = [(1, "s1", 0), (2, "s2", 0), (1, "s3", 0)]


def test_example() -> None:
    snaps = ripple_join(R_EX, S_EX, KEY, KEY, PRICE)
    assert [(x["n_r"], x["n_s"]) for x in snaps] == [(1, 1), (2, 2), (3, 3), (4, 3)]
    assert [x["sum"] for x in snaps] == [3, 8, 15, 15]
    assert [x["estimate"] for x in snaps] == [36, 24, 20, 15]
    assert exact(R_EX, S_EX, PRICE) == 15 and snaps[-1]["half_width"] == 0.0


def test_unbiased_over_all_orders() -> None:
    # The mean of the estimate over all orders of R and S equals the true value at every step.
    s_null = S_EX + [(None, "s4", 0)]
    for s_rows, value in ((S_EX, PRICE), (s_null, ONE), (s_null, PRICE)):
        truth = exact(R_EX, s_rows, value)
        for aspect in ((1, 1), (2, 1), (1, 2), (3, 2)):
            total = None
            count = 0
            for pr in itertools.permutations(R_EX):
                for ps in itertools.permutations(s_rows):
                    est = [x["estimate"] for x in ripple_join(list(pr), list(ps), KEY, KEY, value, aspect)]
                    total = est if total is None else [a + b for a, b in zip(total, est)]
                    count += 1
            assert all(Fraction(t, count) == truth for t in total)


def test_exact_variance_over_all_orders() -> None:
    s_null = S_EX + [(None, "s4", 0)]
    for s_rows, value in ((S_EX, PRICE), (s_null, PRICE), (s_null, ONE)):
        truth = exact(R_EX, s_rows, value)
        for aspect in ((1, 1), (2, 1)):
            sq = None
            count = 0
            for pr in itertools.permutations(R_EX):
                for ps in itertools.permutations(s_rows):
                    snaps = ripple_join(list(pr), list(ps), KEY, KEY, value, aspect)
                    dev = [(x["estimate"] - truth) ** 2 for x in snaps]
                    sq = dev if sq is None else [a + b for a, b in zip(sq, dev)]
                    count += 1
            for x, total in zip(snaps, sq):
                want = exact_variance(R_EX, s_rows, KEY, KEY, value, x["n_r"], x["n_s"])
                assert Fraction(total, count) == want


def test_hash_equals_nested() -> None:
    rng = random.Random(2)
    for trial in range(30):
        dom = rng.choice([3, 4, 5])
        keys = list(range(dom)) + [None]
        r = [(rng.choice(keys), i, rng.randrange(10)) for i in range(rng.randrange(0, 40))]
        s = [(rng.choice(keys), i, 0) for i in range(rng.randrange(0, 40))]
        aspect = rng.choice([(1, 1), (2, 1), (1, 3)])
        a = ripple_join(r, s, KEY, KEY, PRICE, aspect, random.Random(trial), "hash")
        b = ripple_join(r, s, KEY, KEY, PRICE, aspect, random.Random(trial), "nested")
        assert a == b
        assert a[-1]["estimate"] == exact(r, s, PRICE)
        assert a[-1]["pairs"] == exact(r, s, ONE)


def test_empty_inputs() -> None:
    assert ripple_join([], S_EX, KEY, KEY, PRICE)[-1]["estimate"] == 0
    assert ripple_join(R_EX, [], KEY, KEY, PRICE)[-1]["estimate"] == 0


def test_mean_and_coverage() -> None:
    rng = random.Random(5)
    r = [(rng.randrange(5), i, rng.randrange(1, 20)) for i in range(200)]
    s = [(rng.randrange(5), i, 0) for i in range(200)]
    truth = exact(r, s, PRICE)
    runs = 120
    for step in (25, 50):
        ests = []
        covered = 0
        for t in range(runs):
            x = ripple_join(r, s, KEY, KEY, PRICE, rng=random.Random(1000 + t))[step - 1]
            ests.append(x["estimate"])
            covered += abs(x["estimate"] - truth) <= x["half_width"]
        assert abs(sum(ests) / runs - truth) <= 0.03 * truth
        assert covered >= 0.85 * runs
