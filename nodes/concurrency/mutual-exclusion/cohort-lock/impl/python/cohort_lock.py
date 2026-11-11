# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cohort-lock/. The authors are listed in prov/KR24FX.jsonl.
"""The C-BO-MCS cohort lock of Dice, Marathe and Shavit, for the explorer in interleave.py.

The global lock is a test-and-test-and-set lock with backoff on the word
'G'. Each cluster c (a NUMA node) has a local MCS lock with the tail word
('tail', c) and a pass counter ('count', c). Process p owns the MCS node
with the words ('next', p) and ('state', p). The state of a waiting node
becomes GLOBAL when its predecessor passes the global lock with the local
lock, and ACQ when the successor must take the global lock itself.

The holder passes locally only when it detects a waiting cohort member and
the counter is below the bound B (may-pass-local). The mark 'global' is
logged each time a process takes the global lock.
"""

from __future__ import annotations

from typing import Iterator

NIL = None
WAIT, GLOBAL, ACQ = "wait", "global", "acq"


def init(cluster_of: list) -> dict:
    mem: dict = {"G": False}
    for c in set(cluster_of):
        mem[("tail", c)] = NIL
        mem[("count", c)] = 0
    for p in range(len(cluster_of)):
        mem[("next", p)] = NIL
        mem[("state", p)] = WAIT
    return mem


def global_acquire(max_delay: int) -> Iterator:
    """Test-and-test-and-set with randomized backoff on 'G'."""
    while True:
        while (yield ("read", "G")):
            pass
        if not (yield ("tas", "G")):
            return
        d = yield ("coin", max_delay)
        while d > 0:
            yield ("mark", "backoff")
            d -= 1


def cohort_acquire(me: int, c: int, max_delay: int = 1) -> Iterator:
    yield ("write", ("next", me), NIL)  # @line L1
    yield ("write", ("state", me), WAIT)
    pred = yield ("swap", ("tail", c), me)  # @line L2
    if pred is not NIL:  # @line L3
        yield ("write", ("next", pred), me)
        del pred
        st = WAIT
        while st == WAIT:
            st = yield ("read", ("state", me))
        if st == GLOBAL:
            return  # the global lock came with the local lock
        del st
    yield from global_acquire(max_delay)  # @line L4
    yield ("mark", "global")
    yield ("write", ("count", c), 0)  # @line L5


def cohort_release(me: int, c: int, bound: int) -> Iterator:
    succ = yield ("read", ("next", me))  # @line L6
    if succ is NIL and (yield ("read", ("tail", c))) != me:
        while succ is NIL:  # a cohort member has joined: wait for its link
            succ = yield ("read", ("next", me))
    if succ is not NIL:
        k = yield ("read", ("count", c))  # @line L7
        if k < bound:
            yield ("write", ("count", c), k + 1)
            yield ("write", ("state", succ), GLOBAL)
            return
        del k
    yield ("write", "G", False)  # @line L8
    if succ is NIL:  # @line L9
        if (yield ("cas", ("tail", c), me, NIL)):
            return
        while succ is NIL:
            succ = yield ("read", ("next", me))
    yield ("write", ("state", succ), ACQ)


def client(cluster_of: list, bound: int, rounds: int | None = 1, max_delay: int = 1):
    """A process factory: process p lives in cluster cluster_of[p]."""
    cluster_of = tuple(cluster_of)

    def make(pid: int) -> Iterator:
        c = cluster_of[pid]
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from cohort_acquire(pid, c, max_delay)
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from cohort_release(pid, c, bound)
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make
