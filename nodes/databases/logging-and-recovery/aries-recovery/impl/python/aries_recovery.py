# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aries-recovery/. The authors are listed in prov/YSPCY5.jsonl.

"""ARIES on a simulated disk and log.

Model: a page holds several keys and one page_lsn, so two transactions may
change the same page (record-level locking). Stable storage is the disk
(page -> (values, page_lsn)), the stable log and the master record (the LSN of
the begin record of the last complete checkpoint). Volatile storage is the
buffer pool, the log tail, the transaction table (ATT) and the dirty page table
(DPT). The buffer policy is steal and no-force; flush_page obeys the WAL rule.
Each public method is one atomic step; recovery_steps yields after each step,
so a test can crash anywhere, also inside recovery.
"""

from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Rec:
    lsn: int
    kind: str  # update, clr, commit, abort, end, begin_ckpt, end_ckpt
    txn: int = 0
    prev: int = 0  # prevLSN of the same transaction, 0 for none
    page: str = ""
    key: str = ""
    before: int = 0  # update: the old value (undo information)
    after: int = 0  # update: the new value; clr: the value written by the undo
    undo_next: int = 0  # clr: the next record of the transaction to undo
    undone: int = 0  # clr: the update it compensates (only used by checks)
    att: tuple = ()  # end_ckpt: (txn, status, last_lsn, undo_next) tuples
    dpt: tuple = ()  # end_ckpt: (page, rec_lsn) pairs


Disk = dict[str, tuple[dict[str, int], int]]


class Aries:
    """A database with ARIES logging and recovery. Cost: O(1) per update and per
    undo step (plus one log flush per commit and per page write)."""

    def __init__(self, disk: Disk, log: list[Rec] | None = None, master: int = 0) -> None:
        self.disk: Disk = {p: (dict(v), lsn) for p, (v, lsn) in disk.items()}
        self.log: list[Rec] = list(log or [])  # the stable log
        self.master = master
        self.tail: list[Rec] = []
        self.index = {r.lsn: r for r in self.log}
        self.next_lsn = 1 + max(self.index, default=0)
        self.buf: dict[str, list] = {}  # page -> [values, page_lsn]
        self.att: dict[int, list] = {}  # txn -> [status, last_lsn, undo_next]
        self.dpt: dict[str, int] = {}  # page -> rec_lsn
        self.acked: set[int] = set()

    # ---- log and buffer -------------------------------------------------
    def _append(self, **fields) -> Rec:
        r = Rec(lsn=self.next_lsn, **fields)
        self.next_lsn += 1
        self.tail.append(r)
        self.index[r.lsn] = r
        return r

    def flush_log(self, upto: int) -> None:
        keep = []
        for r in self.tail:
            (self.log if r.lsn <= upto else keep).append(r)
        self.tail = keep

    def _fetch(self, page: str) -> list:
        if page not in self.buf:
            vals, plsn = self.disk[page]
            self.buf[page] = [dict(vals), plsn]
        return self.buf[page]

    def flush_page(self, page: str) -> None:
        """Steal or clean a page; the WAL rule flushes the log first."""
        p = self.buf.pop(page)
        self.flush_log(p[1])
        self.disk[page] = (dict(p[0]), p[1])
        self.dpt.pop(page, None)

    def read(self, page: str, key: str) -> int:
        return self._fetch(page)[0][key]

    # ---- normal processing ----------------------------------------------
    def update(self, t: int, page: str, key: str, v: int) -> None:
        e = self.att.setdefault(t, ["U", 0, 0])
        p = self._fetch(page)
        r = self._append(kind="update", txn=t, prev=e[1], page=page, key=key, before=p[0][key], after=v)
        p[0][key], p[1] = v, r.lsn
        self.dpt.setdefault(page, r.lsn)
        e[1] = e[2] = r.lsn

    def commit(self, t: int) -> None:
        e = self.att.setdefault(t, ["U", 0, 0])
        r = self._append(kind="commit", txn=t, prev=e[1])
        self.flush_log(r.lsn)
        self.acked.add(t)
        e[0], e[1] = "C", r.lsn
        self._append(kind="end", txn=t, prev=r.lsn)
        del self.att[t]

    def begin_abort(self, t: int) -> None:
        e = self.att.setdefault(t, ["U", 0, 0])
        r = self._append(kind="abort", txn=t, prev=e[1])
        e[1] = r.lsn

    def savepoint(self, t: int) -> int:
        return self.att.setdefault(t, ["U", 0, 0])[2]

    def undo_step(self, t: int, finish: bool = True) -> bool:
        """Undo the next record of t. Returns True when t has nothing left to
        undo; with finish, an end record is then written and t leaves the ATT.
        A partial rollback passes finish=False."""
        e = self.att[t]
        if e[2] == 0:
            if finish:
                self._append(kind="end", txn=t, prev=e[1])
                del self.att[t]
            return True
        r = self.index[e[2]]
        if r.kind == "update":  # @line L18
            p = self._fetch(r.page)
            c = self._append(kind="clr", txn=t, prev=e[1], page=r.page, key=r.key,
                             after=r.before, undo_next=r.prev, undone=r.lsn)  # @line L19
            p[0][r.key], p[1] = r.before, c.lsn  # @line L20
            self.dpt.setdefault(r.page, c.lsn)
            e[1], e[2] = c.lsn, r.prev
        elif r.kind == "clr":
            e[2] = r.undo_next  # @line L21
        else:
            e[2] = r.prev
        if e[2] == 0:  # @line L22
            if finish:
                self._append(kind="end", txn=t, prev=e[1])
                del self.att[t]
            return True
        return False

    def rollback_to(self, t: int, save: int) -> None:
        """Partial rollback: undo the updates of t made after the savepoint.
        The transaction stays active."""
        while t in self.att and self.att[t][2] > save:
            self.undo_step(t, finish=False)

    def begin_checkpoint(self) -> int:
        return self._append(kind="begin_ckpt").lsn

    def end_checkpoint(self, begin_lsn: int) -> None:
        """Fuzzy checkpoint: copy the two tables into the log; no page is written."""
        att = tuple((t, e[0], e[1], e[2]) for t, e in sorted(self.att.items()))
        dpt = tuple(sorted(self.dpt.items()))
        r = self._append(kind="end_ckpt", att=att, dpt=dpt)
        self.flush_log(r.lsn)
        self.master = begin_lsn

    def current(self) -> dict[tuple[str, str], int]:
        """The database as transactions see it: buffered pages over the disk."""
        out = state(self.disk)
        out.update({(p, k): v for p, (vals, _) in self.buf.items() for k, v in vals.items()})
        return out

    def crash(self) -> tuple[Disk, list[Rec], int]:
        return {p: (dict(v), lsn) for p, (v, lsn) in self.disk.items()}, list(self.log), self.master

    # ---- restart recovery -----------------------------------------------
    def recovery_steps(self, flushes=None) -> Iterator[str]:
        """Run ARIES restart recovery on a fresh instance built from stable
        storage. Yields after each atomic step. `flushes`, if given, is a
        random.Random that writes some pages and log records early, to test
        crashes inside recovery."""
        # Analysis
        start = self.master if self.master else 1  # @line L1
        att, dpt = self.att, self.dpt
        for r in self.log:  # @line L2
            if r.lsn < start:
                continue
            if r.kind in ("update", "clr"):  # @line L3
                e = att.setdefault(r.txn, ["U", 0, 0])
                e[1] = r.lsn
                e[2] = r.lsn if r.kind == "update" else r.undo_next
                dpt.setdefault(r.page, r.lsn)  # @line L4
            elif r.kind in ("commit", "abort"):
                e = att.setdefault(r.txn, ["U", 0, 0])
                e[0] = "C" if r.kind == "commit" else e[0]
                e[1] = r.lsn
            elif r.kind == "end":  # @line L5
                att.pop(r.txn, None)
            elif r.kind == "end_ckpt":  # @line L6
                att.clear()
                att.update({t: [s, last, un] for t, s, last, un in r.att})
                dpt.clear()
                dpt.update(dict(r.dpt))
        for t in sorted(att):  # @line L7
            if att[t][0] == "C":
                self._append(kind="end", txn=t, prev=att[t][1])
                del att[t]
        yield "analysis"
        # Redo: repeat history from the smallest rec_lsn
        # Redo decides with a copy of the analysis DPT; the live DPT keeps
        # following page writes, which may happen during redo.
        redo_dpt = dict(dpt)
        if redo_dpt:
            redo_lsn = min(redo_dpt.values())  # @line L8
            for r in list(self.log):  # @line L9
                if r.lsn < redo_lsn or r.kind not in ("update", "clr"):
                    continue
                if r.page in redo_dpt and r.lsn >= redo_dpt[r.page]:  # @line L10
                    p = self._fetch(r.page)
                    if p[1] < r.lsn:  # @line L11
                        p[0][r.key], p[1] = r.after, r.lsn  # @line L12
                        dpt.setdefault(r.page, r.lsn)
                yield "redo"
                if flushes is not None:
                    self._random_flush(flushes)
        # Undo: all losers together, largest LSN first
        while self.att:  # @line L13
            t = max(self.att, key=lambda u: self.att[u][2])  # @line L14
            if self.att[t][2] == 0:
                self._append(kind="end", txn=t, prev=self.att[t][1])
                del self.att[t]
                continue
            self.undo_step(t)  # @line L15
            yield "undo"
            if flushes is not None:
                self._random_flush(flushes)
        self.flush_log(self.next_lsn)  # @line L16
        b = self.begin_checkpoint()  # @line L17
        self.end_checkpoint(b)
        yield "done"

    def _random_flush(self, rng) -> None:
        c = rng.random()
        if c < 0.3 and self.buf:
            self.flush_page(rng.choice(sorted(self.buf)))
        elif c < 0.5:
            self.flush_log(self.next_lsn)

    def recover(self, stop_after: int | None = None, flushes=None) -> bool:
        """Run recovery; with stop_after = k, stop (to crash) after k steps.
        Returns True when recovery finished."""
        for i, _ in enumerate(self.recovery_steps(flushes)):
            if stop_after is not None and i + 1 >= stop_after:
                return False
        return True


def state(disk: Disk) -> dict[tuple[str, str], int]:
    """The values of a disk, keyed by (page, key)."""
    return {(p, k): v for p, (vals, _) in disk.items() for k, v in vals.items()}
