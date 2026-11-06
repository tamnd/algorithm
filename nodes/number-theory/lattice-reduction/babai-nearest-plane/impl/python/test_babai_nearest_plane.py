# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/babai-nearest-plane/. The authors are listed in prov/70W13Q.jsonl.

import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from babai_nearest_plane import babai_nearest_plane


def dot(u, v):
    return sum((Fraction(a) * b for a, b in zip(u, v)), Fraction(0))


def combo(x, b):
    return [sum((xi * row[j] for xi, row in zip(x, b)), Fraction(0)) for j in range(len(b[0]))]


def sub(u, v):
    return [a - c for a, c in zip(u, v)]


def inverse(a):
    """Exact inverse of a square rational matrix (test-local, row reduction)."""
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        m[c] = [x / m[c][c] for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def dual(b):
    """Rows d_i with <d_i, b_j> = [i = j] in the span of b: D = (B B^T)^-1 B."""
    gi = inverse([[dot(u, v) for v in b] for u in b])
    return [combo(gi[i], b) for i in range(len(b))]


def gso_norms(b):
    bs, norms = [], []
    for row in b:
        w = [Fraction(c) for c in row]
        for s, ns in zip(bs, norms):
            if ns != 0:
                w = sub(w, [dot(row, s) / ns * c for c in s])
        bs.append(w)
        norms.append(dot(w, w))
    return bs, norms


def lll(b):
    """Textbook exact LLL with delta = 3/4 (test-local), used only to shrink oracle boxes."""
    b = [[Fraction(c) for c in row] for row in b]
    k = 1
    while k < len(b):
        bs, ns = gso_norms(b[: k + 1])
        for j in range(k - 1, -1, -1):
            q = floor(dot(b[k], bs[j]) / ns[j] + Fraction(1, 2))
            if q:
                b[k] = sub(b[k], [q * c for c in b[j]])
        mu = dot(b[k], bs[k - 1]) / ns[k - 1]
        nk = ns[k]
        if nk >= (Fraction(3, 4) - mu * mu) * ns[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            k = max(k - 1, 1)
    return b


def np_upper(c, t):
    """A lattice vector near t on basis c (test-local), used only as a radius for the oracle."""
    bs, ns = gso_norms(c)
    w = [Fraction(a) for a in t]
    for i in range(len(c) - 1, -1, -1):
        q = floor(dot(w, bs[i]) / ns[i] + Fraction(1, 2))
        w = sub(w, [q * a for a in c[i]])
    return sub([Fraction(a) for a in t], w)


def cvp_brute(b, t, r2):
    """Exact squared distance from t to the lattice, given r2 >= that distance squared.

    t is split as p + o with p in the span and o orthogonal to it, so the distance is
    ||o||^2 plus the distance from p. On an LLL basis C with Gram-Schmidt rows c_j* the
    squared distance from p to x C is the sum over j of (tau_j - x_j - sum_{i>j} x_i mu_ij)^2
    ||c_j*||^2, so every vector within the radius is found by fixing x_{n-1}, ..., x_0 in turn
    and keeping only the integers that keep the partial sum within the radius.
    """
    c = lll(b)
    bs, ns = gso_norms(c)
    n = len(c)
    tau = [dot(t, bs[j]) / ns[j] for j in range(n)]
    p = combo(tau, bs)
    o = sub(t, p)
    oo = dot(o, o)
    e0 = sub(t, np_upper(c, t))
    r = min(r2, dot(e0, e0)) - oo
    mu = [[dot(c[i], bs[j]) / ns[j] for j in range(n)] for i in range(n)]
    best = [r]

    def search(j, x, partial):
        if j < 0:
            best[0] = min(best[0], partial)
            return
        centre = tau[j] - sum((x[i] * mu[i][j] for i in range(j + 1, n)), Fraction(0))
        w = sqrt_up((best[0] - partial) / ns[j])
        for xj in range(floor(centre - w), floor(centre + w) + 1):
            add = (centre - xj) ** 2 * ns[j]
            if partial + add <= best[0]:
                x[j] = xj
                search(j - 1, x, partial + add)
        x[j] = 0

    search(n - 1, [0] * n, Fraction(0))
    return best[0] + oo


def sqrt_up(q):
    """A rational upper bound for the square root of a nonnegative rational."""
    k = 10**6
    return Fraction(isqrt(q.numerator * k * k // q.denominator) + 1, k)


def random_basis(rng, n, m, lo=-4, hi=4):
    while True:
        b = [[rng.randint(lo, hi) for _ in range(m)] for _ in range(n)]
        _, ns = gso_norms(b)
        if all(x != 0 for x in ns):
            return b


def random_target(rng, m, scale=6):
    return [Fraction(rng.randint(-scale * 8, scale * 8), rng.randint(1, 8)) for _ in range(m)]


def check_in_lattice(b, x, v):
    assert all(isinstance(xi, int) for xi in x)
    assert v == combo(x, b)


def residual_ok(b, t, v):
    """t - v has Gram-Schmidt coefficients in [-1/2, 1/2)."""
    bs, ns = gso_norms(b)
    e = sub(t, v)
    return all(-Fraction(1, 2) <= dot(e, s) / q < Fraction(1, 2) for s, q in zip(bs, ns))


def test_worked_example_good_and_bad_basis():
    t = [Fraction(7, 10), Fraction(23, 10)]
    x, v = babai_nearest_plane([[2, 0], [1, 2]], t)
    assert x == [0, 1] and v == [1, 2]
    assert dot(sub(t, v), sub(t, v)) == Fraction(9, 50)
    x, v = babai_nearest_plane([[4, 4], [9, 10]], t)
    assert x == [-4, 2] and v == [2, 4]
    assert dot(sub(t, v), sub(t, v)) == Fraction(229, 50)


def test_cvp_page_example():
    t = [Fraction(1, 2), Fraction(5, 2)]
    assert babai_nearest_plane([[2, 0], [1, 2]], t)[1] == [1, 2]
    assert babai_nearest_plane([[4, 4], [9, 10]], t)[1] == [2, 4]


def test_target_in_lattice_is_returned():
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 6)
        b = random_basis(rng, n, n + rng.randint(0, 2))
        x0 = [rng.randint(-20, 20) for _ in range(n)]
        x, v = babai_nearest_plane(b, combo(x0, b))
        assert x == x0


def test_dimension_one_is_exact():
    rng = random.Random(22)
    for _ in range(300):
        a = rng.randint(1, 30) * rng.choice([-1, 1])
        t = Fraction(rng.randint(-500, 500), rng.randint(1, 9))
        x, v = babai_nearest_plane([[a]], [t])
        assert abs(t - v[0]) == min(abs(t - k * a) for k in range(-600, 601))


def test_ties_round_up():
    assert babai_nearest_plane([[2]], [1]) == ([1], [2])
    assert babai_nearest_plane([[2]], [-1]) == ([0], [0])


def test_orthogonal_basis_is_exact():
    rng = random.Random(23)
    for _ in range(300):
        n = rng.randint(1, 5)
        diag = [rng.randint(1, 6) for _ in range(n)]
        b = [[diag[i] if i == j else 0 for j in range(n)] for i in range(n)]
        t = random_target(rng, n)
        x, v = babai_nearest_plane(b, t)
        # the distance splits into independent coordinates
        best = sum(min((t[i] - k * diag[i]) ** 2 for k in range(-60, 61)) for i in range(n))
        assert dot(sub(t, v), sub(t, v)) == best


def test_decodes_within_half_the_shortest_gram_schmidt_vector():
    rng = random.Random(24)
    for _ in range(250):
        n = rng.randint(1, 6)
        b = random_basis(rng, n, n + rng.randint(0, 1))
        _, ns = gso_norms(b)
        u_x = [rng.randint(-9, 9) for _ in range(n)]
        e = [Fraction(rng.randint(-50, 50), 7) for _ in range(len(b[0]))]
        ee = dot(e, e)
        if ee * 4 >= min(ns):
            shrink = sqrt_up(ee * 4 / min(ns)) + 1
            e = [c / shrink for c in e]
        assert dot(e, e) * 4 < min(ns)
        x, v = babai_nearest_plane(b, [a + c for a, c in zip(combo(u_x, b), e)])
        assert x == u_x


def test_random_against_brute_force_cvp():
    rng = random.Random(25)
    count = 0
    for n, reps in ((2, 220), (3, 160), (4, 90), (5, 35), (6, 15)):
        for _ in range(reps):
            m = n + rng.randint(0, 1)
            b = random_basis(rng, n, m, -3, 3)
            t = random_target(rng, m, 3)
            x, v = babai_nearest_plane(b, t)
            check_in_lattice(b, x, v)
            assert residual_ok(b, t, v)
            e = sub(t, v)
            ne = dot(e, e)
            best = cvp_brute(b, t, ne)
            assert best <= ne
            _, ns = gso_norms(b)
            # proved: ||t - v||^2 <= dist^2 (1 + max_k sum_{i<=k} ||b_i*||^2 / ||b_k*||^2)
            factor = 1 + max(sum(ns[: k + 1]) / ns[k] for k in range(n))
            assert ne <= best * factor
            count += 1
    assert count >= 500


def test_lll_reduced_basis_within_two_to_the_n_over_two():
    rng = random.Random(26)
    for _ in range(200):
        n = rng.randint(2, 5)
        b = lll(random_basis(rng, n, n, -6, 6))
        t = random_target(rng, n, 4)
        x, v = babai_nearest_plane(b, t)
        ne = dot(sub(t, v), sub(t, v))
        assert ne <= 2**n * cvp_brute(b, t, ne)


def test_translation_invariance():
    rng = random.Random(27)
    for _ in range(100):
        n = rng.randint(1, 5)
        b = random_basis(rng, n, n)
        t = random_target(rng, n)
        z = [rng.randint(-7, 7) for _ in range(n)]
        x, v = babai_nearest_plane(b, t)
        x2, v2 = babai_nearest_plane(b, [a + c for a, c in zip(t, combo(z, b))])
        assert x2 == [a + c for a, c in zip(x, z)]


def test_target_outside_span_uses_projection():
    b = [[1, 0, 0], [0, 3, 0]]
    x, v = babai_nearest_plane(b, [Fraction(2, 5), Fraction(5, 2), Fraction(100)])
    assert x == [0, 1] and v == [0, 3, 0]


def test_nearly_dependent_basis():
    rng = random.Random(28)
    for _ in range(150):
        n = rng.randint(2, 5)
        base = [rng.randint(-5, 5) for _ in range(n)]
        b = [[c * 1000 + rng.randint(-1, 1) * (i == j) for j, c in enumerate(base)] for i in range(n)]
        _, ns = gso_norms(b)
        if any(q == 0 for q in ns):
            continue
        t = random_target(rng, n, 50)
        x, v = babai_nearest_plane(b, t)
        check_in_lattice(b, x, v)
        assert residual_ok(b, t, v)


def test_dependent_rows_raise():
    with pytest.raises(ValueError):
        babai_nearest_plane([[1, 2], [2, 4]], [0, 0])
    with pytest.raises(ValueError):
        babai_nearest_plane([[1, 2]], [0, 0, 0])
    with pytest.raises(ValueError):
        babai_nearest_plane([], [])
