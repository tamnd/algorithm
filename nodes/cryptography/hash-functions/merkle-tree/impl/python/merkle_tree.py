# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-tree/. The authors are listed in prov/9FDHGB.jsonl.
"""Merkle hash trees as in RFC 6962, Section 2.1, with SHA-256.

A leaf d is hashed as SHA-256(0x00 || d) and an inner node as
SHA-256(0x01 || left || right). The tree of n leaves splits at k, the largest
power of two below n. The module gives the tree hash, audit paths (inclusion
proofs), consistency proofs, and verifiers for both kinds of proof.

For study only. The code is not constant time and must not protect real data.
Use the Merkle tree code of a maintained transparency log library, such as
transparency-dev/merkle (Go) or the RFC 6962 code of your CT client, instead.
"""

import hashlib


def _h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def leaf_hash(d: bytes) -> bytes:
    return _h(b"\x00" + d)  # @line L2


def node_hash(left: bytes, right: bytes) -> bytes:
    return _h(b"\x01" + left + right)  # @line L3


def split(n: int) -> int:
    """The largest power of two strictly less than n (for n >= 2)."""
    return 1 << ((n - 1).bit_length() - 1)


def mth(leaves: list[bytes]) -> bytes:
    """Merkle Tree Hash MTH(D[n]) of RFC 6962, Section 2.1."""
    n = len(leaves)
    if n == 0:
        return _h(b"")  # @line L1
    if n == 1:
        return leaf_hash(leaves[0])  # @line L2
    k = split(n)
    return node_hash(mth(leaves[:k]), mth(leaves[k:]))  # @line L3


def audit_path(m: int, leaves: list[bytes]) -> list[bytes]:
    """PATH(m, D[n]) of RFC 6962, Section 2.1.1: the inclusion proof of leaf m."""
    n = len(leaves)
    if not 0 <= m < n:
        raise ValueError("leaf index out of range")
    if n == 1:
        return []
    k = split(n)
    if m < k:
        return audit_path(m, leaves[:k]) + [mth(leaves[k:])]  # @line L4
    return audit_path(m - k, leaves[k:]) + [mth(leaves[:k])]  # @line L4


def root_from_path(m: int, n: int, h: bytes, path: list[bytes]) -> bytes:
    """Recompute the root of a tree of size n from leaf m's hash h and its audit path."""
    if n == 1:
        if path:
            raise ValueError("audit path too long")
        return h
    if not path:
        raise ValueError("audit path too short")
    k = split(n)
    sibling, rest = path[-1], path[:-1]
    if m < k:
        return node_hash(root_from_path(m, k, h, rest), sibling)  # @line L5
    return node_hash(sibling, root_from_path(m - k, n - k, h, rest))  # @line L5


def verify_inclusion(m: int, n: int, leaf: bytes, path: list[bytes], root: bytes) -> bool:
    if not 0 <= m < n:
        return False
    try:
        return root_from_path(m, n, leaf_hash(leaf), path) == root  # @line L6
    except ValueError:
        return False


def _subproof(m: int, leaves: list[bytes], b: bool) -> list[bytes]:
    n = len(leaves)
    if m == n:
        return [] if b else [mth(leaves)]
    k = split(n)
    if m <= k:
        return _subproof(m, leaves[:k], b) + [mth(leaves[k:])]  # @line L7
    return _subproof(m - k, leaves[k:], False) + [mth(leaves[:k])]  # @line L7


def consistency_proof(m: int, leaves: list[bytes]) -> list[bytes]:
    """PROOF(m, D[n]) of RFC 6962, Section 2.1.2, for 0 < m < n."""
    if not 0 < m < len(leaves):
        raise ValueError("need 0 < m < n")
    return _subproof(m, leaves, True)


def _check_sub(m: int, n: int, b: bool, proof: list[bytes], old_root: bytes) -> tuple[bytes, bytes]:
    """Return (hash of the first m leaves of this subtree, hash of the subtree) from the proof."""
    if m == n:
        if b:
            if proof:
                raise ValueError("proof too long")
            return old_root, old_root
        if len(proof) != 1:
            raise ValueError("bad proof length")
        return proof[0], proof[0]
    if not proof:
        raise ValueError("proof too short")
    k = split(n)
    sibling, rest = proof[-1], proof[:-1]
    if m <= k:
        old, new = _check_sub(m, k, b, rest, old_root)
        return old, node_hash(new, sibling)  # @line L8
    old, new = _check_sub(m - k, n - k, False, rest, old_root)
    return node_hash(sibling, old), node_hash(sibling, new)  # @line L8


def verify_consistency(m: int, n: int, old_root: bytes, new_root: bytes, proof: list[bytes]) -> bool:
    """Check that the tree of size m with old_root is a prefix of the tree of size n with new_root."""
    if m == n:
        return not proof and old_root == new_root
    if not 0 < m < n:
        return False
    try:
        old, new = _check_sub(m, n, True, proof, old_root)
    except ValueError:
        return False
    return old == old_root and new == new_root  # @line L9


def naive_root(leaves: list[bytes]) -> bytes:
    """A tree with no domain separation: leaves and nodes both hashed as SHA-256(x). Insecure."""
    if len(leaves) == 1:
        return _h(leaves[0])
    k = split(len(leaves))
    return _h(naive_root(leaves[:k]) + naive_root(leaves[k:]))


def bitcoin_style_root(leaves: list[bytes]) -> bytes:
    """Level by level, duplicating the last node of an odd level (as in Bitcoin). Insecure."""
    level = [_h(x) for x in leaves]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [_h(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]
