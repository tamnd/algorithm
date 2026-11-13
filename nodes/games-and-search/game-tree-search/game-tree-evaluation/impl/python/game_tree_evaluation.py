# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/game-tree-evaluation/. The authors are listed in prov/1ZVZRX.jsonl.

"""Evaluation of Boolean game trees written as NAND trees.

A tree is a leaf, the int 0 or 1, or a tuple of subtrees. An inner node has the
value NAND of its children: 1 if some child is 0, and 0 if all children are 1.
A NAND tree is a game tree with values 0 and 1 for the side to move, so its
value is a negamax value: a position is won (1) when some move leads to a
position that is lost (0) for the opponent.

The cost of an evaluation is the number of leaves it reads.
"""

import itertools
import random
from fractions import Fraction
from functools import lru_cache
from typing import Callable, List, Optional, Tuple, Union

Tree = Union[int, tuple]


class LeafCounter:
    def __init__(self) -> None:
        self.reads = 0


def nand_value(t: Tree) -> int:
    """Reference value: read every leaf."""
    if not isinstance(t, tuple):
        return t
    return 0 if all(nand_value(c) == 1 for c in t) else 1


def r_eval(t: Tree, rng: random.Random, counter: LeafCounter) -> int:
    """Snir's randomized evaluation: try the children in a random order and
    stop at the first child of value 0."""
    if not isinstance(t, tuple):
        counter.reads += 1
        return t
    order = list(t)
    rng.shuffle(order)
    for c in order:
        if r_eval(c, rng, counter) == 0:
            return 1
    return 0


def left_first_eval(t: Tree, counter: LeafCounter) -> int:
    """The deterministic version: children from left to right, with the same stop."""
    if not isinstance(t, tuple):
        counter.reads += 1
        return t
    for c in t:
        if left_first_eval(c, counter) == 0:
            return 1
    return 0


@lru_cache(maxsize=None)
def expected_reads(t: Tree) -> Fraction:
    """Exact expected number of leaves that r_eval reads on t, as a Fraction.
    The cost of a child does not depend on when it is evaluated, so the
    expectation is the mean, over all orders, of the costs up to the first
    child of value 0."""
    if not isinstance(t, tuple):
        return Fraction(1)
    total = Fraction(0)
    perms = list(itertools.permutations(range(len(t))))
    for p in perms:
        for i in p:
            total += expected_reads(t[i])
            if nand_value(t[i]) == 0:
                break
    return total / len(perms)


def worst_case_recurrence(h: int) -> Tuple[Fraction, Fraction]:
    """(C0, C1) for the uniform binary tree of height h: the largest expected
    cost of r_eval over inputs whose value is 0, and over inputs whose value is 1.
    C0(h) = 2 C1(h-1), and C1(h) = C0(h-1) + C1(h-1) / 2."""
    c0, c1 = Fraction(1), Fraction(1)
    for _ in range(h):
        c0, c1 = 2 * c1, c0 + c1 / 2
    return c0, c1


def uniform_trees(h: int):
    """All uniform binary trees of height h (2 ** (2 ** h) of them)."""
    if h == 0:
        yield 0
        yield 1
        return
    subs = list(uniform_trees(h - 1))
    for a in subs:
        for b in subs:
            yield (a, b)


def adversary_tree(h: int, value: int) -> Tree:
    """A uniform binary tree of height h with the given value on which
    left_first_eval reads every leaf: the left child of every inner node is 1."""
    if h == 0:
        return value
    if value == 0:
        return (adversary_tree(h - 1, 1), adversary_tree(h - 1, 1))
    return (adversary_tree(h - 1, 1), adversary_tree(h - 1, 0))


class Adversary:
    """Answers leaf queries on the uniform binary tree of height h so that the
    root value stays open until every leaf has been read. A node is fixed only
    when all its leaves have been read. The first child of a node to be fixed
    gets the value 1, which does not decide a NAND; the second child then
    decides it, and the adversary picks its value to give the parent the value
    that the parent needs."""

    def __init__(self, h: int) -> None:
        self.h = h
        self.n = 2 ** h
        self.value: dict = {}  # (level, index) -> value of a fixed node; level 0 is the leaves

    def _fixed(self, level: int, index: int) -> bool:
        return (level, index) in self.value

    def _needed(self, level: int, index: int) -> int:
        if level == self.h:
            return 0  # any value will do at the root
        sibling = index ^ 1
        if not self._fixed(level, sibling):
            return 1
        # The sibling is fixed to 1, so the parent is NAND(1, x) = 1 - x.
        return 1 - self._needed(level + 1, index // 2)

    def query(self, leaf: int) -> int:
        if self._fixed(0, leaf):
            return self.value[(0, leaf)]
        v = self._needed(0, leaf)
        self.value[(0, leaf)] = v
        level, index = 0, leaf
        while level < self.h and self._fixed(level, index ^ 1):
            a = self.value[(level, index & ~1)]
            b = self.value[(level, index | 1)]
            level, index = level + 1, index // 2
            self.value[(level, index)] = 0 if a == 1 and b == 1 else 1
        return v


def root_known(h: int, known: dict) -> Optional[int]:
    """Value of the root if the leaves in `known` already decide it, else None."""

    def val(level: int, index: int) -> Optional[int]:
        if level == 0:
            return known.get(index)
        a, b = val(level - 1, 2 * index), val(level - 1, 2 * index + 1)
        if a == 0 or b == 0:
            return 1
        if a == 1 and b == 1:
            return 0
        return None

    return val(h, 0)


def run_query_algorithm(h: int, choose: Callable[[dict, List[int]], int], answer: Callable[[int], int]) -> Tuple[int, int]:
    """Run a deterministic query algorithm: `choose(known, unread)` picks the
    next leaf, and the algorithm stops as soon as the root value is decided.
    Return (root value, number of leaves read)."""
    known: dict = {}
    while True:
        r = root_known(h, known)
        if r is not None:
            return r, len(known)
        unread = [i for i in range(2 ** h) if i not in known]
        leaf = choose(known, unread)
        known[leaf] = answer(leaf)
