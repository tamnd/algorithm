# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-q-learning/. The authors are listed in prov/K9FDTT.jsonl.

"""Tabular Double Q-learning (van Hasselt 2010).

Two tables QA and QB. The behavior policy is epsilon-greedy in QA + QB. At each
step a fair coin picks the table to update; that table chooses the greedy action
in the next state, and the other table gives its value.

An environment is any object with:
  env.start(rng)      a start state,
  env.actions(s)      a list of the actions in state s,
  env.step(s, a, rng) a pair (reward, next state), with None for the terminal state.
Ties between greedy actions are broken uniformly at random with rng.
"""

import random


def argmax(values: list, rng: random.Random):
    """The index of a largest value; a tie is broken uniformly at random."""
    m = max(values)
    best = [i for i, v in enumerate(values) if v == m]
    return best[0] if len(best) == 1 else rng.choice(best)


def eps_greedy_sum(QA: dict, QB: dict, s, actions, eps, rng: random.Random):
    """With probability eps a uniform action, else a greedy action for QA + QB."""
    if rng.random() < eps:
        return actions[rng.randrange(len(actions))]
    total = [QA.get((s, a), 0.0) + QB.get((s, a), 0.0) for a in actions]
    return actions[argmax(total, rng)]


def double_target(X: dict, Y: dict, r, s2, actions2, gamma, rng: random.Random):
    """r + gamma * Y(s2, argmax_a X(s2, a)); r alone when s2 is terminal (None)."""
    if s2 is None:
        return r
    b = actions2[argmax([X.get((s2, a), 0.0) for a in actions2], rng)]
    return r + gamma * Y.get((s2, b), 0.0)


def double_q_learning(env, n_episodes: int, alpha, gamma, eps, rng: random.Random,
                      QA: dict | None = None, QB: dict | None = None, max_steps: int = 100_000):
    """Run Double Q-learning; return (QA, QB, first_actions).

    first_actions lists the first action of each episode. alpha is a number or a
    function of n(s, a), the number of visits of the pair (in either table).
    """
    QA = {} if QA is None else QA  # @line L1
    QB = {} if QB is None else QB
    n: dict = {}
    first_actions = []
    for _ in range(n_episodes):  # @line L2
        s = env.start(rng)  # @line L3
        for k in range(max_steps):  # @line L4
            a = eps_greedy_sum(QA, QB, s, env.actions(s), eps, rng)  # @line L5
            if k == 0:
                first_actions.append(a)
            r, s2 = env.step(s, a, rng)  # @line L6
            X, Y = (QA, QB) if rng.random() < 0.5 else (QB, QA)  # @line L7
            acts2 = None if s2 is None else env.actions(s2)
            y = double_target(X, Y, r, s2, acts2, gamma, rng)  # @line L8
            n[(s, a)] = n.get((s, a), 0) + 1
            step = alpha(n[(s, a)]) if callable(alpha) else alpha
            q = X.get((s, a), 0.0)
            X[(s, a)] = q + step * (y - q)  # @line L9
            if s2 is None:
                break
            s = s2  # @line L10
    return QA, QB, first_actions  # @line L11
