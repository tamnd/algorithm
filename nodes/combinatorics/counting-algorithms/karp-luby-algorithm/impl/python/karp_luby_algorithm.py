# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-luby-algorithm/. The authors are listed in prov/68D09K.jsonl.

"""The Karp-Luby estimator for the number of satisfying assignments of a DNF.

A formula is a list of clauses over the variables 1..n. A clause is a list of
nonzero integers: v stands for the literal x_v and -v for its negation, and the
clause is the AND of its literals. The formula is the OR of its clauses.
"""

import bisect
import math
import random
from fractions import Fraction


def prepare(clauses, n):
    """Turn clauses into (mask, value) pairs over bit v - 1; drop contradictory clauses."""
    out = []
    for clause in clauses:
        mask = value = 0
        ok = True
        for lit in clause:
            v = abs(lit)
            if lit == 0 or v > n:
                raise ValueError("literals must be nonzero and refer to variables 1..n")
            bit = 1 << (v - 1)
            want = bit if lit > 0 else 0
            if mask & bit and value & bit != want:
                ok = False  # the clause contains x_v and its negation
                break
            mask |= bit
            value |= want
        if ok:
            out.append((mask, value))
    return out


class KarpLuby:
    """The sampling state: clauses, weights w_i = 2^(n - |C_i|), and their total W."""

    def __init__(self, clauses, n):
        self.n = n
        self.clauses = prepare(clauses, n)  # @line L1
        self.m = len(self.clauses)
        self.prefix = []  # @line L2
        total = 0
        for mask, _ in self.clauses:
            total += 1 << (n - bin(mask).count("1"))
            self.prefix.append(total)
        self.W = total

    def sample(self, rng):
        """One trial: return (i, a, x) with x = 1 if C_i is the first clause that a satisfies."""
        i = bisect.bisect_right(self.prefix, rng.randrange(self.W))  # @line L5
        mask, value = self.clauses[i]
        a = (rng.getrandbits(self.n) & ~mask) | value if self.n else 0  # @line L6
        for j in range(i):  # @line L7
            mj, vj = self.clauses[j]
            if a & mj == vj:
                return i, a, 0
        return i, a, 1

    def estimate(self, samples, rng):
        """W times the fraction of successful trials, as an exact fraction."""
        if self.m == 0:
            return Fraction(0)
        s = 0
        for _ in range(samples):  # @line L4
            s += self.sample(rng)[2]
        return Fraction(self.W * s, samples)  # @line L8


def sample_count(m, eps, delta):
    """N = ceil(3 m ln(2 / delta) / eps^2), enough for the (eps, delta) guarantee."""
    if not (0 < eps < 1 and 0 < delta < 1):
        raise ValueError("need 0 < eps < 1 and 0 < delta < 1")
    return max(1, math.ceil(3 * m * math.log(2 / delta) / (eps * eps)))  # @line L3


def karp_luby(clauses, n, eps, delta, rng=None):
    """Estimate the number of satisfying assignments of the DNF.

    With probability at least 1 - delta, the result is within a factor 1 +- eps
    of the exact count. The result is a Fraction.
    """
    if rng is None:
        rng = random.Random()
    state = KarpLuby(clauses, n)
    if state.m == 0:
        return Fraction(0)
    return state.estimate(sample_count(state.m, eps, delta), rng)
