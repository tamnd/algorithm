# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watkins-q-lambda/. The authors are listed in prov/EMENRX.jsonl.

"""Tabular Watkins's Q(lambda) with accumulating traces.

The traces decay by gamma * lambda after a greedy next action and are cut to 0
after a non-greedy one (Sutton and Barto, Section 12.10).

An environment is any object with:
  env.start(rng)      a start state,
  env.actions(s)      a list of the actions in state s,
  env.step(s, a, rng) a pair (reward, next state), with None for the terminal state.
The behavior is choose(Q, s, actions, rng); the default is epsilon-greedy.
"""

import random


def greedy(Q: dict, s, actions):
    """The first action with the largest Q(s, a), in the order of `actions`."""
    best = actions[0]
    for a in actions[1:]:
        if Q.get((s, a), 0) > Q.get((s, best), 0):
            best = a
    return best


def eps_greedy(Q: dict, s, actions, eps, rng: random.Random):
    """With probability eps a uniform action, else the greedy one."""
    if rng.random() < eps:
        return actions[rng.randrange(len(actions))]
    return greedy(Q, s, actions)


def watkins_q_lambda(env, n_episodes: int, alpha, gamma, lam, eps, rng: random.Random, Q: dict | None = None,
                     choose=None, max_steps: int = 100_000):
    """Run Watkins's Q(lambda); return (Q, returns).

    alpha is a number or a function of the episode index k = 1, 2, ...
    """
    if choose is None:
        def choose(Q, s, actions, rng):
            return eps_greedy(Q, s, actions, eps, rng)
    Q = {} if Q is None else Q  # @line L1
    returns = []
    for k in range(1, n_episodes + 1):  # @line L2
        step = alpha(k) if callable(alpha) else alpha
        z: dict = {}
        s = env.start(rng)
        a = choose(Q, s, env.actions(s), rng)  # @line L3
        total = 0
        for _ in range(max_steps):  # @line L4
            r, s2 = env.step(s, a, rng)  # @line L5
            total += r
            if s2 is None:  # @line L6
                delta, a2, a_star = r - Q.get((s, a), 0), None, None
            else:
                acts2 = env.actions(s2)
                a2 = choose(Q, s2, acts2, rng)  # @line L7
                g = greedy(Q, s2, acts2)
                a_star = a2 if Q.get((s2, a2), 0) == Q.get((s2, g), 0) else g  # @line L8
                delta = r + gamma * Q.get((s2, a_star), 0) - Q.get((s, a), 0)  # @line L9
            z[(s, a)] = z.get((s, a), 0) + 1  # @line L10
            for key, e in z.items():  # @line L11
                Q[key] = Q.get(key, 0) + step * delta * e  # @line L12
            if a2 is not None and a2 == a_star:  # @line L13
                z = {key: gamma * lam * e for key, e in z.items()}
            else:
                z = {}  # @line L14
            if s2 is None:
                break
            s, a = s2, a2  # @line L15
        returns.append(total)
    return Q, returns  # @line L16
