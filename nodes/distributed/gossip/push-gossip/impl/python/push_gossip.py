# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-gossip/. The authors are listed in prov/7Q1FNH.jsonl.

"""Push gossip in the random phone call model.

A deterministic, seeded, lock-step simulator. In every round each process
picks a partner (uniform over all other processes, or uniform over its
neighbours in a given overlay graph), every process sends, then every process
receives, then every process updates its state. A rumor received in round t is
forwarded from round t + 1 on, as in Karp et al. (FOCS 2000).

infect_and_die is the fanout variant of Kermarrec, Massoulie and Ganesh
(IEEE TPDS 2003): a process forwards once, to k distinct random processes, at
the time it first hears the rumor.
"""

import random
from collections.abc import Callable, Sequence

Partner = Callable[[int, random.Random], int]


class PushProcess:
    """One process. Local state: informed or not. One message type: RUMOR."""

    def __init__(self, ident: int, informed: bool = False) -> None:
        self.id = ident
        self.informed = informed
        self.heard = False

    def on_round(self, partner: int) -> list[tuple[int, int, str]]:
        return [(self.id, partner, "RUMOR")] if self.informed else []  # @line L3

    def on_message(self, src: int, msg: str) -> None:
        if msg == "RUMOR":
            self.heard = True

    def end_round(self) -> bool:
        """Apply what arrived this round. Return True if newly informed."""
        new = self.heard and not self.informed  # @line L4
        self.informed = self.informed or self.heard
        self.heard = False
        return new


def complete_partner(n: int) -> Partner:
    """A uniform random process other than the caller."""

    def pick(v: int, rng: random.Random) -> int:
        u = rng.randrange(n - 1)
        return u + 1 if u >= v else u

    return pick


def overlay_partner(adj: Sequence[Sequence[int]]) -> Partner:
    """A uniform random neighbour of the caller in the graph adj."""

    def pick(v: int, rng: random.Random) -> int:
        return adj[v][rng.randrange(len(adj[v]))]

    return pick


def push_gossip(n: int, rng: random.Random, adj: Sequence[Sequence[int]] | None = None,
                source: int = 0, max_rounds: int = 10**6) -> tuple[int, int, list[int]]:
    """Run push until all n processes are informed.

    Return (rounds, messages, informed count after each round, starting with
    the count 1 before round 1). On a disconnected graph the run stops after
    max_rounds rounds.
    """
    pick = complete_partner(n) if adj is None else overlay_partner(adj)
    procs = [PushProcess(i, i == source) for i in range(n)]
    informed, messages, history = 1, 0, [1]
    rounds = 0
    while informed < n and rounds < max_rounds:
        rounds += 1
        out: list[tuple[int, int, str]] = []
        for p in procs:
            if p.informed:  # @line L1
                out.extend(p.on_round(pick(p.id, rng)))  # @line L2
        for src, dst, msg in out:
            procs[dst].on_message(src, msg)
        messages += len(out)
        for p in procs:
            if p.end_round():
                informed += 1
        history.append(informed)
    return rounds, messages, history


def infect_and_die(n: int, k: int, rng: random.Random, source: int = 0) -> int:
    """Fanout k, infect and die. Return the number of processes reached."""
    reached = [False] * n
    reached[source] = True
    count = 1
    frontier = [source]
    while frontier:
        nxt = []
        for v in frontier:
            targets: set[int] = set()
            while len(targets) < k:
                u = rng.randrange(n - 1)
                targets.add(u + 1 if u >= v else u)
            for u in targets:
                if not reached[u]:
                    reached[u] = True
                    count += 1
                    nxt.append(u)
        frontier = nxt
    return count
