# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lsqr/. The authors are listed in prov/BNV7VJ.jsonl.
"""LSQR of Paige and Saunders for min ||y - A x|| with noisy data y.

Golub-Kahan bidiagonalization builds orthonormal bases U_{k+1} and V_k with
A V_k = U_{k+1} B_k, where B_k is lower bidiagonal of size (k+1) x k. LSQR
solves the small problem min ||beta_1 e_1 - B_k z|| by Givens rotations,
one per step, and updates x_k = V_k z_k with a short recurrence. In exact
arithmetic x_k is the CGLS iterate. The rotations also give the residual
norm ||y - A x_k|| = |phibar_k| at no extra cost, so the discrepancy
principle needs no extra product with A.

reorth=True keeps the U and V vectors and orthogonalizes each new vector
against all old ones (two passes). This costs O(k (m + n)) per step but
removes the loss of orthogonality that rounding causes.
"""

import math
from typing import Callable, List, Optional, Sequence

from imgla import matvec, rmatvec

Vector = List[float]
Operator = Callable[[Sequence[float]], Vector]


def _norm(v: Sequence[float]) -> float:
    return math.sqrt(sum(t * t for t in v))


def _reorth(w: Vector, basis: List[Vector]) -> Vector:
    for _ in range(2):
        for b in basis:
            h = sum(p * q for p, q in zip(b, w))
            w = [p - h * q for p, q in zip(w, b)]
    return w


class LSQRResult:
    """x: the last iterate; k: steps done; iterates: x_0, ..., x_k; resnorms:
    |phibar_j| = ||y - A x_j|| (in exact arithmetic) for j = 0, ..., k; alphas and
    betas: the bidiagonal entries alpha_1, ... and beta_1, ...; us, vs: the
    Lanczos vectors (kept only with keep=True or reorth=True); stopped:
    "discrepancy", "breakdown" or "maxit"."""

    def __init__(self, **kw: object) -> None:
        self.__dict__.update(kw)


def lsqr(apply_a: Operator, apply_at: Operator, y: Sequence[float], kmax: int,
         delta: Optional[float] = None, tau: float = 1.01, reorth: bool = False,
         keep: bool = False) -> LSQRResult:
    """Run at most kmax LSQR steps from x_0 = 0.

    Precondition: apply_at is the adjoint of apply_a. If delta is given, stop
    at the first k with |phibar_k| <= tau delta. Cost: per step one product
    with A, one with A^T and O(m + n) more, plus O(k (m + n)) with reorth.
    """
    beta = _norm(y)
    u = [t / beta for t in y] if beta > 0 else [0.0] * len(y)
    v = apply_at(u)
    alpha = _norm(v)
    v = [t / alpha for t in v] if alpha > 0 else v
    w = list(v)
    x = [0.0] * len(v)
    phibar, rhobar = beta, alpha  # @line L1
    store = reorth or keep
    us, vs = ([u], [v]) if store else ([], [])
    alphas, betas = [alpha], [beta]
    iterates, resnorms = [list(x)], [abs(phibar)]
    stopped, k = "maxit", 0
    if delta is not None and abs(phibar) <= tau * delta:
        stopped = "discrepancy"
    elif alpha == 0 or beta == 0:
        stopped = "breakdown"
    while stopped == "maxit" and k < kmax:  # @line L2
        k += 1
        u = [p - alpha * q for p, q in zip(apply_a(v), u)]
        if reorth:
            u = _reorth(u, us)
        beta = _norm(u)
        u = [t / beta for t in u] if beta > 0 else [0.0] * len(u)  # @line L3
        v = [p - beta * q for p, q in zip(apply_at(u), v)]
        if reorth:
            v = _reorth(v, vs)
        alpha = _norm(v)
        v = [t / alpha for t in v] if alpha > 0 else [0.0] * len(v)  # @line L4
        rho = math.hypot(rhobar, beta)
        c, s = rhobar / rho, beta / rho  # @line L5
        theta = s * alpha
        rhobar = -c * alpha
        phi = c * phibar
        phibar = s * phibar  # @line L6
        x = [xi + (phi / rho) * wi for xi, wi in zip(x, w)]
        w = [vi - (theta / rho) * wi for vi, wi in zip(v, w)]  # @line L7
        if store:
            us.append(u)
            vs.append(v)
        alphas.append(alpha)
        betas.append(beta)
        iterates.append(list(x))
        resnorms.append(abs(phibar))
        if delta is not None and abs(phibar) <= tau * delta:  # @line L8
            stopped = "discrepancy"
        elif alpha == 0 or beta == 0:
            stopped = "breakdown"
    return LSQRResult(x=x, k=k, iterates=iterates, resnorms=resnorms, alphas=alphas,  # @line L9
                      betas=betas, us=us, vs=vs, stopped=stopped)


def lsqr_matrix(a: List[List[float]], y: Sequence[float], kmax: int, delta: Optional[float] = None,
                tau: float = 1.01, reorth: bool = False, keep: bool = False) -> LSQRResult:
    """LSQR for a dense matrix A (a list of rows). Cost: O(m n) per step."""
    return lsqr(lambda x: matvec(a, x), lambda r: rmatvec(a, r), y, kmax,
                delta=delta, tau=tau, reorth=reorth, keep=keep)
