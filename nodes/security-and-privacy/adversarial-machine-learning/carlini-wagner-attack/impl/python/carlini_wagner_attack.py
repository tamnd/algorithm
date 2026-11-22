# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carlini-wagner-attack/. The authors are listed in prov/2XQ46N.jsonl.

"""The l2 attack of Carlini and Wagner (2017), on synthetic models only.

The model is given as two functions on an input in [0, 1]^d: its logits and the
Jacobian of the logits. The tests build both from a seeded linear model or a seeded
two-layer ReLU network of mlkit. Nothing here reads real data or touches a real system.
"""

import math
from typing import Callable, Sequence

Vector = list[float]
Logits = Callable[[Vector], Vector]
Jacobian = Callable[[Vector], list[Vector]]


def margin(z: Sequence[float], y: int, kappa: float) -> tuple[float, int]:
    """The untargeted loss f = max(z_y - max_{i != y} z_i, -kappa), and the best other class."""
    j = max((i for i in range(len(z)) if i != y), key=lambda i: z[i])
    return max(z[y] - z[j], -kappa), j


def to_box(w: Sequence[float]) -> Vector:
    """The change of variables x' = (tanh(w) + 1) / 2, which maps R^d onto (0, 1)^d."""
    return [(math.tanh(a) + 1.0) / 2.0 for a in w]


def from_box(x: Sequence[float]) -> Vector:
    """The inverse map w = artanh(2 x - 1), with 2 x - 1 kept inside (-1, 1)."""
    lim = 1.0 - 1e-9
    return [math.atanh(min(max(2.0 * a - 1.0, -lim), lim)) for a in x]


def objective_gradient(logits: Logits, jac: Jacobian, x: Sequence[float], w: Sequence[float], y: int,
                       c: float, kappa: float) -> tuple[float, Vector]:
    """Value and w-gradient of ||x' - x||_2^2 + c f(x') with x' = to_box(w)."""
    xp = to_box(w)
    z = logits(xp)
    f, j = margin(z, y, kappa)
    dist2 = math.fsum((a - b) ** 2 for a, b in zip(xp, x))
    gx = [2.0 * (a - b) for a, b in zip(xp, x)]
    if f > -kappa:  # the max is not clamped, so f = z_y - z_j locally
        jz = jac(xp)
        gx = [g + c * (jz[y][i] - jz[j][i]) for i, g in enumerate(gx)]
    gw = [g * (1.0 - math.tanh(a) ** 2) / 2.0 for g, a in zip(gx, w)]
    return dist2 + c * f, gw


def carlini_wagner_attack(logits: Logits, jac: Jacobian, x: Sequence[float], y: int, c: float = 0.1,
                          kappa: float = 0.0, steps: int = 100, lr: float = 0.05,
                          search_steps: int = 6) -> Vector | None:
    """Smallest l2 adversarial input found by the C&W l2 attack, or None.

    An input x' counts as adversarial when argmax logits(x') != y and the best other
    logit is at least kappa above the logit of y (for kappa = 0 a wrong label is enough,
    with ties going to the first index). The weight c of the
    loss is set by binary search: up when a round fails, down when it succeeds.
    Each round runs Adam on w from the start w = artanh(2 x - 1).
    Precondition: x in [0, 1]^d and argmax logits(x) == y. Cost: search_steps * steps
    evaluations of logits and jac, and O(search_steps * steps * d) more.
    """
    lo, hi = 0.0, math.inf  # @line L1
    best: Vector | None = None
    best_d = math.inf
    for _ in range(search_steps):  # @line L2
        w = from_box(x)  # @line L3
        mom, vel = [0.0] * len(x), [0.0] * len(x)
        success = False
        for t in range(1, steps + 1):  # @line L4
            xp = to_box(w)  # @line L5
            z = logits(xp)
            gap = max(z[i] for i in range(len(z)) if i != y) - z[y]
            if max(range(len(z)), key=lambda i: z[i]) != y and gap >= kappa:  # @line L6
                success = True
                dist = math.dist(xp, x)
                if dist < best_d:
                    best, best_d = xp, dist
            _, g = objective_gradient(logits, jac, x, w, y, c, kappa)  # @line L7
            mom = [0.9 * a + 0.1 * b for a, b in zip(mom, g)]
            vel = [0.999 * a + 0.001 * b * b for a, b in zip(vel, g)]
            mh, vh = 1.0 - 0.9 ** t, 1.0 - 0.999 ** t
            w = [a - lr * (mi / mh) / (math.sqrt(vi / vh) + 1e-12) for a, mi, vi in zip(w, mom, vel)]
        if success:  # @line L8
            hi = c
        else:
            lo = c
        c = (lo + hi) / 2.0 if hi < math.inf else 10.0 * c  # @line L9
    return best  # @line L10
