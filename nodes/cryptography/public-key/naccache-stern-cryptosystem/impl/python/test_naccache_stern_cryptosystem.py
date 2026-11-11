# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naccache-stern-cryptosystem/. The authors are listed in prov/B6YRKD.jsonl.
#
# There are no official test vectors for the Naccache-Stern cryptosystems. The tests check the
# worked examples of the page, round trips and the additive homomorphism on toy keys with
# fixed seeds. The keys are far too small to be secure.

import random

import pytest

import naccache_stern_cryptosystem as ns


def tiny():
    return ns.keygen_from([3, 5, 7, 11], 19, 13, random.Random(0))


def test_worked_example() -> None:
    pk, sk = tiny()
    assert pk == (1155, 1143713, 9)
    assert sk[0] == 1141140
    c = ns.encrypt(pk, 202, None, x=17)
    assert pow(9, 202, 1143713) == 697934
    assert pow(17, 1155, 1143713) == 170166
    assert c == 335411
    assert [pow(c, sk[0] // pi, 1143713) for pi in (3, 5, 7, 11)] == [713069, 963444, 1031227, 1015239]
    assert ns.decrypt(pk, sk, c) == 202
    assert ns.crt([1, 2, 6, 4], [3, 5, 7, 11]) == 202


def test_tiny_key_all_messages() -> None:
    pk, sk = tiny()
    rng = random.Random(1)
    for m in range(pk[0]):
        assert ns.decrypt(pk, sk, ns.encrypt(pk, m, rng)) == m


@pytest.fixture(scope="module")
def key():
    # 16 small primes (sigma has 70 binary digits), a and b of 160 binary digits, N of 391.
    return ns.keygen(16, 160, random.Random(1998))


def test_round_trip(key) -> None:
    pk, sk = key
    rng = random.Random(2)
    for m in [0, 1, pk[0] - 1] + [rng.randrange(pk[0]) for _ in range(10)]:
        assert ns.decrypt(pk, sk, ns.encrypt(pk, m, rng)) == m


def test_homomorphism(key) -> None:
    pk, sk = key
    rng = random.Random(3)
    sigma = pk[0]
    for _ in range(5):
        a, b, k = rng.randrange(sigma), rng.randrange(sigma), rng.randrange(sigma)
        ca, cb = ns.encrypt(pk, a, rng), ns.encrypt(pk, b, rng)
        assert ns.decrypt(pk, sk, ns.add(pk, ca, cb)) == (a + b) % sigma
        assert ns.decrypt(pk, sk, ns.mul_plain(pk, ca, k)) == a * k % sigma


def test_deterministic_variant(key) -> None:
    pk, sk = key
    c = ns.encrypt_deterministic(pk, 12345)
    assert c == ns.encrypt_deterministic(pk, 12345)  # equal messages are visible
    assert ns.decrypt(pk, sk, c) == 12345


def test_probabilistic(key) -> None:
    pk, _ = key
    rng = random.Random(4)
    assert ns.encrypt(pk, 9, rng) != ns.encrypt(pk, 9, rng)


def test_knapsack_1997_example() -> None:
    vs, sk = ns.knapsack_keygen(2003, 3, 4)
    assert vs == [268, 1326, 1282, 1152]
    assert [pow(v, 3, 2003) for v in vs] == [2, 3, 5, 7]
    c = ns.knapsack_encrypt(2003, vs, [1, 0, 1, 1])
    assert c == 743 and pow(c, 3, 2003) == 70
    assert ns.knapsack_decrypt(sk, c) == [1, 0, 1, 1]
    for word in range(16):
        bits = [(word >> i) & 1 for i in range(4)]
        assert ns.knapsack_decrypt(sk, ns.knapsack_encrypt(2003, vs, bits)) == bits
