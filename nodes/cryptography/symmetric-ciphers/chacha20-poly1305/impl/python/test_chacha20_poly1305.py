# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chacha20-poly1305/. The authors are listed in prov/5G1J5X.jsonl.

import random

from chacha20_poly1305 import (
    FAIL,
    P1305,
    aead_decrypt,
    aead_encrypt,
    chacha20_block,
    chacha20_encrypt,
    hchacha20,
    mac_data,
    poly1305_key_gen,
    poly1305_mac,
    quarter_round,
    xchacha20_poly1305_decrypt,
    xchacha20_poly1305_encrypt,
)

KEY_8X = bytes(range(0x80, 0xA0))
LADIES = (
    b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, "
    b"sunscreen would be it."
)


def test_quarter_round_rfc8439_section_2_1_1() -> None:
    s = [0x11111111, 0x01020304, 0x9B8D6F43, 0x01234567]
    quarter_round(s, 0, 1, 2, 3)
    assert s == [0xEA2A92F4, 0xCB1CF8CE, 0x4581472E, 0x5881C4BB]


def test_chacha20_block_rfc8439_section_2_3_2() -> None:
    key = bytes(range(32))
    nonce = bytes.fromhex("000000090000004a00000000")
    assert chacha20_block(key, 1, nonce).hex() == (
        "10f1e7e4d13b5915500fdd1fa32071c4c7d1f4c733c068030422aa9ac3d46c4e"
        "d2826446079faa0914c2d705d98b02a2b5129cd1de164eb9cbd083e8a2503c4e"
    )


def test_chacha20_encrypt_rfc8439_section_2_4_2() -> None:
    # Section 2.4.2: the "sunscreen" plaintext, counter 1; first and last bytes of the ciphertext.
    key = bytes(range(32))
    nonce = bytes.fromhex("000000000000004a00000000")
    c = chacha20_encrypt(key, 1, nonce, LADIES)
    assert c[:16].hex() == "6e2e359a2568f98041ba0728dd0d6981"
    assert c[-2:].hex() == "874d"


def test_poly1305_key_gen_rfc8439_section_2_6_2() -> None:
    nonce = bytes.fromhex("000000000001020304050607")
    assert poly1305_key_gen(KEY_8X, nonce).hex() == (
        "8ad5a08b905f81cc815040274ab29471a833b637e3fd0da508dbb8e2fdd1a646"
    )


def test_poly1305_rfc8439_section_2_5_2() -> None:
    key = bytes.fromhex("85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b")
    assert poly1305_mac(key, b"Cryptographic Forum Research Group").hex() == "a8061dc1305136c6c22b8baf0c0127a9"


def test_aead_rfc8439_section_2_8_2() -> None:
    aad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
    nonce = bytes.fromhex("07000000") + b"@ABCDEFG"  # constant 07000000 || IV 4041424344454647
    assert poly1305_key_gen(KEY_8X, nonce).hex() == (
        "7bac2b252db447af09b67a55a4e955840ae1d6731075d9eb2a9375783ed553ff"
    )
    c, tag = aead_encrypt(KEY_8X, nonce, aad, LADIES)
    assert c.hex() == (
        "d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d6"
        "3dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b36"
        "92ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc"
        "3ff4def08e4b7a9de576d26586cec64b6116"
    )
    assert tag.hex() == "1ae10b594f09e26a7e902ecbd0600691"
    # The Poly1305 input: 4 zero bytes after the AAD, 14 after C, then 0c and 72 as 64-bit lengths.
    m = mac_data(aad, c)
    assert len(m) == 160 and m[12:16] == bytes(4) and m[130:144] == bytes(14)
    assert m[144:].hex() == "0c000000000000007200000000000000"
    assert aead_decrypt(KEY_8X, nonce, aad, c, tag) == LADIES


def test_aead_decryption_rfc8439_appendix_a5() -> None:
    key = bytes.fromhex("1c9240a5eb55d38af333888604f6b5f0473917c1402b80099dca5cbc207075c0")
    c = bytes.fromhex(
        "64a0861575861af460f062c79be643bd5e805cfd345cf389f108670ac76c8cb2"
        "4c6cfc18755d43eea09ee94e382d26b0bdb7b73c321b0100d4f03b7f355894cf"
        "332f830e710b97ce98c8a84abd0b948114ad176e008d33bd60f982b1ff37c855"
        "9797a06ef4f0ef61c186324e2b3506383606907b6a7c02b0f9f6157b53c867e4"
        "b9166c767b804d46a59b5216cde7a4e99040c5a40433225ee282a1b0a06c523e"
        "af4534d7f83fa1155b0047718cbc546a0d072b04b3564eea1b422273f548271a"
        "0bb2316053fa76991955ebd63159434ecebb4e466dae5a1073a6727627097a10"
        "49e617d91d361094fa68f0ff77987130305beaba2eda04df997b714d6c6f2c29"
        "a6ad5cb4022b02709b"
    )
    nonce = bytes.fromhex("000000000102030405060708")
    aad = bytes.fromhex("f33388860000000000004e91")
    tag = bytes.fromhex("eead9d67890cbb22392336fea1851f38")
    assert poly1305_key_gen(key, nonce).hex() == "bdf04aa95ce4de8995b14bb6a18fecaf26478f50c054f563dbc0a21e261572aa"
    expected = (
        "Internet-Drafts are draft documents valid for a maximum of six months and may be updated, "
        "replaced, or obsoleted by other documents at any time. It is inappropriate to use "
        "Internet-Drafts as reference material or to cite them other than as /“work in progress./”"
    ).encode()
    assert len(expected) == 265
    assert aead_decrypt(key, nonce, aad, c, tag) == expected


def test_hchacha20_draft_xchacha_section_2_2_1() -> None:
    nonce = bytes.fromhex("000000090000004a0000000031415927")
    assert hchacha20(bytes(range(32)), nonce).hex() == (
        "82413b4227b27bfed30e42508a877d73a0f9e4d58a74a853c12ec41326d3ecdc"
    )


def test_xchacha20_poly1305_draft_xchacha_appendix_a_3_1() -> None:
    nonce = bytes.fromhex("404142434445464748494a4b4c4d4e4f5051525354555657")
    aad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
    c, tag = xchacha20_poly1305_encrypt(KEY_8X, nonce, aad, LADIES)
    assert c.hex() == (
        "bd6d179d3e83d43b9576579493c0e939572a1700252bfaccbed2902c21396cbb"
        "731c7f1b0b4aa6440bf3a82f4eda7e39ae64c6708c54c216cb96b72e1213b452"
        "2f8c9ba40db5d945b11b69b982c1bb9e3f3fac2bc369488f76b2383565d3fff9"
        "21f9664c97637da9768812f615c68b13b52e"
    )
    assert tag.hex() == "c0875924c1c7987947deafd8780acf49"
    assert xchacha20_poly1305_decrypt(KEY_8X, nonce, aad, c, tag) == LADIES


def test_round_trips() -> None:
    rng = random.Random(8439)
    for length in (0, 1, 15, 16, 17, 63, 64, 65, 200):
        key, nonce = rng.randbytes(32), rng.randbytes(12)
        aad, p = rng.randbytes(rng.randrange(40)), rng.randbytes(length)
        c, tag = aead_encrypt(key, nonce, aad, p)
        assert len(c) == length
        assert aead_decrypt(key, nonce, aad, c, tag) == p


def test_one_changed_bit_is_rejected() -> None:
    rng = random.Random(1)
    key, nonce, aad, p = rng.randbytes(32), rng.randbytes(12), rng.randbytes(13), rng.randbytes(50)
    c, tag = aead_encrypt(key, nonce, aad, p)
    for name, value in (("c", c), ("tag", tag), ("aad", aad), ("nonce", nonce)):
        for bit in range(len(value) * 8):
            bad = bytearray(value)
            bad[bit // 8] ^= 1 << (bit % 8)
            args = {"c": c, "tag": tag, "aad": aad, "nonce": nonce, name: bytes(bad)}
            assert aead_decrypt(key, args["nonce"], args["aad"], args["c"], args["tag"]) == FAIL


def test_lengths_block_separates_aad_and_ciphertext() -> None:
    # Without the lengths, (A = X, C = empty) and (A = empty, C = X) would give the same MAC input.
    x = bytes(range(16))
    assert mac_data(x, b"")[:16] == mac_data(b"", x)[:16] == x  # the same first block
    assert mac_data(x, b"") != mac_data(b"", x)  # only the lengths block tells them apart
    assert mac_data(x, b"")[16:] != mac_data(b"", x)[16:]


def _sqrt_mod_p(a: int) -> list[int]:
    """Square roots modulo p = 2^130 - 5; p = 3 mod 4, so a root is a^((p+1)/4)."""
    root = pow(a, (P1305 + 1) // 4, P1305)
    return [root, P1305 - root] if root * root % P1305 == a else []


def test_nonce_reuse_recovers_the_poly1305_key_and_forges() -> None:
    """Two one-block messages under one nonce: t1 - t2 = (c1 - c2) r^2 mod p, up to the 2^128 wrap."""
    rng = random.Random(613)
    for _ in range(10):
        key, nonce = rng.randbytes(32), rng.randbytes(12)
        p1, p2 = rng.randbytes(16), rng.randbytes(16)  # the attacker knows p1
        c1, t1 = aead_encrypt(key, nonce, b"", p1)
        c2, t2 = aead_encrypt(key, nonce, b"", p2)
        n1, n2 = (int.from_bytes(c + b"\x01", "little") for c in (c1, c2))
        lb = int.from_bytes(mac_data(b"", c1)[16:] + b"\x01", "little")
        v1, v2 = int.from_bytes(t1, "little"), int.from_bytes(t2, "little")
        inv = pow(n1 - n2, -1, P1305)
        found = []
        for j in range(-4, 5):
            for r in _sqrt_mod_p((v1 - v2 + j * (1 << 128)) * inv % P1305):
                if r & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF != r:
                    continue
                s = (v1 - (n1 * r * r + lb * r) % P1305) % (1 << 128)
                if ((n2 * r * r + lb * r) % P1305 + s) % (1 << 128) == v2:
                    found.append(r.to_bytes(16, "little") + s.to_bytes(16, "little"))
        otk = poly1305_key_gen(key, nonce)
        r_true = int.from_bytes(otk[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF
        assert r_true.to_bytes(16, "little") + otk[16:] in found  # the clamped one-time key
        # With (r, s) and the key stream p1 xor c1, forge a new message and new AAD under that nonce.
        stream = bytes(x ^ y for x, y in zip(p1, c1))
        target = b"pay Eve 1000 EUR"
        c3 = bytes(x ^ y for x, y in zip(target, stream))
        aad3 = b"approved"
        tries = [poly1305_mac(otk, mac_data(aad3, c3)) for otk in found]
        assert any(aead_decrypt(key, nonce, aad3, c3, t) == target for t in tries)


def test_fresh_nonces_stop_the_key_recovery() -> None:
    rng = random.Random(614)
    key = rng.randbytes(32)
    n_a, n_b = rng.randbytes(12), rng.randbytes(12)
    assert poly1305_key_gen(key, n_a) != poly1305_key_gen(key, n_b)
    assert chacha20_block(key, 1, n_a) != chacha20_block(key, 1, n_b)


def test_not_key_committing_one_ciphertext_opens_under_two_keys() -> None:
    """Poly1305 is linear in the message, so one free block makes the tag fit two keys
    (the idea of the partitioning oracle attacks of Len, Grubbs and Ristenpart, 2021)."""
    rng = random.Random(2021)
    k1, k2, nonce = rng.randbytes(32), rng.randbytes(32), rng.randbytes(12)
    otks = [poly1305_key_gen(k, nonce) for k in (k1, k2)]
    r = [int.from_bytes(o[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF for o in otks]
    s = [int.from_bytes(o[16:], "little") for o in otks]
    delta = (s[1] - s[0]) % (1 << 128)
    lb = int.from_bytes((0).to_bytes(8, "little") + (32).to_bytes(8, "little") + b"\x01", "little")
    for _ in range(200):
        first = rng.randbytes(16)
        f = int.from_bytes(first + b"\x01", "little")
        a = [(f * ri**3 + lb * ri) % P1305 for ri in r]
        n = (delta - a[0] + a[1]) * pow(r[0] ** 2 - r[1] ** 2, -1, P1305) % P1305
        h2 = (a[1] + n * r[1] ** 2) % P1305
        if 1 << 128 <= n < 1 << 129 and h2 + delta < P1305:
            break
    else:
        raise AssertionError("no solution found")
    c = first + (n - (1 << 128)).to_bytes(16, "little")
    tag = poly1305_mac(otks[0], mac_data(b"", c))
    assert poly1305_mac(otks[1], mac_data(b"", c)) == tag
    m1, m2 = aead_decrypt(k1, nonce, b"", c, tag), aead_decrypt(k2, nonce, b"", c, tag)
    assert m1 != FAIL and m2 != FAIL and m1 != m2
