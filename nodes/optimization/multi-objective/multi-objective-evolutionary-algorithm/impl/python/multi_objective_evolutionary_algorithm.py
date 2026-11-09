# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-evolutionary-algorithm/. The authors are listed in prov/1SG8N5.jsonl.

"""The generic loop of a multi-objective evolutionary algorithm, an unbounded
elitist archive, and GSEMO on bit strings.

All objectives are minimized. A solution is stored with its image as a pair
(x, y) with y = f(x). The archive keeps one solution for each non-dominated
image among all images seen so far.
"""

import random
from typing import Callable, Sequence

Vector = Sequence[float]


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for u, v in zip(a, b):
        if u > v:
            return False
        if u < v:
            strict = True
    return strict


def weakly_dominates(a: Vector, b: Vector) -> bool:
    return all(u <= v for u, v in zip(a, b))


def update_archive(archive: list, x, y) -> bool:
    """Offer (x, y) to an unbounded elitist archive. Return True when it is stored.

    The new pair is rejected when an archive image weakly dominates y. Otherwise
    the members whose image y dominates are removed and the pair is added.
    """
    if any(weakly_dominates(b, y) for _, b in archive):
        return False
    archive[:] = [(u, b) for u, b in archive if not dominates(y, b)]
    archive.append((x, y))
    return True


def moea(
    init: Callable[[random.Random], list],
    f: Callable,
    fitness: Callable[[list], list],
    select: Callable[[list, list, random.Random], list],
    vary: Callable[[list, random.Random], list],
    survive: Callable[[list, list, int, random.Random], list],
    n: int,
    generations: int,
    rng: random.Random,
    on_generation: Callable[[list, list, list], None] | None = None,
) -> tuple[list, list]:
    """Run the generic loop. Return (population, archive) as lists of (x, y).

    init(rng) returns n solutions; fitness(P) returns one value per member;
    select(P, phi, rng) returns parents; vary(parents, rng) returns offspring;
    survive(P, Q, n, rng) returns n pairs from P + Q. on_generation(P, A, Q)
    is called after each generation, for tests.
    """
    pop = [(x, tuple(f(x))) for x in init(rng)]  # @line L1
    archive: list = []
    for x, y in pop:  # @line L2
        update_archive(archive, x, y)
    for _ in range(generations):  # @line L3
        phi = fitness(pop)  # @line L4
        parents = select(pop, phi, rng)  # @line L5
        off = [(x, tuple(f(x))) for x in vary(parents, rng)]  # @line L6
        for x, y in off:  # @line L7
            update_archive(archive, x, y)
        pop = survive(pop, off, n, rng)  # @line L8
        if on_generation is not None:
            on_generation(pop, archive, off)
    return pop, archive  # @line L9


# ---------------------------------------------------------------------------
# Bit strings: GSEMO and two test functions.


def lotz(x: Sequence[int]) -> tuple[int, int]:
    """LeadingOnes and TrailingZeros, both maximized, given as (-LO, -TZ) for minimization."""
    n = len(x)
    lo = next((i for i, b in enumerate(x) if b == 0), n)
    tz = next((i for i, b in enumerate(reversed(x)) if b == 1), n)
    return (-lo, -tz)


def one_min_max(x: Sequence[int]) -> tuple[int, int]:
    """(number of ones, number of zeros). Every bit string is Pareto-optimal."""
    ones = sum(x)
    return (ones, len(x) - ones)


def bit_flip(x: Sequence[int], rng: random.Random) -> tuple[int, ...]:
    """Standard bit mutation: flip each bit with probability 1/n."""
    n = len(x)
    return tuple(b ^ 1 if rng.random() < 1 / n else b for b in x)


def gsemo(
    n: int,
    f: Callable,
    steps: int,
    rng: random.Random,
    on_step: Callable[[list, tuple, tuple], None] | None = None,
) -> list:
    """Global SEMO. The population is itself an unbounded elitist archive.

    Each step picks a member uniformly at random, applies standard bit
    mutation, and offers the child. The child is rejected when a member
    dominates it; otherwise it replaces every member that it weakly dominates,
    so a child with the same image as a member takes its place.
    """
    x0 = tuple(rng.randint(0, 1) for _ in range(n))
    pop = [(x0, tuple(f(x0)))]
    for _ in range(steps):
        parent, _ = rng.choice(pop)
        child = bit_flip(parent, rng)
        y = tuple(f(child))
        if not any(dominates(b, y) for _, b in pop):
            pop = [(u, b) for u, b in pop if not weakly_dominates(y, b)]
            pop.append((child, y))
        if on_step is not None:
            on_step(pop, child, y)
    return pop
