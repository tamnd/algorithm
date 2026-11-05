---
title: Dijkstra's algorithm computes shortest-path distances when all weights are nonnegative
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a directed graph with $w(u, v) \ge 0$ for each edge, and let $s \in V$. Then DIJKSTRA$(G, w, s)$ ends after at most $m + 1$ passes of the loop of line L4. At the end, $d[v] = \delta(s, v)$ for each $v \in V$, and for each $v \ne s$ with $d[v] < \infty$, the edge $(\pi[v], v)$ exists and $d[v] = d[\pi[v]] + w(\pi[v], v)$, so the predecessor edges form a shortest-path tree of the vertices that $s$ reaches.

**Setup.** Let $S = \{v : \text{done}[v] = \text{true}\}$. For $v \in V$ define $\mu_S(v)$ as the least element of the set $\{d[x] + w(x, v) : (x, v) \in E, x \in S\}$, together with the element $0$ if $v = s$; let $\mu_S(v) = \infty$ when this set is empty. We use the [upper-bound property](/upper-bound-property/) of [relaxation](/edge-relaxation/): every finite $d[v]$ is the weight of a walk from $s$ to $v$, so $d[v] \ge \delta(s, v)$ at all times. With $w \ge 0$ there is no negative cycle, so each $\delta(s, v)$ is a finite number or $\infty$, and $\delta(s, v) \ge 0$.

**Invariant.** At each test of line L4:

- **(I1)** $d[v] = \delta(s, v)$ for each $v \in S$, and $\pi[v]$ satisfies the claim for each $v \in S \setminus \{s\}$;
- **(I2)** $d[v] = \mu_S(v)$ for each $v \notin S$; when $d[v] < \infty$ and $v \ne s$, $\pi[v] = x$ for an $x \in S$ with $d[v] = d[x] + w(x, v)$;
- **(I3)** for each $v \notin S$ with $d[v] < \infty$, the heap holds the pair $(d[v], v)$; each pair $(k, v)$ in the heap has $k \ge d[v]$.

**Initialization.** After lines L1 to L3, $S = \emptyset$, $d[s] = 0 = \mu_\emptyset(s)$, and $d[v] = \infty = \mu_\emptyset(v)$ for $v \ne s$. The heap holds only $(0, s)$. All three parts hold.

**Maintenance.** Let line L5 take the pair $(k, u)$ with the least key.

*Case 1: $u \in S$.* Nothing else changes, so the invariant holds.

*Case 2: $u \notin S$.* By (I3), $k \ge d[u]$, and the heap holds $(d[u], u)$, so the least key is at most $d[u]$; thus $k = d[u]$, and $d[u] < \infty$. By (I3) again, each $v \notin S$ with $d[v] < \infty$ has a pair with key $d[v] \ge k$. Hence

$$d[u] = \min_{v \notin S} d[v]. \tag{1}$$

We show $d[u] \le \delta(s, u)$. Since $d[u] < \infty$, $u$ is reachable. Let $P = \langle s = p_0, p_1, \ldots, p_r = u \rangle$ be a shortest path; it exists because there is no negative cycle. Let $p_j$ be the first vertex of $P$ that is not in $S$; it exists because $u \notin S$. If $j = 0$, then $p_j = s$ and $d[s] \le \mu_S(s) \le 0 \le \delta(s, u)$. If $j > 0$, then $p_{j-1} \in S$, so by (I2) and (I1),
$$d[p_j] = \mu_S(p_j) \le d[p_{j-1}] + w(p_{j-1}, p_j) = \delta(s, p_{j-1}) + w(p_{j-1}, p_j) = \delta(s, p_j),$$
where the last equality holds because a prefix of a shortest path is a shortest path. In both cases $d[p_j] \le \delta(s, p_j)$. The rest of $P$, from $p_j$ to $u$, has weight at least $0$ **because each weight is nonnegative**, so $\delta(s, p_j) \le \delta(s, u)$. With (1), $d[u] \le d[p_j] \le \delta(s, u)$. The upper-bound property gives $d[u] \ge \delta(s, u)$, so $d[u] = \delta(s, u)$. Line L7 adds $u$ to $S$; (I2) for $u$ gives the predecessor part of (I1) for $u$, so (I1) holds for $S' = S \cup \{u\}$.

Lines L8 to L11 relax each edge $(u, v)$. For $v \notin S'$, $\mu_{S'}(v) = \min(\mu_S(v), d[u] + w(u, v))$ over the edges from $u$ to $v$, and the relaxations set $d[v]$ to exactly this value, with $\pi[v] = u$ when the new value wins. So (I2) holds. For $v \in S'$, $d[v] = \delta(s, v) \le \delta(s, u) + w(u, v) = d[u] + w(u, v)$, so line L9 fails and nothing changes: (I1) stays true. Each time line L10 lowers $d[v]$, line L11 inserts $(d[v], v)$, and older pairs of $v$ have keys at least the old, larger $d[v]$. So (I3) holds.

**Termination.** Each pass removes one pair from the heap. Pairs are inserted once by line L3 and once by each successful test of line L9. Line L9 runs once for each edge $(u, v)$, at the one pass where $u$ enters $S$, because a vertex enters $S$ only once. So at most $m + 1$ pairs are ever inserted, and the loop makes at most $m + 1$ passes.

**At the end.** The heap is empty. By (I3), $d[v] = \infty$ for each $v \notin S$. Assume that some $v \notin S$ is reachable, and take a path from $s$ to $v$ with its first vertex $y \notin S$. If $y = s$, then $d[s] \le 0$, and if $y \ne s$, its predecessor $x$ on the path is in $S$, so $d[y] \le d[x] + w(x, y) < \infty$ by (I2). Both contradict $d[y] = \infty$. So each vertex outside $S$ is unreachable, and $d[v] = \infty = \delta(s, v)$ for it. For $v \in S$, (I1) gives $d[v] = \delta(s, v)$ and the predecessor condition. For $v \in S \setminus \{s\}$, the value $\pi[v] = x$ was set at the pass where $x$ entered $S$, and at that time $v \notin S$. So $x$ entered $S$ before $v$. Following predecessors from $v$ therefore visits vertices that entered $S$ earlier and earlier, so it stops, and it can only stop at $s$, the one vertex of $S$ with no predecessor. The predecessor edges thus form a tree rooted at $s$, and along each tree path the weights add up to $d[v] = \delta(s, v)$. $\blacksquare$

**Where the hypothesis is used.** Only the step $\delta(s, p_j) \le \delta(s, u)$ uses $w \ge 0$. The example on the page, with the edge $b \to a$ of weight $-3$, breaks exactly this step: there the first vertex of the shortest path to $c$ outside $S$ is $b$, and $\delta(s, b) = 4 > \delta(s, c) = 2$.
