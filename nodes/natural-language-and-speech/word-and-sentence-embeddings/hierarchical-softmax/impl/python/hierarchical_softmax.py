# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-softmax/. The authors are listed in prov/5QHTPW.jsonl.

"""Hierarchical softmax over a binary tree, with a Huffman tree as in word2vec.

The |V| words are the leaves of a full binary tree with |V| - 1 inner nodes.
Each inner node n has a vector u_n. The path of word w is a list of
(node, bit) pairs from the root. At node n the walk goes to child 0 with
probability sigma(u_n . h) and to child 1 with probability sigma(-u_n . h),
so P(w | h) is the product of these factors along the path.
"""

import heapq
import math
from typing import Sequence


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def log_sigmoid(x: float) -> float:
    return -math.log1p(math.exp(-x)) if x >= 0 else x - math.log1p(math.exp(x))


def huffman_paths(counts: Sequence[int]) -> list[list[tuple[int, int]]]:
    """Path of (inner node, bit) pairs from the root to each word; nodes are numbered 0 to |V| - 2."""
    n = len(counts)
    if n == 1:
        return [[]]
    heap = [(c, i, ("leaf", i)) for i, c in enumerate(counts)]
    heapq.heapify(heap)
    children = []
    tie = n
    while len(heap) > 1:
        c0, _, a = heapq.heappop(heap)
        c1, _, b = heapq.heappop(heap)
        children.append((a, b))
        heapq.heappush(heap, (c0 + c1, tie, ("node", len(children) - 1)))
        tie += 1
    root = len(children) - 1
    paths: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    stack = [(root, [])]
    while stack:
        node, path = stack.pop()
        for bit, child in enumerate(children[node]):
            step = path + [(root - node, bit)]  # renumber so that the root is node 0
            if child[0] == "leaf":
                paths[child[1]] = step
            else:
                stack.append((child[1], step))
    return paths


def balanced_paths(n: int) -> list[list[tuple[int, int]]]:
    """Paths in a tree that splits the words in halves (depth ceil(log2 n))."""
    paths: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    counter = [0]

    def build(lo: int, hi: int, path):
        if hi - lo == 1:
            paths[lo] = path
            return
        node = counter[0]
        counter[0] += 1
        mid = (lo + hi + 1) // 2
        build(lo, mid, path + [(node, 0)])
        build(mid, hi, path + [(node, 1)])

    build(0, n, [])
    return paths


def log_prob(h: Sequence[float], nodes, path) -> float:
    """log P(w | h) for the word with this path."""
    total = 0.0
    for n, bit in path:  # @line L1
        s = sum(a * b for a, b in zip(nodes[n], h))  # @line L2
        total += log_sigmoid(s if bit == 0 else -s)  # @line L3
    return total  # @line L4


def loss_gradient(h: Sequence[float], nodes, path):
    """(-log P(w | h), gradient of h, dict of gradients of the inner node vectors)."""
    d = len(h)
    gh = [0.0] * d
    gn: dict[int, list[float]] = {}
    for n, bit in path:
        s = sum(a * b for a, b in zip(nodes[n], h))
        e = sigmoid(s) - (1.0 if bit == 0 else 0.0)  # d(-log factor)/ds
        row = gn.setdefault(n, [0.0] * d)
        for k in range(d):
            gh[k] += e * nodes[n][k]
            row[k] += e * h[k]
    return -log_prob(h, nodes, path), gh, gn


def expected_length(counts: Sequence[int], paths) -> float:
    total = sum(counts)
    return sum(c * len(p) for c, p in zip(counts, paths)) / total


def entropy_bits(counts: Sequence[int]) -> float:
    total = sum(counts)
    return -sum(c / total * math.log2(c / total) for c in counts if c > 0)
