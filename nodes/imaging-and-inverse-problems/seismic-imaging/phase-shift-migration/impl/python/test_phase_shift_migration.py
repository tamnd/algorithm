# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-shift-migration/. The authors are listed in prov/PNBG5B.jsonl.
import math
import unittest

from imgkit import dft, idft
from phase_shift_migration import (
    diffractor_section,
    phase_shift_migration,
    ricker,
    signed_freq,
    vertical_wavenumber,
)

NT, NX, DT, DX = 64, 32, 0.004, 10.0
VEL = 3000.0


def half_filter(data, dt):
    """Multiply the time spectrum of every trace by (i omega)^(1/2), zero at omega = 0."""
    nt, nx = len(data), len(data[0])
    cols = []
    for j in range(nx):
        spec = dft([data[k][j] for k in range(nt)])
        out = []
        for k in range(nt):
            w = signed_freq(k, nt, dt)
            out.append(spec[k] * (1j * w) ** 0.5 if w != 0.0 else 0j)
        cols.append([v.real for v in idft(out)])
    return [[cols[j][k] for j in range(nx)] for k in range(nt)]


def argmax2(img):
    return max((img[i][j], i, j) for i in range(len(img)) for j in range(len(img[0])))[1:]


class TestPhaseShiftMigration(unittest.TestCase):
    def test_flat_event_in_two_layers(self):
        # Reflector at 250 m under 100 m of 2000 m/s and 3000 m/s below:
        # two-way time 2 (100/2000 + 150/3000) = 0.2 s, sample 50.
        nx = 8
        data = [[ricker(k * DT - 0.2, 25.0)] * nx for k in range(NT)]
        vz = [2000.0] * 10 + [3000.0] * 30
        img = phase_shift_migration(data, DT, DX, 10.0, vz)
        for j in range(nx):
            col = [img[i][j] for i in range(len(vz))]
            self.assertEqual(max(range(len(vz)), key=lambda i: col[i]), 25)
            self.assertAlmostEqual(col[25], 1.0, delta=1e-6)

    def test_point_diffractor_focuses(self):
        # Diffractor at x0 = 160 m (column 16), z0 = 192 m; dz = v dt / 2 = 6 m,
        # so the focus is row 32. The half-derivative prefilter makes the
        # migrated pulse zero phase, so the maximum is exactly there.
        dz = VEL * DT / 2.0
        data = half_filter(diffractor_section(NT, NX, DT, DX, 160.0, 192.0, VEL, 25.0), DT)
        img = phase_shift_migration(data, DT, DX, dz, [VEL] * 48)
        self.assertEqual(argmax2(img), (32, 16))

    def test_raw_diffractor_within_one_sample(self):
        dz = VEL * DT / 2.0
        data = diffractor_section(NT, NX, DT, DX, 160.0, 192.0, VEL, 25.0)
        img = phase_shift_migration(data, DT, DX, dz, [VEL] * 48)
        i, j = argmax2(img)
        self.assertLessEqual(abs(i - 32), 1)
        self.assertEqual(j, 16)

    def test_energy_is_focused(self):
        # Away from the focus the image is small compared with the peak.
        dz = VEL * DT / 2.0
        data = half_filter(diffractor_section(NT, NX, DT, DX, 160.0, 192.0, VEL, 25.0), DT)
        img = phase_shift_migration(data, DT, DX, dz, [VEL] * 48)
        peak = img[32][16]
        far = max(abs(img[i][j]) for i in range(48) for j in range(NX) if abs(i - 32) > 6 or abs(j - 16) > 6)
        self.assertLess(far, 0.25 * peak)

    def test_vertical_wavenumber(self):
        w = 2.0 * math.pi * 20.0
        v = 1500.0
        self.assertAlmostEqual(vertical_wavenumber(w, 0.0, v), w / v, places=12)
        self.assertAlmostEqual(vertical_wavenumber(-w, 0.0, v), -w / v, places=12)
        self.assertIsNone(vertical_wavenumber(w, 1.01 * w / v, v))
        self.assertIsNone(vertical_wavenumber(0.0, 0.0, v))
        kx = 0.6 * w / v
        self.assertAlmostEqual(vertical_wavenumber(w, kx, v), 0.8 * w / v, places=12)

    def test_signed_frequencies(self):
        self.assertEqual([round(signed_freq(k, 8, 1.0) * 8 / (2 * math.pi)) for k in range(8)],
                         [0, 1, 2, 3, -4, -3, -2, -1])


if __name__ == "__main__":
    unittest.main()
