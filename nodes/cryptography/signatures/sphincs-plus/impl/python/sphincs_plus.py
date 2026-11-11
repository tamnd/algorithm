# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sphincs-plus/. The authors are listed in prov/XRB4YB.jsonl.
"""SLH-DSA-SHAKE-128f, the FIPS 205 form of SPHINCS+.

The functions follow the algorithms of FIPS 205 (August 2024): WOTS+
(Algorithms 5 to 8), XMSS (9 to 11), the hypertree (12 and 13), FORS
(14 to 17), the internal functions (18 to 20) and pure signing and
verification with a context string (22 and 24). Only the parameter set
SLH-DSA-SHAKE-128f is implemented: n = 16, h = 66, d = 22, h' = 3, a = 6,
k = 33, lg w = 4, m = 34. The hash functions are SHAKE256 (FIPS 205,
Section 11.1) from hashlib; the page is about the signature, not the hash.

For study only. The code is not constant time and it must not protect real
data. For real use take SLH-DSA from a FIPS 140 validated module.
"""

import hashlib
import secrets

N, H, D, HP, A, K, LG_W, M = 16, 66, 22, 3, 6, 33, 4, 34
W = 1 << LG_W
LEN1 = (8 * N + LG_W - 1) // LG_W  # 32
LEN2 = 3  # gen_len2(16, 4), FIPS 205 Algorithm 1
LEN = LEN1 + LEN2  # 35
SIG_BYTES = (1 + K * (1 + A) + H + D * LEN) * N  # 17088

WOTS_HASH, WOTS_PK, TREE, FORS_TREE, FORS_ROOTS, WOTS_PRF, FORS_PRF = range(7)


def shake(data: bytes, out: int = N) -> bytes:
    return hashlib.shake_256(data).digest(out)


class Adrs:
    """The 32-byte address of FIPS 205, Section 4.2 and Table 1."""

    def __init__(self) -> None:
        self.a = bytearray(32)

    def copy(self) -> "Adrs":
        c = Adrs()
        c.a = bytearray(self.a)
        return c

    def _put(self, at: int, value: int, size: int = 4) -> None:
        self.a[at : at + size] = value.to_bytes(size, "big")

    def set_layer(self, x: int) -> None:
        self._put(0, x)

    def set_tree(self, x: int) -> None:
        self._put(4, x, 12)

    def set_type_and_clear(self, y: int) -> None:
        self._put(16, y)
        self.a[20:32] = bytes(12)

    def set_key_pair(self, x: int) -> None:
        self._put(20, x)

    def set_chain(self, x: int) -> None:  # also the tree height
        self._put(24, x)

    def set_hash(self, x: int) -> None:  # also the tree index
        self._put(28, x)

    def key_pair(self) -> int:
        return int.from_bytes(self.a[20:24], "big")

    def tree_index(self) -> int:
        return int.from_bytes(self.a[28:32], "big")


# The six functions of FIPS 205, Section 11.1 (T_l, H and F share one form).
def F(pk_seed: bytes, adrs: Adrs, m: bytes) -> bytes:
    return shake(pk_seed + bytes(adrs.a) + m)


def PRF(pk_seed: bytes, sk_seed: bytes, adrs: Adrs) -> bytes:
    return shake(pk_seed + bytes(adrs.a) + sk_seed)


def PRF_msg(sk_prf: bytes, opt_rand: bytes, msg: bytes) -> bytes:
    return shake(sk_prf + opt_rand + msg)


def H_msg(r: bytes, pk_seed: bytes, pk_root: bytes, msg: bytes) -> bytes:
    return shake(r + pk_seed + pk_root + msg, M)


def base_2b(x: bytes, b: int, out_len: int) -> list[int]:
    """FIPS 205 Algorithm 4: the first out_len * b bits of x, b bits each."""
    i = bits = total = 0
    out = []
    for _ in range(out_len):
        while bits < b:
            total = (total << 8) + x[i]
            i += 1
            bits += 8
        bits -= b
        out.append((total >> bits) % (1 << b))
    return out


# ------------------------------------------------------------------- WOTS+


def chain(x: bytes, i: int, s: int, pk_seed: bytes, adrs: Adrs) -> bytes:
    for j in range(i, i + s):
        adrs.set_hash(j)
        x = F(pk_seed, adrs, x)
    return x


def wots_digits(msg: bytes) -> list[int]:
    d = base_2b(msg, LG_W, LEN1)
    csum = sum(W - 1 - x for x in d)
    csum <<= (8 - (LEN2 * LG_W) % 8) % 8
    return d + base_2b(csum.to_bytes((LEN2 * LG_W + 7) // 8, "big"), LG_W, LEN2)


def _wots_secret(sk_seed: bytes, pk_seed: bytes, adrs: Adrs, i: int) -> bytes:
    sk_adrs = adrs.copy()
    sk_adrs.set_type_and_clear(WOTS_PRF)
    sk_adrs.set_key_pair(adrs.key_pair())
    sk_adrs.set_chain(i)
    return PRF(pk_seed, sk_seed, sk_adrs)


def _wots_compress(tmp: list[bytes], pk_seed: bytes, adrs: Adrs) -> bytes:
    pk_adrs = adrs.copy()
    pk_adrs.set_type_and_clear(WOTS_PK)
    pk_adrs.set_key_pair(adrs.key_pair())
    return F(pk_seed, pk_adrs, b"".join(tmp))  # T_len


def wots_pk_gen(sk_seed: bytes, pk_seed: bytes, adrs: Adrs) -> bytes:
    tmp = []
    for i in range(LEN):
        sk = _wots_secret(sk_seed, pk_seed, adrs, i)
        adrs.set_chain(i)
        tmp.append(chain(sk, 0, W - 1, pk_seed, adrs))
    return _wots_compress(tmp, pk_seed, adrs)


def wots_sign(msg: bytes, sk_seed: bytes, pk_seed: bytes, adrs: Adrs) -> list[bytes]:
    d = wots_digits(msg)
    sig = []
    for i in range(LEN):
        sk = _wots_secret(sk_seed, pk_seed, adrs, i)
        adrs.set_chain(i)
        sig.append(chain(sk, 0, d[i], pk_seed, adrs))
    return sig


def wots_pk_from_sig(sig: list[bytes], msg: bytes, pk_seed: bytes, adrs: Adrs) -> bytes:
    d = wots_digits(msg)
    tmp = []
    for i in range(LEN):
        adrs.set_chain(i)
        tmp.append(chain(sig[i], d[i], W - 1 - d[i], pk_seed, adrs))
    return _wots_compress(tmp, pk_seed, adrs)


# -------------------------------------------------------------------- XMSS


def xmss_node(sk_seed: bytes, i: int, z: int, pk_seed: bytes, adrs: Adrs) -> bytes:
    if z == 0:
        adrs.set_type_and_clear(WOTS_HASH)
        adrs.set_key_pair(i)
        return wots_pk_gen(sk_seed, pk_seed, adrs)
    left = xmss_node(sk_seed, 2 * i, z - 1, pk_seed, adrs)
    right = xmss_node(sk_seed, 2 * i + 1, z - 1, pk_seed, adrs)
    adrs.set_type_and_clear(TREE)
    adrs.set_chain(z)
    adrs.set_hash(i)
    return F(pk_seed, adrs, left + right)  # H


def xmss_sign(msg: bytes, sk_seed: bytes, idx: int, pk_seed: bytes, adrs: Adrs) -> list[bytes]:
    auth = [xmss_node(sk_seed, (idx >> j) ^ 1, j, pk_seed, adrs) for j in range(HP)]
    adrs.set_type_and_clear(WOTS_HASH)
    adrs.set_key_pair(idx)
    return wots_sign(msg, sk_seed, pk_seed, adrs) + auth


def _climb(node: bytes, index: int, auth: list[bytes], pk_seed: bytes, adrs: Adrs) -> bytes:
    """Lines 6 to 18 of Algorithm 11 and lines 8 to 18 of Algorithm 17."""
    for k, sibling in enumerate(auth):
        adrs.set_chain(k + 1)
        if (index >> k) % 2 == 0:
            adrs.set_hash(adrs.tree_index() // 2)
            node = F(pk_seed, adrs, node + sibling)
        else:
            adrs.set_hash((adrs.tree_index() - 1) // 2)
            node = F(pk_seed, adrs, sibling + node)
    return node


def xmss_pk_from_sig(idx: int, sig: list[bytes], msg: bytes, pk_seed: bytes, adrs: Adrs) -> bytes:
    adrs.set_type_and_clear(WOTS_HASH)
    adrs.set_key_pair(idx)
    node = wots_pk_from_sig(sig[:LEN], msg, pk_seed, adrs)
    adrs.set_type_and_clear(TREE)
    adrs.set_hash(idx)
    return _climb(node, idx, sig[LEN:], pk_seed, adrs)


# --------------------------------------------------------------- hypertree


def ht_sign(msg: bytes, sk_seed: bytes, pk_seed: bytes, idx_tree: int, idx_leaf: int) -> list[bytes]:
    out = []
    root = msg
    for j in range(D):
        adrs = Adrs()
        adrs.set_layer(j)
        adrs.set_tree(idx_tree)
        sig = xmss_sign(root, sk_seed, idx_leaf, pk_seed, adrs)  # @line L10
        out += sig
        if j < D - 1:
            root = xmss_pk_from_sig(idx_leaf, sig, root, pk_seed, adrs)  # @line L11
            idx_leaf = idx_tree % (1 << HP)
            idx_tree >>= HP
    return out


def ht_verify(msg: bytes, sig: list[bytes], pk_seed: bytes, idx_tree: int, idx_leaf: int, pk_root: bytes) -> bool:
    node = msg
    step = LEN + HP
    for j in range(D):  # @line L14
        adrs = Adrs()
        adrs.set_layer(j)
        adrs.set_tree(idx_tree)
        node = xmss_pk_from_sig(idx_leaf, sig[j * step : (j + 1) * step], node, pk_seed, adrs)
        idx_leaf = idx_tree % (1 << HP)
        idx_tree >>= HP
    return node == pk_root  # @line L15


# -------------------------------------------------------------------- FORS


def fors_sk_gen(sk_seed: bytes, pk_seed: bytes, adrs: Adrs, idx: int) -> bytes:
    sk_adrs = adrs.copy()
    sk_adrs.set_type_and_clear(FORS_PRF)
    sk_adrs.set_key_pair(adrs.key_pair())
    sk_adrs.set_hash(idx)
    return PRF(pk_seed, sk_seed, sk_adrs)


def fors_node(sk_seed: bytes, i: int, z: int, pk_seed: bytes, adrs: Adrs) -> bytes:
    if z == 0:
        sk = fors_sk_gen(sk_seed, pk_seed, adrs, i)
        adrs.set_chain(0)
        adrs.set_hash(i)
        return F(pk_seed, adrs, sk)
    left = fors_node(sk_seed, 2 * i, z - 1, pk_seed, adrs)
    right = fors_node(sk_seed, 2 * i + 1, z - 1, pk_seed, adrs)
    adrs.set_chain(z)
    adrs.set_hash(i)
    return F(pk_seed, adrs, left + right)


def fors_sign(md: bytes, sk_seed: bytes, pk_seed: bytes, adrs: Adrs) -> list[bytes]:
    out = []
    for i, index in enumerate(base_2b(md, A, K)):  # @line L9
        out.append(fors_sk_gen(sk_seed, pk_seed, adrs, (i << A) + index))
        for j in range(A):
            s = (index >> j) ^ 1
            out.append(fors_node(sk_seed, (i << (A - j)) + s, j, pk_seed, adrs))
    return out


def fors_pk_from_sig(sig: list[bytes], md: bytes, pk_seed: bytes, adrs: Adrs) -> bytes:
    roots = []
    for i, index in enumerate(base_2b(md, A, K)):
        part = sig[i * (A + 1) : (i + 1) * (A + 1)]
        adrs.set_chain(0)
        adrs.set_hash((i << A) + index)
        node = F(pk_seed, adrs, part[0])
        roots.append(_climb(node, index, part[1:], pk_seed, adrs))
    pk_adrs = adrs.copy()
    pk_adrs.set_type_and_clear(FORS_ROOTS)
    pk_adrs.set_key_pair(adrs.key_pair())
    return F(pk_seed, pk_adrs, b"".join(roots))  # T_k


# ---------------------------------------------------------------- SLH-DSA


def keygen_internal(sk_seed: bytes, sk_prf: bytes, pk_seed: bytes) -> tuple[bytes, bytes]:
    """FIPS 205 Algorithm 18. Returns SK (4n bytes) and PK (2n bytes)."""
    adrs = Adrs()
    adrs.set_layer(D - 1)
    pk_root = xmss_node(sk_seed, 0, HP, pk_seed, adrs)
    return sk_seed + sk_prf + pk_seed + pk_root, pk_seed + pk_root


def keygen() -> tuple[bytes, bytes]:
    return keygen_internal(secrets.token_bytes(N), secrets.token_bytes(N), secrets.token_bytes(N))


def split_digest(digest: bytes) -> tuple[bytes, int, int]:
    """Lines 6 to 10 of Algorithm 19: md, idx_tree and idx_leaf."""
    a = (K * A + 7) // 8
    b = (H - HP + 7) // 8
    c = (HP + 7) // 8
    md = digest[:a]
    idx_tree = int.from_bytes(digest[a : a + b], "big") % (1 << (H - HP))
    idx_leaf = int.from_bytes(digest[a + b : a + b + c], "big") % (1 << HP)
    return md, idx_tree, idx_leaf


def _fors_adrs(idx_tree: int, idx_leaf: int) -> Adrs:
    adrs = Adrs()
    adrs.set_tree(idx_tree)
    adrs.set_type_and_clear(FORS_TREE)
    adrs.set_key_pair(idx_leaf)
    return adrs


def sign_internal(msg: bytes, sk: bytes, addrnd: bytes | None = None) -> bytes:
    """FIPS 205 Algorithm 19; addrnd = None gives the deterministic variant."""
    sk_seed, sk_prf, pk_seed, pk_root = (sk[i : i + N] for i in range(0, 4 * N, N))
    opt_rand = pk_seed if addrnd is None else addrnd
    r = PRF_msg(sk_prf, opt_rand, msg)  # @line L2
    digest = H_msg(r, pk_seed, pk_root, msg)  # @line L3
    md, idx_tree, idx_leaf = split_digest(digest)  # @line L4
    adrs = _fors_adrs(idx_tree, idx_leaf)
    sig_fors = fors_sign(md, sk_seed, pk_seed, adrs)  # @line L5
    pk_fors = fors_pk_from_sig(sig_fors, md, pk_seed, adrs)  # @line L6
    sig_ht = ht_sign(pk_fors, sk_seed, pk_seed, idx_tree, idx_leaf)  # @line L7
    return r + b"".join(sig_fors) + b"".join(sig_ht)  # @line L8


def verify_internal(msg: bytes, sig: bytes, pk: bytes) -> bool:
    """FIPS 205 Algorithm 20."""
    if len(sig) != SIG_BYTES or len(pk) != 2 * N:  # @line L12
        return False
    pk_seed, pk_root = pk[:N], pk[N:]
    parts = [sig[i : i + N] for i in range(0, len(sig), N)]
    r, sig_fors, sig_ht = parts[0], parts[1 : 1 + K * (A + 1)], parts[1 + K * (A + 1) :]
    md, idx_tree, idx_leaf = split_digest(H_msg(r, pk_seed, pk_root, msg))
    adrs = _fors_adrs(idx_tree, idx_leaf)
    pk_fors = fors_pk_from_sig(sig_fors, md, pk_seed, adrs)  # @line L13
    return ht_verify(pk_fors, sig_ht, pk_seed, idx_tree, idx_leaf, pk_root)


def _pure(msg: bytes, ctx: bytes) -> bytes:
    if len(ctx) > 255:
        raise ValueError("the context string is longer than 255 bytes")
    return bytes([0, len(ctx)]) + ctx + msg  # @line L1


def sign(msg: bytes, sk: bytes, ctx: bytes = b"", deterministic: bool = False) -> bytes:
    """Pure SLH-DSA signing (FIPS 205 Algorithm 22); hedged by default."""
    addrnd = None if deterministic else secrets.token_bytes(N)
    return sign_internal(_pure(msg, ctx), sk, addrnd)


def verify(msg: bytes, sig: bytes, pk: bytes, ctx: bytes = b"") -> bool:
    """Pure SLH-DSA verification (FIPS 205 Algorithm 24)."""
    if len(ctx) > 255:
        return False
    return verify_internal(_pure(msg, ctx), sig, pk)
