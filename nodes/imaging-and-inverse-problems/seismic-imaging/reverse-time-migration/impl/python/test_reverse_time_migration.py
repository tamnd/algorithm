# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-time-migration/. The authors are listed in prov/Y8PCJ8.jsonl.
import random
import unittest

from reverse_time_migration import (
    background_field,
    born_modeling,
    laplacian,
    reverse_time_migration,
    ricker,
    zeros,
)

H, DT, V = 10.0, 0.002, 2000.0  # v dt / h = 0.4 < 1 / sqrt(2)


def setup(n, nsteps):
    m = [[1.0 / V ** 2] * n for _ in range(n)]
    wav = [ricker(k * DT - 0.06, 20.0) for k in range(nsteps)]
    _, d2 = background_field(m, 2, n // 2, wav, DT, H)
    recs = [(2, j) for j in range(n)]
    return m, d2, recs


class TestReverseTimeMigration(unittest.TestCase):
    def test_image_peaks_at_the_scatterer(self):
        n, nsteps = 32, 180
        m, d2, recs = setup(n, nsteps)
        dm = zeros(n, n)
        dm[18][12] = 0.2 / V ** 2
        data = born_modeling(dm, m, d2, recs, DT, H)
        img = reverse_time_migration(data, m, d2, recs, DT, H)
        # Rows near the source and receivers hold strong direct-wave artifacts; skip them.
        best = max((abs(img[i][j]), i, j) for i in range(5, n) for j in range(n))
        self.assertEqual(best[1:], (18, 12))
        self.assertGreater(img[18][12], 0.0)

    def test_adjoint_of_born_modeling(self):
        n, nsteps = 14, 50
        m, d2, recs = setup(n, nsteps)
        rng = random.Random(3)
        dm = [[rng.gauss(0.0, 1.0) / V ** 2 for _ in range(n)] for _ in range(n)]
        r = [[rng.gauss(0.0, 1.0) for _ in recs] for _ in range(nsteps + 1)]
        a = born_modeling(dm, m, d2, recs, DT, H)
        b = reverse_time_migration(r, m, d2, recs, DT, H)
        left = sum(a[k][q] * r[k][q] for k in range(nsteps + 1) for q in range(len(recs)))
        right = sum(dm[i][j] * b[i][j] for i in range(n) for j in range(n))
        self.assertLess(abs(left - right), 1e-10 * abs(left))

    def test_zero_data_gives_zero_image(self):
        n, nsteps = 8, 10
        m, d2, recs = setup(n, nsteps)
        img = reverse_time_migration([[0.0] * n for _ in range(nsteps + 1)], m, d2, recs, DT, H)
        self.assertEqual(max(abs(v) for row in img for v in row), 0.0)

    def test_laplacian_of_a_quadratic(self):
        # The 5-point Laplacian of x^2 + z^2 is 4 away from the edges.
        n = 6
        u = [[(i * H) ** 2 + (j * H) ** 2 for j in range(n)] for i in range(n)]
        lap = laplacian(u, H)
        for i in range(1, n - 1):
            for j in range(1, n - 1):
                self.assertAlmostEqual(lap[i][j], 4.0, places=9)


if __name__ == "__main__":
    unittest.main()
