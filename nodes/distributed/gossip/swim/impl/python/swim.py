# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swim/. The authors are listed in prov/7NBZ21.jsonl.

"""SWIM (Das, Gupta and Motivala 2002) in a seeded period-based simulator.

Every protocol period each live member probes one target: a direct ping,
and if no ack comes back, a ping-req to k other members, which ping the
target and relay the ack. Targets come from a round-robin pass over a
random permutation of the member list, or uniformly at random.

A failed probe either marks the target faulty at once (basic SWIM) or
marks it suspected (the suspicion mechanism). Membership updates (Alive,
Suspect, Confirm, with incarnation numbers) ride on pings, ping-reqs and
acks: each message carries a few updates, those sent the fewest times
first, and an update is sent at most lam * ceil(log10(n + 1)) times. A
member that hears it is suspected raises its incarnation number and spreads
Alive. A suspicion not refuted within the timeout becomes Confirm.

Messages are lost independently with probability loss. Inside a period the
members probe one after the other, and every message arrives at once or
not at all, so time is counted in whole periods.
"""

import math
import random

ALIVE, SUSPECT, FAULTY = 0, 1, 2


class Swim:
    def __init__(self, n: int, seed: int, k: int = 3, loss: float = 0.0,
                 suspicion: bool = True, order: str = "round-robin",
                 lam: int = 4, susp_mult: int = 4, max_piggyback: int = 8):
        self.rng = random.Random(seed)
        self.n = n
        self.k = k
        self.loss = loss
        self.suspicion = suspicion
        self.order = order
        self.max_piggyback = max_piggyback
        log = max(1.0, math.log10(n))
        self.send_limit = lam * math.ceil(math.log10(n + 1))
        self.timeout = math.ceil(susp_mult * log)
        self.alive = set(range(n))
        self.t = 0
        # view[i][j] = [status, incarnation] as member i sees member j
        self.view = {i: {j: [ALIVE, 0] for j in range(n) if j != i} for i in range(n)}
        self.inc = [0] * n
        self.buffer: dict[int, dict[int, list]] = {i: {} for i in range(n)}
        self.suspect_since: dict[int, dict[int, int]] = {i: {} for i in range(n)}
        self.plist = {i: [] for i in range(n)}
        self.pos = {i: 0 for i in range(n)}
        self.messages = 0
        self.first_failed_probe: dict[int, int] = {}
        self.first_confirm: dict[int, int] = {}
        self.false_suspicions = 0
        self.false_confirms = 0
        self.crash_time: dict[int, int] = {}
        self.last_target: dict[int, int] = {}

    # ------------------------------------------------------------ messages

    def _send(self, src: int, dst: int) -> bool:
        """One message from src to dst with piggybacked updates."""
        self.messages += 1
        if dst not in self.alive or self.rng.random() < self.loss:
            return False
        buf = self.buffer[src]
        ups = sorted(buf.items(), key=lambda kv: kv[1][2])[: self.max_piggyback]   # @line L8
        for key, u in ups:
            u[2] += 1
            if u[2] >= self.send_limit:
                del buf[key]
        for _, u in ups:
            self._apply(dst, u[0], u[1], u[3])
        return True

    def _spread(self, i: int, kind: int, j: int, inc: int) -> None:
        self.buffer[i][j] = [kind, j, 0, inc]

    def _apply(self, i: int, kind: int, j: int, inc: int) -> None:
        """Member i receives the update (kind, j, inc)."""
        if j == i:
            if kind == SUSPECT and inc >= self.inc[i]:                    # @line L5
                self.inc[i] = inc + 1
                self._spread(i, ALIVE, i, self.inc[i])
            return
        cur = self.view[i].get(j)
        if cur is None or cur[0] == FAULTY:
            return
        st, ci = cur
        if kind == FAULTY:                                               # @line L6
            self._confirm(i, j)
            return
        if kind == ALIVE and inc > ci:
            cur[0], cur[1] = ALIVE, inc
            self.suspect_since[i].pop(j, None)
            self._spread(i, ALIVE, j, inc)
        elif kind == SUSPECT and (inc > ci or (inc == ci and st == ALIVE)):
            cur[0], cur[1] = SUSPECT, inc
            self.suspect_since[i][j] = self.t
            self._spread(i, SUSPECT, j, inc)

    def _confirm(self, i: int, j: int) -> None:
        if self.view[i][j][0] == FAULTY:
            return
        self.view[i][j][0] = FAULTY
        self.suspect_since[i].pop(j, None)
        self._spread(i, FAULTY, j, self.view[i][j][1])
        if j in self.alive:
            self.false_confirms += 1
        else:
            self.first_confirm.setdefault(j, self.t)

    # ------------------------------------------------------------ probing

    def _members(self, i: int) -> list[int]:
        return [j for j, v in self.view[i].items() if v[0] != FAULTY]

    def _next_target(self, i: int):
        if self.order == "random":
            m = self._members(i)
            return self.rng.choice(m) if m else None
        for _ in range(2):
            lst = self.plist[i]
            while self.pos[i] < len(lst):
                j = lst[self.pos[i]]
                self.pos[i] += 1
                if self.view[i][j][0] != FAULTY:
                    return j
            lst = sorted(self._members(i))                               # @line L9
            self.rng.shuffle(lst)
            self.plist[i] = lst
            self.pos[i] = 0
        return None

    def probe(self, i: int) -> None:
        j = self._next_target(i)                                         # @line L1
        if j is None:
            return
        self.last_target[i] = j
        if self._send(i, j) and self._send(j, i):                        # @line L2
            return
        others = [m for m in self._members(i) if m != j]
        helpers = self.rng.sample(others, min(self.k, len(others)))
        ok = False
        for m in helpers:                                                # @line L3
            if self._send(i, m) and self._send(m, j) and self._send(j, m) and self._send(m, i):
                ok = True
        if ok:
            return
        if j not in self.alive:
            self.first_failed_probe.setdefault(j, self.t)
        if self.suspicion:                                               # @line L4
            if self.view[i][j][0] == ALIVE:
                if j in self.alive:
                    self.false_suspicions += 1
                self._apply(i, SUSPECT, j, self.view[i][j][1])
        else:
            self._confirm(i, j)

    def period(self) -> None:
        self.t += 1
        order = sorted(self.alive)
        self.rng.shuffle(order)
        for i in order:
            if i in self.alive:
                self.probe(i)
        for i in sorted(self.alive):                                     # @line L7
            for j, since in list(self.suspect_since[i].items()):
                if self.t - since >= self.timeout:
                    self._confirm(i, j)

    def run(self, periods: int) -> None:
        for _ in range(periods):
            self.period()

    def crash(self, j: int) -> None:
        self.alive.discard(j)
        self.crash_time[j] = self.t

    def everyone_knows(self, j: int) -> bool:
        return all(self.view[i][j][0] == FAULTY for i in self.alive if i != j)


def expected_first_detection(n: int, q: float = 1.0) -> float:
    """Expected number of periods until some member probes a crashed member,
    when each of the q (n - 1) live members picks a uniform target among its
    n - 1 others each period: 1 / (1 - (1 - 1/(n - 1))^(q (n - 1))). As n
    grows with q = 1 this tends to e / (e - 1)."""
    miss = (1 - 1 / (n - 1)) ** (q * (n - 1))
    return 1 / (1 - miss)
