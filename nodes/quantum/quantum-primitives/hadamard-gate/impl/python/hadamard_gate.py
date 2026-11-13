# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadamard-gate/. The authors are listed in prov/0GVHJA.jsonl.
"""The Hadamard gate H = (X + Z)/sqrt(2), its n-fold tensor power, and the fast Walsh-Hadamard transform.

Qubit order: qubit j is bit j of the basis index.
"""

import math

from qsim import apply_1q

Vector = list[complex]
Matrix = list[list[complex]]

R = math.sqrt(0.5)
H = [[complex(R), complex(R)], [complex(R), complex(-R)]]


def hadamard_all(state: Vector) -> Vector:
    """H on every qubit, one qubit at a time: n * 2^n operations."""
    n = len(state).bit_length() - 1
    for q in range(n):
        state = apply_1q(state, H, q)
    return state


def hadamard_entry(n: int, x: int, y: int) -> float:
    """<x| H^(x)n |y> = (-1)^(x . y) / sqrt(2^n), where x . y is the parity of x AND y."""
    return (-1) ** bin(x & y).count("1") / math.sqrt(1 << n)


def hadamard_matrix(n: int) -> list[list[float]]:
    return [[hadamard_entry(n, x, y) for y in range(1 << n)] for x in range(1 << n)]


def fwht(v: list) -> list:
    """The unnormalized fast Walsh-Hadamard transform: out[x] = sum_y (-1)^(x . y) v[y], in n * 2^n additions."""
    a = list(v)
    h = 1
    while h < len(a):
        for i in range(0, len(a), 2 * h):
            for j in range(i, i + h):
                a[j], a[j + h] = a[j] + a[j + h], a[j] - a[j + h]
        h *= 2
    return a


def hadamard_transform(state: Vector) -> Vector:
    """H^(x)n |state> computed with the fast transform."""
    s = 1 / math.sqrt(len(state))
    return [s * a for a in fwht(state)]
