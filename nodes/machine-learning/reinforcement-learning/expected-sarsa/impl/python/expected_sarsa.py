# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expected-sarsa/. The authors are listed in prov/HAESKC.jsonl.

"""Tabular Expected SARSA with epsilon-greedy policies.

The target is R + gamma * sum_a pi(a | S') Q(S', a), where pi is the
epsilon-greedy policy for Q with parameter target_eps. With target_eps equal to
the behavior eps the method is on-policy; with target_eps = 0 the target is
greedy, and the method is Q-learning.

An environment is any object with:
  env.start(rng)      a start state,
  env.actions(s)      a list of the actions in state s,
  env.step(s, a, rng) a pair (reward, next state), with None for the terminal state.
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


def eps_greedy_probs(Q: dict, s, actions, eps) -> dict:
    """The probabilities pi(a | s) of the epsilon-greedy policy for Q (ties go to the first best action)."""
    g = greedy(Q, s, actions)
    p = {a: eps / len(actions) for a in actions}
    p[g] = p[g] + (1 - eps)
    return p


def expected_value(Q: dict, s, actions, eps):
    """sum_a pi(a | s) Q(s, a) for the epsilon-greedy policy pi; with eps = 0 it is max_a Q(s, a)."""
    if eps == 0:
        return Q.get((s, greedy(Q, s, actions)), 0.0)
    p = eps_greedy_probs(Q, s, actions, eps)
    return sum(p[a] * Q.get((s, a), 0.0) for a in actions)


def expected_sarsa(env, n_episodes: int, alpha, gamma, eps, rng: random.Random, Q: dict | None = None,
                   target_eps=None, max_steps: int = 100_000):
    """Run Expected SARSA; return (Q, returns).

    The behavior policy is epsilon-greedy with parameter eps; the target policy
    is epsilon-greedy with parameter target_eps (default: eps, on-policy).
    alpha is a number or a function of n(s, a), the number of updates of the pair.
    """
    Q = {} if Q is None else Q  # @line L1
    te = eps if target_eps is None else target_eps
    n: dict = {}
    returns = []
    for _ in range(n_episodes):  # @line L2
        s = env.start(rng)  # @line L3
        total = 0
        for _ in range(max_steps):  # @line L4
            a = eps_greedy(Q, s, env.actions(s), eps, rng)  # @line L5
            r, s2 = env.step(s, a, rng)  # @line L6
            total += r
            y = r if s2 is None else r + gamma * expected_value(Q, s2, env.actions(s2), te)  # @line L7
            n[(s, a)] = n.get((s, a), 0) + 1
            step = alpha(n[(s, a)]) if callable(alpha) else alpha
            q = Q.get((s, a), 0.0)
            Q[(s, a)] = q + step * (y - q)  # @line L8
            if s2 is None:
                break
            s = s2  # @line L9
        returns.append(total)
    return Q, returns  # @line L10
