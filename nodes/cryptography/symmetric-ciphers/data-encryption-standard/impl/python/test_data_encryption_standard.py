# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/data-encryption-standard/. The authors are listed in prov/AFV5EE.jsonl.

import random

from data_encryption_standard import SBOXES, decrypt_block, encrypt_block, key_schedule, set_parity

M64 = (1 << 64) - 1

# NIST SP 800-17 (1998), Appendix B, Table 1: variable plaintext known answer test, key 0101010101010101.
TABLE1 = [
    (0x8000000000000000, 0x95F8A5E5DD31D900),
    (0x4000000000000000, 0xDD7F121CA5015619),
    (0x0400000000000000, 0x55579380D77138EF),
    (0x0040000000000000, 0x424250B37C3DD951),
]

# NIST SP 800-17 (1998), Appendix B, Table 2: variable key known answer test, plaintext 0.
TABLE2 = [
    (0x8001010101010101, 0x95A8D72813DAA94D),
    (0x4001010101010101, 0x0EEC1487DD8C26D5),
    (0x2001010101010101, 0x7AD16FFB79C45926),
    (0x0140010101010101, 0xDF3B99D6577397C8),
    (0x0120010101010101, 0x31FE17369B5288C9),
]

# NIST SP 800-17 (1998), Appendix B, Table 4: substitution table known answer test (key, plaintext, ciphertext).
TABLE4 = [
    (0x0131D9619DC1376E, 0x5CD54CA83DEF57DA, 0x7A389D10354BD271),
    (0x07A1133E4A0B2686, 0x0248D43806F67172, 0x868EBB51CAB4599A),
    (0x04B915BA43FEB5B6, 0x42FD443059577FA2, 0xAF37FB421F8C4095),
    (0x43297FAD38E373FE, 0x762514B829BF486A, 0xEA676B2CB7DB2B7A),
    (0x584023641ABA6176, 0x004BD6EF09176062, 0x88BF0DB6D70DEE56),
]

# NIST SP 800-67 Rev. 2 (2017), Section 3.3.2: the 4 weak keys and the 6 pairs of semi-weak keys.
WEAK = [0x0101010101010101, 0xFEFEFEFEFEFEFEFE, 0xE0E0E0E0F1F1F1F1, 0x1F1F1F1F0E0E0E0E]
SEMI_WEAK = [
    (0x011F011F010E010E, 0x1F011F010E010E01),
    (0x01E001E001F101F1, 0xE001E001F101F101),
    (0x01FE01FE01FE01FE, 0xFE01FE01FE01FE01),
    (0x1FE01FE00EF10EF1, 0xE01FE01FF10EF10E),
    (0x1FFE1FFE0EFE0EFE, 0xFE1FFE1FFE0EFE0E),
    (0xE0FEE0FEF1FEF1FE, 0xFEE0FEE0FEF1FEF1),
]


def test_sp800_17_table1() -> None:
    for pt, ct in TABLE1:
        assert encrypt_block(0x0101010101010101, pt) == ct
        assert decrypt_block(0x0101010101010101, ct) == pt


def test_sp800_17_table2() -> None:
    for key, ct in TABLE2:
        assert encrypt_block(key, 0) == ct
        assert decrypt_block(key, ct) == 0


def test_sp800_17_table4() -> None:
    for key, pt, ct in TABLE4:
        assert encrypt_block(key, pt) == ct
        assert decrypt_block(key, ct) == pt


# NIST SP 800-67 Rev. 1 (2012), Appendix B.1: the first DES step of the TDEA example.
def test_sp800_67_first_step() -> None:
    assert encrypt_block(0x0123456789ABCDEF, 0x5468652071756663) == 0xA28E91724C4BBA31


def test_sboxes_rows_are_permutations() -> None:
    for s in SBOXES:
        for row in range(4):
            assert sorted(s[16 * row:16 * row + 16]) == list(range(16))


def test_complementation_property() -> None:
    rng = random.Random(46)
    for _ in range(50):
        k, x = rng.getrandbits(64), rng.getrandbits(64)
        assert encrypt_block(k ^ M64, x ^ M64) == encrypt_block(k, x) ^ M64


def test_weak_keys() -> None:
    rng = random.Random(3)
    for k in WEAK:
        assert len(set(key_schedule(k))) == 1
        for _ in range(5):
            x = rng.getrandbits(64)
            assert encrypt_block(k, encrypt_block(k, x)) == x


def test_semi_weak_keys() -> None:
    rng = random.Random(5)
    for k1, k2 in SEMI_WEAK:
        assert key_schedule(k1) == key_schedule(k2)[::-1]
        for _ in range(5):
            x = rng.getrandbits(64)
            assert encrypt_block(k2, encrypt_block(k1, x)) == x


def test_parity_bits_are_ignored() -> None:
    rng = random.Random(8)
    for _ in range(20):
        k, x = rng.getrandbits(64), rng.getrandbits(64)
        assert encrypt_block(k, x) == encrypt_block(set_parity(k), x)


def test_round_trip() -> None:
    rng = random.Random(1977)
    for _ in range(200):
        k, x = rng.getrandbits(64), rng.getrandbits(64)
        assert decrypt_block(k, encrypt_block(k, x)) == x
