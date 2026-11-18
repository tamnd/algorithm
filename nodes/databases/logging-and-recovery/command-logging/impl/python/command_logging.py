# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/command-logging/. The authors are listed in prov/DQZNNJ.jsonl.

"""Command logging for a deterministic in-memory database.

Transactions are stored procedures that run one at a time. The log holds one
record per transaction: its id, the name of the procedure and the parameters.
The record goes into the log tail before the procedure runs, and a group
commit writes the tail to stable storage and only then reports the
transactions. A checkpoint is a transaction-consistent snapshot, taken between
two transactions and written in steps. Recovery loads the newest complete
snapshot and runs the logged procedures after it again, in log order.

A procedure gets its random numbers from a source seeded by its transaction
id, so that the replay makes the same choices.
"""

import random
from dataclasses import dataclass

ACCOUNTS = ["a", "b", "c", "d"]


def deposit(db: dict, rnd: random.Random, acct: str, amount: int) -> bool:
    db[acct] += amount
    return True


def transfer(db: dict, rnd: random.Random, src: str, dst: str, amount: int) -> bool:
    if db[src] < amount:
        return False  # the procedure aborts, and it aborts again in the replay
    db[src] -= amount
    db[dst] += amount
    return True


def bonus(db: dict, rnd: random.Random, acct: str) -> bool:
    db[acct] += rnd.randint(1, 50)  # a random choice, seeded by the transaction id
    return True


PROCS = {"deposit": deposit, "transfer": transfer, "bonus": bonus}


@dataclass(frozen=True)
class Cmd:
    lsn: int
    txn: int
    proc: str
    params: tuple


@dataclass(frozen=True)
class Snapshot:
    lsn: int  # the last command whose effect the snapshot holds
    state: dict


class CmdDb:
    def __init__(self, log: list | None = None, snapshots: list | None = None, procs: dict = PROCS):
        self.procs = procs
        self.log: list[Cmd] = list(log or [])  # stable
        self.tail: list[Cmd] = []
        self.snapshots: list[Snapshot] = list(snapshots or [Snapshot(0, {k: 100 for k in ACCOUNTS})])
        self.state: dict = dict(self.snapshots[-1].state)
        self.writing: tuple | None = None  # (lsn, copy, keys written, keys left)

    def _run(self, c: Cmd) -> bool:
        rnd = random.Random(c.txn)  # @line L2
        return self.procs[c.proc](self.state, rnd, *c.params)  # @line L2

    def submit(self, proc: str, *params) -> int:
        """Log a transaction in the tail and run it. Return its id."""
        lsn = len(self.log) + len(self.tail) + 1
        c = Cmd(lsn, txn=1000 + lsn, proc=proc, params=params)  # @line L1
        self.tail.append(c)  # @line L1
        self._run(c)
        return c.txn

    def group_commit(self) -> list[int]:
        """Write the tail to the stable log. Return the ids that may now be reported."""
        done = [c.txn for c in self.tail]
        self.log.extend(self.tail)  # @line L3
        self.tail = []
        return done  # @line L3

    def begin_checkpoint(self) -> None:
        """Take a snapshot between two transactions. A real system marks it and
        copies a record only before a later transaction changes it (copy on
        write); here the copy is made at once and written in steps."""
        lsn = len(self.log) + len(self.tail)  # @line L4
        self.writing = (lsn, dict(self.state), {}, sorted(self.state))  # @line L4

    def checkpoint_step(self) -> None:
        lsn, copy, out, left = self.writing
        if left:
            out[left[0]] = copy[left[0]]  # @line L5
            self.writing = (lsn, copy, out, left[1:])
            return
        if lsn > len(self.log):  # the snapshot may hold only stable commands
            self.group_commit()
        self.snapshots.append(Snapshot(lsn, out))  # @line L5
        self.writing = None

    def crash(self) -> "CmdDb":
        return CmdDb(self.log, self.snapshots, self.procs)

    def recover(self) -> int:
        """Load the newest complete snapshot and replay the log after it.
        Return the number of commands replayed."""
        snap = self.snapshots[-1]  # @line L6
        self.state = dict(snap.state)  # @line L6
        replayed = 0
        for c in self.log[snap.lsn:]:  # @line L7
            self._run(c)  # @line L8
            replayed += 1
        return replayed
