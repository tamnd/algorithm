# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-gcd/. The authors are listed in prov/FT9662.jsonl.

"""Bernstein's batch GCD.

batch_gcd(values) returns, for each i, g_i = gcd(a_i, product of the a_j
with j != i), using a product tree and a remainder tree. Then g_i > 1 exactly
when a_i shares a factor with another input. Signs are ignored. Zero is
allowed: gcd(0, x) = |x|, so a single zero gets the product of the others,
and every other entry a_j gets |a_j|. The empty product is 1.
shared_factor_pairs finishes the job and lists the pairs with a common factor.
"""


def euclid_gcd(a: int, b: int) -> int:
    """gcd(a, b) >= 0 by the Euclidean algorithm."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def product_tree(values: list[int]) -> list[list[int]]:
    """Levels of the product tree, leaves first; the last level is [product]."""
    tree = [list(values)]  # @line L1
    h = 0  # @line L2
    while len(tree[h]) > 1:  # @line L3
        level = tree[h]
        tree.append(  # @line L4
            [level[j] * level[j + 1] for j in range(0, len(level) - 1, 2)]
            + ([level[-1]] if len(level) % 2 else [])
        )
        h += 1  # @line L5
    return tree


def _batch_positive(values: list[int]) -> list[int]:
    tree = product_tree(values)
    h = len(tree) - 1
    rem = tree[h]  # @line L6
    for level in range(h - 1, -1, -1):  # @line L7
        nodes = tree[level]
        rem = [rem[j // 2] % (nodes[j] * nodes[j]) for j in range(len(nodes))]  # @line L8
    g = []
    for i, a in enumerate(values):  # @line L9
        g.append(euclid_gcd(a, rem[i] // a))  # @line L10
    return g  # @line L11


def batch_gcd(values: list[int]) -> list[int]:
    """[gcd(a_i, prod_{j != i} a_j) for each i]."""
    a = [abs(x) for x in values]
    zeros = [i for i, x in enumerate(a) if x == 0]
    if len(zeros) >= 2:
        return [0 if x == 0 else x for x in a]
    if len(zeros) == 1:
        rest = 1
        for x in a:
            if x != 0:
                rest *= x
        return [rest if x == 0 else x for x in a]
    if not a:
        return []
    return _batch_positive(a)


def shared_factor_pairs(values: list[int]) -> list[tuple[int, int, int]]:
    """All (i, j, gcd(a_i, a_j)) with i < j and gcd(a_i, a_j) > 1.

    Batch GCD flags the inputs that share a factor with some other input;
    pairwise gcds are then taken among the flagged inputs only.
    """
    g = batch_gcd(values)
    flagged = [i for i in range(len(values)) if g[i] != 1]
    pairs = []
    for x in range(len(flagged)):
        for y in range(x + 1, len(flagged)):
            i, j = flagged[x], flagged[y]
            d = euclid_gcd(values[i], values[j])
            if d != 1:
                pairs.append((i, j, d))
    return pairs
