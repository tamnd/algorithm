# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eventually-perfect-failure-detector/. The authors are listed in prov/S0DYB3.jsonl.

"""An eventually perfect failure detector (diamond-P) built from heartbeats
and growing timeouts, in a simulated partially synchronous system.

Time is an integer tick. Every process p sends a heartbeat to every other
process at each multiple of eta. Before the global stabilization time GST a
process may skip a heartbeat (it is slow), and a message may take any time,
but a message sent at time s always arrives by max(s, GST) + delta. From GST
on, every live process sends at every multiple of eta, and a message sent at
time s >= GST arrives in [s + 1, s + delta]. A process crashes at a given
tick and sends nothing after that.

The detector module of p keeps, for each q, the time last[q] of the latest
heartbeat from q and a timeout T[q]. If now - last[q] > T[q], p suspects q.
When a heartbeat from a suspected q arrives, p trusts q again and, in the
adaptive version, adds 1 to T[q]. The fixed version never changes T[q].
"""

import random
from typing import Optional


def run(n: int, gst: int, eta: int, delta: int, horizon: int, seed: int, crash_at: Optional[dict[int, int]] = None, adaptive: bool = True, t0: int = 1, after_gst: str = "random") -> dict:
    """Simulate the detector at every process for ticks 0 .. horizon - 1.

    after_gst is "random" (delays uniform in [1, delta]) or "adversary"
    (the heartbeats get the delays 1, delta, eta + 1, 1, delta, eta + 1, ...).
    If delta <= 2 * eta + 1, the adversary makes the gap between two
    arrivals equal to eta + delta - 1 in every third period: the heartbeat
    with delay 1 arrives, the next one arrives delta - 1 + eta ticks later,
    and the third one arrives together with the fourth.
    """
    rng = random.Random(seed)
    crash_at = dict(crash_at or {})
    inbox: dict[int, list[tuple[int, int]]] = {}
    last = [[0] * n for _ in range(n)]
    timeout = [[t0] * n for _ in range(n)]
    susp: list[set[int]] = [set() for _ in range(n)]
    events: list[tuple[int, int, int, str]] = []

    def alive(p: int, t: int) -> bool:
        return p not in crash_at or t < crash_at[p]

    for t in range(horizon):
        # 1. Heartbeats that arrive now.
        for dest, src in inbox.pop(t, []):
            if not alive(dest, t):
                continue
            last[dest][src] = t
            if src in susp[dest]:
                susp[dest].discard(src)
                events.append((t, dest, src, "trust"))
                if adaptive:
                    timeout[dest][src] += 1
        # 2. Timeouts.
        for p in range(n):
            if not alive(p, t):
                continue
            for q in range(n):
                if q != p and q not in susp[p] and t - last[p][q] > timeout[p][q]:
                    susp[p].add(q)
                    events.append((t, p, q, "suspect"))
        # 3. Heartbeats sent now.
        if t % eta == 0:
            for p in range(n):
                if not alive(p, t) or (t < gst and rng.random() < 0.5):
                    continue
                for q in range(n):
                    if q == p:
                        continue
                    if t >= gst and after_gst == "adversary":
                        d = (1, delta, min(delta, eta + 1))[(t // eta) % 3]
                    elif t >= gst:
                        d = rng.randint(1, delta)
                    else:
                        d = rng.randint(1, 4 * gst + delta)
                    arrive = min(t + d, max(t, gst) + delta)
                    inbox.setdefault(arrive, []).append((q, p))

    crashed = sorted(crash_at)
    return {
        "events": events,
        "suspects": [sorted(s) for s in susp],
        "timeout": timeout,
        "crashed": crashed,
        "correct": [p for p in range(n) if p not in crash_at],
        "horizon": horizon,
    }


def false_suspicions(res: dict, since: int = 0) -> int:
    """Suspicions of correct processes, by correct processes, that start at or after `since`."""
    ok = set(res["correct"])
    return sum(1 for t, p, q, k in res["events"] if k == "suspect" and t >= since and p in ok and q in ok)


def last_mistake_end(res: dict) -> int:
    """The last tick at which a correct process trusts a correct process again (0 if never)."""
    ok = set(res["correct"])
    return max((t for t, p, q, k in res["events"] if k == "trust" and p in ok and q in ok), default=0)


def exact_at_end(res: dict) -> bool:
    """Each correct process suspects exactly the crashed processes at the end of the run."""
    return all(res["suspects"][p] == res["crashed"] for p in res["correct"])
