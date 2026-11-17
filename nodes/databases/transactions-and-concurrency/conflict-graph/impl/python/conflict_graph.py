# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-graph/. The authors are listed in prov/R82KKG.jsonl.

"""The conflict graph (precedence graph) of a schedule.

A schedule is a list of actions (op, txn, item). op is "r" or "w" for a read or
a write of item, and "c" or "a" for the commit or abort of txn (item is None).
Two actions conflict when they belong to different transactions, touch the same
item, and at least one of them is a write.
"""

from collections import Counter

Action = tuple[str, int, str | None]


def parse(text: str) -> list[Action]:
    """Parse "r1(x) w2(x) c1 a2" into actions."""
    out: list[Action] = []
    for tok in text.split():
        if "(" in tok:
            out.append((tok[0], int(tok[1 : tok.index("(")]), tok[tok.index("(") + 1 : -1]))
        else:
            out.append((tok[0], int(tok[1:]), None))
    return out


def committed_projection(schedule: list[Action]) -> list[Action]:
    """Keep the reads and writes of committed transactions.

    A schedule with no commit and no abort counts as all committed.
    """
    if not any(op in "ca" for op, _, _ in schedule):
        return [p for p in schedule if p[0] in "rw"]
    done = {t for op, t, _ in schedule if op == "c"}
    return [p for p in schedule if p[0] in "rw" and p[1] in done]


def conflict(p: Action, q: Action) -> bool:
    """True when p and q conflict."""
    return (
        p[0] in "rw"
        and q[0] in "rw"
        and p[1] != q[1]
        and p[2] == q[2]
        and "w" in (p[0], q[0])
    )


def conflict_graph(schedule: list[Action]) -> dict[int, set[int]]:
    """Map each transaction to the set of its successors.

    There is an edge Ti -> Tj when an action of Ti conflicts with a later
    action of Tj. Only reads and writes are used, so pass a committed
    projection if the schedule has aborts.
    """
    graph: dict[int, set[int]] = {}
    seen: dict[str, list[Action]] = {}
    for p in schedule:  # @line L3
        if p[0] not in "rw":
            continue
        graph.setdefault(p[1], set())
        earlier = seen.setdefault(p[2], [])
        for q in earlier:  # @line L4
            if conflict(q, p):
                graph[q[1]].add(p[1])  # @line L5
        earlier.append(p)  # @line L6
    return graph


def serial_order(graph: dict[int, set[int]]) -> list[int] | None:
    """A topological order of the graph (Kahn), or None if it has a cycle.

    Among the transactions that are ready, the one with the smallest number
    goes first, so the result is the same on each run.
    """
    indeg = {v: 0 for v in graph}
    for v in graph:
        for w in graph[v]:
            indeg[w] += 1
    ready = sorted(v for v in graph if indeg[v] == 0)
    order: list[int] = []
    while ready:
        v = ready.pop(0)
        order.append(v)
        for w in sorted(graph[v]):
            indeg[w] -= 1
            if indeg[w] == 0:
                ready.append(w)
        ready.sort()
    return order if len(order) == len(graph) else None


def find_cycle(graph: dict[int, set[int]]) -> list[int] | None:
    """A cycle [v1, v2, ..., vk] with edges v1->v2, ..., vk->v1, or None.

    Iterative depth-first search with white (0), gray (1) and black (2).
    """
    color = {v: 0 for v in graph}
    parent: dict[int, int] = {}
    for root in sorted(graph):
        if color[root]:
            continue
        color[root] = 1
        stack = [(root, iter(sorted(graph[root])))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                color[v] = 2
                stack.pop()
            elif color[w] == 0:
                color[w] = 1
                parent[w] = v
                stack.append((w, iter(sorted(graph[w]))))
            elif color[w] == 1:
                cycle = [v]
                while cycle[-1] != w:
                    cycle.append(parent[cycle[-1]])
                return cycle[::-1]
    return None


def serial_schedule(schedule: list[Action], order: list[int]) -> list[Action]:
    """The serial schedule that runs the transactions of schedule in order."""
    return [p for t in order for p in schedule if p[1] == t]


def conflict_equivalent(s1: list[Action], s2: list[Action]) -> bool:
    """Same actions, and each conflicting pair in the same order."""
    if Counter(s1) != Counter(s2):
        return False

    def ordered_pairs(s: list[Action]) -> set[tuple]:
        # Number the k-th action of each transaction, so equal actions differ.
        count: dict[int, int] = {}
        tagged = []
        for p in s:
            count[p[1]] = count.get(p[1], 0) + 1
            tagged.append((p, count[p[1]]))
        return {
            (a, b)
            for i, a in enumerate(tagged)
            for b in tagged[i + 1 :]
            if conflict(a[0], b[0])
        }

    return ordered_pairs(s1) == ordered_pairs(s2)
