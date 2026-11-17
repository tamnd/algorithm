# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-paging/. The authors are listed in prov/951MHG.jsonl.

"""Shadow paging on a simulated disk of slots.

The disk is an array of slots and one root cell. A slot holds a page value or
a page table (a tuple of slot numbers, one per logical page). The root names
the slot of the current page table, and a write of the root is atomic. A
transaction never writes a slot that the root's table uses: it writes copies
and commits by switching the root. There is no log. Every disk write can be
the last one before a crash (Disk.limit), and restart only recomputes the free
slots from the root.
"""


class Crash(Exception):
    pass


class Disk:
    def __init__(self, n_slots: int, n_pages: int) -> None:
        self.slots: list = [0] * n_slots
        self.slots[0] = tuple(range(1, n_pages + 1))  # the page table; pages hold 0
        self.root = 0
        self.writes = 0  # disk writes done so far
        self.limit: int | None = None  # crash before write number limit + 1

    def _tick(self) -> None:
        if self.limit is not None and self.writes >= self.limit:
            raise Crash
        self.writes += 1

    def write(self, slot: int, value) -> None:
        self._tick()
        self.slots[slot] = value

    def write_root(self, slot: int) -> None:
        self._tick()
        self.root = slot

    def sync(self) -> None:
        """A write barrier. Writes here are synchronous, so it has no effect."""


class ShadowDb:
    """One transaction at a time. Cost: one slot write per first write of a
    page, plus one table write and one root write per commit."""

    def __init__(self, disk: Disk) -> None:
        self.disk = disk
        self.table: list[int] | None = None
        self.new: set[int] = set()
        self.free = self._garbage()  # @line L11

    def _garbage(self) -> set[int]:
        """Restart: every slot not reachable from the root is free."""
        used = {self.disk.root, *self.disk.slots[self.disk.root]}
        return set(range(len(self.disk.slots))) - used

    def _alloc(self) -> int:
        s = min(self.free)
        self.free.discard(s)
        return s

    def begin(self) -> None:
        self.table = list(self.disk.slots[self.disk.root])  # @line L1
        self.new = set()

    def read(self, p: int):
        table = self.table if self.table is not None else self.disk.slots[self.disk.root]
        return self.disk.slots[table[p]]

    def write(self, p: int, v) -> None:
        s = self._alloc()  # @line L2
        self.disk.write(s, v)  # @line L3
        if self.table[p] in self.new:  # @line L4
            self.new.discard(self.table[p])
            self.free.add(self.table[p])
        self.table[p] = s  # @line L5
        self.new.add(s)

    def commit(self) -> None:
        old_root = self.disk.root
        old = set(self.disk.slots[old_root])
        t = self._alloc()
        self.disk.write(t, tuple(self.table))  # @line L6
        self.disk.sync()  # @line L7
        self.disk.write_root(t)  # @line L8
        self.free |= {old_root} | (old - set(self.table))  # @line L9
        self.table, self.new = None, set()

    def abort(self) -> None:
        self.free |= self.new  # @line L10
        self.table, self.new = None, set()

    def state(self) -> tuple:
        """The committed database: the values reachable from the root."""
        return tuple(self.disk.slots[s] for s in self.disk.slots[self.disk.root])


class InPlaceDb(ShadowDb):
    """The wrong design for the tests: writes go over the shadow slot."""

    def write(self, p: int, v) -> None:
        self.disk.write(self.table[p], v)
