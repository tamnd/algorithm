# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discounted-return/. The authors are listed in prov/HDFR24.jsonl.
"""Discounted returns of one episode.

rewards[k] holds R_(k+1), the reward of the step from time k, for k = 0 .. T-1,
so an episode of T steps has the returns G_0 .. G_T with G_T = 0.
"""

from typing import List, Sequence


def returns(rewards: Sequence, gamma) -> List:
    """All returns G_0 .. G_T by the recursion G_t = R_(t+1) + gamma G_(t+1),
    from the end of the episode backward. Cost O(T)."""
    g = 0 * gamma
    out = [g]
    for r in reversed(rewards):
        g = r + gamma * g
        out.append(g)
    out.reverse()
    return out


def return_from(rewards: Sequence, gamma, t: int):
    """G_t = sum_k gamma^k R_(t+k+1) by the direct sum. Cost O(T - t)."""
    return sum((gamma ** k * r for k, r in enumerate(rewards[t:])), 0 * gamma)


def n_step_return(rewards: Sequence, values: Sequence, gamma, t: int, n: int):
    """G_(t:t+n) = R_(t+1) + ... + gamma^(n-1) R_(t+n) + gamma^n V(S_(t+n)).
    values[k] is the estimate V(S_k) for k = 0 .. T, with values[T] = 0 for a
    terminal state. When t + n >= T the result is the full return G_t."""
    T = len(rewards)
    end = min(t + n, T)
    g = return_from(rewards[:end], gamma, t)
    if t + n < T:
        g += gamma ** n * values[t + n]
    return g
