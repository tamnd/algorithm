# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/td-lambda/. The authors are listed in prov/8STJSN.jsonl.

"""Tabular TD(lambda): the backward view with accumulating traces, and the
forward view (the offline lambda-return algorithm) for comparison.

An episode is a list of pairs (S_t, R_(t+1)) for t = 0, ..., T - 1; the state
after the last pair is terminal, with value 0. Numbers may be Fractions.
"""

from typing import Hashable, Iterable, Sequence

Episode = Sequence[tuple[Hashable, object]]


def td_lambda(episodes: Iterable[Episode], lam, alpha, gamma, V: dict | None = None, v0=0, offline: bool = False):
    """Run TD(lambda) with accumulating traces and return V.

    Online (the default), each TD error changes V at once. Offline, the
    increments of an episode are summed and applied at its end, with V fixed
    during the episode. Cost per step: O(number of states with a nonzero trace).
    """
    V = {} if V is None else V
    for ep in episodes:  # @line L1
        T = len(ep)
        z: dict = {}
        inc: dict = {}  # @line L2
        for t in range(T):  # @line L3
            s, r = ep[t]
            nxt = gamma * V.get(ep[t + 1][0], v0) if t + 1 < T else 0
            delta = r + nxt - V.get(s, v0)  # @line L4
            for x in z:
                z[x] = gamma * lam * z[x]
            z[s] = z.get(s, 0) + 1  # @line L5
            for x, e in z.items():  # @line L6
                if offline:
                    inc[x] = inc.get(x, 0) + alpha * delta * e  # @line L7
                else:
                    V[x] = V.get(x, v0) + alpha * delta * e
        if offline:  # @line L8
            for x, d in inc.items():
                V[x] = V.get(x, v0) + d
    return V  # @line L9


def lambda_return(ep: Episode, t: int, lam, gamma, V: dict, v0=0):
    """Return G_t^lambda = (1 - lam) sum_(n=1)^(T-t-1) lam^(n-1) G_(t:t+n) + lam^(T-t-1) G_t."""
    T = len(ep)
    total = 0 * gamma
    G = 0 * gamma  # running sum of the discounted rewards of the window
    for n in range(1, T - t + 1):
        G += gamma ** (n - 1) * ep[t + n - 1][1]
        if t + n < T:
            total += (1 - lam) * lam ** (n - 1) * (G + gamma**n * V.get(ep[t + n][0], v0))
        else:
            total += lam ** (n - 1) * G
    return total


def offline_lambda_return(episodes: Iterable[Episode], lam, alpha, gamma, V: dict | None = None, v0=0):
    """The forward view: at the end of each episode, add alpha (G_t^lambda - V(S_t)) for each t,
    with all targets computed from the values at the start of the episode."""
    V = {} if V is None else V
    for ep in episodes:
        inc: dict = {}
        for t, (s, _) in enumerate(ep):
            inc[s] = inc.get(s, 0) + alpha * (lambda_return(ep, t, lam, gamma, V, v0) - V.get(s, v0))
        for s, d in inc.items():
            V[s] = V.get(s, v0) + d
    return V
