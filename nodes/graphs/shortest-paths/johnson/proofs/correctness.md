---
title: Johnson's algorithm returns all distances or reports a negative cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph with $n$ vertices, $m$ arcs and real weights $w$. Line numbers refer to the pseudocode of JOHNSON on the main page.

**Fact 1 (cycles of $G'$).** The graph $G'$ of line L1 has a negative cycle if and only if $G$ has one.

*Proof.* The new vertex $q$ has no incoming arc, so no cycle of $G'$ passes through $q$. Hence the cycles of $G'$ are exactly the cycles of $G$, with the same weights. $\square$

**Fact 2 (line L3).** Line L3 returns "negative cycle" if and only if $G$ has a negative cycle.

*Proof.* Every vertex of $G'$ is reachable from $q$ by its arc $q \to v$. Bellman-Ford from $q$ reports a negative cycle exactly when a negative cycle is reachable from $q$ (see [Bellman-Ford](/bellman-ford/)). Since every cycle is reachable from $q$, this happens exactly when $G'$ has a negative cycle, which by Fact 1 is when $G$ has one. $\square$

From now on, assume $G$ has no negative cycle.

**Fact 3 ($h$ is real).** For every $v \in V$, $h(v) = \delta(q, v)$ is a real number with $h(v) \le 0$.

*Proof.* $v$ is reachable from $q$, so $\delta(q, v) < \infty$. No negative cycle exists in $G'$, so $\delta(q, v) > -\infty$. The arc $q \to v$ of weight 0 gives $\delta(q, v) \le 0$. $\square$

**Fact 4 ($\hat w \ge 0$).** For every arc $(u, v) \in E$, $\hat w(u, v) = w(u, v) + h(u) - h(v) \ge 0$.

*Proof.* A shortest path from $q$ to $u$ followed by $(u, v)$ is a walk from $q$ to $v$ of weight $h(u) + w(u, v)$, so $h(v) \le h(u) + w(u, v)$. This is the triangle inequality of the [optimality conditions](/shortest-path-optimality-conditions/). Rearranged, it is $\hat w(u, v) \ge 0$. $\square$

**Lemma (reweighting).** For every walk $p = \langle v_0, v_1, \ldots, v_k \rangle$ in $G$, $\hat w(p) = w(p) + h(v_0) - h(v_k)$. Hence for all $u, v \in V$, $v$ is reachable from $u$ under $w$ if and only if under $\hat w$, and when it is, $\hat\delta(u, v) = \delta(u, v) + h(u) - h(v)$.

*Proof.* Sum the reduced costs along $p$:

$$\hat w(p) = \sum_{i=1}^{k} \big(w(v_{i-1}, v_i) + h(v_{i-1}) - h(v_i)\big) = w(p) + h(v_0) - h(v_k),$$

because the sum of $h(v_{i-1}) - h(v_i)$ telescopes. The two weight functions are on the same arc set, so the walks from $u$ to $v$ are the same set in both cases, and reachability is the same. Each walk from $u$ to $v$ changes by the same real constant $h(u) - h(v)$, so the infimum over these walks changes by that constant too. Both infima are real: $\delta(u, v) > -\infty$ because $G$ has no negative cycle, and $\hat\delta(u, v) \ge 0$ by Fact 4. $\square$

**Fact 5 (Dijkstra on $\hat w$).** For each $u$, line L7 returns $\hat\delta(u, v)$ for every $v$, with $\infty$ for the vertices not reachable from $u$.

*Proof.* By Fact 4 all weights $\hat w$ are nonnegative, and [Dijkstra's algorithm](/dijkstra/) is correct on graphs with nonnegative weights. $\square$

**Theorem.** If $G$ has a negative cycle, JOHNSON returns "negative cycle". Otherwise it returns a matrix $D$ with $D[u][v] = \delta(u, v)$ for all $u, v \in V$, where $D[u][v] = \infty$ exactly when $v$ is not reachable from $u$.

*Proof.* The first part is Fact 2. Otherwise, fix $u, v$. If $v$ is not reachable from $u$, Fact 5 gives $\hat\delta(u, v) = \infty$, the lemma says this is the case exactly when $\delta(u, v) = \infty$, and line L8 keeps $\infty$. If $v$ is reachable, Fact 5 and the lemma give

$$D[u][v] = \hat\delta(u, v) - h(u) + h(v) = \delta(u, v) + h(u) - h(v) - h(u) + h(v) = \delta(u, v),$$

where $h(u)$ and $h(v)$ are real by Fact 3. $\square$

**Termination.** Bellman-Ford on $G'$ does at most $n$ passes over its $m + n$ arcs. Line L5 does $m$ steps. Lines L6 to L8 run Dijkstra $n$ times, and each run ends after it extracts each vertex at most once, followed by $n$ steps of line L8. All loops are bounded, so JOHNSON terminates on every finite input. $\blacksquare$
