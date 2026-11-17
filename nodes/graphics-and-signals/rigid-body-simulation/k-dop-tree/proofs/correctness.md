---
title: The k-DOP tree query reports exactly the pairs of triangles that meet
proves: [correctness, termination]
status: full
---

Let $A$ be a set of $n$ triangles and $B$ a set of $m$ triangles in the plane, and let $g(x) = Rx + t$ be a rigid motion, with $R$ a rotation. The query must report the set $S$ of the pairs $(i, j)$ such that the closed triangle $A_i$ meets the closed triangle $g(B_j)$. We work in the real RAM. Let $d_1, \dots, d_4$ be the fixed directions $(1, 0), (0, 1), (1, 1), (1, -1)$. An 8-DOP is a set $D = \{x : \ell_k \le d_k \cdot x \le h_k \text{ for } k = 1, \dots, 4\}$, stored as its 4 intervals $[\ell_k, h_k]$. For a node $v$ let $T(v)$ be the triangles below it and $D(v)$ its stored 8-DOP.

**Lemma 1 (the build).** The build makes a tree with $n$ leaves, one for each triangle, and $2n - 1$ nodes. Each $D(v)$ contains every triangle of $T(v)$.

*Proof.* The interval $k$ of $D(v)$ is the range of $d_k \cdot p$ over the vertices $p$ below $v$, grown by a margin $\ge 0$. So every such vertex satisfies the 4 pairs of inequalities and is in $D(v)$. An 8-DOP is an intersection of half-planes, so it is convex, and it contains each triangle of $T(v)$, which is the convex hull of three of these vertices. A node with $k \ge 2$ triangles is split at the median of a sorted list into two nonempty halves, so the recursion ends at leaves of one triangle. A binary tree with $n$ leaves in which every inner node has two children has $2n - 1$ nodes. $\square$

Call an 8-DOP tight if each of its 4 intervals is equal to the projection of the set on $d_k$, that is, if each bound is attained by a point of the set.

**Lemma 2 (the volumes are tight).** Every 8-DOP that the code computes from a finite set $X$ of points is tight.

*Proof.* Without a margin, the interval $k$ is the range of $d_k \cdot p$ over $X$. The set contains $X$ and lies in the slab, so its projection is exactly this range. With a margin $e > 0$, let $O = \{y : |d_k \cdot y| \le e \text{ for all } k\}$. The points $(\pm e, 0)$, $(0, \pm e)$ and $(\pm e/2, \pm e/2)$ are in $O$, so the projection of $O$ on each $d_k$ is $[-e, e]$. For $p \in X$ and $y \in O$ the point $p + y$ satisfies the grown bounds, so $X + O$ is in the grown 8-DOP. The projection of $X + O$ on $d_k$ is the range over $X$ grown by $e$ on each side, which is the grown interval. So each grown bound is attained by a point of the set. $\square$

**Lemma 3 (the interval test is exact in the plane).** For two tight 8-DOPs $P$ and $Q$ with the same 4 directions, the test returns false exactly when $P$ and $Q$ are disjoint.

*Proof.* The set $P$ lies in its 4 slabs. So if the intervals $k$ of $P$ and $Q$ are disjoint for some $k$, the sets are disjoint. Conversely, let $P$ and $Q$ be disjoint. They are bounded convex polygons. By the [separating axis theorem](/separating-axis-theorem/) in the plane, there is a separating line parallel to an edge of $P$ or of $Q$. Each edge of an 8-DOP lies on one of its 8 bounding lines $d_k \cdot x = \ell_k$ or $d_k \cdot x = h_k$, so the normal of the separating line is some $d_k$, and the projections of $P$ and $Q$ on $d_k$ are disjoint. The two DOPs are tight, so these projections are their intervals $k$, and the test returns false. $\square$

**Lemma 4 (the moved volume).** Let $C$ be the corners of $D(w)$ for a node $w$ of $B$, and let $M(w)$ be the 8-DOP of the points $g(c)$, $c \in C$. Then $M(w)$ contains $g(T(w))$. At the root $r$ of $B$, the 8-DOP of the moved vertices of $B$ also contains $g(T(r))$.

*Proof.* $D(w)$ is a bounded convex polygon, so it is the convex hull of its corners $C$. The map $g$ is affine, so $g(D(w))$ is the convex hull of $g(C)$. $M(w)$ is convex and contains $g(C)$, so it contains $g(D(w))$, which contains $g(T(w))$ by Lemma 1. At the root, the 8-DOP of the moved vertices contains the moved vertices, and by convexity the moved triangles. $\square$

**Theorem.** The query terminates after at most $(2n - 1)(2m - 1)$ tests of two 8-DOPs and returns $S$.

*Proof.* A pushed pair is always (child, same) or (same, child) of the popped pair, so each pair of nodes is reached at most once, along the unique path of pairs from (root, root). This gives the bound, and the query terminates.

*Soundness.* The code adds $(i, j)$ only at a pair of leaves, after the exact separating axis test of the two triangles on their 6 edge normals, which is exact by the same argument as Lemma 3. So every reported pair is in $S$.

*Completeness.* Let $(i, j) \in S$, with a point $x$ in $A_i \cap g(B_j)$. Call a pair of nodes $(a, b)$ good if $A_i \in T(a)$ and $B_j \in T(b)$. The pair (root, root) is good. If a good pair is popped, then $x \in D(a)$ by Lemma 1 and $x$ is in the moved volume of $b$ by Lemma 4. Both volumes are 8-DOPs with the fixed directions, they are tight by Lemma 2, they share the point $x$, and by Lemma 3 the test does not prune the pair. If both nodes are leaves, they are the leaves of $i$ and $j$, and the code reports $(i, j)$. Otherwise the code pushes the two pairs for the two children of one node, and the child that holds the triangle gives a good pair. The depth of a good pair grows at each step, so the leaves of $i$ and $j$ are popped together after finitely many steps, and $(i, j)$ is reported. $\blacksquare$

**Remarks.** Completeness needs only that the test never prunes two volumes that meet, so it holds in 3D too, where the interval test on $k/2$ directions can report an overlap for two disjoint k-DOPs. Then the test is conservative and the query does extra work, but the exact test at the leaves keeps the result exact. The margin of $10^{-9}$ times the scale in the code only grows the volumes, so the theorem holds for it, and it keeps a contact on the boundary of a volume from being lost to rounding in floating point.
