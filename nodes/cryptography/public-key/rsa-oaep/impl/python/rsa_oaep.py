# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-oaep/. The authors are listed in prov/60YSZW.jsonl.
"""RSAES-OAEP encryption, with MGF1 and a hash of your choice.

Every step follows RFC 8017 (PKCS #1 v2.2): MGF1 is Appendix B.2.1, the
encoding is Section 7.1.1 and the decoding is Section 7.1.2. The test file
checks the code against Example 1.1 of the official PKCS #1 v2.1 test vector
file oaep-vect.txt, which uses SHA-1.

For study only. This code is not constant time, it has no blinding, and it
must not be used to protect real data. Use a FIPS 140 validated module. In
particular the decoding here raises one exception for every failure, but it
does not hide the failure reason from a timing observer.
"""

import hashlib
import secrets


class DecryptionError(Exception):
    """One error for every failure, as RFC 8017 Section 7.1.2 asks."""


def i2osp(value: int, length: int) -> bytes:
    """Integer to octet string, RFC 8017 Section 4.1."""
    if value < 0 or value >= 1 << (8 * length):
        raise ValueError("integer too large")
    return value.to_bytes(length, "big")


def os2ip(data: bytes) -> int:
    """Octet string to integer, RFC 8017 Section 4.2."""
    return int.from_bytes(data, "big")


def modulus_length(n: int) -> int:
    """The length k of the modulus in octets."""
    return (n.bit_length() + 7) // 8


def xor_bytes(left: bytes, right: bytes) -> bytes:
    """The octet by octet exclusive or of two strings of the same length."""
    if len(left) != len(right):
        raise ValueError("lengths differ")
    return bytes(a ^ b for a, b in zip(left, right))


def mgf1(seed: bytes, length: int, hash_name: str = "sha1") -> bytes:
    """The mask generation function MGF1 of RFC 8017 Appendix B.2.1."""
    h_len = hashlib.new(hash_name).digest_size
    if length > (1 << 32) * h_len:
        raise ValueError("mask too long")
    out = bytearray()  # @line L1
    counter = 0
    while len(out) < length:  # @line L2
        out.extend(hashlib.new(hash_name, seed + i2osp(counter, 4)).digest())
        counter += 1
    return bytes(out[:length])  # @line L3


def eme_oaep_encode(
    message: bytes,
    k: int,
    label: bytes = b"",
    hash_name: str = "sha1",
    seed: bytes = None,
) -> bytes:
    """EM = 0x00 || maskedSeed || maskedDB, RFC 8017 Section 7.1.1 step 2."""
    h_len = hashlib.new(hash_name).digest_size
    if k < 2 * h_len + 2:
        raise ValueError("modulus too short for this hash")
    if len(message) > k - 2 * h_len - 2:  # @line L4
        raise ValueError("message too long")
    l_hash = hashlib.new(hash_name, label).digest()  # @line L5
    ps = bytes(k - len(message) - 2 * h_len - 2)
    db = l_hash + ps + b"\x01" + message  # @line L6
    if seed is None:  # @line L7
        seed = secrets.token_bytes(h_len)
    if len(seed) != h_len:
        raise ValueError("the seed must have hLen octets")
    db_mask = mgf1(seed, k - h_len - 1, hash_name)
    masked_db = xor_bytes(db, db_mask)  # @line L8
    seed_mask = mgf1(masked_db, h_len, hash_name)
    masked_seed = xor_bytes(seed, seed_mask)  # @line L9
    return b"\x00" + masked_seed + masked_db  # @line L10


def eme_oaep_decode(em: bytes, label: bytes = b"", hash_name: str = "sha1") -> bytes:
    """Undo the encoding, or raise DecryptionError. RFC 8017 Section 7.1.2 step 3."""
    h_len = hashlib.new(hash_name).digest_size
    k = len(em)
    if k < 2 * h_len + 2:
        raise DecryptionError("decryption error")
    l_hash = hashlib.new(hash_name, label).digest()
    y, masked_seed, masked_db = em[0], em[1:1 + h_len], em[1 + h_len:]  # @line L13
    seed = xor_bytes(masked_seed, mgf1(masked_db, h_len, hash_name))  # @line L14
    db = xor_bytes(masked_db, mgf1(seed, k - h_len - 1, hash_name))  # @line L15
    l_hash_seen, rest = db[:h_len], db[h_len:]  # @line L16
    index = 0
    while index < len(rest) and rest[index] == 0:
        index += 1
    bad = y != 0
    bad |= l_hash_seen != l_hash
    bad |= index == len(rest) or rest[index] != 1
    if bad:  # @line L17
        raise DecryptionError("decryption error")
    return rest[index + 1:]  # @line L18


def encrypt(
    n: int,
    e: int,
    message: bytes,
    label: bytes = b"",
    hash_name: str = "sha1",
    seed: bytes = None,
) -> bytes:
    """RSAES-OAEP-ENCRYPT, RFC 8017 Section 7.1.1."""
    k = modulus_length(n)
    em = eme_oaep_encode(message, k, label, hash_name, seed)  # @line L11
    return i2osp(pow(os2ip(em), e, n), k)


def decrypt(
    n: int,
    d: int,
    ciphertext: bytes,
    label: bytes = b"",
    hash_name: str = "sha1",
) -> bytes:
    """RSAES-OAEP-DECRYPT, RFC 8017 Section 7.1.2."""
    k = modulus_length(n)
    h_len = hashlib.new(hash_name).digest_size
    if len(ciphertext) != k or k < 2 * h_len + 2:  # @line L12
        raise DecryptionError("decryption error")
    c = os2ip(ciphertext)
    if c >= n:
        raise DecryptionError("decryption error")
    em = i2osp(pow(c, d, n), k)
    return eme_oaep_decode(em, label, hash_name)


def max_message_length(n: int, hash_name: str = "sha1") -> int:
    """k - 2hLen - 2, the longest message this key and hash can carry."""
    return modulus_length(n) - 2 * hashlib.new(hash_name).digest_size - 2
