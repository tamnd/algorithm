# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thomas-write-rule/. The authors are listed in prov/NVC9CE.jsonl.

"""Timestamp ordering with the Thomas write rule (Thomas 1979).

The read rule is that of basic timestamp ordering. The write rule differs in
one case: a write that is late only because a younger transaction has
already written the item (and none has read it) is obsolete. It is skipped,
and its transaction goes on, instead of being rejected.

Also here: a brute-force test of view serializability, used by the tests to
check what the rule produces.
"""

from itertools import permutations


def start_timestamps(schedule: list) -> dict[int, int]:
    """Timestamps 1, 2, ... in the order in which transactions first appear."""
    ts: dict[int, int] = {}
    for _, t, _ in schedule:
        ts.setdefault(t, len(ts) + 1)
    return ts


def run_twr(schedule: list, ts: dict[int, int] | None = None) -> dict:
    """Feed a fixed schedule of (op, txn, item) to TO with the Thomas write rule.

    A rejected transaction aborts and its later actions are dropped. Returns
    a dict with executed (the actions that ran), ignored (the skipped writes,
    with their positions in the input) and rejected (a set of transactions).
    """
    ts = ts or start_timestamps(schedule)
    rts: dict[str, int] = {}
    wts: dict[str, int] = {}
    executed, ignored, rejected = [], [], set()
    for pos, (op, t, x) in enumerate(schedule):
        if t in rejected:
            continue
        if op == "r":
            if ts[t] < wts.get(x, 0):  # @line L4
                rejected.add(t)
                continue
            rts[x] = max(rts.get(x, 0), ts[t])  # @line L5
            executed.append((op, t, x))
        else:
            if ts[t] < rts.get(x, 0):  # @line L1
                rejected.add(t)  # a younger transaction read the old value
            elif ts[t] < wts.get(x, 0):  # @line L2
                ignored.append((pos, (op, t, x)))  # obsolete: skip it
            else:
                wts[x] = ts[t]  # @line L3
                executed.append((op, t, x))
    return {"executed": executed, "ignored": ignored, "rejected": rejected}


def reads_from(schedule: list) -> list:
    """For the k-th action of each reader, the transaction whose write it reads (0: initial)."""
    last: dict[str, int] = {}
    count: dict[int, int] = {}
    out = []
    for op, t, x in schedule:
        count[t] = count.get(t, 0) + 1
        if op == "r":
            out.append((t, count[t], x, last.get(x, 0)))
        else:
            last[x] = t
    return out


def final_writes(schedule: list) -> dict[str, int]:
    last: dict[str, int] = {}
    for op, t, x in schedule:
        if op == "w":
            last[x] = t
    return last


def view_of(schedule: list) -> tuple:
    """Reads-from (as a multiset, keyed by reader and item) and final writes."""
    return sorted(reads_from(schedule)), final_writes(schedule)


def serial(schedule: list, order: list[int]) -> list:
    return [p for t in order for p in schedule if p[1] == t]


def view_serial_orders(schedule: list) -> list[tuple]:
    """All serial orders that are view equivalent to the schedule (brute force)."""
    txns = sorted({p[1] for p in schedule})
    v = view_of(schedule)
    return [o for o in permutations(txns) if view_of(serial(schedule, list(o))) == v]


def conflict_serializable(schedule: list) -> bool:
    txns = {p[1] for p in schedule}
    edges = {
        (p[1], q[1])
        for i, p in enumerate(schedule)
        for q in schedule[i + 1 :]
        if p[1] != q[1] and p[2] == q[2] and "w" in (p[0], q[0])
    }
    indeg = {t: 0 for t in txns}
    for _, v in edges:
        indeg[v] += 1
    ready = [t for t in txns if indeg[t] == 0]
    seen = 0
    while ready:
        u = ready.pop()
        seen += 1
        for a, b in edges:
            if a == u:
                indeg[b] -= 1
                if indeg[b] == 0:
                    ready.append(b)
    return seen == len(txns)
