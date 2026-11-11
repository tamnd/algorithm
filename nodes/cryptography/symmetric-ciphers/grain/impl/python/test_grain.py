# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grain/. The authors are listed in prov/VM4425.jsonl.

import random

from grain import _init, der_length, grain128aeadv2_decrypt, grain128aeadv2_encrypt

# Grain-128AEADv2 specification (NIST LWC Round 3), Section 7. Hex strings list
# the bytes in order, each byte read least significant bit first.
SPEC = [
    {
        "key": "00000000000000000000000000000000",
        "nonce": "000000000000000000000000",
        "ad": "",
        "pt": "",
        "nfsr": "81f7e0c655d035823310c278438dbc20",
        "lfsr": "8f395a9421b0963364e2ed30679c8ee1",
        "acc": "e89a32b9c0461a6a",
        "reg": "b199ade7204c6bfe",
        "ct": "",
        "tag": "7137d5998c2de4a5",
    },
    {
        "key": "000102030405060708090a0b0c0d0e0f",
        "nonce": "000102030405060708090a0b",
        "ad": "0001020304050607",
        "pt": "0001020304050607",
        "nfsr": "b3c2e1b1eec1f08c2d6eae957f6af9d0",
        "lfsr": "0e1f950d45e05087c4cd63fd00eab310",
        "acc": "c77202737ae7c7ee",
        "reg": "33126dd7a21b9073",
        "ct": "96d1bda7ae11f0ba",
        "tag": "22b0c12039a20e28",
    },
]


def test_state_after_initialization() -> None:
    for v in SPEC:
        s, b, acc, reg = _init(bytes.fromhex(v["key"]), bytes.fromhex(v["nonce"]))
        assert b.to_bytes(16, "little").hex() == v["nfsr"]
        assert s.to_bytes(16, "little").hex() == v["lfsr"]
        assert acc.to_bytes(8, "little").hex() == v["acc"]
        assert reg.to_bytes(8, "little").hex() == v["reg"]


def test_spec_vectors() -> None:
    for v in SPEC:
        key, nonce = bytes.fromhex(v["key"]), bytes.fromhex(v["nonce"])
        ad, pt = bytes.fromhex(v["ad"]), bytes.fromhex(v["pt"])
        ct, tag = grain128aeadv2_encrypt(key, nonce, ad, pt)
        assert ct.hex() == v["ct"] and tag.hex() == v["tag"]
        assert grain128aeadv2_decrypt(key, nonce, ad, ct, tag) == pt


def test_round_trip_and_forgery_rejected() -> None:
    rng = random.Random(3)
    for _ in range(6):
        key, nonce = rng.randbytes(16), rng.randbytes(12)
        ad, pt = rng.randbytes(rng.randrange(12)), rng.randbytes(rng.randrange(1, 12))
        ct, tag = grain128aeadv2_encrypt(key, nonce, ad, pt)
        assert grain128aeadv2_decrypt(key, nonce, ad, ct, tag) == pt
        bad_ct = bytes([ct[0] ^ 1]) + ct[1:]
        assert grain128aeadv2_decrypt(key, nonce, ad, bad_ct, tag) is None
        assert grain128aeadv2_decrypt(key, nonce, ad + b"\x00", ct, tag) is None
        assert grain128aeadv2_decrypt(key, nonce, ad, ct, bytes([tag[0] ^ 0x80]) + tag[1:]) is None


def test_der_length() -> None:
    assert der_length(0) == b"\x00"
    assert der_length(127) == b"\x7f"
    assert der_length(128) == b"\x81\x80"
    assert der_length(300) == b"\x82\x01\x2c"


def test_long_associated_data_round_trip() -> None:
    key, nonce = bytes(range(16)), bytes(12)
    ad = bytes(130)
    ct, tag = grain128aeadv2_encrypt(key, nonce, ad, b"hi")
    assert grain128aeadv2_decrypt(key, nonce, ad, ct, tag) == b"hi"
