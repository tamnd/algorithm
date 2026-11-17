# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiversion-concurrency-control/. The authors are listed in prov/07QKP2.jsonl.

"""Multiversion timestamp ordering (MVTO), after Reed (1978) and Bernstein and
Goodman (1983), with commit dependencies and version garbage collection.

Each version of x holds wts (the timestamp of its writer), rts (the largest
timestamp of a reader), its value and whether its writer has committed. A read
never waits and never aborts. A write aborts if a younger transaction already
read the version it would follow. A transaction that read an uncommitted
version commits only after its writer does, and aborts if its writer aborts.
"""


class Version:
    __slots__ = ("wts", "rts", "value", "committed")

    def __init__(self, wts: int, value, committed: bool) -> None:
        self.wts, self.rts, self.value, self.committed = wts, wts, value, committed


class Mvto:
    def __init__(self, initial: dict) -> None:
        self.versions = {x: [Version(0, v, True)] for x, v in initial.items()}  # sorted by wts
        self.next_ts = 1
        self.status: dict[int, str] = {}  # ts -> active, committed, aborted
        self.deps: dict[int, set[int]] = {}  # ts -> writers it read from, not yet committed
        self.readers: dict[int, set[int]] = {}  # writer ts -> readers of its versions
        self.written: dict[int, set] = {}
        self.reads_from: dict[int, list] = {}  # ts -> [(x, wts)]

    def begin(self) -> int:
        t = self.next_ts  # @line L1
        self.next_ts += 1
        self.status[t] = "active"
        self.deps[t], self.written[t], self.reads_from[t] = set(), set(), []
        return t

    def _visible(self, x, t: int) -> Version:
        return max((v for v in self.versions[x] if v.wts <= t), key=lambda v: v.wts)

    def read(self, t: int, x):
        v = self._visible(x, t)  # @line L2
        v.rts = max(v.rts, t)  # @line L3
        if not v.committed and v.wts != t:  # @line L4
            self.deps[t].add(v.wts)
            self.readers.setdefault(v.wts, set()).add(t)
        self.reads_from[t].append((x, v.wts))
        return v.value

    def write(self, t: int, x, value) -> bool:
        """Returns False if t had to abort."""
        v = self._visible(x, t)  # @line L5
        if v.wts == t:
            v.value = value
            return True
        if v.rts > t:  # @line L6
            self.abort(t)
            return False
        vs = self.versions[x]
        vs.insert(vs.index(v) + 1, Version(t, value, False))  # @line L7
        self.written[t].add(x)
        return True

    def try_commit(self, t: int) -> str:
        """committed, aborted, or wait (a writer it read from is active)."""
        if self.status[t] != "active":
            return self.status[t]
        if any(self.status[d] == "aborted" for d in self.deps[t]):
            self.abort(t)
            return "aborted"
        if self.deps[t]:  # @line L8
            return "wait"
        self.status[t] = "committed"  # @line L9
        for x in self.written[t]:
            for v in self.versions[x]:
                if v.wts == t:
                    v.committed = True
        for r in self.readers.pop(t, ()):
            self.deps[r].discard(t)
        return "committed"

    def abort(self, t: int) -> None:
        if self.status[t] == "aborted":
            return
        self.status[t] = "aborted"
        for x in self.written[t]:  # @line L10
            self.versions[x] = [v for v in self.versions[x] if v.wts != t]
        for r in sorted(self.readers.pop(t, ())):  # cascading abort
            self.abort(r)

    def gc(self) -> int:
        """Drop versions that no present or future transaction can read: for
        each item keep every version with wts >= m and the newest one below m,
        where m is the smallest active timestamp. Returns the number dropped."""
        active = [t for t, s in self.status.items() if s == "active"]
        m = min(active, default=self.next_ts)  # @line L11
        dropped = 0
        for x, vs in self.versions.items():
            below = [v for v in vs if v.wts < m]
            keep = [v for v in vs if v.wts >= m]
            if below:
                keep.insert(0, below[-1])  # @line L12
            dropped += len(vs) - len(keep)
            self.versions[x] = keep
        return dropped
