# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-commit/. The authors are listed in prov/D9GM98.jsonl.

"""Group commit on a simulated clock.

Transactions ask to commit at given integer times. Each request appends one
commit record to the log tail. The log device does one write at a time, and a
write of any number of records takes D time units; the records become durable
when the write ends. A commit is acknowledged only when its record is durable.
The log writer starts a write when the device is idle and the tail holds at
least k records, or its oldest record has waited tau units. With group=False
each write takes one record (no group commit).
"""

from dataclasses import dataclass, field


@dataclass
class Commit:
    txn: int
    lsn: int
    asked: int
    durable: int = -1  # the end time of the write that holds the record
    acked: int = -1


@dataclass
class Run:
    commits: list[Commit] = field(default_factory=list)
    writes: list[tuple[int, int, int]] = field(default_factory=list)  # (start, end, records)

    def latencies(self) -> list[int]:
        return [c.acked - c.asked for c in self.commits]


def simulate(arrivals: list[int], d: int, k: int = 1, tau: int = 0, group: bool = True,
             early_ack: bool = False) -> Run:
    """Run the log writer. early_ack=True is the wrong rule that acknowledges
    a commit when its write starts, for the tests. Cost: O(n) events."""
    arr = sorted(arrivals)
    run, tail, inflight = Run(), [], []
    now, i, busy_until, lsn = 0, 0, None, 0
    while i < len(arr) or tail or inflight:  # @line L5
        times = []
        if i < len(arr):
            times.append(arr[i])
        if inflight:
            times.append(busy_until)
        elif tail:
            times.append(now if len(tail) >= k else max(now, tail[0].asked + tau))
        now = min(times)
        if inflight and busy_until == now:  # @line L8
            for c in inflight:  # @line L9
                c.durable = now
                if not early_ack:  # @line L3
                    c.acked = now  # @line L4
            inflight = []
        while i < len(arr) and arr[i] == now:
            lsn += 1
            c = Commit(txn=i + 1, lsn=lsn, asked=now)  # @line L1
            run.commits.append(c)
            tail.append(c)  # @line L2
            i += 1
        if not inflight and tail and (len(tail) >= k or now >= tail[0].asked + tau):  # @line L6
            n = len(tail) if group else 1
            inflight, tail = tail[:n], tail[n:]  # @line L7
            busy_until = now + d
            run.writes.append((now, busy_until, n))
            if early_ack:
                for c in inflight:
                    c.acked = now
    return run


def acked_before_durable(run: Run) -> list[int]:
    """The transactions whose commit was acknowledged before their record was
    durable. Group commit must keep this empty (a crash at a time in between
    would lose an acknowledged commit)."""
    return [c.txn for c in run.commits if c.acked < c.durable]
