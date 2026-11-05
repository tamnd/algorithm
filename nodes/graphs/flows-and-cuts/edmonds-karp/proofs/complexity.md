---
title: Edmonds-Karp makes at most nm augmentations
proves: [time.worst]
status: full
---

Fix the run of the algorithm on a network with $n$ vertices and $m$ edges. The residual graph $G_f$ has at most $2m$ arcs: $e^+$ and $e^-$ for each edge $e$. Let $\delta_f(v)$ be the number of arcs on a shortest path from $s$ to $v$ in $G_f$, or $\infty$ if there is none.

**Lemma 1 (distances never decrease).** Let $f'$ be the flow after one augmentation of the algorithm, from $f$. Then $\delta_{f'}(v) \ge \delta_f(v)$ for each vertex $v$.

*Proof.* Let $P$ be the augmenting path, a shortest s-t path in $G_f$. Each arc $(x, y)$ of $P$ has $\delta_f(y) = \delta_f(x) + 1$, since a prefix of a shortest path is shortest. The augmentation changes $G_f$ only in two ways: it can remove arcs of $P$ (those whose residual capacity becomes 0), and it can add the reverse $(y, x)$ of an arc $(x, y)$ of $P$. Every arc $(p, q)$ of $G_{f'}$ satisfies $\delta_f(q) \le \delta_f(p) + 1$: for an arc already in $G_f$ this is the property of BFS distances; for a new arc $(y, x)$ it holds since $\delta_f(x) = \delta_f(y) - 1 \le \delta_f(y) + 1$. Now take a shortest path $s = v_0, v_1, \ldots, v_k = v$ in $G_{f'}$, so $k = \delta_{f'}(v)$. Summing $\delta_f(v_{i+1}) \le \delta_f(v_i) + 1$ over $i$ gives $\delta_f(v) \le \delta_f(s) + k = k$. If $v$ is not reachable in $G_{f'}$, the claim is trivial. $\square$

**Lemma 2 (critical arcs).** Call an arc $x = (u, v)$ of $P$ *critical* in a round if $c_f(x) = \Delta$; after the round $c_{f'}(x) = 0$ and $x$ is not in $G_{f'}$. Each arc is critical in at most $n/2$ rounds.

*Proof.* Suppose $x = (u, v)$ is critical in the round with flow $f$. Then $\delta_f(v) = \delta_f(u) + 1$. For $x$ to be critical again, it must first come back into the residual graph, and the only way is an augmentation along a path that uses the reverse arc $(v, u)$, in a round with some flow $g$. That path is shortest in $G_g$, so $\delta_g(u) = \delta_g(v) + 1$. By Lemma 1, $\delta_g(v) \ge \delta_f(v)$. Hence

$$\delta_g(u) = \delta_g(v) + 1 \ge \delta_f(v) + 1 = \delta_f(u) + 2.$$

By Lemma 1 again, at the next round in which $x$ is critical the distance of $u$ is at least $\delta_g(u) \ge \delta_f(u) + 2$. So the distances of $u$ at the rounds where $x$ is critical form a sequence that grows by at least 2 each time. In each such round $u$ lies on a shortest s-t path and is not $t$, so $\delta(u) \le n - 2$; and $\delta(u) \ge 0$. A sequence of integers in $[0, n - 2]$ that grows by at least 2 has at most $\lfloor (n - 2)/2 \rfloor + 1 \le n/2$ terms. $\square$

**Theorem 2.** The algorithm makes at most $nm$ augmentations, and its running time is $O(nm(n + m))$, which is $O(nm^2)$ when $m \ge n$.

*Proof.* In each round the bottleneck $\Delta$ is the residual capacity of some arc of $P$, so each round has at least one critical arc. There are at most $2m$ arcs, each critical at most $n/2$ times by Lemma 2, so there are at most $2m \cdot n/2 = nm$ rounds. Each round costs $O(n + m)$ for the search and $O(n)$ for the augmentation. The final search that fails costs $O(n + m)$ more. Lines L1 and L11 cost $O(n + m)$. $\blacksquare$

Neither lemma uses integrality, so the bound holds for all nonnegative real capacities, and in exact arithmetic the algorithm terminates on every input.
