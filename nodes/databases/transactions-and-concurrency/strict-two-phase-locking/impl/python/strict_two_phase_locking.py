# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strict-two-phase-locking/. The authors are listed in prov/4829PV.jsonl.

"""Strict and rigorous two-phase locking, as a simulator with real values.

A program is a list of actions (op, item) with op "r" or "w". A read takes a
shared lock (S), a write takes an exclusive lock (X), and a write by a
transaction that already holds S upgrades it. Strict 2PL holds every X lock
until the transaction commits or aborts; it may release an S lock once it is
past its lock point and will not touch the item again. Rigorous 2PL holds
every lock until the end.

A write stores a value that depends on everything the attempt has read, so
the final state shows exactly which reads each write saw. A transaction can
abort on its own (a user abort) at a planned point; the scheduler undoes its
writes from the before images and restarts it. Deadlocks are found in the
wait-for graph, and the youngest transaction on a cycle is aborted and
restarted in the same way.
"""

import random

Program = list[tuple[str, str]]


def write_value(t: int, k: int, seen: tuple) -> tuple:
    """The value that action number k of T_t writes after reading seen."""
    return ("f", t, k, seen)


def run_serial(programs: dict[int, Program], order: list[int], initial: dict) -> tuple[dict, dict]:
    """Run the programs one after the other. Return (final state, reads)."""
    db = dict(initial)
    reads: dict[int, list] = {}
    for t in order:
        seen: list = []
        for k, (op, x) in enumerate(programs[t]):
            if op == "r":
                seen.append(db[x])
            else:
                db[x] = write_value(t, k, tuple(seen))
        reads[t] = seen
    return db, reads


def run_strict_2pl(
    programs: dict[int, Program],
    initial: dict,
    rng: random.Random | None = None,
    script: list[int] | None = None,
    rigorous: bool = False,
    user_aborts: dict[int, int] | None = None,
    max_steps: int = 100000,
) -> dict:
    """Run the programs under strict (or rigorous) 2PL.

    user_aborts maps a transaction to the position in its program at which
    its first attempt aborts on its own (len(program) means just before the
    commit). With script, transactions step in that order and then the
    smallest runnable one steps; with rng, a random runnable one steps.

    Returns a dict with:
      schedule:     executed actions (op, txn, item), with "c" and "a" entries
      committed:    the reads and writes of the committed attempts
      commit_order: the transactions in commit order
      lock_point:   the step at which each committed attempt got its last lock
      reads:        the values that each committed attempt read
      final:        the final database state
      events:       the lock trace
    """
    plan = dict(user_aborts or {})
    db = dict(initial)
    held: dict[str, dict[int, str]] = {x: {} for x in initial}
    pc = {t: 0 for t in programs}
    seen: dict[int, list] = {t: [] for t in programs}
    undo: dict[int, list] = {t: [] for t in programs}
    shrinking = {t: False for t in programs}
    lock_point: dict[int, int] = {}
    done: list[int] = []
    reads: dict[int, list] = {}
    schedule: list = []
    events: list = []
    step = 0
    queue = list(script or [])

    def need(t: int) -> dict[str, str]:
        out: dict[str, str] = {}
        for op, x in programs[t]:
            if op == "w" or x not in out:
                out[x] = "X" if op == "w" else "S"
        return out

    def has(t: int, x: str, m: str) -> bool:
        h = held[x].get(t)
        return h == "X" or h == m

    def blocked_on(t: int) -> set[int]:
        if t in done or pc[t] == len(programs[t]):
            return set()
        op, x = programs[t][pc[t]]
        m = "X" if op == "w" else "S"
        if has(t, x, m):
            return set()
        return {u for u, um in held[x].items() if u != t and (m == "X" or um == "X")}

    def release_all(t: int) -> None:
        for x in sorted(held):
            if t in held[x]:
                del held[x][t]
                events.append(("unlock", t, x))

    def abort(t: int) -> None:
        for x, before in reversed(undo[t]):  # @line L9
            db[x] = before
        release_all(t)
        schedule.append(("a", t, None))
        events.append(("abort", t))
        pc[t] = 0
        seen[t] = []
        undo[t] = []
        shrinking[t] = False
        lock_point.pop(t, None)

    def on_cycles() -> list[int]:
        live = [t for t in programs if t not in done]
        edges = {t: blocked_on(t) for t in live}
        found = []
        for t in live:
            reach, stack = set(), list(edges[t])
            while stack:
                v = stack.pop()
                if v not in reach:
                    reach.add(v)
                    stack.extend(edges[v])
            if t in reach:
                found.append(t)
        return found

    def try_step(t: int) -> bool:
        nonlocal step
        if plan.get(t) == pc[t]:
            del plan[t]
            abort(t)
            return True
        if pc[t] == len(programs[t]):
            schedule.append(("c", t, None))
            release_all(t)  # @line L8
            done.append(t)
            reads[t] = seen[t]
            return True
        op, x = programs[t][pc[t]]
        m = "X" if op == "w" else "S"  # @line L1
        if not has(t, x, m):  # @line L2
            assert not shrinking[t], "a lock request after a release breaks two-phase locking"
            if blocked_on(t):  # @line L3
                return False
            held[x][t] = m  # @line L5
            events.append(("lock", t, x, m))
            step += 1
            if all(has(t, y, my) for y, my in need(t).items()):
                lock_point[t] = step
        if op == "r":  # @line L6
            seen[t].append(db[x])
        else:
            undo[t].append((x, db[x]))
            db[x] = write_value(t, pc[t], tuple(seen[t]))
        schedule.append((op, t, x))
        pc[t] += 1
        if not rigorous and t in lock_point:  # @line L7
            rest = {y for _, y in programs[t][pc[t] :]}
            for y in sorted(held):
                if held[y].get(t) == "S" and y not in rest:
                    del held[y][t]
                    shrinking[t] = True
                    events.append(("unlock", t, y))
        return True

    for _ in range(max_steps):
        live = [t for t in programs if t not in done]
        if not live:
            break
        cyc = on_cycles()
        if cyc:  # @line L4
            abort(max(cyc))
            continue
        moved = False
        while queue and not moved:
            t = queue.pop(0)
            if t not in done:
                moved = try_step(t)
                if not moved:
                    queue.insert(0, t)
                    break
        if moved:
            continue
        runnable = [t for t in live if not blocked_on(t)]
        assert runnable, "every transaction waits, so the wait-for graph has a cycle"
        try_step(min(runnable) if rng is None else rng.choice(runnable))
    else:
        raise RuntimeError("step limit reached")

    last_abort = {p[1]: i for i, p in enumerate(schedule) if p[0] == "a"}
    committed = [p for i, p in enumerate(schedule) if p[0] in "rw" and i > last_abort.get(p[1], -1)]
    return {
        "schedule": schedule,
        "committed": committed,
        "commit_order": done,
        "lock_point": lock_point,
        "reads": reads,
        "final": db,
        "events": events,
    }


def is_strict(schedule: list) -> bool:
    """No item written by T_j is read or written by another transaction before T_j ends."""
    dirty: dict[str, set[int]] = {}
    for op, t, x in schedule:
        if op in "ca":
            for owners in dirty.values():
                owners.discard(t)
        elif dirty.get(x, set()) - {t}:
            return False
        elif op == "w":
            dirty.setdefault(x, set()).add(t)
    return True
