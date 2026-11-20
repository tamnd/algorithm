# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operator-inference/. The authors are listed in prov/094ATM.jsonl.
"""Operator inference (OpInf) of Peherstorfer and Willcox, for a quadratic discrete-time model.

The full model is the viscous Burgers equation u_t + (u^2 / 2)_x = nu u_xx on (0, 1) with
u = 0 at both ends, central differences on n interior points and explicit Euler steps:
    x_(k+1) = f(x_k) = x_k + dt (L x_k + Q(x_k)),
with the linear part L and the quadratic part Q. The reduced model has the same form,
    a_(k+1) = A_hat a_k + H_hat s(a_k),   s(a) = (a_i a_j for i <= j),
and OpInf learns A_hat and H_hat by least squares from reduced states only. The full model is
used only as a black box that maps a state to the next state.
"""

import math
from typing import Callable

Vector = list[float]
Matrix = list[list[float]]


def burgers_step(n: int, nu: float, dt: float) -> Callable[[Vector], Vector]:
    """The black-box full model: one explicit Euler step of the discretized Burgers equation."""
    h = 1.0 / (n + 1)

    def f(x: Vector) -> Vector:
        out = []
        for i in range(n):
            left = x[i - 1] if i > 0 else 0.0
            right = x[i + 1] if i < n - 1 else 0.0
            diff = nu * (left - 2.0 * x[i] + right) / (h * h)
            conv = -(right * right - left * left) / (4.0 * h)
            out.append(x[i] + dt * (diff + conv))
        return out

    return f


def trajectory(f: Callable[[Vector], Vector], x0: Vector, k: int) -> list[Vector]:
    xs = [list(x0)]
    for _ in range(k):
        xs.append(f(xs[-1]))
    return xs


def jacobi_eigh(a: Matrix, tol: float = 1e-15, sweeps: int = 60) -> tuple[Vector, Matrix]:
    """Eigenvalues (decreasing) and eigenvectors (columns of v) of a symmetric a, cyclic Jacobi."""
    n = len(a)
    a = [list(row) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= tol * (math.sqrt(sum(a[i][i] ** 2 for i in range(n))) or 1.0):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    a[k][p], a[k][q] = c * a[k][p] - s * a[k][q], s * a[k][p] + c * a[k][q]
                for k in range(n):
                    a[p][k], a[q][k] = c * a[p][k] - s * a[q][k], s * a[p][k] + c * a[q][k]
                for k in range(n):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    order = sorted(range(n), key=lambda i: -a[i][i])
    return [a[i][i] for i in order], [[v[k][i] for i in order] for k in range(n)]


def pod_basis(snaps: list[Vector], r: int) -> tuple[list[Vector], Vector]:
    """r leading POD modes (orthonormal, as a list of columns) and the singular values, from the
    eigenvectors of the n by n matrix S S^T (here n is smaller than the number of snapshots)."""
    n = len(snaps[0])
    cov = [[sum(x[i] * x[j] for x in snaps) for j in range(n)] for i in range(n)]
    lam, w = jacobi_eigh(cov)
    sig = [math.sqrt(max(t, 0.0)) for t in lam]
    modes = [[w[i][j] for i in range(n)] for j in range(r)]
    return modes, sig


def restrict(v: list[Vector], x: Vector) -> Vector:
    """V^T x."""
    return [sum(a * b for a, b in zip(vj, x)) for vj in v]


def lift(v: list[Vector], a: Vector) -> Vector:
    """V a."""
    return [sum(aj * vj[i] for aj, vj in zip(a, v)) for i in range(len(v[0]))]


def sq(a: Vector) -> Vector:
    """The r(r+1)/2 quadratic terms a_i a_j, i <= j."""
    return [a[i] * a[j] for i in range(len(a)) for j in range(i, len(a))]


def reprojected_states(f: Callable[[Vector], Vector], v: list[Vector], x0: Vector, k: int) -> list[Vector]:
    """Re-projection: a_0 = V^T x0 and a_(j+1) = V^T f(V a_j), one black-box step at a time."""
    a = [restrict(v, x0)]
    for _ in range(k):
        a.append(restrict(v, f(lift(v, a[-1]))))
    return a


def lstsq_qr(d: Matrix, rhs: Matrix) -> Matrix:
    """Solve min ||d X - rhs||_F by modified Gram-Schmidt QR (two passes) and back substitution."""
    rows, cols = len(d), len(d[0])
    qcols = [[d[i][j] for i in range(rows)] for j in range(cols)]
    rr = [[0.0] * cols for _ in range(cols)]
    for j in range(cols):
        for _ in range(2):
            for i in range(j):
                c = sum(a * b for a, b in zip(qcols[i], qcols[j]))
                rr[i][j] += c
                qcols[j] = [a - c * b for a, b in zip(qcols[j], qcols[i])]
        nrm = math.sqrt(sum(t * t for t in qcols[j]))
        if nrm == 0.0:
            raise ValueError("the data matrix does not have full column rank")
        rr[j][j] = nrm
        qcols[j] = [t / nrm for t in qcols[j]]
    out = []
    for col in range(len(rhs[0])):
        b = [sum(qcols[j][i] * rhs[i][col] for i in range(rows)) for j in range(cols)]
        x = [0.0] * cols
        for j in range(cols - 1, -1, -1):
            x[j] = (b[j] - sum(rr[j][t] * x[t] for t in range(j + 1, cols))) / rr[j][j]
        out.append(x)
    return [[out[col][j] for col in range(len(rhs[0]))] for j in range(cols)]


def opinf(states: list[list[Vector]], r: int) -> tuple[Matrix, Matrix]:
    """Learn (A_hat, H_hat) from reduced trajectories (each a list of r-vectors a_0..a_K)."""
    d: Matrix = []
    rhs: Matrix = []
    for traj in states:
        for k in range(len(traj) - 1):
            d.append(list(traj[k]) + sq(traj[k]))  # @line L3: the data matrix row [a_k, s(a_k)]
            rhs.append(list(traj[k + 1]))  # @line L4: the right side a_(k+1)
    o = lstsq_qr(d, rhs)  # @line L5: least squares by QR
    a_hat = [[o[j][i] for j in range(r)] for i in range(r)]  # @line L6: O^T = [A_hat H_hat]
    h_hat = [[o[r + j][i] for j in range(len(o) - r)] for i in range(r)]
    return a_hat, h_hat  # @line L7


def learn(f: Callable[[Vector], Vector], x0s: list[Vector], k: int, r: int, reproject: bool) -> tuple[list[Vector], Matrix, Matrix]:
    """The whole method: snapshots, POD basis, reduced data, least squares."""
    snaps = [x for x0 in x0s for x in trajectory(f, x0, k)]
    v, _ = pod_basis(snaps, r)  # @line L1
    if reproject:  # @line L2: reduced states, projected or re-projected
        states = [reprojected_states(f, v, x0, k) for x0 in x0s]
    else:
        states = [[restrict(v, x) for x in trajectory(f, x0, k)] for x0 in x0s]
    a_hat, h_hat = opinf(states, r)
    return v, a_hat, h_hat


def intrusive_rom(f: Callable[[Vector], Vector], v: list[Vector]) -> tuple[Matrix, Matrix]:
    """Reference: the Galerkin projection V^T f(V a) of the full step, read off by polarization.
    f(x) = x + dt (L x + Q(x)) is a polynomial of degree 2 with f(0) = 0."""
    r = len(v)

    def qpart(x: Vector) -> Vector:
        # quadratic part of f: (f(x) + f(-x)) / 2
        fp, fm = f(x), f([-t for t in x])
        return [(a + b) / 2.0 for a, b in zip(fp, fm)]

    def lpart(x: Vector) -> Vector:
        fp, fm = f(x), f([-t for t in x])
        return [(a - b) / 2.0 for a, b in zip(fp, fm)]

    a_hat = [[0.0] * r for _ in range(r)]
    for j in range(r):
        col = restrict(v, lpart(v[j]))
        for i in range(r):
            a_hat[i][j] = col[i]
    pairs = [(i, j) for i in range(r) for j in range(i, r)]
    h_hat = [[0.0] * len(pairs) for _ in range(r)]
    for c, (i, j) in enumerate(pairs):
        if i == j:
            w = qpart(v[i])
        else:
            s = [a + b for a, b in zip(v[i], v[j])]
            w = [a - b - e for a, b, e in zip(qpart(s), qpart(v[i]), qpart(v[j]))]
        col = restrict(v, w)
        for t in range(r):
            h_hat[t][c] = col[t]
    return a_hat, h_hat


def rom_step(a_hat: Matrix, h_hat: Matrix, a: Vector) -> Vector:
    s = sq(a)
    return [sum(ai * x for ai, x in zip(row, a)) + sum(hi * y for hi, y in zip(hrow, s)) for row, hrow in zip(a_hat, h_hat)]


def rom_trajectory(a_hat: Matrix, h_hat: Matrix, a0: Vector, k: int) -> list[Vector]:
    out = [list(a0)]
    for _ in range(k):
        out.append(rom_step(a_hat, h_hat, out[-1]))
    return out
