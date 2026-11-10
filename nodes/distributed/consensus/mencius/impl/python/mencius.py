# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mencius/. The authors are listed in prov/H2QGRY.jsonl.
"""Mencius in a seeded discrete-event simulator.

N servers share one log. Server p is the coordinator of instances p, p + N,
p + 2N, and so on. A coordinator suggests a client command or skips (no-op) in
its own instances at ballot 0. Any other server can revoke an instance with a
full Paxos run at a higher ballot, which may only end with the coordinator's
value or with no-op. Messages can be delayed, reordered and duplicated.
Messages already sent by a server that crashes are still delivered.
"""

import random
from typing import Optional

NOOP = "no-op"


class Server:
    def __init__(self, sim: "Mencius", pid: int) -> None:
        self.sim, self.pid, self.n = sim, pid, sim.n
        self.I = pid                       # the next instance this server coordinates
        self.acc: dict = {}                # instance -> [promised, accepted ballot, accepted value]
        self.learned: dict = {}
        self.mine: dict = {}               # instance -> command suggested by this server
        self.acks: dict = {}
        self.rev: dict = {}                # instance -> the state of a revocation
        self.maxk = 0
        self.executed: list = []
        self.next_exec = 0

    def a(self, j: int) -> list:
        return self.acc.setdefault(j, [(-1, -1), None, None])

    def own_after(self, j: int) -> int:
        """The first instance coordinated by this server that is larger than j."""
        k = j + 1
        return k + (self.pid - k) % self.n

    # ---- the coordinator: Rules 1, 2 and 4 ----
    def suggest(self, v: str) -> None:
        while self.I in self.learned:      # already revoked: never reuse it
            self.I += self.n
        j = self.I
        self.I += self.n
        self.mine[j], self.acks[j] = v, set()
        self.sim.max_suggested = max(self.sim.max_suggested, j)
        self.sim.broadcast(self.pid, ("SUGGEST", j, v), self_too=True)  # @line L1

    def on_suggest(self, j: int, v: str, src: int) -> None:
        if not self.sim.no_skip and j > self.I:
            for k in range(self.I, j, self.n):  # @line L3
                self.skip(k)
            self.I = self.own_after(j)
        st = self.a(j)
        if (0, src) >= st[0]:
            st[0], st[1], st[2] = (0, src), (0, src), v
            self.sim.send(self.pid, src, ("ACK", j))  # @line L2

    def skip(self, k: int) -> None:
        self.sim.skips += 1
        self.learn(k, NOOP)
        self.sim.broadcast(self.pid, ("SKIP", k))

    def on_ack(self, j: int, src: int) -> None:
        if j not in self.mine:
            return
        self.acks[j].add(src)
        if len(self.acks[j]) == self.sim.maj:
            self.learn(j, self.mine[j])  # @line L4
            self.sim.broadcast(self.pid, ("LEARN", j, self.mine[j]))

    def on_skip(self, j: int) -> None:
        self.learn(j, NOOP)  # @line L5

    # ---- revocation: Rule 3, a Paxos run that proposes no-op ----
    def revoke_owner(self, q: int) -> None:
        for j in range(q, self.I, self.n):  # @line L6
            if j not in self.learned:
                self.revoke(j)

    def revoke(self, j: int) -> None:
        self.sim.revocations += 1
        self.maxk += 1
        b = (self.maxk, self.pid)
        self.rev[j] = {"b": b, "phase": 1, "promises": {}, "acks": set(), "v": None}
        self.sim.broadcast(self.pid, ("PREPARE", j, b), self_too=True)

    def on_prepare(self, j: int, b: tuple, src: int) -> None:
        self.maxk = max(self.maxk, b[0])
        st = self.a(j)
        if b > st[0]:
            st[0] = b
            self.sim.send(self.pid, src, ("PROMISE", j, b, st[1], st[2]))  # @line L7
        else:
            self.sim.send(self.pid, src, ("NACK", j, st[0]))

    def on_promise(self, j: int, b: tuple, ab: Optional[tuple], av: Optional[str], src: int) -> None:
        r = self.rev.get(j)
        if r is None or r["b"] != b or r["phase"] != 1:
            return
        r["promises"][src] = (ab, av)
        if len(r["promises"]) < self.sim.maj:
            return
        votes = [p for p in r["promises"].values() if p[0] is not None]
        v = max(votes)[1] if votes and not self.sim.unsafe_revoke else NOOP  # @line L8
        r["phase"], r["v"] = 2, v
        self.sim.broadcast(self.pid, ("ACCEPT", j, b, v), self_too=True)

    def on_accept(self, j: int, b: tuple, v: str, src: int) -> None:
        self.maxk = max(self.maxk, b[0])
        st = self.a(j)
        if b >= st[0]:
            st[0], st[1], st[2] = b, b, v
            self.sim.send(self.pid, src, ("ACCEPTED", j, b))  # @line L9
        else:
            self.sim.send(self.pid, src, ("NACK", j, st[0]))

    def on_accepted(self, j: int, b: tuple, src: int) -> None:
        r = self.rev.get(j)
        if r is None or r["b"] != b or r["phase"] != 2:
            return
        r["acks"].add(src)
        if len(r["acks"]) == self.sim.maj:
            self.learn(j, r["v"])  # @line L10
            self.sim.broadcast(self.pid, ("LEARN", j, r["v"]))

    def on_nack(self, promised: tuple) -> None:
        self.maxk = max(self.maxk, promised[0])

    # ---- learning and execution ----
    def learn(self, j: int, v: str) -> None:
        if j in self.learned:
            if self.learned[j] != v:
                self.sim.violation = True
            return
        self.learned[j] = v
        if v == NOOP and self.mine.get(j, NOOP) != NOOP and not self.sim.no_rule4:
            self.suggest(self.mine[j])  # @line L11
        while self.next_exec in self.learned:
            x = self.learned[self.next_exec]
            if x != NOOP:
                self.executed.append(x)  # @line L12
            self.next_exec += 1


class Mencius:
    def __init__(self, n: int, seed: int, commands: list, clients_at: Optional[list] = None,
                 dup: float = 0.0, crashes: int = 0, crash_prob: float = 0.0,
                 suspect_prob: float = 0.0, ticks: bool = True, no_skip: bool = False,
                 unsafe_revoke: bool = False, no_rule4: bool = False,
                 max_steps: int = 100000) -> None:
        self.n, self.maj = n, n // 2 + 1
        self.rng = random.Random(seed)
        self.commands = list(commands)
        self.clients_at = clients_at if clients_at is not None else list(range(n))
        self.dup = dup
        self.crashes_left, self.crash_prob = crashes, crash_prob
        self.suspect_prob, self.ticks = suspect_prob, ticks
        self.no_skip, self.unsafe_revoke, self.no_rule4 = no_skip, unsafe_revoke, no_rule4
        self.max_steps = max_steps
        self.servers = [Server(self, p) for p in range(n)]
        self.crashed: set = set()
        self.net: list = []
        self.max_suggested = -1
        self.violation = False
        self.skips = self.revocations = 0
        self.sent_to: dict = {}            # command -> the server that suggested it first

    def send(self, src: int, dst: int, msg: tuple) -> None:
        self.net.append((src, dst, msg))
        if self.rng.random() < self.dup:
            self.net.append((src, dst, msg))

    def broadcast(self, src: int, msg: tuple, self_too: bool = False) -> None:
        for dst in range(self.n):
            if dst != src or self_too:
                self.send(src, dst, msg)

    def deliver(self, src: int, dst: int, msg: tuple) -> None:
        if dst in self.crashed:
            return
        s, kind = self.servers[dst], msg[0]
        if kind == "SUGGEST":
            s.on_suggest(msg[1], msg[2], src)
        elif kind == "ACK":
            s.on_ack(msg[1], src)
        elif kind == "SKIP":
            s.on_skip(msg[1])
        elif kind == "LEARN":
            s.learn(msg[1], msg[2])
        elif kind == "PREPARE":
            s.on_prepare(msg[1], msg[2], src)
        elif kind == "PROMISE":
            s.on_promise(msg[1], msg[2], msg[3], msg[4], src)
        elif kind == "ACCEPT":
            s.on_accept(msg[1], msg[2], msg[3], src)
        elif kind == "ACCEPTED":
            s.on_accepted(msg[1], msg[2], src)
        else:
            s.on_nack(msg[2])

    def live(self) -> list:
        return [s for s in self.servers if s.pid not in self.crashed]

    def done(self) -> bool:
        return all(j in s.learned for s in self.live() for j in range(self.max_suggested + 1))

    def run(self) -> "Mencius":
        pending = list(self.commands)
        for _ in range(self.max_steps):
            live = self.live()
            if pending and self.rng.random() < 0.2:
                cands = [p for p in self.clients_at if p not in self.crashed]
                if cands:
                    p = self.rng.choice(cands)
                    self.sent_to[pending[0]] = p
                    self.servers[p].suggest(pending.pop(0))
            if self.crashes_left and self.rng.random() < self.crash_prob and len(live) > 1:
                self.crashed.add(self.rng.choice(live).pid)
                self.crashes_left -= 1
            if self.suspect_prob and self.rng.random() < self.suspect_prob:
                p = self.rng.choice(self.live())
                p.revoke_owner(self.rng.choice([q for q in range(self.n) if q != p.pid]))
            if self.net:
                i = self.rng.randrange(len(self.net))
                self.net[i], self.net[-1] = self.net[-1], self.net[i]
                self.deliver(*self.net.pop())
                continue
            if pending:
                continue
            if self.done() or not self.ticks:
                break
            # Quiet network: a timeout fires at one live server, which revokes
            # every instance below its own index that it has not learned.
            p = self.rng.choice(self.live())
            for q in range(self.n):
                p.revoke_owner(q)
        return self

    def logs_agree(self) -> bool:
        logs = [s.executed for s in self.live()]
        longest = max(logs, key=len)
        return all(lg == longest[:len(lg)] for lg in logs)

    def no_duplicates(self) -> bool:
        return all(len(s.executed) == len(set(s.executed)) for s in self.servers)

    def all_executed(self, commands: Optional[list] = None) -> bool:
        want = set(self.commands if commands is None else commands)
        return all(want <= set(s.executed) for s in self.live())
