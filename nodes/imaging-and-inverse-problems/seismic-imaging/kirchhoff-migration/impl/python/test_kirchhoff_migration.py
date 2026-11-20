# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kirchhoff-migration/. The authors are listed in prov/ZFVWK9.jsonl.
import cmath
import math
import random
import unittest

from imgkit import dft2, idft
from kirchhoff_migration import (
    diffraction_stack,
    half_derivative,
    kirchhoff_migration,
    kirchhoff_modeling,
    kirchhoff_weight,
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


def signed(k, n):
    return k if 2 * k < n else k - n


def phase_shift_oracle(data, dt, dx, dz, nz, vel):
    """Constant velocity phase-shift migration, an independent reference."""
    nt, nx = len(data), len(data[0])
    p = dft2(data)
    vh = vel / 2.0
    img = []
    for _ in range(nz):
        row = [sum(p[k][j] for k in range(nt)) / nt for j in range(nx)]
        img.append([v.real for v in idft(row)])
        for k in range(nt):
            w = 2.0 * math.pi * signed(k, nt) / (nt * dt)
            for j in range(nx):
                kx = 2.0 * math.pi * signed(j, nx) / (nx * dx)
                a = (w / vh) ** 2 - kx * kx
                if w == 0.0 or a <= 0.0:
                    p[k][j] = 0j
                else:
                    p[k][j] *= cmath.exp(1j * math.copysign(math.sqrt(a), w) * dz)
    return img


def argmax2(img):
    return max((img[i][j], i, j) for i in range(len(img)) for j in range(len(img[0])))[1:]


class TestKirchhoffMigration(unittest.TestCase):
    def test_point_diffractor_focuses(self):
        img = kirchhoff_migration(diffractor(160.0, 192.0), DT, DX, DZ, 48, VEL)
        i, j = argmax2(img)
        self.assertLessEqual(abs(i - 32), 1)
        self.assertEqual(j, 16)

    def test_agrees_with_phase_shift(self):
        data = diffractor(160.0, 192.0)
        a = kirchhoff_migration(data, DT, DX, DZ, 48, VEL)
        b = phase_shift_oracle(data, DT, DX, DZ, 48, VEL)
        rows = range(4, 48)  # the formula is a high frequency approximation; skip z near 0
        num = sum((a[i][j] - b[i][j]) ** 2 for i in rows for j in range(NX))
        den = sum(b[i][j] ** 2 for i in rows for j in range(NX))
        self.assertLess(math.sqrt(num / den), 0.15)

    def test_stack_and_modeling_are_adjoint(self):
        rng = random.Random(7)
        nt, nx, nz = 40, 12, 10
        d = [[rng.gauss(0.0, 1.0) for _ in range(nx)] for _ in range(nt)]
        m = [[rng.gauss(0.0, 1.0) for _ in range(nx)] for _ in range(nz)]
        lt_d = diffraction_stack(d, DT, DX, DZ, nz, VEL)
        l_m = kirchhoff_modeling(m, DT, nt, DX, DZ, VEL)
        left = sum(l_m[k][j] * d[k][j] for k in range(nt) for j in range(nx))
        right = sum(m[i][j] * lt_d[i][j] for i in range(nz) for j in range(nx))
        self.assertLess(abs(left - right), 1e-12 * max(abs(left), 1.0))

    def test_half_derivative_twice_is_minus_derivative(self):
        # (-i omega)^(1/2) applied twice is -i omega, the symbol of -d/dt here.
        n, dt = 64, 0.004
        f = 5.0 / (n * dt)
        trace = [math.sin(2.0 * math.pi * f * k * dt) for k in range(n)]
        twice = half_derivative(half_derivative(trace, dt), dt)
        for k in range(n):
            self.assertAlmostEqual(twice[k], -2.0 * math.pi * f * math.cos(2.0 * math.pi * f * k * dt), delta=1e-9)

    def test_weight_and_traveltime(self):
        w, t = kirchhoff_weight(0.0, 300.0, 400.0, 2000.0)
        self.assertAlmostEqual(t, 0.5, places=12)  # r = 500 m, t = 2 r / v
        self.assertAlmostEqual(w, 0.6 / math.sqrt(2.0 * math.pi * 1000.0 * 500.0), places=15)


if __name__ == "__main__":
    unittest.main()
