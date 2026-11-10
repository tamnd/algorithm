# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viewstamped-replication/. The authors are listed in prov/FP530T.jsonl.
"""Viewstamped Replication (the 2012 "Revisited" protocol) in a seeded simulator.

N = 2f + 1 replicas, no stable storage. The primary of view v is replica
v mod N. The simulator covers normal operation, view changes and the recovery
of a replica that lost its state. Messages can be delayed, reordered and
duplicated. A replica that crashes loses all state and later runs recovery.
At most f replicas are crashed or recovering at any time.
"""

import random
from typing import Optional


class Replica:
    def __init__(self, sim: "VR", i: int) -> None:
        self.sim, self.i = sim, i
        self.reset()

    def reset(self, status: str = "normal") -> None:
        self.view = 0
        self.status = status
        self.log: list = []
        self.commit = 0
        self.last_normal = 0
        self.executed: list = []
        self.ack_hi: dict = {}             # primary: backup -> highest n acknowledged
        self.svc: dict = {}                # view -> senders of StartViewChange
        self.dvc: dict = {}                # view -> sender -> (v', log, k)
        self.sent_dvc: set = set()
        self.held: list = []               # messages of a later view, kept for later
        self.pending: dict = {}            # backup: n -> op, received out of order
        self.nonce: Optional[int] = None
        self.responses: dict = {}

    def primary(self, v: int) -> int:
        return v % self.sim.n

    def is_primary(self) -> bool:
        return self.status == "normal" and self.primary(self.view) == self.i

    def execute(self) -> None:
        while len(self.executed) < self.commit:
            self.executed.append(self.log[len(self.executed)])

    def set_view(self, v: int) -> None:
        self.view = v
        held, self.held = self.held, []
        for m in held:
            self.sim.net.append(m)

    # ---- normal operation ----
    def on_request(self, op: str) -> None:
        if not self.is_primary():
            return
        if op in self.log:
            if op in self.log[:self.commit]:
                self.sim.replied.add(op)
            return
        self.log.append(op)  # @line L1
        n = len(self.log)
        self.sim.bcast(self.i, ("PREPARE", self.view, op, n, self.commit))

    def on_prepare(self, v: int, op: str, n: int, k: int) -> None:
        self.pending[n] = op
        while len(self.log) + 1 in self.pending:
            self.log.append(self.pending.pop(len(self.log) + 1))  # @line L2
        self.sim.send(self.i, self.primary(v), ("PREPAREOK", v, len(self.log)))
        self.on_commit(k)

    def on_prepare_ok(self, n: int, src: int) -> None:
        if not self.is_primary():
            return
        # n never exceeds the log of a correct primary; the clamp matters only
        # in the broken variant where a primary forgets its log.
        self.ack_hi[src] = min(max(self.ack_hi.get(src, 0), n), len(self.log))
        his = sorted(self.ack_hi.values(), reverse=True)
        if len(his) >= self.sim.f and his[self.sim.f - 1] > self.commit:
            self.commit = his[self.sim.f - 1]  # @line L3
            self.sim.record_commit(self.view, self.log[:self.commit])
            self.execute()
            for op in self.log[:self.commit]:
                self.sim.replied.add(op)
            self.sim.bcast(self.i, ("COMMIT", self.view, self.commit))

    def on_commit(self, k: int) -> None:
        self.commit = max(self.commit, min(k, len(self.log)))
        self.execute()  # @line L4

    # ---- view change ----
    def start_view_change(self, v: int) -> None:
        if v <= self.view and self.status != "normal":
            return
        if v <= self.view:
            v = self.view + 1
        self.set_view(v)
        self.status = "view-change"  # @line L5
        self.pending = {}
        self.sim.bcast(self.i, ("SVC", v))
        self.maybe_send_dvc(v)

    def on_svc(self, v: int, src: int) -> None:
        if v > self.view:
            self.start_view_change(v)
        if v == self.view and self.status == "view-change":
            self.svc.setdefault(v, set()).add(src)
            self.maybe_send_dvc(v)

    def maybe_send_dvc(self, v: int) -> None:
        if len(self.svc.get(v, ())) >= self.sim.f and v not in self.sent_dvc:
            self.sent_dvc.add(v)
            msg = ("DVC", v, self.last_normal, list(self.log), self.commit)
            self.sim.send(self.i, self.primary(v), msg)  # @line L6

    def on_dvc(self, v: int, vn: int, log: list, k: int, src: int) -> None:
        if v > self.view:
            self.start_view_change(v)
        if v != self.view or self.status != "view-change":
            return
        got = self.dvc.setdefault(v, {})
        got.setdefault(src, (vn, log, k))
        if len(got) < self.sim.f + 1:
            return
        if self.sim.unsafe_pick:
            best = next(iter(got.values()))
        else:
            best = max(got.values(), key=lambda t: (t[0], len(t[1])))  # @line L7
        self.log = list(best[1])
        self.commit = min(max(t[2] for t in got.values()), len(self.log))
        self.status, self.last_normal, self.ack_hi = "normal", v, {}  # @line L8
        self.sim.record_commit(v, self.log[:self.commit])
        self.execute()
        self.sim.bcast(self.i, ("STARTVIEW", v, list(self.log), self.commit))

    def on_start_view(self, v: int, log: list, k: int) -> None:
        if v < self.view or (v == self.view and self.status == "normal"):
            return
        self.set_view(v)
        self.log, self.status, self.last_normal = list(log), "normal", v  # @line L9
        self.pending = {}
        self.commit = min(self.commit, len(self.log))
        self.on_commit(k)
        if len(self.log) > self.commit:
            self.sim.send(self.i, self.primary(v), ("PREPAREOK", v, len(self.log)))

    # ---- recovery ----
    def start_recovery(self) -> None:
        self.sim.nonce += 1
        self.nonce, self.responses = self.sim.nonce, {}
        self.sim.bcast(self.i, ("RECOVERY", self.nonce))  # @line L10

    def on_recovery(self, nonce: int, src: int) -> None:
        if self.status != "normal":
            return
        state = (list(self.log), self.commit) if self.is_primary() else None
        self.sim.send(self.i, src, ("RECRESP", self.view, nonce, state))  # @line L11

    def on_recovery_response(self, v: int, nonce: int, state: Optional[tuple], src: int) -> None:
        if self.status != "recovering" or nonce != self.nonce:
            return
        self.responses[src] = (v, state)
        if len(self.responses) < self.sim.f + 1:
            return
        top = max(r[0] for r in self.responses.values())
        p = top % self.sim.n
        if p not in self.responses or self.responses[p][0] != top:
            return
        log, k = self.responses[p][1]
        self.view, self.log, self.commit = top, list(log), k  # @line L12
        self.status, self.last_normal = "normal", top
        self.execute()


class VR:
    def __init__(self, f: int, seed: int, ops: list, dup: float = 0.0,
                 crash_prob: float = 0.0, view_change_prob: float = 0.0,
                 unsafe_pick: bool = False, amnesia: bool = False,
                 max_steps: int = 60000) -> None:
        self.f, self.n = f, 2 * f + 1
        self.rng = random.Random(seed)
        self.ops = list(ops)
        self.dup, self.crash_prob, self.view_change_prob = dup, crash_prob, view_change_prob
        self.unsafe_pick, self.amnesia = unsafe_pick, amnesia
        self.max_steps = max_steps
        self.replicas = [Replica(self, i) for i in range(self.n)]
        self.down: set = set()             # crashed and not yet recovering
        self.net: list = []
        self.replied: set = set()
        self.committed: dict = {}          # position -> op, as seen by primaries
        self.violation = False
        self.history: list = []            # executed lists of replicas that crashed
        self.nonce = 0
        self.view_changes = self.recoveries = 0

    def send(self, src: int, dst: int, msg: tuple) -> None:
        self.net.append((src, dst, msg))
        if self.rng.random() < self.dup:
            self.net.append((src, dst, msg))

    def bcast(self, src: int, msg: tuple) -> None:
        for d in range(self.n):
            if d != src:
                self.send(src, d, msg)

    def record_commit(self, v: int, prefix: list) -> None:
        for pos, op in enumerate(prefix):
            if self.committed.setdefault(pos, op) != op:
                self.violation = True

    def deliver(self, src: int, dst: int, msg: tuple) -> None:
        if dst in self.down:
            return
        r, kind = self.replicas[dst], msg[0]
        if kind == "REQUEST":
            r.on_request(msg[1])
            return
        if r.status == "recovering":
            if kind == "RECRESP":
                r.on_recovery_response(msg[1], msg[2], msg[3], src)
            return
        if kind == "RECOVERY":
            r.on_recovery(msg[1], src)
        elif kind == "SVC":
            r.on_svc(msg[1], src)
        elif kind == "DVC":
            r.on_dvc(msg[1], msg[2], msg[3], msg[4], src)
        elif kind == "STARTVIEW":
            r.on_start_view(msg[1], msg[2], msg[3])
        elif kind in ("PREPARE", "PREPAREOK", "COMMIT"):
            v = msg[1]
            if v > r.view or (v == r.view and r.status != "normal"):
                r.held.append((src, dst, msg))   # wait for the StartView of v
            elif v == r.view:
                if kind == "PREPARE":
                    r.on_prepare(v, msg[2], msg[3], msg[4])
                elif kind == "PREPAREOK":
                    r.on_prepare_ok(msg[2], src)
                else:
                    r.on_commit(msg[2])

    def out_of_service(self) -> int:
        return len(self.down) + sum(1 for r in self.replicas if r.status == "recovering")

    def crash(self, i: int) -> None:
        r = self.replicas[i]
        self.history.append(list(r.executed))
        self.down.add(i)
        r.reset()

    def restart(self, i: int) -> None:
        self.down.discard(i)
        r = self.replicas[i]
        self.recoveries += 1
        if self.amnesia:
            # Wrong: rejoin at once with an empty log, as if nothing happened.
            r.reset("normal")
            return
        r.reset("recovering")
        r.start_recovery()

    def run(self) -> "VR":
        pending = list(self.ops)
        rng = self.rng
        for _ in range(self.max_steps):
            if pending and rng.random() < 0.15:
                op = pending.pop(0)
                for d in range(self.n):
                    self.send(-1, d, ("REQUEST", op))
            if self.crash_prob and rng.random() < self.crash_prob:
                up = [i for i in range(self.n) if i not in self.down]
                if self.out_of_service() < self.f:
                    self.crash(rng.choice(up))
                elif self.down:
                    self.restart(rng.choice(sorted(self.down)))
            if self.view_change_prob and rng.random() < self.view_change_prob:
                self.timeout()
            if self.net:
                j = rng.randrange(len(self.net))
                self.net[j], self.net[-1] = self.net[-1], self.net[j]
                self.deliver(*self.net.pop())
                continue
            if pending:
                continue
            for i in sorted(self.down):
                self.restart(i)
            if self.settled():
                break
            # Quiet network. An idle primary sends Commit as a heartbeat to
            # backups that are behind; otherwise clients resend unanswered
            # requests, or a timeout fires.
            beat = False
            for p in self.replicas:
                if p.i not in self.down and p.is_primary() and any(
                        r.i not in self.down and r.view == p.view and r.commit < p.commit
                        for r in self.replicas):
                    self.bcast(p.i, ("COMMIT", p.view, p.commit))
                    beat = True
            if beat:
                continue
            for r in self.replicas:
                if r.status == "recovering" and r.i not in self.down:
                    r.start_recovery()
            if rng.random() < 0.5:
                for op in self.ops:
                    if op not in self.replied:
                        for d in range(self.n):
                            self.send(-1, d, ("REQUEST", op))
            else:
                self.timeout()
        return self

    def timeout(self) -> None:
        live = [r for r in self.replicas if r.i not in self.down and r.status != "recovering"]
        if live:
            self.view_changes += 1
            r = self.rng.choice(live)
            r.start_view_change(r.view + 1)

    def settled(self) -> bool:
        rs = [r for r in self.replicas if r.i not in self.down]
        return (set(self.ops) <= self.replied and all(r.status == "normal" for r in rs)
                and len({r.view for r in rs}) == 1
                and all(r.executed == rs[0].executed for r in rs)
                and len(rs[0].executed) == len(rs[0].log))

    # ---- checks ----
    def committed_kept(self) -> bool:
        """No two primaries committed different ops at one position, and every
        committed op is still at its position in the log of every replica in
        normal status."""
        if self.violation:
            return False
        for r in self.replicas:
            if r.i in self.down or r.status != "normal":
                continue
            for pos, op in self.committed.items():
                if pos >= len(r.log) or r.log[pos] != op:
                    return False
        return True

    def executions_agree(self) -> bool:
        runs = self.history + [r.executed for r in self.replicas]
        longest = max(runs, key=len)
        return all(x == longest[:len(x)] for x in runs)
