# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/picnic-signature/. The authors are listed in prov/CCDYS8.jsonl.

"""A toy signature in the style of Picnic: ZKB++ with Fiat-Shamir.

This is NOT the Picnic specification. Picnic proves knowledge of a LowMC key
with 128-bit blocks; this code proves knowledge of the key of a toy 32-bit
XOR/AND/rotation cipher, made up for study and trivially broken by brute
force over 2^32 keys. The proof system follows ZKB++ (Chase et al., CCS 2017):
three players hold XOR shares of the key, each AND gate uses the formula of
ZKBoo, the prover commits to the three views, a hash picks two views to open
in each of t parallel rounds, and the third output share is recomputed from
the public output.

For study only and not constant time. For real signatures use ML-DSA or
SLH-DSA from a FIPS 140 validated module.
"""

import hashlib
import random

MASK = 0xFFFFFFFF
ROUNDS = 4
RC = (0x9E3779B9, 0x7F4A7C15, 0xF39CC060, 0x5CEDC834)
T_ROUNDS = 219  # (2/3)^219 < 2^-128, as in Picnic-L1-FS
SEED_BYTES = 16


def rotl(x: int, r: int) -> int:
    return ((x << r) | (x >> (32 - r))) & MASK


def toy_cipher(key: int, pt: int) -> int:
    """The toy one-way function E_k(p): 4 rounds of s ^= rotl(s,1) & rotl(s,2), rotate, add key."""
    s = pt ^ key
    for r in range(ROUNDS):
        s ^= rotl(s, 1) & rotl(s, 2)
        s = rotl(s, 5) ^ RC[r] ^ key
    return s


def _hash(*parts) -> bytes:
    h = hashlib.shake_128()
    for part in parts:
        if isinstance(part, int):
            part = part.to_bytes(4, "little")
        h.update(len(part).to_bytes(4, "little") + part)
    return h.digest(32)


def _words(ws) -> bytes:
    return b"".join(w.to_bytes(4, "little") for w in ws)


def _expand(seed: bytes, player: int):
    """The key share (used by players 0 and 1 only) and the random tape of a player."""
    d = hashlib.shake_128(b"tape" + bytes([player]) + seed).digest(4 * (ROUNDS + 1))
    w = [int.from_bytes(d[4 * i: 4 * i + 4], "little") for i in range(ROUNDS + 1)]
    return w[0], w[1:]


def _commit(seed: bytes, k2, z) -> bytes:
    return _hash(b"commit", seed, b"" if k2 is None else k2, _words(z))


def _and_share(a0, b0, a1, b1, r0, r1) -> int:
    """Share of the AND of a and b for player i, from its own shares and those of player i + 1."""
    return (a0 & b0) ^ (a1 & b0) ^ (a0 & b1) ^ r0 ^ r1


def _step(s: int, z: int, key: int, r: int, player: int) -> int:
    """The linear part of round r for one share."""
    return rotl(s ^ z, 5) ^ key ^ (RC[r] if player == 0 else 0)


def mpc_run(pt: int, keys, tapes):
    """Run the 3-player protocol for E_k(p) on key shares; return the output shares and views."""
    s = [pt ^ keys[0], keys[1], keys[2]]
    z = [[], [], []]
    for r in range(ROUNDS):
        a = [rotl(x, 1) for x in s]
        b = [rotl(x, 2) for x in s]
        zr = [_and_share(a[i], b[i], a[(i + 1) % 3], b[(i + 1) % 3],
                         tapes[i][r], tapes[(i + 1) % 3][r]) for i in range(3)]
        for i in range(3):
            z[i].append(zr[i])
            s[i] = _step(s[i], zr[i], keys[i], r, i)
    return s, z


def challenge(pk, msg: bytes, ys, cs, t: int):
    """t values in {0, 1, 2} from the hash, by rejection of the bit pair 11 (as in Picnic)."""
    p, y = pk
    seed = _hash(b"challenge", p, y, msg, _words(w for row in ys for w in row), b"".join(c for row in cs for c in row))
    out, n = [], 8 * t
    while len(out) < t:
        bits = int.from_bytes(hashlib.shake_128(seed).digest(n), "little")
        out = []
        for i in range(4 * n):
            v = (bits >> (2 * i)) & 3
            if v < 3:
                out.append(v)
                if len(out) == t:
                    break
        n *= 2
    return out


def keygen(rng: random.Random):
    k = rng.getrandbits(32)
    p = rng.getrandbits(32)
    return k, (p, toy_cipher(k, p))


def sign(k: int, pk, msg: bytes, rng: random.Random, t: int = T_ROUNDS):
    p, _ = pk
    seeds, k2s, views, ys, cs = [], [], [], [], []
    for _ in range(t):  # @line L1
        sd = [rng.randbytes(SEED_BYTES) for _ in range(3)]  # @line L2
        (k0, t0), (k1, t1), (_, t2) = (_expand(sd[i], i) for i in range(3))
        k2 = k ^ k0 ^ k1
        out, z = mpc_run(p, (k0, k1, k2), (t0, t1, t2))  # @line L3
        k2b = k2.to_bytes(4, "little")
        c = [_commit(sd[i], k2b if i == 2 else None, z[i]) for i in range(3)]  # @line L4
        seeds.append(sd)
        k2s.append(k2b)
        views.append(z)
        ys.append(out)
        cs.append(c)
    es = challenge(pk, msg, ys, cs, t)  # @line L5
    resp = []
    for j in range(t):  # @line L6
        e = es[j]
        f, g = (e + 1) % 3, (e + 2) % 3
        resp.append((seeds[j][e], seeds[j][f], k2s[j] if 2 in (e, f) else None,
                     list(views[j][f]), cs[j][g]))  # @line L7
    return es, resp  # @line L8


def reconstruct(pk, e: int, r):
    """From one response, recompute the three output shares and the three commitments."""
    p, y = pk
    seed_e, seed_f, k2b, z_f, c_g = r
    f, g = (e + 1) % 3, (e + 2) % 3
    keys, tapes = [], []
    for player, sd in ((e, seed_e), (f, seed_f)):
        kp, tp = _expand(sd, player)
        if player == 2:
            if k2b is None:
                raise ValueError("missing input share of player 2")
            kp = int.from_bytes(k2b, "little")
        keys.append(kp)
        tapes.append(tp)
    s = [(p if e == 0 else 0) ^ keys[0], (p if f == 0 else 0) ^ keys[1]]
    z_e = []
    for rd in range(ROUNDS):
        a = [rotl(x, 1) for x in s]
        b = [rotl(x, 2) for x in s]
        ze = _and_share(a[0], b[0], a[1], b[1], tapes[0][rd], tapes[1][rd])
        z_e.append(ze)
        s[0] = _step(s[0], ze, keys[0], rd, e)
        s[1] = _step(s[1], z_f[rd], keys[1], rd, f)
    ys = [0, 0, 0]
    ys[e], ys[f] = s
    ys[g] = y ^ s[0] ^ s[1]
    cs = [b"", b"", b""]
    cs[g] = c_g
    cs[e] = _commit(seed_e, k2b if e == 2 else None, z_e)
    cs[f] = _commit(seed_f, k2b if f == 2 else None, z_f)
    return ys, cs


def verify(pk, msg: bytes, sig) -> bool:
    es, resp = sig
    if len(es) != len(resp) or any(e not in (0, 1, 2) for e in es):
        return False
    ys, cs = [], []
    try:
        for e, r in zip(es, resp):  # @line L9
            if len(r[3]) != ROUNDS or (r[2] is not None) != (2 in (e, (e + 1) % 3)):
                return False
            y_row, c_row = reconstruct(pk, e, r)  # @line L10
            ys.append(y_row)  # @line L11
            cs.append(c_row)
    except (ValueError, TypeError, IndexError):
        return False
    return challenge(pk, msg, ys, cs, len(es)) == es  # @line L12


def signature_size(sig) -> int:
    """Bytes in a packed form: 2 bits per challenge, then each response."""
    es, resp = sig
    n = (2 * len(es) + 7) // 8
    for seed_e, seed_f, k2b, z_f, c_g in resp:
        n += len(seed_e) + len(seed_f) + (4 if k2b is not None else 0) + 4 * len(z_f) + len(c_g)
    return n
