# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-matching/. The authors are listed in prov/GYSR9F.jsonl.
"""Tests of motion matching.

The scan with early exit and the k-d tree must return the same frame as a
brute force nearest neighbor search, ties included. The normalization gives
every dimension zero mean and the weight as its standard deviation. The run
loop jumps only to the nearest frame, and does not jump when the next frame
is already the best. The database is made in code with a fixed seed.
"""

import math
import random

import motion_matching as mm

GROUPS = [("foot_pos", 0, 4), ("foot_vel", 4, 8), ("hip_vel", 8, 10),
          ("traj_pos", 10, 16), ("traj_dir", 16, 22)]
WEIGHTS = {"foot_pos": 0.75, "foot_vel": 1.0, "hip_vel": 1.0, "traj_pos": 1.0, "traj_dir": 1.5}


def clip(n, speed, turn, phase, rng):
    """Feature vectors of a 2D walk with constant speed and turn rate."""
    out = []
    for i in range(n):
        t = i / 30.0
        ph = 2.0 * math.pi * 1.1 * t + phase
        lf = (0.15 + 0.2 * math.sin(ph), 0.1)
        rf = (0.15 - 0.2 * math.sin(ph), -0.1)
        lv = (0.2 * 2 * math.pi * 1.1 * math.cos(ph), 0.0)
        rv = (-lv[0], 0.0)
        hip = (speed, 0.02 * math.sin(2 * ph))
        traj, dirs = [], []
        for k in (20, 40, 60):
            a = turn * k / 30.0
            if abs(turn) > 1e-9:
                r = speed / turn
                traj += [r * math.sin(a), r * (1 - math.cos(a))]
            else:
                traj += [speed * k / 30.0, 0.0]
            dirs += [math.cos(a), math.sin(a)]
        v = list(lf + rf + lv + rv + hip) + traj + dirs
        out.append([x + rng.gauss(0.0, 0.01) for x in v])
    return out


def database(seed=1):
    rng = random.Random(seed)
    feats = []
    for speed, turn, phase in ((1.2, 0.0, 0.0), (1.2, 0.6, 1.0), (1.2, -0.6, 2.0),
                               (2.5, 0.0, 0.5), (0.0, 0.0, 0.0)):
        feats += clip(60, speed, turn, phase, rng)
    # an exact duplicate row to test ties
    feats.append(list(feats[10]))
    return mm.Database(feats, GROUPS, WEIGHTS)


def test_normalization():
    db = database()
    for k in range(db.d):
        col = [x[k] for x in db.X]
        m = sum(col) / db.f
        s = math.sqrt(sum((c - m) ** 2 for c in col) / db.f)
        assert abs(m) < 1e-9
        name = next(n for n, a, b in GROUPS if a <= k < b)
        if db.std[k] != 1.0:
            assert abs(s - WEIGHTS[name]) < 1e-9


def test_searches_equal_brute_force():
    db = database()
    tree = mm.KdTree(db)
    rng = random.Random(9)
    queries = [list(db.raw[rng.randrange(db.f)]) for _ in range(50)]
    queries += [[x + rng.gauss(0.0, 0.3) for x in db.raw[rng.randrange(db.f)]] for _ in range(150)]
    queries += [[rng.gauss(0.0, 2.0) for _ in range(db.d)] for _ in range(50)]
    queries.append(list(db.raw[10]))  # tie between frame 10 and the duplicate
    for q in queries:
        b = mm.search_brute(db, q)
        assert mm.search_scan(db, q) == b
        assert tree.search(q) == b
    assert mm.search_brute(db, db.raw[10]) == 10


def test_playable_frames_only():
    db = database()
    db.playable = [i for i in range(db.f) if i % 60 < 40]
    tree = mm.KdTree(db)
    rng = random.Random(4)
    for _ in range(60):
        q = [x + rng.gauss(0.0, 0.2) for x in db.raw[rng.randrange(db.f)]]
        b = mm.search_brute(db, q)
        assert b in db.playable
        assert mm.search_scan(db, q) == b == tree.search(q)


def test_run_jumps_to_nearest_and_stays_when_best():
    db = database()
    db.playable = [i for i in range(db.f - 1) if i % 60 < 55]
    # the input asks for the features of the turning clip, frame 70 onward
    target = lambda t, frame: db.raw[70 + t]
    played, jumps = mm.run(db, target, 40, 10, start=0)
    assert jumps, "the first search must leave the straight clip"
    t0, _, to = jumps[0]
    assert to == mm.search_brute(db, target(t0, None))
    # when the query is the next frame itself, no jump happens
    played, jumps = mm.run(db, lambda t, frame: db.raw[frame], 40, 5, start=120)
    assert jumps == []
    assert played == list(range(120, 160))
