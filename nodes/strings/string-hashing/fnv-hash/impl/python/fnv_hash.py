# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fnv-hash/. The authors are listed in prov/GWRZNB.jsonl.

# FNV primes and offset bases for 32 and 64 bits (RFC 9923, Section 5).
PRIME = {32: 16777619, 64: 1099511628211}
OFFSET = {32: 2166136261, 64: 14695981039346656037}


def _bytes(data: bytes | str) -> bytes:
    return data.encode("utf-8") if isinstance(data, str) else bytes(data)


def fnv1a(data: bytes | str, bits: int = 32, offset: int | None = None) -> int:
    """FNV-1a hash of a byte string (str is encoded as UTF-8): XOR the byte, then multiply."""
    prime, mask = PRIME[bits], (1 << bits) - 1
    b = _bytes(data)
    h = OFFSET[bits] if offset is None else offset & mask  # @line L1
    for i in range(len(b)):  # @line L2
        h ^= b[i]  # @line L3
        h = (h * prime) & mask  # @line L4
    return h  # @line L5


def fnv1(data: bytes | str, bits: int = 32, offset: int | None = None) -> int:
    """FNV-1 hash: the same steps as FNV-1a in the other order (multiply, then XOR)."""
    prime, mask = PRIME[bits], (1 << bits) - 1
    h = OFFSET[bits] if offset is None else offset & mask
    for byte in _bytes(data):
        h = ((h * prime) & mask) ^ byte
    return h


def xor_fold(h: int, k: int) -> int:
    """Reduce a hash to k bits by XOR folding, as RFC 9923 recommends: (h XOR (h >> k)) mod 2^k."""
    return (h ^ (h >> k)) & ((1 << k) - 1)
