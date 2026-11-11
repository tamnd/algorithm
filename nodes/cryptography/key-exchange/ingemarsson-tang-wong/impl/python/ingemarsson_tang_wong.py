# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ingemarsson-tang-wong/. The authors are listed in prov/EHMDDS.jsonl.
"""The Ingemarsson-Tang-Wong conference key protocol (IEEE Trans. Inf.
Theory, 1982), in its simplest symmetric form: the n members sit on a ring,
and in each of n - 1 rounds every member raises the value it got from its
left neighbour to its own secret and passes the result to the right. After
n - 1 rounds every member holds g^(x_1 x_2 ... x_n).

The group is the subgroup of quadratic residues modulo the 1024-bit safe
prime of RFC 5054, Appendix A, with g = 4 of prime order q. The protocol is
unauthenticated: it resists only a passive attacker.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L5 match the pseudocode on the page.
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


def run(n: int, rng=secrets.randbelow):
    """Run the ring with n >= 2 members. Returns (secrets, keys, rounds, messages, exps per member)."""
    xs = [1 + rng(Q - 1) for _ in range(n)]                          # @line L1
    exps = [1] * n
    held = [pow(G, x, P) for x in xs]                                 # @line L2
    rounds = messages = 0
    for _ in range(n - 1):                                            # @line L3
        got = [held[(i - 1) % n] for i in range(n)]                   # @line L4: member i receives from member i - 1
        if not all(in_group(v) for v in got):
            raise ValueError("value outside the group")
        held = [pow(got[i], xs[i], P) for i in range(n)]              # @line L5
        exps = [e + 1 for e in exps]
        rounds, messages = rounds + 1, messages + n
    return xs, held, rounds, messages, exps
