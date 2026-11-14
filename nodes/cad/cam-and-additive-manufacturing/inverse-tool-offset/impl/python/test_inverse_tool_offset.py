# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-tool-offset/. The authors are listed in prov/RAY63F.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from inverse_tool_offset import ball_tool, flat_tool, footprint, inverse_tool_offset


def gather(f, tool):
    """Brute force: at each grid point, the maximum over all samples of the part of
    f[q] - T(q - p), taken only where q - p is in the footprint."""
    nx, ny = len(f), len(f[0])
    z = [[None] * ny for _ in range(nx)]
    for p in range(nx):
        for q in range(ny):
            for i in range(nx):
                for j in range(ny):
                    o = (i - p, j - q)
                    if o in tool:
                        v = f[i][j] - tool[o]
                        if z[p][q] is None or v > z[p][q]:
                            z[p][q] = v
    return z


def terrain(rng, nx, ny):
    return [[rng.uniform(-1.0, 1.0) for _ in range(ny)] for _ in range(nx)]


def test_pin_example():
    f = [[0.0] * 5 for _ in range(5)]
    f[2][2] = 1.0
    z = inverse_tool_offset(f, ball_tool(1.0, 0.5))
    row = [round(v, 6) for v in z[2]]
    assert row == [0.0, 0.866025, 1.0, 0.866025, 0.0]
    assert round(z[1][1], 6) == 0.707107
    assert len(footprint(1.0, 0.5)) == 13


def test_scatter_equals_gather_exactly():
    rng = random.Random(1)
    for _ in range(4):
        nx, ny = rng.randrange(8, 14), rng.randrange(8, 14)
        f = terrain(rng, nx, ny)
        tool = ball_tool(rng.choice([0.5, 1.0, 1.5]), 0.25)
        assert inverse_tool_offset(f, tool) == gather(f, tool)


def test_flat_tool_is_exact_with_fractions():
    rng = random.Random(2)
    for _ in range(4):
        nx, ny = rng.randrange(6, 11), rng.randrange(6, 11)
        f = [[F(rng.randrange(-50, 51), 7) for _ in range(ny)] for _ in range(nx)]
        tool = flat_tool(F(3, 2), F(1, 2))
        z = inverse_tool_offset(f, tool)
        assert z == gather(f, tool)
        for p in range(nx):
            for q in range(ny):
                disk = [f[i][j] for i in range(nx) for j in range(ny) if (i - p) ** 2 + (j - q) ** 2 <= 9]
                assert z[p][q] == max(disk)


def test_no_gouge_at_samples_and_contact():
    rng = random.Random(3)
    f = terrain(rng, 16, 16)
    tool = ball_tool(1.0, 0.25)
    z = inverse_tool_offset(f, tool)
    for p in range(16):
        for q in range(16):
            touch = False
            for (a, b), t in tool.items():
                i, j = p + a, q + b
                if 0 <= i < 16 and 0 <= j < 16:
                    assert z[p][q] + t >= f[i][j]
                    touch = touch or z[p][q] + t == f[i][j]
            assert touch


def test_ball_on_a_tilted_plane():
    """The grid result is at most the continuous offset, and close to it (measured)."""
    for m, d in ((0.5, 0.25), (1.0, 0.25), (2.0, 0.125)):
        r = 2.0
        n = int(12 / d)
        f = [[m * i * d for _ in range(n)] for i in range(n)]
        z = inverse_tool_offset(f, ball_tool(r, d))
        k = int(r / d) + 1
        worst = 0.0
        for i in range(k, n - k):
            exact = m * i * d + r * (math.sqrt(1 + m * m) - 1)
            for j in range(k, n - k):
                assert z[i][j] <= exact + 1e-12
                worst = max(worst, exact - z[i][j])
        assert worst <= m * d * d


def test_bad_input():
    with pytest.raises(ValueError):
        footprint(0, 1)
    with pytest.raises(ValueError):
        ball_tool(1.0, 0.0)
