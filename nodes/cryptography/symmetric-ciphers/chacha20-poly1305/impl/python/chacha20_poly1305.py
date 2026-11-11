# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chacha20-poly1305/. The authors are listed in prov/5G1J5X.jsonl.
"""AEAD_CHACHA20_POLY1305 of RFC 8439, Section 2.8, with its own ChaCha20 and Poly1305.

For study only. Python big integers are not constant time, so the Poly1305 part
leaks timing, and this code must not protect real data. Use the ChaCha20-Poly1305
AEAD of libsodium (crypto_aead_chacha20poly1305_ietf_encrypt) or of a FIPS 140
validated module that offers it, instead.

The XChaCha20-Poly1305 functions at the end follow draft-irtf-cfrg-xchacha-03,
an expired Internet-Draft, not an RFC.
"""

MASK32 = 0xFFFFFFFF
CONSTANTS = (0x61707865, 0x3320646E, 0x79622D32, 0x6B206574)  # "expand 32-byte k"
P1305 = (1 << 130) - 5
FAIL = "FAIL"


def _rotl(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & MASK32


def quarter_round(s: list[int], a: int, b: int, c: int, d: int) -> None:
    """RFC 8439, Section 2.1, on the state words a, b, c, d."""
    s[a] = (s[a] + s[b]) & MASK32
    s[d] = _rotl(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & MASK32
    s[b] = _rotl(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b]) & MASK32
    s[d] = _rotl(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & MASK32
    s[b] = _rotl(s[b] ^ s[c], 7)


def _words(b: bytes) -> list[int]:
    return [int.from_bytes(b[i : i + 4], "little") for i in range(0, len(b), 4)]


def _rounds(state: list[int]) -> list[int]:
    x = list(state)
    for _ in range(10):  # 10 double rounds = 20 rounds
        quarter_round(x, 0, 4, 8, 12)  # column round
        quarter_round(x, 1, 5, 9, 13)
        quarter_round(x, 2, 6, 10, 14)
        quarter_round(x, 3, 7, 11, 15)
        quarter_round(x, 0, 5, 10, 15)  # diagonal round
        quarter_round(x, 1, 6, 11, 12)
        quarter_round(x, 2, 7, 8, 13)
        quarter_round(x, 3, 4, 9, 14)
    return x


def chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
    """RFC 8439, Section 2.3: 64 bytes of key stream for a 32-byte key, a 32-bit counter and a 12-byte nonce."""
    if len(key) != 32 or len(nonce) != 12 or not 0 <= counter <= MASK32:
        raise ValueError("ChaCha20 needs a 32-byte key, a 12-byte nonce and a 32-bit counter")
    state = list(CONSTANTS) + _words(key) + [counter] + _words(nonce)  # @line L1
    x = _rounds(state)  # @line L2
    out = [(a + b) & MASK32 for a, b in zip(x, state)]  # @line L3
    return b"".join(w.to_bytes(4, "little") for w in out)  # @line L4


def chacha20_encrypt(key: bytes, counter: int, nonce: bytes, data: bytes) -> bytes:
    """RFC 8439, Section 2.4: XOR data with the key stream of blocks counter, counter + 1, ..."""
    if counter + (len(data) + 63) // 64 - 1 > MASK32:
        raise ValueError("the 32-bit block counter would wrap")
    out = bytearray()
    for j in range(0, len(data), 64):
        ks = chacha20_block(key, counter + j // 64, nonce)
        out += bytes(x ^ y for x, y in zip(data[j : j + 64], ks))
    return bytes(out)


def poly1305_mac(key: bytes, msg: bytes) -> bytes:
    """RFC 8439, Section 2.5: the 16-byte tag of msg under the one-time key (r, s)."""
    r = int.from_bytes(key[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF
    s = int.from_bytes(key[16:32], "little")
    acc = 0
    for i in range(0, len(msg), 16):
        acc = (acc + int.from_bytes(msg[i : i + 16] + b"\x01", "little")) * r % P1305
    return ((acc + s) % (1 << 128)).to_bytes(16, "little")


def _pad16(x: bytes) -> bytes:
    return bytes(-len(x) % 16)


def mac_data(aad: bytes, c: bytes) -> bytes:
    """AAD || pad16(AAD) || C || pad16(C) || le64(len(AAD)) || le64(len(C))."""
    return aad + _pad16(aad) + c + _pad16(c) + len(aad).to_bytes(8, "little") + len(c).to_bytes(8, "little")


def poly1305_key_gen(key: bytes, nonce: bytes) -> bytes:
    """RFC 8439, Section 2.6: the first 32 bytes of ChaCha20 block 0."""
    return chacha20_block(key, 0, nonce)[:32]


def tags_equal(a: bytes, b: bytes) -> bool:
    """Read every byte and fold the differences with OR: no early exit."""
    d = len(a) ^ len(b)
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def aead_encrypt(key: bytes, nonce: bytes, aad: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    """RFC 8439, Section 2.8. Returns (ciphertext, 16-byte tag)."""
    otk = poly1305_key_gen(key, nonce)  # @line L5
    c = chacha20_encrypt(key, 1, nonce, plaintext)  # @line L6
    m = mac_data(aad, c)  # @line L7
    tag = poly1305_mac(otk, m)  # @line L8
    return c, tag  # @line L9


def aead_decrypt(key: bytes, nonce: bytes, aad: bytes, c: bytes, tag: bytes) -> bytes | str:
    """RFC 8439, Section 2.8: the tag is checked on the ciphertext before decryption."""
    otk = poly1305_key_gen(key, nonce)  # @line L10
    expected = poly1305_mac(otk, mac_data(aad, c))  # @line L11
    if not tags_equal(expected, tag):  # @line L12
        return FAIL
    return chacha20_encrypt(key, 1, nonce, c)  # @line L13


# ---- XChaCha20-Poly1305, draft-irtf-cfrg-xchacha-03 (an expired draft, not an RFC). ----


def hchacha20(key: bytes, nonce16: bytes) -> bytes:
    """Section 2.2: the ChaCha20 rounds on (constants, key, 16-byte nonce), no final addition,
    and output words 0 to 3 and 12 to 15."""
    if len(key) != 32 or len(nonce16) != 16:
        raise ValueError("HChaCha20 needs a 32-byte key and a 16-byte nonce")
    x = _rounds(list(CONSTANTS) + _words(key) + _words(nonce16))
    return b"".join(w.to_bytes(4, "little") for w in x[0:4] + x[12:16])


def xchacha20_poly1305_encrypt(key: bytes, nonce24: bytes, aad: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    """A 24-byte nonce: a subkey from HChaCha20 on the first 16 bytes, then the RFC 8439 AEAD
    with the nonce 0x00000000 || the last 8 bytes."""
    if len(nonce24) != 24:
        raise ValueError("XChaCha20 needs a 24-byte nonce")
    return aead_encrypt(hchacha20(key, nonce24[:16]), bytes(4) + nonce24[16:], aad, plaintext)


def xchacha20_poly1305_decrypt(key: bytes, nonce24: bytes, aad: bytes, c: bytes, tag: bytes) -> bytes | str:
    if len(nonce24) != 24:
        raise ValueError("XChaCha20 needs a 24-byte nonce")
    return aead_decrypt(hchacha20(key, nonce24[:16]), bytes(4) + nonce24[16:], aad, c, tag)
