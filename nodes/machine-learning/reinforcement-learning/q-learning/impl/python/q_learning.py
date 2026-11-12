# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/q-learning/. The authors are listed in prov/CHAYP3.jsonl.

"""Tabular Q-learning (Watkins 1989): off-policy TD control with the max target.

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


def q_update(Q: dict, s, a, r, s2, actions2, alpha, gamma) -> None:
    """One Q-learning update from the transition (s, a, r, s2); actions2 are the actions of s2."""
    y = r if s2 is None else r + gamma * max(Q.get((s2, b), 0.0) for b in actions2)
    q = Q.get((s, a), 0.0)
    Q[(s, a)] = q + alpha * (y - q)


def q_learning(env, n_episodes: int, alpha, gamma, eps, rng: random.Random, Q: dict | None = None, max_steps: int = 100_000):
    """Run Q-learning with an epsilon-greedy behavior policy; return (Q, returns).

    alpha is a number or a function of n(s, a), the number of updates of the pair
    so far (1 at the first update); eps is a number or a function of the episode
    number k = 1, 2, ... An episode stops at the terminal state or after
    max_steps steps (for continuing tasks). eps = 1 gives a uniform behavior policy.
    """
    Q = {} if Q is None else Q  # @line L1
    n: dict = {}
    returns = []
    for k in range(1, n_episodes + 1):  # @line L2
        e = eps(k) if callable(eps) else eps
        s = env.start(rng)  # @line L3
        total = 0
        for _ in range(max_steps):  # @line L4
            a = eps_greedy(Q, s, env.actions(s), e, rng)  # @line L5
            r, s2 = env.step(s, a, rng)  # @line L6
            total += r
            n[(s, a)] = n.get((s, a), 0) + 1
            step = alpha(n[(s, a)]) if callable(alpha) else alpha
            y = r if s2 is None else r + gamma * max(Q.get((s2, b), 0.0) for b in env.actions(s2))  # @line L7
            q = Q.get((s, a), 0.0)
            Q[(s, a)] = q + step * (y - q)  # @line L8
            if s2 is None:
                break
            s = s2  # @line L9
        returns.append(total)
    return Q, returns  # @line L10


def q_learning_from_log(transitions, actions, alpha, gamma, Q: dict | None = None):
    """Off-policy use: apply the Q-learning update to a logged list of (s, a, r, s2) in order."""
    Q = {} if Q is None else Q
    for s, a, r, s2 in transitions:
        q_update(Q, s, a, r, s2, None if s2 is None else actions(s2), alpha, gamma)
    return Q


def greedy_path(env, Q: dict, s, rng: random.Random, limit: int = 1000):
    """Follow the greedy policy from s; return the list of states, or None if it does not end in limit steps."""
    path = [s]
    for _ in range(limit):
        _, s = env.step(s, greedy(Q, s, env.actions(s)), rng)
        if s is None:
            return path
        path.append(s)
    return None
