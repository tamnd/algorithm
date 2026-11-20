# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potential-game/. The authors are listed in prov/9E88DE.jsonl.

"""Exact potentials of finite cost games.

A game is a pair (sizes, cost). sizes[i] is the number of pure strategies of player i,
numbered from 0, and cost maps each profile (a tuple) to the tuple of the players' costs,
which each player minimizes. An exact potential is a function phi on profiles with
phi(t) - phi(s) = cost[t][i] - cost[s][i] whenever t differs from s only in the strategy of i.
"""

import itertools
from fractions import Fraction


def profiles(sizes):
    """All pure profiles, in lexicographic order."""
    return list(itertools.product(*[range(k) for k in sizes]))


def deviations(sizes, s):
    """Yield (i, t) for every profile t that differs from s only in the strategy of player i."""
    for i, k in enumerate(sizes):
        for a in range(k):
            if a != s[i]:
                yield i, s[:i] + (a,) + s[i + 1 :]


def exact_potential(sizes, cost):
    """Return an exact potential as a dict from profiles to Fraction, with value 0 at the first profile, or None."""
    start = tuple(0 for _ in sizes)
    phi = {start: Fraction(0)}  # @line L1
    queue = [start]
    while queue:  # @line L2
        s = queue.pop()
        for i, t in deviations(sizes, s):  # @line L3
            value = phi[s] + Fraction(cost[t][i]) - Fraction(cost[s][i])
            if t not in phi:  # @line L4
                phi[t] = value
                queue.append(t)
            elif phi[t] != value:  # @line L5
                return None
    return phi  # @line L6


def is_exact_potential(sizes, cost, phi):
    """Check the defining equation on every unilateral deviation, exactly."""
    return all(
        phi[t] - phi[s] == cost[t][i] - cost[s][i] for s in profiles(sizes) for i, t in deviations(sizes, s)
    )


def four_cycle_sums(sizes, cost):
    """Return the set of sums of the deviators' cost changes around all 4-cycles of two players."""
    sums = set()
    for s in profiles(sizes):
        for i, j in itertools.combinations(range(len(sizes)), 2):
            for a in range(sizes[i]):
                for b in range(sizes[j]):
                    if a == s[i] or b == s[j]:
                        continue
                    p = s[:i] + (a,) + s[i + 1 :]
                    q = p[:j] + (b,) + p[j + 1 :]
                    r = s[:j] + (b,) + s[j + 1 :]
                    total = (
                        (cost[p][i] - cost[s][i])
                        + (cost[q][j] - cost[p][j])
                        + (cost[r][i] - cost[q][i])
                        + (cost[s][j] - cost[r][j])
                    )
                    sums.add(Fraction(total))
    return sums


def pure_nash(sizes, cost):
    """All pure Nash equilibria, by brute force over unilateral deviations."""
    return [s for s in profiles(sizes) if all(cost[t][i] >= cost[s][i] for i, t in deviations(sizes, s))]
