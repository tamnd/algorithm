# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crc32c/. The authors are listed in prov/7288F4.jsonl.

import random

from crc32c import POLY, crc32c, crc32c_bitwise, crc32c_update, has_weight_2_or_4, syndromes, to_wire

RNG = random.Random(3720)

# RFC 3720 (iSCSI), Appendix B.4 "CRC Examples". The RFC lists the digest
# bytes in transmission order; copied by hand.
READ_10_PDU = bytes.fromhex(
    "01c00000" "00000000" "00000000" "00000000"
    "14000000" "00000400" "00000014" "00000018"
    "28000000" "00000000" "02000000" "00000000"
)
RFC3720_B4 = [
    (bytes(32), "aa36918a"),  # 32 bytes of zeros
    (bytes([0xFF] * 32), "43aba862"),  # 32 bytes of ones
    (bytes(range(32)), "4e79dd46"),  # 32 bytes incrementing 00..1f
    (bytes(range(31, -1, -1)), "5cdb3f11"),  # 32 bytes decrementing 1f..00
    (READ_10_PDU, "563a96d9"),  # an iSCSI Read (10) command PDU
]


def test_rfc3720_vectors() -> None:
    assert len(READ_10_PDU) == 48
    for data, wire in RFC3720_B4:
        assert to_wire(crc32c(data)).hex() == wire
        assert to_wire(crc32c_bitwise(data)).hex() == wire


def test_catalogue_check_and_residue() -> None:
    # CRC-32/ISCSI in the reveng catalogue: check 0xE3069283, residue 0xB798B438.
    assert crc32c(b"123456789") == 0xE3069283
    for n in (0, 1, 7, 100):
        data = bytes(RNG.randrange(256) for _ in range(n))
        codeword = data + to_wire(crc32c(data))
        reg = crc32c_update(0xFFFFFFFF, codeword)
        assert reg == 0xB798B438


def test_table_equals_bitwise_and_streaming() -> None:
    for n in range(0, 80):
        data = bytes(RNG.randrange(256) for _ in range(n))
        assert crc32c(data) == crc32c_bitwise(data)
        cut = RNG.randrange(n + 1)
        assert crc32c(data[cut:], crc32c(data[:cut])) == crc32c(data)


def test_hamming_distance_at_1024_data_bits() -> None:
    # Koopman's CRC zoo: CRC-32C (0x8F6E37A0 in Koopman notation) has HD 6
    # up to 5243 data bits; IEEE CRC-32 (0x82608EDB) has HD 5 only, from 269
    # to 2974 data bits. Check both at 1024 data bits + 32 check bits.
    n = 1024 + 32
    assert not has_weight_2_or_4(n, POLY)
    # The search finds what it should: x^32 + 1 is a weight-2 codeword and
    # x^32 + x^2 + x + 1 is a weight-4 codeword, both of length 33.
    assert has_weight_2_or_4(33, 0x1) and has_weight_2_or_4(33, 0x7)
    assert not has_weight_2_or_4(32, 0x7)
    # Weight 3 and 5 are impossible for CRC-32C: G(x) has an even number of
    # terms, so (x + 1) divides it and every codeword has even weight.
    assert bin((1 << 32) | POLY).count("1") % 2 == 0
    # IEEE CRC-32 has odd-weight codewords: find one of weight 5 by a random
    # triple that meets a pair (meet in the middle).
    s = syndromes(n, 0x04C11DB7)
    pairs = {}
    for a in range(n):
        for b in range(a + 1, n):
            pairs.setdefault(s[a] ^ s[b], (a, b))
    found = None
    for _ in range(200000):
        a, b, c = RNG.sample(range(n), 3)
        hit = pairs.get(s[a] ^ s[b] ^ s[c])
        if hit and len({a, b, c, *hit}) == 5:
            found = {a, b, c, *hit}
            break
    assert found is not None
    acc = 0
    for i in found:
        acc ^= s[i]
    assert acc == 0
