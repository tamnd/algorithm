# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-graph/. The authors are listed in prov/VP75X0.jsonl.
"""Tests of motion graph construction.

The closed form alignment is checked against a known transform and against
a dense search over the angle. Every transition is below the threshold and
is a local minimum. Tarjan's components equal the components from brute
force mutual reachability, and the pruned graph is the largest of them.
The motion data is made in code from smooth functions with a fixed seed.
"""

import math
import random

import motion_graph as mg


def walk(n, heading, x0, z0, phase, amp, rng):
    """A walking point cloud of 5 joints at 30 frames per second."""
    out = []
    ch, sh = math.cos(heading), math.sin(heading)
    for i in range(n):
        t = i / 30.0
        ph = 2.0 * math.pi * t + phase
        local = [
            (1.2 * t, 1.0 + 0.03 * math.cos(2 * ph), 0.0),
            (1.2 * t + amp * math.sin(ph), 0.1 + 0.08 * max(0.0, math.sin(ph)), 0.15),
            (1.2 * t - amp * math.sin(ph), 0.1 + 0.08 * max(0.0, -math.sin(ph)), -0.15),
            (1.2 * t - 0.2 * math.sin(ph), 1.1, 0.25),
            (1.2 * t + 0.2 * math.sin(ph), 1.1, -0.25),
        ]
        frame = []
        for (x, y, z) in local:
            x += rng.gauss(0.0, 0.002)
            z += rng.gauss(0.0, 0.002)
            frame.append((x * ch - z * sh + x0, y, x * sh + z * ch + z0))
        out.append(frame)
    return out


def database(seed=4):
    rng = random.Random(seed)
    return [walk(40, 0.0, 0.0, 0.0, 0.0, 0.3, rng),
            walk(40, 0.7, 2.0, 1.0, 1.0, 0.3, rng),
            walk(20, 0.0, 0.0, 0.0, 0.0, 0.6, rng)]


def reach(adj, s):
    seen = {s}
    todo = [s]
    while todo:
        v = todo.pop()
        for u in adj[v]:
            if u not in seen:
                seen.add(u)
                todo.append(u)
    return seen


def brute_scc(adj):
    n = len(adj)
    R = [reach(adj, v) for v in range(n)]
    comps = {frozenset(u for u in R[v] if v in R[u]) for v in range(n)}
    return sorted(sorted(c) for c in comps)


def test_alignment_recovers_a_rigid_transform():
    rng = random.Random(1)
    P = [(rng.uniform(-1, 1), rng.uniform(0, 2), rng.uniform(-1, 1)) for _ in range(12)]
    t, x0, z0 = 0.9, 0.4, -1.3
    # Q is P moved by the inverse transform, so aligning Q to P gives (t, x0, z0)
    ct, st = math.cos(t), math.sin(t)
    Q = []
    for p in P:
        x, z = p[0] - x0, p[2] - z0
        Q.append((x * ct - z * st, p[1], x * st + z * ct))
    a = mg.align_2d(P, Q)
    assert abs(a[0] - t) < 1e-12 and abs(a[1] - x0) < 1e-12 and abs(a[2] - z0) < 1e-12
    assert mg.cloud_distance(P, Q) < 1e-24


def test_alignment_is_optimal_against_angle_search():
    rng = random.Random(2)
    for _ in range(20):
        P = [(rng.uniform(-1, 1), rng.uniform(0, 2), rng.uniform(-1, 1)) for _ in range(8)]
        Q = [(rng.uniform(-1, 1), rng.uniform(0, 2), rng.uniform(-1, 1)) for _ in range(8)]
        w = [rng.uniform(0.1, 1.0) for _ in range(8)]
        best = mg.cloud_distance(P, Q, w)
        for s in range(720):
            th = 2.0 * math.pi * s / 720
            # the best translation for a fixed angle is the weighted mean gap
            R = [mg.transform(q, th, 0.0, 0.0) for q in Q]
            W = sum(w)
            dx = sum(wi * (p[0] - r[0]) for wi, p, r in zip(w, P, R)) / W
            dz = sum(wi * (p[2] - r[2]) for wi, p, r in zip(w, P, R)) / W
            assert mg.cloud_distance(P, Q, w, (th, dx, dz)) >= best - 1e-12


def test_transitions_below_threshold_and_local_minima():
    clips = database()
    k, thr = 5, 0.003
    r = mg.build(clips, k, thr)
    D, starts = r["D"], r["starts"]
    sset = set(starts)
    want = []
    for a in starts:
        for b in starts:
            if abs(a - b) < k or D[(a, b)] >= thr:
                continue
            nb = [D[(a + i, b + j)] for i in (-1, 0, 1) for j in (-1, 0, 1)
                  if (i or j) and a + i in sset and b + j in sset]
            if all(D[(a, b)] <= v for v in nb):
                want.append((a, b))
    assert r["transitions"] == want
    assert len(want) > 0
    assert all(D[t] < thr for t in r["transitions"])


def test_tarjan_equals_brute_force_on_random_graphs():
    rng = random.Random(5)
    for _ in range(40):
        n = rng.randint(1, 25)
        adj = [[u for u in range(n) if rng.random() < 0.12] for _ in range(n)]
        assert sorted(mg.tarjan_scc(adj)) == brute_scc(adj)


def test_pruning_is_the_largest_scc():
    clips = database()
    r = mg.build(clips, 5, 0.003)
    comps = brute_scc(r["adj"])
    size = max(len(c) for c in comps)
    assert len(r["keep"]) == size
    assert sorted(r["keep"]) in comps
    # every kept frame reaches every other kept frame inside the pruned graph
    for v in list(r["keep"])[:10]:
        assert reach(r["pruned"], v) == r["keep"]
    # measured on this database: the third clip (frames 80 .. 99) is cut off
    assert not any(80 <= v < 100 for v in r["keep"])
    assert 0 < size < 100


def test_blend_weight_ends():
    k = 10
    assert mg.blend_weight(-1, k) == 1.0
    assert abs(mg.blend_weight(k - 1, k)) < 1e-15
    vals = [mg.blend_weight(p, k) for p in range(-1, k)]
    assert all(b < a for a, b in zip(vals, vals[1:]))
