# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/internet-checksum/. The authors are listed in prov/EH9YR6.jsonl.

"""The Internet checksum of RFC 1071, used by IPv4, ICMP, UDP and TCP.

The bytes are paired into 16-bit big-endian words (an odd last byte is padded
with a zero byte), the words are added in ones' complement arithmetic, and the
checksum is the ones' complement (bitwise NOT) of the sum. A message that holds
a correct checksum sums to 0xFFFF.

Cost: Theta(n) for n bytes, one addition per 16-bit word, O(1) extra space.
"""

import struct

MASK16 = 0xFFFF


def ones_sum(data: bytes, start: int = 0) -> int:
    """Ones' complement sum of the 16-bit big-endian words of data, added to start."""
    if len(data) % 2:  # @line L1
        data = bytes(data) + b"\x00"
    s = start  # @line L2
    for i in range(0, len(data), 2):  # @line L3
        s += (data[i] << 8) | data[i + 1]  # @line L4
    while s >> 16:  # @line L5
        s = (s & MASK16) + (s >> 16)  # @line L6
    return s


def internet_checksum(data: bytes) -> int:
    """The 16-bit Internet checksum of data (with its checksum field set to zero)."""
    return ~ones_sum(data) & MASK16  # @line L7


def verify(data: bytes) -> bool:
    """True when data, including its checksum field, sums to 0xFFFF (-0)."""
    return ones_sum(data) == MASK16


def ipv4_header_checksum(header: bytes) -> int:
    """Checksum of an IPv4 header: the checksum field (bytes 10 and 11) counts as zero."""
    if len(header) < 20 or len(header) % 4:
        raise ValueError("an IPv4 header has 20 to 60 bytes, a multiple of 4")
    h = bytes(header[:10]) + b"\x00\x00" + bytes(header[12:])
    return internet_checksum(h)


def pseudo_header_v4(src: bytes, dst: bytes, protocol: int, length: int) -> bytes:
    """The IPv4 pseudo header of TCP and UDP: source, destination, zero, protocol, length."""
    return bytes(src) + bytes(dst) + struct.pack("!BBH", 0, protocol, length)


def udp_checksum_v4(src: bytes, dst: bytes, udp: bytes) -> int:
    """UDP checksum over the pseudo header and the datagram (checksum field taken as 0).

    RFC 768: a computed checksum of zero is sent as all ones, because a zero in
    the field means that the sender did not compute a checksum.
    """
    seg = bytes(udp[:6]) + b"\x00\x00" + bytes(udp[8:])
    c = internet_checksum(pseudo_header_v4(src, dst, 17, len(udp)) + seg)
    return c if c != 0 else MASK16


def tcp_checksum_v4(src: bytes, dst: bytes, segment: bytes) -> int:
    """TCP checksum over the pseudo header and the segment (checksum field at bytes 16 and 17 taken as 0)."""
    seg = bytes(segment[:16]) + b"\x00\x00" + bytes(segment[18:])
    return internet_checksum(pseudo_header_v4(src, dst, 6, len(segment)) + seg)
