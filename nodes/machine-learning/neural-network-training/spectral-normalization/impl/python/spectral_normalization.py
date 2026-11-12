# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-normalization/. The authors are listed in prov/FFNMF4.jsonl.
"""Spectral normalization (Miyato, Kataoka, Koyama and Yoshida 2018): W_SN = W / sigma(W), with the
largest singular value sigma(W) estimated by one step of power iteration per training update and a
persistent left vector u. A cyclic Jacobi eigensolver on W^T W gives the exact value for tests.
"""

import math
import random

Vec = list[float]
Mat = list[list[float]]


def matvec(w: Mat, x: Vec) -> Vec:
    return [sum(a * b for a, b in zip(row, x)) for row in w]


def matvec_t(w: Mat, u: Vec) -> Vec:
    out = [0.0] * len(w[0])
    for row, ui in zip(w, u):
        for j, a in enumerate(row):
            out[j] += a * ui
    return out


def norm(x: Vec) -> float:
    return math.sqrt(sum(v * v for v in x))


def unit(x: Vec) -> Vec:
    n = norm(x)
    return [v / n for v in x]


def power_step(w: Mat, u: Vec) -> tuple[Vec, Vec, float]:
    """One step of Algorithm 1: v = W^T u / ||W^T u||, u = W v / ||W v||, sigma = u^T W v."""
    v = unit(matvec_t(w, u))
    wv = matvec(w, v)
    u = unit(wv)
    return u, v, sum(a * b for a, b in zip(u, wv))


class SpectralNorm:
    """Holds the persistent vector u of one layer. Each call does one power step and returns W / sigma."""

    def __init__(self, rows: int, rng: random.Random) -> None:
        self.u = unit([rng.gauss(0.0, 1.0) for _ in range(rows)])

    def normalize(self, w: Mat) -> tuple[Mat, float]:
        self.u, _, sigma = power_step(w, self.u)
        return [[a / sigma for a in row] for row in w], sigma


def jacobi_eigen(a: Mat, sweeps: int = 50) -> tuple[Vec, Mat]:
    """Eigenvalues and eigenvectors (as columns) of a small symmetric matrix by cyclic Jacobi rotations."""
    n = len(a)
    a = [row[:] for row in a]
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30:
            break
        for p in range(n - 1):
            for r in range(p + 1, n):
                if abs(a[p][r]) < 1e-300:
                    continue
                theta = (a[r][r] - a[p][p]) / (2 * a[p][r])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akr = a[k][p], a[k][r]
                    a[k][p], a[k][r] = c * akp - s * akr, s * akp + c * akr
                for k in range(n):
                    apk, ark = a[p][k], a[r][k]
                    a[p][k], a[r][k] = c * apk - s * ark, s * apk + c * ark
                for k in range(n):
                    qkp, qkr = q[k][p], q[k][r]
                    q[k][p], q[k][r] = c * qkp - s * qkr, s * qkp + c * qkr
    return [a[i][i] for i in range(n)], q


def top_singular(w: Mat) -> tuple[float, Vec, Vec]:
    """The exact largest singular value and its singular vectors u, v, from the eigenproblem of W^T W."""
    cols = len(w[0])
    wtw = [[sum(row[i] * row[j] for row in w) for j in range(cols)] for i in range(cols)]
    vals, vecs = jacobi_eigen(wtw)
    k = max(range(cols), key=lambda i: vals[i])
    v = [vecs[i][k] for i in range(cols)]
    wv = matvec(w, v)
    sigma = norm(wv)
    return sigma, [a / sigma for a in wv], v


def sn_weight_grad(w: Mat, grad_sn: Mat) -> Mat:
    """dL/dW for L(W / sigma(W)), given G = dL/dW_SN and a simple top singular value:
    dL/dW = (G - <G, W_SN> u v^T) / sigma, since d sigma / dW = u v^T."""
    sigma, u, v = top_singular(w)
    inner = sum(g * a / sigma for grow, wrow in zip(grad_sn, w) for g, a in zip(grow, wrow))
    return [[(grad_sn[i][j] - inner * u[i] * v[j]) / sigma for j in range(len(w[0]))] for i in range(len(w))]


def relu_net(ws: list[Mat], x: Vec) -> Vec:
    """x -> W_L relu(... relu(W_1 x)) with no biases."""
    h = x
    for k, w in enumerate(ws):
        h = matvec(w, h)
        if k < len(ws) - 1:
            h = [max(a, 0.0) for a in h]
    return h
