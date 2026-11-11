# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntru-encrypt/. The authors are listed in prov/T0H5SG.jsonl.
"""NTRUEncrypt in two forms.

1. ClassicNTRU: the 1998 scheme of Hoffstein, Pipher and Silverman in
   Z[x]/(x^N - 1): h = p g f^-1 mod q, e = r h + m mod q, and decryption by
   a = f e mod q (centered), then m = f_p^-1 a mod p. It takes any (N, p, q)
   and is used here with small toy parameters.

2. ntruhps2048509: the KEM of the NIST round 3 NTRU submission (HPS variant,
   n = 509, q = 2048), with the byte formats of the reference code, so that
   the known answer tests can be checked. In this variant f is ternary,
   g has a fixed type (127 ones and 127 minus ones), the public key is
   h = 3 g / f, and the KEM has no re-encryption: decryption recovers r and
   m and checks that they lie in the message space.

For study only. This code is not constant time and must not be used to
protect real data.
"""

import hashlib
import secrets


# ---------------------------------------------------------------- polynomials
def cyclic_mul(a, b, n, mod):
    """a * b in Z_mod[x]/(x^n - 1), by Kronecker substitution on Python integers."""
    w = 2 * mod.bit_length() + n.bit_length() + 2
    A = sum((x % mod) << (w * i) for i, x in enumerate(a))
    B = sum((x % mod) << (w * i) for i, x in enumerate(b))
    C = A * B
    mask = (1 << w) - 1
    out = [0] * n
    for k in range(2 * n - 1):
        out[k % n] += (C >> (w * k)) & mask
    return [x % mod for x in out]


def _deg(a):
    d = len(a) - 1
    while d >= 0 and a[d] == 0:
        d -= 1
    return d


def inv_mod_prime(a, m, p):
    """Inverse of a modulo the polynomial m over GF(p), or None (extended Euclid)."""
    r0, r1 = [x % p for x in m], [x % p for x in a]
    s0, s1 = [0], [1]
    while _deg(r1) >= 0:
        d0, d1 = _deg(r0), _deg(r1)
        if d0 < d1:
            r0, r1, s0, s1 = r1, r0, s1, s0
            continue
        inv_lead = pow(r1[d1], -1, p)
        quo = [0] * (d0 - d1 + 1)
        rem = r0[:d0 + 1]
        for k in range(d0 - d1, -1, -1):
            c = rem[k + d1] * inv_lead % p
            quo[k] = c
            if c:
                for j in range(d1 + 1):
                    rem[k + j] = (rem[k + j] - c * r1[j]) % p
        prod = [0] * (len(quo) + len(s1))
        for i, x in enumerate(quo):
            if x:
                for j, y in enumerate(s1):
                    prod[i + j] += x * y
        s_new = [((s0[i] if i < len(s0) else 0) - (prod[i] if i < len(prod) else 0)) % p for i in range(max(len(s0), len(prod)))]
        r0, r1, s0, s1 = r1, rem, s1, s_new
    if _deg(r0) != 0:
        return None
    c = pow(r0[0], -1, p)
    n = len(m) - 1  # s0 already has degree below deg(m) = n
    return ([x * c % p for x in s0] + [0] * n)[:n]


def inv_mod_power_of_two(a, m, n, q, reduce):
    """Inverse modulo (q, m) for q = 2^k: inverse mod 2, then Newton steps b <- b (2 - a b)."""
    b = inv_mod_prime(a, m, 2)
    if b is None:
        return None
    mod = 2
    while mod < q:
        mod = min(mod * mod, q)
        ab = reduce(cyclic_mul(a, b, n, mod), mod)
        two_minus = [(-x) % mod for x in ab]
        two_minus[0] = (two_minus[0] + 2) % mod
        b = reduce(cyclic_mul(b, two_minus, n, mod), mod)
    return b


def center(x, mod):
    x %= mod
    return x - mod if x > mod // 2 else x


# ---------------------------------------------------------------- 1. classic NTRUEncrypt
class ClassicNTRU:
    """The 1998 scheme in Z[x]/(x^N - 1) with ternary f, g, r and a ternary message."""

    def __init__(self, n, p, q, df, dg, dr):
        self.n, self.p, self.q, self.df, self.dg, self.dr = n, p, q, df, dg, dr
        self.ring = [-1] + [0] * (n - 1) + [1]  # x^N - 1, low degree first

    def _ternary(self, rng, ones, minus):
        v = [1] * ones + [-1] * minus + [0] * (self.n - ones - minus)
        rng.shuffle(v)
        return v

    def _reduce(self, v, mod):
        return [x % mod for x in v]

    def keygen(self, rng):
        while True:
            # @line L1
            f = self._ternary(rng, self.df, self.df - 1)
            # @line L2
            fp = inv_mod_prime(f, self.ring, self.p)
            fq = inv_mod_power_of_two(f, self.ring, self.n, self.q, self._reduce)
            if fp is not None and fq is not None:
                break
        g = self._ternary(rng, self.dg, self.dg)
        # @line L3
        h = [self.p * x % self.q for x in cyclic_mul(fq, g, self.n, self.q)]
        # @line L4
        return h, (f, fp)

    def encrypt(self, h, m, rng):
        # @line L5
        r = self._ternary(rng, self.dr, self.dr)
        # @line L6
        return [(x + y) % self.q for x, y in zip(cyclic_mul(r, h, self.n, self.q), m)]

    def decrypt(self, sk, e):
        f, fp = sk
        # @line L7
        a = [center(x, self.q) for x in cyclic_mul(f, e, self.n, self.q)]
        # @line L8
        return [center(x, self.p) for x in cyclic_mul(fp, a, self.n, self.p)]


# ---------------------------------------------------------------- 2. ntruhps2048509
N, LOGQ = 509, 11
Q = 1 << LOGQ
WEIGHT = Q // 8 - 2                       # 254
IID_BYTES = N - 1                         # 508
FT_BYTES = (30 * (N - 1) + 7) // 8        # 1905
FG_BYTES = IID_BYTES + FT_BYTES           # 2413
TRIT_BYTES = (N - 1 + 4) // 5             # 102
OWCPA_BYTES = (LOGQ * (N - 1) + 7) // 8   # 699
PK_BYTES = CT_BYTES = OWCPA_BYTES
SK_BYTES = 2 * TRIT_BYTES + OWCPA_BYTES + 32  # 935
PHI = [1] * N                             # 1 + x + ... + x^(N-1)


def mod_phi(v, mod):
    """Reduce modulo Phi_N so that the coefficient of x^(N-1) is 0."""
    return [(x - v[N - 1]) % mod for x in v]


def sample_iid(u):
    return [b % 3 for b in u[:N - 1]] + [0]


def sample_fixed_type(u):
    bits = int.from_bytes(u, "little")
    s = []
    for i in range(N - 1):
        x = (((bits >> (30 * i)) & ((1 << 30) - 1)) << 2) | (1 if i < WEIGHT // 2 else 2 if i < WEIGHT else 0)
        s.append(x - (1 << 32) if x >= 1 << 31 else x)  # the reference sorts int32 values
    s.sort()
    return [x & 3 for x in s] + [0]


def s3_tobytes(a):
    out = bytearray()
    for i in range(0, N - 1, 5):
        c = 0
        for j in range(min(5, N - 1 - i) - 1, -1, -1):
            c = 3 * c + a[i + j]
        out.append(c & 255)
    return bytes(out)


def s3_frombytes(b):
    a = []
    for i in range(TRIT_BYTES):
        c = b[i]
        for _ in range(min(5, N - 1 - 5 * i)):
            a.append(c % 3)
            c //= 3
    return mod_phi(a + [0], 3)


def sq_tobytes(a):
    acc = 0
    for i in range(N - 1):
        acc |= (a[i] % Q) << (LOGQ * i)
    return acc.to_bytes(OWCPA_BYTES, "little")


def sq_frombytes(b):
    acc = int.from_bytes(b, "little")
    return [(acc >> (LOGQ * i)) & (Q - 1) for i in range(N - 1)] + [0]


def rq_sum_zero_frombytes(b):
    a = sq_frombytes(b)
    a[N - 1] = (-sum(a)) % Q
    return a


def z3_to_zq(a):
    return [Q - 1 if x == 2 else x for x in a]


def owcpa_keypair(seed):
    # @line L9
    f = sample_iid(seed[:IID_BYTES])
    g = sample_fixed_type(seed[IID_BYTES:FG_BYTES])
    # @line L10
    finv3 = inv_mod_prime(f, PHI, 3) + [0]  # f^-1 in Z_3[x]/Phi_N
    fq = z3_to_zq(f)
    gq = [3 * x % Q for x in z3_to_zq(g)]
    gf = mod_phi(cyclic_mul(gq, fq, N, Q), Q)
    invgf = inv_mod_power_of_two(gf, PHI, N, Q, mod_phi)  # (g f)^-1 in Z_q[x]/Phi_N
    invh = mod_phi(cyclic_mul(cyclic_mul(invgf, fq, N, Q), fq, N, Q), Q)  # f / (3 g)
    h = cyclic_mul(cyclic_mul(invgf, gq, N, Q), gq, N, Q)  # 3 g / f, and h(1) = 0
    # @line L11
    sk = s3_tobytes(f) + s3_tobytes(finv3) + sq_tobytes(invh)
    return sq_tobytes(h), sk


def owcpa_enc(r, m, pk):
    h = rq_sum_zero_frombytes(pk)
    # @line L13
    ct = [(x + y) % Q for x, y in zip(cyclic_mul(z3_to_zq(r), h, N, Q), z3_to_zq(m))]
    return sq_tobytes(ct)


def owcpa_dec(c_bytes, sk):
    c = rq_sum_zero_frombytes(c_bytes)
    f = z3_to_zq(s3_frombytes(sk[:TRIT_BYTES]))
    # @line L15
    cf = cyclic_mul(c, f, N, Q)
    mf = mod_phi([center(x, Q) % 3 for x in cf], 3)
    finv3 = s3_frombytes(sk[TRIT_BYTES:2 * TRIT_BYTES])
    m = mod_phi(cyclic_mul(mf, finv3, N, 3), 3)
    fail = c_bytes[-1] >> ((LOGQ * (N - 1)) % 8) != 0
    if not (m.count(1) == m.count(2) == WEIGHT // 2):
        fail = True
    # @line L16
    b = [(x - y) % Q for x, y in zip(c, z3_to_zq(m))]
    invh = sq_frombytes(sk[2 * TRIT_BYTES:2 * TRIT_BYTES + OWCPA_BYTES])
    r = mod_phi(cyclic_mul(b, invh, N, Q), Q)
    if any(x not in (0, 1, Q - 1) for x in r):
        fail = True
    r3 = [2 if x == Q - 1 else x for x in r]
    return s3_tobytes(r3) + s3_tobytes(m), fail


def keygen(seed=None, prf_key=None):
    seed = seed if seed is not None else secrets.token_bytes(FG_BYTES)
    prf_key = prf_key if prf_key is not None else secrets.token_bytes(32)
    pk, sk = owcpa_keypair(seed)
    return pk, sk + prf_key


def encaps(pk, coins=None):
    coins = coins if coins is not None else secrets.token_bytes(FG_BYTES)
    # @line L12
    r = sample_iid(coins[:IID_BYTES])
    m = sample_fixed_type(coins[IID_BYTES:FG_BYTES])
    # @line L14
    k = hashlib.sha3_256(s3_tobytes(r) + s3_tobytes(m)).digest()
    return owcpa_enc(r, m, pk), k


def decaps(sk, ct):
    rm, fail = owcpa_dec(ct, sk)
    # @line L17
    if fail:
        return hashlib.sha3_256(sk[SK_BYTES - 32:] + ct).digest()
    return hashlib.sha3_256(rm).digest()
