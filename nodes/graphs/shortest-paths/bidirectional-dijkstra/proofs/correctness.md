---
title: Bidirectional Dijkstra returns a shortest path
proves: [correctness, termination]
status: full
---

**Claim.** Let $G$ be a directed graph with weights $w \ge 0$ and let $s, t$ be vertices. BIDIRECTIONAL-DIJKSTRA returns $\mu = \delta(s, t)$. If $\mu < \infty$, the returned vertex sequence is a walk from $s$ to $t$ of weight $\mu$, and it is a path when all weights are positive.

**Termination.** Each side inserts an entry into its queue only when line L9 lowers a label, which happens at most once per scan of an edge, and each vertex is marked done at most once per side. So each queue receives at most $1 + m$ entries, each pass of the loop removes one entry, and the loop ends after at most $2(m + 1)$ passes, or earlier by line L4. When both queues are empty, line L4 sees $\infty + \infty \ge \mu$ and stops.

**Notation.** The forward search runs on $G$ from $s$; its distances are $\delta_f(v) = \delta(s, v)$. The backward search runs on the reversed graph from $t$; its distances are $\delta_b(v) = \delta(v, t)$. Write $\min(Q)$ for the least key in $Q$, with $\min(\emptyset) = \infty$.

**Step 1: facts about each side.** Each side, on its own, is Dijkstra's algorithm with a lazy-deletion heap; the other side only reads its labels in line L10. So the following hold for each side $X$, from the proof of [Dijkstra's algorithm](/dijkstra-correctness/):

- (a) $d_X[v] \ge \delta_X(v)$ always, and if $d_X[v] < \infty$, following $\pi_X$ from $v$ gives a path to the root of side $X$ of weight exactly $d_X[v]$ (forward: from $s$ to $v$; backward: from $v$ to $t$).
- (b) When $u$ is marked done on side $X$, $d_X[u] = \delta_X(u)$, and the label never changes after that.
- (c) At any moment, every vertex $v$ with $\delta_X(v) < \min(Q_X)$ is done on side $X$.

For (c): let $v$ be a vertex with $\delta_X(v) < \infty$ not done on side $X$, and let $R$ be a shortest path to $v$ on side $X$. Its first vertex is done or is the root with its entry still in $Q_X$. Let $y$ be the first vertex of $R$ not done; if $y$ is the root, its entry $(0, y)$ is in the queue; otherwise its predecessor on $R$ is done, so by (b) and the relaxation of that edge, $d_X[y] = \delta_X(y)$ and the entry $(\delta_X(y), y)$ is in $Q_X$. So $\min(Q_X) \le \delta_X(y) \le \delta_X(v)$, since weights are nonnegative. This is the contrapositive of (c).

**Step 2: $\mu$ is an upper bound.** When line L10 sets $\mu$ from an edge $(u, v)$ scanned on the forward side, $d_f[u]$ is the weight of a path $s \leadsto u$ and $d_b[v] < \infty$ is the weight of a path $v \leadsto t$ by (a), so $\mu$ is the weight of the walk $s \leadsto u \to v \leadsto t$. The backward case is symmetric, with the edge used in its original direction. So $\mu \ge \delta(s, t)$ at all times, and if $s = t$, $\mu = 0 = \delta(s, t)$ from line L2.

**Step 3: at the stop, $\mu \le \delta(s, t)$.** Suppose $s \ne t$, the loop stops, and $\delta(s, t) < \mu$. Then $\delta(s, t) < \infty$; let $P = (v_0 = s, v_1, \ldots, v_k = t)$ be a shortest path. Let $F = \min(Q_f)$ and $B = \min(Q_b)$ at the stop, so $F + B \ge \mu$. For each $i$, $\delta(s, v_i) + \delta(v_i, t) = \delta(s, t) < F + B$, so $\delta(s, v_i) < F$ or $\delta(v_i, t) < B$.

Call $v_i$ *forward* if $\delta(s, v_i) < F$. Since $\delta(s, v_i)$ does not decrease along $P$, the forward vertices are $v_0, \ldots, v_{j}$ for some $j \in \{-1, 0, \ldots, k\}$ ($j = -1$ meaning none), and the others satisfy $\delta(v_i, t) < B$. By (c), forward vertices are done forward and the others are done backward.

- If $0 \le j < k$, the edge $(v_j, v_{j+1})$ joins a vertex done forward to a vertex done backward.
- If $j = -1$, all of $P$ is done backward. Take the edge $(v_0, v_1)$; its first end is $s$ with $d_f[s] = 0 = \delta(s, s)$ from line L1 on.
- If $j = k$, all of $P$ is done forward. Take the edge $(v_{k-1}, v_k)$; its last end is $t$ with $d_b[t] = 0$.

In each case let $(x, y)$ be that edge. Consider the moment when the later of "x done forward" and "y done backward" happened; in the cases $j = -1$ and $j = k$, consider when $y$ was done backward or $x$ was done forward, respectively. If that moment was the forward scan of $x$, line L10 examined $(x, y)$ with $d_f[x] = \delta(s, x)$ and $d_b[y] = \delta(y, t)$ (final by (b), or 0 at $t$). If it was the backward scan of $y$, line L10 examined the reversed edge with $d_b[y] = \delta(y, t)$ and $d_f[x] = \delta(s, x)$. Either way, afterwards $\mu \le \delta(s, x) + w(x, y) + \delta(y, t) = w(P) = \delta(s, t)$, since $P$ is a shortest path and its sub-paths are shortest. As $\mu$ never increases, this contradicts $\delta(s, t) < \mu$. Here $x \ne y$, since $P$ is a path and $s \ne t$, so line L10, which skips only self-loops, does examine $(x, y)$.

So $\mu = \delta(s, t)$ by Steps 2 and 3. In particular, $\mu = \infty$ exactly when $t$ is not reachable from $s$.

**Step 4: the path.** If $\mu < \infty$ and $s \ne t$, let $(a, b)$ be the edge remembered when $\mu$ took its final value, scanned on side $X$. At that time $\mu = d_f[a] + w(a, b) + d_b[b]$. Labels only decrease, so at the end $d_f[a] + w(a, b) + d_b[b] \le \mu$. By (a), $\pi_f$ gives a path $s \leadsto a$ of weight $d_f[a]$ and $\pi_b$ gives a path $b \leadsto t$ of weight $d_b[b]$. The joined walk has weight at most $\mu = \delta(s, t)$, hence exactly $\delta(s, t)$. Each chain is a path. If the two chains share a vertex $z$, the walk contains the closed walk $z \leadsto a \to b \leadsto z$; its weight is 0, because cutting it would leave an $s$-$t$ walk lighter than $\delta(s, t)$ otherwise. With all weights positive no closed walk has weight 0, so the chains are disjoint and the sequence is a path. $\blacksquare$
