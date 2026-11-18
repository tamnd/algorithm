# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fuzzy-checkpoint/. The authors are listed in prov/EF79FV.jsonl.

"""A fuzzy checkpoint whose two tables are copied at different times, and the
analysis pass that merges them with the log.

Model: each page holds one integer. Stable storage is the disk (page ->
(pageLSN, value)), the stable log and the master record. Volatile storage is
the buffer (dirty pages only), the log tail, the transaction table (ATT) and
the dirty page table (DPT). The buffer policy is steal and no-force with the
WAL rule. Rollback, in normal processing and in recovery, writes compensation
log records (CLRs). The LSN of a record is its index in the log plus 1.

A checkpoint is four separate steps, and any other step can run between them:
ckpt_begin (append BEGIN_CHECKPOINT), copy_att, copy_dpt (in either order) and
ckpt_end (append END_CHECKPOINT with both copies, force it, set the master).
No page is written by a checkpoint.

recovery() is a generator that yields after each step, so that a test can
crash inside recovery. Redo and undo are those of ARIES.
"""

from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Rec:
    lsn: int
    kind: str  # BEGIN, UPDATE, CLR, COMMIT, ABORT, END, BEGIN_CHECKPOINT, END_CHECKPOINT
    txn: int = 0
    prev: int = 0  # prevLSN, 0 for the first record of a transaction
    page: str = ""
    before: int = 0
    after: int = 0
    undo_next: int = 0  # CLR only
    att: tuple = ()  # END_CHECKPOINT: (txn, status, lastLSN, undoNext) for each entry
    dpt: tuple = ()  # END_CHECKPOINT: (page, recLSN) for each entry


TXN_KINDS = ("BEGIN", "UPDATE", "CLR", "COMMIT", "ABORT")


class Db:
    def __init__(self, disk: dict, log: list | None = None, master: int = 0) -> None:
        self.disk = {p: (v if isinstance(v, tuple) else (0, v)) for p, v in disk.items()}
        self.log: list[Rec] = list(log or [])
        self.master = master
        self.tail: list[Rec] = []
        self.buf: dict[str, list] = {}  # dirty page -> [pageLSN, value]
        self.att: dict[int, list] = {}  # txn -> [status, lastLSN, undoNext]
        self.dpt: dict[str, int] = {}  # dirty page -> recLSN
        self.ck: dict = {}  # the checkpoint in progress
        self.stats = {"analysis": 0, "redo": 0, "undo": 0, "page_reads": 0}

    # ---- log, buffer, disk ------------------------------------------------
    def rec(self, lsn: int) -> Rec:
        return self.log[lsn - 1] if lsn <= len(self.log) else self.tail[lsn - len(self.log) - 1]

    def _append(self, **fields) -> Rec:
        r = Rec(lsn=len(self.log) + len(self.tail) + 1, **fields)
        self.tail.append(r)
        return r

    def flush_log(self, upto: int | None = None) -> None:
        n = len(self.tail) if upto is None else max(0, upto - len(self.log))
        self.log += self.tail[:n]
        self.tail = self.tail[n:]

    def value(self, p: str) -> int:
        return self.buf[p][1] if p in self.buf else self.disk[p][1]

    def page_lsn(self, p: str) -> int:
        return self.buf[p][0] if p in self.buf else self.disk[p][0]

    def _change(self, p: str, lsn: int, v: int) -> None:
        if p not in self.buf:
            self.dpt[p] = lsn  # the first change since the page was clean
        self.buf[p] = [lsn, v]

    def flush_page(self, p: str) -> None:
        if p not in self.buf:
            return
        lsn, v = self.buf.pop(p)
        self.flush_log(lsn)  # the WAL rule
        self.disk[p] = (lsn, v)
        del self.dpt[p]

    def crash(self) -> "Db":
        return Db(dict(self.disk), list(self.log), self.master)

    def _chain(self, lsn: int) -> int:
        """Normalize a chain pointer: a BEGIN record ends the chain."""
        return 0 if lsn == 0 or self.rec(lsn).kind == "BEGIN" else lsn

    # ---- normal processing ------------------------------------------------
    def begin(self, t: int) -> None:
        r = self._append(kind="BEGIN", txn=t)
        self.att[t] = ["active", r.lsn, 0]

    def update(self, t: int, p: str, w: int) -> None:
        r = self._append(kind="UPDATE", txn=t, prev=self.att[t][1], page=p, before=self.value(p), after=w)
        self._change(p, r.lsn, w)
        self.att[t][1:] = [r.lsn, r.lsn]

    def commit(self, t: int) -> None:
        r = self._append(kind="COMMIT", txn=t, prev=self.att[t][1])
        self.flush_log(r.lsn)
        self.att[t][:2] = ["committed", r.lsn]

    def end(self, t: int) -> None:
        self._append(kind="END", txn=t, prev=self.att[t][1])
        del self.att[t]

    def abort(self, t: int) -> None:
        r = self._append(kind="ABORT", txn=t, prev=self.att[t][1])
        self.att[t][:2] = ["aborting", r.lsn]

    def undo_step(self, t: int) -> bool:
        """Undo the next update of t, or end t. Return True when t has ended."""
        status, last, nxt = self.att[t]
        if nxt == 0:
            self.end(t)
            return True
        r = self.rec(nxt)
        if r.kind == "UPDATE":
            c = self._append(kind="CLR", txn=t, prev=last, page=r.page, after=r.before, undo_next=self._chain(r.prev))
            self._change(r.page, c.lsn, r.before)
            self.att[t][1:] = [c.lsn, c.undo_next]
        elif r.kind == "CLR":
            self.att[t][2] = r.undo_next
        else:  # ABORT
            self.att[t][2] = self._chain(r.prev)
        return False

    # ---- the fuzzy checkpoint ---------------------------------------------
    def ckpt_begin(self) -> None:
        b = self._append(kind="BEGIN_CHECKPOINT")  # @line L1
        self.ck = {"b": b.lsn}

    def copy_att(self) -> None:
        self.ck["att"] = tuple((t, *e) for t, e in sorted(self.att.items()))  # @line L2

    def copy_dpt(self) -> None:
        self.ck["dpt"] = tuple(sorted(self.dpt.items()))  # @line L3

    def ckpt_end(self) -> None:
        e = self._append(kind="END_CHECKPOINT", att=self.ck["att"], dpt=self.ck["dpt"])  # @line L4
        self.flush_log(e.lsn)  # @line L5
        self.master = self.ck["b"]  # @line L6
        self.ck = {}

    # ---- recovery -----------------------------------------------------------
    def merge_checkpoint(self, att: dict, dpt: dict, ended: set, r: Rec) -> None:
        for t, status, last, nxt in r.att:  # @line L13
            if t not in att and t not in ended:  # @line L13
                att[t] = [status, last, nxt]
        for p, rec_lsn in r.dpt:  # @line L14
            dpt[p] = min(dpt.get(p, rec_lsn), rec_lsn)  # @line L14

    def analysis(self, start: int | None = None, use_checkpoints: bool = True) -> tuple[dict, dict, int]:
        """Rebuild the ATT and the DPT from the stable log. Return them and the
        LSN where redo starts. The committed transactions are left in the ATT
        with status committed."""
        if start is None:
            start = self.master or 1  # @line L7
        att: dict[int, list] = {}  # @line L7
        dpt: dict[str, int] = {}  # @line L7
        ended: set[int] = set()  # @line L7
        for r in self.log[start - 1 :]:  # @line L8
            self.stats["analysis"] += 1
            if r.kind in TXN_KINDS:  # @line L9
                e = att.setdefault(r.txn, ["active", 0, 0])
                e[1] = r.lsn
                if r.kind in ("UPDATE",):
                    e[2] = r.lsn
                elif r.kind == "CLR":
                    e[2] = r.undo_next
                elif r.kind == "ABORT":
                    e[0], e[2] = "aborting", self._chain(r.prev)
                elif r.kind == "COMMIT":
                    e[0] = "committed"
            if r.kind in ("UPDATE", "CLR") and r.page not in dpt:  # @line L10
                dpt[r.page] = r.lsn  # @line L10
            if r.kind == "END":  # @line L11
                att.pop(r.txn, None)  # @line L11
                ended.add(r.txn)  # @line L11
            if r.kind == "END_CHECKPOINT" and use_checkpoints:  # @line L12
                self.merge_checkpoint(att, dpt, ended, r)
        redo_lsn = min(dpt.values(), default=len(self.log) + 1)  # @line L16
        return att, dpt, redo_lsn

    def recovery(self) -> Iterator[str]:
        self.buf, self.tail, self.att, self.dpt, self.ck = {}, [], {}, {}, {}
        self.stats = {"analysis": 0, "redo": 0, "undo": 0, "page_reads": 0}
        att, dpt, redo_lsn = self.analysis()
        for t in sorted(att):  # @line L15
            if att[t][0] == "committed":
                self._append(kind="END", txn=t, prev=att[t][1])  # @line L15
                del att[t]
        self.att = att
        yield "analysis"
        fetched: set[str] = set()
        for r in self.log[redo_lsn - 1 :]:  # @line L17: redo, repeating history
            self.stats["redo"] += 1
            if r.kind not in ("UPDATE", "CLR") or r.page not in dpt or r.lsn < dpt[r.page]:
                continue
            if r.page not in fetched:
                fetched.add(r.page)
                self.stats["page_reads"] += 1
            if self.page_lsn(r.page) < r.lsn:
                self._change(r.page, r.lsn, r.after)
                yield "redo"
        while self.att:  # @line L18: undo the losers, largest undoNext first
            t = max(self.att, key=lambda u: self.att[u][2])
            if self.att[t][2]:
                self.stats["undo"] += 1
            self.undo_step(t)
            yield "undo"
        self.flush_log()  # @line L19
        yield "flush"

    def recover(self) -> None:
        for _ in self.recovery():
            pass

    def state(self) -> dict[str, int]:
        return {p: self.value(p) for p in sorted(self.disk)}
