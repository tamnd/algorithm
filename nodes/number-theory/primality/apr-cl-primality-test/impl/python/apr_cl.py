# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apr-cl-primality-test/. The authors are listed in prov/MW7HYF.jsonl.
"""The APR-CL primality test with Jacobi sums (Adleman, Pomerance, Rumely,
Cohen and Lenstra), in the form of the page.

The test uses an even t with t/2 odd and primes q_1 < ... < q_j with
q_i - 1 | t and s = q_1 ... q_j > sqrt(n). For each prime q | s and each
odd prime p | q - 1 it checks that a power of the Jacobi sum J(p, q) is a
root of unity modulo n, in the ring Z[zeta_m] with m = p^k exactly dividing
q - 1. For p = 2 it checks (-q)^((n - 1)/2) = +1 or -1. If all checks pass,
every prime factor of n is a power of n modulo s, and a search over the
t powers finds a factor of each composite n.

aprcl(n) returns True or False, and None only if the search for an extra
prime in line L16 gives up, which does not happen for any n tested.
"""

from __future__ import annotations

from functools import lru_cache
from math import gcd, isqrt, lcm
from typing import NamedTuple

# Values of t, each 2 times an odd number, in increasing order. The
# largest gives s > 10^295, so the table covers n below about 10^590.
T_TABLE = (
    2, 6, 30, 90, 210, 630, 2310, 6930, 30030, 90090, 117810, 139230,
    270270, 450450, 1531530, 2645370, 4594590, 7657650, 29099070,
)
# Extra primes q tried for one odd p in line L16 before the test gives up.
EXTRA_TRIES = 60

Poly = list[int]


class Plan(NamedTuple):
    """The data of line L2: the primes q dividing s, s itself, and t."""

    primes: tuple[int, ...]
    s: int
    t: int


def small_is_prime(n: int) -> bool:
    """Trial division; used only for numbers below 10^8 (t + 1 and q)."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_factors(n: int) -> list[int]:
    """The distinct prime factors of a small n > 0, by trial division."""
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def divisors(n: int) -> list[int]:
    ds = [1]
    for p in prime_factors(n):
        e = 0
        m = n
        while m % p == 0:
            m //= p
            e += 1
        ds = [d * p**i for d in ds for i in range(e + 1)]
    return sorted(ds)


def valuation(p: int, n: int) -> int:
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


@lru_cache(maxsize=None)
def candidate_primes(t: int) -> tuple[int, ...]:
    """All primes q with q - 1 | t, in increasing order."""
    return tuple(d + 1 for d in divisors(t) if small_is_prime(d + 1))


def plan(n: int) -> Plan:
    """Line L2: the first t of the table with enough primes, and the
    shortest list of the smallest such primes with s^2 > n."""
    for t in T_TABLE:
        s = 1
        chosen: list[int] = []
        for q in candidate_primes(t):
            chosen.append(q)
            s *= q
            if s * s > n:
                return Plan(tuple(chosen), s, lcm(*(q - 1 for q in chosen)))
    raise ValueError("n is too large for the table of t")


def primitive_root(q: int) -> int:
    """The least primitive root of the prime q."""
    if q == 2:
        return 1
    fs = prime_factors(q - 1)
    g = 2
    while any(pow(g, (q - 1) // f, q) == 1 for f in fs):
        g += 1
    return g


@lru_cache(maxsize=4096)
def jacobi_sums(q: int) -> dict[int, tuple[int, ...]]:
    """For each odd prime p | q - 1, with m = p^k exactly dividing q - 1, the
    Jacobi sum J(p, q) = sum of chi(x) chi(1 - x) over x in F_q, as the
    coefficients of 1, z, ..., z^(m-1) with z a primitive m-th root of 1.
    Here chi(g^i) = z^i for the least primitive root g."""
    g = primitive_root(q)
    order = q - 1
    log = [0] * q
    x = 1
    for i in range(order):
        log[x] = i
        x = x * g % q
    # e(i) = i + log(1 - g^i) for 1 <= i <= q - 2; count e(i) mod L.
    ms = {p: p ** valuation(p, order) for p in prime_factors(order) if p > 2}
    if not ms:
        return {}
    big = lcm(*ms.values())
    counts = [0] * big
    x = 1
    for i in range(1, order):
        x = x * g % q
        counts[(i + log[q + 1 - x]) % big] += 1
    return {p: tuple(sum(counts[j::m]) for j in range(m)) for p, m in ms.items()}


def unit_w(m: int, p: int) -> int:
    """w = sum over y in (Z/m)^* of floor(2y/m) / y modulo m. The proof
    needs p not dividing w; plan_pairs checks it."""
    return sum((2 * y // m) * pow(y, -1, m) for y in range(1, m) if y % p) % m


# Arithmetic in Z[zeta_m] = Z[x]/(Phi_m(x)) modulo n. An element is the
# list of its phi(m) coefficients on 1, x, ..., x^(phi(m) - 1).


def reduce_cyclotomic(a: Poly, m: int, p: int) -> Poly:
    """The image in Z[x]/(Phi_m) of a polynomial a of degree below m, with
    Phi_m(x) = sum of x^(i m/p) for 0 <= i < p. Coefficients are not
    reduced modulo n."""
    a = list(a) + [0] * (m - len(a))
    step = m // p
    deg = m - step
    for i in range(m - 1, deg - 1, -1):
        c = a[i]
        if c:
            a[i] = 0
            for j in range(p - 1):
                a[i - deg + j * step] -= c
    return a[:deg]


class Ring:
    """Z[zeta_m] modulo n, for m = p^k with p prime and gcd(m, n) = 1."""

    def __init__(self, m: int, p: int, n: int) -> None:
        self.m = m
        self.p = p
        self.n = n
        self.deg = m - m // p

    def one(self) -> Poly:
        return [1] + [0] * (self.deg - 1)

    def from_cyclic(self, a: Poly) -> Poly:
        """The image of an element of Z[x]/(x^m - 1), given by m coefficients."""
        return [c % self.n for c in reduce_cyclotomic(a, self.m, self.p)]

    def mul(self, a: Poly, b: Poly) -> Poly:
        """Schoolbook product, then x^m = 1, then Phi_m, then mod n."""
        d, m = self.deg, self.m
        c = [0] * (2 * d - 1)
        if a is b:
            for i in range(d):
                ai = a[i]
                if ai:
                    c[2 * i] += ai * ai
                    ai2 = 2 * ai
                    for j in range(i + 1, d):
                        c[i + j] += ai2 * a[j]
        else:
            for i in range(d):
                ai = a[i]
                if ai:
                    for j in range(d):
                        c[i + j] += ai * b[j]
        if len(c) > m:
            for i in range(m, len(c)):
                c[i - m] += c[i]
            del c[m:]
        return [v % self.n for v in reduce_cyclotomic(c, m, self.p)]

    def power(self, a: Poly, e: int) -> Poly:
        """a^e, by binary powering for small e and with a window of 4
        binary digits for large e."""
        result = self.one()
        if e < 64:
            base = a
            while e:
                if e & 1:
                    result = self.mul(result, base)
                e >>= 1
                if e:
                    base = self.mul(base, base)
            return result
        table = [result, a]
        for _ in range(14):
            table.append(self.mul(table[-1], a))
        started = False
        for shift in range((e.bit_length() + 3) // 4 * 4 - 4, -4, -4):
            if started:
                for _ in range(4):
                    result = self.mul(result, result)
            digit = (e >> shift) & 15
            if digit:
                result = self.mul(result, table[digit]) if started else table[digit]
                started = True
        return result

    def sigma(self, a: Poly, c: int) -> Poly:
        """The automorphism zeta -> zeta^c, for c prime to m."""
        m = self.m
        out = [0] * m
        for i, v in enumerate(a):
            out[i * c % m] = v
        return self.from_cyclic(out)

    def root_index(self, a: Poly) -> int | None:
        """The h in [0, m) with a = zeta^h, or None if there is none."""
        for h in range(self.m):
            unit = [0] * self.m
            unit[h] = 1
            if self.from_cyclic(unit) == a:
                return h
        return None


def jacobi_power(n: int, q: int, p: int) -> int | None:
    """Lines L9 to L11 for the pair (p, q): S = J(p, q)^(alpha_n) modulo n,
    where alpha_n = sum over y of floor(n y/m) sigma_y^(-1). Returns the h
    with S = zeta^h, or None if S is not a root of unity."""
    coeffs = jacobi_sums(q)[p]  # @line L9
    m = len(coeffs)
    ring = Ring(m, p, n)
    j = ring.from_cyclic(list(coeffs))
    units = [y for y in range(1, m) if y % p]
    # S = (J^theta)^(n // m) * J^(alpha_r), theta = sum y sigma_y^(-1).
    s1 = ring.one()
    for y in units:
        s1 = ring.mul(s1, ring.power(ring.sigma(j, pow(y, -1, m)), y))
    r = n % m
    s3 = ring.one()
    for y in units:
        f = r * y // m
        if f:
            s3 = ring.mul(s3, ring.power(ring.sigma(j, pow(y, -1, m)), f))
    big_s = ring.mul(ring.power(s1, n // m), s3)  # @line L10
    return ring.root_index(big_s)


def is_square(n: int) -> bool:
    return n >= 0 and isqrt(n) ** 2 == n


def jacobi_symbol(a: int, n: int) -> int:
    """The Jacobi symbol (a/n) for odd n > 0."""
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def check_units(primes: tuple[int, ...]) -> None:
    for q in primes:
        for p in prime_factors(q - 1):
            if p > 2:
                m = p ** valuation(p, q - 1)
                if unit_w(m, p) % p == 0:
                    raise ValueError("p divides w(m); use another Jacobi sum")


def make_plan(n: int, primes: tuple[int, ...] | None) -> Plan:
    """The plan of line L2, or a given list of primes, checked: each q is 2
    or a prime with q = 3 mod 4, and s^2 > n."""
    if primes is None:
        return plan(n)
    for q in primes:
        if not small_is_prime(q) or (q > 2 and q % 4 != 3):
            raise ValueError("each q must be 2 or a prime q = 3 mod 4")
    s = 1
    for q in primes:
        s *= q
    if s * s <= n:
        raise ValueError("s^2 must exceed n")
    return Plan(tuple(sorted(primes)), s, lcm(*(q - 1 for q in primes)))


def divisor_search(n: int, s: int, t: int) -> int | None:
    """Lines L17 to L19: the first n^i mod s, 1 <= i < t, that is a proper
    factor of n, or None."""
    nm = n % s
    r = 1
    for _ in range(1, t):  # @line L17
        r = r * nm % s  # @line L18
        if 1 < r < n and n % r == 0:  # @line L19
            return r
    return None


def aprcl(n: int, primes: tuple[int, ...] | None = None) -> bool | None:
    """True if n is prime, False if not. None only if line L16 gives up.
    The optional primes replace the table choice of line L2 (for tests)."""
    if n < 2:  # @line L1
        return False
    primes, s, t = make_plan(n, primes)  # @line L2
    check_units(primes)
    small = set(primes) | set(prime_factors(t))
    if n in small:  # @line L3
        return True
    if gcd(n, t * s) > 1:  # @line L4
        return False
    odd_ps = [p for p in prime_factors(t) if p > 2]
    done = {p: pow(n, p - 1, p * p) != 1 for p in odd_ps}  # @line L5
    done[2] = n % 4 == 3  # @line L6
    for q in primes:  # @line L7
        if q == 2:
            continue
        for p in prime_factors(q - 1):  # @line L8
            if p == 2:
                continue
            h = jacobi_power(n, q, p)
            if h is None:  # @line L11
                return False
            if h % p:  # @line L12
                done[p] = True
        e = pow(-q % n, (n - 1) // 2, n)  # @line L13
        if e not in (1, n - 1):  # @line L14
            return False
        if e == n - 1:  # @line L15
            done[2] = True
    for p in sorted(done):  # @line L16
        if done[p]:
            continue
        verdict = extra_check(n, p, set(primes))
        if verdict is not True:
            return verdict
    return divisor_search(n, s, t) is None  # @line L20


def extra_check(n: int, p: int, used: set[int]) -> bool | None:
    """Line L16 for one p: True when the condition L_p is now proved,
    False when n is shown composite, None when the tries run out."""
    if p == 2:
        # Here n = 1 mod 4. Find z with Jacobi symbol (z/n) = -1; for a
        # prime n, Euler's criterion gives z^((n-1)/2) = -1.
        if is_square(n):
            return False
        z = 2
        while True:
            j = jacobi_symbol(z, n)
            if j == 0:
                return False
            if j == -1:
                return pow(z, (n - 1) // 2, n) == n - 1
            z += 1
    tries = 0
    q = 2 * p + 1
    while tries < EXTRA_TRIES:
        if q not in used and small_is_prime(q):
            if n % q == 0:
                return n == q
            tries += 1
            h = jacobi_power(n, q, p)
            if h is None:
                return False
            if h % p:
                return True
        q += 2 * p
    return None


class Report(NamedTuple):
    """The data that the worked example shows."""

    primes: tuple[int, ...]
    s: int
    t: int
    roots: dict[tuple[int, int], int]
    signs: dict[int, int]
    factor: int | None


def trace(n: int) -> Report:
    """Run the main checks for n and record the h of each pair, the sign
    (-q)^((n-1)/2) of each q, and the factor that lines L17 to L19 find
    (None if there is none)."""
    primes, s, t = plan(n)
    roots: dict[tuple[int, int], int] = {}
    signs: dict[int, int] = {}
    for q in primes:
        if q == 2:
            continue
        for p in prime_factors(q - 1):
            if p > 2:
                h = jacobi_power(n, q, p)
                roots[(p, q)] = -1 if h is None else h
        e = pow(-q % n, (n - 1) // 2, n)
        signs[q] = -1 if e == n - 1 else e
    return Report(primes, s, t, roots, signs, divisor_search(n, s, t))


def gauss_jacobi_check(q: int, p: int) -> bool:
    """J(p, q) times its complex conjugate is q in Z[zeta_m]: a check of the
    Jacobi sums used in the tests."""
    coeffs = list(jacobi_sums(q)[p])
    m = len(coeffs)
    conj = [0] * m
    for i, v in enumerate(coeffs):
        conj[(-i) % m] = v
    full = [0] * m
    for i, a in enumerate(coeffs):
        if a:
            for k, b in enumerate(conj):
                full[(i + k) % m] += a * b
    red = reduce_cyclotomic(full, m, p)
    return red == [q] + [0] * (len(red) - 1)

