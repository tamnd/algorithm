# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-integer-root/. The authors are listed in prov/8QNZZT.jsonl.


def newton_root(n: int, k: int = 2, stats: list | None = None) -> int:
    """floor(n^(1/k)) for n >= 0 and k >= 1, by Newton's method on integers.

    The iteration x <- floor(((k - 1) x + floor(n / x^(k-1))) / k) starts above
    the root and decreases strictly until it reaches it. Each step is one integer
    division and a few multiplications; Python's int does the multiprecision work.
    If stats is a list, the number of steps is appended to it.
    """
    if n < 0:
        raise ValueError("n must be nonnegative")
    if k < 1:
        raise ValueError("k must be at least 1")
    if k == 1 or n < 2:  # @line L1
        return n
    x = 1 << -(-n.bit_length() // k)  # @line L2: 2^ceil(B/k) > n^(1/k)
    steps = 0
    while True:  # @line L3
        y = ((k - 1) * x + n // x ** (k - 1)) // k  # @line L4
        steps += 1
        if y >= x:  # @line L5
            if stats is not None:
                stats.append(steps)
            return x
        x = y  # @line L6


def isqrt(n: int) -> int:
    """floor(sqrt(n)), the case k = 2: x <- floor((x + floor(n / x)) / 2)."""
    return newton_root(n, 2)


def root_rem(n: int, k: int = 2) -> tuple[int, int]:
    """(s, r) with s = floor(n^(1/k)) and r = n - s^k."""
    s = newton_root(n, k)
    return s, n - s**k


def is_perfect_power(n: int) -> tuple[int, int] | None:
    """(a, k) with n = a^k, k >= 2 and k largest, or None; for n >= 2."""
    if n < 2:
        return None
    best = None
    for k in range(2, n.bit_length() + 1):
        s = newton_root(n, k)
        if s < 2:
            break
        if s**k == n:
            best = (s, k)
    return best
