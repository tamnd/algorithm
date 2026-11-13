# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grover-adaptive-search/. The authors are listed in prov/Z3TQD9.jsonl.
"""Grover adaptive search on the qs1 state-vector simulator.

The cost function f is given on all n-bit strings x, where the variable
x_i is bit i of x and qubit 0 is the least significant bit. A = H^n
prepares the uniform state. For a threshold y, the oracle O_y is the
phase flip |x> -> (-1)^[f(x) < y] |x>. Gilliam, Woerner and Gonciulea
build it from a value register that holds f(x) - y and a sign test; the
simulator applies the phase flip directly, which has the same effect on
the key register. Each Grover iteration counts as one query, and the
evaluation of f at the measured point counts as one more.
"""

import math
import random
from fractions import Fraction
from typing import Optional, Sequence

from qsim import apply_diagonal, probabilities, sample

LAMBDA = Fraction(6, 5)


# Cost functions.

def qubo_value(q: Sequence[Sequence[float]], b: Sequence[float], c: float, x: int) -> float:
    """f(x) = sum_ij Q[i][j] x_i x_j + sum_i b_i x_i + c, with x_i = bit i of x."""
    n = len(b)
    bits = [(x >> i) & 1 for i in range(n)]
    total = c
    for i in range(n):
        if bits[i]:
            total += b[i]
            for j in range(n):
                if bits[j]:
                    total += q[i][j]
    return total


def qubo_table(q: Sequence[Sequence[float]], b: Sequence[float], c: float) -> list[float]:
    """The values f(0), f(1), ..., f(2^n - 1)."""
    return [qubo_value(q, b, c, x) for x in range(1 << len(b))]


def maxcut_qubo(n: int, edges: Sequence[tuple[int, int]]) -> tuple[list[list[int]], list[int], int]:
    """(Q, b, c) with f(x) = -(number of edges cut by x).

    An edge (u, v) is cut when x_u + x_v - 2 x_u x_v = 1.
    """
    q = [[0] * n for _ in range(n)]
    b = [0] * n
    for u, v in edges:
        b[u] -= 1
        b[v] -= 1
        q[u][v] += 1
        q[v][u] += 1
    return q, b, 0


# The quantum part.

def grover_state(values: Sequence[float], y: float, r: int) -> list[complex]:
    """G_y^r A|0> for the marking f(x) < y; makes r oracle queries.

    The diffusion A (2|0><0| - I) A^dagger with A = H^n is the reflection
    of every amplitude about the mean.
    """
    size = len(values)
    if size & (size - 1) or size == 0:
        raise ValueError("the number of points must be a power of 2")
    amp = 1.0 / math.sqrt(size)
    state = [amp + 0j] * size
    for _ in range(r):
        apply_diagonal(state, lambda x: -1.0 if values[x] < y else 1.0)
        mean = sum(state) / size
        for x in range(size):
            state[x] = 2 * mean - state[x]
    return state


def num_choices(k: Fraction, size: int) -> int:
    """The number of rotation counts r with 0 <= r < min(k, sqrt N)."""
    if k * k >= size:
        return math.isqrt(size - 1) + 1
    return math.ceil(k)


def next_k(k: Fraction, size: int, lam: Fraction = LAMBDA) -> Fraction:
    """min(lam k, sqrt N), kept exact: each value with k^2 >= N stands for sqrt N."""
    grown = lam * k
    if grown * grown >= size:
        return Fraction(size)
    return grown


def expected_bound(size: int) -> float:
    """Q(N) = 1 + 18 sqrt(N) + ln(N) (log_{6/5} sqrt(N) + 5), the bound of the
    Duerr-Hoyer proof on the expected queries until a minimum is found."""
    log_term = math.log(math.sqrt(size)) / math.log(6 / 5) + 5
    return 1 + 18 * math.sqrt(size) + math.log(size) * log_term


def default_budget(size: int) -> int:
    return math.ceil(2 * expected_bound(size))


def grover_adaptive_search(values: Sequence[float], rng: random.Random,
                           budget: Optional[int] = None,
                           patience: Optional[int] = None,
                           lam: Fraction = LAMBDA,
                           target: Optional[float] = None):
    """Run GROVER-ADAPTIVE-SEARCH on the table values = (f(0), ..., f(N-1)).

    The run stops when the queries reach the budget, or after patience
    rounds in a row without an improvement, whichever comes first. With
    neither given, the budget is default_budget(N). If target is given,
    the run also stops as soon as y <= target (for the tests).
    Return (x, y, queries, rounds), where rounds lists the tuples
    (y, k, r, measured x, f(measured x), improved) in order.
    """
    size = len(values)
    if budget is None and patience is None:
        budget = default_budget(size)
    x = rng.randrange(size)  # @line L1
    y = values[x]
    used = 1
    k = Fraction(1)  # @line L2
    fails = 0
    rounds = []
    while (budget is None or used < budget) and (patience is None or fails < patience):  # @line L3
        if target is not None and y <= target:
            break
        r = rng.randrange(num_choices(k, size))  # @line L4
        xm = sample(probabilities(grover_state(values, y, r)), rng)  # @line L5
        used += r + 1  # @line L6
        improved = values[xm] < y
        rounds.append((y, k, r, xm, values[xm], improved))
        if improved:  # @line L7
            x, y = xm, values[xm]
            k = Fraction(1)
            fails = 0
        else:
            k = next_k(k, size, lam)  # @line L8
            fails += 1
    return x, y, used, rounds  # @line L9


# Exact analysis, for the tests and the tables of the page.

def round_success(c: int, size: int, t: int) -> float:
    """(1/c) sum_{r<c} sin^2((2r+1) theta) with sin^2 theta = t/N."""
    if t == 0:
        return 0.0
    if t == size:
        return 1.0
    theta = math.asin(math.sqrt(t / size))
    return 0.5 - math.sin(4 * c * theta) / (4 * c * math.sin(2 * theta))


def phase_stop_probability(size: int, t: int, patience: int, lam: Fraction = LAMBDA) -> float:
    """The probability that patience rounds in a row fail, from k = 1, with t
    points below the threshold."""
    k = Fraction(1)
    stop = 1.0
    for _ in range(patience):
        stop *= 1 - round_success(num_choices(k, size), size, t)
        k = next_k(k, size, lam)
    return stop


def patience_success(counts: Sequence[int], patience: int, lam: Fraction = LAMBDA) -> float:
    """The exact probability that the run with the patience rule alone
    returns a minimum, for a table whose distinct values, in increasing
    order, occur counts[0], counts[1], ... times."""
    size = sum(counts)
    success = [1.0]  # success[k]: the threshold has the (k+1)-th smallest value
    below = counts[0]
    for _ in counts[1:]:
        go_on = 1 - phase_stop_probability(size, below, patience, lam)
        reach = sum(counts[i] * success[i] for i in range(len(success))) / below
        success.append(go_on * reach)
        below += counts[len(success) - 1]
    return sum(n_k * s for n_k, s in zip(counts, success)) / size


def patience_expected_queries(counts: Sequence[int], patience: int, lam: Fraction = LAMBDA) -> float:
    """The exact expected number of queries of the run with the patience
    rule alone, for value counts as in patience_success."""
    size = sum(counts)
    below = [sum(counts[:k]) for k in range(len(counts))]  # t for each value
    cost = []
    go_on = []
    for t in below:
        k = Fraction(1)
        reach = 1.0
        total = 0.0
        for _ in range(patience):
            c = num_choices(k, size)
            total += reach * ((c - 1) / 2 + 1)
            reach *= 1 - round_success(c, size, t)
            k = next_k(k, size, lam)
        cost.append(total)
        go_on.append(1 - reach)
    visit = [n_k / size for n_k in counts]
    for j in range(len(counts) - 1, 0, -1):
        for k in range(j):
            visit[k] += visit[j] * go_on[j] * counts[k] / below[j]
    return 1 + sum(v * c for v, c in zip(visit, cost))


def value_counts(values: Sequence[float]) -> list[int]:
    """The number of points with each distinct value, in increasing order."""
    seen: dict = {}
    for v in values:
        seen[v] = seen.get(v, 0) + 1
    return [seen[v] for v in sorted(seen)]
