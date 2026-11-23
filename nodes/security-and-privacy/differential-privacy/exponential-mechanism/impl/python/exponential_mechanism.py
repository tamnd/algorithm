# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-mechanism/. The authors are listed in prov/T51N2F.jsonl.
"""The exponential mechanism of McSherry and Talwar.

It picks a candidate r with probability proportional to
exp(epsilon u(x, r) / (c Delta)), where Delta is the sensitivity of the
utility u and c = 2 in general. When u is monotone in the data (one step to a
neighbor moves every utility in the same direction), c = 1 is enough.

The scores are shifted by their maximum before exp, so large utilities do
not overflow. Floats and random.Random are used so that the tests are
reproducible; a deployment needs a cryptographic source of randomness and an
exact sampler.
"""

from __future__ import annotations

import math
import random
from typing import Callable, Hashable, Sequence, TypeVar

X = TypeVar("X")
R = TypeVar("R", bound=Hashable)


def _scores(x: X, candidates: Sequence[R], u: Callable[[X, R], float], sensitivity: float, epsilon: float, monotone: bool) -> list[float]:
    if not candidates:
        raise ValueError("need at least one candidate")
    if sensitivity <= 0 or epsilon <= 0:
        raise ValueError("need sensitivity > 0 and epsilon > 0")
    c = 1.0 if monotone else 2.0
    return [epsilon * u(x, r) / (c * sensitivity) for r in candidates]


def exponential_mechanism(
    x: X,
    candidates: Sequence[R],
    u: Callable[[X, R], float],
    sensitivity: float,
    epsilon: float,
    rng: random.Random,
    monotone: bool = False,
) -> R:
    """Sample r with probability proportional to exp(epsilon u(x, r) / (c Delta)).

    Precondition: a nonempty candidate list, Delta >= the sensitivity of u in
    the data for every r, and epsilon > 0. Use monotone=True only if u is
    monotone in the data under the chosen neighbor relation.
    Cost: O(|R|) evaluations of u and O(|R|) other operations.
    """
    if not candidates:
        raise ValueError("need at least one candidate")
    if sensitivity <= 0 or epsilon <= 0:
        raise ValueError("need sensitivity > 0 and epsilon > 0")
    c = 1.0 if monotone else 2.0  # @line L1
    s = [epsilon * u(x, r) / (c * sensitivity) for r in candidates]  # @line L2
    m = max(s)  # @line L3
    w = [math.exp(si - m) for si in s]  # @line L4
    total = sum(w)  # @line L5
    t = rng.random() * total  # @line L6
    for r, wr in zip(candidates, w):  # @line L7
        t -= wr  # @line L8
        if t < 0:  # @line L9
            return r
    return candidates[-1]  # @line L10


def exponential_pmf(
    x: X,
    candidates: Sequence[R],
    u: Callable[[X, R], float],
    sensitivity: float,
    epsilon: float,
    monotone: bool = False,
) -> dict[R, float]:
    """The output pmf of exponential_mechanism, in floats. Cost: O(|R|)."""
    s = _scores(x, candidates, u, sensitivity, epsilon, monotone)
    m = max(s)
    w = [math.exp(si - m) for si in s]
    total = sum(w)
    out: dict[R, float] = {}
    for r, wr in zip(candidates, w):
        out[r] = out.get(r, 0.0) + wr / total
    return out


def utility_threshold(opt: float, sensitivity: float, epsilon: float, n_candidates: int, t: float, monotone: bool = False) -> float:
    """OPT - (c Delta / epsilon)(ln |R| + t); the output falls below it with probability at most e^(-t)."""
    c = 1.0 if monotone else 2.0
    return opt - c * sensitivity / epsilon * (math.log(n_candidates) + t)
