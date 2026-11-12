# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muzero/. The authors are listed in prov/RGAS70.jsonl.

"""The planning part of MuZero (Schrittwieser et al. 2020): Monte Carlo tree search
with the pUCT rule over a given learned model.

This file does not train anything. The model is given as three functions, as in
the paper: represent(observation) -> hidden state (h), dynamics(state, action) ->
(reward, next state) (g), and predict(state) -> (priors, value) (f). TableModel
builds them from tables. The search follows the pseudocode of the paper
(arXiv 1911.08265, Appendix B and the published pseudocode): pUCT with the
constants c1 = 1.25 and c2 = 19652, Q values normalized by the smallest and
largest values seen in the tree, and a backup of discounted rewards plus the
leaf value. Root exploration noise is left out.
"""

import math


class TableModel:
    """A learned model stored as tables. Unknown keys raise KeyError."""

    def __init__(self, dynamics, priors, values, represent=None):
        self.g, self.p, self.v = dynamics, priors, values
        self.h = represent or {}

    def represent(self, observation):
        return self.h.get(observation, observation)

    def dynamics(self, state, action):
        return self.g[(state, action)]

    def predict(self, state):
        return self.p[state], self.v[state]


class MinMax:
    def __init__(self):
        self.lo, self.hi = math.inf, -math.inf

    def update(self, x):
        self.lo, self.hi = min(self.lo, x), max(self.hi, x)

    def normalize(self, x):
        return (x - self.lo) / (self.hi - self.lo) if self.hi > self.lo else x


class Node:
    __slots__ = ("prior", "state", "reward", "children", "N", "W")

    def __init__(self, prior):
        self.prior, self.state, self.reward = prior, None, 0.0
        self.children, self.N, self.W = {}, 0, 0.0

    def value(self):
        return self.W / self.N if self.N else 0.0


def expand(node, priors):
    for a, p in enumerate(priors):
        node.children[a] = Node(p)


def score(parent, child, stats, gamma, c1, c2):
    """pUCT: normalized Q plus a prior-weighted exploration bonus."""
    total = parent.N
    u = child.prior * math.sqrt(total) / (1 + child.N) * (c1 + math.log((total + c2 + 1) / c2))
    q = stats.normalize(child.reward + gamma * child.value()) if child.N > 0 else 0.0
    return q + u


def search(model, observation, gamma, simulations, c1=1.25, c2=19652):
    """Run the given number of simulations. Return (visit counts of the root actions, chosen action, root)."""
    root = Node(1.0)
    root.state = model.represent(observation)  # @line L1
    priors, _ = model.predict(root.state)
    expand(root, priors)
    stats = MinMax()
    for _ in range(simulations):  # @line L2
        node, path = root, [root]  # @line L3
        while node.children:  # @line L4
            a = max(node.children, key=lambda b: score(node, node.children[b], stats, gamma, c1, c2))  # @line L5
            node = node.children[a]
            path.append(node)
        node.reward, node.state = model.dynamics(path[-2].state, a)  # @line L6
        priors, G = model.predict(node.state)  # @line L7
        expand(node, priors)
        for u in reversed(path):  # @line L8
            u.W += G  # @line L9
            u.N += 1
            stats.update(u.reward + gamma * u.value())
            G = u.reward + gamma * G
    visits = [root.children[a].N for a in sorted(root.children)]  # @line L10
    return visits, visits.index(max(visits)), root
