# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-order-hold-discretization/. The authors are listed in prov/TDAR9X.jsonl.

import cmath
import itertools
import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
import ctlsim as cs
from zero_order_hold_discretization import zoh, zoh_ss


def maxdiff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def rand_int_matrix(rng, n, m, lo=-5, hi=5):
    return [[rng.randint(lo, hi) for _ in range(m)] for _ in range(n)]


def leibniz_det(a):
    n = len(a)
    total = 0
    for perm in itertools.permutations(range(n)):
        inversions = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        prod = 1
        for i in range(n):
            prod *= a[i][perm[i]]
        total += -prod if inversions % 2 else prod
    return total


# ctlmat


def test_ctlmat_self_test():
    assert cm._self_test()


def test_basic_ops():
    a = [[1, 2, 3], [4, 5, 6]]
    assert cm.zeros(2, 3) == [[0, 0, 0], [0, 0, 0]]
    assert cm.eye(2) == [[1, 0], [0, 1]]
    assert cm.transpose(a) == [[1, 4], [2, 5], [3, 6]]
    assert cm.add(a, a) == cm.scale(2, a)
    assert cm.sub(a, a) == cm.zeros(2, 3)
    assert cm.mul(a, cm.transpose(a)) == [[14, 32], [32, 77]]
    assert cm.matvec(a, [1, 0, -1]) == [-2, -2]
    assert cm.dot([1, 2, 3], [4, 5, 6]) == 32
    assert cm.trace([[1, 2], [3, 4]]) == 5
    with pytest.raises(ValueError):
        cm.mul(a, a)
    with pytest.raises(ValueError):
        cm.add(a, cm.eye(2))


def test_mul_associative_exact():
    rng = random.Random(1)
    for _ in range(50):
        n, m, p, q = (rng.randint(1, 4) for _ in range(4))
        a = rand_int_matrix(rng, n, m)
        b = [[Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(p)] for _ in range(m)]
        c = rand_int_matrix(rng, p, q)
        assert cm.mul(cm.mul(a, b), c) == cm.mul(a, cm.mul(b, c))


def test_block_kron_vec():
    a = [[1, 2], [3, 4]]
    b = [[5], [6]]
    m = cm.block([[a, b], [0, [[7]]]])
    assert m == [[1, 2, 5], [3, 4, 6], [0, 0, 7]]
    assert cm.kron([[1, 2]], [[1], [3]]) == [[1, 2], [3, 6]]
    assert cm.vec(a) == [1, 3, 2, 4]
    assert cm.unvec([1, 3, 2, 4], 2) == a
    rng = random.Random(2)
    for _ in range(30):
        n, m2, p = (rng.randint(1, 3) for _ in range(3))
        aa = rand_int_matrix(rng, n, m2)
        x = rand_int_matrix(rng, m2, p)
        bb = rand_int_matrix(rng, p, 2)
        left = cm.vec(cm.mul(cm.mul(aa, x), bb))
        right = cm.matvec(cm.kron(cm.transpose(bb), aa), cm.vec(x))
        assert left == right


def test_solve_inv_det_exact():
    rng = random.Random(3)
    for _ in range(80):
        n = rng.randint(1, 5)
        a = rand_int_matrix(rng, n, n)
        d = cm.det(a)
        assert d == leibniz_det(a)
        b = [rng.randint(-9, 9) for _ in range(n)]
        if d == 0:
            with pytest.raises(ValueError):
                cm.solve(a, b)
            continue
        x = cm.solve(a, b)
        assert all(isinstance(v, Fraction) for v in x)
        assert cm.matvec(a, x) == b
        assert cm.mul(a, cm.inv(a)) == cm.eye(n)
        c = rand_int_matrix(rng, n, n)
        assert cm.det(cm.mul(a, c)) == d * cm.det(c)


def test_solve_float_and_complex():
    rng = random.Random(4)
    for _ in range(50):
        n = rng.randint(1, 6)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] += 3.0
        b = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(n)]
        x = cm.solve(a, b)
        assert maxdiff(cm.mul(a, x), b) < 1e-12
        ac = [[complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            ac[i][i] += 4.0
        bc = [complex(1, 1)] * n
        xc = cm.solve(ac, bc)
        assert max(abs(u - v) for u, v in zip(cm.matvec(ac, xc), bc)) < 1e-12


def test_charpoly_exact():
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randint(1, 6)
        a = rand_int_matrix(rng, n, n)
        p = cm.charpoly(a)
        assert len(p) == n + 1 and p[0] == 1
        for s in range(-3, 4):
            si_a = [[(s if i == j else 0) - a[i][j] for j in range(n)] for i in range(n)]
            assert cm.polyval(p, s) == cm.det(si_a)
        acc = cm.zeros(n)
        for k, c in enumerate(p):
            acc = cm.add(acc, cm.scale(c, cm.mat_power(a, n - k)))
        assert acc == cm.zeros(n)


def test_poly_arithmetic():
    rng = random.Random(6)
    for _ in range(50):
        p = [rng.randint(-5, 5) for _ in range(rng.randint(1, 6))]
        q = [rng.randint(-5, 5) for _ in range(rng.randint(1, 6))]
        for x in (Fraction(-3, 2), Fraction(0), Fraction(2), Fraction(5, 3)):
            assert cm.polyval(cm.polyadd(p, q), x) == cm.polyval(p, x) + cm.polyval(q, x)
            assert cm.polyval(cm.polymul(p, q), x) == cm.polyval(p, x) * cm.polyval(q, x)
        x = Fraction(1, 7)
        eps = Fraction(1, 10 ** 30)
        slope = (cm.polyval(p, x + eps) - cm.polyval(p, x)) / eps
        assert abs(slope - cm.polyval(cm.polyder(p), x)) < Fraction(1, 10 ** 20)
    assert cm.polyadd([1, 2, 3], [-1, 0, 0]) == [2, 3]


def test_polyroots_against_known_roots():
    rng = random.Random(7)
    for _ in range(100):
        roots = []
        while len(roots) < rng.randint(1, 6):
            if rng.random() < 0.5:
                roots.append(complex(rng.uniform(-3, 3), 0.0))
            else:
                z = complex(rng.uniform(-3, 3), rng.uniform(0.2, 3))
                roots += [z, z.conjugate()]
        roots.sort(key=lambda v: (v.real, v.imag))
        if any(abs(u - v) < 0.1 for u, v in itertools.combinations(roots, 2)):
            continue
        p = [1.0]
        for z in roots:
            p = cm.polymul(p, [1.0, -z])
        p = [v.real for v in p]
        got = cm.polyroots(p)
        assert len(got) == len(roots)
        assert max(abs(u - v) for u, v in zip(got, roots)) < 1e-9
        for u, v in itertools.combinations(got, 2):
            assert (u.real, u.imag) <= (v.real, v.imag)


def test_polyroots_special_cases():
    assert cm.polyroots([5]) == []
    assert cm.polyroots([2, -4]) == [complex(2, 0)]
    r = cm.polyroots([1, 0, 0])
    assert r == [0j, 0j]
    r = cm.polyroots([1, -1, 0.5])
    assert all(abs(abs(z) - 1 / math.sqrt(2)) < 1e-12 for z in r)
    assert r[0].imag < 0 < r[1].imag and r[0] == r[1].conjugate()
    r = cm.polyroots([1, -2, 1])
    assert all(abs(z - 1) < 1e-7 for z in r)
    r = cm.polyroots([1, 4, 6, 4, 1])
    assert all(abs(z + 1) < 1e-2 for z in r)
    assert sorted(r, key=lambda v: (v.real, v.imag)) == r
    assert sorted((z.conjugate() for z in r), key=lambda v: (v.real, v.imag)) == r
    rng = random.Random(16)
    for _ in range(300):
        d = rng.randint(1, 10)
        p = [rng.choice([-1, 1]) * rng.uniform(0.5, 5)] + [rng.uniform(-5, 5) for _ in range(d)]
        for z in cm.polyroots(p):
            size = sum(abs(c) * abs(z) ** (d - k) for k, c in enumerate(p))
            assert abs(cm.polyval(p, z)) <= 1e-12 * size
    r = cm.polyroots([1, -1j])
    assert abs(r[0] - 1j) < 1e-15
    r = cm.polyroots([Fraction(1), Fraction(-3), Fraction(2)])
    assert abs(r[0] - 1) < 1e-12 and abs(r[1] - 2) < 1e-12
    with pytest.raises(ValueError):
        cm.polyroots([0, 0])


def test_expm_known_cases():
    for t in (0.0, 0.3, 1.0, 5.0, 40.0):
        e = cm.expm([[0, t], [-t, 0]])
        want = [[math.cos(t), math.sin(t)], [-math.sin(t), math.cos(t)]]
        assert maxdiff(e, want) < 1e-12 * max(1.0, t)
    e = cm.expm([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
    assert maxdiff(e, [[1, 1, 0.5], [0, 1, 1], [0, 0, 1]]) < 1e-15
    e = cm.expm([[-30.0, 0.0], [0.0, 2.0]])
    assert abs(e[0][0] - math.exp(-30)) < 1e-14 * math.exp(-30) * 100
    assert abs(e[1][1] - math.exp(2)) < 1e-13 * math.exp(2)
    e = cm.expm([[1j * math.pi]])
    assert abs(e[0][0] + 1) < 1e-14


def test_expm_against_eigendecomposition():
    rng = random.Random(8)
    for _ in range(40):
        n = rng.randint(1, 5)
        lam = [rng.uniform(-3, 2) for _ in range(n)]
        v = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            v[i][i] += 2.0
        vi = cm.inv(v)
        a = cm.mul(cm.mul(v, [[lam[i] if i == j else 0.0 for j in range(n)] for i in range(n)]), vi)
        want = cm.mul(cm.mul(v, [[math.exp(lam[i]) if i == j else 0.0 for j in range(n)] for i in range(n)]), vi)
        got = cm.expm(a)
        scale_ = max(1.0, max(abs(x) for row in want for x in row))
        assert maxdiff(got, want) < 1e-11 * scale_
        assert maxdiff(cm.mul(got, cm.expm(cm.scale(-1, a))), cm.eye(n)) < 1e-10


def test_expm_sum_rule():
    a = [[1.0, 2.0], [0.0, 3.0]]
    b = cm.mul(a, a)
    assert maxdiff(cm.expm(cm.add(a, b)), cm.mul(cm.expm(a), cm.expm(b))) < 1e-12 * math.exp(12)
    p = [[0.0, 1.0], [0.0, 0.0]]
    q = [[0.0, 0.0], [1.0, 0.0]]
    assert maxdiff(cm.expm(cm.add(p, q)), cm.mul(cm.expm(p), cm.expm(q))) > 0.1


def test_mat_power():
    rng = random.Random(9)
    a = rand_int_matrix(rng, 3, 3)
    acc = cm.eye(3)
    for k in range(8):
        assert cm.mat_power(a, k) == acc
        acc = cm.mul(acc, a)
    b = [[2, 1], [1, 1]]
    assert cm.mul(cm.mat_power(b, -3), cm.mat_power(b, 3)) == cm.eye(2)


def test_pos_def_exact_and_float_agree():
    rng = random.Random(10)
    seen = set()
    for _ in range(200):
        n = rng.randint(1, 5)
        r = rand_int_matrix(rng, n, n, -3, 3)
        s = cm.add(cm.mul(cm.transpose(r), r), cm.scale(rng.randint(-4, 2), cm.eye(n)))
        exact = cm.is_pos_def(s)
        flt = cm.is_pos_def([[float(v) for v in row] for row in s])
        # Skip matrices that are singular, where float rounding may decide.
        if cm.det(s) == 0:
            continue
        assert exact == flt
        seen.add(exact)
        if exact:
            assert cm.is_pos_def(s, Fraction(0)) and not cm.is_pos_def(s, 10 ** 6)
    assert seen == {True, False}
    assert not cm.is_pos_def([[1, 2], [0, 5]])
    assert cm.is_symmetric([[1.0, 2.0], [2.0 + 1e-13, 1.0]], 1e-12)
    assert not cm.is_symmetric([[1, 2], [3, 1]])


def test_norm2():
    assert abs(cm.norm2([3, 4]) - 5.0) < 1e-15
    assert abs(cm.norm2([[1j]]) - 1.0) < 1e-12
    rng = random.Random(11)
    for _ in range(30):
        n, m = rng.randint(1, 5), rng.randint(1, 5)
        u = [rng.uniform(-1, 1) for _ in range(n)]
        v = [rng.uniform(-1, 1) for _ in range(m)]
        a = [[ui * vj for vj in v] for ui in u]
        assert abs(cm.norm2(a) - cm.norm2(u) * cm.norm2(v)) < 1e-12
        b = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]
        nb = cm.norm2(b)
        for _ in range(20):
            x = [rng.gauss(0, 1) for _ in range(m)]
            assert cm.norm2(cm.matvec(b, x)) <= nb * cm.norm2(x) * (1 + 1e-12)


# ctlsim


def test_ctlsim_self_test():
    assert cs._self_test()


def test_rk4_exact_on_polynomials():
    f = lambda t, x, u: [t ** 3]
    x = cs.rk4_step(f, 0.0, [0.0], None, 0.5)
    assert abs(x[0] - 0.5 ** 4 / 4) < 1e-15
    _, xs, _ = cs.simulate(f, [0.0], 0.0, 2.0, 0.25)
    assert abs(xs[-1][0] - 4.0) < 1e-12


def test_simulate_hold_and_steps():
    calls = []

    def control(t, x):
        calls.append(t)
        return [1.0]

    f = cs.lti([[0.0, 1.0], [0.0, 0.0]], [[0.0], [1.0]])
    ts, xs, us = cs.simulate(f, [0.0, 0.0], 0.0, 1.0, 0.01, control, hold=0.1)
    assert len(ts) == 101 and len(xs) == 101 and len(us) == 100
    assert len(calls) == 10
    assert all(abs(t - 0.1 * j) < 1e-12 for j, t in enumerate(calls))
    assert abs(xs[-1][0] - 0.5) < 1e-12 and abs(xs[-1][1] - 1.0) < 1e-12
    with pytest.raises(ValueError):
        cs.simulate(f, [0.0, 0.0], 0.0, 1.0, 0.03)
    with pytest.raises(ValueError):
        cs.simulate(f, [0.0, 0.0], 0.0, 1.0, 0.01, control, hold=0.015)


def test_simulate_discrete_exact():
    a = [[Fraction(1, 2), 1], [0, Fraction(1, 3)]]
    def F(k, x, u):
        y = cm.matvec(a, x)
        y[0] += u
        return y

    xs, us = cs.simulate_discrete(F, [1, 1], 5, lambda k, x: Fraction(k))
    x = [1, 1]
    for k in range(5):
        x = cm.matvec(a, x)
        x[0] += k
        assert xs[k + 1] == x
    assert us == [0, 1, 2, 3, 4]


def test_lti_scalar_and_none_input():
    f = cs.lti([[-1.0]], [[2.0]])
    assert f(0.0, [1.0], 3.0) == [5.0]
    assert f(0.0, [1.0], None) == [-1.0]
    assert cs.lti([[2.0]])(0.0, [1.0], [7.0]) == [2.0]


# zero-order hold


def test_double_integrator_check_values():
    for h in (0.1, 0.5, 1.0, 2.0):
        ad, bd = zoh([[0, 1], [0, 0]], [[0], [1]], h)
        assert maxdiff(ad, [[1, h], [0, 1]]) < 1e-14
        assert maxdiff(bd, [[h * h / 2], [h]]) < 1e-14


def test_rotation_and_scalar():
    for h in (0.1, 1.0, 3.0):
        ad, bd = zoh([[0, 1], [-1, 0]], [[0], [1]], h)
        assert maxdiff(ad, [[math.cos(h), math.sin(h)], [-math.sin(h), math.cos(h)]]) < 1e-13
        assert maxdiff(bd, [[1 - math.cos(h)], [math.sin(h)]]) < 1e-13
    for a in (-2.0, -0.5, 0.7):
        ad, bd = zoh([[a]], [[3.0]], 0.4)
        assert abs(ad[0][0] - math.exp(a * 0.4)) < 1e-14
        assert abs(bd[0][0] - 3.0 * (math.exp(a * 0.4) - 1) / a) < 1e-13


def test_against_inverse_formula():
    rng = random.Random(12)
    for _ in range(40):
        n, m = rng.randint(1, 5), rng.randint(1, 3)
        a = [[rng.uniform(-2, 2) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] -= 2.5
        b = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]
        h = rng.choice([0.05, 0.2, 1.0])
        ad, bd = zoh(a, b, h)
        assert maxdiff(ad, cm.expm(cm.scale(h, a))) < 1e-13
        want = cm.mul(cm.solve(a, cm.sub(ad, cm.eye(n))), b)
        assert maxdiff(bd, want) < 1e-11


def test_semigroup_property():
    rng = random.Random(13)
    for _ in range(20):
        n, m = rng.randint(1, 4), rng.randint(1, 2)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        b = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]
        ad1, bd1 = zoh(a, b, 0.3)
        ad2, bd2 = zoh(a, b, 0.6)
        assert maxdiff(ad2, cm.mul(ad1, ad1)) < 1e-12
        assert maxdiff(bd2, cm.add(cm.mul(ad1, bd1), bd1)) < 1e-12


def test_against_rk4_with_held_input():
    rng = random.Random(14)
    h, dt, steps = 0.2, 0.002, 15
    assert round(h / dt) == 100
    for _ in range(4):
        n, m = rng.randint(1, 4), rng.randint(1, 2)
        a = [[rng.uniform(-1.5, 1.0) for _ in range(n)] for _ in range(n)]
        b = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]
        inputs = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(steps)]
        x0 = [rng.uniform(-1, 1) for _ in range(n)]
        control = lambda t, x: inputs[round(t / h)]
        ts, xs, _ = cs.simulate(cs.lti(a, b), x0, 0.0, steps * h, dt, control, hold=h)
        ad, bd = zoh(a, b, h)
        x = x0
        for k in range(steps):
            x = [p + q for p, q in zip(cm.matvec(ad, x), cm.matvec(bd, inputs[k]))]
            cont = xs[(k + 1) * 100]
            assert max(abs(p - q) for p, q in zip(x, cont)) < 1e-9


def test_poles_map_by_exponential():
    rng = random.Random(15)
    for _ in range(20):
        n = rng.randint(1, 4)
        lam = sorted(rng.uniform(-3, 1) for _ in range(n))
        a = [[lam[i] if i == j else (rng.uniform(-1, 1) if j > i else 0.0) for j in range(n)] for i in range(n)]
        t = rand_int_matrix(rng, n, n)
        for i in range(n):
            t[i][i] += 20
        a = cm.mul(cm.mul(t, a), cm.inv([[float(v) for v in row] for row in t]))
        h = 0.5
        ad, _ = zoh(a, [[1.0]] * n, h)
        got = cm.polyroots(cm.charpoly(ad))
        want = [complex(math.exp(v * h), 0) for v in lam]
        if any(abs(u - v) < 0.05 for u, v in itertools.combinations(want, 2)):
            continue
        assert max(abs(u - v) for u, v in zip(got, want)) < 1e-7


def test_sampling_zeros_triple_integrator():
    a = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
    b = [[0], [0], [1]]
    c = [[1, 0, 0]]
    for h in (0.1, 1.0):
        ad, bd, cc, _ = zoh_ss(a, b, c, [[0]], h)
        # det(zI - Ad + Bd C) - det(zI - Ad) is the numerator of C (zI - Ad)^(-1) Bd.
        num = cm.polyadd(cm.charpoly(cm.sub(ad, cm.mul(bd, cc))), cm.scale(-1, [cm.charpoly(ad)])[0])
        num = num[-3:]
        want = [h ** 3 / 6, 4 * h ** 3 / 6, h ** 3 / 6]
        assert max(abs(p - q) for p, q in zip(num, want)) < 1e-12
        zs = cm.polyroots(num)
        assert abs(zs[0] - (-2 - math.sqrt(3))) < 1e-9 and abs(zs[1] - (-2 + math.sqrt(3))) < 1e-9


def test_bad_input():
    with pytest.raises(ValueError):
        zoh([[0.0]], [[1.0]], 0.0)
    with pytest.raises(ValueError):
        zoh([[0.0, 1.0]], [[1.0]], 0.1)
