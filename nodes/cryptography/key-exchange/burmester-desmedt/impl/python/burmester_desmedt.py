# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burmester-desmedt/. The authors are listed in prov/BRF2MN.jsonl.
"""The Burmester-Desmedt conference key protocol (Eurocrypt 1994), the
broadcast version: two rounds, and the key is
g^(x_1 x_2 + x_2 x_3 + ... + x_n x_1).

Round 1: member i broadcasts z_i = g^x_i. Round 2: member i broadcasts
X_i = (z_{i+1} / z_{i-1})^x_i. Each member then forms the key with a
telescoping product that needs one more exponentiation and 2(n - 1)
multiplications.

The group is the subgroup of quadratic residues modulo the 1024-bit safe
prime of RFC 5054, Appendix A, with g = 4 of prime order q. This is the
unauthenticated protocol: it resists only a passive attacker. Katz and Yung
(Crypto 2003) add authentication with a signature compiler.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L6 match the pseudocode on the page.
"""

import secrets

P = int(
    "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C"
    "9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE4"
    "8E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B29"
    "7BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9A"
    "FD5138FE8376435B9FC61D2FC0EB06E3",
    16,
)
Q = (P - 1) // 2
G = 4


def in_group(X: int) -> bool:
    return 1 < X < P and pow(X, Q, P) == 1


def inv(a: int) -> int:
    return pow(a, P - 2, P)


def round1(x: int) -> int:
    return pow(G, x, P)                                                 # @line L1


def check_broadcast(values, allow_one: bool = False):
    """Every member checks every received value. All members receive the same
    broadcast, so the simulation checks each value once."""
    if not all(in_group(v) or (allow_one and v == 1) for v in values):
        raise ValueError("value outside the group")


def round2(i: int, x: int, z) -> int:
    n = len(z)
    return pow(z[(i + 1) % n] * inv(z[(i - 1) % n]) % P, x, P)          # @line L2


def key(i: int, x: int, z, X) -> int:
    n = len(z)
    y = pow(z[(i - 1) % n], x, P)                                       # @line L3: g^(x_{i-1} x_i)
    K = y
    for j in range(1, n):                                               # @line L4
        y = y * X[(i + j - 1) % n] % P                                  # @line L5: g^(x_{i+j-1} x_{i+j})
        K = K * y % P                                                   # @line L6
    return K


def run(n: int, rng=secrets.randbelow):
    """Run BD with n >= 2 members. Returns (secrets, keys)."""
    xs = [1 + rng(Q - 1) for _ in range(n)]
    z = [round1(x) for x in xs]
    check_broadcast(z)
    X = [round2(i, xs[i], z) for i in range(n)]
    check_broadcast(X, allow_one=(n == 2))      # with n = 2, X_i = 1 always
    return xs, [key(i, xs[i], z, X) for i in range(n)]
