# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-exclusion-lower-bounds/. The authors are listed in prov/44E0B1.jsonl.
"""The covering run of the Burns-Lynch proof for two processes.

An algorithm is given by a function ``act(i, pc)`` that returns the next step
of process i (0 or 1) in the local state pc:

    ("r", reg, nxt)         read the register reg; the next state is nxt(value)
    ("w", reg, value, pc2)  write value to reg; the next state is pc2
    ("cs",)                 the process is in the critical section

Each process starts at the beginning of its entry section in the state 0, and
the shared memory starts as the dict ``init``. The processes are deterministic.

``covering_run`` builds the run of the proof on the page: process 0 runs alone
until it is about to write a register R (it covers R), process 1 runs alone
until it enters, then process 0 does its write and runs alone. If process 1
wrote no register other than R, the run ends with both processes in the
critical section. Cost: O(L) steps, where L bounds the length of a solo run.
"""
from __future__ import annotations

CS, WRITE, NEVER = "cs", "write", "never"


def _key(pc, mem: dict) -> tuple:
    return pc, tuple(sorted(mem.items()))


def solo(act, i: int, pc, mem: dict, stop_at_write: bool, limit: int = 10000):
    """Run process i alone from (pc, mem). Changes mem in place.

    Stops when the process is in the critical section (CS), when it is about
    to write and stop_at_write is set (WRITE), or when its state repeats or
    the limit is hit (NEVER: it does not enter alone).
    Returns (status, pc, run, written) where run lists the process of each
    step and written is the set of registers that it wrote.
    """
    run, written, seen = [], set(), set()
    for _ in range(limit):
        a = act(i, pc)
        if a[0] == "cs":
            return CS, pc, run, written
        if a[0] == "w" and stop_at_write:
            return WRITE, pc, run, written
        k = _key(pc, mem)
        if k in seen:
            return NEVER, pc, run, written
        seen.add(k)
        if a[0] == "w":
            mem[a[1]] = a[2]
            written.add(a[1])
            pc = a[3]
        else:
            pc = a[2](mem[a[1]])
        run.append(i)
    return NEVER, pc, run, written


def covering_run(act, init: dict, limit: int = 10000) -> dict:
    """Build the covering run for processes p = 0 and q = 1.

    Returns a dict with the key "result":
      "violation": "run" (a list of process ids) ends with both in the CS;
      "escape": q wrote a register that p does not cover ("covered", "q_writes");
      "p alone does not enter" or "q alone does not enter": the algorithm is
      not deadlock free, so the theorem says nothing about it.
    """
    p, q = 0, 1
    st, _, _, _ = solo(act, p, 0, dict(init), False, limit)
    if st != CS:
        return {"result": "p alone does not enter"}
    mem = dict(init)
    st, pc_p, alpha, _ = solo(act, p, 0, mem, True, limit)
    covered = act(p, pc_p)[1] if st == WRITE else None
    # Now p covers the register `covered` (or p is already in the CS), and the memory is still init.
    assert mem == init
    st, _, sigma, q_writes = solo(act, q, 0, mem, False, limit)
    if st != CS:
        return {"result": "q alone does not enter"}
    if covered is None:
        # p entered without a write, so q could not see it.
        return {"result": "violation", "covered": None, "run": alpha + sigma}
    if q_writes - {covered}:
        return {"result": "escape", "covered": covered, "q_writes": q_writes}
    st, _, rest, _ = solo(act, p, pc_p, mem, False, limit)
    # The write of p hides every write of q, so p goes on as when it was alone.
    assert st == CS
    return {"result": "violation", "covered": covered, "run": alpha + sigma + rest}


def replay(act, init: dict, run: list) -> tuple:
    """Run the steps in run (a list of process ids) from the start; return (pcs, mem)."""
    pcs, mem = [0, 0], dict(init)
    for i in run:
        a = act(i, pcs[i])
        assert a[0] != "cs", "a process in the CS takes no step here"
        if a[0] == "w":
            mem[a[1]] = a[2]
            pcs[i] = a[3]
        else:
            pcs[i] = a[2](mem[a[1]])
    return tuple(pcs), mem


def can_both_enter(act, init: dict, limit: int = 200000) -> bool:
    """Search all interleavings of one entry of each process; True if both can be in the CS."""
    start = (0, 0, tuple(sorted(init.items())))
    seen, stack = {start}, [start]
    while stack:
        pc0, pc1, items = stack.pop()
        pcs = (pc0, pc1)
        if all(act(i, pcs[i])[0] == "cs" for i in (0, 1)):
            return True
        for i in (0, 1):
            a = act(i, pcs[i])
            if a[0] == "cs":
                continue
            mem = dict(items)
            new = list(pcs)
            if a[0] == "w":
                mem[a[1]] = a[2]
                new[i] = a[3]
            else:
                new[i] = a[2](mem[a[1]])
            s = (new[0], new[1], tuple(sorted(mem.items())))
            if s not in seen:
                if len(seen) > limit:
                    raise RuntimeError("too many states")
                seen.add(s)
                stack.append(s)
    return False
