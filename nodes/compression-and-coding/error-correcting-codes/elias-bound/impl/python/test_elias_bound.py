# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-bound/. The authors are listed in prov/BBQKPZ.jsonl.

import random
from itertools import product
from math import log2

from elias_bound import (
    ball_list_bound, count_in_ball, elias_bound, elias_rate, hamming_bound, hamming_rate,
    johnson_radius, plotkin_rate, volume,
)

# A_2(n, d) (or the upper end of the known range) from A. E. Brouwer,
# Table of general binary codes, https://aeb.win.tue.nl/codes/binary-1.html
BROUWER_UPPER = {(12, 4): 144, (16, 6): 256, (20, 8): 256, (24, 8): 4096, (24, 10): 268,
                 (20, 6): 2279, (24, 6): 24106, (17, 4): 3276}

GOLAY_G = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]  # x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1


def golay_words() -> list[tuple[int, ...]]:
    gen = [tuple([0] * i + GOLAY_G + [0] * (23 - 12 - i)) for i in range(12)]
    words = []
    for m in range(2 ** 12):
        w = [0] * 23
        for i in range(12):
            if (m >> i) & 1:
                w = [a ^ b for a, b in zip(w, gen[i])]
        words.append(tuple(w))
    return words


def test_finite_values() -> None:
    table = {(12, 4): (315, 311), (24, 10): (1295, 882), (64, 16): (26184380591, 17004939455),
             (100, 30): (24141609256495, 2033245478054)}
    for (n, d), (h, e) in table.items():
        assert hamming_bound(2, n, d) == h
        assert elias_bound(2, n, d)[0] == e
    for (n, d), a in BROUWER_UPPER.items():
        assert elias_bound(2, n, d)[0] >= a


def test_ball_count_on_codes() -> None:
    # The lemma of the proof: a ball of radius r below the Johnson radius holds at most
    # ball_list_bound(r) codewords, checked at random centres on the Golay code.
    words = golay_words()
    rng = random.Random(1954)
    for r in range(0, 8):
        k = ball_list_bound(2, 23, 7, r)
        if k is None:
            continue
        for _ in range(40):
            center = tuple(rng.randrange(2) for _ in range(23))
            assert count_in_ball(words, center, r) <= k


def test_averaging_step() -> None:
    # sum over all centres x of |C cap B(x, r)| = |C| V_q(n, r), so some ball has >= the mean
    rng = random.Random(7)
    for q, n in ((2, 8), (3, 5)):
        allw = list(product(range(q), repeat=n))
        code = rng.sample(allw, 20)
        for r in range(n + 1):
            total = sum(count_in_ball(code, x, r) for x in allw)
            assert total == len(code) * volume(q, n, r)


def test_bound_holds_on_greedy_codes() -> None:
    rng = random.Random(1956)
    for _ in range(100):
        q = rng.choice([2, 3])
        n = rng.randint(3, 7 if q == 2 else 5)
        d = rng.randint(2, n)
        allw = list(product(range(q), repeat=n))
        rng.shuffle(allw)
        code: list[tuple[int, ...]] = []
        for x in allw:
            if all(sum(a != b for a, b in zip(x, c)) >= d for c in code):
                code.append(x)
        assert len(code) <= elias_bound(q, n, d)[0]


def test_asymptotic() -> None:
    assert abs(johnson_radius(0.2) - (1 - (1 - 0.4) ** 0.5) / 2) < 1e-12
    assert abs(elias_rate(0.2) - 0.4920) < 1e-4
    assert abs(elias_rate(0.45) - 0.0734) < 1e-4
    for delta in (0.05, 0.1, 0.2, 0.3, 0.4, 0.45):
        assert elias_rate(delta) < hamming_rate(delta)
        assert elias_rate(delta) < plotkin_rate(delta)
    # the finite bound approaches the asymptotic rate
    for n, tol in ((600, 0.025), (1500, 0.012)):
        for delta in (0.1, 0.25):
            d = int(delta * n)
            r = log2(elias_bound(2, n, d)[0]) / n
            assert 0 < r - elias_rate(d / n) < tol
