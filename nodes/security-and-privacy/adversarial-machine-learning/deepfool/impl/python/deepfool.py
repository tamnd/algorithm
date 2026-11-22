# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deepfool/. The authors are listed in prov/A515G9.jsonl.

"""DeepFool of Moosavi-Dezfooli, Fawzi and Frossard (2016), multi-class l2 version, on synthetic models only.

The model is given as two functions on an input: its logits and the Jacobian of the
logits. The tests build both from a seeded affine model or a seeded two-layer ReLU
network of mlkit. Nothing here reads real data or touches a real system.
"""

import math
from typing import Callable, Sequence

Vector = list[float]
Logits = Callable[[Vector], Vector]
Jacobian = Callable[[Vector], list[Vector]]


def _argmax(z: Sequence[float]) -> int:
    return max(range(len(z)), key=lambda i: z[i])


def nearest_boundary_step(z: Sequence[float], jz: Sequence[Sequence[float]], k0: int) -> Vector:
    """The l2 step to the nearest boundary of the linearized classifier at the current point.

    For each class k != k0, w_k = grad z_k - grad z_k0 and f_k = z_k - z_k0. The step is
    (|f_l| / ||w_l||^2) w_l for the class l that minimizes |f_l| / ||w_l||. Cost O(K d).
    """
    best_l, best_ratio = -1, math.inf
    for k in range(len(z)):
        if k == k0:
            continue
        wk = [a - b for a, b in zip(jz[k], jz[k0])]
        nk = math.sqrt(math.fsum(t * t for t in wk))
        if nk == 0.0:
            continue
        ratio = abs(z[k] - z[k0]) / nk
        if ratio < best_ratio:
            best_l, best_ratio, best_w, best_n = k, ratio, wk, nk
    if best_l < 0:
        return [0.0] * len(jz[0])
    c = (abs(z[best_l] - z[k0]) + 1e-12) / (best_n * best_n)
    return [c * t for t in best_w]


def deepfool(logits: Logits, jac: Jacobian, x: Sequence[float], overshoot: float = 0.02,
             max_iter: int = 50) -> tuple[Vector, int]:
    """Run DeepFool from x. Returns (the perturbed input, the number of iterations).

    The perturbation is r = (1 + overshoot) * the sum of the steps; the returned input is
    clip01(x + r). The loop stops when the label differs from the label of x, or after
    max_iter iterations, and then the label may still be the same. Precondition:
    overshoot >= 0. Cost: one logits and one Jacobian call per iteration, and O(K d) more.
    """
    k0 = _argmax(logits(list(x)))  # @line L1
    r = [0.0] * len(x)
    for it in range(max_iter + 1):  # @line L2
        p = [min(max(a + (1.0 + overshoot) * t, 0.0), 1.0) for a, t in zip(x, r)]  # @line L3
        z = logits(p)
        if _argmax(z) != k0 or it == max_iter:  # @line L4
            return p, it
        jz = jac(p)  # @line L5
        step = nearest_boundary_step(z, jz, k0)  # @line L6
        r = [a + b for a, b in zip(r, step)]  # @line L7
    return p, max_iter  # @line L8
