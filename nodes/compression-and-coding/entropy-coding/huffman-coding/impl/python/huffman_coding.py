# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huffman-coding/. The authors are listed in prov/06ZXXT.jsonl.

"""Huffman coding: build an optimal prefix code, encode and decode.

The weights are non-negative numbers (counts or probabilities). Two
builders are given: the heap method for any order of the weights, and the
two-queue method of van Leeuwen for weights that are already sorted.
"""

import heapq
from typing import Hashable, Sequence

# A tree is either a leaf (an int, the index of a symbol) or a pair
# (left, right) of trees.
Tree = object


def huffman_tree(weights: Sequence[float]) -> Tree:
    """Return a Huffman tree for the weights, by the heap method.

    Ties are broken by creation order: an older item comes out of the
    heap first. One symbol gives a single leaf.
    """
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    heap: list = []  # @line L1  items are (weight, age, tree)
    for i, w in enumerate(weights):  # @line L2
        heap.append((w, i, i))
    heapq.heapify(heap)  # bottom-up construction, O(n)
    age = n
    for _ in range(n - 1):  # @line L3
        wx, _, x = heapq.heappop(heap)  # @line L4
        wy, _, y = heapq.heappop(heap)  # @line L5
        z = (x, y)  # @line L6
        wz = wx + wy  # @line L7
        heapq.heappush(heap, (wz, age, z))  # @line L8
        age += 1
    return heap[0][2]  # @line L9


def huffman_tree_sorted(weights: Sequence[float]) -> Tree:
    """Two-queue method for weights sorted in non-decreasing order.

    Leaves wait in queue A, merged nodes in queue B. Merged weights come
    out in non-decreasing order, so B stays sorted and each step takes
    the two smallest fronts. On a tie the leaf is taken first, which gives
    the code with the smallest maximum length among optimal codes.
    """
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    if any(weights[i] > weights[i + 1] for i in range(n - 1)):
        raise ValueError("weights must be sorted")
    a = [(w, i) for i, w in enumerate(weights)]
    b: list = []
    ia = ib = 0

    def take():
        nonlocal ia, ib
        if ia < n and (ib >= len(b) or a[ia][0] <= b[ib][0]):
            ia += 1
            return a[ia - 1]
        ib += 1
        return b[ib - 1]

    for _ in range(n - 1):
        w1, t1 = take()
        w2, t2 = take()
        b.append((w1 + w2, (t1, t2)))
    return b[-1][1] if b else 0


def code_lengths(tree: Tree, n: int) -> list[int]:
    """Depth of each leaf. A tree that is one leaf gives length 0."""
    lengths = [0] * n
    stack = [(tree, 0)]
    while stack:
        t, d = stack.pop()
        if isinstance(t, tuple):
            stack.append((t[0], d + 1))
            stack.append((t[1], d + 1))
        else:
            lengths[t] = d
    return lengths


def codewords(tree: Tree, n: int) -> list[str]:
    """The codeword of each symbol: 0 for a left edge, 1 for a right edge.

    A tree with one leaf gets the codeword "0", so that each symbol of a
    message still costs one bit.
    """
    if not isinstance(tree, tuple):
        return ["0"]
    words = [""] * n
    stack = [(tree, "")]
    while stack:
        t, w = stack.pop()
        if isinstance(t, tuple):
            stack.append((t[0], w + "0"))
            stack.append((t[1], w + "1"))
        else:
            words[t] = w
    return words


def huffman_code(freq: dict) -> dict:
    """Map each symbol of a frequency table to its Huffman codeword."""
    symbols = sorted(freq, key=repr)
    tree = huffman_tree([freq[s] for s in symbols])
    words = codewords(tree, len(symbols))
    return {s: words[i] for i, s in enumerate(symbols)}


def encode(message: Sequence[Hashable], code: dict) -> str:
    return "".join(code[s] for s in message)


def decode(bits: str, code: dict) -> list:
    """Decode by walking a trie of the codewords, one bit at a time."""
    root: dict = {}
    for s, w in code.items():
        node = root
        for b in w[:-1]:
            node = node.setdefault(b, {})
        node[w[-1]] = (s,)  # a leaf is a 1-tuple, an inner node is a dict
    out = []
    node = root
    for b in bits:
        nxt = node[b]
        if isinstance(nxt, tuple):
            out.append(nxt[0])
            node = root
        else:
            node = nxt
    if node is not root:
        raise ValueError("the bit string ends inside a codeword")
    return out


def cost(weights: Sequence[float], lengths: Sequence[int]) -> float:
    return sum(w * l for w, l in zip(weights, lengths))
