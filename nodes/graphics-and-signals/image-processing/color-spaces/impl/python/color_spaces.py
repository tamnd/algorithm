# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/color-spaces/. The authors are listed in prov/PBFC5X.jsonl.

"""Conversions between common color spaces.

- RGB to XYZ: the 3 by 3 matrix built from the primaries and the white point,
  and the sRGB matrix of IEC 61966-2-1 with its 4-digit entries.
- XYZ to CIELAB and back, with the exact constants (6/29)^3 and 24389/27.
- Full-range YCbCr with the BT.601 luma weights, as in JPEG (JFIF).
- HSV, the hexcone model of Alvy Ray Smith (1978).

The RGB values here are linear for XYZ and Lab, and the usual encoded
values for YCbCr and HSV. All maps except the cube root of Lab are
rational, so with Fraction inputs they round trip exactly.
"""

from fractions import Fraction as F

SRGB_TO_XYZ = [
    [F("0.4124"), F("0.3576"), F("0.1805")],
    [F("0.2126"), F("0.7152"), F("0.0722")],
    [F("0.0193"), F("0.1192"), F("0.9505")],
]
SRGB_PRIMARIES = [(F("0.64"), F("0.33")), (F("0.30"), F("0.60")), (F("0.15"), F("0.06"))]
D65 = (F("0.3127"), F("0.3290"))

EPS = F(216, 24389)  # (6/29)^3
KAPPA = F(24389, 27)  # (29/3)^3


def mat_vec(m: list[list], v: list) -> list:
    return [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]


def inverse3(m: list[list]) -> list[list]:
    """Inverse of a 3 by 3 matrix by the adjugate. Exact for Fraction entries."""
    (a, b, c), (d, e, f), (g, h, i) = m
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    if det == 0:
        raise ValueError("the matrix is singular")
    adj = [
        [e * i - f * h, c * h - b * i, b * f - c * e],
        [f * g - d * i, a * i - c * g, c * d - a * f],
        [d * h - e * g, b * g - a * h, a * e - b * d],
    ]
    return [[v / det for v in row] for row in adj]


def xy_to_xyz(x, y) -> list:
    """Chromaticity (x, y) to XYZ with Y = 1."""
    return [x / y, 1, (1 - x - y) / y]


def rgb_to_xyz_matrix(primaries, white) -> list[list]:
    """The matrix M with M (1, 1, 1) = white and with columns along the primaries."""
    cols = [xy_to_xyz(x, y) for x, y in primaries]
    p = [[cols[j][i] for j in range(3)] for i in range(3)]
    scale = mat_vec(inverse3(p), xy_to_xyz(*white))
    return [[p[i][j] * scale[j] for j in range(3)] for i in range(3)]


def _f(t):
    return t ** (1 / 3) if t > EPS else (KAPPA * t + 16) / 116


def _f_inv(u):
    return u**3 if u > F(6, 29) else (116 * u - 16) / KAPPA


def xyz_to_lab(xyz: list, white: list) -> tuple:
    fx, fy, fz = (_f(v / w) for v, w in zip(xyz, white))
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def lab_to_xyz(lab: tuple, white: list) -> list:
    big_l, a, b = lab
    fy = (big_l + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    return [_f_inv(u) * w for u, w in zip((fx, fy, fz), white)]


KR, KB = F(299, 1000), F(114, 1000)
KG = 1 - KR - KB


def rgb_to_ycbcr(r, g, b) -> tuple:
    """Full-range YCbCr for 8-bit values, without rounding."""
    y = KR * r + KG * g + KB * b
    return y, 128 + (b - y) / (2 * (1 - KB)), 128 + (r - y) / (2 * (1 - KR))


def ycbcr_to_rgb(y, cb, cr) -> tuple:
    r = y + 2 * (1 - KR) * (cr - 128)
    b = y + 2 * (1 - KB) * (cb - 128)
    return r, (y - KR * r - KB * b) / KG, b


def rgb_to_hsv(r, g, b) -> tuple:
    """Smith's hexcone. r, g, b in [0, 1]; h in [0, 6) in sectors of 60 degrees."""
    v = max(r, g, b)
    d = v - min(r, g, b)
    s = 0 if v == 0 else d / v
    if d == 0:
        return 0, s, v
    if v == r:
        h = (g - b) / d % 6
    elif v == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h, s, v


def hsv_to_rgb(h, s, v) -> tuple:
    def channel(n):
        k = (n + h) % 6
        return v - v * s * max(0, min(k, 4 - k, 1))

    return channel(5), channel(3), channel(1)
