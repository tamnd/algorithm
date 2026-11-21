# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cgls/. The authors are listed in prov/83ANX4.jsonl.
import math
import random
import unittest
from fractions import Fraction

from cgls import cgls, cgls_matrix, ritz_filter_factor
from imgla import adjoint_gap, matmul, matvec, norm2, solve, svd, sym_eig, transpose


def exact_ops(a):
    """A x and A^T y in exact arithmetic (no float start value)."""
    at = transpose(a)
    return (lambda x: [sum(v * w for v, w in zip(row, x)) for row in a],
            lambda y: [sum(v * w for v, w in zip(row, y)) for row in at])


def int_matrix(rng, m, n):
    return [[Fraction(rng.randint(-4, 4)) for _ in range(n)] for _ in range(m)]


def krylov_solution(a, y, k):
    """Brute force: minimize ||y - A x|| over x in K_k(A^T A, A^T y), exactly."""
    ap, atp = exact_ops(a)
    basis = [atp(y)]
    for _ in range(k - 1):
        basis.append(atp(ap(basis[-1])))
    ak = [ap(b) for b in basis]
    gram = [[sum(p * q for p, q in zip(u, w)) for w in ak] for u in ak]
    rhs = [sum(p * q for p, q in zip(u, y)) for u in ak]
    c = solve(gram, rhs)
    n = len(a[0])
    return [sum(c[j] * basis[j][i] for j in range(k)) for i in range(n)]


class TestCGLS(unittest.TestCase):
    def test_iterates_minimize_over_krylov_space(self):
        rng = random.Random(21)
        a = int_matrix(rng, 7, 4)
        y = [Fraction(rng.randint(-5, 5)) for _ in range(7)]
        ap, atp = exact_ops(a)
        res = cgls(ap, atp, y, 4)
        for k in range(1, 5):
            self.assertEqual(res.iterates[k], krylov_solution(a, y, k))

    def test_page_example(self):
        # A = diag(1, 1/2, ..., 1/32), x^dagger = ones, noise +-1/20, tau = 3/2.
        d = [Fraction(1, 2 ** j) for j in range(6)]
        e = [Fraction(1, 20) * s for s in (1, -1, 1, -1, 1, -1)]
        y = [a + b for a, b in zip(d, e)]

        def op(x):
            return [a * b for a, b in zip(d, x)]

        res = cgls(op, op, y, 6)
        errs = [math.sqrt(sum((float(v) - 1.0) ** 2 for v in x)) for x in res.iterates]
        self.assertEqual(min(range(7), key=lambda k: errs[k]), 4)
        self.assertAlmostEqual(errs[4], 1.1217, places=4)
        self.assertEqual(res.iterates[6], [b / a for a, b in zip(d, y)])
        self.assertEqual(res.res2[6], 0)
        delta2 = sum(t * t for t in e)
        stop = cgls(op, op, y, 6, delta=math.sqrt(delta2), tau=1.5)
        self.assertEqual((stop.k, stop.stopped), (3, "discrepancy"))
        first = next(k for k, r2 in enumerate(res.res2) if r2 <= Fraction(9, 4) * delta2)
        self.assertEqual(first, 3)

    def test_finite_termination(self):
        rng = random.Random(22)
        a = int_matrix(rng, 6, 4)
        y = [Fraction(rng.randint(-5, 5)) for _ in range(6)]
        ap, atp = exact_ops(a)
        res = cgls(ap, atp, y, 10)
        self.assertEqual(res.stopped, "breakdown")
        self.assertLessEqual(res.k, 4)
        ata = matmul(transpose(a), a)
        self.assertEqual(res.x, solve(ata, atp(y)))

    def test_rank_deficient_gives_minimum_norm_solution(self):
        rng = random.Random(23)
        b = int_matrix(rng, 6, 2)
        c = int_matrix(rng, 2, 5)
        a = matmul(b, c)
        y = [Fraction(rng.randint(-5, 5)) for _ in range(6)]
        ap, atp = exact_ops(a)
        res = cgls(ap, atp, y, 10)
        self.assertEqual(res.stopped, "breakdown")
        self.assertEqual(res.k, 2)
        self.assertTrue(all(t == 0 for t in atp([p - q for p, q in zip(y, ap(res.x))])))
        u, s, v = svd([[float(t) for t in row] for row in a])
        ref = [0.0] * 5
        for i in range(2):
            coef = sum(u[r][i] * float(y[r]) for r in range(6)) / s[i]
            ref = [rj + coef * v[j][i] for j, rj in enumerate(ref)]
        for p, q in zip(res.x, ref):
            self.assertAlmostEqual(float(p), q, places=9)

    def test_monotone_quantities(self):
        rng = random.Random(24)
        a = int_matrix(rng, 8, 5)
        y = [Fraction(rng.randint(-5, 5)) for _ in range(8)]
        ap, atp = exact_ops(a)
        res = cgls(ap, atp, y, 5)
        xls = res.x if res.stopped == "breakdown" else solve(matmul(transpose(a), a), atp(y))
        xn = [sum(t * t for t in x) for x in res.iterates]
        en = [sum((p - q) ** 2 for p, q in zip(x, xls)) for x in res.iterates]
        for j in range(len(res.iterates) - 1):
            self.assertLessEqual(res.res2[j + 1], res.res2[j])
            self.assertGreaterEqual(xn[j + 1], xn[j])
            self.assertLessEqual(en[j + 1], en[j])

    def test_ritz_filter_factors(self):
        rng = random.Random(25)
        a = [[rng.uniform(-1.0, 1.0) for _ in range(5)] for _ in range(9)]
        y = [rng.gauss(0.0, 1.0) for _ in range(9)]
        u, s, v = svd(a)
        ata = matmul(transpose(a), a)
        for k in (1, 2, 3):
            x = cgls_matrix(a, y, k).x
            # Orthonormal basis of K_k(A^T A, A^T y) by Gram-Schmidt, twice.
            q, w = [], [sum(a[r][j] * y[r] for r in range(9)) for j in range(5)]
            for _ in range(k):
                for _ in range(2):
                    for b in q:
                        h = sum(p * t for p, t in zip(b, w))
                        w = [p - h * t for p, t in zip(w, b)]
                nw = norm2(w)
                q.append([p / nw for p in w])
                w = matvec(ata, q[-1])
            t = [[sum(qi[r] * sum(ata[r][c] * qj[c] for c in range(5)) for r in range(5))
                  for qj in q] for qi in q]
            ritz, _ = sym_eig(t)
            ref = [0.0] * 5
            for i, si in enumerate(s):
                coef = ritz_filter_factor(si, ritz) * sum(u[r][i] * y[r] for r in range(9)) / si
                ref = [rj + coef * v[j][i] for j, rj in enumerate(ref)]
            for p, r in zip(x, ref):
                self.assertAlmostEqual(p, r, places=8)

    def test_discrepancy_stop(self):
        rng = random.Random(26)
        a = [[rng.uniform(-1.0, 1.0) for _ in range(6)] for _ in range(12)]
        xt = [rng.gauss(0.0, 1.0) for _ in range(6)]
        e = [rng.gauss(0.0, 1.0) for _ in range(12)]
        delta, tau = 0.3, 1.1
        ne = norm2(e)
        y = [p + delta * q / ne for p, q in zip(matvec(a, xt), e)]
        res = cgls_matrix(a, y, 50, delta=delta, tau=tau)
        self.assertEqual(res.stopped, "discrepancy")
        self.assertLessEqual(res.res2[-1], (tau * delta) ** 2)
        for r in res.res2[:-1]:
            self.assertGreater(r, (tau * delta) ** 2)

    def test_matrix_free_operator(self):
        n = 40
        h = 1.0 / n
        rng = random.Random(27)

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
        # Few steps: the two versions round differently, and late CG steps on an
        # ill-conditioned operator amplify rounding differences.
        free = cgls(op, opt, z, 4).x
        dense = cgls_matrix(a, z, 4).x
        gap = norm2([p - q for p, q in zip(free, dense)])
        self.assertLess(gap, 1e-8 * norm2(dense))

    def test_discrepancy_rule_on_integration_operator(self):
        # Diagonal model of (A x)(s) = int_0^s x; x^dagger = 1 - t, so nu = 1/2.
        n = 200
        sig = [2.0 / ((2 * k - 1) * math.pi) for k in range(1, n + 1)]
        xd = [math.sqrt(2.0) * t * t for t in sig]
        y = [t * x for t, x in zip(sig, xd)]

        def op(x):
            return [t * v for t, v in zip(sig, x)]

        rng = random.Random(3)
        e = [rng.gauss(0.0, 1.0) for _ in range(n)]
        ne = norm2(e)
        errs, deltas = [], [1e-2, 1e-5]
        for delta in deltas:
            yd = [p + delta * q / ne for p, q in zip(y, e)]
            res = cgls(op, op, yd, 60)
            all_errs = [norm2([p - q for p, q in zip(x, xd)]) for x in res.iterates]
            k = next(j for j, r in enumerate(res.res2) if r <= (1.5 * delta) ** 2)
            self.assertLessEqual(all_errs[k], 2.0 * min(all_errs))
            errs.append(all_errs[k])
        slope = math.log(errs[0] / errs[1]) / math.log(deltas[0] / deltas[1])
        self.assertLess(abs(slope - 0.5), 0.15)


if __name__ == "__main__":
    unittest.main()
