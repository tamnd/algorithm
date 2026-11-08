# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagged-fibonacci-generator/. The authors are listed in prov/V53JWN.jsonl.

"""Lagged Fibonacci generators x_n = (x_(n-k) op x_(n-j)) mod 2^w, and Knuth's ran_array."""

import math
import random
from typing import Iterable, List, Tuple

OPS = ("add", "sub", "mul", "xor")


class LaggedFibonacci:
    """x_n = (x_(n-k) op x_(n-j)) mod 2^w with lags 0 < j < k.

    The k most recent values sit in a circular buffer; `pos` indexes x_(n-k).
    For "sub" the result is x_(n-k) - x_(n-j), as in Knuth's ran_array.
    """

    def __init__(self, j: int, k: int, w: int, op: str, values: Iterable[int]) -> None:
        if not 0 < j < k:
            raise ValueError("need lags 0 < j < k")
        if op not in OPS:
            raise ValueError("op must be one of add, sub, mul, xor")
        if w < 1:
            raise ValueError("need a word size w >= 1")
        self.j, self.k, self.w, self.op = j, k, w, op
        self.mask = (1 << w) - 1
        buf = [v & self.mask for v in values]
        if len(buf) != k:
            raise ValueError("need exactly k initial values")
        if op in ("add", "sub") and all(v % 2 == 0 for v in buf):  # @line L7
            raise ValueError("an additive generator needs at least one odd initial value")
        if op == "mul" and any(v % 2 == 0 for v in buf):
            raise ValueError("a multiplicative generator needs all initial values odd")
        if op == "xor" and not any(buf):
            raise ValueError("an xor generator needs a nonzero initial value")
        self.buf = buf  # @line L6
        self.pos = 0

    def next(self) -> int:
        k, p = self.k, self.pos
        q = p + k - self.j  # @line L1
        if q >= k:
            q -= k
        a, b = self.buf[p], self.buf[q]
        if self.op == "add":  # @line L2
            x = (a + b) & self.mask
        elif self.op == "sub":
            x = (a - b) & self.mask
        elif self.op == "mul":
            x = (a * b) & self.mask
        else:
            x = a ^ b
        self.buf[p] = x  # @line L3
        p += 1  # @line L4
        self.pos = 0 if p == k else p
        return x  # @line L5

    def uniform(self) -> float:
        """A value in [0, 1) from the top 53 bits (or all w bits if w < 53)."""
        x = self.next()
        if self.w > 53:
            return (x >> (self.w - 53)) / 2.0**53
        return x / 2.0**self.w


def splitmix64_values(seed: int, count: int) -> List[int]:
    """Initial values from SplitMix64, a standard way to fill a large state."""
    m64 = (1 << 64) - 1
    out, s = [], seed & m64
    for _ in range(count):
        s = (s + 0x9E3779B97F4A7C15) & m64
        z = s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & m64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & m64
        out.append(z ^ (z >> 31))
    return out


def seeded(j: int, k: int, w: int, op: str, seed: int) -> LaggedFibonacci:
    vals = splitmix64_values(seed, k)
    if op == "mul":
        vals = [v | 1 for v in vals]
    elif op in ("add", "sub"):
        vals[0] |= 1
    return LaggedFibonacci(j, k, w, op, vals)


def period(j: int, k: int, w: int, op: str, values: Iterable[int]) -> Tuple[int, int]:
    """(tail length, period) of the state sequence, by exhaustive search; small cases only."""
    g = LaggedFibonacci(j, k, w, op, values)
    seen = {}
    n = 0
    while True:
        state = tuple(g.buf[(g.pos + i) % k] for i in range(k))
        if state in seen:
            return seen[state], n - seen[state]
        seen[state] = n
        g.next()
        n += 1


def max_period(k: int, w: int, op: str) -> int:
    """The maximal period when x^k + x^j + 1 is primitive modulo 2."""
    if op in ("add", "sub"):
        return (2**k - 1) * 2 ** (w - 1)
    if op == "mul":
        return (2**k - 1) * 2 ** max(w - 3, 0)
    return 2**k - 1


# ---- primitivity of trinomials over GF(2), with polynomials as ints ----

def _gf2_mulmod(u: int, v: int, mod: int) -> int:
    k = mod.bit_length() - 1
    r = 0
    while v:
        if v & 1:
            r ^= u
        v >>= 1
        u <<= 1
        if (u >> k) & 1:
            u ^= mod
    return r


def _gf2_xpow(n: int, mod: int) -> int:
    r, b = 1, 2
    while n:
        if n & 1:
            r = _gf2_mulmod(r, b, mod)
        b = _gf2_mulmod(b, b, mod)
        n >>= 1
    return r


def _is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    rng = random.Random(n)
    while True:
        c = rng.randrange(1, n)
        x = y = rng.randrange(2, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def prime_factors(n: int) -> List[int]:
    out, stack = set(), [n]
    while stack:
        x = stack.pop()
        if x == 1:
            continue
        if _is_probable_prime(x):
            out.add(x)
            continue
        d = _pollard_rho(x)
        stack += [d, x // d]
    return sorted(out)


def trinomial_is_primitive(k: int, j: int) -> bool:
    """Whether x^k + x^j + 1 is primitive over GF(2), for 0 < j < k."""
    mod = (1 << k) | (1 << j) | 1
    order = 2**k - 1
    if _gf2_xpow(order, mod) != 1:
        return False
    return all(_gf2_xpow(order // q, mod) != 1 for q in prime_factors(order))


# ---- Knuth's ran_array: subtractive lags (100, 37) modulo 2^30 ----

class KnuthRanArray:
    """A port of ran_start and ran_array from Knuth's rng.c (2002 version)."""

    KK, LL, MM = 100, 37, 1 << 30

    def __init__(self, seed: int) -> None:
        self.ran_x = [0] * self.KK
        self._start(seed)

    def _diff(self, x: int, y: int) -> int:
        return (x - y) & (self.MM - 1)

    def ran_array(self, n: int) -> List[int]:
        kk, ll = self.KK, self.LL
        if n < kk:
            raise ValueError("n must be at least 100")
        aa = self.ran_x[:] + [0] * (n - kk)
        for j in range(kk, n):
            aa[j] = self._diff(aa[j - kk], aa[j - ll])
        j = n
        for i in range(ll):
            self.ran_x[i] = self._diff(aa[j - kk], aa[j - ll])
            j += 1
        for i in range(ll, kk):
            self.ran_x[i] = self._diff(aa[j - kk], self.ran_x[i - ll])
            j += 1
        return aa

    def _start(self, seed: int) -> None:
        kk, ll, mm = self.KK, self.LL, self.MM
        x = [0] * (kk + kk - 1)
        ss = (seed + 2) & (mm - 2)
        for j in range(kk):
            x[j] = ss
            ss <<= 1
            if ss >= mm:
                ss -= mm - 2
        x[1] += 1
        ss, t = seed & (mm - 1), 70 - 1
        while t:
            for j in range(kk - 1, 0, -1):
                x[j + j], x[j + j - 1] = x[j], 0
            for j in range(kk + kk - 2, kk - 1, -1):
                x[j - (kk - ll)] = self._diff(x[j - (kk - ll)], x[j])
                x[j - kk] = self._diff(x[j - kk], x[j])
            if ss & 1:
                for j in range(kk, 0, -1):
                    x[j] = x[j - 1]
                x[0] = x[kk]
                x[ll] = self._diff(x[ll], x[kk])
            if ss:
                ss >>= 1
            else:
                t -= 1
        for j in range(ll):
            self.ran_x[j + kk - ll] = x[j]
        for j in range(ll, kk):
            self.ran_x[j - ll] = x[j]
        for _ in range(10):
            self.ran_array(kk + kk - 1)
