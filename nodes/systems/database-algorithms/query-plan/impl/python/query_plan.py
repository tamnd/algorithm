# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/query-plan/. The authors are listed in prov/MHRFHJ.jsonl.
"""Join trees of a query plan: enumerate the shapes and count them.

A join tree is a relation name (a leaf) or a pair (left, right).
The left input is the outer input and the right input is the inner input,
so (A, B) and (B, A) are different trees.
"""

from itertools import combinations, permutations
from math import comb, factorial


def left_deep_trees(rels):
    """Yield each left-deep tree: every right input is a leaf."""
    for order in permutations(rels):
        tree = order[0]
        for r in order[1:]:
            tree = (tree, r)
        yield tree


def bushy_trees(rels):
    """Yield each join tree with the leaves rels, each leaf used once."""
    rels = tuple(rels)
    if len(rels) == 1:
        yield rels[0]
        return
    first, rest = rels[0], rels[1:]
    # Split rels into two nonempty parts. Fix the part of `first` to
    # avoid a double count, then put that part on the left and on the right.
    for k in range(0, len(rest)):
        for chosen in combinations(rest, k):
            part1 = (first,) + chosen
            part2 = tuple(r for r in rest if r not in chosen)
            if not part2:
                continue
            for t1 in bushy_trees(part1):
                for t2 in bushy_trees(part2):
                    yield (t1, t2)
                    yield (t2, t1)


def is_left_deep(tree):
    while isinstance(tree, tuple):
        if isinstance(tree[1], tuple):
            return False
        tree = tree[0]
    return True


def is_right_deep(tree):
    while isinstance(tree, tuple):
        if isinstance(tree[0], tuple):
            return False
        tree = tree[1]
    return True


def is_zigzag(tree):
    """Each join has at least one leaf input."""
    while isinstance(tree, tuple):
        left, right = tree
        if isinstance(left, tuple) and isinstance(right, tuple):
            return False
        tree = left if isinstance(left, tuple) else right
    return True


def count_left_deep(n):
    return factorial(n)


def count_bushy(n):
    """(2(n - 1))! / (n - 1)!, which equals n! times the Catalan number C(n - 1)."""
    return factorial(2 * (n - 1)) // factorial(n - 1)


def catalan(m):
    return comb(2 * m, m) // (m + 1)


def leaves(tree):
    out, stack = [], [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, tuple):
            stack.append(t[1])
            stack.append(t[0])
        else:
            out.append(t)
    return out


def show(tree):
    if isinstance(tree, tuple):
        return "(" + show(tree[0]) + " ⋈ " + show(tree[1]) + ")"
    return str(tree)
