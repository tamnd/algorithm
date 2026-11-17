# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/checkpointing/. The authors are listed in prov/3HY3MZ.jsonl.

"""Checkpoints for a write-ahead-logging database, on a simulated disk and log.

Each item is its own page with a page_lsn. The buffer policy is steal and
no-force; flush_page obeys the WAL rule and commit forces the log. Three
checkpoints are offered: consistent (quiescent), action consistent (sharp,
all dirty pages written, transactions keep running) and fuzzy (only the
tables are written). Restart starts at the checkpoint named by the master
record, and with master = 0 it reads the whole log, which gives the reference
result.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rec:
    lsn: int
    kind: str  # update, commit, abort, begin_ckpt, end_ckpt, ckpt
    txn: int = 0
    prev: int = 0
    item: str = ""
    before: int = 0
    after: int = 0
    att: tuple = ()  # (txn, last_lsn) pairs
    dpt: tuple = ()  # (item, rec_lsn) pairs


Disk = dict[str, tuple[int, int]]  # item -> (value, page_lsn)


class Db:
    def __init__(self, disk: Disk, log: list[Rec] | None = None, master: int = 0) -> None:
        self.disk = dict(disk)
        self.log = list(log or [])  # stable log
        self.tail: list[Rec] = []
        self.master = master
        self.next_lsn = 1 + (self.log[-1].lsn if self.log else 0)
        self.buf: dict[str, list] = {}  # item -> [value, page_lsn]
        self.att: dict[int, int] = {}  # txn -> last_lsn
        self.dpt: dict[str, int] = {}  # item -> rec_lsn
        self.acked: set[int] = set()
        self.scanned = 0  # log records read by the last restart

    def _append(self, **f) -> Rec:
        r = Rec(lsn=self.next_lsn, **f)
        self.next_lsn += 1
        self.tail.append(r)
        return r

    def flush_log(self, upto: int) -> None:
        self.log += [r for r in self.tail if r.lsn <= upto]
        self.tail = [r for r in self.tail if r.lsn > upto]

    def _fetch(self, x: str) -> list:
        if x not in self.buf:
            self.buf[x] = list(self.disk[x])
        return self.buf[x]

    def flush_page(self, x: str) -> None:
        v, plsn = self.buf.pop(x)
        self.flush_log(plsn)  # the WAL rule
        self.disk[x] = (v, plsn)
        self.dpt.pop(x, None)

    def update(self, t: int, x: str, v: int) -> None:
        p = self._fetch(x)
        r = self._append(kind="update", txn=t, prev=self.att.get(t, 0), item=x, before=p[0], after=v)
        p[0], p[1] = v, r.lsn
        self.dpt.setdefault(x, r.lsn)
        self.att[t] = r.lsn

    def commit(self, t: int) -> None:
        r = self._append(kind="commit", txn=t, prev=self.att.get(t, 0))
        self.flush_log(r.lsn)  # the commit rule
        self.acked.add(t)
        self.att.pop(t, None)

    def abort(self, t: int) -> None:
        """Roll back by logging restoring updates, newest first, then abort."""
        for r in self._chain(self.att.get(t, 0)):
            self.update(t, r.item, r.before)
        self._append(kind="abort", txn=t, prev=self.att.get(t, 0))
        self.att.pop(t, None)

    def _records(self) -> dict[int, Rec]:
        return {r.lsn: r for r in self.log + self.tail}

    def _chain(self, lsn: int) -> list[Rec]:
        recs, out = self._records(), []
        while lsn:
            out.append(recs[lsn])
            lsn = recs[lsn].prev
        return out

    # ---- checkpoints ----------------------------------------------------
    def fuzzy_begin(self) -> int:
        return self._append(kind="begin_ckpt").lsn  # @line L1

    def fuzzy_end(self, begin_lsn: int) -> None:
        att = tuple(sorted(self.att.items()))  # @line L2
        dpt = tuple(sorted(self.dpt.items()))
        e = self._append(kind="end_ckpt", att=att, dpt=dpt)  # @line L3
        self.flush_log(e.lsn)  # @line L4
        self.master = begin_lsn  # @line L5

    def consistent_checkpoint(self) -> None:
        """Call only when no transaction is active (the caller quiesces)."""
        assert not self.att  # @line L6
        for x in sorted(self.buf):  # @line L7
            self.flush_page(x)
        c = self._append(kind="ckpt")  # @line L8
        self.flush_log(c.lsn)
        self.master = c.lsn  # @line L9

    def sharp_checkpoint(self) -> None:
        """Action consistent: write all dirty pages, record the active
        transactions, and do not wait for them."""
        for x in sorted(self.buf):
            self.flush_page(x)
        c = self._append(kind="ckpt", att=tuple(sorted(self.att.items())))
        self.flush_log(c.lsn)
        self.master = c.lsn

    # ---- restart --------------------------------------------------------
    def crash(self) -> tuple[Disk, list[Rec], int]:
        return dict(self.disk), list(self.log), self.master

    def recover(self, redo_from_checkpoint: bool = False) -> None:
        """Restart from the master record. redo_from_checkpoint=True is the
        wrong rule that starts redo at the checkpoint, for the tests."""
        start = self.master or 1  # @line L10
        att, dpt = {}, {}
        for r in self.log:
            if r.lsn < start:
                continue
            self.scanned += 1
            if r.kind == "update":
                att[r.txn] = r.lsn
                dpt.setdefault(r.item, r.lsn)
            elif r.kind in ("commit", "abort"):
                att.pop(r.txn, None)
            elif r.kind in ("end_ckpt", "ckpt"):
                att, dpt = dict(r.att), dict(r.dpt)
        redo = min(dpt.values(), default=None)  # @line L11
        if redo is not None and redo_from_checkpoint:
            redo = max(redo, start)
        for r in self.log:
            if redo is None or r.lsn < redo or r.kind != "update":
                continue
            if r.lsn < start:
                self.scanned += 1
            if r.item in dpt and r.lsn >= dpt[r.item]:
                p = self._fetch(r.item)
                if p[1] < r.lsn:
                    p[0], p[1] = r.after, r.lsn
        losers = sorted((r for t in att for r in self._chain(att[t])), key=lambda r: -r.lsn)  # @line L12
        self.scanned += sum(1 for r in losers if r.lsn < start)
        for r in losers:
            self._fetch(r.item)[0] = r.before
        for x in sorted({r.item for r in losers}):
            self.flush_page(x)
        for t in sorted(att):
            self._append(kind="abort", txn=t, prev=att[t])
        self.flush_log(self.next_lsn)

    def current(self) -> dict[str, int]:
        out = {x: v for x, (v, _) in self.disk.items()}
        out.update({x: p[0] for x, p in self.buf.items()})
        return out
