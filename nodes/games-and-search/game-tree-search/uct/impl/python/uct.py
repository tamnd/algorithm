# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uct/. The authors are listed in prov/TGTRKB.jsonl.

"""UCT (Kocsis and Szepesvari 2006): rollout-based search that picks the action at every node of the
stored tree by UCB1, with the bias term 2 Cp sqrt(ln N(s) / N(s, a)).

The game is an explicit tree: an inner node is a list of children, a leaf is a number p in [0, 1].
Player 0 moves at even depth and maximizes the reward, player 1 moves at odd depth and maximizes
1 minus the reward. With stochastic=True a leaf pays 1 with probability p and 0 otherwise, so its
expected reward is p; otherwise it pays p.
"""

import math
import random


class Stats:
    """N(s), and N(s, a) and the mean reward Q(s, a) to player 0 for every action a of node s."""

    __slots__ = ("n", "counts", "sums")

    def __init__(self, k: int):
        self.n = 0
        self.counts = [0] * k
        self.sums = [0.0] * k

    def mean(self, a: int) -> float:
        # A ratio of a sum and a count, so equal statistics give equal floats and ties stay ties.
        return self.sums[a] / self.counts[a]


def uct(tree, iterations: int, rng: random.Random, cp: float = 1 / math.sqrt(2), stochastic: bool = False, trace=None):
    """Run UCT from the root of tree and return (best root action, table of statistics).

    The best action has the largest mean reward for the player at the root. The table maps the
    path of each visited inner node to its Stats. If trace is a list, the root action of every
    iteration is appended to it. Precondition: the root is an inner node and iterations >= 1.
    Cost: O(iterations * depth) time; at most one Stats per visited inner node.
    """
    table: dict = {}
    for _ in range(iterations):  # @line L1
        node, path, visited = tree, (), []
        while isinstance(node, list):
            st = table.get(path)
            if st is None:
                st = table[path] = Stats(len(node))
            untried = [a for a, c in enumerate(st.counts) if c == 0]
            if untried:
                a = untried[0]  # @line L4
            else:
                sign = 1.0 if len(path) % 2 == 0 else -1.0
                bias = 2 * cp * math.sqrt(math.log(st.n))
                a = max(range(len(node)), key=lambda b: sign * st.mean(b) + bias / math.sqrt(st.counts[b]))  # @line L5
            if trace is not None and not path:
                trace.append(a)
            visited.append((st, a))
            node, path = node[a], path + (a,)  # @line L6
        r = (1.0 if rng.random() < node else 0.0) if stochastic else float(node)  # @line L3
        for st, a in visited:  # @line L9
            st.n += 1  # @line L7
            st.counts[a] += 1
            st.sums[a] += r  # @line L8
    root = table[()]
    # Player 0 moves at the root and maximizes the mean; untried actions are never chosen.
    best = max(range(len(tree)), key=lambda b: root.mean(b) if root.counts[b] else -math.inf)  # @line L2
    return best, table


def ucb1(probs, pulls: int, rng: random.Random):
    """Plain UCB1 of Auer, Cesa-Bianchi and Fischer (2002) on Bernoulli arms, as a reference.

    Plays each arm once, then the arm with the largest mean + sqrt(2 ln n / n_j). Returns the list of
    arms played.
    """
    k = len(probs)
    counts, sums, out = [0] * k, [0.0] * k, []
    for t in range(pulls):
        if t < k:
            j = t
        else:
            j = max(range(k), key=lambda b: sums[b] / counts[b] + math.sqrt(2 * math.log(t) / counts[b]))
        r = 1.0 if rng.random() < probs[j] else 0.0
        counts[j] += 1
        sums[j] += r
        out.append(j)
    return out
