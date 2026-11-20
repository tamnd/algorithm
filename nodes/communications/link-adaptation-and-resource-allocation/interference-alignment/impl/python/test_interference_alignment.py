# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interference-alignment/. The authors are listed in prov/BAD5BM.jsonl.

import math
import random

import pytest

from cbb import cn, dot, matvec
from interference_alignment import (
    align_three_users,
    desired_gains,
    eigvec2,
    leakage,
    orthogonal_unit,
    parallel_defect,
    sum_rate,
)


def page_channels():
    m = {
        (1, 1): [[1, 0], [0, 1]], (2, 2): [[1, 1], [0, 1]], (3, 3): [[2, 0], [1, 1]],
        (1, 2): [[1, 2], [0, 1]], (1, 3): [[1, 0], [1, 1]],
        (2, 1): [[2, 1], [1, 1]], (2, 3): [[1, 0], [0, 2]],
        (3, 1): [[0, 1], [1, 0]], (3, 2): [[1, 1], [1, 2]],
    }
    return [[[[complex(x) for x in row] for row in m[k + 1, j + 1]] for j in range(3)] for k in range(3)]


def random_channels(rng: random.Random):
    return [[[[cn(rng, 1.0) for _ in range(2)] for _ in range(2)] for _ in range(3)] for _ in range(3)]


def direction(x):
    """x scaled so that its first entry is 1."""
    return [c / x[0] for c in x]


def test_page_example() -> None:
    h = page_channels()
    v, u = align_three_users(h)
    assert leakage(h, v, u) < 1e-18
    lam = (math.sqrt(17) - 3) / 2
    assert direction(v[0]) == pytest.approx([1, (lam - 1) / 2], abs=1e-12)
    assert direction(v[1]) == pytest.approx([1, -2.4384471871911697 / 2.8768943743823394], abs=1e-12)
    assert direction(v[2]) == pytest.approx([1, 0.7807764064044151 / 3.5615528128088303], abs=1e-12)
    # the interference directions at the three receivers
    assert direction(matvec(h[0][1], v[1])) == pytest.approx([1, 2.4384471871911697 / 2], abs=1e-12)
    assert direction(matvec(h[1][0], v[0])) == pytest.approx([1, 1.5615528128088303 / 3.5615528128088303], abs=1e-12)
    assert direction(matvec(h[2][0], v[0])) == pytest.approx([1, 2 / -0.4384471871911697], abs=1e-12)
    assert min(desired_gains(h, v, u)) > 0.1


def test_eigvec2() -> None:
    lam, x = eigvec2([[2, 1], [1, 2]], 0)
    assert lam == pytest.approx(3)
    assert abs(x[0] - x[1]) < 1e-12
    lam, x = eigvec2([[1, 0], [0, 1]], 1)
    assert lam == pytest.approx(1)
    assert sum(abs(c) ** 2 for c in x) == pytest.approx(1)


def test_orthogonal_unit() -> None:
    rng = random.Random(5)
    for _ in range(50):
        a = [cn(rng, 1.0), cn(rng, 1.0)]
        u = orthogonal_unit(a)
        assert abs(dot(u, a)) < 1e-12
        assert sum(abs(c) ** 2 for c in u) == pytest.approx(1.0, abs=1e-12)


def test_zero_leakage_on_random_channels() -> None:
    rng = random.Random(2008)
    for _ in range(200):
        h = random_channels(rng)
        for which in (0, 1):
            v, u = align_three_users(h, which)
            assert leakage(h, v, u) < 1e-9
            for k in range(3):
                i, j = [x for x in range(3) if x != k]
                assert parallel_defect(matvec(h[k][i], v[i]), matvec(h[k][j], v[j])) < 1e-9
            assert min(desired_gains(h, v, u)) > 0.0


def test_random_beams_leak() -> None:
    rng = random.Random(77)
    h = random_channels(rng)
    v = [[cn(rng, 1.0), cn(rng, 1.0)] for _ in range(3)]
    u = [orthogonal_unit(matvec(h[k][(k + 1) % 3], v[(k + 1) % 3])) for k in range(3)]
    assert leakage(h, v, u) > 1e-3


def test_three_degrees_of_freedom() -> None:
    rng = random.Random(11)
    h = random_channels(rng)
    v, u = align_three_users(h)
    lo, hi = sum_rate(h, v, u, 1e6), sum_rate(h, v, u, 1e10)
    # each factor 10^4 in power adds 3 log2(10^4) bits when 3 streams are free of interference
    assert (hi - lo) == pytest.approx(3 * math.log2(1e4), abs=1e-3)
