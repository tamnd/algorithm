# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/revised-simplex-method/. The authors are listed in prov/0XTBN3.jsonl.

import itertools
import random
from fractions import Fraction

from revised_simplex_method import revised_simplex_method


def solve_square(cols, b):
    """Solve cols x = b for m columns and m rows. None if the columns are dependent."""
    m = len(b)
    rows = [[Fraction(cols[j][i]) for j in range(m)] + [Fraction(b[i])] for i in range(m)]
    for col in range(m):
        p = next((i for i in range(col, m) if rows[i][col] != 0), None)
        if p is None:
            return None
        rows[col], rows[p] = rows[p], rows[col]
        rows[col] = [v / rows[col][col] for v in rows[col]]
        for i in range(m):
            if i != col and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [vi - f * vc for vi, vc in zip(rows[i], rows[col])]
    return [rows[i][m] for i in range(m)]


def feasible_bases(a, b, n):
    """All (basis, x) with A_B nonsingular and A_B^-1 b >= 0 (A has full row rank m)."""
    m = len(a)
    out = []
    for s in itertools.combinations(range(n), m):
        xs = solve_square([[row[j] for row in a] for j in s], b)
        if xs is not None and all(v >= 0 for v in xs):
            x = [Fraction(0)] * n
            for j, v in zip(s, xs):
                x[j] = v
            out.append((list(s), x))
    return out


def brute(a, b, c):
    n = len(c)
    vertices = [x for _, x in feasible_bases(a, b, n)]
    rays = [x for _, x in feasible_bases(a + [[1] * n], [0] * len(a) + [1], n)] if len(a) + 1 <= n else []
    if any(sum(cj * dj for cj, dj in zip(c, d)) < 0 for d in rays):
        return "unbounded", None
    return "optimal", min(sum(cj * xj for cj, xj in zip(c, x)) for x in vertices)


def check(a, b, c, res):
    m, n = len(a), len(c)
    assert all(v >= 0 for v in res.x)
    assert all(sum(a[i][j] * res.x[j] for j in range(n)) == b[i] for i in range(m))
    if res.status == "optimal":
        slack = [c[j] - sum(a[i][j] * res.y[i] for i in range(m)) for j in range(n)]
        assert all(s >= 0 for s in slack)
        assert sum(bi * yi for bi, yi in zip(b, res.y)) == res.value
    else:
        d = res.ray
        assert all(v >= 0 for v in d)
        assert all(sum(a[i][j] * d[j] for j in range(n)) == 0 for i in range(m))
        assert sum(cj * dj for cj, dj in zip(c, d)) < 0


def inverse_checker(a, b):
    """A callback that checks B^-1 A_B = I and B^-1 b >= 0 after each pivot."""
    m = len(a)

    def on_pivot(basis, binv):
        for i in range(m):
            for k, j in enumerate(basis):
                assert sum(binv[i][t] * a[t][j] for t in range(m)) == int(i == k)
        assert all(sum(binv[i][t] * b[t] for t in range(m)) >= 0 for i in range(m))

    return on_pivot


def test_example() -> None:
    a = [[1, 0, 1, 0, 0], [0, 2, 0, 1, 0], [3, 2, 0, 0, 1]]
    b, c = [4, 12, 18], [-3, -5, 0, 0, 0]
    res = revised_simplex_method(a, b, c, [2, 3, 4], rule="dantzig", on_pivot=inverse_checker(a, b))
    assert res.status == "optimal" and res.value == -36 and res.pivots == 2
    assert res.x == [2, 6, 2, 0, 0] and res.y == [0, Fraction(-3, 2), -1]
    assert res.basis == [2, 1, 0]


def test_beale() -> None:
    a = [[1, 0, 0, Fraction(1, 4), -8, -1, 9], [0, 1, 0, Fraction(1, 2), -12, Fraction(-1, 2), 3], [0, 0, 1, 0, 0, 1, 0]]
    b, c = [0, 0, 1], [0, 0, 0, Fraction(-3, 4), 20, Fraction(-1, 2), 6]
    assert revised_simplex_method(a, b, c, [0, 1, 2], rule="dantzig").status == "cycle"
    res = revised_simplex_method(a, b, c, [0, 1, 2], rule="bland", on_pivot=inverse_checker(a, b))
    assert res.status == "optimal" and res.value == Fraction(-5, 4)


def test_klee_minty() -> None:
    for n in range(1, 7):
        a = [[2 * 10 ** (i - j) for j in range(i)] + [1] + [0] * (n - i - 1) + [int(k == i) for k in range(n)] for i in range(n)]
        b = [100**i for i in range(n)]
        c = [-(10 ** (n - 1 - j)) for j in range(n)] + [0] * n
        res = revised_simplex_method(a, b, c, list(range(n, 2 * n)), rule="dantzig")
        assert res.pivots == 2**n - 1 and res.value == -(100 ** (n - 1))


def test_against_brute_force() -> None:
    rng = random.Random(83)
    seen = set()
    done = 0
    while done < 600:
        m, n = rng.randint(1, 3), rng.randint(3, 6)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        b = [0 if rng.random() < 0.4 else rng.randint(0, 6) for _ in range(m)]
        c = [rng.randint(-4, 4) for _ in range(n)]
        starts = feasible_bases(a, b, n)
        if not starts:
            continue
        basis, _ = rng.choice(starts)
        want = brute(a, b, c)
        for rule in ("bland", "dantzig"):
            res = revised_simplex_method(a, b, c, basis, rule=rule, on_pivot=inverse_checker(a, b))
            if res.status == "cycle":
                continue
            assert (res.status, res.value) == want, (a, b, c, basis, rule)
            check(a, b, c, res)
        seen.add(want[0])
        done += 1
    assert seen == {"optimal", "unbounded"}
