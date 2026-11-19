# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-good-turing/. The authors are listed in prov/P5RKY6.jsonl.

import math
import random

import pytest

from simple_good_turing import averaged_counts, fit_line, simple_good_turing, simple_good_turing_counts

TABLE = {1: 268, 2: 112, 3: 70, 4: 41, 5: 24, 6: 14, 7: 15, 8: 7, 9: 6, 10: 4, 12: 3, 15: 2, 20: 1, 31: 1}


def counts_from_table(nr: dict[int, int]) -> dict[str, int]:
    out, i = {}, 0
    for r, n in nr.items():
        for _ in range(n):
            out[f"t{i}"] = r
            i += 1
    return out


def test_averaged_counts() -> None:
    z = averaged_counts({1: 10, 2: 4, 4: 2, 7: 1})
    # q = 0, t = 2; q = 1, t = 4; q = 2, t = 7; q = 4, t = 2 * 7 - 4 = 10
    assert z == {1: 10.0, 2: 8 / 3, 4: 4 / 5, 7: 2 / 6}


def test_fit_line_exact() -> None:
    a, b = fit_line([0.0, 1.0, 2.0, 3.0], [5.0, 3.0, 1.0, -1.0])
    assert math.isclose(a, 5.0) and math.isclose(b, -2.0)


def test_worked_example() -> None:
    rstar, a, b, switch = simple_good_turing_counts(TABLE)
    assert switch == 3
    assert math.isclose(a, 6.813929, abs_tol=1e-6)
    assert math.isclose(b, -2.576710, abs_tol=1e-6)
    assert math.isclose(rstar[1], 2 * 112 / 268)  # the Turing estimate
    assert math.isclose(rstar[2], 3 * 70 / 112)
    assert math.isclose(rstar[3], 3 * (4 / 3) ** (b + 1))  # the smoothed estimate
    assert math.isclose(rstar[3], 1.906027, abs_tol=1e-6)
    p, p0, _, _ = simple_good_turing(counts_from_table(TABLE))
    assert math.isclose(p0, 268 / 1442)
    assert math.isclose(p0 + sum(p.values()), 1.0, abs_tol=1e-12)


def test_smoothed_count_closed_form() -> None:
    """With S(r) = exp(a) r^b, the smoothed count is r (1 + 1/r)^(b + 1)."""
    rstar, _, b, switch = simple_good_turing_counts(TABLE)
    for r in TABLE:
        if r >= switch:
            assert math.isclose(rstar[r], r * (1 + 1 / r) ** (b + 1), rel_tol=1e-12)


def test_once_smoothed_always_smoothed() -> None:
    rng = random.Random(5)
    for _ in range(200):
        nr = {}
        for r in range(1, 25):
            v = int(rng.uniform(0.3, 1.7) * 400 / r ** 2)
            if v > 0:
                nr[r] = v
        if len(nr) < 2:
            continue
        rstar, _, b, switch = simple_good_turing_counts(nr)
        rs = sorted(nr)
        assert switch is not None
        for r in rs:
            n1 = nr.get(r + 1, 0)
            if r < switch:
                assert rstar[r] == (r + 1) * n1 / nr[r]
            else:
                assert math.isclose(rstar[r], r * (1 + 1 / r) ** (b + 1), rel_tol=1e-12)
        # the switch is at the first r without N_(r+1) or with a small difference
        for r in rs:
            if r == switch:
                break
            assert nr.get(r + 1, 0) > 0


def test_zipf_samples_are_proper() -> None:
    rng = random.Random(3)
    weights = [1 / (i + 1) for i in range(300)]
    for _ in range(20):
        tokens = rng.choices(range(300), weights=weights, k=2000)
        counts: dict[int, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        p, p0, rstar, b = simple_good_turing(counts)
        assert b < -1
        assert math.isclose(p0 + sum(p.values()), 1.0, abs_tol=1e-12)
        assert all(0 < v < 1 for v in p.values())
        n = len(tokens)
        assert math.isclose(p0, sum(1 for r in counts.values() if r == 1) / n)
        # for large counts the smoothed estimate is close to the raw count
        top = max(counts.values())
        assert abs(rstar[top] / top - 1) < 0.05


def test_errors() -> None:
    with pytest.raises(ValueError):
        simple_good_turing_counts({1: 5})
    with pytest.raises(ValueError):
        simple_good_turing({"a": 1, "b": 1})
