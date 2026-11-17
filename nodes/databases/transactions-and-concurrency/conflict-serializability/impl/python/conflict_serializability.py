# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-serializability/. The authors are listed in prov/YBK3Q3.jsonl.

"""Conflict serializability of a schedule, by the conflict graph and by brute force.

A schedule is a list of actions (op, txn, item) with op "r" or "w". Two actions
conflict when they belong to different transactions, touch the same item and at
least one of them is a write. Pass the committed projection of a schedule.
"""

import itertools
from collections import Counter, deque

Action = tuple[str, int, str]


def parse(text: str) -> list[Action]:
    """Parse "r1(x) w2(x)" into actions."""
    return [(t[0], int(t[1 : t.index("(")]), t[t.index("(") + 1 : -1]) for t in text.split()]


def conflict(p: Action, q: Action) -> bool:
    return p[1] != q[1] and p[2] == q[2] and "w" in (p[0], q[0])


def _tag(s: list[Action]) -> list[tuple[Action, int]]:
    """Give the k-th action of each transaction the number k, so that equal actions differ."""
    count: Counter = Counter()
    out = []
    for p in s:
        count[p[1]] += 1
        out.append((p, count[p[1]]))
    return out


def conflict_pairs(s: list[Action]) -> set[tuple]:
    """The ordered pairs (a, b) of conflicting actions with a before b."""
    t = _tag(s)
    return {(a, b) for i, a in enumerate(t) for b in t[i + 1 :] if conflict(a[0], b[0])}


def conflict_equivalent(s1: list[Action], s2: list[Action]) -> bool:
    """Same actions, and every pair of conflicting actions in the same order."""
    return Counter(s1) == Counter(s2) and conflict_pairs(s1) == conflict_pairs(s2)


def transactions(s: list[Action]) -> list[int]:
    return sorted({p[1] for p in s})


def serial(s: list[Action], order) -> list[Action]:
    """The serial schedule that runs the transactions of s in the given order."""
    return [p for t in order for p in s if p[1] == t]


def serialization_order(s: list[Action]) -> list[int] | None:
    """A serial order that s is conflict equivalent to, or None.

    Build the conflict graph and take a topological order (Kahn's algorithm,
    smallest ready transaction first). None means the graph has a cycle.
    """
    succ: dict[int, set[int]] = {t: set() for t in transactions(s)}
    by_item: dict[str, list[Action]] = {}
    for p in s:
        for q in by_item.setdefault(p[2], []):
            if conflict(q, p):
                succ[q[1]].add(p[1])
        by_item[p[2]].append(p)
    indeg = Counter(w for v in succ for w in succ[v])
    ready = deque(sorted(v for v in succ if indeg[v] == 0))
    order = []
    while ready:
        v = ready.popleft()
        order.append(v)
        for w in sorted(succ[v]):
            indeg[w] -= 1
            if indeg[w] == 0:
                ready.append(w)
    return order if len(order) == len(succ) else None


def is_conflict_serializable(s: list[Action]) -> bool:
    return serialization_order(s) is not None


def brute_force_orders(s: list[Action]) -> list[tuple[int, ...]]:
    """All serial orders whose serial schedule is conflict equivalent to s."""
    return [o for o in itertools.permutations(transactions(s)) if conflict_equivalent(s, serial(s, o))]


def swap_closure(s: list[Action]) -> set[tuple[Action, ...]]:
    """All schedules reachable from s by swapping adjacent actions that are
    from different transactions and do not conflict. Exponential: tiny inputs only."""
    start = tuple(s)
    seen = {start}
    todo = [start]
    while todo:
        cur = todo.pop()
        for i in range(len(cur) - 1):
            a, b = cur[i], cur[i + 1]
            if a[1] != b[1] and not conflict(a, b):
                nxt = cur[:i] + (b, a) + cur[i + 2 :]
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
    return seen
