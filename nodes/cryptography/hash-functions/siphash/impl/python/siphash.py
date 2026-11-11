# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/siphash/. The authors are listed in prov/V4BHB1.jsonl.
"""SipHash-c-d (Aumasson and Bernstein, INDOCRYPT 2012) and HalfSipHash-c-d.

siphash(key, msg) is SipHash-2-4 with a 16-byte key and a 64-bit output.
The rounds c and d are parameters, so SipHash-1-3 is siphash(key, msg, 1, 3).
halfsiphash32 is HalfSipHash with 32-bit words, a 64-bit key and a 32-bit output.

For study only. The code is not constant time and must not protect real data.
Use the SipHash of your language runtime, or the crypto_shorthash function of
libsodium, instead.
"""

M64 = (1 << 64) - 1
M32 = (1 << 32) - 1


def _rotl64(x: int, b: int) -> int:
    return ((x << b) | (x >> (64 - b))) & M64


def _rotl32(x: int, b: int) -> int:
    return ((x << b) | (x >> (32 - b))) & M32


def sipround(v: list[int]) -> None:
    """One SipRound on the four 64-bit words v0, v1, v2, v3 (ARX: add, rotate, xor)."""
    v0, v1, v2, v3 = v
    v0 = (v0 + v1) & M64
    v1 = _rotl64(v1, 13) ^ v0
    v0 = _rotl64(v0, 32)
    v2 = (v2 + v3) & M64
    v3 = _rotl64(v3, 16) ^ v2
    v0 = (v0 + v3) & M64
    v3 = _rotl64(v3, 21) ^ v0
    v2 = (v2 + v1) & M64
    v1 = _rotl64(v1, 17) ^ v2
    v2 = _rotl64(v2, 32)
    v[:] = [v0, v1, v2, v3]


def message_words(msg: bytes, word: int) -> list[int]:
    """Cut msg into little-endian words of `word` bytes; the last word ends with |msg| mod 256."""
    full = len(msg) - len(msg) % word
    words = [int.from_bytes(msg[i : i + word], "little") for i in range(0, full, word)]
    tail = msg[full:] + bytes(word - 1 - len(msg) % word) + bytes([len(msg) & 0xFF])
    words.append(int.from_bytes(tail, "little"))  # @line L3
    return words


def siphash_state(key: bytes, msg: bytes, c: int = 2, d: int = 4) -> list[int]:
    """The state before the final xor, for tracing; see siphash."""
    if len(key) != 16:
        raise ValueError("a SipHash key has 16 bytes")
    k0 = int.from_bytes(key[:8], "little")  # @line L1
    k1 = int.from_bytes(key[8:], "little")  # @line L1
    v = [
        k0 ^ 0x736F6D6570736575,  # @line L2
        k1 ^ 0x646F72616E646F6D,
        k0 ^ 0x6C7967656E657261,
        k1 ^ 0x7465646279746573,
    ]
    for m in message_words(msg, 8):
        v[3] ^= m  # @line L4
        for _ in range(c):
            sipround(v)  # @line L4
        v[0] ^= m  # @line L4
    v[2] ^= 0xFF  # @line L5
    for _ in range(d):
        sipround(v)  # @line L6
    return v


def siphash(key: bytes, msg: bytes, c: int = 2, d: int = 4) -> int:
    """SipHash-c-d of msg under a 16-byte key, as a 64-bit integer."""
    v = siphash_state(key, msg, c, d)
    return v[0] ^ v[1] ^ v[2] ^ v[3]  # @line L7


def siphash_bytes(key: bytes, msg: bytes, c: int = 2, d: int = 4) -> bytes:
    """The 8-byte output in the byte order of the reference code (little-endian)."""
    return siphash(key, msg, c, d).to_bytes(8, "little")


def _half_round(v: list[int]) -> None:
    v0, v1, v2, v3 = v
    v0 = (v0 + v1) & M32
    v1 = _rotl32(v1, 5) ^ v0
    v0 = _rotl32(v0, 16)
    v2 = (v2 + v3) & M32
    v3 = _rotl32(v3, 8) ^ v2
    v0 = (v0 + v3) & M32
    v3 = _rotl32(v3, 7) ^ v0
    v2 = (v2 + v1) & M32
    v1 = _rotl32(v1, 13) ^ v2
    v2 = _rotl32(v2, 16)
    v[:] = [v0, v1, v2, v3]


def halfsiphash32(key: bytes, msg: bytes, c: int = 2, d: int = 4) -> bytes:
    """HalfSipHash-c-d with an 8-byte key and a 4-byte output (reference halfsiphash.c)."""
    if len(key) != 8:
        raise ValueError("a HalfSipHash key has 8 bytes")
    k0 = int.from_bytes(key[:4], "little")
    k1 = int.from_bytes(key[4:], "little")
    v = [k0, k1, 0x6C796765 ^ k0, 0x74656462 ^ k1]
    for m in message_words(msg, 4):
        v[3] ^= m
        for _ in range(c):
            _half_round(v)
        v[0] ^= m
    v[2] ^= 0xFF
    for _ in range(d):
        _half_round(v)
    return (v[1] ^ v[3]).to_bytes(4, "little")
