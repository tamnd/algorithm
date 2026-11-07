# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-fast-doubling/. The authors are listed in prov/N8HHBP.jsonl.


def fib_pair(n: int, modulus: int | None = None) -> tuple[int, int]:
    """Return (F(n), F(n + 1)) by fast doubling, reduced mod `modulus` if given.

    Precondition: n >= 0, and modulus >= 1 if given. Cost: one pass per bit
    of n, with three multiplications each (one product and two squares), so
    Theta(log n) multiplications; without a modulus the bit cost is O(M(n)),
    dominated by the last pass on numbers of about 0.347 n bits.
    """
    if n < 0:
        raise ValueError("n must be nonnegative")
    if modulus is not None and modulus < 1:
        raise ValueError("modulus must be positive")
    a, b = 0, 1  # @line L1: (a, b) = (F(k), F(k + 1)) for k = 0
    for t in bin(n)[2:]:  # @line L2: the bits of n, most significant first
        c = a * (2 * b - a)  # @line L3: F(2k)
        d = a * a + b * b  # @line L4: F(2k + 1)
        if t == "0":  # @line L5: k becomes 2k
            a, b = c, d
        else:  # @line L6: k becomes 2k + 1
            a, b = d, c + d
        if modulus is not None:
            a, b = a % modulus, b % modulus
    if modulus is not None:
        a, b = a % modulus, b % modulus
    return a, b  # @line L7


def fibonacci(n: int) -> int:
    """F(n) for n >= 0, with F(0) = 0 and F(1) = 1."""
    return fib_pair(n)[0]


def fibonacci_mod(n: int, modulus: int) -> int:
    """F(n) mod `modulus` for n >= 0 and modulus >= 1."""
    return fib_pair(n, modulus)[0]
