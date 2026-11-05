# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-scc/. The authors are listed in prov/JH9ZVM.jsonl.


def tarjan_scc(adj: list[list[int]]) -> list[int]:
    """Return comp, where comp[v] is the number of the strongly connected component of v.

    The graph is directed, with vertices 0 .. n-1 and adjacency lists adj. Parallel
    arcs (repeated entries) and self-loops (v in adj[v]) are allowed. The components
    are numbered 0, 1, ... in the order their roots finish, which is a reverse
    topological order of the condensation: for each arc (u, v), comp[u] >= comp[v].
    The recursion of STRONGCONNECT is replaced by an explicit stack of frames
    (v, i), where i is the position of the next arc of v to scan.
    Time O(n + m), extra space O(n).
    """
    n = len(adj)
    index = [-1] * n  # @line L1
    low = [0] * n
    on_stack = [False] * n
    stack: list[int] = []
    comp = [-1] * n
    counter = 0
    k = 0
    call: list[tuple[int, int]] = []

    def enter(v: int) -> None:
        nonlocal counter
        index[v] = low[v] = counter  # @line L5
        counter += 1
        stack.append(v)  # @line L6
        on_stack[v] = True
        call.append((v, 0))

    for u in range(n):  # @line L2
        if index[u] != -1:  # @line L3
            continue
        enter(u)
        while call:
            v, i = call[-1]
            if i < len(adj[v]):
                call[-1] = (v, i + 1)
                w = adj[v][i]  # @line L7
                if index[w] == -1:  # @line L8
                    enter(w)  # @line L9
                elif on_stack[w]:  # @line L10
                    low[v] = min(low[v], index[w])
                continue
            call.pop()  # STRONGCONNECT(v) ends here
            if low[v] == index[v]:  # @line L11
                while True:  # @line L12
                    w = stack.pop()  # @line L13
                    on_stack[w] = False
                    comp[w] = k
                    if w == v:
                        break
                k += 1  # @line L14
            if call:  # back in the parent p: the second half of line L9
                p = call[-1][0]
                low[p] = min(low[p], low[v])
    return comp  # @line L4
