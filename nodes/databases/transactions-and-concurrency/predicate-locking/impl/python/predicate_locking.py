# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predicate-locking/. The authors are listed in prov/THBP05.jsonl.

"""Predicate locking with box predicates, compared with locks on rows.

A row is a dict of integer attributes. A predicate is a box: a dict that maps
some attributes to a closed interval (lo, hi). An attribute that the box does
not name is unconstrained. A row with id r and values v is locked as the point
box {"id": (r, r), a: (v, v), ...}, so it intersects a box P exactly when the
row satisfies P.

Actions of a transaction:
  ("select", P)       read the rows that satisfy P        S lock on P
  ("insert", r, row)  add row r                           X lock on the new point
  ("update", r, row)  replace the values of row r         X on the old and new points
  ("delete", r)       remove row r                        X on the old point
An update or delete of a row that does not exist reads the predicate "id = r"
(S lock on {"id": (r, r)}) and does nothing.

Two locks conflict when they belong to different transactions, at least one
is X, and their boxes intersect. All locks are held until commit. A deadlock
is found in the wait-for graph; the youngest transaction on a cycle aborts,
its writes are undone and it restarts.

The scheme "tuple" locks row ids instead of boxes, which lets phantoms in.
"""

import random

INF = float("inf")


def interval(box: dict, a: str) -> tuple:
    return box.get(a, (-INF, INF))


def intersects(p: dict, q: dict) -> bool:
    """Do the boxes p and q share a point?"""
    for a in set(p) | set(q):  # @line L1
        lo1, hi1 = interval(p, a)
        lo2, hi2 = interval(q, a)
        if max(lo1, lo2) > min(hi1, hi2):  # @line L2
            return False
    return True  # @line L3


def satisfies(rid: int, row: dict, p: dict) -> bool:
    values = dict(row, id=rid)
    return all(lo <= values.get(a, 0) <= hi for a, (lo, hi) in p.items())


def point(rid: int, row: dict) -> dict:
    box = {a: (v, v) for a, v in row.items()}
    box["id"] = (rid, rid)
    return box


def select(table: dict, p: dict) -> list:
    return sorted((r, tuple(sorted(row.items()))) for r, row in table.items() if satisfies(r, row, p))


def apply(table: dict, act: tuple) -> None:
    if act[0] == "insert":
        table[act[1]] = dict(act[2])
    elif act[0] == "update" and act[1] in table:
        table[act[1]] = dict(act[2])
    elif act[0] == "delete":
        table.pop(act[1], None)


class PredicateLockManager:
    """A lock table of (transaction, mode, box) entries."""

    def __init__(self) -> None:
        self.locks: list[tuple[int, str, dict]] = []

    def blockers(self, t: int, mode: str, box: dict) -> set[int]:
        """The transactions whose locks conflict with a request of t."""
        out = set()
        for u, m, b in self.locks:  # @line L4
            if u != t and "X" in (m, mode) and intersects(b, box):  # @line L5
                out.add(u)
        return out

    def grant(self, t: int, mode: str, box: dict) -> None:
        if (t, mode, box) not in self.locks:
            self.locks.append((t, mode, box))  # @line L6

    def release(self, t: int) -> None:
        self.locks = [e for e in self.locks if e[0] != t]  # @line L7


def needed(act: tuple, table: dict, scheme: str) -> list[tuple[str, object]]:
    """The locks that an action needs, as (mode, box) or (mode, row id)."""
    kind = act[0]
    if scheme == "tuple":
        if kind == "select":
            return [("S", r) for r, _ in select(table, act[1])]
        return [("X", act[1])]
    if kind == "select":
        return [("S", act[1])]  # the predicate itself
    r = act[1]
    if kind == "insert":
        return [("X", point(r, act[2]))]
    if r not in table:
        return [("S", {"id": (r, r)})]  # read "row r exists"
    need = [("X", point(r, table[r]))]  # the old value
    if kind == "update":
        need.append(("X", point(r, act[2])))  # the new value
    return need


def run(
    programs: dict[int, list],
    initial: dict[int, dict],
    scheme: str = "predicate",
    rng: random.Random | None = None,
    script: list[int] | None = None,
    max_steps: int = 100000,
) -> dict:
    """Run the programs under strict 2PL with predicate locks or row locks."""
    assert scheme in ("predicate", "tuple")
    table = {r: dict(row) for r, row in initial.items()}
    lm = PredicateLockManager()
    rows_held: list[tuple[int, str, int]] = []  # row locks of the tuple scheme
    pc = {t: 0 for t in programs}
    results: dict[int, list] = {t: [] for t in programs}
    undo: dict[int, list] = {t: [] for t in programs}
    done: list[int] = []
    schedule: list = []
    queue = list(script or [])

    def blockers(t: int) -> set[int]:
        if t in done or pc[t] == len(programs[t]):
            return set()
        out = set()
        for mode, obj in needed(programs[t][pc[t]], table, scheme):
            if scheme == "predicate":
                out |= lm.blockers(t, mode, obj)
            else:
                out |= {u for u, m, r in rows_held if u != t and r == obj and "X" in (m, mode)}
        return out

    def release(t: int) -> None:
        nonlocal rows_held
        lm.release(t)
        rows_held = [e for e in rows_held if e[0] != t]

    def on_cycles() -> list[int]:
        live = [t for t in programs if t not in done]
        edges = {t: blockers(t) for t in live}
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

    def step(t: int) -> None:
        if pc[t] == len(programs[t]):
            release(t)  # commit
            done.append(t)
            schedule.append(("c", t))
            return
        act = programs[t][pc[t]]
        for mode, obj in needed(act, table, scheme):
            if scheme == "predicate":
                lm.grant(t, mode, obj)
            else:
                rows_held.append((t, mode, obj))
        if act[0] == "select":
            results[t].append(select(table, act[1]))
        else:
            r = act[1]
            undo[t].append((r, dict(table[r]) if r in table else None))
            apply(table, act)
        schedule.append((act[0], t) + tuple(act[1:2]))
        pc[t] += 1

    for _ in range(max_steps):
        live = [t for t in programs if t not in done]
        if not live:
            break
        cyc = on_cycles()
        if cyc:
            v = max(cyc)  # the youngest transaction on a cycle
            for r, old in reversed(undo[v]):
                if old is None:
                    table.pop(r, None)
                else:
                    table[r] = old
            undo[v], results[v], pc[v] = [], [], 0
            release(v)
            schedule.append(("a", v))
            continue
        runnable = [t for t in live if not blockers(t)]
        while queue and queue[0] in done:
            queue.pop(0)
        if queue and queue[0] in runnable:
            step(queue.pop(0))
        else:
            step(min(runnable) if rng is None or queue else rng.choice(runnable))
    else:
        raise RuntimeError("step limit reached")
    return {"results": results, "schedule": schedule, "commit_order": done, "table": table}


def run_serial(programs: dict[int, list], initial: dict[int, dict], order: list[int]) -> tuple[dict, dict]:
    """The select results and final table when the programs run one by one."""
    table = {r: dict(row) for r, row in initial.items()}
    results: dict[int, list] = {}
    for t in order:
        results[t] = []
        for act in programs[t]:
            if act[0] == "select":
                results[t].append(select(table, act[1]))
            else:
                apply(table, act)
    return results, table
