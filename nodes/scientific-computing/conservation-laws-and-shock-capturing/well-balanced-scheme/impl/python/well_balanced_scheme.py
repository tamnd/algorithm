# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/well-balanced-scheme/. The authors are listed in prov/DMAAHD.jsonl.

"""Well-balanced first-order scheme for the 1D shallow water equations with a bottom.

Equations: h_t + (hu)_x = 0, (hu)_t + (hu^2 + g h^2 / 2)_x = -g h z_x, with bottom z(x).
Cells of width dx with values (h_i, q_i = h_i u_i) and bottom z_i; solid walls at both ends.
The well-balanced scheme is the hydrostatic reconstruction of Audusse, Bouchut, Bristeau,
Klein and Perthame (2004) with the Rusanov flux: at each face the depths are rebuilt
relative to z* = max(z_i, z_{i+1}), the flux is evaluated at the rebuilt states, and the
momentum fluxes seen by the two cells are corrected by g/2 (h^2 - h*^2). The naive scheme
(Rusanov flux plus a centred source term) is included for comparison.

Precondition: h_i >= 0, dx > 0, dt > 0, and dt max(|u| + sqrt(g h)) <= dx / 2 for h >= 0.
Cost: Theta(m) per step for m cells; memory Theta(m).
"""

import math
from typing import List, Tuple

G = 9.81
State = Tuple[List[float], List[float]]


def phys_flux(h: float, q: float, g: float = G) -> Tuple[float, float]:
    u = q / h if h > 0 else 0.0
    return q, q * u + g * h * h / 2


def rusanov(hl, ql, hr, qr, g=G):
    """Rusanov (local Lax-Friedrichs) flux for shallow water; dry states have speed 0."""
    ul = ql / hl if hl > 0 else 0.0
    ur = qr / hr if hr > 0 else 0.0
    a = max(abs(ul) + math.sqrt(g * hl), abs(ur) + math.sqrt(g * hr))
    fl, fr = phys_flux(hl, ql, g), phys_flux(hr, qr, g)
    return (0.5 * (fl[0] + fr[0]) - 0.5 * a * (hr - hl),
            0.5 * (fl[1] + fr[1]) - 0.5 * a * (qr - ql))


def _with_walls(h, q, z):
    """Ghost cells for solid walls: same depth and bottom, opposite momentum."""
    return [h[0]] + h + [h[-1]], [-q[0]] + q + [-q[-1]], [z[0]] + z + [z[-1]]


def hr_step(h: List[float], q: List[float], z: List[float], dx: float, dt: float, g: float = G) -> State:
    """One forward Euler step of the hydrostatic reconstruction scheme."""
    H, Q, Z = _with_walls(h, q, z)
    n = len(h)
    left, right = [], []                       # flux seen by the cell left / right of each face
    for i in range(n + 1):                     # face between ghost-padded cells i and i + 1
        zs = max(Z[i], Z[i + 1])                                           # @line L1
        hl = max(0.0, H[i] + Z[i] - zs)                                    # @line L2
        hr = max(0.0, H[i + 1] + Z[i + 1] - zs)
        ul = Q[i] / H[i] if H[i] > 0 else 0.0
        ur = Q[i + 1] / H[i + 1] if H[i + 1] > 0 else 0.0
        f0, f1 = rusanov(hl, hl * ul, hr, hr * ur, g)                      # @line L3
        left.append((f0, f1 + g / 2 * (H[i] * H[i] - hl * hl)))            # @line L4
        right.append((f0, f1 + g / 2 * (H[i + 1] * H[i + 1] - hr * hr)))
    lam = dt / dx
    hn = [h[i] - lam * (left[i + 1][0] - right[i][0]) for i in range(n)]   # @line L5
    qn = [q[i] - lam * (left[i + 1][1] - right[i][1]) for i in range(n)]
    return hn, qn


def naive_step(h: List[float], q: List[float], z: List[float], dx: float, dt: float, g: float = G) -> State:
    """Rusanov flux plus the centred source -g h_i (z_{i+1} - z_{i-1}) / (2 dx); not well balanced."""
    H, Q, Z = _with_walls(h, q, z)
    n = len(h)
    F = [rusanov(H[i], Q[i], H[i + 1], Q[i + 1], g) for i in range(n + 1)]
    lam = dt / dx
    hn = [h[i] - lam * (F[i + 1][0] - F[i][0]) for i in range(n)]
    qn = [q[i] - lam * (F[i + 1][1] - F[i][1]) - dt * g * h[i] * (Z[i + 2] - Z[i]) / (2 * dx)
          for i in range(n)]
    return hn, qn


def max_speed(h, q, g=G):
    return max((abs(b / a) + math.sqrt(g * a)) if a > 0 else 0.0 for a, b in zip(h, q))


def run(step, h, q, z, dx, T, cfl=0.45, g=G) -> State:
    """Advance to time T with dt = cfl dx / max speed (a forward Euler scheme)."""
    if not dx > 0:
        raise ValueError("dx must be positive")
    if min(h) < 0:
        raise ValueError("depths must be nonnegative")
    t = 0.0
    while t < T - 1e-14:
        s = max_speed(h, q, g)
        dt = min(cfl * dx / s if s > 0 else T - t, T - t)
        h, q = step(h, q, z, dx, dt, g)
        t += dt
    return h, q
