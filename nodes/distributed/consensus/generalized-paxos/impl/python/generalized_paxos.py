# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-paxos/. The authors are listed in prov/8MFRY7.jsonl.
"""Generalized Paxos over command histories, in a seeded discrete-event simulator.

A command is a pair (name, key). Two commands interfere when they are
different and have the same key. A c-struct is a command history: a set of
commands with an order for each pair of interfering commands.
"""

import random
from itertools import combinations
from typing import Iterable, Optional

Cmd = tuple


def interfere(c: Cmd, d: Cmd) -> bool:
    return c != d and c[1] == d[1]


class History:
    """A c-struct. Equal histories have equal command sets and equal orders."""

    __slots__ = ("cmds", "before")

    def __init__(self, cmds: Iterable = (), before: Iterable = ()) -> None:
        self.cmds = frozenset(cmds)
        self.before = frozenset(before)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, History) and self.cmds == other.cmds and self.before == other.before

    def __hash__(self) -> int:
        return hash((self.cmds, self.before))

    def __repr__(self) -> str:
        return f"History({sorted(self.cmds)}, {sorted(self.before)})"

    def append(self, c: Cmd) -> "History":
        """v . C: put C after every command of v that interferes with it."""
        if c in self.cmds:
            return self
        return History(self.cmds | {c}, self.before | {(d, c) for d in self.cmds if interfere(d, c)})

    @staticmethod
    def of(seq: Iterable[Cmd]) -> "History":
        h = BOTTOM
        for c in seq:
            h = h.append(c)
        return h


BOTTOM = History()


def prefix(v: History, w: History) -> bool:
    """v is a prefix of w: w = v . s for some sequence s."""
    if not v.cmds <= w.cmds or not v.before <= w.before:
        return False
    # Nothing outside v may come before a command of v.
    return all(x in v.cmds for (x, y) in w.before if y in v.cmds)


def glb(v: History, w: History) -> History:
    """The largest common prefix of v and w."""
    t = set(v.cmds & w.cmds)
    changed = True
    while changed:
        changed = False
        for c in sorted(t):
            bad = False
            for (x, y) in v.before | w.before:
                if y == c and x not in t:
                    bad = True  # c has a predecessor that is not common
                elif y == c and x in t and ((x, y) in v.before) != ((x, y) in w.before):
                    bad = True  # v and w order c and x in different ways
            if bad:
                t.discard(c)
                changed = True
    return History(t, {(x, y) for (x, y) in v.before if x in t and y in t})


def lub(v: History, w: History) -> Optional[History]:
    """The smallest common extension of v and w, or None if they are not compatible."""
    for x in v.cmds - w.cmds:
        for y in w.cmds - v.cmds:
            if interfere(x, y):
                return None
    u = History(v.cmds | w.cmds, v.before | w.before)
    if any((y, x) in u.before for (x, y) in u.before):
        return None
    if prefix(v, u) and prefix(w, u):
        return u
    return None


def glb_all(hs: Iterable[History]) -> History:
    hs = list(hs)
    g = hs[0]
    for h in hs[1:]:
        g = glb(g, h)
    return g


def lub_all(hs: Iterable[History]) -> Optional[History]:
    u = BOTTOM
    for h in hs:
        u = lub(u, h)
        if u is None:
            return None
    return u


def is_fast(m: tuple) -> bool:
    return m[0] % 2 == 0


class Inconsistent(Exception):
    pass


def proved_safe(reports: dict, n: int, qsize) -> History:
    """reports maps acceptor -> (vrnd, vval) from an m-quorum Q."""
    k = max(r[0] for r in reports.values())
    if k is None or k == (-1, -1):
        return BOTTOM
    q = set(reports)
    gammas = []
    for r in combinations(range(n), qsize(k)):  # minimal k-quorums are enough
        inter = q & set(r)
        if inter and all(reports[a][0] == k for a in inter):  # @line L3
            gammas.append(glb_all(reports[a][1] for a in sorted(inter)))
    if not gammas:
        return next(reports[a][1] for a in sorted(q) if reports[a][0] == k)  # @line L4
    u = lub_all(gammas)
    if u is None:
        raise Inconsistent("the values proved safe are not compatible")
    return u


class Acceptor:
    def __init__(self, sim: "GeneralizedPaxos", a: int) -> None:
        self.sim, self.a = sim, a
        self.bal = (-1, -1)
        self.vrnd = (-1, -1)
        self.vval = BOTTOM
        self.proposed: list[Cmd] = []

    def on_1a(self, m: tuple, src: str) -> None:
        if m > self.bal:
            self.bal = m  # @line L7
            self.sim.send(src, ("1b", m, self.a, self.vrnd, self.vval))
        else:
            self.sim.send(src, ("nack", self.bal))

    def on_2a(self, m: tuple, v: History, src: str) -> None:
        if m >= self.bal and (self.vrnd < m or prefix(self.vval, v)):
            self.bal, self.vrnd, self.vval = m, m, v  # @line L8
            if is_fast(m):
                for c in self.proposed:
                    self.vval = self.vval.append(c)
            self.send_2b()
        elif m < self.bal:
            self.sim.send(src, ("nack", self.bal))

    def on_propose(self, c: Cmd) -> None:
        if c not in self.proposed:
            self.proposed.append(c)
        if self.bal == self.vrnd and is_fast(self.vrnd) and c not in self.vval.cmds:
            self.vval = self.vval.append(c)  # @line L9
            self.send_2b()

    def send_2b(self) -> None:
        for dst in self.sim.learner_ids:
            self.sim.send(dst, ("2b", self.vrnd, self.a, self.vval))


class Leader:
    def __init__(self, sim: "GeneralizedPaxos", lid: int) -> None:
        self.sim, self.lid = sim, lid
        self.name = f"L{lid}"
        self.round_seen = -1
        self.ballot: Optional[tuple] = None
        self.phase = 0
        self.reports: dict = {}
        self.w = BOTTOM
        self.known: list[Cmd] = []

    def start(self, fast: bool) -> None:
        r = self.round_seen + 1
        if (r % 2 == 0) != fast:
            r += 1
        self.round_seen = r
        self.ballot = (r, self.lid)  # @line L1
        self.phase, self.reports = 1, {}
        self.sim.ballots_started += 1
        for a in range(self.sim.n):
            self.sim.send(a, ("1a", self.ballot, self.name))

    def on_1b(self, m: tuple, a: int, vrnd: tuple, vval: History) -> None:
        if m != self.ballot or self.phase != 1:
            return
        self.reports[a] = (vrnd, vval)
        if len(self.reports) < self.sim.qsize(m):  # @line L2
            return
        w = proved_safe(self.reports, self.sim.n, self.sim.qsize)
        for c in self.known:
            w = w.append(c)
        self.w, self.phase = w, 2
        self.broadcast_2a()

    def on_propose(self, c: Cmd) -> None:
        if c not in self.known:
            self.known.append(c)
        if self.phase == 2 and not is_fast(self.ballot) and c not in self.w.cmds:
            self.w = self.w.append(c)  # @line L5
            self.broadcast_2a()

    def on_nack(self, bal: tuple) -> None:
        self.round_seen = max(self.round_seen, bal[0])

    def broadcast_2a(self) -> None:
        self.sim.twoa_sent += 1
        for a in range(self.sim.n):
            self.sim.send(a, ("2a", self.ballot, self.w, self.name))


class Learner:
    def __init__(self, sim: "GeneralizedPaxos") -> None:
        self.sim = sim
        self.votes: dict = {}
        self.learned = BOTTOM
        self.history = [BOTTOM]

    def on_2b(self, m: tuple, a: int, v: History) -> None:
        mine = self.votes.setdefault(m, {})
        cur = mine.get(a)
        if cur is not None and not prefix(cur, v):
            return  # an older vote that arrived late
        mine[a] = v  # @line L10
        for q in combinations(sorted(mine), self.sim.qsize(m)):
            g = glb_all(mine[x] for x in q)
            new = lub(self.learned, g)  # @line L11
            if new is None:
                raise Inconsistent(f"learned {self.learned} and chosen {g} are not compatible")
            self.learned = new
        self.history.append(self.learned)


class GeneralizedPaxos:
    def __init__(self, n: int, seed: int, commands: list, qc: Optional[int] = None,
                 qf: Optional[int] = None, n_leaders: int = 2, n_learners: int = 2,
                 dup: float = 0.0, drop: float = 0.0, crashes: int = 0, crash_prob: float = 0.0,
                 duel_prob: float = 0.0, max_steps: int = 20000) -> None:
        self.n = n
        self.rng = random.Random(seed)
        self.commands = list(commands)
        self.qc = qc if qc is not None else n // 2 + 1
        self.qf = qf if qf is not None else -(-3 * n // 4)
        self.dup, self.drop = dup, drop
        self.crashes_left, self.crash_prob = crashes, crash_prob
        self.duel_prob = duel_prob
        self.max_steps = max_steps
        self.acceptors = [Acceptor(self, a) for a in range(n)]
        self.leaders = [Leader(self, i) for i in range(n_leaders)]
        self.learners = [Learner(self) for _ in range(n_learners)]
        self.learner_ids = [f"X{i}" for i in range(n_learners)]
        self.crashed: set = set()
        self.net: list = []
        self.ballots_started = 0
        self.twoa_sent = 0

    def qsize(self, m: tuple) -> int:
        return self.qf if is_fast(m) else self.qc

    def send(self, dst: object, msg: tuple) -> None:
        if self.rng.random() < self.drop:
            return
        self.net.append((dst, msg))
        if self.rng.random() < self.dup:
            self.net.append((dst, msg))

    def propose(self, c: Cmd) -> None:
        for a in range(self.n):
            self.send(a, ("propose", c))
        for ld in self.leaders:
            self.send(ld.name, ("propose", c))

    def deliver(self, dst: object, msg: tuple) -> None:
        if dst in self.crashed:
            return
        kind = msg[0]
        if isinstance(dst, int):
            acc = self.acceptors[dst]
            if kind == "1a":
                acc.on_1a(msg[1], msg[2])
            elif kind == "2a":
                acc.on_2a(msg[1], msg[2], msg[3])
            elif kind == "propose":
                acc.on_propose(msg[1])
        elif dst.startswith("L"):
            ld = self.leaders[int(dst[1:])]
            if kind == "1b":
                ld.on_1b(*msg[1:])
            elif kind == "propose":
                ld.on_propose(msg[1])
            elif kind == "nack":
                ld.on_nack(msg[1])
        else:
            self.learners[int(dst[1:])].on_2b(*msg[1:])

    def step(self) -> bool:
        if not self.net:
            return False
        i = self.rng.randrange(len(self.net))
        self.net[i], self.net[-1] = self.net[-1], self.net[i]
        dst, msg = self.net.pop()
        self.deliver(dst, msg)
        return True

    def live_leaders(self) -> list:
        return [ld for ld in self.leaders if ld.name not in self.crashed]

    def done(self) -> bool:
        want = set(self.commands)
        return all(want <= x.learned.cmds for x in self.learners)

    def run(self, start_fast: bool = True) -> "GeneralizedPaxos":
        self.leaders[0].start(start_fast)
        pending = list(self.commands)
        steps = 0
        while steps < self.max_steps:
            steps += 1
            if pending and self.rng.random() < 0.3:
                self.propose(pending.pop(0))
            if self.crashes_left and self.rng.random() < self.crash_prob:
                victim = self.rng.randrange(self.n)
                if victim not in self.crashed:
                    self.crashed.add(victim)
                    self.crashes_left -= 1
            if self.duel_prob and self.rng.random() < self.duel_prob:
                lds = self.live_leaders()
                self.rng.choice(lds).start(self.rng.random() < 0.5)
            if self.step():
                continue
            if pending:
                continue
            if self.done():
                break
            # @line L6 nothing is in flight and a command is not learned: a new
            # classic ballot, and clients send their commands again.
            lds = self.live_leaders()
            self.rng.choice(lds).start(False)
            for c in self.commands:
                if not all(c in x.learned.cmds for x in self.learners):
                    self.propose(c)
        return self

    def consistent(self) -> bool:
        """Each learner's value only grows, and all learned values are compatible."""
        for x in self.learners:
            for a, b in zip(x.history, x.history[1:]):
                if not prefix(a, b):
                    return False
        return lub_all(x.learned for x in self.learners) is not None

    def proposed_only(self) -> bool:
        return all(x.learned.cmds <= set(self.commands) for x in self.learners)
