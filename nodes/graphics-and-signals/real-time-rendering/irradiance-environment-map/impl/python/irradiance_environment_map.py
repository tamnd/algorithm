# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irradiance-environment-map/. The authors are listed in prov/H7PF86.jsonl.

"""The irradiance environment map of Ramamoorthi and Hanrahan (2001).

The environment is a list of texels (direction, radiance, solid angle) of one
color channel, for distant lighting. The algorithm projects the radiance onto
the nine real spherical harmonics of order l <= 2, puts the coefficients into
a symmetric 4 by 4 matrix M (Equation 12 of the paper), and evaluates the
irradiance at a unit normal n as E(n) = (n, 1)^T M (n, 1) (Equation 11).
For an RGB map, run it once for each channel.

Precondition: the directions are unit vectors and the solid angles add up to
4 pi (any quadrature rule on the sphere). Cost: Theta(9 S) for S texels to
build M, and Theta(1) for each evaluation.

The basis order in a coefficient list is (0,0), (1,-1), (1,0), (1,1), (2,-2),
(2,-1), (2,0), (2,1), (2,2). The convention is the one of the paper:
z is the polar axis, x = sin theta cos phi and y = sin theta sin phi.
"""

import math

# Normalization constants of the real spherical harmonics (Equation 3).
Y0 = 0.5 / math.sqrt(math.pi)                    # 0.282095
Y1 = math.sqrt(3.0 / (4.0 * math.pi))            # 0.488603
Y2 = 0.5 * math.sqrt(15.0 / math.pi)             # 1.092548
Y20 = 0.25 * math.sqrt(5.0 / math.pi)            # 0.315392
Y22 = 0.25 * math.sqrt(15.0 / math.pi)           # 0.546274

# The clamped cosine kernel in each band (Equations 8 and 9).
A_HAT = (math.pi, 2.0 * math.pi / 3.0, math.pi / 4.0)
BAND = (0, 1, 1, 1, 2, 2, 2, 2, 2)

# The constants of Equation 12, from the two lists above.
C1 = A_HAT[2] * Y22                              # 0.429043
C2 = A_HAT[1] * Y1 / 2.0                         # 0.511664
C3 = A_HAT[2] * Y20 * 3.0                        # 0.743125
C4 = A_HAT[0] * Y0                               # 0.886227
C5 = A_HAT[2] * Y20                              # 0.247708

Vec = tuple[float, float, float]
Texel = tuple[Vec, float, float]


def sh9(d: Vec) -> list[float]:
    """The nine real spherical harmonics at the unit vector d."""
    x, y, z = d
    return [
        Y0,
        Y1 * y,
        Y1 * z,
        Y1 * x,
        Y2 * x * y,
        Y2 * y * z,
        Y20 * (3.0 * z * z - 1.0),
        Y2 * x * z,
        Y22 * (x * x - y * y),
    ]


def project(texels: list[Texel]) -> list[float]:
    """Equation 10: L_lm = sum of L(w) Y_lm(w) dw over the texels."""
    coeffs = [0.0] * 9  # @line L1
    for d, radiance, domega in texels:  # @line L2
        y = sh9(d)
        for k in range(9):  # @line L3
            coeffs[k] += radiance * y[k] * domega
    return coeffs


def irradiance_matrix(coeffs: list[float]) -> list[list[float]]:
    """Equation 12: the symmetric 4 by 4 matrix M from the nine L_lm."""
    l00, l1m1, l10, l11, l2m2, l2m1, l20, l21, l22 = coeffs
    return [  # @line L4
        [C1 * l22, C1 * l2m2, C1 * l21, C2 * l11],
        [C1 * l2m2, -C1 * l22, C1 * l2m1, C2 * l1m1],
        [C1 * l21, C1 * l2m1, C3 * l20, C2 * l10],
        [C2 * l11, C2 * l1m1, C2 * l10, C4 * l00 - C5 * l20],
    ]


def build(texels: list[Texel]) -> list[list[float]]:
    """IRRADIANCE-MAP: lines L1 to L5."""
    m = irradiance_matrix(project(texels))
    return m  # @line L5


def irradiance(m: list[list[float]], n: Vec) -> float:
    """Equation 11: E(n) = (n, 1)^T M (n, 1) for a unit normal n."""
    h = (n[0], n[1], n[2], 1.0)  # @line L6
    return sum(h[i] * m[i][j] * h[j] for i in range(4) for j in range(4))  # @line L7


def irradiance_sh(coeffs: list[float], n: Vec) -> float:
    """Equation 7: E(n) = sum of A_hat_l L_lm Y_lm(n), the same value as line L7."""
    y = sh9(n)
    return sum(A_HAT[BAND[k]] * coeffs[k] * y[k] for k in range(9))


def irradiance_brute_force(texels: list[Texel], n: Vec) -> float:
    """The reference: E(n) = sum of L(w) max(0, n . w) dw over all texels."""
    total = 0.0
    for d, radiance, domega in texels:
        c = n[0] * d[0] + n[1] * d[1] + n[2] * d[2]
        if c > 0.0:
            total += radiance * c * domega
    return total


def point_light_coeffs(d: Vec, power: float) -> list[float]:
    """The exact coefficients of a delta light of the given power in direction d."""
    return [power * y for y in sh9(d)]


def gauss_legendre(n: int) -> list[tuple[float, float]]:
    """Nodes and weights of the n point Gauss-Legendre rule on [-1, 1], by Newton's method."""
    out = []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1.0)
        out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    return out


def sphere_texels(radiance, n_z: int, n_phi: int) -> list[Texel]:
    """Sample a radiance function on the sphere as texels.

    The rule is Gauss-Legendre in z on [-1, 0] and on [0, 1] separately, and
    uniform in phi. It integrates exactly a polynomial in (x, y, z) of degree
    below min(2 n_z, n_phi) on each hemisphere, so a lighting with a jump at
    the horizon still projects exactly when it is a polynomial on each half.
    """
    texels = []
    rule = gauss_legendre(n_z)
    for lo in (-1.0, 0.0):
        for t, w in rule:
            z = lo + 0.5 * (t + 1.0)
            s = math.sqrt(max(0.0, 1.0 - z * z))
            for j in range(n_phi):
                phi = 2.0 * math.pi * (j + 0.5) / n_phi
                d = (s * math.cos(phi), s * math.sin(phi), z)
                texels.append((d, radiance(d), 0.5 * w * 2.0 * math.pi / n_phi))
    return texels
