# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grain/. The authors are listed in prov/VM4425.jsonl.

"""Grain-128AEADv2 (Hell, Johansson, Maximov, Meier, Sonnerup, Yoshida), for study only.

This is the Round 3 NIST lightweight cryptography finalist, with the byte API of
its specification (Section 2.6): associated data is prefixed by a DER-style length
encoding and authenticated but not encrypted, and the tag is 64 bits.

This code is not constant time as Python runs it and must not protect real
data. Use a vetted AEAD from libsodium, OpenSSL or a FIPS 140 validated module.

Bit order, as in the specification (Section 7): bit j of byte b of a key, nonce,
message or tag is bit 8b + j of the bit string, so the least significant bit of
each byte comes first. Each register is a Python int whose bit i is s_i or b_i.
"""

from typing import Optional

M128 = (1 << 128) - 1
NFSR_TAPS_A = (2, 15, 36, 45, 64, 73, 89)


def _bits(data: bytes) -> list[int]:
    return [(x >> j) & 1 for x in data for j in range(8)]


def _from_bits(bits: list[int]) -> bytes:
    return bytes(sum(bits[8 * i + j] << j for j in range(8)) for i in range(len(bits) // 8))


def _pre_output(s: int, b: int) -> int:
    """y_t = h(x) + s_93 + sum of b_j for j in A (Section 2.1)."""

    def S(i: int) -> int:
        return (s >> i) & 1

    def B(i: int) -> int:
        return (b >> i) & 1

    h = (B(12) & S(8)) ^ (S(13) & S(20)) ^ (B(95) & S(42)) ^ (S(60) & S(79)) ^ (B(12) & B(95) & S(94))
    y = h ^ S(93)
    for j in NFSR_TAPS_A:
        y ^= B(j)
    return y


def _feedback(s: int, b: int) -> tuple[int, int]:
    """Return (L(S), s_0 + F(B)), the LFSR and NFSR feedback bits (Section 2.1)."""

    def S(i: int) -> int:
        return (s >> i) & 1

    def B(i: int) -> int:
        return (b >> i) & 1

    lin = S(0) ^ S(7) ^ S(38) ^ S(70) ^ S(81) ^ S(96)
    f = B(0) ^ B(26) ^ B(56) ^ B(91) ^ B(96)
    f ^= (B(3) & B(67)) ^ (B(11) & B(13)) ^ (B(17) & B(18)) ^ (B(27) & B(59))
    f ^= (B(40) & B(48)) ^ (B(61) & B(65)) ^ (B(68) & B(84))
    f ^= (B(22) & B(24) & B(25)) ^ (B(70) & B(78) & B(82)) ^ (B(88) & B(92) & B(93) & B(95))
    return lin, S(0) ^ f


def _clock(s: int, b: int, in_s: int, in_b: int) -> tuple[int, int, int]:
    """One clock: output y_t, shift both registers, and XOR in_s, in_b into the new bits."""
    y = _pre_output(s, b)
    fs, fb = _feedback(s, b)
    s = (s >> 1) | ((fs ^ in_s) << 127)
    b = (b >> 1) | ((fb ^ in_b) << 127)
    return y, s, b


def _init(key: bytes, nonce: bytes) -> tuple[int, int, int, int]:
    """Return (S, B, A, R) after the 512 initialization clocks (Section 2.2). Cost: Theta(512)."""
    if len(key) != 16 or len(nonce) != 12:
        raise ValueError("Grain-128AEADv2 needs a 16-byte key and a 12-byte nonce")
    k = _bits(key)
    b = int.from_bytes(key, "little")  # @line L1
    s = int.from_bytes(nonce, "little") | (((1 << 31) - 1) << 96)  # @line L1
    for _ in range(320):  # @line L2
        y = _pre_output(s, b)
        _, s, b = _clock(s, b, y, y)
    for t in range(320, 384):  # @line L3
        y = _pre_output(s, b)
        _, s, b = _clock(s, b, y ^ k[t - 256], y ^ k[t - 320])
    acc = reg = 0
    for j in range(64):  # @line L4
        y, s, b = _clock(s, b, 0, 0)
        acc |= y << j
    for j in range(64):  # @line L5
        y, s, b = _clock(s, b, 0, 0)
        reg |= y << j
    return s, b, acc, reg


def der_length(n: int) -> bytes:
    """Encode(n) of Section 2.6.1: one byte below 128, else 0x80 | count, then big-endian bytes."""
    if n < 128:
        return bytes([n])
    body = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(body)]) + body


def _process(key: bytes, nonce: bytes, ad: bytes, data: bytes, decrypt: bool) -> tuple[bytes, bytes]:
    """Run the AEAD mode over Encode(|ad|) || ad || data. Return (output data, tag).

    Cost: Theta(512 + 16 (|ad| + |data|)) clocks, two clocks for each bit.
    """
    s, b, acc, reg = _init(key, nonce)
    head = _bits(der_length(len(ad)) + ad)  # @line L6
    body = _bits(data)
    out = []
    for i, x in enumerate(head + body):  # @line L7
        z, s, b = _clock(s, b, 0, 0)  # @line L8
        zp, s, b = _clock(s, b, 0, 0)  # @line L8
        if i >= len(head):  # @line L9
            out.append(x ^ z)
            if decrypt:
                x ^= z  # the plaintext bit is what the accumulator authenticates
        if x:  # @line L10
            acc ^= reg
        reg = (reg >> 1) | (zp << 63)  # @line L11
    acc ^= reg  # @line L12
    return _from_bits(out), acc.to_bytes(8, "little")


def grain128aeadv2_encrypt(key: bytes, nonce: bytes, ad: bytes, pt: bytes) -> tuple[bytes, bytes]:
    """Return (ciphertext, 8-byte tag). Precondition: 16-byte key, 12-byte nonce, a new nonce per key."""
    return _process(key, nonce, ad, pt, decrypt=False)


def grain128aeadv2_decrypt(key: bytes, nonce: bytes, ad: bytes, ct: bytes, tag: bytes) -> Optional[bytes]:
    """Return the plaintext, or None if the tag is wrong. No plaintext is released on failure."""
    pt, t = _process(key, nonce, ad, ct, decrypt=True)
    diff = 0
    for x, y in zip(t, tag):  # @line L13
        diff |= x ^ y
    if diff != 0 or len(tag) != 8:
        return None
    return pt
