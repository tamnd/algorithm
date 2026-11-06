# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divisor-count-sieve/. The authors are listed in prov/VFD6YZ.jsonl.


def divisor_count_sieve(n: int) -> list[int]:
    """Return d[0 .. n], where d[m] is the number of positive divisors of m for m >= 1, and d[0] = 0.

    Precondition: n >= 0.
    Cost: Theta(n log n) word operations; the output list is the only table.
    """
    d = [0] * (n + 1)  # @line L1
    for e in range(1, n + 1):  # @line L2
        for m in range(e, n + 1, e):  # @line L3
            d[m] += 1  # @line L4
    return d  # @line L5


def divisor_power_sum_sieve(n: int, k: int = 1) -> list[int]:
    """Return s[0 .. n], where s[m] = sigma_k(m), the sum of e**k over the divisors e of m, and s[0] = 0.

    Precondition: n >= 0 and k >= 0.
    Cost: Theta(n log n) additions on numbers up to about n**k times log log n.
    """
    s = [0] * (n + 1)
    for e in range(1, n + 1):
        w = e**k
        for m in range(e, n + 1, e):
            s[m] += w
    return s
