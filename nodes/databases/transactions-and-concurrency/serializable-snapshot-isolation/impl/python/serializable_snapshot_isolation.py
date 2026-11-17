# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serializable-snapshot-isolation/. The authors are listed in prov/04RT24.jsonl.

"""Serializable snapshot isolation of Cahill, Rohm and Fekete (2008).

The base is snapshot isolation: a transaction reads the newest version
committed at or before its start, keeps its writes private until commit, and
commits only if no concurrent transaction committed a write to the same item
(first committer wins).

On top of it, every read takes an SIREAD lock that stays after commit, and
every transaction has two flags. `inc[t]` says that some concurrent
transaction read an item that t writes (an rw edge into t); `outc[t]` says
that t read an item that a concurrent transaction writes (an rw edge out of
t). A transaction with both flags is a possible pivot of the dangerous
structure of Fekete et al. (2005), and the algorithm aborts it, or aborts the
transaction whose operation would make a committed transaction a pivot.

With ssi=False the class runs plain snapshot isolation, for comparison.
"""


class Aborted(Exception):
    pass


class SsiDb:
    def __init__(self, initial: dict, ssi: bool = True) -> None:
        self.ssi = ssi
        self.clock = 0
        self.versions = {x: [(0, v, 0)] for x, v in initial.items()}  # (commit_ts, value, writer)
        self.start: dict[int, int] = {}
        self.commit_ts: dict[int, int] = {}
        self.state: dict[int, str] = {}  # running, committed or aborted
        self.inc: dict[int, bool] = {}
        self.outc: dict[int, bool] = {}
        self.pending: dict[int, dict] = {}
        self.siread: dict = {}  # item -> set of transactions holding an SIREAD lock
        self.reads: list[tuple] = []  # (txn, item, writer of the version read)
        self.written: dict[int, set] = {}  # committed txn -> items written
        self.why: dict[int, str] = {}

    def begin(self, t: int) -> None:
        self.start[t], self.inc[t], self.outc[t] = self.clock, False, False  # @line L1
        self.state[t], self.pending[t] = "running", {}

    def read(self, t: int, x):
        self.siread.setdefault(x, set()).add(t)  # @line L2
        if self.ssi:
            for u, s in self.state.items():  # @line L3
                if u != t and s == "running" and x in self.pending[u]:
                    self.inc[u], self.outc[t] = True, True
            newer = [w for ts, _, w in self.versions[x] if ts > self.start[t]]  # @line L4
            if any(self.outc[u] for u in newer):  # @line L5
                self._fail(t, "unsafe read")
            for u in newer:  # @line L6
                self.inc[u], self.outc[t] = True, True
        if x in self.pending[t]:  # @line L7
            self.reads.append((t, x, t))
            return self.pending[t][x]
        ts, v, w = max((ver for ver in self.versions[x] if ver[0] <= self.start[t]), key=lambda ver: ver[0])
        self.reads.append((t, x, w))
        return v

    def write(self, t: int, x, v) -> None:
        if self.ssi:
            readers = [u for u in self.siread.get(x, ()) if u != t and  # @line L8
                       (self.state[u] == "running" or self.commit_ts[u] > self.start[t])]
            if any(self.state[u] == "committed" and self.inc[u] for u in readers):  # @line L9
                self._fail(t, "unsafe write")
            for u in readers:  # @line L10
                self.outc[u], self.inc[t] = True, True
        self.pending[t][x] = v  # @line L11

    def commit(self, t: int) -> int:
        if self.ssi and self.inc[t] and self.outc[t]:  # @line L12
            self._fail(t, "pivot")
        s = self.start[t]
        if any(ts > s for x in self.pending[t] for ts, _, _ in self.versions[x]):  # @line L13
            self._fail(t, "first committer wins")
        self.clock += 1  # @line L14
        for x, v in self.pending[t].items():
            self.versions[x].append((self.clock, v, t))
        self.state[t], self.commit_ts[t] = "committed", self.clock
        self.written[t] = set(self.pending[t])
        self.release()
        return self.clock

    def abort(self, t: int) -> None:
        self.state[t], self.pending[t] = "aborted", {}  # @line L15
        for holders in self.siread.values():
            holders.discard(t)
        self.release()

    def release(self) -> None:
        """Drop the SIREAD locks of committed transactions that no running
        transaction overlaps: every running or future transaction started at
        or after their commit."""
        oldest = min((self.start[u] for u, s in self.state.items() if s == "running"), default=self.clock)
        for holders in self.siread.values():  # @line L16
            for u in list(holders):
                if self.state[u] == "committed" and self.commit_ts[u] <= oldest:
                    holders.discard(u)

    def _fail(self, t: int, why: str) -> None:
        self.abort(t)
        self.why[t] = why
        raise Aborted(t, why)

    def value(self, x):
        return max(self.versions[x], key=lambda ver: ver[0])[1]
