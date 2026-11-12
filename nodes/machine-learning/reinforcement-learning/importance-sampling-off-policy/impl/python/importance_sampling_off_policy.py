# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/importance-sampling-off-policy/. The authors are listed in prov/5BH86H.jsonl.

"""Off-policy evaluation of v_pi(s0) from episodes of a behavior policy mu by importance sampling.

An episode is a list of (state, action, reward) steps. pi(a, s) and mu(a, s) return action
probabilities. Three estimators: ordinary IS (unbiased), weighted IS (biased, consistent, lower
variance) and per-decision IS (unbiased, weights each reward only by the ratios before it).
With Fractions the estimates are exact.
"""

import random
from fractions import Fraction
from typing import Callable, Hashable, Sequence

Number = float | Fraction
Episode = Sequence[tuple[Hashable, Hashable, Number]]
Policy = Callable[[Hashable, Hashable], Number]


def off_policy_estimates(episodes: Sequence[Episode], pi: Policy, mu: Policy, gamma: Number = 1) -> tuple[Number, Number, Number]:
    """Return (ordinary IS, weighted IS, per-decision IS) estimates of v_pi(s0).

    Weighted IS is 0 when every ratio is 0. O(total number of steps) time, O(1) memory.
    """
    n = s_ord = s_w = s_pd = 0  # @line L1
    for episode in episodes:  # @line L2
        rho, g, g_pd, disc = 1, 0, 0, 1  # @line L3
        for s, a, r in episode:  # @line L4
            rho = rho * pi(a, s) / mu(a, s)  # @line L5
            g, g_pd, disc = g + disc * r, g_pd + disc * rho * r, disc * gamma  # @line L6
        n, s_ord, s_w, s_pd = n + 1, s_ord + rho * g, s_w + rho, s_pd + g_pd  # @line L7
    return s_ord / n, (s_ord / s_w if s_w != 0 else 0 * s_ord), s_pd / n  # @line L8


Step = Callable[[Hashable, Hashable], Sequence[tuple[Number, Number, Hashable | None]]]


def episode_distribution(step: Step, policy: Policy, actions: Sequence, s0: Hashable, max_len: int) -> list[tuple[Number, list]]:
    """All episodes from s0 of at most max_len steps, with their probabilities under `policy`.

    step(s, a) lists (probability, reward, next state or None for the end). Episodes still running
    after max_len steps are dropped, so the probabilities sum to 1 only for a finite horizon.
    """
    out = []
    frontier = [(1, [], s0)]
    for _ in range(max_len):
        nxt = []
        for prob, ep, s in frontier:
            for a in actions:
                pa = policy(a, s)
                if pa == 0:
                    continue
                for pt, r, s2 in step(s, a):
                    item = (prob * pa * pt, ep + [(s, a, r)], s2)
                    (out.append(item[:2]) if s2 is None else nxt.append(item))
        frontier = nxt
    return out


def sample_episode(step: Step, policy: Policy, actions: Sequence, s0: Hashable, rng: random.Random, max_len: int = 10**6) -> list:
    """One episode of `policy` from s0."""
    ep, s = [], s0
    for _ in range(max_len):
        a = rng.choices(list(actions), weights=[float(policy(b, s)) for b in actions])[0]
        outcomes = step(s, a)
        _, r, s2 = outcomes[rng.choices(range(len(outcomes)), weights=[float(o[0]) for o in outcomes])[0]]
        ep.append((s, a, r))
        if s2 is None:
            return ep
        s = s2
    return ep


def example_5_5_step(s, a):
    """Sutton and Barto, Example 5.5: one state. 'left' returns with probability 0.9 (reward 0) or
    ends with reward +1 (probability 0.1); 'right' ends with reward 0."""
    if a == "left":
        return [(Fraction(9, 10), 0, s), (Fraction(1, 10), 1, None)]
    return [(Fraction(1), 0, None)]
