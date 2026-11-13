# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grover-search/. The authors are listed in prov/XD74ZG.jsonl.
"""Grover's search algorithm on the qs1 state-vector simulator.

The search space is {0, 1, ..., N - 1}. f(x) is 1 for a marked item and 0
otherwise, and the algorithm sees f only through the phase oracle
|x> -> (-1)^f(x) |x>. Qubit 0 is the least significant bit of x.
"""

import math
import random
from typing import Callable, Optional

from qsim import H, apply_1q, apply_diagonal, basis_state, probabilities, sample

Oracle = Callable[[int], int]


def num_qubits(n_items: int) -> int:
    """The number of qubits that hold an index below n_items."""
    if n_items < 1:
        raise ValueError("n_items must be at least 1")
    return max(1, (n_items - 1).bit_length())


def num_iterations(n_items: int, n_marked: int) -> int:
    """floor(pi / (4 theta)) with sin(theta) = sqrt(M / N), for 1 <= M <= N."""
    if not 1 <= n_marked <= n_items:
        raise ValueError("need 1 <= n_marked <= n_items")
    theta = math.asin(math.sqrt(n_marked / n_items))
    return math.floor(math.pi / (4.0 * theta))


def uniform_state(n_items: int) -> list[complex]:
    """The state |s> = N^(-1/2) sum of |x> over x < N, on num_qubits(N) qubits."""
    n = num_qubits(n_items)
    if n_items == 1 << n:
        state = basis_state(n, 0)
        for q in range(n):
            apply_1q(state, q, H)
        return state
    amp = 1.0 / math.sqrt(n_items)
    return [amp + 0j if x < n_items else 0j for x in range(1 << n)]


def phase_oracle(state: list[complex], f: Oracle) -> None:
    """One query: |x> -> (-1)^f(x) |x>."""
    apply_diagonal(state, lambda x: -1.0 if f(x) else 1.0)


def diffusion_gates(state: list[complex], n: int) -> None:
    """D = H^n (2|0><0| - I) H^n = 2|s><s| - I, for N = 2^n."""
    for q in range(n):
        apply_1q(state, q, H)
    apply_diagonal(state, lambda x: 1.0 if x == 0 else -1.0)
    for q in range(n):
        apply_1q(state, q, H)


def diffusion_mean(state: list[complex], n_items: int) -> None:
    """D = 2|s><s| - I for any N: each amplitude a_x becomes 2 mean - a_x."""
    mean = sum(state[:n_items]) / n_items
    for x in range(n_items):
        state[x] = 2 * mean - state[x]


def grover_iteration(state: list[complex], n_items: int, f: Oracle, gates: bool = False) -> None:
    """G = D O: one query, then the reflection about |s>."""
    phase_oracle(state, f)
    if gates:
        n = num_qubits(n_items)
        if n_items != 1 << n:
            raise ValueError("the gate form needs N = 2^n")
        diffusion_gates(state, n)
    else:
        diffusion_mean(state, n_items)


def grover_state(n_items: int, f: Oracle, k: int, gates: bool = False) -> list[complex]:
    """The state G^k |s>."""
    state = uniform_state(n_items)
    for _ in range(k):
        grover_iteration(state, n_items, f, gates)
    return state


def success_probability(n_items: int, f: Oracle, k: int, gates: bool = False) -> float:
    """The exact probability that a measurement after k iterations gives a marked item."""
    probs = probabilities(grover_state(n_items, f, k, gates))
    return sum(p for x, p in enumerate(probs[:n_items]) if f(x))


def grover_search(n_items: int, f: Oracle, n_marked: int, rng: random.Random,
                  gates: bool = False) -> tuple[Optional[int], int]:
    """Run GROVER-SEARCH once. Return (a marked item or None, the number of queries).

    n_marked is the number M of marked items, 1 <= M <= N. The count of
    queries includes the classical check of the measured item.
    """
    k = num_iterations(n_items, n_marked)  # @line L1
    state = uniform_state(n_items)  # @line L2
    for _ in range(k):  # @line L3
        phase_oracle(state, f)  # @line L4
        if gates:  # @line L5
            diffusion_gates(state, num_qubits(n_items))
        else:
            diffusion_mean(state, n_items)
    x = sample(probabilities(state), rng)  # @line L6
    if f(x):  # @line L7
        return x, k + 1
    return None, k + 1  # @line L8
