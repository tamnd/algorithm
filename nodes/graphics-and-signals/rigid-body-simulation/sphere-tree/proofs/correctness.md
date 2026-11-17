---
title: The sphere tree query is exact when it runs to the leaves and covers every contact when it stops early
proves: [correctness, termination]
status: full
---

Let $A$ be a set of $n$ triangles and $B$ a set of $m$ triangles in the plane, and let $g(x) = Rx + t$ be a rigid motion, with $R$ a rotation. Let $S$ be the set of the pairs $(i, j)$ such that the closed triangle $A_i$ meets the closed triangle $g(B_j)$. We work in the real RAM. For a node $v$ let $T(v)$ be the triangles below it, and let $c(v)$ and $r(v)$ be the center and the radius of its circle $C(v)$.

**Lemma 1 (the build).** The build makes a tree with $n$ leaves, one for each triangle, and $2n - 1$ nodes. Each circle $C(v)$ contains every triangle of $T(v)$.

*Proof.* The radius is the radius of a circle that holds every vertex below $v$, grown by a margin $\ge 0$. The disk is convex, so it holds each triangle of $T(v)$, which is the convex hull of three of these vertices. The circle need not be the smallest one for this lemma, so the lemma does not depend on the seed of the shuffle. A node with $k \ge 2$ triangles is split at the median of a sorted list into two nonempty halves, so the recursion ends at leaves of one triangle, and a binary tree with $n$ leaves in which every inner node has two children has $2n - 1$ nodes. $\square$

The three loops in the code are Welzl's algorithm: the outer loop keeps the smallest circle of the first $i$ points, the middle loop the smallest circle of the first $j$ points with $p_i$ on the boundary, and the inner loop the circle with $p_i$ and $p_j$ on the boundary. Its correctness is on the page of [Welzl's algorithm](/welzls-algorithm/). The query needs only Lemma 1.

**Lemma 2 (the moved circle).** The disk with the center $g(c(w))$ and the radius $r(w)$ is $g(C(w))$, and it contains $g(T(w))$ for each node $w$ of $B$.

*Proof.* A rigid motion keeps distances, so it maps the disk with the center $c$ and the radius $r$ onto the disk with the center $g(c)$ and the radius $r$. It maps $T(w) \subseteq C(w)$ into $g(C(w))$. $\square$

Two closed disks meet exactly when the distance of their centers is at most the sum of their radii, so the circle test of the code is exact for disks.

**Theorem.** The query terminates after at most $(2n - 1)(2m - 1)$ circle tests. Every pair that it reports is in $S$. With no level limit, it reports all of $S$ and returns no possible pairs. With the level limit $L$, it does at most $2^{L + 1} - 1$ tests, and for each $(i, j) \in S$ that it does not report, there is a returned possible pair $(a, b)$ with $A_i \in T(a)$, $B_j \in T(b)$ and $C(a) \cap g(C(b)) \ne \emptyset$.

*Proof.* Each pair in the frontier of round $\lambda + 1$ is (child, same) or (same, child) of a pair in the frontier of round $\lambda$, so each pair of nodes is reached at most once, along the unique path of pairs from (root, root), and the depth of the pairs in round $\lambda$ is $\lambda$. This bounds the number of tests by the number of pairs of nodes, and the query terminates. A pair is refined into two pairs, so the frontier of round $\lambda$ has at most $2^\lambda$ pairs. With the limit $L$, no pair is pushed after round $L$, so the tests are at most $1 + 2 + \dots + 2^L = 2^{L + 1} - 1$.

*Soundness.* The code adds $(i, j)$ only at a pair of leaves, after the exact separating axis test of the two triangles on their 6 edge normals. So every reported pair is in $S$. A possible pair $(a, b)$ is returned only after its circle test succeeds, so its disks meet.

*Coverage.* Let $(i, j) \in S$, with a point $x$ in $A_i \cap g(B_j)$. Call a pair of nodes $(a, b)$ good if $A_i \in T(a)$ and $B_j \in T(b)$. The pair (root, root) is good and is in the first frontier. If a good pair is tested, then $x \in C(a)$ by Lemma 1 and $x \in g(C(b))$ by Lemma 2, so the disks meet and the test does not prune it. Then one of three things happens. If both nodes are leaves, they are the leaves of $i$ and $j$, and the code reports $(i, j)$. If the round is the limit $L$, the code returns $(a, b)$ as a possible pair, which has the stated property. Otherwise the code pushes the two pairs for the two children of one node, and the child that holds the triangle gives a good pair in the next frontier. The depth of the good pair grows by one in each round, so one of the first two cases happens. With no limit, only the first case can happen, so $(i, j)$ is reported, and no possible pair is ever returned. $\blacksquare$

**Remarks.** The same proof holds in 3D with balls, and it holds for a tree whose spheres come from the medial axis, as long as the sphere of each node holds all the geometry below it. The margin of $10^{-9}$ times the scale in the code only grows the radii, so the theorem holds for it, and it keeps a contact on a circle from being lost to rounding in floating point.
