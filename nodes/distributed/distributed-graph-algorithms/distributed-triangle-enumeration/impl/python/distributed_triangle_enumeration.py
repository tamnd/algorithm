# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-triangle-enumeration/. The authors are listed in prov/7GRAF4.jsonl.

"""Triangle listing in the congested clique by a partition of the nodes
(the plan of Dolev, Lenzen and Peled).

Let q be the integer cube root of n. Node v is in part v mod q. Node t < q^3
is the receiver of the ordered triple (a, b, c) with t = a q^2 + b q + c, and
it lists each triangle x < y < z with x, y, z in the parts a, b, c. Each
triangle has one such triple, so it is listed once. The receiver needs one
bit for each pair it must test: (x, y) with x < y in parts (a, b), (b, c)
and (a, c). For each pair one end reports the bit: x reports {x, y} if
(y - x) mod n is in 1 .. floor(n/2), with ties at n/2 to the smaller end.
All nodes know this schedule, so a message holds only bits and no labels.

The bits travel in two phases: each bit goes from its reporter to a relay,
and then from the relay to its receiver. The relays come from a fixed plan
(relay_plan) that keeps the load of each link near the mean. In each phase a link
carries at most B = ceil(log2 n) bits per round. The rounds of a phase are
the largest load of a link, divided by B and rounded up.
"""

import math


def cube_root(n: int) -> int:
    q = round(n ** (1 / 3))
    while q**3 > n:
        q -= 1
    while (q + 1) ** 3 <= n:
        q += 1
    return q


def reporter(x: int, y: int, n: int) -> int:
    d = (y - x) % n
    if 2 * d < n or (2 * d == n and x < y):
        return x
    return y


def schedule(n: int) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """For each (reporter, receiver), the pairs it reports, in a fixed order."""
    q = cube_root(n)
    parts = [[v for v in range(n) if v % q == a] for a in range(q)]
    out: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for t in range(q**3):
        a, b, c = t // (q * q), (t // q) % q, t % q
        need = set()
        for p1, p2 in ((a, b), (b, c), (a, c)):
            for x in parts[p1]:
                for y in parts[p2]:
                    if x < y:
                        need.add((x, y))
        for x, y in sorted(need):
            out.setdefault((reporter(x, y, n), t), []).append((x, y))
    return out


def relay_plan(n: int, sched: dict[tuple[int, int], list[tuple[int, int]]]) -> tuple[dict[tuple[int, int], list[int]], int]:
    """Choose a relay for each bit so that no link carries more than cap bits
    in either phase, with cap = ceil(Delta / n) + 1, where Delta is the most
    bits that one node sends or receives. The plan depends only on n, so
    every node computes the same plan with no communication. Reporter x scans
    the relays round robin from where it stopped, and takes the first relay r
    with room on the link x -> r and on the link r -> t. A hop from a node to
    itself uses no link."""
    out = [0] * n
    inn = [0] * n
    for (x, t), pairs in sched.items():
        out[x] += len(pairs)
        inn[t] += len(pairs)
    delta = max(max(out), max(inn))
    cap = -(-delta // n) + 1
    l1: dict[tuple[int, int], int] = {}
    l2: dict[tuple[int, int], int] = {}
    ptr = list(range(n))
    plan: dict[tuple[int, int], list[int]] = {}
    for (x, t), pairs in sorted(sched.items()):
        rs = []
        for _ in pairs:
            for step in range(n):
                r = (ptr[x] + step) % n
                ok1 = r == x or l1.get((x, r), 0) < cap
                ok2 = r == t or l2.get((r, t), 0) < cap
                if ok1 and ok2:
                    break
            else:
                raise RuntimeError("no relay with room")
            if r != x:
                l1[(x, r)] = l1.get((x, r), 0) + 1
            if r != t:
                l2[(r, t)] = l2.get((r, t), 0) + 1
            ptr[x] = (r + 1) % n
            rs.append(r)
        plan[(x, t)] = rs
    return plan, cap


def clique_triangles(n: int, edges: list[tuple[int, int]]) -> dict:
    """Return the listed triangles (with the lister of each), the rounds of the
    two phases, the message size B, the largest link loads and the bits."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    q = cube_root(n)
    B = max(1, math.ceil(math.log2(n)))
    sched = schedule(n)
    load1: dict[tuple[int, int], int] = {}
    load2: dict[tuple[int, int], int] = {}
    at_relay: dict[int, dict[tuple[int, int, int], bool]] = {r: {} for r in range(n)}
    total = 0
    plan, cap = relay_plan(n, sched)
    # phase 1: each reporter sends each bit to the relay that the plan gives
    for (x, t), pairs in sorted(sched.items()):
        for j, (u, v) in enumerate(pairs):
            bit = v in adj[u]  # the reporter x is u or v, so it knows this bit
            r = plan[(x, t)][j]
            if r != x:
                load1[(x, r)] = load1.get((x, r), 0) + 1
            at_relay[r][(x, t, j)] = bit
            total += 1
    # phase 2: each relay forwards each bit to its receiver
    known: dict[int, set[tuple[int, int]]] = {t: set() for t in range(q**3)}
    for r in range(n):
        for (x, t, j), bit in at_relay[r].items():
            if r != t:
                load2[(r, t)] = load2.get((r, t), 0) + 1
            if bit:
                known[t].add(sched[(x, t)][j])
    # local work: each receiver lists the triangles of its triple
    listed: list[tuple[tuple[int, int, int], int]] = []
    for t in range(q**3):
        a, b, c = t // (q * q), (t // q) % q, t % q
        e = known[t]
        for x, y in e:
            if x % q != a or y % q != b:
                continue
            for z in range(y + 1, n):
                if z % q == c and (y, z) in e and (x, z) in e:
                    listed.append(((x, y, z), t))
    m1 = max(load1.values(), default=0)
    m2 = max(load2.values(), default=0)
    rounds = (math.ceil(m1 / B), math.ceil(m2 / B))
    return {
        "triangles": listed,
        "q": q,
        "B": B,
        "max_load": (m1, m2),
        "rounds": rounds,
        "total_rounds": sum(rounds),
        "bits": total,
        "cap": cap,
    }


def brute_triangles(n: int, edges: list[tuple[int, int]]) -> set[tuple[int, int, int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return {(x, y, z) for x in range(n) for y in adj[x] if y > x for z in adj[y] if z > y and z in adj[x]}
