---
title: The Buss kernel returns an equivalent instance with at most k'^2 edges and k'^2 + k' vertices
proves: [correctness]
status: full
---

The input is a graph $G_0 = (V_0, E_0)$ and an integer $k_0 \ge 0$. For a graph $H$ we write $\tau(H)$ for the least size of a vertex cover of $H$, and we say that $(H, j)$ is a *yes-instance* when $j \ge 0$ and $\tau(H) \le j$. The fixed instance $(K_2, 0)$, one edge and budget 0, is a no-instance, because $\tau(K_2) = 1$.

**Lemma 1 (high degree).** Let $j \ge 0$ and let $v$ be a vertex of $H$ with $\deg_H(v) > j$. Then every vertex cover $S$ of $H$ with $|S| \le j$ contains $v$. Hence $(H, j)$ is a yes-instance if and only if $(H - v, j - 1)$ is one, and if $S'$ is a cover of $H - v$ then $S' \cup \{v\}$ is a cover of $H$.

*Proof.* Let $S$ be a cover with $|S| \le j$ and suppose $v \notin S$. Each edge $\{v, u\}$ has an endpoint in $S$, and it is not $v$, so $u \in S$. Then $S$ contains all neighbors of $v$, which are more than $j$ vertices, a contradiction. So $v \in S$.

If $(H, j)$ is a yes-instance, take a cover $S$ with $|S| \le j$. It contains $v$, and $S \setminus \{v\}$ covers every edge of $H - v$, because those edges do not meet $v$. So $\tau(H - v) \le j - 1$. Since $\tau(H - v) \ge 0$, this also gives $j - 1 \ge 0$, so $(H - v, j - 1)$ is a yes-instance. Conversely, if $S'$ covers $H - v$ with $|S'| \le j - 1$, then $S' \cup \{v\}$ covers each edge of $H - v$ by $S'$ and each edge at $v$ by $v$, and it has at most $j$ vertices. $\square$

**Lemma 2 (isolated vertices).** If $u$ is isolated in $H$, then $\tau(H - u) = \tau(H)$, and every cover of $H - u$ is a cover of $H$.

*Proof.* $H$ and $H - u$ have the same edges. $\square$

**Lemma 3 (size).** Let $j \ge 0$, and let $H$ have no isolated vertex and maximum degree at most $j$. If $\tau(H) \le j$, then $|E(H)| \le j^2$ and $|V(H)| \le j^2 + j$.

*Proof.* Take a cover $S$ with $|S| \le j$. Every edge has an endpoint in $S$, and each vertex of $S$ has at most $j$ edges, so $|E(H)| \le \sum_{s \in S} \deg(s) \le j \cdot j$. A vertex $u \notin S$ is not isolated, so it has an edge $\{u, s\}$, and $s \in S$ because the edge is covered and $u \notin S$. So every vertex outside $S$ is a neighbor of some vertex of $S$, and $|V(H) \setminus S| \le \sum_{s \in S} \deg(s) \le j^2$. Hence $|V(H)| \le j^2 + j$. $\square$

**Loop invariant.** Let $(G, k, F)$ be the values at the test of line L2. Then:

1. $G = G_0 - F$, and $|F| = k_0 - k$;
2. $(G_0, k_0)$ is a yes-instance if and only if $(G, k)$ is one (where $(G, k)$ with $k < 0$ counts as a no-instance);
3. if $S$ is a cover of $G$ with $|S| \le k$, then $S \cup F$ is a cover of $G_0$ with $|S \cup F| \le k_0$.

*Proof.* Before the loop, $F = \emptyset$, $G = G_0$ and $k = k_0$, so all three hold. Suppose they hold and the body at line L3 runs. Then $k \ge 0$ and $\deg_G(v) > k$. Line L3 sets $G \leftarrow G - v$, $F \leftarrow F \cup \{v\}$ and $k \leftarrow k - 1$. Part 1 holds again because $v \in V(G)$ is not in $F$. By Lemma 1 with $H = G$ and $j = k$, the instance $(G, k)$ is a yes-instance exactly when $(G - v, k - 1)$ is one, so part 2 holds. For part 3, let $S$ cover $G - v$ with $|S| \le k - 1$. By Lemma 1, $S \cup \{v\}$ covers $G$ and has at most $k$ vertices, and by the old part 3, $(S \cup \{v\}) \cup F$ covers $G_0$ and has at most $k_0$ vertices. $\square$

**Termination.** Each pass lowers $k$ by one, and the loop stops when $k < 0$. So it runs at most $k_0 + 1$ times.

**Theorem.** BUSS-KERNEL$(G_0, k_0)$ returns $((G', k'), F')$ such that:

1. $(G_0, k_0)$ is a yes-instance if and only if $(G', k')$ is one;
2. $0 \le k' \le k_0$, $|E(G')| \le k'^2$ and $|V(G')| \le k'^2 + k'$, unless the output is $(K_2, 0)$;
3. if the output is not $(K_2, 0)$ and $S'$ covers $G'$ with $|S'| \le k'$, then $S' \cup F'$ covers $G_0$ and $|S' \cup F'| \le k_0$.

*Proof.* When the loop stops, the invariant holds, and either $k < 0$ or every vertex of $G$ has degree at most $k$.

*Line L4.* If $k < 0$, then by part 2 of the invariant $(G_0, k_0)$ is a no-instance, and the output $(K_2, 0)$ is a no-instance too. Claim 1 holds, and claims 2 and 3 do not apply.

From now on $k \ge 0$, and every vertex of $G$ has degree at most $k$. *Line L5* deletes the isolated vertices. By Lemma 2 this keeps $\tau(G)$ and every cover, so the invariant still holds, and now $G$ has no isolated vertex and maximum degree at most $k$.

*Line L6.* If $|E(G)| > k^2$ or $|V(G)| > k^2 + k$, then by Lemma 3 with $H = G$ and $j = k$, $\tau(G) > k$. So $(G, k)$ is a no-instance, by part 2 of the invariant so is $(G_0, k_0)$, and the output $(K_2, 0)$ is correct.

*Line L7.* Otherwise the output is $(G, k)$ and $F$. Claim 1 is part 2 of the invariant. For claim 2, $k \ge 0$, $k = k_0 - |F| \le k_0$, and the failed test at line L6 gives $|E(G)| \le k^2$ and $|V(G)| \le k^2 + k$. Claim 3 is part 3 of the invariant. $\square$

**Running time.** Let $n = |V_0|$ and $m = |E_0|$. The implementation keeps for each vertex the set of its neighbors and puts the vertices into buckets $B[0..\Delta]$ by degree, where $\Delta$ is the largest degree. A pointer $d$ starts at $\Delta$. To find a vertex for line L2, move $d$ down while $B[d]$ is empty; then a vertex of degree $> k$ exists exactly when $d > k$. Removing $v$ at line L3 takes $O(1 + \deg(v))$ time: each neighbor $u$ loses $v$ and moves from bucket $\deg(u)$ to bucket $\deg(u) - 1$. Degrees never grow, so a bucket above $d$ never becomes nonempty again, and $d$ moves down at most $\Delta \le n$ times in total. Each edge is removed at most once. So the loop costs $O(n + m)$, and lines L5 to L7 scan the remaining graph in $O(n + m)$. The total time is $O(n + m)$, and the buckets and neighbor sets take $O(n + m)$ space. $\square$

**Tightness.** Let $H_k$ be $k$ disjoint stars, each with a center and $k$ leaves. Each vertex has degree at most $k$, there is no isolated vertex, and the $k$ centers form a cover, so $\tau(H_k) = k$ (each star needs one vertex). Then BUSS-KERNEL$(H_k, k)$ changes nothing and returns $(H_k, k)$, with exactly $k^2$ edges and $k^2 + k$ vertices. So the bounds of claim 2 are reached for every $k \ge 1$.
