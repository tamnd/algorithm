# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xmss/. The authors are listed in prov/CAW1KT.jsonl.
"""XMSS following the algorithms of RFC 8391, with SHA-256 and n = 32.

The hash functions, the address structure, WOTS+ with w = 16, the L-tree,
the randomized tree hash and the message hash follow RFC 8391 (Sections 2
to 4), as for the parameter set XMSS-SHA2_h_256. The tree height h is a
parameter: the tests use h = 4 and h = 5, which are NOT standard parameter
sets (RFC 8391 defines h = 10, 16 and 20).

RFC 8391 leaves the generation of the WOTS+ secret values to the
implementation; here they come from SK_SEED with the PRF and the address.
The RFC text has no test vectors, so this code is checked only by round
trips and is not tested for byte compatibility with other implementations.

The page is about the signature, not the hash, so SHA-256 comes from hashlib.
For study only. The code is not constant time and it must not protect real
data. XMSS is stateful: the index must never repeat. For real use take XMSS
from a FIPS 140 validated module (NIST SP 800-208).
"""

import hashlib
import secrets
import struct

N = 32
W = 16
LEN1, LEN2 = 64, 3
LEN = LEN1 + LEN2


def to_byte(x: int, k: int) -> bytes:
    return x.to_bytes(k, "big")


def _h(prefix: int, key: bytes, m: bytes) -> bytes:
    return hashlib.sha256(to_byte(prefix, N) + key + m).digest()


def F(key: bytes, m: bytes) -> bytes:
    return _h(0, key, m)


def H(key: bytes, m: bytes) -> bytes:
    return _h(1, key, m)


def H_msg(key: bytes, m: bytes) -> bytes:
    return _h(2, key, m)


def PRF(key: bytes, m: bytes) -> bytes:
    return _h(3, key, m)


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


class Adrs:
    """The 32-byte address: eight 32-bit words (RFC 8391, Section 2.5)."""

    def __init__(self) -> None:
        self.w = [0] * 8

    def copy(self) -> "Adrs":
        a = Adrs()
        a.w = list(self.w)
        return a

    def set_type(self, t: int) -> None:
        self.w[3] = t
        self.w[4:8] = [0, 0, 0, 0]

    def set_ots(self, i: int) -> None:  # also the L-tree address (word 4)
        self.w[4] = i

    def set_chain(self, i: int) -> None:  # also the tree height (word 5)
        self.w[5] = i

    def set_hash(self, i: int) -> None:  # also the tree index (word 6)
        self.w[6] = i

    def set_key_and_mask(self, i: int) -> None:
        self.w[7] = i

    def bytes(self) -> bytes:
        return struct.pack(">8I", *self.w)


# ------------------------------------------------------------------- WOTS+


def chain(x: bytes, start: int, steps: int, seed: bytes, adrs: Adrs) -> bytes:
    for j in range(start, start + steps):
        adrs.set_hash(j)
        adrs.set_key_and_mask(0)
        key = PRF(seed, adrs.bytes())
        adrs.set_key_and_mask(1)
        bm = PRF(seed, adrs.bytes())
        x = F(key, xor(x, bm))
    return x


def base_w(data: bytes, out_len: int) -> list[int]:
    out = []
    for byte in data:
        out += [byte >> 4, byte & 15]
    return out[:out_len]


def wots_digits(msg: bytes) -> list[int]:
    d = base_w(msg, LEN1)
    csum = sum(W - 1 - x for x in d)
    csum <<= 8 - ((LEN2 * 4) % 8)  # = 4 for w = 16
    return d + base_w(to_byte(csum, 2), LEN2)


def wots_sk(sk_seed: bytes, adrs: Adrs, i: int) -> bytes:
    a = adrs.copy()
    a.set_chain(i)
    a.set_hash(0)
    a.set_key_and_mask(0)
    return PRF(sk_seed, a.bytes())


def wots_pk(sk_seed: bytes, seed: bytes, adrs: Adrs) -> list[bytes]:
    out = []
    for i in range(LEN):
        adrs.set_chain(i)
        out.append(chain(wots_sk(sk_seed, adrs, i), 0, W - 1, seed, adrs))
    return out


def wots_sign(msg: bytes, sk_seed: bytes, seed: bytes, adrs: Adrs) -> list[bytes]:
    b = wots_digits(msg)
    out = []
    for i in range(LEN):
        adrs.set_chain(i)
        out.append(chain(wots_sk(sk_seed, adrs, i), 0, b[i], seed, adrs))
    return out


def wots_pk_from_sig(sig: list[bytes], msg: bytes, seed: bytes, adrs: Adrs) -> list[bytes]:
    b = wots_digits(msg)
    out = []
    for i in range(LEN):
        adrs.set_chain(i)
        out.append(chain(sig[i], b[i], W - 1 - b[i], seed, adrs))
    return out


# --------------------------------------------------------- trees and XMSS


def rand_hash(left: bytes, right: bytes, seed: bytes, adrs: Adrs) -> bytes:
    adrs.set_key_and_mask(0)
    key = PRF(seed, adrs.bytes())  # @line L1
    adrs.set_key_and_mask(1)
    bm0 = PRF(seed, adrs.bytes())
    adrs.set_key_and_mask(2)
    bm1 = PRF(seed, adrs.bytes())
    return H(key, xor(left, bm0) + xor(right, bm1))  # @line L2


def ltree(pk: list[bytes], seed: bytes, adrs: Adrs) -> bytes:
    """Compress the len WOTS+ public values to one n-byte value."""
    pk = list(pk)
    length = len(pk)
    height = 0
    while length > 1:  # @line L3
        adrs.set_chain(height)  # tree height
        for i in range(length // 2):
            adrs.set_hash(i)  # tree index
            pk[i] = rand_hash(pk[2 * i], pk[2 * i + 1], seed, adrs)
        if length % 2 == 1:
            pk[length // 2] = pk[length - 1]
        length = (length + 1) // 2
        height += 1
    return pk[0]  # @line L4


def leaf(sk_seed: bytes, seed: bytes, idx: int) -> bytes:
    a = Adrs()
    a.set_type(0)
    a.set_ots(idx)
    pk = wots_pk(sk_seed, seed, a)
    a.set_type(1)
    a.set_ots(idx)  # L-tree address
    return ltree(pk, seed, a)


def node_adrs(height: int, index: int) -> Adrs:
    a = Adrs()
    a.set_type(2)
    a.set_chain(height)  # tree height of the children
    a.set_hash(index)  # tree index of the parent
    return a


class XmssSigner:
    """XMSS with tree height h. The index idx is the state."""

    def __init__(self, h: int, sk_seed: bytes | None = None, sk_prf: bytes | None = None, pub_seed: bytes | None = None) -> None:
        self.h = h
        self.sk_seed = sk_seed or secrets.token_bytes(N)
        self.sk_prf = sk_prf or secrets.token_bytes(N)
        self.seed = pub_seed or secrets.token_bytes(N)
        level = [leaf(self.sk_seed, self.seed, i) for i in range(1 << h)]
        self.tree = [level]
        for j in range(h):
            level = [
                rand_hash(level[2 * k], level[2 * k + 1], self.seed, node_adrs(j, k))
                for k in range(len(level) // 2)
            ]
            self.tree.append(level)
        self.root = self.tree[h][0]
        self.idx = 0

    def public_key(self) -> tuple[bytes, bytes]:
        return self.root, self.seed

    def sign(self, message: bytes) -> tuple[int, bytes, list[bytes], list[bytes]]:
        idx = self.idx  # @line L5
        if idx >= 1 << self.h:
            raise RuntimeError("all one-time keys are used")
        self.idx = idx + 1
        r = PRF(self.sk_prf, to_byte(idx, 32))  # @line L6
        m2 = H_msg(r + self.root + to_byte(idx, N), message)  # @line L7
        a = Adrs()
        a.set_type(0)
        a.set_ots(idx)
        sig_ots = wots_sign(m2, self.sk_seed, self.seed, a)  # @line L8
        auth = [self.tree[j][(idx >> j) ^ 1] for j in range(self.h)]
        return idx, r, sig_ots, auth  # @line L9


def root_from_sig(idx: int, sig_ots: list[bytes], auth: list[bytes], m2: bytes, seed: bytes) -> bytes:
    a = Adrs()
    a.set_type(0)
    a.set_ots(idx)
    pk = wots_pk_from_sig(sig_ots, m2, seed, a)
    a.set_type(1)
    a.set_ots(idx)
    node = ltree(pk, seed, a)  # @line L11
    for k in range(len(auth)):  # @line L12
        parent_index = idx >> (k + 1)
        if (idx >> k) & 1 == 0:
            node = rand_hash(node, auth[k], seed, node_adrs(k, parent_index))
        else:
            node = rand_hash(auth[k], node, seed, node_adrs(k, parent_index))
    return node


def verify(pk: tuple[bytes, bytes], h: int, message: bytes, sig: tuple[int, bytes, list[bytes], list[bytes]]) -> bool:
    root, seed = pk
    idx, r, sig_ots, auth = sig
    if not 0 <= idx < 1 << h or len(auth) != h or len(sig_ots) != LEN:
        return False
    m2 = H_msg(r + root + to_byte(idx, N), message)  # @line L10
    return root_from_sig(idx, sig_ots, auth, m2, seed) == root  # @line L13


def signature_bytes(sig: tuple[int, bytes, list[bytes], list[bytes]]) -> bytes:
    """The RFC 8391 encoding: idx (4 bytes) || r || WOTS+ signature || auth."""
    idx, r, sig_ots, auth = sig
    return to_byte(idx, 4) + r + b"".join(sig_ots) + b"".join(auth)
