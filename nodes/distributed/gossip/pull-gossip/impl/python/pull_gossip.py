# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pull-gossip/. The authors are listed in prov/1XHB8V.jsonl.

"""Pull gossip in the random phone call model.

A deterministic, seeded, lock-step simulator. In every round each process calls
a partner (uniform over all other processes, or uniform over its neighbours in
an overlay graph). The call itself carries no rumor; as in Karp et al. (FOCS
2000), calls are placed in every round anyway. A called process that knew the
rumor at the start of the round sends it back to the caller in the same round
(a pull transmission), without knowing whether the caller has it already.
State changes take effect at the end of the round, so a rumor learned in round
t is passed on from round t + 1 on.
"""

import random
from collections.abc import Callable, Sequence

Partner = Callable[[int, random.Random], int]


class PullProcess:
    """One process. Message types: CALL (free) and RUMOR (a transmission)."""

    def __init__(self, ident: int, informed: bool = False) -> None:
        self.id = ident
        self.informed = informed
        self.heard = False

    def on_round(self, partner: int) -> list[tuple[int, int, str]]:
        return [(self.id, partner, "CALL")]  # @line L2

    def on_message(self, src: int, msg: str) -> list[tuple[int, int, str]]:
        if msg == "CALL":
            return [(self.id, src, "RUMOR")] if self.informed else []  # @line L3
        if msg == "RUMOR":
            self.heard = True
        return []

    def end_round(self) -> bool:
        new = self.heard and not self.informed  # @line L4
        self.informed = self.informed or self.heard
        self.heard = False
        return new


def complete_partner(n: int) -> Partner:
    def pick(v: int, rng: random.Random) -> int:
        u = rng.randrange(n - 1)
        return u + 1 if u >= v else u

    return pick


def overlay_partner(adj: Sequence[Sequence[int]]) -> Partner:
    def pick(v: int, rng: random.Random) -> int:
        return adj[v][rng.randrange(len(adj[v]))]

    return pick


def one_round(procs: list[PullProcess], pick: Partner, rng: random.Random) -> tuple[int, int]:
    """Run one round. Return (newly informed, rumor transmissions)."""
    calls: list[tuple[int, int, str]] = []
    for p in procs:
        calls.extend(p.on_round(pick(p.id, rng)))  # @line L1
    replies: list[tuple[int, int, str]] = []
    for src, dst, msg in calls:
        replies.extend(procs[dst].on_message(src, msg))
    for src, dst, msg in replies:
        procs[dst].on_message(src, msg)
    new = sum(p.end_round() for p in procs)
    return new, len(replies)


def pull_gossip(n: int, rng: random.Random, adj: Sequence[Sequence[int]] | None = None,
                source: int = 0, max_rounds: int = 10**6) -> tuple[int, int, list[int]]:
    """Run pull until all n processes are informed.

    Return (rounds, rumor transmissions, informed count after each round,
    starting with 1 before round 1).
    """
    pick = complete_partner(n) if adj is None else overlay_partner(adj)
    procs = [PullProcess(i, i == source) for i in range(n)]
    informed, transmissions, history, rounds = 1, 0, [1], 0
    while informed < n and rounds < max_rounds:
        rounds += 1
        new, tx = one_round(procs, pick, rng)
        informed += new
        transmissions += tx
        history.append(informed)
    return rounds, transmissions, history


def uninformed_after_one_round(n: int, uninformed: int, rng: random.Random) -> int:
    """Start with the given number of uninformed processes and run one round."""
    procs = [PullProcess(i, i >= uninformed) for i in range(n)]
    one_round(procs, complete_partner(n), rng)
    return sum(not p.informed for p in procs)
