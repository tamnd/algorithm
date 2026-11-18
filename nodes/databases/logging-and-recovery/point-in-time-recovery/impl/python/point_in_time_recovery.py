# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-in-time-recovery/. The authors are listed in prov/9VV51Q.jsonl.

"""Point-in-time recovery from a fuzzy archive copy and the archive log.

Normal processing is write-ahead logging with record locks held to the end
of the transaction, steal and no-force, and physical update records. Each
commit record carries the time of the commit. A fuzzy copy reads the disk one
page at a time while transactions run; its start LSN is the smallest recLSN of
the pages that are dirty in the buffer when it begins. The log is kept on a
device of its own and is the archive log.

recover_to(archive, log, t) builds a new database that holds the effects of
exactly the transactions that committed at or before time t.
"""

from dataclasses import dataclass

PAGE_OF = {"a": "P1", "b": "P1", "c": "P2", "d": "P2", "e": "P3"}
INIT = {"a": 10, "b": 20, "c": 30, "d": 40, "e": 50}


@dataclass(frozen=True)
class Rec:
    lsn: int
    kind: str  # begin, update, clr, commit, end, begin_copy, end_copy
    txn: int = 0
    prev: int = 0
    page: str = ""
    key: str = ""
    before: int = 0
    after: int = 0
    time: int = 0  # commit only
    undo_next: int = 0  # clr only


@dataclass(frozen=True)
class Copy:
    start: int  # redo from here
    end: int  # LSN of the end_copy record
    pages: dict  # page -> (values, page_lsn)


class Db:
    def __init__(self):
        self.disk: dict = {}
        for k, p in sorted(PAGE_OF.items()):
            self.disk.setdefault(p, ({}, 0))[0][k] = INIT[k]
        self.log: list[Rec] = []  # stable log, also the archive log
        self.tail: list[Rec] = []
        self.buf: dict[str, list] = {}  # page -> [values, page_lsn, rec_lsn or 0]
        self.last: dict[int, int] = {}
        self.locks: dict[str, int] = {}
        self.clock = 0
        self.archive: list[Copy] = []
        self.copying: tuple | None = None  # (start, pages copied, pages left)

    def _append(self, **kw) -> Rec:
        r = Rec(lsn=len(self.log) + len(self.tail) + 1, **kw)
        self.tail.append(r)
        if r.txn:
            self.last[r.txn] = r.lsn
        return r

    def flush_log(self) -> None:
        self.log.extend(self.tail)
        self.tail = []

    def _fix(self, p: str) -> list:
        if p not in self.buf:
            vals, lsn = self.disk[p]
            self.buf[p] = [dict(vals), lsn, 0]
        return self.buf[p]

    def flush_page(self, p: str) -> None:
        if p in self.buf:
            pg = self.buf[p]
            if pg[1] > len(self.log):  # the WAL rule
                self.flush_log()
            self.disk[p] = (dict(pg[0]), pg[1])
            pg[2] = 0

    def begin(self, txn: int) -> None:
        self._append(kind="begin", txn=txn)

    def _set(self, txn: int, key: str, value: int, kind: str, undo_next: int = 0) -> None:
        pg = self._fix(PAGE_OF[key])
        r = self._append(kind=kind, txn=txn, prev=self.last[txn], page=PAGE_OF[key], key=key,
                         before=pg[0][key], after=value, undo_next=undo_next)
        pg[0][key], pg[1] = value, r.lsn
        if not pg[2]:
            pg[2] = r.lsn

    def write(self, txn: int, key: str, value: int) -> bool:
        if self.locks.setdefault(key, txn) != txn:
            return False
        self._set(txn, key, value, "update")
        return True

    def _end(self, txn: int) -> None:
        self._append(kind="end", txn=txn, prev=self.last.pop(txn))
        for k in [k for k, t in self.locks.items() if t == txn]:
            del self.locks[k]

    def commit(self, txn: int) -> int:
        self.clock += 1
        self._append(kind="commit", txn=txn, prev=self.last[txn], time=self.clock)
        self.flush_log()
        self._end(txn)
        return self.clock

    def abort(self, txn: int) -> None:
        """Roll back at once with CLRs."""
        nxt = self.last[txn]
        while nxt:
            r = self.rec(nxt)
            if r.kind == "update":
                self._set(txn, r.key, r.before, "clr", undo_next=r.prev)
            nxt = r.undo_next if r.kind == "clr" else r.prev
        self._end(txn)

    def rec(self, lsn: int) -> Rec:
        i = lsn - 1
        return self.log[i] if i < len(self.log) else self.tail[i - len(self.log)]

    def begin_copy(self) -> None:
        r = self._append(kind="begin_copy")
        self.flush_log()
        start = min([pg[2] for pg in self.buf.values() if pg[2]] + [r.lsn])
        self.copying = (start, {}, sorted(self.disk))

    def copy_step(self) -> None:
        """Copy one page from the disk, or end the copy."""
        start, pages, left = self.copying
        if left:
            pages[left[0]] = (dict(self.disk[left[0]][0]), self.disk[left[0]][1])
            self.copying = (start, pages, left[1:])
            return
        r = self._append(kind="end_copy")
        self.flush_log()
        self.archive.append(Copy(start, r.lsn, pages))
        self.copying = None


def target_lsn(log: list[Rec], t: int) -> int:
    """The last LSN before the first commit after time t."""
    for r in log:
        if r.kind == "commit" and r.time > t:
            return r.lsn - 1
    return len(log)


def recover_to(archive: list[Copy], log: list[Rec], t: int) -> tuple[dict, list[Rec]]:
    """A new database with the transactions committed at or before t, and the
    log of the new branch."""
    stop = target_lsn(log, t)  # @line L1
    usable = [c for c in archive if c.end <= stop]
    if not usable:
        raise ValueError("no archive copy ended before the target")
    copy = max(usable, key=lambda c: c.end)  # @line L2
    disk = {p: [dict(v), lsn] for p, (v, lsn) in copy.pages.items()}  # @line L2
    head = log[:stop]  # @line L3
    for r in head[copy.start - 1:]:  # @line L4
        if r.kind in ("update", "clr") and disk[r.page][1] < r.lsn:  # @line L5
            disk[r.page][0][r.key], disk[r.page][1] = r.after, r.lsn  # @line L5
    last: dict[int, int] = {}
    for r in head:  # @line L6
        if r.kind == "end":
            last.pop(r.txn, None)
        elif r.txn and r.kind != "commit":
            last[r.txn] = r.lsn  # @line L6
        elif r.kind == "commit":
            last[r.txn] = 0  # committed by the target: not a loser
    branch = list(head)
    for txn in sorted(t for t, lsn in last.items() if lsn):  # @line L7
        nxt, prev = last[txn], last[txn]
        while nxt:
            r = branch[nxt - 1]
            if r.kind == "update":  # @line L7
                c = Rec(lsn=len(branch) + 1, kind="clr", txn=txn, prev=prev, page=r.page, key=r.key,
                        before=disk[r.page][0][r.key], after=r.before, undo_next=r.prev)
                branch.append(c)  # @line L7
                disk[r.page][0][r.key], disk[r.page][1] = r.before, c.lsn  # @line L7
                prev = c.lsn
            nxt = r.undo_next if r.kind == "clr" else r.prev
        branch.append(Rec(lsn=len(branch) + 1, kind="end", txn=txn, prev=prev))  # @line L8
    return {p: (v, lsn) for p, (v, lsn) in disk.items()}, branch  # @line L8
