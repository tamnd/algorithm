# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-path-based-scc/. The authors are listed in prov/X5MM3D.jsonl.


def strong_components(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], int]:
    """Gabow's path-based strong components of a directed graph on 0 .. n-1.

    Precondition: each edge (u, v) has 0 <= u, v < n. Loops and parallel edges are
    allowed. Returns (comp, c): comp[v] is the number of the component of v, and the
    components are numbered 0 .. c-1 in the order they close, which is a reverse
    topological order of the condensation. The search uses an explicit stack, and
    the time and the extra space are O(n + m).
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    pre = [0] * n  # @line L1
    comp = [-1] * n
    counter = 0
    count = 0
    s: list[int] = []  # the stack S of vertices with no component yet
    b: list[int] = []  # the boundary stack B of preorder numbers
    for r in range(n):  # @line L2
        if pre[r]:
            continue
        calls: list[tuple[int, int]] = []  # (vertex, index of its next edge)
        counter += 1  # @line L3
        pre[r] = counter
        s.append(r)  # @line L4
        b.append(pre[r])
        calls.append((r, 0))
        while calls:
            v, k = calls[-1]
            if k < len(adj[v]):  # @line L5
                calls[-1] = (v, k + 1)
                w = adj[v][k]
                if pre[w] == 0:  # @line L6
                    counter += 1
                    pre[w] = counter
                    s.append(w)
                    b.append(pre[w])
                    calls.append((w, 0))
                elif comp[w] < 0:  # @line L7
                    while pre[w] < b[-1]:  # @line L8
                        b.pop()
                continue
            calls.pop()
            if b[-1] == pre[v]:  # @line L9
                b.pop()  # @line L10
                while True:  # @line L11
                    x = s.pop()
                    comp[x] = count
                    if x == v:
                        break
                count += 1
    return comp, count
