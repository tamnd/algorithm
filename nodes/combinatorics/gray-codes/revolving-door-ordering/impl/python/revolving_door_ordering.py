# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/revolving-door-ordering/. The authors are listed in prov/JJSYG3.jsonl.

from collections.abc import Iterator
from math import comb


def revolving_door(n: int, k: int) -> Iterator[list[int]]:
    """Yield the k-subsets of {1..n} in revolving door order as a 0/1 array.

    a[e - 1] == 1 when element e is in the subset. The same list object is yielded
    each time and is changed in place (one element out, one in), so copy it if you
    keep it. An explicit stack replaces the recursion of the pseudocode.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0 or k > n:
        return
    a = [1] * k + [0] * (n - k)  # @line L1
    # Stack items: ("walk", m, t, forward) or ("swap", out, in), 1-based elements.
    stack: list[tuple] = [("walk", n, k, True)]  # @line L2
    while stack:
        item = stack.pop()
        if item[0] == "swap":
            _, out_e, in_e = item
            a[out_e - 1] = 0  # @line L7: also L11 with the roles swapped
            a[in_e - 1] = 1
            continue
        _, m, t, forward = item
        if t == 0 or t == m:  # @line L3
            yield a  # @line L3
            continue
        x = t - 1 if t >= 2 else m - 1  # @line L4
        if forward:  # @line L5
            # Pushed in reverse: L6, then L7, then L8 run in this order.
            stack.append(("walk", m - 1, t - 1, False))  # @line L8
            stack.append(("swap", x, m))  # @line L7
            stack.append(("walk", m - 1, t, True))  # @line L6
        else:  # @line L9
            stack.append(("walk", m - 1, t, False))  # @line L12
            stack.append(("swap", m, x))  # @line L11
            stack.append(("walk", m - 1, t - 1, True))  # @line L10


def revolving_door_subsets(n: int, k: int) -> list[tuple[int, ...]]:
    """Return the revolving door list as sorted tuples of elements of {1..n}."""
    return [tuple(i + 1 for i, bit in enumerate(a) if bit) for a in revolving_door(n, k)]


def rank(subset: tuple[int, ...] | list[int]) -> int:
    """Return the position of a k-subset of positive integers in revolving door order.

    For t_1 < ... < t_k the rank is the sum over i of (-1)**(k - i) * (C(t_i, i) - 1).
    """
    t = sorted(subset)
    k = len(t)
    if len(set(t)) != k or (k and t[0] < 1):
        raise ValueError("subset must hold distinct positive integers")
    r = 0
    for i in range(1, k + 1):
        term = comb(t[i - 1], i) - 1
        r += term if (k - i) % 2 == 0 else -term
    return r


def unrank(r: int, n: int, k: int) -> tuple[int, ...]:
    """Return the k-subset of {1..n} at position r of the revolving door order."""
    if not 0 <= k <= n or not 0 <= r < comb(n, k):
        raise ValueError("r, n or k is out of range")
    out = []
    while k > 0:
        x = k
        while comb(x, k) <= r:  # least x with C(x, k) > r
            x += 1
        out.append(x)
        r = comb(x, k) - 1 - r
        k -= 1
    return tuple(sorted(out))
