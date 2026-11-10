# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jain-vazirani-facility-location/. The authors are listed in prov/9ZC0XC.jsonl.

from fractions import Fraction
from typing import Sequence

Number = int | Fraction


def _pay_time(fi: Fraction, base: Fraction, points: list[Fraction], t: Fraction) -> Fraction:
    """Least s >= t with base + sum of max(0, s - p) over p in points >= fi."""
    need = fi - base
    if need <= 0:
        return t
    pts = sorted(points)
    total = Fraction(0)
    for k in range(1, len(pts) + 1):
        total += pts[k - 1]
        s = (need + total) / k
        if s >= pts[k - 1] and (k == len(pts) or s <= pts[k]):
            return max(s, t)
    raise ValueError("no active client")


def jain_vazirani_facility_location(f: Sequence[Number], c: Sequence[Sequence[Number]]):
    """Primal-dual 3-approximation for metric uncapacitated facility location (Jain and Vazirani 2001).

    f[i] >= 0 is the opening cost of facility i, and c[i][j] >= 0 the cost to connect client j
    to facility i; c must be a metric on facilities and clients. Returns (chosen, assign, alpha):
    chosen lists the open facilities, assign[j] is the facility of client j, and alpha is a
    feasible dual solution with connection cost + 3 * facility cost <= 3 * sum(alpha).
    Time O((m + n) * m * n log n) with exact arithmetic, for m facilities and n clients.
    """
    m, n = len(f), len(c[0])
    f = [Fraction(v) for v in f]
    c = [[Fraction(v) for v in row] for row in c]
    alpha = [Fraction(0)] * n  # @line L1
    active = set(range(n))
    opened: list[int] = []
    t = Fraction(0)
    first = True
    while active:  # @line L2
        if not first:
            times = []
            for i in range(m):
                if i in opened:
                    times += [c[i][j] for j in active if c[i][j] >= t]
                else:
                    base = sum((max(Fraction(0), alpha[j] - c[i][j]) for j in range(n) if j not in active), Fraction(0))
                    times.append(_pay_time(f[i], base, [c[i][j] for j in active], t))
            t = min(times)  # @line L3
        first = False
        for j in active:
            alpha[j] = t
        changed = True
        while changed:
            changed = False
            for i in range(m):
                if i not in opened:
                    paid = sum((max(Fraction(0), alpha[j] - c[i][j]) for j in range(n)), Fraction(0))
                    if paid >= f[i]:
                        opened.append(i)  # @line L4
                        changed = True
            for j in sorted(active):
                if any(c[i][j] <= alpha[j] for i in opened):
                    active.discard(j)  # @line L5
                    changed = True
    beta = [[max(Fraction(0), alpha[j] - c[i][j]) for j in range(n)] for i in range(m)]
    chosen: list[int] = []  # @line L6
    for i in opened:  # @line L7
        if not any(beta[i][j] > 0 and beta[k][j] > 0 for k in chosen for j in range(n)):
            chosen.append(i)  # @line L8
    assign = [min(chosen, key=lambda i: (c[i][j], i)) for j in range(n)]  # @line L9
    return chosen, assign, alpha  # @line L10
