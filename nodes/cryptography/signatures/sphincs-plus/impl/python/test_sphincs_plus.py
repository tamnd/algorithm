# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sphincs-plus/. The authors are listed in prov/XRB4YB.jsonl.
"""Tests for SLH-DSA-SHAKE-128f.

The vectors come from the NIST ACVP-Server repository (gen-val/json-files),
SLH-DSA-keyGen-FIPS205 test case 31 and SLH-DSA-sigGen-FIPS205 test case 58
(SLH-DSA-SHAKE-128f, deterministic, external interface, pure, with a context).
The 17088-byte signature of test case 58 is checked by its SHA-256 digest
and its first 16 bytes, so that it does not need to be copied here.
"""

import hashlib

import pytest

from sphincs_plus import (
    K,
    LEN,
    M,
    N,
    SIG_BYTES,
    base_2b,
    keygen_internal,
    sign,
    sign_internal,
    split_digest,
    verify,
    verify_internal,
    wots_digits,
)

TC58_SK = bytes.fromhex(
    "29B12FEFB5411A79AAF84B3CBF8A02218E2B5A524FDC4A8D8279DB47DD74B5A8"
    "4F190B458385EF8EBD1C6FCAF8F41657E9A0392166A29A3B05AB262627011DC9"
)
TC58_PK = TC58_SK[32:]
TC58_MSG = bytes.fromhex(
    "00FFDCA5C6F2279728713DD597E26220A44424314B9ED8DEE43E812121CACD05"
    "48049C6FC08F31E2740EA444A6066C7EABFAF2B6C896649C6E9C35F8D49BA6CD"
    "B6E3DC03600E1A96FBECC7AF3B477A193656BCC79783E82408FC7DDB262CCF3C"
    "BEDF8C2120A3D468C1893AB1BB6C99EC785B25A4D764AD4205FCA73576DC2035"
    "9E831CD434F2755CFA942B44C5EE20B032F4B747626DBFDAB4C01495FFCFFDED"
    "CE009FDB1CCBE02FA38811973F61031A91A70473C9EF363D5F399F142218E40C"
    "2B6AA6C908B2573667813698AB1E1454D537AEE3DC285774C9A88E740248B0D9"
    "20BDB553B5D851408BE19C2164FFE6EDADA25CD3F204CAE1BE5B"
)
TC58_CTX = bytes.fromhex(
    "0574B468E6D8487D5A61E3EB9ED9013F778FF989A25BC7726DB90C9FEBECBD42"
    "C3066CC8212EFC8AD827E9C34D5F"
)
TC58_SIG_SHA256 = "987f710aee822acb0ed6baaceea7220e3ef24bc3bff264472bf8300590de4630"


def test_parameters() -> None:
    assert (LEN, M, SIG_BYTES) == (35, 34, 17088)
    assert (K * 6 + 7) // 8 + (63 + 7) // 8 + (3 + 7) // 8 == M


def test_base_2b() -> None:
    assert base_2b(bytes([0x12, 0x34]), 4, 4) == [1, 2, 3, 4]
    assert base_2b(bytes([0b10101011, 0b11001100]), 6, 2) == [0b101010, 0b111100]
    assert wots_digits(bytes(N))[LEN - 3 :] == [0x1, 0xE, 0x0]  # 32 * 15 = 480 = 0x1E0


def test_split_digest() -> None:
    digest = bytes(25) + bytes([0xFF] * 8) + bytes([0xFF])
    md, idx_tree, idx_leaf = split_digest(digest)
    assert md == bytes(25)
    assert idx_tree == (1 << 63) - 1  # 64 bits read, 63 kept
    assert idx_leaf == 7  # 8 bits read, 3 kept


def test_acvp_keygen_tc31() -> None:
    sk, pk = keygen_internal(
        bytes.fromhex("3956AB391B4D22FC907AF0740326D061"),
        bytes.fromhex("AB0EB206436F2B86EBE086D77739B3E4"),
        bytes.fromhex("56505C229F4E7FA6B201714C7DCC9DA3"),
    )
    assert pk.hex().upper() == "56505C229F4E7FA6B201714C7DCC9DA366578F1F24C3FE371C97C14CE0E79CDC"
    assert sk[32:] == pk


def test_acvp_siggen_tc58() -> None:
    sig = sign(TC58_MSG, TC58_SK, TC58_CTX, deterministic=True)
    assert len(sig) == 17088
    assert sig[:16].hex().upper() == "7C9F71ABD898CBF659E8026B382980D4"
    assert hashlib.sha256(sig).hexdigest() == TC58_SIG_SHA256
    assert verify(TC58_MSG, sig, TC58_PK, TC58_CTX)
    assert not verify(TC58_MSG, sig, TC58_PK, b"")


@pytest.fixture(scope="module")
def hedged() -> tuple[bytes, bytes, bytes]:
    sk, pk = keygen_internal(bytes([1]) * N, bytes([2]) * N, bytes([3]) * N)
    msg = b"pay Bob 10"
    sig = sign_internal(bytes([0, 0]) + msg, sk, bytes([4]) * N)
    return pk, msg, sig


def test_hedged_round_trip(hedged: tuple[bytes, bytes, bytes]) -> None:
    pk, msg, sig = hedged
    assert verify(msg, sig, pk)
    assert not verify(b"pay Bob 99", sig, pk)
    assert not verify(msg, sig, pk, b"ctx")


def test_changed_signature_rejected(hedged: tuple[bytes, bytes, bytes]) -> None:
    pk, msg, sig = hedged
    for pos in (0, N + 5, (1 + K * 7) * N + 3, len(sig) - 1):  # R, FORS, first and last HT layer
        bad = bytearray(sig)
        bad[pos] ^= 1
        assert not verify(msg, bytes(bad), pk)
    assert not verify(msg, sig[:-1], pk)


def test_pure_domain_separation(hedged: tuple[bytes, bytes, bytes]) -> None:
    pk, msg, sig = hedged
    # The signature is on 0x00 || 0x00 || msg, so it does not verify for msg itself.
    assert verify_internal(bytes([0, 0]) + msg, sig, pk)
    assert not verify_internal(msg, sig, pk)
