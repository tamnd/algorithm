# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shavit-touitou-stm/. The authors are listed in prov/9B9H5V.jsonl.

"""The STM of Shavit and Touitou (PODC 1995) on the simulated word memory of stmsim.

A transaction is static: its data set (the words it reads and writes) is
known when it starts, and its effect is a function f of the old values of the
data set, which returns (new values for some words of the set, result).

Shared words:
    a                  a data word
    ("own", a)         the record that owns a, or None
    ("status", r)      the status of record r: None (undecided), "success",
                       or ("failure", a) when the acquire of word a failed
    ("old", r)         the agreed old values of record r: a tuple of (a, v)
Records are named by (p, s): process p, attempt s. The data set and f of a
record are immutable and read by helpers with no shared step.

Every shared write that a helper might do late uses LL/SC, so that a helper
that wakes up after the transaction is over changes nothing. The STM acquires
ownerships in increasing address order and, when it fails, releases what it
holds and helps the owner that stopped it (once, not recursively). This makes
it lock-free.
"""

from __future__ import annotations

from typing import Any, Callable

from stmsim import Proc

SUCCESS = "success"


class ShavitTouitou:
    def __init__(self, data: dict, nprocs: int = 3, max_attempts: int = 30, helping: bool = True,
                 skip_equal: bool = True) -> None:
        self.data = dict(data)
        self.nprocs = nprocs
        self.max_attempts = max_attempts
        self.helping = helping
        self.skip_equal = skip_equal  # False gives the broken variant that the tests show
        self.records: dict = {}  # r -> (sorted data set, f)
        self.helps = 0

    def memory(self) -> dict:
        w = dict(self.data)
        for a in self.data:
            w[("own", a)] = None
        for p in range(self.nprocs):
            for s in range(self.max_attempts):
                w[("status", (p, s))] = None
                w[("old", (p, s))] = ()
        return w

    # ------------------------------------------------------------ one record

    def acquire(self, r: tuple, a: Any) -> Proc:
        """Return True if r owns a, False if r is decided or a is owned by another record."""
        while True:
            o = yield ("ll", ("own", a))  # @line L5
            if o == r:
                return True
            if (yield ("read", ("status", r))) is not None:  # @line L6
                return False
            if o is None:  # @line L7
                if (yield ("sc", ("own", a), r)):
                    return True
                continue
            if (yield ("ll", ("status", r))) is None:  # @line L8
                yield ("sc", ("status", r), ("failure", a))
            return False

    def agree_old(self, r: tuple) -> Proc:
        for a in self.records[r][0]:
            while True:
                old = yield ("ll", ("old", r))  # @line L9
                if a in dict(old):
                    break
                v = yield ("read", a)
                if (yield ("sc", ("old", r), old + ((a, v),))):
                    break
        return dict((yield ("read", ("old", r))))

    def update(self, r: tuple, new: dict) -> Proc:
        for a in self.records[r][0]:
            if a not in new:
                continue
            v = yield ("ll", a)  # @line L10
            # Write only if the word does not hold the new value yet. Without this test, a helper whose LL
            # comes after another helper's write could write the same value again after the release, and
            # so wipe out the write of the next owner (test_without_the_value_test_an_update_is_lost).
            if (v != new[a] or not self.skip_equal) and (yield ("read", ("own", a))) == r:
                yield ("sc", a, new[a])

    def release(self, r: tuple) -> Proc:
        for a in self.records[r][0]:
            if (yield ("ll", ("own", a))) == r:  # @line L11
                yield ("sc", ("own", a), None)

    def transaction(self, r: tuple, initiator: bool) -> Proc:
        """Run record r to its end. Return (status, agreed old values or None)."""
        addrs, f = self.records[r]
        for a in addrs:  # @line L1
            if not (yield from self.acquire(r, a)):
                break
        else:
            if (yield ("ll", ("status", r))) is None:  # @line L2
                yield ("sc", ("status", r), SUCCESS)
        st = yield ("read", ("status", r))
        if st == SUCCESS:  # @line L3
            old = yield from self.agree_old(r)
            new, _ = f(old)
            yield from self.update(r, new)
            yield from self.release(r)
            return st, old
        yield from self.release(r)  # @line L4
        if initiator and self.helping:
            o = yield ("read", ("own", st[1]))  # the record that owns the word now, as in the paper
            if o is not None:
                self.helps += 1
                yield from self.transaction(o, False)
        return st, None

    # ------------------------------------------------------------ the interface

    def run(self, p: int, addrs, f: Callable[[dict], tuple[dict, Any]], tries: int | None = None) -> Proc:
        """Run the static transaction (addrs, f) for process p until it succeeds,
        at most tries attempts. Record events in the stmsim history."""
        serial = self.__dict__.setdefault("_serial", {})
        k = 0
        while tries is None or k < tries:
            k += 1
            r = (p, serial.get(p, 0))  # @line L12
            serial[p] = r[1] + 1
            if r[1] >= self.max_attempts:
                raise RuntimeError("too many attempts for the preallocated records")
            self.records[r] = (tuple(sorted(addrs, key=repr)), f)
            yield ("ev", r, "begin")
            st, old = yield from self.transaction(r, True)
            if st == SUCCESS:
                new, result = f(old)
                for a in self.records[r][0]:
                    yield ("ev", r, "read", a, old[a])
                for a, v in new.items():
                    yield ("ev", r, "write", a, v)
                yield ("ev", r, "tryc")
                yield ("ev", r, "commit")
                return result
            yield ("ev", r, "abort")
        return None


# ---------------------------------------------------------------- static transactions


def transfer(i: int, j: int, amt: int):
    ai, aj = f"a{i}", f"a{j}"
    return [ai, aj], lambda old: ({ai: old[ai] - amt, aj: old[aj] + amt}, None)


def audit(m: int):
    addrs = [f"a{i}" for i in range(m)]
    return addrs, lambda old: ({}, sum(old[a] for a in addrs))


def increment(a: str):
    return [a], lambda old: ({a: old[a] + 1}, old[a] + 1)
