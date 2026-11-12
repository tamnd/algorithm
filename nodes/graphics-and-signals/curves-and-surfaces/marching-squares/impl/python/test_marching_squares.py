# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-squares/. The authors are listed in prov/YVD13Y.jsonl.

import random
from collections import Counter, deque
from fractions import Fraction

from marching_squares import CORNER, EDGE, SADDLE, TABLE, chain_loops, marching_squares, saddle_joins_inside

HALF = Fraction(1, 2)


def crossings_brute(grid, c):
    """All points where the linear interpolant along a grid edge equals c, by a scan of all edges."""
    h, w = len(grid), len(grid[0])
    pts = set()
    for j in range(h):
        for i in range(w):
            for di, dj in ((1, 0), (0, 1)):
                i2, j2 = i + di, j + dj
                if i2 >= w or j2 >= h:
                    continue
                fa, fb = grid[j][i], grid[j2][i2]
                if (fa < c) != (fb < c):
                    t = Fraction(c - fa) / (fb - fa)
                    pts.add((i + t * di, j + t * dj))
    return pts


def test_example() -> None:
    grid = [
        [3, 3, 3, 3],
        [3, 0, 4, 3],
        [3, 4, 1, 3],
        [3, 3, 3, 3],
    ]

    def areas(c):
        out = []
        for lp in chain_loops(marching_squares(grid, c)):
            assert lp[0] == lp[-1]
            out.append(sum(lp[k][0] * lp[k + 1][1] - lp[k + 1][0] * lp[k][1] for k in range(len(lp) - 1)) / 2)
        return sorted(out)

    # the center cell is a saddle with saddle value 16/7
    assert Fraction(0 * 1 - 4 * 4, 0 + 1 - 4 - 4) == Fraction(16, 7)
    segs = marching_squares(grid, 2)
    assert len(segs) == 8
    assert ((Fraction(1, 3), 1), (1, Fraction(1, 3))) in segs
    assert areas(2) == [Fraction(25, 72), Fraction(49, 72)]  # 16/7 > 2: two loops
    assert areas(Fraction(5, 2)) == [Fraction(673, 288)]  # 16/7 < 5/2: one loop


def test_saddle_cell_both_ways() -> None:
    # inside corners 0 and 2; the saddle value is (f0 f2 - f1 f3) / (f0 + f2 - f1 - f3)
    joined = [[0, 3], [3, 1]]  # f0 = 0, f1 = 3, f2 = 1, f3 = 3: saddle value 9/5 < 2
    sep = [[0, 10], [10, 1]]  # saddle value 100/9 > 2
    a = marching_squares(joined, 2)
    b = marching_squares(sep, 2)
    assert len(a) == 2 and len(b) == 2
    assert saddle_joins_inside(0, 3, 1, 3, 2) and not saddle_joins_inside(0, 10, 1, 10, 2)
    # joined: each segment cuts off one outside corner (1 or 3)
    ends_a = {tuple(sorted(s)) for s in a}
    ends_b = {tuple(sorted(s)) for s in b}
    assert ends_a != ends_b


def test_table_orientation() -> None:
    mid = {e: (Fraction(CORNER[a][0] + CORNER[b][0], 2), Fraction(CORNER[a][1] + CORNER[b][1], 2)) for e, (a, b) in enumerate(EDGE)}
    for case in range(16):
        lists = SADDLE[case] if case in SADDLE else (TABLE[case],)
        for pairs in lists:
            used = [e for pr in pairs for e in pr]
            # each edge with a sign change is used exactly once, and no other edge
            change = [e for e, (a, b) in enumerate(EDGE) if (case >> a & 1) != (case >> b & 1)]
            assert sorted(used) == sorted(change)
            for ea, eb in pairs:
                p, q = mid[ea], mid[eb]
                for k in set(EDGE[ea]) | set(EDGE[eb]):
                    cx, cy = CORNER[k]
                    cr = (q[0] - p[0]) * (cy - p[1]) - (q[1] - p[1]) * (cx - p[0])
                    assert (cr > 0) == bool(case >> k & 1)


def test_edges() -> None:
    assert marching_squares([[0, 0], [0, 0]], 1) == []
    assert marching_squares([[5, 5], [5, 5]], 1) == []
    # a value equal to c counts as outside
    assert marching_squares([[1, 1], [1, 1]], 1) == []
    segs = marching_squares([[0, 2], [2, 2]], 1)
    assert segs == [((HALF, 0), (0, HALF))] or segs == [((Fraction(1, 2), 0), (0, Fraction(1, 2)))]
    # float input
    segs = marching_squares([[0.0, 2.0], [2.0, 2.0]], 1.0)
    assert len(segs) == 1 and abs(segs[0][0][0] - 0.5) < 1e-12


def bilinear_joined_dense(f, c, n=60):
    """Are corners 0 and 2 (case 5) or 1 and 3 (case 10) in one inside component of the bilinear interpolant?"""
    f0, f1, f2, f3 = f
    def val(a, b):
        # n^2 times the bilinear interpolant at (a / n, b / n), an exact integer
        return f0 * (n - a) * (n - b) + f1 * a * (n - b) + f2 * a * b + f3 * (n - a) * b
    cn = c * n * n
    ins = [[val(a, b) < cn for a in range(n + 1)] for b in range(n + 1)]
    case = sum(1 << k for k in range(4) if f[k] < c)
    s, t = ((0, 0), (n, n)) if case == 5 else ((n, 0), (0, n))
    seen = {s}
    dq = deque([s])
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            u, v = x + dx, y + dy
            if 0 <= u <= n and 0 <= v <= n and (u, v) not in seen and ins[v][u]:
                seen.add((u, v))
                dq.append((u, v))
    return t in seen


def test_decider_against_dense_sampling() -> None:
    rng = random.Random(51)
    checked = 0
    while checked < 60:
        f = [rng.randint(-9, 9) for _ in range(4)]
        c = Fraction(rng.randint(-17, 17), 2)
        case = sum(1 << k for k in range(4) if f[k] < c)
        if case not in (5, 10):
            continue
        den = f[0] + f[2] - f[1] - f[3]
        sv = Fraction(f[0] * f[2] - f[1] * f[3], den)
        if abs(sv - c) < Fraction(1, 4):
            continue  # too close to the tie for a 60 by 60 sampling
        checked += 1
        assert saddle_joins_inside(*f, c) == bilinear_joined_dense(f, c)


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    for trial in range(500):
        w, h = rng.randint(2, 7), rng.randint(2, 7)
        grid = [[rng.randint(-6, 6) for _ in range(w)] for _ in range(h)]
        closed = trial % 2 == 0
        if closed:
            for j in range(h):
                for i in range(w):
                    if i in (0, w - 1) or j in (0, h - 1):
                        grid[j][i] = 9
        c = Fraction(2 * rng.randint(-6, 5) + 1, 2)  # never equal to a sample
        segs = marching_squares(grid, c)
        ends = [p for s in segs for p in s]
        cnt = Counter(ends)
        brute = crossings_brute(grid, c)
        # the endpoints are exactly the crossing points of the grid edges
        assert set(cnt) == brute
        # each crossing on an interior edge is shared by two segments, on the border by one
        for (x, y), k in cnt.items():
            border = (x in (0, w - 1) and y != int(y)) or (y in (0, h - 1) and x != int(x))
            assert k == (1 if border else 2)
        # each segment lies in one cell: both ends on the boundary of the same unit square
        for p, q in segs:
            i = min(int(p[0]), int(q[0]), w - 2)
            j = min(int(p[1]), int(q[1]), h - 2)
            for x, y in (p, q):
                assert i <= x <= i + 1 and j <= y <= j + 1
                assert x in (i, i + 1) or y in (j, j + 1)
        if closed:
            starts = Counter(s[0] for s in segs)
            stops = Counter(s[1] for s in segs)
            assert all(starts[p] == 1 and stops[p] == 1 for p in cnt)
            for lp in chain_loops(segs):
                assert lp[0] == lp[-1]
                area = sum(lp[k][0] * lp[k + 1][1] - lp[k + 1][0] * lp[k][1] for k in range(len(lp) - 1))
                assert area != 0
