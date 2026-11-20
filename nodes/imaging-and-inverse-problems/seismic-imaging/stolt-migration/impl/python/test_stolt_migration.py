# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stolt-migration/. The authors are listed in prov/HTV0W8.jsonl.
import cmath
import math
import unittest

from imgkit import dft2, idft
from stolt_migration import diffractor_section, ricker, signed_index, stolt_map, stolt_migration

NT, NX, DT, DX = 64, 32, 0.004, 10.0
VEL = 3000.0
DZ = VEL * DT / 2.0


def phase_shift_oracle(data, dt, dx, dz, nz, vel):
    """Constant velocity phase-shift migration, used as an independent reference."""
    nt, nx = len(data), len(data[0])
    p = dft2(data)
    vh = vel / 2.0
    img = []
    for _ in range(nz):
        row = [sum(p[k][j] for k in range(nt)) / nt for j in range(nx)]
        img.append([v.real for v in idft(row)])
        for k in range(nt):
            w = 2.0 * math.pi * signed_index(k, nt) / (nt * dt)
            for j in range(nx):
                kx = 2.0 * math.pi * signed_index(j, nx) / (nx * dx)
                a = (w / vh) ** 2 - kx * kx
                if w == 0.0 or a <= 0.0:
                    p[k][j] = 0j
                else:
                    p[k][j] *= cmath.exp(1j * math.copysign(math.sqrt(a), w) * dz)
    return img


def argmax2(img):
    return max((img[i][j], i, j) for i in range(len(img)) for j in range(len(img[0])))[1:]


class TestStoltMigration(unittest.TestCase):
    def test_flat_event_maps_time_to_depth(self):
        # A flat event at t0 = 0.2 s goes to z = v' t0 = 300 m, row 50.
        data = [[ricker(k * DT - 0.2, 25.0)] * 8 for k in range(NT)]
        img = stolt_migration(data, DT, DX, DZ, 64, VEL)
        for j in range(8):
            for i in range(64):
                self.assertAlmostEqual(img[i][j], ricker(i * DT - 0.2, 25.0), delta=1e-6)

    def test_point_diffractor_focuses(self):
        data = diffractor_section(NT, NX, DT, DX, 160.0, 192.0, VEL, 25.0)
        img = stolt_migration(data, DT, DX, DZ, 64, VEL)
        i, j = argmax2(img)
        self.assertLessEqual(abs(i - 32), 1)
        self.assertEqual(j, 16)

    def test_agrees_with_phase_shift(self):
        data = diffractor_section(NT, NX, DT, DX, 160.0, 192.0, VEL, 25.0)
        a = stolt_migration(data, DT, DX, DZ, 48, VEL)
        b = phase_shift_oracle(data, DT, DX, DZ, 48, VEL)
        num = sum((a[i][j] - b[i][j]) ** 2 for i in range(48) for j in range(NX))
        den = sum(b[i][j] ** 2 for i in range(48) for j in range(NX))
        self.assertLess(math.sqrt(num / den), 0.2)

    def test_stolt_map(self):
        vh = 1000.0
        w, jac = stolt_map(0.03, 0.04, vh)
        self.assertAlmostEqual(w, 50.0, places=9)
        self.assertAlmostEqual(jac, 0.6 * vh, places=9)
        w, jac = stolt_map(-0.03, 0.04, vh)
        self.assertAlmostEqual(w, -50.0, places=9)
        self.assertAlmostEqual(jac, 0.6 * vh, places=9)
        self.assertEqual(stolt_map(0.0, 0.0, vh), (0.0, 0.0))
        # At kx = 0 the map is the plain time-to-depth stretch omega = v' kz.
        w, jac = stolt_map(0.02, 0.0, vh)
        self.assertAlmostEqual(w, 20.0, places=9)
        self.assertAlmostEqual(jac, vh, places=9)

    def test_zero_data_gives_zero_image(self):
        img = stolt_migration([[0.0] * 4 for _ in range(16)], DT, DX, DZ, 8, VEL)
        self.assertEqual(max(abs(v) for row in img for v in row), 0.0)


if __name__ == "__main__":
    unittest.main()
