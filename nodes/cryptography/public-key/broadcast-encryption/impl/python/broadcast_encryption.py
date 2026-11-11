# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/broadcast-encryption/. The authors are listed in prov/FF58G6.jsonl.
#
# The complete subtree (CS) method of Naor, Naor and Lotspiech (Crypto 2001) for broadcast
# encryption to stateless receivers. The n users are the leaves of a complete binary tree; each
# node has a key, and a user holds the keys on its path to the root. To revoke a set R, the
# center covers the other leaves with the subtrees that hang off the Steiner tree of R, and
# wraps the session key under the key of each covering subtree.
# Nodes are numbered as in a heap: the root is 1, the children of v are 2v and 2v + 1, and
# user u (0 <= u < n) sits at leaf n + u.
# For study only. The key wrap and the cipher are toys built from HMAC-SHA256, and the code is
# not constant time. A real system uses AES key wrap (RFC 3394) and an AEAD cipher, as AACS does.

import hashlib
import hmac
import random


def _prf(key: bytes, *parts: bytes) -> bytes:
    h = hmac.new(key, digestmod=hashlib.sha256)
    for part in parts:
        h.update(len(part).to_bytes(4, "big") + part)
    return h.digest()


def _check(n: int) -> None:
    if n < 1 or n & (n - 1):
        raise ValueError("n must be a power of 2")


def path(n: int, u: int):
    """The nodes from the leaf of user u up to the root."""
    _check(n)
    v, out = n + u, []
    while v >= 1:
        out.append(v)
        v //= 2
    return out


def node_key(master: bytes, v: int) -> bytes:
    """The center derives the key of node v from its master secret."""
    return _prf(master, b"cs-node", v.to_bytes(8, "big"))


def user_keys(master: bytes, n: int, u: int):
    """The log2(n) + 1 keys that user u stores."""
    return {v: node_key(master, v) for v in path(n, u)}


def cover(n: int, revoked):
    """The CS cover: the children of Steiner tree nodes that are not in the Steiner tree."""
    _check(n)
    if not revoked:
        return [1]
    steiner = set()
    for u in revoked:
        steiner.update(path(n, u))
    out = []
    for v in sorted(steiner):
        if v < n:  # an inner node
            out.extend(c for c in (2 * v, 2 * v + 1) if c not in steiner)
    return sorted(out)


def leaves_under(n: int, v: int):
    """The users in the subtree of node v."""
    lo = hi = v
    while lo < n:
        lo, hi = 2 * lo, 2 * hi + 1
    return range(lo - n, hi - n + 1)


def _stream(K: bytes, nonce: bytes, length: int) -> bytes:
    out, ctr = b"", 0
    while len(out) < length:
        out += _prf(K, b"enc", nonce, ctr.to_bytes(8, "big"))
        ctr += 1
    return out[:length]


def broadcast(master: bytes, n: int, revoked, message: bytes, rng: random.Random):
    """Return (nonce, header, body, tag): the header wraps a fresh session key K for each cover node."""
    K = bytes(rng.getrandbits(8) for _ in range(32))
    nonce = bytes(rng.getrandbits(8) for _ in range(16))
    header = []
    for v in cover(n, set(revoked)):
        pad = _prf(node_key(master, v), b"wrap", nonce, v.to_bytes(8, "big"))
        header.append((v, bytes(a ^ b for a, b in zip(K, pad))))
    body = bytes(a ^ b for a, b in zip(message, _stream(K, nonce, len(message))))
    tag = _prf(K, b"tag", nonce, body)[:16]
    return nonce, header, body, tag


def receive(keys, ct):
    """Decrypt with the node keys of one user (or the pooled keys of a coalition); None if no key fits."""
    nonce, header, body, tag = ct
    for v, wrapped in header:
        if v in keys:
            pad = _prf(keys[v], b"wrap", nonce, v.to_bytes(8, "big"))
            K = bytes(a ^ b for a, b in zip(wrapped, pad))
            if not hmac.compare_digest(_prf(K, b"tag", nonce, body)[:16], tag):
                return None
            return bytes(a ^ b for a, b in zip(body, _stream(K, nonce, len(body))))
    return None
