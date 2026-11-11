# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/additive-checksum/. The authors are listed in prov/MQA7XD.jsonl.

"""Additive checksums: the sum of the data words modulo 2^k.

The message is cut into words of w bytes (w = 1 or 2 here), each read as a
big-endian unsigned integer. A message whose length is not a multiple of w
is padded at the end with zero bytes. The checksum is the sum of the words
modulo 2^k with k = 8w (two's complement addition, the carry out of the top
bit is lost).

Cost: one addition per word, so Theta(n) time for n bytes and O(1) space.
"""


def additive_checksum(data: bytes, w: int = 1) -> int:
    """Return the sum of the w-byte big-endian words of data, modulo 2^(8w)."""
    if w < 1:
        raise ValueError("the word size must be at least one byte")
    modulus = 1 << (8 * w)
    if len(data) % w:
        data = bytes(data) + bytes(w - len(data) % w)  # pad with zero bytes
    s = 0  # @line L1
    for i in range(0, len(data), w):  # @line L2
        word = int.from_bytes(data[i : i + w], "big")  # @line L3
        s = (s + word) % modulus  # @line L4
    return s  # @line L5


def sum8(data: bytes) -> int:
    """The 8-bit additive checksum: the sum of the bytes modulo 256."""
    return additive_checksum(data, 1)


def sum16(data: bytes) -> int:
    """The 16-bit additive checksum: the sum of big-endian 16-bit words modulo 65536."""
    return additive_checksum(data, 2)


def check_value(data: bytes, w: int = 1) -> int:
    """Return the w-byte word c such that the checksum of data followed by c is 0.

    c is the two's complement negation of the checksum. The length of data
    must be a multiple of w, so that c falls on a word boundary.
    """
    if len(data) % w:
        raise ValueError("the data length must be a multiple of the word size")
    return (-additive_checksum(data, w)) % (1 << (8 * w))


def verify(data_with_check: bytes, w: int = 1) -> bool:
    """True when the message, including its check word, sums to 0."""
    return additive_checksum(data_with_check, w) == 0
