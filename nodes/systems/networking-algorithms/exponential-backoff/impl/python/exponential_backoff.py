# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-backoff/. The authors are listed in prov/SRY509.jsonl.

"""Capped exponential backoff with jitter, as a retry policy.

After failure n (n = 0, 1, 2, ...), the client waits a delay derived from
v = min(cap, base * factor**n). The jitter modes are:
  none          wait v
  full          wait uniform(0, v)
  equal         wait v/2 + uniform(0, v/2)
  decorrelated  wait min(cap, uniform(base, 3 * previous wait))
The time is simulated: no function here really sleeps.
"""

import random
from collections.abc import Callable, Iterator
from typing import NamedTuple

JITTERS = ("none", "full", "equal", "decorrelated")


def backoff_delays(
    base: float,
    cap: float,
    jitter: str = "full",
    rng: random.Random | None = None,
    factor: float = 2,
) -> Iterator[float]:
    """Yield the wait after failure 0, 1, 2, ... (an endless stream)."""
    if jitter not in JITTERS:
        raise ValueError(f"jitter is one of {JITTERS}")
    if base <= 0 or cap < base:
        raise ValueError("need 0 < base <= cap")
    rng = rng or random.Random()
    n, prev = 0, base
    while True:
        v = min(cap, base * factor**n)  # @line L4
        if jitter == "none":
            d = v  # @line L5
        elif jitter == "full":
            d = rng.uniform(0, v)  # @line L6
        elif jitter == "equal":
            d = v / 2 + rng.uniform(0, v / 2)  # @line L7
        else:
            d = min(cap, rng.uniform(base, 3 * prev))  # @line L8
        prev = d
        yield d
        n += 1


class Outcome(NamedTuple):
    ok: bool
    attempts: int
    waited: float


def retry(
    operation: Callable[[int], bool],
    base: float,
    cap: float,
    max_attempts: int,
    jitter: str = "full",
    rng: random.Random | None = None,
) -> Outcome:
    """Call operation(attempt) until it returns True or the budget is spent."""
    delays = backoff_delays(base, cap, jitter, rng)
    waited = 0.0
    for n in range(max_attempts):  # @line L1
        if operation(n):  # @line L2
            return Outcome(True, n + 1, waited)
        if n + 1 == max_attempts:  # @line L3
            break
        waited += next(delays)  # @line L9
    return Outcome(False, max_attempts, waited)


class Contention(NamedTuple):
    finished: int  # clients that succeeded
    calls: int  # attempts made in total
    makespan: int  # slot of the last success, or -1


def contention(
    clients: int,
    jitter: str,
    rng: random.Random,
    base: float = 1,
    cap: float = 1000,
    max_attempts: int = 30,
) -> Contention:
    """All clients try at slot 0. An attempt succeeds only if it is alone in its slot.

    A client whose attempt collides waits its next backoff delay and tries
    again at slot floor(now + delay) + 1.
    """
    streams = [backoff_delays(base, cap, jitter, rng) for _ in range(clients)]
    nxt = {c: 0 for c in range(clients)}
    tries = dict.fromkeys(range(clients), 0)
    calls, done, last = 0, 0, -1
    while nxt:
        slot = min(nxt.values())
        here = [c for c, s in nxt.items() if s == slot]
        calls += len(here)
        for c in here:
            tries[c] += 1
        if len(here) == 1:
            del nxt[here[0]]
            done, last = done + 1, slot
            continue
        for c in here:
            if tries[c] == max_attempts:
                del nxt[c]
            else:
                nxt[c] = int(slot + next(streams[c])) + 1
    return Contention(done, calls, last)
