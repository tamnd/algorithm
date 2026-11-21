# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-svd/. The authors are listed in prov/7EBBWK.jsonl.
# This file also tests the shared helpers imgla.py and imgkit.py.

import cmath
import math
import random
from fractions import Fraction

import imgkit as ik
import imgla as la
from truncated_svd import discrepancy_index, filter_factors, tsvd, tsvd_from_svd, tsvd_path


def rand_matrix(rng, m, n):
    return [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(m)]


def max_abs_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def integration_matrix(n):
    """Rectangle rule for (A x)(s) = int_0^s x(t) dt on [0, 1]: h on and below the diagonal."""
    h = 1.0 / n
    return [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]


# ------------------------------------------------------------------ imgla


def test_svd_reconstructs() -> None:
    rng = random.Random(1)
    for m, n in ((6, 4), (4, 6), (5, 5)):
        a = rand_matrix(rng, m, n)
        u, s, v = la.svd(a)
        p = min(m, n)
        assert len(s) == p and all(s[i] >= s[i + 1] for i in range(p - 1))
        us = [[u[i][j] * s[j] for j in range(p)] for i in range(m)]
        assert max_abs_diff(la.matmul(us, la.transpose(v)), a) < 1e-10
        assert max_abs_diff(la.matmul(la.transpose(u), u), la.eye(p)) < 1e-10
        assert max_abs_diff(la.matmul(la.transpose(v), v), la.eye(p)) < 1e-10


def test_svd_rank_deficient() -> None:
    a = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 0.0, 1.0], [0.0, 0.0, 0.0]]
    u, s, v = la.svd(a)
    assert s[2] < 1e-12
    assert max_abs_diff(la.matmul(la.transpose(u), u), la.eye(3)) < 1e-10
    z = la.zeros(3, 2)
    u0, s0, v0 = la.svd(z)
    assert s0 == [0.0, 0.0]
    assert max_abs_diff(la.matmul(la.transpose(u0), u0), la.eye(2)) < 1e-12


def test_sym_eig_reconstructs() -> None:
    rng = random.Random(2)
    b = rand_matrix(rng, 5, 5)
    a = [[b[i][j] + b[j][i] for j in range(5)] for i in range(5)]
    w, q = la.sym_eig(a)
    assert all(w[i] <= w[i + 1] for i in range(4))
    qw = [[q[i][j] * w[j] for j in range(5)] for i in range(5)]
    assert max_abs_diff(la.matmul(qw, la.transpose(q)), a) < 1e-10
    assert max_abs_diff(la.matmul(la.transpose(q), q), la.eye(5)) < 1e-10


def test_adjoint_gap_matrix() -> None:
    rng = random.Random(3)
    a = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(4)] for _ in range(6)]
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(4)]
    y = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(6)]
    gap = la.adjoint_gap(lambda t: la.matvec(a, t), lambda t: la.rmatvec(a, t), x, y)
    assert gap < 1e-12
    ah = la.conj_transpose(a)
    assert max(abs(p - q) for p, q in zip(la.matvec(ah, y), la.rmatvec(a, y))) < 1e-12
    wrong = la.adjoint_gap(lambda t: la.matvec(a, t), lambda t: la.matvec(la.transpose(a), t), x, y)
    assert wrong > 1e-3


def test_solve_and_cholesky() -> None:
    a = [[Fraction(2), Fraction(1), Fraction(0)], [Fraction(4), Fraction(3), Fraction(1)], [Fraction(0), Fraction(1), Fraction(5)]]
    x = la.solve(a, [Fraction(3), Fraction(8), Fraction(6)])
    assert x == [Fraction(1), Fraction(1), Fraction(1)]
    rng = random.Random(4)
    b = rand_matrix(rng, 5, 5)
    spd = la.matmul(la.transpose(b), b)
    for i in range(5):
        spd[i][i] += 1.0
    rhs = [rng.gauss(0, 1) for _ in range(5)]
    low = la.cholesky(spd)
    assert max_abs_diff(la.matmul(low, la.transpose(low)), spd) < 1e-10
    x1 = la.cho_solve(low, rhs)
    x2 = la.solve(spd, rhs)
    assert max(abs(p - q) for p, q in zip(x1, x2)) < 1e-10
    xm = la.solve(spd, [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    assert len(xm) == 5 and len(xm[0]) == 2
    assert abs(la.dot([1j, 2.0], [1j, 1.0]) - 3.0) < 1e-15
    assert abs(la.norm2([[3.0, 0.0], [0.0, 4.0]]) - 5.0) < 1e-15


# ------------------------------------------------------------------ imgkit


def test_dft_check_value_and_inverse() -> None:
    xf = ik.dft([1, 2, 3, 4])
    for got, want in zip(xf, (10, -2 + 2j, -2, -2 - 2j)):
        assert abs(got - want) < 1e-12
    rng = random.Random(5)
    for n in (8, 12, 16):
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        back = ik.idft(ik.dft(x))
        assert max(abs(p - q) for p, q in zip(back, x)) < 1e-12
        xf = ik.dft(x)
        assert abs(sum(abs(v) ** 2 for v in xf) - n * sum(abs(v) ** 2 for v in x)) < 1e-9
        direct = [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]
        assert max(abs(p - q) for p, q in zip(xf, direct)) < 1e-10


def test_dft2_and_shift() -> None:
    rng = random.Random(6)
    img = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(4)]
    back = ik.idft2(ik.dft2(img))
    assert max_abs_diff(back, img) < 1e-12
    xf = ik.dft2(img)
    assert abs(xf[0][0] - sum(map(sum, img))) < 1e-12
    assert ik.fftshift([0, 1, 2, 3]) == [2, 3, 0, 1]
    assert ik.fftshift([0, 1, 2, 3, 4]) == [3, 4, 0, 1, 2]
    for n in (4, 5):
        assert ik.ifftshift(ik.fftshift(list(range(n)))) == list(range(n))
    sh = ik.fftshift([[0, 1], [2, 3]])
    assert sh == [[3, 2], [1, 0]]
    assert ik.ifftshift(sh) == [[0, 1], [2, 3]]


def test_circ_conv() -> None:
    rng = random.Random(7)
    n = 12
    x = [rng.gauss(0, 1) for _ in range(n)]
    h = [rng.gauss(0, 1) for _ in range(n)]
    y = ik.circ_conv(x, h)
    yf = ik.idft([a * b for a, b in zip(ik.dft(x), ik.dft(h))])
    assert max(abs(p - q) for p, q in zip(y, yf)) < 1e-12
    delta = ik.spikes_1d(n, [0], [1.0])
    assert ik.circ_conv(x, delta) == x
    img = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(4)]
    k2 = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(4)]
    c2 = ik.circ_conv2(img, k2)
    f2 = ik.idft2([[a * b for a, b in zip(ra, rb)] for ra, rb in zip(ik.dft2(img), ik.dft2(k2))])
    assert max_abs_diff(c2, f2) < 1e-12
    d2 = ik.new_image(4, 4)
    d2[0][0] = 1.0
    assert ik.circ_conv2(img, d2) == img


def test_image_ops() -> None:
    a = [[1.0, 2.0], [3.0, 4.0]]
    b = ik.img_scale(a, 2.0)
    assert ik.img_add(a, b) == [[3.0, 6.0], [9.0, 12.0]]
    assert ik.img_dot(a, a) == 30.0
    assert abs(ik.img_norm(a) - math.sqrt(30.0)) < 1e-15
    assert ik.unflatten(ik.flatten(a), 2, 2) == a
    xs, ys = ik.pixel_centers(4)
    assert xs == [-0.75, -0.25, 0.25, 0.75] and ys == [0.75, 0.25, -0.25, -0.75]


def test_shepp_logan_centers() -> None:
    assert len(ik.SHEPP_LOGAN) == 10 and len(ik.MODIFIED_SHEPP_LOGAN) == 10
    assert abs(ik.ellipse_value(0.0, 0.0, ik.SHEPP_LOGAN) - 1.02) < 1e-12
    assert abs(ik.ellipse_value(0.0, 0.0, ik.MODIFIED_SHEPP_LOGAN) - 0.2) < 1e-12
    img = ik.ellipse_phantom(33, ik.MODIFIED_SHEPP_LOGAN)
    assert abs(img[16][16] - 0.2) < 1e-12
    assert img[0][0] == 0.0
    # The large dark ellipse on the right of the image (x = 0.22) lies inside the brain.
    assert abs(ik.ellipse_value(0.22, 0.0, ik.SHEPP_LOGAN) - 1.0) < 1e-12


def test_parallel_beam_matrix() -> None:
    # A bin about twice the pixel size keeps the ripple of pixel-driven projection small.
    n, nbins = 32, 23
    angles = [math.pi * a / 8 for a in range(8)]
    rows = ik.parallel_beam_matrix(n, angles, nbins)
    assert len(rows) == len(angles) * nbins
    rng = random.Random(8)
    x = [rng.gauss(0, 1) for _ in range(n * n)]
    y = [rng.gauss(0, 1) for _ in range(len(rows))]
    gap = la.adjoint_gap(lambda t: ik.sp_matvec(rows, t), lambda t: ik.sp_rmatvec(rows, t, n * n), x, y)
    assert gap < 1e-12
    disk = ik.flatten(ik.disk_phantom(n, 1.0))
    proj = ik.sp_matvec(rows, disk)
    width = 2.0 * math.sqrt(2.0) / nbins
    for a in range(len(angles)):
        for b in range(nbins // 2 - 3, nbins // 2 + 4):
            s = -math.sqrt(2.0) + (b + 0.5) * width
            exact = 2.0 * math.sqrt(1.0 - s * s)
            assert abs(proj[a * nbins + b] - exact) <= 0.05 * exact


def test_noise() -> None:
    rng = random.Random(9)
    draws = [ik.poisson_sample(rng, 4.0) for _ in range(2000)]
    assert abs(sum(draws) / 2000 - 4.0) < 0.2
    big = [ik.poisson_sample(rng, 75.0) for _ in range(400)]
    assert abs(sum(big) / 400 - 75.0) < 2.0
    assert ik.poisson_sample(rng, 0.0) == 0
    g = ik.gauss_noise(rng, (3, 4), 0.5)
    assert len(g) == 3 and len(g[0]) == 4
    v = ik.gauss_noise(random.Random(10), 4000, 2.0)
    var = sum(t * t for t in v) / len(v)
    assert abs(var - 4.0) < 0.3


# ------------------------------------------------------------------ TSVD


def test_integration_operator_singular_values() -> None:
    # The lower triangular matrix of ones has singular values 1 / (2 sin((2k - 1) pi / (4n + 2))).
    n = 24
    _, s, _ = la.svd(integration_matrix(n))
    for k in range(1, n + 1):
        assert abs(s[k - 1] - 1.0 / (2 * n * math.sin((2 * k - 1) * math.pi / (4 * n + 2)))) < 1e-12
    # They approach the continuous values 2 / ((2k - 1) pi); sigma_1 tends to 2 / pi = 0.63662.
    for k in range(1, 4):
        assert abs(s[k - 1] - 2.0 / ((2 * k - 1) * math.pi)) < 0.15 * 2.0 / ((2 * k - 1) * math.pi)
    assert abs(2.0 / math.pi - 0.63662) < 5e-6


def test_tsvd_matches_eigen_route() -> None:
    # Reference: the eigen decomposition of A^T A (a different algorithm) gives
    # x_k = sum_{i<=k} (<v_i, A^T y> / lambda_i) v_i over the k largest eigenvalues.
    rng = random.Random(11)
    m, n = 9, 6
    a = rand_matrix(rng, m, n)
    y = [rng.gauss(0, 1) for _ in range(m)]
    w, q = la.sym_eig(la.matmul(la.transpose(a), a))
    aty = la.rmatvec(a, y)
    for k in range(n + 1):
        x = tsvd(a, y, k)
        ref = [0.0] * n
        for idx in range(n - 1, n - 1 - k, -1):
            vi = [q[j][idx] for j in range(n)]
            c = sum(p * t for p, t in zip(vi, aty)) / w[idx]
            ref = [r + c * t for r, t in zip(ref, vi)]
        assert max(abs(p - t) for p, t in zip(x, ref)) < 1e-9


def test_full_rank_is_least_squares() -> None:
    rng = random.Random(12)
    a = rand_matrix(rng, 8, 5)
    y = [rng.gauss(0, 1) for _ in range(8)]
    x = tsvd(a, y, 5)
    ref = la.solve(la.matmul(la.transpose(a), a), la.rmatvec(a, y))
    assert max(abs(p - t) for p, t in zip(x, ref)) < 1e-10


def test_minimum_norm_on_rank_deficient() -> None:
    # Two equal columns: rank 1. The minimum norm solution splits the weight equally.
    a = [[1.0, 1.0], [1.0, 1.0], [0.0, 0.0]]
    u, s, v = la.svd(a)
    x = tsvd_from_svd(u, s, v, [2.0, 2.0, 5.0], 1)
    assert abs(x[0] - 1.0) < 1e-12 and abs(x[1] - 1.0) < 1e-12
    try:
        tsvd_from_svd(u, s, v, [2.0, 2.0, 5.0], 2)
    except ValueError:
        pass
    else:
        raise AssertionError("k above the rank must be rejected")


def test_path_norms_and_filters() -> None:
    rng = random.Random(13)
    m, n = 10, 7
    a = rand_matrix(rng, m, n)
    y = [rng.gauss(0, 1) for _ in range(m)]
    u, s, v = la.svd(a)
    res, nrm = tsvd_path(u, s, y)
    for k in range(n + 1):
        x = tsvd_from_svd(u, s, v, y, k)
        r = [p - t for p, t in zip(la.matvec(a, x), y)]
        assert abs(la.norm2(r) - res[k]) < 1e-10
        assert abs(la.norm2(x) - nrm[k]) < 1e-10
        assert all(res[k] >= res[k + 1] - 1e-15 for k in range(n))
    assert filter_factors(2, 4) == [1.0, 1.0, 0.0, 0.0]


def test_eckart_young() -> None:
    rng = random.Random(14)
    m, n, k = 6, 5, 2
    a = rand_matrix(rng, m, n)
    u, s, v = la.svd(a)
    ak = [[sum(u[i][t] * s[t] * v[j][t] for t in range(k)) for j in range(n)] for i in range(m)]
    diff = [[a[i][j] - ak[i][j] for j in range(n)] for i in range(m)]
    _, sd, _ = la.svd(diff)
    assert abs(sd[0] - s[k]) < 1e-10
    best_f = la.norm2(diff)
    assert abs(best_f - math.sqrt(sum(t * t for t in s[k:]))) < 1e-10
    for _ in range(100):
        left = rand_matrix(rng, m, k)
        right = rand_matrix(rng, k, n)
        cand = la.matmul(left, right)
        d = [[a[i][j] - cand[i][j] for j in range(n)] for i in range(m)]
        assert la.norm2(d) >= best_f - 1e-12
        _, sc, _ = la.svd(d)
        assert sc[0] >= s[k] - 1e-12


def test_noise_amplification_and_discrepancy() -> None:
    n = 24
    a = integration_matrix(n)
    u, s, v = la.svd(a)
    t = [(j + 0.5) / n for j in range(n)]
    x_true = [math.sin(math.pi * tj) for tj in t]
    y_exact = la.matvec(a, x_true)
    rng = random.Random(15)
    e = [rng.gauss(0, 1) for _ in range(n)]
    delta = 1e-2
    scale = delta / la.norm2(e)
    y = [p + scale * q for p, q in zip(y_exact, e)]
    errs = [la.norm2([p - q for p, q in zip(tsvd_from_svd(u, s, v, y, k), x_true)]) for k in range(n + 1)]
    best = min(range(n + 1), key=lambda k: errs[k])
    assert 0 < best < n
    assert errs[n] > 2.0 * errs[best]
    res, _ = tsvd_path(u, s, y)
    k_dp = discrepancy_index(res, delta, tau=1.1)
    assert k_dp is not None
    assert res[k_dp] <= 1.1 * delta and (k_dp == 0 or res[k_dp - 1] > 1.1 * delta)
    assert errs[k_dp] <= 3.0 * errs[best]


def worst_case_error(sigma, delta, nu, rho):
    """TSVD error for the worst pair of a source element and a noise vector of a diagonal problem.

    k is the largest index with sigma_k >= delta^(1/(2 nu + 1)). The exact solution is
    rho sigma_{k+1}^(2 nu) e_{k+1} (it satisfies the source condition with ||w|| = rho)
    and the noise is delta e_k. Returns (error, k).
    """
    p = len(sigma)
    u = la.eye(p)
    level = delta ** (1.0 / (2 * nu + 1))
    k = max(i + 1 for i in range(p) if sigma[i] >= level)
    x_true = [0.0] * p
    x_true[k] = rho * sigma[k] ** (2 * nu)
    y = [sigma[i] * x_true[i] for i in range(p)]
    y[k - 1] += delta
    x = tsvd_from_svd(u, sigma, u, y, k)
    return la.norm2([p_ - q for p_, q in zip(x, x_true)]), k


def test_convergence_rate() -> None:
    sigma = [1.0 / i for i in range(1, 161)]
    deltas = [1e-1, 1e-2, 1e-3, 1e-4]
    rho = 1.0
    for nu in (0.5, 1.0):
        rate = 2 * nu / (2 * nu + 1)
        errs = []
        for d in deltas:
            err, _ = worst_case_error(sigma, d, nu, rho)
            assert err <= (1 + rho) * d ** rate + 1e-15
            errs.append(err)
        xs = [math.log(d) for d in deltas]
        ys = [math.log(e) for e in errs]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        slope = sum((p - mx) * (q - my) for p, q in zip(xs, ys)) / sum((p - mx) ** 2 for p in xs)
        assert abs(slope - rate) < 0.15


def test_rate_bound_random_noise() -> None:
    # Error <= delta / sigma_k + rho sigma_{k+1}^(2 nu) for any noise with ||e|| <= delta.
    rng = random.Random(16)
    p, nu, rho = 60, 0.5, 1.0
    sigma = [1.0 / i for i in range(1, p + 1)]
    u = la.eye(p)
    w = [rng.gauss(0, 1) for _ in range(p)]
    wn = la.norm2(w)
    w = [rho * t / wn for t in w]
    x_true = [sigma[i] ** (2 * nu) * w[i] for i in range(p)]
    for d in (1e-2, 1e-3, 1e-4):
        e = [rng.gauss(0, 1) for _ in range(p)]
        en = la.norm2(e)
        y = [sigma[i] * x_true[i] + d * e[i] / en for i in range(p)]
        k = max(i + 1 for i in range(p) if sigma[i] >= d ** (1.0 / (2 * nu + 1)))
        x = tsvd_from_svd(u, sigma, u, y, k)
        err = la.norm2([a - b for a, b in zip(x, x_true)])
        bound = d / sigma[k - 1] + (rho * sigma[k] ** (2 * nu) if k < p else 0.0)
        assert err <= bound + 1e-14
        assert bound <= (1 + rho) * d ** (2 * nu / (2 * nu + 1)) + 1e-15
