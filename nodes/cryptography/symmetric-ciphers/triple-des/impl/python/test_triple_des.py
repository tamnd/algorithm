# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triple-des/. The authors are listed in prov/1FR1YR.jsonl.

import random

from triple_des import des_decrypt, des_encrypt, tdea_decrypt, tdea_encrypt

# NIST SP 800-67 Rev. 1 (January 2012), Appendix B.1: TDEA ECB example with three distinct keys.
K1, K2, K3 = 0x0123456789ABCDEF, 0x23456789ABCDEF01, 0x456789ABCDEF0123
# (P, F_K1(P), I_K2(F_K1(P)), C) for each of the three blocks.
B1 = [
    (0x5468652071756663, 0xA28E91724C4BBA31, 0x5A2EA7F983A2F53F, 0xA826FD8CE53B855F),
    (0x6B2062726F776E20, 0x167E47EC24F71D63, 0xEA141A7DD69701F0, 0xCCE21C8112256FE6),
    (0x666F78206A756D70, 0x2C1A917234425365, 0x8059EE8212E22A79, 0x68D5C05DD9B6B900),
]

# NIST SP 800-17 (1998), Appendix B, Table 4, row 1: a single DES vector (key, plaintext, ciphertext).
DES_VECTOR = (0x0131D9619DC1376E, 0x5CD54CA83DEF57DA, 0x7A389D10354BD271)


def test_sp800_67_appendix_b1() -> None:
    for p, a, b, c in B1:
        assert des_encrypt(K1, p) == a
        assert des_decrypt(K2, a) == b
        assert tdea_encrypt(K1, K2, K3, p) == c
        assert tdea_decrypt(K1, K2, K3, c) == p


def test_des_vector() -> None:
    k, p, c = DES_VECTOR
    assert des_encrypt(k, p) == c


def test_one_key_bundle_is_single_des() -> None:
    # With K1 = K2 = K3 the first two steps cancel, so EDE is one DES encryption.
    rng = random.Random(3)
    for _ in range(10):
        k, x = rng.getrandbits(64), rng.getrandbits(64)
        assert tdea_encrypt(k, k, k, x) == des_encrypt(k, x)


def test_round_trip_keying_options() -> None:
    rng = random.Random(67)
    for _ in range(30):
        k1, k2, k3, x = (rng.getrandbits(64) for _ in range(4))
        assert tdea_decrypt(k1, k2, k3, tdea_encrypt(k1, k2, k3, x)) == x
        assert tdea_decrypt(k1, k2, k1, tdea_encrypt(k1, k2, k1, x)) == x


# A toy cipher for the meet-in-the-middle attack: 16-bit block, 12-bit key, 4 rounds. Not secure.
TOY_S = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
TOY_SI = [TOY_S.index(v) for v in range(16)]
M16 = 0xFFFF


def _rotl(x: int, r: int) -> int:
    return ((x << r) | (x >> (16 - r))) & M16


def _toy_keys(key: int) -> list[int]:
    k16 = key | ((key & 0xF) << 12)
    return [_rotl(k16, 4 * i) for i in range(5)]


def _nibbles(x: int, box: list[int]) -> int:
    return sum(box[(x >> s) & 0xF] << s for s in (0, 4, 8, 12))


def toy_encrypt(key: int, x: int) -> int:
    ks = _toy_keys(key)
    for i in range(4):
        x = _rotl(_nibbles(x ^ ks[i], TOY_S), 5)
    return x ^ ks[4]


def toy_decrypt(key: int, y: int) -> int:
    ks = _toy_keys(key)
    y ^= ks[4]
    for i in range(3, -1, -1):
        y = _nibbles(_rotl(y, 11), TOY_SI) ^ ks[i]
    return y


def mitm(pairs: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], int]:
    """Recover (k1, k2) of y = E_k2(E_k1(x)) with 2 * 2^12 toy calls and a table of 2^12 entries."""
    calls = 0
    x0, y0 = pairs[0]
    table: dict[int, list[int]] = {}
    for k1 in range(1 << 12):
        table.setdefault(toy_encrypt(k1, x0), []).append(k1)
        calls += 1
    found = []
    for k2 in range(1 << 12):
        mid = toy_decrypt(k2, y0)
        calls += 1
        for k1 in table.get(mid, []):
            if all(toy_encrypt(k2, toy_encrypt(k1, x)) == y for x, y in pairs[1:]):
                found.append((k1, k2))
    return found, calls


def test_toy_cipher_round_trip() -> None:
    rng = random.Random(12)
    for _ in range(200):
        k, x = rng.randrange(1 << 12), rng.randrange(1 << 16)
        assert toy_decrypt(k, toy_encrypt(k, x)) == x


def test_meet_in_the_middle_recovers_both_keys() -> None:
    rng = random.Random(1977)
    for _ in range(2):
        k1, k2 = rng.randrange(1 << 12), rng.randrange(1 << 12)
        xs = rng.sample(range(1 << 16), 3)
        pairs = [(x, toy_encrypt(k2, toy_encrypt(k1, x))) for x in xs]
        found, calls = mitm(pairs)
        assert found == [(k1, k2)]
        assert calls == 2 * (1 << 12)
