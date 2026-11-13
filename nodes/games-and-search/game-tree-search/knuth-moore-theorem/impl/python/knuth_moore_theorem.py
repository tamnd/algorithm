# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-moore-theorem/. The authors are listed in prov/AZCEZ2.jsonl.

"""Tools to check the Knuth-Moore theorem on small trees.

Trees are nested lists. A leaf is a number, an inner node is a non-empty list
of children. Unless a function says otherwise, leaves hold values for MAX and
MAX moves at the root.
"""

import math
from itertools import combinations
from typing import List, Optional, Sequence, Union

INF = math.inf
Tree = Union[int, list]


def minimal_tree_size(b: int, d: int) -> int:
    """The Knuth-Moore count b^ceil(d/2) + b^floor(d/2) - 1."""
    return b ** ((d + 1) // 2) + b ** (d // 2) - 1


def build_uniform(leaves: Sequence, b: int, d: int) -> Tree:
    """The uniform tree of degree b and height d with the given leaves, left to right."""
    if d == 0:
        return leaves[0]
    k = len(leaves) // b
    return [build_uniform(leaves[i * k : (i + 1) * k], b, d - 1) for i in range(b)]


def minimax(tree: Tree, max_to_move: bool = True):
    """Plain minimax value, the reference."""
    if not isinstance(tree, list):
        return tree
    vals = [minimax(c, not max_to_move) for c in tree]
    return max(vals) if max_to_move else min(vals)


def to_negamax(tree: Tree, max_to_move: bool = True) -> Tree:
    """Turn MAX-view leaves into values for the side to move."""
    if not isinstance(tree, list):
        return tree if max_to_move else -tree
    return [to_negamax(c, not max_to_move) for c in tree]


def alpha_beta(tree: Tree, alpha=-INF, beta=INF, fail_soft: bool = True, visited: Optional[List[tuple]] = None, path: tuple = ()):
    """F2 of Knuth and Moore (fail_soft=False) or its fail-soft form, on a negamax tree.

    The path of each evaluated leaf is appended to `visited`.
    """
    if not isinstance(tree, list):
        if visited is not None:
            visited.append(path)
        return tree
    m = -INF if fail_soft else alpha
    for i, c in enumerate(tree):
        t = -alpha_beta(c, -beta, -max(m, alpha), fail_soft, visited, path + (i,))
        if t > m:
            m = t
        if m >= beta:
            return m
    return m


def perfectly_ordered(tree: Tree, max_to_move: bool = True) -> Tree:
    """Reorder the children so that the first child of every inner node is a best move.

    The sort is stable, so among equal children the old order is kept.
    """
    if not isinstance(tree, list):
        return tree
    kids = [perfectly_ordered(c, not max_to_move) for c in tree]
    kids.sort(key=lambda c: minimax(c, not max_to_move), reverse=max_to_move)
    return kids


def worst_first(tree: Tree, max_to_move: bool = True) -> Tree:
    """Reorder the children of every node so that the worst move for the mover comes first."""
    if not isinstance(tree, list):
        return tree
    kids = [worst_first(c, not max_to_move) for c in tree]
    kids.sort(key=lambda c: minimax(c, not max_to_move), reverse=not max_to_move)
    return kids


def no_cutoff_tree(values: Sequence, b: int, d: int, max_to_move: bool = True) -> Tree:
    """A uniform tree on which alpha-beta makes no cutoff (Knuth and Moore, Section 7).

    `values` must be distinct; they are sorted and dealt out so that, at every
    node, every leaf below an earlier child is worse for the mover than every
    leaf below a later child.
    """
    vals = sorted(values)
    if d == 0:
        return vals[0]
    k = len(vals) // b
    chunks = [vals[i * k : (i + 1) * k] for i in range(b)]
    if not max_to_move:
        chunks.reverse()
    return [no_cutoff_tree(ch, b, d - 1, not max_to_move) for ch in chunks]


def is_critical(path: tuple) -> bool:
    """Knuth and Moore: a_1 ... a_l is critical if a_i = 1 for all even i or for all odd i.

    Paths here count children from 0, so the test is on the entries equal to 0.
    """
    return all(x == 0 for x in path[0::2]) or all(x == 0 for x in path[1::2])


def leaf_paths(tree: Tree, path: tuple = ()) -> List[tuple]:
    if not isinstance(tree, list):
        return [path]
    out = []
    for i, c in enumerate(tree):
        out.extend(leaf_paths(c, path + (i,)))
    return out


def value_with(tree: Tree, seen: set, fill, path: tuple = (), max_to_move: bool = True):
    """Minimax value after every leaf outside `seen` is replaced by `fill`."""
    if not isinstance(tree, list):
        return tree if path in seen else fill
    vals = [value_with(c, seen, fill, path + (i,), not max_to_move) for i, c in enumerate(tree)]
    return max(vals) if max_to_move else min(vals)


def determines(tree: Tree, seen: set, low, high) -> bool:
    """Does the set `seen` of leaves fix the value for all values of the other leaves in [low, high]?

    The value is monotone in each leaf, so the two extreme fillings suffice.
    """
    return value_with(tree, seen, low) == value_with(tree, seen, high)


def smallest_proof(tree: Tree, low, high) -> int:
    """Size of a smallest set of leaves that fixes the value, by brute force over all subsets."""
    leaves = leaf_paths(tree)
    for size in range(len(leaves) + 1):
        for subset in combinations(leaves, size):
            if determines(tree, set(subset), low, high):
                return size
    raise AssertionError("the full set of leaves always fixes the value")
