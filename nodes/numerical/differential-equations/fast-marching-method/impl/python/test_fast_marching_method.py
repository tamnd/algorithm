# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-marching-method/. The authors are listed in prov/XZFJD7.jsonl.

import math
import random

import pytest

from fast_marching_method import INF, discrete_residual, fast_marching, upwind_update


def sweep_oracle(s, h, sources, max_rounds=200):
    """Independent solver: Gauss-Seidel sweeps of the same discrete equations to a fixed point."""
    rows, cols = len(s), len(s[0])
    T = [[INF] * cols for _ in range(rows)]
    for i, j in sources:
        T[i][j] = 0.0
    src = set(sources)
    orders = [(range(rows), range(cols)), (range(rows - 1, -1, -1), range(cols)),
              (range(rows - 1, -1, -1), range(cols - 1, -1, -1)), (range(rows), range(cols - 1, -1, -1))]
    for _ in range(max_rounds):
        change = 0.0
        for I, J in orders:
            for i in I:
                for j in J:
                    if (i, j) in src or s[i][j] == INF:
                        continue
                    a = min(T[i][j - 1] if j > 0 else INF, T[i][j + 1] if j < cols - 1 else INF)
                    b = min(T[i - 1][j] if i > 0 else INF, T[i + 1][j] if i < rows - 1 else INF)
                    t = upwind_update(s[i][j] * h, a, b)
                    if t < T[i][j]:
                        change = max(change, T[i][j] - t if T[i][j] < INF else INF)
                        T[i][j] = t
        if change == 0.0:
            break
    return T


def test_update_formula():
    assert upwind_update(1.0, 0.0, INF) == 1.0
    assert upwind_update(1.0, 1.0, 1.0) == pytest.approx(1 + math.sqrt(2) / 2)
    assert upwind_update(1.0, 0.0, 1.0) == 1.0
    assert upwind_update(1.0, INF, INF) == INF
    t = upwind_update(1.0, 0.3, 0.7)
    assert (t - 0.3) ** 2 + (t - 0.7) ** 2 == pytest.approx(1.0)


def test_worked_example_3x3():
    r = fast_marching([[1.0] * 3 for _ in range(3)], 1.0, [(0, 0)])
    want = [[0.0, 1.0, 2.0], [1.0, 1.0 + math.sqrt(2) / 2, None], [2.0, None, None]]
    T = r.T
    for i in range(3):
        for j in range(3):
            if want[i][j] is not None:
                assert T[i][j] == pytest.approx(want[i][j])
    t12 = upwind_update(1.0, T[0][2], T[1][1])
    assert T[1][2] == pytest.approx(t12) and T[2][1] == pytest.approx(t12)
    assert T[2][2] == pytest.approx(upwind_update(1.0, T[2][1], T[1][2]))
    assert [round(T[i][j], 4) for i, j in r.order] == sorted(round(T[i][j], 4) for i, j in r.order)
    assert round(T[1][2], 4) == 2.5453 and round(T[2][2], 4) == 3.2524


def test_random_grids_match_sweeping_oracle():
    rng = random.Random(20241108)
    for case in range(500):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        s = [[rng.choice([0.5, 1.0, 1.5, 2.0, rng.uniform(0.3, 3.0)]) for _ in range(cols)]
             for _ in range(rows)]
        for _ in range(rng.randint(0, 3)):
            s[rng.randrange(rows)][rng.randrange(cols)] = INF
        cells = [(i, j) for i in range(rows) for j in range(cols) if s[i][j] < INF]
        if not cells:
            continue
        sources = rng.sample(cells, rng.randint(1, min(2, len(cells))))
        h = rng.choice([1.0, 0.5, 0.1])
        r = fast_marching(s, h, sources)
        o = sweep_oracle(s, h, sources)
        for i in range(rows):
            for j in range(cols):
                if o[i][j] == INF:
                    assert r.T[i][j] == INF
                else:
                    assert r.T[i][j] == pytest.approx(o[i][j], rel=1e-12, abs=1e-12)
        assert discrete_residual(r.T, s, h, sources) < 1e-12
        ts = [r.T[i][j] for i, j in r.order]
        assert all(ts[k] <= ts[k + 1] + 1e-15 for k in range(len(ts) - 1))


def test_convergence_point_source():
    errs = []
    for n in (21, 41, 81):
        h = 2.0 / (n - 1)
        c = (n - 1) // 2
        r = fast_marching([[1.0] * n for _ in range(n)], h, [(c, c)])
        errs.append(max(abs(r.T[i][j] - h * math.hypot(i - c, j - c))
                        for i in range(n) for j in range(n)))
        assert r.T[c][n - 1] == pytest.approx(1.0, abs=1e-12)
    assert errs[0] == pytest.approx(8.2112e-2, rel=1e-3)
    assert errs[0] > errs[1] > errs[2]
    assert 1.4 < errs[0] / errs[1] < 2.0 and 1.4 < errs[1] / errs[2] < 2.0


def test_plane_wave_is_exact():
    # sources on the whole left column, s = 1: T = x exactly
    n, h = 9, 0.25
    r = fast_marching([[1.0] * n for _ in range(n)], h, [(i, 0) for i in range(n)])
    assert all(r.T[i][j] == pytest.approx(j * h) for i in range(n) for j in range(n))


def test_obstacle_and_unreachable():
    s = [[1.0, INF, 1.0], [1.0, INF, 1.0], [1.0, INF, 1.0]]
    r = fast_marching(s, 1.0, [(0, 0)])
    assert r.T[0][2] == INF and r.T[1][1] == INF and r.T[2][0] == 2.0
    s[2][1] = 1.0
    r = fast_marching(s, 1.0, [(0, 0)])
    assert r.T[2][1] == 3.0 and r.T[0][2] == 6.0


def test_edge_cases():
    r = fast_marching([[2.0]], 0.5, [(0, 0)])
    assert r.T == [[0.0]] and r.order == [(0, 0)]
    r = fast_marching([[1.0, 2.0, 1.0, 1.0]], 1.0, [(0, 0)])
    assert r.T == [[0.0, 2.0, 3.0, 4.0]]
    r = fast_marching([[1.0] * 3], 1.0, [])
    assert r.T == [[INF] * 3] and r.order == []
    with pytest.raises(ValueError):
        fast_marching([[1.0]], 0.0, [(0, 0)])
    with pytest.raises(ValueError):
        fast_marching([[1.0]], 1.0, [(1, 0)])
    with pytest.raises(ValueError):
        fast_marching([[0.0]], 1.0, [(0, 0)])
