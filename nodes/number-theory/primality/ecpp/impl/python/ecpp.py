# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecpp/. The authors are listed in prov/5ZT65R.jsonl.

"""Atkin-Morain elliptic curve primality proving (ECPP).

ecpp(n) returns a primality certificate (a list of Step records) when n is
prime, and None when n is composite. The answer is never wrong: a None comes
with a proof that n is composite, and a certificate is a proof that n is
prime, which verify_certificate checks with the Goldwasser-Kilian theorem.
Randomness affects only the running time. The last number of a chain is
below 2^64 and is proved prime by the strong test to the first 12 prime
bases, which is exact below 2^64.

Each step finds a fundamental discriminant D < 0 with 4n = u^2 + |D| v^2, an
order m of a curve with complex multiplication by D that splits as m = k q
with q a probable prime above (n^(1/4) + 1)^2, builds the curve from a root of
the Hilbert class polynomial H_D modulo n, and checks [k]P != O and [m]P = O
for a point P. Then the primality of n follows from the primality of q.

Cost, with lg n binary digits and arbitrary precision integers (Python int):
heuristically O((log n)^2) discriminants and orders per step, each order
costing a probable prime test of O((log n)^3), and O(log n) steps, so
O((log n)^5) to O((log n)^6) in all; no part of this is proved.
"""

import math
import random
from decimal import Decimal, localcontext
from typing import NamedTuple

LEAF = 2**64
TRIAL_BOUND = 2**16
MAX_ABS_DISCRIMINANT = 10000
MAX_CLASS_NUMBER = 40
POINT_TRIES = 20
FIRST_12_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


class Composite(Exception):
    """Raised when the current number is proved composite."""


class Step(NamedTuple):
    """One link of a certificate: the curve y^2 = x^3 + a x + b modulo n,
    the point P = (x, y), and the order m = k q with [k]P != O, [m]P = O."""

    n: int
    a: int
    b: int
    x: int
    y: int
    k: int
    q: int


def primes_up_to(m: int) -> list[int]:
    """The primes p <= m, by the sieve of Eratosthenes."""
    if m < 2:
        return []
    sieve = bytearray([1]) * (m + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, math.isqrt(m) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, m + 1, i)))
    return [i for i in range(m + 1) if sieve[i]]


SMALL_PRIMES = primes_up_to(TRIAL_BOUND)


# ---------------------------------------------------------------- integers


def jacobi(a: int, n: int) -> int:
    """The Jacobi symbol (a/n) for odd n >= 1."""
    if n < 1 or n % 2 == 0:
        raise ValueError("n must be odd and positive")
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


def is_strong_probable_prime(n: int, base: int) -> bool:
    """The strong (Miller-Rabin) test of the odd number n > 2 to one base."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(base, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def is_prime_below_leaf(n: int) -> bool:
    """Exact primality for 0 <= n < 2^64: the strong test to the first 12
    primes has no composite liar below 2^64 (Sorenson and Webster 2017)."""
    if n >= LEAF:
        raise ValueError("n must be below 2^64")
    if n < 2:
        return False
    for p in FIRST_12_PRIMES:
        if n % p == 0:
            return n == p
    return all(is_strong_probable_prime(n, p) for p in FIRST_12_PRIMES)


def is_probable_prime(n: int) -> bool:
    """Exact below 2^64; above, the strong test to the first 12 primes."""
    if n < LEAF:
        return is_prime_below_leaf(n)
    if n % 2 == 0 or not is_strong_probable_prime(n, 2):
        return False
    return all(is_strong_probable_prime(n, p) for p in FIRST_12_PRIMES[1:])


def inverse(x: int, n: int) -> int:
    """x^(-1) modulo n; raises Composite if gcd(x, n) is a proper factor."""
    x %= n
    g = math.gcd(x, n)
    if g != 1:
        if g == n:
            raise ZeroDivisionError("x is 0 modulo n")
        raise Composite(g)
    return pow(x, -1, n)


def sqrt_mod(a: int, n: int) -> int | None:
    """Tonelli-Shanks: a root of y^2 = a modulo n, correct when n is an odd
    prime and (a/n) = 1. For other n it may return None or a wrong value, so
    the caller checks the answer."""
    a %= n
    if a == 0:
        return 0
    if n % 4 == 3:
        return pow(a, (n + 1) // 4, n)
    q, s = n - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while True:
        j = jacobi(z, n)
        if j == -1:
            break
        if j == 0:
            raise Composite(math.gcd(z, n))
        z += 1
    m, c, t, r = s, pow(z, q, n), pow(a, q, n), pow(a, (q + 1) // 2, n)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % n
            i += 1
            if i == m:
                return None
        b = pow(c, 1 << (m - i - 1), n)
        m, c = i, b * b % n
        t, r = t * c % n, r * b % n
    return r


def large_enough(q: int, n: int) -> bool:
    """Exact test of q > (n^(1/4) + 1)^2, that is n < (q^(1/2) - 1)^4."""
    if q <= 1:
        return False
    rest = q * q + 6 * q + 1 - n
    return rest > 0 and rest * rest > 16 * (q + 1) ** 2 * q


def cornacchia(d: int, n: int) -> tuple[int, int] | None:
    """Modified Cornacchia (Crandall and Pomerance, Algorithm 2.3.13): u, v
    with u^2 + d v^2 = 4n, for -D = d, D = 0 or 1 modulo 4 and (D/n) = 1. For
    a prime n the answer is None exactly when no solution exists. Raises
    Composite if no square root of D modulo n is found."""
    disc = -d % n
    x0 = sqrt_mod(disc, n)
    if x0 is None or x0 * x0 % n != disc:
        raise Composite()
    if (x0 + d) % 2:
        x0 = n - x0
    a, b, c = 2 * n, x0, math.isqrt(4 * n)
    while b > c:
        a, b = b, a % b
    t = 4 * n - b * b
    if t % d:
        return None
    v = math.isqrt(t // d)
    if v * v != t // d:
        return None
    return b, v


# ------------------------------------------------- discriminants and H_D


def _squarefree(m: int) -> bool:
    p = 2
    while p * p <= m:
        if m % (p * p) == 0:
            return False
        p += 1
    return True


def is_fundamental(D: int) -> bool:
    """D < 0 is a fundamental discriminant."""
    if D >= 0:
        return False
    if D % 4 == 1:
        return _squarefree(-D)
    if D % 4 == 0:
        return (D // 4) % 4 in (2, 3) and _squarefree(-D // 4)
    return False


def reduced_forms(D: int) -> list[tuple[int, int, int]]:
    """The reduced forms (a, b, c), b^2 - 4ac = D: |b| <= a <= c, and b >= 0
    when |b| = a or a = c. Their number is the class number h(D)."""
    forms = []
    a = 1
    while 3 * a * a <= -D:
        for b in range(-a + 1, a + 1):
            num = b * b - D
            if num % (4 * a):
                continue
            c = num // (4 * a)
            if c < a or (b < 0 and c == a):
                continue
            forms.append((a, b, c))
        a += 1
    return forms


_DISCRIMINANTS: list[int] = []


def discriminants() -> list[int]:
    """Fundamental D with |D| <= 10000 and h(D) <= 40, by h then |D|. The
    class numbers come from one pass over all reduced forms."""
    if not _DISCRIMINANTS:
        count: dict[int, int] = {}
        a = 1
        while 3 * a * a <= MAX_ABS_DISCRIMINANT:
            for b in range(-a + 1, a + 1):
                c = a
                while 4 * a * c - b * b <= MAX_ABS_DISCRIMINANT:
                    if not (b < 0 and c == a):
                        D = b * b - 4 * a * c
                        count[D] = count.get(D, 0) + 1
                    c += 1
            a += 1
        found = sorted((h, -D) for D, h in count.items() if h <= MAX_CLASS_NUMBER and is_fundamental(D))
        _DISCRIMINANTS.extend(-d for _, d in found)
    return _DISCRIMINANTS


def _pi() -> Decimal:
    """pi to the current precision (the recipe of the decimal module)."""
    with localcontext() as ctx:
        ctx.prec += 2
        lasts, t, s, n, na, d, da = 0, Decimal(3), Decimal(3), 1, 0, 0, 24
        while s != lasts:
            lasts = s
            n, na = n + na, na + 8
            d, da = d + da, da + 32
            t = (t * n) / d
            s += t
    return +s


def _cos_sin(x: Decimal) -> tuple[Decimal, Decimal]:
    """cos x and sin x by their Taylor series, for |x| <= 4."""
    with localcontext() as ctx:
        ctx.prec += 4
        cos_sum, sin_sum = Decimal(0), Decimal(0)
        term, k = Decimal(1), 0
        while term:
            if k % 2 == 0:
                cos_sum += term if k % 4 == 0 else -term
            else:
                sin_sum += term if k % 4 == 1 else -term
            k += 1
            term = term * x / k
            if abs(term) < Decimal(10) ** (-ctx.prec - 2):
                break
    return +cos_sum, +sin_sum


def _cmul(u: tuple[Decimal, Decimal], v: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def _cdiv(u: tuple[Decimal, Decimal], v: tuple[Decimal, Decimal]) -> tuple[Decimal, Decimal]:
    norm = v[0] * v[0] + v[1] * v[1]
    return ((u[0] * v[0] + u[1] * v[1]) / norm, (u[1] * v[0] - u[0] * v[1]) / norm)


def _j_value(a: int, b: int, D: int, pi: Decimal, digits: int) -> tuple[Decimal, Decimal]:
    """j((-b + i sqrt|D|) / (2a)) as j = (256 f + 1)^3 / f, f = q (P(q^2)/P(q))^24,
    with q = exp(2 pi i tau) and P(q) = prod (1 - q^k), the Euler series."""
    one = (Decimal(1), Decimal(0))
    decay = pi * Decimal(-D).sqrt() / a
    rho = (-decay).exp()
    c, s = _cos_sin(-pi * b / a)
    q = (rho * c, rho * s)
    top = int(Decimal(digits) * Decimal(10).ln() / decay) + 3
    powers = [one, q]
    for _ in range(2 * top + 2):
        powers.append(_cmul(powers[-1], q))

    def euler(step: int) -> tuple[Decimal, Decimal]:
        total = [Decimal(1), Decimal(0)]
        k = 1
        while (k * (3 * k - 1) // 2) * step < len(powers):
            sign = -1 if k % 2 else 1
            for e in (k * (3 * k - 1) // 2, k * (3 * k + 1) // 2):
                if e * step < len(powers):
                    total[0] += sign * powers[e * step][0]
                    total[1] += sign * powers[e * step][1]
            k += 1
        return (total[0], total[1])

    ratio = _cdiv(euler(2), euler(1))
    r24 = one
    for _ in range(24):
        r24 = _cmul(r24, ratio)
    f = _cmul(q, r24)
    g = (256 * f[0] + 1, 256 * f[1])
    return _cdiv(_cmul(_cmul(g, g), g), f)


_HILBERT: dict[int, list[int]] = {}


def hilbert_class_polynomial(D: int) -> list[int]:
    """H_D(X), coefficients from X^0 up (Crandall and Pomerance, Algorithm
    7.5.8), from the j-values of the reduced forms in high precision."""
    if D in _HILBERT:
        return _HILBERT[D]
    forms = reduced_forms(D)
    size = sum(math.pi * math.sqrt(-D) / a for a, _, _ in forms) / math.log(10)
    digits = int(size) + len(forms) + 40
    with localcontext() as ctx:
        ctx.prec = digits
        pi = _pi()
        poly = [(Decimal(1), Decimal(0))]
        for a, b, _ in forms:
            j = _j_value(a, b, D, pi, digits)
            neg = (-j[0], -j[1])
            new = [(Decimal(0), Decimal(0))] * (len(poly) + 1)
            for i, coef in enumerate(poly):
                new[i + 1] = (new[i + 1][0] + coef[0], new[i + 1][1] + coef[1])
                prod = _cmul(coef, neg)
                new[i] = (new[i][0] + prod[0], new[i][1] + prod[1])
            poly = new
        result = []
        tolerance = Decimal(10) ** -10
        for re, im in poly:
            near = int(re.to_integral_value())
            if abs(im) > tolerance or abs(re - near) > tolerance:
                raise ArithmeticError("precision too low for H_D")
            result.append(near)
    _HILBERT[D] = result
    return result


# -------------------------------------------------- polynomials modulo n


def _trim(f: list[int]) -> list[int]:
    while f and f[-1] == 0:
        f.pop()
    return f


def _poly_mul(f: list[int], g: list[int], n: int) -> list[int]:
    """f g modulo n, by Kronecker substitution."""
    if not f or not g:
        return []
    width = 2 * n.bit_length() + max(len(f), len(g)).bit_length() + 1
    big_f = 0
    for c in reversed(f):
        big_f = (big_f << width) | c
    big_g = 0
    for c in reversed(g):
        big_g = (big_g << width) | c
    prod = big_f * big_g
    mask = (1 << width) - 1
    out = []
    for _ in range(len(f) + len(g) - 1):
        out.append((prod & mask) % n)
        prod >>= width
    return _trim(out)


def _monic(f: list[int], n: int) -> list[int]:
    lead = inverse(f[-1], n)
    return [c * lead % n for c in f]


def _poly_rem(f: list[int], g: list[int], n: int) -> list[int]:
    """f modulo the monic polynomial g, over Z_n."""
    f = list(f)
    dg = len(g) - 1
    for i in range(len(f) - 1, dg - 1, -1):
        c = f[i] % n
        if c:
            for t in range(dg):
                f[i - dg + t] -= c * g[t]
        f[i] = 0
    return _trim([c % n for c in f[:dg]])


def _poly_gcd(f: list[int], g: list[int], n: int) -> list[int]:
    """Monic gcd over Z_n; raises Composite if a leading coefficient is not
    invertible."""
    f, g = _trim(list(f)), _trim(list(g))
    while g:
        g = _monic(g, n)
        f, g = g, _poly_rem(f, g, n)
    return _monic(f, n) if f else f


def _poly_pow(base: list[int], e: int, g: list[int], n: int) -> list[int]:
    """base^e modulo (g, n), g monic, by left-to-right binary powering."""
    result = [1]
    for bit in bin(e)[2:]:
        result = _poly_rem(_poly_mul(result, result, n), g, n)
        if bit == "1":
            result = _poly_rem(_poly_mul(result, base, n), g, n)
    return result


def find_root(poly: list[int], n: int, rng: random.Random, tries: int = 64) -> int | None:
    """A root modulo n of poly, by the Cantor-Zassenhaus split, or None. A
    returned value r always has poly(r) = 0 modulo n."""
    h = _trim([c % n for c in poly])
    if len(h) < 2:
        return None
    h = _monic(h, n)
    # The distinct linear factors of h: g = gcd(h, X^n - X).
    x_n = _poly_pow([0, 1], n, h, n)
    x_n += [0] * (2 - len(x_n))
    x_n[1] -= 1
    g = _poly_gcd(h, _trim([c % n for c in x_n]), n)
    while len(g) > 2:
        # Split g by gcd(g, (X + t)^((n-1)/2) - 1) for a random t.
        for _ in range(tries):
            w = _poly_pow([rng.randrange(n), 1], (n - 1) // 2, g, n) or [0]
            w[0] -= 1
            d = _poly_gcd(g, _trim([c % n for c in w]), n)
            if 1 < len(d) < len(g):
                g = d
                break
        else:
            return None
    if len(g) != 2:
        return None
    root = -g[0] % n
    value = 0
    for c in reversed(poly):
        value = (value * root + c) % n
    return root if value == 0 else None


# ------------------------------------------------- curves modulo n


Point = tuple[int, int] | None


def ec_add(p: Point, r: Point, a: int, n: int) -> Point:
    """p + r on y^2 = x^3 + a x + b over Z_n (None is O). Every step is valid
    modulo each prime factor of n, or Composite is raised."""
    if p is None:
        return r
    if r is None:
        return p
    x1, y1 = p
    x2, y2 = r
    if x1 == x2:
        if (y1 + y2) % n == 0:
            return None
        if y1 != y2:
            # For a prime n, equal x forces y1 = y2 or y1 = -y2.
            g = math.gcd(y1 - y2, n)
            raise Composite(g) if 1 < g < n else Composite()
        lam = (3 * x1 * x1 + a) * inverse(2 * y1, n) % n
    else:
        lam = (y2 - y1) * inverse(x2 - x1, n) % n
    x3 = (lam * lam - x1 - x2) % n
    return (x3, (lam * (x1 - x3) - y1) % n)


def ec_mul(k: int, p: Point, a: int, n: int) -> Point:
    """[k]p for k >= 1, by left-to-right double and add."""
    result: Point = None
    for bit in bin(k)[2:]:
        result = ec_add(result, result, a, n)
        if bit == "1":
            result = ec_add(result, p, a, n)
    return result


def curve_orders(d: int, n: int, u: int, v: int) -> list[int]:
    """The orders of the curves with complex multiplication by D = -d over
    F_n, n prime, given u^2 + d v^2 = 4n."""
    if d == 4:
        return [n + 1 + u, n + 1 - u, n + 1 + 2 * v, n + 1 - 2 * v]
    if d == 3:
        s, t = (u + 3 * v) // 2, (u - 3 * v) // 2
        return [n + 1 + u, n + 1 - u, n + 1 + s, n + 1 - s, n + 1 + t, n + 1 - t]
    return [n + 1 + u, n + 1 - u]


def _nonresidue(n: int, noncube: bool) -> int | None:
    """The least g with (g/n) = -1 and, if asked, g^((n-1)/3) != 1."""
    for g in range(2, min(n, 10**5)):
        j = jacobi(g, n)
        if j == 0:
            raise Composite(math.gcd(g, n))
        if j == -1 and (not noncube or pow(g, (n - 1) // 3, n) != 1):
            return g
    return None


def twists(D: int, j: int, n: int) -> list[tuple[int, int]] | None:
    """The curves (a, b) with j-invariant j (CM by D) up to isomorphism over
    F_n, n prime: 6 for D = -3, 4 for D = -4, 2 otherwise (Algorithm 7.5.9)."""
    if D == -3:
        g = _nonresidue(n, True)
        return None if g is None else [(0, -pow(g, e, n) % n) for e in range(6)]
    g = _nonresidue(n, False)
    if g is None:
        return None
    if D == -4:
        return [(-pow(g, e, n) % n, 0) for e in range(4)]
    if j % n in (0, 1728 % n):
        return None
    c = j * inverse(j - 1728, n) % n
    a, b = -3 * c % n, 2 * c % n
    return [(a, b), (a * g * g % n, b * g * g * g % n)]


def random_point(a: int, b: int, n: int, rng: random.Random, tries: int = 200) -> tuple[int, int] | None:
    """A point (x, y) on y^2 = x^3 + a x + b modulo n with y != 0, or None
    after the given number of tries (for a prime n each try succeeds with
    probability about 1/2)."""
    for _ in range(tries):
        x = rng.randrange(n)
        rhs = (x * x * x + a * x + b) % n
        j = jacobi(rhs, n)
        if j == 1:
            y = sqrt_mod(rhs, n)
            if y is None or y * y % n != rhs:
                raise Composite()
            return (x, y)
        if j == 0 and rhs:
            raise Composite(math.gcd(rhs, n))
    return None


def split_order(m: int, n: int, bad: set[int]) -> tuple[int, int] | None:
    """m = k q with k > 1, q a probable prime above (n^(1/4) + 1)^2 and not
    in bad, after removing the primes up to min(2^16, n^(1/2)) from m."""
    limit = min(TRIAL_BOUND, math.isqrt(n))
    q = m
    for p in SMALL_PRIMES:
        if p > limit:
            break
        while q % p == 0:
            q //= p
    k = m // q
    if k == 1 or q in bad or not large_enough(q, n) or not is_probable_prime(q):
        return None
    return k, q


# ------------------------------------------------------------- the test


def _step(n: int, rng: random.Random, bad: set[int]) -> Step:
    """One Atkin-Morain step for n >= 2^64 (or the leaf bound): returns a
    Step whose q is a smaller probable prime, or raises Composite."""
    for D in discriminants():
        d = -D
        if d >= 4 * n or jacobi(D, n) != 1:  # @line L7
            continue
        solution = cornacchia(d, n)
        if solution is None:
            continue
        u, v = solution
        j = None
        for m in curve_orders(d, n, u, v):  # @line L8
            split = split_order(m, n, bad)
            if split is None:
                continue
            k, q = split
            if j is None:
                j = find_root(hilbert_class_polynomial(D), n, rng)  # @line L9
                if j is None:
                    break
            curves = twists(D, j, n)
            if curves is None:
                break
            refuted = 0
            for a, b in curves:  # @line L10
                g = math.gcd((4 * a**3 + 27 * b * b) % n, n)
                if g != 1:
                    raise Composite(g)
                for _ in range(POINT_TRIES):
                    point = random_point(a, b, n, rng)  # @line L11
                    if point is None:
                        break
                    x, y = point
                    u_point = ec_mul(k, point, a, n)
                    if u_point is None:
                        continue
                    if ec_mul(q, u_point, a, n) is None:  # @line L12
                        return Step(n, a, b, x, y, k, q)
                    refuted += 1
                    break
            if refuted == len(curves):
                raise Composite()  # @line L13
    raise RuntimeError("no suitable discriminant in the table")  # @line L14


def ecpp(n: int, rng: random.Random | None = None, leaf: int = LEAF) -> list[Step] | None:
    """A certificate of primality for n (a list of Step records, empty when
    n < leaf), or None if n is composite. The leaf bound must lie in
    [50, 2^64]; smaller values only make the chains longer."""
    if not 50 <= leaf <= LEAF:
        raise ValueError("leaf must be in [50, 2^64]")
    rng = rng if rng is not None else random.Random()
    chain: list[Step] = []  # @line L1
    bad: set[int] = set()
    while True:  # @line L2
        try:
            if n < leaf:  # @line L3
                if is_prime_below_leaf(n):
                    return chain  # @line L4
                raise Composite()  # @line L5
            if n % 2 == 0 or n % 3 == 0 or math.isqrt(n) ** 2 == n or not is_strong_probable_prime(n, 2):
                raise Composite()  # @line L6
            step = _step(n, rng, bad)
            chain.append(step)
            n = step.q
        except Composite:
            if not chain:
                return None  # @line L15
            bad.add(n)  # @line L16
            n = chain.pop().n
        except RuntimeError:
            if not chain:
                raise
            bad.add(n)
            n = chain.pop().n


def verify_certificate(n: int, chain: list[Step]) -> bool:
    """Check a certificate with the Goldwasser-Kilian theorem: for each step,
    n coprime to 6, a nonsingular curve, P on it, q > (n^(1/4) + 1)^2,
    [k]P != O and [q]([k]P) = O; and the last number prime below 2^64."""
    for st in chain:
        if st.n != n or n < 5 or math.gcd(n, 6) != 1 or st.k < 1:
            return False
        if math.gcd((4 * st.a**3 + 27 * st.b**2) % n, n) != 1:
            return False
        if (st.y * st.y - st.x**3 - st.a * st.x - st.b) % n:
            return False
        if not large_enough(st.q, n):
            return False
        try:
            u_point = ec_mul(st.k, (st.x % n, st.y % n), st.a % n, n)
            if u_point is None or ec_mul(st.q, u_point, st.a % n, n) is not None:
                return False
        except (Composite, ZeroDivisionError):
            return False
        n = st.q
    return n < LEAF and is_prime_below_leaf(n)
