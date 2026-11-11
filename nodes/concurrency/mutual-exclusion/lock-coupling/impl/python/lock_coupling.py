# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-coupling/. The authors are listed in prov/R9GFHC.jsonl.
"""A sorted linked list set with lock coupling (hand-over-hand locking).

The list has the sentinel nodes 'H' (key -inf) and 'T' (key +inf). Node x
has the shared words ('next', x) and ('lock', x). Keys do not change, so a
process knows the key of each node without a shared step. A new node for
operation j of process p has the name (p, j) and is declared in advance.

Acquiring a lock is one guarded atomic step (it waits while the lock is
held); releasing it is a write.

With couple=False the traversal holds at most one lock at a time. That is
the bug that lock coupling prevents.
"""

from __future__ import annotations

from typing import Iterator

NEG, POS = float("-inf"), float("inf")


def setup(initial: list, programs: list) -> tuple:
    """Build the memory and the key map. programs[p] is a list of (name, key)."""
    keys = {"H": NEG, "T": POS}
    chain = ["H"] + [("init", k) for k in sorted(initial)] + ["T"]
    for k in initial:
        keys[("init", k)] = k
    for p, prog in enumerate(programs):
        for j, (name, k) in enumerate(prog):
            if name == "add":
                keys[(p, j)] = k
    mem: dict = {}
    for x in keys:
        mem[("next", x)] = None
        mem[("lock", x)] = False
    for a, b in zip(chain, chain[1:]):
        mem[("next", a)] = b
    return mem, keys


def lock(x):
    w = ("lock", x)
    return ("atomic", lambda mem, pid: [(None, {w: True})], lambda mem, pid: not mem[w])


def unlock(x):
    return ("write", ("lock", x), False)


def locate(key, _keys: dict, couple: bool) -> Iterator:
    """Return (pred, curr) with key(pred) < key <= key(curr), both locked (when couple)."""
    yield lock("H")  # @line L1
    pred = "H"
    curr = yield ("read", ("next", pred))  # @line L2
    if not couple:
        yield unlock(pred)
    yield lock(curr)  # @line L3
    while _keys[curr] < key:  # @line L4
        if couple:
            yield unlock(pred)  # @line L5
        pred = curr  # @line L6
        curr = yield ("read", ("next", pred))
        if not couple:
            yield unlock(pred)
        yield lock(curr)  # @line L7
    return pred, curr


def operation(name, key, me, _keys, couple) -> Iterator:
    pred, curr = yield from locate(key, _keys, couple)
    if name == "contains":
        ok = _keys[curr] == key
    elif name == "add":
        ok = _keys[curr] != key
        if ok:  # link the new node me between pred and curr
            yield ("write", ("next", me), curr)
            yield ("write", ("next", pred), me)
    else:
        ok = _keys[curr] == key
        if ok:  # unlink curr; both pred and curr are locked
            succ = yield ("read", ("next", curr))
            yield ("write", ("next", pred), succ)
            del succ
    yield unlock(curr)
    if couple:
        yield unlock(pred)
    return ok


def client(programs: list, keys: dict, couple: bool = True):
    progs = tuple(tuple(p) for p in programs)
    _keys = dict(keys)

    def make(pid: int) -> Iterator:
        j = 0
        while j < len(progs[pid]):
            name, key = progs[pid][j]
            yield ("mark", "inv", (name, key))
            ok = yield from operation(name, key, (pid, j), _keys, couple)
            yield ("mark", "res", ok)
            del ok
            j += 1
    return make


def set_spec(state: frozenset, name: str, key) -> tuple:
    if name == "contains":
        return state, key in state
    if name == "add":
        return state | {key}, key not in state
    return state - {key}, key in state
