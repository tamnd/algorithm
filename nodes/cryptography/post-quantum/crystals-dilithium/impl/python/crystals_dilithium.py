# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crystals-dilithium/. The authors are listed in prov/1PTKAJ.jsonl.
"""ML-DSA (FIPS 204, August 2024), the standard form of CRYSTALS-Dilithium.

The code follows FIPS 204: ML-DSA.KeyGen_internal, ML-DSA.Sign_internal and
ML-DSA.Verify_internal (Algorithms 6, 7 and 8), the external functions with a
context string (Algorithms 1, 2 and 3), and the helper functions of Section 7
(the encodings, ExpandA, ExpandS, ExpandMask, SampleInBall, Power2Round,
Decompose, HighBits, LowBits, MakeHint, UseHint and the NTT). SHAKE128 and
SHAKE256 come from hashlib: the page is about the signature, not about Keccak.
The pre-hash variant HashML-DSA is not implemented.

For study only. This code is not constant time, it branches on secret data,
and it must not be used to protect real data. Use a FIPS 140 validated module
or a reviewed library such as liboqs or BoringSSL for ML-DSA.
"""

import hashlib
import secrets

N = 256
Q = 8380417
D = 13
ZETA = 1753

# name: (k, l, eta, tau, lambda, gamma1, gamma2, omega)
PARAMS = {
    "ML-DSA-44": (4, 4, 2, 39, 128, 1 << 17, (Q - 1) // 88, 80),
    "ML-DSA-65": (6, 5, 4, 49, 192, 1 << 19, (Q - 1) // 32, 55),
    "ML-DSA-87": (8, 7, 2, 60, 256, 1 << 19, (Q - 1) // 32, 75),
}


def _bitrev8(i):
    return int(format(i, "08b")[::-1], 2)


ZETAS = [pow(ZETA, _bitrev8(i), Q) for i in range(256)]
N_INV = pow(256, -1, Q)  # 8347681


def shake256(data, n):
    return hashlib.shake_256(data).digest(n)


def mod_pm(r, alpha):
    """The centered representative of r mod alpha, in (-alpha/2, alpha/2]."""
    r0 = r % alpha
    if r0 > alpha // 2:
        r0 -= alpha
    return r0


def inf_norm(vec):
    """The max over all coefficients of |c mod+- q|."""
    return max(abs(mod_pm(c, Q)) for p in vec for c in p)


# --------------------------------------------------------------- the NTT
def ntt(w):
    w = list(w)
    m = 0
    length = 128
    while length >= 1:
        for start in range(0, N, 2 * length):
            m += 1
            z = ZETAS[m]
            for j in range(start, start + length):
                t = z * w[j + length] % Q
                w[j + length] = (w[j] - t) % Q
                w[j] = (w[j] + t) % Q
        length //= 2
    return w


def ntt_inv(w):
    w = list(w)
    m = 256
    length = 1
    while length < N:
        for start in range(0, N, 2 * length):
            m -= 1
            z = Q - ZETAS[m]
            for j in range(start, start + length):
                t = w[j]
                w[j] = (t + w[j + length]) % Q
                w[j + length] = z * (t - w[j + length]) % Q
        length *= 2
    return [x * N_INV % Q for x in w]


def _pmul(a, b):
    return [x * y % Q for x, y in zip(a, b)]


def _padd(a, b):
    return [(x + y) % Q for x, y in zip(a, b)]


def _psub(a, b):
    return [(x - y) % Q for x, y in zip(a, b)]


def _matvec(a_hat, v_hat):
    out = []
    for row in a_hat:
        acc = [0] * N
        for a, v in zip(row, v_hat):
            acc = _padd(acc, _pmul(a, v))
        out.append(acc)
    return out


# ------------------------------------------------------------- bit packing
def simple_bit_pack(w, b):
    """Coefficients in [0, b], each in bitlen(b) binary digits, least significant first."""
    bits = b.bit_length()
    acc = 0
    for c in reversed(w):
        acc = (acc << bits) | c
    return acc.to_bytes(32 * bits, "little")


def simple_bit_unpack(v, b):
    bits = b.bit_length()
    acc = int.from_bytes(v, "little")
    m = (1 << bits) - 1
    return [(acc >> (bits * i)) & m for i in range(N)]


def bit_pack(w, a, b):
    """Coefficients in [-a, b], stored as b - c."""
    return simple_bit_pack([b - mod_pm(c, Q) for c in w], a + b)


def bit_unpack(v, a, b):
    return [(b - x) % Q for x in simple_bit_unpack(v, a + b)]


def hint_bit_pack(h, omega, k):
    y = bytearray(omega + k)
    index = 0
    for i in range(k):
        for j in range(N):
            if h[i][j]:
                y[index] = j
                index += 1
        y[omega + i] = index
    return bytes(y)


def hint_bit_unpack(y, omega, k):
    h = [[0] * N for _ in range(k)]
    index = 0
    for i in range(k):
        if y[omega + i] < index or y[omega + i] > omega:
            return None
        first = index
        while index < y[omega + i]:
            if index > first and y[index - 1] >= y[index]:
                return None
            h[i][y[index]] = 1
            index += 1
    for i in range(index, omega):
        if y[i] != 0:
            return None
    return h


# ---------------------------------------------------------------- sampling
def rej_ntt_poly(seed):
    """Uniform polynomial mod q from SHAKE128, three bytes per trial (top bit cleared)."""
    length = 840
    while True:
        buf = hashlib.shake_128(seed).digest(length)
        a = []
        for pos in range(0, length - 2, 3):
            z = buf[pos] | (buf[pos + 1] << 8) | ((buf[pos + 2] & 0x7F) << 16)
            if z < Q:
                a.append(z)
                if len(a) == N:
                    return a
        length *= 2


def _coeff_from_half_byte(b, eta):
    if eta == 2 and b < 15:
        return 2 - (b % 5)
    if eta == 4 and b < 9:
        return 4 - b
    return None


def rej_bounded_poly(seed, eta):
    """Coefficients in [-eta, eta] from SHAKE256, two half bytes per byte."""
    length = 272
    while True:
        buf = shake256(seed, length)
        a = []
        for z in buf:
            for half in (z & 15, z >> 4):
                c = _coeff_from_half_byte(half, eta)
                if c is not None and len(a) < N:
                    a.append(c % Q)
            if len(a) == N:
                return a
        length *= 2


def expand_a(rho, k, l):
    return [[rej_ntt_poly(rho + bytes([s, r])) for s in range(l)] for r in range(k)]


def expand_s(rho1, k, l, eta):
    s1 = [rej_bounded_poly(rho1 + r.to_bytes(2, "little"), eta) for r in range(l)]
    s2 = [rej_bounded_poly(rho1 + (r + l).to_bytes(2, "little"), eta) for r in range(k)]
    return s1, s2


def expand_mask(rho2, kappa, l, gamma1):
    c = 1 + (gamma1 - 1).bit_length()
    return [bit_unpack(shake256(rho2 + (kappa + r).to_bytes(2, "little"), 32 * c), gamma1 - 1, gamma1)
            for r in range(l)]


def sample_in_ball(seed, tau):
    """A polynomial with tau coefficients in {-1, 1} and the rest 0 (inside-out Fisher-Yates)."""
    buf = shake256(seed, 8 + 4 * 256)
    pos = 8
    signs = int.from_bytes(buf[:8], "little")
    c = [0] * N
    for i in range(N - tau, N):
        while True:
            if pos >= len(buf):
                buf = shake256(seed, 2 * len(buf))
            j = buf[pos]
            pos += 1
            if j <= i:
                break
        c[i] = c[j]
        c[j] = Q - 1 if (signs >> (i + tau - N)) & 1 else 1
    return c


# ----------------------------------------------------------- rounding
def power2round(r):
    """r = r1 2^d + r0 with r0 in (-2^(d-1), 2^(d-1)]."""
    rp = r % Q
    r0 = mod_pm(rp, 1 << D)
    return (rp - r0) >> D, r0


def decompose(r, gamma2):
    rp = r % Q
    r0 = mod_pm(rp, 2 * gamma2)
    if rp - r0 == Q - 1:
        return 0, r0 - 1
    return (rp - r0) // (2 * gamma2), r0


def high_bits(r, gamma2):
    return decompose(r, gamma2)[0]


def low_bits(r, gamma2):
    return decompose(r, gamma2)[1]


def make_hint(z, r, gamma2):
    """1 when adding z changes the high bits of r."""
    return int(high_bits(r, gamma2) != high_bits(r + z, gamma2))


def use_hint(h, r, gamma2):
    m = (Q - 1) // (2 * gamma2)
    r1, r0 = decompose(r, gamma2)
    if h == 1 and r0 > 0:
        return (r1 + 1) % m
    if h == 1 and r0 <= 0:
        return (r1 - 1) % m
    return r1


def w1_encode(w1, gamma2):
    b = (Q - 1) // (2 * gamma2) - 1
    return b"".join(simple_bit_pack(p, b) for p in w1)


# --------------------------------------------------------------- encodings
def pk_encode(rho, t1):
    return rho + b"".join(simple_bit_pack(p, (1 << 10) - 1) for p in t1)


def pk_decode(pk, k):
    return pk[:32], [simple_bit_unpack(pk[32 + 320 * i:32 + 320 * (i + 1)], (1 << 10) - 1) for i in range(k)]


def sk_encode(rho, key, tr, s1, s2, t0, eta):
    out = rho + key + tr
    out += b"".join(bit_pack(p, eta, eta) for p in s1)
    out += b"".join(bit_pack(p, eta, eta) for p in s2)
    out += b"".join(bit_pack(p, (1 << (D - 1)) - 1, 1 << (D - 1)) for p in t0)
    return out


def sk_decode(sk, k, l, eta):
    rho, key, tr = sk[:32], sk[32:64], sk[64:128]
    sz = 32 * (2 * eta).bit_length()
    pos = 128
    s1 = []
    for _ in range(l):
        s1.append(bit_unpack(sk[pos:pos + sz], eta, eta))
        pos += sz
    s2 = []
    for _ in range(k):
        s2.append(bit_unpack(sk[pos:pos + sz], eta, eta))
        pos += sz
    t0 = []
    for _ in range(k):
        t0.append(bit_unpack(sk[pos:pos + 32 * D], (1 << (D - 1)) - 1, 1 << (D - 1)))
        pos += 32 * D
    return rho, key, tr, s1, s2, t0


def sig_encode(c_tilde, z, h, gamma1, omega, k):
    return c_tilde + b"".join(bit_pack(p, gamma1 - 1, gamma1) for p in z) + hint_bit_pack(h, omega, k)


def sig_decode(sig, k, l, lam, gamma1, omega):
    clen = lam // 4
    zsz = 32 * (1 + (gamma1 - 1).bit_length())
    if len(sig) != clen + l * zsz + omega + k:
        return None
    c_tilde = sig[:clen]
    z = [bit_unpack(sig[clen + i * zsz:clen + (i + 1) * zsz], gamma1 - 1, gamma1) for i in range(l)]
    h = hint_bit_unpack(sig[clen + l * zsz:], omega, k)
    return c_tilde, z, h


# --------------------------------------------------- the internal functions
def keygen_internal(xi, name="ML-DSA-44"):
    """Algorithm 6: keys from the 32-byte seed xi."""
    k, l, eta, _, _, _, _, _ = PARAMS[name]
    seed = shake256(xi + bytes([k, l]), 128)
    rho, rho1, key = seed[:32], seed[32:96], seed[96:]  # @line L1
    a_hat = expand_a(rho, k, l)
    s1, s2 = expand_s(rho1, k, l, eta)  # @line L2
    t = [_padd(ntt_inv(p), e) for p, e in zip(_matvec(a_hat, [ntt(s) for s in s1]), s2)]  # @line L3
    t1, t0 = [], []
    for p in t:
        pair = [power2round(c) for c in p]  # @line L4
        t1.append([x for x, _ in pair])
        t0.append([y % Q for _, y in pair])
    pk = pk_encode(rho, t1)
    tr = shake256(pk, 64)  # @line L5
    return pk, sk_encode(rho, key, tr, s1, s2, t0, eta)  # @line L6


def sign_internal(sk, msg, rnd, name="ML-DSA-44", stats=None):
    """Algorithm 7: Fiat-Shamir with aborts. msg is the formatted message M'."""
    k, l, eta, tau, lam, gamma1, gamma2, omega = PARAMS[name]
    beta = tau * eta
    rho, key, tr, s1, s2, t0 = sk_decode(sk, k, l, eta)
    s1_hat = [ntt(p) for p in s1]
    s2_hat = [ntt(p) for p in s2]
    t0_hat = [ntt(p) for p in t0]
    a_hat = expand_a(rho, k, l)
    mu = shake256(tr + msg, 64)
    rho2 = shake256(key + rnd + mu, 64)  # @line L7
    kappa = 0
    while True:  # @line L8
        if stats is not None:
            stats["tries"] = stats.get("tries", 0) + 1
        y = expand_mask(rho2, kappa, l, gamma1)  # @line L9
        kappa += l
        w = [ntt_inv(p) for p in _matvec(a_hat, [ntt(p) for p in y])]
        w1 = [[high_bits(c, gamma2) for c in p] for p in w]  # @line L10
        c_tilde = shake256(mu + w1_encode(w1, gamma2), lam // 4)
        c_hat = ntt(sample_in_ball(c_tilde, tau))  # @line L11
        cs1 = [ntt_inv(_pmul(c_hat, p)) for p in s1_hat]
        cs2 = [ntt_inv(_pmul(c_hat, p)) for p in s2_hat]
        z = [_padd(a, b) for a, b in zip(y, cs1)]
        r = [_psub(a, b) for a, b in zip(w, cs2)]  # @line L12
        if inf_norm(z) >= gamma1 - beta:
            continue
        if max(abs(low_bits(c, gamma2)) for p in r for c in p) >= gamma2 - beta:  # @line L13
            continue
        ct0 = [ntt_inv(_pmul(c_hat, p)) for p in t0_hat]
        if inf_norm(ct0) >= gamma2:
            continue
        h = [[make_hint((-a) % Q, b + a, gamma2) for a, b in zip(pa, pb)] for pa, pb in zip(ct0, r)]  # @line L14
        if sum(map(sum, h)) > omega:  # @line L15
            continue
        return sig_encode(c_tilde, z, h, gamma1, omega, k)  # @line L16


def verify_internal(pk, msg, sig, name="ML-DSA-44"):
    """Algorithm 8."""
    k, l, eta, tau, lam, gamma1, gamma2, omega = PARAMS[name]
    beta = tau * eta
    rho, t1 = pk_decode(pk, k)
    dec = sig_decode(sig, k, l, lam, gamma1, omega)
    if dec is None or dec[2] is None:  # @line L17
        return False
    c_tilde, z, h = dec
    if inf_norm(z) >= gamma1 - beta:  # @line L18
        return False
    a_hat = expand_a(rho, k, l)
    tr = shake256(pk, 64)
    mu = shake256(tr + msg, 64)
    c_hat = ntt(sample_in_ball(c_tilde, tau))  # @line L19
    az = _matvec(a_hat, [ntt(p) for p in z])
    ct1 = [_pmul(c_hat, ntt([(x << D) % Q for x in p])) for p in t1]
    w_approx = [ntt_inv(_psub(a, b)) for a, b in zip(az, ct1)]  # @line L20
    w1 = [[use_hint(hb, c, gamma2) for hb, c in zip(hp, wp)] for hp, wp in zip(h, w_approx)]  # @line L21
    return c_tilde == shake256(mu + w1_encode(w1, gamma2), lam // 4)  # @line L22


# --------------------------------------------------- the external functions
def keygen(name="ML-DSA-44"):
    """Algorithm 1."""
    return keygen_internal(secrets.token_bytes(32), name)  # @line L23


def _format(msg, ctx):
    if len(ctx) > 255:
        raise ValueError("context string longer than 255 bytes")
    return bytes([0, len(ctx)]) + ctx + msg


def sign(sk, msg, ctx=b"", name="ML-DSA-44", deterministic=False):
    """Algorithm 2: the hedged variant by default, the deterministic one with rnd = 0^32."""
    rnd = bytes(32) if deterministic else secrets.token_bytes(32)  # @line L24
    return sign_internal(sk, _format(msg, ctx), rnd, name)


def verify(pk, msg, sig, ctx=b"", name="ML-DSA-44"):
    """Algorithm 3."""
    if len(ctx) > 255:
        return False
    return verify_internal(pk, _format(msg, ctx), sig, name)  # @line L25
