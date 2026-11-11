# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gf2-polynomial-arithmetic/. The authors are listed in prov/DX1XMN.jsonl.

"""Polynomials over GF(2) stored as Python ints.

Bit i of the int is the coefficient of x^i. So 0b1011 is x^3 + x + 1,
and 0 is the zero polynomial. All functions are pure and use only int
operations: XOR is addition, shift is multiplication by a power of x.
"""


def deg(a: int) -> int:
    """Degree of a. The zero polynomial has degree -1 here."""
    return a.bit_length() - 1


def add(a: int, b: int) -> int:
    """a + b. Over GF(2), subtraction is the same operation."""
    return a ^ b


def mul(a: int, b: int) -> int:
    """Carry-less product a * b (schoolbook shift and XOR)."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def divmod2(a: int, b: int) -> tuple[int, int]:
    """Return (q, r) with a = q * b + r and deg r < deg b. Long division."""
    if b == 0:
        raise ZeroDivisionError("division by the zero polynomial")
    db = deg(b)
    q = 0
    while a and deg(a) >= db:
        s = deg(a) - db
        q ^= 1 << s
        a ^= b << s
    return q, a


def mod(a: int, b: int) -> int:
    return divmod2(a, b)[1]


def gcd(a: int, b: int) -> int:
    """Greatest common divisor (monic, as every nonzero GF(2) polynomial is)."""
    while b:
        a, b = b, mod(a, b)
    return a


def mulmod(a: int, b: int, m: int) -> int:
    return mod(mul(a, b), m)


def powmod(a: int, e: int, m: int) -> int:
    """a^e mod m by square and multiply, with e >= 0."""
    r = mod(1, m)
    a = mod(a, m)
    while e:
        if e & 1:
            r = mulmod(r, a, m)
        a = mulmod(a, a, m)
        e >>= 1
    return r


def prime_factors(n: int) -> list[int]:
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def x_pow_2k(k: int, f: int) -> int:
    """x^(2^k) mod f, by k squarings."""
    r = mod(0b10, f)
    for _ in range(k):
        r = mulmod(r, r, f)
    return r


def is_irreducible(f: int) -> bool:
    """Rabin's test over GF(2).

    f of degree n >= 1 is irreducible if and only if x^(2^n) = x mod f and
    gcd(x^(2^(n/q)) - x, f) = 1 for each prime q that divides n.
    """
    n = deg(f)
    if n < 1:
        return False
    if x_pow_2k(n, f) != mod(0b10, f):
        return False
    for q in prime_factors(n):
        h = x_pow_2k(n // q, f) ^ 0b10
        if gcd(f, h) != 1:
            return False
    return True


def is_irreducible_brute(f: int) -> bool:
    """Trial division by every polynomial of degree 1 to deg(f) // 2."""
    n = deg(f)
    if n < 1:
        return False
    for g in range(2, 1 << (n // 2 + 1)):
        if mod(f, g) == 0:
            return False
    return True


def order_of_x(f: int) -> int:
    """Least e >= 1 with x^e = 1 mod f. Needs f(0) = 1 and deg f >= 1."""
    if f & 1 == 0 or deg(f) < 1:
        raise ValueError("x has no order modulo f")
    e, r = 1, mod(0b10, f)
    while r != 1:
        r = mulmod(r, 0b10, f)
        e += 1
    return e


def is_primitive(f: int) -> bool:
    """f is irreducible of degree n and x has order 2^n - 1 modulo f."""
    n = deg(f)
    if not is_irreducible(f):
        return False
    m = (1 << n) - 1
    for q in prime_factors(m):
        if powmod(0b10, m // q, f) == 1:
            return False
    return True


def mobius(n: int) -> int:
    r, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            r = -r
        p += 1
    return -r if n > 1 else r


def necklace_count(d: int) -> int:
    """(1/d) * sum over k | d of mu(d/k) 2^k: the number of irreducible
    polynomials of degree d over GF(2)."""
    s = sum(mobius(d // k) << k for k in range(1, d + 1) if d % k == 0)
    return s // d


def to_str(a: int) -> str:
    """Human form, for example 'x^3 + x + 1'."""
    if a == 0:
        return "0"
    terms = []
    for i in range(deg(a), -1, -1):
        if (a >> i) & 1:
            terms.append("1" if i == 0 else "x" if i == 1 else f"x^{i}")
    return " + ".join(terms)
