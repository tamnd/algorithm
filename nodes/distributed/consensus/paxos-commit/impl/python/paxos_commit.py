# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paxos-commit/. The authors are listed in prov/KZW5JY.jsonl.
"""Paxos Commit in a seeded discrete-event simulator.

N resource managers (RMs), 2F + 1 acceptors and some leaders. Each RM's vote,
Prepared or Aborted, is chosen by its own Paxos instance, in which ballot 0
belongs to the RM itself. The transaction commits if and only if every
instance chooses Prepared. Messages can be delayed, reordered and duplicated.
Messages already sent by a node that crashes are still delivered.
"""

import random
from collections import Counter
from typing import Optional

PREPARED, ABORTED = "Prepared", "Aborted"
B0 = (0, -1)          # ballot 0, owned by the RM of each instance


class PaxosCommit:
    def __init__(self, n_rm: int, f: int, seed: int, abort_prob: float = 0.0,
                 n_leaders: int = 1, dup: float = 0.0, leader_crash_prob: float = 0.0,
                 acc_crashes: int = 0, rm_crash_prob: float = 0.0, crash_prob: float = 0.02,
                 timeout_prob: float = 0.0, unsafe_recovery: bool = False,
                 max_steps: int = 100000) -> None:
        self.timeout_prob = timeout_prob
        self.N, self.F = n_rm, f
        self.n_acc, self.maj = 2 * f + 1, f + 1
        self.rng = random.Random(seed)
        self.abort_prob, self.n_leaders, self.dup = abort_prob, n_leaders, dup
        self.leader_crash_prob, self.rm_crash_prob = leader_crash_prob, rm_crash_prob
        self.acc_crashes_left, self.crash_prob = acc_crashes, crash_prob
        self.unsafe_recovery, self.max_steps = unsafe_recovery, max_steps
        self.crashed: set = set()
        self.net: list = []
        self.count: Counter = Counter()
        # RM state
        self.vote: dict = {}               # rm -> its vote, once cast
        self.outcome: dict = {}            # rm -> the outcome it learned
        # acceptor state
        self.promised = [B0] * self.n_acc
        self.accepted = [dict() for _ in range(self.n_acc)]   # rm -> (ballot, value)
        self.sent_b0 = [False] * self.n_acc
        # leader state
        self.maxk = [0] * n_leaders
        self.reports = [dict() for _ in range(n_leaders)]     # (ballot, acc) -> {rm: value}
        self.ph1 = [None] * n_leaders                         # ballot, 1b replies
        self.decided: dict = {}            # leader -> outcome it decided
        self.recoveries = 0

    # ---- network ----
    def send(self, src: tuple, dst: tuple, msg: tuple) -> None:
        self.count[msg[0]] += 1
        self.net.append((src, dst, msg))
        if self.rng.random() < self.dup:
            self.net.append((src, dst, msg))

    def deliver(self, src: tuple, dst: tuple, msg: tuple) -> None:
        if dst in self.crashed:
            return
        kind, role, x = msg[0], dst[0], dst[1]
        if kind == "BeginCommit":
            self.leader_on_begin(x)
        elif kind == "Prepare":
            self.rm_vote(x)
        elif kind == "2a":
            self.acc_on_2a(x, msg[1], msg[2])
        elif kind == "2b":
            self.leader_on_2b(x, src[1], msg[1], msg[2])
        elif kind == "1a":
            self.acc_on_1a(x, msg[1], src)
        elif kind == "1b":
            self.leader_on_1b(x, src[1], msg[1], msg[2])
        elif kind == "Outcome":
            self.rm_on_outcome(x, msg[1])

    # ---- resource managers ----
    def rm_vote(self, r: int) -> None:
        if r in self.vote:
            return
        v = ABORTED if self.rng.random() < self.abort_prob else PREPARED
        self.vote[r] = v                   # written to stable storage first
        for a in range(self.maj):
            self.send(("rm", r), ("acc", a), ("2a", {r: v}, B0))  # @line L3

    def rm_on_outcome(self, r: int, out: str) -> None:
        if r in self.outcome and self.outcome[r] != out:
            self.outcome[r] = "CONFLICT"
        self.outcome.setdefault(r, out)  # @line L12

    # ---- acceptors ----
    def acc_on_2a(self, a: int, vals: dict, b: tuple) -> None:
        if b < self.promised[a]:
            return
        self.promised[a] = b
        for r, v in vals.items():
            self.accepted[a][r] = (b, v)  # @line L4
        if b != B0:
            for ldr in range(self.n_leaders):
                if ldr == b[1]:
                    self.send(("acc", a), ("ldr", ldr), ("2b", b, dict(vals)))
            return
        if not self.sent_b0[a] and all(r in self.accepted[a] for r in range(self.N)):
            self.sent_b0[a] = True
            mine = {r: v for r, (bb, v) in self.accepted[a].items()}
            for ldr in range(self.n_leaders):
                self.send(("acc", a), ("ldr", ldr), ("2b", B0, mine))  # @line L5

    def acc_on_1a(self, a: int, b: tuple, src: tuple) -> None:
        if b > self.promised[a]:
            self.promised[a] = b
            self.send(("acc", a), src, ("1b", b, dict(self.accepted[a])))  # @line L9

    # ---- leaders ----
    def leader_on_begin(self, ldr: int) -> None:
        for r in range(1, self.N):
            self.send(("ldr", ldr), ("rm", r), ("Prepare",))  # @line L2

    def leader_on_2b(self, ldr: int, a: int, b: tuple, vals: dict) -> None:
        if ldr in self.decided:
            return
        rep = self.reports[ldr]
        rep[(b, a)] = vals
        chosen: dict = {}
        for r in range(self.N):
            for bb in {k[0] for k in rep}:
                n = sum(1 for (b2, _), vs in rep.items() if b2 == bb and r in vs)
                if n >= self.maj:  # @line L6
                    chosen[r] = next(vs[r] for (b2, _), vs in rep.items() if b2 == bb and r in vs)
        if ABORTED in chosen.values():
            out = ABORTED
        elif len(chosen) == self.N:
            out = "Committed"
        else:
            return
        self.decided[ldr] = out
        for r in range(self.N):
            self.send(("ldr", ldr), ("rm", r), ("Outcome", out))  # @line L7

    def start_recovery(self, ldr: int) -> None:
        self.recoveries += 1
        self.maxk[ldr] = max(self.maxk) + 1
        b = (self.maxk[ldr], ldr)
        self.ph1[ldr] = (b, {})
        for a in range(self.n_acc):
            self.send(("ldr", ldr), ("acc", a), ("1a", b))  # @line L8

    def leader_on_1b(self, ldr: int, a: int, b: tuple, acc: dict) -> None:
        if self.ph1[ldr] is None or self.ph1[ldr][0] != b:
            return
        replies = self.ph1[ldr][1]
        replies[a] = acc
        if len(replies) != self.maj:
            return
        vals = {}
        for r in range(self.N):
            seen = [rep[r] for rep in replies.values() if r in rep]
            if seen and not self.unsafe_recovery:
                vals[r] = max(seen)[1]
            else:
                vals[r] = ABORTED  # @line L10
        for a2 in range(self.n_acc):
            self.send(("ldr", ldr), ("acc", a2), ("2a", vals, b))  # @line L11

    # ---- the run ----
    def live_leaders(self) -> list:
        return [x for x in range(self.n_leaders) if ("ldr", x) not in self.crashed]

    def finished(self) -> bool:
        return all(r in self.outcome for r in range(self.N) if ("rm", r) not in self.crashed)

    def run(self) -> "PaxosCommit":
        self.rm_vote(0)
        self.send(("rm", 0), ("ldr", 0), ("BeginCommit",))  # @line L1
        for _ in range(self.max_steps):
            rng = self.rng
            if rng.random() < self.crash_prob:
                what = rng.random()
                live = self.live_leaders()
                if what < self.leader_crash_prob and len(live) > 1:
                    self.crashed.add(("ldr", rng.choice(live)))
                elif what < self.leader_crash_prob + self.rm_crash_prob:
                    self.crashed.add(("rm", rng.randrange(self.N)))
                elif self.acc_crashes_left:
                    accs = [a for a in range(self.n_acc) if ("acc", a) not in self.crashed]
                    self.crashed.add(("acc", rng.choice(accs)))
                    self.acc_crashes_left -= 1
            if self.timeout_prob and rng.random() < self.timeout_prob and self.live_leaders():
                # A timeout that fires too early: safe, but it may abort.
                self.start_recovery(rng.choice(self.live_leaders()))
            if self.net:
                i = rng.randrange(len(self.net))
                self.net[i], self.net[-1] = self.net[-1], self.net[i]
                self.deliver(*self.net.pop())
                continue
            if self.finished() or not self.live_leaders():
                break
            # Quiet network and an RM without an outcome: a leader times out.
            self.start_recovery(rng.choice(self.live_leaders()))
        return self

    def consistent(self) -> bool:
        outs = set(self.decided.values()) | {o for o in self.outcome.values()}
        return "CONFLICT" not in outs and len(outs) <= 1

    def valid(self) -> bool:
        """Commit only if every RM voted Prepared."""
        if "Committed" in self.outcome.values() or "Committed" in self.decided.values():
            return all(self.vote.get(r) == PREPARED for r in range(self.N))
        return True

    def result(self) -> Optional[str]:
        outs = set(self.outcome.values())
        return outs.pop() if len(outs) == 1 else None
