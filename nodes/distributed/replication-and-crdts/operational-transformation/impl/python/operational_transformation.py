# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operational-transformation/. The authors are listed in prov/C2XWTY.jsonl.

"""Operational transformation on strings, with Jupiter-style server-based control.

Operations are ("ins", p, ch, uid), ("del", p) and ("nop",), with 0-based
positions. transform(a, b) returns a version of a to run after b, when a and b
were both made on the same state. It is the inclusion transform of Ressel et
al. (1996): positions shift past the other operation, ties between two inserts
at one position go to the smaller uid, and two deletes of one character leave
a nop. It satisfies TP1, which is all that Jupiter needs.

Jupiter (Nichols, Curtis, Dixon and Lamping 1995) runs a two-party protocol
on each client-server link. Each side counts the messages it has sent (my)
and received (other) and keeps its unacknowledged messages. An incoming
message says how many of our messages its sender had seen, so we drop those,
and transform the incoming operation against the rest. The server applies
each client operation, then sends it on the links to the other clients.
Links must be FIFO.
"""

from collections import deque
from typing import Any

Op = tuple


def apply(doc: str, op: Op) -> str:
    if op[0] == "ins":
        return doc[: op[1]] + op[2] + doc[op[1]:]
    if op[0] == "del":
        return doc[: op[1]] + doc[op[1] + 1:]
    return doc


def transform(a: Op, b: Op) -> Op:
    """a transformed against b: the effect of a, to run on a state where b ran."""
    if a[0] == "nop" or b[0] == "nop":  # @line L1
        return a
    if a[0] == "ins" and b[0] == "ins":
        if a[1] < b[1] or (a[1] == b[1] and a[3] < b[3]):  # @line L2
            return a
        return ("ins", a[1] + 1, a[2], a[3])  # @line L3
    if a[0] == "ins":  # b deletes
        return a if a[1] <= b[1] else ("ins", a[1] - 1, a[2], a[3])  # @line L4
    if b[0] == "ins":  # a deletes
        return a if a[1] < b[1] else ("del", a[1] + 1)  # @line L5
    if a[1] < b[1]:  # both delete
        return a
    if a[1] > b[1]:
        return ("del", a[1] - 1)  # @line L6
    return ("nop",)  # @line L7


def xform(c: Op, s: Op) -> tuple[Op, Op]:
    """The pair (c', s') with s then c' equal to c then s'."""
    return transform(c, s), transform(s, c)


class Link:
    """One end of a Jupiter link."""

    def __init__(self) -> None:
        self.my = 0
        self.other = 0
        self.out: list[tuple[int, Op]] = []  # (my count when sent, op)

    def send(self, op: Op) -> tuple[Op, int, int]:
        msg = (op, self.my, self.other)  # @line L8
        self.out.append((self.my, op))
        self.my += 1
        return msg

    def receive(self, msg: tuple[Op, int, int]) -> Op:
        op, their_my, their_other = msg
        self.out = [(k, o) for k, o in self.out if k >= their_other]  # @line L9
        assert their_my == self.other, "links are FIFO"
        for idx, (k, o) in enumerate(self.out):  # @line L10
            op, o2 = xform(op, o)  # @line L11
            self.out[idx] = (k, o2)  # @line L12
        self.other += 1
        return op  # @line L13


class Client:
    def __init__(self, uid: int, doc: str = "") -> None:
        self.uid, self.doc, self.link = uid, doc, Link()

    def insert(self, p: int, ch: str) -> tuple:
        op = ("ins", p, ch, self.uid)
        self.doc = apply(self.doc, op)
        return self.link.send(op)

    def delete(self, p: int) -> tuple:
        op = ("del", p)
        self.doc = apply(self.doc, op)
        return self.link.send(op)

    def receive(self, msg: tuple) -> None:
        self.doc = apply(self.doc, self.link.receive(msg))

    def check_invariant(self) -> None:
        assert self.link.other >= 0 and len(self.link.out) <= self.link.my


class Server:
    def __init__(self, n: int, doc: str = "") -> None:
        self.doc = doc
        self.links = [Link() for _ in range(n)]

    def receive(self, k: int, msg: tuple) -> list[tuple[int, tuple]]:
        """Apply a message from client k. Returns the messages for the other clients."""
        op = self.links[k].receive(msg)
        self.doc = apply(self.doc, op)
        return [(j, l.send(op)) for j, l in enumerate(self.links) if j != k]


def simulate(seed: int, n: int, nops: int, start: str = "") -> list[str]:
    """Random edits by n clients over FIFO links. Returns the final documents, server last."""
    import random

    rng = random.Random(seed)
    clients = [Client(i, start) for i in range(n)]
    server = Server(n, start)
    up = [deque() for _ in range(n)]  # client -> server
    down = [deque() for _ in range(n)]  # server -> client
    made = 0
    while made < nops or any(up) or any(down):
        busy = [("up", i) for i in range(n) if up[i]] + [("down", i) for i in range(n) if down[i]]
        if made < nops and (not busy or rng.random() < 0.4):
            c = clients[rng.randrange(n)]
            if c.doc and rng.random() < 0.3:
                up[c.uid].append(c.delete(rng.randrange(len(c.doc))))
            else:
                up[c.uid].append(c.insert(rng.randrange(len(c.doc) + 1), rng.choice("abcxyz")))
            made += 1
        else:
            side, i = rng.choice(busy)
            if side == "up":
                for j, m in server.receive(i, up[i].popleft()):
                    down[j].append(m)
            else:
                clients[i].receive(down[i].popleft())
                clients[i].check_invariant()
    return [c.doc for c in clients] + [server.doc]


def dopt_puzzle(doc: str, o1: Op, o2: Op, o3: Op) -> dict[str, Any]:
    """Site 1 runs o1 then o3; site 2 runs o2, concurrent with both.

    dOPT at site 2 transforms o3 against o2 directly, although o3 was made
    after o1 and o2 was not. The correct order transforms against T(o2, o1).
    """
    site1 = apply(apply(doc, o1), o3)
    site1 = apply(site1, transform(transform(o2, o1), o3))
    site2 = apply(apply(doc, o2), transform(o1, o2))
    wrong = apply(site2, transform(o3, o2))
    right = apply(site2, transform(o3, transform(o2, o1)))
    return {"site1": site1, "dopt_site2": wrong, "correct_site2": right}


def find_dopt_divergence(alphabet: str = "ab", max_len: int = 2):
    """The first case, by a fixed search order, where dOPT leaves the two sites different."""
    import itertools

    def ops(d: str, uid: int, chars: str):
        for p in range(len(d) + 1):
            for ch in chars:
                yield ("ins", p, ch, uid)
        for p in range(len(d)):
            yield ("del", p)

    for length in range(max_len + 1):
        for doc in map("".join, itertools.product(alphabet, repeat=length)):
            for o1 in ops(doc, 1, "x"):
                for o2 in ops(doc, 2, "y"):
                    for o3 in ops(apply(doc, o1), 1, "z"):
                        r = dopt_puzzle(doc, o1, o2, o3)
                        if r["site1"] != r["dopt_site2"]:
                            return doc, o1, o2, o3, r
    return None
