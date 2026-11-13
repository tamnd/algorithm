# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-mode-decomposition/. The authors are listed in prov/H7DRYS.jsonl.

import math
import random
from fractions import Fraction

from empirical_mode_decomposition import emd, extrema, meets_rule, natural_spline, sd, sift_once, zero_crossings


def two_tones_and_trend(n=200):
    return [round(100 * math.sin(2 * math.pi * i / 10)) + round(60 * math.sin(2 * math.pi * i / 47)) + i // 4 for i in range(n)]


def test_extrema_and_zero_crossings_by_hand() -> None:
    h = [0, 3, 1, -2, -2, 4, 5, 5, -1]
    assert extrema(h) == ([1, 6], [3])
    assert zero_crossings(h) == 3


def test_spline_interpolates_and_is_exact_on_lines() -> None:
    knots, values = [0, 3, 4, 9], [1.0, -2.0, 0.5, 3.0]
    s = natural_spline(knots, values, 10)
    assert all(abs(s[k] - v) < 1e-12 for k, v in zip(knots, values))
    line = natural_spline([0, 2, 5, 9], [1.0, 2.0, 3.5, 5.5], 10)
    assert all(abs(line[i] - (1 + 0.5 * i)) < 1e-12 for i in range(10))


def check_decomposition(x, **kw):
    imfs, residue, info = emd(x, **kw)
    # Completeness, exactly.
    for i, v in enumerate(x):
        assert sum(c[i] for c in imfs) + residue[i] == v
    # Every IMF meets the rule that ended its sifting, or sifting hit the cap.
    for c, d in zip(imfs, info):
        assert sift_once(d["prev"]) == c
        if d["reason"] == "rule":
            maxima, minima = extrema(c)
            assert abs(len(maxima) + len(minima) - zero_crossings(c)) <= 1
            assert sd(d["prev"], c) < kw.get("sd_limit", Fraction(1, 100))
            assert meets_rule(d["prev"], c, kw.get("sd_limit", Fraction(1, 100)))
        else:
            assert d["sifts"] == kw.get("max_sifts", 50)
    return imfs, residue, info


def test_two_tones_and_trend() -> None:
    x = two_tones_and_trend()
    imfs, residue, info = check_decomposition(x)
    assert [d["reason"] for d in info] == ["rule"] * len(imfs)
    maxima, minima = extrema(imfs[0])
    assert len(maxima) + len(minima) == 40  # the 10-sample tone: two extrema per period over 200 samples


def test_random_integer_signals() -> None:
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        walk, x = 0, []
        for _ in range(120):
            walk += rng.randint(-3, 3)
            x.append(walk + rng.randint(-20, 20))
        check_decomposition(x, max_imfs=5)


def test_cap_branch_is_recorded() -> None:
    x = two_tones_and_trend(120)
    imfs, _, info = check_decomposition(x, max_sifts=1, sd_limit=Fraction(0), max_imfs=3)
    assert [d["reason"] for d in info] == ["cap"] * len(imfs)


def test_monotone_input_is_its_own_residue() -> None:
    x = [i * i for i in range(30)]
    imfs, residue, _ = emd(x)
    assert imfs == [] and residue == [Fraction(v) for v in x]
