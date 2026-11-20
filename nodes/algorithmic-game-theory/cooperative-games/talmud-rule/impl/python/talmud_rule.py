# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/talmud-rule/. The authors are listed in prov/J1054R.jsonl.
"""The Talmud rule for bankruptcy problems (Aumann and Maschler 1985).

A bankruptcy problem is a list of claims c_1, ..., c_n >= 0 and an estate E with
0 <= E <= C = c_1 + ... + c_n. The Talmud rule gives constrained equal awards on the
half claims while E <= C/2, and for a larger estate it gives each claimant half its claim
plus constrained equal losses on the other half. It equals the nucleolus of the bankruptcy
game v(S) = max(0, E - c(N minus S)).

All arithmetic is in Fraction, so the result is exact. The cost is O(n log n) for the sort.
"""

from fractions import Fraction


def _check(claims, estate):
    claims = [Fraction(c) for c in claims]
    estate = Fraction(estate)
    if any(c < 0 for c in claims):
        raise ValueError("claims must be nonnegative")
    if estate < 0 or estate > sum(claims):
        raise ValueError("the estate must be between 0 and the sum of the claims")
    return claims, estate


def cea(claims, amount):
    """Constrained equal awards: x_i = min(c_i, lam) with sum x = amount."""
    claims, amount = _check(claims, amount)
    n = len(claims)
    order = sorted(range(n), key=lambda i: claims[i])  # @line L5
    x = [Fraction(0)] * n
    rest = amount
    for k, i in enumerate(order):  # @line L6
        lam = rest / (n - k)  # @line L7
        if claims[i] <= lam:  # @line L8
            x[i] = claims[i]
            rest -= claims[i]
        else:
            for j in order[k:]:  # @line L9
                x[j] = lam
            break
    return x  # @line L10


def cel(claims, amount):
    """Constrained equal losses: x_i = max(0, c_i - mu) with sum x = amount."""
    claims, amount = _check(claims, amount)
    loss = cea(claims, sum(claims) - amount)
    return [c - l for c, l in zip(claims, loss)]


def talmud(claims, estate):
    """Return the Talmud awards as a list of Fractions, in the order of the claims."""
    claims, estate = _check(claims, estate)
    total = sum(claims)  # @line L1
    half = [c / 2 for c in claims]
    if estate <= total / 2:  # @line L2
        return cea(half, estate)
    loss = cea(half, total - estate)  # @line L3
    return [c - l for c, l in zip(claims, loss)]  # @line L4


def contested_garment(c1, c2, estate):
    """The two-claimant rule of the Mishna: each concedes what exceeds its own claim, the
    rest is split equally."""
    (c1, c2), estate = _check([c1, c2], estate)
    a1 = max(Fraction(0), estate - c2)  # conceded to claimant 1 by claimant 2
    a2 = max(Fraction(0), estate - c1)
    rest = estate - a1 - a2
    return [a1 + rest / 2, a2 + rest / 2]
