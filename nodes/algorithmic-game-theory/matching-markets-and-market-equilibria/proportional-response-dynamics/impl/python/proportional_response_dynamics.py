# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proportional-response-dynamics/. The authors are listed in prov/M8R35N.jsonl.
"""Proportional response dynamics for a linear Fisher market, in floating point.

Buyers are 0, ..., n - 1 and goods are 0, ..., m - 1, with one unit of each good. u[i][j] >= 0 is
the utility of buyer i for all of good j and e[i] > 0 is her budget. Every buyer likes some good
and every good is liked by some buyer. In each round, every buyer splits her budget over the goods
in proportion to the utility that each good gave her in the last round. The price of a good is
the total money bid on it, and each buyer gets a share of the good equal to her share of the bids.
"""

import math


def round_once(u, e, b):
    """One round of the dynamics: return the prices of the bids b and the next bids."""
    n, m = len(u), len(u[0])
    p = [sum(b[i][j] for i in range(n)) for j in range(m)]  # @line L3
    x = [[b[i][j] / p[j] if b[i][j] > 0 else 0.0 for j in range(m)] for i in range(n)]  # @line L4
    v = [sum(u[i][j] * x[i][j] for j in range(m)) for i in range(n)]  # @line L5
    nb = [[e[i] * u[i][j] * x[i][j] / v[i] for j in range(m)] for i in range(n)]  # @line L6
    return p, nb


def proportional_response(u, e, rounds, b0=None):
    """Run the given number of rounds. Return the list of bid matrices b^0, ..., b^rounds."""
    n, m = len(u), len(u[0])
    if b0 is None:  # @line L1
        b0 = []
        for i in range(n):
            liked = [j for j in range(m) if u[i][j] > 0]
            b0.append([e[i] / len(liked) if u[i][j] > 0 else 0.0 for j in range(m)])
    history = [b0]
    b = b0
    for _ in range(rounds):  # @line L2
        _, b = round_once(u, e, b)
        history.append(b)
    return history  # @line L7


def prices(b):
    """The price of each good: the total money bid on it."""
    return [sum(row[j] for row in b) for j in range(len(b[0]))]


def shmyrev(u, b):
    """The convex potential of Shmyrev: sum_j p_j log p_j - sum_ij b_ij log u_ij. Proportional
    response is mirror descent on it, so it never goes up."""
    p = prices(b)
    value = sum(q * math.log(q) for q in p if q > 0)
    value -= sum(b[i][j] * math.log(u[i][j]) for i in range(len(b)) for j in range(len(b[0])) if b[i][j] > 0)
    return value


def kl(a, b):
    """Kullback-Leibler divergence of two bid matrices with the same row sums."""
    return sum(a[i][j] * math.log(a[i][j] / b[i][j])
               for i in range(len(a)) for j in range(len(a[0])) if a[i][j] > 0)
