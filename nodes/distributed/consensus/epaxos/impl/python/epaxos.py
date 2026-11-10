# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epaxos/. The authors are listed in prov/D37K98.jsonl.
"""EPaxos commit and execution in a seeded discrete-event simulator.

N = 2F + 1 replicas. A command is a pair (name, key); two commands interfere
when they have the same key. The simulator covers the fast path, the slow
(Paxos-Accept) path, and execution by strongly connected components. It does
not cover the recovery of the instances of a failed replica, so only replicas
that lead no command may crash.
"""

import random
from typing import Optional


def interfere(c: tuple, d: tuple) -> bool:
    return c[1] == d[1]


def fast_quorum_size(f: int) -> int:
    return f + (f + 1) // 2


class Inst:
    __slots__ = ("cmd", "seq", "deps", "status")

    def __init__(self, cmd: tuple, seq: int, deps: frozenset, status: str) -> None:
        self.cmd, self.seq, self.deps, self.status = cmd, seq, deps, status


def tarjan(root: tuple, succ) -> list:
    """Iterative Tarjan. Returns the SCCs reachable from root, each one after
    all SCCs it can reach, so in an order fit for execution."""
    index: dict = {}
    low: dict = {}
    stack: list = []
    on: set = set()
    out: list = []
    counter = 0

    def push(v: tuple) -> None:
        nonlocal counter
        index[v] = low[v] = counter
        counter += 1
        stack.append(v)
        on.add(v)

    push(root)
    work = [(root, iter(succ(root)))]
    while work:
        v, it = work[-1]
        advanced = False
        for w in it:
            if w not in index:
                push(w)
                work.append((w, iter(succ(w))))
                advanced = True
                break
            if w in on:
                low[v] = min(low[v], index[w])
        if advanced:
            continue
        work.pop()
        if work:
            u = work[-1][0]
            low[u] = min(low[u], low[v])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(comp)
    return out


class Replica:
    def __init__(self, sim: "EPaxos", r: int) -> None:
        self.sim, self.r = sim, r
        self.cmds: dict = {}
        self.next_i = 0
        self.lead: dict = {}
        self.executed: list = []
        self.done: set = set()

    def local_attrs(self, cmd: tuple, iid: tuple) -> tuple:
        ifs = [j for j, x in self.cmds.items() if j != iid and interfere(x.cmd, cmd)]
        seq = 1 + max((self.cmds[j].seq for j in ifs), default=0)
        return seq, frozenset(ifs)

    # ---- the command leader ----
    def propose(self, cmd: tuple) -> None:
        iid = (self.r, self.next_i)
        self.next_i += 1
        seq, deps = self.local_attrs(cmd, iid)  # @line L1
        self.cmds[iid] = Inst(cmd, seq, deps, "pre")
        self.lead[iid] = {"phase": "pre", "replies": {}, "acks": set(), "orig": (seq, deps)}
        self.sim.broadcast(self.r, ("PreAccept", iid, cmd, seq, deps))  # @line L2

    def on_preaccept_ok(self, iid: tuple, seq: int, deps: frozenset, src: int) -> None:
        st = self.lead.get(iid)
        if st is None or st["phase"] != "pre":
            return
        st["replies"][src] = (seq, deps)
        if len(st["replies"]) >= self.sim.fq - 1:
            self.decide_phase1(iid)

    def decide_phase1(self, iid: tuple) -> None:
        st = self.lead[iid]
        replies = list(st["replies"].values())
        if self.sim.unsafe_fast and len(replies) >= self.sim.fq - 1:
            self.commit(iid, *st["orig"])  # wrong: ignores what the replies added
            return
        if len(replies) >= self.sim.fq - 1 and all(r == replies[0] for r in replies):
            self.sim.fast_commits += 1
            self.commit(iid, *replies[0])  # @line L5
            return
        if len(replies) < self.sim.f:
            return
        inst = self.cmds[iid]
        seq = max([inst.seq] + [s for s, _ in replies])
        deps = inst.deps.union(*[d for _, d in replies])  # @line L6
        st["phase"] = "accept"
        self.sim.slow_commits += 1
        self.cmds[iid] = Inst(inst.cmd, seq, deps, "acc")
        self.sim.broadcast(self.r, ("Accept", iid, inst.cmd, seq, deps))

    def on_accept_ok(self, iid: tuple, src: int) -> None:
        st = self.lead.get(iid)
        if st is None or st["phase"] != "accept":
            return
        st["acks"].add(src)
        if len(st["acks"]) >= self.sim.f:
            inst = self.cmds[iid]
            self.commit(iid, inst.seq, inst.deps)  # @line L7

    def commit(self, iid: tuple, seq: int, deps: frozenset) -> None:
        self.lead[iid]["phase"] = "committed"
        cmd = self.cmds[iid].cmd
        self.cmds[iid] = Inst(cmd, seq, deps, "com")  # @line L8
        self.sim.broadcast(self.r, ("Commit", iid, cmd, seq, deps))
        self.try_execute()

    # ---- every replica ----
    def on_preaccept(self, iid: tuple, cmd: tuple, seq: int, deps: frozenset, src: int) -> None:
        cur = self.cmds.get(iid)
        if cur is not None:
            if cur.status == "pre":  # a duplicate: answer the same again
                self.sim.send(self.r, src, ("PreAcceptOK", iid, cur.seq, cur.deps))
            return
        lseq, ldeps = self.local_attrs(cmd, iid)
        seq, deps = max(seq, lseq), deps | ldeps  # @line L3
        self.cmds[iid] = Inst(cmd, seq, deps, "pre")
        self.sim.send(self.r, src, ("PreAcceptOK", iid, seq, deps))  # @line L4

    def on_accept(self, iid: tuple, cmd: tuple, seq: int, deps: frozenset, src: int) -> None:
        cur = self.cmds.get(iid)
        if cur is None or cur.status != "com":
            self.cmds[iid] = Inst(cmd, seq, deps, "acc")  # @line L9
        self.sim.send(self.r, src, ("AcceptOK", iid))

    def on_commit(self, iid: tuple, cmd: tuple, seq: int, deps: frozenset) -> None:
        self.cmds[iid] = Inst(cmd, seq, deps, "com")
        self.try_execute()

    # ---- execution ----
    def ready(self, root: tuple) -> bool:
        """@line L10 root and all instances it reaches through deps are committed."""
        seen, todo = {root}, [root]
        while todo:
            v = todo.pop()
            x = self.cmds.get(v)
            if x is None or x.status != "com":
                return False
            for d in x.deps:
                if d not in self.done and d not in seen:
                    seen.add(d)
                    todo.append(d)
        return True

    def try_execute(self) -> None:
        if self.sim.naive_execute:
            for iid in sorted(self.cmds):
                if self.cmds[iid].status == "com" and iid not in self.done:
                    self.run(iid)  # wrong: in commit order, ignoring deps
            return
        for iid in sorted(self.cmds):
            x = self.cmds[iid]
            if x.status != "com" or iid in self.done or not self.ready(iid):
                continue
            succ = lambda v: sorted(d for d in self.cmds[v].deps if d not in self.done)
            for comp in tarjan(iid, succ):  # @line L11
                for v in sorted(comp, key=lambda v: (self.cmds[v].seq, v)):
                    self.run(v)  # @line L12

    def run(self, iid: tuple) -> None:
        self.done.add(iid)
        self.executed.append(self.cmds[iid].cmd)


class EPaxos:
    def __init__(self, f: int, seed: int, commands: list, proposers: Optional[list] = None,
                 dup: float = 0.0, crashes: int = 0, crash_prob: float = 0.0,
                 unsafe_fast: bool = False, naive_execute: bool = False,
                 max_steps: int = 50000) -> None:
        self.f = f
        self.n = 2 * f + 1
        self.fq = fast_quorum_size(f)
        self.rng = random.Random(seed)
        self.commands = list(commands)
        self.proposers = proposers if proposers is not None else list(range(self.n))
        self.dup = dup
        self.crashes_left, self.crash_prob = crashes, crash_prob
        self.unsafe_fast, self.naive_execute = unsafe_fast, naive_execute
        self.max_steps = max_steps
        self.replicas = [Replica(self, r) for r in range(self.n)]
        self.crashed: set = set()
        self.net: list = []
        self.fast_commits = self.slow_commits = 0

    def send(self, src: int, dst: int, msg: tuple) -> None:
        self.net.append((src, dst, msg))
        if self.rng.random() < self.dup:
            self.net.append((src, dst, msg))

    def broadcast(self, src: int, msg: tuple) -> None:
        for dst in range(self.n):
            if dst != src:
                self.send(src, dst, msg)

    def deliver(self, src: int, dst: int, msg: tuple) -> None:
        if dst in self.crashed:
            return
        r = self.replicas[dst]
        kind = msg[0]
        if kind == "PreAccept":
            r.on_preaccept(msg[1], msg[2], msg[3], msg[4], src)
        elif kind == "PreAcceptOK":
            r.on_preaccept_ok(msg[1], msg[2], msg[3], src)
        elif kind == "Accept":
            r.on_accept(msg[1], msg[2], msg[3], msg[4], src)
        elif kind == "AcceptOK":
            r.on_accept_ok(msg[1], src)
        else:
            r.on_commit(msg[1], msg[2], msg[3], msg[4])

    def live(self) -> list:
        return [r for r in self.replicas if r.r not in self.crashed]

    def run(self) -> "EPaxos":
        pending = list(self.commands)
        for _ in range(self.max_steps):
            if pending and self.rng.random() < 0.2:
                self.replicas[self.rng.choice(self.proposers)].propose(pending.pop(0))
            if self.crashes_left and self.rng.random() < self.crash_prob:
                cands = [r for r in range(self.n) if r not in self.proposers and r not in self.crashed]
                if cands:
                    self.crashed.add(self.rng.choice(cands))
                    self.crashes_left -= 1
            if self.net:
                i = self.rng.randrange(len(self.net))
                self.net[i], self.net[-1] = self.net[-1], self.net[i]
                self.deliver(*self.net.pop())
                continue
            if pending:
                continue
            # Quiet network: a leader that waits for a fast quorum that will
            # not answer takes the slow path with the replies it has.
            stuck = False
            for r in self.live():
                for iid, st in r.lead.items():
                    if st["phase"] == "pre":
                        r.decide_phase1(iid)
                        stuck = True
            if not stuck or not self.net:
                break
        return self

    def all_executed(self) -> bool:
        return all(len(r.executed) == len(self.commands) for r in self.live())

    def same_order_for_conflicts(self) -> bool:
        """For each key, all replicas run its commands in the same order."""
        keys = {c[1] for c in self.commands}
        for k in keys:
            orders = [[c for c in r.executed if c[1] == k] for r in self.live()]
            longest = max(orders, key=len)
            if any(o != longest[:len(o)] for o in orders):
                return False
        return True

    def conflicts_are_ordered(self) -> bool:
        """Committed interfering instances: one is in the deps of the other."""
        com: dict = {}
        for r in self.live():
            for iid, x in r.cmds.items():
                if x.status == "com":
                    com[iid] = x
        for a, x in com.items():
            for b, y in com.items():
                if a < b and interfere(x.cmd, y.cmd) and a not in y.deps and b not in x.deps:
                    return False
        return True
