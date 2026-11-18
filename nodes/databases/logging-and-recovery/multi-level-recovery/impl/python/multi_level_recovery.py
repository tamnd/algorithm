# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-level-recovery/. The authors are listed in prov/7Q7BG3.jsonl.

"""Two-level transaction recovery on a simulated disk and log.

Level 1 operations are ADD(x, d) on counters. Each one is a subtransaction of
level 0 page writes: x := x + d, then t := t + d (t holds the total), then an
op_commit record that holds the inverse ADD(x, -d). Level 0 locks on x and t
are held only while the operation runs. ADDs commute, so level 1 needs no
locks, and two transactions may change the same counter before either commits.

Stable storage is the disk (page -> (values, page_lsn)) and the stable log.
The buffer pool, the log tail, the locks and the transaction tables are
volatile. The buffer policy is steal and no-force with the WAL rule. Each
public method is one atomic step, and restart() yields after each step, so a
test can crash anywhere, also inside recovery.
"""

from dataclasses import dataclass
from typing import Iterator

PAGE_OF = {"t": "P0", "a": "P1", "b": "P1", "c": "P2", "d": "P2"}
INIT = {"t": 100, "a": 10, "b": 20, "c": 30, "d": 40}


@dataclass(frozen=True)
class Rec:
    lsn: int
    kind: str  # begin, update, op_commit, clr, comp_commit, abort, commit, end
    txn: int
    prev: int = 0  # prevLSN of the same transaction, 0 for none
    page: str = ""
    key: str = ""
    before: int = 0
    after: int = 0  # update and clr: the value written
    undo_next: int = 0  # clr and comp_commit: the next record to undo
    inv: tuple = ()  # op_commit: (key, delta) of the inverse ADD
    op_prev: int = 0  # op_commit: lastLSN of the transaction before the operation
    undone: int = 0  # clr: the update it undoes; comp_commit: the op_commit


def fresh_disk() -> dict:
    disk: dict = {}
    for k, p in sorted(PAGE_OF.items()):
        disk.setdefault(p, ({}, 0))[0][k] = INIT[k]
    return disk


def state(disk: dict) -> dict:
    return {k: v for p in sorted(disk) for k, v in disk[p][0].items()}


class MLR:
    def __init__(self, disk: dict, log: list | None = None, physical_undo: bool = False):
        self.disk = disk
        self.log: list[Rec] = list(log or [])
        self.tail: list[Rec] = []
        self.buf: dict[str, list] = {}
        self.last: dict[int, int] = {}  # txn -> lastLSN
        self.undo_next: dict[int, int] = {}  # txn -> next record to undo (rollback and restart)
        self.plan: dict[int, list] = {}  # txn -> level 0 actions still to run
        self.locks: dict[str, int] = {}  # level 0 locks: key -> txn
        self.physical_undo = physical_undo  # the wrong method, for the tests

    # ------------------------------------------------------------ storage
    def rec(self, lsn: int) -> Rec:
        i = lsn - 1
        return self.log[i] if i < len(self.log) else self.tail[i - len(self.log)]

    def _append(self, **kw) -> Rec:
        r = Rec(lsn=len(self.log) + len(self.tail) + 1, **kw)
        self.tail.append(r)
        if r.txn and r.kind != "end":
            self.last[r.txn] = r.lsn
        return r

    def _page(self, p: str) -> list:
        if p not in self.buf:
            vals, lsn = self.disk[p]
            self.buf[p] = [dict(vals), lsn]
        return self.buf[p]

    def flush_log(self) -> None:
        self.log.extend(self.tail)
        self.tail = []

    def flush_page(self, p: str) -> None:
        if p in self.buf:
            if self.buf[p][1] > len(self.log):  # WAL rule
                self.flush_log()
            self.disk[p] = (dict(self.buf[p][0]), self.buf[p][1])

    def crash(self) -> "MLR":
        return MLR(self.disk, self.log, self.physical_undo)

    def value(self, key: str) -> int:
        return self._page(PAGE_OF[key])[0][key]

    # ------------------------------------------------------------ level 0 actions
    def _write(self, txn: int, key: str, new: int) -> None:
        pg = self._page(PAGE_OF[key])
        r = self._append(kind="update", txn=txn, prev=self.last[txn], page=PAGE_OF[key],
                         key=key, before=pg[0][key], after=new)  # @line L20
        pg[0][key], pg[1] = new, r.lsn

    def can_act(self, txn: int) -> bool:
        a = self.plan[txn][0]
        return a[0] != "w" or self.locks.get(a[1], txn) == txn

    def _act(self, txn: int) -> None:
        """Run the next level 0 action of the operation or compensation of txn."""
        a = self.plan[txn].pop(0)
        if a[0] == "w":
            self.locks[a[1]] = txn  # @line L19
            self._write(txn, a[1], self.value(a[1]) + a[2])  # @line L20
            return
        for k in [k for k, t in self.locks.items() if t == txn]:
            del self.locks[k]  # release the level 0 locks at the end of the operation
        if a[0] == "oc":
            self._append(kind="op_commit", txn=txn, prev=self.last[txn],
                         inv=(a[1], -a[2]), op_prev=a[3])  # @line L21
        else:
            self._append(kind="comp_commit", txn=txn, prev=self.last[txn],
                         undone=a[1], undo_next=a[2])  # @line L14
            self.undo_next[txn] = a[2]  # @line L14

    @staticmethod
    def _compensation(r: Rec) -> list:
        key, d = r.inv
        return [("w", key, d), ("w", "t", d), ("cc", r.lsn, r.op_prev)]  # @line L13

    # ------------------------------------------------------------ normal processing
    def begin(self, txn: int) -> None:
        self._append(kind="begin", txn=txn)
        self.plan[txn] = []

    def add(self, txn: int, key: str, d: int) -> None:
        """Start the level 1 operation ADD(key, d); step() runs its level 0 actions."""
        p = self.last[txn]  # @line L19
        self.plan[txn] = [("w", key, d), ("w", "t", d), ("oc", key, d, p)]  # @line L19

    def busy(self, txn: int) -> bool:
        return bool(self.plan.get(txn))

    def step(self, txn: int) -> None:
        """One level 0 action of txn, or one rollback step if txn is rolling back."""
        if self.plan[txn]:
            self._act(txn)
        else:
            self._l1_step(txn)

    def commit(self, txn: int) -> None:
        self._append(kind="commit", txn=txn, prev=self.last[txn])
        self.flush_log()
        self._append(kind="end", txn=txn, prev=self.last[txn])
        del self.plan[txn]
        del self.last[txn]

    def abort(self, txn: int) -> None:
        r = self._append(kind="abort", txn=txn, prev=self.last[txn])
        self.undo_next[txn] = r.lsn

    def rolling_back(self, txn: int) -> bool:
        return txn in self.undo_next

    def _l1_step(self, txn: int) -> None:
        """Lines L12 to L17 for one transaction. A compensation is planned here and
        its level 0 actions run in the next steps."""
        r = self.rec(self.undo_next[txn])  # @line L12
        if r.kind == "op_commit":
            self.plan[txn] = self._compensation(r)  # @line L13
        elif r.kind == "comp_commit":
            self.undo_next[txn] = r.undo_next  # @line L15
        elif r.kind == "abort":
            self.undo_next[txn] = r.prev  # @line L16
        else:  # begin
            self._append(kind="end", txn=txn, prev=self.last[txn])  # @line L17
            del self.undo_next[txn]  # @line L17
            self.plan.pop(txn, None)
            self.last.pop(txn, None)

    # ------------------------------------------------------------ restart
    def restart(self) -> Iterator[None]:
        """Analysis, redo, the level 0 pass and the level 1 pass. Yields after each step."""
        winners: set[int] = set()
        self.last, self.undo_next, self.plan, self.locks = {}, {}, {}, {}
        for r in self.log:  # @line L1
            if r.kind == "commit":
                winners.add(r.txn)  # @line L2
            elif r.kind == "end":
                winners.discard(r.txn)  # @line L2
                self.last.pop(r.txn, None)
                self.undo_next.pop(r.txn, None)
            else:
                self.last[r.txn] = r.lsn  # @line L3
                jump = r.kind in ("clr", "comp_commit")
                self.undo_next[r.txn] = r.undo_next if jump else r.lsn  # @line L3
        for t in sorted(winners):
            self._append(kind="end", txn=t, prev=self.last[t])  # @line L4
            del self.undo_next[t]
            del self.last[t]
        yield
        for r in list(self.log):  # @line L5
            if r.kind in ("update", "clr"):
                pg = self._page(r.page)
                if pg[1] < r.lsn:  # @line L6
                    pg[0][r.key], pg[1] = r.after, r.lsn  # @line L6
                    yield
        for t in sorted(self.undo_next, key=lambda t: -self.undo_next[t]):  # @line L7
            while True:
                r = self.rec(self.undo_next[t])
                if self.physical_undo and r.kind in ("op_commit", "abort", "comp_commit"):
                    # the wrong method: undo completed operations page by page
                    self.undo_next[t] = r.undo_next if r.kind == "comp_commit" else r.prev
                    continue
                if r.kind not in ("update", "clr"):  # @line L8
                    break
                if r.kind == "clr":
                    self.undo_next[t] = r.undo_next  # @line L9
                    continue
                c = self._append(kind="clr", txn=t, prev=self.last[t], page=r.page, key=r.key,
                                 after=r.before, undo_next=r.prev, undone=r.lsn)  # @line L10
                pg = self._page(r.page)
                pg[0][r.key], pg[1] = r.before, c.lsn  # @line L10
                self.undo_next[t] = r.prev  # @line L10
                yield
        while self.undo_next:  # @line L11
            t = max(self.undo_next, key=lambda t: self.undo_next[t])  # @line L12
            self._l1_step(t)
            yield
            while self.plan.get(t):  # the level 0 actions of a compensation
                self._act(t)  # @line L13
                yield
        self.flush_log()  # @line L18

    def recover(self) -> None:
        for _ in self.restart():
            pass
