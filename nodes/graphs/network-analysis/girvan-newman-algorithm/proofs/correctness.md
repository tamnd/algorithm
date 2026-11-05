---
title: Girvan-Newman computes exact edge betweenness, stops after m rounds, and returns the best level of its dendrogram
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be an undirected simple graph with $n$ vertices and $m$ edges. For a graph $H$ on $V$ and $s, t \in V$, write $d(s, t)$ for the distance in $H$, $\sigma_{st}$ for the number of shortest $s$-$t$ paths ($\sigma_{ss} = 1$), and $\sigma_{st}(e)$ for the number of those that contain the edge $e$.

**Lemma 1 (BFS counts).** After line L12 for a source $s$, $\mathrm{dist}[v] = d(s, v)$ and $\sigma[v] = \sigma_{sv}$ for every $v$ reached, and $S$ lists the reached vertices in non-decreasing order of distance.

*Proof.* BFS sets $\mathrm{dist}$ correctly and dequeues vertices in non-decreasing distance. A shortest $s$-$w$ path with $w \ne s$ ends with an edge $\{v, w\}$ where $d(s, v) = d(s, w) - 1$, and its prefix is a shortest $s$-$v$ path, so $\sigma_{sw} = \sum_{v} \sigma_{sv}$ over these $v$. The BFS adds $\sigma[v]$ to $\sigma[w]$ for each such $v$ when $v$ is dequeued, and every such $v$ is dequeued before $w$, so by induction on the distance $\sigma[w] = \sigma_{sw}$. $\square$

Call an edge $\{v, w\}$ with $d(s, v) = d(s, w) - 1$ a *DAG edge* $v \to w$ of $s$. A shortest path from $s$ uses only DAG edges, in their direction.

**Lemma 2 (pair counts on an edge).** For a DAG edge $v \to w$ of $s$ and a vertex $t$, the number of shortest $s$-$t$ paths that use $\{v, w\}$ is $\sigma_{sv} \cdot \sigma_{wt}$ if $d(s, t) = d(s, w) + d(w, t)$, and 0 otherwise.

*Proof.* Such a path is a shortest $s$-$v$ path, then the edge, then a shortest $w$-$t$ path, and its length is $d(s, w) + d(w, t)$; it is shortest exactly when this equals $d(s, t)$. Every choice of the two parts gives a different path. $\square$

Define $\delta_s(x) = \sum_{t \notin \{s, x\}} \sigma_{st}(x) / \sigma_{st}$, where $\sigma_{st}(x)$ is the number of shortest $s$-$t$ paths through the vertex $x$, and the sum runs over the reachable $t$. Define $c_s(v, w) = \sum_{t \ne s} \sigma_{st}(\{v, w\}) / \sigma_{st}$ for a DAG edge $v \to w$.

**Lemma 3 (Brandes' recursion for edges).** For a DAG edge $v \to w$ of $s$, $c_s(v, w) = \frac{\sigma_{sv}}{\sigma_{sw}} (1 + \delta_s(w))$, and $\delta_s(v) = \sum_{w : v \to w} c_s(v, w)$.

*Proof.* By Lemma 2 with $t = w$, the edge lies on $\sigma_{sv}$ of the $\sigma_{sw}$ shortest $s$-$w$ paths. For $t \ne w$ with $w$ on a shortest $s$-$t$ path, $\sigma_{st}(w) = \sigma_{sw} \sigma_{wt}$, so Lemma 2 gives $\sigma_{st}(\{v,w\}) = \frac{\sigma_{sv}}{\sigma_{sw}} \sigma_{st}(w)$; for other $t$ both sides are 0. Summing over $t$ gives the first identity. Every shortest $s$-$t$ path through $v$ with $t \ne v$ leaves $v$ by exactly one DAG edge $v \to w$, so $\sigma_{st}(v) = \sum_w \sigma_{st}(\{v, w\})$; dividing by $\sigma_{st}$ and summing over $t$ gives the second. $\square$

**Lemma 4 (EDGE-BETWEENNESS is exact).** EDGE-BETWEENNESS($H$) returns $B_H(e)$ for every edge $e$ of $H$.

*Proof.* Fix $s$. Line L14 visits $S$ in reverse, so in non-increasing distance. When $w$ is visited, every DAG edge $w \to x$ has $x$ farther from $s$, so $x$ was visited earlier and has added its full share to $\delta[w]$. By induction in this order and Lemma 3, $\delta[w] = \delta_s(w)$ when $w$ is visited, and line L16 adds $c = c_s(v, w)$ to $B[\{v, w\}]$ for each DAG edge $v \to w$. An edge that is not a DAG edge of $s$ (both ends at one distance, or unreached) lies on no shortest path from $s$ and gets nothing, and so does $c_s$. So after line L16, $B[e] = \sum_s \sum_{t \ne s} \sigma_{st}(e)/\sigma_{st}$, the sum over ordered pairs. Unreachable $t$ contribute 0 on both sides. The ordered sum counts each unordered pair twice with the same value, since a path reversed is a shortest path between the same ends, so line L17 gives $B_H(e)$. $\square$

**Lemma 5 (loop invariant).** At the test of line L2, $P$ is the set of components of $H$; $levels$ lists the component partitions of the graphs $H$ seen so far, each once, in order of appearance; and $best$ is the first element of $levels$ with the largest value of $Q_G$.

*Proof.* Line L1 makes it true. In one round, line L5 removes one edge of $H$. Removing an edge $\{u, v\}$ either leaves the components unchanged, when $u$ and $v$ stay connected, or splits the one component that holds it into two. In the first case, the number of components is still $|P|$, line L6 fails and nothing changes, and $P$ is still right. In the second case, the count grows by one, line L7 sets $P$ to the new components and appends this partition, which differs from all earlier ones since the count of components only grows. Line L8 replaces $best$ only when the new value is strictly larger, so $best$ stays the first maximum. $\square$

**Theorem.** GIRVAN-NEWMAN($G$) stops after exactly $m$ rounds. It returns the dendrogram $levels$ of all distinct partitions into components that arise while the edges are removed in the order of line L4, from the components of $G$ to the partition into singletons, and $best$, a partition in $levels$ of largest modularity in $G$, the first one on ties.

*Proof.* Each round removes one edge of the finite set $E$ and adds none, so after $m$ rounds $H$ has no edges and line L2 fails. By Lemma 4, line L4 picks an edge of maximum edge betweenness in the current $H$, as the algorithm requires. By Lemma 5 at exit, $levels$ and $best$ are as stated, and the last partition is the one of the edgeless graph, which is all singletons. $\square$

∎
