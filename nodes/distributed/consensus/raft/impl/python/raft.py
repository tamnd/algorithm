# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raft/. The authors are listed in prov/MSG4TW.jsonl.

"""Raft (Ongaro and Ousterhout 2014) as message handlers, run in a seeded discrete event simulator.

Each server is a state machine with one handler per message type. The
simulator holds the messages in flight in an explicit list. A seeded
scheduler picks the next event: deliver a message (in any order, so it
reorders), drop or duplicate it, fire an election timeout, send heartbeats,
take a client command, crash or restart a server, or change the partition.
The model is asynchronous with crash-recovery failures: current_term,
voted_for and log survive a crash, and all other state is lost.

The checks of the page run on every event: at most one leader per term
(election safety), the log matching property, state machine safety and
leader completeness. A violation is recorded in Cluster.violations.

commit_rule="raft" is the rule of the paper: a leader commits an index only
when the entry there has the leader's own term and a majority stores it.
commit_rule="count" drops the term test. It is unsafe, and the Figure 8 run
of the tests shows why.
"""

from __future__ import annotations

import random
from typing import Callable, Optional

FOLLOWER, CANDIDATE, LEADER = "follower", "candidate", "leader"

Entry = tuple[int, object]  # (term, command)
Msg = dict


class Server:
    """One Raft server. Handlers return the list of messages to send."""

    def __init__(self, sid: int, n: int, commit_rule: str = "raft") -> None:
        self.id, self.n, self.commit_rule = sid, n, commit_rule
        # persistent state (survives a crash)
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.log: list[Entry] = [(0, None)]  # index 0 is a sentinel
        # hooks set by the cluster
        self.on_leader: Callable[[int, int], None] = lambda sid, term: None
        self.on_commit: Callable[[int, int, int, int], None] = lambda sid, term, lo, hi: None
        self.on_apply: Callable[[int, int, Entry], None] = lambda sid, i, e: None
        self.reset_volatile()

    def reset_volatile(self) -> None:
        self.role = FOLLOWER
        self.heard = False
        self.votes: set[int] = set()
        self.commit_index = 0
        self.last_applied = 0
        self.state: list[object] = []  # the state machine: the applied commands
        self.next_index: dict[int, int] = {}
        self.match_index: dict[int, int] = {}

    def last_index(self) -> int:
        return len(self.log) - 1

    def last_term(self) -> int:
        return self.log[-1][0]

    def msg(self, kind: str, dst: int, **kw: object) -> Msg:
        return {"kind": kind, "src": self.id, "dst": dst, "term": self.current_term, **kw}

    def step_down(self, term: int) -> None:
        self.current_term = term  # @line L31
        self.role = FOLLOWER
        self.voted_for = None

    # ---- leader election
    def on_election_timeout(self) -> list[Msg]:
        """The election timer fires. It is reset when the server hears from a leader or grants a vote."""
        if self.role == LEADER or self.heard:
            self.heard = False
            return []
        self.current_term += 1  # @line L1
        self.role = CANDIDATE
        self.voted_for = self.id
        self.votes = {self.id}  # @line L2
        out = [self.msg("RV", j, last_index=self.last_index(), last_term=self.last_term())  # @line L3
               for j in range(self.n) if j != self.id]
        return out + self.maybe_win()

    def on_request_vote(self, m: Msg) -> list[Msg]:
        if m["term"] > self.current_term:
            self.step_down(m["term"])  # @line L4
        up_to_date = (m["last_term"] > self.last_term()  # @line L5
                      or (m["last_term"] == self.last_term() and m["last_index"] >= self.last_index()))
        grant = (m["term"] == self.current_term and self.voted_for in (None, m["src"])  # @line L6
                 and up_to_date)
        if grant:
            self.voted_for = m["src"]  # @line L7
            self.heard = True
        return [self.msg("RVR", m["src"], granted=grant)]  # @line L8

    def on_vote_reply(self, m: Msg) -> list[Msg]:
        if m["term"] > self.current_term:
            self.step_down(m["term"])  # @line L9
            return []
        if self.role == CANDIDATE and m["term"] == self.current_term and m["granted"]:
            self.votes.add(m["src"])  # @line L10
        return self.maybe_win()

    def maybe_win(self) -> list[Msg]:
        if self.role == CANDIDATE and 2 * len(self.votes) > self.n:  # @line L11
            self.role = LEADER
            self.next_index = {j: self.last_index() + 1 for j in range(self.n)}
            self.match_index = {j: 0 for j in range(self.n)}
            self.match_index[self.id] = self.last_index()
            self.on_leader(self.id, self.current_term)
            return self.heartbeat()
        return []

    # ---- log replication
    def client_request(self, cmd: object) -> list[Msg]:
        if self.role != LEADER:
            return []
        self.log.append((self.current_term, cmd))  # @line L12
        self.match_index[self.id] = self.last_index()
        out = self.heartbeat()
        self.advance_commit()  # a one-server cluster commits at once
        return out

    def heartbeat(self) -> list[Msg]:
        if self.role != LEADER:
            return []
        return [self.send_append(j) for j in range(self.n) if j != self.id]

    def send_append(self, j: int) -> Msg:
        prev = self.next_index[j] - 1  # @line L13
        return self.msg("AE", j, prev_index=prev, prev_term=self.log[prev][0],  # @line L14
                        entries=tuple(self.log[prev + 1:]), leader_commit=self.commit_index)

    def on_append_entries(self, m: Msg) -> list[Msg]:
        if m["term"] > self.current_term:
            self.step_down(m["term"])  # @line L15
        if m["term"] < self.current_term:
            return [self.msg("AER", m["src"], success=False, match=0)]  # @line L16
        if self.role == LEADER:
            raise AssertionError("two leaders in one term")  # election safety
        self.role = FOLLOWER  # @line L17
        self.heard = True
        p = m["prev_index"]
        if p > self.last_index() or self.log[p][0] != m["prev_term"]:  # @line L18
            return [self.msg("AER", m["src"], success=False, match=0)]
        for k, e in enumerate(m["entries"]):  # @line L19
            i = p + 1 + k
            if i <= self.last_index() and self.log[i][0] != e[0]:
                del self.log[i:]  # @line L20
            if i > self.last_index():
                self.log.append(e)  # @line L21
        last_new = p + len(m["entries"])
        if m["leader_commit"] > self.commit_index:
            self.commit_index = max(self.commit_index, min(m["leader_commit"], last_new))  # @line L22
        self.apply()
        return [self.msg("AER", m["src"], success=True, match=last_new)]  # @line L23

    def on_append_reply(self, m: Msg) -> list[Msg]:
        if m["term"] > self.current_term:
            self.step_down(m["term"])  # @line L24
            return []
        if self.role != LEADER or m["term"] != self.current_term:  # @line L25
            return []
        j = m["src"]
        if m["success"]:
            self.match_index[j] = max(self.match_index[j], m["match"])  # @line L26
            self.next_index[j] = self.match_index[j] + 1
            self.advance_commit()
            if self.match_index[j] < self.last_index():
                return [self.send_append(j)]
            return []
        self.next_index[j] = max(1, self.next_index[j] - 1)  # @line L27
        return [self.send_append(j)]

    def advance_commit(self) -> None:
        old = self.commit_index
        for big_n in range(self.last_index(), self.commit_index, -1):  # @line L28
            own_term = self.log[big_n][0] == self.current_term or self.commit_rule == "count"
            count = sum(1 for k in range(self.n) if self.match_index.get(k, 0) >= big_n)
            if own_term and 2 * count > self.n:  # @line L29
                self.commit_index = big_n
                break
        if self.commit_index > old:
            self.on_commit(self.id, self.current_term, old + 1, self.commit_index)
        self.apply()

    def apply(self) -> None:
        while self.last_applied < self.commit_index:  # @line L30
            self.last_applied += 1
            e = self.log[self.last_applied]
            self.state.append(e[1])
            self.on_apply(self.id, self.last_applied, e)


class Cluster:
    """A seeded simulator of n Raft servers with loss, duplication, reordering, partitions and crashes."""

    def __init__(self, n: int, seed: int = 0, commit_rule: str = "raft", drop: float = 0.0,
                 dup: float = 0.0, lifo: bool = False) -> None:
        self.n, self.rng, self.drop, self.dup, self.lifo = n, random.Random(seed), drop, dup, lifo
        self.servers = [Server(i, n, commit_rule) for i in range(n)]
        self.alive = [True] * n
        self.group = [0] * n  # servers talk only inside their group
        self.inflight: list[Msg] = []
        self.leaders: dict[int, set[int]] = {}  # term -> servers that led it
        self.committed: dict[int, tuple[Entry, int]] = {}  # index -> (entry, term of commit)
        self.applied: dict[int, Entry] = {}  # index -> entry applied there
        self.violations: list[str] = []
        self.next_cmd = 0
        for s in self.servers:
            s.on_leader, s.on_commit, s.on_apply = self._leader, self._commit, self._apply

    # ---- checks
    def _leader(self, sid: int, term: int) -> None:
        self.leaders.setdefault(term, set()).add(sid)
        if len(self.leaders[term]) > 1:
            self.violations.append(f"election safety: term {term} has leaders {sorted(self.leaders[term])}")
        log = self.servers[sid].log
        for i, (e, cterm) in self.committed.items():
            if term > cterm and (i >= len(log) or log[i] != e):
                self.violations.append(f"leader completeness: leader {sid} of term {term} lacks index {i}")

    def _commit(self, sid: int, term: int, lo: int, hi: int) -> None:
        log = self.servers[sid].log
        for i in range(lo, hi + 1):
            if i in self.committed and self.committed[i][0] != log[i]:
                self.violations.append(f"commit safety: index {i} committed twice with different entries")
            self.committed.setdefault(i, (log[i], term))

    def _apply(self, sid: int, i: int, e: Entry) -> None:
        if i in self.applied and self.applied[i] != e:
            self.violations.append(f"state machine safety: index {i} applied as {self.applied[i]} and {e}")
        self.applied.setdefault(i, e)

    def check_log_matching(self) -> None:
        logs = [s.log for s in self.servers]
        for a in range(self.n):
            for b in range(a + 1, self.n):
                la, lb = logs[a], logs[b]
                top = min(len(la), len(lb)) - 1
                # the highest index where the terms agree; the prefixes must then be equal
                for i in range(top, 0, -1):
                    if la[i][0] == lb[i][0]:
                        if la[: i + 1] != lb[: i + 1]:
                            self.violations.append(f"log matching: servers {a} and {b} at index {i}")
                        break

    # ---- the network and the events
    def send(self, msgs: list[Msg]) -> None:
        self.inflight.extend(msgs)

    def deliver(self, k: int) -> None:
        m = self.inflight.pop(k)
        src, dst = m["src"], m["dst"]
        if not self.alive[dst] or self.group[src] != self.group[dst]:
            return
        if self.drop and self.rng.random() < self.drop:
            return
        if self.dup and self.rng.random() < self.dup:
            self.inflight.append(dict(m))
        s = self.servers[dst]
        handler = {"RV": s.on_request_vote, "RVR": s.on_vote_reply,
                   "AE": s.on_append_entries, "AER": s.on_append_reply}[m["kind"]]
        try:
            self.send(handler(m))
        except AssertionError as err:
            self.violations.append(str(err))

    def timeout(self, i: int, force: bool = False) -> None:
        """Fire the election timer of server i. With force, it fires even if i heard a leader."""
        if force:
            self.servers[i].heard = False
        if self.alive[i]:
            self.send(self.servers[i].on_election_timeout())

    def heartbeat(self, i: int) -> None:
        if self.alive[i]:
            self.send(self.servers[i].heartbeat())

    def client(self, i: int, cmd: object) -> None:
        if self.alive[i]:
            self.send(self.servers[i].client_request(cmd))

    def crash(self, i: int) -> None:
        self.alive[i] = False

    def restart(self, i: int) -> None:
        if not self.alive[i]:
            self.alive[i] = True
            self.servers[i].reset_volatile()

    def run_group(self, group: set[int], limit: int = 10000) -> None:
        """Deliver, in order, every message inside group until none is left. Drop the others."""
        for _ in range(limit):
            self.inflight = [m for m in self.inflight if m["src"] in group and m["dst"] in group]
            if not self.inflight:
                return
            self.deliver(0)

    def random_step(self) -> None:
        r, n, rng = self.rng.random(), self.n, self.rng
        if r < 0.70 and self.inflight:
            self.deliver(len(self.inflight) - 1 if self.lifo else rng.randrange(len(self.inflight)))
        elif r < 0.76:
            self.timeout(rng.randrange(n))
        elif r < 0.86:
            self.heartbeat(rng.randrange(n))
        elif r < 0.94:
            leaders = [s.id for s in self.servers if s.role == LEADER and self.alive[s.id]]
            if leaders and self.next_cmd < 40:
                self.next_cmd += 1
                self.client(rng.choice(leaders), f"c{self.next_cmd}")
        elif r < 0.955:
            self.crash(rng.randrange(n))
        elif r < 0.98:
            self.restart(rng.randrange(n))
        elif r < 0.99:
            self.group = [rng.randrange(2) for _ in range(n)]
        else:
            self.group = [0] * n

    def run(self, steps: int) -> None:
        for t in range(steps):
            self.random_step()
            if t % 25 == 0:
                self.check_log_matching()
        self.check_log_matching()
