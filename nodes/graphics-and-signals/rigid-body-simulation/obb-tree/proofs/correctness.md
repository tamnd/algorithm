---
title: The OBB tree query reports exactly the pairs of triangles that meet
proves: [correctness, termination]
status: full
---

Let $A$ be a set of $n$ triangles and $B$ a set of $m$ triangles in the plane, and let $g(x) = Rx + t$ be a rigid motion, with $R$ a rotation. The query must report the set $S$ of the pairs $(i, j)$ such that the closed triangle $A_i$ meets the closed triangle $g(B_j)$. We work in the real RAM. For a node $v$ let $T(v)$ be the triangles below it and $\beta(v)$ its box.

**Lemma 1 (the build).** The build makes a tree with $n$ leaves, one for each triangle, and $2n - 1$ nodes. Each box contains every vertex of every triangle below its node.

*Proof.* The box of a node has a unit axis $u$, the axis $u^\perp$, and the intervals $[\min_p u \cdot p, \max_p u \cdot p]$ and $[\min_p u^\perp \cdot p, \max_p u^\perp \cdot p]$ over the vertices $p$ below the node, each grown by a margin $\ge 0$. A point is in the box exactly when its two coordinates are in the two intervals, so every vertex below the node is in the box. This holds for any choice of $u$, so the principal axis is a matter of a tight fit, not of correctness. A node with $k \ge 2$ triangles splits them into two nonempty sets: by the mean, or by the median if the mean leaves one side empty. So the sizes go down, the recursion ends at leaves of one triangle, and a binary tree with $n$ leaves in which every inner node has two children has $2n - 1$ nodes. $\square$

The boxes are convex, so by Lemma 1 the box of $v$ contains every triangle of $T(v)$, which is the convex hull of its vertices.

**Lemma 2 (the box test is exact).** For two boxes $P$ and $Q$, the test returns false exactly when $P$ and $Q$ are disjoint.

*Proof.* The test projects both boxes on each of the 4 axes $u_P, u_P^\perp, u_Q, u_Q^\perp$. The projection of a box with the center $c$, the axes $u, u^\perp$ and the half extents $h_1, h_2$ on a unit vector $L$ is the interval with the center $L \cdot c$ and the radius $h_1 |L \cdot u| + h_2 |L \cdot u^\perp|$. The test returns false when the two intervals on some axis are disjoint, and then the boxes are disjoint. Conversely, by the [separating axis theorem](/separating-axis-theorem/) in the plane, two disjoint convex polygons have a separating line parallel to an edge of one of them. Then their projections on the normal of that edge are disjoint. The edge normals of a box are its two axes, so one of the 4 axes separates them. $\square$

The same argument with the 6 edge normals shows that the triangle test is exact.

**Theorem.** The query terminates after at most $(2n - 1)(2m - 1)$ box tests and returns $S$.

*Proof.* A rigid motion keeps containment, so $g(\beta(w))$ contains $g(T(w))$ for each node $w$ of $B$, and the code moves the box of $w$ by $g$. A pushed pair is always (child, same) or (same, child) of the popped pair, so each pair of nodes $(a, b)$ is reached at most once, along the unique path of pairs from (root, root). This gives the bound on the tests, and the query terminates.

*Soundness.* The code adds $(i, j)$ only at a pair of leaves after the exact triangle test, so every reported pair is in $S$.

*Completeness.* Let $(i, j) \in S$, with a point $x$ in $A_i \cap g(B_j)$. Call a pair of nodes $(a, b)$ good if $A_i \in T(a)$ and $B_j \in T(b)$. The pair (root, root) is good. If a good pair is popped, then $x \in \beta(a)$ and $x \in g(\beta(b))$, so the boxes meet, and by Lemma 2 the test does not prune the pair. If both nodes are leaves, they are the leaves of $i$ and $j$, and the code reports $(i, j)$. Otherwise the code pushes the two pairs for the two children of one node, and the child that holds the triangle gives a good pair. The depth of a good pair grows at each step, so after finitely many steps the leaves of $i$ and $j$ are popped together, and $(i, j)$ is reported. $\blacksquare$

**Remarks.** In 3D the same proof works with the 15 axes of Gottschalk, Lin and Manocha: the 3 face normals of each box and the 9 cross products of an edge direction of one box with an edge direction of the other. The code grows each box by a margin of $10^{-9}$ times the scale of the coordinates, so that rounding in floating point cannot remove a contact point from a box. The theorem holds for any margin $\ge 0$.
