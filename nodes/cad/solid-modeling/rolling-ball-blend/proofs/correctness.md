---
title: The rolling-ball cross sections lie on the envelope and meet both surfaces with the same tangent plane
proves: [correctness]
status: full
---

Let $S_1$ and $S_2$ be surfaces with signed distance functions $\mathrm{sd}_1$ and $\mathrm{sd}_2$. Assume that on an open set $U$ each $\mathrm{sd}_i$ is $C^2$ with $|\nabla \mathrm{sd}_i| = 1$, that $\mathrm{sd}_i(x)$ is the signed distance from $x$ to $S_i$, and that the nearest point of $S_i$ to $x$ is unique and equal to $x - \mathrm{sd}_i(x) \, n_i(x)$, where $n_i = \nabla \mathrm{sd}_i$. This holds near a smooth surface at distances below its smallest radius of curvature on that side, and everywhere for planes, and for cylinders away from the axis. Fix $r > 0$ and $s_1, s_2 \in \{+1, -1\}$.

Let $c : (\alpha, \beta) \to U$ be a $C^1$ curve with $c'(\sigma) \ne 0$ and $\mathrm{sd}_i(c(\sigma)) = s_i r$ for $i = 1, 2$ and all $\sigma$, the exact spine. Write $n_i$ for $n_i(c(\sigma))$, $p_i(\sigma) = c(\sigma) - s_i r n_i$, and $K(\sigma) = \{x : |x - c(\sigma)| = r, \ (x - c(\sigma)) \cdot c'(\sigma) = 0\}$.

**Lemma 1 (the tangent).** $n_1 \cdot c' = n_2 \cdot c' = 0$. If $n_1 \nparallel n_2$, then $c'$ is a nonzero multiple of $n_1 \times n_2$.

*Proof.* Differentiate $\mathrm{sd}_i(c(\sigma)) = s_i r$ by the chain rule: $\nabla \mathrm{sd}_i(c) \cdot c' = 0$. A nonzero vector perpendicular to two independent vectors is a multiple of their cross product. $\square$

**Lemma 2 (the envelope).** Let $E$ be the envelope of the spheres $\Sigma(\sigma) = \{x : |x - c(\sigma)|^2 = r^2\}$, the set of points $x$ for which some $\sigma$ solves $G(x, \sigma) = |x - c(\sigma)|^2 - r^2 = 0$ and $\partial_\sigma G(x, \sigma) = 0$. Then the points of $E$ for the parameter $\sigma$ form the circle $K(\sigma)$, which has radius $r$ and lies in the plane through $c(\sigma)$ normal to $c'(\sigma)$.

*Proof.* $\partial_\sigma G = -2 (x - c(\sigma)) \cdot c'(\sigma)$. So the two conditions are exactly $|x - c| = r$ and $(x - c) \cdot c' = 0$, which define $K(\sigma)$. The plane through the center $c$ cuts the sphere in a great circle of radius $r$. $\square$

**Lemma 3 (the contact points).** $p_i(\sigma) \in S_i$, $p_i(\sigma) \in K(\sigma)$, and $c(\sigma) - p_i(\sigma) = s_i r \, n_i(p_i)$.

*Proof.* By the assumption on nearest points, $c - \mathrm{sd}_i(c) n_i(c) = c - s_i r n_i$ is the nearest point of $S_i$ to $c$, so $p_i \in S_i$. Next, $|p_i - c| = r |n_i| = r$, and $(p_i - c) \cdot c' = -s_i r \, n_i \cdot c' = 0$ by Lemma 1, so $p_i \in K(\sigma)$. Finally, the gradient of a distance function is constant along the segment from a point to its nearest point on the surface, because the distance grows with slope $1$ along that segment, so $n_i(p_i) = n_i(c)$, and $c - p_i = s_i r n_i(p_i)$. $\square$

**Lemma 4 (no cut near the contact).** The ball $\{x : |x - c(\sigma)| < r\}$ contains no point of $S_i$ that lies in $U$.

*Proof.* A point $y \in S_i$ with $|y - c| < r$ would give $|\mathrm{sd}_i(c)| \le |y - c| < r$, against $|\mathrm{sd}_i(c)| = r$. $\square$

**Lemma 5 (tangency).** At $p_i$, the sphere $\Sigma(\sigma)$, the envelope $E$ and the surface $S_i$ have the same tangent plane, the plane through $p_i$ normal to $n_i(p_i)$.

*Proof.* The normal of the sphere at $p_i$ is $(p_i - c)/r = -s_i n_i(p_i)$ by Lemma 3, which is parallel to the normal of $S_i$. The sphere touches $E$ along $K(\sigma)$, which contains $p_i$: at a regular point of the envelope, the envelope and the sphere through it have the same tangent plane, because $\nabla_x G(x, \sigma) = 2(x - c)$ is normal to both. So all three normals are parallel. $\square$

**Theorem.** Let the spine points computed at lines L1 to L7 be exact points $c(\sigma_0), c(\sigma_1), \ldots$ of a regular spine with $n_1 \nparallel n_2$. Then for each one, the points $p_1$ and $p_2$ of line L9 are the points where the ball of radius $r$ around $c$ touches $S_1$ and $S_2$, the arc of line L10 lies on the characteristic circle $K(\sigma_j)$ and hence on the envelope of the rolling ball, and the envelope meets each $S_i$ at $p_i$ with the same tangent plane. So the blend is a $G^1$ blending surface along the trimlines $\sigma \mapsto p_1(\sigma)$ and $\sigma \mapsto p_2(\sigma)$, and the ball does not cut either surface near the contact.

*Proof.* Line L9 computes $p_i = c - s_i r n_i(c)$, which by Lemma 3 lies on $S_i$ and on $K(\sigma_j)$. The arc of line L10 is a great circle arc of radius $r$ around $c$ from $p_1$ to $p_2$. The great circle through two points of a sphere that are not antipodal is unique, and $K(\sigma_j)$ is a great circle through $p_1$ and $p_2$ by Lemmas 2 and 3. The points are not antipodal: $p_1 - c$ and $p_2 - c$ are $-s_1 r n_1$ and $-s_2 r n_2$, which are not opposite because $n_1 \nparallel n_2$. So the arc lies on $K(\sigma_j)$, and by Lemma 2 on $E$. Tangency is Lemma 5, and the last claim is Lemma 4. $\blacksquare$

**What is not claimed.** The curvature of the blend across a trimline is $1/r$ in the direction of the arc, while the curvature of $S_i$ in that direction is in general different, for example $0$ for a plane. So the join is not $G^2$ in general. The theorem is about exact spine points. The computed points satisfy the two equations only within the Newton tolerance, and the trace can leave the branch it started on if the step $h$ is long compared with the distance to another branch.
