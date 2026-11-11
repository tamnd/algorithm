# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-transactional-memory/. The authors are listed in prov/932XZC.jsonl.
"""A simplified Hybrid NOrec: hardware transactions with a NOrec software path.

`atomic` is a generator for one simulated processor. It first runs the block
as a hardware transaction of the best-effort HTM in htmsim.py, up to `tries`
times. If that fails, it runs the block as a NOrec software transaction.
Both kinds run at the same time, and two shared words keep them apart:

  SEQ  the NOrec sequence lock. It is odd while a software transaction
       writes back. A hardware transaction reads it first (it subscribes),
       so the writer's compare-and-swap on SEQ aborts every hardware
       transaction, and a new one sees an odd value and aborts itself.
  HWC  a counter that every writing hardware transaction increments just
       before it commits. A hardware commit does not change SEQ, so the
       software path polls HWC as well as SEQ to learn that memory changed.

The software path is NOrec: it buffers writes, keeps the values it read,
and after each read checks that SEQ and HWC did not change; if one did, it
validates by value and restarts if a value differs. At commit it takes SEQ,
checks HWC once more (validating if it changed), writes back, and releases.

The switches subscribe=False and watch_hw=False exist only for the tests,
which show that each check is needed.

A block is a generator function `body(v)` that reads by `x = yield from
v.read(a)` and writes by `yield from v.write(a, x)`, and returns a result.

Precondition: SEQ and HWC are keys of the memory and start at 0 and an
even value; no other code writes them. Cost: each hardware try is O(k)
steps for a block of k accesses; a software read costs O(1) steps when
nothing committed, and O(r) for a validation with r values read.
"""

from __future__ import annotations

from htmsim import EXPLICIT, RETRY, Abort, explicit_code

SEQ = "seq"
HWC = "hwc"
SW_BUSY = 0xFE   # explicit abort code: a software transaction writes back


class Restart(Exception):
    """The software transaction saw a changed value and must start again."""


class HardwareView:
    """Accesses of a hardware transaction: one HTM instruction per step."""

    def __init__(self, htm, p: int) -> None:
        self.htm = htm
        self.p = p
        self.wrote = False

    def read(self, a):
        value = self.htm.load(self.p, a)
        yield
        return value

    def write(self, a, v):
        self.htm.store(self.p, a, v)
        self.wrote = True
        yield


class SoftwareTx:
    """One attempt of a NOrec software transaction on processor p."""

    def __init__(self, htm, p: int, watch_hw: bool) -> None:
        self.htm = htm
        self.p = p
        self.watch_hw = watch_hw
        self.reads: dict = {}
        self.writes: dict = {}
        self.s = 0
        self.h = 0

    def _ld(self, a):
        return self.htm.load(self.p, a)

    def _clock(self):
        """Read SEQ (waiting until it is even) and HWC; return both."""
        while True:
            yield (lambda: self.htm.mem[SEQ] % 2 == 0)
            s = self._ld(SEQ)
            if s % 2 == 0:
                break
        yield
        h = self._ld(HWC) if self.watch_hw else 0
        yield
        return s, h

    def _unchanged(self):
        s = self._ld(SEQ)
        yield
        if s != self.s:
            return False
        if self.watch_hw:
            h = self._ld(HWC)
            yield
            if h != self.h:
                return False
        return True

    def _values_ok(self):
        for a, v in self.reads.items():
            ok = self._ld(a) == v
            yield
            if not ok:
                return False
        return True

    def validate(self):
        """Wait for a moment with no writer in which every value read is
        still in memory; move the snapshot there, or raise Restart."""
        while True:
            self.s, self.h = yield from self._clock()
            if not (yield from self._values_ok()):
                raise Restart
            if (yield from self._unchanged()):
                return

    def start(self):
        self.s, self.h = yield from self._clock()

    def read(self, a):
        if a in self.writes:
            yield
            return self.writes[a]
        value = self._ld(a)
        yield
        while not (yield from self._unchanged()):
            yield from self.validate()
            value = self._ld(a)
            yield
        self.reads[a] = value
        return value

    def write(self, a, v):
        self.writes[a] = v
        yield

    def commit(self):
        if not self.writes:
            return                      # read-only: valid at its last read
        while not self.htm.cas(self.p, SEQ, self.s, self.s + 1):
            yield
            yield from self.validate()
        yield
        if self.watch_hw:
            h = self._ld(HWC)
            yield
            if h != self.h and not (yield from self._values_ok()):
                self.htm.store(self.p, SEQ, self.s)   # nothing written: undo the lock
                yield
                raise Restart
        for a, v in self.writes.items():
            self.htm.store(self.p, a, v)
            yield
        self.htm.store(self.p, SEQ, self.s + 2)
        yield


def atomic(htm, p: int, body, tries: int = 2, subscribe: bool = True,
           watch_hw: bool = True, stats: dict | None = None):
    """Run body atomically on processor p; return (result, "hw" or "sw")."""
    for _ in range(tries):
        yield (lambda: htm.mem[SEQ] % 2 == 0)
        htm.begin(p)
        view = HardwareView(htm, p)
        try:
            if subscribe and htm.load(p, SEQ) % 2 == 1:
                htm.abort(p, SW_BUSY)
            yield
            result = yield from body(view)
            if view.wrote:
                c = htm.load(p, HWC)
                yield
                htm.store(p, HWC, c + 1)
                yield
            htm.commit(p)
        except Abort as abort:
            busy = bool(abort.status & EXPLICIT) and explicit_code(abort.status) == SW_BUSY
            yield
            if not (abort.status & RETRY) and not busy:
                break
            continue
        yield
        return result, "hw"
    while True:
        tx = SoftwareTx(htm, p, watch_hw)
        try:
            yield from tx.start()
            result = yield from body(tx)
            yield from tx.commit()
        except Restart:
            if stats is not None:
                stats["restarts"] = stats.get("restarts", 0) + 1
            yield
            continue
        return result, "sw"
