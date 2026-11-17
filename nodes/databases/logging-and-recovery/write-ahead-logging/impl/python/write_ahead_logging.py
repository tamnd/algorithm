# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-ahead-logging/. The authors are listed in prov/MBX83W.jsonl.

"""Write-ahead logging with before and after images, a steal and no-force
buffer pool, and restart recovery by redo (repeat history) then undo.

Model: one item per page. A page has a value and a pageLSN. Stable storage is
the disk (item -> (value, pageLSN)) and the stable log. Volatile storage is the
buffer pool and the log tail; a crash keeps only stable storage. Each method is
one atomic step of the simulation. The flags wal_rule and commit_rule exist only
so that tests can show what breaks when a rule is dropped.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LogRecord:
    lsn: int
    kind: str  # "update", "commit" or "abort"
    txn: int
    item: str = ""
    before: int = 0
    after: int = 0


Disk = dict[str, tuple[int, int]]


class WalSystem:
    """A database with a write-ahead log. Cost: O(1) per update, O(k) per log
    flush of k records, O(u) per abort of a transaction with u updates."""

    def __init__(self, disk: Disk, log: list[LogRecord] | None = None,
                 wal_rule: bool = True, commit_rule: bool = True) -> None:
        self.disk: Disk = dict(disk)
        self.stable_log: list[LogRecord] = list(log or [])
        self.tail: list[LogRecord] = []
        self.buffer: dict[str, list[int]] = {}  # item -> [value, pageLSN]
        self.next_lsn = 1 + max((r.lsn for r in self.stable_log), default=0)
        self.acked: set[int] = set()
        self.wal_rule = wal_rule
        self.commit_rule = commit_rule

    def _append(self, kind: str, txn: int, item: str = "", before: int = 0, after: int = 0) -> LogRecord:
        rec = LogRecord(self.next_lsn, kind, txn, item, before, after)
        self.next_lsn += 1
        self.tail.append(rec)
        return rec

    def _fetch(self, x: str) -> list[int]:
        if x not in self.buffer:
            v, plsn = self.disk[x]
            self.buffer[x] = [v, plsn]
        return self.buffer[x]

    def read(self, x: str) -> int:
        return self._fetch(x)[0]

    def update(self, t: int, x: str, v: int) -> None:
        p = self._fetch(x)  # @line L1
        r = self._append("update", t, x, before=p[0], after=v)  # @line L2
        p[0], p[1] = v, r.lsn  # @line L3

    def flush_log(self, upto: int) -> None:
        """Move every tail record with lsn <= upto to the stable log."""
        keep = []
        for r in self.tail:
            (self.stable_log if r.lsn <= upto else keep).append(r)
        self.tail = keep

    def flush_page(self, x: str) -> None:
        """Steal: write a buffered page to disk, whoever changed it."""
        p = self.buffer.pop(x)
        if self.wal_rule:
            self.flush_log(p[1])  # @line L4
        self.disk[x] = (p[0], p[1])  # @line L5

    def commit(self, t: int) -> None:
        r = self._append("commit", t)  # @line L6
        if self.commit_rule:
            self.flush_log(r.lsn)  # @line L7
        self.acked.add(t)  # @line L8

    def abort(self, t: int) -> None:
        """Roll back t while running: log a restoring update for each update of
        t, newest first, then an abort record. No flush is needed."""
        mine = [r for r in self.stable_log + self.tail if r.kind == "update" and r.txn == t]
        for r in reversed(mine):
            self.update(t, r.item, r.before)
        self._append("abort", t)

    def crash(self) -> tuple[Disk, list[LogRecord]]:
        """Lose the buffer pool and the log tail; return stable storage."""
        return dict(self.disk), list(self.stable_log)


def recovery_steps(disk: Disk, log: list[LogRecord]) -> list[tuple[str, object]]:
    """Restart recovery. Returns the stable writes it makes, in order: ("page",
    (x, value, pageLSN)) and, last, ("log", [abort records]). A crash may stop
    the list anywhere; running recovery again on the result is still correct.
    Cost: O(|log| + |disk|) time."""
    pages = dict(disk)
    for r in log:  # @line L9
        if r.kind == "update" and pages[r.item][1] < r.lsn:  # @line L10
            pages[r.item] = (r.after, r.lsn)
    ended = {r.txn for r in log if r.kind in ("commit", "abort")}
    losers = sorted({r.txn for r in log if r.kind == "update"} - ended)  # @line L11
    for r in reversed(log):  # @line L12
        if r.kind == "update" and r.txn in losers:
            pages[r.item] = (r.before, pages[r.item][1])
    steps: list[tuple[str, object]] = []
    for x in sorted(pages):  # @line L13
        if pages[x] != disk[x]:
            steps.append(("page", (x, pages[x][0], pages[x][1])))
    next_lsn = 1 + max((r.lsn for r in log), default=0)
    aborts = [LogRecord(next_lsn + i, "abort", t) for i, t in enumerate(losers)]
    steps.append(("log", aborts))
    return steps


def recover(disk: Disk, log: list[LogRecord], stop_after: int | None = None) -> tuple[Disk, list[LogRecord]]:
    """Run recovery on stable storage. With stop_after = k, crash after the first
    k stable writes of recovery. Returns the new stable storage."""
    disk, log = dict(disk), list(log)
    for i, (kind, arg) in enumerate(recovery_steps(disk, log)):
        if stop_after is not None and i >= stop_after:
            break
        if kind == "page":
            x, v, plsn = arg  # type: ignore[misc]
            disk[x] = (v, plsn)
        else:
            log.extend(arg)  # type: ignore[arg-type]
    return disk, log
