# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/model-based-reinforcement-learning/. The authors are listed in prov/1JFJ2J.jsonl.

"""Certainty-equivalence control with a count model.

The agent counts transitions and sums rewards, builds the maximum-likelihood
model (P_hat, R_hat), plans on it by value iteration, and acts greedily with
respect to the plan, with epsilon-greedy exploration. An environment has a
start state and a method step(s, a) -> (r, s2). A model is given in the form
P[s][a] = list of (probability, next state), R[s][a] = expected reward.
"""

import random


class CountModel:
    def __init__(self, n_states, n_actions, r_unknown=0.0):
        """A pair with no data is a self-loop with reward r_unknown; r_unknown = Rmax gives R-max optimism."""
        self.nS, self.nA, self.r_unknown = n_states, n_actions, r_unknown
        self.N = [[0] * n_actions for _ in range(n_states)]
        self.Nt = [[{} for _ in range(n_actions)] for _ in range(n_states)]
        self.Rsum = [[0.0] * n_actions for _ in range(n_states)]

    def observe(self, s, a, r, s2):
        self.N[s][a] += 1
        self.Nt[s][a][s2] = self.Nt[s][a].get(s2, 0) + 1
        self.Rsum[s][a] += r

    def estimate(self):
        """The maximum-likelihood model (P_hat, R_hat)."""
        P, R = [], []
        for s in range(self.nS):
            prow, rrow = [], []
            for a in range(self.nA):
                n = self.N[s][a]
                if n == 0:
                    prow.append([(1.0, s)])
                    rrow.append(self.r_unknown)
                else:
                    prow.append([(c / n, t) for t, c in sorted(self.Nt[s][a].items())])
                    rrow.append(self.Rsum[s][a] / n)
            P.append(prow)
            R.append(rrow)
        return P, R


def q_values(P, R, gamma, V, s):
    return [R[s][a] + gamma * sum(p * V[t] for p, t in P[s][a]) for a in range(len(P[s]))]


def value_iteration(P, R, gamma, tol=1e-10, max_sweeps=100000):
    """Plan on a model: return (V, greedy policy) with ||V - V*|| <= tol * gamma / (1 - gamma)."""
    V = [0.0] * len(P)
    for _ in range(max_sweeps):
        W = [max(q_values(P, R, gamma, V, s)) for s in range(len(P))]
        done = max(abs(w - v) for w, v in zip(W, V)) <= tol
        V = W
        if done:
            break
    pi = []
    for s in range(len(P)):
        q = q_values(P, R, gamma, V, s)
        pi.append(q.index(max(q)))
    return V, pi


def certainty_equivalence(env, n_states, n_actions, gamma, steps, epsilon=0.1, plan_every=50, seed=0, r_unknown=0.0):
    """Learn a count model from interaction and plan on it. Return (model, policy, V_hat)."""
    rng = random.Random(seed)
    model = CountModel(n_states, n_actions, r_unknown)  # @line L1
    V, pi = value_iteration(*model.estimate(), gamma)
    s = env.start
    for t in range(1, steps + 1):  # @line L2
        a = rng.randrange(n_actions) if rng.random() < epsilon else pi[s]  # @line L3
        r, s2 = env.step(s, a)  # @line L4
        model.observe(s, a, r, s2)  # @line L5
        if t % plan_every == 0 or t == steps:  # @line L6
            P_hat, R_hat = model.estimate()  # @line L7
            V, pi = value_iteration(P_hat, R_hat, gamma)  # @line L8
        s = s2  # @line L9
    return model, pi, V  # @line L10
