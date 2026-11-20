# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-approximation-of-transport/. The authors are listed in prov/P2WTRA.jsonl.
"""The one-speed diffusion approximation in a slab, solved by cell-centered finite volumes.

    -d/dx (D dphi/dx) + sigma_a phi = q,   J = -D dphi/dx (Fick's law),
    D = 1 / (3 sigma_tr),  sigma_tr = sigma_t - mu_bar sigma_s.

Cells j = 0 .. M - 1 of widths dx[j] carry constant data. The current through
the face between cells j and j + 1 is (phi_j - phi_(j+1)) / R with the
resistance R = dx_j / (2 D_j) + dx_(j+1) / (2 D_(j+1)), so the scheme is
exact for a flux that is linear in each cell and keeps the particle balance
of every cell.

Face conditions, for the current that leaves the slab:
    "zero"     phi = 0 on the face:              J_out = phi_cell / (dx / (2 D))
    "marshak"  vacuum, Marshak condition J_out = phi_face / 2, which is phi = 0 at the extrapolated distance 2 D
    a number d phi = 0 at the distance d outside the face: J_out = phi_cell / (dx / (2 D) + d / D)
    "reflect"  J_out = 0

The tridiagonal system is solved by the Thomas algorithm of the shared helper scisparse.
"""

import math

from scisparse import thomas

MILNE = 0.7104461  # the extrapolation distance of the Milne problem in mean free paths, c = 1


def diffusion_coefficient(sigma_t, sigma_s=0.0, mu_bar=0.0):
    """D = 1 / (3 sigma_tr) with the transport cross section sigma_tr = sigma_t - mu_bar sigma_s."""
    return 1.0 / (3.0 * (sigma_t - mu_bar * sigma_s))


def _face_resistance(bc, d, h):
    """Resistance from the cell center to the point where phi = 0, or None for no leakage."""
    if bc == "reflect":
        return None
    if bc == "zero":
        return h / (2.0 * d)
    if bc == "marshak":
        return h / (2.0 * d) + 2.0
    return h / (2.0 * d) + float(bc) / d


def solve_fixed_source(D, sigma_a, q, dx, left="marshak", right="marshak"):
    """Solve the diffusion equation with the cell data D, sigma_a and q.

    Returns (phi, leak_left, leak_right), the leakages being the currents that leave each face."""
    m = len(dx)
    a, b, c, rhs = [0.0] * m, [0.0] * m, [0.0] * m, [0.0] * m
    for j in range(m):
        b[j] = sigma_a[j] * dx[j]
        rhs[j] = q[j] * dx[j]
    for j in range(m - 1):
        g = 1.0 / (dx[j] / (2.0 * D[j]) + dx[j + 1] / (2.0 * D[j + 1]))
        b[j] += g
        b[j + 1] += g
        c[j] -= g
        a[j + 1] -= g
    rl = _face_resistance(left, D[0], dx[0])
    rr = _face_resistance(right, D[-1], dx[-1])
    if rl is not None:
        b[0] += 1.0 / rl
    if rr is not None:
        b[-1] += 1.0 / rr
    phi = thomas(a, b, c, rhs)
    leak_left = phi[0] / rl if rl is not None else 0.0
    leak_right = phi[-1] / rr if rr is not None else 0.0
    return phi, leak_left, leak_right


def k_eigenvalue(D, sigma_a, nu_sigma_f, dx, left="zero", right="zero", tol=1e-12, max_iter=10000):
    """Power iteration on the fission source. Returns (k, phi normalized to max 1, iterations)."""
    m = len(dx)
    phi = [1.0] * m
    k = 1.0
    for it in range(1, max_iter + 1):
        src = [nu_sigma_f[j] * phi[j] / k for j in range(m)]
        new, _, _ = solve_fixed_source(D, sigma_a, src, dx, left, right)
        prod_old = sum(nu_sigma_f[j] * phi[j] * dx[j] for j in range(m))
        prod_new = sum(nu_sigma_f[j] * new[j] * dx[j] for j in range(m))
        k_new = k * prod_new / prod_old
        top = max(new)
        phi = [v / top for v in new]
        if abs(k_new - k) <= tol * k_new:
            return k_new, phi, it
        k = k_new
    return k, phi, max_iter


def bare_slab_k(nu_sigma_f, sigma_a, D, width):
    """k of a bare homogeneous slab with phi = 0 at the faces of the given width: buckling (pi / width)^2."""
    return nu_sigma_f / (sigma_a + D * (math.pi / width) ** 2)


def slab_leakage_marshak(q, sigma_a, D, width):
    """Exact diffusion leakage through each face of a homogeneous slab with a uniform source and Marshak faces.

    phi = (q / sigma_a) (1 - A cosh(kappa (x - width / 2))), kappa = sqrt(sigma_a / D),
    A = 1 / (cosh(kappa width / 2) + 2 D kappa sinh(kappa width / 2))."""
    kappa = math.sqrt(sigma_a / D)
    h = kappa * width / 2.0
    amp = 1.0 / (math.cosh(h) + 2.0 * D * kappa * math.sinh(h))
    return q / sigma_a * D * amp * kappa * math.sinh(h)


def diffusion_decay_constant(c):
    """kappa in units of sigma_t for phi ~ exp(-kappa sigma_t x) in a source-free medium: kappa^2 = 3 (1 - c)."""
    return math.sqrt(3.0 * (1.0 - c))


def transport_decay_constant(c):
    """The exact one-speed transport value: the root kappa in (0, 1) of c atanh(kappa) / kappa = 1, for 0 < c < 1."""
    lo, hi = 1e-15, 1.0 - 1e-16
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if c * math.atanh(mid) / mid < 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
