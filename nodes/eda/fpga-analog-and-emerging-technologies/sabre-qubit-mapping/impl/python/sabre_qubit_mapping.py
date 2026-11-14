# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sabre-qubit-mapping/. The authors are listed in prov/2MX74V.jsonl.

"""SABRE qubit mapping, after Li, Ding and Xie (ASPLOS 2019).

A circuit is a list of gates on logical qubits 0..n-1. A gate is a tuple
(name, qubits), with one or two qubits, for example ("cx", (0, 2)). The
device is N physical qubits 0..N-1 and a list of undirected coupling edges.

A layout is a list: layout[a] is the physical qubit of logical qubit a.

The output of a pass is a list of operations on physical qubits:
("gate", i, (p,) or (p, q)) runs gate i of the input circuit, and
("swap", (p, q)) exchanges the states of p and q.

Besides the paper, the search has a release valve: after `limit` SWAPs in a
row with no gate run, it routes the closest gate of the front layer along a
shortest path. Without it the heuristic can cycle; with it every pass ends.
"""

import random
from collections import deque


def distances(n_phys, edges):
    """All-pairs shortest path lengths of the coupling graph, by BFS."""
    adj = [[] for _ in range(n_phys)]
    for p, q in edges:
        adj[p].append(q)
        adj[q].append(p)
    dist = []
    for s in range(n_phys):
        d = [None] * n_phys
        d[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if d[v] is None:
                    d[v] = d[u] + 1
                    queue.append(v)
        if any(x is None for x in d):
            raise ValueError("the coupling graph must be connected")
        dist.append(d)
    return adj, dist


def dependence_dag(gates):
    """Successors and the number of predecessors of every gate."""
    last = {}
    succ = [[] for _ in gates]
    npred = [0] * len(gates)
    for i, (_, qs) in enumerate(gates):
        preds = {last[a] for a in qs if a in last}
        for j in preds:
            succ[j].append(i)
        npred[i] = len(preds)
        for a in qs:
            last[a] = i
    return succ, npred


def swap_search(gates, layout, n_phys, adj, dist, rng, ext_size=20, weight=0.5,
                delta=0.001, decay_reset=5, limit=None):
    """One traversal of the circuit. Return (operations, final layout)."""
    layout = list(layout)
    owner = [None] * n_phys  # owner[p] is the logical qubit on p, or None
    for a, p in enumerate(layout):
        owner[p] = a
    if limit is None:
        limit = 10 * n_phys
    succ, npred = dependence_dag(gates)
    npred = list(npred)
    front = [i for i in range(len(gates)) if npred[i] == 0]  # @line L6
    ops = []
    decay = [1.0] * n_phys
    steps = 0  # search steps since the last reset of the decay
    stalled = 0  # SWAPs since the last gate was run

    def apply_swap(p, q):
        a, b = owner[p], owner[q]
        owner[p], owner[q] = b, a
        if a is not None:
            layout[a] = q
        if b is not None:
            layout[b] = p
        ops.append(("swap", (p, q)))

    def gate_dist(i, lay):
        a, b = gates[i][1]
        return dist[lay[a]][lay[b]]

    while front:  # @line L7
        ready = [i for i in front if len(gates[i][1]) == 1 or gate_dist(i, layout) == 1]
        if ready:  # @line L8
            for i in ready:
                front.remove(i)
                ops.append(("gate", i, tuple(layout[a] for a in gates[i][1])))
                for j in succ[i]:
                    npred[j] -= 1
                    if npred[j] == 0:
                        front.append(j)
            decay = [1.0] * n_phys
            steps = 0
            stalled = 0
            continue
        if stalled >= limit:  # @line L9
            # release valve: walk one qubit of the closest gate toward the other
            i = min(front, key=lambda g: (gate_dist(g, layout), g))
            a, b = gates[i][1]
            while dist[layout[a]][layout[b]] > 1:
                p = layout[a]
                q = min(v for v in adj[p] if dist[v][layout[b]] == dist[p][layout[b]] - 1)
                apply_swap(p, q)
            stalled = 0
            continue
        # the extended set: the first two-qubit gates after the front layer
        ext = []  # @line L10
        seen = set(front)
        left = {j: npred[j] for j in range(len(gates))}
        queue = deque(front)
        while queue and len(ext) < ext_size:
            i = queue.popleft()
            for j in succ[i]:
                left[j] -= 1
                if left[j] == 0 and j not in seen:
                    seen.add(j)
                    queue.append(j)
                    if len(gates[j][1]) == 2:
                        ext.append(j)
                        if len(ext) == ext_size:
                            break
        cands = set()
        for i in front:
            for a in gates[i][1]:
                p = layout[a]
                for q in adj[p]:
                    cands.add((min(p, q), max(p, q)))
        best, best_score = [], None
        for p, q in sorted(cands):  # @line L11
            lay = list(layout)
            a, b = owner[p], owner[q]
            if a is not None:
                lay[a] = q
            if b is not None:
                lay[b] = p
            h = sum(gate_dist(i, lay) for i in front) / len(front)
            if ext:
                h += weight * sum(gate_dist(i, lay) for i in ext) / len(ext)
            h *= max(decay[p], decay[q])
            if best_score is None or h < best_score - 1e-12:
                best, best_score = [(p, q)], h
            elif abs(h - best_score) <= 1e-12:
                best.append((p, q))
        p, q = rng.choice(best)
        apply_swap(p, q)  # @line L12
        stalled += 1
        steps += 1
        if steps % decay_reset == 0:
            decay = [1.0] * n_phys
        else:
            decay[p] += delta
            decay[q] += delta
    return ops, layout


def swap_count(ops):
    return sum(1 for op in ops if op[0] == "swap")


def sabre(n_log, gates, n_phys, edges, seed=0, trials=5, traversals=3, **kw):
    """Return (operations, initial layout, final layout) with the fewest SWAPs."""
    if n_log > n_phys:
        raise ValueError("more logical than physical qubits")
    if traversals % 2 == 0:
        raise ValueError("the number of traversals must be odd, so the last one is forward")
    rng = random.Random(seed)
    adj, dist = distances(n_phys, edges)  # @line L1
    reverse = list(reversed(gates))
    best = None
    for _ in range(trials):
        layout = rng.sample(range(n_phys), n_log)  # @line L2
        for t in range(traversals - 1):  # @line L3
            # forward, backward, forward, ...: the final layout of one pass
            # is the initial layout of the next
            _, layout = swap_search(gates if t % 2 == 0 else reverse, layout, n_phys, adj, dist, rng, **kw)
        start = layout
        ops, final = swap_search(gates, start, n_phys, adj, dist, rng, **kw)  # @line L4
        if best is None or swap_count(ops) < swap_count(best[0]):
            best = (ops, start, final)
    return best  # @line L5


def to_three_cnots(ops):
    """Expand every SWAP into three CNOTs, the middle one reversed."""
    out = []
    for op in ops:
        if op[0] == "swap":
            p, q = op[1]
            out += [("cx", (p, q)), ("cx", (q, p)), ("cx", (p, q))]
        else:
            out.append(op)
    return out
