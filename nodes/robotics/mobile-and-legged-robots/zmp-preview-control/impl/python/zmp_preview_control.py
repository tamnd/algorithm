# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zmp-preview-control/. The authors are listed in prov/CQQDWX.jsonl.
"""ZMP preview control on the cart-table model (Kajita et al. 2003).

One horizontal axis. The state is x = (c, c', c'') of the center of mass,
the input is the jerk u = c''', and the output is the ZMP of the
cart-table model, p = c - (zc / g) c''. The controller works on the
incremental state X = (e, dx), where e = p - p_ref is the ZMP error and
dx = x_k - x_(k-1), with the input du = u_k - u_(k-1). It minimizes

    sum over k of  Qe e_k^2 + dx_k^T Qx dx_k + R du_k^2

and uses the next N reference values. The law is

    du_k = -K X_k + sum_(j = 1..N) f_j (p_ref[k + j] - p_ref[k + j - 1]).

Matrices are lists of rows; the linear algebra is in rbm.py.
"""

import rbm

G = 9.81


def cart_table(T, zc, g=G):
    """Return A, B, C of the cart-table model sampled with period T."""
    A = [[1.0, T, T * T / 2.0], [0.0, 1.0, T], [0.0, 0.0, 1.0]]
    B = [T ** 3 / 6.0, T * T / 2.0, T]
    C = [1.0, 0.0, -zc / g]
    return A, B, C


def augment(A, B, C):
    """Return the incremental model X+ = At X + Bt du - I1 dr."""
    ca = [rbm.dot(C, [A[i][j] for i in range(3)]) for j in range(3)]
    at = [[1.0] + ca] + [[0.0] + list(A[i]) for i in range(3)]
    bt = [rbm.dot(C, B)] + list(B)
    return at, bt


def solve_dare(at, bt, q, r, tol=1e-12, max_iter=200000):
    """Solve P = Q + A^T P A - A^T P B (R + B^T P B)^(-1) B^T P A by iteration.

    The input is scalar, so R + B^T P B is a number. The iteration starts
    at P = Q and stops when no entry changes by more than tol times the
    largest entry of P.
    """
    n = len(at)
    p = [row[:] for row in q]
    a_t = rbm.transpose(at)
    for _ in range(max_iter):
        pb = rbm.matvec(p, bt)
        s = r + rbm.dot(bt, pb)
        bpa = [rbm.dot(pb, [at[i][j] for i in range(n)]) for j in range(n)]
        apa = rbm.mul(a_t, rbm.mul(p, at))
        new = [[q[i][j] + apa[i][j] - bpa[i] * bpa[j] / s for j in range(n)] for i in range(n)]
        big = max(abs(v) for row in new for v in row)
        diff = max(abs(new[i][j] - p[i][j]) for i in range(n) for j in range(n))
        p = new
        if diff <= tol * big:
            return p
    raise ValueError("the Riccati iteration did not converge")


def preview_gains(T, zc, n_preview, qe=1.0, qx=0.0, r=1e-6, g=G):
    """Return (K, f, P): the state gain, the N preview gains and the Riccati solution."""
    A, B, C = cart_table(T, zc, g)  # @line L1
    at, bt = augment(A, B, C)  # @line L2
    q = rbm.zeros(4, 4)
    q[0][0] = qe
    for i in range(1, 4):
        q[i][i] = qx
    p = solve_dare(at, bt, q, r)  # @line L3
    pb = rbm.matvec(p, bt)
    s = r + rbm.dot(bt, pb)
    k = [rbm.dot(pb, [at[i][j] for i in range(4)]) / s for j in range(4)]  # @line L4
    ac = [[at[i][j] - bt[i] * k[j] for j in range(4)] for i in range(4)]  # @line L5
    ac_t = rbm.transpose(ac)
    v = [p[i][0] for i in range(4)]  # @line L6: v = P I1
    f = []
    for _ in range(n_preview):  # @line L7
        f.append(rbm.dot(bt, v) / s)  # @line L8
        v = rbm.matvec(ac_t, v)  # @line L9
    return k, f, p


def preview_control(p_ref, T, zc, n_preview, x0=None, qe=1.0, qx=0.0, r=1e-6, g=G):
    """Run the closed loop on the cart-table model.

    p_ref[k] is the ZMP reference at step k; values past the end repeat the
    last one. Return (xs, ps, us): the states x_0 .. x_K, the ZMP p_0 .. p_(K-1)
    and the jerks u_0 .. u_(K-1), where K = len(p_ref).
    """
    A, B, C = cart_table(T, zc, g)
    k_gain, f, _ = preview_gains(T, zc, n_preview, qe, qx, r, g)
    last = len(p_ref) - 1

    def ref(i):
        return p_ref[min(i, last)]

    x = list(x0) if x0 is not None else [ref(0), 0.0, 0.0]
    x_prev = list(x)  # @line L10
    u = 0.0
    xs, ps, us = [list(x)], [], []
    for kk in range(len(p_ref)):  # @line L11
        p = rbm.dot(C, x)
        e = p - ref(kk)  # @line L12
        dx = [a - b for a, b in zip(x, x_prev)]  # @line L13
        du = -(k_gain[0] * e + rbm.dot(k_gain[1:], dx))  # @line L14
        du += sum(f[j - 1] * (ref(kk + j) - ref(kk + j - 1)) for j in range(1, n_preview + 1))
        u += du  # @line L15
        x_prev = x
        x = [a + b * u for a, b in zip(rbm.matvec(A, x), B)]  # @line L16
        ps.append(p)
        us.append(u)
        xs.append(list(x))
    return xs, ps, us


def walking_reference(T, step_time, n_steps, step_length, half_width, settle=1.0):
    """Return ZMP references (px, py) for straight walking.

    The ZMP rests at 0 for settle seconds, then moves to each foot in turn:
    foot i (i = 1 .. n_steps) is at x = (i - 1) step_length and
    y = +half_width or -half_width, alternating, for step_time seconds.
    At the end it returns to the middle of the last two feet.
    """
    px, py = [], []
    m = int(round(settle / T))
    px += [0.0] * m
    py += [0.0] * m
    s = int(round(step_time / T))
    for i in range(1, n_steps + 1):
        x = (i - 1) * step_length
        y = half_width if i % 2 == 1 else -half_width
        px += [x] * s
        py += [y] * s
    x_end = (n_steps - 1) * step_length
    px += [x_end] * (2 * m)
    py += [0.0] * (2 * m)
    return px, py
