# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serpent/. The authors are listed in prov/9ATZRG.jsonl.

import random

import pytest

from serpent import SBOX, decrypt_block, encrypt_block, lt, lt_inv

# NESSIE test vectors for Serpent, files Serpent-128-128, Serpent-192-128 and
# Serpent-256-128 ".verified.test-vectors". Hex strings are byte strings.
NESSIE = [
    # (file, set and vector, key, plain, cipher)
    ("128 set 1 #0", "80000000000000000000000000000000",
     "00000000000000000000000000000000", "264E5481EFF42A4606ABDA06C0BFDA3D"),
    ("128 set 1 #1", "40000000000000000000000000000000",
     "00000000000000000000000000000000", "4A231B3BC727993407AC6EC8350E8524"),
    ("128 set 2 #0", "00000000000000000000000000000000",
     "80000000000000000000000000000000", "A3B35DE7C358DDD82644678C64B8BCBB"),
    ("128 set 3 #0", "00000000000000000000000000000000",
     "00000000000000000000000000000000", "3620B17AE6A993D09618B8768266BAE9"),
    ("128 set 4 #0", "000102030405060708090A0B0C0D0E0F",
     "00112233445566778899AABBCCDDEEFF", "563E2CF8740A27C164804560391E9B27"),
    ("128 set 4 #1", "2BD6459F82C5B300952C49104881FF48",
     "EA024714AD5C4D84EA024714AD5C4D84", "92D7F8EF2C36C53409F275902F06539F"),
    ("192 set 4 #0", "000102030405060708090A0B0C0D0E0F1011121314151617",
     "00112233445566778899AABBCCDDEEFF", "6AB816C82DE53B93005008AFA2246A02"),
    ("256 set 1 #0", "8000000000000000000000000000000000000000000000000000000000000000",
     "00000000000000000000000000000000", "A223AA1288463C0E2BE38EBD825616C0"),
    ("256 set 2 #0", "0000000000000000000000000000000000000000000000000000000000000000",
     "80000000000000000000000000000000", "8314675E8AD5C3ECD83D852BCF7F566E"),
    ("256 set 3 #0", "0000000000000000000000000000000000000000000000000000000000000000",
     "00000000000000000000000000000000", "49672BA898D98DF95019180445491089"),
    ("256 set 4 #0", "000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F",
     "00112233445566778899AABBCCDDEEFF", "2868B7A2D28ECD5E4FDEFAC3C4330074"),
]


@pytest.mark.parametrize("name,key,pt,ct", NESSIE)
def test_nessie(name: str, key: str, pt: str, ct: str) -> None:
    k = bytes.fromhex(key)
    assert encrypt_block(k, bytes.fromhex(pt)).hex().upper() == ct, name
    assert decrypt_block(k, bytes.fromhex(ct)).hex().upper() == pt, name


def test_nessie_iterated_100_times() -> None:
    # Serpent-128-128, set 4, vector 0: "Iterated 100 times".
    key = bytes.fromhex("000102030405060708090A0B0C0D0E0F")
    x = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
    for _ in range(100):
        x = encrypt_block(key, x)
    assert x.hex().upper() == "70795D35DEC6561F8AD83B2F454F9CC5"


def test_sboxes_are_permutations() -> None:
    for box in SBOX:
        assert sorted(box) == list(range(16))


def test_linear_transform_inverse() -> None:
    rng = random.Random(14)
    for _ in range(50):
        x = [rng.getrandbits(32) for _ in range(4)]
        assert lt_inv(lt(x)) == x


def test_round_trip_random() -> None:
    rng = random.Random(15)
    for n in (5, 16, 24, 32):
        key = rng.randbytes(n)
        m = rng.randbytes(16)
        assert decrypt_block(key, encrypt_block(key, m)) == m
