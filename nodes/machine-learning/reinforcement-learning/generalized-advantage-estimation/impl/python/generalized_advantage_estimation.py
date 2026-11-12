# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-advantage-estimation/. The authors are listed in prov/25P3CM.jsonl.

"""Generalized advantage estimation (Schulman et al. 2016).

A segment of T steps is given by rewards[t] = R_(t+1), values[t] = V(S_t) for
t = 0..T-1, dones[t] = True if the episode ends right after step t, and
last_value = V(S_T), used only if the last step does not end the episode.
All arithmetic is generic, so Fractions give exact results.

Cost: O(T) arithmetic operations and O(T) memory for the output.
"""


def td_errors(rewards, values, dones, last_value, gamma):
    """delta_t = R_(t+1) + gamma V(S_(t+1)) - V(S_t), with V = 0 after an end."""
    T = len(rewards)
    out = []
    for t in range(T):
        nxt = last_value if t == T - 1 else values[t + 1]
        out.append(rewards[t] + (0 if dones[t] else gamma * nxt) - values[t])
    return out


def gae(rewards, values, dones, last_value, gamma, lam):
    """Return (advantages, lambda-returns) of the segment by the backward recursion."""
    T = len(rewards)
    adv = [None] * T
    ret = [None] * T
    A = 0 * gamma  # @line L1
    for t in range(T - 1, -1, -1):  # @line L2
        nxt = last_value if t == T - 1 else values[t + 1]
        delta = rewards[t] + (0 if dones[t] else gamma * nxt) - values[t]  # @line L3
        A = delta + (0 if dones[t] else gamma * lam * A)  # @line L4
        adv[t] = A
        ret[t] = A + values[t]  # @line L5
    return adv, ret  # @line L6


def gae_direct(rewards, values, dones, last_value, gamma, lam):
    """The same advantages from the definition: sum_l (gamma lam)^l delta_(t+l), stopped at an end."""
    deltas = td_errors(rewards, values, dones, last_value, gamma)
    T = len(rewards)
    out = []
    for t in range(T):
        tot, w = 0 * gamma, 1
        for j in range(t, T):
            tot += w * deltas[j]
            if dones[j]:
                break
            w *= gamma * lam
        out.append(tot)
    return out
