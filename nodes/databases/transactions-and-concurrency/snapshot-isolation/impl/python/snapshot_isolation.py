# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snapshot-isolation/. The authors are listed in prov/ZZY45M.jsonl.

"""Snapshot isolation as defined by Berenson et al. (1995).

Each committed version of an item carries the commit timestamp of its writer.
A transaction gets a start timestamp at its first operation and reads, for
each item, its own write if any, else the newest version with a commit
timestamp at most its start timestamp. Writes are kept private until commit.
At commit it gets a new timestamp, and it commits only if no transaction that
committed in its interval (start, commit] wrote an item that it also wrote
(first committer wins).
"""


class Aborted(Exception):
    pass


class SnapshotDb:
    def __init__(self, initial: dict) -> None:
        self.clock = 0
        self.versions = {x: [(0, v, 0)] for x, v in initial.items()}  # (commit_ts, value, txn)
        self.start: dict[int, int] = {}
        self.writes: dict[int, dict] = {}
        self.history: list[tuple] = []  # (op, txn, item, version txn or value)
        self.committed: dict[int, int] = {}  # txn -> commit_ts

    def _begin(self, t: int) -> None:
        if t not in self.start:
            self.start[t] = self.clock
            self.writes[t] = {}

    def read(self, t: int, x: str):
        self._begin(t)
        if x in self.writes[t]:
            v = self.writes[t][x]
            self.history.append(("r", t, x, t))
            return v
        ts, v, w = max(ver for ver in self.versions.get(x, [(0, None, 0)]) if ver[0] <= self.start[t])
        self.history.append(("r", t, x, w))
        return v

    def write(self, t: int, x: str, v) -> None:
        self._begin(t)
        self.writes[t][x] = v
        self.history.append(("w", t, x, v))

    def commit(self, t: int) -> int:
        self._begin(t)
        s = self.start[t]
        for x in self.writes[t]:
            if any(ts > s for ts, _, _ in self.versions.get(x, [])):
                self.history.append(("a", t))
                raise Aborted(t)  # first committer wins
        self.clock += 1
        for x, v in self.writes[t].items():
            self.versions.setdefault(x, []).append((self.clock, v, t))
        self.committed[t] = self.clock
        self.history.append(("c", t))
        return self.clock

    def abort(self, t: int) -> None:
        self._begin(t)
        self.history.append(("a", t))

    def snapshot(self, ts: int | None = None) -> dict:
        ts = self.clock if ts is None else ts
        return {x: max(v for v in vs if v[0] <= ts)[1] for x, vs in self.versions.items()}
