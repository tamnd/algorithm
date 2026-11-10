# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coffman-graham-algorithm/. The authors are listed in prov/7X27J2.jsonl.


def topological_order(succ: list[set[int]]) -> list[int]:
    """Return the jobs in an order where each arc goes forward. Raises ValueError on a cycle."""
    n = len(succ)
    indeg = [0] * n
    for v in range(n):
        for w in succ[v]:
            indeg[w] += 1
    stack = [v for v in range(n) if indeg[v] == 0]
    order = []
    while stack:
        v = stack.pop()
        order.append(v)
        for w in succ[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    if len(order) != n:
        raise ValueError("the precedence graph has a cycle")
    return order


def transitive_reduction(succ: list[set[int]]) -> list[set[int]]:
    """Keep the arc v -> w only if no other path leads from v to w. Cost O(n (n + e))."""
    n = len(succ)
    order = topological_order(succ)
    reach: list[set[int]] = [set() for _ in range(n)]
    for v in reversed(order):
        for w in succ[v]:
            reach[v].add(w)
            reach[v] |= reach[w]
    return [{w for w in succ[v] if not any(w in reach[u] for u in succ[v] if u != w)} for v in range(n)]


def coffman_graham_labels(succ: list[set[int]]) -> list[int]:
    """Return the Coffman-Graham labels 1..n of a transitively reduced DAG.

    At each step, among the unlabeled jobs whose immediate successors all have
    labels, the job whose decreasing list of successor labels is
    lexicographically smallest gets the next label. Ties go to the smaller
    job index. Cost O(n^2 + n e) comparisons of label lists in this direct form.
    """
    n = len(succ)
    label = [0] * n
    for k in range(1, n + 1):  # @line L2
        ready = [j for j in range(n) if label[j] == 0 and all(label[w] for w in succ[j])]  # @line L3
        key = {j: sorted((label[w] for w in succ[j]), reverse=True) for j in ready}  # @line L4
        best = min(ready, key=lambda j: (key[j], j))  # @line L5
        label[best] = k  # @line L6
    return label


def coffman_graham(succ: list[set[int]], m: int) -> list[int]:
    """Schedule unit jobs with precedence succ on m identical machines.

    succ[v] is the set of jobs that must wait for v. The result is the slot of
    each job: job v runs in [slot[v] - 1, slot[v]). The schedule is optimal
    for m = 2 and has makespan at most (2 - 2/m) OPT for m >= 2.
    Precondition: succ is acyclic and m >= 1.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    n = len(succ)
    red = transitive_reduction(succ)  # @line L1
    label = coffman_graham_labels(red)
    waiting = [0] * n
    for v in range(n):
        for w in red[v]:
            waiting[w] += 1
    slot = [0] * n
    avail = [v for v in range(n) if waiting[v] == 0]
    t, done = 0, 0  # @line L7
    while done < n:  # @line L8
        t += 1  # @line L9
        avail.sort(key=lambda v: -label[v])
        batch, avail = avail[:m], avail[m:]  # @line L10
        for v in batch:
            slot[v] = t
            done += 1
        for v in batch:
            for w in red[v]:
                waiting[w] -= 1
                if waiting[w] == 0:
                    avail.append(w)
    return slot  # @line L11
