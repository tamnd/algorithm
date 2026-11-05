---
title: The successive shortest path algorithm returns a cheapest flow of the requested value
proves: [correctness, termination]
status: full
---

**Setting.** $G = (V, E)$ is a directed graph with integer capacities $u(e) \ge 0$, real costs $c(e)$, a source $s$, a sink $t \ne s$, and a target $d \in \mathbb{Z}_{\ge 0} \cup \{\infty\}$. The edges of positive capacity contain no cycle of negative cost. For a flow $x$, the residual graph $G_x$ has, for each edge $e = (v, w)$, a forward edge $(v, w)$ with capacity $u(e) - x(e)$ and cost $c(e)$, and a backward edge $(w, v)$ with capacity $x(e)$ and cost $-c(e)$; only edges of positive capacity are present. For potentials $\pi$, the reduced cost of a residual edge $r = (v, w)$ is $c^{\pi}(r) = c(r) + \pi(v) - \pi(w)$. Let $R(x)$ be the set of vertices that $s$ reaches in $G_x$.

**Lemma 1 (potentials cancel on cycles).** For every directed cycle $C$, $\sum_{r \in C} c^{\pi}(r) = \sum_{r \in C} c(r)$.

*Proof.* Each vertex of $C$ is the tail of one edge of $C$ and the head of one, so the terms $\pi(v) - \pi(w)$ sum to 0. $\square$

**Lemma 2 (negative cycle optimality).** A flow $x$ of value $k$ is a cheapest flow of value $k$ if $G_x$ has no cycle of negative cost.

*Proof.* Let $x'$ be a flow of value $k$. For each edge put $x'(e) - x(e)$ on its forward residual edge if this is positive, and $x(e) - x'(e)$ on its backward residual edge otherwise. The result $h$ respects the residual capacities. Both flows have value $k$ and satisfy conservation, so $h$ is conserved at every vertex, including $s$ and $t$: it is a circulation in $G_x$, with cost $c(x') - c(x)$. A circulation is a nonnegative sum of flows around directed cycles of its support, which are cycles of $G_x$. Each has cost at least 0, so $c(x') \ge c(x)$. $\square$

**Lemma 3 (the start).** After line L2, $c^{\pi}(e) \ge 0$ for every edge $e$ of positive capacity, and the zero flow is a cheapest flow of value 0.

*Proof.* With no negative cycle, Bellman-Ford from the root returns shortest distances $\pi$, and $\pi(w) \le \pi(v) + c(v, w)$ for each edge $(v, w)$ that it uses, which is $c^{\pi}(v, w) \ge 0$. At $x = 0$ the residual graph has exactly these edges, so by Lemma 1 it has no negative cycle, and Lemma 2 applies. $\square$

**Invariant.** Before each round: (a) $c^{\pi}(r) \ge 0$ for each residual edge $r$ of $G_x$ whose tail is in $R(x)$; (b) $G_x$ has no cycle of negative cost; (c) $x$ is a cheapest flow of its value.

*It holds at the start* by Lemma 3; (a) holds for all edges then.

*It is preserved.* Let $\mathrm{dist}$ be the distances of line L4, which are correct because Dijkstra only scans edges with tails in $R(x)$, whose lengths are nonnegative by (a). Let $\pi' = \pi + \mathrm{dist}$ on $R(x)$ and $\pi' = \pi$ elsewhere. For a residual edge $r = (v, w)$ with $v \in R(x)$, also $w \in R(x)$, and $\mathrm{dist}(w) \le \mathrm{dist}(v) + c^{\pi}(r)$, so $c^{\pi'}(r) = c^{\pi}(r) + \mathrm{dist}(v) - \mathrm{dist}(w) \ge 0$. For the edges of the shortest path $P$ equality holds, so $c^{\pi'}(r) = 0$ on $P$. Let $x'$ be the flow after line L8. Each residual edge of $G_{x'}$ is either a residual edge of $G_x$ or the reverse of an edge of $P$, which has reduced cost $-0 = 0$. The new reverse edges join vertices of $R(x)$, and the other edges were already there, so $R(x') \subseteq R(x)$. Hence every edge of $G_{x'}$ with tail in $R(x')$ has $c^{\pi'} \ge 0$, which is (a).

For (b), take a cycle $C$ of $G_{x'}$. Each edge of $C$ is either an edge of $G_x$ or the reverse of an edge of $P$. *Case 1: $C$ has a vertex in $R(x)$.* An edge of $G_x$ with tail in $R(x)$ has its head in $R(x)$, and a reversed edge has both ends in $R(x)$; so, walking around $C$, every vertex of $C$ is in $R(x)$. Then every edge of $C$ has $c^{\pi'} \ge 0$ by the computation above, and by Lemma 1 the cost of $C$ is at least 0. *Case 2: $C$ has no vertex in $R(x)$.* Then $C$ uses no reversed edge, so it is a cycle of $G_x$, and its cost is at least 0 by (b) for $x$.

(c) follows from (b) by Lemma 2. $\square$

**Lemma 4 (termination).** The loop runs at most $\min(d, f^{*})$ rounds when this is finite, and stops with value $\min(d, f^{*})$, where $f^{*}$ is the maximum flow value.

*Proof.* Capacities are integers, so by induction the flow and the residual capacities stay integral and each $\delta$ is a positive integer, because $d - \mathrm{value} \ge 1$ inside the loop. The value grows by at least 1 per round and never exceeds $d$ or $f^{*}$. The loop stops when the value reaches $d$, or when $t \notin R(x)$; in the second case $G_x$ has no $s$-$t$ path, so $x$ is a maximum flow by the max-flow min-cut theorem. $f^{*}$ is finite, because $f^{*} \le \sum_{e \text{ out of } s} u(e)$. $\square$

**Theorem.** The algorithm returns a flow of value $\min(d, f^{*})$ that has the least cost among all flows of that value.

*Proof.* By Lemma 4 it stops with that value, and by part (c) of the invariant the flow is a cheapest one of its value. $\blacksquare$
