# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ellipsoid-against-hope/. The authors are listed in prov/WQZKXN.jsonl.
"""Ellipsoid against hope: a correlated equilibrium from the ellipsoid method on an infeasible dual.

The game is a pair (sizes, pay) as in the shared helper agtgame; players maximize. The dual
variables are y_i(j, l) >= 0, one per player i and ordered pair j != l of its strategies. For a
pure profile s, let

    g(y, s) = sum_i sum_{l != s_i} y_i(s_i, l) (u_i(s) - u_i(l, s_-i)).

The dual system "y >= 0 and g(y, s) <= -1 for every profile s" is infeasible, because the game
has a correlated equilibrium. The ellipsoid method runs on it with a separation oracle in the
pure-profile form of Jiang and Leyton-Brown: for every y >= 0 it returns a profile s with
g(y, s) >= 0 (up to rounding), so the constraint of s is violated. The profiles found are
collected, and the LP restricted to them gives a correlated equilibrium supported on them.

The ellipsoid steps and the oracle use float; the final LP is exact (Fraction, by agtlp), so
the returned distribution is an exact correlated equilibrium. The oracle sums over profiles
directly, as for a game in normal form; for a succinct game this sum is the expected utility
oracle of the game.
"""

import math
from fractions import Fraction

from agtgame import profiles
from agtlp import lp_max


def _replace(s, i, a):
    return s[:i] + (a,) + s[i + 1:]


def dual_index(sizes):
    """Return the list of the dual coordinates (i, j, l), in a fixed order."""
    return [(i, j, l) for i, k in enumerate(sizes) for j in range(k) for l in range(k) if l != j]


def gain_column(game, s, index):
    """Return the coefficients of g(., s): for coordinate (i, j, l), u_i(s) - u_i(l, s_-i) if s_i = j, else 0."""
    _, pay = game
    return [pay[s][i] - pay[_replace(s, i, l)][i] if s[i] == j else Fraction(0) for (i, j, l) in index]


def stationary_of_rates(rates):
    """Return a distribution x on 0..k-1 with x(j) sum_l r(j, l) = sum_l x(l) r(l, j) for the
    nonnegative rates r (a k by k list, diagonal ignored). It lives on a closed class of the
    graph of positive rates, where it is unique."""
    k = len(rates)
    succ = [[l for l in range(k) if l != j and rates[j][l] > 0] for j in range(k)]

    def reach(j):
        seen, stack = {j}, [j]
        while stack:
            a = stack.pop()
            for b in succ[a]:
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
        return seen

    reachable = [reach(j) for j in range(k)]
    root = next(j for j in range(k) if all(j in reachable[b] for b in reachable[j]))
    cls = sorted(reachable[root])
    m = len(cls)
    # Balance equations on the class, with the last one replaced by sum x = 1.
    M = []
    for a in cls[:-1]:
        row = [(-sum(rates[a][b] for b in cls if b != a) if c == a else rates[c][a]) for c in cls]
        M.append(row + [0.0])
    M.append([1.0] * m + [1.0])
    for col in range(m):
        piv = max(range(col, m), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        for r in range(m):
            if r != col and M[r][col] != 0.0:
                f = M[r][col] / M[col][col]
                M[r] = [p - f * q for p, q in zip(M[r], M[col])]
    x = [0.0] * k
    for t, a in enumerate(cls):
        x[a] = max(M[t][m] / M[t][t], 0.0)
    total = sum(x)
    return [v / total for v in x]


def separation_oracle(game, y, index):
    """For y >= 0, return a pure profile s with g(y, s) >= 0 (up to rounding).

    Each player's y_i defines a Markov chain; the product x of the stationary distributions has
    E_x g(y, s) = 0. The method of conditional expectations then fixes one player at a time,
    keeping the conditional expectation at least 0."""
    sizes, pay = game
    n = len(sizes)
    yv = {key: v for key, v in zip(index, y)}
    x = []
    for i, k in enumerate(sizes):
        rates = [[yv.get((i, j, l), 0.0) for l in range(k)] for j in range(k)]
        x.append(stationary_of_rates(rates))

    def g(s):
        return sum(yv[(i, s[i], l)] * float(pay[s][i] - pay[_replace(s, i, l)][i])
                   for i in range(n) for l in range(sizes[i]) if l != s[i])

    fixed = ()
    for i in range(n):
        rest = sizes[i + 1:]
        best, best_val = None, None
        for a in range(sizes[i]):
            val = 0.0
            for tail in profiles(rest):
                w = 1.0
                for t, b in enumerate(tail):
                    w *= x[i + 1 + t][b]
                if w:
                    val += w * g(fixed + (a,) + tail)
            if best_val is None or val > best_val:
                best, best_val = a, val
        fixed = fixed + (best,)
    return fixed


def restricted_lp(game, support):
    """Return a correlated equilibrium supported on the given profiles, or None if none exists."""
    sizes, pay = game
    S = sorted(support)
    rows = []
    for (i, j, l) in dual_index(sizes):
        rows.append([pay[_replace(s, i, l)][i] - pay[s][i] if s[i] == j else 0 for s in S])
    status, p, _, _ = lp_max([0] * len(S), rows, [0] * len(rows), [[1] * len(S)], [1])
    if status != "optimal":
        return None
    return {s: q for s, q in zip(S, p) if q != 0}


def ellipsoid_against_hope(game, radius=10.0, max_steps=20000):
    """Return (p, X, steps): a correlated equilibrium p (a dict from profiles to Fraction), the
    set X of profiles that the oracle produced, and the number of ellipsoid steps."""
    sizes, _ = game
    index = dual_index(sizes)
    d = len(index)
    if d == 0:  # every player has one strategy
        s = tuple(0 for _ in sizes)
        return {s: Fraction(1)}, {s}, 0
    c = [0.0] * d  # @line L1
    P = [[radius * radius if a == b else 0.0 for b in range(d)] for a in range(d)]
    X = set()
    p = None
    for step in range(1, max_steps + 1):  # @line L2
        y = c  # @line L3
        neg = next((r for r in range(d) if y[r] < 0), None)
        if neg is not None:  # @line L4
            a = [0.0] * d
            a[neg] = -1.0  # keep the half where y_r >= 0
        else:  # @line L5
            s = separation_oracle(game, y, index)  # @line L6
            if s not in X:
                X.add(s)  # @line L7
                p = restricted_lp(game, X)  # @line L8
                if p is not None:
                    return p, X, step  # @line L9
            a = [float(v) for v in gain_column(game, s, index)]  # keep the half where g(., s) <= g(y, s)
        # Central cut: the smallest ellipsoid that contains {z in E : a . z <= a . c}.
        Pa = [sum(P[r][t] * a[t] for t in range(d)) for r in range(d)]
        aPa = sum(a[r] * Pa[r] for r in range(d))
        if aPa <= 0:
            continue  # a = 0: the profile gives no information; another center will differ
        root = math.sqrt(aPa)
        c = [c[r] - Pa[r] / ((d + 1) * root) for r in range(d)]
        f = d * d / (d * d - 1.0)
        P = [[f * (P[r][t] - 2.0 / (d + 1) * Pa[r] * Pa[t] / aPa) for t in range(d)] for r in range(d)]
    raise RuntimeError("no correlated equilibrium found within max_steps ellipsoid steps")
