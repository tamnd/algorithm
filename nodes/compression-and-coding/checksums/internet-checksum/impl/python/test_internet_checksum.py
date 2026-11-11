# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/internet-checksum/. The authors are listed in prov/EH9YR6.jsonl.

import random
import struct

from internet_checksum import (
    internet_checksum,
    ipv4_header_checksum,
    ones_sum,
    tcp_checksum_v4,
    udp_checksum_v4,
    verify,
)


def oracle_sum(data: bytes) -> int:
    """Independent ones' complement sum: the total of the words, reduced mod 0xFFFF into 1..0xFFFF."""
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack("!%dH" % (len(data) // 2), data))
    return 0 if total == 0 else (total - 1) % 0xFFFF + 1


def test_rfc1071_section3() -> None:
    # RFC 1071 Section 3, numerical example: the bytes 00 01 f2 03 f4 f5 f6 f7
    # have the ones' complement sum ddf2. The checksum is its complement, 220d.
    data = bytes.fromhex("0001f203f4f5f6f7")
    assert ones_sum(data) == 0xDDF2
    assert internet_checksum(data) == 0x220D
    assert verify(data + bytes.fromhex("220d"))


def test_ipv4_header_example() -> None:
    # The IPv4 header of Wikipedia, "Internet checksum", Examples:
    # 4500 0073 0000 4000 4011 b861 c0a8 0001 c0a8 00c7 (192.168.0.1 to 192.168.0.199, UDP, TTL 64).
    header = bytes.fromhex("450000730000400040110000c0a80001c0a800c7")
    assert ones_sum(header) == 0x479E
    assert ipv4_header_checksum(header) == 0xB861
    full = bytes.fromhex("45000073000040004011b861c0a80001c0a800c7")
    assert ones_sum(full) == 0xFFFF
    assert verify(full)
    assert ipv4_header_checksum(full) == 0xB861  # the old field value is ignored


def test_edges() -> None:
    assert internet_checksum(b"") == 0xFFFF
    assert internet_checksum(b"\x00\x00") == 0xFFFF
    assert internet_checksum(b"\xff\xff") == 0x0000
    assert internet_checksum(b"\x01") == 0xFEFF  # odd length: 01 00
    assert internet_checksum(b"\xff" * 1000) == 0x0000


def test_random_against_oracle_and_verify() -> None:
    rng = random.Random(5101)
    for _ in range(800):
        n = rng.randrange(0, 64)
        data = bytes(rng.choice([0, 255, rng.randrange(256)]) for _ in range(n))
        assert ones_sum(data) == oracle_sum(data)
        c = internet_checksum(data)
        assert c == ~oracle_sum(data) & 0xFFFF
        if n % 2 == 0:
            for pos in range(0, n + 1, 2):  # the field can sit at any even offset
                msg = data[:pos] + struct.pack("!H", c) + data[pos:]
                assert verify(msg)


def test_udp_with_pseudo_header() -> None:
    rng = random.Random(5102)
    src, dst = bytes([192, 0, 2, 1]), bytes([198, 51, 100, 7])
    for _ in range(300):
        payload = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 30)))
        udp = struct.pack("!HHHH", 5353, 53, 8 + len(payload), 0) + payload
        c = udp_checksum_v4(src, dst, udp)
        assert c != 0
        sent = udp[:6] + struct.pack("!H", c) + udp[8:]
        pseudo = src + dst + struct.pack("!BBH", 0, 17, len(udp))
        assert verify(pseudo + sent)


def test_tcp_with_pseudo_header() -> None:
    src, dst = bytes([10, 0, 0, 1]), bytes([10, 0, 0, 2])
    seg = struct.pack("!HHIIBBHHH", 40000, 80, 1, 0, 5 << 4, 0x02, 65535, 0, 0) + b"hello"
    c = tcp_checksum_v4(src, dst, seg)
    sent = seg[:16] + struct.pack("!H", c) + seg[18:]
    assert verify(src + dst + struct.pack("!BBH", 0, 6, len(seg)) + sent)


def test_known_misses() -> None:
    rng = random.Random(5103)
    data = bytes(rng.randrange(1, 255) for _ in range(40))
    c = internet_checksum(data)
    # Swapping two aligned 16-bit words is never detected.
    words = [data[i : i + 2] for i in range(0, 40, 2)]
    words[3], words[11] = words[11], words[3]
    assert internet_checksum(b"".join(words)) == c
    # A word 0x0000 replaced by 0xFFFF (or back) is never detected.
    z = data[:10] + b"\x00\x00" + data[12:]
    f = data[:10] + b"\xff\xff" + data[12:]
    assert internet_checksum(z) == internet_checksum(f)
    # Every single-bit error is detected.
    for i in range(40):
        for bit in range(8):
            b = bytearray(data)
            b[i] ^= 1 << bit
            assert internet_checksum(bytes(b)) != c
