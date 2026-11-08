# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lecuyer-combined-generator/. The authors are listed in prov/9FJDDG.jsonl.

"""L'Ecuyer's combined generators: several MRGs with distinct prime moduli, summed modulo m_1."""

import math
import random
from fractions import Fraction
from typing import List, Sequence, Tuple


class MRG:
    """x_n = (a_1 x_(n-1) + ... + a_k x_(n-k)) mod m; state holds (x_(n-k), ..., x_(n-1))."""

    def __init__(self, m: int, coeffs: Sequence[int], seed: Sequence[int]) -> None:
        if m < 2 or not coeffs:
            raise ValueError("need m >= 2 and at least one coefficient")
        if len(seed) != len(coeffs):
            raise ValueError("the seed needs one value per coefficient")
        if any(not 0 <= v < m for v in seed) or not any(seed):
            raise ValueError("seed values must be in [0, m) and not all zero")
        self.m, self.a = m, [c % m for c in coeffs]
        self.state = list(seed)

    def next(self) -> int:
        k = len(self.a)
        x = sum(self.a[i] * self.state[k - 1 - i] for i in range(k)) % self.m  # @line L3
        self.state = self.state[1:] + [x]  # @line L4
        return x


class CombinedMRG:
    """z_n = (sum_j delta_j x_(j,n)) mod m_1 and u_n = z_n / m_1 (with z = 0 mapped inside (0, 1))."""

    def __init__(self, components: Sequence[MRG], deltas: Sequence[int], denominator_plus_one: bool = True) -> None:
        if len(components) != len(deltas) or not components:
            raise ValueError("need one delta per component")
        self.comp, self.delta = list(components), list(deltas)
        self.m1 = self.comp[0].m
        self.plus_one = denominator_plus_one
        self.last_x: List[int] = []

    def next_z(self) -> int:
        z = 0  # @line L1
        xs = []
        for c, d in zip(self.comp, self.delta):  # @line L2
            x = c.next()
            xs.append(x)
            z += d * x  # @line L5
        self.last_x = xs
        return z % self.m1  # @line L6

    def uniform(self) -> float:
        """A value in (0, 1): z / (m_1 + 1), or m_1 / (m_1 + 1) when z = 0 (as in MRG32k3a)."""
        z = self.next_z()
        if self.plus_one:
            return (z if z > 0 else self.m1) / (self.m1 + 1)  # @line L7
        return z / self.m1

    def exact_w(self) -> Fraction:
        """The exact combination w_n = (sum_j delta_j x_(j,n) / m_j) mod 1 for the last step."""
        w = sum(Fraction(d * x, c.m) for c, d, x in zip(self.comp, self.delta, self.last_x))
        return w - math.floor(w)


def equivalent_mrg(components: Sequence[MRG], deltas: Sequence[int]) -> Tuple[int, List[int], List[int]]:
    """The single MRG modulo m = prod m_j that produces m * w_n exactly.

    Returns (m, coefficients, weights), where weights[j] = delta_j * (m / m_j) mod m,
    so that X_n = sum_j weights[j] x_(j,n) mod m equals m * w_n. Moduli must be
    pairwise coprime.
    """
    ms = [c.m for c in components]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            if math.gcd(ms[i], ms[j]) != 1:
                raise ValueError("moduli must be pairwise coprime")
    m = math.prod(ms)
    k = max(len(c.a) for c in components)
    coeffs = []
    for i in range(k):
        # Chinese remainder theorem: a_i = a_(j,i) mod m_j for every j.
        a = 0
        for c in components:
            aj = c.a[i] if i < len(c.a) else 0
            mj = c.m
            nj = m // mj
            a += aj * nj * pow(nj, -1, mj)
        coeffs.append(a % m)
    weights = [(d * (m // c.m)) % m for c, d in zip(components, deltas)]
    return m, coeffs, weights


def lecuyer1988(s1: int = 12345, s2: int = 67890) -> Tuple[MRG, MRG]:
    """The two LCG components of L'Ecuyer (1988)."""
    return MRG(2147483563, [40014], [s1]), MRG(2147483399, [40692], [s2])


def lecuyer1988_next(c1: MRG, c2: MRG) -> int:
    """One output of the 1988 combination: z = (x_1 - x_2) mod (m_1 - 1), with 0 replaced by m_1 - 1."""
    z = (c1.next() - c2.next()) % (c1.m - 1)
    return z if z > 0 else c1.m - 1


MRG32K3A_M1 = 4294967087
MRG32K3A_M2 = 4294944443


def mrg32k3a(seed: Sequence[int] = (12345,) * 6) -> CombinedMRG:
    """MRG32k3a: two order-3 MRGs, combined as (x_1 - x_2) mod m_1, output z / (m_1 + 1)."""
    c1 = MRG(MRG32K3A_M1, [0, 1403580, -810728], list(seed[:3]))
    c2 = MRG(MRG32K3A_M2, [527612, 0, -1370589], list(seed[3:]))
    return CombinedMRG([c1, c2], [1, -1])


# ---- primitivity of the characteristic polynomial modulo a prime ----

def _polmulmod(u: List[int], v: List[int], monic: List[int], p: int) -> List[int]:
    k = len(monic) - 1
    r = [0] * (2 * k - 1)
    for i, x in enumerate(u):
        if x:
            for j, y in enumerate(v):
                r[i + j] = (r[i + j] + x * y) % p
    for d in range(len(r) - 1, k - 1, -1):
        c = r[d]
        if c:
            for i in range(k + 1):
                r[d - k + i] = (r[d - k + i] - c * monic[i]) % p
    return (r[:k] + [0] * k)[:k]


def _zpow(n: int, monic: List[int], p: int) -> List[int]:
    k = len(monic) - 1
    res = [1 % p] + [0] * (k - 1)
    base = ([0, 1] + [0] * k)[:k] if k > 1 else [(-monic[0]) % p]
    while n:
        if n & 1:
            res = _polmulmod(res, base, monic, p)
        base = _polmulmod(base, base, monic, p)
        n >>= 1
    return res


def _is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
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


def prime_factors(n: int) -> List[int]:
    out, stack = set(), [n]
    while stack:
        x = stack.pop()
        if x == 1:
            continue
        if _is_probable_prime(x):
            out.add(x)
            continue
        if x % 2 == 0:
            stack += [2, x // 2]
            continue
        rng = random.Random(x)
        while True:
            c = rng.randrange(1, x)
            a = b = rng.randrange(2, x)
            d = 1
            while d == 1:
                a = (a * a + c) % x
                b = (b * b + c) % x
                b = (b * b + c) % x
                d = math.gcd(abs(a - b), x)
            if d != x:
                break
        stack += [d, x // d]
    return sorted(out)


def mrg_is_primitive(m: int, coeffs: Sequence[int]) -> bool:
    """Whether z^k - a_1 z^(k-1) - ... - a_k is primitive modulo the prime m.

    Then every nonzero seed gives the maximal period m^k - 1.
    """
    k = len(coeffs)
    monic = [(-coeffs[k - 1 - i]) % m for i in range(k)] + [1]
    order = m**k - 1
    one = [1] + [0] * (k - 1)
    if _zpow(order, monic, m) != one:
        return False
    return all(_zpow(order // q, monic, m) != one for q in prime_factors(order))


def state_period(component: MRG) -> int:
    """Period of one component by stepping; small moduli only."""
    start = list(component.state)
    n = 0
    while True:
        component.next()
        n += 1
        if component.state == start:
            return n
