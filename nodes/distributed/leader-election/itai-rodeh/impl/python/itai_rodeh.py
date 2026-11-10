# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/itai-rodeh/. The authors are listed in prov/Y6D4ZP.jsonl.

"""Itai-Rodeh election on an anonymous unidirectional ring of known size n.

This is the form presented by Fokkink: Chang-Roberts with random identifiers
from {1..n}, round numbers, a hop counter and a bit that marks a message
dirty when it meets another active process with the same round and value.
Channels are FIFO. Process p_i sends to p_{i+1}.

A schedule picks the next channel to deliver from:
  "random": a seeded random non-empty channel,
  "first":  the non-empty channel with the smallest index,
  "last":   the non-empty channel with the largest index.
The coin flips use their own seeded generator.
"""

import random
from collections import deque


class Process:
    def __init__(self, n: int, coins: random.Random) -> None:
        self.n = n
        self.coins = coins
        self.active = True
        self.leader = False
        self.round = 0
        self.id = 0

    def new_round(self) -> tuple:  # @line L2
        self.round += 1
        self.id = self.coins.randint(1, self.n)
        return (self.id, self.round, 1, False)

    def start(self) -> list[tuple]:  # @line L1
        return [self.new_round()]

    def receive(self, msg: tuple) -> list[tuple]:
        i, r, h, dirty = msg
        if not self.active:  # @line L3
            return [(i, r, h + 1, dirty)]
        if (r, i) > (self.round, self.id):  # @line L4
            self.active = False
            return [(i, r, h + 1, dirty)]
        if (r, i) < (self.round, self.id):  # @line L5
            return []
        if h < self.n:  # @line L6
            return [(i, r, h + 1, True)]
        if not dirty:  # @line L7
            self.leader = True
            return []
        return [self.new_round()]  # @line L8


class Fixed:
    """Coins that return given values, for worked examples."""

    def __init__(self, values: list[int]) -> None:
        self.values = list(values)

    def randint(self, a: int, b: int) -> int:
        return self.values.pop(0)


def itai_rodeh(n: int, seed: int, schedule: str = "random", draws: list[list[int]] | None = None) -> dict:
    """Run one election on a ring of n anonymous processes; return the result.

    schedule "sync" delivers all messages in transit in lock-step steps, which
    is the run in which every message takes one time unit. draws[i], if
    given, is the list of values that p_i draws, one per round.
    """
    coins = random.Random(seed)
    sched = random.Random(seed + 1_000_003)
    procs = [Process(n, Fixed(draws[i]) if draws else coins) for i in range(n)]
    chans = [deque() for _ in range(n)]  # chans[i] carries p_i -> p_{i+1}
    messages = 0
    time = 0
    elected_at = None
    for i, p in enumerate(procs):
        for m in p.start():
            chans[i].append(m)
            messages += 1
    while schedule == "sync" and any(chans):
        time += 1
        batch = [(c, chans[c].popleft()) for c in range(n) if chans[c]]
        for c, msg in batch:
            j = (c + 1) % n
            for m in procs[j].receive(msg):
                chans[j].append(m)
                messages += 1
            if procs[j].leader and elected_at is None:
                elected_at = time
    while True:
        busy = [i for i in range(n) if chans[i]]
        if not busy:
            break
        if schedule == "first":
            c = busy[0]
        elif schedule == "last":
            c = busy[-1]
        else:
            c = sched.choice(busy)
        msg = chans[c].popleft()
        j = (c + 1) % n
        for m in procs[j].receive(msg):
            chans[j].append(m)
            messages += 1
    return {
        "leaders": [i for i in range(n) if procs[i].leader],
        "active": [i for i in range(n) if procs[i].active],
        "rounds": max(p.round for p in procs),
        "messages": messages,
        "elected_at": elected_at,
    }


def unique_max_probability(k: int, n: int) -> float:
    """The chance that k values drawn from {1..n} have a unique maximum."""
    total = 0.0
    for m in range(1, n + 1):
        total += k * (1 / n) * ((m - 1) / n) ** (k - 1)
    return total
