# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newhope/. The authors are listed in prov/8ZNYFG.jsonl.
"""NewHope512-CPA-KEM as in the NIST round 2 submission (version of 2019-03-30).

This is the encryption-based NewHope (the "NewHope-Simple" line of work), not
the 2016 key exchange with reconciliation. Parameters: n = 512, q = 12289,
binomial noise with k = 8, gamma = 10968 (a primitive 1024-th root of unity)
and omega = gamma^2 = 3. Each of the 256 message bits is spread over two
coefficients. The NTT follows the reference code step by step (inputs in a
bit-reversed order, the same butterflies and tables), so the bytes match the
known answer tests of the submission.

For study only. This code is not constant time and must not be used to
protect real data.
"""

import hashlib
import secrets

N, Q, K = 512, 12289, 8
GAMMA = 10968
OMEGA = GAMMA * GAMMA % Q  # 3
POLYBYTES = 14 * N // 8         # 896
COMPBYTES = 3 * N // 8          # 192
PK_BYTES = POLYBYTES + 32       # 928
SK_BYTES = POLYBYTES            # 896
CT_BYTES = POLYBYTES + COMPBYTES  # 1088


def _bitrev(i, bits):
    return int(format(i, "0%db" % bits)[::-1], 2)


# Plain (not Montgomery) versions of the tables in precomp.c.
GAMMAS_BITREV = [pow(GAMMA, _bitrev(i, 9), Q) for i in range(N)]
OMEGAS_INV_BITREV = [pow(OMEGA, -_bitrev(i, 8), Q) for i in range(N // 2)]
GAMMAS_INV_SCALED = [pow(GAMMA, -i, Q) * pow(N, -1, Q) % Q for i in range(N)]
BITREV9 = [_bitrev(i, 9) for i in range(N)]


def shake128(b, n):
    return hashlib.shake_128(b).digest(n)


def shake256(b, n):
    return hashlib.shake_256(b).digest(n)


def _ntt_core(a, w):
    """The butterfly loop of ntt.c: a[j] + a[j+d] and w (a[j] - a[j+d])."""
    a = list(a)
    dist = 1
    while dist < N:
        for start in range(dist):
            t = 0
            for j in range(start, N - 1, 2 * dist):
                x, y = a[j], a[j + dist]
                a[j] = (x + y) % Q
                a[j + dist] = w[t] * (x - y) % Q
                t += 1
        dist <<= 1
    return a


def ntt(p):
    """poly_ntt: multiply by the gamma table, then the butterflies with the same table."""
    return _ntt_core([x * g % Q for x, g in zip(p, GAMMAS_BITREV)], GAMMAS_BITREV)


def invntt(p):
    """poly_invntt: bit-reverse, butterflies with omega^-1, then scale by gamma^-i / n."""
    a = [p[BITREV9[i]] for i in range(N)]
    a = _ntt_core(a, OMEGAS_INV_BITREV)
    return [x * g % Q for x, g in zip(a, GAMMAS_INV_SCALED)]


def pointwise(a, b):
    return [x * y % Q for x, y in zip(a, b)]


def add(a, b):
    return [(x + y) % Q for x, y in zip(a, b)]


def to_bytes(p):
    """poly_tobytes: 14 binary digits per coefficient, little-endian."""
    acc = 0
    for i, x in enumerate(p):
        acc |= (x % Q) << (14 * i)
    return acc.to_bytes(POLYBYTES, "little")


def from_bytes(b):
    acc = int.from_bytes(b[:POLYBYTES], "little")
    return [(acc >> (14 * i)) & 0x3FFF for i in range(N)]


def compress(p):
    acc = 0
    for i, x in enumerate(p):
        acc |= ((((x % Q) << 3) + Q // 2) // Q & 7) << (3 * i)
    return acc.to_bytes(COMPBYTES, "little")


def decompress(b):
    acc = int.from_bytes(b, "little")
    return [(((acc >> (3 * i)) & 7) * Q + 4) >> 3 for i in range(N)]


def from_msg(m):
    p = [0] * N
    for i in range(256):
        if (m[i >> 3] >> (i & 7)) & 1:
            p[i] = p[i + 256] = Q // 2
    return p


def to_msg(p):
    """Each bit is read from two coefficients: sum of |x - q/2| compared with q/2."""
    out = bytearray(32)
    for i in range(256):
        t = sum(abs((p[i + 256 * j] % Q) - Q // 2) for j in range(2))
        if t < Q // 2:
            out[i >> 3] |= 1 << (i & 7)
    return bytes(out)


def gen_a(seed):
    """poly_uniform: 8 blocks of 64 coefficients, SHAKE128(seed || i), keep 16-bit values < 5q."""
    a = []
    for i in range(N // 64):
        buf = shake128(seed + bytes([i]), 168 * 6)
        got = 0
        for j in range(0, len(buf), 2):
            v = buf[j] | (buf[j + 1] << 8)
            if v < 5 * Q:
                a.append(v % Q)
                got += 1
                if got == 64:
                    break
    return a


def sample(seed, nonce):
    """poly_sample: binomial noise hw(a) - hw(b) with 8-bit a and b."""
    p = []
    for i in range(N // 64):
        buf = shake256(seed + bytes([nonce, i]), 128)
        p += [(bin(buf[2 * j]).count("1") - bin(buf[2 * j + 1]).count("1")) % Q for j in range(64)]
    return p


# ---------------------------------------------------------------- CPA-PKE
def pke_keygen(z32):
    # @line L1
    z = shake256(z32, 64)
    public_seed, noise_seed = z[:32], z[32:]
    # @line L2
    ahat = gen_a(public_seed)
    # @line L3
    shat = ntt(sample(noise_seed, 0))
    ehat = ntt(sample(noise_seed, 1))
    # @line L4
    bhat = add(ehat, pointwise(shat, ahat))
    # @line L5
    return to_bytes(bhat) + public_seed, to_bytes(shat)


def pke_enc(pk, m, coin):
    v = from_msg(m)
    # @line L6
    bhat, public_seed = from_bytes(pk), pk[POLYBYTES:]
    ahat = gen_a(public_seed)
    # @line L7
    sp, ep, epp = sample(coin, 0), sample(coin, 1), sample(coin, 2)
    # @line L8
    sp = ntt(sp)
    uhat = add(pointwise(ahat, sp), ntt(ep))
    # @line L9
    vp = add(add(invntt(pointwise(bhat, sp)), epp), v)
    # @line L10
    return to_bytes(uhat) + compress(vp)


def pke_dec(sk, ct):
    # @line L11
    shat = from_bytes(sk)
    uhat, vp = from_bytes(ct), decompress(ct[POLYBYTES:])
    # @line L12
    tmp = [(x - y) % Q for x, y in zip(invntt(pointwise(shat, uhat)), vp)]
    return to_msg(tmp)


# ---------------------------------------------------------------- CPA-KEM
def keygen(seed=None):
    # @line L13
    return pke_keygen(seed if seed is not None else secrets.token_bytes(32))


def encaps(pk, coins=None):
    # @line L14
    buf = shake256(coins if coins is not None else secrets.token_bytes(32), 64)
    # @line L15
    ct = pke_enc(pk, buf[:32], buf[32:])
    # @line L16
    return ct, shake256(buf[:32], 32)


def decaps(sk, ct):
    # @line L17
    return shake256(pke_dec(sk, ct), 32)
