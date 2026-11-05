---
title: The Dulmage-Mendelsohn decomposition runs in O((n + m) n^(1/2)) time
proves: [time.worst]
status: full
---

Let $G = (X \cup Y, E)$ have $n$ vertices and $m$ edges, stored as adjacency lists on both sides. Each operation on an index, a mark or a queue costs $O(1)$ on the [word RAM](/word-ram/).

**Line L1.** [Hopcroft-Karp](/hopcroft-karp/) finds a maximum matching in $O((n + m)\sqrt n)$ time and $\Theta(n + m)$ space.

**Lines L2 to L6.** In the search from the free left vertices, a left vertex is enqueued only when it is marked, and it is marked at most once, so at most $|X|$ vertices are dequeued. A dequeued vertex scans its adjacency list once, at $O(1)$ per edge, including the lookup of $\text{mate}[y]$ in line L5. So the search costs $O(n + m)$, and so does the mirror search of line L6.

**Lines L7 and L8.** $V_0$ is found by one pass over the marks, $O(n)$. $H$ has at most $|X|$ nodes and at most one arc per edge, built by one pass over the adjacency lists of $X_0$: $O(n + m)$.

**Lines L9 to L11.** [Tarjan's algorithm](/tarjan-scc/) runs in time linear in the size of $H$, $O(n + m)$, and reversing its output costs $O(n)$. Line L10 looks up one mate per left vertex, and writing the parts costs $O(n)$.

**Total.** $O((n + m)\sqrt n) + O(n + m) = O((n + m)\sqrt n)$ time. The space is the graph, the mate arrays, the marks, the queues, $H$ and Tarjan's stack, all $O(n + m)$, and the graph itself needs $\Omega(n + m)$, so it is $\Theta(n + m)$. $\blacksquare$
