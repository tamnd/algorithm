# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undo-log/. The authors are listed in prov/X5CC3X.jsonl.

"""The undo log of an eager-versioning STM: the old values of the words that one transaction wrote in place.

Before the first write of a transaction to a word, the log saves the old value
of the word. The write then goes straight to memory. At commit the log is
thrown away. At abort the log writes the old values back, in reverse order.

The STM must keep other transactions away from a word from the first write to
the end of the transaction (with a write lock), because memory holds a value
that may still be undone. This module is the private log only.

With first_write_only=False the log saves an entry at every write. Then the
order of the rollback matters: only the reverse order restores the oldest value.
"""

from __future__ import annotations

from typing import Any


class UndoLog:
    def __init__(self, first_write_only: bool = True) -> None:
        self.entries: list[tuple[Any, Any]] = []  # (word, old value), in the order of the writes
        self.logged: set = set()
        self.first_write_only = first_write_only

    def write(self, mem: dict, a: Any, v: Any) -> None:
        """Write v to word a in place, after saving the old value if needed."""
        if not (self.first_write_only and a in self.logged):  # @line L1
            self.entries.append((a, mem[a]))  # @line L2
            self.logged.add(a)
        mem[a] = v  # @line L3

    def rollback(self, mem: dict, reverse: bool = True) -> int:
        """Restore the old values. Return the number of words written."""
        order = reversed(self.entries) if reverse else iter(self.entries)
        n = 0
        for a, old in order:  # @line L4
            mem[a] = old
            n += 1
        self.discard()
        return n

    def commit(self) -> None:
        self.discard()  # @line L5

    def discard(self) -> None:
        self.entries.clear()
        self.logged.clear()

    def __len__(self) -> int:
        return len(self.entries)
