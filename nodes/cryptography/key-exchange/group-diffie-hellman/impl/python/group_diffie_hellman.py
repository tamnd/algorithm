# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-diffie-hellman/. The authors are listed in prov/YAZFG4.jsonl.
"""GDH.2 of Steiner, Tsudik and Waidner (ACM CCS 1996): an upflow in which
each member raises a growing list of partial keys, then one broadcast from
the last member. The key is g^(x_1 x_2 ... x_n).

The group is the subgroup of quadratic residues modulo the 1024-bit safe
prime of RFC 5054, Appendix A, with g = 4 of prime order q. The protocol is
unauthenticated: it resists only a passive attacker.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L7 match the pseudocode on the page.
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


class Member:
    def __init__(self, index: int, rng=secrets.randbelow):
        self.i = index
        self.x = 1 + rng(Q - 1)
        self.exps = 0
        self.key = None

    def _exp(self, base: int, e: int) -> int:
        if not in_group(base):
            raise ValueError("value outside the group")
        self.exps += 1
        return pow(base, e, P)

    def upflow(self, flow):
        """flow = (partials, cardinal). partials[k] lacks x_k; cardinal has every x so far."""
        partials, card = flow
        out = [self._exp(v, self.x) for v in partials] + [card]           # @line L2
        return out, self._exp(card, self.x)                               # @line L3

    def last(self, flow):
        partials, card = flow
        self.key = self._exp(card, self.x)                                # @line L5
        return [self._exp(v, self.x) for v in partials]                   # @line L6

    def finish(self, broadcast):
        self.key = self._exp(broadcast[self.i], self.x)                   # @line L7


def run(n: int, rng=secrets.randbelow):
    """Run GDH.2 with n >= 2 members. Returns (members, rounds, messages)."""
    members = [Member(i, rng) for i in range(n)]
    flow = ([], G)                                                        # @line L1: M_1 starts from g
    rounds = messages = 0
    for m in members[:-1]:
        flow = m.upflow(flow)                                             # @line L4: send to the next member
        rounds, messages = rounds + 1, messages + 1
    broadcast = members[-1].last(flow)
    rounds, messages = rounds + 1, messages + 1
    for m in members[:-1]:
        m.finish(broadcast)
    return members, rounds, messages
