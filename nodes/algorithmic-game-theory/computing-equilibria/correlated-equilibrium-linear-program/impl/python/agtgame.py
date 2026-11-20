# SPDX-License-Identifier: MIT
# Shared helper of the algorithmic game theory pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Finite games in normal form, with exact payoffs and exact equilibrium checks.

A game is a pair (sizes, pay). sizes is a tuple (k_1, ..., k_n) of the numbers of pure
strategies of the n players; the pure strategies of player i are 0, ..., k_i - 1. pay is a
dict that maps each profile, a tuple s = (s_1, ..., s_n), to a tuple of n Fraction
utilities, which each player maximizes. A cost game passes the utilities u = -c.

A mixed profile sigma is a list of n lists; sigma[i][a] is the probability, a Fraction,
that player i plays a. A distribution on profiles (for correlated and coarse correlated
equilibria) is a dict from profiles to Fraction; missing profiles have probability 0.

All checks are exact: there is no tolerance anywhere. There is no LP and no equilibrium
algorithm in this module.
"""

from fractions import Fraction
from itertools import product


def profiles(sizes):
    """Return the list of all pure profiles, in lexicographic order."""
    return list(product(*(range(k) for k in sizes)))


def from_bimatrix(A, B):
    """Return the game of the bimatrix (A, B): the row player gets A[r][c], the column player B[r][c]."""
    m, n = len(A), len(A[0])
    if len(B) != m or any(len(row) != n for row in A) or any(len(row) != n for row in B):
        raise ValueError("A and B must be m by n matrices of the same shape")
    pay = {(r, c): (Fraction(A[r][c]), Fraction(B[r][c])) for r in range(m) for c in range(n)}
    return (m, n), pay


def random_game(rng, sizes, lo, hi):
    """Return a game with integer utilities drawn uniformly from lo to hi (inclusive), as Fraction."""
    sizes = tuple(sizes)
    pay = {s: tuple(Fraction(rng.randint(lo, hi)) for _ in sizes) for s in profiles(sizes)}
    return sizes, pay


def _replace(s, i, a):
    return s[:i] + (a,) + s[i + 1:]


def _weight(sigma, s, skip=None):
    w = Fraction(1)
    for k, a in enumerate(s):
        if k != skip:
            w *= sigma[k][a]
            if w == 0:
                return w
    return w


def expected_utility(game, i, sigma):
    """Return u_i(sigma), the expected utility of player i when the players draw independently."""
    sizes, pay = game
    return sum((_weight(sigma, s) * pay[s][i] for s in profiles(sizes)), Fraction(0))


def deviation_payoffs(game, i, sigma):
    """Return the list of u_i(a, sigma_-i) for every pure strategy a of player i."""
    sizes, pay = game
    out = [Fraction(0)] * sizes[i]
    for s in profiles(sizes):
        w = _weight(sigma, s, skip=i)
        if w:
            out[s[i]] += w * pay[s][i]
    return out


def pure_best_responses(game, i, sigma):
    """Return the sorted list of the pure strategies of player i that maximize u_i(a, sigma_-i)."""
    d = deviation_payoffs(game, i, sigma)
    best = max(d)
    return [a for a, v in enumerate(d) if v == best]


def max_gain(game, sigma):
    """Return the largest gain of any player from a pure deviation: max_i (max_a u_i(a, sigma_-i) - u_i(sigma)).

    The result is never negative, because u_i(sigma) is an average of the deviation payoffs.
    """
    sizes, _ = game
    gain = Fraction(0)
    for i in range(len(sizes)):
        d = deviation_payoffs(game, i, sigma)
        u = sum((p * v for p, v in zip(sigma[i], d)), Fraction(0))
        gain = max(gain, max(d) - u)
    return gain


def is_distribution(p):
    """Return True if p (a sequence, or a dict of probabilities) is nonnegative and sums to exactly 1."""
    vals = list(p.values()) if isinstance(p, dict) else list(p)
    return all(v >= 0 for v in vals) and sum(vals, Fraction(0)) == 1


def _is_mixed_profile(game, sigma):
    sizes, _ = game
    return len(sigma) == len(sizes) and all(
        len(sigma[i]) == k and is_distribution(sigma[i]) for i, k in enumerate(sizes))


def is_nash(game, sigma):
    """Return True if sigma is a mixed Nash equilibrium: no pure deviation gains for any player."""
    return _is_mixed_profile(game, sigma) and max_gain(game, sigma) == 0


def is_epsilon_nash(game, sigma, eps):
    """Return True if no player gains more than eps by a pure deviation (the additive form)."""
    return _is_mixed_profile(game, sigma) and max_gain(game, sigma) <= eps


def _check_dist(game, dist):
    sizes, _ = game
    allowed = set(profiles(sizes))
    return all(s in allowed for s in dist) and is_distribution(dist)


def is_correlated(game, dist):
    """Return True if dist is a correlated equilibrium.

    For every player i and every pair a, b of its pure strategies, the sum over the profiles s
    with s_i = a of dist(s) (u_i(s) - u_i(b, s_-i)) is at least 0.
    """
    sizes, pay = game
    if not _check_dist(game, dist):
        return False
    for i, k in enumerate(sizes):
        for a in range(k):
            rows = [(q, s) for s, q in dist.items() if s[i] == a and q]
            for b in range(k):
                if b != a and sum((q * (pay[s][i] - pay[_replace(s, i, b)][i]) for q, s in rows), Fraction(0)) < 0:
                    return False
    return True


def is_coarse_correlated(game, dist):
    """Return True if dist is a coarse correlated equilibrium.

    For every player i and every pure strategy b, E_{s ~ dist} u_i(s) >= E_{s ~ dist} u_i(b, s_-i).
    """
    sizes, pay = game
    if not _check_dist(game, dist):
        return False
    for i, k in enumerate(sizes):
        here = sum((q * pay[s][i] for s, q in dist.items()), Fraction(0))
        for b in range(k):
            if sum((q * pay[_replace(s, i, b)][i] for s, q in dist.items()), Fraction(0)) > here:
                return False
    return True


def pure_nash_brute(game):
    """Return the list of all pure Nash equilibria, found by checking every profile."""
    sizes, pay = game
    out = []
    for s in profiles(sizes):
        if all(pay[s][i] >= pay[_replace(s, i, b)][i] for i in range(len(sizes)) for b in range(sizes[i])):
            out.append(s)
    return out
