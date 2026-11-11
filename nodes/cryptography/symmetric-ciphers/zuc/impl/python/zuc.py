# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zuc/. The authors are listed in prov/MQAR4N.jsonl.

"""The ZUC-128 keystream generator, ETSI/SAGE 128-EEA3 & 128-EIA3 Document 2, version 1.6, for study only.

This is the current ZUC (versions 1.5 and 1.6 have the same algorithm), not the
withdrawn version 1.4. The code is not constant time as Python runs it (it uses
table lookups and data-dependent branches) and must not protect real data.
"""

P = (1 << 31) - 1  # the prime 2^31 - 1
M32 = 0xFFFFFFFF

# Section 3.5: the 15-bit constants d_0 .. d_15, written in binary in the specification.
D = [
    int(b, 2)
    for b in (
        "100010011010111", "010011010111100", "110001001101011", "001001101011110",
        "101011110001001", "011010111100010", "111000100110101", "000100110101111",
        "100110101111000", "010111100010011", "110101111000100", "001101011110001",
        "101111000100110", "011110001001101", "111100010011010", "100011110101100",
    )
]

# Section 3.4.1, Tables 3.1 and 3.2: the S-boxes S0 and S1 (S2 = S0, S3 = S1).
S0 = bytes.fromhex(
    "3e725b47cae0003304d1549809b96dcb7b1bf932af9d6aa5b82dfc1d08530390"
    "4d4e8499e4ced991ddb685488b296eaccdc1f81e734369c6b5bdfd396320d438"
    "767db2a7cfed57c5f32cbb142106559be3ef5e314f7f5aa40d8251495fba581c"
    "4a16d517a892241f8cffd8ae2e01d3ad3b4bda46ebc9de9a8f87d73a806f2fc8"
    "b1b437f70a2213287ccc3c89c7c3965607bf7ef00b2b975235417961a64c10fe"
    "bc2695888ab0a3fbc01894f2e1e5e95dd0dc1166645cec59427512f5749caa23"
    "0e86abbe2a02e767e644a26cc2939ff1f6fa36d250689e6271153dd640c4e20f"
    "8e83776b25053f0c30ea70b7a1e8a9658d271adb81b3a0f4457a19dfee783460"
)
S1 = bytes.fromhex(
    "55c263713bc847869f3cda5b29aafd778cc5940ca61a1300e3a8167240f9f842"
    "4426689681d9453e1076c6a78b3943e13ab5562ac06db3052266bfdc0bfa6248"
    "dd20110636c9c1cff62752bb69f5d4877f844cd29c57a4bc4f9adffed68d7aeb"
    "2b53d85ca11417fb23d57d3067730809eeb7703f61b2198e4ee54b938f5ddba9"
    "adf1ae2ecb0dfcf42d466e1d97e8d1e94d37a5755e839eab829db91ce0cd4989"
    "01b6bd5824a25f387899159050b895e4d091c7ceed0fb46fa0ccf0024a79c3de"
    "a3efea51e66b18ec1b2c80f774e7ff215a6a541e41319235c433070aba7e0e34"
    "88b1987cf33d606c7bcad31f3265042864be859b2f598ad7b025acaf1203e2f2"
)


def _rotl(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & M32


def l1(x: int) -> int:
    return x ^ _rotl(x, 2) ^ _rotl(x, 10) ^ _rotl(x, 18) ^ _rotl(x, 24)


def l2(x: int) -> int:
    return x ^ _rotl(x, 8) ^ _rotl(x, 14) ^ _rotl(x, 22) ^ _rotl(x, 30)


def sbox(x: int) -> int:
    """The 32x32 S-box S = (S0, S1, S0, S1), applied to the bytes from the most significant."""
    return (S0[x >> 24] << 24) | (S1[(x >> 16) & 0xFF] << 16) | (S0[(x >> 8) & 0xFF] << 8) | S1[x & 0xFF]


def bit_reorganization(s: list[int]) -> tuple[int, int, int, int]:
    """Section 3.3. H is bits 30..15 and L is bits 15..0 of a 31-bit cell."""

    def hi(i: int) -> int:
        return (s[i] >> 15) & 0xFFFF

    def lo(i: int) -> int:
        return s[i] & 0xFFFF

    return (hi(15) << 16) | lo(14), (lo(11) << 16) | hi(9), (lo(7) << 16) | hi(5), (lo(2) << 16) | hi(0)


def nonlinear_f(x0: int, x1: int, x2: int, r: list[int]) -> int:
    """Section 3.4: return W and update the memory cells r = [R1, R2]."""
    w = ((x0 ^ r[0]) + r[1]) & M32  # @line L11
    w1 = (r[0] + x1) & M32  # @line L12
    w2 = r[1] ^ x2  # @line L12
    r[0] = sbox(l1(((w1 & 0xFFFF) << 16) | (w2 >> 16)))  # @line L13
    r[1] = sbox(l2(((w2 & 0xFFFF) << 16) | (w1 >> 16)))  # @line L13
    return w


def lfsr_clock(s: list[int], u: int) -> None:
    """Section 3.2: initialization mode with input u, or working mode with u = 0."""
    v = ((1 << 15) * s[15] + (1 << 17) * s[13] + (1 << 21) * s[10] + (1 << 20) * s[4] + (1 + (1 << 8)) * s[0] + u) % P  # @line L14
    s[:] = s[1:] + [v if v != 0 else P]  # @line L15


def zuc_keystream(key: bytes, iv: bytes, n: int) -> list[int]:
    """Return the 32-bit keystream words Z_1 .. Z_n.

    Precondition: 16-byte key and 16-byte IV. Cost: Theta(33 + n) clocks, each a
    constant number of word operations and 8 byte S-box lookups.
    """
    if len(key) != 16 or len(iv) != 16:
        raise ValueError("ZUC needs a 128-bit key and a 128-bit IV")
    s = [(key[i] << 23) | (D[i] << 8) | iv[i] for i in range(16)]  # @line L1
    r = [0, 0]  # @line L1
    for _ in range(32):  # @line L2
        x0, x1, x2, _x3 = bit_reorganization(s)  # @line L3
        w = nonlinear_f(x0, x1, x2, r)  # @line L3
        lfsr_clock(s, w >> 1)  # @line L4
    x0, x1, x2, _x3 = bit_reorganization(s)  # @line L5
    nonlinear_f(x0, x1, x2, r)  # @line L5
    lfsr_clock(s, 0)  # @line L6
    out = []
    for _ in range(n):  # @line L7
        x0, x1, x2, x3 = bit_reorganization(s)  # @line L8
        out.append(nonlinear_f(x0, x1, x2, r) ^ x3)  # @line L9
        lfsr_clock(s, 0)  # @line L10
    return out
