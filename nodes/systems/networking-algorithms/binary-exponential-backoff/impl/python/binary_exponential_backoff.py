# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-exponential-backoff/. The authors are listed in prov/R0C39B.jsonl.

"""Truncated binary exponential backoff, as in IEEE 802.3 (classic Ethernet).

After the n-th collision of a frame, the station waits k slot times, with k
drawn uniformly from 0 .. 2**min(n, 10) - 1. After 16 attempts that all
collide, it drops the frame. The channel here is slotted: a transmission
takes one slot, and two or more transmissions in the same slot collide.
"""

import random
from typing import NamedTuple, Protocol

ATTEMPT_LIMIT = 16
BACKOFF_LIMIT = 10


class Rng(Protocol):
    def randrange(self, stop: int) -> int: ...


def backoff_slots(n: int, rng: Rng) -> int:
    """The number of slots to wait after the n-th collision (n >= 1)."""
    if n < 1:
        raise ValueError("n counts collisions and starts at 1")
    return rng.randrange(2 ** min(n, BACKOFF_LIMIT))  # @line L6


class Station(NamedTuple):
    sent: list[int]  # slot of each successful frame
    dropped: int  # frames dropped after ATTEMPT_LIMIT collisions
    collisions: int  # collisions in total


def simulate(frames: list[int], rng: Rng, max_slots: int = 10**6) -> list[Station]:
    """Station i has frames[i] frames ready at slot 0. Return what happened.

    A station sends its frames one after the other. A new frame starts with
    n = 0 and is tried in the next slot.
    """
    left = list(frames)
    nxt = [0 if f > 0 else -1 for f in frames]  # slot of the next attempt
    n = [0] * len(frames)  # collisions of the current frame  # @line L1
    sent: list[list[int]] = [[] for _ in frames]
    dropped, coll = [0] * len(frames), [0] * len(frames)
    slot = 0
    while any(f > 0 for f in left):
        if slot >= max_slots:
            raise RuntimeError("slot limit reached")
        here = [i for i in range(len(frames)) if left[i] > 0 and nxt[i] == slot]  # @line L2
        if len(here) == 1:  # @line L3
            i = here[0]
            sent[i].append(slot)
            left[i] -= 1
            n[i], nxt[i] = 0, slot + 1
        elif len(here) > 1:
            for i in here:
                n[i] += 1  # @line L4
                coll[i] += 1
                if n[i] == ATTEMPT_LIMIT:  # @line L5
                    dropped[i] += 1
                    left[i] -= 1
                    n[i], nxt[i] = 0, slot + 1
                else:
                    nxt[i] = slot + 1 + backoff_slots(n[i], rng)  # @line L7
        slot += 1
    return [Station(sent[i], dropped[i], coll[i]) for i in range(len(frames))]


def expected_collisions_two_stations() -> float:
    """Exact mean number of collisions when two stations start together.

    After collision c, the two draws are equal (and collide again) with
    probability 2**-min(c, 10). The frame is dropped at collision 16.
    """
    total, p = 0.0, 1.0
    for c in range(1, ATTEMPT_LIMIT + 1):
        total += p  # p = P(at least c collisions)
        p *= 2.0 ** -min(c, BACKOFF_LIMIT)
    return total
