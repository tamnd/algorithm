# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-and-key-temporal-checking/. The authors are listed in prov/NYGPH2.jsonl.

"""Lock and key temporal checking on a simulated heap.

Each allocation gets a key that is never reused and a lock location that holds
the key while the allocation is live. A pointer carries the key and the
address of the lock. An access is allowed only if the lock still holds the
key; free overwrites the lock, so every copy of every pointer into the
allocation fails at once, with no search for the copies. Pointers stored in
memory keep their key and lock in a disjoint table keyed by the address where
the pointer is stored, so the memory layout does not change.

The memory is a Python bytearray, never real memory. This checks temporal
safety only; spatial checks are a separate layer.
"""

from dataclasses import dataclass

WORD = 4  # bytes in a stored pointer
INVALID = 0  # the value free writes to a lock; no key is 0


class AccessError(Exception):
    """An access or a free was refused."""


class TemporalError(AccessError):
    """The allocation of the pointer is no longer live."""


@dataclass(frozen=True)
class KeyedPtr:
    """A pointer in a register with the key of its allocation and the index of its lock."""

    value: int
    key: int
    lock: int


NULL = KeyedPtr(0, 0, 0)  # lock 0 holds -1, which matches no key


class LockAndKeyHeap:
    """A first-fit heap with a lock space and a disjoint pointer metadata table.

    The check and pointer loads and stores cost O(1); alloc and free cost O(h)
    for h holes in the free list, plus O(1) for the lock. Precondition: the
    program makes pointers only with alloc, add, load_ptr and int_to_ptr.
    """

    def __init__(self, size: int = 256) -> None:
        if size < 2:
            raise ValueError("size must be at least 2")
        self.mem = bytearray(size)
        self.holes: list[tuple[int, int]] = [(1, size - 1)]  # address 0 stays unused
        self.blocks: dict[int, tuple[int, int]] = {}  # base -> (size, lock)
        self.locks: list[int] = [-1]  # the lock space; lock 0 belongs to no allocation
        self.free_locks: list[int] = []
        self.next_key = 1
        self.meta: dict[int, tuple[int, int]] = {}  # address of a stored pointer -> (key, lock)

    def alloc(self, n: int) -> KeyedPtr:
        """Allocate n >= 1 zeroed bytes. Return NULL if no hole is large enough."""
        if n < 1:
            raise ValueError("n must be positive")
        for i, (start, length) in enumerate(self.holes):
            if length >= n:
                break
        else:
            return NULL
        b = start  # @line L1
        if length == n:
            del self.holes[i]
        else:
            self.holes[i] = (start + n, length - n)
        key = self.next_key  # @line L2: never reused
        self.next_key += 1
        if self.free_locks:  # @line L3: lock locations are reused, keys are not
            lock = self.free_locks.pop()
        else:
            lock = len(self.locks)
            self.locks.append(INVALID)
        self.locks[lock] = key  # @line L4
        self.blocks[b] = (n, lock)
        self.mem[b:b + n] = bytes(n)
        return KeyedPtr(b, key, lock)  # @line L5

    def add(self, p: KeyedPtr, k: int) -> KeyedPtr:
        """Pointer arithmetic: the key and the lock go along."""
        return KeyedPtr(p.value + k, p.key, p.lock)  # @line L6

    def int_to_ptr(self, v: int) -> KeyedPtr:
        """A pointer made from an integer has no valid key."""
        return KeyedPtr(v, 0, 0)

    def check(self, p: KeyedPtr) -> None:
        """Raise TemporalError unless the allocation of p is live."""
        if self.locks[p.lock] != p.key:  # @line L7
            raise TemporalError(f"key {p.key} does not match lock {p.lock}")  # @line L8

    def load(self, p: KeyedPtr, w: int) -> int:
        self.check(p)  # @line L9
        return int.from_bytes(self.mem[p.value:p.value + w], "little")  # @line L10

    def store(self, p: KeyedPtr, w: int, v: int) -> None:
        self.check(p)  # @line L9
        self.mem[p.value:p.value + w] = (v % (1 << (8 * w))).to_bytes(w, "little")  # @line L10

    def free(self, p: KeyedPtr) -> None:
        """Free the allocation of p; p must be live and point to its start."""
        self.check(p)  # @line L11: catches a double free
        if p.value not in self.blocks or self.blocks[p.value][1] != p.lock:
            raise AccessError(f"free of {p.value}, which is not the start of its allocation")
        n, lock = self.blocks.pop(p.value)
        self.locks[lock] = INVALID  # @line L12: every copy of every pointer now fails L7
        self.free_locks.append(lock)  # @line L13
        self._release(p.value, n)

    def store_ptr(self, loc: KeyedPtr, q: KeyedPtr) -> None:
        """Store q at loc: the value in memory, the key and lock in the table."""
        self.check(loc)  # @line L14
        self.mem[loc.value:loc.value + WORD] = (q.value % (1 << (8 * WORD))).to_bytes(WORD, "little")
        self.meta[loc.value] = (q.key, q.lock)

    def load_ptr(self, loc: KeyedPtr) -> KeyedPtr:
        """Load a pointer from loc with the key and lock stored for that address."""
        self.check(loc)  # @line L15
        v = int.from_bytes(self.mem[loc.value:loc.value + WORD], "little")
        key, lock = self.meta.get(loc.value, (0, 0))
        return KeyedPtr(v, key, lock)

    def _release(self, base: int, n: int) -> None:
        holes = sorted(self.holes + [(base, n)])
        merged: list[tuple[int, int]] = []
        for s, l in holes:
            if merged and merged[-1][0] + merged[-1][1] == s:
                merged[-1] = (merged[-1][0], merged[-1][1] + l)
            else:
                merged.append((s, l))
        self.holes = merged

    def check_invariant(self) -> None:
        """Each live block owns one lock that holds a distinct key; free locks hold INVALID."""
        owned = [lock for _, lock in self.blocks.values()]
        assert len(set(owned)) == len(owned) and 0 not in owned
        assert not set(owned) & set(self.free_locks)
        keys = [self.locks[lock] for lock in owned]
        assert len(set(keys)) == len(keys) and all(0 < k < self.next_key for k in keys)
        assert all(self.locks[lock] == INVALID for lock in self.free_locks)
        assert self.locks[0] == -1
        spans = sorted([(b, b + n) for b, (n, _) in self.blocks.items()] + [(s, s + l) for s, l in self.holes])
        pos = 1
        for lo, hi in spans:
            assert lo == pos and hi > lo
            pos = hi
        assert pos == len(self.mem)
