# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-cryptosystem/. The authors are listed in prov/3WNX9E.jsonl.

import math
import random

import pytest
from rabin_cryptosystem import (
    DecryptionError,
    RabinKey,
    RootOracle,
    chosen_ciphertext_attack,
    decode,
    decrypt,
    encode,
    encrypt,
    factor_with_root_oracle,
    is_probable_prime,
    max_message_length,
    random_blum_prime,
    square_roots,
)

# A toy key: two primes of 256 binary digits, both 3 modulo 4. No real key
# is this small; 2048 binary digits or more is the standard size.
P = 105908492941222169474449981002310379398085384265116641546952413843437928473451
Q = 95620244125405084075196090488760440489158181254653715904431741281660987667043
KEY = RabinKey(p=P, q=Q)


def test_the_toy_key_is_a_blum_integer() -> None:
    assert is_probable_prime(P) and is_probable_prime(Q)
    assert P % 4 == 3 and Q % 4 == 3
    assert KEY.n == P * Q and KEY.n.bit_length() == 512
    assert max_message_length(KEY.n) >= 60


def test_key_generation_gives_blum_primes() -> None:
    rnd = random.Random(20251111)
    key = RabinKey.generate(256, rnd)
    assert key.p % 4 == 3 and key.q % 4 == 3
    assert is_probable_prime(key.p) and is_probable_prime(key.q)
    assert key.p.bit_length() == key.q.bit_length() == 128
    assert decrypt(key, encrypt(key.n, b"generated key")) == b"generated key"


def test_encode_and_decode_round_trip() -> None:
    assert decode(encode(b"")) == b""
    for length in range(0, 40):
        message = bytes(range(length))
        assert decode(encode(message)) == message
    assert decode(encode(b"abc") + 1) is None  # a changed integer loses the tag
    assert decode(0) is None


def test_encryption_and_decryption_round_trip() -> None:
    rnd = random.Random(5)
    for _ in range(25):
        message = bytes(rnd.randrange(256) for _ in range(rnd.randrange(0, 50)))
        ciphertext = encrypt(KEY.n, message)
        assert decrypt(KEY, ciphertext) == message


def test_a_ciphertext_has_four_roots_and_only_one_decodes() -> None:
    """The ambiguity of squaring, and the redundancy that resolves it."""
    ciphertext = encrypt(KEY.n, b"four roots, one message")
    roots = square_roots(KEY, ciphertext)
    assert len(roots) == 4
    assert all(root * root % KEY.n == ciphertext for root in roots)
    # The roots come in pairs that add up to N, and the two pairs differ.
    assert roots[0] + roots[3] == KEY.n and roots[1] + roots[2] == KEY.n
    assert sum(1 for root in roots if decode(root) is not None) == 1
    assert decrypt(KEY, ciphertext) == b"four roots, one message"


def test_a_value_that_is_not_a_square_fails() -> None:
    ciphertext = encrypt(KEY.n, b"hello")
    with pytest.raises(DecryptionError):
        decrypt(KEY, (ciphertext + 1) % KEY.n)  # almost surely not a residue


def test_a_decryption_oracle_factors_the_modulus() -> None:
    """The proof of Rabin's theorem, run as a program."""
    rnd = random.Random(1979)
    oracle = RootOracle(key=KEY, rnd=rnd)
    found = factor_with_root_oracle(KEY.n, oracle, rnd)
    assert found is not None
    assert set(found) == {P, Q}
    assert oracle.queries <= 20  # two on average


def test_each_query_succeeds_with_probability_one_half() -> None:
    """One query, one coin flip: the oracle answers +-x half of the time."""
    rnd = random.Random(2)
    oracle = RootOracle(key=KEY, rnd=rnd)
    wins = 0
    trials = 60
    for _ in range(trials):
        x = rnd.randrange(2, KEY.n - 1)
        y = oracle(x * x % KEY.n)
        if y not in (x, KEY.n - x) and 1 < math.gcd(x - y, KEY.n) < KEY.n:
            wins += 1
    assert 0.3 * trials < wins < 0.7 * trials


def test_the_same_proof_is_a_chosen_ciphertext_attack() -> None:
    """The attacker never sends the target, and still reads it."""
    secret = b"the oracle never saw this ciphertext"
    target = encrypt(KEY.n, secret)
    rnd = random.Random(80)
    oracle = RootOracle(key=KEY, rnd=rnd)
    recovered, factors = chosen_ciphertext_attack(KEY.n, oracle, rnd, target)
    assert recovered == secret
    assert set(factors) == {P, Q}


def test_a_blum_prime_generator_keeps_its_promise() -> None:
    rnd = random.Random(3)
    for bits in (64, 96):
        prime = random_blum_prime(bits, rnd)
        assert prime.bit_length() == bits and prime % 4 == 3
        assert is_probable_prime(prime)
