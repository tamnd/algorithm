# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quorum-replication/. The authors are listed in prov/TKDEFR.jsonl.

"""Quorum replication of a read/write register.

n servers each store (tag, value). A client operation talks to all servers (or
to a chosen set) and waits for a quorum of replies. Three modes:

- "abd": the multi-writer form of Attiya, Bar-Noy and Dolev. A write first reads
  the largest timestamp from a read quorum and stores (ts + 1, client id). A read
  takes the largest pair from a read quorum and writes it back to a write
  quorum before it returns.
- "swmr": the single-writer form of ABD. The one writer keeps its own counter
  and skips the query phase.
- "gifford": weighted voting with plain version numbers and one vote per
  server. A write reads the largest version from a read quorum and stores
  version + 1; a read returns the value with the largest version and does not
  write back.

The flag writeback=False removes the second phase of an ABD read, to show why
it is needed. The module also has a Wing and Gong style linearizability check.
"""

import heapq
import random
from typing import Callable, Hashable


class Sim:
    def __init__(self, seed: int, delay: tuple[int, int] = (1, 10)) -> None:
        self.rng = random.Random(seed)
        self.delay = delay
        self.now = 0
        self.heap: list = []
        self.seq = 0
        self.stamp_no = 0
        self.crashed: set[Hashable] = set()
        self.handlers: dict[Hashable, Callable] = {}
        self.messages = 0
        self.slow: dict[tuple, int] = {}  # (src, dst) -> fixed delay, for constructed runs

    def stamp(self) -> int:
        self.stamp_no += 1
        return self.stamp_no

    def at(self, t: int, fn: Callable[[], None]) -> None:
        heapq.heappush(self.heap, (t, self.seq, fn))
        self.seq += 1

    def send(self, src: Hashable, dst: Hashable, msg: tuple) -> None:
        if src in self.crashed:
            return
        self.messages += 1
        d = self.slow.get((src, dst))
        t = self.now + (d if d is not None else self.rng.randint(*self.delay))
        self.at(t, lambda: self.deliver(dst, src, msg))

    def deliver(self, dst: Hashable, src: Hashable, msg: tuple) -> None:
        if dst not in self.crashed:
            self.handlers[dst](src, msg)

    def run(self, until: int = 10 ** 7) -> None:
        while self.heap and self.heap[0][0] <= until:
            t, _, fn = heapq.heappop(self.heap)
            self.now = t
            fn()


class Server:
    def __init__(self, sid: int, sim: Sim, tag0: tuple) -> None:
        self.sid = sid
        self.sim = sim
        self.tag = tag0
        self.value: object = None

    def on_message(self, src: Hashable, msg: tuple) -> None:
        if msg[0] == "QUERY":
            self.sim.send(("S", self.sid), src, ("QREP", msg[1], self.tag, self.value))
        elif msg[0] == "STORE":
            _, opid, tag, value = msg
            if tag > self.tag:  # @line L8
                self.tag, self.value = tag, value
            self.sim.send(("S", self.sid), src, ("SACK", opid))  # @line L9


class Client:
    def __init__(self, cid: int, sim: Sim, n: int, ops: list[dict], history: list,
                 mode: str, r: int, w: int, writeback: bool = True) -> None:
        self.cid = cid
        self.sim = sim
        self.n = n
        self.ops = list(ops)
        self.history = history
        self.mode = mode
        self.r = r
        self.w = w
        self.writeback = writeback
        self.ts = 0  # the writer's counter in "swmr" mode
        self.opid = 0
        self.need = 0
        self.replies: list = []
        self.cont: Callable | None = None
        self.rec: dict | None = None

    def me(self) -> tuple:
        return ("C", self.cid)

    def phase(self, msg: tuple, targets: list[int] | None, need: int, cont: Callable) -> None:
        self.opid += 1
        self.replies = []
        self.need = need
        self.cont = cont
        for s in (targets if targets is not None else range(self.n)):
            self.sim.send(self.me(), ("S", s), (msg[0], self.opid) + msg[1:])

    def on_message(self, src: Hashable, msg: tuple) -> None:
        if msg[1] != self.opid or self.cont is None:
            return
        self.replies.append(msg)
        if len(self.replies) == self.need:
            cont, self.cont = self.cont, None
            cont(self.replies)

    def start(self) -> None:
        if not self.ops:
            return
        op = self.ops.pop(0)
        rec = {"op": op["op"], "arg": op.get("arg"), "inv": self.sim.stamp(), "res": None, "out": None}
        self.history.append(rec)
        self.rec = rec
        q1, q2 = op.get("q1"), op.get("q2")
        if op["op"] == "write":
            if self.mode == "swmr":
                self.ts += 1
                self.store((self.ts, self.cid), rec["arg"], q2)
            else:
                self.phase(("QUERY",), q1, self.r, lambda reps: self.write_tag(reps, q2))  # @line L1
        else:
            self.phase(("QUERY",), q1, self.r, lambda reps: self.read_pick(reps, q2))  # @line L4

    def write_tag(self, reps: list, q2: list[int] | None) -> None:
        ts = max(m[2][0] for m in reps)
        tag = (ts + 1,) if self.mode == "gifford" else (ts + 1, self.cid)  # @line L2
        self.store(tag, self.rec["arg"], q2)

    def store(self, tag: tuple, value: object, q2: list[int] | None) -> None:
        self.phase(("STORE", tag, value), q2, self.w, lambda reps: self.finish(None))  # @line L3

    def read_pick(self, reps: list, q2: list[int] | None) -> None:
        best = reps[0]
        for m in reps[1:]:
            if m[2] > best[2]:
                best = m
        tag, value = best[2], best[3]  # @line L5
        if self.mode == "gifford" or not self.writeback:
            self.finish(value)
        else:
            self.phase(("STORE", tag, value), q2, self.w, lambda reps: self.finish(value))  # @line L6

    def finish(self, out: object) -> None:
        rec = self.rec
        rec["res"] = self.sim.stamp()
        rec["out"] = out  # @line L7
        self.sim.at(self.sim.now + self.sim.rng.randint(0, 3), self.start)


def make(seed: int, n: int, mode: str = "abd", r: int | None = None, w: int | None = None,
         writeback: bool = True) -> dict:
    sim = Sim(seed)
    maj = n // 2 + 1
    r = maj if r is None else r
    w = maj if w is None else w
    tag0 = (0,) if mode == "gifford" else (0, -1)
    servers = [Server(i, sim, tag0) for i in range(n)]
    for s in servers:
        sim.handlers[("S", s.sid)] = s.on_message
    return {"sim": sim, "servers": servers, "n": n, "mode": mode, "r": r, "w": w,
            "writeback": writeback, "history": []}


def add_client(sys: dict, cid: int, ops: list[dict], start: int | None = None) -> Client:
    sim = sys["sim"]
    c = Client(cid, sim, sys["n"], ops, sys["history"], sys["mode"], sys["r"], sys["w"], sys["writeback"])
    sim.handlers[c.me()] = c.on_message
    sim.at(sim.rng.randint(0, 5) if start is None else start, c.start)
    return c


def run(seed: int, n: int, ops_per_client: list[list[dict]], mode: str = "abd",
        r: int | None = None, w: int | None = None, writeback: bool = True,
        crash: dict[int, int] | None = None) -> dict:
    sys = make(seed, n, mode, r, w, writeback)
    for cid, ops in enumerate(ops_per_client):
        add_client(sys, cid, ops)
    sim = sys["sim"]
    for s, t in (crash or {}).items():
        sim.at(t, lambda s=s: sim.crashed.add(("S", s)))
    sim.run()
    return sys


# ---------------------------------------------------------------- checker

def linearizable(history: list[dict], init: object = None) -> bool:
    """Wing and Gong search for a register history (op, arg, inv, res, out)."""
    ops = [h for h in history if not (h["res"] is None and h["op"] == "read")]
    inf = float("inf")
    res = [h["res"] if h["res"] is not None else inf for h in ops]
    n = len(ops)
    must = sum(1 << i for i in range(n) if ops[i]["res"] is not None)
    seen: set = set()

    def search(done: int, val: object) -> bool:
        if done & must == must:
            return True
        if (done, val) in seen:
            return False
        seen.add((done, val))
        first = min((res[j] for j in range(n) if not done >> j & 1), default=inf)
        for i in range(n):
            if done >> i & 1 or ops[i]["inv"] > first:
                continue
            o = ops[i]
            if o["op"] == "write":
                if search(done | 1 << i, o["arg"]):
                    return True
            elif o["out"] == val and search(done | 1 << i, val):
                return True
        return False

    return search(0, init)


# ---------------------------------------------------------------- constructed runs

def inversion_run(writeback: bool) -> dict:
    """n = 3. The writer's STORE reaches S0 at once and S1, S2 late. Reader A reads
    from {S0, S1} and finishes; then reader B reads from {S1, S2}."""
    sys = make(0, 3, "swmr", writeback=writeback)
    sim = sys["sim"]
    for s in (1, 2):
        sim.slow[(("C", 0), ("S", s))] = 1000
    sim.slow[(("C", 0), ("S", 0))] = 1
    add_client(sys, 0, [{"op": "write", "arg": 1}], start=0)
    add_client(sys, 1, [{"op": "read", "q1": [0, 1], "q2": [0, 1]}], start=20)
    sim.run(100)
    add_client(sys, 2, [{"op": "read", "q1": [1, 2], "q2": [1, 2]}], start=sim.now + 1)
    sim.run(200)
    return sys


def stale_read_run(n: int, r: int, w: int) -> dict:
    """Gifford mode, R + W <= N: the write quorum is the first w servers, the read
    quorum the last r servers, and they do not meet."""
    sys = make(0, n, "gifford", r, w)
    sim = sys["sim"]
    add_client(sys, 0, [{"op": "write", "arg": 1, "q1": list(range(n - r, n)), "q2": list(range(w))}], start=0)
    sim.run(100)
    add_client(sys, 1, [{"op": "read", "q1": list(range(n - r, n))}], start=sim.now + 1)
    sim.run(200)
    return sys


def disjoint_writes_run(mode: str) -> dict:
    """N = 4, R = 3, W = 2 (R + W > N but 2W = N). Two writers read version 0 at
    the same time and store to the disjoint quorums {S0, S1} and {S2, S3}. Then
    three reads, one after another. Each read takes the first reply among those
    with the largest tag; the delays make S0, then S2, then S0 answer first."""
    sys = make(0, 4, mode, 3, 2)
    sim = sys["sim"]
    add_client(sys, 0, [{"op": "write", "arg": "a", "q1": [0, 1, 2], "q2": [0, 1]}], start=0)
    add_client(sys, 1, [{"op": "write", "arg": "b", "q1": [1, 2, 3], "q2": [2, 3]}], start=0)
    sim.run(100)
    t = sim.now
    for i, first in enumerate([0, 2, 0]):
        cid = 2 + i
        for s in range(4):
            sim.slow[(("C", cid), ("S", s))] = 1
            sim.slow[(("S", s), ("C", cid))] = 1 if s == first else 5
        add_client(sys, cid, [{"op": "read", "q1": [0, 1, 2, 3], "q2": [0, 1, 2, 3]}], start=t + 1)
        sim.run(t + 60)
        t = sim.now
    return sys
