---
title: The maximum-capacity augmenting path algorithm returns a maximum flow after at most m ln f* + 1 augmentations
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ is a directed graph with $n$ vertices, $m$ edges, integer capacities $c(e) \ge 0$, a source $s$ and a sink $t \ne s$. Parallel and antiparallel edges are allowed. For a flow $f$, the residual graph $G_f$ has, for each edge $e = (u, v)$, a forward residual edge $(u, v)$ of capacity $c(e) - f(e)$ and a backward residual edge $(v, u)$ of capacity $f(e)$. The bottleneck of a path is the least residual capacity on it. Let $f^{*}$ be the maximum flow value.

**Lemma 1 (WIDEST-PATH).** When a vertex $u$ is extracted for the first time at line L9, $b[u]$ equals the largest bottleneck $w(u)$ of an $s$-$u$ path in $G_f$ (with $w(s) = \infty$), and following via from $u$ gives a path with that bottleneck. Vertices with $w(u) = 0$ keep $b[u] = 0$.

*Proof.* Every value $b[v] > 0$ is the bottleneck of the path that via records, so $b[v] \le w(v)$ always. Suppose the claim fails, and let $u$ be the first extracted vertex with $b[u] < w(u)$. Take a path $P$ from $s$ to $u$ with bottleneck $w(u)$. Let $(x, y)$ be the first edge of $P$ with $x$ extracted and $y$ not yet extracted before $u$; it exists because $s$ is extracted first and $u$ is not yet extracted. The part of $P$ up to $x$ has bottleneck at least $w(u)$, so $w(x) \ge w(u)$ and, by the choice of $u$, $b[x] = w(x)$. When $x$ was scanned, line L12 made $b[y] \ge \min(b[x], c_f(x, y)) \ge w(u)$, and $y$ entered $Q$ with that key. Since $u$ came out of $Q$ before $y$, $b[u] \ge b[y] \ge w(u)$, a contradiction. The case $y = u$ gives $b[u] \ge w(u)$ directly. $\square$

So WIDEST-PATH returns an empty path exactly when $G_f$ has no $s$-$t$ path of positive capacity, and otherwise a path with the largest bottleneck.

**Lemma 2 (augmentation).** If $P$ is an $s$-$t$ path in $G_f$ with bottleneck $\delta > 0$, line L5 gives a flow of value $|f| + \delta$.

*Proof.* On a forward edge the flow rises by $\delta \le c(e) - f(e)$; on a backward edge it falls by $\delta \le f(e)$; so capacities hold. Each inner vertex of $P$ has one edge of $P$ in and one out, and in each of the four cases of forward or backward edges the net change of its inflow minus outflow is 0. At $s$ the net outflow rises by $\delta$. $\square$

**Lemma 3 (a wide path exists).** If $|f| < f^{*}$, then $G_f$ has an $s$-$t$ path with bottleneck at least $(f^{*} - |f|)/m$.

*Proof.* Let $g$ be a maximum flow. Define $h$ on $G_f$ edge by edge: for $e = (u, v)$, if $g(e) \ge f(e)$ put $g(e) - f(e)$ on the forward residual edge, and otherwise put $f(e) - g(e)$ on the backward one. These amounts are within the residual capacities, $h$ is conserved at every vertex other than $s$ and $t$ because $f$ and $g$ are, and its value is $|g| - |f| = r > 0$. At most one residual edge per edge of $G$ carries $h$, so $h$ has at most $m$ edges in its support. By [flow decomposition](/flow-decomposition/), $h$ is a sum of at most $m$ path flows and cycle flows, each removing at least one support edge, and the path flows sum to $r$. So some $s$-$t$ path carries at least $r/m$, and each of its edges has residual capacity at least that much. $\square$

**Lemma 4 (termination).** With integer capacities the flow stays integral, and each $\delta$ is a positive integer.

*Proof.* By induction: residual capacities of an integral flow are integers, so $\delta$ is a positive integer, and Lemma 2 keeps the flow integral. $\square$

**Theorem.** The algorithm stops after at most $\lfloor m \ln f^{*} \rfloor + 1$ augmentations when $f^{*} \ge 1$, and after none when $f^{*} = 0$. It returns a maximum flow $f$, and the set $S$ of vertices that $s$ reaches in $G_f$ is a minimum cut.

*Proof.* Let $r_k$ be the missing flow $f^{*} - |f|$ after $k$ augmentations, so $r_0 = f^{*}$. By Lemmas 1 and 3, the next augmentation uses $\delta \ge r_k / m$, so $r_{k+1} \le r_k (1 - 1/m) \le r_k e^{-1/m}$, and $r_k \le f^{*} e^{-k/m}$. For $k > m \ln f^{*}$ this is less than 1, and $r_k$ is an integer by Lemma 4, so $r_k = 0$. So after $\lfloor m \ln f^{*} \rfloor + 1$ augmentations the flow is maximum; then $G_f$ has no positive $s$-$t$ path (otherwise Lemma 2 would give a larger flow), WIDEST-PATH returns empty, and the loop stops. If $f^{*} = 0$, $G_f = G$ at the start has no positive $s$-$t$ path and the loop stops at once. At the end, $t \notin S$; every edge from $S$ to $V \setminus S$ is full and every edge from $V \setminus S$ to $S$ is empty, since otherwise a residual edge would leave $S$. So $|f| = c(S)$, and by weak duality $f$ is maximum and $S$ is a minimum cut. $\blacksquare$
