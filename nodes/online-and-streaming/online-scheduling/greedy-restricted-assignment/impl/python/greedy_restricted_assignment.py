# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-restricted-assignment/. The authors are listed in prov/FJFX7X.jsonl.

from fractions import Fraction
from typing import Iterable, Sequence, Union

Number = Union[int, Fraction]


class GreedyRestrictedAssignment:
    """Online greedy for restricted assignment on m machines, numbered 0 to m - 1.

    Each call of assign() places one job, final, on the eligible machine of
    least load. Ties go to the lowest machine index.
    """

    def __init__(self, m: int) -> None:
        if m < 1:
            raise ValueError("m must be at least 1")
        self.m = m
        self.loads: list[Number] = [0] * m  # @line L1

    def assign(self, p: Number, eligible: Iterable[int]) -> int:
        """Place a job of size p on a machine of `eligible` and return that machine."""
        if p < 0:
            raise ValueError("job sizes must be non-negative")
        best = -1
        for i in eligible:  # @line L3
            if not 0 <= i < self.m:
                raise ValueError(f"machine {i} is out of range")
            if best < 0 or self.loads[i] < self.loads[best] or (self.loads[i] == self.loads[best] and i < best):
                best = i
        if best < 0:
            raise ValueError("the eligible set is empty")
        self.loads[best] += p  # @line L5
        return best  # @line L4

    def makespan(self) -> Number:
        return max(self.loads)


def greedy_restricted_assignment(
    m: int, jobs: Sequence[tuple[Number, Sequence[int]]]
) -> tuple[list[int], list[Number]]:
    """Run greedy on the jobs (p_t, M_t) in order. Return the machine of each job and the final loads."""
    g = GreedyRestrictedAssignment(m)
    assignment = []
    for p, eligible in jobs:  # @line L2
        assignment.append(g.assign(p, eligible))
    return assignment, list(g.loads)  # @line L6
