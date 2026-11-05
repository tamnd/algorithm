# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tremaux-traversal/. The authors are listed in prov/BKR094.jsonl.


def tremaux_traversal(
    n: int, edges: list[tuple[int, int]], s: int
) -> tuple[list[int], list[int | None]]:
    """Walk a maze by Tremaux's rules from s and return (walk, parent).

    The maze is the undirected multigraph with the vertices 0 .. n-1 and the passages
    edges[i] = (a, b); self-loops and parallel passages are allowed. At each vertex the
    passages are tried in the order of the edge list. The walk is the list of vertices
    visited by the walker, from s back to s; it uses each passage of the component of s
    exactly twice. parent[v] is the vertex from which v was first entered (None for s
    and for vertices outside the component). Time O(n + m), extra space O(n + m).
    """
    inc: list[list[int]] = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        inc[a].append(i)
        if b != a:
            inc[b].append(i)
    marks = [0] * len(edges)  # @line L1
    visited = [False] * n
    entry: list[int | None] = [None] * n
    parent: list[int | None] = [None] * n
    pos = [0] * n
    visited[s] = True
    v = s
    walk = [s]
    while True:  # @line L2
        while pos[v] < len(inc[v]) and marks[inc[v][pos[v]]] > 0:
            pos[v] += 1
        if pos[v] < len(inc[v]):  # @line L3
            e = inc[v][pos[v]]
            a, b = edges[e]
            w = b if a == v else a
            marks[e] = 1  # @line L4
            walk.append(w)
            if visited[w]:  # @line L5
                marks[e] = 2
                walk.append(v)
            else:
                visited[w] = True  # @line L6
                entry[w] = e
                parent[w] = v
                v = w
        elif entry[v] is not None:  # @line L7
            e = entry[v]
            marks[e] = 2  # @line L8
            a, b = edges[e]
            v = b if a == v else a
            walk.append(v)
        else:
            return walk, parent  # @line L9
