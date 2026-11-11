# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sha-2/. The authors are listed in prov/CGBNHK.jsonl.

import hashlib

from sha_2 import (
    IV224,
    IV256,
    IV384,
    IV512,
    IV512_224,
    IV512_256,
    K32,
    K64,
    compress,
    pad,
    sha224,
    sha256,
    sha384,
    sha512,
    sha512_224,
    sha512_256,
)

ABC = b"abc"
M448 = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
M896 = (
    b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmno"
    b"ijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu"
)

# NIST, Cryptographic Standards and Guidelines, Example Values: SHA224.pdf, SHA256.pdf,
# SHA384.pdf, SHA512.pdf, SHA512_224.pdf and SHA512_256.pdf, the one-block and the
# multi-block examples, copied by hand.
NIST = [
    (sha224, ABC, "23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7"),
    (sha224, M448, "75388b16512776cc5dba5da1fd890150b0c6455cb4f58b1952522525"),
    (sha256, ABC, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    (sha256, M448, "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    (sha384, ABC, "cb00753f45a35e8bb5a03d699ac65007272c32ab0eded163"
                  "1a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7"),
    (sha384, M896, "09330c33f71147e83d192fc782cd1b4753111b173b3b05d2"
                   "2fa08086e3b0f712fcc7c71a557e2db966c3e9fa91746039"),
    (sha512, ABC, "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a"
                  "2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f"),
    (sha512, M896, "8e959b75dae313da8cf4f72814fc143f8f7779c6eb9f7fa17299aeadb6889018"
                   "501d289e4900f7e4331b99dec4b5433ac7d329eeb6dd26545e96e55b874be909"),
    (sha512_224, ABC, "4634270f707b6a54daae7530460842e20e37ed265ceee9a43e8924aa"),
    (sha512_224, M896, "23fec5bb94d60b23308192640b0c453335d664734fe40e7268674af9"),
    (sha512_256, ABC, "53048e2681941ef99b2e29b76b4c7dabe4c2d0c634fc6d46e0e2f13107e7af23"),
    (sha512_256, M896, "3928e184fb8690f840da3988121d31be65cb9d3ef83ee6146feac861e19b563a"),
]


def test_nist_examples() -> None:
    assert len(M448) * 8 == 448 and len(M896) * 8 == 896
    for fn, msg, want in NIST:
        assert fn(msg).hex() == want, (fn.__name__, msg)


# NIST Example Values, SHA256.pdf: the registers A..H for "abc" after t = 0 and t = 1.
def test_nist_sha256_trace() -> None:
    trace: list = []
    compress(list(IV256), pad(ABC, 32), 32, trace)
    assert trace[0] == (0x5D6AEBCD, 0x6A09E667, 0xBB67AE85, 0x3C6EF372,
                        0xFA2A4622, 0x510E527F, 0x9B05688C, 0x1F83D9AB)
    assert trace[1][0] == 0x5A6AD9AD and trace[1][4] == 0x78CE7989


def test_derived_constants() -> None:
    # The first and last constants, and the first word of each IV, as printed in FIPS 180-4.
    assert len(K32) == 64 and len(K64) == 80
    assert K32[0] == 0x428A2F98 and K32[63] == 0xC67178F2
    assert K64[0] == 0x428A2F98D728AE22 and K64[79] == 0x6C44198C4A475817
    assert all(K64[i] >> 32 == K32[i] for i in range(64))
    assert IV256[0] == 0x6A09E667 and IV224[0] == 0xC1059ED8
    assert IV512[0] == 0x6A09E667F3BCC908 and IV384[0] == 0xCBBB9D5DC1059ED8
    assert IV512_224[0] == 0x8C3D37C819544DA2
    assert IV512_256[0] == 0x22312194FC2BF72C


def test_against_hashlib() -> None:
    pairs = [(sha224, "sha224"), (sha256, "sha256"), (sha384, "sha384"), (sha512, "sha512")]
    for n in (0, 1, 55, 56, 63, 64, 111, 112, 127, 128, 200):
        msg = bytes((3 * i + 1) & 255 for i in range(n))
        for fn, name in pairs:
            assert fn(msg) == hashlib.new(name, msg).digest(), (name, n)


def test_truncation_hides_state() -> None:
    # SHA-224 and SHA-512/256 output only part of the final chaining value, unlike SHA-256.
    assert len(sha224(ABC)) == 28 and len(sha512_256(ABC)) == 32
    assert sha512_256(ABC) != sha512(ABC)[:32]
