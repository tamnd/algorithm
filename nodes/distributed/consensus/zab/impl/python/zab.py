# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zab/. The authors are listed in prov/M3MBBQ.jsonl.

"""Zab (ZooKeeper Atomic Broadcast) in a seeded simulator.

The simulator follows the three phases of Junqueira, Reed and Serafini (DSN 2011):
discovery (CEPOCH, NEWEPOCH, ACK-E), synchronization (NEWLEADER, ACK-LD,
COMMIT-LD) and broadcast (PROPOSE, ACK, COMMIT). Channels are FIFO, like TCP.
A connection belongs to one election; a process that switches leader or loses
a message drops the connection and ignores later messages on it.

Each process keeps on stable storage the accepted epoch f.p, the current epoch
f.a, its history h_f and the sequence of transactions it has delivered. A
crash loses everything else. An oracle plays leader election: it picks a live
process as prospective leader and moves some live processes to it.

A transaction is (epoch, counter, value); its zxid is (epoch, counter).
"""

from __future__ import annotations

import random
from collections import deque
from typing import Optional

Txn = tuple[int, int, str]


class Proc:
    def __init__(self, pid: int) -> None:
        self.pid = pid
        self.alive = True
        # stable storage
        self.p = 0  # accepted epoch f.p
        self.a = 0  # current epoch f.a
        self.hist: list[Txn] = []
        self.delivered: list[Txn] = []
        # volatile
        self.leader: Optional[int] = None
        self.cid: Optional[int] = None
        self.ld_len = 0  # length of the NEWLEADER history
        self.lead: Optional[dict] = None  # leader state when this process leads


class Zab:
    def __init__(self, n: int, seed: int = 0, bad_choice: bool = False) -> None:
        self.n = n
        self.q = n // 2 + 1
        self.rng = random.Random(seed)
        self.procs = [Proc(i) for i in range(n)]
        self.chan: dict[tuple[int, int], deque] = {}
        self.next_cid = 0
        self.next_value = 0
        self.bad_choice = bad_choice  # broken variant: pick a random history in L4
        self.violations: list[str] = []
        self.initial: dict[int, list[Txn]] = {}  # epoch -> initial history I_e
        self.established: dict[int, int] = {}  # epoch -> leader that got all ACK-E
        self.proposed: dict[int, list[Txn]] = {}  # epoch -> transactions in broadcast order

    # ------------------------------------------------------------ plumbing

    def send(self, src: int, dst: int, cid: int, msg: tuple) -> None:
        self.chan.setdefault((src, dst), deque()).append((cid, msg))

    def pending(self) -> list[tuple[int, int]]:
        return [k for k, q in self.chan.items() if q]

    def elect(self, leader: int, members: set[int]) -> None:
        """Oracle: the live processes in members (with the leader) follow `leader` on a new connection."""
        self.next_cid += 1
        cid = self.next_cid
        members = {m for m in members | {leader} if self.procs[m].alive}
        for m in members:
            f = self.procs[m]
            if f.lead is not None:
                f.lead = None  # it stops leading its old connection
            f.leader, f.cid, f.ld_len = leader, cid, 0
            self.send(m, leader, cid, ("CEPOCH", f.p))  # @line L1
        self.procs[leader].lead = {"cid": cid, "phase": 1, "Q": [], "cepoch": {}, "acke": {},
                                   "ackld": set(), "e": None, "counter": 0, "acks": {},
                                   "next_commit": 1}

    def disconnect(self, pid: int) -> None:
        f = self.procs[pid]
        f.leader = f.cid = None
        f.lead = None

    def crash(self, pid: int) -> None:
        self.disconnect(pid)
        self.procs[pid].alive = False

    def recover(self, pid: int) -> None:
        self.procs[pid].alive = True

    def drop(self, src: int, dst: int) -> None:
        """Lose the head message of a channel. The follower end of that connection drops it."""
        cid, _ = self.chan[(src, dst)].popleft()
        for pid, other in ((src, dst), (dst, src)):
            f = self.procs[pid]
            if f.cid == cid and f.leader == other:
                f.leader = f.cid = None  # it stops following; a leader keeps its leader state

    def deliver_one(self, src: int, dst: int) -> None:
        cid, msg = self.chan[(src, dst)].popleft()
        d = self.procs[dst]
        if not d.alive:
            return
        if d.lead is not None and d.lead["cid"] == cid and msg[0] in ("CEPOCH", "ACK-E", "ACK-LD", "ACK"):
            self.on_leader(d, src, msg)
        elif d.cid == cid and d.leader == src and msg[0] in ("NEWEPOCH", "NEWLEADER", "COMMIT-LD",
                                                           "PROPOSE", "COMMIT"):
            self.on_follower(d, src, msg)

    # ------------------------------------------------------------ leader

    def to_q(self, L: Proc, msg: tuple) -> None:
        for f in L.lead["Q"]:
            self.send(L.pid, f, L.lead["cid"], msg)

    def on_leader(self, L: Proc, src: int, msg: tuple) -> None:
        st = L.lead
        kind = msg[0]
        if kind == "CEPOCH" and st["phase"] == 1 and src not in st["cepoch"]:
            st["cepoch"][src] = msg[1]
            if len(st["cepoch"]) >= self.q:
                st["Q"] = sorted(st["cepoch"])
                st["e"] = max(st["cepoch"].values()) + 1
                st["phase"] = 2
                self.to_q(L, ("NEWEPOCH", st["e"]))  # @line L2
        elif kind == "CEPOCH" and st["phase"] == 4 and src not in st["Q"]:
            # a late follower: bring it up to date in one go and add it to Q
            e, cid = st["e"], st["cid"]
            hist = st["I"] + self.proposed.get(e, [])
            committed = len(st["I"]) + st["next_commit"] - 1
            self.send(L.pid, src, cid, ("NEWEPOCH", e))
            self.send(L.pid, src, cid, ("NEWLEADER", e, list(hist), committed))
            self.send(L.pid, src, cid, ("COMMIT-LD", e))
            st["Q"].append(src)
        elif kind == "ACK-E" and st["phase"] == 2:
            st["acke"][src] = (msg[1], msg[2])
            if len(st["acke"]) == len(st["Q"]):
                if self.bad_choice:
                    chosen = self.rng.choice(list(st["acke"].values()))[1]
                else:
                    def key(v):  # largest (f.a, last zxid of h_f)
                        a, h = v
                        return (a, (h[-1][0], h[-1][1]) if h else (0, 0))
                    chosen = max(st["acke"].values(), key=key)[1]  # @line L4
                e = st["e"]
                if e in self.established:
                    self.violations.append(f"two leaders established epoch {e}")
                self.established[e] = L.pid
                self.initial[e] = list(chosen)
                st["I"] = list(chosen)
                st["phase"] = 3
                self.to_q(L, ("NEWLEADER", e, list(chosen), len(chosen)))  # @line L5
        elif kind == "ACK-LD" and st["phase"] == 3:
            st["ackld"].add(src)
            if len(st["ackld"]) >= self.q:
                st["phase"] = 4
                self.to_q(L, ("COMMIT-LD", st["e"]))  # @line L7
        elif kind == "ACK" and st["phase"] == 4:
            c = msg[1][1]
            st["acks"].setdefault(c, set()).add(src)
            while len(st["acks"].get(st["next_commit"], ())) >= self.q:
                self.to_q(L, ("COMMIT", (st["e"], st["next_commit"])))  # @line L11
                st["next_commit"] += 1

    def propose(self, pid: int) -> bool:
        L = self.procs[pid]
        if not L.alive or L.lead is None or L.lead["phase"] != 4:
            return False
        st = L.lead
        st["counter"] += 1
        self.next_value += 1
        txn = (st["e"], st["counter"], f"v{self.next_value}")
        self.proposed.setdefault(st["e"], []).append(txn)
        self.to_q(L, ("PROPOSE", txn))  # @line L9
        return True

    # ------------------------------------------------------------ follower

    def deliver_upto(self, f: Proc, k: int) -> None:
        if f.delivered != f.hist[: len(f.delivered)]:
            self.violations.append(f"process {f.pid} delivered something outside its history")
            return
        f.delivered = f.delivered + f.hist[len(f.delivered): k]

    def on_follower(self, f: Proc, src: int, msg: tuple) -> None:
        kind = msg[0]
        if kind == "NEWEPOCH":
            e = msg[1]
            if e > f.p:
                f.p = e
                self.send(f.pid, src, f.cid, ("ACK-E", f.a, list(f.hist)))  # @line L3
            else:
                self.disconnect(f.pid)  # back to election
        elif kind == "NEWLEADER":
            e, hist = msg[1], msg[2]
            if f.p != e:
                self.disconnect(f.pid)
                return
            f.a = e  # @line L6
            if f.delivered != hist[: len(f.delivered)]:
                self.violations.append(f"process {f.pid} delivered a transaction not in I_{e}")
            f.hist = list(hist)
            f.ld_len = msg[3]  # the prefix that COMMIT-LD delivers
            self.send(f.pid, src, f.cid, ("ACK-LD", e))
        elif kind == "COMMIT-LD":
            self.deliver_upto(f, f.ld_len)  # @line L8
        elif kind == "PROPOSE":
            txn = msg[1]
            f.hist.append(txn)
            self.send(f.pid, src, f.cid, ("ACK", (txn[0], txn[1])))  # @line L10
        elif kind == "COMMIT":
            zxid = msg[1]
            k = next((i + 1 for i, t in enumerate(f.hist) if (t[0], t[1]) == zxid), None)
            if k is None:
                self.violations.append(f"process {f.pid} got COMMIT for a zxid it does not have")
                return
            self.deliver_upto(f, k)  # @line L12

    # ------------------------------------------------------------ runs and checks

    def random_run(self, steps: int, max_down: Optional[int] = None) -> None:
        rng = self.rng
        max_down = (self.n - 1) // 2 if max_down is None else max_down
        self.elect(0, set(range(self.n)))
        for _ in range(steps):
            r = rng.random()
            live = [p.pid for p in self.procs if p.alive]
            down = [p.pid for p in self.procs if not p.alive]
            pend = self.pending()
            if r < 0.03:
                L = rng.choice(live)
                self.elect(L, {m for m in live if rng.random() < 0.7})
            elif r < 0.05 and len(down) < max_down:
                self.crash(rng.choice(live))
            elif r < 0.07 and down:
                self.recover(rng.choice(down))
            elif r < 0.08 and pend:
                self.drop(*rng.choice(pend))
            elif r < 0.2:
                leaders = [p for p in live if self.procs[p].lead is not None]
                if leaders:
                    self.propose(rng.choice(leaders))
            elif pend:
                self.deliver_one(*rng.choice(pend))

    def check(self) -> list[str]:
        out = list(self.violations)
        seqs = [p.delivered for p in self.procs]
        for i, a in enumerate(seqs):  # agreement and total order: prefix-consistent deliveries
            for b in seqs[i + 1:]:
                s, t = (a, b) if len(a) <= len(b) else (b, a)
                if t[: len(s)] != s:
                    out.append("two processes delivered different sequences")
        for p in self.procs:
            d = p.delivered
            if len(set(d)) != len(d):
                out.append(f"process {p.pid} delivered a transaction twice")
            epochs = [t[0] for t in d]
            if epochs != sorted(epochs):
                out.append(f"process {p.pid} broke global primary order")
            for e in set(epochs):
                cs = [t[1] for t in d if t[0] == e]
                if cs != list(range(1, len(cs) + 1)):
                    out.append(f"process {p.pid} broke local primary order in epoch {e}")
        delivered_all = {t for s in seqs for t in s}
        for e, txns in self.proposed.items():  # primary integrity
            if not txns:
                continue
            init = set(self.initial[e])
            for t in delivered_all:
                if t[0] < e and t not in init:
                    out.append(f"primary of epoch {e} broadcast without delivering {t}")
        return out
