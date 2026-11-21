# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-bar-method/. The authors are listed in prov/Q00HZV.jsonl.
"""The D-bar method for the conductivity problem on the unit disk, with the
scattering transform t^exp of Siltanen, Mueller and Isaacson.

The data are the Dirichlet-to-Neumann map of a conductivity gamma that is 1
near the boundary. For a radial gamma this map is diagonal in the Fourier
basis e^{i n phi}, with eigenvalues lambda_n (lambda_n = n for gamma = 1).

1. The approximate scattering transform, for k in the complex plane,

       t^exp(k) = int e^{i conj(k) conj(z)} (Lambda_gamma - Lambda_1) e^{i k z} ds(z)
                = 2 pi sum_{n >= 1} (-1)^n |k|^(2n) (lambda_n - n) / (n!)^2     (radial gamma).

2. For each point z, solve the truncated D-bar equation in k,

       mu(z, k) = 1 + 1/(4 pi^2) int_{|k'| <= R} t(k') e_{-z}(k') conj(mu(z, k')) / ((k - k') conj(k')) dk',

   with e_z(k) = exp(i (k z + conj(k z))), on a grid of cell centers with
   spacing h, by fixed-point iteration. The singular cell k' = k is left
   out, which is the principal value of the integral over that cell.

3. gamma(z) = Re mu(z, 0)^2.

Complex numbers are Python complex values; z = x1 + i x2.
"""

import cmath
import math


def layered_dn_eigenvalues(rho, gamma_in, gamma_out, nmax):
    """lambda_1..lambda_nmax of the DN map on the unit disk for gamma = gamma_in on
    r < rho and gamma_out on rho < r < 1."""
    m = (gamma_out - gamma_in) / (gamma_out + gamma_in)
    out = []
    for n in range(1, nmax + 1):
        q = m * rho ** (2 * n)
        out.append(gamma_out * n * (1 - q) / (1 + q))
    return out


def radial_dn_eigenvalues(gamma, nmax, ds=0.005, s0=-8.0):
    """lambda_1..lambda_nmax of the DN map on the unit disk for a radial gamma(r).

    For u = U(r) e^{i n phi}, w = r gamma U'/U satisfies, in s = log r,
    dw/ds = n^2 gamma - w^2 / gamma, with w = n gamma(0) near r = 0, and
    lambda_n = w(r = 1). Classical Runge-Kutta from s = s0 to s = 0.
    """
    steps = int(round(-s0 / ds))
    out = []
    for n in range(1, nmax + 1):
        def f(s, w):
            g = gamma(math.exp(s))
            return n * n * g - w * w / g
        s, w = s0, n * gamma(math.exp(s0))
        for _ in range(steps):
            k1 = f(s, w)
            k2 = f(s + ds / 2, w + ds / 2 * k1)
            k3 = f(s + ds / 2, w + ds / 2 * k2)
            k4 = f(s + ds, w + ds * k3)
            w += ds / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            s += ds
        out.append(w)
    return out


def t_exp_radial(lams, k):
    """t^exp(k) for a radial conductivity with DN eigenvalues lams[n - 1] = lambda_n."""
    a = abs(k) ** 2
    total = 0.0
    term = 1.0  # |k|^(2n) / (n!)^2, built step by step
    for n, lam in enumerate(lams, start=1):
        term *= a / (n * n)
        total += (-1) ** n * term * (lam - n)
    return 2 * math.pi * total


def k_grid(R, h):
    """The cell centers h (i + i' j) with |k| <= R, with k = 0 first."""
    n = int(math.floor(R / h + 1e-9))
    pts = [complex(i * h, j * h) for i in range(-n, n + 1) for j in range(-n, n + 1)]
    pts = [k for k in pts if abs(k) <= R + 1e-12]
    pts.sort(key=lambda k: (abs(k), k.real, k.imag))
    return pts


def cauchy_matrix(grid):
    """The entries 1 / (k - k') for k, k' on the grid, 0 on the diagonal."""
    return [[(1 / (k - kp) if k != kp else 0j) for kp in grid] for k in grid]


def cauchy_transform(grid, h, values, inv=None):
    """(1/pi) int F(k') / (k - k') dk' on the grid, by the midpoint rule without the self cell."""
    inv = inv if inv is not None else cauchy_matrix(grid)
    c = h * h / math.pi
    return [c * sum(a * v for a, v in zip(row, values)) for row in inv]


def d_bar(lams, points, R, h, iters=200, tol=1e-12, return_mu=False):
    """Reconstruct gamma at the points z (complex numbers in the unit disk).

    lams are the DN eigenvalues lambda_1, lambda_2, ... of a radial
    conductivity; R is the cutoff of the scattering transform and h the grid
    spacing. Returns the list of gamma(z), or of (gamma(z), mu on the grid,
    the grid, the weights w) if return_mu is true.
    """
    grid = k_grid(R, h)  # @line L1
    tvals = [t_exp_radial(lams, k) for k in grid]  # @line L2
    inv = cauchy_matrix(grid)
    c = h * h / (4 * math.pi * math.pi)
    out = []
    for z in points:  # @line L3
        w = [(c * tv * cmath.exp(-2j * (kp * z).real) / kp.conjugate() if kp != 0 else 0j)
             for kp, tv in zip(grid, tvals)]  # @line L4
        mu = [1 + 0j] * len(grid)  # @line L5
        for _ in range(iters):  # @line L6
            cm = [wi * m.conjugate() for wi, m in zip(w, mu)]
            new = [1 + sum(a * b for a, b in zip(row, cm)) for row in inv]  # @line L7
            change = max(abs(a - b) for a, b in zip(new, mu))
            mu = new
            if change < tol:  # @line L8
                break
        else:
            raise RuntimeError("the fixed-point iteration did not converge")
        gz = (mu[0] * mu[0]).real  # @line L9
        out.append((gz, mu, grid, w) if return_mu else gz)
    return out  # @line L10


def gamma0_reference(lams, R, steps=4000):
    """gamma(0) from the truncated equation with a radial real t, in closed form:
    exp(-(1/pi) int_0^R t(s) / s ds), by Simpson's rule."""
    def f(s):
        return t_exp_radial(lams, s) / s if s > 0 else 0.0
    hs = R / steps
    acc = f(0.0) + f(R)
    for i in range(1, steps):
        acc += (4 if i % 2 else 2) * f(i * hs)
    return math.exp(-(acc * hs / 3) / math.pi)
