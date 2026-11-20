# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-minded-bidder-mechanism/. The authors are listed in prov/Z6TN8C.jsonl.

import itertools
import random
from fractions import Fraction
from math import isqrt

from single_minded_bidder_mechanism import sign_surd, single_minded_mechanism


def fs(*items):
    return frozenset(items)


ALL_BUNDLES = [frozenset(c) for r in (1, 2, 3) for c in itertools.combinations(range(3), r)]


def optimum(bids):
    best = 0
    for r in range(len(bids) + 1):
        for chosen in itertools.combinations(range(len(bids)), r):
            items = [x for i in chosen for x in bids[i][0]]
            if len(items) == len(set(items)):
                best = max(best, sum(bids[i][1] for i in chosen))
    return best


def welfare(bids, winners):
    return sum(bids[i][1] for i in winners)


def random_bids(rng, n, m, top):
    out = []
    for _ in range(n):
        size = rng.randrange(1, m + 1)
        out.append((frozenset(rng.sample(range(m), size)), rng.randrange(0, top)))
    return out


def test_example() -> None:
    bids = [(fs(0, 1), 6), (fs(1, 2), 5), (fs(2, 3), 4), (fs(0, 1, 2, 3), 9)]
    winners, pay = single_minded_mechanism(bids)
    assert winners == [3]
    # Without bidder 3, bidder 0 wins first and meets {0, 1, 2, 3}: 6 sqrt(4 / 2).
    assert pay[3] == (Fraction(6), 2)
    assert pay[0] == pay[1] == pay[2] == (0, 1)
    assert optimum(bids) == 10
    bids = [(fs(0), 3), (fs(0, 1), 4), (fs(1), 1)]
    winners, pay = single_minded_mechanism(bids)
    assert winners == [0, 2]
    # Bidder 0 is blocked by bidder 1 without it: 4 sqrt(1 / 2) = 2 sqrt(2).
    assert pay[0] == (Fraction(2), 2)
    # Without bidder 2, bidder 0 wins first and blocks bidder 1, so no winner
    # meets item 1 and bidder 2 pays 0.
    assert pay[2] == (0, 1)


def test_edges() -> None:
    assert single_minded_mechanism([]) == ([], [])
    assert single_minded_mechanism([(fs(0), 5)]) == ([0], [(0, 1)])
    # Equal keys: the smaller index wins and pays exactly its own value.
    assert single_minded_mechanism([(fs(0), 2), (fs(0), 2)]) == ([0], [(Fraction(2), 1), (0, 1)])
    # Keys 1 and 9/4: the big bundle wins and pays 1 * sqrt(4 / 1) = 2.
    winners, pay = single_minded_mechanism([(fs(0), 1), (fs(0, 1, 2, 3), 3)])
    assert winners == [1] and pay[1] == (Fraction(2), 1)
    for bad in ([(fs(), 1)], [(fs(0), -1)]):
        try:
            single_minded_mechanism(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input must be rejected")


def test_feasible_and_sqrt_m_approximation() -> None:
    rng = random.Random(1)
    for _ in range(1500):
        n, m = rng.randrange(1, 7), rng.randrange(1, 6)
        bids = random_bids(rng, n, m, 10)
        winners, pay = single_minded_mechanism(bids)
        items = [x for i in winners for x in bids[i][0]]
        assert len(items) == len(set(items))
        opt, w = optimum(bids), welfare(bids, winners)
        used = len(set().union(*[b[0] for b in bids]))
        assert opt * opt <= used * w * w
        for i in range(n):
            if i not in winners:
                assert pay[i] == (0, 1)
            else:
                # Individual rationality: v_i - c sqrt(r) >= 0.
                assert sign_surd(bids[i][1], -pay[i][0], pay[i][1]) >= 0


def test_tight_example() -> None:
    for m in (4, 9, 16):
        k = isqrt(m)
        big = k + Fraction(1, 100)
        bids = [(frozenset(range(m)), big)] + [(fs(j), 1) for j in range(m)]
        winners, _ = single_minded_mechanism(bids)
        assert winners == [0]
        if m <= 9:
            assert optimum(bids) == m
        # The ratio m / (sqrt(m) + 1/100) of the optimum to the greedy welfare.
        assert m / big > k - Fraction(1, 10)


def wins(bids, i, value):
    trial = list(bids)
    trial[i] = (bids[i][0], value)
    return i in single_minded_mechanism(trial)[0]


def test_payment_is_critical_value() -> None:
    rng = random.Random(2)
    scale = 10 ** 6
    for _ in range(400):
        bids = random_bids(rng, rng.randrange(1, 6), rng.randrange(1, 6), 10)
        winners, pay = single_minded_mechanism(bids)
        for i in winners:
            c, r = pay[i]
            # lo <= c sqrt(r) <= hi, with hi - lo = 1 / scale.
            lo = Fraction(isqrt(int(c * c * r * scale * scale)), scale)
            hi = lo + Fraction(1, scale)
            assert sign_surd(hi, -c, r) > 0
            assert wins(bids, i, hi)
            if sign_surd(lo, -c, r) < 0:
                assert not wins(bids, i, lo)


def utility(true_bundle, true_value, bids, i):
    winners, pay = single_minded_mechanism(bids)
    if i not in winners:
        return 0, 0, 1
    gain = true_value if true_bundle <= bids[i][0] else 0
    return gain, pay[i][0], pay[i][1]


def test_truthful_is_dominant() -> None:
    rng = random.Random(3)
    for _ in range(80):
        bids = random_bids(rng, 3, 3, 5)
        for i in range(3):
            bundle, value = bids[i]
            a, c, r = utility(bundle, value, bids, i)
            for lie_bundle in ALL_BUNDLES:
                for lie_value in range(0, 6):
                    trial = list(bids)
                    trial[i] = (lie_bundle, lie_value)
                    a2, c2, r2 = utility(bundle, value, trial, i)
                    # (a - c sqrt r) - (a2 - c2 sqrt r2) >= 0
                    assert sign_surd(a - a2, -c, r, c2, r2) >= 0


def test_sign_surd() -> None:
    rng = random.Random(4)
    for _ in range(3000):
        a, b, c = (Fraction(rng.randrange(-20, 21), rng.randrange(1, 5)) for _ in range(3))
        x, y = rng.randrange(0, 30), rng.randrange(0, 30)
        approx = float(a) + float(b) * x ** 0.5 + float(c) * y ** 0.5
        s = sign_surd(a, b, x, c, y)
        if abs(approx) > 1e-9:
            assert s == (1 if approx > 0 else -1)
    assert sign_surd(0, 1, 2, -1, 2) == 0
    assert sign_surd(3, -1, 9) == 0
    assert sign_surd(-5, 1, 2, 1, 8) == -1
    assert sign_surd(Fraction(-3), 1, 2, 1, 2) == -1
    assert sign_surd(Fraction(-3), 1, 3, 1, 3) == 1
