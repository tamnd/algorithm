# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landweber-iteration/. The authors are listed in prov/G6JZZF.jsonl.
import math
import random
import unittest

from imgla import adjoint_gap, matvec, norm2, rmatvec, svd
from landweber_iteration import error_bound, filter_factor, landweber, landweber_matrix


def rand_matrix(rng, m, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]


def pinv_solution(a, y):
    """x^dagger = A^dagger y from the SVD (the reference method)."""
    u, s, v = svd(a)
    tol = max(s) * 1e-12
    x = [0.0] * len(a[0])
    for i, si in enumerate(s):
        if si > tol:
            c = sum(u[r][i] * y[r] for r in range(len(y))) / si
            x = [xj + c * v[j][i] for j, xj in enumerate(x)]
    return x


def cumsum(x, h):
    """Matrix-free rectangle rule for (A x)(s) = int_0^s x(t) dt."""
    out, acc = [], 0.0
    for v in x:
        acc += h * v
        out.append(acc)
    return out


def rcumsum(y, h):
    """The adjoint of cumsum: (A* y)(t) = int_t^1 y(s) ds."""
    out, acc = [0.0] * len(y), 0.0
    for i in range(len(y) - 1, -1, -1):
        acc += h * y[i]
        out[i] = acc
    return out


class TestLandweber(unittest.TestCase):
    def test_check_value(self):
        self.assertAlmostEqual(filter_factor(0.01, 1.0, 100), 0.63397, places=5)
        res = landweber_matrix([[1.0]], [1.0], omega=0.01, kmax=100)
        self.assertAlmostEqual(res.x[0], 0.63397, places=5)

    def test_page_trace(self):
        # A = diag(1, 0.1), x^dagger = (1, 1), y^delta = (1, 0.11), omega = 1, tau delta = 0.015.
        a = [[1.0, 0.0], [0.0, 0.1]]
        res = landweber_matrix(a, [1.0, 0.11], omega=1.0, kmax=1000, delta=0.01, tau=1.5)
        self.assertEqual((res.k, res.stopped), (199, "discrepancy"))
        self.assertAlmostEqual(res.x[1], 1.1 * (1.0 - 0.99 ** 199), places=10)
        self.assertAlmostEqual(res.residuals[0], 1.00603, places=5)
        self.assertGreater(res.residuals[198], 0.015)
        x100 = landweber_matrix(a, [1.0, 0.11], omega=1.0, kmax=100).x
        self.assertAlmostEqual(x100[1], 0.69736, places=5)

    def test_filter_factors_match_svd(self):
        rng = random.Random(11)
        a = rand_matrix(rng, 7, 5)
        y = [rng.gauss(0.0, 1.0) for _ in range(7)]
        u, s, v = svd(a)
        omega = 1.0 / (s[0] * s[0])
        for k in (1, 3, 10, 40):
            x = landweber_matrix(a, y, omega=omega, kmax=k).x
            ref = [0.0] * 5
            for i, si in enumerate(s):
                c = filter_factor(omega, si, k) * sum(u[r][i] * y[r] for r in range(7)) / si
                ref = [rj + c * v[j][i] for j, rj in enumerate(ref)]
            for p, q in zip(x, ref):
                self.assertAlmostEqual(p, q, places=10)

    def test_residual_is_monotone(self):
        rng = random.Random(12)
        for _ in range(5):
            a = rand_matrix(rng, 8, 6)
            y = [rng.gauss(0.0, 1.0) for _ in range(8)]
            res = landweber_matrix(a, y, kmax=60)
            for r0, r1 in zip(res.residuals, res.residuals[1:]):
                self.assertLessEqual(r1, r0 + 1e-12)

    def test_exact_data_converges_to_minimum_norm_solution(self):
        rng = random.Random(13)
        b = rand_matrix(rng, 6, 2)
        c = rand_matrix(rng, 2, 4)
        a = [[sum(b[i][t] * c[t][j] for t in range(2)) for j in range(4)] for i in range(6)]
        y = [rng.gauss(0.0, 1.0) for _ in range(6)]
        u, s, v = svd(a)
        omega = 1.0 / (s[0] * s[0])
        x = landweber_matrix(a, y, omega=omega, kmax=4000).x
        ref = pinv_solution(a, y)
        self.assertLess(norm2([p - q for p, q in zip(x, ref)]), 1e-8 * norm2(ref))

    def test_discrepancy_stop(self):
        rng = random.Random(14)
        a = rand_matrix(rng, 10, 6)
        xt = [rng.gauss(0.0, 1.0) for _ in range(6)]
        e = [rng.gauss(0.0, 1.0) for _ in range(10)]
        delta = 0.05
        ne = norm2(e)
        y = [p + delta * q / ne for p, q in zip(matvec(a, xt), e)]
        tau = 1.2
        res = landweber_matrix(a, y, kmax=100000, delta=delta, tau=tau)
        self.assertEqual(res.stopped, "discrepancy")
        self.assertLessEqual(res.residuals[-1], tau * delta)
        for r in res.residuals[:-1]:
            self.assertGreater(r, tau * delta)

    def test_data_error_bound(self):
        rng = random.Random(15)
        a = rand_matrix(rng, 9, 6)
        u, s, v = svd(a)
        omega = 1.0 / (s[0] * s[0])
        y = [rng.gauss(0.0, 1.0) for _ in range(9)]
        e = [rng.gauss(0.0, 1.0) for _ in range(9)]
        delta = 1e-3
        ne = norm2(e)
        yd = [p + delta * q / ne for p, q in zip(y, e)]
        for k in (1, 5, 25, 125):
            x0 = landweber_matrix(a, y, omega=omega, kmax=k).x
            x1 = landweber_matrix(a, yd, omega=omega, kmax=k).x
            gap = norm2([p - q for p, q in zip(x0, x1)])
            self.assertLessEqual(gap, math.sqrt(omega * k) * delta * (1 + 1e-12))

    def test_rate_on_integration_operator(self):
        # Diagonal model of (A x)(s) = int_0^s x on L^2(0, 1). x^dagger = 1 - t = A* 1
        # has coefficients sqrt2 sigma_k^2, so nu = 1/2 and rho = 1. The noise sits on
        # the component that the step count k amplifies most.
        n = 200
        sig = [2.0 / ((2 * k - 1) * math.pi) for k in range(1, n + 1)]
        xd = [math.sqrt(2.0) * t * t for t in sig]
        y = [t * x for t, x in zip(sig, xd)]
        omega = 1.0 / (sig[0] * sig[0])

        def op(x):
            return [t * v for t, v in zip(sig, x)]

        errs, deltas = [], [1e-2, 1e-3, 1e-4]
        for delta in deltas:
            k = math.ceil(1.0 / delta)
            m = max(range(n), key=lambda i: filter_factor(omega, sig[i], k) / sig[i])
            yd = list(y)
            yd[m] += delta
            x = landweber(op, op, yd, omega, k).x
            err = norm2([p - q for p, q in zip(x, xd)])
            self.assertLessEqual(err, error_bound(0.5, 1.0, omega, k, delta))
            errs.append(err)
        for i in range(2):
            slope = math.log(errs[i] / errs[i + 1]) / math.log(deltas[i] / deltas[i + 1])
            self.assertLess(abs(slope - 0.5), 0.15)

    def test_matrix_free_operator(self):
        n = 50
        h = 1.0 / n
        rng = random.Random(16)
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        self.assertLess(adjoint_gap(lambda w: cumsum(w, h), lambda w: rcumsum(w, h), x, z), 1e-12)
        a = [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]
        y = [rng.gauss(0.0, 1.0) for _ in range(n)]
        omega = 1.0 / sum(v * v for row in a for v in row)
        free = landweber(lambda w: cumsum(w, h), lambda w: rcumsum(w, h), y, omega, 30).x
        dense = landweber(lambda w: matvec(a, w), lambda w: rmatvec(a, w), y, omega, 30).x
        for p, q in zip(free, dense):
            self.assertAlmostEqual(p, q, places=10)


if __name__ == "__main__":
    unittest.main()
