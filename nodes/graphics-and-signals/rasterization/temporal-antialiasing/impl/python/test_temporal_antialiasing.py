# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temporal-antialiasing/. The authors are listed in prov/Y521G8.jsonl.

import math
import random
from fractions import Fraction as F

from temporal_antialiasing import halton, taa_frame, temporal_antialiasing


def radical_inverse(n, base):
    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return sum(F(d, base ** (k + 1)) for k, d in enumerate(digits))


def grid_scene(rng, w, h, cells=6):
    """A static scene: random colors on a fine grid of cells per pixel."""
    vals = [[(F(rng.randint(0, 9)), F(rng.randint(0, 1))) for _ in range(w * cells)] for _ in range(h * cells)]

    def render(t, x, y):
        return vals[min(math.floor(y * cells), h * cells - 1)][min(math.floor(x * cells), w * cells - 1)]

    return render


def test_halton() -> None:
    assert [halton(k, 2) for k in range(1, 5)] == [F(1, 2), F(1, 4), F(3, 4), F(1, 8)]
    assert [halton(k, 3) for k in range(1, 5)] == [F(1, 3), F(2, 3), F(1, 9), F(4, 9)]
    for n in range(2000):
        for b in (2, 3, 5):
            assert halton(n, b) == radical_inverse(n, b)


def test_static_scene_is_the_weighted_sum() -> None:
    rng = random.Random(2014)
    for _ in range(500):
        w, h = rng.randint(1, 3), rng.randint(1, 3)
        render = grid_scene(rng, w, h)
        alpha = F(rng.randint(1, 9), 10)
        frames = rng.randint(1, 6)
        out = temporal_antialiasing(render, w, h, frames, alpha, clamp=False)[-1]
        for j in range(h):
            for i in range(w):
                samples = [render(k, i + halton(k, 2), j + halton(k, 3)) for k in range(1, frames + 1)]
                want = [F(0), F(0)]
                for k, s in enumerate(samples, start=1):
                    weight = (1 - alpha) ** (frames - 1) if k == 1 else alpha * (1 - alpha) ** (frames - k)
                    want = [a + weight * c for a, c in zip(want, s)]
                assert out[j][i] == tuple(want)


def test_one_over_t_is_supersampling() -> None:
    rng = random.Random(6)
    for _ in range(100):
        w, h = rng.randint(1, 3), rng.randint(1, 3)
        render = grid_scene(rng, w, h)
        frames = rng.randint(1, 12)
        outs = temporal_antialiasing(render, w, h, frames, lambda t: F(1, t), clamp=False)
        for t, out in enumerate(outs, start=1):
            for j in range(h):
                for i in range(w):
                    samples = [render(k, i + halton(k, 2), j + halton(k, 3)) for k in range(1, t + 1)]
                    assert out[j][i] == tuple(sum(c, F(0)) / t for c in zip(*samples))


def test_reprojection_of_a_moving_scene() -> None:
    rng = random.Random(12)
    for _ in range(60):
        w, h = 7, 6
        static = grid_scene(rng, w + 12, h + 12)
        vx, vy = rng.randint(-1, 1), rng.randint(-1, 1)

        def render(t, x, y):
            return static(0, x - t * vx + 6, y - t * vy + 6)

        frames = 4
        out = temporal_antialiasing(render, w, h, frames, lambda t: F(1, t), motion=lambda t, i, j: (vx, vy), clamp=False)[-1]
        for j in range(h):
            for i in range(w):
                if not (0 <= i - frames * abs(vx) and i + frames * abs(vx) < w and 0 <= j - frames * abs(vy) and j + frames * abs(vy) < h):
                    continue
                samples = [render(frames, i + halton(k, 2), j + halton(k, 3)) for k in range(1, frames + 1)]
                assert out[j][i] == tuple(sum(c, F(0)) / frames for c in zip(*samples))


def test_clamp_keeps_the_neighborhood_range() -> None:
    rng = random.Random(3)
    for _ in range(100):
        w, h = rng.randint(1, 4), rng.randint(1, 4)
        history = [[(F(rng.randint(-20, 30)),) for _ in range(w)] for _ in range(h)]
        cur_vals = [[(F(rng.randint(0, 9)),) for _ in range(w)] for _ in range(h)]

        def render(t, x, y):
            return cur_vals[math.floor(y)][math.floor(x)]

        mv = (F(rng.randint(-8, 8), 4), F(rng.randint(-8, 8), 4))
        out = taa_frame(2, history, render, w, h, F(1, 5), motion=lambda t, i, j: mv)
        for j in range(h):
            for i in range(w):
                near = [cur_vals[b][a][0] for b in range(max(0, j - 1), min(h, j + 2)) for a in range(max(0, i - 1), min(w, i + 2))]
                assert min(near) <= out[j][i][0] <= max(near)


def test_ghosting_example() -> None:
    def render(t, x, y):
        return (F(1),) if t <= 20 else (F(0),)

    plain = temporal_antialiasing(render, 2, 2, 30, F(1, 10), clamp=False)
    clamped = temporal_antialiasing(render, 2, 2, 30, F(1, 10), clamp=True)
    assert plain[19][0][0] == (F(1),)
    assert plain[29][0][0] == (F(9, 10) ** 10,)
    assert clamped[20][0][0] == (F(0),)


def test_edge_example_and_floats() -> None:
    def render(t, x, y):
        return (F(1),) if x > F(4, 3) else (F(0),)

    # the edge crosses the middle pixel of three; its neighbors are 0 and 1, so the clamp does nothing
    outs = temporal_antialiasing(render, 3, 1, 8, lambda t: F(1, t))
    assert [o[0][1][0] for o in outs] == [F(1), F(1, 2), F(2, 3), F(1, 2), F(3, 5), F(2, 3), F(5, 7), F(5, 8)]
    # alone, the pixel is its own neighborhood, and the clamp throws the history away
    alone = temporal_antialiasing(lambda t, x, y: render(t, x + 1, y), 1, 1, 8, lambda t: F(1, t))
    assert [o[0][0][0] for o in alone] == [F(1), F(0), F(1), F(0), F(1), F(1), F(1), F(0)]
    flo = temporal_antialiasing(lambda t, x, y: (float(x > 1 / 3),), 1, 1, 8, 0.1)
    assert 0.0 <= flo[-1][0][0][0] <= 1.0
