# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/registration-curves/. The authors are listed in prov/2DMA1Q.jsonl.
"""Tests of registration curves.

The slope limited dynamic time warping equals a brute force search over all
admissible paths on small random grids. The time warp is monotone, starts
and ends at the corners and obeys the slope limit. A slower copy of a clip
is registered close to the true time ratio, a rigidly moved copy gives its
transform back, and the blended times never decrease. Motion data is made
in code.
"""

import math
import random

import registration_curves as rc


def brute(D, L):
    n, m = len(D), len(D[0])
    best = [math.inf, None]

    def go(i, j, s, r, c, path):
        if i == n - 1 and j == m - 1:
            if c < best[0]:
                best[0], best[1] = c, list(path)
            return
        for k, (di, dj) in enumerate(rc.STEPS):
            a, b = i + di, j + dj
            if a >= n or b >= m:
                continue
            nr = 0 if k == 0 else (r + 1 if k == s else 1)
            if nr > L:
                continue
            path.append((a, b))
            go(a, b, k, nr, c + D[a][b], path)
            path.pop()

    go(0, 0, 0, 0, D[0][0], [(0, 0)])
    return best[0]


def check_path(path, n, m, L):
    assert path[0] == (0, 0) and path[-1] == (n - 1, m - 1)
    run, last = 0, None
    for (i, j), (a, b) in zip(path, path[1:]):
        step = (a - i, b - j)
        assert step in rc.STEPS
        if step == (1, 1):
            run, last = 0, None
        else:
            run = run + 1 if step == last else 1
            last = step
            assert run <= L


def walk(n, speed, heading, x0, z0):
    out = []
    ch, sh = math.cos(heading), math.sin(heading)
    for i in range(n):
        ph = 2 * math.pi * speed * i / 30.0
        local = [(0.0, 1.0 + 0.04 * math.cos(2 * ph), 0.0),
                 (0.3 * math.sin(ph), 0.1 + 0.08 * max(0.0, math.sin(ph)), 0.15),
                 (-0.3 * math.sin(ph), 0.1 + 0.08 * max(0.0, -math.sin(ph)), -0.15),
                 (-0.2 * math.sin(ph), 1.2, 0.25),
                 (0.2 * math.sin(ph), 1.2, -0.25)]
        out.append([(x * ch - z * sh + x0, y, x * sh + z * ch + z0) for x, y, z in local])
    return out


def test_dtw_equals_brute_force():
    rng = random.Random(3)
    for _ in range(40):
        n, m = rng.randint(1, 6), rng.randint(1, 6)
        L = rng.randint(1, 3)
        D = [[rng.random() for _ in range(m)] for _ in range(n)]
        b = brute(D, L)
        if b == math.inf:
            try:
                rc.time_warp(D, L)
                assert False, "a path was found where none exists"
            except ValueError:
                pass
            continue
        cost, path = rc.time_warp(D, L)
        assert abs(cost - b) < 1e-12
        assert abs(sum(D[i][j] for i, j in path) - cost) < 1e-12
        check_path(path, n, m, L)


def test_timewarp_of_slower_copy():
    A = walk(31, 1.0, 0.0, 0.0, 0.0)   # one cycle in 30 frames
    B = walk(46, 2.0 / 3.0, 0.0, 0.0, 0.0)  # the same cycle in 45 frames
    reg = rc.register(A, B, L=2)
    path = reg["path"]
    check_path(path, 31, 46, 2)
    for i, j in path:
        assert abs(j - 1.5 * i) <= 1.5


def test_alignment_recovers_rigid_move():
    A = walk(20, 1.0, 0.0, 0.0, 0.0)
    B = walk(20, 1.0, 0.0, 0.0, 0.0)
    th, x0, z0 = 2.5, 1.0, -2.0
    ct, st = math.cos(th), math.sin(th)
    # B is A moved by the inverse of (th, x0, z0)
    B = [[((x - x0) * ct - (z - z0) * st, y, (x - x0) * st + (z - z0) * ct) for x, y, z in fr]
         for fr in A]
    reg = rc.register(A, B, L=2)
    assert reg["path"] == [(i, i) for i in range(20)]
    for t, a, b in reg["align"]:
        assert abs(t - th) < 1e-9 and abs(a - x0) < 1e-9 and abs(b - z0) < 1e-9
    frames, _ = rc.blend(A, B, reg, 0.5)
    assert max(abs(p - q) for fa, fb in zip(frames, A) for pa, pb in zip(fa, fb)
               for p, q in zip(pa, pb)) < 1e-9


def test_blend_times_are_monotone():
    A = walk(31, 1.0, 0.0, 0.0, 0.0)
    B = walk(40, 0.8, 0.4, 0.5, 0.5)
    reg = rc.register(A, B, L=3)
    for w in (0.0, 0.25, 0.5, 1.0):
        _, times = rc.blend(A, B, reg, w)
        assert all(b >= a for a, b in zip(times, times[1:]))
        assert times[0] == 0 and abs(times[-1] - (w * 30 + (1 - w) * 39)) < 1e-12
    angles = [t for t, _, _ in reg["align"]]
    assert all(abs(b - a) < math.pi for a, b in zip(angles, angles[1:]))
