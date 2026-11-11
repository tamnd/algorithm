# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trivium/. The authors are listed in prov/RVXXYX.jsonl.

"""The Trivium stream cipher of De Canniere and Preneel (eSTREAM, 2005), for study only.

This code is not constant time as Python runs it and must not protect real
data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

Bit order, as in the eSTREAM reference code and test vectors: key bit K_i
(1 <= i <= 80) of the specification is bit (80-i) mod 8, counting from the
least significant bit, of key byte (80-i) // 8. So K_80 is the least
significant bit of byte 0 and K_1 is the most significant bit of byte 9.
The IV is loaded in the same way. Keystream bit z_1 is the least significant
bit of the first output byte.
"""


def _bits_lsb_first(b: bytes) -> list[int]:
    return [(x >> j) & 1 for x in b for j in range(8)]


def trivium_keystream_bits(key: bytes, iv: bytes, n: int) -> list[int]:
    """Return the first n keystream bits z_1 .. z_n.

    Precondition: 10-byte key and 10-byte IV. Cost: Theta(1152 + n) steps of a
    288-bit state (Theta(288) list work per step here, Theta(1) in hardware).
    """
    if len(key) != 10 or len(iv) != 10:
        raise ValueError("Trivium needs an 80-bit key and an 80-bit IV")
    k, v = _bits_lsb_first(key), _bits_lsb_first(iv)
    s = [0] * 289  # s[1] .. s[288]; s[0] is unused
    s[1:94] = k[::-1] + [0] * 13  # @line L1
    s[94:178] = v[::-1] + [0] * 4  # @line L2
    s[178:289] = [0] * 108 + [1, 1, 1]  # @line L3
    out = []
    for i in range(1, 1152 + n + 1):  # @line L4
        t1, t2, t3 = s[66] ^ s[93], s[162] ^ s[177], s[243] ^ s[288]  # @line L5
        if i > 1152:
            out.append(t1 ^ t2 ^ t3)  # @line L6
        t1 ^= (s[91] & s[92]) ^ s[171]  # @line L7
        t2 ^= (s[175] & s[176]) ^ s[264]  # @line L8
        t3 ^= (s[286] & s[287]) ^ s[69]  # @line L9
        s[1:94] = [t3] + s[1:93]  # @line L10
        s[94:178] = [t1] + s[94:177]  # @line L11
        s[178:289] = [t2] + s[178:288]  # @line L12
    return out


def trivium_keystream(key: bytes, iv: bytes, nbytes: int) -> bytes:
    """Return nbytes keystream bytes, bit z_(8j+1) as the least significant bit of byte j."""
    z = trivium_keystream_bits(key, iv, 8 * nbytes)
    return bytes(sum(z[8 * j + b] << b for b in range(8)) for j in range(nbytes))


def trivium_crypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    """Encrypt or decrypt data by XOR with the keystream. Never reuse a (key, IV) pair."""
    ks = trivium_keystream(key, iv, len(data))
    return bytes(a ^ b for a, b in zip(data, ks))
