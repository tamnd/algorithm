# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precomputed-atmospheric-scattering/. The authors are listed in prov/22XP7T.jsonl.

"""A toy of precomputed atmospheric scattering: a transmittance table and single scattering.

This is a toy, not the full method. It precomputes the transmittance table
T(r, mu) of a spherical planet with an exponential Rayleigh and Mie
atmosphere, and uses it to compute the single scattered light along one view
ray by quadrature. The full method also stores single scattering in a 4D
table over (r, mu, mu_s, nu), adds multiple scattering orders and ground
irradiance, and reads the tables in a shader; this file does none of that.

Units: lengths in km, scattering coefficients in 1/km, the sun irradiance is
1 in each of the three channels (red 680 nm, green 550 nm, blue 440 nm), so
the result is radiance per unit sun irradiance, in 1/sr. The Rayleigh values
and scale heights are those of Bruneton and Neyret (2008); the Mie values and
the planet radii are tuning constants of this toy.

Geometry: r is the distance to the planet center, mu the cosine of the view
zenith angle, mu_s that of the sun zenith angle, nu the cosine of the angle
between the view and the sun. A point at distance s along the view ray has
r_s = sqrt(r^2 + s^2 + 2 r mu s), mu_s' = (r mu + s) / r_s and
mu_s_s = (r mu_s + s nu) / r_s.
"""

import math

Vec3 = tuple[float, float, float]

RG = 6360.0                        # ground radius, km (tuning of the toy)
RT = 6420.0                        # top of the atmosphere, km (tuning of the toy)
H_R = 8.0                          # Rayleigh scale height, km
H_M = 1.2                          # Mie scale height, km
BETA_R = (5.8e-3, 13.5e-3, 33.1e-3)  # Rayleigh scattering at sea level, 1/km
BETA_M_SCA = 4.0e-3                # Mie scattering at sea level, 1/km (tuning)
BETA_M_EXT = BETA_M_SCA / 0.9      # Mie extinction, 1/km (tuning: albedo 0.9)
G_MIE = 0.8                        # Mie asymmetry (tuning)


def phase_rayleigh(nu: float) -> float:
    """Rayleigh phase function, normalized over the sphere: 3 / (16 pi) (1 + nu^2)."""
    return 3.0 / (16.0 * math.pi) * (1.0 + nu * nu)


def phase_mie(nu: float, g: float = G_MIE) -> float:
    """Cornette-Shanks phase function, normalized over the sphere."""
    k = 3.0 / (8.0 * math.pi) * (1.0 - g * g) / (2.0 + g * g)
    return k * (1.0 + nu * nu) / (1.0 + g * g - 2.0 * g * nu) ** 1.5


def extinction(r: float) -> Vec3:
    """Extinction coefficient at radius r, per channel, in 1/km."""
    h = max(r - RG, 0.0)
    rm = BETA_M_EXT * math.exp(-h / H_M)
    rr = math.exp(-h / H_R)
    return (BETA_R[0] * rr + rm, BETA_R[1] * rr + rm, BETA_R[2] * rr + rm)


def mu_horizon(r: float) -> float:
    """The cosine of the view zenith angle of the horizon seen from radius r."""
    return -math.sqrt(max(0.0, 1.0 - (RG / r) ** 2))


def hits_ground(r: float, mu: float) -> bool:
    return mu < mu_horizon(r)


def dist_to_top(r: float, mu: float) -> float:
    return max(0.0, -r * mu + math.sqrt(max(0.0, r * r * (mu * mu - 1.0) + RT * RT)))


def dist_to_ground(r: float, mu: float) -> float:
    return max(0.0, -r * mu - math.sqrt(max(0.0, r * r * (mu * mu - 1.0) + RG * RG)))


def point_on_ray(r: float, mu: float, s: float) -> tuple[float, float]:
    """Radius and view zenith cosine at distance s along the ray (r, mu)."""
    rs = math.sqrt(max(r * r + s * s + 2.0 * r * mu * s, RG * RG))
    return rs, max(-1.0, min(1.0, (r * mu + s) / rs))


def optical_depth(r: float, mu: float, d: float, q: int = 200) -> Vec3:
    """Integral of the extinction over the first d km of the ray, trapezoidal rule with q steps."""
    if d <= 0.0:
        return (0.0, 0.0, 0.0)
    ds = d / q
    acc = [0.0, 0.0, 0.0]
    for k in range(q + 1):
        w = 0.5 if k in (0, q) else 1.0
        e = extinction(point_on_ray(r, mu, k * ds)[0])
        for c in range(3):
            acc[c] += w * e[c]
    return (acc[0] * ds, acc[1] * ds, acc[2] * ds)


def transmittance_to_top(r: float, mu: float, q: int = 200) -> Vec3:
    """Direct quadrature of the transmittance from (r, mu) to the top, for a ray that misses the ground."""
    tau = optical_depth(r, mu, dist_to_top(r, mu), q)
    return (math.exp(-tau[0]), math.exp(-tau[1]), math.exp(-tau[2]))


H_TOP = math.sqrt(RT * RT - RG * RG)  # distance from the ground to the top along the horizon


def table_coords(r: float, mu: float) -> tuple[float, float]:
    """The unit coordinates (x_r, x_mu) of a ray (r, mu) that misses the ground.

    x_r = rho / H with rho = sqrt(r^2 - RG^2), and x_mu places the distance d
    to the top between its least value RT - r (straight up) and its largest
    value rho + H (along the horizon). This is the mapping of Bruneton's 2017
    code; it puts more entries near the horizon, where T changes fast.
    """
    rho = math.sqrt(max(0.0, r * r - RG * RG))
    d = dist_to_top(r, mu)
    d_min, d_max = RT - r, rho + H_TOP
    x_mu = (d - d_min) / (d_max - d_min) if d_max > d_min else 0.0
    return rho / H_TOP, min(max(x_mu, 0.0), 1.0)


def ray_of_coords(x_r: float, x_mu: float) -> tuple[float, float]:
    """The inverse of table_coords."""
    rho = H_TOP * x_r
    r = math.sqrt(rho * rho + RG * RG)
    d_min, d_max = RT - r, rho + H_TOP
    d = d_min + x_mu * (d_max - d_min)
    mu = 1.0 if d == 0.0 else (H_TOP * H_TOP - rho * rho - d * d) / (2.0 * r * d)
    return r, max(-1.0, min(1.0, mu))


class TransmittanceTable:
    """T(r, mu) to the top of the atmosphere on a regular grid in (x_r, x_mu)."""

    def __init__(self, nr: int = 32, nu: int = 64, q: int = 200) -> None:
        if nr < 2 or nu < 2:
            raise ValueError("the table needs at least 2 entries per axis")
        self.nr, self.nu = nr, nu
        self.data = []
        for i in range(nr):
            row = []
            for j in range(nu):
                r, mu = ray_of_coords(i / (nr - 1), j / (nu - 1))
                row.append(transmittance_to_top(r, mu, q))  # @line L1
            self.data.append(row)

    def lookup(self, r: float, mu: float) -> Vec3:
        """Bilinear lookup of T(r, mu) for a ray that does not hit the ground."""
        r = min(max(r, RG), RT)
        x_r, x_mu = table_coords(r, mu)
        x = x_r * (self.nr - 1)
        y = x_mu * (self.nu - 1)
        i, j = min(int(x), self.nr - 2), min(int(y), self.nu - 2)
        fx, fy = x - i, y - j
        d = self.data
        return tuple(
            (1 - fx) * ((1 - fy) * d[i][j][c] + fy * d[i][j + 1][c])
            + fx * ((1 - fy) * d[i + 1][j][c] + fy * d[i + 1][j + 1][c])
            for c in range(3))

    def between(self, r: float, mu: float, s: float, ground: bool) -> Vec3:
        """Transmittance from (r, mu) to the point at distance s, from two table lookups."""
        rs, mus = point_on_ray(r, mu, s)
        if ground:
            num, den = self.lookup(rs, -mus), self.lookup(r, -mu)
        else:
            num, den = self.lookup(r, mu), self.lookup(rs, mus)
        return tuple(min(1.0, num[c] / den[c]) for c in range(3))


def single_scattering(table: TransmittanceTable, r: float, mu: float, mu_s: float,
                      nu: float, q: int = 100, g: float = G_MIE) -> Vec3:
    """Single scattered radiance along the view ray (r, mu) for the sun at (mu_s, nu)."""
    ground = hits_ground(r, mu)
    d = dist_to_ground(r, mu) if ground else dist_to_top(r, mu)  # @line L2
    pr, pm = phase_rayleigh(nu), phase_mie(nu, g)
    acc = [0.0, 0.0, 0.0]  # @line L3
    for k in range(q + 1):  # @line L4
        s = k * d / q
        w = 0.5 if k in (0, q) else 1.0
        ry, _ = point_on_ray(r, mu, s)  # @line L5
        mu_sy = max(-1.0, min(1.0, (r * mu_s + s * nu) / ry))
        t_view = table.between(r, mu, s, ground)  # @line L6
        if hits_ground(ry, mu_sy):  # @line L7
            continue
        t_sun = table.lookup(ry, mu_sy)
        h = ry - RG
        br, bm = math.exp(-h / H_R), BETA_M_SCA * math.exp(-h / H_M)
        for c in range(3):
            acc[c] += w * t_view[c] * t_sun[c] * (BETA_R[c] * br * pr + bm * pm)  # @line L8
    ds = d / q
    return (acc[0] * ds, acc[1] * ds, acc[2] * ds)  # @line L9


def single_scattering_direct(r: float, mu: float, mu_s: float, nu: float,
                             q: int = 100, q_inner: int = 200, g: float = G_MIE) -> Vec3:
    """The same integral with every transmittance by direct quadrature, for the tests."""
    ground = hits_ground(r, mu)
    d = dist_to_ground(r, mu) if ground else dist_to_top(r, mu)
    pr, pm = phase_rayleigh(nu), phase_mie(nu, g)
    acc = [0.0, 0.0, 0.0]
    for k in range(q + 1):
        s = k * d / q
        w = 0.5 if k in (0, q) else 1.0
        ry, _ = point_on_ray(r, mu, s)
        mu_sy = max(-1.0, min(1.0, (r * mu_s + s * nu) / ry))
        if hits_ground(ry, mu_sy):
            continue
        tau = optical_depth(r, mu, s, q_inner)
        t_sun = transmittance_to_top(ry, mu_sy, q_inner)
        h = ry - RG
        br, bm = math.exp(-h / H_R), BETA_M_SCA * math.exp(-h / H_M)
        for c in range(3):
            acc[c] += w * math.exp(-tau[c]) * t_sun[c] * (BETA_R[c] * br * pr + bm * pm)
    ds = d / q
    return (acc[0] * ds, acc[1] * ds, acc[2] * ds)
