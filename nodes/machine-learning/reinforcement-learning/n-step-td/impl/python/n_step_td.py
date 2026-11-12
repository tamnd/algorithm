# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/n-step-td/. The authors are listed in prov/FP2Z3F.jsonl.

"""Tabular n-step TD prediction.

An episode is a list of pairs (S_t, R_(t+1)) for t = 0, ..., T - 1; the state
after the last pair is terminal, with value 0. The update of V(S_tau) uses the
n-step return G_(tau:tau+n) and happens, in the online algorithm, at time
tau + n. Doing the updates in the order tau = 0, 1, ..., T - 1 gives the same
values, because the update of time tau + n sees exactly the earlier updates.
"""

from typing import Hashable, Iterable, Sequence

Episode = Sequence[tuple[Hashable, object]]


def n_step_return(ep: Episode, tau: int, n: int, gamma, V: dict, v0=0):
    """Return G_(tau:tau+n): n discounted rewards, then gamma^n V(S_(tau+n)) if not terminal."""
    T = len(ep)
    G = 0 * gamma
    for i in range(tau + 1, min(tau + n, T) + 1):
        G += gamma ** (i - tau - 1) * ep[i - 1][1]
    if tau + n < T:
        G += gamma**n * V.get(ep[tau + n][0], v0)
    return G


def n_step_td(episodes: Iterable[Episode], n: int, alpha, gamma, V: dict | None = None, v0=0):
    """Run n-step TD over the episodes and return V. Precondition: n >= 1.

    Cost: O(n) arithmetic operations per step (O(1) with a sliding sum),
    O(n) memory for the window plus the table.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    V = {} if V is None else V
    for ep in episodes:  # @line L1
        T = len(ep)
        for tau in range(T):  # @line L2
            G = 0 * gamma
            for i in range(tau + 1, min(tau + n, T) + 1):  # @line L3
                G += gamma ** (i - tau - 1) * ep[i - 1][1]
            if tau + n < T:  # @line L4
                G += gamma**n * V.get(ep[tau + n][0], v0)
            s = ep[tau][0]
            vs = V.get(s, v0)
            V[s] = vs + alpha * (G - vs)  # @line L5
    return V  # @line L6
