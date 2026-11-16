# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dubins-path/. The authors are listed in prov/4DQ75R.jsonl.

import math
import random

from dubins_path import WORDS, dubins_candidates, dubins_path, endpoint, sample, step, wrap

TWO_PI = 2.0 * math.pi


def pose_error(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(wrap(a[2] - b[2])))


def random_pose(rng, size=5.0):
    return (rng.uniform(-size, size), rng.uniform(-size, size), rng.uniform(-math.pi, math.pi))


# An independent solver: build the turning circles and find the tangent lines and the
# middle circles numerically, without the closed forms of the module.

def arc(theta_from, theta_to, kind):
    a = (theta_to - theta_from) % TWO_PI if kind == "L" else (theta_from - theta_to) % TWO_PI
    return 0.0 if a > TWO_PI - 1e-7 else a


def center(q, kind, rho):
    x, y, th = q
    if kind == "L":
        return x - rho * math.sin(th), y + rho * math.cos(th)
    return x + rho * math.sin(th), y - rho * math.cos(th)


def point_on(c, kind, psi, rho):
    """Point of the circle with center c where a car turning in direction kind has heading psi."""
    if kind == "L":
        return c[0] + rho * math.sin(psi), c[1] - rho * math.cos(psi)
    return c[0] - rho * math.sin(psi), c[1] + rho * math.cos(psi)


def heading_at(c, kind, p):
    ang = math.atan2(p[1] - c[1], p[0] - c[0])
    return ang + math.pi / 2.0 if kind == "L" else ang - math.pi / 2.0


def geometric_csc(q0, q1, rho, a, b):
    ca, cb = center(q0, a, rho), center(q1, b, rho)

    def f(psi):
        pa, pb = point_on(ca, a, psi, rho), point_on(cb, b, psi, rho)
        return math.cos(psi) * (pb[1] - pa[1]) - math.sin(psi) * (pb[0] - pa[0])

    best = math.inf
    n = 720
    grid = [(-math.pi + TWO_PI * i / n) for i in range(n + 1)]
    vals = [f(p) for p in grid]
    for i in range(n):
        lo, hi, flo = grid[i], grid[i + 1], vals[i]
        if flo == 0.0:
            hi = lo
        elif flo * vals[i + 1] > 0.0:
            continue
        for _ in range(80):
            if hi - lo < 1e-15:
                break
            mid = 0.5 * (lo + hi)
            fm = f(mid)
            if (fm < 0.0) == (flo < 0.0):
                lo, flo = mid, fm
            else:
                hi = mid
        psi = 0.5 * (lo + hi)
        pa, pb = point_on(ca, a, psi, rho), point_on(cb, b, psi, rho)
        s = math.cos(psi) * (pb[0] - pa[0]) + math.sin(psi) * (pb[1] - pa[1])
        if s < -1e-9:
            continue
        total = rho * arc(q0[2], psi, a) + max(s, 0.0) + rho * arc(psi, q1[2], b)
        best = min(best, total)
    return best


def geometric_ccc(q0, q1, rho, a):
    m = "R" if a == "L" else "L"
    c0, c1 = center(q0, a, rho), center(q1, a, rho)
    dx, dy = c1[0] - c0[0], c1[1] - c0[1]
    dist = math.hypot(dx, dy)
    if dist > 4.0 * rho or dist < 1e-12:
        return math.inf
    h = math.sqrt(max(4.0 * rho * rho - dist * dist / 4.0, 0.0))
    mx, my = c0[0] + dx / 2.0, c0[1] + dy / 2.0
    best = math.inf
    for sgn in (1.0, -1.0):
        cm = (mx - sgn * h * dy / dist, my + sgn * h * dx / dist)
        t1 = ((c0[0] + cm[0]) / 2.0, (c0[1] + cm[1]) / 2.0)
        t2 = ((c1[0] + cm[0]) / 2.0, (c1[1] + cm[1]) / 2.0)
        psi1, psi2 = heading_at(c0, a, t1), heading_at(c1, a, t2)
        mid = (psi2 - psi1) % TWO_PI if m == "L" else (psi1 - psi2) % TWO_PI
        total = rho * (arc(q0[2], psi1, a) + mid + arc(psi2, q1[2], a))
        best = min(best, total)
    return best


def geometric_min(q0, q1, rho):
    best = math.inf
    for a in "LR":
        for b in "LR":
            best = min(best, geometric_csc(q0, q1, rho, a, b))
        best = min(best, geometric_ccc(q0, q1, rho, a))
    return best


def test_every_candidate_ends_at_the_goal():
    rng = random.Random(11)
    for _ in range(2000):
        q0, q1 = random_pose(rng), random_pose(rng)
        rho = rng.uniform(0.3, 2.0)
        cands = dubins_candidates(q0, q1, rho)
        assert len(cands) >= 4
        for length, word, seg in cands:
            assert min(seg) >= 0.0
            assert abs(length - sum(seg)) < 1e-12
            assert pose_error(endpoint(q0, word, seg, rho), q1) < 1e-9


def test_matches_independent_geometric_construction():
    rng = random.Random(12)
    for _ in range(150):
        q0, q1 = random_pose(rng, 3.0), random_pose(rng, 3.0)
        rho = rng.uniform(0.5, 1.5)
        length = dubins_path(q0, q1, rho)[0]
        assert abs(length - geometric_min(q0, q1, rho)) < 1e-7


def random_forward_path(rng, rho):
    word = "".join(rng.choice("LSR") for _ in range(rng.randint(1, 5)))
    seg = []
    for k in word:
        seg.append(rng.uniform(0.0, 4.0) if k == "S" else rho * rng.uniform(0.0, TWO_PI))
    return word, seg


def test_no_forward_path_is_shorter():
    rng = random.Random(13)
    for _ in range(3000):
        rho = rng.uniform(0.5, 1.5)
        q0 = random_pose(rng)
        word, seg = random_forward_path(rng, rho)
        q1 = endpoint(q0, word, seg, rho)
        # When a straight part has length 0, p is the square root of a rounded p^2 near 0,
        # so p can come out near 1e-8 instead of 0. That is the tolerance here.
        assert dubins_path(q0, q1, rho)[0] <= sum(seg) + 1e-7


def test_every_word_is_optimal_somewhere():
    rng = random.Random(14)
    seen = set()
    for _ in range(3000):
        q0, q1 = random_pose(rng, 2.0), random_pose(rng, 2.0)
        seen.add(dubins_path(q0, q1, 1.0)[1])
    assert seen == set(WORDS)


def test_hand_cases():
    # A straight line: length 4 m.
    length, word, seg = dubins_path((0.0, 0.0, 0.0), (4.0, 0.0, 0.0), 1.0)
    assert abs(length - 4.0) < 1e-12 and word in ("LSL", "RSR")
    # A quarter of a left circle of radius 1 m.
    length, word, seg = dubins_path((0.0, 0.0, 0.0), (1.0, 1.0, math.pi / 2.0), 1.0)
    assert abs(length - math.pi / 2.0) < 1e-9
    # A U-turn in place needs a CCC path of length 7 pi / 3 (radius 1 m).
    length, word, seg = dubins_path((0.0, 0.0, 0.0), (0.0, 0.0, -math.pi), 1.0)
    assert abs(length - 7.0 * math.pi / 3.0) < 1e-9 and word in ("RLR", "LRL")
    # Scaling: lengths scale with rho.
    a = dubins_path((0.0, 0.0, 0.3), (2.0, 1.0, -1.0), 1.0)[0]
    b = dubins_path((0.0, 0.0, 0.3), (6.0, 3.0, -1.0), 3.0)[0]
    assert abs(3.0 * a - b) < 1e-9


def test_symmetries():
    rng = random.Random(15)
    for _ in range(500):
        q0, q1 = random_pose(rng), random_pose(rng)
        length, word, seg = dubins_path(q0, q1, 1.0)
        # Mirror in the x axis swaps L and R.
        m = dubins_path((q0[0], -q0[1], -q0[2]), (q1[0], -q1[1], -q1[2]), 1.0)
        assert abs(m[0] - length) < 1e-9
        # Driving the path backward in time is a forward path from the reversed goal.
        r = dubins_path((q1[0], q1[1], q1[2] + math.pi), (q0[0], q0[1], q0[2] + math.pi), 1.0)
        assert abs(r[0] - length) < 1e-9


def test_samples_are_close_and_on_the_path():
    q0, q1 = (0.0, 0.0, 0.0), (3.0, -2.0, 2.0)
    length, word, seg = dubins_path(q0, q1, 1.0)
    pts = sample(q0, word, seg, 1.0, 0.05)
    assert pose_error(pts[-1], q1) < 1e-9
    for p, q in zip(pts, pts[1:]):
        assert math.hypot(q[0] - p[0], q[1] - p[1]) <= 0.05 + 1e-12
    assert pose_error(step(q0, "S", 0.0, 1.0), q0) == 0.0
