# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/security-game/. The authors are listed in prov/ZA3ZMX.jsonl.
"""Strong Stackelberg equilibria of security games by one compact LP per target, in Fraction.

A game has T targets and k identical defender resources; each resource covers one target.
For target t, dc[t] > du[t] are the defender's payoffs when t is attacked while covered or
uncovered, and ac[t] < au[t] are the attacker's. The defender commits to a coverage vector
c with 0 <= c[t] <= 1 and sum(c) <= k (or sum(c) = k if all resources must be used); the
attacker attacks a target with the highest expected payoff, breaking ties in the defender's
favor.
"""

from fractions import Fraction

from agtlp import lp_max


def utilities(game, c, t):
    """(defender, attacker) expected payoffs when target t is attacked under coverage c."""
    dc, du, ac, au = game
    ct = Fraction(c[t])
    return ct * dc[t] + (1 - ct) * du[t], ct * ac[t] + (1 - ct) * au[t]


def best_for_target(game, k, t, use_all=False):
    """Return (value, c) of the best coverage under which t is a best target to attack, or None.

    With use_all, the coverage must sum to exactly k (no resource stays idle), and k <= T.
    """
    dc, du, ac, au = game
    T = len(dc)
    if use_all and not 0 <= k <= T:
        raise ValueError("use_all needs 0 <= k <= T")
    obj = [Fraction(0)] * T
    obj[t] = Fraction(dc[t] - du[t])
    A_ub, b_ub = [], []
    for s in range(T):
        if s != t:
            # Attacker: c_s (ac_s - au_s) + au_s <= c_t (ac_t - au_t) + au_t.
            row = [Fraction(0)] * T
            row[s] = Fraction(ac[s] - au[s])
            row[t] = -Fraction(ac[t] - au[t])
            A_ub.append(row)
            b_ub.append(Fraction(au[t] - au[s]))  # @line L2
    for s in range(T):
        A_ub.append([Fraction(int(r == s)) for r in range(T)])
        b_ub.append(Fraction(1))
    if use_all:
        status, c, value, _ = lp_max(obj, A_ub, b_ub, [[Fraction(1)] * T], [Fraction(k)])
    else:
        A_ub.append([Fraction(1)] * T)
        b_ub.append(Fraction(k))  # @line L3
        status, c, value, _ = lp_max(obj, A_ub, b_ub)
    if status != "optimal":  # @line L4
        return None
    return value + du[t], c


def strong_stackelberg(game, k, use_all=False):
    """Return (value, c, t): the defender's optimal coverage, its value and the attacked target."""
    best = None
    for t in range(len(game[0])):  # @line L1
        res = best_for_target(game, k, t, use_all)
        if res is not None and (best is None or res[0] > best[0]):  # @line L5
            best = (res[0], res[1], t)
    return best  # @line L6


def attacker_response(game, c):
    """The attacker's best target under c, with ties broken in the defender's favor."""
    T = len(game[0])
    pay = [utilities(game, c, t) for t in range(T)]
    top = max(a for _, a in pay)
    return max((t for t in range(T) if pay[t][1] == top), key=lambda t: (pay[t][0], -t))


def comb_mixture(c):
    """Write coverage c (entries in [0, 1]) as a distribution over sets of at most ceil(sum c) targets.

    Lay the c[t] end to end on [0, sum c]. For an offset u in [0, 1), cover the targets whose
    intervals contain u, u + 1, u + 2, ... . Each target is covered for a set of offsets of
    measure c[t], and no target twice, since its interval is at most 1 long. Return a list of
    (probability, sorted tuple of targets), one entry for each interval of offsets.
    """
    c = [Fraction(v) for v in c]
    ends, total = [], Fraction(0)
    for v in c:
        total += v
        ends.append(total)
    cuts = sorted({Fraction(0), Fraction(1)} | {e - int(e) for e in ends if 0 < e - int(e)})
    out = []
    for lo, hi in zip(cuts, cuts[1:]):
        u = (lo + hi) / 2
        cover, start = [], Fraction(0)
        for t, e in enumerate(ends):
            # Target t holds the points in [start, e); find a point u + r in it.
            r = 0
            while u + r < e:
                if u + r >= start:
                    cover.append(t)
                    break
                r += 1
            start = e
        out.append((hi - lo, tuple(cover)))
    return out
