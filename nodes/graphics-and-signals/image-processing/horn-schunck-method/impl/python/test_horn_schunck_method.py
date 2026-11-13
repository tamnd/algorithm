# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horn-schunck-method/. The authors are listed in prov/J0BY18.jsonl.

import math
import random
from fractions import Fraction as F

from horn_schunck_method import derivatives, horn_schunck, local_average

U0, V0 = F(1, 2), F(-1, 4)


def bowl(x, y):
    return 2 * ((x - F(15, 2)) ** 2 + (y - F(15, 2)) ** 2)


def frames(f, n, u0, v0):
    e1 = [[f(F(x), F(y)) for x in range(n)] for y in range(n)]
    e2 = [[f(x - u0, y - v0) for x in range(n)] for y in range(n)]
    return e1, e2


def max_error(u, v, u0, v0):
    return max(math.hypot(a - u0, b - v0) for ru, rv in zip(u, v) for a, b in zip(ru, rv))


def solve(a, b):
    """Gaussian elimination with exact Fractions, the reference solver."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                k = m[r][c] / m[c][c]
                m[r] = [x - k * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def test_cube_estimates_are_exact_for_a_quadratic() -> None:
    e1, e2 = frames(bowl, 6, U0, V0)
    ex, ey, et = derivatives(e1, e2)
    for y in range(5):
        for x in range(5):
            # E(x, y, t) = bowl(x - U0 t, y - V0 t) at the cube center (x + 1/2, y + 1/2, 1/2)
            px, py = x + F(1, 2) - U0 / 2, y + F(1, 2) - V0 / 2
            fx, fy = 4 * (px - F(15, 2)), 4 * (py - F(15, 2))
            assert (ex[y][x], ey[y][x], et[y][x]) == (fx, fy, -U0 * fx - V0 * fy)
            assert ex[y][x] * U0 + ey[y][x] * V0 + et[y][x] == 0


def test_average_weights_sum_to_one() -> None:
    assert local_average([[F(5)] * 4 for _ in range(3)]) == [[F(5)] * 4 for _ in range(3)]
    u = [[F(0)] * 3 for _ in range(3)]
    u[1][1] = F(12)
    assert local_average(u)[0] == [F(1), F(2), F(1)]


def test_constant_flow_is_an_exact_fixed_point() -> None:
    e1, e2 = frames(bowl, 8, U0, V0)
    start = [[U0] * 7 for _ in range(7)], [[V0] * 7 for _ in range(7)]
    u, v = horn_schunck(e1, e2, 10, 3, *start)
    assert u == start[0] and v == start[1]


def test_converges_to_the_constant_flow_from_zero() -> None:
    e1, e2 = frames(bowl, 16, U0, V0)
    e1 = [[float(v) for v in r] for r in e1]
    e2 = [[float(v) for v in r] for r in e2]
    u = v = None
    errors = []
    for _ in range(4):
        u, v = horn_schunck(e1, e2, 10.0, 100, u, v)
        errors.append(max_error(u, v, 0.5, -0.25))
    assert errors[0] < 0.08 and errors[1] < 0.008 and errors[3] < 1e-4
    assert errors == sorted(errors, reverse=True)


def test_iteration_approaches_the_direct_solution() -> None:
    rng = random.Random(8)
    n, alpha2 = 5, F(4)
    e1 = [[F(rng.randrange(16)) for _ in range(n)] for _ in range(n)]
    e2 = [[F(rng.randrange(16)) for _ in range(n)] for _ in range(n)]
    ex, ey, et = derivatives(e1, e2)
    m = n - 1
    idx = {(y, x): k for k, (y, x) in enumerate((y, x) for y in range(m) for x in range(m))}
    size = 2 * m * m
    a = [[F(0)] * size for _ in range(size)]
    b = [F(0)] * size
    for (y, x), k in idx.items():
        gx, gy, gt = ex[y][x], ey[y][x], et[y][x]
        # (alpha2 + Ex^2) u + Ex Ey v - alpha2 ubar = -Ex Et, and the same for v
        for comp, (g, other) in enumerate(((gx, gy), (gy, gx))):
            row = 2 * k + comp
            a[row][row] += alpha2 + g * g
            a[row][2 * k + 1 - comp] += g * other
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy or dx:
                        wgt = F(1, 6) if dy == 0 or dx == 0 else F(1, 12)
                        q = (min(max(y + dy, 0), m - 1), min(max(x + dx, 0), m - 1))
                        a[row][2 * idx[q] + comp] -= alpha2 * wgt
            b[row] = -g * gt
    sol = solve(a, b)
    fu = [[float(sol[2 * idx[(y, x)]]) for x in range(m)] for y in range(m)]
    fv = [[float(sol[2 * idx[(y, x)] + 1]) for x in range(m)] for y in range(m)]
    u, v = horn_schunck([[float(t) for t in r] for r in e1], [[float(t) for t in r] for r in e2], 4.0, 3000)
    assert max(abs(p - q) for r1, r2 in zip(u + v, fu + fv) for p, q in zip(r1, r2)) < 1e-9


def test_one_direction_of_texture_gives_only_the_normal_flow() -> None:
    def ramp(x, y):
        return x * x + 10 * x

    e1, e2 = frames(ramp, 8, U0, V0)
    u, v = horn_schunck([[float(t) for t in r] for r in e1], [[float(t) for t in r] for r in e2], 1.0, 300)
    assert all(t == 0 for r in v for t in r)
    assert max(abs(t - 0.5) for r in u for t in r) < 1e-6
