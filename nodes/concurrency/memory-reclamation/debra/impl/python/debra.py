# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/debra/. The authors are listed in prov/K7CR9Y.jsonl.
"""DEBRA and DEBRA+ (Brown) on the simulator in smr_sim.py.

The static block "debra" holds the global epoch G and one announcement per
process: a pair (epoch, quiescent). Each process has three limbo bags. When
a process starts an operation and sees a new epoch, it rotates its bags and
frees the oldest one, which holds nodes retired three observed epochs ago.
At each operation it checks one other process; when it has checked all n
processes in the current epoch, it tries to advance G.

DEBRA+ adds neutralization: if a check fails and the own bags hold at
least T nodes, the checker sends a signal to the slow process and counts
it as quiescent. The signalled process handles the signal before its next
shared step: in the read phase it restarts its operation. In the write
phase it continues, and its reservations (one slot per pointer it will
write with) keep those nodes out of the freed bag.

Precondition: references to shared nodes are held only inside an
operation. Cost: O(1) steps per operation, plus the frees. Plain DEBRA
stops reclaiming when a process stops inside an operation; with DEBRA+,
each process holds at most T + 3 * (n + 1) + 3 * n * K unfreed nodes when
each operation retires at most one node.

BAGS is 3 in the real scheme; a subclass with BAGS = 2 frees one epoch too
early and is kept for the tests.
"""

from __future__ import annotations

from smr_sim import Gen, Memory, NoReclaim, Restart


class Debra(NoReclaim):
    name = "debra"
    K = 2
    BAGS = 3

    def __init__(self, mem: Memory, n: int, plus: bool = False, T: int = 8) -> None:
        super().__init__(mem, n)
        self.plus, self.T = plus, T
        self.bags: list = [[[] for _ in range(self.BAGS)] for _ in range(n)]
        self.cur = [0] * n
        self.seen = [0] * n
        self.ck = [0] * n
        self.phase = [False] * n
        self.neut = [False] * n
        mem.cells["debra"] = {"G": 0, **{t: (0, True) for t in range(n)}}
        if plus:
            mem.cells["sig"] = {t: False for t in range(n)}
            mem.cells["res"] = {(t, i): None for t in range(n) for i in range(self.K)}

    def restartable(self, t: int) -> bool:
        return self.phase[t]

    def on_signal(self, t: int) -> bool:
        self.neut[t] = True
        return self.phase[t]

    def held(self, t: int) -> int:
        return sum(len(b) for b in self.bags[t])

    def begin(self, t: int) -> Gen:
        """Leave the quiescent state: see the epoch, rotate on a change, announce, check one process."""
        self.neut[t] = False
        e = yield ("read", "debra", "G")  # @line L1
        if e != self.seen[t]:  # @line L2
            self.seen[t], self.ck[t] = e, 0
            self.cur[t] = (self.cur[t] + 1) % self.BAGS
            old, self.bags[t][self.cur[t]] = self.bags[t][self.cur[t]], []
            yield from self.free_bag(t, old)  # @line L3
        yield ("write", "debra", t, (e, False))  # @line L4
        q = self.ck[t]
        v = yield ("read", "debra", q)  # @line L5
        ok = v[1] or v[0] == e
        if not ok and self.plus:
            if (yield ("read", "sig", q)):
                ok = True
            elif self.held(t) >= self.T:
                yield ("signal", q)  # @line L6
                ok = True
        if ok:
            self.ck[t] += 1
            if self.ck[t] >= self.n:  # @line L7
                yield ("cas", "debra", "G", e, e + 1)  # @line L8
                self.ck[t] = 0

    def free_bag(self, t: int, bag: list) -> Gen:
        """Free a bag; in DEBRA+ keep the nodes that some process reserved for its write phase."""
        keep = set()
        if self.plus and bag:
            for q in range(self.n):
                for i in range(self.K):
                    r = yield ("read", "res", (q, i))
                    if r is not None:
                        keep.add(r)
        for a in bag:
            if a in keep:
                self.bags[t][self.cur[t]].append(a)
            else:
                yield ("free", a)

    def attempt(self, t: int) -> Gen:
        """Start of a read phase. A neutralized process announces again first."""
        if self.plus and self.neut[t]:
            yield from self.begin(t)
        self.phase[t] = True

    def before_write(self, t: int, ptrs: list) -> Gen:
        """End of the read phase: reserve the nodes the write phase uses, then check for a signal."""
        if self.plus:
            self.phase[t] = False
            for i, p in enumerate(ptrs[: self.K]):
                yield ("write", "res", (t, i), p)
            if self.neut[t]:
                yield from self.begin(t)
                for i in range(len(ptrs[: self.K])):
                    yield ("write", "res", (t, i), None)
                self.phase[t] = True
                raise Restart()

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        self.bags[t][self.cur[t]].append(a)  # @line L9
        return
        yield

    def end(self, t: int) -> Gen:
        """Enter the quiescent state."""
        self.phase[t] = False
        if self.plus:
            for i in range(self.K):
                yield ("write", "res", (t, i), None)
        yield ("write", "debra", t, (self.seen[t], True))  # @line L10
