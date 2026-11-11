# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lpbcast/. The authors are listed in prov/DD2C6C.jsonl.

"""lpbcast (Eugster, Guerraoui, Handurukande, Kouznetsov and Kermarrec 2003)
in a seeded round-based simulator.

Every process p keeps a view of at most l processes, a buffer subs of
recent subscriptions, a buffer unsubs of recent unsubscriptions, a buffer
events of notifications received since its last gossip, and eventIds, the
ids of delivered notifications. Once per round each process sends one gossip
message (events, subs plus itself, unsubs, eventIds) to F random members of
its view and empties events. A receiver updates its view from the unsubs and
subs, delivers new events, and notes ids it has not delivered; with
retrieval on, it fetches those events from the sender at the end of the
round.

Rounds are synchronous: all messages of a round are built from the state at
the start of the round and handled after all of them are sent, in random
order. Messages are lost with probability loss.
"""

import math
import random


class Lpbcast:
    def __init__(self, n: int, l: int, fanout: int, seed: int,
                 subs_max: int | None = None, unsubs_max: int | None = None,
                 ids_max: int = 10 ** 6, retrieve: bool = False, loss: float = 0.0):
        self.rng = random.Random(seed)
        self.l = l
        self.fanout = fanout
        self.subs_max = l if subs_max is None else subs_max
        self.unsubs_max = l if unsubs_max is None else unsubs_max
        self.ids_max = ids_max
        self.retrieve = retrieve
        self.loss = loss
        self.alive = set(range(n))
        self.view: dict[int, set[int]] = {}
        for p in range(n):
            others = self.rng.sample(range(n - 1), l)
            self.view[p] = {x if x < p else x + 1 for x in others}
        self.subs: dict[int, set[int]] = {p: set() for p in range(n)}
        self.unsubs: dict[int, set[int]] = {p: set() for p in range(n)}
        self.events: dict[int, set[int]] = {p: set() for p in range(n)}
        self.ids: dict[int, list[int]] = {p: [] for p in range(n)}
        self.idset: dict[int, set[int]] = {p: set() for p in range(n)}
        self.retrieve_buf: dict[int, dict[int, int]] = {p: {} for p in range(n)}
        self.delivered: dict[int, set[int]] = {}
        self.messages = 0
        self.retrievals = 0
        self.next_id = n

    # ------------------------------------------------------------ helpers

    def _trim(self, s: set, m: int) -> None:
        if len(s) > m:
            s.difference_update(self.rng.sample(sorted(s), len(s) - m))

    def _deliver(self, p: int, e: int) -> None:
        self.idset[p].add(e)
        self.ids[p].append(e)
        self.delivered.setdefault(e, set()).add(p)
        while len(self.ids[p]) > self.ids_max:
            self.idset[p].discard(self.ids[p].pop(0))

    # ------------------------------------------------------------ API

    def broadcast(self, p: int, e: int) -> None:
        """Process p lpbcasts notification e."""
        self._deliver(p, e)
        self.events[p].add(e)

    def join(self, contact: int) -> int:
        """A new process that knows one member subscribes through it."""
        p = self.next_id
        self.next_id += 1
        self.alive.add(p)
        self.view[p] = {contact}
        for d in (self.subs, self.unsubs, self.events, self.idset, self.retrieve_buf):
            d[p] = type(d[contact])()
        self.ids[p] = []
        self.subs[contact].add(p)
        return p

    def unsubscribe(self, p: int) -> None:
        """p leaves; it gossips its unsubscription once to F view members."""
        msg = (set(), set(), {p}, [])
        targets = self.rng.sample(sorted(self.view[p]), min(self.fanout, len(self.view[p])))
        self.alive.discard(p)
        for q in targets:
            if q in self.alive:
                self._receive(q, p, msg)

    # ------------------------------------------------------------ protocol

    def _receive(self, p: int, sender: int, msg) -> None:
        events, subs, unsubs, ids = msg
        v = self.view[p]
        for u in unsubs:                                                 # @line L3
            v.discard(u)
            self.subs[p].discard(u)
            if u != p:
                self.unsubs[p].add(u)
        for s in subs:                                                   # @line L4
            if s != p and s not in v and s not in self.unsubs[p]:
                v.add(s)
                self.subs[p].add(s)
        if len(v) > self.l:                                              # @line L5
            out = self.rng.sample(sorted(v), len(v) - self.l)
            v.difference_update(out)
            self.subs[p].update(out)
        self._trim(self.subs[p], self.subs_max)                          # @line L6
        self._trim(self.unsubs[p], self.unsubs_max)
        for e in events:                                                 # @line L7
            if e not in self.idset[p]:
                self._deliver(p, e)
                self.events[p].add(e)
        for e in ids:                                                    # @line L8
            if e not in self.idset[p]:
                self.retrieve_buf[p].setdefault(e, sender)

    def round(self) -> None:
        outbox = []
        for p in sorted(self.alive):
            msg = (set(self.events[p]), self.subs[p] | {p},              # @line L1
                   set(self.unsubs[p]), list(self.ids[p]))
            v = sorted(self.view[p])
            for q in self.rng.sample(v, min(self.fanout, len(v))):        # @line L2
                outbox.append((q, p, msg))
            self.events[p] = set()
        self.rng.shuffle(outbox)
        for q, p, msg in outbox:
            self.messages += 1
            if q in self.alive and self.rng.random() >= self.loss:
                self._receive(q, p, msg)
        if self.retrieve:                                                # @line L9
            for p in sorted(self.alive):
                for e, frm in sorted(self.retrieve_buf[p].items()):
                    if e not in self.idset[p] and frm in self.alive:
                        self.retrievals += 1
                        self._deliver(p, e)
                self.retrieve_buf[p] = {}
        else:
            for p in self.alive:
                self.retrieve_buf[p] = {}

    def run(self, rounds: int) -> None:
        for _ in range(rounds):
            self.round()

    # ------------------------------------------------------------ measures

    def delivery_ratio(self, e: int) -> float:
        return len(self.delivered.get(e, set()) & self.alive) / len(self.alive)

    def in_degrees(self) -> dict[int, int]:
        d = {p: 0 for p in self.alive}
        for p in self.alive:
            for q in self.view[p]:
                if q in d:
                    d[q] += 1
        return d


def infect_and_die_reach(f: float) -> float:
    """The root x of x = 1 - exp(-f x): the fraction of a large group that a
    rumour reaches when every node forwards it once to f random nodes."""
    x = 1.0
    for _ in range(200):
        x = 1 - math.exp(-f * x)
    return x
