# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-adversarial-perturbation/. The authors are listed in prov/NQDGS5.jsonl.

"""The universal perturbation algorithm of Moosavi-Dezfooli et al. (2017), on synthetic models only.

One perturbation v with ||v||_p <= epsilon is grown over a data set, so that the label of
clip01(x + v) differs from the label of x for many x. The inner step is a small DeepFool.
The model is given as its logits and the Jacobian of its logits; the tests build both
from seeded affine models and seeded ReLU networks of mlkit. Nothing here reads real
data or touches a real system.
"""

import math
from typing import Callable, Sequence

import mlkit as m

Vector = list[float]
Logits = Callable[[Vector], Vector]
Jacobian = Callable[[Vector], list[Vector]]


def project_ball(v: Sequence[float], epsilon: float, norm: str) -> Vector:
    """Projection onto the ball of radius epsilon around 0, in the l2 or the l_infinity norm. Cost O(d)."""
    zero = [0.0] * len(v)
    if norm == "inf":
        return m.project_linf(v, zero, epsilon)
    return m.project_l2(v, zero, epsilon)


def minimal_step(logits: Logits, jac: Jacobian, p: Sequence[float], label: int, overshoot: float = 0.02,
                 max_iter: int = 10) -> Vector:
    """A DeepFool step r so that the label of clip01(p + r) differs from label, or the best try.

    Each iteration moves to the nearest boundary of the linearized model. The total step
    is scaled by 1 + overshoot. Cost: at most max_iter logits and Jacobian calls.
    """
    r = [0.0] * len(p)
    for _ in range(max_iter):
        q = m.clip01([a + (1.0 + overshoot) * t for a, t in zip(p, r)])
        z = logits(q)
        if m.argmax(z) != label:
            break
        jz = jac(q)
        best, best_ratio = None, math.inf
        for k in range(len(z)):
            if k == label:
                continue
            wk = m.sub(jz[k], jz[label])
            nk = m.norm2(wk)
            if nk > 0.0 and abs(z[k] - z[label]) / nk < best_ratio:
                best, best_ratio = (k, wk, nk), abs(z[k] - z[label]) / nk
        if best is None:
            break
        k, wk, nk = best
        r = m.add(r, m.scale((abs(z[k] - z[label]) + 1e-12) / (nk * nk), wk))
    return m.scale(1.0 + overshoot, r)


def fooling_rate(logits: Logits, data: Sequence[Sequence[float]], v: Sequence[float]) -> float:
    """Fraction of the points x of data whose label at clip01(x + v) differs from the label at x."""
    if not data:
        return 0.0
    fooled = sum(1 for x in data if m.argmax(logits(m.clip01(m.add(x, v)))) != m.argmax(logits(list(x))))
    return fooled / len(data)


def universal_perturbation(logits: Logits, jac: Jacobian, data: Sequence[Sequence[float]], epsilon: float,
                           norm: str = "2", target_rate: float = 0.8, max_passes: int = 10) -> tuple[Vector, float]:
    """Grow one perturbation over data. Returns (v, the fooling rate of v on data).

    The loop stops when the fooling rate reaches target_rate or after max_passes passes
    over the data. Preconditions: epsilon >= 0, norm is "2" or "inf", data is not empty.
    Cost per pass: n label calls and at most n DeepFool runs.
    """
    v = [0.0] * len(data[0])  # @line L1
    rate = 0.0
    for _ in range(max_passes):  # @line L2
        for x in data:  # @line L3
            label = m.argmax(logits(list(x)))
            p = m.clip01(m.add(x, v))
            if m.argmax(logits(p)) == label:  # @line L4
                r = minimal_step(logits, jac, p, label)  # @line L5
                v = project_ball(m.add(v, r), epsilon, norm)  # @line L6
        rate = fooling_rate(logits, data, v)  # @line L7
        if rate >= target_rate:  # @line L8
            break
    return v, rate  # @line L9
