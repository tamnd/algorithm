---
title: BUILD computes the relative neighborhood graph, which contains every minimum spanning tree and lies in the Gabriel graph
proves: [correctness, termination]
status: full
---

**Setting.** $P = \{p_0, \ldots, p_{n-1}\}$ is a set of distinct points in the plane. The open lune of $p_i$ and $p_j$ is $L_{ij} = \{r : \|p_i - r\| < \|p_i - p_j\| \text{ and } \|p_j - r\| < \|p_i - p_j\|\}$, the intersection of the two open disks of radius $\|p_i - p_j\|$ centered at $p_i$ and $p_j$. The pair $\{i, j\}$ is an RNG edge when no $p_k$ with $k \ne i, j$ lies in $L_{ij}$.

**Lemma 1 (the test of line L5).** For $k \ne i, j$, line L5 succeeds if and only if $p_k \in L_{ij}$.

*Proof.* Line L2 sets $d = \|p_i - p_j\|^2$. Line L5 succeeds when $\max(\|p_i - p_k\|^2, \|p_j - p_k\|^2) < d$, that is, when both squared distances are less than $d$. Squaring is increasing on non-negative numbers, so this holds exactly when both distances are less than $\|p_i - p_j\|$. $\square$

**Lemma 2 (BUILD is correct).** After BUILD, $j \in adj[i]$ and $i \in adj[j]$ hold exactly for the RNG edges $\{i, j\}$, and there are no other entries.

*Proof.* Lines L1 to L7 consider each unordered pair once, and only line L7 writes to $adj$. For a fixed pair, $empty$ starts true at line L3 and becomes false at line L6 exactly when line L5 finds a $k$ with $p_k \in L_{ij}$ (Lemma 1); it never becomes true again, so stopping the loop early is safe. Line L7 adds the edge in both directions exactly when no such $k$ exists. Lines L8 and L9 only read $adj$. $\square$

**Termination.** All loops run over finite index ranges, so BUILD performs at most $\binom{n}{2}(n - 2)$ lune tests.

**Lemma 3 (minimum spanning trees).** If $\{p, q\}$ is an edge of some Euclidean minimum spanning tree $T$ of $P$, then $\{p, q\}$ is an RNG edge.

*Proof.* Suppose some $r \in P \setminus \{p, q\}$ lies in the lune, so $\|p - r\| < \|p - q\|$ and $\|q - r\| < \|p - q\|$. Removing $pq$ from $T$ leaves two trees, one containing $p$ and one containing $q$. If $r$ is in the tree of $p$, the edge $rq$ joins the two trees; otherwise $pr$ does. Either edge is shorter than $pq$, so adding it gives a spanning tree lighter than $T$, a contradiction. $\square$

**Lemma 4 (the RNG is in the Gabriel graph).** Every RNG edge is a Gabriel edge.

*Proof.* If $\{p, q\}$ is not a Gabriel edge, some third point $r$ has $(p - r) \cdot (q - r) \le 0$, and
$$\|p - q\|^2 = \|p - r\|^2 + \|q - r\|^2 - 2 (p - r) \cdot (q - r) \ge \|p - r\|^2 + \|q - r\|^2.$$
Both terms on the right are positive since the points are distinct, so both are less than $\|p - q\|^2$: $r$ is in the lune, and $\{p, q\}$ is not an RNG edge. $\square$

**Conclusion.** By Lemma 2 BUILD stores exactly the relative neighborhood graph, and it terminates. By Lemma 3 the graph contains a spanning tree, so it is connected. By Lemma 4 and the inclusion of the Gabriel graph in every Delaunay triangulation (proved on the [Gabriel graph](/gabriel-graph/) page), it is a subgraph of a planar straight-line graph, so it is planar and has at most $3n - 6$ edges for $n \ge 3$. $\blacksquare$
