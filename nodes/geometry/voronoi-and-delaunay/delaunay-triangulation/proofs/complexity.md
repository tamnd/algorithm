---
title: Expected cost of the randomized incremental Delaunay triangulation
proves: [complexity]
status: full
---

**Claim.** Let $P$ be a set of $n \ge 3$ points with no three on a line and no four on a circle, inserted in a uniformly random order. Then the expected number of DAG nodes made is less than $9n$, the expected number of flips is less than $3n$, and the expected number of DAG nodes visited by all calls of LOCATE is at most $16n + 48 n H_n = O(n \log n)$, where $H_n = 1 + 1/2 + \cdots + 1/n$. So the expected total time is $O(n \log n)$ and the expected space is $O(n)$, if each dictionary operation costs $O(1)$. In the worst case over all orders and inputs, the time is $O(n^3)$ and the space $O(n^2)$.

**Notation.** Let $p_1, \ldots, p_n$ be the order and $S_j = \{p_1, \ldots, p_j\}$. By general position, the first three points make the first triangle, line L7 never runs, a ghost is in conflict with a point only by the strict side test, and $S_j$ has exactly one Delaunay triangulation (see [uniqueness](/delaunay-triangulation-uniqueness/)). By the correctness proof, after step $j \ge 3$ the live nodes are $D_j$, the triangles of this triangulation with the ghosts of its hull edges, and step $j \ge 4$ is the [Bowyer-Watson](/bowyer-watson-algorithm/) step on the conflict set $K_j \subseteq D_{j-1}$ of $p_j$. Let $D_j^*$ be the nodes of $D_j$ with $p_j$ as a vertex, and $D_3^* = D_3$. For a node $N \in D_j^*$ let $K(N)$ be the set of points of $P \setminus S_j$ in conflict with $N$. Let $d_j$ be the number of nodes at $p_j$ in $D_j$.

**Lemma 1 (one step).** For $j \ge 4$, step $j$ makes $d_j - 3$ flips and $2 d_j - 3$ nodes, and $E[d_j] < 6$.

*Proof.* Line L6 makes three nodes at $p_j$. Each flip removes one node at $p_j$ and makes two, so the number of live nodes at $p_j$ goes up by one, and it ends at $d_j$. So there are $d_j - 3$ flips and $3 + 2(d_j - 3)$ nodes. Fix the set $S_j$. Then $D_j$ is fixed and $p_j$ is a uniformly random point of $S_j$. By Lemma 2 of the [Bowyer-Watson complexity proof](/bowyer-watson-algorithm/), the sum of $d$ over all points of $S_j$ is $6j - 6 - h < 6j$, so $E[d_j \mid S_j] < 6$. This is [backwards analysis](/backwards-analysis/). $\square$

With $4$ nodes for step $3$, the expected number of nodes is less than $4 + 9(n - 3) < 9n$, and the expected number of flips is less than $3n$, by [linearity of expectation](/linearity-of-expectation/).

**Lemma 2 (charging a visit).** Let LOCATE$(p_r)$ visit a node $N$ made in step $j < r$. If $N$ is in $D_j^*$, then $p_r \in K(N)$. Otherwise $N$ was made and removed in step $j$, its base edge $(x, y)$ is a directed edge of a node $c_N \in K_j$, and $p_r$ is in conflict with $c_N$.

*Proof.* A visited node has $p_r$ in its region, and $p_r$ is not one of its vertices. If $N$ is real, $p_r$ is in the closed triangle, so it is strictly inside its circle by (F1) of the Bowyer-Watson proof. If $N$ is a ghost, its region is strictly beyond its real edge. This gives the first case. In the second case $N = (x, y, p_j)$ was made for a border edge $(x, y)$ of the set $C \subseteq K_j$ of the correctness proof, so $(x, y)$ is an edge of a node $c_N \in C$. Since $N$ was removed in step $j$, it was the $t_1$ of a flip, so the node $t_2$ across $(x, y)$ is in $K_j$ too.

- *$N$ real and $c_N$ real.* The affine functions $f_N$ and $f_{c_N}$ agree on the line $xy$, and $f_N(p_j) = |p_j|^2 < f_{c_N}(p_j)$ since $c_N \in K_j$. As $p_j$ is strictly left of $x \to y$, $f_N \le f_{c_N}$ on the closed left side, which holds $N$. So $|p_r|^2 < f_N(p_r) \le f_{c_N}(p_r)$.
- *$N$ real and $c_N = (x, y, G)$.* Then $p_r$ is in the closed triangle $N$, on the closed left side of $x \to y$, and not on the line $xy$ by general position, so $\mathrm{orient}(x, y, p_r) > 0$.
- *$N$ a ghost.* Say $N$ is the ghost with the real edge $u p_j$ and base edge $(u, G)$; the other case is the mirror image. Then $c_N$ is the old ghost of the hull edge $u \to a$, and $t_2$ the old ghost of the hull edge $w \to u$, and $p_j$ is strictly to the right of both. Let $D$ be the closed cone at $u$ of the points on the closed left of both lines, translated to the origin. It is pointed, since no three points are on a line, and $o - u$ is in its interior, while $p_j - u$ is in the interior of $-D$. A point $z$ of the region of $N$ has $z = o + \lambda (u - o) + \mu (p_j - o)$ with $\lambda, \mu \ge 0$ and $\lambda + \mu > 1$ (Lemma 5 of the correctness proof), so $z - u = (1 - \lambda - \mu)(o - u) + \mu (p_j - u)$ is in the interior of $-D$. So $z$ is strictly right of $u \to a$, and in conflict with $c_N$. $\square$

A node $c$ is the $c_N$ of at most three nodes $N$, one for each of its directed edges, since a border edge, once flipped, never comes back. A node $c \in K_j$ is in $D_i^*$ for the step $i < j$ that made it, and a point $p_r$ with $r > j$ in conflict with $c$ is in $K(c)$. Each node is removed at most once. LOCATE tests at most three children per visited node. So the number of visits, over all $r$, is at most

$$V \le \sum_{j = 3}^{n} \sum_{N \in D_j^*} |K(N)| + 3 \sum_{j = 3}^{n} \sum_{N \in D_j^*} |K(N)| = 4 \sum_{j = 3}^{n} \sum_{N \in D_j^*} |K(N)|.$$

**Lemma 3 (conflicts at one step).** $\sum_{N \in D_3^*} |K(N)| \le 4n$, and for $4 \le j \le n$, $E\left[\sum_{N \in D_j^*} |K(N)|\right] < 12 (n - j) / j$.

*Proof.* The first bound holds as $|D_3| = 4$. Fix $j \ge 4$ and the set $S_j$. A node of $D_j$ has at most three real vertices, and $p_j$ is uniform in $S_j$, so each node is in $D_j^*$ with probability at most $3/j$, and

$$E\left[\sum_{N \in D_j^*} |K(N)| \,\Big|\, S_j\right] \le \frac{3}{j} \sum_{N \in D_j} |K(N)| = \frac{3}{j} \sum_{q \in P \setminus S_j} k(q, S_j),$$

where $k(q, S_j)$ is the number of nodes of $D_j$ in conflict with $q$. If $q$ were inserted next, its conflict set would have $k(q, S_j)$ nodes and, by Lemma 1 of the correctness proof, the new nodes at $q$ would number $k(q, S_j) + 2$; so $k(q, S_j) = d(q) - 2$, where $d(q)$ is the number of nodes at $q$ in the Delaunay triangulation of $S_j \cup \{q\}$. Given $S_j$, the point $p_{j+1}$ is uniform in $P \setminus S_j$ for $j < n$, so $E\left[\sum_{q \notin S_j} k(q, S_j)\right] = (n - j)\, E[d_{j+1} - 2] < 4 (n - j)$ by Lemma 1. Taking the expectation over $S_j$ gives the bound. $\square$

**Proof of the claim.** By Lemma 3, $E[V] \le 4 \left(4n + \sum_{j=4}^{n} 12 (n - j)/j\right) \le 16 n + 48 n H_n$. Outside LOCATE, a step costs $O(1)$ per node made and per pop, which is $O(1 + d_j)$, so $O(n)$ expected in total. The space is the number of nodes and dictionary entries, $O(n)$ expected.

*Worst case.* Before step $j$ there are $2j - 4$ live nodes, so a conflict set has at most $2j$ nodes and step $j$ makes at most $4 + 2 \cdot 2j$ nodes (Lemma 4 of the correctness proof). So the DAG has $O(n^2)$ nodes, a LOCATE path has $O(n^2)$ nodes, and the $n$ locations and the flips take $O(n^3)$ time. These worst-case bounds are only upper bounds; they are not shown to be tight here.

*What is not covered.* With cocircular points, as in a grid, $D_j$ is not unique and depends on the order, so Lemma 1 and Lemma 3 do not apply as stated. The tests on grids show small costs, but this is observed, not proved. $\blacksquare$
