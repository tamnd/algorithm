# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t1-t2-reduction/. The authors are listed in prov/VPKTQX.jsonl.
"""The T1-T2 reduction of Hecht and Ullman.

t1_t2_reduce(n, edges, root) applies T1 (delete a self-loop) and T2 (merge a
vertex other than the root that has exactly one predecessor into that
predecessor) until neither applies. It returns (left, left_edges, steps):
the vertices and edges of the limit graph and the list of steps taken, each
("T1", v) or ("T2", v, u) for "v merged into u". Only the vertices that the
root reaches take part. The graph is reducible exactly when one vertex is
left; is_reducible says so, and cfg_is_reducible does it for a toy IR
program.
"""

import toyir


def t1_t2_reduce(n, edges, root):
    if n < 1 or not 0 <= root < n:
        raise ValueError("a flow graph needs n >= 1 vertices and a root in range")
    out = [[] for _ in range(n)]
    for a, b in edges:
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError("edge endpoint out of range")
        out[a].append(b)

    # Keep the vertices that root reaches, with successor and predecessor sets.
    seen = [False] * n  # @line L1
    seen[root] = True
    stack = [root]
    while stack:
        v = stack.pop()
        for w in out[v]:
            if not seen[w]:
                seen[w] = True
                stack.append(w)
    succ = {v: set() for v in range(n) if seen[v]}
    pred = {v: set() for v in succ}
    for a, b in edges:
        if seen[a]:
            succ[a].add(b)
            pred[b].add(a)

    steps = []
    work = sorted(succ, reverse=True)  # @line L2
    while work:  # @line L3
        v = work.pop()  # @line L4
        if v not in succ:
            continue
        if v in succ[v]:  # @line L5
            succ[v].discard(v)  # @line L6
            pred[v].discard(v)
            steps.append(("T1", v))
        if v != root and len(pred[v]) == 1:  # @line L7
            (u,) = pred[v]
            moved = succ[v]
            succ[u].discard(v)  # @line L8
            for w in moved:  # @line L9
                pred[w].discard(v)  # @line L10
                pred[w].add(u)
                succ[u].add(w)
            del succ[v], pred[v]  # @line L11
            steps.append(("T2", v, u))
            work.append(u)
            work.extend(moved)
    left = sorted(succ)  # @line L12
    left_edges = sorted((a, b) for a in succ for b in succ[a])
    return left, left_edges, steps


def is_reducible(n, edges, root):
    """True if T1 and T2 reduce the part that root reaches to one vertex."""
    return len(t1_t2_reduce(n, edges, root)[0]) == 1


def cfg_is_reducible(prog):
    """Reducibility of the control flow graph of a toy IR program."""
    labels = list(prog.blocks)
    index = {lab: i for i, lab in enumerate(labels)}
    edges = [(index[a], index[b]) for a, b in toyir.edges(prog)]
    return is_reducible(len(labels), edges, 0)
