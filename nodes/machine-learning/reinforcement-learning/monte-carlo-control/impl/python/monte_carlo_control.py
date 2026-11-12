# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-control/. The authors are listed in prov/VZ2NZH.jsonl.

"""Monte Carlo control: exploring starts (MC ES), on-policy control with
epsilon-soft policies, and off-policy control with weighted importance sampling.

An environment is any object with:
  env.states          a list of the nonterminal states,
  env.actions(s)      a list of the actions in state s,
  env.start(rng)      a start state (used by the on-policy and off-policy forms),
  env.step(s, a, rng) a pair (reward, next state), with None for the terminal state.
All randomness comes from the random.Random object passed in.
"""

import random
from typing import Callable


def greedy(Q: dict, s, actions) -> object:
    """The first action with the largest Q(s, a), in the order of `actions`."""
    best = actions[0]
    for a in actions[1:]:
        if Q.get((s, a), 0) > Q.get((s, best), 0):
            best = a
    return best


def run_episode(env, s, a, choose: Callable, rng: random.Random, max_steps: int):
    """Generate S_0, A_0, R_1, ... from the pair (s, a), then actions from choose(s)."""
    ep = []
    while True:
        r, s2 = env.step(s, a, rng)
        ep.append((s, a, r))
        if s2 is None:
            return ep
        if len(ep) >= max_steps:
            raise RuntimeError("episode did not end within max_steps")
        s, a = s2, choose(s2)


def mc_es(env, n_episodes: int, gamma, rng: random.Random, max_steps: int = 10_000):
    """Monte Carlo control with exploring starts and first-visit sample averages.

    Returns (pi, Q, N): the greedy policy, the action values and the visit counts.
    """
    Q: dict = {}
    N: dict = {}
    pi = {s: env.actions(s)[0] for s in env.states}  # @line L1
    pairs = [(s, a) for s in env.states for a in env.actions(s)]
    for _ in range(n_episodes):  # @line L2
        s0, a0 = pairs[rng.randrange(len(pairs))]  # @line L3
        ep = run_episode(env, s0, a0, lambda s: pi[s], rng, max_steps)  # @line L4
        first = {}
        for t, (s, a, _) in enumerate(ep):
            first.setdefault((s, a), t)
        G = 0  # @line L5
        for t in range(len(ep) - 1, -1, -1):  # @line L6
            s, a, r = ep[t]
            G = gamma * G + r  # @line L7
            if first[(s, a)] < t:  # @line L8
                continue
            N[(s, a)] = N.get((s, a), 0) + 1
            q = Q.get((s, a), 0)
            Q[(s, a)] = q + (G - q) / N[(s, a)]  # @line L9
            pi[s] = greedy(Q, s, env.actions(s))  # @line L10
    return pi, Q, N  # @line L11


def eps_greedy_choice(Q: dict, s, actions, eps, rng: random.Random):
    """Draw an action of the epsilon-greedy policy for Q: uniform with probability eps, else greedy."""
    if rng.random() < eps:
        return actions[rng.randrange(len(actions))]
    return greedy(Q, s, actions)


def on_policy_mc_control(env, n_episodes: int, gamma, eps, rng: random.Random, max_steps: int = 10_000):
    """On-policy first-visit MC control for epsilon-soft policies (no exploring starts).

    eps is a number or a function of the episode number k = 1, 2, ...
    Returns (Q, N); the policy is epsilon-greedy for Q.
    """
    Q: dict = {}
    N: dict = {}
    for k in range(1, n_episodes + 1):
        e = eps(k) if callable(eps) else eps
        choose = lambda s: eps_greedy_choice(Q, s, env.actions(s), e, rng)
        s0 = env.start(rng)
        ep = run_episode(env, s0, choose(s0), choose, rng, max_steps)
        first = {}
        for t, (s, a, _) in enumerate(ep):
            first.setdefault((s, a), t)
        G = 0
        for t in range(len(ep) - 1, -1, -1):
            s, a, r = ep[t]
            G = gamma * G + r
            if first[(s, a)] < t:
                continue
            N[(s, a)] = N.get((s, a), 0) + 1
            q = Q.get((s, a), 0)
            Q[(s, a)] = q + (G - q) / N[(s, a)]
    return Q, N


def off_policy_mc_control(env, n_episodes: int, gamma, rng: random.Random, max_steps: int = 10_000):
    """Off-policy every-visit MC control with weighted importance sampling.

    The behavior policy is uniform over the actions; the target policy is greedy
    for Q. Returns (pi, Q, C), with C the cumulative importance weights.
    """
    Q: dict = {}
    C: dict = {}
    pi = {s: env.actions(s)[0] for s in env.states}
    for _ in range(n_episodes):
        uniform = lambda s: env.actions(s)[rng.randrange(len(env.actions(s)))]
        s0 = env.start(rng)
        ep = run_episode(env, s0, uniform(s0), uniform, rng, max_steps)
        G = 0
        W = 1
        for t in range(len(ep) - 1, -1, -1):
            s, a, r = ep[t]
            G = gamma * G + r
            C[(s, a)] = C.get((s, a), 0) + W
            q = Q.get((s, a), 0)
            Q[(s, a)] = q + W / C[(s, a)] * (G - q)
            pi[s] = greedy(Q, s, env.actions(s))
            if a != pi[s]:
                break
            W = W * len(env.actions(s))  # W / b(a | s) with b uniform and pi(a | s) = 1
    return pi, Q, C
