# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rumor-mongering/. The authors are listed in prov/97KQKR.jsonl.

"""Rumor mongering (Demers et al., PODC 1987), with the SIR final size and
death certificates for deletions.

The simulator is deterministic, seeded and runs in lock-step cycles. Each
site is susceptible (does not know the update), infective (knows it and
spreads it) or removed (knows it and has stopped). A sender learns at once
whether a contact was unnecessary, that is, whether the partner knew the
update at the start of the cycle.

Variants, as in Section 1.4 of Demers et al.:
  feedback: lose interest only after an unnecessary contact.
  blind:    lose interest after any contact.
  coin:     lose interest with probability 1/k at each such event.
  counter:  lose interest after k such events.

Section 1.4 says only that a counter site loses interest "after k unnecessary
contacts". The footnote of Table 3 (pull) resets the counter when a contact
was needed. reset=True (the default) counts unnecessary contacts since the
last necessary one; with it, feedback and counter on 1000 sites give the
residue and traffic of Table 1. reset=False counts all unnecessary contacts
and gives a larger residue for k >= 2 (0.048 against 0.037 at k = 2).
"""

import math
import random
from dataclasses import dataclass

S, I, R = 0, 1, 2


@dataclass
class Outcome:
    residue: float  # fraction of sites that never received the update
    traffic: float  # update messages sent, divided by the number of sites
    t_ave: float    # mean cycle of arrival over the sites that received it
    t_last: int     # cycle of arrival at the last site that received it
    cycles: int     # cycles until no site was infective


class Site:
    """One site. Message type: UPDATE. The reply bit says if it was needed."""

    def __init__(self, ident: int, k: int, feedback: bool, counter: bool, reset: bool = False) -> None:
        self.id = ident
        self.state = S
        self.k = k
        self.feedback = feedback
        self.counter = counter
        self.reset = reset
        self.count = 0
        self.arrival = -1
        self.got = False

    def on_message(self, src: int, msg: str, was_state: int) -> bool:
        """Receive UPDATE. Return True if the contact was necessary."""
        if msg == "UPDATE":
            if was_state == S:
                self.got = True
                return True
        return False

    def after_contact(self, necessary: bool, rng: random.Random) -> None:
        """The sender side of one contact."""
        if self.state != I:
            return
        if self.feedback and necessary:  # @line L5
            if self.reset:
                self.count = 0  # @line L6
            return
        if self.counter:
            self.count += 1  # @line L7
            if self.count >= self.k:
                self.state = R
        elif rng.random() < 1.0 / self.k:  # @line L8
            self.state = R

    def end_cycle(self, cycle: int) -> bool:
        new = self.got and self.state == S  # @line L4
        if new:
            self.state, self.arrival = I, cycle
        self.got = False
        return new


def rumor_mongering(n: int, k: int, rng: random.Random, feedback: bool = True, counter: bool = True,
                    source: int = 0, max_cycles: int = 10**5, reset: bool = True) -> Outcome:
    """Push rumor mongering of one update from source until no site is infective."""
    sites = [Site(i, k, feedback, counter, reset) for i in range(n)]
    sites[source].state, sites[source].arrival = I, 0
    sent, cycle = 0, 0
    while cycle < max_cycles and any(s.state == I for s in sites):
        cycle += 1
        start = [s.state for s in sites]
        for s in sites:
            if start[s.id] != I:  # @line L1
                continue
            u = rng.randrange(n - 1)  # @line L2
            u = u + 1 if u >= s.id else u
            sent += 1
            necessary = sites[u].on_message(s.id, "UPDATE", start[u])  # @line L3
            s.after_contact(necessary, rng)
        for s in sites:
            s.end_cycle(cycle)
    got = [s.arrival for s in sites if s.arrival >= 0]
    return Outcome(1 - len(got) / n, sent / n, sum(got) / len(got), max(got), cycle)


def rumor_jump_chain(n: int, k: int, rng: random.Random) -> int:
    """Feedback and coin, one contact at a time: the chain whose fluid limit is
    ds/dt = -s i, di/dt = s i - (1/k)(1 - s) i. Return the number of sites
    that never heard the rumor."""
    s, i = n - 1, 1
    while i > 0:
        u = rng.randrange(n - 1)  # the partner of a random infective site
        if u < s:
            s, i = s - 1, i + 1
        elif rng.random() < 1.0 / k:
            i -= 1
    return s


def residue_equation(k: float) -> float:
    """The root in (0, 1) of s = exp(-(k + 1)(1 - s)), by bisection."""
    lo, hi = 1e-300, 1.0 - 1e-12
    f = lambda s: s - math.exp(-(k + 1) * (1 - s))
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# The SIR model of Kermack and McKendrick, for comparison.

def sir_final_size(r0: float) -> float:
    """The fraction never infected: the root in (0, 1) of s = exp(-r0 (1 - s)), for r0 > 1."""
    return residue_equation(r0 - 1)


def sir_jump_chain(n: int, r0: float, rng: random.Random, initial: int = 1) -> int:
    """Stochastic SIR with infection rate r0 s i / n and recovery rate i.

    Only the order of events matters for the final size, so the chain runs on
    the embedded jump process. Return the number of sites never infected.
    """
    s, i = n - initial, initial
    while i > 0:
        infect = r0 * s * i / n
        if rng.random() * (infect + i) < infect:
            s, i = s - 1, i + 1
        else:
            i -= 1
    return s


# Deletion: plain removal, certificates with a fixed lifetime, and dormant
# death certificates with an activation timestamp (Demers et al., Section 2).

ITEM, CERT = "item", "cert"


class Replica:
    """One replica of a key-value store, reconciled by push-pull anti-entropy.

    entries maps key -> (ITEM, value, ts) or (CERT, ts, activated).
    dormant maps key -> (ts, activated); dormant certificates are not sent.
    """

    def __init__(self, ident: int, mode: str, tau1: int, tau2: int) -> None:
        self.id = ident
        self.mode = mode  # "plain", "timeout" or "dormant"
        self.tau1 = tau1
        self.tau2 = tau2
        self.entries: dict[str, tuple] = {}
        self.dormant: dict[str, tuple[int, int]] = {}
        self.retention: dict[str, frozenset[int]] = {}
        self.online = True

    def write(self, key: str, value: str, ts: int) -> None:
        self.receive({key: (ITEM, value, ts)}, ts, {})

    def delete(self, key: str, ts: int, retention: frozenset[int]) -> None:
        if self.mode == "plain":
            self.entries.pop(key, None)
        else:
            self.entries[key] = (CERT, ts, ts)
            self.retention[key] = retention

    def value(self, key: str) -> str | None:
        e = self.entries.get(key)
        return e[1] if e is not None and e[0] == ITEM else None

    def receive(self, entries: dict[str, tuple], now: int, retention: dict[str, frozenset[int]]) -> None:
        """Merge entries sent by a partner. The larger timestamp wins."""
        for key, e in entries.items():
            ts = e[2] if e[0] == ITEM else e[1]
            if e[0] == ITEM and key in self.dormant:
                cts, _ = self.dormant[key]
                if ts < cts:
                    # An obsolete item met a dormant certificate: reactivate it.
                    del self.dormant[key]
                    self.entries[key] = (CERT, cts, now)
                    continue
            mine = self.entries.get(key)
            if mine is None:
                self.entries[key] = e
            else:
                mts = mine[2] if mine[0] == ITEM else mine[1]
                if ts > mts or (ts == mts and e[0] == CERT and mine[0] == ITEM):
                    self.entries[key] = e
                elif ts == mts and e[0] == CERT and mine[0] == CERT and e[2] > mine[2]:
                    self.entries[key] = e  # keep the later activation time
            if e[0] == CERT and key in retention:
                self.retention[key] = retention[key]

    def expire(self, now: int) -> None:
        for key in [k for k, e in self.entries.items() if e[0] == CERT]:
            _, ts, activated = self.entries[key]
            if now - activated <= self.tau1:
                continue
            del self.entries[key]
            if self.mode == "dormant" and self.id in self.retention.get(key, ()):
                self.dormant[key] = (ts, activated)
        for key in [k for k, (_, a) in self.dormant.items() if now - a > self.tau1 + self.tau2]:
            del self.dormant[key]


def anti_entropy_cycle(replicas: list[Replica], now: int, rng: random.Random) -> None:
    """Each online replica runs push-pull anti-entropy with one random online replica."""
    up = [r for r in replicas if r.online]
    for r in up:
        if len(up) < 2:
            return
        q = up[rng.randrange(len(up) - 1)]
        if q is r:
            q = up[-1]
        mine, theirs = dict(r.entries), dict(q.entries)
        q.receive(mine, now, r.retention)
        r.receive(theirs, now, q.retention)
    for r in replicas:
        r.expire(now)


def deletion_scenario(mode: str, rng: random.Random, n: int = 20, tau1: int = 30, tau2: int = 400,
                      retention_size: int = 3, offline_until: int = 80, end: int = 200) -> int:
    """Write x everywhere, take replica n-1 offline, delete x at replica 0,
    bring replica n-1 back at offline_until with its old copy, and run to end.
    Return the number of replicas that hold x at the end.
    """
    replicas = [Replica(i, mode, tau1, tau2) for i in range(n)]
    for r in replicas:
        r.write("x", "v1", 1)
    replicas[n - 1].online = False
    retention = frozenset(rng.sample(range(n - 1), retention_size))
    replicas[0].delete("x", 2, retention)
    for now in range(3, end + 1):
        if now == offline_until:
            replicas[n - 1].online = True
        anti_entropy_cycle(replicas, now, rng)
    return sum(r.value("x") is not None for r in replicas)
