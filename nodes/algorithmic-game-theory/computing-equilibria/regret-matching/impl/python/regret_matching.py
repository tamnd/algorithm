# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regret-matching/. The authors are listed in prov/FJGSGJ.jsonl.
"""Regret matching in a repeated finite game.

regret_matching runs the procedure of Hart and Mas-Colell (2000) for all players at once: a
player who played j last switches to l with probability proportional to the positive part
of the conditional regret D_i(j, l), with an inertia constant mu. Its empirical distribution
of play converges almost surely to the set of correlated equilibria. The regrets are kept
exactly, in Fraction, so the correlated equilibrium gap of the empirical distribution is
known exactly.

RegretMatcher is the unconditional version: it plays each action with probability
proportional to its positive external regret. It is the learner that counterfactual regret
minimization uses, and its external regret after t rounds is at most delta sqrt(k t), where
delta is the payoff range and k the number of actions. It works in float.

The game is a pair (sizes, pay) as in the shared helper agtgame; players maximize.
"""

import math
from fractions import Fraction


def _replace(s, i, a):
    return s[:i] + (a,) + s[i + 1:]


def _draw(rng, p):
    """Draw an index from the distribution p (a list of Fraction that sums to 1)."""
    x = rng.random()
    acc = Fraction(0)
    for a, q in enumerate(p):
        acc += q
        if x < acc:
            return a
    return max(a for a, q in enumerate(p) if q > 0)


def payoff_range(game, i):
    """Return max_s u_i(s) - min_s u_i(s)."""
    vals = [u[i] for u in game[1].values()]
    return max(vals) - min(vals)


def regret_matching(game, T, rng, mu=None):
    """Play T rounds of conditional regret matching for every player.

    Return (z, D). z is the empirical distribution of the T profiles played, a dict from
    profiles to Fraction. D[i][j][l] is the exact sum over the rounds t with s_i^t = j of
    u_i(l, s_-i^t) - u_i(s^t); D[i][j][j] is 0.

    Precondition: T >= 1, and mu > (k_i - 1) delta_i for every player i, where delta_i is
    the payoff range of player i. The default mu is the smallest integer above all these
    bounds. rng is a random.Random. Cost: O(n k) payoff lookups and Fraction operations per
    round, where k is the largest number of strategies; O(n k^2) space for D, plus the
    support of z.
    """
    sizes, pay = game
    n = len(sizes)
    bounds = [(sizes[i] - 1) * payoff_range(game, i) for i in range(n)]
    mu = Fraction(math.floor(max(bounds)) + 1) if mu is None else Fraction(mu)
    if any(mu <= b for b in bounds):
        raise ValueError("mu must exceed (k_i - 1) times the payoff range of every player")
    if T < 1:
        raise ValueError("T must be at least 1")
    D = [[[Fraction(0)] * k for _ in range(k)] for k in sizes]  # @line L1
    s = tuple(rng.randrange(k) for k in sizes)  # @line L2
    counts = {}
    for t in range(1, T + 1):  # @line L3
        counts[s] = counts.get(s, 0) + 1
        nxt = []
        for i in range(n):  # @line L4
            k = sizes[i]
            j = s[i]  # @line L5
            here = pay[s][i]
            for l in range(k):
                if l != j:
                    D[i][j][l] += pay[_replace(s, i, l)][i] - here  # @line L6
            p = [max(D[i][j][l], Fraction(0)) / (t * mu) if l != j else Fraction(0) for l in range(k)]  # @line L7
            p[j] = 1 - sum(p, Fraction(0))  # @line L8
            nxt.append(_draw(rng, p))  # @line L9
        s = tuple(nxt)
    z = {prof: Fraction(c, T) for prof, c in counts.items()}  # @line L10
    return z, D


def ce_gap(D, T):
    """Return max(0, max_{i, j, l} D[i][j][l]) / T, the correlated equilibrium gap of z."""
    top = max((v for Di in D for row in Di for v in row), default=Fraction(0))
    return max(top, Fraction(0)) / T


class RegretMatcher:
    """Unconditional regret matching for one player with k actions (float).

    strategy() returns the current mixed strategy, proportional to the positive parts of
    the cumulative external regrets (uniform when all are at most 0). update(u) takes the
    payoff u[l] that each action l would have earned this round, and adds u[l] minus the
    expected payoff of the current strategy to the regret of l. Cost: O(k) per call.
    """

    def __init__(self, k):
        if k < 1:
            raise ValueError("k must be at least 1")
        self.regret = [0.0] * k

    def strategy(self):
        pos = [max(r, 0.0) for r in self.regret]
        total = sum(pos)
        if total <= 0.0:
            return [1.0 / len(pos)] * len(pos)
        return [r / total for r in pos]

    def update(self, u):
        p = self.strategy()
        value = sum(q * x for q, x in zip(p, u))
        for l, x in enumerate(u):
            self.regret[l] += x - value
        return value


def expected_self_play(game, T):
    """Let every player run RegretMatcher on expected payoffs for T rounds (deterministic).

    Return the list of the T mixed profiles played (lists of float). The uniform average of
    their product distributions is an epsilon-coarse correlated equilibrium with epsilon at
    most max_i delta_i sqrt(k_i / T). Cost: O(T n |S|) float operations.
    """
    sizes, pay = game
    n = len(sizes)
    fpay = {s: [float(v) for v in u] for s, u in pay.items()}
    learners = [RegretMatcher(k) for k in sizes]
    history = []
    for _ in range(T):
        sigma = [m.strategy() for m in learners]
        history.append(sigma)
        dev = [[0.0] * k for k in sizes]
        for s, u in fpay.items():
            for i in range(n):
                w = 1.0
                for k2, a in enumerate(s):
                    if k2 != i:
                        w *= sigma[k2][a]
                dev[i][s[i]] += w * u[i]
        for i in range(n):
            learners[i].update(dev[i])
    return history
