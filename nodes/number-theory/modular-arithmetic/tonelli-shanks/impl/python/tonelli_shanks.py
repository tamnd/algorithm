# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tonelli-shanks/. The authors are listed in prov/5CEZWX.jsonl.

"""Tonelli-Shanks algorithm.

Computes x with x*x = a (mod p) for an odd prime p, or reports that a is a
quadratic nonresidue. Write p - 1 = q * 2^s with q odd. The algorithm takes a
quadratic nonresidue z (here the least one, found by trial with Euler's
criterion) and corrects the first guess a^((q+1)/2) by powers of z^q.

Precondition: p is an odd prime. The function does not test primality.

Cost: O(log p + s^2) multiplications modulo p, plus one exponentiation
(O(log p) multiplications) for each candidate z tried. Residues are Python
integers in 0..p-1; for p of k binary digits each multiplication costs
O(k^2) bit operations with schoolbook arithmetic.
"""


def mod_pow(b: int, e: int, m: int) -> int:
    """Return b^e mod m for e >= 0 and m >= 1, by right-to-left square-and-multiply."""
    result = 1 % m
    b %= m
    while e > 0:
        if e & 1:
            result = result * b % m
        b = b * b % m
        e >>= 1
    return result


def tonelli_shanks(a: int, p: int) -> int | None:
    """Return x in 0..p-1 with x^2 = a (mod p), or None if a is a nonresidue.

    p must be an odd prime. For a = 0 (mod p) the answer is 0.
    """
    if p < 3 or p % 2 == 0:
        raise ValueError("p must be an odd prime")
    a %= p  # @line L1
    if a == 0:
        return 0
    if mod_pow(a, (p - 1) // 2, p) != 1:  # @line L2
        return None
    q, s = p - 1, 0  # @line L3
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:  # @line L4
        return mod_pow(a, (p + 1) // 4, p)
    z = 2  # @line L5
    while mod_pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    c = mod_pow(z, q, p)  # @line L6
    x = mod_pow(a, (q + 1) // 2, p)
    t = mod_pow(a, q, p)
    m = s
    while t != 1:  # @line L7
        i, u = 0, t  # @line L8
        while u != 1:
            u = u * u % p
            i += 1
        b = c  # @line L9
        for _ in range(m - i - 1):
            b = b * b % p
        m = i  # @line L10
        c = b * b % p
        t = t * c % p
        x = x * b % p
    return x  # @line L11


def sqrt_mod_prime(a: int, p: int) -> int | None:
    """Return the smaller of the two square roots of a modulo the odd prime p, or None."""
    x = tonelli_shanks(a, p)
    if x is None:
        return None
    return min(x, p - x)
