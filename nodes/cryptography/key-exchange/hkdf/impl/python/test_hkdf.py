# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hkdf/. The authors are listed in prov/DCNWKP.jsonl.

import hashlib
import random

import pytest

from hkdf import derive_secret, hkdf, hkdf_expand, hkdf_expand_label, hkdf_extract


def H(s: str) -> bytes:
    return bytes.fromhex(s.replace(" ", ""))


# RFC 5869 Appendix A.1 to A.3 (SHA-256), copied by hand:
# (IKM, salt, info, L, PRK, OKM).
RFC5869 = [
    (
        "0b" * 22,
        "000102030405060708090a0b0c",
        "f0f1f2f3f4f5f6f7f8f9",
        42,
        "077709362c2e32df0ddc3f0dc47bba6390b6c73bb50f9c3122ec844ad7c2b3e5",
        "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865",
    ),
    (
        bytes(range(0x00, 0x50)).hex(),
        bytes(range(0x60, 0xB0)).hex(),
        bytes(range(0xB0, 0x100)).hex(),
        82,
        "06a6b88c5853361a06104c9ceb35b45cef760014904671014a193f40c15fc244",
        "b11e398dc80327a1c8e7f78c596a49344f012eda2d4efad8a050cc4c19afa97c"
        "59045a99cac7827271cb41c65e590e09da3275600c2f09b8367793a9aca3db71"
        "cc30c58179ec3e87c14c01d5c1f3434f1d87",
    ),
    (
        "0b" * 22,
        "",
        "",
        42,
        "19ef24a32c717b167f33a91d6f648bdf96596776afdb6377ac434c1c293ccb04",
        "8da4e775a563c18f715f802a063c5a31b8a11f5c5ee1879ec3454e5f3c738d2d9d201395faa4b61a96c8",
    ),
]


@pytest.mark.parametrize("ikm,salt,info,length,prk,okm", RFC5869, ids=["A.1", "A.2", "A.3"])
def test_rfc5869_appendix_a(ikm: str, salt: str, info: str, length: int, prk: str, okm: str) -> None:
    assert hkdf_extract(H(salt), H(ikm)) == H(prk)
    assert hkdf_expand(H(prk), H(info), length) == H(okm)
    assert hkdf(H(salt), H(ikm), H(info), length) == H(okm)


# RFC 8448 Section 3 (simple 1-RTT handshake), the start of the TLS 1.3 key schedule.
EARLY_SECRET = "33ad0a1c607ec03b09e6cd9893680ce210adf300aa1f2660e1b22e10f170f92a"
EMPTY_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
DERIVED_INFO = (
    "0020 0d 746c73313320646572697665 64"
    "20 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
DERIVED = "6f2615a108c702c5678f54fc9dbab69716c076189c48250cebeac3576c3611ba"
ECDHE_SHARED = "8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d"
HANDSHAKE_SECRET = "1dc826e93606aa6fdc0aadc12f741b01046aa6b99f691ed221a9f0ca043fbeac"
CH_SH_HASH = "860c06edc07858ee8e78f0e7428c58edd6b43f2ca3e6e95f02ed063cf0e1cad8"
C_HS_TRAFFIC = "b3eddb126e067f35a780b3abf45e2d8f3b1a950738f52e9600746a0e27a55a21"
S_HS_TRAFFIC = "b67b7d690cc16c4e75e54213cb2d37b4e9c912bcded9105d42befd59d391ad38"
S_HS_KEY = "3fce516009c21727d0f2e4e86ee403bc"
S_HS_IV = "5d313eb2671276ee13000b30"


def test_rfc8448_key_schedule() -> None:
    early = hkdf_extract(bytes(32), bytes(32))
    assert early == H(EARLY_SECRET)
    assert hashlib.sha256(b"").digest() == H(EMPTY_HASH)
    derived = derive_secret(early, b"derived", H(EMPTY_HASH))
    assert derived == H(DERIVED)
    assert hkdf_expand(early, H(DERIVED_INFO), 32) == H(DERIVED)
    handshake = hkdf_extract(derived, H(ECDHE_SHARED))
    assert handshake == H(HANDSHAKE_SECRET)
    assert derive_secret(handshake, b"c hs traffic", H(CH_SH_HASH)) == H(C_HS_TRAFFIC)
    s_hs = derive_secret(handshake, b"s hs traffic", H(CH_SH_HASH))
    assert s_hs == H(S_HS_TRAFFIC)
    assert hkdf_expand_label(s_hs, b"key", b"", 16) == H(S_HS_KEY)
    assert hkdf_expand_label(s_hs, b"iv", b"", 12) == H(S_HS_IV)


def test_expand_label_layout() -> None:
    out = hkdf_expand_label(bytes(32), b"key", b"", 16)
    info = bytes([0, 16, 9]) + b"tls13 key" + bytes([0])
    assert out == hkdf_expand(bytes(32), info, 16)


def test_output_is_a_prefix_and_info_separates_keys() -> None:
    rng = random.Random(5869)
    prk = hkdf_extract(rng.randbytes(16), rng.randbytes(32))
    long = hkdf_expand(prk, b"ctx", 200)
    for n in (1, 31, 32, 33, 64, 199):
        assert hkdf_expand(prk, b"ctx", n) == long[:n]
    assert hkdf_expand(prk, b"client key", 32) != hkdf_expand(prk, b"server key", 32)


def test_length_limit() -> None:
    prk = bytes(32)
    assert len(hkdf_expand(prk, b"", 255 * 32)) == 255 * 32
    with pytest.raises(ValueError):
        hkdf_expand(prk, b"", 255 * 32 + 1)


def test_sha512_variant_runs() -> None:
    prk = hkdf_extract(b"", b"ikm", "sha512")
    assert len(prk) == 64
    assert len(hkdf_expand(prk, b"", 100, "sha512")) == 100
