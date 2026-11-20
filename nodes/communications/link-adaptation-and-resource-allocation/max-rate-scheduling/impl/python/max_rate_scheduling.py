# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-rate-scheduling/. The authors are listed in prov/ZZJV41.jsonl.

"""Max-rate (max C/I) scheduling.

In each time slot t the scheduler knows the rate r[t][k][n] >= 0 that user k
would get on resource n (a slot, a subcarrier or a resource block). It gives
each resource to a user with the largest rate, breaking ties toward the
smallest user index, and adds that rate to the user's served total. This
maximizes the total served rate in every slot, and so over any horizon,
among all schedulers that give each resource to one user.

The module also has the analysis tools of the page: the probability that
user i has the strongest of K independent Rayleigh-faded channels, and the
mean rate E[log2(1 + snr X)] of the best of K users, X the largest of K
independent Exp(1) gains.
"""

import itertools
import math


def max_rate_slot(rates: list[list[float]]) -> list[int]:
    """Assign each resource of one slot. rates[k][n] is the rate of user k on resource n.

    Returns a list with the chosen user of each resource (the smallest index on ties).
    """
    if not rates or not rates[0]:
        raise ValueError("need at least one user and one resource")
    k_users, n_res = len(rates), len(rates[0])
    if any(len(r) != n_res for r in rates):
        raise ValueError("every user needs a rate on every resource")
    choice = []
    for n in range(n_res):  # @line L2
        best = 0
        for k in range(1, k_users):  # @line L3
            if rates[k][n] > rates[best][n]:
                best = k
        choice.append(best)  # @line L4
    return choice


def max_rate_schedule(slots: list[list[list[float]]]) -> tuple[list[list[int]], list[float]]:
    """Run the scheduler over slots[t][k][n]. Return the choices per slot and the total served per user."""
    if not slots:
        return [], []
    served = [0.0] * len(slots[0])
    choices = []
    for rates in slots:  # @line L1
        choice = max_rate_slot(rates)
        for n, k in enumerate(choice):
            served[k] += rates[k][n]  # @line L5
        choices.append(choice)
    return choices, served  # @line L6


def slot_total(rates: list[list[float]], choice: list[int]) -> float:
    """The total rate of one slot under an assignment choice[n] of users to resources."""
    return sum(rates[k][n] for n, k in enumerate(choice))


def brute_force_slot(rates: list[list[float]]) -> tuple[float, list[int]]:
    """The best total over all K^N assignments of one slot, and the first assignment that reaches it."""
    k_users, n_res = len(rates), len(rates[0])
    best_total, best_choice = -math.inf, []
    for choice in itertools.product(range(k_users), repeat=n_res):
        total = slot_total(rates, list(choice))
        if total > best_total:
            best_total, best_choice = total, list(choice)
    return best_total, best_choice


def win_probability(means: list[float], i: int) -> float:
    """P(user i has the largest gain) for independent exponential gains with the given means.

    With rates lam_j = 1 / means[j], P = integral of lam_i e^(-lam_i x) prod_{j != i} (1 - e^(-lam_j x)) dx,
    and expanding the product gives the sum over subsets S of the other users of
    (-1)^|S| lam_i / (lam_i + sum_{j in S} lam_j).
    """
    if any(m <= 0 for m in means):
        raise ValueError("means must be positive")
    lam = [1.0 / m for m in means]
    others = [lam[j] for j in range(len(lam)) if j != i]
    total = 0.0
    for size in range(len(others) + 1):
        for subset in itertools.combinations(others, size):
            total += (-1) ** size * lam[i] / (lam[i] + sum(subset))
    return total


def max_tail(k: int, x: float) -> float:
    """P(X > x) = 1 - (1 - e^(-x))^k for X the largest of k independent Exp(1) gains."""
    if x <= 0.0:
        return 1.0
    return -math.expm1(k * math.log1p(-math.exp(-x)))


def _simpson(f, a: float, b: float, steps: int) -> float:
    if steps % 2:
        steps += 1
    h = (b - a) / steps
    total = f(a) + f(b)
    for s in range(1, steps):
        total += (4.0 if s % 2 else 2.0) * f(a + s * h)
    return total * h / 3.0


def expected_of_max(k: int, dh, steps: int = 20000) -> float:
    """E[h(X)] - h(0) for X the largest of k independent Exp(1) gains, given the derivative dh of h.

    Uses E[h(X)] = h(0) + integral over x >= 0 of h'(x) P(X > x) dx, by Simpson's
    rule on [0, 45 + ln k]; past that point P(X > x) is below k e^(-45 - ln k) = e^(-45).
    dh must be smooth on the scale of the step.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    return _simpson(lambda x: dh(x) * max_tail(k, x), 0.0, 45.0 + math.log(k), steps)


def expected_max_rate(k: int, snr: float, steps: int = 4000) -> float:
    """E[log2(1 + snr X)] in bit/s/Hz for X the largest of k independent Exp(1) gains (Rayleigh fading).

    With y = ln(1 + snr x), E = (1 / ln 2) integral over y >= 0 of P(X > (e^y - 1) / snr) dy,
    a smooth integrand for every snr.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    if snr <= 0:
        raise ValueError("snr must be positive")
    top = math.log1p(snr * (45.0 + math.log(k)))
    return _simpson(lambda y: max_tail(k, math.expm1(y) / snr), 0.0, top, steps) / math.log(2.0)


def harmonic(k: int) -> float:
    """H_k = 1 + 1/2 + ... + 1/k, the mean of the largest of k independent Exp(1) gains."""
    return sum(1.0 / j for j in range(1, k + 1))
