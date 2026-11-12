# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/remembered-set/. The authors are listed in prov/ASEXAM.jsonl.

"""A remembered set: a sequential store buffer in front of a hash set.

An entry is a slot (object, field) with slot precision, or an object with
object precision. The write barrier calls record() when a store puts a young
pointer into an old object. The fast path appends to a buffer of fixed
capacity; a full buffer is drained into the hash set, which removes the
duplicates. At a minor collection, roots() drains the buffer and yields the
slots to scan. After the collection, retain() drops the entries that no
longer hold a young pointer.
"""

from typing import Callable, Hashable, Iterable, Iterator

Slot = tuple[Hashable, int]


class RememberedSet:
    def __init__(self, capacity: int, precision: str = "slot") -> None:
        if capacity < 1:
            raise ValueError("the buffer capacity must be at least 1")
        if precision not in ("slot", "object"):
            raise ValueError("precision is 'slot' or 'object'")
        self.capacity = capacity
        self.precision = precision
        self.buffer: list[Hashable] = []
        self.table: set[Hashable] = set()
        self.remembered: set[Hashable] = set()  # the header bits of object precision
        self.drains = 0
        self.appends = 0

    def record(self, obj: Hashable, field: int) -> None:
        """Remember that field `field` of the old object `obj` holds a young pointer.

        Cost: O(1), plus O(capacity) when the buffer is full.
        """
        e = (obj, field) if self.precision == "slot" else obj  # @line L1
        if self.precision == "object" and obj in self.remembered:  # @line L2
            return
        if self.precision == "object":  # @line L3
            self.remembered.add(obj)
        self.buffer.append(e)  # @line L4
        self.appends += 1
        if len(self.buffer) == self.capacity:  # @line L5
            self.drain()

    def drain(self) -> None:
        """Move the buffer into the hash set. Cost: O(len(buffer)) expected."""
        self.drains += 1
        for e in self.buffer:  # @line L6
            self.table.add(e)
        self.buffer.clear()  # @line L7

    def roots(self, fields_of: Callable[[Hashable], list], is_young: Callable[[object], bool]) -> Iterator[Slot]:
        """Yield each remembered slot that holds a young pointer, once."""
        self.drain()  # @line L8
        for e in list(self.table):  # @line L9
            if self.precision == "slot":
                obj, i = e
                if is_young(fields_of(obj)[i]):  # @line L10
                    yield (obj, i)
            else:
                for i, t in enumerate(fields_of(e)):
                    if is_young(t):
                        yield (e, i)

    def retain(self, keep: Callable[[Hashable], bool]) -> None:
        """After a collection: keep only the entries for which keep(entry) holds."""
        self.drain()
        self.table = {e for e in self.table if keep(e)}  # @line L11
        if self.precision == "object":
            self.remembered = set(self.table)

    def forget_objects(self, dead: Iterable[Hashable]) -> None:
        """Remove the entries of old objects that a major collection freed."""
        dead = set(dead)
        self.drain()
        if self.precision == "slot":
            self.table = {e for e in self.table if e[0] not in dead}
        else:
            self.table -= dead
            self.remembered -= dead

    def covers(self, obj: Hashable, field: int) -> bool:
        """True when the slot is remembered, in the buffer or in the table."""
        e = (obj, field) if self.precision == "slot" else obj
        return e in self.table or e in self.buffer

    def __len__(self) -> int:
        return len(self.table) + len(self.buffer)
