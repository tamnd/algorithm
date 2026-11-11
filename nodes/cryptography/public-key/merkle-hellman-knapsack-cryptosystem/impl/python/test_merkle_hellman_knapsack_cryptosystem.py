# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-hellman-knapsack-cryptosystem/. The authors are listed in prov/FC4WWX.jsonl.

import random

import pytest
from lll import lll_reduce
from merkle_hellman_knapsack_cryptosystem import (
    DecryptionError,
    MerkleHellmanKey,
    decrypt,
    density,
    encrypt,
    is_superincreasing,
    low_density_attack,
    solve_superincreasing,
    superincreasing_sequence,
)

# The textbook key: the private sequence, the modulus and the multiplier of the
# small example on the page. No real key is this small, and no key of this
# scheme is safe at any size.
SMALL_SEQUENCE = [2, 3, 6, 13, 27, 52]
SMALL_KEY = MerkleHellmanKey(
    sequence=SMALL_SEQUENCE, modulus=105, multiplier=31, permutation=list(range(6))
)


def test_the_small_key_matches_the_page() -> None:
    assert SMALL_KEY.public_key == [62, 93, 81, 88, 102, 37]
    assert SMALL_KEY.inverse == 61  # 31 * 61 = 1891 = 18 * 105 + 1
    bits = [0, 1, 1, 0, 0, 1]
    ciphertext = encrypt(SMALL_KEY.public_key, bits)
    assert ciphertext == 93 + 81 + 37 == 211
    assert SMALL_KEY.inverse * ciphertext % SMALL_KEY.modulus == 61
    assert solve_superincreasing(SMALL_SEQUENCE, 61) == bits  # 52 + 6 + 3
    assert decrypt(SMALL_KEY, ciphertext) == bits


def test_generated_sequences_are_superincreasing() -> None:
    rnd = random.Random(1978)
    for n in (4, 8, 16):
        sequence = superincreasing_sequence(n, rnd)
        assert len(sequence) == n
        assert is_superincreasing(sequence)
    assert not is_superincreasing([1, 2, 2])
    assert not is_superincreasing([5, 4])


def test_the_greedy_pass_is_exact() -> None:
    """A superincreasing sequence has at most one subset for each sum."""
    rnd = random.Random(5)
    sequence = superincreasing_sequence(10, rnd)
    for _ in range(40):
        bits = [rnd.randrange(2) for _ in range(10)]
        target = sum(bit * term for bit, term in zip(bits, sequence))
        assert solve_superincreasing(sequence, target) == bits
    assert solve_superincreasing(SMALL_SEQUENCE, 1) is None
    assert solve_superincreasing(SMALL_SEQUENCE, sum(SMALL_SEQUENCE) + 1) is None


def test_encryption_and_decryption_round_trip() -> None:
    rnd = random.Random(20251111)
    key = MerkleHellmanKey.generate(16, rnd)
    for _ in range(20):
        bits = [rnd.randrange(2) for _ in range(16)]
        assert decrypt(key, encrypt(key.public_key, bits)) == bits


def test_the_permutation_is_undone() -> None:
    rnd = random.Random(11)
    key = MerkleHellmanKey.generate(12, rnd)
    assert key.permutation != list(range(12))  # the seed gives a real shuffle
    for position in range(12):
        bits = [1 if index == position else 0 for index in range(12)]
        assert decrypt(key, encrypt(key.public_key, bits)) == bits


def test_the_density_is_near_one_half() -> None:
    """The shape Merkle and Hellman proposed is exactly the shape lattices break."""
    rnd = random.Random(3)
    key = MerkleHellmanKey.generate(24, rnd)
    assert 0.45 < density(key.public_key) < 0.55
    assert max(key.public_key).bit_length() >= 2 * 24 - 4


def test_a_value_that_is_not_a_ciphertext_fails() -> None:
    # 2 * 61 mod 105 = 17, and no subset of the sequence sums to 17.
    assert solve_superincreasing(SMALL_SEQUENCE, 17) is None
    with pytest.raises(DecryptionError):
        decrypt(SMALL_KEY, 2)


def test_bad_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):  # not superincreasing
        MerkleHellmanKey(sequence=[2, 2], modulus=11, multiplier=3, permutation=[0, 1])
    with pytest.raises(ValueError):  # the modulus is too small
        MerkleHellmanKey(sequence=[2, 3], modulus=5, multiplier=3, permutation=[0, 1])
    with pytest.raises(ValueError):  # the multiplier is not a unit
        MerkleHellmanKey(sequence=[2, 3], modulus=10, multiplier=4, permutation=[0, 1])
    with pytest.raises(ValueError):  # not a permutation
        MerkleHellmanKey(sequence=[2, 3], modulus=11, multiplier=3, permutation=[0, 0])
    with pytest.raises(ValueError):
        encrypt([1, 2, 3], [1, 0])
    with pytest.raises(ValueError):
        encrypt([1, 2], [1, 2])


def test_the_lattice_attack_reads_the_message_from_the_public_key_alone() -> None:
    """The break: no trapdoor, no factoring, just one basis reduction."""
    for seed in (1, 2, 3):
        rnd = random.Random(seed)
        key = MerkleHellmanKey.generate(20, rnd)
        bits = [rnd.randrange(2) for _ in range(20)]
        ciphertext = encrypt(key.public_key, bits)
        # The attack sees the public key and the ciphertext. Nothing else.
        assert low_density_attack(key.public_key, ciphertext) == bits


def test_the_lattice_attack_on_the_small_key() -> None:
    ciphertext = encrypt(SMALL_KEY.public_key, [0, 1, 1, 0, 0, 1])
    assert low_density_attack(SMALL_KEY.public_key, ciphertext) == [0, 1, 1, 0, 0, 1]


def test_the_copied_lll_reduces_a_known_basis() -> None:
    reduced = lll_reduce([[1, 1, 1], [-1, 0, 2], [3, 5, 6]])
    assert reduced == [[0, 1, 0], [1, 0, 1], [-2, 0, 1]]
