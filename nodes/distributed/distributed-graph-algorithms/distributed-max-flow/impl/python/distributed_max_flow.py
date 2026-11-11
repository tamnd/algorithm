# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-max-flow/. The authors are listed in prov/6669RS.jsonl.

"""Synchronous push-relabel as a CONGEST algorithm (Goldberg and Tarjan).

Each node is a processor and knows only its own arcs. One pulse is two
rounds. In the first round each active node pushes the excess that it had at
the start of the pulse along admissible arcs, one message (an amount) per arc.
In the second round each node that still has excess left relabels to one more
than the smallest start label over its residual arcs, and every node that
changed its label tells its neighbours. Labels stay valid, so the run ends
with a maximum preflow that is a flow; the value is the excess at t.

The number of pulses depends on n and on the capacities, not on the diameter.
"""

from collections import deque


def push_relabel_pulses(n: int, arcs: list[tuple[int, int, int]], s: int, t: int) -> dict:
    """arcs: (u, v, c) with c > 0; an undirected edge is two arcs.
    Return the flow value, the flow on each arc pair, the pulses, the rounds
    and the messages."""
    cap: dict[tuple[int, int], int] = {}
    nbrs: list[set[int]] = [set() for _ in range(n)]
    for u, v, c in arcs:
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)
        nbrs[u].add(v)
        nbrs[v].add(u)
    flow = {e: 0 for e in cap}

    def res(u: int, v: int) -> int:
        return cap[(u, v)] - flow[(u, v)]

    def move(u: int, v: int, x: int) -> None:
        flow[(u, v)] += x
        flow[(v, u)] -= x

    d = [0] * n
    d[s] = n
    excess = [0] * n
    messages = 0
    for v in sorted(nbrs[s]):  # round 0: s saturates its arcs
        x = res(s, v)
        if x > 0:
            move(s, v, x)
            excess[v] += x
            excess[s] -= x
            messages += 1
    pulses = 0
    while True:
        active = [v for v in range(n) if v not in (s, t) and excess[v] > 0]
        if not active:
            break
        pulses += 1
        start = d[:]
        incoming = [0] * n
        left = {}
        # round 1 of the pulse: pushes, with the start labels and start excess
        for v in active:
            e = excess[v]
            for w in sorted(nbrs[v]):
                if e == 0:
                    break
                if start[v] == start[w] + 1 and res(v, w) > 0:
                    x = min(e, res(v, w))
                    move(v, w, x)
                    e -= x
                    incoming[w] += x
                    messages += 1
            left[v] = e
        for v in active:
            excess[v] = left[v]
        for w in range(n):
            excess[w] += incoming[w]
        # round 2 of the pulse: relabel the nodes that could not push it all
        for v in active:
            if left[v] > 0:
                d[v] = 1 + min(start[w] for w in nbrs[v] if res(v, w) > 0)
                messages += len(nbrs[v])
    value = excess[t]
    return {
        "value": value,
        "flow": flow,
        "pulses": pulses,
        "rounds": 1 + 2 * pulses,
        "messages": messages,
        "max_label": max(d),
    }


def edmonds_karp(n: int, arcs: list[tuple[int, int, int]], s: int, t: int) -> int:
    """The oracle: shortest augmenting paths."""
    cap: dict[tuple[int, int], int] = {}
    adj: list[set[int]] = [set() for _ in range(n)]
    for u, v, c in arcs:
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)
        adj[u].add(v)
        adj[v].add(u)
    total = 0
    while True:
        prev = {s: s}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for v in adj[u]:
                if v not in prev and cap[(u, v)] > 0:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return total
        x, v = min(cap[(prev[v], v)] for v in path_nodes(prev, s, t)), t
        while v != s:
            u = prev[v]
            cap[(u, v)] -= x
            cap[(v, u)] += x
            v = u
        total += x


def path_nodes(prev: dict[int, int], s: int, t: int) -> list[int]:
    out, v = [], t
    while v != s:
        out.append(v)
        v = prev[v]
    return out


def bottleneck_fan(k: int) -> tuple[int, list[tuple[int, int, int]], int, int]:
    """s joined to a path of k nodes with capacity k, and each path node but
    the first joined to t with capacity 1. The hop diameter is 2, but most
    excess must go back to s, so the labels must climb above n."""
    n = k + 2
    s, t = k, k + 1
    arcs = []
    for i in range(k):
        arcs += [(s, i, k), (i, s, k)]
        if i < k - 1:
            arcs += [(i, i + 1, k), (i + 1, i, k)]
        if i > 0:
            arcs += [(i, t, 1), (t, i, 1)]
    return n, arcs, s, t
