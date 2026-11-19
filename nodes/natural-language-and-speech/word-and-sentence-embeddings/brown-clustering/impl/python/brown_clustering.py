# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brown-clustering/. The authors are listed in prov/HG0BRB.jsonl.
"""Brown clustering: greedy merging of word classes.

Each merge joins the two classes whose merge keeps the average mutual
information (AMI) of adjacent classes highest. The bigrams are the adjacent
token pairs inside each sentence, with no padding. Logs are natural, so the
AMI is in nats.
"""

from collections import Counter
from dataclasses import dataclass
from math import log


@dataclass(frozen=True)
class Merge:
    """One merge. left and right are tree nodes, node is the new tree node.

    Leaves 0 .. V-1 are the words in the order of vocabulary(). Internal
    nodes are numbered V, V+1, ... in the order of the merges. ami is the
    AMI of the partition just after the merge, in nats.
    """

    left: int
    right: int
    node: int
    ami: float


def vocabulary(corpus: list[list[str]]) -> list[str]:
    """The word types, by decreasing count, ties in string order."""
    count = Counter(w for sentence in corpus for w in sentence)
    return sorted(count, key=lambda w: (-count[w], w))


def bigram_counts(corpus: list[list[str]], words: list[str]) -> tuple[list[list[int]], int]:
    """The matrix n[l][m] of adjacent pairs (words[l], words[m]) and its total."""
    index = {w: i for i, w in enumerate(words)}
    n = [[0] * len(words) for _ in words]
    total = 0
    for sentence in corpus:
        for a, b in zip(sentence, sentence[1:]):
            n[index[a]][index[b]] += 1
            total += 1
    return n, total


def _q(c: int, left: int, right: int, total: int) -> float:
    """p log(p / (pl pr)) with p = c / total, pl = left / total, pr = right / total."""
    if c == 0:
        return 0.0
    return c / total * log(c * total / (left * right))


def average_mutual_information(n: list[list[int]], total: int) -> float:
    """AMI of the class bigram matrix n, computed from scratch, in nats."""
    k = len(n)
    left = [sum(row) for row in n]
    right = [sum(n[l][m] for l in range(k)) for m in range(k)]
    return sum(_q(n[l][m], left[l], right[m], total) for l in range(k) for m in range(k))


def brown_clustering(
    corpus: list[list[str]], num_classes: int = 1
) -> tuple[list[list[str]], list[Merge]]:
    """Merge classes greedily until num_classes classes remain.

    Precondition: num_classes >= 1. Returns the classes (each a list of
    words, the kept class first) and the merges in order. Ties within 1e-12
    go to the first pair (i, j) in the order of the current class indices.
    Cost: O(N + V^4) time for V types and N tokens, O(V^2) space.
    """
    if num_classes < 1:
        raise ValueError("num_classes must be at least 1")
    words = vocabulary(corpus)
    classes = [[w] for w in words]  # @line L1
    nodes = list(range(len(words)))
    n, total = bigram_counts(corpus, words)  # @line L2
    merges: list[Merge] = []
    k = len(words)  # @line L3
    while k > num_classes:  # @line L4
        left = [sum(row) for row in n]  # @line L5
        right = [sum(n[l][m] for l in range(k)) for m in range(k)]
        q = [[_q(n[l][m], left[l], right[m], total) for m in range(k)] for l in range(k)]
        s = [sum(q[l][i] for l in range(k)) + sum(q[i]) - q[i][i] for i in range(k)]
        ami = sum(map(sum, q))
        best = (0.0, -1, -1)
        for i in range(k):  # @line L6
            for j in range(i + 1, k):
                li, ri = left[i] + left[j], right[i] + right[j]
                v = ami - s[i] - s[j] + q[i][j] + q[j][i]  # @line L7
                v += _q(n[i][i] + n[i][j] + n[j][i] + n[j][j], li, ri, total)
                for l in range(k):
                    if l != i and l != j:
                        v += _q(n[l][i] + n[l][j], left[l], ri, total)
                        v += _q(n[i][l] + n[j][l], li, right[l], total)
                if best[1] < 0 or v > best[0] + 1e-12:  # @line L8
                    best = (v, i, j)
        v, i, j = best
        for m in range(k):  # @line L9
            n[i][m] += n[j][m]
        for l in range(k):
            n[l][i] += n[l][j]
        del n[j]
        for row in n:
            del row[j]
        classes[i] = classes[i] + classes[j]
        del classes[j]
        merges.append(Merge(nodes[i], nodes[j], len(words) + len(merges), v))  # @line L10
        nodes[i] = merges[-1].node
        del nodes[j]
        k -= 1
    return classes, merges  # @line L11


def bit_strings(corpus: list[list[str]]) -> dict[str, str]:
    """The path of each word in the full merge tree: 0 for left, 1 for right.

    The left child of a merge is the kept class. A corpus with one type
    gives that type the empty string.
    """
    words = vocabulary(corpus)
    if not words:
        return {}
    _, merges = brown_clustering(corpus, 1)
    children = {m.node: (m.left, m.right) for m in merges}
    root = merges[-1].node if merges else 0
    codes: dict[str, str] = {}
    stack = [(root, "")]
    while stack:
        node, code = stack.pop()
        if node < len(words):
            codes[words[node]] = code
        else:
            a, b = children[node]
            stack.append((a, code + "0"))
            stack.append((b, code + "1"))
    return codes
