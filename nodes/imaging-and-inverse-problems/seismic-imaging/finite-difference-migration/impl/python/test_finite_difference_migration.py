# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-difference-migration/. The authors are listed in prov/BK5R80.jsonl.
import math
import random
import unittest

from finite_difference_migration import (
    apply_t,
    diffraction_step,
    finite_difference_migration,
    kz_15_degree,
    kz_crank_nicolson,
    thomas_solve,
)

NT, NX, DT, DX = 64, 32, 0.004, 10.0
VEL = 3000.0
DZ = VEL * DT / 2.0


def ricker(t, f0):
    a = (math.pi * f0 * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def diffractor(x0, z0):
    out = [[0.0] * NX for _ in range(NT)]
    for j in range(NX):
        t0 = 2.0 * math.hypot(z0, j * DX - x0) / VEL
        for k in range(NT):
            out[k][j] = ricker(k * DT - t0, 25.0)
    return out


def norm(p):
    return math.sqrt(sum(abs(v) ** 2 for v in p))


class TestFiniteDifferenceMigration(unittest.TestCase):
    def test_thomas_solve(self):
        rng = random.Random(11)
        n = 9
        lower = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        upper = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        diag = [complex(5.0 + rng.random(), rng.uniform(-1, 1)) for _ in range(n)]
        rhs = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        x = thomas_solve(lower, diag, upper, rhs)
        for j in range(n):
            s = diag[j] * x[j]
            if j > 0:
                s += lower[j] * x[j - 1]
            if j < n - 1:
                s += upper[j] * x[j + 1]
            self.assertLess(abs(s - rhs[j]), 1e-12)

    def test_step_keeps_the_norm(self):
        # For a constant b the step is a Cayley transform of a real symmetric
        # matrix, so it is unitary.
        rng = random.Random(5)
        p = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(20)]
        q = diffraction_step(p, [0.7] * 20)
        self.assertAlmostEqual(norm(q), norm(p), delta=1e-12)

    def test_step_solves_the_scheme(self):
        rng = random.Random(6)
        p = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(12)]
        b = [rng.uniform(0.1, 2.0) for _ in range(12)]
        q = diffraction_step(p, b)
        tp, tq = apply_t(p), apply_t(q)
        for j in range(12):
            self.assertLess(abs((q[j] - 0.5j * b[j] * tq[j]) - (p[j] + 0.5j * b[j] * tp[j])), 1e-12)

    def test_point_diffractor_focuses(self):
        img = finite_difference_migration(diffractor(160.0, 192.0), DT, DX, DZ, [[VEL] * NX for _ in range(48)])
        best = max((img[i][j], i, j) for i in range(48) for j in range(NX))
        self.assertLessEqual(abs(best[1] - 32), 1)
        self.assertEqual(best[2], 16)

    def test_flat_event_is_a_time_to_depth_map(self):
        # For kx = 0 the scheme is the exact phase shift: a flat event at
        # t0 = 0.2 s goes to z = v' t0 = 300 m, row 50. The Dirichlet ends
        # disturb the columns near the edges, so check the middle ones.
        data = [[ricker(k * DT - 0.2, 25.0)] * NX for k in range(NT)]
        img = finite_difference_migration(data, DT, DX, DZ, [[VEL] * NX for _ in range(60)])
        for j in range(12, 20):
            self.assertEqual(max(range(60), key=lambda i: img[i][j]), 50)

    def test_dispersion(self):
        w, vh = 2.0 * math.pi * 25.0, 1500.0
        self.assertAlmostEqual(kz_crank_nicolson(w, 0.0, vh, DX, DZ), w / vh, places=12)
        self.assertAlmostEqual(kz_15_degree(w, 0.0, vh), w / vh, places=12)
        # The 15 degree relation is the second-order Taylor polynomial of the
        # exact one, and the discrete one tends to it for small steps.
        kx = 0.1 * w / vh
        exact = math.sqrt((w / vh) ** 2 - kx * kx)
        self.assertLess(abs(kz_15_degree(w, kx, vh) - exact), 1e-4 * exact)
        self.assertLess(abs(kz_crank_nicolson(w, kx, vh, 0.1, 0.1) - kz_15_degree(w, kx, vh)), 1e-4 * exact)
        # The error grows with the angle.
        kx2 = 0.7 * w / vh
        exact2 = math.sqrt((w / vh) ** 2 - kx2 * kx2)
        self.assertGreater(abs(kz_15_degree(w, kx2, vh) - exact2), 0.05 * exact2)


if __name__ == "__main__":
    unittest.main()
