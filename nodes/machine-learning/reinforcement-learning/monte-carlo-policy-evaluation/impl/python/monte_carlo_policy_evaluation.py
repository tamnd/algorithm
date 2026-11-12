# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-policy-evaluation/. The authors are listed in prov/WSWCCF.jsonl.

"""Monte Carlo policy evaluation (first-visit and every-visit).

An episode is a list of pairs (S_t, R_(t+1)) for t = 0, ..., T - 1: the state
at time t and the reward that follows it. The terminal state is not listed.
Rewards and gamma may be ints, floats or fractions.Fraction.
"""

import random
from typing import Callable, Hashable, Iterable, Sequence

Episode = Sequence[tuple[Hashable, object]]


def mc_policy_evaluation(episodes: Iterable[Episode], gamma, first_visit: bool = True):
    """Return (V, N): the average return of each state and the number of returns averaged.

    With first_visit=True only the return after the first visit to a state in
    each episode counts; else every visit counts. A state that never occurs
    has no entry. Cost: O(T) time per episode of length T, O(number of states)
    memory besides one episode.
    """
    V: dict = {}
    N: dict = {}  # @line L1
    for ep in episodes:  # @line L2
        first = {}
        for t, (s, _) in enumerate(ep):  # @line L3
            first.setdefault(s, t)
        G = 0 * gamma  # @line L4
        for t in range(len(ep) - 1, -1, -1):  # @line L5
            s, r = ep[t]
            G = gamma * G + r  # @line L6
            if first_visit and first[s] < t:  # @line L7
                continue
            N[s] = N.get(s, 0) + 1  # @line L8
            v = V.get(s, 0 * G)
            V[s] = v + (G - v) / N[s]  # @line L9
    return V, N  # @line L10


def constant_alpha_mc(episodes: Iterable[Episode], gamma, alpha, v0=0, first_visit: bool = False):
    """Constant step size Monte Carlo: V(S_t) += alpha (G_t - V(S_t)) after each episode.

    The updates of one episode use the values from the start of the episode
    (offline), so the result does not depend on the order of the visits.
    """
    V: dict = {}
    for ep in episodes:
        first = {}
        for t, (s, _) in enumerate(ep):
            first.setdefault(s, t)
        G = 0 * gamma
        inc: dict = {}
        for t in range(len(ep) - 1, -1, -1):
            s, r = ep[t]
            G = gamma * G + r
            if first_visit and first[s] < t:
                continue
            inc[s] = inc.get(s, 0) + alpha * (G - V.get(s, v0))
        for s, d in inc.items():
            V[s] = V.get(s, v0) + d
    return V


def generate_episode(start, step: Callable, policy: Callable, rng: random.Random, max_steps: int = 10**6):
    """Run one episode and return it as a list of (S_t, R_(t+1)).

    policy(s, rng) returns an action; step(s, a, rng) returns (r, s2, done).
    """
    ep = []
    s = start
    for _ in range(max_steps):
        a = policy(s, rng)
        r, s2, done = step(s, a, rng)
        ep.append((s, r))
        if done:
            return ep
        s = s2
    raise RuntimeError("the episode did not end within max_steps")
