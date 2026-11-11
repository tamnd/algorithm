# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bcrypt/. The authors are listed in prov/PKNJPH.jsonl.

import random

import pytest

from bcrypt import (
    P_INIT,
    S_INIT,
    b64_decode,
    b64_encode,
    bcrypt_raw,
    blowfish_key_schedule,
    checkpw,
    hashpw,
)


def test_pi_tables() -> None:
    # Schneier, Description of a new variable-length key, 64-bit block cipher
    # (Blowfish), FSE 1993, subkey generation: the tables are the hex digits of
    # pi after the point, P1 = 0x243f6a88, P2 = 0x85a308d3. The S-boxes follow
    # the P-array in the same digit string; the first S-box word d1310ba6 is
    # also checked indirectly by the Eric Young vectors below.
    assert P_INIT[0] == 0x243F6A88
    assert P_INIT[1] == 0x85A308D3
    assert S_INIT[0][0] == 0xD1310BA6
    assert len(P_INIT) == 18 and all(len(box) == 256 for box in S_INIT)


@pytest.mark.parametrize(
    "key, clear, cipher",
    [
        # Eric Young, Blowfish test vectors (schneier.com, vectors.txt), ecb test data.
        ("0000000000000000", "0000000000000000", "4EF997456198DD78"),
        ("FFFFFFFFFFFFFFFF", "FFFFFFFFFFFFFFFF", "51866FD5B85ECB8A"),
        ("3000000000000000", "1000000000000001", "7D856F9A613063F2"),
        ("0123456789ABCDEF", "1111111111111111", "61F9C3802281B096"),
        ("FEDCBA9876543210", "0123456789ABCDEF", "0ACEAB0FC6A0A28D"),
        ("7CA110454A1A6E57", "01A1D6D039776742", "59C68245EB05282B"),
    ],
)
def test_blowfish_vectors(key: str, clear: str, cipher: str) -> None:
    bf = blowfish_key_schedule(bytes.fromhex(key))
    x = bytes.fromhex(clear)
    left, right = bf.encrypt(int.from_bytes(x[:4], "big"), int.from_bytes(x[4:], "big"))
    assert f"{left:08X}{right:08X}" == cipher


@pytest.mark.parametrize(
    "password, setting, expected",
    [
        # pyca/bcrypt, tests/test_bcrypt.py, list _test_vectors (cost 4 and 5).
        # The $2a$05$ vectors with U*U are the Openwall crypt_blowfish test vectors.
        (
            b"Kk4DQuMMfZL9o",
            b"$2b$04$cVWp4XaNU8a4v1uMRum2SO",
            b"$2b$04$cVWp4XaNU8a4v1uMRum2SO026BWLIoQMD/TXg5uZV.0P.uO8m3YEm",
        ),
        (
            b"9IeRXmnGxMYbs",
            b"$2b$04$pQ7gRO7e6wx/936oXhNjrO",
            b"$2b$04$pQ7gRO7e6wx/936oXhNjrOUNOHL1D0h1N2IDbJZYs.1ppzSof6SPy",
        ),
        (
            b"U*U",
            b"$2a$05$CCCCCCCCCCCCCCCCCCCCC.",
            b"$2a$05$CCCCCCCCCCCCCCCCCCCCC.E5YPO9kmyuRGyh0XouQYb4YMJKvyOeW",
        ),
        (
            b"U*U*",
            b"$2a$05$CCCCCCCCCCCCCCCCCCCCC.",
            b"$2a$05$CCCCCCCCCCCCCCCCCCCCC.VGOzA784oUp/Z0DY336zx7pLYAy0lwK",
        ),
        (
            b"U*U*U",
            b"$2a$05$XXXXXXXXXXXXXXXXXXXXXO",
            b"$2a$05$XXXXXXXXXXXXXXXXXXXXXOAcXxm9kjPGEMsLznoKqmqw7tc8WCx4a",
        ),
        (
            b"\xa3",
            b"$2a$05$/OK.fbVrR/bpIqNJ5ianF.",
            b"$2a$05$/OK.fbVrR/bpIqNJ5ianF.Sa7shbm4.OzKpvFnX1pQLmQW96oUlCq",
        ),
        (
            b"g7\r\x01\xf3\xd4\xd0\xa9JB^\x18\x007P\xb2N\xc7\x1c\xee\x87&\x83C"
            b"\x8b\xe8\x18\xc5>\x86\x14/\xd6\xcc\x1cJ\xde\xd7ix\xeb\xdeO\xef"
            b"\xe1i\xac\xcb\x03\x96v1' \xd6@.m\xa5!\xa0\xef\xc0(",
            b"$2a$04$tecY.9ylRInW/rAAzXCXPO",
            b"$2a$04$tecY.9ylRInW/rAAzXCXPOOlyYeCNzmNTzPDNSIFztFMKbvs/s5XG",
        ),
        # pyca/bcrypt, list _2y_test_vectors: $2y$ is the fixed Openwall prefix.
        (
            b"\xff\xff\xa3",
            b"$2y$05$/OK.fbVrR/bpIqNJ5ianF.",
            b"$2y$05$/OK.fbVrR/bpIqNJ5ianF.CE5elHaaO4EbggVDjb8P19RukzXSM3e",
        ),
    ],
)
def test_bcrypt_vectors(password: bytes, setting: bytes, expected: bytes) -> None:
    assert hashpw(password, setting) == expected
    assert checkpw(password, expected)


def test_wrong_password() -> None:
    # pyca/bcrypt, test_checkpw_wrong_password.
    assert not checkpw(b"badpass", b"$2b$04$2Siw3Nv3Q/gTOIPetAyPr.GNj3aO0lb1E5E9UumYGKjP9BYqlNWJe")


def test_72_byte_limit() -> None:
    salt = bytes(range(16))
    base = bytes(range(65, 65 + 26)) * 3  # 78 bytes
    assert bcrypt_raw(base[:72], salt, 4) == bcrypt_raw(base[:72] + b"tail", salt, 4)
    assert bcrypt_raw(base[:71], salt, 4) != bcrypt_raw(base[:72], salt, 4)


def test_base64_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(20):
        data = rng.randbytes(16)
        assert b64_decode(b64_encode(data)[:22], 16) == data
    assert len(b64_encode(bytes(23))) == 31


def test_salt_and_cost_change_output() -> None:
    salt = bytes(16)
    a = bcrypt_raw(b"password", salt, 4)
    assert a != bcrypt_raw(b"password", bytes(15) + b"\x01", 4)
    assert a != bcrypt_raw(b"password", salt, 5)


def test_avalanche() -> None:
    rng = random.Random(2)
    total, trials = 0, 6
    salt = rng.randbytes(16)
    for _ in range(trials):
        p = bytearray(rng.randbytes(8))
        a = int.from_bytes(bcrypt_raw(bytes(p), salt, 4), "big")
        p[rng.randrange(8)] ^= 1 << rng.randrange(7)
        b = int.from_bytes(bcrypt_raw(bytes(p), salt, 4), "big")
        total += bin(a ^ b).count("1")
    assert 70 < total / trials < 114  # about 92 of 184 bits
