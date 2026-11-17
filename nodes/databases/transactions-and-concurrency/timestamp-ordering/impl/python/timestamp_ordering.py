# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timestamp-ordering/. The authors are listed in prov/X0WMGA.jsonl.

"""Basic timestamp ordering (Bernstein and Goodman 1981).

Each transaction gets a timestamp when it starts. Each item x keeps the
largest timestamp of a transaction that has read it, rts(x), and of one that
has written it, wts(x). An action is accepted only if it does not come too
late in timestamp order; otherwise its transaction is rejected (aborted) and
may restart with a new, larger timestamp. Every accepted pair of conflicting
actions is then in timestamp order.
"""

import random


class TOScheduler:
    """The read and write rules of basic timestamp ordering."""

    def __init__(self) -> None:
        self.rts: dict[str, int] = {}
        self.wts: dict[str, int] = {}

    def read(self, ts: int, x: str) -> bool:
        if ts < self.wts.get(x, 0):  # @line L1
            return False  # x was already written by a younger transaction
        self.rts[x] = max(self.rts.get(x, 0), ts)  # @line L2
        return True

    def write(self, ts: int, x: str) -> bool:
        if ts < self.rts.get(x, 0) or ts < self.wts.get(x, 0):  # @line L3
            return False  # a younger transaction already read or wrote x
        self.wts[x] = ts  # @line L4
        return True


def start_timestamps(schedule: list) -> dict[int, int]:
    """Timestamps 1, 2, ... in the order in which transactions first appear."""
    ts: dict[int, int] = {}
    for _, t, _ in schedule:
        ts.setdefault(t, len(ts) + 1)
    return ts


def run_to_on_schedule(schedule: list, ts: dict[int, int] | None = None) -> tuple[list, set[int]]:
    """Feed a fixed input schedule of (op, txn, item) to the scheduler.

    A rejected transaction aborts, and its later actions are dropped.
    Return (accepted actions, rejected transactions).
    """
    ts = ts or start_timestamps(schedule)
    sched = TOScheduler()
    out, rejected = [], set()
    for op, t, x in schedule:
        if t in rejected:
            continue
        ok = sched.read(ts[t], x) if op == "r" else sched.write(ts[t], x)
        if ok:
            out.append((op, t, x))
        else:
            rejected.add(t)
    return out, rejected


def run_to(programs: dict[int, list], rng: random.Random, max_steps: int = 100000) -> dict:
    """Run the programs in a random interleaving under basic TO with restarts.

    A rejected transaction aborts and restarts from its first action with a
    new timestamp, larger than every timestamp given so far. Returns the
    committed projection, the final timestamp of each transaction, and the
    number of restarts.
    """
    sched = TOScheduler()
    clock = 0
    ts: dict[int, int] = {}
    pc = {t: 0 for t in programs}
    restarts = 0

    def start(t: int) -> None:
        nonlocal clock
        clock += 1
        ts[t] = clock
        pc[t] = 0

    for t in programs:
        start(t)
    log: list = []
    for _ in range(max_steps):
        live = [t for t in programs if pc[t] <= len(programs[t])]
        if not live:
            break
        t = rng.choice(live)
        if pc[t] == len(programs[t]):
            pc[t] += 1  # commit
            continue
        op, x = programs[t][pc[t]]
        ok = sched.read(ts[t], x) if op == "r" else sched.write(ts[t], x)
        if ok:
            log.append((op, t, x, ts[t]))
            pc[t] += 1
        else:
            restarts += 1
            start(t)  # @line L5
    else:
        raise RuntimeError("step limit reached")
    committed = [(op, t, x) for op, t, x, s in log if s == ts[t]]
    return {"committed": committed, "ts": ts, "restarts": restarts}
