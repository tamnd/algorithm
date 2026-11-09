# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genetic-programming/. The authors are listed in prov/R0CA6Z.jsonl.

import random
from collections.abc import Callable, Sequence
from typing import Union

# A tree is the terminal "x", an integer constant, or a tuple (op, left, right).
Tree = Union[str, int, tuple]

FUNCTIONS = ("add", "sub", "mul")
TERMINALS: tuple[Tree, ...] = ("x", 1)


def evaluate(tree: Tree, x: int) -> int:
    """The value of the expression tree at x. Cost: O(size(tree))."""
    if tree == "x":
        return x
    if isinstance(tree, int):
        return tree
    op, a, b = tree
    u, v = evaluate(a, x), evaluate(b, x)
    if op == "add":
        return u + v
    if op == "sub":
        return u - v
    return u * v


def size(tree: Tree) -> int:
    """The number of nodes."""
    return 1 + size(tree[1]) + size(tree[2]) if isinstance(tree, tuple) else 1


def depth(tree: Tree) -> int:
    """The number of edges on the longest path from the root to a leaf; a terminal has depth 0."""
    return 1 + max(depth(tree[1]), depth(tree[2])) if isinstance(tree, tuple) else 0


def full(d: int, rng: random.Random) -> Tree:
    """A random tree in which every leaf has depth exactly d."""
    if d == 0:
        return rng.choice(TERMINALS)
    return (rng.choice(FUNCTIONS), full(d - 1, rng), full(d - 1, rng))


def grow(d: int, rng: random.Random) -> Tree:
    """A random tree of depth at most d: each node above depth d is drawn uniformly from functions and terminals."""
    if d == 0:
        return rng.choice(TERMINALS)
    k = rng.randrange(len(FUNCTIONS) + len(TERMINALS))
    if k >= len(FUNCTIONS):
        return TERMINALS[k - len(FUNCTIONS)]
    return (FUNCTIONS[k], grow(d - 1, rng), grow(d - 1, rng))


def ramped_half_and_half(n: int, d_min: int, d_max: int, rng: random.Random) -> list[Tree]:
    """Tree i has depth limit d_min + (i // 2) mod (d_max - d_min + 1); it is built by full for even i and by grow for odd i."""
    ramp = d_max - d_min + 1
    return [(full if i % 2 == 0 else grow)(d_min + (i // 2) % ramp, rng) for i in range(n)]


def subtree_at(tree: Tree, i: int) -> Tree:
    """The subtree rooted at the node with preorder index i (the root has index 0)."""
    if i == 0:
        return tree
    _, a, b = tree
    sa = size(a)
    return subtree_at(a, i - 1) if i - 1 < sa else subtree_at(b, i - 1 - sa)


def replace_at(tree: Tree, i: int, sub: Tree) -> Tree:
    """A copy of tree in which the subtree at preorder index i is replaced by sub."""
    if i == 0:
        return sub
    op, a, b = tree
    sa = size(a)
    if i - 1 < sa:
        return (op, replace_at(a, i - 1, sub), b)
    return (op, a, replace_at(b, i - 1 - sa, sub))


def subtree_crossover(a: Tree, b: Tree, rng: random.Random) -> Tree:
    """Replace a uniform random subtree of a by a uniform random subtree of b. Cost: O(size(a) + size(b))."""
    i = rng.randrange(size(a))
    j = rng.randrange(size(b))
    return replace_at(a, i, subtree_at(b, j))


def subtree_mutation(a: Tree, d: int, rng: random.Random) -> Tree:
    """Replace a uniform random subtree of a by a new tree from grow(d)."""
    i = rng.randrange(size(a))
    return replace_at(a, i, grow(d, rng))


def total_error(tree: Tree, cases: Sequence[tuple[int, int]]) -> int:
    """The sum of |tree(x) - y| over the fitness cases (x, y)."""
    return sum(abs(evaluate(tree, x) - y) for x, y in cases)


def tournament(errors: Sequence[int], k: int, rng: random.Random) -> int:
    """Draw k indices with replacement; return the one with the smallest error, the first drawn on a tie."""
    entrants = [rng.randrange(len(errors)) for _ in range(k)]
    return min(entrants, key=lambda i: errors[i])


def genetic_programming(
    cases: Sequence[tuple[int, int]],
    n: int,
    generations: int,
    k: int,
    p_c: float,
    p_m: float,
    elites: int,
    init_depth: int,
    max_depth: int,
    mut_depth: int,
    rng: random.Random,
    on_generation: Callable[[int, list[Tree], list[int]], None] | None = None,
) -> tuple[Tree, int, list[int]]:
    """Generational tree GP for symbolic regression with functions + - * and terminals x and 1.

    Each generation copies the `elites` best trees, then fills the population
    with children: subtree crossover with probability p_c, subtree mutation
    with probability p_m, otherwise a copy, each from tournament parents of
    size k. A child deeper than max_depth is replaced by its first parent.
    Stops after `generations` generations or when the error is 0.
    Precondition: n > elites >= 1, 2 <= init_depth <= max_depth, mut_depth <= max_depth.
    Returns (best tree, its error, history of the best error).
    Cost: O(generations * n * (S * len(cases) + k)) time for trees of at most S nodes.
    """
    pop = ramped_half_and_half(n, 2, init_depth, rng)  # @line L1
    errors = [total_error(t, cases) for t in pop]  # @line L2
    history = [min(errors)]
    g = 0
    while g < generations and min(errors) > 0:  # @line L3
        g += 1
        order = sorted(range(n), key=lambda i: errors[i])
        new = [pop[i] for i in order[:elites]]  # @line L4
        while len(new) < n:  # @line L5
            r = rng.random()
            a = pop[tournament(errors, k, rng)]
            if r < p_c:  # @line L6
                child = subtree_crossover(a, pop[tournament(errors, k, rng)], rng)
            elif r < p_c + p_m:  # @line L7
                child = subtree_mutation(a, mut_depth, rng)
            else:
                child = a  # @line L8
            if depth(child) > max_depth:  # @line L9
                child = a
            new.append(child)  # @line L10
        pop = new  # @line L11
        errors = [total_error(t, cases) for t in pop]
        history.append(min(errors))
        if on_generation is not None:
            on_generation(g, list(pop), list(errors))
    b = min(range(n), key=lambda i: errors[i])
    return pop[b], errors[b], history  # @line L12
