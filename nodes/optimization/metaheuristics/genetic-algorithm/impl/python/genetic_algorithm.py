# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genetic-algorithm/. The authors are listed in prov/F1GKBX.jsonl.

import random
from collections.abc import Callable, Sequence
from fractions import Fraction
from typing import Union

Bits = tuple[int, ...]
Number = Union[int, float, Fraction]


def roulette_wheel_select(fitness: Sequence[Number], u: Number) -> int:
    """Return the index chosen by a roulette wheel for a point u in [0, 1).

    Precondition: each fitness is at least 0 and the sum is positive.
    Index i owns the interval [c(i-1), c(i)) of [0, total), where c is the
    prefix sum, so for a uniform u it is chosen with probability
    fitness[i] / total. Cost: O(len(fitness)).
    """
    total = sum(fitness)
    target = u * total
    acc: Number = 0
    last = 0
    for i, fi in enumerate(fitness):
        if fi > 0:
            last = i
        acc += fi
        if target < acc:
            return i
    return last  # only reached through rounding of floats


def tournament_winner(fitness: Sequence[Number], entrants: Sequence[int]) -> int:
    """The entrant with the largest fitness; on a tie, the one with the smallest index."""
    return max(entrants, key=lambda i: (fitness[i], -i))


def tournament_select(fitness: Sequence[Number], k: int, rng: random.Random) -> int:
    """Draw k indices uniformly with replacement and return the winner. Cost: O(k)."""
    entrants = [rng.randrange(len(fitness)) for _ in range(k)]
    return tournament_winner(fitness, entrants)


def one_point_crossover(a: Bits, b: Bits, cut: int) -> tuple[Bits, Bits]:
    """Swap the tails after position cut, for 1 <= cut <= len(a) - 1."""
    return a[:cut] + b[cut:], b[:cut] + a[cut:]


def uniform_crossover(a: Bits, b: Bits, mask: Sequence[int]) -> tuple[Bits, Bits]:
    """Child 1 takes position i from a when mask[i] = 1, else from b. Child 2 takes the other gene."""
    c = tuple(x if m else y for x, y, m in zip(a, b, mask))
    d = tuple(y if m else x for x, y, m in zip(a, b, mask))
    return c, d


def bit_flip_mutation(x: Bits, p_m: float, rng: random.Random) -> Bits:
    """Flip each bit independently with probability p_m. Cost: O(len(x))."""
    return tuple(1 - xi if rng.random() < p_m else xi for xi in x)


def next_generation(
    population: Sequence[Bits],
    f: Callable[[Bits], Number],
    p_c: float,
    p_m: float,
    elite: int,
    rng: random.Random,
    selection: str = "tournament",
    k: int = 2,
) -> list[Bits]:
    """Lines L4 to L9 of the page: one generation of the genetic algorithm.

    The elite strings with the largest fitness are copied first; then pairs
    of parents are selected, crossed with one-point crossover with
    probability p_c, and mutated bit by bit with probability p_m.
    Cost: O(N l) random numbers and N fitness calls.
    """
    n = len(population)
    fit = [f(x) for x in population]
    order = sorted(range(n), key=lambda i: (fit[i], -i), reverse=True)
    q = [population[i] for i in order[:elite]]  # @line L4
    length = len(population[0])
    while len(q) < n:  # @line L5
        if selection == "roulette":
            a = population[roulette_wheel_select(fit, rng.random())]  # @line L6
            b = population[roulette_wheel_select(fit, rng.random())]
        else:
            a = population[tournament_select(fit, k, rng)]
            b = population[tournament_select(fit, k, rng)]
        if rng.random() < p_c and length > 1:  # @line L7
            a, b = one_point_crossover(a, b, rng.randint(1, length - 1))
        a = bit_flip_mutation(a, p_m, rng)  # @line L8
        b = bit_flip_mutation(b, p_m, rng)
        q.append(a)  # @line L9
        if len(q) < n:
            q.append(b)
    return q


def genetic_algorithm(
    f: Callable[[Bits], Number],
    length: int,
    pop_size: int,
    p_c: float,
    p_m: float,
    elite: int,
    generations: int,
    rng: random.Random,
    selection: str = "tournament",
    k: int = 2,
    target: Number | None = None,
) -> tuple[Bits, Number, list[Number]]:
    """Maximize f over {0, 1}^length with a generational genetic algorithm.

    Returns (best, f(best), history), where history[t] is the largest fitness
    in the population of generation t. The run stops early when the best
    fitness reaches target. Precondition: f >= 0 when selection is
    "roulette". Cost: O(generations * pop_size * length) plus the fitness calls.
    """
    population = [tuple(rng.randint(0, 1) for _ in range(length)) for _ in range(pop_size)]  # @line L1
    best = max(population, key=f)  # @line L2
    history = [f(best)]
    for _ in range(generations):  # @line L3
        if target is not None and f(best) >= target:
            break
        population = next_generation(population, f, p_c, p_m, elite, rng, selection, k)  # @line L10
        top = max(population, key=f)
        history.append(f(top))
        if f(top) > f(best):  # @line L11
            best = top
    return best, f(best), history  # @line L12


def one_plus_one_ea(f: Callable[[Bits], Number], n: int, optimum: Number, rng: random.Random, max_steps: int) -> int:
    """The (1+1) EA with mutation rate 1/n. Returns the number of iterations until f(x) = optimum, or -1."""
    x = tuple(rng.randint(0, 1) for _ in range(n))
    fx = f(x)
    for t in range(max_steps + 1):
        if fx == optimum:
            return t
        y = bit_flip_mutation(x, 1.0 / n, rng)
        fy = f(y)
        if fy >= fx:
            x, fx = y, fy
    return -1


def onemax(x: Bits) -> int:
    """The number of ones."""
    return sum(x)
