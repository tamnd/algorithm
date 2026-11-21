# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-krylov-regularization/. The authors are listed in prov/WCZ0JJ.jsonl.
import math
import random
import unittest

from hybrid_krylov_regularization import choose_wgcv, hybrid_lsqr, hybrid_matrix
from imgla import adjoint_gap, matmul, matvec, norm2, rmatvec, solve, transpose


def rand_matrix(rng, m, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]


def krylov_basis(a, y, k):
    """Orthonormal basis of K_k(A^T A, A^T y) by Gram-Schmidt, twice."""
    ata = matmul(transpose(a), a)
    q, w = [], rmatvec(a, y)
    for _ in range(k):
        for _ in range(2):
            for b in q:
                h = sum(p * t for p, t in zip(b, w))
                w = [p - h * t for p, t in zip(w, b)]
        nw = norm2(w)
        q.append([p / nw for p in w])
        w = matvec(ata, q[-1])
    return q


def restricted_tikhonov(a, y, q, lam):
    """Brute force: minimize ||A x - y||^2 + lam ||x||^2 over x = Q c."""
    aq = [matvec(a, b) for b in q]
    k = len(q)
    gram = [[sum(p * t for p, t in zip(aq[i], aq[j])) + (lam if i == j else 0.0)
             for j in range(k)] for i in range(k)]
    c = solve(gram, [sum(p * t for p, t in zip(u, y)) for u in aq])
    return [sum(c[j] * q[j][i] for j in range(k)) for i in range(len(a[0]))]


def integration_problem(n, rel, seed):
    h = 1.0 / n
    a = [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]
    xt = [math.exp(-(((i + 0.5) * h - 0.5) / 0.15) ** 2) for i in range(n)]
    y = matvec(a, xt)
    rng = random.Random(seed)
    e = [rng.gauss(0.0, 1.0) for _ in range(n)]
    ne = norm2(e)
    delta = rel * norm2(y)
    return a, xt, [p + delta * q / ne for p, q in zip(y, e)], delta


def rel_err(x, xt):
    return norm2([p - q for p, q in zip(x, xt)]) / norm2(xt)


class TestHybrid(unittest.TestCase):
    def test_projected_tikhonov_is_restricted_tikhonov(self):
        rng = random.Random(41)
        a = rand_matrix(rng, 9, 6)
        y = [rng.gauss(0.0, 1.0) for _ in range(9)]
        for lam in (0.0, 0.1, 2.0):
            res = hybrid_matrix(a, y, 4, rule=lam)
            for k in range(1, 5):
                ref = restricted_tikhonov(a, y, krylov_basis(a, y, k), lam)
                gap = norm2([p - q for p, q in zip(res.iterates[k - 1], ref)])
                self.assertLess(gap, 1e-8 * norm2(ref))

    def test_full_space_gives_tikhonov(self):
        rng = random.Random(42)
        a = rand_matrix(rng, 8, 5)
        y = [rng.gauss(0.0, 1.0) for _ in range(8)]
        lam = 0.3
        x = hybrid_matrix(a, y, 5, rule=lam).x
        ata = matmul(transpose(a), a)
        for i in range(5):
            ata[i][i] += lam
        ref = solve(ata, rmatvec(a, y))
        for p, q in zip(x, ref):
            self.assertAlmostEqual(p, q, places=9)

    def test_projected_residual_is_true_residual(self):
        rng = random.Random(43)
        a = rand_matrix(rng, 10, 7)
        y = [rng.gauss(0.0, 1.0) for _ in range(10)]
        res = hybrid_matrix(a, y, 5, rule=0.05)
        for x, rn in zip(res.iterates, res.resnorms):
            true = norm2([p - q for p, q in zip(matvec(a, x), y)])
            self.assertAlmostEqual(rn, true, places=10)

    def test_discrepancy_rule(self):
        a, xt, yd, delta = integration_problem(48, 0.01, 7)
        tau = 1.01
        res = hybrid_matrix(a, yd, 15, rule="dp", delta=delta, tau=tau)
        for lam, rn in zip(res.lams, res.resnorms):
            if lam > 0.0:
                self.assertAlmostEqual(rn / (tau * delta), 1.0, places=6)
        # Within a factor 1.5 of the best parameter on a grid, for the same Krylov space.
        best = min(rel_err(res.solve(10.0 ** (-p / 8.0)), xt) for p in range(0, 120))
        self.assertLess(rel_err(res.x, xt), 1.5 * best)

    def test_no_semi_convergence_in_k(self):
        a, xt, yd, delta = integration_problem(48, 0.01, 8)
        dp = hybrid_matrix(a, yd, 15, rule="dp", delta=delta)
        plain = hybrid_matrix(a, yd, 15, rule=0.0)
        e10, e15 = rel_err(dp.iterates[9], xt), rel_err(dp.iterates[14], xt)
        self.assertLess(abs(e15 - e10), 0.05 * e10)
        self.assertGreater(rel_err(plain.x, xt), 2.0 * e15)

    def test_wgcv_minimizes_its_function(self):
        a, xt, yd, delta = integration_problem(48, 0.001, 9)
        res = hybrid_matrix(a, yd, 10, rule="wgcv")
        proj = res.proj
        for omega in (1.0, 1.5):
            lam = choose_wgcv(proj, omega)
            s1 = proj.s[0] ** 2
            fine = min(proj.gcv(s1 * 10.0 ** (-14.0 * i / 2000.0), omega) for i in range(2001))
            self.assertLessEqual(proj.gcv(lam, omega), fine * (1.0 + 1e-9))

    def test_matrix_free_operator(self):
        n = 30
        h = 1.0 / n
        rng = random.Random(44)

        def op(x):
            out, acc = [], 0.0
            for t in x:
                acc += h * t
                out.append(acc)
            return out

        def opt(y):
            out, acc = [0.0] * n, 0.0
            for i in range(n - 1, -1, -1):
                acc += h * y[i]
                out[i] = acc
            return out

        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        self.assertLess(adjoint_gap(op, opt, x, z), 1e-12)
        a = [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]
        free = hybrid_lsqr(op, opt, z, 6, rule=1e-4).x
        dense = hybrid_matrix(a, z, 6, rule=1e-4).x
        self.assertLess(norm2([p - q for p, q in zip(free, dense)]), 1e-8 * norm2(dense))


if __name__ == "__main__":
    unittest.main()
