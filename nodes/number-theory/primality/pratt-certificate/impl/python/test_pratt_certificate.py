# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pratt-certificate/. The authors are listed in prov/QY13TB.jsonl.

import math
import random

from pratt_certificate import _probable_prime as probably_prime
from pratt_certificate import build_pratt, factorize, multiplications, verify_cost, verify_pratt

LIMIT = 100_000


def sieve(n: int) -> list[bool]:
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_p[i]:
            is_p[i * i :: i] = [False] * len(is_p[i * i :: i])
    return is_p


def is_prime_td(n: int) -> bool:
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


CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361]
STRONG_PSP = [2047, 1373653, 25326001, 3215031751, 2152302898747, 3474749660383, 341550071728321, 3825123056546413051]


def test_example_1279() -> None:
    cert = build_pratt(1279)
    assert cert == [
        (3, 2, {2: 1}),
        (5, 2, {2: 2}),
        (7, 3, {2: 1, 3: 1}),
        (71, 7, {2: 1, 5: 1, 7: 1}),
        (1279, 3, {2: 1, 3: 2, 71: 1}),
    ]
    assert verify_pratt(1279, cert)
    assert pow(3, 639, 1279) == 1278 and pow(3, 213, 1279) == 775 and pow(3, 9, 1279) == 498
    assert pow(7, 35, 71) == 70 and pow(7, 7, 71) == 14 and pow(7, 5, 71) == 51
    assert verify_cost(cert) == 48  # Crandall and Pomerance: M(1279) = 48
    assert [multiplications(e) for e in (639, 213, 9, 35, 7, 5, 2, 3, 1)] == [16, 11, 4, 7, 4, 3, 1, 2, 0]


def test_small_inputs() -> None:
    assert verify_pratt(2, []) and build_pratt(2) == []
    for n in (-7, 0, 1, 4, 6, 100):
        assert not verify_pratt(n, []) and build_pratt(n) is None
    assert verify_pratt(3, [(3, 2, {2: 1})])
    assert not verify_pratt(3, [])


def test_all_n_up_to_limit() -> None:
    is_p = sieve(LIMIT)
    rng = random.Random(1)
    for n in range(LIMIT + 1):
        cert = build_pratt(n, rng)
        if is_p[n]:
            assert cert is not None and verify_pratt(n, cert), n
            # The certificate is short: fewer than lg n entries, fewer than 2 lg^2 n products.
            if n > 2:
                assert len(cert) < math.log2(n) and verify_cost(cert) < 2 * math.log2(n) ** 2, n
        else:
            assert cert is None, n


def subcertificate(f: dict[int, int], rng: random.Random) -> list:
    """Certificates of the odd primes of f, merged, each prime once."""
    out: list = []
    for q in sorted(f):
        if q != 2:
            out += [e for e in build_pratt(q, rng) if e[0] not in {x[0] for x in out}]
    return out


def test_composites_are_never_certified() -> None:
    """For an odd composite p no base satisfies the conditions, so an entry
    for p always fails. Try every base for all odd composites below 1000."""
    rng = random.Random(0)
    for p in range(9, 1000, 2):
        if is_prime_td(p):
            continue
        f = factorize(p - 1, rng)
        sub = subcertificate(f, rng)
        assert verify_pratt(sub[-1][0] if sub else 2, sub)
        for a in range(p):
            assert not verify_pratt(p, [*sub, (p, a, f)]), (p, a)


def test_carmichael_and_strong_pseudoprimes() -> None:
    rng = random.Random(2)
    for n in CARMICHAEL + STRONG_PSP:
        assert build_pratt(n, rng) is None, n
        f = factorize(n - 1, rng)
        sub = subcertificate(f, rng)
        for a in (2, 3, 5, 7, n - 1):
            assert not verify_pratt(n, [*sub, (n, a, f)])


def test_tampered_certificates_fail() -> None:
    rng = random.Random(3)
    n = 1279
    good = build_pratt(n)
    assert not verify_pratt(n, good[:-1])  # missing root
    assert not verify_pratt(n, good[1:])  # missing child 3
    assert not verify_pratt(n, [good[-1], *good[:-1]])  # child after parent
    assert not verify_pratt(n, [*good[:-1], (1279, 2, good[-1][2])])  # 2 is not a primitive root
    assert not verify_pratt(n, [*good[:-1], (1279, 3, {2: 1, 639: 1})])  # 639 not proven
    assert not verify_pratt(n, [*good[:-1], (1279, 3, {2: 1, 3: 1, 71: 1})])  # wrong product
    assert not verify_pratt(n, [*good[:-1], (1279, 3, {2: 1, 3: 2, 71: 1, 5: 0})])  # zero exponent
    assert not verify_pratt(1281, [*good[:-1], (1281, 3, {2: 5, 5: 1, 8: 1})])
    # A certificate for one prime does not certify another.
    assert not verify_pratt(1283, good)
    for _ in range(200):
        bad = [list(e) for e in good]
        i = rng.randrange(len(bad))
        bad[i][1] = rng.randrange(2, bad[i][0])
        bad_cert = [(p, a, f) for p, a, f in bad]
        ok = all(
            pow(a, (p - 1) // 2, p) == p - 1 and all(pow(a, (p - 1) // (2 * q), p) != p - 1 for q in f if q != 2)
            for p, a, f in bad_cert
        )
        assert verify_pratt(n, bad_cert) == ok


def test_large_primes() -> None:
    rng = random.Random(4)
    for k in (61, 89, 107, 127):
        n = 2**k - 1
        cert = build_pratt(n, rng)
        assert cert is not None and verify_pratt(n, cert) and verify_cost(cert) < 2 * k * k
    n = 3 * 2**534 + 1  # 162 digits
    cert = build_pratt(n, rng)
    assert cert is not None and verify_pratt(n, cert) and cert[-1][0] == n
    # Primes 2 * (product of primes below 10^4) + 1 with several hundred digits.
    small = [p for p in range(3, 10_000) if is_prime_td(p)]
    found = 0
    while found < 3:
        m = 2
        while m.bit_length() < 900:
            m *= rng.choice(small)
        n = m + 1
        cert = build_pratt(n, rng)
        assert (cert is not None) == probably_prime(n)
        if cert is not None:
            assert verify_pratt(n, cert) and verify_cost(cert) < 2 * math.log2(n) ** 2
            found += 1


def test_large_composites_rejected() -> None:
    rng = random.Random(5)
    m521, m607 = 2**521 - 1, 2**607 - 1
    assert build_pratt(m521 * m607, rng) is None
    assert build_pratt(m521**2, rng) is None
    assert build_pratt(2**512 + 1, rng) is None


def test_random_inputs_against_trial_division() -> None:
    rng = random.Random(6)
    for _ in range(300):
        n = rng.randrange(10**9, 10**12)
        assert (build_pratt(n, rng) is not None) == is_prime_td(n)
