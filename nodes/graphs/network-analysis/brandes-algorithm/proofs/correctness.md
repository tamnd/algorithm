---
title: Brandes' algorithm computes betweenness centrality
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph; an undirected graph is the directed graph with both arcs $(u, v)$ and $(v, u)$ for each edge. Each arc has a length $\ell(u, v) > 0$, and $\ell \equiv 1$ in the form without weights. Fix a source $s$. Let $d(w) = d_G(s, w)$, with $d(w) = \infty$ if $w$ is not reachable, and let $\sigma_{sw}$ be the number of shortest paths from $s$ to $w$, with $\sigma_{ss} = 1$ and $\sigma_{sw} = 0$ for unreachable $w$. The *predecessor set* is $P_s(w) = \{v : (v, w) \in E,\ d(v) + \ell(v, w) = d(w) < \infty\}$.

**Termination.** Line L2 runs $n$ times. In one run, each vertex enters the queue at most once (line L8 enqueues $w$ only when $d[w] = \infty$ and makes it finite), so lines L5 to L9 run at most $n$ times and scan finite lists. Line L11 pops exactly the vertices pushed at line L6. So the algorithm stops. The Dijkstra form settles each vertex once and stops in the same way.

**Lemma 1 (Bellman criterion).** A vertex $v$ lies on a shortest path from $s$ to $t$ if and only if $d(v) + d_G(v, t) = d(t) < \infty$. Every shortest path to $w \ne s$ ends with an arc $(v, w)$ with $v \in P_s(w)$, and its part up to $v$ is a shortest path to $v$. Hence $\sigma_{sw} = \sum_{v \in P_s(w)} \sigma_{sv}$ for $w \ne s$.

*Proof.* A subpath of a shortest path is a shortest path, since a shorter subpath could replace it. So the first statement holds, and a shortest path $s \ldots v w$ has $d(v) + \ell(v, w) = d(w)$, so $v \in P_s(w)$. Conversely, for $v \in P_s(w)$, each shortest path to $v$ followed by $(v, w)$ has length $d(w)$. This is a bijection between the shortest paths to $w$ and the pairs (a predecessor $v$, a shortest path to $v$), which gives the sum. $\square$

**Lemma 2 (the search).** After lines L4 to L9 (or their Dijkstra form) for the source $s$: $d[w] = d(w)$, $\sigma[w] = \sigma_{sw}$ and $P[w] = P_s(w)$ for every $w$, and $S$ holds the reachable vertices with $d$ non-decreasing from the bottom to the top.

*Proof.* Without weights, lines L4 to L8 are the breadth-first search, which sets $d[w] = d(w)$ and dequeues the vertices in non-decreasing order of $d$; line L6 pushes them in that order. Line L9 runs once for each arc $(v, w)$ out of a reachable $v$, after $d[w]$ is final (either $w$ was discovered before, or line L8 just set it), and it appends $v$ to $P[w]$ exactly when $d(w) = d(v) + 1$, that is when $v \in P_s(w)$. So $P[w] = P_s(w)$. When $v$ is dequeued, all its predecessors have smaller $d$ and were dequeued before, so all their contributions to $\sigma[v]$ were made, and by Lemma 1 and induction on $d$, $\sigma[v] = \sigma_{sv}$ when $v$ passes it on. The final $\sigma[w]$ is the sum over all $v \in P_s(w)$, which is $\sigma_{sw}$ by Lemma 1.

With positive lengths, Dijkstra's algorithm settles the vertices in non-decreasing order of $d$ and with $d[v] = d(v)$ at settling. Every $v \in P_s(w)$ has $d(v) < d(w)$, since $\ell > 0$, so it is settled before $w$, and when it scans $(v, w)$ the test either makes $v$ the first predecessor found with the current best value or adds it to a list of equal value. Values found later that are smaller reset the list and the count; at the time $w$ is settled, $d[w] = d(w)$, and the list holds exactly the settled $v$ with $d(v) + \ell(v, w) = d(w)$, which are all of $P_s(w)$, and by induction $\sigma[w] = \sum_{v \in P_s(w)} \sigma_{sv} = \sigma_{sw}$. $\square$

**Lemma 3 (the dependency recursion).** For each $v$,

$$\delta_{s\bullet}(v) = \sum_{w \,:\, v \in P_s(w)} \frac{\sigma_{sv}}{\sigma_{sw}} \bigl(1 + \delta_{s\bullet}(w)\bigr),$$

where $\delta_{s\bullet}(v) = \sum_{t \ne s, v} \sigma_{st}(v) / \sigma_{st}$, with the sum over reachable $t$.

*Proof.* Fix a reachable $t \ne v$ with $\sigma_{st}(v) > 0$. Each shortest path from $s$ to $t$ through $v$ leaves $v$ along exactly one arc $(v, w)$, and by Lemma 1, $v \in P_s(w)$ and $w$ is on the path. So $\sigma_{st}(v) = \sum_{w : v \in P_s(w)} \sigma_{st}(v, w)$, where $\sigma_{st}(v, w)$ counts the shortest $s$-$t$ paths that use the arc $(v, w)$.

Count $\sigma_{st}(v, w)$. If $t = w$, it is $\sigma_{sv}$: a shortest path to $v$ followed by the arc. If $t \ne w$, a path that uses $(v, w)$ is a shortest path to $v$, the arc, and a shortest path from $w$ to $t$, so $\sigma_{st}(v, w) = \sigma_{sv} \cdot \sigma_{wt}$. The number of shortest $s$-$t$ paths through $w$ is $\sigma_{st}(w) = \sigma_{sw} \sigma_{wt}$, so $\sigma_{st}(v, w) = \frac{\sigma_{sv}}{\sigma_{sw}} \sigma_{st}(w)$. Hence

$$\frac{\sigma_{st}(v, w)}{\sigma_{st}} = \frac{\sigma_{sv}}{\sigma_{sw}} \cdot \begin{cases} 1 & t = w, \\ \sigma_{st}(w) / \sigma_{st} & t \ne w. \end{cases}$$

Sum over $t$ and over $w$, and exchange the two sums. For a fixed $w$, the term $t = w$ gives $\frac{\sigma_{sv}}{\sigma_{sw}}$, and the terms $t \ne w$ give $\frac{\sigma_{sv}}{\sigma_{sw}} \delta_{s\bullet}(w)$. Pairs $(t, w)$ with $\sigma_{st}(v, w) = 0$ contribute 0 on both sides, since then $\sigma_{st}(w) = 0$ or $t$ is not reachable. This gives the formula. $\square$

**Lemma 4 (the accumulation).** After lines L10 to L14 for the source $s$, $\delta[v] = \delta_{s\bullet}(v)$ for every reachable $v$, and the values added to $C_B$ are $\delta_{s\bullet}(w)$ for $w \ne s$.

*Proof.* If $v \in P_s(w)$, then $d(v) < d(w)$, so $v$ is below $w$ in $S$ by Lemma 2 and is popped after $w$. When $w$ is popped, every $x$ with $w \in P_s(x)$ is further from $s$ and was popped before, and each such pop added $\frac{\sigma_{sw}}{\sigma_{sx}}(1 + \delta[x])$ to $\delta[w]$ at line L13. Line L13 adds to $\delta[w]$ only at these pops. By induction on the order of pops, each $\delta[x]$ used was already final and equal to $\delta_{s\bullet}(x)$, so by Lemma 3, $\delta[w] = \delta_{s\bullet}(w)$ when $w$ is popped. It is not changed later, since later pops only add to their predecessors, which are closer to $s$. Line L14 then adds it for $w \ne s$. Unreachable vertices are never pushed and get no addition, which is right since $\delta_{s\bullet}(v) = 0$ for them. $\square$

**Theorem.** BRANDES$(G)$ returns $C_B(v) = \sum_{s \ne v \ne t} \sigma_{st}(v) / \sigma_{st}$ for every $v$ in the directed case, and half of it in the undirected case.

*Proof.* By Lemma 4, after the loop of line L2, $C_B[v] = \sum_{s \ne v} \delta_{s\bullet}(v) = \sum_{s \ne v} \sum_{t \ne s, v} \sigma_{st}(v) / \sigma_{st}$, which is the sum over ordered pairs. For an undirected graph, the pairs $(s, t)$ and $(t, s)$ have the same shortest paths reversed and give equal terms, so line L15 turns the sum into one over unordered pairs. $\blacksquare$
