# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rc4/. The authors are listed in prov/F9NPHX.jsonl.

"""RC4 (ARC4), for study only.

RC4 is broken. RFC 7465 prohibits it in TLS. This code is not constant time
and must not protect real data. Use an AEAD such as ChaCha20-Poly1305 or
AES-GCM from libsodium, OpenSSL or a FIPS 140 validated module instead.
"""


def rc4_ksa(key: bytes) -> list[int]:
    """Return the state S after the key-scheduling algorithm (KSA).

    Precondition: 1 <= len(key) <= 256.
    Cost: 256 swaps, so Theta(256) byte operations for any key length.
    """
    if not 1 <= len(key) <= 256:
        raise ValueError("RC4 needs a key of 1 to 256 bytes")
    s = list(range(256))  # @line L1
    j = 0  # @line L2
    for i in range(256):  # @line L3
        j = (j + s[i] + key[i % len(key)]) & 0xFF  # @line L4
        s[i], s[j] = s[j], s[i]  # @line L5
    return s


def rc4_keystream(key: bytes, m: int) -> bytes:
    """Return the first m bytes of the RC4 keystream for this key.

    Precondition: 1 <= len(key) <= 256 and m >= 0.
    Cost: the KSA plus Theta(m) byte operations (PRGA).
    """
    s = rc4_ksa(key)
    out = bytearray()
    i = j = 0  # @line L6
    for _ in range(m):  # @line L7
        i = (i + 1) & 0xFF  # @line L8
        j = (j + s[i]) & 0xFF  # @line L9
        s[i], s[j] = s[j], s[i]  # @line L10
        out.append(s[(s[i] + s[j]) & 0xFF])  # @line L11
    return bytes(out)


def rc4_crypt(key: bytes, data: bytes) -> bytes:
    """Encrypt or decrypt data: XOR it with the RC4 keystream.

    Precondition: 1 <= len(key) <= 256.
    Cost: Theta(len(data)) byte operations after the KSA.
    """
    ks = rc4_keystream(key, len(data))
    return bytes(a ^ b for a, b in zip(data, ks))
