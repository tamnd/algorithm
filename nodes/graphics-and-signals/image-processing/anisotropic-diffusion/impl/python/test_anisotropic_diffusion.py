# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anisotropic-diffusion/. The authors are listed in prov/MYHS4D.jsonl.

import random
from fractions import Fraction as F

from anisotropic_diffusion import anisotropic_diffusion, diffusion_step, g_exponential, g_rational


def neighbors_inside(img, y, x):
    h, w = len(img), len(img[0])
    return [img[y + dy][x + dx] for dy, dx in ((0, -1), (0, 1), (-1, 0), (1, 0))
            if 0 <= y + dy < h and 0 <= x + dx < w]


def stencil_clamp(img, lam):
    """Direct 2D filtering with the 5-point kernel [0 l 0; l 1-4l l; 0 l 0] and the clamp border."""
    h, w = len(img), len(img[0])
    k = {(0, 0): 1 - 4 * lam, (0, -1): lam, (0, 1): lam, (-1, 0): lam, (1, 0): lam}
    return [[sum(c * img[min(max(y + dy, 0), h - 1)][min(max(x + dx, 0), w - 1)] for (dy, dx), c in k.items())
             for x in range(w)] for y in range(h)]


def random_image(rng, h, w):
    return [[F(rng.randint(0, 255)) for _ in range(w)] for _ in range(h)]


def test_example_row() -> None:
    img = [[10, 12, 10, 50, 48, 50]]
    one = diffusion_step(img, F(1, 4), g_rational(F(10)))
    assert one[0][:3] == [F(545, 52), F(287, 26), F(9785, 884)]
    two = anisotropic_diffusion(img, 2, F(1, 4), g_rational(F(10)))
    assert sum(two[0]) == 180
    assert abs(float(two[0][2]) - 11.679) < 1e-3


def test_edges() -> None:
    assert anisotropic_diffusion([], 3, F(1, 4), g_rational(1)) == []
    assert anisotropic_diffusion([[F(7)]], 5, F(1, 4), g_rational(1)) == [[7]]
    img = [[1, 2], [3, 4]]
    assert anisotropic_diffusion(img, 0, F(1, 4), g_rational(1)) == img
    try:
        anisotropic_diffusion(img, -1, F(1, 4), g_rational(1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative step count must be rejected")


def test_mass_is_conserved_exactly() -> None:
    rng = random.Random(1990)
    for _ in range(80):
        h, w = rng.randint(1, 7), rng.randint(1, 7)
        img = random_image(rng, h, w)
        lam = F(rng.randint(1, 5), 20)
        steps = 1 if h * w > 9 else 2
        out = anisotropic_diffusion(img, steps, lam, g_rational(F(rng.randint(1, 60))))
        assert sum(map(sum, out)) == sum(map(sum, img))


def test_maximum_principle_for_lambda_up_to_quarter() -> None:
    rng = random.Random(629)
    for _ in range(80):
        h, w = rng.randint(1, 7), rng.randint(1, 7)
        img = random_image(rng, h, w)
        lam = F(rng.randint(1, 5), 20)
        g = g_rational(F(rng.randint(1, 500)))
        nxt = diffusion_step(img, lam, g)
        for y in range(h):
            for x in range(w):
                local = neighbors_inside(img, y, x) + [img[y][x]]
                assert min(local) <= nxt[y][x] <= max(local)
        fl = [[float(v) for v in row] for row in img]
        out = anisotropic_diffusion(fl, 20, float(lam), lambda s, g=g: float(g(F(s))))
        lo, hi = min(map(min, fl)), max(map(max, fl))
        assert all(lo - 1e-9 <= v <= hi + 1e-9 for row in out for v in row)


def test_exponential_conductance_with_tolerance() -> None:
    rng = random.Random(639)
    for _ in range(40):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        img = [[float(rng.randint(0, 255)) for _ in range(w)] for _ in range(h)]
        out = anisotropic_diffusion(img, 6, 0.25, g_exponential(rng.choice([5.0, 20.0, 100.0])))
        assert abs(sum(map(sum, out)) - sum(map(sum, img))) < 1e-8
        lo, hi = min(map(min, img)), max(map(max, img))
        assert all(lo - 1e-9 <= v <= hi + 1e-9 for row in out for v in row)


def test_constant_conductance_equals_five_point_stencil() -> None:
    rng = random.Random(12)
    for _ in range(60):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        img = random_image(rng, h, w)
        lam = F(rng.randint(1, 5), 20)
        assert diffusion_step(img, lam, lambda s: 1) == stencil_clamp(img, lam)


def test_step_above_quarter_breaks_the_maximum_principle() -> None:
    board = [[F((x + y) % 2) for x in range(4)] for y in range(4)]
    nxt = diffusion_step(board, F(3, 10), g_rational(F(10)))
    assert board[1][2] == 1
    assert nxt[1][2] == 1 - F(12, 10) * F(100, 101) == F(-19, 101)
    assert nxt[1][1] == F(120, 101) > 1
    assert sum(map(sum, nxt)) == sum(map(sum, board))
