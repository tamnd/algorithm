# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lsqr/. The authors are listed in prov/BNV7VJ.jsonl.
import math
import random
import unittest

from imgla import adjoint_gap, matmul, matvec, norm2, rmatvec, solve, transpose
from lsqr import lsqr, lsqr_matrix


def rand_matrix(rng, m, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]


def krylov_solution(a, y, k):
    """Brute force: minimize ||y - A x|| over K_k(A^T A, A^T y) with an orthonormal basis."""
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
    aq = [matvec(a, b) for b in q]
    gram = [[sum(p * t for p, t in zip(u, v)) for v in aq] for u in aq]
    c = solve(gram, [sum(p * t for p, t in zip(u, y)) for u in aq])
    return [sum(c[j] * q[j][i] for j in range(k)) for i in range(len(a[0]))]


def max_orth_loss(vs):
    return max(abs(sum(p * q for p, q in zip(vs[i], vs[j])) - (1.0 if i == j else 0.0))
               for i in range(len(vs)) for j in range(len(vs)))


class TestLSQR(unittest.TestCase):
    def test_bidiagonalization(self):
        rng = random.Random(31)
        a = rand_matrix(rng, 9, 6)
        y = [rng.gauss(0.0, 1.0) for _ in range(9)]
        k = 4
        res = lsqr_matrix(a, y, k, keep=True)
        self.assertLess(max_orth_loss(res.us), 1e-12)
        self.assertLess(max_orth_loss(res.vs[:k]), 1e-12)
        # A v_i = alpha_i u_i + beta_{i+1} u_{i+1}, the columns of A V_k = U_{k+1} B_k.
        for i in range(k):
            lhs = matvec(a, res.vs[i])
            rhs = [res.alphas[i] * p + res.betas[i + 1] * q for p, q in zip(res.us[i], res.us[i + 1])]
            for p, q in zip(lhs, rhs):
                self.assertAlmostEqual(p, q, places=12)
        self.assertAlmostEqual(res.betas[0], norm2(y), places=12)

    def test_iterates_match_krylov_least_squares(self):
        rng = random.Random(32)
        a = rand_matrix(rng, 10, 6)
        y = [rng.gauss(0.0, 1.0) for _ in range(10)]
        res = lsqr_matrix(a, y, 6)
        for k in range(1, 7):
            ref = krylov_solution(a, y, k)
            gap = norm2([p - q for p, q in zip(res.iterates[k], ref)])
            self.assertLess(gap, 1e-8 * norm2(ref))

    def test_residual_norm_estimate(self):
        rng = random.Random(33)
        a = rand_matrix(rng, 10, 6)
        y = [rng.gauss(0.0, 1.0) for _ in range(10)]
        res = lsqr_matrix(a, y, 6)
        for x, est in zip(res.iterates, res.resnorms):
            true = norm2([p - q for p, q in zip(y, matvec(a, x))])
            self.assertAlmostEqual(est, true, places=10)
        for r0, r1 in zip(res.resnorms, res.resnorms[1:]):
            self.assertLessEqual(r1, r0 + 1e-14)

    def test_full_rank_least_squares(self):
        rng = random.Random(34)
        a = rand_matrix(rng, 8, 5)
        y = [rng.gauss(0.0, 1.0) for _ in range(8)]
        x = lsqr_matrix(a, y, 5).x
        ref = solve(matmul(transpose(a), a), rmatvec(a, y))
        for p, q in zip(x, ref):
            self.assertAlmostEqual(p, q, places=9)

    def test_small_cases(self):
        res = lsqr_matrix([[2.0]], [6.0], 5)
        self.assertEqual(res.x, [3.0])
        self.assertEqual(res.stopped, "breakdown")
        self.assertEqual(res.k, 1)
        res = lsqr_matrix([[1.0, 2.0], [3.0, 4.0]], [0.0, 0.0], 5)
        self.assertEqual((res.x, res.k, res.stopped), ([0.0, 0.0], 0, "breakdown"))

    def test_discrepancy_stop(self):
        rng = random.Random(35)
        a = rand_matrix(rng, 12, 6)
        xt = [rng.gauss(0.0, 1.0) for _ in range(6)]
        e = [rng.gauss(0.0, 1.0) for _ in range(12)]
        delta, tau = 0.3, 1.1
        ne = norm2(e)
        y = [p + delta * q / ne for p, q in zip(matvec(a, xt), e)]
        res = lsqr_matrix(a, y, 50, delta=delta, tau=tau)
        self.assertEqual(res.stopped, "discrepancy")
        self.assertLessEqual(res.resnorms[-1], tau * delta)
        for r in res.resnorms[:-1]:
            self.assertGreater(r, tau * delta)

    def test_loss_of_orthogonality_and_reorthogonalization(self):
        n = 60
        h = 1.0 / n
        a = [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]
        y = [(i + 0.5) * h * (1.0 - (i + 0.5) * h / 2.0) for i in range(n)]
        plain = lsqr_matrix(a, y, 20, keep=True)
        full = lsqr_matrix(a, y, 20, reorth=True)
        self.assertGreater(max_orth_loss(plain.vs), 0.1)
        self.assertLess(max_orth_loss(full.vs), 1e-12)

    def test_matrix_free_operator(self):
        n = 40
        h = 1.0 / n
        rng = random.Random(36)

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
        free = lsqr(op, opt, z, 4).x
        dense = lsqr_matrix(a, z, 4).x
        self.assertLess(norm2([p - q for p, q in zip(free, dense)]), 1e-8 * norm2(dense))


if __name__ == "__main__":
    unittest.main()
