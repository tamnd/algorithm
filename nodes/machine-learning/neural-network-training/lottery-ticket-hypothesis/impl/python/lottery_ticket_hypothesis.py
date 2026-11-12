# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lottery-ticket-hypothesis/. The authors are listed in prov/66QJ8T.jsonl.

"""Iterative magnitude pruning (IMP) with rewinding, the procedure of Frankle and Carbin.

The model is given by a gradient function grad_fn(theta) -> list. Training is
plain gradient descent on the masked weights: after each step the pruned
weights are set to 0 again, so they stay at 0.

Round r of IMP:
  1. train the masked network from the rewind point,
  2. remove the given fraction of the remaining weights with the smallest
     magnitude after training,
  3. reset the remaining weights to their values at the rewind point.
rewind = 0 is the original procedure (reset to the initialization);
rewind = j > 0 resets to iteration j of the first dense run (Frankle et al. 2020).
"""

from fractions import Fraction
from typing import Callable, List, Sequence, Tuple

Vector = List[float]


def masked_gd(theta: Sequence[float], mask: Sequence[int], grad_fn: Callable, eta: float, steps: int) -> List[Vector]:
    """Gradient descent on the weights where mask = 1. Returns all iterates theta_0..theta_steps."""
    t = [a * m for a, m in zip(theta, mask)]
    out = [t]
    for _ in range(steps):
        g = grad_fn(t)
        t = [(a - eta * b) * m for a, b, m in zip(t, g, mask)]
        out.append(t)
    return out


def prune_count(alive: int, rate: Fraction) -> int:
    """The number of weights to remove in one round: floor(rate * alive)."""
    return int(Fraction(rate) * alive)


def magnitude_prune(theta: Sequence[float], mask: Sequence[int], rate: Fraction) -> List[int]:
    """Remove floor(rate * alive) of the alive weights with the smallest |theta|. Ties break by index."""
    alive = [i for i, m in enumerate(mask) if m]
    k = prune_count(len(alive), rate)
    order = sorted(alive, key=lambda i: (abs(theta[i]), i))
    new = list(mask)
    for i in order[:k]:
        new[i] = 0
    return new


def imp(theta0: Sequence[float], grad_fn: Callable, rounds: int, rate: Fraction, eta: float, steps: int,
        rewind: int = 0) -> Tuple[List[int], Vector, List[dict]]:
    """Iterative magnitude pruning with rewinding to iteration `rewind` of the dense run.

    Returns the final mask, the weights of the last trained ticket, and one
    record per round with the mask, the start point and the trained weights.
    """
    if not 0 <= rewind <= steps:
        raise ValueError("rewind must be in [0, steps]")
    mask = [1] * len(theta0)
    dense = masked_gd(theta0, mask, grad_fn, eta, steps)
    anchor = dense[rewind]
    trained = dense[-1]
    history = [{"mask": mask, "start": list(theta0), "trained": trained}]
    for _ in range(rounds):
        mask = magnitude_prune(trained, mask, rate)
        start = [a * m for a, m in zip(anchor, mask)]
        trained = masked_gd(start, mask, grad_fn, eta, steps - rewind)[-1]
        history.append({"mask": mask, "start": start, "trained": trained})
    return mask, trained, history


def random_mask(size: int, keep: int, rng) -> List[int]:
    """A random mask with exactly `keep` ones: the random pruning baseline."""
    idx = set(rng.sample(range(size), keep))
    return [1 if i in idx else 0 for i in range(size)]


def least_squares(xs: Sequence[Sequence[float]], ys: Sequence[float]):
    """Loss (1/2n) ||X theta - y||^2 and its gradient, for a linear model."""
    n = len(xs)

    def residual(theta):
        return [sum(a * b for a, b in zip(row, theta)) - y for row, y in zip(xs, ys)]

    def loss(theta):
        return sum(r * r for r in residual(theta)) / (2 * n)

    def grad(theta):
        r = residual(theta)
        return [sum(xs[i][j] * r[i] for i in range(n)) / n for j in range(len(theta))]

    return loss, grad
