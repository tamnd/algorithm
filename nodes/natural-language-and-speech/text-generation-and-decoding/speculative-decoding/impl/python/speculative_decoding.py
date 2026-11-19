# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/speculative-decoding/. The authors are listed in prov/K824EJ.jsonl.

"""Speculative decoding (Leviathan, Kalman and Matias 2023; Chen et al. 2023).

The target model p and the draft model q are functions that take a prefix
(a tuple of strings) and return a dict from each token to its probability.
The end token is the string "</s>". The code takes these distributions as
given; it does not run or train a network. One call of the target on
gamma + 1 prefixes stands for the one parallel forward pass of a real
system, and is counted as one target call.
"""

import random
from typing import Callable, Dict, List, Optional, Tuple

EOS = "</s>"

Dist = Dict[str, float]
Model = Callable[[Tuple[str, ...]], Dist]


def sample(dist: Dist, rng: random.Random) -> str:
    """Draw a token from dist (weights that need not sum to 1), by the cumulative sum."""
    total = sum(dist.values())
    u = rng.random() * total
    acc = 0.0
    last = None
    for w, pw in dist.items():
        if pw <= 0:
            continue
        acc += pw
        last = w
        if u < acc:
            return w
    if last is None:
        raise ValueError("every weight is zero")
    return last


def residual(p: Dist, q: Dist) -> Dist:
    """Return max(0, p - q), normalized. If p and q are equal, return p."""
    r = {w: max(0, p[w] - q.get(w, 0)) for w in p}
    total = sum(r.values())
    if total == 0:
        return dict(p)
    return {w: v / total for w, v in r.items()}


def speculative_step(
    prefix: Tuple[str, ...],
    target: Model,
    draft: Model,
    gamma: int,
    rng: random.Random,
    room: int,
    stats: Optional[Dict[str, int]] = None,
) -> List[str]:
    """Return the 1 to gamma + 1 tokens that one step appends to prefix.

    At most room tokens are returned. The draft proposes up to
    min(gamma, room - 1) tokens and stops after "</s>".
    """
    g = min(gamma, room - 1)
    xs: List[str] = []
    qs: List[Dist] = []
    for _ in range(g):  # @line L1
        q = draft(prefix + tuple(xs))
        x = sample(q, rng)  # @line L2
        xs.append(x)
        qs.append(q)
        if x == EOS:
            break
    ended = bool(xs) and xs[-1] == EOS
    ps = [target(prefix + tuple(xs[:i])) for i in range(len(xs) + (0 if ended else 1))]  # @line L3
    if stats is not None:
        stats["target_calls"] = stats.get("target_calls", 0) + 1
        stats["draft_calls"] = stats.get("draft_calls", 0) + len(xs)
        stats["drafted"] = stats.get("drafted", 0) + len(xs)
    for i, x in enumerate(xs):  # @line L4
        r = rng.random()  # @line L5
        if stats is not None:
            stats["tried"] = stats.get("tried", 0) + 1
        if r * qs[i][x] < ps[i].get(x, 0):  # @line L6
            if stats is not None:
                stats["accepted"] = stats.get("accepted", 0) + 1
            continue
        return xs[:i] + [sample(residual(ps[i], qs[i]), rng)]  # @line L7
    if ended:  # @line L8
        return xs
    return xs + [sample(ps[len(xs)], rng)]  # @line L9


def speculative_decode(
    target: Model,
    draft: Model,
    gamma: int,
    max_len: int,
    rng: random.Random,
    stats: Optional[Dict[str, int]] = None,
) -> List[str]:
    """Return an output of at most max_len tokens, distributed as a sample of the target."""
    if gamma < 0 or max_len < 1:
        raise ValueError("gamma must be at least 0 and max_len at least 1")
    y: List[str] = []
    while len(y) < max_len and (not y or y[-1] != EOS):
        y += speculative_step(tuple(y), target, draft, gamma, rng, max_len - len(y), stats)
    return y


def expected_tokens_per_step(alpha: float, gamma: int) -> float:
    """Return (1 - alpha^(gamma + 1)) / (1 - alpha), the mean tokens per target call.

    This holds when every draft token is accepted with the same probability
    alpha, independently of the others.
    """
    if alpha == 1:
        return gamma + 1
    return (1 - alpha ** (gamma + 1)) / (1 - alpha)


def acceptance_rate(p: Dist, q: Dist) -> float:
    """Return alpha = sum over w of min(p(w), q(w))."""
    return sum(min(p[w], q.get(w, 0)) for w in p)
