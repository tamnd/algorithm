# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gibbs-sampling/. The authors are listed in prov/JKAGEE.jsonl.

import itertools
import random
from fractions import Fraction
from typing import Callable, Hashable, Sequence

State = tuple
Weight = Callable[[Sequence[Hashable]], float]


def gibbs_sampling(
    weight: Weight,
    domains: Sequence[Sequence[Hashable]],
    x0: Sequence[Hashable],
    n_steps: int,
    rng: random.Random,
    scan: str = "systematic",
) -> list[State]:
    """Run Gibbs sampling on a finite product space and return the states X_1..X_T.

    weight(x) >= 0 is the unnormalized target; domains[i] lists the values of x_i.
    scan is "systematic" (one sweep per step) or "random" (one coordinate per step).
    Precondition: weight(x0) > 0. Cost: per step, sum of |D_i| over the updated i weight calls.
    """
    if scan not in ("systematic", "random"):
        raise ValueError("scan must be 'systematic' or 'random'")
    x = list(x0)  # @line L1
    if not weight(x) > 0:
        raise ValueError("x0 must have positive weight")
    d = len(domains)
    chain: list[State] = []
    for _ in range(n_steps):  # @line L2
        if scan == "systematic":
            order: Sequence[int] = range(d)  # @line L3
        else:
            order = (rng.randrange(d),)  # @line L4
        for i in order:  # @line L5
            ws = []
            for v in domains[i]:
                x[i] = v
                ws.append(weight(x))
            u = rng.random() * sum(ws)
            new = None
            acc = 0.0
            for v, w in zip(domains[i], ws):  # @line L6
                if w > 0:
                    new = v  # the last value of positive weight guards against rounding
                    acc += w
                    if u < acc:
                        break
            x[i] = new  # @line L7
        chain.append(tuple(x))  # @line L8
    return chain  # @line L9


def transition_matrix(
    weight: Callable[[Sequence[Hashable]], Fraction],
    domains: Sequence[Sequence[Hashable]],
    scan: str = "systematic",
) -> tuple[list[State], list[list[Fraction]]]:
    """Exact kernel of one step on the states of positive weight, with Fractions."""
    states = [s for s in itertools.product(*domains) if weight(s) > 0]
    index = {s: k for k, s in enumerate(states)}
    n, d = len(states), len(domains)

    def single(i: int) -> list[list[Fraction]]:
        k = [[Fraction(0)] * n for _ in range(n)]
        for s in states:
            cands = [s[:i] + (v,) + s[i + 1:] for v in domains[i]]
            tot = sum(weight(c) for c in cands)
            for c in cands:
                if weight(c) > 0:
                    k[index[s]][index[c]] += weight(c) / tot
        return k

    ks = [single(i) for i in range(d)]
    if scan == "random":
        return states, [[sum(k[a][b] for k in ks) / d for b in range(n)] for a in range(n)]
    p = ks[0]
    for k in ks[1:]:
        p = [[sum(p[a][c] * k[c][b] for c in range(n)) for b in range(n)] for a in range(n)]
    return states, p
