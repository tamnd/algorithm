# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backus-gilbert-method/. The authors are listed in prov/GT011W.jsonl.
import math
import random
import unittest

from backus_gilbert_method import (areas, averaging_kernel, backus_gilbert, noise_variance,
                                   spread, spread_matrix, weights)
from imgla import solve


def setup(m=10, width=0.08, n=400):
    ts = [(i + 0.5) / n for i in range(n)]
    ws = [1.0 / n] * n
    g = [[math.exp(-0.5 * ((t - (i + 0.5) / m) / width) ** 2) / (width * math.sqrt(2.0 * math.pi))
          for t in ts] for i in range(m)]
    cov = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    return ts, ws, g, cov


def objective(a, s, cov, mu):
    m = len(a)
    return sum(a[i] * (s[i][j] + mu * cov[i][j]) * a[j] for i in range(m) for j in range(m))


class TestBackusGilbert(unittest.TestCase):
    def test_box_spread(self):
        n = 2000
        ts = [(i + 0.5) / n for i in range(n)]
        ws = [1.0 / n] * n
        for wdt in (0.1, 0.3):
            box = [1.0 / wdt if abs(t - 0.5) < wdt / 2 else 0.0 for t in ts]
            self.assertAlmostEqual(spread(box, ts, ws, 0.5), wdt, places=5)

    def test_unit_area_and_kkt(self):
        ts, ws, g, cov = setup()
        c = areas(g, ws)
        for p, mu in ((0.5, 1e-3), (0.27, 0.1)):
            a = weights(g, ts, ws, p, mu, cov)
            self.assertAlmostEqual(sum(x * y for x, y in zip(a, c)), 1.0, places=12)
            # Brute force: the KKT system [[2 W, c], [c^T, 0]] [a; l] = [0; 1].
            s = spread_matrix(g, ts, ws, p)
            m = len(c)
            kkt = [[2.0 * (s[i][j] + mu * cov[i][j]) for j in range(m)] + [c[i]] for i in range(m)]
            kkt.append(list(c) + [0.0])
            ref = solve(kkt, [0.0] * m + [1.0])[:m]
            for x, y in zip(a, ref):
                self.assertAlmostEqual(x, y, places=6)

    def test_optimal_among_feasible_weights(self):
        ts, ws, g, cov = setup()
        c = areas(g, ws)
        p, mu = 0.6, 0.01
        a = weights(g, ts, ws, p, mu, cov)
        s = spread_matrix(g, ts, ws, p)
        best = objective(a, s, cov, mu)
        rng = random.Random(71)
        cc = sum(x * x for x in c)
        for _ in range(30):
            v = [rng.gauss(0.0, 1.0) for _ in c]
            proj = sum(x * y for x, y in zip(v, c)) / cc
            d = [x - proj * y for x, y in zip(v, c)]
            b = [x + 0.01 * y for x, y in zip(a, d)]
            self.assertGreaterEqual(objective(b, s, cov, mu), best)

    def test_spread_matrix_matches_kernel_spread(self):
        ts, ws, g, cov = setup()
        a = weights(g, ts, ws, 0.4, 0.05, cov)
        s = spread_matrix(g, ts, ws, 0.4)
        direct = spread(averaging_kernel(g, a), ts, ws, 0.4)
        self.assertAlmostEqual(objective(a, s, cov, 0.0), direct, places=10)

    def test_trade_off_is_monotone(self):
        ts, ws, g, cov = setup()
        for p in (0.5, 0.33):
            prev_s, prev_v = -1.0, math.inf
            for mu in (1e-6, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0):
                a = weights(g, ts, ws, p, mu, cov)
                sp = spread(averaging_kernel(g, a), ts, ws, p)
                nv = noise_variance(a, cov)
                self.assertGreaterEqual(sp, prev_s - 1e-12)
                self.assertLessEqual(nv, prev_v + 1e-12)
                prev_s, prev_v = sp, nv

    def test_constants_are_reproduced(self):
        ts, ws, g, cov = setup()
        data = [3.0 * ci for ci in areas(g, ws)]
        est = backus_gilbert(g, ts, ws, data, [0.2, 0.5, 0.9], 0.01, cov)
        for v in est:
            self.assertAlmostEqual(v, 3.0, places=10)

    def test_estimate_is_local_average(self):
        ts, ws, g, cov = setup()
        # A function that varies slowly on the scale of the spread (about 0.12).
        x = [math.sin(math.pi * t) + 0.5 * t for t in ts]
        data = [sum(w * gi * xi for w, gi, xi in zip(ws, gk, x)) for gk in g]
        for p in (0.3, 0.5, 0.7):
            a = weights(g, ts, ws, p, 1e-4, cov)
            k = averaging_kernel(g, a)
            avg = sum(w * ki * xi for w, ki, xi in zip(ws, k, x))
            est = backus_gilbert(g, ts, ws, data, [p], 1e-4, cov)[0]
            self.assertAlmostEqual(est, avg, places=10)
            self.assertLess(abs(est - (math.sin(math.pi * p) + 0.5 * p)), 0.08)


if __name__ == "__main__":
    unittest.main()
