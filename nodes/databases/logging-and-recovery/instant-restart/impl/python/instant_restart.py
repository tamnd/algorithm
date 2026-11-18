# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instant-restart/. The authors are listed in prov/81XW5M.jsonl.

"""A toy version of instant restart (Graefe, Guy and Sauer) on a simulated disk.

Normal processing is write-ahead logging with record locks held to the end of
the transaction, steal and no-force, and physical update records. Restart
runs log analysis only and then opens the system. A page that still needs
redo is redone when it is first fixed in the buffer, from the list of its log
records that analysis built (the per-page chain). A loser is rolled back when
a new transaction asks for one of its locks. A background step does the rest
of the work, one page or one undo at a time.

There are no checkpoints, so analysis reads the whole log. A crash keeps the
disk (page -> (values, page_lsn)) and the stable log and loses the rest.
"""

from dataclasses import dataclass

PAGE_OF = {"a": "P1", "b": "P1", "c": "P2", "d": "P2", "e": "P3", "f": "P3"}
INIT = {"a": 10, "b": 20, "c": 30, "d": 40, "e": 50, "f": 60}


@dataclass(frozen=True)
class Rec:
    lsn: int
    kind: str  # begin, update, clr, commit, abort, end
    txn: int
    prev: int = 0
    page: str = ""
    key: str = ""
    before: int = 0
    after: int = 0
    undo_next: int = 0  # clr only


def fresh_disk() -> dict:
    disk: dict = {}
    for k, p in sorted(PAGE_OF.items()):
        disk.setdefault(p, ({}, 0))[0][k] = INIT[k]
    return disk


class Db:
    def __init__(self, disk: dict, log: list | None = None):
        self.disk = disk
        self.log: list[Rec] = list(log or [])
        self.tail: list[Rec] = []
        self.buf: dict[str, list] = {}
        self.last: dict[int, int] = {}  # txn -> lastLSN
        self.undo_next: dict[int, int] = {}  # txns that roll back -> next record to undo
        self.locks: dict[str, int] = {}  # record lock: key -> txn
        self.chain: dict[str, list[int]] = {}  # page -> LSNs of its records (restart only)
        self.need_redo: set[str] = set()
        self.losers: set[int] = set()
        self.redone: list[str] = []  # pages redone since the restart, in order

    # ------------------------------------------------------------ storage
    def rec(self, lsn: int) -> Rec:
        i = lsn - 1
        return self.log[i] if i < len(self.log) else self.tail[i - len(self.log)]

    def _append(self, **kw) -> Rec:
        r = Rec(lsn=len(self.log) + len(self.tail) + 1, **kw)
        self.tail.append(r)
        if r.kind != "end":
            self.last[r.txn] = r.lsn
        return r

    def flush_log(self) -> None:
        self.log.extend(self.tail)
        self.tail = []

    def flush_page(self, p: str) -> None:
        if p in self.buf:
            if self.buf[p][1] > len(self.log):  # WAL rule
                self.flush_log()
            self.disk[p] = (dict(self.buf[p][0]), self.buf[p][1])

    def crash(self) -> "Db":
        return Db(self.disk, self.log)

    def fix(self, p: str) -> list:
        """Bring page p into the buffer, and redo it first if it needs redo."""
        if p not in self.buf:
            vals, lsn = self.disk[p]
            self.buf[p] = [dict(vals), lsn]
        if p in self.need_redo:  # @line L5
            pg = self.buf[p]
            for lsn in self.chain[p]:  # @line L6
                r = self.rec(lsn)
                if pg[1] < r.lsn:  # @line L7
                    pg[0][r.key], pg[1] = r.after, r.lsn  # @line L7
            self.need_redo.discard(p)  # @line L8
            self.redone.append(p)
        return self.buf[p]

    # ------------------------------------------------------------ transactions
    def begin(self, txn: int) -> None:
        self._append(kind="begin", txn=txn)

    def lock(self, txn: int, key: str) -> bool:
        """Take the lock on key for txn. A loser's lock is freed by rolling the
        loser back at once; a lock of another live transaction is a conflict."""
        holder = self.locks.get(key, txn)
        if holder in self.losers:  # @line L9
            self.rollback(holder)  # @line L9
            holder = txn
        if holder != txn:
            return False
        self.locks[key] = txn  # @line L10
        return True

    def read(self, txn: int, key: str) -> int | None:
        if not self.lock(txn, key):
            return None
        return self.fix(PAGE_OF[key])[0][key]

    def write(self, txn: int, key: str, value: int) -> bool:
        if not self.lock(txn, key):
            return False
        pg = self.fix(PAGE_OF[key])
        r = self._append(kind="update", txn=txn, prev=self.last[txn], page=PAGE_OF[key],
                         key=key, before=pg[0][key], after=value)
        pg[0][key], pg[1] = value, r.lsn
        return True

    def _release(self, txn: int) -> None:
        for k in [k for k, t in self.locks.items() if t == txn]:
            del self.locks[k]

    def commit(self, txn: int) -> None:
        self._append(kind="commit", txn=txn, prev=self.last[txn])
        self.flush_log()
        self._append(kind="end", txn=txn, prev=self.last[txn])
        self._release(txn)
        del self.last[txn]

    def abort(self, txn: int) -> None:
        r = self._append(kind="abort", txn=txn, prev=self.last[txn])
        self.undo_next[txn] = r.prev

    def undo_step(self, txn: int) -> None:
        """Undo one update of txn with a CLR, or end its rollback."""
        nxt = self.undo_next[txn]
        if nxt:
            r = self.rec(nxt)  # @line L11
            if r.kind == "clr":
                self.undo_next[txn] = r.undo_next  # @line L11
                return
            if r.kind == "update":
                pg = self.fix(r.page)  # @line L12
                c = self._append(kind="clr", txn=txn, prev=self.last[txn], page=r.page, key=r.key,
                                 before=pg[0][r.key], after=r.before, undo_next=r.prev)  # @line L12
                pg[0][r.key], pg[1] = r.before, c.lsn  # @line L12
            self.undo_next[txn] = r.prev  # @line L11
            return
        self._append(kind="end", txn=txn, prev=self.last[txn])  # @line L13
        del self.undo_next[txn]
        del self.last[txn]
        self.losers.discard(txn)
        self._release(txn)  # @line L13

    def rollback(self, txn: int) -> None:
        while txn in self.undo_next:  # @line L16
            self.undo_step(txn)  # @line L16

    # ------------------------------------------------------------ restart
    def restart(self) -> None:
        """Log analysis. After it the system accepts new transactions."""
        won: set[int] = set()
        for r in self.log:  # @line L1
            if r.kind == "commit":
                won.add(r.txn)
                self.last[r.txn] = r.lsn
            elif r.kind == "end":
                won.discard(r.txn)
                self.last.pop(r.txn, None)
                self.undo_next.pop(r.txn, None)
            else:
                self.last[r.txn] = r.lsn  # @line L1
                self.undo_next[r.txn] = r.undo_next if r.kind == "clr" else r.lsn  # @line L1
            if r.kind in ("update", "clr"):
                self.chain.setdefault(r.page, []).append(r.lsn)  # @line L2
                self.need_redo.add(r.page)  # @line L2
        for t in sorted(won):
            self._append(kind="end", txn=t, prev=self.last.pop(t))  # @line L4
            del self.undo_next[t]
        self.losers = set(self.undo_next)
        for t in sorted(self.losers):  # @line L3
            nxt = self.undo_next[t]
            while nxt:  # walk the chain of t; lock each record it changed
                r = self.rec(nxt)
                if r.kind == "update":
                    self.locks[r.key] = t  # @line L3
                nxt = r.undo_next if r.kind == "clr" else r.prev
        # from here on new transactions run

    def background_step(self) -> bool:
        """One unit of the remaining restart work. Returns False when none is left."""
        if self.need_redo:
            self.fix(min(self.need_redo))  # @line L14
            return True
        if self.losers:
            t = max(self.losers, key=lambda t: self.undo_next[t])  # @line L15
            self.undo_step(t)  # @line L15
            return True
        return False

    def value(self, key: str) -> int:
        return self.fix(PAGE_OF[key])[0][key]
