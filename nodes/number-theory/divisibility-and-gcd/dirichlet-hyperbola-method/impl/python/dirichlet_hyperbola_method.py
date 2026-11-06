# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dirichlet-hyperbola-method/. The authors are listed in prov/6FBZTF.jsonl.

"""Dirichlet hyperbola method.

divisor_summatory(n) returns D(n) = d(1) + d(2) + ... + d(n), the number of
pairs (a, b) of positive integers with ab <= n, using floor(sqrt(n))
divisions. hyperbola_sum is the general form: the sum of f(a) g(b) over
ab <= n, given the prefix sums F and G of f and g. For n <= 0 both sums are
empty and the result is 0. Integers are Python integers of any size.
"""

from typing import Callable


def integer_sqrt(n: int) -> int:
    """The largest s with s * s <= n, for n >= 0, by Newton's method on integers."""
    if n < 0:
        raise ValueError("integer_sqrt of a negative number")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)  # x >= sqrt(n)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def divisor_summatory(n: int) -> int:
    """D(n), the sum of the number of divisors of k over 1 <= k <= n."""
    if n <= 0:  # @line L1
        return 0
    s = integer_sqrt(n)  # @line L2
    t = 0  # @line L3
    for a in range(1, s + 1):  # @line L4
        t += n // a  # @line L5
    return 2 * t - s * s  # @line L6


def hyperbola_sum(
    f: Callable[[int], int],
    g: Callable[[int], int],
    big_f: Callable[[int], int],
    big_g: Callable[[int], int],
    n: int,
) -> int:
    """The sum of f(a) * g(b) over positive a, b with a * b <= n.

    big_f(x) must return f(1) + ... + f(x) and big_g(x) likewise for g,
    for 0 <= x <= n. Uses 2 * floor(sqrt(n)) calls of each kind.
    """
    if n <= 0:
        return 0
    s = integer_sqrt(n)
    total = 0
    for a in range(1, s + 1):
        total += f(a) * big_g(n // a)
    for b in range(1, s + 1):
        total += g(b) * big_f(n // b)
    return total - big_f(s) * big_g(s)


def sigma_summatory(n: int) -> int:
    """The sum of sigma(k), the sum of the divisors of k, over 1 <= k <= n."""
    return hyperbola_sum(
        lambda a: a,
        lambda b: 1,
        lambda x: x * (x + 1) // 2,
        lambda x: x,
        n,
    )
