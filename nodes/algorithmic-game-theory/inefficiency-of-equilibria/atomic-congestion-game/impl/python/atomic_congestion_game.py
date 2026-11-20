# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/atomic-congestion-game/. The authors are listed in prov/AE0S3S.jsonl.

"""Atomic congestion games: costs, Rosenthal's potential and best-response dynamics.

A game is a pair (costs, strategies). costs[e][j - 1] is c_e(j), the cost that each of the
j players on resource e pays. strategies[i] is the list of the strategies of player i, and
each strategy is a set of resource indices. A profile is a tuple whose entry i is the index
of the strategy that player i plays. Players minimize their costs.
"""

import itertools
from fractions import Fraction


def loads(game, profile):
    """Return the number of players on each resource."""
    costs, strategies = game
    x = [0] * len(costs)
    for i, k in enumerate(profile):
        for e in strategies[i][k]:
            x[e] += 1
    return x


def player_cost(game, profile, i):
    """Return c_i(profile), the sum of c_e(x_e) over the resources of player i."""
    costs, strategies = game
    x = loads(game, profile)
    return sum((Fraction(costs[e][x[e] - 1]) for e in strategies[i][profile[i]]), Fraction(0))


def social_cost(game, profile):
    """Return the sum of the players' costs, which is the sum of x_e c_e(x_e) over the resources."""
    costs, _ = game
    x = loads(game, profile)
    return sum((x[e] * Fraction(costs[e][x[e] - 1]) for e in range(len(costs)) if x[e] > 0), Fraction(0))


def rosenthal_potential(game, profile):
    """Return Phi = sum over resources e of c_e(1) + ... + c_e(x_e)."""
    costs, _ = game
    x = loads(game, profile)
    return sum((Fraction(c) for e in range(len(costs)) for c in costs[e][: x[e]]), Fraction(0))


def all_profiles(game):
    _, strategies = game
    return list(itertools.product(*[range(len(s)) for s in strategies]))


def pure_nash(game):
    """All pure Nash equilibria, by checking every unilateral deviation of every profile."""
    _, strategies = game
    out = []
    for p in all_profiles(game):
        if all(
            player_cost(game, p[:i] + (k,) + p[i + 1 :], i) >= player_cost(game, p, i)
            for i in range(len(strategies))
            for k in range(len(strategies[i]))
        ):
            out.append(p)
    return out


def best_response_dynamics(game, start):
    """Run round-robin best-response dynamics from start.

    Return (profile, steps), where profile is a pure Nash equilibrium and steps lists
    (player, gain, drop of Phi) for each move. The theorem says that gain equals the drop.
    """
    _, strategies = game
    s = tuple(start)
    steps = []
    changed = True
    while changed:  # @line L1
        changed = False
        for i in range(len(strategies)):  # @line L2
            current = player_cost(game, s, i)
            best = min(range(len(strategies[i])), key=lambda k: (player_cost(game, s[:i] + (k,) + s[i + 1 :], i), k))  # @line L3
            t = s[:i] + (best,) + s[i + 1 :]
            gain = current - player_cost(game, t, i)
            if gain > 0:  # @line L4
                steps.append((i, gain, rosenthal_potential(game, s) - rosenthal_potential(game, t)))
                s = t
                changed = True
    return s, steps  # @line L5
