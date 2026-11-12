# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incomplete-lineage-sorting/. The authors are listed in prov/W29D9B.jsonl.
"""Gene tree probabilities under incomplete lineage sorting.

A species tree is a leaf name (str) or a triple (left, right, b), where b is
the branch above that node. For simulation b is a length in coalescent units;
for the exact functions b is q = exp(-length), so a rational q gives exact
results. The root has b = None. One gene copy is sampled per species.
A gene tree is a leaf name or a pair; canon() puts it in a fixed form.
"""

import math
import random
from collections import defaultdict
from fractions import Fraction


def canon(tree):
    """A canonical form of a rooted gene tree, with an explicit stack."""
    out, stack = {}, [(tree, False)]
    while stack:
        x, done = stack.pop()
        if not isinstance(x, tuple):
            out[id(x)] = x
        elif done:
            a, b = out[id(x[0])], out[id(x[1])]
            out[id(x)] = (a, b) if repr(a) <= repr(b) else (b, a)
        else:
            stack.append((x, True))
            stack.extend((y, False) for y in x)
    return out[id(tree)]


def three_taxon(q):
    """(matching, each mismatching) probability for ((A,B),C) with q = exp(-T)."""
    return 1 - 2 * q / 3, q / 3


def caterpillar_four(q_young, q_old):
    """P(matching) and P(symmetric ((A,B),(C,D))) for the species tree
    (((A,B):y,C):x,D), with q_young = exp(-y) and q_old = exp(-x)."""
    y, x = q_young, q_old
    x3 = x ** 3
    one_in_old = x - x3  # no merge on the young branch, then exactly one of 3 on the old
    sym = y * (x3 / 9 + one_in_old / 6) + (1 - y) * x / 3
    match = (1 - y) * (1 - 2 * x / 3) + y * (
        (1 - x3 - 3 * one_in_old / 2) / 3 + one_in_old / 6 + x3 / 18
    )
    return match, sym


def anomaly_bound(x: float) -> float:
    """Degnan and Rosenberg's a(x): the caterpillar is in the anomaly zone iff y < a(x)."""
    e2, e3 = math.exp(2 * x), math.exp(3 * x)
    return math.log(2 / 3 + (3 * e2 - 2) / (18 * (e3 - e2)))


def _rising(a, k):
    return math.prod(range(a, a + k))


def _falling(a, k):
    return math.prod(range(a - k + 1, a + 1))


def lineage_count_probability(i: int, j: int, q):
    """Tavare's g_ij: P(i lineages become j in a branch with q = exp(-length)), j >= 1."""
    total = Fraction(0) if isinstance(q, (int, Fraction)) else 0.0
    for k in range(j, i + 1):
        num = (2 * k - 1) * (-1) ** (k - j) * _rising(j, k - 1) * _falling(i, k)
        den = math.factorial(j) * math.factorial(k - j) * _rising(i, k)
        total += q ** (k * (k - 1) // 2) * Fraction(num, den)
    return total


def _merge_down(lineages: tuple, j: int) -> dict:
    """Merge uniform random pairs until j lineages are left; exact law of the result."""
    dist = {tuple(sorted(lineages, key=repr)): Fraction(1)}
    for k in range(len(lineages), j, -1):
        nxt = defaultdict(Fraction)
        pairs = k * (k - 1) // 2
        for state, p in dist.items():
            for a in range(k):
                for b in range(a + 1, k):
                    rest = [state[c] for c in range(k) if c != a and c != b]
                    rest.append(canon((state[a], state[b])))
                    nxt[tuple(sorted(rest, key=repr))] += p / pairs
        dist = nxt
    return dist


def gene_tree_distribution(species) -> dict:
    """The exact law of the rooted gene tree topology under the multispecies
    coalescent, by enumeration over the lineages that leave each branch."""
    results, stack = {}, [(species, False)]
    while stack:
        node, done = stack.pop()
        if not isinstance(node, tuple):
            results[id(node)] = {(node,): Fraction(1)}
            continue
        if not done:
            stack.append((node, True))
            stack.extend((c, False) for c in node[:2])
            continue
        left, right, q = node
        out = defaultdict(Fraction)
        for s1, p1 in results[id(left)].items():
            for s2, p2 in results[id(right)].items():
                state, p = s1 + s2, p1 * p2
                i = len(state)
                ends = [(1, 1)] if q is None else [(j, lineage_count_probability(i, j, q)) for j in range(1, i + 1)]
                for j, g in ends:
                    if g == 0:
                        continue
                    for s3, p3 in _merge_down(state, j).items():
                        out[s3] += p * g * p3
        results[id(node)] = out
    return {state[0]: p for state, p in results[id(species)].items()}


def simulate_gene_tree(species, rng: random.Random):
    """Draw one gene tree under the multispecies coalescent (lengths, not q)."""
    results, stack = {}, [(species, False)]
    while stack:
        node, done = stack.pop()
        if not isinstance(node, tuple):
            results[id(node)] = [node]
            continue
        if not done:
            stack.append((node, True))
            stack.extend((c, False) for c in node[:2])
            continue
        left, right, length = node
        lin = results[id(left)] + results[id(right)]
        clock = 0.0
        while len(lin) > 1:
            k = len(lin)
            clock += rng.expovariate(k * (k - 1) / 2)
            if length is not None and clock > length:
                break
            a, b = rng.sample(range(k), 2)
            merged = (lin[a], lin[b])
            lin = [lin[c] for c in range(k) if c != a and c != b] + [merged]
        results[id(node)] = lin
    return canon(results[id(species)][0])


def unrooted_split(gene_tree, four: set) -> frozenset:
    """The quartet split ab|cd shown by a rooted binary gene tree on four leaves."""
    a, b = gene_tree
    for side in (a, b):
        if isinstance(side, tuple) and isinstance(side[0], str) and isinstance(side[1], str):
            pair = frozenset(side)
            return frozenset([pair, frozenset(four - pair)])
    # a caterpillar ((( x, y), z), w): the deepest cherry gives the split
    side = a if isinstance(a, tuple) else b
    while not (isinstance(side[0], str) and isinstance(side[1], str)):
        side = side[0] if isinstance(side[0], tuple) else side[1]
    pair = frozenset(side)
    return frozenset([pair, frozenset(four - pair)])
