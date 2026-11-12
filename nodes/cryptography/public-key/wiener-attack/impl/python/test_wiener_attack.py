# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiener-attack/. The authors are listed in prov/TNJ165.jsonl.

import math
import random

from wiener_attack import (
    ToyWeakKey,
    continued_fraction,
    convergents,
    is_square,
    weak_key,
    wiener_attack,
    wiener_bound,
)

# Toy primes with q < p < 2q, the shape the theorem asks for.
P_256 = 273864138845241657029075268143536711069
Q_256 = 173710947069375085680776429514357002701
P_512 = 110449470566697461878973964718851827302191347553279945192450277528447536588917
Q_512 = 58988822039778636421579244604185529507126928801894249821805959749406623978057


def test_continued_fraction_and_convergents() -> None:
    """Two textbook expansions, and the recurrences that build the fractions."""
    assert continued_fraction(649, 200) == [3, 4, 12, 4]
    assert list(convergents([3, 4, 12, 4])) == [(3, 1), (13, 4), (159, 49), (649, 200)]
    assert continued_fraction(415, 93) == [4, 2, 6, 7]
    for h, k in convergents(continued_fraction(415, 93)):
        assert math.gcd(h, k) == 1
    assert list(convergents(continued_fraction(415, 93)))[-1] == (415, 93)


def test_is_square() -> None:
    assert all(is_square(i * i) for i in range(0, 200))
    assert not any(is_square(i * i + 1) for i in range(1, 200))
    assert not is_square(-4)


def test_the_small_worked_example() -> None:
    """p = 239, q = 379, d = 5. The attack takes the first convergent."""
    key = ToyWeakKey(p=239, q=379, d=5)
    assert key.n == 90581 and key.e == 17993
    assert 379 < 2 * 239  # the ratio hypothesis holds
    # Here d = 5 is N^(1/4)/3 = 5.78 rounded down, so d < N^(1/4)/3 holds.
    assert key.d == wiener_bound(key.n) and key.is_in_the_wiener_range()
    p, q, d = wiener_attack(*key.public)
    assert {p, q} == {239, 379} and d == 5


def test_a_toy_key_of_255_binary_digits() -> None:
    rnd = random.Random(20251111)
    key = weak_key(P_256, Q_256, rnd)
    assert key.is_in_the_wiener_range()
    assert key.d.bit_length() >= 60  # a small exponent, but not a tiny one
    p, q, d = wiener_attack(*key.public)
    assert {p, q} == {P_256, Q_256}
    assert d == key.d
    message = 0x6c6974746c65206420697320776f726b
    assert pow(pow(message, key.e, key.n), d, key.n) == message


def test_a_toy_key_of_512_binary_digits() -> None:
    rnd = random.Random(424242)
    key = weak_key(P_512, Q_512, rnd)
    assert key.n.bit_length() == 511
    assert key.is_in_the_wiener_range()
    assert key.d.bit_length() >= 124
    assert wiener_attack(*key.public) == (max(P_512, Q_512), min(P_512, Q_512), key.d)


def test_many_weak_keys_in_a_row() -> None:
    rnd = random.Random(7)
    for _ in range(10):
        key = weak_key(P_256, Q_256, rnd)
        found = wiener_attack(*key.public)
        assert found is not None and found[2] == key.d


def test_a_normal_key_resists() -> None:
    """With e = 65537 the private exponent is full size, and nothing is found."""
    n = P_256 * Q_256
    phi = (P_256 - 1) * (Q_256 - 1)
    e = 65537
    d = pow(e, -1, phi)
    assert d > wiener_bound(n)
    assert wiener_attack(n, e) is None


def test_the_bound_is_the_fourth_root_over_three() -> None:
    n = P_512 * Q_512
    bound = wiener_bound(n)
    assert (3 * bound) ** 4 <= n
    assert (3 * (bound + 1)) ** 4 > n or (bound + 1) ** 4 * 81 > n
