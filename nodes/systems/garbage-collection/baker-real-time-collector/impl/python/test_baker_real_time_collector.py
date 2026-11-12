# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baker-real-time-collector/. The authors are listed in prov/DE61E5.jsonl.

import random

import pytest

from baker_real_time_collector import Baker, CollectorBehind


class Shadow:
    """The same mutator on an abstract heap with no collector: the oracle."""

    def __init__(self, registers: int, fields: int) -> None:
        self.heap: dict[int, list[int | None]] = {}
        self.regs: list[int | None] = [None] * registers
        self.p = fields
        self.names = 0

    def reachable(self) -> dict[int, list[int | None]]:
        seen: dict[int, list[int | None]] = {}
        stack = [r for r in self.regs if r is not None]
        while stack:
            a = stack.pop()
            if a not in seen:
                seen[a] = list(self.heap[a])
                stack.extend(y for y in self.heap[a] if y is not None)
        return seen


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def step(gc: Baker, sh: Shadow, op: tuple) -> None:
    kind = op[0]
    if kind == "load":
        _, i, j, f = op
        if sh.regs[j] is not None:
            sh.regs[i] = sh.heap[sh.regs[j]][f]
        gc.op_load(i, j, f)
    elif kind == "store":
        _, i, f, j = op
        if sh.regs[i] is not None:
            sh.heap[sh.regs[i]][f] = sh.regs[j]
        gc.op_store(i, f, j)
    elif kind == "move":
        _, i, j = op
        sh.regs[i] = sh.regs[j]
        gc.regs[i] = gc.regs[j]
    elif kind == "clear":
        sh.regs[op[1]] = None
        gc.regs[op[1]] = None
    else:
        sh.heap[sh.names] = [None] * sh.p
        sh.regs[op[1]] = sh.names
        sh.names += 1
        gc.op_alloc(op[1])


def check(gc: Baker, sh: Shadow, live: int) -> None:
    # The to-space invariant: the mutator never holds a from-space address.
    assert all(r is None or gc.in_to_space(r) for r in gc.regs)
    # The collector keeps exactly the reachable graph, by logical name.
    regs, graph = gc.logical_graph()
    assert regs == sh.regs
    assert graph == sh.reachable()
    assert len(graph) <= live


def random_run(gc: Baker, live: int, steps: int, rng: random.Random) -> None:
    sh = Shadow(len(gc.regs), gc.p)
    r = len(gc.regs)
    for _ in range(steps):
        x = rng.random()
        if x < 0.4:
            if len(sh.reachable()) < live:
                step(gc, sh, ("alloc", rng.randrange(r)))
        elif x < 0.65:
            step(gc, sh, ("load", rng.randrange(r), rng.randrange(r), rng.randrange(gc.p)))
        elif x < 0.85:
            step(gc, sh, ("store", rng.randrange(r), rng.randrange(gc.p), rng.randrange(r)))
        elif x < 0.95:
            step(gc, sh, ("move", rng.randrange(r), rng.randrange(r)))
        else:
            step(gc, sh, ("clear", rng.randrange(r)))
        check(gc, sh, live)


def queue_run(gc: Baker, live: int, steps: int) -> None:
    """A FIFO list of `live` cells: r0 is the head, r1 the tail, r2 the new cell."""
    sh = Shadow(len(gc.regs), gc.p)
    for _ in range(steps):
        if sh.regs[0] is not None and len(sh.reachable()) >= live:
            step(gc, sh, ("load", 0, 0, 0))  # drop the head
        step(gc, sh, ("alloc", 2))
        if sh.regs[0] is None:
            step(gc, sh, ("move", 0, 2))
        else:
            step(gc, sh, ("store", 1, 0, 2))
        step(gc, sh, ("move", 1, 2))
        step(gc, sh, ("clear", 2))
        check(gc, sh, live)


@pytest.mark.parametrize("seed", range(6))
def test_bound_holds_on_random_mutators(seed: int) -> None:
    live, k = 12, 3
    size = live + ceil_div(live, k)  # 16, the smallest semispace the bound allows
    gc = Baker(size, registers=4, k=k)
    random_run(gc, live, 3000, random.Random(seed))
    assert gc.flips >= 20
    assert gc.max_scans <= k and gc.max_copied <= live


def test_bound_for_many_parameters() -> None:
    rng = random.Random(42)
    for _ in range(30):
        live = rng.randrange(3, 20)
        k = rng.randrange(1, 6)
        gc = Baker(live + ceil_div(live, k), registers=3, k=k, fields=rng.randrange(1, 4))
        random_run(gc, live, 600, rng)
        assert gc.max_copied <= live


def test_queue_at_the_bound() -> None:
    # L = 16 and k = 2 need S = 16 + 8 = 24.
    gc = Baker(24, registers=3, k=2, fields=1)
    queue_run(gc, 16, 2000)
    assert gc.flips == 220 and gc.max_copied <= 16 and gc.max_scans == 2


def test_queue_falls_behind_when_k_is_too_small() -> None:
    # k = 1 would need S = 32; with S = 24 the scan does not end in time.
    gc = Baker(24, registers=3, k=1, fields=1)
    with pytest.raises(CollectorBehind):
        queue_run(gc, 16, 2000)
    assert gc.flips == 1
    # The bound is sufficient, not tight: this workload needs S = 30.
    queue_run(Baker(30, registers=3, k=1, fields=1), 16, 2000)
    with pytest.raises(CollectorBehind):
        queue_run(Baker(29, registers=3, k=1, fields=1), 16, 2000)


def test_new_cells_are_black_and_old_ones_are_copied_once() -> None:
    gc = Baker(8, registers=2, k=1)
    a = gc.allocate()  # to-space is [0, 8); new cells grow down from 7
    assert a == 7 and gc.top == 7
    gc.regs[0] = a
    b = gc.allocate()
    gc.mem[a][0] = b
    gc.mem[b][1] = a  # a cycle a <-> b
    for _ in range(6):
        gc.allocate()  # garbage
    assert gc.top == gc.copy == 0
    gc.allocate()  # the flip: to-space is now [8, 16)
    assert gc.flips == 1 and gc.regs[0] == 8
    assert gc.forward == {7: 8, 6: 9}  # the root was copied, then one scan step copied b
    assert gc.mem[8] == [9, None] and gc.mem[9] == [None, 7]  # b is still gray
    assert gc.load(9, 1) == 8  # the read barrier follows the forwarding address
