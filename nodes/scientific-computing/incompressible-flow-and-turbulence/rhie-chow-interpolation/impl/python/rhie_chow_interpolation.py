# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rhie-chow-interpolation/. The authors are listed in prov/SYEY5V.jsonl.

"""Rhie-Chow momentum interpolation on a periodic 1D collocated grid.

n cells of width h = 1 / n; u[i] and p[i] live at the cell centers, and face i
is between the cells i and i + 1 (indices wrap). The model momentum equation

    c u - nu u_xx = s - p_x

is discretized as a_P u_i - a_N (u_{i-1} + u_{i+1}) = s_i - G_i(p) with
a_N = nu / h^2, a_P = c + 2 a_N and the central cell gradient
G_i(p) = (p_{i+1} - p_{i-1}) / (2 h). Continuity says that the face
velocities are equal: (u_f[i] - u_f[i-1]) / h = 0.

simple() runs SIMPLE with momentum under-relaxation alpha and pressure
under-relaxation alpha_p. The face velocity is the Rhie-Chow formula
u_f = avg(uhat) - d_f (p_{i+1} - p_i) / h with uhat = H / a_P and d = 1 / a_P
of the relaxed equation; majumdar=True adds Majumdar's term
(1 - alpha) (u_f_old - avg(u_old)), which makes the fixed point independent of alpha.
"""

from scisparse import cg


def cell_gradient(p, h):
    n = len(p)
    return [(p[(i + 1) % n] - p[i - 1]) / (2 * h) for i in range(n)]


def avg(x):
    """Linear interpolation of a cell field to the faces."""
    n = len(x)
    return [(x[i] + x[(i + 1) % n]) / 2 for i in range(n)]


def face_difference(p, h):
    n = len(p)
    return [(p[(i + 1) % n] - p[i]) / h for i in range(n)]


def face_divergence(uf, h):
    return [(uf[i] - uf[i - 1]) / h for i in range(len(uf))]


def linear_continuity_operator(p, h, a):
    """Continuity of linearly interpolated cell velocities: the pressure part, -div(avg(G p / a))."""
    return [-x for x in face_divergence(avg([g / a for g in cell_gradient(p, h)]), h)]


def rhie_chow_continuity_operator(p, h, a):
    """Continuity of Rhie-Chow face velocities: the pressure part, -div(d_f dp / h), the compact stencil."""
    return [-x for x in face_divergence([g / a for g in face_difference(p, h)], h)]


def _compact_matrix(n, h, d):
    w = d / (h * h)
    return [{i: 2 * w, (i - 1) % n: -w, (i + 1) % n: -w} for i in range(n)]


def simple(s, c, nu, alpha=0.7, alpha_p=0.3, majumdar=False, tol=1e-12, maxit=20000):
    """Returns (u, uf, p, iterations); p has mean 0."""
    n = len(s)
    h = 1.0 / n
    an = nu / (h * h)
    ap = (c + 2 * an) / alpha                     # relaxed diagonal
    d = 1 / ap
    A = _compact_matrix(n, h, d)
    u = [0.0] * n
    uf = [0.0] * n
    p = [0.0] * n
    for it in range(1, maxit + 1):
        G = cell_gradient(p, h)
        hh = [an * (u[i - 1] + u[(i + 1) % n]) + s[i] + (1 - alpha) * ap * u[i] for i in range(n)]
        uhat = [x / ap for x in hh]                                        # @line L1
        ustar = [uhat[i] - d * G[i] for i in range(n)]                    # @line L2
        ufs = [a - d * b for a, b in zip(avg(uhat), face_difference(p, h))]  # @line L3
        if majumdar:
            ufs = [ufs[i] + (1 - alpha) * (uf[i] - au) for i, au in enumerate(avg(u))]
        rhs = [-x for x in face_divergence(ufs, h)]
        pc, _ = cg(A, rhs, tol=1e-13)                                      # @line L4
        mean = sum(pc) / n
        pc = [x - mean for x in pc]
        Gc = cell_gradient(pc, h)
        uf = [a - d * b for a, b in zip(ufs, face_difference(pc, h))]      # @line L5
        unew = [ustar[i] - d * Gc[i] for i in range(n)]
        p = [p[i] + alpha_p * pc[i] for i in range(n)]
        change = max(abs(unew[i] - u[i]) for i in range(n))
        u = unew
        if change < tol and max(map(abs, pc)) < tol:
            return u, uf, p, it                                            # @line L6
    raise RuntimeError("SIMPLE did not converge")


def momentum_residual(u, p, s, c, nu):
    n = len(u)
    h = 1.0 / n
    an = nu / (h * h)
    G = cell_gradient(p, h)
    return max(abs((c + 2 * an) * u[i] - an * (u[i - 1] + u[(i + 1) % n]) - s[i] + G[i]) for i in range(n))
