# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierholzer-algorithm/. The authors are listed in prov/0QG3S6.jsonl.


def hierholzer_algorithm(
    n: int, edges: list[tuple[int, int]], directed: bool = False
) -> tuple[list[int], list[int]] | None:
    """Return an Eulerian trail of the graph, or None if it has none.

    The graph has the vertices 0 .. n-1 and the edges edges[i] = (u, v), numbered by i.
    It may have parallel edges, self-loops and isolated vertices; if directed is True,
    edge (u, v) goes from u to v. The result is (walk, trail): walk lists the m + 1
    vertices and trail lists the m edge numbers, and trail[i] joins walk[i] to walk[i+1].
    The trail is closed whenever an Eulerian circuit exists. Time O(n + m), extra space
    O(n + m).
    """
    m = len(edges)
    if n == 0:
        return ([], []) if m == 0 else None
    inc: list[list[int]] = [[] for _ in range(n)]
    bal = [0] * n  # out - in if directed, degree if undirected
    for e, (u, v) in enumerate(edges):
        inc[u].append(e)
        if directed:
            bal[u] += 1
            bal[v] -= 1
        else:
            inc[v].append(e)
            bal[u] += 1
            bal[v] += 1
    # L1: degree condition; L2: choose the start vertex
    if directed:
        plus = [v for v in range(n) if bal[v] == 1]
        minus = [v for v in range(n) if bal[v] == -1]
        if any(abs(b) > 1 for b in bal) or len(plus) != len(minus) or len(plus) > 1:  # @line L1
            return None
        odd = plus
    else:
        odd = [v for v in range(n) if bal[v] % 2 == 1]
        if len(odd) not in (0, 2):  # @line L1
            return None
    if odd:  # @line L2
        s = odd[0]
    else:
        s = next((v for v in range(n) if inc[v]), 0)
    used = [False] * m  # @line L3
    nxt = [0] * n
    stack: list[tuple[int, int]] = [(s, -1)]  # @line L4
    out: list[tuple[int, int]] = []
    while stack:  # @line L5
        v, _ = stack[-1]  # @line L6
        while nxt[v] < len(inc[v]) and used[inc[v][nxt[v]]]:  # @line L7
            nxt[v] += 1
        if nxt[v] < len(inc[v]):  # @line L8
            f = inc[v][nxt[v]]  # @line L9
            used[f] = True
            a, b = edges[f]
            w = b if a == v else a
            stack.append((w, f))  # @line L10
        else:
            out.append(stack.pop())  # @line L11
    if len(out) < m + 1:  # @line L12
        return None
    out.reverse()  # @line L13
    return [v for v, _ in out], [f for _, f in out[1:]]
