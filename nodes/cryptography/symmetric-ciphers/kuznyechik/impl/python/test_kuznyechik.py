# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kuznyechik/. The authors are listed in prov/0Z0TM1.jsonl.

import random

from kuznyechik import C, PI, PI_INV, decrypt_block, encrypt_block, key_schedule, l_layer, r_step, s_layer


def h(s: str) -> list[int]:
    return list(bytes.fromhex(s))


# RFC 7801 Section 5.1, transformation S.
def test_rfc7801_s() -> None:
    assert s_layer(h("ffeeddccbbaa99881122334455667700")) == h("b66cd8887d38e8d77765aeea0c9a7efc")
    assert s_layer(h("0c3322fed531e4630d80ef5c5a81c50b")) == h("23ae65633f842d29c5df529c13f5acda")


# RFC 7801 Section 5.2, transformation R.
def test_rfc7801_r() -> None:
    assert r_step(h("00000000000000000000000000000100")) == h("94000000000000000000000000000001")
    assert r_step(h("64a59400000000000000000000000000")) == h("0d64a594000000000000000000000000")


# RFC 7801 Section 5.3, transformation L.
def test_rfc7801_l() -> None:
    assert l_layer(h("64a59400000000000000000000000000")) == h("d456584dd0e3e84cc3166e4b7fa2890d")
    assert l_layer(h("0e93691a0cfc60408b7b68f66b513c13")) == h("e6a8094fee0aa204fd97bcb0b44b8580")


KEY = bytes.fromhex("8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef")


# RFC 7801 Section 5.4, round constants C_1 and C_8 and the round keys.
def test_rfc7801_key_schedule() -> None:
    assert C[0] == h("6ea276726c487ab85d27bd10dd849401")
    assert C[7] == h("f6593616e6055689adfba18027aa2a08")
    ks = key_schedule(KEY)
    assert ks[2] == h("db31485315694343228d6aef8cc78c44")
    assert ks[3] == h("3d4553d8e9cfec6815ebadc40a9ffd04")
    assert ks[9] == h("72e9dd7416bcf45b755dbaa88e4a4043")


# RFC 7801 Sections 5.5 and 5.6, test encryption and decryption.
def test_rfc7801_encrypt_decrypt() -> None:
    pt = bytes.fromhex("1122334455667700ffeeddccbbaa9988")
    ct = bytes.fromhex("7f679d90bebc24305a468d42b9d4edcd")
    assert encrypt_block(KEY, pt) == ct
    assert decrypt_block(KEY, ct) == pt


def test_pi_is_permutation() -> None:
    assert sorted(PI) == list(range(256))
    # RFC 7801 Section 4.1 lists Pi^-1 starting with 165, 45, 50, 143.
    assert PI_INV[:4] == [165, 45, 50, 143]


def test_round_trip_random() -> None:
    rng = random.Random(5)
    for _ in range(6):
        key, m = rng.randbytes(32), rng.randbytes(16)
        assert decrypt_block(key, encrypt_block(key, m)) == m
