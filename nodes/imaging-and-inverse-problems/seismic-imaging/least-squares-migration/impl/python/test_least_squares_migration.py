# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-migration/. The authors are listed in prov/H0YJBB.jsonl.
import math
import random
import unittest

from least_squares_migration import born_kirchhoff_operator, damped, least_squares_migration, matvec, rmatvec

NT, DT, NXG, DX, NZ, DZ, ZTOP, VEL, F0 = 40, 0.004, 10, 10.0, 8, 10.0, 40.0, 2000.0, 30.0
N = NXG * NZ


def operator():
    rows = born_kirchhoff_operator(NT, DT, NXG, DX, NZ, DZ, ZTOP, VEL, F0)
    return rows, (lambda x: matvec(rows, x)), (lambda y: rmatvec(rows, y, N))


def true_model():
    m = [0.0] * N
    m[2 * NXG + 3] = 1.0
    m[5 * NXG + 6] = -0.5
    for j in range(NXG):
        m[6 * NXG + j] += 0.3
    return m


def solve_dense(a, b):
    """Gaussian elimination with partial pivoting, an independent reference."""
    n = len(b)
    a = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            if f != 0.0:
                for k in range(c, n + 1):
                    a[r][k] -= f * a[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (a[r][n] - sum(a[r][k] * x[k] for k in range(r + 1, n))) / a[r][r]
    return x


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


class TestLeastSquaresMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, lop, ltop = operator()
        cls.lop, cls.ltop = staticmethod(lop), staticmethod(ltop)
        cls.m_true = true_model()
        cls.d = cls.lop(cls.m_true)

    def test_adjoint(self):
        rng = random.Random(1)
        x = [rng.gauss(0, 1) for _ in range(N)]
        y = [rng.gauss(0, 1) for _ in range(NT * NXG)]
        left = sum(a * b for a, b in zip(self.lop(x), y))
        right = sum(a * b for a, b in zip(x, self.ltop(y)))
        self.assertLess(abs(left - right), 1e-12 * abs(left))

    def test_residual_does_not_increase(self):
        _, norms = least_squares_migration(self.lop, self.ltop, self.d, N, 25)
        for a, b in zip(norms, norms[1:]):
            self.assertLessEqual(b, a * (1.0 + 1e-12))
        self.assertLess(norms[-1], 0.05 * norms[0])

    def test_damped_matches_direct_solve(self):
        cols = [[0.0] * NT * NXG for _ in range(N)]
        for k, row in enumerate(self.rows):
            for c, w in row:
                cols[c][k] += w
        ata = [[sum(a * b for a, b in zip(cols[i], cols[j])) for j in range(N)] for i in range(N)]
        eps = 0.1 * max(ata[i][i] for i in range(N))
        for i in range(N):
            ata[i][i] += eps
        ref = solve_dense(ata, self.ltop(self.d))
        lop, ltop, dd = damped(self.lop, self.ltop, self.d, N, eps)
        m, _ = least_squares_migration(lop, ltop, dd, N, 60)
        self.assertLess(dist(m, ref), 1e-6 * math.sqrt(sum(v * v for v in ref)))

    def test_better_than_scaled_migration(self):
        mig = self.ltop(self.d)
        lmig = self.lop(mig)
        alpha = sum(a * b for a, b in zip(lmig, self.d)) / sum(a * a for a in lmig)
        scaled = [alpha * v for v in mig]
        m, _ = least_squares_migration(self.lop, self.ltop, self.d, N, 25)
        ref = math.sqrt(sum(v * v for v in self.m_true))
        self.assertLess(dist(m, self.m_true) / ref, 0.8 * dist(scaled, self.m_true) / ref)


if __name__ == "__main__":
    unittest.main()
