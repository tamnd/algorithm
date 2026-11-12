# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precise-garbage-collection/. The authors are listed in prov/KYZMZH.jsonl.

"""Precise root finding with stack maps, and a copying collection that uses it.

A frame is a function, the safepoint at which it is stopped (a call site),
and its slots. The compiler emits a stack map for each safepoint: the slots
that hold live pointers there, and the derived pointers as pairs (base slot,
derived slot), in the style of Diwan, Moss and Hudson. Heap objects have a
precise layout: the first `nptr` words are pointers, the rest are data.

Because every pointer is known, the collector can move objects and update
every pointer, and a dead or non-pointer slot never keeps an object alive.
"""

from dataclasses import dataclass, field


@dataclass
class StackMap:
    pointers: list[int]  # slots that hold live base pointers
    derived: list[tuple[int, int]] = field(default_factory=list)  # (base slot, derived slot)


@dataclass
class Frame:
    func: str
    pc: int  # the safepoint where the frame is stopped
    slots: list[int]


@dataclass
class Obj:
    nptr: int  # the first nptr words are pointers
    words: list[int]


class NotAtSafepoint(Exception):
    pass


def collect(heap: dict[int, Obj], stack: list[Frame],
            maps: dict[tuple[str, int], StackMap], next_addr: int) -> tuple[dict[int, Obj], int]:
    """Copy the objects that the live roots reach into fresh addresses
    starting at next_addr, update every pointer, and return the new heap
    and the next free address. The old heap is left unchanged."""
    new: dict[int, Obj] = {}
    forward: dict[int, int] = {}
    queue: list[int] = []

    def evacuate(a: int) -> int:
        nonlocal next_addr
        if a == 0:
            return 0  # the null pointer
        if a not in forward:
            o = heap[a]
            forward[a] = next_addr
            new[next_addr] = Obj(o.nptr, list(o.words))
            queue.append(next_addr)
            next_addr += max(1, len(o.words))
        return forward[a]

    offsets: list[tuple[Frame, int, int, int]] = []
    for f in stack:  # walk the frames from the oldest to the newest
        m = maps.get((f.func, f.pc))
        if m is None:
            raise NotAtSafepoint(f"{f.func} is stopped at {f.pc}, which has no stack map")
        for b, d in m.derived:
            offsets.append((f, b, d, f.slots[d] - f.slots[b]))  # derived minus base
        for s in m.pointers:
            f.slots[s] = evacuate(f.slots[s])  # a root is updated in place
    k = 0
    while k < len(queue):  # Cheney scan of the copies
        o = new[queue[k]]
        k += 1
        for i in range(o.nptr):
            o.words[i] = evacuate(o.words[i])
    for f, b, d, off in offsets:
        f.slots[d] = f.slots[b] + off  # recompute the derived pointer from its moved base
    return new, next_addr


def conservative_roots(heap: dict[int, Obj], stack: list[Frame]) -> set[int]:
    """What a collector without stack maps would have to keep: every slot
    value that equals an object address is a possible pointer."""
    return {v for f in stack for v in f.slots if v in heap}
