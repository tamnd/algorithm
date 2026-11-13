# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bbht-search/. The authors are listed in prov/TE4YP7.jsonl.
"""BBHT search (Boyer, Brassard, Hoyer and Tapp) on the qs1 state-vector simulator.

The search space is {0, 1, ..., N - 1}, and f(x) is 1 for a marked item.
The number M of marked items is not an input. The algorithm sees f only
through the phase oracle |x> -> (-1)^f(x) |x>, and checks each measured item
with one classical evaluation of f. Qubit 0 is the least significant bit of x.
"""

import math
import random
from fractions import Fraction
from typing import Callable, Optional

from qsim import apply_diagonal, probabilities, sample

Oracle = Callable[[int], int]

LAMBDA = Fraction(6, 5)


def num_qubits(n_items: int) -> int:
    if n_items < 1:
        raise ValueError("n_items must be at least 1")
    return max(1, (n_items - 1).bit_length())


def uniform_state(n_items: int) -> list[complex]:
    """|s> on num_qubits(N) qubits; the indices x >= N have amplitude 0."""
    amp = 1.0 / math.sqrt(n_items)
    return [amp + 0j if x < n_items else 0j for x in range(1 << num_qubits(n_items))]


def grover_iteration(state: list[complex], n_items: int, f: Oracle) -> None:
    """G = D O_f: one query, then a_x -> 2 mean - a_x on the N items."""
    apply_diagonal(state, lambda x: -1.0 if x < n_items and f(x) else 1.0)
    mean = sum(state[:n_items]) / n_items
    for x in range(n_items):
        state[x] = 2 * mean - state[x]


def grover_state(n_items: int, f: Oracle, j: int) -> list[complex]:
    """The state G^j |s>."""
    state = uniform_state(n_items)
    for _ in range(j):
        grover_iteration(state, n_items, f)
    return state


def num_choices(m: Fraction, n_items: int) -> int:
    """The number of integers j with 0 <= j < min(m, sqrt N)."""
    if m * m >= n_items:
        return math.isqrt(n_items - 1) + 1
    return math.ceil(m)


def next_m(m: Fraction, n_items: int, lam: Fraction = LAMBDA) -> Fraction:
    """min(lam m, sqrt N), kept exact: each value with m^2 >= N stands for sqrt N."""
    grown = lam * m
    if grown * grown >= n_items:
        return Fraction(n_items)
    return grown


def default_budget(n_items: int) -> int:
    """A limit on Grover iterations: 18 sqrt(N), rounded up."""
    return math.ceil(18 * math.sqrt(n_items))


def bbht_search(n_items: int, f: Oracle, rng: random.Random,
                budget: Optional[int] = None,
                lam: Fraction = LAMBDA) -> tuple[Optional[int], int, int]:
    """Run BBHT-SEARCH. Return (a marked item or None, Grover iterations, rounds).

    Each round makes j quantum queries and one classical query, so the
    total number of queries is iterations + rounds. The run stops with None
    once the iterations reach the budget (default 18 sqrt N).
    """
    if not 1 < lam < Fraction(4, 3):
        raise ValueError("lam must be in (1, 4/3)")
    limit = default_budget(n_items) if budget is None else budget
    m = Fraction(1)  # @line L1
    used = 0
    rounds = 0
    while used < limit:  # @line L2
        j = rng.randrange(num_choices(m, n_items))  # @line L3
        state = grover_state(n_items, f, j)  # @line L4
        x = sample(probabilities(state), rng)  # @line L5
        used += j
        rounds += 1
        if f(x):  # @line L6
            return x, used, rounds
        m = next_m(m, n_items, lam)  # @line L7
    return None, used, rounds  # @line L8
