# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimistic-concurrency-control/. The authors are listed in prov/8MJ6N3.jsonl.

"""Optimistic concurrency control of Kung and Robinson (1981): read phase,
validation and write phase, with serial and parallel backward validation.

Transaction numbers are given out from the counter tnc at the end of the write
phase. A transaction remembers tnc at its start; at validation it checks the
write sets of the transactions numbered start + 1 .. finish against its read
set. Parallel validation also checks the write sets of the transactions that
were validating at the same time against its read and write sets. `ops` logs
every access to the shared database, for the tests.

With serial validation the committed transactions are conflict equivalent to
the serial order of their transaction numbers. With parallel validation they
are conflict equivalent to the order in which they entered validation, which
can differ from the order of the numbers (see the tests).
"""


class Occ:
    def __init__(self, db: dict) -> None:
        self.db = dict(db)
        self.tnc = 0
        self.ws_of_tn: dict[int, set] = {}  # transaction number -> write set
        self.start: dict[int, int] = {}
        self.rs: dict[int, set] = {}
        self.ws: dict[int, dict] = {}
        self.tn: dict[int, int] = {}  # committed transaction -> its number
        self.active: set[int] = set()  # in validation or write phase (parallel)
        self.finish: dict[int, tuple[int, frozenset]] = {}
        self.entered: dict[int, int] = {}
        self.ops: list[tuple] = []  # (kind, txn, item) on the shared database

    # ---- read phase -----------------------------------------------------
    def begin(self, t: int) -> None:
        self.start[t], self.rs[t], self.ws[t] = self.tnc, set(), {}  # @line L1

    def read(self, t: int, x):
        self.rs[t].add(x)  # @line L2
        if x in self.ws[t]:
            return self.ws[t][x]
        self.ops.append(("r", t, x))
        return self.db[x]

    def write(self, t: int, x, v) -> None:
        self.ws[t][x] = v  # @line L3

    def _backward_ok(self, t: int, finish: int) -> bool:
        return all(not (self.ws_of_tn[n] & self.rs[t]) for n in range(self.start[t] + 1, finish + 1))

    # ---- serial validation: one critical section --------------------------
    def serial_commit(self, t: int) -> bool:
        finish = self.tnc  # @line L4
        if not self._backward_ok(t, finish):  # @line L5
            return False
        for x, v in sorted(self.ws[t].items()):  # @line L6
            self.db[x] = v
            self.ops.append(("w", t, x))
        self.tnc += 1  # @line L7
        self.tn[t] = self.tnc
        self.ws_of_tn[self.tnc] = set(self.ws[t])
        return True

    # ---- parallel validation: short critical sections ----------------------
    def enter_validation(self, t: int) -> None:
        self.finish[t] = (self.tnc, frozenset(self.active))  # @line L8
        self.active.add(t)
        self.entered[t] = len(self.entered)  # the order of the ends of read phases

    def validate(self, t: int) -> bool:
        finish, others = self.finish[t]
        ok = self._backward_ok(t, finish)  # @line L9
        mine = self.rs[t] | set(self.ws[t])
        if any(set(self.ws[u]) & mine for u in others):  # @line L10
            ok = False
        if not ok:
            self.active.discard(t)  # @line L11
        return ok

    def write_one(self, t: int, x) -> None:
        self.db[x] = self.ws[t][x]  # @line L12
        self.ops.append(("w", t, x))

    def finish_commit(self, t: int) -> None:
        self.tnc += 1  # @line L13
        self.tn[t] = self.tnc
        self.ws_of_tn[self.tnc] = set(self.ws[t])
        self.active.discard(t)
