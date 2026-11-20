# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-back-projection/. The authors are listed in prov/4TK0K9.jsonl.
"""Universal back-projection for photoacoustic tomography in 3D (Xu and Wang 2005).

The initial pressure p0 starts a wave p(r, t) with speed c and zero initial
velocity. Point detectors on a closed surface record p(r0, t). The formula

    p0(r) = (1 / Omega0) * sum over detectors of b(r0, |r - r0| / c) dOmega0,
    b(r0, t) = 2 p(r0, t) - 2 t dp/dt(r0, t),

with the solid angle dOmega0 of each detector element seen from r, is exact for
a sphere, a cylinder and a plane in 3D (Xu and Wang 2005; Finch, Patch and
Rakesh 2004 for the sphere). This file uses a sphere of detectors.

Units in the tests: lengths in mm, times in microseconds, c = 1.54 mm/us.
"""

import math


def gauss_legendre(n):
    """Nodes and weights of the n point Gauss-Legendre rule on [-1, 1]."""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        dp = 1.0
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        xs.append(x)
        ws.append(2.0 / ((1.0 - x * x) * dp * dp))
    return xs, ws


def sphere_detectors(radius, n_theta, n_phi):
    """Detector elements on a sphere about the origin.

    Returns a list of (position, inward unit normal, area). The areas are the
    weights of the Gauss-Legendre rule in cos(theta) times the uniform rule in phi,
    so they integrate smooth functions on the sphere with spectral accuracy.
    """
    us, ws = gauss_legendre(n_theta)
    dets = []
    for u, w in zip(us, ws):
        st = math.sqrt(1.0 - u * u)
        for k in range(n_phi):
            ph = 2.0 * math.pi * k / n_phi
            n_out = (st * math.cos(ph), st * math.sin(ph), u)
            pos = tuple(radius * a for a in n_out)
            inward = tuple(-a for a in n_out)
            dets.append((pos, inward, w * (2.0 * math.pi / n_phi) * radius * radius))
    return dets


def solid_angle_element(r, det):
    """dOmega0 = dS0 * (n0 . (r - r0)) / |r - r0|^3 with the normal n0 toward r."""
    pos, normal, area = det
    d = [r[i] - pos[i] for i in range(3)]
    dist = math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
    return area * (normal[0] * d[0] + normal[1] * d[1] + normal[2] * d[2]) / dist ** 3, dist


def back_projection_term(p, dt):
    """b(t_k) = 2 p(t_k) - 2 t_k dp/dt(t_k) for samples p[k] at t_k = k dt.

    The time derivative is a central difference inside and a one sided one at the ends.
    """
    n = len(p)
    b = [0.0] * n
    for k in range(n):
        if 0 < k < n - 1:
            dpdt = (p[k + 1] - p[k - 1]) / (2.0 * dt)
        elif k == 0:
            dpdt = (p[1] - p[0]) / dt
        else:
            dpdt = (p[k] - p[k - 1]) / dt
        b[k] = 2.0 * p[k] - 2.0 * (k * dt) * dpdt  # @line L2
    return b


def sample(b, dt, t):
    """Linear interpolation of the samples b[k] at t_k = k dt; zero outside the record."""
    x = t / dt
    k = int(math.floor(x))
    if k < 0 or k >= len(b) - 1:
        return 0.0
    f = x - k
    return (1.0 - f) * b[k] + f * b[k + 1]


def universal_back_projection(data, dets, dt, c, points, omega0=None):
    """Reconstruct p0 at the given points from sampled data[d][k] = p(r0_d, k dt).

    omega0 is the solid angle of the whole surface seen from the point (4 pi for a
    closed surface); None uses the sum of the solid angle elements instead.
    """
    bs = [back_projection_term(p, dt) for p in data]  # @line L1
    out = []
    for r in points:  # @line L3
        total, omega = 0.0, 0.0
        for det, b in zip(dets, bs):  # @line L4
            d_omega, dist = solid_angle_element(r, det)  # @line L5
            total += d_omega * sample(b, dt, dist / c)  # @line L6
            omega += d_omega  # @line L7
        out.append(total / (omega if omega0 is None else omega0))  # @line L8
    return out  # @line L9


def universal_back_projection_exact_b(b_func, dets, c, points, omega0=4.0 * math.pi):
    """The same sum with b(r0, t) given as a function, without time sampling."""
    out = []
    for r in points:
        total = 0.0
        for det in dets:
            d_omega, dist = solid_angle_element(r, det)
            total += d_omega * b_func(det[0], dist / c)
        out.append(total / omega0)
    return out


# A Gaussian ball p0(x) = exp(-|x - centre|^2 / (2 s^2)) has a closed form wave.

def ball_initial_pressure(x, centre, s):
    d = math.dist(x, centre)
    return math.exp(-d * d / (2.0 * s * s))


def ball_pressure(x, t, centre, s, c):
    """p(x, t) = ((d - ct) g(d - ct) + (d + ct) g(d + ct)) / (2 d) with g(u) = exp(-u^2 / (2 s^2))."""
    d = math.dist(x, centre)
    a, b = d - c * t, d + c * t
    return (a * math.exp(-a * a / (2.0 * s * s)) + b * math.exp(-b * b / (2.0 * s * s))) / (2.0 * d)


def ball_pressure_dt(x, t, centre, s, c):
    """The exact time derivative of ball_pressure."""
    d = math.dist(x, centre)
    a, b = d - c * t, d + c * t

    def h(u):
        return (1.0 - u * u / (s * s)) * math.exp(-u * u / (2.0 * s * s))

    return c * (h(b) - h(a)) / (2.0 * d)


def ball_data(dets, centre, s, c, dt, nt, window=7.0):
    """Sampled pressure p(r0, k dt) for k < nt at every detector, zero where |d - ct| > window s."""
    data = []
    for pos, _, _ in dets:
        d = math.dist(pos, centre)
        row = [0.0] * nt
        k_lo = max(0, int((d - window * s) / (c * dt)))
        k_hi = min(nt, int((d + window * s) / (c * dt)) + 2)
        for k in range(k_lo, k_hi):
            row[k] = ball_pressure(pos, k * dt, centre, s, c)
        data.append(row)
    return data
