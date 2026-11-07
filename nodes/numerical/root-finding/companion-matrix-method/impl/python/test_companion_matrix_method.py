# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/companion-matrix-method/. The authors are listed in prov/4VFJZ5.jsonl.

import cmath
import math
import random
import unittest

from companion_matrix_method import balance, companion, companion_roots, hessenberg_eigenvalues


def from_roots(rs):
    p = [1 + 0j]
    for r in rs:
        p = [x - r * y for x, y in zip(p + [0], [0] + p)]
    return p


def match_error(found, expected):
    left = list(found)
    err = 0.0
    for r in expected:
        j = min(range(len(left)), key=lambda i: abs(left[i] - r))
        err = max(err, abs(left[j] - r))
        left.pop(j)
    return err


def char_poly_at(C, z):
    """det(zI - C) by Gaussian elimination, for checking the companion matrix."""
    n = len(C)
    M = [[(z if i == j else 0) - C[i][j] for j in range(n)] for i in range(n)]
    det = 1 + 0j
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            return 0j
        if p != c:
            M[c], M[p] = M[p], M[c]
            det = -det
        det *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for j in range(c, n):
                M[r][j] -= f * M[c][j]
    return det


class TestCompanion(unittest.TestCase):
    def test_characteristic_polynomial(self):
        a = [2, -3, 5, 7, -11]
        C = companion(a)
        for z in (0.5, -1.25, 2 + 1j):
            p = sum(c * z ** (len(a) - 1 - i) for i, c in enumerate(a)) / a[0]
            self.assertAlmostEqual(abs(char_poly_at(C, z) - p), 0, delta=1e-12)

    def test_balancing_is_a_similarity(self):
        a = [complex(x) for x in from_roots(range(1, 9))]
        C = companion(a)
        B = [row[:] for row in C]
        balance(B)
        for z in (0.5, 3.3, 7 + 2j):
            self.assertLess(abs(char_poly_at(B, z) - char_poly_at(C, z)), 1e-6 * (1 + abs(char_poly_at(C, z))))

    def test_small_examples(self):
        r = companion_roots([1, -6, 11, -6])
        self.assertEqual(r.status, "converged")
        self.assertLess(match_error(r.roots, [1, 2, 3]), 1e-14)
        r = companion_roots([1, 0, 3, 6, 10])
        self.assertLess(match_error(r.roots, [-1 + 1j, -1 - 1j, 1 + 2j, 1 - 2j]), 1e-14)

    def test_roots_of_unity(self):
        r = companion_roots([1] + [0] * 29 + [-1])
        self.assertLess(match_error(r.roots, [cmath.exp(2j * math.pi * k / 30) for k in range(30)]), 1e-13)

    def test_wilkinson_balancing_matters(self):
        w = [x.real for x in from_roots(range(1, 21))]
        bal = companion_roots(w)
        raw = companion_roots(w, balanced=False)
        self.assertEqual(bal.status, "converged")
        self.assertLess(match_error(bal.roots, range(1, 21)), 0.1)
        self.assertGreater(match_error(raw.roots, range(1, 21)), 1.0)
        w10 = [x.real for x in from_roots(range(1, 11))]
        self.assertLess(match_error(companion_roots(w10).roots, range(1, 11)), 1e-8)

    def test_multiple_roots_lose_accuracy_like_eps_to_1_over_m(self):
        for m, bound in ((2, 1e-7), (3, 1e-4), (4, 1e-3)):
            r = companion_roots([x.real for x in from_roots([1] * m + [-2])])
            self.assertLess(match_error(r.roots, [1] * m + [-2]), bound)

    def test_zero_roots_and_low_degree(self):
        self.assertEqual(companion_roots([3, 0, 0]).roots, [0j, 0j])
        r = companion_roots([1, -3, 2, 0])  # x (x - 1)(x - 2)
        self.assertLess(match_error(r.roots, [0, 1, 2]), 1e-14)
        self.assertEqual(companion_roots([2, -4]).roots, [2 + 0j])
        self.assertEqual(companion_roots([0, 0, 1, -5]).roots, [5 + 0j])  # leading zeros stripped

    def test_bad_input_and_cap(self):
        for bad in ([1, float("nan")], [1, math.inf], [0, 0], []):
            with self.assertRaises(ValueError):
                companion_roots(bad)
        r = companion_roots([1, 0, 3, 6, 10], max_iter=0)
        self.assertEqual(r.status, "failed")

    def test_hessenberg_eigenvalues_triangular(self):
        H = [[1 + 0j, 5, 7], [0j, 2, 4], [0j, 0j, 3]]
        eig, sweeps, status = hessenberg_eigenvalues(H)
        self.assertEqual((sorted(e.real for e in eig), sweeps, status), ([1, 2, 3], 0, "converged"))

    def test_random_polynomials(self):
        rng = random.Random(20261108)
        sweeps = 0
        for _ in range(500):
            n = rng.randint(2, 12)
            rs = []
            while len(rs) < n:
                if n - len(rs) >= 2 and rng.random() < 0.5:
                    z = complex(rng.uniform(-3, 3), rng.uniform(0.3, 3))
                    cand = [z, z.conjugate()]
                else:
                    cand = [complex(rng.uniform(-3, 3))]
                if all(abs(u - v) > 0.3 for u in cand for v in rs):
                    rs += cand
            r = companion_roots([x.real for x in from_roots(rs)])
            self.assertEqual(r.status, "converged")
            self.assertEqual(len(r.roots), n)
            self.assertLess(match_error(r.roots, rs), 1e-9)
            sweeps += r.sweeps / n
        self.assertLess(sweeps / 500, 5)


if __name__ == "__main__":
    unittest.main()
