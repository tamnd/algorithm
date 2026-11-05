# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deepwalk/. The authors are listed in prov/0SCSY9.jsonl.

import math
import random


def random_walk(adj: list[list[int]], start: int, t: int, rng: random.Random) -> list[int]:
    """A walk of at most t vertices from start; each step goes to a uniform out-neighbour.

    The walk stops early at a vertex with no out-neighbour.
    """
    walk = [start]
    while len(walk) < t and adj[walk[-1]]:
        walk.append(rng.choice(adj[walk[-1]]))
    return walk


def window_pairs(walk: list[int], w: int) -> list[tuple[int, int]]:
    """The skip-gram pairs (centre, context) of a walk, with a window of w on each side."""
    pairs = []
    for j in range(len(walk)):
        for k in range(max(0, j - w), min(len(walk), j + w + 1)):
            if k != j:
                pairs.append((walk[j], walk[k]))
    return pairs


def tree_path(n: int, u: int) -> list[tuple[int, int]]:
    """Inner nodes and signs from the root to the leaf of u in a complete binary tree.

    The tree has the n vertices as leaves in heap layout: inner nodes 0 .. n-2,
    the leaf of u is node n - 1 + u. The sign is +1 when the path goes to the left
    child and -1 when it goes to the right child.
    """
    node = n - 1 + u
    path = []
    while node > 0:
        parent = (node - 1) // 2
        path.append((parent, 1 if node == 2 * parent + 1 else -1))
        node = parent
    path.reverse()
    return path


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def hs_probability(phi_v: list[float], psi: list[list[float]], n: int, u: int) -> float:
    """Pr(u | v) under the hierarchical softmax: the product of the branch probabilities."""
    p = 1.0
    for node, sign in tree_path(n, u):
        p *= sigmoid(sign * dot(psi[node], phi_v))
    return p


def deepwalk(adj: list[list[int]], d: int = 8, w: int = 2, gamma: int = 10, t: int = 10,
             alpha: float = 0.05, seed: int = 0) -> list[list[float]]:
    """Return a d-dimensional embedding of each vertex, learned from random walks."""
    return deepwalk_with_tree(adj, d, w, gamma, t, alpha, seed)[0]


def deepwalk_with_tree(adj: list[list[int]], d: int = 8, w: int = 2, gamma: int = 10, t: int = 10,
                       alpha: float = 0.05, seed: int = 0) -> tuple[list[list[float]], list[list[float]]]:
    """Return the embedding phi and the vectors psi of the inner nodes of the tree.

    adj[v] lists the out-neighbours of v (both directions for an undirected
    graph). Each of gamma passes starts one walk of at most t vertices at every
    vertex, in a random order; each pair of vertices at most w apart in a walk is
    one step of stochastic gradient descent on the skip-gram loss with a
    hierarchical softmax. The run is deterministic for a fixed seed.
    """
    n = len(adj)
    rng = random.Random(seed)
    phi = [[(rng.random() - 0.5) / d for _ in range(d)] for _ in range(n)]  # @line L1
    psi = [[0.0] * d for _ in range(max(n - 1, 0))]
    for _ in range(gamma):  # @line L2
        order = list(range(n))  # @line L3
        rng.shuffle(order)
        for v in order:  # @line L4
            walk = random_walk(adj, v, t, rng)  # @line L5
            for j in range(len(walk)):  # @line L6
                x = phi[walk[j]]
                for k in range(max(0, j - w), min(len(walk), j + w + 1)):  # @line L7
                    if k == j:
                        continue
                    grad = [0.0] * d  # @line L8: the loss is -log Pr(walk[k] | x)
                    for node, sign in tree_path(n, walk[k]):
                        y = psi[node]
                        g = alpha * (1.0 - sigmoid(sign * dot(y, x))) * sign
                        for i in range(d):  # @line L9: gradient steps on x and on the path
                            grad[i] += g * y[i]
                            y[i] += g * x[i]
                    for i in range(d):
                        x[i] += grad[i]
    return phi, psi  # @line L10
