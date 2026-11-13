# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/color-spaces/. The authors are listed in prov/PBFC5X.jsonl.

import math
import random
from fractions import Fraction as F

from color_spaces import (
    D65,
    EPS,
    KAPPA,
    SRGB_PRIMARIES,
    SRGB_TO_XYZ,
    hsv_to_rgb,
    inverse3,
    lab_to_xyz,
    mat_vec,
    rgb_to_hsv,
    rgb_to_xyz_matrix,
    rgb_to_ycbcr,
    xyz_to_lab,
    ycbcr_to_rgb,
)

# IEC 61966-2-1 Amendment 1 (2003), the inverse matrix to 7 decimals
XYZ_TO_SRGB_2003 = [
    [F("3.2406255"), F("-1.5372080"), F("-0.4986286")],
    [F("-0.9689307"), F("1.8757561"), F("0.0415175")],
    [F("0.0557101"), F("-0.2040211"), F("1.0569959")],
]
# IEC 61966-2-1 (1999), the inverse matrix to 4 decimals
XYZ_TO_SRGB_1999 = [
    [3.2406, -1.5372, -0.4986],
    [-0.9689, 1.8758, 0.0415],
    [0.0557, -0.2040, 1.0570],
]
WHITE = [sum(row) for row in SRGB_TO_XYZ]


def rounded(m, digits):
    return [[round(v, digits) for v in row] for row in m]


def test_matrix_from_primaries_matches_standard() -> None:
    m = rgb_to_xyz_matrix(SRGB_PRIMARIES, D65)
    assert rounded(m, 4) == SRGB_TO_XYZ
    assert sum(m[1]) == 1
    assert mat_vec(m, [1, 1, 1]) == [D65[0] / D65[1], 1, (1 - D65[0] - D65[1]) / D65[1]]


def test_inverse_matches_published_values() -> None:
    inv = inverse3(SRGB_TO_XYZ)
    assert rounded(inv, 7) == XYZ_TO_SRGB_2003
    assert [[round(float(v), 4) for v in row] for row in inv] == XYZ_TO_SRGB_1999
    ident = [[sum(SRGB_TO_XYZ[i][k] * inv[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    assert ident == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def test_exact_rgb_xyz_round_trip() -> None:
    rng = random.Random(11)
    inv = inverse3(SRGB_TO_XYZ)
    for _ in range(500):
        rgb = [F(rng.randint(0, 255), 255) for _ in range(3)]
        assert mat_vec(inv, mat_vec(SRGB_TO_XYZ, rgb)) == rgb


def test_lab_constants_join_exactly() -> None:
    assert EPS == F(6, 29) ** 3 and KAPPA == F(29, 3) ** 3
    assert (KAPPA * EPS + 16) / 116 == F(6, 29)
    assert KAPPA / 116 == F(1, 3) * F(29, 6) ** 2


def test_lab_reference_values() -> None:
    def lab_of(rgb):
        return [round(float(v), 4) for v in xyz_to_lab(mat_vec(SRGB_TO_XYZ, rgb), WHITE)]

    assert lab_of([1, 1, 1]) == [100.0, 0.0, 0.0]
    assert lab_of([1, 0, 0]) == [53.2329, 80.1053, 67.2228]
    assert lab_of([0, 1, 0]) == [87.737, -86.1884, 83.1861]
    assert lab_of([0, 0, 1]) == [32.3026, 79.1936, -107.8537]
    assert round(float(xyz_to_lab([0, F(18, 100), 0], WHITE)[0]), 4) == 49.4961


def test_lab_round_trips() -> None:
    rng = random.Random(12)
    for _ in range(500):
        # exact on the linear segment, near black
        xyz = [w * F(rng.randint(0, 2000), 250000) for w in WHITE]
        lab = xyz_to_lab(xyz, WHITE)
        assert all(isinstance(v, F) for v in lab)
        assert lab_to_xyz(lab, WHITE) == xyz
        # close on the cube-root segment
        xyz = [float(w) * rng.uniform(0.01, 1) for w in WHITE]
        back = lab_to_xyz(xyz_to_lab(xyz, [float(w) for w in WHITE]), [float(w) for w in WHITE])
        assert all(math.isclose(a, b, rel_tol=1e-12) for a, b in zip(xyz, back))


def test_ycbcr() -> None:
    assert rgb_to_ycbcr(0, 0, 0) == (0, 128, 128)
    assert rgb_to_ycbcr(255, 255, 255) == (255, 128, 128)
    # the Cb and Cr weights, rounded to 6 digits as in JFIF (ITU-T T.871)
    cb_r = (rgb_to_ycbcr(1, 0, 0)[1] - 128)
    cb_g = (rgb_to_ycbcr(0, 1, 0)[1] - 128)
    cr_g = (rgb_to_ycbcr(0, 1, 0)[2] - 128)
    cr_b = (rgb_to_ycbcr(0, 0, 1)[2] - 128)
    assert [round(float(v), 6) for v in (cb_r, cb_g, cr_g, cr_b)] == [-0.168736, -0.331264, -0.418688, -0.081312]
    rng = random.Random(13)
    for _ in range(500):
        rgb = tuple(F(rng.randint(0, 255)) for _ in range(3))
        assert ycbcr_to_rgb(*rgb_to_ycbcr(*rgb)) == rgb


def test_hsv() -> None:
    assert rgb_to_hsv(1, 0, 0) == (0, 1, 1)
    assert rgb_to_hsv(0, 1, 0) == (2, 1, 1)
    assert rgb_to_hsv(F(1, 2), F(1, 2), F(1, 2)) == (0, 0, F(1, 2))
    rng = random.Random(14)
    for _ in range(1000):
        rgb = tuple(F(rng.randint(0, 255), 255) for _ in range(3))
        h, s, v = rgb_to_hsv(*rgb)
        assert 0 <= h < 6 and 0 <= s <= 1 and v == max(rgb)
        assert hsv_to_rgb(h, s, v) == rgb
