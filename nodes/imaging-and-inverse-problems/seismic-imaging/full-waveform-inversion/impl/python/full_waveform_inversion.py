# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/full-waveform-inversion/. The authors are listed in prov/H0DMN3.jsonl.
"""Full waveform inversion (FWI) of 1D acoustic data with the adjoint-state gradient.

Conventions (the imaging and inverse problems pages):
- The 1D constant density acoustic wave equation m u_tt - u_zz = f with the
  model m = 1 / v^2 per grid cell (s^2/m^2) and u = 0 for t <= 0.
- The scheme, for n = 0 .. N - 1, with u^0 = u^{-1} = 0:
      u^{n+1} = 2 u^n - u^{n-1} + (dt^2 / m) (L u^n + f^n),
  L u_i = (u_{i-1} - 2 u_i + u_{i+1}) / h^2 and u = 0 outside the grid
  (Dirichlet ends). It is stable for v dt / h <= 1 (CFL condition in 1D).
- The data are u^n at the receiver cells for n = 0 .. N. The misfit is
      J(m) = (1/2) sum_n sum_r (u^n_r - d^n_r)^2.
- The gradient comes from the adjoint state of the discrete scheme:
      lam^k = 2 lam^{k+1} - lam^{k+2} + (dt^2 / m) L lam^{k+1} + (1 / m) R^T res^k,
  for k = N .. 1 with lam^{N+1} = lam^{N+2} = 0, and
      dJ/dm_i = - sum_{n=0}^{N-1} lam^{n+1}_i (u^{n+1} - 2 u^n + u^{n-1})_i.
  This is the exact gradient of the discrete misfit (no discretization gap).
- The FWI loop is gradient descent with a backtracking (Armijo) line search.

Cost per iteration: one forward and one adjoint propagation, O(N n) each for
n cells and N steps, plus a few forward runs in the line search; the forward
field is stored, O(N n) memory.
"""

import math


def second_diff(u, h):
    """L u with u = 0 outside the grid."""
    n = len(u)
    c = 1.0 / (h * h)
    return [c * ((u[i - 1] if i > 0 else 0.0) - 2.0 * u[i] + (u[i + 1] if i < n - 1 else 0.0)) for i in range(n)]


def forward(m, src_cell, wavelet, recs, dt, h):
    """Run the scheme for len(wavelet) steps; the source adds wavelet[n] / h at src_cell.

    Returns (fields, data): fields[n] = u^n for n = 0 .. N, data[n][r] = u^n at recs[r].
    """
    n = len(m)
    prev, cur = [0.0] * n, [0.0] * n
    fields = [cur]
    for k in range(len(wavelet)):
        lap = second_diff(cur, h)
        lap[src_cell] += wavelet[k] / h
        nxt = [2.0 * cur[i] - prev[i] + dt * dt * lap[i] / m[i] for i in range(n)]
        fields.append(nxt)
        prev, cur = cur, nxt
    return fields, [[u[c] for c in recs] for u in fields]


def misfit(m, src_cell, wavelet, recs, dobs, dt, h):
    """J(m) = (1/2) sum over times and receivers of the squared data residual."""
    _, d = forward(m, src_cell, wavelet, recs, dt, h)
    return 0.5 * sum((a - b) ** 2 for ra, rb in zip(d, dobs) for a, b in zip(ra, rb))


def gradient(m, src_cell, wavelet, recs, dobs, dt, h):
    """The misfit J(m) and its exact gradient by the adjoint-state method."""
    n = len(m)
    fields, d = forward(m, src_cell, wavelet, recs, dt, h)  # @line L1
    res = [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(d, dobs)]  # @line L2
    j = 0.5 * sum(x * x for row in res for x in row)
    nsteps = len(wavelet)
    lam1, lam2 = [0.0] * n, [0.0] * n  # @line L3
    g = [0.0] * n
    zero = [0.0] * n
    for k in range(nsteps, 0, -1):  # @line L4
        lap = second_diff(lam1, h)
        lam = [2.0 * lam1[i] - lam2[i] + dt * dt * lap[i] / m[i] for i in range(n)]
        for r, c in enumerate(recs):
            lam[c] += res[k][r] / m[c]  # @line L5
        u_next = fields[k]
        u_cur = fields[k - 1]
        u_prev = fields[k - 2] if k >= 2 else zero
        for i in range(n):
            g[i] -= lam[i] * (u_next[i] - 2.0 * u_cur[i] + u_prev[i])  # @line L6
        lam1, lam2 = lam, lam1
    return j, g  # @line L7


def full_waveform_inversion(m0, src_cell, wavelet, recs, dobs, dt, h, iters, max_rel_step=0.05):
    """Gradient descent with backtracking on J(m), started at m0.

    The first trial step changes m by max_rel_step times max(m) at the cell of
    the largest gradient entry; it is halved until the Armijo condition
    J(m - a g) <= J(m) - 1e-4 a ||g||^2 holds (at most 30 halvings).
    Returns the final model and the list of misfits.
    """
    m = list(m0)
    history = []
    for _ in range(iters):
        j, g = gradient(m, src_cell, wavelet, recs, dobs, dt, h)
        history.append(j)
        gmax = max(abs(x) for x in g)
        gg = sum(x * x for x in g)
        if gmax == 0.0:
            break
        a = max_rel_step * max(m) / gmax
        for _ in range(30):
            trial = [mi - a * gi for mi, gi in zip(m, g)]
            if min(trial) > 0.0 and misfit(trial, src_cell, wavelet, recs, dobs, dt, h) <= j - 1e-4 * a * gg:
                m = trial
                break
            a *= 0.5
        else:
            break
    history.append(misfit(m, src_cell, wavelet, recs, dobs, dt, h))
    return m, history


def ricker(t, f0):
    """The Ricker wavelet (1 - 2 a) exp(-a) with a = (pi f0 t)^2, peak frequency f0."""
    a = (math.pi * f0 * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)
