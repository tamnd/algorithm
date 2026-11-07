# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qr-algorithm/. The authors are listed in prov/9ACH0R.jsonl.

import cmath
import math
import random
from fractions import Fraction

from qr_algorithm import hessenberg, qr_algorithm

U = 2.0**-53


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def ct(a):
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def fro(a):
    return math.sqrt(sum(abs(t) ** 2 for row in a for t in row))


def diff(a, b):
    return math.sqrt(sum(abs(x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb)))


def eye(n):
    return [[float(i == j) for j in range(n)] for i in range(n)]


def check_schur(a, res, c=20):
    """Backward error, orthogonality and exact triangularity, against small multiples of n u."""
    n = len(a)
    assert res.converged
    assert all(res.t[i][j] == 0 for i in range(n) for j in range(i))
    assert diff(mm(mm(res.q, res.t), ct(res.q)), a) <= c * n * U * max(fro(a), 1e-300)
    assert diff(mm(ct(res.q), res.q), eye(n)) <= c * n * U


def householder_orthogonal(n, rng, k=3):
    q = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(k):
        v = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        vv = sum(t * t for t in v)
        if vv == 0:
            continue
        qv = [sum(q[i][j] * v[j] for j in range(n)) for i in range(n)]
        q = [[q[i][j] - 2 * qv[i] * v[j] / vv for j in range(n)] for i in range(n)]
    return q


def rational_inverse(m):
    n = len(m)
    a = [list(r) + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(m)]
    for c in range(n):
        p = next(i for i in range(c, n) if a[i][c] != 0)
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [t / piv for t in a[c]]
        for i in range(n):
            if i != c and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return [r[n:] for r in a]


def similar(v, d, vi):
    """V D V^{-1} for a block diagonal D given as a full rational matrix, rounded to floats."""
    return [[float(x) for x in row] for row in mm(mm(v, d), vi)]


def block_diag(lam):
    """Real block diagonal matrix: an int gives a 1 by 1 block, a pair (a, b) the block [[a, b], [-b, a]]."""
    n = sum(1 if isinstance(t, int) else 2 for t in lam)
    d = [[Fraction(0)] * n for _ in range(n)]
    i, eig = 0, []
    for t in lam:
        if isinstance(t, int):
            d[i][i] = Fraction(t)
            eig.append(complex(t))
            i += 1
        else:
            a, b = t
            d[i][i] = d[i + 1][i + 1] = Fraction(a)
            d[i][i + 1], d[i + 1][i] = Fraction(b), Fraction(-b)
            eig += [complex(a, b), complex(a, -b)]
            i += 2
    return d, eig


def known_nonsymmetric(lam, rng):
    d, eig = block_diag(lam)
    n = len(d)
    v = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        v[i][i] += 7
    return similar(v, d, rational_inverse(v)), eig


def known_symmetric(lam, rng):
    n = len(lam)
    q = householder_orthogonal(n, rng)
    d = [[Fraction(lam[i]) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    return similar(q, d, [list(r) for r in zip(*q)])


def charpoly(a):
    """Exact coefficients of det(t I - A), c[0] = 1, by Faddeev-LeVerrier in Fractions."""
    n = len(a)
    a = [[Fraction(t) for t in row] for row in a]
    c = [Fraction(1)]
    m = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        am = mm(a, m)
        m = [[am[i][j] + (c[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = mm(a, m)
        c.append(-sum(am[i][i] for i in range(n)) / k)
    return c


def poly_from_roots(roots):
    c = [1 + 0j]
    for z in roots:
        c = [x - z * y for x, y in zip(c + [0j], [0j] + c)]
    return c


def match(got, want, tol):
    """Greedy matching of two lists of complex numbers."""
    rest = list(want)
    for z in got:
        k = min(range(len(rest)), key=lambda i: abs(rest[i] - z))
        assert abs(rest[k] - z) <= tol, (z, rest[k])
        rest.pop(k)


def orders(e):
    return [math.log(e[k + 1] / e[k]) / math.log(e[k] / e[k - 1]) for k in range(1, len(e) - 1)]


def runs(history):
    """Split the history into the sequences of |h[hi][hi-1]| for each fixed hi."""
    out = {}
    for hi, v in history:
        out.setdefault(hi, []).append(v)
    return out.values()


def test_page_example():
    a = [[1.0, 2.0, 3.0], [1.0, 4.0, 5.0], [0.0, 1.0, 6.0]]
    want = [0.4492308744, 2.9154240704, 7.6353450551]
    seen = {}
    for shift, steps in (("none", 39), ("rayleigh", 9), ("wilkinson", 5)):
        res = qr_algorithm(a, shift=shift, maxit=200)
        check_schur(a, res)
        match(res.eigenvalues, want, 1e-9)
        assert res.iterations == steps
        seen[shift] = [v for hi, v in res.history if hi == 2]
    for k, w in enumerate([8.51e-02, 6.79e-05, 2.78e-11]):
        assert abs(seen["wilkinson"][k] - w) <= 0.01 * w
    for k, w in enumerate([2.36e00, 5.72e-01, 6.75e-02, 9.22e-03]):
        assert abs(seen["none"][k] - w) <= 0.01 * w
    c = charpoly([[1, 2, 3], [1, 4, 5], [0, 1, 6]])
    assert c == [1, -11, 27, -10]


def test_random_real_backward_error():
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randint(1, 10)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        res = qr_algorithm(a)
        check_schur(a, res)
        tr = sum(a[i][i] for i in range(n))
        assert abs(sum(res.eigenvalues) - tr) <= 20 * n * U * fro(a)


def test_random_complex_backward_error():
    rng = random.Random(2)
    for _ in range(20):
        n = rng.randint(1, 8)
        a = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
        check_schur(a, qr_algorithm(a))


def test_exact_characteristic_polynomial_trace_and_determinant():
    rng = random.Random(3)
    for _ in range(25):
        n = rng.randint(2, 7)
        ai = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        a = [[float(t) for t in r] for r in ai]
        res = qr_algorithm(a)
        check_schur(a, res)
        c = charpoly(ai)
        got = poly_from_roots(res.eigenvalues)
        nrm = fro(a)
        for k in range(n + 1):
            assert abs(got[k] - float(c[k])) <= 1e-9 * math.comb(n, k) * max(1.0, nrm) ** k
        det = (-1) ** n * c[n]
        prod = 1
        for z in res.eigenvalues:
            prod *= z
        assert abs(prod - float(det)) <= 1e-9 * max(1.0, nrm) ** n


def test_known_real_and_complex_spectra():
    rng = random.Random(4)
    for _ in range(20):
        lam = [rng.randint(-9, 9) for _ in range(rng.randint(0, 3))]
        lam += [(rng.randint(-5, 5), rng.randint(1, 5)) for _ in range(rng.randint(1, 2))]
        a, eig = known_nonsymmetric(lam, rng)
        res = qr_algorithm(a)
        check_schur(a, res, c=50)
        tol = 1e-8 * max(1.0, fro(a))
        # Equal eigenvalues may be defective in principle, but V D V^{-1} is diagonalizable here.
        match(res.eigenvalues, eig, tol)


def test_symmetric_known_spectrum_real_eigenvalues():
    rng = random.Random(5)
    for _ in range(20):
        n = rng.randint(2, 8)
        lam = [rng.randint(-20, 20) for _ in range(n)]
        a = known_symmetric(lam, rng)
        res = qr_algorithm(a)
        check_schur(a, res)
        match(res.eigenvalues, [complex(t) for t in lam], 1e-12 * max(1.0, fro(a)))
        # For a Hermitian matrix the Schur factor is diagonal up to rounding.
        off = math.sqrt(sum(abs(res.t[i][j]) ** 2 for i in range(n) for j in range(i + 1, n)))
        assert off <= 100 * n * U * fro(a)


def test_toeplitz_and_companion():
    n = 10
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    res = qr_algorithm(a)
    check_schur(a, res)
    match(res.eigenvalues, [complex(2 - 2 * math.cos(k * math.pi / (n + 1))) for k in range(1, n + 1)], 1e-13)
    coeffs = poly_from_roots([1, 2, 3, 4, 5])  # (t-1)...(t-5)
    comp = [[-coeffs[j + 1].real for j in range(5)]] + [[float(i == j) for j in range(5)] for i in range(4)]
    res = qr_algorithm(comp)
    check_schur(comp, res)
    match(res.eigenvalues, [1, 2, 3, 4, 5], 1e-8)


def test_unshifted_rate_is_the_eigenvalue_ratio():
    # Unshifted QR is simultaneous iteration: h[n][n-1] shrinks like |lambda_n / lambda_{n-1}|^k,
    # and the diagonal of T comes out ordered by decreasing modulus.
    for seed in range(6):
        rng = random.Random(seed)
        for a in (known_nonsymmetric([8, 4, 2, 1], rng)[0], known_symmetric([1, 8, 2, 4], rng)):
            res = qr_algorithm(a, shift="none", maxit=500)
            check_schur(a, res, c=50)
            e = [v for hi, v in res.history if hi == 3]
            obs = [e[k + 1] / e[k] for k in range(len(e) - 9, len(e) - 1)]
            assert all(abs(o - 0.5) <= 0.01 for o in obs)
            assert [round(abs(z), 9) for z in res.eigenvalues] == [8, 4, 2, 1]


def test_wilkinson_shift_cubic_for_symmetric_quadratic_otherwise():
    rng = random.Random(7)
    sym, non = [], []
    for _ in range(30):
        n = rng.randint(3, 8)
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        s = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
        for a, out in ((s, sym), (b, non)):
            res = qr_algorithm(a)
            for e in runs(res.history):
                e = [t for t in e if t > 1e-200]
                if len(e) >= 3 and e[0] < 0.1:
                    out += orders(e)
    sym.sort()
    non.sort()
    assert len(sym) >= 10 and len(non) >= 10
    assert 2.6 <= sym[len(sym) // 2] <= 3.6
    assert 1.6 <= non[len(non) // 2] <= 2.5


def test_iterations_per_eigenvalue_observed():
    # Observed, not proved: about 2 to 4 complex single-shift steps per eigenvalue.
    rng = random.Random(8)
    steps = eigs = 0
    for _ in range(30):
        n = rng.randint(4, 12)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        res = qr_algorithm(a)
        assert res.converged
        steps += res.iterations
        eigs += n
    assert 2.0 <= steps / eigs <= 4.0


def test_cyclic_permutation_needs_exceptional_shifts():
    n = 6
    p = [[1.0 if i == j + 1 or (i == 0 and j == n - 1) else 0.0 for j in range(n)] for i in range(n)]
    res = qr_algorithm(p, shift="none", maxit=50)
    assert not res.converged and all(abs(v - 1.0) <= 1e-12 for hi, v in res.history)
    res = qr_algorithm(p)
    check_schur(p, res)
    assert res.history[8][1] >= 0.999  # the first 9 Wilkinson-shift steps make no progress
    match(res.eigenvalues, [cmath.exp(2j * math.pi * k / n) for k in range(n)], 1e-12)


def test_rayleigh_shift_stalls_on_the_swap_wilkinson_does_not():
    a = [[0.0, 1.0], [1.0, 0.0]]
    res = qr_algorithm(a, shift="rayleigh")
    check_schur(a, res)
    assert 10 <= res.iterations <= 15 and all(v >= 0.999 for hi, v in res.history[:9])
    res = qr_algorithm(a)
    check_schur(a, res)
    assert res.iterations == 1
    match(res.eigenvalues, [1, -1], 1e-15)


def test_jordan_block_is_ill_conditioned_but_backward_stable():
    n = 8
    a = [[2.0 if i == j else (1.0 if j == i + 1 else 0.0) for j in range(n)] for i in range(n)]
    a[n - 1][0] = 1e-14  # make it Hessenberg-unreduced and nontrivial
    res = qr_algorithm(a)
    check_schur(a, res)
    # The eigenvalues are 2 + (1e-14)^(1/8) w with w an 8th root of unity, modulus 0.0178.
    for z in res.eigenvalues:
        assert abs(abs(z - 2) - 1e-14 ** (1 / 8)) <= 0.01
    assert abs(sum(res.eigenvalues) / n - 2) <= 10 * U


def test_edge_cases():
    res = qr_algorithm([[3.5]])
    assert res.converged and res.eigenvalues == [3.5] and res.iterations == 0
    z = [[0.0] * 3 for _ in range(3)]
    res = qr_algorithm(z)
    assert res.converged and all(t == 0 for t in res.eigenvalues)
    tri = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 0.0, 6.0]]
    res = qr_algorithm(tri)
    check_schur(tri, res)
    assert res.iterations == 0 and res.eigenvalues == [1, 4, 6]
    block = [[1.0, 2.0, 0.0, 0.0], [3.0, 4.0, 0.0, 0.0], [0.0, 0.0, 0.0, -1.0], [0.0, 0.0, 1.0, 0.0]]
    res = qr_algorithm(block)
    check_schur(block, res)
    match(res.eigenvalues, [(5 + math.sqrt(33)) / 2, (5 - math.sqrt(33)) / 2, 1j, -1j], 1e-13)


def test_hessenberg_reduction_invariants():
    rng = random.Random(9)
    for _ in range(20):
        n = rng.randint(1, 9)
        a = [[complex(rng.uniform(-1, 1), rng.uniform(-1, 1) * (n % 2)) for _ in range(n)] for _ in range(n)]
        h, q = hessenberg(a)
        assert all(h[i][j] == 0 for i in range(n) for j in range(i - 1))
        assert diff(mm(mm(q, h), ct(q)), a) <= 20 * n * U * fro(a)
        assert diff(mm(ct(q), q), eye(n)) <= 20 * n * U
