# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/footskate-cleanup/. The authors are listed in prov/QJ3V2G.jsonl.
"""Tests of footskate cleanup.

A planar walk is made in code: the ankles follow planned paths, with a
slow slide (the footskate) during each plant, and the leg angles come from
two-bone IK. After cleanup each planted ankle stays on its target, no bone
grows by more than eps, a clean walk is not changed, frames far from every
plant are not changed, and the root projection matches a grid search.
"""

import math
import random

import footskate_cleanup as fc

L1, L2 = 0.45, 0.50


def walk(frames=60, slide=0.003, height=0.85, v=0.04, rng=None):
    """Plants: left on [30k, 30k + 17], right shifted by 15 frames."""
    plants = {"L": [], "R": []}
    paths = {"L": [None] * frames, "R": [None] * frames}
    for leg, shift in (("L", 0), ("R", 15)):
        starts = list(range(shift - 30, frames, 30))
        for s in starts:
            t = s + 17
            mid = v * (s + 8.5)
            if 0 <= s and t < frames:
                plants[leg].append((s, t))
            for i in range(max(s, 0), min(t, frames - 1) + 1):
                noise = rng.uniform(-0.002, 0.002) if rng else 0.0
                paths[leg][i] = (mid + slide * (i - s - 8.5) + noise, 0.08)
            # swing to the next plant
            nmid = v * (s + 30 + 8.5)
            for i in range(t + 1, min(s + 30, frames)):
                if i < 0:
                    continue
                u = (i - t) / 13.0
                x = (mid + slide * 8.5) * (1 - u) + (nmid - slide * 8.5) * u
                paths[leg][i] = (x, 0.08 + 0.1 * math.sin(math.pi * u))
    out = []
    for i in range(frames):
        root = (v * i, height + 0.01 * math.cos(2 * math.pi * i / 15.0))
        fr = {"root": root}
        for leg in ("L", "R"):
            fr[leg] = fc.two_bone(root, paths[leg][i], L1, L2, -1.0)
        out.append(fr)
    return out, plants


def test_two_bone_reaches_target():
    rng = random.Random(1)
    for _ in range(500):
        root = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        d = rng.uniform(0.06, L1 + L2)
        a = rng.uniform(-math.pi, math.pi)
        target = (root[0] + d * math.cos(a), root[1] + d * math.sin(a))
        for sign in (-1.0, 1.0):
            phi, knee = fc.two_bone(root, target, L1, L2, sign)
            p = fc.leg_points(root, phi, knee, L1, L2)[1]
            assert math.dist(p, target) < 1e-9
            assert knee * sign >= -1e-12


def test_planted_ankles_stay_on_target():
    rng = random.Random(2)
    frames, plants = walk(rng=rng)
    before = max(math.dist(fc.ankle(frames[s], leg, L1, L2), fc.ankle(frames[t], leg, L1, L2))
                 for leg in plants for s, t in plants[leg])
    out, targets = fc.cleanup(frames, plants, L1, L2, eps=0.05, b=4)
    assert before > 0.04  # the input slides
    for leg in targets:
        for (s, t), c in targets[leg]:
            for i in range(s, t + 1):
                assert math.dist(fc.ankle(out[i], leg), c) < 1e-9


def test_bone_change_is_bounded():
    rng = random.Random(3)
    frames, plants = walk(rng=rng, height=0.94, slide=0.006, v=0.05)
    eps = 0.05
    out, targets = fc.cleanup(frames, plants, L1, L2, eps=eps, b=4)
    stretched = 0
    for fr in out:
        for leg in ("L", "R"):
            a, b = fr["len_" + leg]
            assert 1.0 - 1e-12 <= a / L1 <= 1.0 + eps + 1e-12
            assert abs(a / L1 - b / L2) < 1e-12
            stretched += a > L1 * (1 + 1e-9)
    assert stretched > 0  # this input needs some stretch or root motion
    for leg in targets:
        for (s, t), c in targets[leg]:
            for i in range(s, t + 1):
                assert math.dist(fc.ankle(out[i], leg), c) < 1e-9


def test_clean_walk_is_unchanged():
    frames, plants = walk(slide=0.0)
    out, _ = fc.cleanup(frames, plants, L1, L2)
    for a, b in zip(frames, out):
        assert math.dist(a["root"], b["root"]) < 1e-12
        for leg in ("L", "R"):
            assert abs(a[leg][0] - b[leg][0]) < 1e-9 and abs(a[leg][1] - b[leg][1]) < 1e-9


def test_far_frames_unchanged_and_blend_is_smooth():
    frames, _ = walk(frames=60, slide=0.004)
    plants = {"L": [(25, 34)], "R": []}
    b = 4
    out, _ = fc.cleanup(frames, plants, L1, L2, b=b)
    for i in list(range(0, 25 - b - 1)) + list(range(34 + b + 2, 60)):
        assert out[i] == {**frames[i], "len_L": (L1, L2), "len_R": (L1, L2)}
    assert fc.smooth_weight(0, b) == 1.0 and fc.smooth_weight(b + 1, b) == 0.0
    ws = [fc.smooth_weight(k, b) for k in range(b + 2)]
    assert all(x > y for x, y in zip(ws, ws[1:]))


def grid_nearest(h, disks, step=0.002, box=2.0):
    best = None
    n = int(2 * box / step)
    for a in range(n + 1):
        x = h[0] - box + a * step
        for c in range(n + 1):
            y = h[1] - box + c * step
            if all(math.dist((x, y), q) <= r for q, r in disks):
                d = math.dist((x, y), h)
                if best is None or d < best:
                    best = d
    return best


def test_root_projection_matches_grid_search():
    rng = random.Random(4)
    for _ in range(6):
        c1 = (rng.uniform(-0.5, 0.5), rng.uniform(-0.2, 0.2))
        c2 = (c1[0] + rng.uniform(0.4, 1.6), c1[1] + rng.uniform(-0.3, 0.3))
        r = 0.95
        h = (rng.uniform(-0.5, 1.5), rng.uniform(0.2, 1.2))
        disks = [(c1, r), (c2, r)]
        p = fc.project_root(h, disks)
        g = grid_nearest(h, disks, step=0.01, box=1.5)
        if g is None:
            assert p is None or math.dist(c1, c2) > 2 * r - 0.03
            continue
        assert p is not None
        assert all(math.dist(p, c) <= r + 1e-9 for c, _ in disks)
        assert math.dist(p, h) <= g + 1e-9
        assert math.dist(p, h) >= g - 0.015
    assert fc.project_root((0.0, 0.0), [((-1.0, 0.0), 0.4), ((1.0, 0.0), 0.4)]) is None
