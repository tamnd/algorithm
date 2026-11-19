# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mention-pair-model/. The authors are listed in prov/XJ8G58.jsonl.

"""The mention-pair model of coreference (Soon, Ng and Lim 2001; Ng and Cardie 2002).

Mentions are numbered 0 .. N-1 in document order. A gold clustering is a list
chain[k] that gives the gold entity of mention k (or None for a mention that
is in no chain).

- soon_instances: the training pairs of Soon et al. (Section 2.3);
- ng_cardie_instances: the same, with the closest non-pronominal antecedent
  as the positive pair of a non-pronominal anaphor (Ng and Cardie, Section 3);
- a logistic regression classifier with its loss and gradient (Soon et al.
  used a C5 decision tree; any classifier that gives P(coreferent) works);
- closest_first and best_first: the two ways to pick an antecedent;
- components: the clusters given by the links, with a union-find structure.

The classifier decides each pair alone, so its decisions need not be
transitive; only the clustering step makes the output a partition.
"""

import math
from typing import Callable, Dict, List, Optional, Sequence, Tuple

Pair = Tuple[int, int]


def soon_instances(chain: Sequence[Optional[int]]) -> List[Tuple[int, int, int]]:
    """Return (i, j, label) training pairs, i < j, as in Soon et al. (2001), Section 2.3.

    For each mention j that has an earlier mention of its chain, the closest such
    mention i gives a positive pair, and each mention strictly between i and j
    gives a negative pair with j.
    """
    out = []
    for j in range(len(chain)):
        if chain[j] is None:
            continue
        i = next((k for k in range(j - 1, -1, -1) if chain[k] == chain[j]), None)  # @line L1
        if i is None:
            continue
        out.append((i, j, 1))  # @line L2
        out.extend((k, j, 0) for k in range(i + 1, j))
    return out


def ng_cardie_instances(chain: Sequence[Optional[int]], is_pronoun: Sequence[bool]):
    """Training pairs as in Ng and Cardie (2002), Section 3: for a non-pronominal anaphor the
    positive antecedent is the closest non-pronominal mention of its chain, for a pronoun the
    closest mention of its chain. Negatives pair j with the mentions between i and j, as in
    Soon et al. The paper does not say what happens to mentions of the same chain between
    them; this code skips them, so no coreferent pair is labeled negative."""
    out = []
    for j in range(len(chain)):
        if chain[j] is None:
            continue
        ok = [k for k in range(j - 1, -1, -1) if chain[k] == chain[j]
              and (is_pronoun[j] or not is_pronoun[k])]
        if not ok:
            continue
        i = ok[0]
        out.append((i, j, 1))
        out.extend((k, j, 0) for k in range(i + 1, j) if chain[k] != chain[j])
    return out


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def log_loss(w: Sequence[float], data: Sequence[Tuple[Sequence[float], int]], l2: float = 0.0) -> float:
    """Mean negative log likelihood of logistic regression, plus (l2 / 2) |w|^2. Natural log."""
    total = 0.0
    for x, y in data:
        z = sum(a * b for a, b in zip(w, x))
        # log(1 + exp(-z)) for y = 1 and log(1 + exp(z)) for y = 0, computed stably
        t = -z if y == 1 else z
        total += max(t, 0.0) + math.log1p(math.exp(-abs(t)))
    return total / len(data) + 0.5 * l2 * sum(a * a for a in w)


def log_loss_grad(w, data, l2: float = 0.0) -> List[float]:
    """Gradient of log_loss: mean of (sigmoid(w . x) - y) x, plus l2 w."""
    g = [l2 * a for a in w]
    for x, y in data:
        r = (sigmoid(sum(a * b for a, b in zip(w, x))) - y) / len(data)
        for k, xk in enumerate(x):
            g[k] += r * xk
    return g


def train(data, dim: int, steps: int = 500, lr: float = 0.5, l2: float = 0.01) -> List[float]:
    """Logistic regression by plain gradient descent from w = 0."""
    w = [0.0] * dim
    for _ in range(steps):  # @line L3
        g = log_loss_grad(w, data, l2)
        w = [a - lr * b for a, b in zip(w, g)]
    return w


def closest_first(n: int, prob: Callable[[int, int], float], threshold: float = 0.5) -> List[Optional[int]]:
    """Soon et al. (2001), Section 2.5: link j to the closest i < j with prob(i, j) > threshold."""
    ante: List[Optional[int]] = [None] * n
    for j in range(1, n):  # @line L4
        for i in range(j - 1, -1, -1):  # @line L5
            if prob(i, j) > threshold:  # @line L6
                ante[j] = i
                break
    return ante


def best_first(n: int, prob: Callable[[int, int], float], threshold: float = 0.5) -> List[Optional[int]]:
    """Ng and Cardie (2002): link j to the i < j with the largest prob(i, j) above the threshold.
    On ties the closest i wins."""
    ante: List[Optional[int]] = [None] * n
    for j in range(1, n):
        best, arg = threshold, None
        for i in range(j - 1, -1, -1):
            p = prob(i, j)
            if p > best:
                best, arg = p, i
        ante[j] = arg
    return ante


class DisjointSet:
    """Union-find with path halving and union by size."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        a, b = self.find(a), self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]


def components(n: int, links: Sequence[Pair]) -> List[List[int]]:
    """The clusters of the links: the connected components, each sorted, ordered by first mention."""
    ds = DisjointSet(n)
    for i, j in links:  # @line L7
        ds.union(i, j)
    groups: Dict[int, List[int]] = {}
    for k in range(n):
        groups.setdefault(ds.find(k), []).append(k)
    return sorted(groups.values())


def clusters_from_antecedents(ante: Sequence[Optional[int]]) -> List[List[int]]:
    return components(len(ante), [(i, j) for j, i in enumerate(ante) if i is not None])


def non_transitive_triples(n: int, prob: Callable[[int, int], float], threshold: float = 0.5):
    """All triples a < b < c where two of the three pairs are classified coreferent and the third is not."""
    out = []
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                yes = [prob(a, b) > threshold, prob(b, c) > threshold, prob(a, c) > threshold]
                if sum(yes) == 2:
                    out.append((a, b, c))
    return out
