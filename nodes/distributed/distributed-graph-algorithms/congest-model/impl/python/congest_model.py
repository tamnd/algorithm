# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/congest-model/. The authors are listed in prov/ECCJVR.jsonl.

"""A synchronous round simulator that enforces the CONGEST bandwidth limit.

The network is an adjacency list adj: adj[v][i] is the neighbour of v behind
port i of v. Node v has a unique identifier ids[v] and an input inputs[v].

An algorithm is an object with three methods:

    init(ident, inp, deg)      -> the initial state of a node
    send(state, rnd)           -> one message per port; None means no message
    receive(state, rnd, inbox) -> the new state; inbox[i] arrived on port i

In CONGEST mode with constant c, every message is encoded with a fixed
self-delimiting code (see bits()) and must have at most
c * ceil(log2(n + 1)) bits; a longer message raises CongestViolation. LOCAL
mode only records the sizes.

Algorithms here:
    SyncBFS       distances from the node with input 1; messages are one integer
    SmallestFirst every node learns all identifiers; each round a node sends the
                  smallest identifier that it knows and has not sent yet
    Gather        every node learns the whole graph; fine in LOCAL, too big for CONGEST

and dumbbell(), with the counting lower bound for learning all identifiers.
"""

import math


class CongestViolation(Exception):
    pass


def gamma_len(k: int) -> int:
    return 2 * (k.bit_length() - 1) + 1


def bits(msg: object) -> int:
    """2-bit type tag per value; integers in zigzag gamma code; containers have a gamma length prefix."""
    total = 0
    stack = [msg]
    while stack:
        x = stack.pop()
        total += 2
        if isinstance(x, bool):
            total += 1
        elif isinstance(x, int):
            z = 2 * x if x >= 0 else -2 * x - 1
            total += gamma_len(z + 1)
        elif isinstance(x, (tuple, list, frozenset)):
            total += gamma_len(len(x) + 1)
            stack.extend(x)
        else:
            raise TypeError(f"cannot encode {type(x).__name__}")
    return total


def budget(n: int, c: int) -> int:
    """c * ceil(log2(n + 1)) bits per message per edge per round."""
    return c * max(1, n.bit_length())


def back_ports(adj):
    where = [{w: j for j, w in enumerate(nbrs)} for nbrs in adj]
    return [[where[w][v] for w in adj[v]] for v in range(len(adj))]


def run(adj, ids, inputs, alg, rounds, mode="CONGEST", c=4, stop=None):
    """Returns (states, stats); stats has rounds, messages, total_bits, max_bits."""
    n = len(adj)
    assert len(set(ids)) == n
    back = back_ports(adj)
    limit = budget(n, c) if mode == "CONGEST" else None
    states = [alg.init(ids[v], inputs[v], len(adj[v])) for v in range(n)]
    stats = {"rounds": 0, "messages": 0, "total_bits": 0, "max_bits": 0}
    for rnd in range(1, rounds + 1):
        if stop is not None and stop(states):
            break
        inbox = [[None] * len(adj[v]) for v in range(n)]
        for v in range(n):
            for i, msg in enumerate(alg.send(states[v], rnd)):
                if msg is None:
                    continue
                b = bits(msg)
                if limit is not None and b > limit:
                    raise CongestViolation(f"round {rnd}, node {v}, port {i}: {b} bits > {limit}")
                stats["messages"] += 1
                stats["total_bits"] += b
                stats["max_bits"] = max(stats["max_bits"], b)
                inbox[adj[v][i]][back[v][i]] = msg
        states = [alg.receive(states[v], rnd, inbox[v]) for v in range(n)]
        stats["rounds"] = rnd
    if stop is not None and not stop(states):
        raise RuntimeError("the round limit was reached")
    return states, stats


class SyncBFS:
    def init(self, ident, inp, deg):
        return (deg, 0 if inp == 1 else None, inp == 1)

    def send(self, state, rnd):
        deg, d, fresh = state
        return [d] * deg if fresh else [None] * deg

    def receive(self, state, rnd, inbox):
        deg, d, _ = state
        if d is None:
            heard = [x for x in inbox if x is not None]
            if heard:
                return (deg, min(heard) + 1, True)
        return (deg, d, False)


class SmallestFirst:
    """State: (deg, known, sent), both frozensets of identifiers."""

    def init(self, ident, inp, deg):
        return (deg, frozenset([ident]), frozenset())

    @staticmethod
    def pick(state):
        rest = state[1] - state[2]
        return min(rest) if rest else None

    def send(self, state, rnd):
        return [self.pick(state)] * state[0]

    def receive(self, state, rnd, inbox):
        deg, known, sent = state
        x = self.pick(state)
        if x is not None:
            sent = sent | {x}
        return (deg, known | {y for y in inbox if y is not None}, sent)


class Gather:
    """Learn the whole graph (see the LOCAL model page); messages grow with the graph."""

    def init(self, ident, inp, deg):
        return (ident, inp, deg, {})

    def send(self, state, rnd):
        ident, _, deg, known = state
        if rnd == 1:
            return [ident] * deg
        return [tuple(sorted(known.items()))] * deg

    def receive(self, state, rnd, inbox):
        ident, inp, deg, known = state
        known = dict(known)
        if rnd == 1:
            known[ident] = (inp, tuple(inbox))
        else:
            for msg in inbox:
                for u, rec in msg:
                    known[u] = rec
        return (ident, inp, deg, known)


def dumbbell(n: int) -> list[list[int]]:
    """Two stars with n // 2 nodes each; the centres 0 and n // 2 are joined by the bridge."""
    h = n // 2
    adj = [[] for _ in range(2 * h)]
    for c0 in (0, h):
        for v in range(c0 + 1, c0 + h):
            adj[c0].append(v)
            adj[v].append(c0)
    adj[0].append(h)
    adj[h].append(0)
    return adj


def all_ids_lower_bound(n: int, big_n: int, b: int) -> float:
    """Rounds needed on dumbbell(n) to learn all identifiers from {1..big_n} with b-bit messages.

    The right side's final state is fixed by the messages that cross the
    bridge to it, at most 2^(b+1) choices per round, and it must tell apart
    all choices of the left identifiers: binom(big_n - n/2, n/2) of them.
    """
    h = n // 2
    return math.log2(math.comb(big_n - h, h)) / (b + 1)
