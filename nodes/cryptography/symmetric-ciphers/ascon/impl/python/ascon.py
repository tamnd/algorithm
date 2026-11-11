# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ascon/. The authors are listed in prov/F7H5VG.jsonl.

"""Ascon-AEAD128 as specified in NIST SP 800-232 (August 2025), for study only.

This is the standardized version, not Ascon-128 or Ascon-128a v1.2: the IV,
the byte order (little-endian words) and the domain separation differ. The
code is not constant time as Python runs it and must not protect real data.
Use a vetted implementation, such as one in a FIPS 140 validated module.
"""

MASK = (1 << 64) - 1
IV = 0x00001000808C0001
# const_0 .. const_15 of SP 800-232 Table 5; round i of p[r] adds const_{16-r+i}.
CONST = [0x3C, 0x2D, 0x1E, 0x0F, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B]
ROT = [(19, 28), (61, 39), (1, 6), (10, 17), (7, 41)]


def _rotr(x: int, r: int) -> int:
    return ((x >> r) | (x << (64 - r))) & MASK


def ascon_p(s: list[int], rounds: int) -> None:
    """Apply Ascon-p[rounds] to the five 64-bit words of s, in place.

    Precondition: 1 <= rounds <= 16. Cost: Theta(rounds) word operations.
    """
    for i in range(16 - rounds, 16):  # @line L1
        s[2] ^= CONST[i]  # @line L2
        # The substitution layer: the 5-bit S-box on each of the 64 bit slices.
        x0, x1, x2, x3, x4 = s  # @line L3
        x0 ^= x4
        x4 ^= x3
        x2 ^= x1
        t0, t1, t2, t3, t4 = (~x0 & x1), (~x1 & x2), (~x2 & x3), (~x3 & x4), (~x4 & x0)
        x0 ^= t1
        x1 ^= t2
        x2 ^= t3
        x3 ^= t4
        x4 ^= t0
        x1 ^= x0
        x0 ^= x4
        x3 ^= x2
        x2 = ~x2 & MASK
        s[:] = [x0 & MASK, x1 & MASK, x2, x3 & MASK, x4 & MASK]
        for j, (a, b) in enumerate(ROT):  # @line L4
            s[j] ^= _rotr(s[j], a) ^ _rotr(s[j], b)


def _le(b: bytes) -> int:
    return int.from_bytes(b, "little")


def _pad(block: bytes) -> bytes:
    """Pad a block of fewer than 16 bytes with 0x01 and zeros, to 16 bytes."""
    return block + b"\x01" + bytes(15 - len(block))


def _init(key: bytes, nonce: bytes) -> tuple[list[int], int, int]:
    k0, k1 = _le(key[:8]), _le(key[8:])
    s = [IV, k0, k1, _le(nonce[:8]), _le(nonce[8:])]  # @line L5
    ascon_p(s, 12)  # @line L6
    s[3] ^= k0
    s[4] ^= k1
    return s, k0, k1


def _absorb_ad(s: list[int], ad: bytes) -> None:
    if ad:  # @line L7
        full = len(ad) // 16 * 16
        blocks = [ad[i:i + 16] for i in range(0, full, 16)] + [_pad(ad[full:])]
        for blk in blocks:
            s[0] ^= _le(blk[:8])
            s[1] ^= _le(blk[8:])
            ascon_p(s, 8)
    s[4] ^= 1 << 63  # @line L8


def _finalize(s: list[int], k0: int, k1: int) -> bytes:
    s[2] ^= k0  # @line L12
    s[3] ^= k1
    ascon_p(s, 12)
    return ((s[3] ^ k0).to_bytes(8, "little") + (s[4] ^ k1).to_bytes(8, "little"))  # @line L13


def ascon_aead128_encrypt(key: bytes, nonce: bytes, ad: bytes, pt: bytes) -> tuple[bytes, bytes]:
    """Return (ciphertext, 128-bit tag).

    Precondition: 16-byte key, 16-byte nonce never repeated under the key.
    Cost: Theta(|ad| + |pt|) word operations (one p[8] per 16 bytes).
    """
    if len(key) != 16 or len(nonce) != 16:
        raise ValueError("Ascon-AEAD128 needs a 16-byte key and a 16-byte nonce")
    s, k0, k1 = _init(key, nonce)
    _absorb_ad(s, ad)
    out = bytearray()
    full = len(pt) // 16 * 16
    for i in range(0, full, 16):  # @line L9
        s[0] ^= _le(pt[i:i + 8])
        s[1] ^= _le(pt[i + 8:i + 16])
        out += s[0].to_bytes(8, "little") + s[1].to_bytes(8, "little")
        ascon_p(s, 8)
    last = _pad(pt[full:])  # @line L10
    s[0] ^= _le(last[:8])
    s[1] ^= _le(last[8:])
    out += (s[0].to_bytes(8, "little") + s[1].to_bytes(8, "little"))[: len(pt) - full]  # @line L11
    return bytes(out), _finalize(s, k0, k1)


def ascon_aead128_decrypt(key: bytes, nonce: bytes, ad: bytes, ct: bytes, tag: bytes) -> bytes | None:
    """Return the plaintext, or None if the tag does not verify.

    Precondition: as for encryption. Cost: Theta(|ad| + |ct|) word operations.
    The tag comparison here is not constant time.
    """
    if len(key) != 16 or len(nonce) != 16:
        raise ValueError("Ascon-AEAD128 needs a 16-byte key and a 16-byte nonce")
    s, k0, k1 = _init(key, nonce)
    _absorb_ad(s, ad)
    out = bytearray()
    full = len(ct) // 16 * 16
    for i in range(0, full, 16):
        c0, c1 = _le(ct[i:i + 8]), _le(ct[i + 8:i + 16])
        out += (s[0] ^ c0).to_bytes(8, "little") + (s[1] ^ c1).to_bytes(8, "little")
        s[0], s[1] = c0, c1
        ascon_p(s, 8)
    ks = s[0].to_bytes(8, "little") + s[1].to_bytes(8, "little")
    p_last = bytes(a ^ b for a, b in zip(ct[full:], ks))
    out += p_last
    padded = _pad(p_last)
    s[0] ^= _le(padded[:8])
    s[1] ^= _le(padded[8:])
    return bytes(out) if _finalize(s, k0, k1) == tag else None  # @line L14
