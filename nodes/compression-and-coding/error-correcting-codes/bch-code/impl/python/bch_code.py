# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bch-code/. The authors are listed in prov/RQPH9G.jsonl.
"""Binary BCH codes: the generator polynomial from cyclotomic cosets.

The field GF(2^m) comes from gf.py. A binary polynomial is returned as an
int whose bit i is the coefficient of x^i.
"""

from gf import GF2m


def cyclotomic_coset(s: int, n: int, q: int = 2) -> list[int]:
    """The coset {s, s q, s q^2, ...} modulo n, in the order of generation."""
    out, x = [], s % n
    while x not in out:
        out.append(x)
        x = x * q % n
    return out


def minimal_polynomial(field: GF2m, beta_exp: int, n: int, s: int) -> int:
    """The minimal polynomial over GF(2) of beta^s, where beta = alpha^beta_exp has order n.

    It is the product of (x - beta^j) over the cyclotomic coset of s modulo n.
    """
    p = [1]
    for j in cyclotomic_coset(s, n):
        p = field.pmul(p, [field.alpha(beta_exp * j), 1])
    if any(c not in (0, 1) for c in p):
        raise ArithmeticError("the product is not over GF(2)")
    return sum(c << i for i, c in enumerate(p))


def gf2_mul(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def gf2_mod(a: int, b: int) -> int:
    db = b.bit_length()
    while a.bit_length() >= db:
        a ^= b << (a.bit_length() - db)
    return a


def bch_generator(field: GF2m, delta: int, b: int = 1, n: int | None = None) -> tuple[int, list[int]]:
    """Generator of the binary BCH code of length n and designed distance delta.

    g(x) = lcm of the minimal polynomials of beta^b, ..., beta^(b + delta - 2),
    where beta = alpha^((2^m - 1) / n) has order n. The default n = 2^m - 1 gives
    a primitive code; b = 1 gives a narrow-sense code. Returns g and its zeros.
    """
    if n is None:
        n = field.n
    if field.n % n:
        raise ValueError("n must divide 2^m - 1")
    beta_exp = field.n // n
    g, zeros = 1, set()
    for i in range(b, b + delta - 1):
        j = i % n
        if j in zeros:
            continue  # its minimal polynomial is already a factor
        g = gf2_mul(g, minimal_polynomial(field, beta_exp, n, j))
        zeros.update(cyclotomic_coset(j, n))
    return g, sorted(zeros)


def encode_systematic(m: int, n: int, g: int) -> int:
    """c(x) = x^(n-k) m(x) + (x^(n-k) m(x) mod g(x)) over GF(2)."""
    r = g.bit_length() - 1
    shifted = m << r
    if shifted >> n:
        raise ValueError("the message is too long")
    return shifted | gf2_mod(shifted, g)


def min_distance(g: int, n: int) -> int:
    """The least weight of a nonzero multiple m(x) g(x) of degree < n (brute force, small k)."""
    k = n - (g.bit_length() - 1)
    best = n
    # Gray code walk over all 2^k messages: one XOR per step
    c = 0
    for i in range(1, 1 << k):
        bit = (i & -i).bit_length() - 1
        c ^= g << bit
        best = min(best, bin(c).count("1"))
    return best
