# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cluster-reconfiguration/. The authors are listed in prov/3KQHHP.jsonl.
"""Membership changes in a small model of a Raft log.

A configuration is a frozenset of servers, or a pair (old, new) for the joint
configuration of joint consensus. A quorum of a simple configuration is a
majority of it; a quorum of a joint one is a majority of old and a majority of
new. As in Raft, each server uses the latest configuration in its log, whether
it is committed or not.

The model is adversarial: elections, replication and commits happen in a
random order, and a leader counts acknowledgements it got earlier even if the
follower has since moved on. It checks that no two leaders commit different
entries at the same index.
"""

import itertools
import random
from typing import Optional


def is_quorum(cfg, votes: set) -> bool:
    if isinstance(cfg, tuple):
        return is_quorum(cfg[0], votes) and is_quorum(cfg[1], votes)
    return 2 * len(cfg & votes) > len(cfg)


def members(cfg) -> frozenset:
    return cfg[0] | cfg[1] if isinstance(cfg, tuple) else cfg


def quorums(cfg, universe: frozenset) -> list:
    """All minimal quorums of cfg, as sets."""
    out: list = []
    for k in range(1, len(universe) + 1):
        for q in itertools.combinations(sorted(universe), k):
            s = set(q)
            if is_quorum(cfg, s) and not any(o <= s for o in out):
                out.append(s)
    return out


def always_meet(c1, c2) -> bool:
    """Every quorum of c1 meets every quorum of c2."""
    u = members(c1) | members(c2)
    return all(q1 & q2 for q1 in quorums(c1, u) for q2 in quorums(c2, u))


class Server:
    def __init__(self, sid: int, cfg0: frozenset) -> None:
        self.sid, self.cfg0 = sid, cfg0
        self.term = 0
        self.voted: dict = {}
        self.log: list = []                # entries (term, eid, cfg or None)
        self.leader_of: Optional[int] = None
        self.acked: dict = {}              # leader only: server -> matched length
        self.commit = 0

    def config(self):
        for e in reversed(self.log):
            if e[2] is not None:
                return e[2]
        return self.cfg0

    def last(self) -> tuple:
        return (self.log[-1][0] if self.log else 0, len(self.log))


class Model:
    """mode is "joint", "single" or "direct". With noop_rule, a new leader
    must commit an entry of its own term before it adds a configuration."""

    def __init__(self, seed: int, mode: str, noop_rule: bool, universe: int = 5,
                 cfg0: tuple = (1, 2, 3)) -> None:
        self.rng = random.Random(seed)
        self.mode, self.noop_rule = mode, noop_rule
        self.universe = frozenset(range(1, universe + 1))
        c0 = frozenset(cfg0)
        self.s = {i: Server(i, c0) for i in self.universe}
        self.committed: dict = {}
        self.violation = False
        self.eid = 0
        self.changes = 0

    # ---- Raft steps ----
    def elect(self, c: int, voters: set) -> bool:
        cand = self.s[c]
        cand.term += 1
        t = cand.term
        cand.voted[t] = c
        got = {c}
        for v in voters - {c}:
            sv = self.s[v]
            if sv.term > t or sv.voted.get(t, c) != c:
                continue
            if cand.last() < sv.last():    # the log must be up to date
                continue
            sv.term, sv.voted[t] = t, c
            sv.leader_of = None
            got.add(v)
        if not is_quorum(cand.config(), got):
            return False
        cand.leader_of, cand.acked = t, {c: len(cand.log)}
        return True

    def append(self, ldr: Server, cfg=None) -> None:
        self.eid += 1
        ldr.log.append((ldr.term, self.eid, cfg))
        ldr.acked[ldr.sid] = len(ldr.log)

    def replicate(self, ldr: Server, f: int, k: int) -> None:
        fs = self.s[f]
        if fs.term > ldr.term or f == ldr.sid:
            return
        fs.term = ldr.term
        if fs.leader_of is not None and fs.leader_of < ldr.term:
            fs.leader_of = None
        lcp = 0
        while lcp < min(len(fs.log), len(ldr.log)) and fs.log[lcp] == ldr.log[lcp]:
            lcp += 1
        fs.log = list(ldr.log[:max(k, lcp)])
        ldr.acked[f] = max(ldr.acked.get(f, 0), len(fs.log))

    def try_commit(self, ldr: Server) -> None:
        cfg = ldr.config()
        for i in range(len(ldr.log), ldr.commit, -1):
            if ldr.log[i - 1][0] != ldr.term:
                continue
            votes = {x for x, n in ldr.acked.items() if n >= i}
            if is_quorum(cfg, votes):
                ldr.commit = i
                for j in range(i):
                    if self.committed.setdefault(j, ldr.log[j][1]) != ldr.log[j][1]:
                        self.violation = True
                return

    def config_committed(self, ldr: Server) -> bool:
        last_cfg = max((i for i, e in enumerate(ldr.log) if e[2] is not None), default=-1)
        return last_cfg < ldr.commit

    def own_term_committed(self, ldr: Server) -> bool:
        return any(e[0] == ldr.term for e in ldr.log[:ldr.commit])

    def change(self, ldr: Server, new: Optional[frozenset] = None) -> bool:
        if not self.config_committed(ldr):
            return False
        if self.noop_rule and not self.own_term_committed(ldr):
            return False
        cur = ldr.config()
        if isinstance(cur, tuple):
            self.append(ldr, cur[1])       # second step of joint consensus
            self.changes += 1
            return True
        if new is None:
            if self.mode == "single":
                x = self.rng.choice(sorted(self.universe))
                new = cur - {x} if x in cur else cur | {x}
            else:
                new = frozenset(x for x in self.universe if self.rng.random() < 0.6)
        if not new or new == cur:
            return False
        self.changes += 1
        self.append(ldr, (cur, new) if self.mode == "joint" else new)
        return True

    # ---- a random run ----
    def leaders(self) -> list:
        return [x for x in self.s.values() if x.leader_of == x.term]

    def run(self, steps: int = 80) -> "Model":
        rng = self.rng
        for _ in range(steps):
            r = rng.random()
            lds = self.leaders()
            if r < 0.2 or not lds:
                c = rng.choice(sorted(self.universe))
                voters = {x for x in self.universe if rng.random() < 0.6}
                if self.elect(c, voters) and self.noop_rule:
                    self.append(self.s[c])
                continue
            ldr = rng.choice(lds)
            if r < 0.4:
                self.append(ldr)
            elif r < 0.55:
                self.change(ldr)
            elif r < 0.9:
                f = rng.choice(sorted(self.universe))
                self.replicate(ldr, f, rng.randrange(len(ldr.log) + 1))
            else:
                self.try_commit(ldr)
        return self


def ongaro_scenario(noop_rule: bool) -> dict:
    """The 2015 counterexample for single-server changes in Raft.

    C0 = {1, 2, 3, 4}. Leader 1 adds server 5, but the entry reaches only
    server 5. Leader 2 removes server 1 and commits that with {2, 3}. Then
    server 1 wins an election with {1, 4, 5} and commits its own log."""
    m = Model(0, "single", noop_rule, universe=5, cfg0=(1, 2, 3, 4))
    s = m.s
    m.elect(1, {1, 2, 3, 4})
    m.append(s[1])
    for f in (2, 3, 4, 5):
        m.replicate(s[1], f, 1)
    m.try_commit(s[1])                     # entry 1 is committed
    m.change(s[1], frozenset({1, 2, 3, 4, 5}))
    m.replicate(s[1], 5, 2)                # C_add reaches only server 5
    out = {"leader2": m.elect(2, {2, 3, 4})}
    c_remove = frozenset({2, 3, 4})
    if noop_rule:
        m.append(s[2])                     # the no-op of term 2
        for f in (3, 4):
            m.replicate(s[2], f, len(s[2].log))
        m.try_commit(s[2])                 # it needs 3 of the 4 old servers
    out["c_remove_added"] = m.change(s[2], c_remove)
    m.replicate(s[2], 3, len(s[2].log))
    m.try_commit(s[2])                     # 2 of {2, 3, 4} is a majority
    out["c_remove_committed"] = s[2].commit == len(s[2].log)
    # server 1 times out, and tries again with a higher term
    out["leader1_again"] = m.elect(1, {1, 4, 5}) or m.elect(1, {1, 4, 5})
    if out["leader1_again"]:
        m.append(s[1])
        for f in (4, 5):
            m.replicate(s[1], f, len(s[1].log))
        m.try_commit(s[1])
    out["violation"] = m.violation
    return out
