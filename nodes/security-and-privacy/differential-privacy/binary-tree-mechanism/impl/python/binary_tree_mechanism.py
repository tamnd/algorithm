# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-tree-mechanism/. The authors are listed in prov/6G5Z3M.jsonl.
"""The binary tree mechanism for continual counting (Chan, Shi and Song 2010;
Dwork, Naor, Pitassi and Rothblum 2010), in its streaming form.

The input is a stream of bits sigma(1), ..., sigma(T). At each time t the
mechanism releases a noisy count of the ones seen so far. Neighbors are
event-level: two streams of the same length T that differ at one time step.

The code uses random.Random so that the tests can be repeated, and it adds
float noise. Both are fine for study and wrong for a deployment: a real
release needs a cryptographic source of randomness and an exact sampler
(Mironov 2012; Canonne, Kamath and Steinke 2020).
"""

from __future__ import annotations

import math
import random
from typing import Callable, Sequence


def laplace_noise(b: float, rng: random.Random) -> float:
    """One draw of Lap(b), the density (1/(2b)) exp(-|z|/b), by the inverse CDF.

    Precondition: b > 0. Cost: one uniform draw and O(1) time.
    """
    u = rng.random() - 0.5
    while u == -0.5:  # the open interval (-1/2, 1/2) excludes -1/2
        u = rng.random() - 0.5
    s = (u > 0) - (u < 0)
    return -b * s * math.log(1.0 - 2.0 * abs(u))


def levels(T: int) -> int:
    """The number of levels L = floor(log2 T) + 1 of the dyadic tree over 1..T. Precondition: T >= 1."""
    if T < 1:
        raise ValueError("T must be at least 1")
    return T.bit_length()


def node_interval(t: int) -> tuple[int, int]:
    """The dyadic interval (t - 2^i, t] of the node closed at time t, where 2^i is the lowest one bit of t.

    Returned as the pair (first, last) of time steps. Precondition: t >= 1.
    """
    low = t & -t
    return (t - low + 1, t)


def binary_tree_counter_with_noise(
    stream: Sequence[int],
    noise: Callable[[int], float],
) -> tuple[list[float], list[float]]:
    """Run the streaming binary mechanism with a given noise source.

    noise(t) is the noise added to the node closed at time t. The function
    returns (outputs, nodes): outputs[t - 1] is the release at time t, and
    nodes[t - 1] is the noisy value of the node closed at time t.
    Precondition: the items are 0 or 1 (any reals work for the sums).
    Cost: O(T log T) time in total, O(log T) per step, and O(log T) words
    of state besides the returned lists.
    """
    T = len(stream)
    if T == 0:
        return [], []
    L = levels(T)  # @line L1
    a = [0.0] * L  # exact p-sums, one per level
    a_hat = [0.0] * L  # their noisy values
    outputs: list[float] = []
    nodes: list[float] = []
    for t in range(1, T + 1):  # @line L2
        i = ((t & -t).bit_length()) - 1  # @line L3
        a[i] = stream[t - 1] + sum(a[:i])  # @line L4
        for j in range(i):  # @line L5
            a[j] = 0.0
            a_hat[j] = 0.0
        a_hat[i] = a[i] + noise(t)  # @line L6
        nodes.append(a_hat[i])
        outputs.append(sum(a_hat[j] for j in range(L) if (t >> j) & 1))  # @line L7
    return outputs, nodes


def binary_tree_counter(stream: Sequence[int], epsilon: float, rng: random.Random) -> list[float]:
    """Release a noisy running count of a bit stream with the binary tree mechanism.

    Each node gets Lap(L / epsilon) noise, with L = floor(log2 T) + 1. Every
    time step lies in at most L nodes, so the vector of noisy nodes is
    epsilon-DP for event-level neighbors, and the outputs, which are sums of
    nodes, are epsilon-DP by post-processing.
    Precondition: epsilon > 0 and the items are 0 or 1.
    Cost: O(log T) time and one Laplace draw per step.
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if not stream:
        return []
    b = levels(len(stream)) / epsilon
    outputs, _ = binary_tree_counter_with_noise(stream, lambda t: laplace_noise(b, rng))
    return outputs


def node_vector(stream: Sequence[int]) -> list[int]:
    """The exact value of each node: nodes[t - 1] is the sum of the stream over node_interval(t). Cost: O(T log T)."""
    out = []
    for t in range(1, len(stream) + 1):
        lo, hi = node_interval(t)
        out.append(sum(stream[lo - 1:hi]))
    return out


def error_variance(t: int, T: int, epsilon: float) -> float:
    """The exact variance of the release at time t: popcount(t) nodes, each with variance 2 (L / epsilon)^2."""
    b = levels(T) / epsilon
    return bin(t).count("1") * 2.0 * b * b
