# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aimd/. The authors are listed in prov/378JCS.jsonl.

import random
from fractions import Fraction as F

import pytest

from aimd import aimd, jain_index, linear_step


def test_page_example():
    t = aimd([1, 7], 10, 1, F(1, 2), 12)
    assert t[3] == [F(3, 2), F(9, 2)]
    assert t[7] == [F(9, 4), F(15, 4)]
    assert t[11] == [F(21, 8), F(27, 8)]
    assert [sum(x) for x in t[3:12]] == [6, 8, 10, 12, 6, 8, 10, 12, 6]
    assert jain_index([1, 7]) == F(16, 25)


def test_aimd_converges_to_fair_line():
    t = aimd([F(1), F(7)], 10, 1, F(1, 2), 200)
    x = t[-1]
    assert abs(x[1] - x[0]) < F(1, 10**14)
    assert 1 - jain_index(x) < F(1, 10**20)


def test_aiad_and_mimd_keep_the_unfairness():
    x = [F(1), F(7)]
    for _ in range(200):
        x = linear_step(x, 10, (1, 1), (-1, 1))
        assert x[1] - x[0] == 6  # AIAD keeps the difference
    y = [F(1), F(7)]
    for _ in range(200):
        y = linear_step(y, 10, (0, 2), (0, F(1, 2)))
        assert y[1] == 7 * y[0]  # MIMD keeps the ratio
    assert jain_index(y) == F(16, 25)


def test_miad_moves_away_from_fairness():
    x = [F(1), F(7)]
    for _ in range(60):
        x = linear_step(x, 10, (0, F(9, 8)), (-1, 1))
    assert x[0] == 0


def test_bad_parameters():
    with pytest.raises(ValueError):
        aimd([1, 2], 10, 1, 1, 5)
    with pytest.raises(ValueError):
        aimd([1, 2], 10, 0, F(1, 2), 5)


def test_random_starts_difference_and_band():
    rng = random.Random(1989)
    for _ in range(500):
        n = rng.randrange(1, 6)
        c = rng.randrange(1, 50)
        a = F(rng.randrange(1, 5), rng.randrange(1, 4))
        b = F(rng.randrange(1, 9), 10)
        x0 = [F(rng.randrange(0, 60)) for _ in range(n)]
        t = aimd(x0, c, a, b, 80)
        decreases = 0
        in_band = False
        for k in range(1, len(t)):
            if sum(t[k - 1]) > c:
                decreases += 1
            spread = max(t[k]) - min(t[k])
            assert spread == (max(x0) - min(x0)) * b**decreases
            ok = b * c < sum(t[k]) <= c + n * a
            assert ok or not in_band  # once inside the band, the total stays there
            in_band = in_band or ok
        assert in_band
