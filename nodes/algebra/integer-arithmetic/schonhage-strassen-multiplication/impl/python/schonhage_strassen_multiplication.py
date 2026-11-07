# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schonhage-strassen-multiplication/. The authors are listed in prov/XRQ0DB.jsonl.

"""Schönhage-Strassen multiplication modulo 2^n + 1, after Brent and Zimmermann's
Algorithm FFTMulMod, with a negacyclic convolution of length K = 2^k over the
ring Z / (2^n' + 1), where 2 is a root of unity.

Elements of the rings are Python ints used only as bit strings: additions,
subtractions, shifts and masks. Every product of two ring elements goes through
the recursion, and the base case is schoolbook multiplication on limb arrays
in radix 2^8. The public functions take and return limb arrays.
"""


class Stats:
    def __init__(self) -> None:
        self.max_depth = 0
        self.base_products = 0
        self.levels: dict[int, list[tuple[int, int, int]]] = {}  # depth -> (n, K, n')


def _to_limbs(x: int, w: int = 8) -> list[int]:
    out = []
    while x:
        out.append(x & ((1 << w) - 1))
        x >>= w
    return out


def _from_limbs(d: list[int], w: int = 8) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def _schoolbook(a: list[int], b: list[int], w: int = 8) -> list[int]:
    mask = (1 << w) - 1
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j, y in enumerate(b):
            t = c[i + j] + x * y + carry
            c[i + j] = t & mask
            carry = t >> w
        c[i + len(b)] = carry
    return c


def _reduce(x: int, m: int) -> int:
    """x mod 2^m + 1 for 0 <= x, by folding: 2^m = -1."""
    mod = (1 << m) + 1
    mask = (1 << m) - 1
    sign = 1
    acc = 0
    while x:
        acc += sign * (x & mask)
        x >>= m
        sign = -sign
    while acc < 0:
        acc += mod
    while acc >= mod:
        acc -= mod
    return acc


def mul2exp(x: int, s: int, m: int) -> int:
    """x * 2^s mod 2^m + 1, for 0 <= x <= 2^m, by a shift and one subtraction."""
    mod = (1 << m) + 1
    s %= 2 * m
    if s >= m:  # 2^m = -1
        x = (mod - x) % mod
        s -= m
    t = x << s
    lo, hi = t & ((1 << m) - 1), t >> m
    r = lo - hi
    return r + mod if r < 0 else r


def _fft(a: list[int], e: int, m: int) -> list[int]:
    """DFT of a over Z/(2^m + 1) with the root omega = 2^e, len(a) a power of 2.

    Recursive radix-2; every twiddle multiplication is mul2exp.
    """
    K = len(a)
    if K == 1:
        return list(a)
    mod = (1 << m) + 1
    even = _fft(a[0::2], 2 * e, m)
    odd = _fft(a[1::2], 2 * e, m)
    out = [0] * K
    for j in range(K // 2):
        t = mul2exp(odd[j], j * e, m)
        u = even[j]
        out[j] = (u + t) % mod
        out[j + K // 2] = (u - t) % mod
    return out


def _choose(n: int) -> int:
    """The number k of the split into K = 2^k pieces: about half the length of n."""
    k = max(1, (n.bit_length() - 1) // 2)
    while n % (1 << k):
        k -= 1
    return k


def _next_size(M: int, k: int) -> int:
    """The smallest n' >= 2M + k + 1 that is a multiple of K = 2^k and of a
    power of two near its own square root, so that the next level can split it."""
    need = 2 * M + k + 1
    j = max(k, (need.bit_length() + 1) // 2)
    step = 1 << j
    return -(-need // step) * step


def mulmod(A: int, B: int, n: int, threshold: int = 64, st: Stats | None = None, depth: int = 0) -> int:
    """A * B mod 2^n + 1 for residues 0 <= A, B <= 2^n."""
    mod = (1 << n) + 1
    if st is not None:
        st.max_depth = max(st.max_depth, depth)
    if A == 1 << n:  # A = -1
        return (mod - B) % mod
    if B == 1 << n:
        return (mod - A) % mod
    k = _choose(n)
    K = 1 << k  # @line L2: K pieces of M binary digits
    M = n // K
    n2 = _next_size(M, k)  # @line L3: n' >= 2M + k + 1, a multiple of K
    if n <= threshold or n2 >= n:  # @line L1: base case, also when the pieces would not be smaller
        if st is not None:
            st.base_products += 1
        p = _from_limbs(_schoolbook(_to_limbs(A), _to_limbs(B)))
        return _reduce(p, n)
    if st is not None:
        st.levels.setdefault(depth, []).append((n, K, n2))
    mask = (1 << M) - 1
    a = [(A >> (j * M)) & mask for j in range(K)]
    b = [(B >> (j * M)) & mask for j in range(K)]
    t = n2 // K  # theta = 2^t, theta^K = 2^n' = -1
    a = [mul2exp(a[j], j * t, n2) for j in range(K)]  # @line L4: weights theta^j
    b = [mul2exp(b[j], j * t, n2) for j in range(K)]
    fa = _fft(a, 2 * t, n2)  # @line L5: two forward transforms, omega = theta^2
    fb = _fft(b, 2 * t, n2)
    fc = [mulmod(x, y, n2, threshold, st, depth + 1) for x, y in zip(fa, fb)]  # @line L6: K products mod 2^n' + 1
    c = _fft(fc, -2 * t, n2)  # @line L7: inverse transform, omega^(-1)
    mod2 = (1 << n2) + 1
    out = 0
    for j in range(K):
        cj = mul2exp(c[j], -(k + j * t), n2)  # @line L8: divide by K theta^j
        if cj >= (j + 1) << (2 * M):  # @line L9: the value is negative
            cj -= mod2
        out += cj << (j * M)  # @line L10: C = sum c_j 2^(jM)
    return out % mod


def ssa_multiply(a: list[int], b: list[int], w: int = 8, threshold: int = 64, st: Stats | None = None) -> list[int]:
    """Product of two limb arrays in radix 2^w, as len(a) + len(b) limbs.

    The product is computed modulo 2^n + 1 for an n at least the length of the
    product in binary digits, so the residue is the product itself.
    """
    if w not in (4, 8, 16):
        raise ValueError("w must be 4, 8 or 16")
    L = (len(a) + len(b)) * w
    if L == 0:
        return []
    x, y = _from_limbs(a, w), _from_limbs(b, w)
    j = (L + 1).bit_length() // 2
    n = -(-(L + 1) // (1 << j)) << j  # n > L, a multiple of 2^j with j about half the length of L
    p = mulmod(x, y, n, threshold, st)
    out = _to_limbs(p, w)
    return out + [0] * (len(a) + len(b) - len(out))
