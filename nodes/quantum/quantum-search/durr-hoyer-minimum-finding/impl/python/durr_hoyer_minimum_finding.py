# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/durr-hoyer-minimum-finding/. The authors are listed in prov/5EDMDS.jsonl.
"""Duerr-Hoyer minimum finding on the qs1 state-vector simulator.

The table T[0..N-1] is read through two kinds of query: a classical read
of one entry, and the phase oracle |x> -> (-1)^[T[x] < T[y]] |x> for the
current threshold index y. Each Grover iteration makes one oracle query.
Qubit 0 is the least significant bit of the index x.
"""

import math
import random
from fractions import Fraction
from typing import Optional, Sequence

from qsim import apply_diagonal, probabilities, sample

LAMBDA = Fraction(6, 5)


def num_qubits(n_items: int) -> int:
    if n_items < 1:
        raise ValueError("n_items must be at least 1")
    return max(1, (n_items - 1).bit_length())


def grover_state(table: Sequence, y: int, j: int) -> list[complex]:
    """G^j |s> for the marking f(x) = [T[x] < T[y]]; makes j oracle queries."""
    n_items = len(table)
    amp = 1.0 / math.sqrt(n_items)
    state = [amp + 0j if x < n_items else 0j for x in range(1 << num_qubits(n_items))]
    threshold = table[y]
    for _ in range(j):
        apply_diagonal(state, lambda x: -1.0 if x < n_items and table[x] < threshold else 1.0)
        mean = sum(state[:n_items]) / n_items
        for x in range(n_items):
            state[x] = 2 * mean - state[x]
    return state


def num_choices(m: Fraction, n_items: int) -> int:
    """The number of integers j with 0 <= j < min(m, sqrt N)."""
    if m * m >= n_items:
        return math.isqrt(n_items - 1) + 1
    return math.ceil(m)


def next_m(m: Fraction, n_items: int) -> Fraction:
    """min(6/5 m, sqrt N), kept exact: each value with m^2 >= N stands for sqrt N."""
    grown = LAMBDA * m
    if grown * grown >= n_items:
        return Fraction(n_items)
    return grown


def expected_bound(n_items: int) -> float:
    """1 + 18 sqrt(N) + ln(N) (log_{6/5} sqrt(N) + 5): the proved bound on E[C]."""
    log_term = math.log(math.sqrt(n_items)) / math.log(6 / 5) + 5
    return 1 + 18 * math.sqrt(n_items) + math.log(n_items) * log_term


def default_budget(n_items: int) -> int:
    """Twice the proved bound on the expected queries, so success >= 1/2."""
    return math.ceil(2 * expected_bound(n_items))


def durr_hoyer_minimum(table: Sequence, rng: random.Random,
                       budget: Optional[int] = None,
                       target=None) -> tuple[int, int, list[int]]:
    """Run DURR-HOYER-MINIMUM. Return (y, queries, the thresholds in order).

    The run stops when the queries reach the budget (default
    default_budget(N)). If target is given, it also stops as soon as
    T[y] <= target; the tests use this to measure the queries until the
    minimum is found.
    """
    n_items = len(table)
    if budget is None:
        budget = default_budget(n_items)
    y = rng.randrange(n_items)  # @line L1
    used = 1
    thresholds = [y]
    m = Fraction(1)  # @line L2
    while used < budget:  # @line L3
        if target is not None and table[y] <= target:
            break
        j = rng.randrange(num_choices(m, n_items))  # @line L4
        x = sample(probabilities(grover_state(table, y, j)), rng)  # @line L5
        used += j + 1  # @line L6
        if x < n_items and table[x] < table[y]:  # @line L7
            y = x
            m = Fraction(1)
            thresholds.append(y)
        else:
            m = next_m(m, n_items)  # @line L8
    return y, used, thresholds  # @line L9


# Exact expectations, for the tests and the example of the page.

def round_success(c: int, n_items: int, t: int) -> float:
    """P_c = (1/c) sum_{j<c} sin^2((2j+1) theta) for t marked items, 0 < t < N."""
    theta = math.asin(math.sqrt(t / n_items))
    return 0.5 - math.sin(4 * c * theta) / (4 * c * math.sin(2 * theta))


def phase_cost(n_items: int, t: int) -> tuple[float, float]:
    """Exact (E[iterations], E[rounds]) of one threshold phase with t marked items."""
    m = Fraction(1)
    reach = 1.0
    iters = 0.0
    rounds = 0.0
    while True:
        c = num_choices(m, n_items)
        p = round_success(c, n_items, t)
        if m == n_items:  # capped: the rest is a geometric tail
            return iters + reach * (c - 1) / 2 / p, rounds + reach / p
        iters += reach * (c - 1) / 2
        rounds += reach
        reach *= 1 - p
        m = next_m(m, n_items)


def expected_queries(counts: Sequence[int]) -> float:
    """Exact E[C], the queries until T[y] is the minimum, for a table whose
    distinct values, in increasing order, occur counts[0], counts[1], ... times."""
    n_items = sum(counts)
    total = 1.0
    below = counts[0]
    for n_k in counts[1:]:
        r_k = below + n_k
        iters, rounds = phase_cost(n_items, below)
        total += n_k / r_k * (iters + rounds)
        below = r_k
    return total
