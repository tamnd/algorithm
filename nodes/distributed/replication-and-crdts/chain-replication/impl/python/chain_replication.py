# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chain-replication/. The authors are listed in prov/BZKFM5.jsonl.

"""Chain replication (van Renesse and Schneider, OSDI 2004) for one register.

Servers form a chain. Updates enter at the head, which numbers them; each server
applies an update and forwards it; the tail replies to the client and sends an
ack back up the chain. Queries go to the tail. A master, assumed reliable,
detects crashes (fail-stop) after a delay and repairs the chain:

- head crash: the successor becomes the head;
- tail crash: the predecessor becomes the tail and replies for its Sent entries;
- middle crash: the predecessor resends its Sent entries to the successor.

The simulation has FIFO links with random delays. Messages to a crashed server
are lost; a server ignores forwards from a server that is no longer its
predecessor. Clients retry after a timeout, and the head drops retries of
updates it already has.
"""

import heapq
import random
from dataclasses import dataclass, field


@dataclass
class Entry:
    seq: int
    rid: tuple[int, int]  # (client, request number)
    value: object


@dataclass
class Server:
    sid: int
    state: object = None
    last: int = 0
    hist: list[Entry] = field(default_factory=list)
    sent: list[Entry] = field(default_factory=list)
    done: set = field(default_factory=set)


class Chain:
    def __init__(self, n: int, seed: int, delay: tuple[int, int] = (1, 6),
                 detect: int = 20, timeout: int = 120, init: object = None,
                 read_at: str = "tail") -> None:
        self.rng = random.Random(seed)
        self.read_at = read_at  # "tail", or "any" for the broken variant that reads anywhere
        self.delay, self.detect, self.timeout = delay, detect, timeout
        self.servers = {i: Server(i, state=init) for i in range(n)}
        self.chain = list(range(n))  # the master's view; index 0 is the head
        self.crashed: set[int] = set()
        self.now = 0
        self.q: list = []
        self.k = 0
        self.link_time: dict = {}
        self.clients: dict[int, dict] = {}
        self.history: list[dict] = []
        self.messages = 0
        self.check = False

    # ---- simulation core ----
    def at(self, t: int, fn, *args) -> None:
        self.k += 1
        heapq.heappush(self.q, (t, self.k, fn, args))

    def send(self, src, dst, fn, *args) -> None:
        if isinstance(src, int) and src in self.crashed:
            return
        self.messages += 1
        t = max(self.now + self.rng.randint(*self.delay), self.link_time.get((src, dst), 0))
        self.link_time[(src, dst)] = t  # FIFO per link
        self.at(t, self._deliver, dst, fn, args)

    def _deliver(self, dst, fn, args) -> None:
        if isinstance(dst, int) and dst in self.crashed:
            return
        fn(*args)

    def run(self, until: int = 10 ** 9) -> None:
        while self.q and self.q[0][0] <= until:
            t, _, fn, args = heapq.heappop(self.q)
            self.now = t
            fn(*args)
            if self.check:
                assert self.invariants_hold(), self.now

    # ---- chain helpers (the servers' view equals the master's view) ----
    def pred(self, s: int) -> int | None:
        i = self.chain.index(s)
        return self.chain[i - 1] if i > 0 else None

    def succ(self, s: int) -> int | None:
        i = self.chain.index(s)
        return self.chain[i + 1] if i + 1 < len(self.chain) else None

    def is_tail(self, s: int) -> bool:
        return self.chain[-1] == s

    # ---- servers ----
    def client_update(self, s: int, rid: tuple[int, int], value: object) -> None:
        sv = self.servers[s]
        if s not in self.chain or self.chain[0] != s:
            return  # not the head (any more); the client will retry
        if rid in sv.done:  # @line L1
            return
        self.process(s, Entry(sv.last + 1, rid, value))  # @line L2

    def forward(self, src: int, s: int, e: Entry) -> None:
        if s not in self.chain or self.pred(s) != src:
            return  # from a server that is no longer the predecessor
        if e.seq == self.servers[s].last + 1:  # @line L3
            self.process(s, e)

    def process(self, s: int, e: Entry) -> None:
        sv = self.servers[s]
        sv.state, sv.last = e.value, e.seq  # @line L4
        sv.hist.append(e)
        sv.done.add(e.rid)
        if self.is_tail(s):
            self.send(s, ("client", e.rid[0]), self.reply, e.rid, None)  # @line L5
            p = self.pred(s)
            if p is not None:
                self.send(s, p, self.ack, s, p, e.seq)
        else:
            sv.sent.append(e)
            self.send(s, self.succ(s), self.forward, s, self.succ(s), e)  # @line L6

    def ack(self, src: int, s: int, seq: int) -> None:
        if s not in self.chain or self.succ(s) != src:
            return
        sv = self.servers[s]
        sv.sent = [e for e in sv.sent if e.seq > seq]  # @line L7
        p = self.pred(s)
        if p is not None:
            self.send(s, p, self.ack, s, p, seq)

    def query(self, s: int, rid: tuple[int, int]) -> None:
        if s not in self.chain or (self.read_at == "tail" and not self.is_tail(s)):
            return
        self.send(s, ("client", rid[0]), self.reply, rid, self.servers[s].state)  # @line L8

    # ---- master ----
    def crash(self, s: int) -> None:
        self.crashed.add(s)
        self.at(self.now + self.detect, self.repair, s)

    def repair(self, s: int) -> None:
        if s not in self.chain:
            return
        i = self.chain.index(s)
        was_tail = i == len(self.chain) - 1
        self.chain.remove(s)  # @line L9
        if not self.chain:
            return
        if was_tail:
            t = self.chain[-1]  # @line L10
            tv = self.servers[t]
            for e in tv.sent:
                self.send(t, ("client", e.rid[0]), self.reply, e.rid, None)
            if tv.sent and self.pred(t) is not None:
                self.send(t, self.pred(t), self.ack, t, self.pred(t), tv.sent[-1].seq)
            tv.sent = []
        elif i > 0:
            sm, sp = self.chain[i - 1], self.chain[i]
            for e in self.servers[sm].sent:
                self.send(sm, sp, self.forward, sm, sp, e)  # @line L11

    # ---- clients ----
    def add_client(self, c: int, ops: list[tuple[str, object]], start: int = 0) -> None:
        self.clients[c] = {"ops": ops, "i": 0, "rec": None}
        self.at(start, self._next, c)

    def _next(self, c: int) -> None:
        cl = self.clients[c]
        if cl["i"] >= len(cl["ops"]):
            return
        op, arg = cl["ops"][cl["i"]]
        rec = {"op": op, "arg": arg, "inv": self.now, "res": None, "out": None,
               "rid": (c, cl["i"])}
        cl["rec"] = rec
        self.history.append(rec)
        self._try(c, rec["rid"])

    def _try(self, c: int, rid: tuple[int, int]) -> None:
        cl = self.clients[c]
        rec = cl["rec"]
        if rec is None or rec["rid"] != rid or rec["res"] is not None or not self.chain:
            return
        if rec["op"] == "write":
            h = self.chain[0]
            self.send(("client", c), h, self.client_update, h, rid, rec["arg"])
        else:
            t = self.chain[-1] if self.read_at == "tail" else self.rng.choice(self.chain)
            self.send(("client", c), t, self.query, t, rid)
        self.at(self.now + self.timeout, self._try, c, rid)

    def reply(self, rid: tuple[int, int], out: object) -> None:
        cl = self.clients[rid[0]]
        rec = cl["rec"]
        if rec is None or rec["rid"] != rid or rec["res"] is not None:
            return  # a duplicate reply
        rec["res"], rec["out"] = self.now, out
        cl["i"] += 1
        cl["rec"] = None
        self.at(self.now + self.rng.randint(0, 4), self._next, rid[0])

    # ---- invariants ----
    def invariants_hold(self) -> bool:
        """Update propagation: along the chain each history is a prefix of the one
        before it. Sent: what a server holds and has not in Sent is at the tail."""
        live = self.chain
        if not live:
            return True
        seqs = {s: [e.seq for e in self.servers[s].hist] for s in live}
        for a, b in zip(live, live[1:]):
            ha, hb = seqs[a], seqs[b]
            if ha[: len(hb)] != hb:
                return False
        tail = seqs[live[-1]]
        for s in live:
            sent = {e.seq for e in self.servers[s].sent}
            rest = [q for q in seqs[s] if q not in sent]
            if tail[: len(rest)] != rest:
                return False
        return True


def linearizable(history: list[dict], init: object = None) -> bool:
    """Wing and Gong search for a register. Each record has op, arg, inv, res, out.

    A pending write (res None) may or may not take effect; a pending read is dropped.
    """
    ops = [h for h in history if not (h["res"] is None and h["op"] == "read")]
    inf = float("inf")
    res = [h["res"] if h["res"] is not None else inf for h in ops]
    n = len(ops)
    must = sum(1 << i for i in range(n) if ops[i]["res"] is not None)
    seen: set = set()

    def search(done: int, val: object) -> bool:
        if done & must == must:
            return True
        key = (done, val)
        if key in seen:
            return False
        seen.add(key)
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


def random_run(seed: int, n: int = 4, clients: int = 3, ops: int = 5,
               crashes: list[tuple[int, int]] | None = None, check: bool = True,
               read_at: str = "tail") -> Chain:
    """Clients do random reads and writes of unique values; crashes is a list
    of (time, server)."""
    rng = random.Random(seed)
    ch = Chain(n, seed, read_at=read_at)
    ch.check = check
    for c in range(clients):
        seq = [("write", f"{c}.{j}") if rng.random() < 0.5 else ("read", None) for j in range(ops)]
        ch.add_client(c, seq, start=rng.randint(0, 10))
    for t, s in crashes or []:
        ch.at(t, ch.crash, s)
    ch.run()
    return ch
