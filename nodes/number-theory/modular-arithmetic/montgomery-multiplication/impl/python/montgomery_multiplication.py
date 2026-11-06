# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/montgomery-multiplication/. The authors are listed in prov/C3XQAV.jsonl.

"""Montgomery multiplication.

For an odd modulus n >= 1 and R = 2^r > n, a residue a is kept in Montgomery
form aR mod n. REDC(T) computes T * R^(-1) mod n for 0 <= T < n*R with two
multiplications, a mask, a shift and at most one subtraction, and no division
by n. The product of two numbers in Montgomery form is REDC(a*b).

Cost: on the word RAM with n < 2^w and r = w, one product is O(1) word
operations. Python integers have arbitrary precision; for n of k binary
digits one product costs O(M(k)) bit operations, where M(k) is the cost of
one k-digit multiplication. The setup costs O(M(k)) as well (Newton steps
for -n^(-1) mod R and one reduction for R^2 mod n).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MontgomeryContext:
    """Constants for one odd modulus n: r, R = 2^r > n, n' = -n^(-1) mod R, R^2 mod n."""

    n: int
    r: int
    mask: int
    n_prime: int
    r2: int


def montgomery_setup(n: int, r: int | None = None) -> MontgomeryContext:
    """Precompute the constants for an odd modulus n >= 1.

    r defaults to the bit length of n, the least r with 2^r > n. A larger r,
    such as a multiple of the word size, is accepted.
    """
    if n < 1 or n % 2 == 0:
        raise ValueError("Montgomery multiplication needs an odd modulus n >= 1")
    if r is None:
        r = n.bit_length()  # @line L1
    if (1 << r) <= n:
        raise ValueError("need R = 2^r > n")
    big_r = 1 << r
    x = 1  # @line L2
    j = 1  # @line L3
    while j < r:  # @line L4
        j = min(2 * j, r)  # @line L5
        x = (x * (2 - n * x)) & ((1 << j) - 1)
    n_prime = (-x) & (big_r - 1)  # @line L6
    r2 = (big_r * big_r) % n  # @line L7
    return MontgomeryContext(n, r, big_r - 1, n_prime, r2)


def redc(ctx: MontgomeryContext, t: int) -> int:
    """Return t * R^(-1) mod n, for 0 <= t < n*R."""
    m = ((t & ctx.mask) * ctx.n_prime) & ctx.mask  # @line L8
    u = (t + m * ctx.n) >> ctx.r  # @line L9
    if u >= ctx.n:  # @line L10
        u -= ctx.n
    return u  # @line L11


def mont_mul(ctx: MontgomeryContext, a: int, b: int) -> int:
    """Return a*b*R^(-1) mod n for a, b in 0..n-1; on Montgomery forms, the form of the product."""
    return redc(ctx, a * b)  # @line L12


def to_montgomery(ctx: MontgomeryContext, a: int) -> int:
    """Return a*R mod n for a in 0..n-1."""
    return redc(ctx, a * ctx.r2)  # @line L13


def from_montgomery(ctx: MontgomeryContext, a: int) -> int:
    """Return a*R^(-1) mod n for a in 0..n-1, the inverse of to_montgomery."""
    return redc(ctx, a)  # @line L14


def montgomery_modmul(a: int, b: int, n: int) -> int:
    """Return a*b mod n for an odd n >= 1, by converting to Montgomery form and back."""
    ctx = montgomery_setup(n)
    a %= n
    b %= n
    return from_montgomery(ctx, mont_mul(ctx, to_montgomery(ctx, a), to_montgomery(ctx, b)))


def montgomery_pow(base: int, e: int, n: int) -> int:
    """Return base^e mod n for an odd n >= 1 and e >= 0, by square-and-multiply in Montgomery form."""
    if e < 0:
        raise ValueError("exponent must be non-negative")
    ctx = montgomery_setup(n)
    x = to_montgomery(ctx, base % n)
    acc = to_montgomery(ctx, 1 % n)
    for bit in bin(e)[2:]:
        acc = mont_mul(ctx, acc, acc)
        if bit == "1":
            acc = mont_mul(ctx, acc, x)
    return from_montgomery(ctx, acc)
