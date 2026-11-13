# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-counting/. The authors are listed in prov/STRRDC.jsonl.
"""Quantum counting (Brassard, Hoyer and Tapp) on the qs1 state-vector simulator.

The search register holds x in {0, ..., N - 1} on the n low qubits
(qubits 0 .. n - 1). The counting register holds y in {0, ..., P - 1},
P = 2^t, on the t high qubits (qubits n .. n + t - 1). In each register
the lowest qubit is the least significant bit.
"""

import math
import random
from typing import Callable

from qsim import (
    H,
    apply_1q,
    apply_controlled_1q,
    apply_controlled_block,
    apply_diagonal,
    apply_permutation,
    phase_gate,
    register_probabilities,
    sample,
)

Oracle = Callable[[int], int]


def num_qubits(n_items: int) -> int:
    if n_items < 1:
        raise ValueError("n_items must be at least 1")
    return max(1, (n_items - 1).bit_length())


def grover_iteration(block: list[complex], n_items: int, f: Oracle) -> None:
    """G = D O_f on the search register: one query, then a_x -> 2 mean - a_x."""
    apply_diagonal(block, lambda x: -1.0 if x < n_items and f(x) else 1.0)
    mean = sum(block[:n_items]) / n_items
    for x in range(n_items):
        block[x] = 2 * mean - block[x]


def swap_qubits(state: list[complex], a: int, b: int) -> None:
    if a == b:
        return
    perm = []
    for i in range(len(state)):
        ba = (i >> a) & 1
        bb = (i >> b) & 1
        j = i & ~((1 << a) | (1 << b)) | (bb << a) | (ba << b)
        perm.append(j)
    apply_permutation(state, perm)


def inverse_qft(state: list[complex], low: int, width: int) -> None:
    """QFT^(-1) on qubits low .. low + width - 1: |y> -> P^(-1/2) sum_k e^(-2 pi i y k / P) |k>."""
    for i in range(width // 2):
        swap_qubits(state, low + i, low + width - 1 - i)
    for a in range(width):
        for b in range(a):
            angle = -2.0 * math.pi / (1 << (a - b + 1))
            apply_controlled_1q(state, [low + b], low + a, phase_gate(angle))
        apply_1q(state, low + a, H)


def counting_state(n_items: int, f: Oracle, t: int) -> tuple[list[complex], int, int]:
    """The state just before the measurement (line L6). Return (state, n, queries)."""
    n = num_qubits(n_items)
    amp = 1.0 / math.sqrt(n_items)
    state = [0j] * (1 << (n + t))
    for x in range(n_items):  # L1: |0>^t |s>
        state[x] = amp + 0j
    for j in range(t):  # L2
        apply_1q(state, n + j, H)
    queries = 0
    for j in range(t):  # L3
        reps = 1 << j

        def power(block: list[complex], reps: int = reps) -> list[complex]:
            out = block[:]
            for _ in range(reps):
                grover_iteration(out, n_items, f)
            return out

        apply_controlled_block(state, n + j, n, power)  # L4
        queries += reps
    inverse_qft(state, n, t)  # L5
    return state, n, queries


def outcome_probabilities(n_items: int, f: Oracle, t: int) -> list[float]:
    """The exact distribution of y, the result of line L6."""
    state, n, _ = counting_state(n_items, f, t)
    return register_probabilities(state, n, t)


def estimate(n_items: int, y: int, t: int) -> float:
    """M~ = N sin^2(pi y / P)."""
    return n_items * math.sin(math.pi * y / (1 << t)) ** 2


def error_bound(n_items: int, n_marked: int, t: int, k: int = 1) -> float:
    """2 pi k sqrt(M (N - M)) / P + pi^2 k^2 N / P^2 (Brassard, Hoyer, Mosca and Tapp, Theorem 13)."""
    p = 1 << t
    return (2 * math.pi * k * math.sqrt(n_marked * (n_items - n_marked)) / p
            + math.pi ** 2 * k ** 2 * n_items / p ** 2)


def quantum_counting(n_items: int, f: Oracle, t: int, rng: random.Random) -> tuple[float, int, int]:
    """Run QUANTUM-COUNTING once with P = 2^t. Return (M~, y, queries)."""
    n = num_qubits(n_items)
    amp = 1.0 / math.sqrt(n_items)
    state = [0j] * (1 << (n + t))
    for x in range(n_items):  # @line L1
        state[x] = amp + 0j
    for j in range(t):  # @line L2
        apply_1q(state, n + j, H)
    queries = 0
    for j in range(t):  # @line L3
        reps = 1 << j

        def power(block: list[complex], reps: int = reps) -> list[complex]:
            out = block[:]
            for _ in range(reps):
                grover_iteration(out, n_items, f)
            return out

        apply_controlled_block(state, n + j, n, power)  # @line L4
        queries += reps
    inverse_qft(state, n, t)  # @line L5
    y = sample(register_probabilities(state, n, t), rng)  # @line L6
    theta = math.pi * y / (1 << t)  # @line L7
    return n_items * math.sin(theta) ** 2, y, queries  # @line L8
