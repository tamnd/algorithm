# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-locking/. The authors are listed in prov/JSBTG5.jsonl.

"""Basic two-phase locking (Eswaran, Gray, Lorie and Traiger 1976), as a simulator.

A program is a list of actions (op, item) with op "r" or "w". The scheduler
takes a shared lock (S) before a read and an exclusive lock (X) before a write,
upgrading S to X when the same transaction writes an item it has read. A
transaction gets its locks in a growing phase. Once it holds every lock it
will need (its lock point), it may release a lock on an item that it will not
touch again; after its first release it never asks for a lock again. At the
end it commits and releases the rest. Before each step the scheduler looks
for a cycle in the wait-for graph (a deadlock); the youngest transaction on a
cycle is aborted and restarted. A blocked transaction is still in its growing
phase and has released nothing, so its abort undoes writes that no other
transaction has seen.
"""

import random

Program = list[tuple[str, str]]


class LockTable:
    """Locks per item: a map from transaction to mode "S" or "X"."""

    def __init__(self) -> None:
        self.held: dict[str, dict[int, str]] = {}

    def mode(self, t: int, x: str) -> str | None:
        return self.held.get(x, {}).get(t)

    def blockers(self, t: int, x: str, m: str) -> set[int]:
        """The other transactions whose lock on x conflicts with mode m."""
        return {u for u, um in self.held.get(x, {}).items() if u != t and (m == "X" or um == "X")}

    def grant(self, t: int, x: str, m: str) -> None:
        self.held.setdefault(x, {})[t] = m

    def release(self, t: int, x: str) -> None:
        self.held[x].pop(t)

    def items_of(self, t: int) -> list[str]:
        return sorted(x for x, h in self.held.items() if t in h)


def needs(prog: Program) -> dict[str, str]:
    """The strongest mode that the program needs on each item."""
    out: dict[str, str] = {}
    for op, x in prog:
        if op == "w" or x not in out:
            out[x] = "X" if op == "w" else "S"
    return out


def run_2pl(
    programs: dict[int, Program],
    rng: random.Random | None = None,
    script: list[int] | None = None,
    p_release: float = 0.5,
    max_steps: int = 100000,
) -> dict:
    """Run the programs under basic 2PL.

    With script, the transactions step in that order (then round robin), and
    each one releases a lock as soon as two-phase rules allow it. With rng,
    a random unblocked transaction steps, and it releases an unneeded lock
    with probability p_release at each step.

    Returns a dict with:
      schedule:   executed actions (op, txn, item), with "c" and "a" entries
      committed:  the committed projection (reads and writes of the last attempts)
      lock_point: the step at which each committed transaction got its last lock
      events:     the lock trace ("lock", t, x, mode), ("unlock", t, x)
      aborts:     the number of deadlock aborts
    """
    locks = LockTable()
    pc = {t: 0 for t in programs}
    need = {t: needs(p) for t, p in programs.items()}
    shrinking = {t: False for t in programs}
    lock_point: dict[int, int] = {}
    done: set[int] = set()
    schedule: list = []
    events: list = []
    aborts = 0
    step = 0
    queue = list(script or [])

    def past_lock_point(t: int) -> bool:
        return all(
            locks.mode(t, x) == m or (m == "S" and locks.mode(t, x) == "X") for x, m in need[t].items()
        )

    def unneeded(t: int) -> list[str]:
        rest = {x for _, x in programs[t][pc[t] :]}
        return [x for x in locks.items_of(t) if x not in rest]

    def blocked_on(t: int) -> set[int]:
        if pc[t] == len(programs[t]):
            return set()
        op, x = programs[t][pc[t]]
        m = "X" if op == "w" else "S"
        have = locks.mode(t, x)
        if have == "X" or have == m:
            return set()
        return locks.blockers(t, x, m)

    def try_step(t: int, eager: bool) -> bool:
        """One move of t. Return False if t is blocked."""
        nonlocal step
        if past_lock_point(t) and (eager or (rng is not None and rng.random() < p_release)):
            for x in unneeded(t):
                locks.release(t, x)
                shrinking[t] = True
                events.append(("unlock", t, x))
        if pc[t] == len(programs[t]):  # @line L9
            for x in locks.items_of(t):
                locks.release(t, x)
                events.append(("unlock", t, x))
            schedule.append(("c", t, None))
            done.add(t)
            return True
        op, x = programs[t][pc[t]]
        m = "X" if op == "w" else "S"  # @line L1
        if locks.mode(t, x) not in (m, "X"):  # @line L2
            assert not shrinking[t], "a lock request after a release breaks two-phase locking"  # @line L3
            if blocked_on(t):  # @line L4
                return False
            locks.grant(t, x, m)  # @line L6
            events.append(("lock", t, x, m))
            step += 1
            if past_lock_point(t):
                lock_point[t] = step
        schedule.append((op, t, x))  # @line L7
        pc[t] += 1
        if eager and past_lock_point(t):  # @line L8
            for x in unneeded(t):
                locks.release(t, x)
                shrinking[t] = True
                events.append(("unlock", t, x))
        return True

    def on_cycles() -> list[int]:
        """The transactions that lie on a cycle of the wait-for graph."""
        live = [t for t in programs if t not in done]
        edges = {t: blocked_on(t) for t in live}
        found = []
        for t in live:
            seen, stack = set(), list(edges[t])
            while stack:
                v = stack.pop()
                if v not in seen:
                    seen.add(v)
                    stack.extend(edges[v])
            if t in seen:
                found.append(t)
        return found

    for _ in range(max_steps):
        live = [t for t in programs if t not in done]
        if not live:
            break
        cyc = on_cycles()  # deadlock detection on the wait-for graph
        if cyc:  # @line L5
            # Abort the youngest transaction on any cycle. The oldest live
            # transaction is never chosen, so restarts cannot starve it.
            victim = max(cyc)
            for x in locks.items_of(victim):
                locks.release(victim, x)
                events.append(("unlock", victim, x))
            schedule.append(("a", victim, None))
            events.append(("abort", victim))
            pc[victim] = 0
            shrinking[victim] = False
            lock_point.pop(victim, None)
            aborts += 1
            continue
        moved = False
        while queue and not moved:
            t = queue.pop(0)
            if t not in done:
                moved = try_step(t, eager=True)
                if not moved:
                    queue.insert(0, t)
                    break
        if moved:
            continue
        runnable = [t for t in live if not blocked_on(t)]
        assert runnable, "every transaction waits, so the wait-for graph has a cycle"
        if rng is None:
            try_step(min(runnable), eager=True)
        else:
            try_step(rng.choice(runnable), eager=False)
    else:
        raise RuntimeError(f"step limit reached; last actions {schedule[-12:]}, locks {locks.held}")

    committed = []
    for i, p in enumerate(schedule):
        if p[0] in "rw" and not any(q == ("a", p[1], None) for q in schedule[i + 1 :]):
            committed.append(p)
    return {
        "schedule": schedule,
        "committed": committed,
        "lock_point": lock_point,
        "events": events,
        "aborts": aborts,
    }
