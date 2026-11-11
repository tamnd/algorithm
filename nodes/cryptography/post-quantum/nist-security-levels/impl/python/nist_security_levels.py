# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nist-security-levels/. The authors are listed in prov/RP9RYK.jsonl.

"""The NIST post-quantum security categories and a Grover cost calculator.

NIST defines five security categories by the cost of attacks on AES and SHA-3
(call for proposals, December 2016, Section 4.A.5, and the call for additional
signatures, September 2022, Section 4.B.3). For key search on AES, the quantum
cost is given as 2^X / MAXDEPTH gates, where MAXDEPTH is a bound on the depth
(the serial running time) of the quantum circuit.

This module explains that formula. A Grover search on a k-bit key with depth
at most MAXDEPTH must be split over S machines that each search 2^k / S keys.
Each machine runs (pi / 4) * sqrt(2^k / S) Grover iterations of depth d and
gate count g. The depth bound fixes S, and the total gate count is then
(pi / 4)^2 * d * g * 2^k / MAXDEPTH. All values are in log2, as floats.

For study only. This is a cost model, not cryptographic code.
"""

import math
from dataclasses import dataclass

LOG2_PI_4 = math.log2(math.pi / 4)

# The three plausible values of MAXDEPTH in the calls: 2^40, 2^64, 2^96.
MAXDEPTHS_LOG2 = (40, 64, 96)

# Gate counts in the 2016 call (quantum figures after Grassl et al. 2016).
# Each entry: key bits -> (X in 2^X / MAXDEPTH quantum gates, classical gates).
AES_2016 = {128: (170, 143), 192: (233, 207), 256: (298, 272)}
# The same table in the 2022 call (quantum figures after Jaques et al. 2020).
AES_2022 = {128: (157, 143), 192: (221, 207), 256: (285, 272)}
# Classical gate counts for collision search on SHA3-256, SHA3-384, SHA3-512.
SHA3_COLLISION = {256: 146, 384: 210, 512: 274}

# Category -> (reference attack, log2 classical gates, quantum X or None),
# with the 2022 figures.
CATEGORIES = {
    1: ("key search on AES-128", 143, 157),
    2: ("collision search on SHA-256 or SHA3-256", 146, None),
    3: ("key search on AES-192", 207, 221),
    4: ("collision search on SHA-384 or SHA3-384", 210, None),
    5: ("key search on AES-256", 272, 285),
}


@dataclass(frozen=True)
class GroverCost:
    """The cost of a depth-limited Grover key search, all values in log2."""

    machines: float
    iterations_per_machine: float
    depth: float
    total_gates: float


def grover_iterations_log2(k: int) -> float:
    """log2 of the (pi / 4) * 2^(k / 2) iterations of one serial Grover search."""
    return LOG2_PI_4 + k / 2


def parallel_grover(k: int, maxdepth_log2: float, depth_log2: float, gates_log2: float) -> GroverCost:
    """Cost of a Grover search on a k-bit key split over machines to fit MAXDEPTH.

    depth_log2 and gates_log2 are the depth d and the gate count g of one
    Grover iteration (one call to the cipher circuit and one diffusion step).
    If one machine already fits in the depth bound, no split is made, and the
    cost stays at the serial cost.
    """
    machines = k + 2 * (LOG2_PI_4 + depth_log2) - 2 * maxdepth_log2
    machines = max(0.0, machines)
    iterations = LOG2_PI_4 + (k - machines) / 2
    depth = iterations + depth_log2
    total = machines + iterations + gates_log2
    return GroverCost(machines, iterations, depth, total)


def constant_from_table(table: dict) -> dict:
    """For each key size k with quantum cost 2^X / MAXDEPTH, return X - k.

    In the parallel model, X - k = 2 log2(pi / 4) + log2(d * g), so this is
    the cost of one Grover iteration that the table assumes.
    """
    return {k: x - k for k, (x, _) in table.items()}


def predicted_quantum_log2(k: int, constant: float) -> float:
    """The X in 2^X / MAXDEPTH for a k-bit key, from the constant X - k."""
    return k + constant


def crossover_maxdepth_log2(k: int, table: dict) -> float:
    """The MAXDEPTH (log2) above which Grover costs fewer gates than classical search."""
    quantum, classical = table[k]
    return quantum - classical


def meets_category(category: int, classical_log2: float, quantum_log2_at=None) -> bool:
    """True if an attack costs at least the category threshold in every metric.

    classical_log2 is the best classical attack cost in gates. quantum_log2_at,
    if given, maps a MAXDEPTH (log2) to the best quantum attack cost in gates;
    it is checked at the three values of MAXDEPTH of the call. Categories 2
    and 4 have no quantum figure, so the classical threshold is used there.
    """
    _, classical_threshold, quantum_x = CATEGORIES[category]
    if classical_log2 < classical_threshold:
        return False
    if quantum_log2_at is None:
        return True
    for maxdepth in MAXDEPTHS_LOG2:
        threshold = classical_threshold if quantum_x is None else min(quantum_x - maxdepth, classical_threshold)
        if quantum_log2_at(maxdepth) < threshold:
            return False
    return True


def category_of(classical_log2: float, quantum_log2_at=None) -> int:
    """The highest category met, or 0 if the attack is cheaper than category 1."""
    best = 0
    for category in sorted(CATEGORIES):
        if meets_category(category, classical_log2, quantum_log2_at):
            best = category
    return best
