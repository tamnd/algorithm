# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pohlig-hellman/. The authors are listed in prov/PW5NFF.jsonl.

from math import isqrt


def _bsgs(g: int, h: int, n: int, p: int) -> int | None:
    """Least x >= 0 with g^x = h (mod p), or None; requires ord(g) <= n."""
    m = isqrt(n - 1) + 1
    table: dict[int, int] = {}
    e = 1 % p
    for j in range(m):
        if e not in table:
            table[e] = j
        e = e * g % p
    u = pow(g, -m, p)
    gamma = h
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = gamma * u % p
    return None


def _crt(residues: list[tuple[int, int]]) -> int:
    """The x in [0, prod m) with x = a (mod m) for pairwise coprime moduli m."""
    x, mod = 0, 1
    for a, m in residues:
        t = (a - x) * pow(mod, -1, m) % m
        x, mod = x + mod * t, mod * m
    return x


def pohlig_hellman(g: int, h: int, p: int, factors: dict[int, int]) -> int | None:
    """Pohlig-Hellman discrete logarithm in the group of units modulo p.

    factors maps each prime l to its exponent e in an integer N = prod l^e that
    is a multiple of ord(g), for example the factorization of p - 1 for a prime
    p. Return the least x >= 0 with g^x = h (mod p), or None if h is not a
    power of g. The group need not be cyclic: a final check g^x = h decides.
    Precondition: p >= 2, gcd(g, p) = 1, every key of factors is prime and
    ord(g) divides N. Raises ValueError if p < 2.
    Cost: O(log(N)^2 + sum of e (l)^(1/2)) multiplications modulo p, and
    O(max l^(1/2)) stored residues.
    """
    if p < 2:
        raise ValueError("need p >= 2")
    g %= p
    h %= p
    r = 1
    for l, e in factors.items():
        r *= l ** e
    for l in factors:  # @line L1
        while r % l == 0 and pow(g, r // l, p) == 1 % p:  # @line L2
            r //= l  # @line L3
    if pow(h, r, p) != 1 % p:  # @line L4
        return None
    residues: list[tuple[int, int]] = []  # @line L5
    for l in factors:  # @line L6
        f, q = 0, r  # @line L7
        while q % l == 0:
            f, q = f + 1, q // l
        if f == 0:
            continue
        gl, hl = pow(g, q, p), pow(h, q, p)  # @line L8
        gamma = pow(gl, l ** (f - 1), p)  # @line L9
        xl = 0  # @line L10
        for k in range(f):  # @line L11
            delta = pow(hl * pow(gl, -xl, p) % p, l ** (f - 1 - k), p)  # @line L12
            d = _bsgs(gamma, delta, l, p)  # @line L13
            if d is None:  # @line L14
                return None
            xl += d * l ** k  # @line L15
        residues.append((xl, l ** f))  # @line L16
    x = _crt(residues)  # @line L17
    if pow(g, x, p) != h:  # @line L18
        return None
    return x  # @line L19
