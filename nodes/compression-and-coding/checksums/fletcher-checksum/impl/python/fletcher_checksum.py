# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fletcher-checksum/. The authors are listed in prov/4GV784.jsonl.

"""Fletcher checksums (Fletcher 1982): two running sums modulo 2^b - 1.

Fletcher-16 reads bytes (b = 8, modulus 255); Fletcher-32 reads 16-bit words
(b = 16, modulus 65535). Both sums start at 0:

    A <- (A + d_i) mod M,    B <- (B + A) mod M,

and the checksum is B * 2^b + A. The fast versions add up to a block of words
before they reduce, which is safe while B stays below 2^32 (the deferred
modulo). With A, B < M at the start of a block and every word at most M:

    B < M + k*M + M*k*(k+1)/2 <= 2^32 - 1

holds for k = 5802 bytes (M = 255) and k = 360 words (M = 65535).

Fletcher-32 needs a byte order for its 16-bit words. The published test
vectors (Wikipedia, "Fletcher's checksum") use little-endian words, so that is
the default here. An odd length is padded with one zero byte.

Cost: Theta(n) additions for n bytes, and one reduction per block.
"""

BLOCK16 = 5802  # bytes per block for Fletcher-16 with 32-bit sums
BLOCK32 = 360  # words per block for Fletcher-32 with 32-bit sums
LIMIT = (1 << 32) - 1


def fletcher_plain(words: list[int], m: int) -> tuple[int, int]:
    """The definition: reduce after every word. Returns (A, B)."""
    a = b = 0
    for d in words:
        a = (a + d) % m
        b = (b + a) % m
    return a, b


def _fletcher_blocks(words: list[int], m: int, block: int) -> tuple[int, int]:
    """Two running sums with the modulo deferred to the end of each block."""
    a = b = 0  # @line L1
    i = 0
    while i < len(words):  # @line L2
        end = min(i + block, len(words))  # @line L3
        while i < end:  # @line L4
            a += words[i]  # @line L5
            b += a  # @line L6
            i += 1
        assert b <= LIMIT, "the block bound keeps both sums inside 32 bits"
        a %= m  # @line L7
        b %= m  # @line L8
    return a, b  # @line L9


def fletcher16(data: bytes) -> int:
    """Fletcher-16 of a byte string: (B << 8) | A with sums modulo 255."""
    a, b = _fletcher_blocks(list(data), 255, BLOCK16)
    return (b << 8) | a


def fletcher32(data: bytes, order: str = "little") -> int:
    """Fletcher-32 of a byte string read as 16-bit words: (B << 16) | A with sums modulo 65535."""
    if len(data) % 2:
        data = bytes(data) + b"\x00"
    words = [int.from_bytes(data[i : i + 2], order) for i in range(0, len(data), 2)]
    a, b = _fletcher_blocks(words, 65535, BLOCK32)
    return (b << 16) | a


def fletcher16_check_bytes(data: bytes) -> bytes:
    """Two check bytes c0, c1 such that the Fletcher-16 sums of data + c0 + c1 are both 0 mod 255.

    This is the form in which the OSI protocols carry the checksum: the receiver
    runs the same loop over the whole message and expects A = B = 0 mod 255.
    """
    a, b = fletcher_plain(list(data), 255)
    c0 = 255 - (a + b) % 255
    c1 = 255 - (a + c0) % 255
    return bytes([c0, c1])
