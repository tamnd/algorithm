# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dagger/. The authors are listed in prov/C2SKZR.jsonl.

"""DAgger (Ross, Gordon and Bagnell, 2011) and behavior cloning on a windy lane.

The lane: position x in -L..L. A wind pushes right by 1 at every step, and the
action a in {-2, -1, 0} steers left, so the next position is clip(x + a + 1).
The expert steers against the wind: a = -2 if x > 0, -1 if x = 0, 0 if x < 0.
From x = 0 the expert stays at 0 for ever. The cost of a step is
min(|x|, 4) / 4, in [0, 1]. An episode has T steps from x = 0.

The learner is a table: in each state it predicts the most common expert label
seen there, and "no steering" (a = 0) where it has seen no label. It is an
imperfect classifier: with probability eps it outputs a uniformly random
action instead. A policy is a function x -> {action: probability}. Expected
costs and losses are exact, by a forward pass over the distribution of x.
"""

import random
from collections import Counter

ACTIONS = (-2, -1, 0)
WIND = 1


class Lane:
    def __init__(self, half_width: int = 8, horizon: int = 40) -> None:
        self.L, self.T = half_width, horizon

    def states(self):
        return range(-self.L, self.L + 1)

    def next_state(self, x: int, a: int) -> int:
        return max(-self.L, min(self.L, x + a + WIND))

    @staticmethod
    def cost(x: int) -> float:
        return min(abs(x), 4) / 4


def expert_action(x: int) -> int:
    return -2 if x > 0 else (-1 if x == 0 else 0)


def expert(x: int):
    return {expert_action(x): 1.0}


class TableLearner:
    """Majority label per state; no steering (0) where no label was seen;
    a uniformly random action with probability eps."""

    def __init__(self, data=(), eps: float = 0.1) -> None:
        votes: dict[int, Counter] = {}
        for x, a in data:
            votes.setdefault(x, Counter())[a] += 1
        self.table = {x: max(ACTIONS, key=lambda a: (c[a], a)) for x, c in votes.items()}
        self.eps = eps

    def action(self, x: int) -> int:
        return self.table.get(x, 0)

    def __call__(self, x: int):
        out = {a: self.eps / len(ACTIONS) for a in ACTIONS}
        out[self.action(x)] += 1.0 - self.eps
        return out


def mixture(beta: float, policy):
    """pi_i = beta * expert + (1 - beta) * policy."""
    def pi(x: int):
        out = {a: (1.0 - beta) * p for a, p in policy(x).items()}
        a = expert_action(x)
        out[a] = out.get(a, 0.0) + beta
        return out
    return pi


def draw(dist, rng: random.Random):
    u, acc = rng.random(), 0.0
    for a, p in dist.items():
        acc += p
        if u < acc:
            return a
    return a


def rollout(env: Lane, policy, rng: random.Random):
    """One episode of policy from x = 0; returns the visited states."""
    x, visited = 0, []
    for _ in range(env.T):
        visited.append(x)
        x = env.next_state(x, draw(policy(x), rng))
    return visited


def state_distributions(env: Lane, policy):
    """d_t(x) for t = 0..T-1, exactly."""
    d = {0: 1.0}
    out = []
    for _ in range(env.T):
        out.append(d)
        nxt: dict[int, float] = {}
        for x, p in d.items():
            for a, q in policy(x).items():
                y = env.next_state(x, a)
                nxt[y] = nxt.get(y, 0.0) + p * q
        d = nxt
    return out


def expected_cost(env: Lane, policy) -> float:
    """J(policy) = E[sum_t cost(x_t)], exactly."""
    return sum(p * env.cost(x) for d in state_distributions(env, policy) for x, p in d.items())


def loss(env: Lane, policy, under) -> float:
    """(1/T) sum_t E_{x ~ d_t(under)} Pr[policy(x) != expert(x)], the 0-1 loss."""
    return sum(p * (1.0 - policy(x).get(expert_action(x), 0.0))
               for d in state_distributions(env, under) for x, p in d.items()) / env.T


def expert_gap(env: Lane) -> float:
    """u = max over t, x, a of Q*_t(x, a) - Q*_t(x, expert(x)), where Q*_t is
    the expert's cost-to-go with t steps left after taking a in x."""
    v = {x: 0.0 for x in env.states()}
    u = 0.0
    for _ in range(env.T):
        q = {x: {a: env.cost(x) + v[env.next_state(x, a)] for a in ACTIONS} for x in env.states()}
        for x in env.states():
            u = max(u, max(q[x].values()) - q[x][expert_action(x)])
        v = {x: q[x][expert_action(x)] for x in env.states()}
    return u


def behavior_cloning(env: Lane, n_traj: int, rng: random.Random, eps: float = 0.1) -> TableLearner:
    """Fit the table to expert labels on n_traj expert episodes."""
    data = []
    for _ in range(n_traj):
        data += [(x, expert_action(x)) for x in rollout(env, expert, rng)]
    return TableLearner(data, eps)


def dagger(env: Lane, n_iter: int, traj_per_iter: int, rng: random.Random, betas=None,
           eps: float = 0.1):
    """DAgger; returns the learned policies pi_hat_1, ..., pi_hat_{N+1}.

    betas[i] is the weight of the expert in iteration i + 1; the default is
    beta_1 = 1 and beta_i = 0 afterwards."""
    if betas is None:
        betas = [1.0] + [0.0] * (n_iter - 1)
    data = []  # @line L1
    learner = TableLearner((), eps)  # @line L1
    learned = [learner]
    for i in range(n_iter):  # @line L2
        pi = mixture(betas[i], learner)  # @line L3
        for _ in range(traj_per_iter):  # @line L4
            visited = rollout(env, pi, rng)  # @line L4
            data += [(x, expert_action(x)) for x in visited]  # @line L5
        learner = TableLearner(data, eps)  # @line L6
        learned.append(learner)  # @line L7
    return learned  # @line L8
