---
title: Smallest-last ordering computes the degeneracy in linear time
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph with $n$ vertices and $m$ edges. For $k = 1, \ldots, n + 1$, let $R_k$ be the set of vertices removed before round $k$ of the loop of line L3, and let $G_k = G - R_k$. The degeneracy of $G$ is $\mathrm{dgn}(G) = \max \{ \delta(H) : H \subseteq G,\ V(H) \ne \emptyset \}$, and $0$ when $n = 0$.

**Claim.** SMALLEST-LAST$(G)$ stops after $n$ rounds. The returned order $v_1, \ldots, v_n$ lists each vertex once, $v_k$ has minimum degree in $G_k$, and the returned $d$ satisfies $d = \max_k \deg_{G_k}(v_k) = \mathrm{dgn}(G)$. Each $v_k$ has at most $d$ neighbors among $v_{k+1}, \ldots, v_n$. The time is $O(n + m)$.

**Invariant.** At the start of round $k$ (before line L4):

> **(S)** $R_k = \{v_1, \ldots, v_{k-1}\}$ is the set of marked vertices. For each $w \notin R_k$, $\deg[w] = \deg_{G_k}(w)$ and $w$ lies in the bucket $B[\deg[w]]$, and no bucket holds a marked vertex. Every bucket $B[j]$ with $j < i$ is empty. Also $0 \le i$, and $i \le \delta(G_k)$ when $G_k$ is not empty.

*Initialization.* For $k = 1$, $R_1 = \emptyset$ and $G_1 = G$. Line L1 sets $\deg[v] = \deg_G(v)$ and puts each vertex in $B[\deg[v]]$. Line L2 sets $i = 0$, and no bucket has index below 0.

*Maintenance.* Fix round $k \le n$. Then $G_k$ has $n - k + 1 \ge 1$ vertices, so some bucket is non-empty, and by (S) each non-empty bucket has index at least $i$. Line L4 raises $i$ to the smallest index $j$ with $B[j] \ne \emptyset$. The vertices of $G_k$ are exactly the bucket contents and each $w$ is in $B[\deg_{G_k}(w)]$, so this smallest $j$ is $\delta(G_k)$. Line L5 takes $v_k$ from $B[\delta(G_k)]$, so $\deg_{G_k}(v_k) = \delta(G_k) = i$, and line L6 marks it and sets $d$ to $\max(d, \deg_{G_k}(v_k))$.

Now $G_{k+1} = G_k - v_k$. A vertex $w$ of $G_{k+1}$ has $\deg_{G_{k+1}}(w) = \deg_{G_k}(w) - 1$ if $w$ is adjacent to $v_k$, and $\deg_{G_k}(w)$ otherwise. Lines L7 and L8 visit exactly the unmarked neighbors of $v_k$, each once because $G$ is simple, and move each one down by one bucket. So the degree and bucket parts of (S) hold for $G_{k+1}$, and $v_k$ is in no bucket. Each degree fell by at most 1, so $\delta(G_{k+1}) \ge \delta(G_k) - 1 = i - 1$. Every bucket below $i - 1$ was empty and received no vertex, because a vertex moves from $B[j]$ to $B[j - 1]$ only for $j \ge i$. Line L9 sets $i$ to $\max(i - 1, 0)$, which gives (S) for round $k + 1$.

*Termination.* Each round marks one new vertex, and the loop of line L4 stops because a non-empty bucket exists. So the algorithm stops after $n$ rounds, and $v_1, \ldots, v_n$ is an order of $V$.

**The value of $d$.** By the maintenance step, $d = \max_k \delta(G_k)$ at the end.

- $d \le \mathrm{dgn}(G)$: each $G_k$ with $k \le n$ is a non-empty subgraph of $G$.
- $d \ge \mathrm{dgn}(G)$: let $H$ be a non-empty subgraph of $G$, and let $k$ be the smallest index with $v_k \in V(H)$. Then $V(H) \subseteq V(G_k)$, so $H \subseteq G_k$, and $\delta(H) \le \deg_H(v_k) \le \deg_{G_k}(v_k) = \delta(G_k) \le d$.

**Later neighbors.** The neighbors of $v_k$ among $v_{k+1}, \ldots, v_n$ are its neighbors in $G_k$, and there are $\deg_{G_k}(v_k) \le d$ of them. So greedy coloring in the order $v_n, \ldots, v_1$ sees at most $d$ colored neighbors at each vertex and uses at most $d + 1$ colors.

**Time.** Line L1 costs $O(n + m)$. Lines L5, L6 and L9 cost $O(1)$ per round. Lines L7 and L8 scan the list of $v_k$ once in round $k$, so $\sum_v \deg(v) = 2m$ steps of $O(1)$ in total, with buckets that support insertion and deletion in $O(1)$. For line L4, let $I$ be the number of increments of $i$. The value $i$ starts at 0, falls by at most 1 in each of the $n$ rounds, and stays at most $n - 1$, since a degree in a graph of at most $n$ vertices is at most $n - 1$. So $I \le (n - 1) + n$, and the tests of line L4 cost $O(n + I) = O(n)$. The total is $O(n + m)$. $\blacksquare$
