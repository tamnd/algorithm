# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undo-redo-logging/. The authors are listed in prov/E549PJ.jsonl.

"""Undo/redo logging with the record forms of Garcia-Molina, Ullman and Widom.

Model: each database item X is one page that holds one integer. Stable storage
is the disk (item -> (pageLSN, value)) and the stable log. Volatile storage is
the buffer (the dirty items only), the log tail and the list of updates of each
active transaction. The buffer policy is steal and no-force: output may write a
dirty item at any time, and it obeys rule UR1 (the update record first).

The LSN of a record is its index in the log plus 1. Record kinds and the forms
of the book: START is <START T>, UPDATE is <T, X, v, w>, COMMIT is <COMMIT T>,
ABORT is <ABORT T>, START_CKPT is <START CKPT (T_1, ..., T_k)> and END_CKPT is
<END CKPT>. Each public method is one atomic step. recovery() is a generator
that yields after each step, so that a test can crash inside recovery.
"""

from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Rec:
    lsn: int
    kind: str  # START, UPDATE, COMMIT, ABORT, START_CKPT, END_CKPT
    txn: int = 0
    item: str = ""
    old: int = 0  # v, the before image (undo information)
    new: int = 0  # w, the after image (redo information)
    active: tuple = ()  # START_CKPT: the active transactions T_1, ..., T_k


class Db:
    """A database with undo/redo logging. Each step costs O(1), except a log
    flush (the records in the tail) and a checkpoint (the dirty items)."""

    def __init__(self, disk: dict, log: list | None = None) -> None:
        # disk maps an item to its value, or to a pair (pageLSN, value)
        self.disk = {x: (v if isinstance(v, tuple) else (0, v)) for x, v in disk.items()}
        self.log: list[Rec] = list(log or [])  # the stable log
        self.tail: list[Rec] = []  # the log records not yet on disk
        self.buf: dict[str, list] = {}  # dirty item -> [pageLSN, value]
        self.updates: dict[int, list[Rec]] = {}  # active T -> its update records
        self.read_count = 0  # log records read by the last recovery

    # ---- log and buffer -------------------------------------------------
    def _append(self, **fields) -> Rec:
        r = Rec(lsn=len(self.log) + len(self.tail) + 1, **fields)
        self.tail.append(r)
        return r

    def flush_log(self, upto: int | None = None) -> None:
        keep = []
        for r in self.tail:
            (self.log if upto is None or r.lsn <= upto else keep).append(r)
        self.tail = keep

    def flushed_lsn(self) -> int:
        return len(self.log)

    def value(self, x: str) -> int:
        return self.buf[x][1] if x in self.buf else self.disk[x][1]

    def _set(self, x: str, lsn: int, v: int) -> None:
        self.buf[x] = [lsn, v]

    def output(self, x: str) -> None:
        """Write a dirty item to disk (steal or clean)."""
        if x not in self.buf:
            return
        lsn, v = self.buf.pop(x)
        self.flush_log(lsn)  # @line L3: rule UR1, the update record first
        assert lsn <= self.flushed_lsn()
        self.disk[x] = (lsn, v)  # @line L4

    def crash(self) -> "Db":
        """Lose the buffer, the log tail and every volatile table."""
        return Db(dict(self.disk), list(self.log))

    # ---- normal processing ----------------------------------------------
    def start(self, t: int) -> None:
        self._append(kind="START", txn=t)
        self.updates[t] = []

    def write(self, t: int, x: str, w: int) -> None:
        v = self.value(x)  # @line L1
        r = self._append(kind="UPDATE", txn=t, item=x, old=v, new=w)  # @line L2
        self._set(x, r.lsn, w)  # @line L2
        self.updates[t].append(r)

    def commit(self, t: int) -> None:
        r = self._append(kind="COMMIT", txn=t)  # @line L5
        self.flush_log(r.lsn)  # @line L5: the commit returns after this
        del self.updates[t]

    def abort(self, t: int) -> None:
        for r in reversed(self.updates.pop(t)):  # @line L6: newest first
            lsn = self.buf[r.item][0] if r.item in self.buf else self.disk[r.item][0]
            self._set(r.item, lsn, r.old)  # @line L6
        self._append(kind="ABORT", txn=t)  # @line L7

    def ckpt_start(self) -> None:
        r = self._append(kind="START_CKPT", active=tuple(sorted(self.updates)))  # @line L8
        self.flush_log(r.lsn)  # @line L8

    def ckpt_flush(self) -> None:
        for x in sorted(self.buf):  # @line L9
            self.output(x)  # @line L9

    def ckpt_end(self) -> None:
        r = self._append(kind="END_CKPT")  # @line L10
        self.flush_log(r.lsn)  # @line L10

    # ---- recovery ---------------------------------------------------------
    def last_checkpoint(self) -> tuple[int, tuple]:
        """The LSN s and the list of the START CKPT that matches the last
        END CKPT of the stable log, or (0, ()) if there is none."""
        seen_end = False
        for r in reversed(self.log):
            if r.kind == "END_CKPT":
                seen_end = True
            elif r.kind == "START_CKPT" and seen_end:
                return r.lsn, r.active
        return 0, ()

    def recovery(self, write_aborts: bool = True) -> Iterator[str]:
        self.buf, self.tail, self.updates = {}, [], {}
        s, listed = self.last_checkpoint()  # @line L11
        cand = set(listed) | {r.txn for r in self.log[s:] if r.kind == "START"}  # @line L12
        committed: set[int] = set()  # @line L12
        open_ = set(listed)  # @line L12
        self.read_count = 0
        for r in reversed(self.log):  # @line L13: the undo pass
            if r.lsn < s and not open_:  # @line L14
                break
            self.read_count += 1
            if r.kind == "COMMIT":  # @line L15
                committed.add(r.txn)
            elif r.kind == "START":  # @line L16
                open_.discard(r.txn)
            elif r.kind == "UPDATE" and r.txn in cand and r.txn not in committed:  # @line L17
                self._set(r.item, r.lsn, r.old)
                yield "undo"
        for r in self.log[s:]:  # @line L18: the redo pass
            self.read_count += 1
            if r.kind == "UPDATE" and r.txn in committed:  # @line L19
                self._set(r.item, r.lsn, r.new)
                yield "redo"
        for x in sorted(self.buf):  # @line L20
            self.output(x)
            yield "output"
        if write_aborts:
            for t in sorted(cand - committed):  # @line L21
                self._append(kind="ABORT", txn=t)
            self.flush_log()  # @line L21
            yield "abort records"

    def recover(self) -> None:
        for _ in self.recovery():
            pass

    def state(self) -> dict[str, int]:
        return {x: self.value(x) for x in sorted(self.disk)}
