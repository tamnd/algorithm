# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primary-backup-replication/. The authors are listed in prov/04PKB8.jsonl.

"""Primary-backup (passive) replication of a read/write register.

The primary executes each request, sends the new state to every backup of the
current view, waits for all their acknowledgements, and only then replies
(a blocking protocol, as in Alsberg and Day 1976 and the crash protocol of
Budhiraja, Marzullo, Schneider and Toueg 1993). It handles one write at a time.

A view service plays the failure detector. With detect="perfect" it learns of a
crash after a fixed delay and installs a new view whose primary is the smallest
live server; this is the crash model with a perfect failure detector. With
detect="timeout" a backup that cannot hear the primary declares it dead, which
is wrong during a partition and leads to split brain.

A new primary first sends its whole state to the backups and waits for them
(state transfer), then serves. Clients retry with the same request id, and the
reply cache keeps a retried write from running twice.

The module also holds a small Wing and Gong style checker of linearizability
for register histories.
"""

import heapq
import random
from typing import Callable, Hashable


class Sim:
    """A heap of timed events, seeded delays, crashes and a set of cut links."""

    def __init__(self, seed: int, delay: tuple[int, int] = (1, 5)) -> None:
        self.rng = random.Random(seed)
        self.delay = delay
        self.now = 0
        self.heap: list = []
        self.seq = 0
        self.stamp_no = 0
        self.crashed: set[Hashable] = set()
        self.cut: set[frozenset] = set()
        self.handlers: dict[Hashable, Callable] = {}
        self.on_crash: list[Callable[[Hashable], None]] = []

    def stamp(self) -> int:
        self.stamp_no += 1
        return self.stamp_no

    def at(self, t: int, fn: Callable[[], None]) -> None:
        heapq.heappush(self.heap, (t, self.seq, fn))
        self.seq += 1

    def send(self, src: Hashable, dst: Hashable, msg: tuple) -> None:
        if src in self.crashed or frozenset((src, dst)) in self.cut:
            return
        t = self.now + self.rng.randint(*self.delay)
        self.at(t, lambda: self.deliver(dst, src, msg))

    def deliver(self, dst: Hashable, src: Hashable, msg: tuple) -> None:
        if dst not in self.crashed and frozenset((src, dst)) not in self.cut:
            self.handlers[dst](src, msg)

    def crash(self, pid: Hashable) -> None:
        if pid not in self.crashed:
            self.crashed.add(pid)
            for fn in self.on_crash:
                fn(pid)

    def run(self, until: int = 10 ** 6) -> None:
        while self.heap and self.heap[0][0] <= until:
            t, _, fn = heapq.heappop(self.heap)
            self.now = t
            fn()


class ViewService:
    """Holds the views. A view is (number, primary, backups)."""

    def __init__(self, sim: Sim, n: int, detect: str, delay: int = 15) -> None:
        self.sim = sim
        self.view = (1, 0, tuple(range(1, n)))
        self.servers: dict[int, "Server"] = {}
        self.delay = delay
        self.detect = detect
        sim.on_crash.append(self.crashed)

    def crashed(self, pid: Hashable) -> None:
        if self.detect == "perfect" and pid[0] == "S":
            self.sim.at(self.sim.now + self.delay, lambda: self.remove(pid[1]))

    def remove(self, pid: int) -> None:
        num, p, bs = self.view
        live = [s for s in (p,) + bs if s != pid and ("S", s) not in self.sim.crashed]
        if pid not in (p,) + bs or not live:
            return
        if pid == p:
            self.view = (num + 1, live[0], tuple(live[1:]))
        else:
            self.view = (num + 1, p, tuple(b for b in bs if b != pid))
        for s in (self.view[1],) + self.view[2]:
            self.servers[s].new_view(self.view)

    def false_suspicion(self, suspect: int, by: int) -> None:
        """detect = "timeout": server `by` stops hearing the primary and takes over alone."""
        num, p, bs = self.view
        local = (num + 1, by, tuple(b for b in bs if b not in (by, suspect)))
        self.servers[by].new_view(local)


class Server:
    def __init__(self, sid: int, sim: Sim, view: tuple) -> None:
        self.sid = sid
        self.sim = sim
        self.view = view
        self.value: object = None
        self.cache: dict[Hashable, object] = {}
        self.queue: list[tuple] = []
        self.inflight: tuple | None = None
        self.waiting: set[int] = set()
        self.serving = view[1] == sid
        self.crash_after: int | None = None  # crash after this many UPDATE sends
        self.updates_sent = 0

    def me(self) -> tuple:
        return ("S", self.sid)

    def is_primary(self) -> bool:
        return self.view[1] == self.sid

    # ------------------------------------------------------------ primary
    def on_request(self, client: Hashable, rid: Hashable, op: str, arg: object) -> None:
        if not self.is_primary():
            return  # not the primary: the client times out and asks the view service
        self.queue.append((client, rid, op, arg))  # @line L1
        self.step()

    def step(self) -> None:
        while self.serving and self.inflight is None and self.queue:
            client, rid, op, arg = self.queue.pop(0)
            if rid in self.cache:  # @line L2
                self.reply(client, rid, self.cache[rid])
            elif op == "read":
                self.reply(client, rid, self.value)  # @line L3
            else:
                self.value = arg  # @line L4
                self.cache[rid] = "ok"
                self.inflight = (client, rid)
                self.waiting = set(self.view[2])
                for b in self.view[2]:
                    self.sim.send(self.me(), ("S", b), ("UPDATE", self.view[0], self.value, rid))  # @line L5
                    self.updates_sent += 1
                    if self.crash_after is not None and self.updates_sent >= self.crash_after:
                        self.sim.crash(self.me())
                        return
                self.check_done()

    def check_done(self) -> None:
        if self.inflight is not None and not self.waiting:  # @line L7
            client, rid = self.inflight
            self.inflight = None
            self.reply(client, rid, self.cache[rid])  # @line L8

    def reply(self, client: Hashable, rid: Hashable, out: object) -> None:
        self.sim.send(self.me(), client, ("REPLY", rid, out))

    def on_ack(self, b: int, view: int) -> None:
        if view == self.view[0] and self.is_primary():
            self.waiting.discard(b)  # @line L6
            if not self.serving and not self.waiting:
                self.serving = True  # state transfer done
                self.check_done()
                self.step()
            else:
                self.check_done()
                self.step()

    # ------------------------------------------------------------ views
    def new_view(self, view: tuple) -> None:
        self.view = view
        self.serving = False
        if self.is_primary():
            # state transfer: the new primary's state wins at every backup
            self.waiting = set(view[2])
            for b in view[2]:
                self.sim.send(self.me(), ("S", b), ("STATE", view[0], self.value, dict(self.cache)))  # @line L9
            if not self.waiting:
                self.serving = True
                self.check_done()
                self.step()

    # ------------------------------------------------------------ backup
    def on_update(self, src: Hashable, view: int, value: object, rid: Hashable) -> None:
        if view != self.view[0] or self.is_primary():
            return
        self.value = value  # @line L10
        self.cache[rid] = "ok"
        self.sim.send(self.me(), src, ("ACK", self.sid, view))  # @line L11

    def on_state(self, src: Hashable, view: int, value: object, cache: dict) -> None:
        if view != self.view[0] or self.is_primary():
            return
        self.value = value
        self.cache = dict(cache)
        self.sim.send(self.me(), src, ("ACK", self.sid, view))

    def on_message(self, src: Hashable, msg: tuple) -> None:
        kind = msg[0]
        if kind == "REQ":
            self.on_request(src, msg[1], msg[2], msg[3])
        elif kind == "UPDATE":
            self.on_update(src, msg[1], msg[2], msg[3])
        elif kind == "STATE":
            self.on_state(src, msg[1], msg[2], msg[3])
        elif kind == "ACK":
            self.on_ack(msg[1], msg[2])


class Client:
    """Runs its operations one after another; retries a request after a timeout."""

    def __init__(self, cid: int, sim: Sim, vs: ViewService, ops: list[tuple],
                 history: list, timeout: int = 30, target: Callable | None = None) -> None:
        self.cid = cid
        self.sim = sim
        self.vs = vs
        self.ops = list(ops)
        self.history = history
        self.timeout = timeout
        self.target = target or (lambda: vs.view[1])
        self.cur: dict | None = None
        self.k = 0

    def me(self) -> tuple:
        return ("C", self.cid)

    def start(self) -> None:
        if not self.ops:
            return
        op, arg = self.ops.pop(0)
        self.k += 1
        rid = (self.cid, self.k)
        rec = {"op": op, "arg": arg, "inv": self.sim.stamp(), "res": None, "out": None}
        self.history.append(rec)
        self.cur = {"rid": rid, "rec": rec}
        self.send()

    def send(self) -> None:
        cur = self.cur
        if cur is None:
            return
        self.sim.send(self.me(), ("S", self.target()), ("REQ", cur["rid"], cur["rec"]["op"], cur["rec"]["arg"]))
        rid = cur["rid"]
        self.sim.at(self.sim.now + self.timeout, lambda: self.retry(rid))

    def retry(self, rid: Hashable) -> None:
        if self.cur is not None and self.cur["rid"] == rid:
            self.send()

    def on_message(self, src: Hashable, msg: tuple) -> None:
        _, rid, out = msg
        if self.cur is None or rid != self.cur["rid"]:
            return
        rec = self.cur["rec"]
        rec["res"] = self.sim.stamp()
        rec["out"] = out if rec["op"] == "read" else None
        self.cur = None
        self.sim.at(self.sim.now + self.sim.rng.randint(0, 4), self.start)


def run(seed: int, n: int, ops_per_client: list[list[tuple]],
        crash: dict[int, int] | None = None, crash_after: dict[int, int] | None = None,
        until: int = 3000) -> dict:
    """crash: server -> time; crash_after: server -> number of UPDATE sends before it crashes."""
    sim = Sim(seed)
    vs = ViewService(sim, n, "perfect")
    servers = [Server(i, sim, vs.view) for i in range(n)]
    for s in servers:
        vs.servers[s.sid] = s
        sim.handlers[s.me()] = s.on_message
        if crash_after and s.sid in crash_after:
            s.crash_after = crash_after[s.sid]
    history: list = []
    clients = [Client(i, sim, vs, ops, history) for i, ops in enumerate(ops_per_client)]
    for c in clients:
        sim.handlers[c.me()] = c.on_message
        sim.at(sim.rng.randint(0, 5), c.start)
    for s, t in (crash or {}).items():
        sim.at(t, lambda s=s: sim.crash(("S", s)))
    sim.run(until)
    return {"sim": sim, "vs": vs, "servers": servers, "history": history}


def split_brain_run() -> dict:
    """Two servers. A partition cuts S0 from S1. With timeout detection S1 takes over
    while S0 still serves reads to client 0. Client 1 writes 2 at S1, then client 0
    reads at S0 and gets the old value 1."""
    sim = Sim(0, delay=(1, 1))
    vs = ViewService(sim, 2, "timeout")
    servers = [Server(i, sim, vs.view) for i in range(2)]
    for s in servers:
        vs.servers[s.sid] = s
        sim.handlers[s.me()] = s.on_message
    history: list = []
    c0 = Client(0, sim, vs, [("write", 1)], history, target=lambda: 0)
    c1 = Client(1, sim, vs, [("write", 2)], history, target=lambda: 1)
    for c in (c0, c1):
        sim.handlers[c.me()] = c.on_message
    sim.at(0, c0.start)
    sim.run(20)  # write 1 completes at S0 and S1
    sim.cut.add(frozenset((("S", 0), ("S", 1))))
    vs.false_suspicion(0, 1)  # S1 times out on S0 and becomes primary of its own view
    sim.at(sim.now + 1, c1.start)
    sim.run(sim.now + 20)  # write 2 completes at S1
    c0.ops.append(("read", None))
    sim.at(sim.now + 1, c0.start)
    sim.run(sim.now + 20)  # the read at S0 returns 1
    return {"history": history, "servers": servers}


# ---------------------------------------------------------------- checker

def linearizable(history: list[dict], init: object = None) -> bool:
    """Wing and Gong search for a register. Each record has op, arg, inv, res, out.

    A record with res None is pending: a pending write may or may not take effect,
    and a pending read is dropped. Exponential in the worst case; fine for short
    histories.
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
