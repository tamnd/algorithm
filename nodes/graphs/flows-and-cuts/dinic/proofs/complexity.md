---
title: Dinic's algorithm runs in O(n^2 m) time
proves: [time.worst]
status: full
---

Fix a run on a network with $n$ vertices and $m$ edges, and assume, as for every maximum flow bound stated in terms of $m$, that $m \ge n - 1$ after removing the vertices that no edge touches; otherwise add $O(n)$ to each bound. Each arithmetic operation and comparison costs $O(1)$.

**Theorem 1 (phases).** There are at most $n$ runs of line L3. By Claim 5 of the correctness proof, $d_f(t)$ grows by at least 1 in each phase, and it lies in $\{1, \dots, n - 1\}$ while the loop continues, so there are at most $n - 1$ phases and one final search.

**Theorem 2 (one phase costs O(nm)).** Line L1 costs $O(m)$ once. Line L3 is a breadth-first search over at most $2m$ arcs: $O(n + m)$. Line L5 costs $O(n)$. In the loop of lines L7 to L14:

- lines L12 and L14 each move a pointer one arc forward, and there are $2m$ arcs, so they run at most $2m$ times in all, at $O(1)$ each;
- line L9 runs at most $m$ times (Claim 4 of the correctness proof) and costs $O(|P|) = O(n)$ each time, since $|P| = d(t) \le n - 1$;
- line L11 adds an arc to $P$, and each arc added to $P$ leaves it later by line L9 (at most $n - 1$ arcs per run, already counted) or by line L14 (one arc per run). So line L11 runs at most $(n - 1) \cdot m + 2m$ times;
- line L13 runs once.

So the loop costs $O(nm + m) = O(nm)$, and one phase costs $O(n + m + nm) = O(nm)$.

**Theorem 3 (total).** By Theorems 1 and 2 the time is $O(n \cdot nm) = O(n^2 m)$. The arrays $c_f$, the adjacency lists, $\text{level}$, $it$, the queue and $P$ take $\Theta(n + m)$ space. Nothing in the count uses integrality, so the bound holds for real capacities. $\blacksquare$
