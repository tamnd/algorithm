# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brassard-hoyer-tapp-collision/. The authors are listed in prov/QEG4BF.jsonl.
"""The Brassard-Høyer-Tapp collision algorithm (LATIN 1998), simulated on n qubits.

F maps X = {0, ..., N-1} with N = 2**n to some set Y and is r-to-one. COLLISION(F, k)
reads F on a set K of k points, sorts the table, and looks for a collision inside K. If
there is none, it runs Grover search for an x outside K with F(x) in F(K). Then exactly
t = (r - 1) k points are marked, so the number of Grover iterations is known.

The Grover part runs on the qsim state vector (qubit 0 is the least significant bit of x).
The query count follows the paper: one evaluation of F per evaluation of H.
"""

import bisect
import math
import random

from qsim import apply_1q, apply_diagonal, probabilities, uniform_state

H_GATE = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]


def random_r_to_one(n: int, r: int, rng: random.Random) -> list[int]:
    """A random r-to-one function on 2**n points, as a list of values."""
    size = 1 << n
    if size % r:
        raise ValueError("r must divide N")
    vals = [i // r for i in range(size)]
    rng.shuffle(vals)
    return vals


def grover_state(n: int, marked: list[bool], iterations: int) -> list[complex]:
    """The state after the given number of Grover iterations with the phase oracle of marked."""
    state = uniform_state(n)
    oracle = [-1.0 if m else 1.0 for m in marked]
    zero = [-1.0] + [1.0] * ((1 << n) - 1)
    for _ in range(iterations):
        state = apply_diagonal(state, oracle)  # one query of H, so one evaluation of F
        for q in range(n):
            state = apply_1q(state, H_GATE, q)
        state = apply_diagonal(state, zero)  # 2|0><0| - I up to a global sign
        for q in range(n):
            state = apply_1q(state, H_GATE, q)
        state = [-a for a in state]
    return state


def grover_iterations(n_items: int, t: int) -> int:
    theta = math.asin(math.sqrt(t / n_items))
    return math.floor(math.pi / (4 * theta))


def default_k(n_items: int, r: int) -> int:
    return max(1, round((n_items / r) ** (1 / 3)))


def collision(f: list[int], r: int, k: int, rng: random.Random, keys=None):
    """Return (x0, x1, evaluations) with x0 != x1 and f[x0] == f[x1].

    keys fixes the set K (for the worked example); otherwise K is a random k-subset.
    """
    n_items = len(f)
    n = n_items.bit_length() - 1
    evals = 0
    if keys is None:
        keys = rng.sample(range(n_items), k)  # @line L1
    k = len(keys)
    table = []
    for x in keys:  # @line L2
        table.append((f[x], x))
        evals += 1
    table.sort()  # @line L3
    for (y0, x0), (y1, x1) in zip(table, table[1:]):  # @line L4
        if y0 == y1:
            return x0, x1, evals  # @line L5
    ys = [y for y, _ in table]
    in_k = set(keys)

    def h(x):  # one evaluation of F and a binary search in the sorted table
        j = bisect.bisect_left(ys, f[x])
        return x not in in_k and j < len(ys) and ys[j] == f[x]

    marked = [h(x) for x in range(n_items)]  # the phase oracle of H, as a diagonal
    t = (r - 1) * k  # @line L6
    iters = grover_iterations(n_items, t)
    while True:
        state = grover_state(n, marked, iters)  # @line L7
        evals += iters
        p = probabilities(state)
        x1 = rng.choices(range(n_items), weights=p)[0]  # @line L8
        evals += 1  # check the result: one more evaluation of F
        if h(x1):  # @line L9
            j = bisect.bisect_left(ys, f[x1])
            return table[j][1], x1, evals  # @line L10


def success_probability(n_items: int, t: int, iterations: int) -> float:
    theta = math.asin(math.sqrt(t / n_items))
    return math.sin((2 * iterations + 1) * theta) ** 2
