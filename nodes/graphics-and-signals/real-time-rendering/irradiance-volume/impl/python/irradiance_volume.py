# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irradiance-volume/. The authors are listed in prov/CE3Y53.jsonl.

"""An irradiance volume: a regular 3D grid of probes that store irradiance.

Each probe holds the nine spherical harmonic coefficients E_lm of the
irradiance at its position (the coefficients are already convolved with the
clamped cosine, so E(n) = sum of E_lm Y_lm(n)). A query at a point p and a
unit normal n blends the coefficients of the 8 probes of the cell around p
with trilinear weights and evaluates the blend at n. Points outside the grid
are clamped to its boundary. Visibility is ignored, which is why light can
leak through thin walls.

Precondition: at least 2 probes along each axis, spacing > 0. Cost: O(1) per
query (8 probes of 9 coefficients) and Theta(X Y Z) memory for X Y Z probes.
"""

import math

Vec = tuple[float, float, float]

Y0 = 0.5 / math.sqrt(math.pi)
Y1 = math.sqrt(3.0 / (4.0 * math.pi))
Y2 = 0.5 * math.sqrt(15.0 / math.pi)
Y20 = 0.25 * math.sqrt(5.0 / math.pi)
Y22 = 0.25 * math.sqrt(15.0 / math.pi)
A_HAT = (math.pi, 2.0 * math.pi / 3.0, math.pi / 4.0)
BAND = (0, 1, 1, 1, 2, 2, 2, 2, 2)


def sh9(d: Vec) -> list[float]:
    """The nine real spherical harmonics at d, z as the polar axis."""
    x, y, z = d
    return [Y0, Y1 * y, Y1 * z, Y1 * x, Y2 * x * y, Y2 * y * z,
            Y20 * (3.0 * z * z - 1.0), Y2 * x * z, Y22 * (x * x - y * y)]


def irradiance_coeffs(radiance_coeffs: list[float]) -> list[float]:
    """Convolve nine radiance coefficients L_lm with the clamped cosine: E_lm = A_hat_l L_lm."""
    return [A_HAT[BAND[k]] * radiance_coeffs[k] for k in range(9)]


def eval_sh(coeffs: list[float], n: Vec) -> float:
    """The function with these nine coefficients, at the direction n."""
    return sum(c * y for c, y in zip(coeffs, sh9(n)))


class IrradianceVolume:
    """A grid of dims[0] by dims[1] by dims[2] probes at origin + spacing * (i, j, k)."""

    def __init__(self, origin: Vec = (0.0, 0.0, 0.0), spacing: float = 1.0,
                 dims: tuple[int, int, int] = (2, 2, 2)) -> None:
        if min(dims) < 2 or spacing <= 0.0:
            raise ValueError("need at least 2 probes per axis and a positive spacing")
        self.origin = origin
        self.spacing = spacing
        self.dims = dims
        nx, ny, nz = dims
        self.probes = [[[[0.0] * 9 for _ in range(nz)] for _ in range(ny)] for _ in range(nx)]

    def probe_position(self, i: int, j: int, k: int) -> Vec:
        o, h = self.origin, self.spacing
        return (o[0] + h * i, o[1] + h * j, o[2] + h * k)

    def set_probe(self, i: int, j: int, k: int, coeffs: list[float]) -> None:
        """Store nine irradiance coefficients at probe (i, j, k)."""
        if len(coeffs) != 9:
            raise ValueError("a probe holds nine coefficients")
        self.probes[i][j][k] = [float(c) for c in coeffs]

    def probe(self, i: int, j: int, k: int) -> list[float]:
        return list(self.probes[i][j][k])

    def bake(self, coeffs_at) -> None:
        """Fill every probe with coeffs_at(position), for example a projection of the radiance there."""
        nx, ny, nz = self.dims
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    self.set_probe(i, j, k, coeffs_at(self.probe_position(i, j, k)))

    def cell_and_weights(self, p: Vec) -> tuple[tuple[int, int, int], Vec]:
        """The lowest corner of the cell of p and the fractions inside it, after clamping."""
        base, frac = [], []
        for a in range(3):
            g = (p[a] - self.origin[a]) / self.spacing  # @line L1
            g = min(max(g, 0.0), self.dims[a] - 1.0)
            i = min(int(math.floor(g)), self.dims[a] - 2)  # @line L2
            base.append(i)
            frac.append(g - i)
        return (base[0], base[1], base[2]), (frac[0], frac[1], frac[2])

    def sample_coeffs(self, p: Vec) -> list[float]:
        """The trilinear blend of the nine coefficients of the 8 probes around p."""
        (i, j, k), (fx, fy, fz) = self.cell_and_weights(p)
        out = [0.0] * 9  # @line L3
        for a in (0, 1):  # @line L4
            wa = fx if a else 1.0 - fx
            for b in (0, 1):
                wb = fy if b else 1.0 - fy
                for c in (0, 1):
                    w = wa * wb * (fz if c else 1.0 - fz)  # @line L5
                    pr = self.probes[i + a][j + b][k + c]
                    for m in range(9):
                        out[m] += w * pr[m]  # @line L6
        return out

    def sample(self, p: Vec, n: Vec) -> float:
        """SAMPLE: the irradiance at the point p for the unit normal n."""
        return eval_sh(self.sample_coeffs(p), n)  # @line L7

    def check_invariant(self) -> None:
        nx, ny, nz = self.dims
        assert len(self.probes) == nx
        for plane in self.probes:
            assert len(plane) == ny
            for row in plane:
                assert len(row) == nz
                assert all(len(c) == 9 for c in row)
