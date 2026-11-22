# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobian-saliency-map-attack/. The authors are listed in prov/NXJN7D.jsonl.

"""The Jacobian saliency map attack (JSMA) of Papernot et al. (2016), on synthetic models only.

This is the targeted version that increases features, picks pairs of features and uses
the Jacobian of the logits (the variant that Carlini and Wagner call JSMA-Z). The model
is given as two functions on an input: its logits and the Jacobian of the logits. The
tests build both from seeded affine models or seeded ReLU networks of mlkit. Nothing
here reads real data or touches a real system.
"""

import math
from typing import Callable, Optional, Sequence

Vector = list[float]
Logits = Callable[[Vector], Vector]
Jacobian = Callable[[Vector], list[Vector]]


def _argmax(z: Sequence[float]) -> int:
    return max(range(len(z)), key=lambda i: z[i])


def saliency_pair(jz: Sequence[Sequence[float]], target: int, domain: Sequence[int]) -> Optional[tuple[int, int]]:
    """The pair (p, q) of the search domain with the largest saliency, or None.

    For a pair, alpha is the sum over p and q of d z_target / d x_i, and beta is the sum
    over p and q of the derivatives of all other logits. A pair is allowed only when
    alpha > 0 and beta < 0, and its saliency is -alpha * beta. Ties go to the first pair
    in the order of the domain. Cost O(K d + |domain|^2).
    """
    a = [jz[target][i] for i in range(len(jz[0]))]
    b = [math.fsum(jz[j][i] for j in range(len(jz)) if j != target) for i in range(len(jz[0]))]
    best, best_s = None, 0.0
    for u in range(len(domain)):
        for v in range(u + 1, len(domain)):
            p, q = domain[u], domain[v]
            alpha, beta = a[p] + a[q], b[p] + b[q]
            if alpha > 0 and beta < 0 and -alpha * beta > best_s:
                best, best_s = (p, q), -alpha * beta
    return best


def jsma(logits: Logits, jac: Jacobian, x: Sequence[float], target: int, theta: float = 1.0,
         max_distortion: float = 1.0) -> tuple[Vector, bool, list[int]]:
    """Run the attack from x toward the class target.

    Each iteration adds theta to the two chosen features and clips them at 1; a chosen
    feature leaves the search domain. The number of changed features stays at most
    floor(max_distortion * d). Returns (the perturbed input, success, the changed
    features in the order of change). Preconditions: x in [0, 1]^d, theta > 0.
    Cost: one logits and one Jacobian call per iteration, and O(d^2) for the pair search.
    """
    xa = list(x)  # @line L1
    domain = [i for i in range(len(xa)) if xa[i] < 1.0]
    budget = math.floor(max_distortion * len(xa))  # @line L2
    changed: list[int] = []
    while _argmax(logits(xa)) != target and len(changed) + 2 <= budget and len(domain) >= 2:  # @line L3
        jz = jac(xa)  # @line L4
        pair = saliency_pair(jz, target, domain)  # @line L5
        if pair is None:  # @line L6
            break
        for i in pair:  # @line L7
            xa[i] = min(xa[i] + theta, 1.0)
            domain.remove(i)
            changed.append(i)
    return xa, _argmax(logits(xa)) == target, changed  # @line L8
