---
title: Every triangulation that DistMesh returns is an exact Delaunay mesh, and the loop stops only because of its cap
proves: [correctness, termination]
status: full
---

**What is proved and what is not.** The proof below covers the parts of DistMesh that have a proof: each retriangulation (L5 and L11) gives triangles that are counterclockwise, conforming and Delaunay for the rounded points, and for a convex domain with a true signed distance function every returned triangle lies in the domain. It does not cover the force iteration L3 to L10. There is no proof that the points converge, and no proof that the final triangles have a bounded angle. Persson and Strang give no such proof either. The implementation stops because L3 has an iteration cap, and that is the whole termination argument.

**Notation.** The points are distinct integer points $P$ (the float positions times $2^{24}$, rounded). For a triangle $t$, $D_t$ is its open circumdisk and $C_t$ its circle. ORIENT2D and INCIRCLE are exact on integers.

**Lemma 1 (pencil of circles).** Let $x \ne y$, let $H^+$ and $H^-$ be the two open half planes of the line $xy$, and let $n$ be the unit normal pointing into $H^+$. Every circle through $x$ and $y$ has its centre at $m + s n$ with $m = (x + y)/2$ and one real $s$. Let $D(s)$ be its open disk. If $s < s'$, then $D(s) \cap H^+ \subsetneq D(s') \cap H^+$ and $D(s') \cap H^- \subsetneq D(s) \cap H^-$, and the circle of $D(s)$ in $H^+$ lies inside $D(s')$. Every $D(s)$ meets the line $xy$ in the open segment between $x$ and $y$.

*Proof.* The power of a point $q$ with respect to the circle with parameter $s$ is $|q - m - s n|^2 - r(s)^2$ with $r(s)^2 = |x - m|^2 + s^2$. It equals $|q - m|^2 - |x - m|^2 - 2 s\,(q - m)\cdot n$, which is affine in $s$. For $q \in H^+$, $(q - m)\cdot n > 0$, so the power strictly decreases as $s$ grows: a point of $H^+$ inside or on the circle for $s$ is strictly inside for $s'$. For $q \in H^-$ the power strictly increases with $s$. On the line, $(q - m)\cdot n = 0$, so the power does not depend on $s$, and it is negative exactly on the open segment $xy$. $\square$

**Lemma 2 (adjacent triangles).** Suppose every triangle of a triangulation has an empty open circumdisk. Let $t$ and $u$ share the edge $xy$, with $t$ in $H^+$ and $u$ in $H^-$, and parameters $s_t$, $s_u$. Then $s_u \le s_t$, so $D_t \cap H^- \subseteq D_u \cap H^-$.

*Proof.* Let $w$ be the third vertex of $u$; it lies on $C_u$ and in $H^-$. If $s_t < s_u$, Lemma 1 for $H^-$ puts the points of $C_u$ in $H^-$ inside $D_t$, so $w \in D_t$, which is not empty. $\square$

**Theorem 3 (Bowyer-Watson in DELAUNAY).** After each insertion, the triangles form a triangulation of the super triangle, every triangle is counterclockwise, and every open circumdisk contains none of the inserted points.

*Proof.* By induction on the insertions. At the start there is one counterclockwise triangle and no inserted point. Let $p$ be the next point. It is strictly inside the super triangle, because the super triangle is 64 times larger than the box of the points.

*The start triangle is bad.* The first loop of DELAUNAY finds a closed triangle $t_0$ that contains $p$. The points are distinct, so $p$ is not a vertex, and a closed triangle without its vertices lies in its open circumdisk. So INCIRCLE gives a positive value.

*All bad triangles are found.* Call a triangle bad if $p \in D_t$. Let $t$ be bad and pick a point $c$ inside $t$ so that the segment from $c$ to $p$ misses every vertex. Follow the segment: it crosses triangles $t = t_0', t_1', \dots, t_k'$, where $t_k'$ contains $p$. If $t_i'$ is bad and the segment leaves it through the edge $xy$ into $t_{i+1}'$, then $p$ is in $H^-$ or on the open edge $xy$ (with $t_i'$ in $H^+$). In the first case, Lemma 2 gives $p \in D_{t_i'} \cap H^- \subseteq D_{t_{i+1}'}$. In the second case, $p$ is on the open segment $xy$, which by Lemma 1 lies in both disks. So $t_{i+1}'$ is bad, and $t$ is joined to a bad triangle that contains $p$ by a path of bad neighbours. The triangles that contain $p$ are $t_0$ and, if $p$ is on an edge, the neighbour across it, which is also bad. The search grows the cavity from $t_0$ through shared edges, so it finds every bad triangle.

*The cavity is star shaped from $p$.* Let $xy$ be an edge of the cavity boundary, with the bad triangle $t$ in $H^+$. If the other side of $xy$ has no triangle, $xy$ is an edge of the super triangle, and $p$, which is strictly inside it, is in $H^+$. Otherwise the triangle $u$ on the other side is good. If $p$ were in $H^-$, Lemma 2 would give $p \in D_u$. If $p$ were on the line $xy$, it would be on the open segment, since $p \in D_t$, and then $p \in D_u$ by Lemma 1. Both contradict that $u$ is good. So $p \in H^+$, and the new triangle $(x, y, p)$ is counterclockwise. The new triangles are the cones from $p$ over the boundary of a region that is star shaped from $p$, so they tile the cavity, and the triangulation outside it does not change.

*The new disks are empty.* Take the new triangle $(x, y, p)$ with parameter $s_p$. Since $p \in H^+$ is inside $C_t$, Lemma 1 gives $s_p < s_t$. If a good triangle $u$ is across $xy$, then $p$ is not inside $D_u$, and Lemma 1 gives $s_u \le s_p$. So $D_p \cap H^+ \subseteq D_t$ and $D_p \cap H^- \subseteq D_u$, and $D_p$ on the line is the open segment $xy$, which lies in $D_t$. The old disks $D_t$ and $D_u$ held no earlier point, so $D_p$ holds none either; $p$ is on $C_p$. If no triangle is across $xy$, the side $H^-$ is outside the super triangle and holds no point. The disks of the triangles outside the cavity do not contain $p$, by the definition of bad. $\square$

**Corollary 4 (the returned triangles).** The triangles returned by DELAUNAY, the ones with no super vertex, are counterclockwise, have disjoint interiors, share edges properly, and have empty open circumdisks with respect to all input points. Each step L5 and L11 keeps a subset of them, so the DistMesh output has the same properties for the returned rounded points. This is the property the tests check with an exact INCIRCLE against every point.

The super triangle is finite, so a thin triangle on the convex hull can be missing from the result when the hull has nearly collinear points. The returned triangles are still Delaunay, and in the tests the square is covered exactly.

**Proposition 5 (inside a convex domain).** Let the domain $\Omega = \{x : f_d(x) \le 0\}$ be convex. If every returned point satisfies $f_d \le 0$, every returned triangle lies in $\Omega$.

*Proof.* A triangle is the convex hull of its vertices, and a convex set contains the convex hull of any of its points. $\square$

For the disk, the projection $p - f_d(p) \nabla f_d(p)$ with the exact gradient moves a point outside onto the circle, and the numerical gradient and the rounding to $2^{-24}$ leave it within about $10^{-7}$ of it, which is what the test checks. For a nonconvex domain, the centroid test of L5 does not prove that a triangle lies inside: a triangle can cut across a thin notch with its centroid in the domain. That case is a known pitfall of the method, not a proved property.

**Termination.** DELAUNAY stops, since each insertion visits finitely many triangles. Each pass of L3 to L10 does finite work. L3 runs at most `max_iter` times. So DISTMESH stops. Whether L10 is reached before the cap is a measured fact: with $h_0 = 0.2$ on the unit disk it took 90 iterations, with $h_0 = 0.1$ it took 197, and on the square with $h_0 = 0.25$ it took 51.
