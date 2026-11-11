# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-key-agreement-problem/. The authors are listed in prov/67D8KM.jsonl.
"""A common test harness for group key agreement. A Meter counts modular
exponentiations, messages and rounds, so the costs of the classic protocols
can be compared on the same group:

* leader: a non-contributory baseline. One member picks the key and sends it
  to each other member under a pairwise Diffie-Hellman key.
* itw: the Ingemarsson-Tang-Wong ring (1982), n - 1 rounds.
* gdh2: GDH.2 of Steiner, Tsudik and Waidner (1996), n rounds.
* bd: Burmester-Desmedt (1994), two rounds.

All four are unauthenticated: they resist only a passive attacker. The group
is the subgroup of quadratic residues modulo a toy 128-bit safe prime.
Multiplications and inversions are not counted, only exponentiations.

For study only. The code is not constant time, and it must not protect real
data.
"""

import hashlib
import secrets

P = 255211775190703847597530955573826162347   # a toy safe prime, p = 2q + 1
Q = (P - 1) // 2
G = 4


class Meter:
    def __init__(self, n: int):
        self.n = n
        self.exps = [0] * n          # exponentiations per member
        self.messages = 0
        self.rounds = 0

    def exp(self, member: int, base: int, e: int) -> int:
        self.exps[member] += 1
        return pow(base, e, P)

    def round(self, messages: int):
        self.rounds += 1
        self.messages += messages


def secrets_for(n: int, rng=secrets.randbelow):
    return [1 + rng(Q - 1) for _ in range(n)]


def leader(xs, chosen: int | None = None, rng=secrets.randbelow):
    """Member 0 picks K and wraps it for each member. Returns (keys, meter)."""
    n, m = len(xs), Meter(len(xs))
    pub = [m.exp(i, G, xs[i]) for i in range(n)]
    m.round(n)                                          # everyone broadcasts g^x_i
    K = chosen if chosen is not None else rng(2**128)
    wrapped = {}
    for i in range(1, n):
        k = m.exp(0, pub[i], xs[0])
        wrapped[i] = K ^ int.from_bytes(hashlib.sha256(k.to_bytes(16, "big")).digest()[:16], "big")
    m.round(1)                                          # one broadcast with n - 1 wrapped keys
    keys = [K]
    for i in range(1, n):
        k = m.exp(i, pub[0], xs[i])
        keys.append(wrapped[i] ^ int.from_bytes(hashlib.sha256(k.to_bytes(16, "big")).digest()[:16], "big"))
    return keys, m


def itw(xs):
    """Ring: in round j, member i raises what it got from member i - 1 and passes it on."""
    n, m = len(xs), Meter(len(xs))
    held = [m.exp(i, G, xs[i]) for i in range(n)]
    for _ in range(n - 1):
        m.round(n)
        held = [m.exp(i, held[(i - 1) % n], xs[i]) for i in range(n)]
    return held, m


def gdh2(xs):
    """Upflow of growing lists, then one broadcast from the last member."""
    n, m = len(xs), Meter(len(xs))
    partials, card = [], G                 # partials[k]: the product without member k; card: the product so far
    for i in range(n - 1):
        new_partials = [m.exp(i, v, xs[i]) for v in partials] + [card]
        card = m.exp(i, card, xs[i])
        partials = new_partials
        m.round(1)
    last = n - 1
    keys = [None] * n
    keys[last] = m.exp(last, card, xs[last])
    broadcast = [m.exp(last, v, xs[last]) for v in partials]
    m.round(1)
    for i in range(n - 1):
        keys[i] = m.exp(i, broadcast[i], xs[i])
    return keys, m


def bd(xs):
    """Round 1: z_i = g^x_i. Round 2: X_i = (z_{i+1} / z_{i-1})^x_i. Then the telescoping product."""
    n, m = len(xs), Meter(len(xs))
    z = [m.exp(i, G, xs[i]) for i in range(n)]
    m.round(n)
    X = [m.exp(i, z[(i + 1) % n] * pow(z[(i - 1) % n], P - 2, P) % P, xs[i]) for i in range(n)]
    m.round(n)
    keys = []
    for i in range(n):
        y = m.exp(i, z[(i - 1) % n], xs[i])      # g^(x_{i-1} x_i)
        K = y
        for j in range(1, n):
            y = y * X[(i + j - 1) % n] % P       # g^(x_{i+j-1} x_{i+j})
            K = K * y % P
        keys.append(K)
    return keys, m
