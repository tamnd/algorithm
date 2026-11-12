# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sarsa/. The authors are listed in prov/568W6N.jsonl.

"""Tabular SARSA: on-policy TD control with an epsilon-greedy policy.

An environment is any object with:
  env.start(rng)      a start state,
  env.actions(s)      a list of the actions in state s,
  env.step(s, a, rng) a pair (reward, next state), with None for the terminal state.
Q is a dict keyed by (state, action); missing entries are 0, and the terminal
state has value 0. All randomness comes from the random.Random object passed in.
"""

import random


def greedy(Q: dict, s, actions):
    """The first action with the largest Q(s, a), in the order of `actions`."""
    best = actions[0]
    for a in actions[1:]:
        if Q.get((s, a), 0.0) > Q.get((s, best), 0.0):
            best = a
    return best


def eps_greedy(Q: dict, s, actions, eps, rng: random.Random):
    """With probability eps a uniform action, else the greedy one."""
    if rng.random() < eps:
        return actions[rng.randrange(len(actions))]
    return greedy(Q, s, actions)


def sarsa(env, n_episodes: int, alpha, gamma, eps, rng: random.Random, Q: dict | None = None, max_steps: int = 100_000):
    """Run SARSA and return (Q, returns), with the undiscounted return of each episode.

    alpha is a number or a function of n(s, a), the number of updates of the pair
    so far (1 at the first update); eps is a number or a function of the episode
    number k = 1, 2, ... (for a GLIE schedule).
    """
    Q = {} if Q is None else Q  # @line L1
    n: dict = {}
    returns = []
    for k in range(1, n_episodes + 1):  # @line L2
        e = eps(k) if callable(eps) else eps
        s = env.start(rng)
        a = eps_greedy(Q, s, env.actions(s), e, rng)  # @line L3
        total = 0
        for _ in range(max_steps):  # @line L4
            r, s2 = env.step(s, a, rng)  # @line L5
            total += r
            if s2 is None:
                target, a2 = r, None
            else:
                a2 = eps_greedy(Q, s2, env.actions(s2), e, rng)
                target = r + gamma * Q.get((s2, a2), 0.0)  # @line L6
            n[(s, a)] = n.get((s, a), 0) + 1
            step = alpha(n[(s, a)]) if callable(alpha) else alpha
            q = Q.get((s, a), 0.0)
            Q[(s, a)] = q + step * (target - q)  # @line L7
            if s2 is None:
                break
            s, a = s2, a2  # @line L8
        returns.append(total)
    return Q, returns  # @line L9


def greedy_path(env, Q: dict, s, rng: random.Random, limit: int = 1000):
    """Follow the greedy policy from s; return the list of states, or None if it does not end in limit steps."""
    path = [s]
    for _ in range(limit):
        _, s = env.step(s, greedy(Q, s, env.actions(s)), rng)
        if s is None:
            return path
        path.append(s)
    return None
