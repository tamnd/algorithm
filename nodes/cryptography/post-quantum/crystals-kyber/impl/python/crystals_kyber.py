# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crystals-kyber/. The authors are listed in prov/X4A2D0.jsonl.
"""ML-KEM (FIPS 203, August 2024), the standard form of CRYSTALS-Kyber.

The code follows the algorithms of FIPS 203 by number: Algorithms 3 to 12 for
the encodings, the sampling and the NTT, Algorithms 13 to 15 for K-PKE,
Algorithms 16 to 18 for the internal ML-KEM functions and Algorithms 19 to 21
for the external API with its input checks. SHA3-256, SHA3-512, SHAKE128 and
SHAKE256 come from hashlib: the page is about the KEM, not about Keccak.

For study only. This code is not constant time (it branches on secret data and
compares ciphertexts with ==), and it must not be used to protect real data.
Use a FIPS 140 validated module or a reviewed library such as liboqs or
BoringSSL for ML-KEM.
"""

import hashlib
import secrets

N = 256
Q = 3329
ZETA = 17

# name: (k, eta1, eta2, du, dv)
PARAMS = {
    "ML-KEM-512": (2, 3, 2, 10, 4),
    "ML-KEM-768": (3, 2, 2, 10, 4),
    "ML-KEM-1024": (4, 2, 2, 11, 5),
}


def _bitrev7(i):
    return int(format(i, "07b")[::-1], 2)


# zeta^BitRev7(i) for the NTT, and zeta^(2 BitRev7(i) + 1) for BaseCaseMultiply.
ZETAS = [pow(ZETA, _bitrev7(i), Q) for i in range(128)]
GAMMAS = [pow(ZETA, 2 * _bitrev7(i) + 1, Q) for i in range(128)]
N_INV = pow(128, -1, Q)  # 3303


# ------------------------------------------------------------ hash functions
def H(s):
    return hashlib.sha3_256(s).digest()


def J(s):
    return hashlib.shake_256(s).digest(32)


def G(s):
    d = hashlib.sha3_512(s).digest()
    return d[:32], d[32:]


def PRF(eta, s, b):
    return hashlib.shake_256(s + bytes([b])).digest(64 * eta)


# ------------------------------------------------- encodings (Algorithms 3-6)
def byte_encode(f, d):
    """Algorithm 5: pack 256 integers of d binary digits, least significant first."""
    acc = 0
    for i in reversed(range(N)):
        acc = (acc << d) | f[i]
    return acc.to_bytes(32 * d, "little")


def byte_decode(b, d):
    """Algorithm 6: the inverse of byte_encode; for d = 12 reduce mod q."""
    acc = int.from_bytes(b, "little")
    m = (1 << d) - 1
    f = [(acc >> (d * i)) & m for i in range(N)]
    if d == 12:
        f = [x % Q for x in f]
    return f


def compress(x, d):
    """Compress_d(x) = round((2^d / q) x) mod 2^d, in integer arithmetic."""
    return (((x << d) + Q // 2) // Q) & ((1 << d) - 1)


def decompress(y, d):
    """Decompress_d(y) = round((q / 2^d) y)."""
    return (y * Q + (1 << (d - 1))) >> d


# ------------------------------------------------- sampling (Algorithms 7-8)
def sample_ntt(seed34):
    """Algorithm 7: rejection sampling of an NTT-domain polynomial from SHAKE128."""
    length = 840
    while True:
        buf = hashlib.shake_128(seed34).digest(length)
        a = []
        pos = 0
        while len(a) < N and pos + 3 <= length:
            c0, c1, c2 = buf[pos], buf[pos + 1], buf[pos + 2]
            pos += 3
            d1 = c0 + 256 * (c1 % 16)
            d2 = (c1 // 16) + 16 * c2
            if d1 < Q:
                a.append(d1)
            if d2 < Q and len(a) < N:
                a.append(d2)
        if len(a) == N:
            return a
        length *= 2  # the XOF is a stream: a longer output extends the shorter one


def sample_cbd(b, eta):
    """Algorithm 8: centered binomial distribution from 64 eta bytes."""
    bits = int.from_bytes(b, "little")
    f = []
    for i in range(N):
        x = sum((bits >> (2 * i * eta + j)) & 1 for j in range(eta))
        y = sum((bits >> (2 * i * eta + eta + j)) & 1 for j in range(eta))
        f.append((x - y) % Q)
    return f


# --------------------------------------------------- the NTT (Algorithms 9-12)
def ntt(f):
    """Algorithm 9: the incomplete NTT of Z_q[X]/(X^256 + 1) into 128 quadratic factors."""
    f = list(f)
    i = 1
    length = 128
    while length >= 2:
        for start in range(0, N, 2 * length):
            z = ZETAS[i]
            i += 1
            for j in range(start, start + length):
                t = z * f[j + length] % Q
                f[j + length] = (f[j] - t) % Q
                f[j] = (f[j] + t) % Q
        length //= 2
    return f


def ntt_inv(f):
    """Algorithm 10: the inverse NTT, with the final factor 128^(-1) = 3303."""
    f = list(f)
    i = 127
    length = 2
    while length <= 128:
        for start in range(0, N, 2 * length):
            z = ZETAS[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (t + f[j + length]) % Q
                f[j + length] = z * (f[j + length] - t) % Q
        length *= 2
    return [x * N_INV % Q for x in f]


def multiply_ntts(f, g):
    """Algorithms 11 and 12: products in the 128 rings Z_q[X]/(X^2 - gamma)."""
    h = [0] * N
    for i in range(128):
        a0, a1, b0, b1 = f[2 * i], f[2 * i + 1], g[2 * i], g[2 * i + 1]
        h[2 * i] = (a0 * b0 + a1 * b1 * GAMMAS[i]) % Q
        h[2 * i + 1] = (a0 * b1 + a1 * b0) % Q
    return h


def _add(f, g):
    return [(a + b) % Q for a, b in zip(f, g)]


def _sub(f, g):
    return [(a - b) % Q for a, b in zip(f, g)]


def _matrix(rho, k):
    """A_hat[i][j] = SampleNTT(rho || j || i), as in Algorithms 13 and 14."""
    return [[sample_ntt(rho + bytes([j, i])) for j in range(k)] for i in range(k)]


# ------------------------------------------------- K-PKE (Algorithms 13-15)
def kpke_keygen(d, params):
    """Algorithm 13. The byte k after d is the domain separation of FIPS 203."""
    k, eta1, _, _, _ = params
    rho, sigma = G(d + bytes([k]))  # @line L1
    a_hat = _matrix(rho, k)  # @line L2
    nonce = 0
    s = []
    for _ in range(k):
        s.append(sample_cbd(PRF(eta1, sigma, nonce), eta1))  # @line L3
        nonce += 1
    e = []
    for _ in range(k):
        e.append(sample_cbd(PRF(eta1, sigma, nonce), eta1))
        nonce += 1
    s_hat = [ntt(p) for p in s]
    e_hat = [ntt(p) for p in e]
    t_hat = []
    for i in range(k):
        acc = e_hat[i]
        for j in range(k):
            acc = _add(acc, multiply_ntts(a_hat[i][j], s_hat[j]))  # @line L4
        t_hat.append(acc)
    ek = b"".join(byte_encode(p, 12) for p in t_hat) + rho
    dk = b"".join(byte_encode(p, 12) for p in s_hat)
    return ek, dk  # @line L5


def kpke_encrypt(ek, m, r, params):
    """Algorithm 14: encrypt the 32-byte message m with the 32-byte randomness r."""
    k, eta1, eta2, du, dv = params
    t_hat = [byte_decode(ek[384 * i:384 * (i + 1)], 12) for i in range(k)]
    rho = ek[384 * k:384 * k + 32]
    a_hat = _matrix(rho, k)  # @line L6
    nonce = 0
    y = []
    for _ in range(k):
        y.append(sample_cbd(PRF(eta1, r, nonce), eta1))
        nonce += 1
    e1 = []
    for _ in range(k):
        e1.append(sample_cbd(PRF(eta2, r, nonce), eta2))
        nonce += 1
    e2 = sample_cbd(PRF(eta2, r, nonce), eta2)  # @line L7
    y_hat = [ntt(p) for p in y]
    u = []
    for i in range(k):
        acc = [0] * N
        for j in range(k):
            acc = _add(acc, multiply_ntts(a_hat[j][i], y_hat[j]))  # the transpose of A
        u.append(_add(ntt_inv(acc), e1[i]))  # @line L8
    mu = [decompress(b, 1) for b in byte_decode(m, 1)]
    acc = [0] * N
    for j in range(k):
        acc = _add(acc, multiply_ntts(t_hat[j], y_hat[j]))
    v = _add(_add(ntt_inv(acc), e2), mu)  # @line L9
    c1 = b"".join(byte_encode([compress(x, du) for x in p], du) for p in u)
    c2 = byte_encode([compress(x, dv) for x in v], dv)
    return c1 + c2  # @line L10


def kpke_decrypt(dk, c, params):
    """Algorithm 15: w = v' - NTT^(-1)(s_hat^T o NTT(u')), then round each coefficient."""
    k, _, _, du, dv = params
    u = [[decompress(x, du) for x in byte_decode(c[32 * du * i:32 * du * (i + 1)], du)]
         for i in range(k)]
    v = [decompress(x, dv) for x in byte_decode(c[32 * du * k:32 * du * k + 32 * dv], dv)]  # @line L11
    s_hat = [byte_decode(dk[384 * i:384 * (i + 1)], 12) for i in range(k)]
    acc = [0] * N
    for j in range(k):
        acc = _add(acc, multiply_ntts(s_hat[j], ntt(u[j])))
    w = _sub(v, ntt_inv(acc))  # @line L12
    return byte_encode([compress(x, 1) for x in w], 1)  # @line L13


# ------------------------------------------ ML-KEM internal (Algorithms 16-18)
def keygen_internal(d, z, params):
    """Algorithm 16: dk = dk_PKE || ek || H(ek) || z."""
    ek, dk_pke = kpke_keygen(d, params)  # @line L14
    return ek, dk_pke + ek + H(ek) + z  # @line L15


def encaps_internal(ek, m, params):
    """Algorithm 17: (K, r) = G(m || H(ek)), c = K-PKE.Encrypt(ek, m, r)."""
    key, r = G(m + H(ek))  # @line L16
    return key, kpke_encrypt(ek, m, r, params)  # @line L17


def decaps_internal(dk, c, params):
    """Algorithm 18: decrypt, re-encrypt, and return J(z || c) when the check fails."""
    k = params[0]
    dk_pke = dk[:384 * k]
    ek = dk[384 * k:768 * k + 32]
    h = dk[768 * k + 32:768 * k + 64]
    z = dk[768 * k + 64:768 * k + 96]  # @line L18
    m2 = kpke_decrypt(dk_pke, c, params)
    key2, r2 = G(m2 + h)
    k_bar = J(z + c)  # @line L19
    c2 = kpke_encrypt(ek, m2, r2, params)  # @line L20
    if c != c2:  # @line L21 (implicit rejection)
        key2 = k_bar
    return key2


# ------------------------------------------- external API (Algorithms 19-21)
def sizes(params):
    k, _, _, du, dv = params
    return {"ek": 384 * k + 32, "dk": 768 * k + 96, "c": 32 * (du * k + dv)}


def keygen(name="ML-KEM-768"):
    """Algorithm 19 with fresh randomness d and z."""
    return keygen_internal(secrets.token_bytes(32), secrets.token_bytes(32), PARAMS[name])  # @line L22


def check_ek(ek, params):
    """The type check and the modulus check of Section 7.2."""
    k = params[0]
    if len(ek) != sizes(params)["ek"]:
        return False
    for i in range(k):
        part = ek[384 * i:384 * (i + 1)]
        if byte_encode(byte_decode(part, 12), 12) != part:
            return False
    return True


def check_dk(dk, params):
    """The type check and the hash check of Section 7.3."""
    k = params[0]
    if len(dk) != sizes(params)["dk"]:
        return False
    return H(dk[384 * k:768 * k + 32]) == dk[768 * k + 32:768 * k + 64]


def encaps(ek, name="ML-KEM-768"):
    """Algorithm 20 with a fresh 32-byte m."""
    params = PARAMS[name]
    if not check_ek(ek, params):  # @line L23
        raise ValueError("encapsulation key fails the input check")
    return encaps_internal(ek, secrets.token_bytes(32), params)


def decaps(dk, c, name="ML-KEM-768"):
    """Algorithm 21."""
    params = PARAMS[name]
    if len(c) != sizes(params)["c"] or not check_dk(dk, params):  # @line L24
        raise ValueError("input fails the check")
    return decaps_internal(dk, c, params)
