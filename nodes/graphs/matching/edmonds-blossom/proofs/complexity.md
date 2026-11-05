---
title: Edmonds' blossom algorithm runs in O(n^3) time
proves: [time.worst]
status: full
---

Let $G$ have $n$ vertices and $m$ edges. The graph $G'$ is represented as in the implementation: the adjacency lists of $G$, an array $\text{base}$, the labels, the tree of each vertex, the array $\text{mate}$, and parent links. Each array access and comparison costs $O(1)$ on the [word RAM](/word-ram/).

**Phases.** By the termination argument of the correctness proof there are at most $\lfloor n/2 \rfloor + 1$ phases.

**Scanning.** In one phase each vertex is enqueued at most once, and when dequeued it scans its adjacency list once. The test of line L6 compares $\text{base}[v]$ with $\text{base}[w]$ and $\text{mate}[v]$ with $w$, line L7 reads two labels and two tree names, and line L11 sets a constant number of entries. So the scans cost $O(n + m)$ per phase, apart from the work of lines L8 and L10.

**Contractions.** Each contraction replaces the vertices of an odd cycle of $G'$, at least three of them, by one, so the number of vertices of $G'$ drops by at least 2, and there are at most $n/2$ contractions per phase. A contraction finds the base by walking from $v$ to the root and from $w$ upwards until the first marked vertex, following $\text{mate}$, the parent links and $\text{base}$: $O(n)$ steps. Marking the two paths costs $O(n)$, and the loop that sets $\text{base}[x] \leftarrow b$ for the vertices of the blossom and enqueues the formerly inner ones visits all $n$ vertices once: $O(n)$. So the contractions cost $O(n^2)$ per phase.

**Augmentation.** Line L8 follows $\text{mate}$ and the links from $v$ and from $w$ to their roots; each step visits a new vertex of the path, so this costs $O(n)$, and flipping the path costs $O(n)$ too.

**Total.** One phase costs $O(n + m + n^2) = O(n^2 + m)$, and all phases $O(n(n^2 + m))$. For a simple graph $m \le n^2/2$, which gives $O(n^3)$. The space is $\Theta(n + m)$: the adjacency lists and a constant number of arrays of length $n$, plus the queue, which holds each vertex at most once per phase. $\blacksquare$
