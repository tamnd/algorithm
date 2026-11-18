# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-behind-logging/. The authors are listed in prov/80XPYE.jsonl.

"""Write-behind logging (Arulraj, Perron and Pavlo) on simulated non-volatile memory.

Data lives in NVM as multiversion tuples: each version holds a key, a value and
the timestamp of the transaction that wrote it. A new version first sits in
the volatile CPU cache and may reach NVM at any time (an eviction). The dirty
tuple table (DTT), in DRAM, lists the versions of each transaction.

Transactions run one at a time and are grouped. At a group commit the system
persists every version of the group, and only then persists a log record
<c_p, c_d, gaps>: every timestamp up to c_p is decided, and no transaction of
the next group gets a timestamp of c_d or more. After a crash, the interval
(c_p, c_d) of the last record is a gap: versions with a timestamp in a gap are
not visible. Recovery reads one log record and writes one. There is no redo
and no undo; garbage collection removes the versions in the gaps later.
"""

from dataclasses import dataclass

INIT = {"a": 10, "b": 20, "c": 30, "d": 40}


@dataclass(frozen=True)
class Version:
    key: str
    value: int
    ts: int


@dataclass(frozen=True)
class LogRec:
    cp: int
    cd: int
    gaps: tuple  # of (low, high), open intervals


def in_gap(ts: int, gaps) -> bool:
    return any(lo < ts < hi for lo, hi in gaps)


class WblDb:
    def __init__(self, nvm: list | None = None, log: list | None = None, group: int = 100):
        self.G = group
        self.nvm: list[Version] = list(nvm or [])  # persistent
        self.log: list[LogRec] = list(log or [LogRec(0, group, ())])  # persistent
        self.cache: list[Version] = []  # volatile
        self.dtt: dict[int, list[Version]] = {}  # volatile
        self.pending: list[int] = []  # transactions of the open group
        self.next_ts = self.log[-1].cp + 1
        self.records_read = 0

    # ------------------------------------------------------------ reads
    def read(self, key: str) -> int:
        gaps = self.log[-1].gaps
        best = None
        for v in self.nvm + self.cache:
            if v.key == key and not in_gap(v.ts, gaps):  # @line L7
                if best is None or v.ts > best.ts:  # @line L7
                    best = v
        return INIT[key] if best is None else best.value

    def state(self) -> dict:
        return {k: self.read(k) for k in INIT}

    # ------------------------------------------------------------ transactions
    def begin(self) -> int:
        if self.next_ts >= self.log[-1].cd:
            raise RuntimeError("the group is full: call group_commit first")  # the promise of c_d
        ts = self.next_ts
        self.next_ts += 1
        self.dtt[ts] = []
        return ts

    def write(self, ts: int, key: str, value: int) -> None:
        for old in [o for o in self.dtt[ts] if o.key == key]:  # a transaction keeps one version per key
            self.dtt[ts].remove(old)
            self.cache = [o for o in self.cache if o != old]
            self.nvm = [o for o in self.nvm if o != old]
        v = Version(key, value, ts)
        self.cache.append(v)
        self.dtt[ts].append(v)

    def evict(self, i: int) -> None:
        """The cache writes one version to NVM before commit."""
        if self.cache:
            self.nvm.append(self.cache.pop(i % len(self.cache)))

    def commit(self, ts: int) -> None:
        """Pre-commit: the versions stay visible, and the transaction is
        reported at the end of its group."""
        self.pending.append(ts)

    def abort(self, ts: int) -> None:
        mine = set(self.dtt.pop(ts))
        self.cache = [v for v in self.cache if v not in mine]
        self.nvm = [v for v in self.nvm if v not in mine]

    def group_commit(self) -> list[int]:
        """Persist the group, then its log record. Return the reported transactions."""
        for ts in self.pending:  # @line L1
            for v in self.dtt.pop(ts):  # @line L1
                if v in self.cache:
                    self.cache.remove(v)
                    self.nvm.append(v)  # @line L1
        cp = self.next_ts - 1  # @line L2
        cd = cp + self.G  # @line L2
        gaps = tuple(g for g in self.log[-1].gaps if any(in_gap(v.ts, [g]) for v in self.nvm))
        self.log.append(LogRec(cp, cd, gaps))  # @line L3
        done, self.pending = self.pending, []
        return done  # @line L4

    # ------------------------------------------------------------ failure and recovery
    def crash(self) -> "WblDb":
        return WblDb(self.nvm, self.log, self.G)

    def recover(self) -> None:
        last = self.log[-1]  # @line L5
        self.records_read = 1
        gaps = last.gaps + ((last.cp, last.cd),)  # @line L6
        self.log.append(LogRec(last.cd, last.cd + self.G, gaps))  # @line L6
        self.next_ts = last.cd + 1

    def gc_step(self) -> bool:
        """Remove one version that lies in a gap. Return False if none is left."""
        gaps = self.log[-1].gaps
        for i, v in enumerate(self.nvm):
            if in_gap(v.ts, gaps):
                del self.nvm[i]  # @line L8
                return True
        return False
