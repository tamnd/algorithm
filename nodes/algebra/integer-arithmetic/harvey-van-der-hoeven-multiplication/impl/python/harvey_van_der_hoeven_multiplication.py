# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harvey-van-der-hoeven-multiplication/. The authors are listed in prov/H0NKE4.jsonl.

"""A toy structural model of the first stage of the Harvey-van der Hoeven algorithm.

An integer product becomes a cyclic convolution of length S = s_1 * ... * s_d
for distinct primes s_i. The Chinese remainder theorem turns it into a
d-dimensional cyclic convolution of size s_1 x ... x s_d (Agarwal and Cooley),
which is done by a d-dimensional DFT, one dimension at a time. Each DFT of
prime length s is turned into a cyclic convolution of length s - 1 by Rader's
algorithm, the step of the paper's conditional variant. The arithmetic is
exact, modulo a prime q = 1 (mod S), instead of approximate complex numbers.
Gaussian resampling, the synthetic FFTs and the recursion of the real
algorithm are not modelled: the convolutions of length s - 1 are done
directly and only counted.
"""

from dataclasses import dataclass
from math import prod


@dataclass
class Counts:
    """Operations of the toy, by kind."""

    prime_dfts: int = 0
    rader_convolutions: int = 0
    pointwise_products: int = 0


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin, valid for n < 3.3 * 10^24."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for p in small:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _prime_factors(n: int) -> list[int]:
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


def primitive_root(p: int) -> int:
    """The smallest generator of the multiplicative group modulo the prime p."""
    factors = _prime_factors(p - 1)
    g = 1
    while True:
        g += 1
        if all(pow(g, (p - 1) // f, p) != 1 for f in factors):
            return g


class Plan:
    """The sizes s_i, the modulus q and the roots of unity."""

    def __init__(self, sizes: tuple[int, ...], b: int):
        if len(set(sizes)) != len(sizes) or not all(is_prime(s) for s in sizes):
            raise ValueError("the sizes must be distinct primes")
        self.sizes, self.b = tuple(sizes), b
        self.S = prod(sizes)
        self.chunks = (self.S + 1) // 2  # 2 * chunks - 1 <= S: no cyclic wrap
        bound = self.chunks * ((1 << b) - 1) ** 2
        q = (bound // self.S + 1) * self.S + 1
        while not is_prime(q):
            q += self.S
        self.q = q  # a prime, q = 1 (mod S), q > every coefficient of the product
        gq = primitive_root(q)
        self.roots = [pow(gq, (q - 1) // s, q) for s in sizes]  # primitive s_i-th roots
        self.gens = [primitive_root(s) for s in sizes]
        self.strides = [prod(sizes[i + 1 :]) for i in range(len(sizes))]


def cyclic_convolution(a: list[int], c: list[int], q: int) -> list[int]:
    """Cyclic convolution of two vectors of the same length, mod q, done directly."""
    n = len(a)
    out = [0] * n
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(c):
                k = i + j - n if i + j >= n else i + j
                out[k] = (out[k] + x * y) % q
    return out


def prime_dft(x: list[int], root: int, g: int, q: int, counts: Counts) -> list[int]:
    """DFT of prime length s with the root `root`, by Rader's algorithm."""
    s = len(x)
    counts.prime_dfts += 1
    out = [0] * s
    out[0] = sum(x) % q  # @line L10
    if s == 2:
        out[1] = (x[0] - x[1]) % q
        return out
    ginv = pow(g, -1, s)
    a = [x[pow(g, k, s)] for k in range(s - 1)]  # @line L11
    c = [pow(root, pow(ginv, k, s), q) for k in range(s - 1)]
    conv = cyclic_convolution(a, c, q)
    counts.rader_convolutions += 1
    for p in range(s - 1):  # @line L12
        out[pow(ginv, p, s)] = (x[0] + conv[p]) % q
    return out


def dft_d(cells: list[int], plan: Plan, sign: int, counts: Counts) -> list[int]:
    """d-dimensional DFT of an array stored in row-major order, one dimension at a time."""
    q, S = plan.q, plan.S
    cells = list(cells)
    for i, s in enumerate(plan.sizes):  # @line L7
        stride = plan.strides[i]
        root = pow(plan.roots[i], sign, q)
        for base in range(S):  # @line L8
            if (base // stride) % s:
                continue  # base is the start of a line along dimension i
            idx = [base + stride * k for k in range(s)]
            line = prime_dft([cells[t] for t in idx], root, plan.gens[i], q, counts)
            for t, val in zip(idx, line):
                cells[t] = val
    return cells  # @line L9


def crt_cell(j: int, plan: Plan) -> int:
    """The row-major index of the cell (j mod s_1, ..., j mod s_d)."""
    return sum((j % s) * st for s, st in zip(plan.sizes, plan.strides))


def hvdh_toy_multiply(u: int, v: int, plan: Plan, counts: Counts | None = None) -> int:
    """Return u * v for 0 <= u, v < 2^(b * chunks)."""
    counts = counts if counts is not None else Counts()
    b, S, q = plan.b, plan.S, plan.q
    if u < 0 or v < 0:
        raise ValueError("operands must be nonnegative")
    if max(u.bit_length(), v.bit_length()) > b * plan.chunks:
        raise ValueError("operands too long for this plan")
    mask = (1 << b) - 1
    cell = [crt_cell(j, plan) for j in range(S)]

    def to_cells(z: int) -> list[int]:
        arr = [0] * S
        for j in range(plan.chunks):  # @line L1
            arr[cell[j]] = z & mask  # @line L2
            z >>= b
        return arr

    fu = dft_d(to_cells(u), plan, 1, counts)  # @line L3
    fv = dft_d(to_cells(v), plan, 1, counts)
    prodcells = []
    for x, y in zip(fu, fv):  # @line L4
        prodcells.append(x * y % q)
        counts.pointwise_products += 1
    back = dft_d(prodcells, plan, -1, counts)  # @line L5
    inv_s = pow(S, -1, q)
    result = 0
    for j in range(S - 1, -1, -1):  # @line L6
        result = (result << b) + back[cell[j]] * inv_s % q
    return result


def expected_counts(sizes: tuple[int, ...]) -> tuple[int, int]:
    """(prime DFTs, Rader convolutions) of one d-dimensional DFT."""
    S = prod(sizes)
    dfts = sum(S // s for s in sizes)
    convs = sum(S // s for s in sizes if s > 2)
    return dfts, convs
