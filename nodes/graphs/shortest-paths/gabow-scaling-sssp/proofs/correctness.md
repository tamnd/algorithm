---
title: Gabow's scaling algorithm is correct
proves: [correctness, termination]
status: full
---

**Claim.** Let every weight be an integer in $0 \ldots N$, and let $b$ be the number of bits of $N$ ($b = 0$ if $N = 0$). For $0 \le i \le b$, let $w_i(e) = \lfloor w(e) / 2^{b-i} \rfloor$ and let $d_i(v)$ be the distance from $s$ to $v$ under $w_i$ ($+\infty$ if $s$ does not reach $v$). After line L1, $d = d_0$, and after the iteration $i$ of line L2, $d = d_i$. Since $w_b = w$, GABOW-SCALING returns $\delta(s, v)$ for every $v$. It ends after $b$ iterations.

Reachability does not depend on the weights, so $d_i(v) = \infty$ for one $i$ exactly when it holds for all $i$; call the other vertices *reachable*. All weights $w_i$ are nonnegative integers, so there is no negative cycle, every $d_i(v)$ for reachable $v$ is a nonnegative integer, and it is the weight of a simple path (deleting a cycle from a walk does not increase its weight).

**Step 1: the rounding bounds.** Write $w(e) = q \cdot 2^{b-i+1} + \rho$ with $0 \le \rho < 2^{b-i+1}$. Then $w_{i-1}(e) = q$ and $w_i(e) = 2q + \lfloor \rho / 2^{b-i} \rfloor$ with $\lfloor \rho / 2^{b-i} \rfloor \in \{0, 1\}$. So $2 w_{i-1}(e) \le w_i(e) \le 2 w_{i-1}(e) + 1$.

**Step 2: scale 0.** $w_0 = 0$ on every edge (every weight is below $2^b$), so $d_0(v) = 0$ for every reachable $v$, and line L1 sets exactly this.

**Step 3: the reduced lengths are nonnegative.** Assume $d = d_{i-1}$ at the start of iteration $i$. For an edge $(u, v)$ with $u$ reachable, $v$ is reachable too, and $d_{i-1}(v) \le d_{i-1}(u) + w_{i-1}(u, v)$. With Step 1, $r(u, v) = w_i(u, v) + 2 d_{i-1}(u) - 2 d_{i-1}(v) \ge w_i(u, v) - 2 w_{i-1}(u, v) \ge 0$. Edges out of unreachable vertices are never scanned in line L5, because such a vertex never gets a finite label.

**Step 4: reduced distances.** For a path $P$ from $s$ to a reachable $v$, the potentials telescope: $r(P) = w_i(P) + 2 d_{i-1}(s) - 2 d_{i-1}(v) = w_i(P) - 2 d_{i-1}(v)$. So $\delta_r(v) = d_i(v) - 2 d_{i-1}(v)$, where $\delta_r$ is the distance under $r$.

**Step 5: reduced distances are below $n$.** Let $P$ be a simple shortest path to $v$ under $w_{i-1}$; it has at most $n - 1$ edges. By Step 1, $w_i(P) \le 2 w_{i-1}(P) + (n - 1) = 2 d_{i-1}(v) + n - 1$. So $d_i(v) \le 2 d_{i-1}(v) + n - 1$, and by Step 4, $0 \le \delta_r(v) \le n - 1$.

**Step 6: the sweep is exact.** Line L5 is Dijkstra's algorithm with nonnegative integer lengths (Step 3), with the priority queue replaced by buckets swept in increasing order, except that a tentative label of $n$ or more is not recorded. We show that every reachable $v$ is scanned from bucket $\delta_r(v)$ with label $\delta_r(v)$, by induction on $\delta_r(v)$ and, for equal values, on the number of edges of a shortest $r$-path with fewest edges. For $v = s$, $\delta_r(s) = 0$ and $s$ starts in bucket 0. For $v \ne s$, let $u$ be the vertex before $v$ on a shortest $r$-path to $v$ with fewest edges. Then $\delta_r(u) = \delta_r(v) - r(u, v) \le \delta_r(v)$, and if equal, the path to $u$ has fewer edges. By induction, $u$ is scanned from bucket $\delta_r(u)$ while the sweep is at level $\delta_r(u) \le \delta_r(v)$, and it offers $v$ the label $\delta_r(u) + r(u, v) = \delta_r(v) \le n - 1$, which is recorded unless the label is already at most that. Labels are always lengths of paths, so they are never below $\delta_r(v)$. So, from that moment on, the label of $v$ is $\delta_r(v)$ and $v$ is in bucket $\delta_r(v)$, which the sweep reaches no earlier than now (the sweep is at level $\delta_r(u) \le \delta_r(v)$). When the sweep reaches that bucket, $v$ is scanned with label $\delta_r(v)$, unless it was scanned earlier, which would require an earlier label equal to the level then, that is, a label below $\delta_r(v)$, impossible. A scanned vertex is not scanned again. So line L5 gives $\delta(v) = \delta_r(v)$ for every reachable $v$, and the parent of $v$ is a vertex $u$ with $\delta_r(v) = \delta_r(u) + r(u, v)$.

**Step 7: the update.** Line L6 sets $d(v) = 2 d_{i-1}(v) + \delta_r(v) = d_i(v)$ by Step 4, for every reachable $v$, and leaves $\infty$ for the others. This completes the induction.

**Parents.** In the last sweep, the parent $u$ of $v$ satisfies $\delta_r(v) = \delta_r(u) + r(u, v)$, so by Step 4, $d_b(v) = d_b(u) + w(u, v)$; such edges, one into each reachable $v \ne s$, form a shortest-path tree (each parent was scanned before its child, so there is no cycle). When $b = 0$, all weights are 0 and the tree of line L1 is a shortest-path tree.

**Termination.** Line L1 is a finite search, the loop has $b$ iterations, and each sweep visits $n$ buckets, each holding finitely many entries. $\blacksquare$
