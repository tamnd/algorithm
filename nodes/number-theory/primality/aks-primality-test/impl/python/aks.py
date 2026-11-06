# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aks-primality-test/. The authors are listed in prov/JR8RT8.jsonl.

"""The AKS primality test (Agrawal, Kayal and Saxena, 2004 version).

aks(n) returns True exactly when n is prime. It is deterministic, never
wrong, and runs in time polynomial in log n with no unproved hypothesis.

Cost, with lg n binary digits: r = O((lg n)^5) by the AKS bound, and in
practice r is a little above (lg n)^2. Step L8 is run for at most
sqrt(phi(r)) lg n values of a, and each needs O(lg n) products of polynomials
of degree below r with coefficients modulo n. With fast multiplication that
is O~(r^(3/2) (lg n)^3) bit operations, O~((lg n)^(21/2)) in the worst case.
Integers are of arbitrary precision (Python int). Polynomial products use
Kronecker substitution: the coefficients are packed into one big integer.

The logarithms lg n = log2 n are computed with 60 decimal digits. For n not
a power of 2 the numbers (lg n)^2 and sqrt(phi(r)) lg n are not integers, so
the floors below are exact at this precision for every n in practical range.
"""

import decimal
import math


def integer_root(n: int, b: int) -> int:
    """The largest x >= 0 with x^b <= n, for n >= 0 and b >= 1 (Newton's method)."""
    if n < 0 or b < 1:
        raise ValueError("need n >= 0 and b >= 1")
    if n < 2 or b == 1:
        return n
    x = 1 << ((n.bit_length() + b - 1) // b)  # x^b > n
    while True:
        y = ((b - 1) * x + n // x ** (b - 1)) // b
        if y >= x:
            break
        x = y
    while x**b > n:
        x -= 1
    while (x + 1) ** b <= n:
        x += 1
    return x


def is_perfect_power(n: int) -> bool:
    """True when n = a^b for integers a >= 2 and b >= 2."""
    if n < 4:
        return False
    for b in range(2, n.bit_length() + 1):
        if integer_root(n, b) ** b == n:
            return True
    return False


def _lg(n: int) -> decimal.Decimal:
    with decimal.localcontext() as ctx:
        ctx.prec = 60
        return decimal.Decimal(n).ln() / decimal.Decimal(2).ln()


def lg_squared_floor(n: int) -> int:
    """floor((log2 n)^2) for n >= 1."""
    if n & (n - 1) == 0:
        k = n.bit_length() - 1
        return k * k
    with decimal.localcontext() as ctx:
        ctx.prec = 60
        return int(_lg(n) ** 2)


def euler_phi(r: int) -> int:
    """Euler's totient of r >= 1, by trial division."""
    result, m, d = r, r, 2
    while d * d <= m:
        if m % d == 0:
            while m % d == 0:
                m //= d
            result -= result // d
        d += 1
    if m > 1:
        result -= result // m
    return result


def smallest_r(n: int) -> int:
    """The least r >= 2 with gcd(r, n) = 1 and multiplicative order o_r(n) > (log2 n)^2."""
    k_max = lg_squared_floor(n)  # o_r(n) > (lg n)^2 means o_r(n) > k_max
    r = max(2, k_max + 2)  # o_r(n) <= phi(r) <= r - 1, so smaller r cannot work
    while True:
        if math.gcd(r, n) == 1:
            x, k = 1, 0
            while k < k_max:
                x = x * n % r
                k += 1
                if x == 1:
                    break
            else:
                return r
        r += 1


def step_bound(n: int, r: int) -> int:
    """floor(sqrt(phi(r)) * log2 n)."""
    phi = euler_phi(r)
    if n & (n - 1) == 0:
        k = n.bit_length() - 1
        return math.isqrt(phi * k * k)
    with decimal.localcontext() as ctx:
        ctx.prec = 60
        return int(decimal.Decimal(phi).sqrt() * _lg(n))


def _pack(f: list[int], width: int) -> int:
    """One integer with one width-byte slot per coefficient (Kronecker substitution)."""
    return int.from_bytes(b"".join(c.to_bytes(width, "little") for c in f), "little")


def _square_mod(f: list[int], n: int, width: int) -> list[int]:
    """f^2 mod (X^r - 1, n), for a list f of r coefficients in [0, n)."""
    r = len(f)
    p = _pack(f, width)
    raw = (p * p).to_bytes(2 * r * width, "little")
    c = [int.from_bytes(raw[i * width : (i + 1) * width], "little") for i in range(2 * r)]
    return [(c[i] + c[i + r]) % n for i in range(r)]  # X^(r+i) = X^i


def _times_x_plus_a(f: list[int], a: int, n: int) -> list[int]:
    """f * (X + a) mod (X^r - 1, n)."""
    r = len(f)
    return [(a * f[i] + f[i - 1]) % n for i in range(r)]  # f[-1] wraps from X^(r-1)


def power_x_plus_a(a: int, n: int, r: int) -> list[int]:
    """The coefficients of (X + a)^n mod (X^r - 1, n), for n >= 2 and r >= 2.

    Left-to-right binary powering. A slot of the packed square holds a sum of
    at most r products of two numbers below n, so it fits in the width.
    """
    width = (r * (n - 1) ** 2).bit_length() // 8 + 1
    f = [0] * r
    f[0] = a % n
    f[1] = 1
    for bit in bin(n)[3:]:
        f = _square_mod(f, n, width)
        if bit == "1":
            f = _times_x_plus_a(f, a, n)
    return f


def aks(n: int) -> bool:
    """Return True if n is prime and False otherwise (AKS)."""
    if n < 2:  # @line L1
        return False
    if is_perfect_power(n):  # @line L2
        return False
    r = smallest_r(n)  # @line L3
    for a in range(2, min(r, n - 1) + 1):  # @line L4
        if 1 < math.gcd(a, n) < n:
            return False
    if n <= r:  # @line L5
        return True
    ell = step_bound(n, r)  # @line L6
    for a in range(1, ell + 1):  # @line L7
        target = [0] * r
        target[0] = a % n
        target[n % r] = (target[n % r] + 1) % n
        if power_x_plus_a(a, n, r) != target:  # @line L8
            return False
    return True  # @line L9
