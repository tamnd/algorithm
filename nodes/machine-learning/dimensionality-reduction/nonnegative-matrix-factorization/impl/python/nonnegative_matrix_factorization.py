# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonnegative-matrix-factorization/. The authors are listed in prov/N3ZBGQ.jsonl.

"""Nonnegative matrix factorization by the multiplicative updates of Lee and Seung.

Given a nonnegative m x n matrix V and a rank r, find nonnegative W (m x r)
and H (r x n) with V close to W H. The Frobenius updates are

    H <- H * (W^T V) / (W^T W H),    W <- W * (V H^T) / (W H H^T),

element by element. Each update never increases ||V - W H||_F^2. The
Kullback-Leibler updates are also given.
"""

import random

Matrix = list[list[float]]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def transpose(a: Matrix) -> Matrix:
    return [list(r) for r in zip(*a)]


def frobenius_loss(v: Matrix, w: Matrix, h: Matrix) -> float:
    """||V - W H||_F^2."""
    wh = matmul(w, h)
    return sum((a - b) ** 2 for ra, rb in zip(v, wh) for a, b in zip(ra, rb))


def kl_loss(v: Matrix, w: Matrix, h: Matrix) -> float:
    """The generalized Kullback-Leibler divergence D(V || W H)."""
    import math
    wh = matmul(w, h)
    total = 0.0
    for ra, rb in zip(v, wh):
        for a, b in zip(ra, rb):
            total += (a * math.log(a / b) if a > 0 else 0.0) - a + b
    return total


def _mult(x: Matrix, num: Matrix, den: Matrix) -> Matrix:
    """x * num / den element by element. A zero denominator keeps the entry (then num is 0 too)."""
    return [[xv * nv / dv if dv > 0 else xv for xv, nv, dv in zip(rx, rn, rd)]
            for rx, rn, rd in zip(x, num, den)]


def update_h_frobenius(v: Matrix, w: Matrix, h: Matrix) -> Matrix:
    wt = transpose(w)
    return _mult(h, matmul(wt, v), matmul(matmul(wt, w), h))


def update_w_frobenius(v: Matrix, w: Matrix, h: Matrix) -> Matrix:
    ht = transpose(h)
    return _mult(w, matmul(v, ht), matmul(w, matmul(h, ht)))


def random_init(m: int, n: int, r: int, rng: random.Random, scale: float = 1.0) -> tuple[Matrix, Matrix]:
    w = [[rng.uniform(0.1, 1.0) * scale for _ in range(r)] for _ in range(m)]
    h = [[rng.uniform(0.1, 1.0) * scale for _ in range(n)] for _ in range(r)]
    return w, h


def nmf(v: Matrix, r: int, rng: random.Random, iters: int = 500, tol: float = 0.0,
        init: tuple[Matrix, Matrix] | None = None) -> tuple[Matrix, Matrix, list[float]]:
    """Frobenius NMF. Return (W, H, the loss after each full iteration, starting with the initial loss)."""
    if any(x < 0 for row in v for x in row):
        raise ValueError("V must be nonnegative")
    m, n = len(v), len(v[0])
    w, h = init if init is not None else random_init(m, n, r, rng)  # @line L1
    w, h = [row[:] for row in w], [row[:] for row in h]
    losses = [frobenius_loss(v, w, h)]
    for _ in range(iters):  # @line L2
        h = update_h_frobenius(v, w, h)  # @line L3
        w = update_w_frobenius(v, w, h)  # @line L4
        losses.append(frobenius_loss(v, w, h))
        if losses[-2] - losses[-1] <= tol * losses[-2]:  # @line L5
            break
    return w, h, losses  # @line L6


def update_h_kl(v: Matrix, w: Matrix, h: Matrix) -> Matrix:
    wh = matmul(w, h)
    ratio = [[a / b if b > 0 else 0.0 for a, b in zip(ra, rb)] for ra, rb in zip(v, wh)]
    num = matmul(transpose(w), ratio)
    colsum = [sum(w[i][a] for i in range(len(w))) for a in range(len(w[0]))]
    den = [[colsum[a]] * len(h[0]) for a in range(len(h))]
    return _mult(h, num, den)


def update_w_kl(v: Matrix, w: Matrix, h: Matrix) -> Matrix:
    return transpose(update_h_kl(transpose(v), transpose(h), transpose(w)))


def nmf_kl(v: Matrix, r: int, rng: random.Random, iters: int = 500) -> tuple[Matrix, Matrix, list[float]]:
    """KL-divergence NMF with the multiplicative updates. Return (W, H, losses)."""
    m, n = len(v), len(v[0])
    w, h = random_init(m, n, r, rng)
    losses = [kl_loss(v, w, h)]
    for _ in range(iters):
        h = update_h_kl(v, w, h)
        w = update_w_kl(v, w, h)
        losses.append(kl_loss(v, w, h))
    return w, h, losses
