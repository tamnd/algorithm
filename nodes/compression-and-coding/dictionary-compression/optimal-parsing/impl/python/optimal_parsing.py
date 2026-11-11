# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-parsing/. The authors are listed in prov/2HK8NC.jsonl.

"""Optimal parsing of a text with a static dictionary.

A parse cuts t into phrases that are all members of the dictionary D. Each
phrase w has a cost cost(w) >= 0 (1 for every phrase if we count phrases).
The parses are the paths from node 0 to node n in a directed acyclic graph
with an edge i -> i + |w| for each w in D that occurs at i. The cheapest
parse is a shortest path, which a right-to-left dynamic program finds.

- optimal_parse: the dynamic program, with a trie walk from each position.
- greedy_parse: the longest phrase at each step.
- flexible_parse: the phrase whose end gives the farthest next phrase end
  (optimal in phrase count when D is prefix-closed and has every symbol).
"""

from collections.abc import Callable

INF = float("inf")


class Trie:
    """A trie of the dictionary, as nested dicts; the key None marks a member."""

    def __init__(self, words) -> None:
        self.root: dict = {}
        for w in words:
            node = self.root
            for c in w:
                node = node.setdefault(c, {})
            node[None] = True

    def match_ends(self, t, i: int):
        """Yield each end e > i such that t[i:e] is in the dictionary."""
        node, j = self.root, i
        while j < len(t) and t[j] in node:
            node = node[t[j]]
            j += 1
            if None in node:
                yield j


def optimal_parse(t, words, cost: Callable | None = None) -> tuple[float, list]:
    """Return (minimum cost, phrases). cost(w) gives the cost of phrase w.

    With no cost function every phrase costs 1. The cost is INF and the list
    is empty if no parse exists.
    """
    if cost is None:
        def cost(w):
            return 1
    trie = Trie(words)
    n = len(t)
    best = [INF] * (n + 1)
    nxt = [-1] * (n + 1)
    best[n] = 0  # @line L1
    for i in range(n - 1, -1, -1):  # @line L2
        best[i] = INF  # @line L3
        for e in trie.match_ends(t, i):  # @line L4
            c = cost(t[i:e]) + best[e]
            if c < best[i]:  # @line L5
                best[i], nxt[i] = c, e  # @line L6
    if best[0] == INF:
        return INF, []
    out, i = [], 0
    while i < n:  # @line L7
        out.append(t[i:nxt[i]])
        i = nxt[i]
    return best[0], out  # @line L8


def longest_end(trie: Trie, t, i: int) -> int:
    """The end of the longest phrase at i, or i if none."""
    e = i
    for e2 in trie.match_ends(t, i):
        e = e2
    return e


def greedy_parse(t, words) -> list | None:
    """Longest phrase first; None if it gets stuck."""
    trie = Trie(words)
    out, i = [], 0
    while i < len(t):
        e = longest_end(trie, t, i)
        if e == i:
            return None
        out.append(t[i:e])
        i = e
    return out


def flexible_parse(t, words) -> list | None:
    """Flexible parsing: among the phrases at i, take the one whose end j
    maximizes j + (length of the longest phrase at j). None if stuck."""
    trie = Trie(words)
    n = len(t)
    out, i = [], 0
    while i < n:
        best_end, reach = -1, -1
        for e in trie.match_ends(t, i):
            r = n if e == n else longest_end(trie, t, e)
            if r > reach or (r == reach and e > best_end):
                best_end, reach = e, r
        if best_end < 0:
            return None
        out.append(t[i:best_end])
        i = best_end
    return out
