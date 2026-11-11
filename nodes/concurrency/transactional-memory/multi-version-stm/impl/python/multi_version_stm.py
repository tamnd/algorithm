# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-version-stm/. The authors are listed in prov/0DZJAM.jsonl.

"""A multi-version STM in the style of JVSTM, on the simulated word memory of stmsim.

Shared words:
    a              a versioned box: a tuple ((version, value), ...), newest first
    "G"            the global clock: the version of the last committed update
    "L"            the global commit lock: None when free, else the owner
    ("active", p)  the read version announced by process p, or None (keep="active")

A transaction reads G once at begin (its read version rv) and from then on
reads, in each box, the newest version whose number is at most rv. A writer
installs its new versions while it holds L and only then sets G = wv, so a
version numbered at most rv is always complete. A transaction with no writes
commits with no check and never aborts, as long as the versions it needs are
kept. An update transaction validates at commit: every box it read must
still have its newest version at most rv.

keep = None      keep every version (space grows with every committed write)
keep = k         keep the k newest versions of each box; k = 1 is a
                 single-version STM, and a reader whose version has been
                 dropped aborts
keep = "active"  keep the versions that some running transaction may need:
                 those newer than the oldest announced rv (or than G), and
                 the newest one at or below it

Counters: max_space (the largest total number of versions over all boxes),
max_box (the longest box).
"""

from __future__ import annotations

from typing import Any

from stmsim import Abort, Proc, Tx, nothing


class MultiVersionSTM:
    def __init__(self, keep: Any = None) -> None:
        if not (keep is None or keep == "active" or (isinstance(keep, int) and keep >= 1)):
            raise ValueError(keep)
        self.keep = keep
        self.procs: set = set()
        self.space: dict = {}
        self.max_space = 0
        self.max_box = 1

    def memory(self, data: dict, nprocs: int = 8) -> dict:
        w = {a: ((0, v),) for a, v in data.items()}
        w["G"] = 0
        w["L"] = None
        self.procs = set(range(nprocs))
        if self.keep == "active":
            for p in self.procs:
                w[("active", p)] = None
        self.space = {a: 1 for a in data}
        self.max_space = len(data)
        return w

    def begin(self, tx: Tx) -> Proc:
        tx.rset = []
        tx.wset = {}
        tx.locked = False
        tx.rv = yield ("read", "G")
        if self.keep == "active":
            while True:  # announce rv, then check that the clock has not moved meanwhile
                yield ("write", ("active", tx.tid[0]), tx.rv)
                g = yield ("read", "G")
                if g == tx.rv:
                    break
                tx.rv = g

    def read(self, tx: Tx, a: Any) -> Proc:
        if a in tx.wset:
            return tx.wset[a]
        box = yield ("read", a)
        for ver, v in box:
            if ver <= tx.rv:
                tx.rset.append(a)
                return v
        raise Abort  # every version this snapshot can use has been dropped

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        tx.wset[a] = v
        yield from nothing()

    def _trim(self, box: tuple, floor: int) -> tuple:
        if self.keep is None:
            return box
        if self.keep != "active":
            return box[:self.keep]
        out = []
        for ver, v in box:
            out.append((ver, v))
            if ver <= floor:
                break
        return tuple(out)

    def commit(self, tx: Tx) -> Proc:
        if not tx.wset:
            yield from self._retire(tx)
            return
        while not (yield ("cas", "L", None, tx.tid)):
            yield ("await", "L", "eq", None)
        tx.locked = True
        for a in tx.rset:
            box = yield ("read", a)
            if box[0][0] > tx.rv:
                raise Abort
        g = yield ("read", "G")
        wv = g + 1
        floor = g
        if self.keep == "active":
            for p in sorted(self.procs):
                r = yield ("read", ("active", p))
                if r is not None:
                    floor = min(floor, r)
        for a, v in tx.wset.items():
            box = yield ("read", a)
            box = self._trim(((wv, v),) + box, floor)
            yield ("write", a, box)
            self.space[a] = len(box)
            self.max_box = max(self.max_box, len(box))
        self.max_space = max(self.max_space, sum(self.space.values()))
        yield ("write", "G", wv)
        yield ("write", "L", None)
        tx.locked = False
        yield from self._retire(tx)

    def _retire(self, tx: Tx) -> Proc:
        if self.keep == "active":
            yield ("write", ("active", tx.tid[0]), None)

    def rollback(self, tx: Tx) -> Proc:
        if tx.locked:
            yield ("write", "L", None)
            tx.locked = False
        yield from self._retire(tx)
        tx.wset = {}
