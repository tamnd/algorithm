# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yule-model/. The authors are listed in prov/CV9KCF.jsonl.
"""The Yule pure-birth model: a simulator and the exact tree probabilities.

A tree is a leaf label (an int) or a pair (left, right) of trees. A ranked
tree shape is None for a leaf or a triple (rank, left, right), where rank 1
is the root split and rank n - 1 is the last split.
"""

import math
import random
from fractions import Fraction


def grow(choices: list) -> tuple:
    """Replay a split sequence. choices[k - 1] in 0..k-1 is the position of
    the lineage that splits while k lineages exist; the split lineage keeps
    its position and its new sister goes to the end of the list.

    Returns (children, rank, tips): children[x] = (a, b) for each split node x,
    rank[x] = k for the k-th split, and tips lists the n leaf nodes in order.
    """
    children, rank, tips, nxt = {}, {}, [0], 1
    for k, i in enumerate(choices, start=1):
        assert 0 <= i < k
        x = tips[i]
        children[x], rank[x] = (nxt, nxt + 1), k
        tips[i] = nxt
        tips.append(nxt + 1)
        nxt += 2
    return children, rank, tips


def labeled_tree(children: dict, tips: list, labels: list):
    """The topology of a grown tree, with labels[j] on tips[j]."""
    name = dict(zip(tips, labels))
    built, stack = {}, [0]
    while stack:
        x = stack[-1]
        if x in name:
            built[x] = name[x]
            stack.pop()
        elif x in children and all(c in built for c in children[x]):
            a, b = children[x]
            built[x] = (built[a], built[b])
            stack.pop()
        else:
            stack.extend(children[x])
    return built[0]


def ranked_shape(children: dict, rank: dict):
    """The ranked tree shape of a grown tree, in a canonical child order."""
    built, stack = {}, [0]
    while stack:
        x = stack[-1]
        if x not in children:
            built[x] = None
            stack.pop()
        elif all(c in built for c in children[x]):
            a, b = sorted((built[c] for c in children[x]), key=repr)
            built[x] = (rank[x], a, b)
            stack.pop()
        else:
            stack.extend(children[x])
    return built[0]


def simulate(n: int, rate: float, rng: random.Random):
    """Grow a Yule tree from one lineage until it has n >= 1 lineages.

    Each lineage splits at the given rate, so with k lineages the waiting
    time is exponential with rate k * rate and the lineage that splits is
    uniform. Labels 0..n-1 go to the tips in a uniform random order.
    Returns (tree, shape, times), where times[k - 1] is the time with k lineages.
    """
    times, choices = [], []  # @line L1: the lineages start as [root]
    for k in range(1, n):  # @line L2
        times.append(rng.expovariate(k * rate))  # @line L3
        choices.append(rng.randrange(k))  # @line L4
    children, rank, tips = grow(choices)  # @line L5: grow replays the splits
    labels = list(range(n))  # @line L6
    rng.shuffle(labels)
    return labeled_tree(children, tips, labels), ranked_shape(children, rank), times  # @line L7


def clusters(tree) -> frozenset:
    """The set of leaf sets below the internal nodes. Two rooted binary
    trees on the same labels have the same topology iff these sets agree."""
    out, stack = [], [tree]
    while stack:
        x = stack.pop()
        if isinstance(x, tuple):
            out.append(frozenset(leaves(x)))
            stack.extend(x)
    return frozenset(out)


def leaves(tree) -> list:
    """The leaf labels of a tree, with an explicit stack."""
    out, stack = [], [tree]
    while stack:
        x = stack.pop()
        if isinstance(x, tuple):
            stack.extend(x)
        else:
            out.append(x)
    return out


def internal_clade_sizes(tree) -> list:
    """The number of leaves below each internal node."""
    sizes, stack = [], [tree]
    while stack:
        x = stack.pop()
        if isinstance(x, tuple):
            sizes.append(len(leaves(x)))
            stack.extend(x)
    return sizes


def topology_probability(tree) -> Fraction:
    """P(T) = 2^(n-1) / (n! * prod over internal v of (n_v - 1))."""
    n = len(leaves(tree))
    p = Fraction(2 ** (n - 1), math.factorial(n))
    for s in internal_clade_sizes(tree):
        p /= s - 1
    return p


def number_of_rankings(tree) -> int:
    """The orders of the splits that respect ancestry: (n-1)! / prod (n_v - 1)."""
    n = len(leaves(tree))
    r = Fraction(math.factorial(n - 1))
    for s in internal_clade_sizes(tree):
        r /= s - 1
    assert r.denominator == 1
    return int(r)


def cherries(tree) -> int:
    """The number of internal nodes whose two children are leaves."""
    count, stack = 0, [tree]
    while stack:
        x = stack.pop()
        if isinstance(x, tuple):
            if not isinstance(x[0], tuple) and not isinstance(x[1], tuple):
                count += 1
            stack.extend(x)
    return count


def shape_cherries(shape) -> tuple:
    """(internal nodes, cherries) of a ranked tree shape."""
    internal = cher = 0
    stack = [shape]
    while stack:
        x = stack.pop()
        if x is not None:
            internal += 1
            if x[1] is None and x[2] is None:
                cher += 1
            stack.extend((x[1], x[2]))
    return internal, cher


def ranked_shape_probability(shape) -> Fraction:
    """P(ranked shape) = 2^(n-1-c) / (n-1)!, with c the number of cherries."""
    internal, c = shape_cherries(shape)
    return Fraction(2 ** (internal - c), math.factorial(internal))


def labeled_history_count(n: int) -> int:
    """The number of ranked labeled histories: n! (n-1)! / 2^(n-1)."""
    return math.factorial(n) * math.factorial(n - 1) // 2 ** (n - 1)
