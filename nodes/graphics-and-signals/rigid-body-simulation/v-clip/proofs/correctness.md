---
title: The 2D V-Clip walk always terminates, with a closest pair of features or a witness of penetration
proves: [correctness, termination]
status: full
---

Let $A$ and $B$ be strictly convex polygons with vertices in counterclockwise order, and use exact arithmetic. Features are vertices and closed edges. For a closed convex set $C$, $\pi_C(x)$ is the point of $C$ closest to $x$. For an edge $e = [e_0, e_1]$ with direction $d = e_1 - e_0$ and outward unit normal $n_e$, $s_e(x) = n_e \cdot (x - e_0)$, and $e(\lambda) = e_0 + \lambda d$ for $\lambda \in [0, 1]$. Strict convexity gives $s_e(y) \le 0$ on the polygon of $e$, with equality only on $e$.

The Voronoi region of a vertex $a$ with neighbors $a^-$, $a^+$ is $VR(a) = \{x : (x - a) \cdot (a^\pm - a) \le 0\}$, two half-planes, each with the edge $[a, a^\pm]$ as its neighbor. The Voronoi region of an edge is $VR(e) = \{x : (x - e_0) \cdot d \ge 0,\ (x - e_1) \cdot d \le 0,\ s_e(x) \ge 0\}$.

We use four facts. Their proofs are on the page of the [Lin-Canny algorithm](/lin-canny-closest-features/), in its correctness proof.

- **(F1)** If $x \in VR(f)$, then $\pi_P(x) = \pi_f(x)$ for the polygon $P$ of $f$.
- **(F2)** If $p = \pi_A(q)$ and $q = \pi_B(p)$, then $|p - q| = d(A, B)$, and $A \cap B = \emptyset$ if $p \ne q$.
- **(F3)** If $k$ maximizes $s_k(v)$ over the edges of $Q$, then $v \in Q$ when $s_k(v) \le 0$, and $\pi_Q(v) \in k$ when $s_k(v) > 0$.
- **(F4)** If $(c - a) \cdot (a' - a) > 0$ for a neighbor $a'$ of the vertex $a$, then the edge $[a, a']$ has a point closer to $c$ than $a$.

**Lemma 1 (the clip).** Let $v$ be a vertex of $P$ and $e$ an edge of $Q$. For a plane of $VR(v)$ with direction $u$, let $f(\lambda) = (e(\lambda) - v) \cdot u$, an affine function. CLIP returns:

1. a plane with $f(0) > 0$ and $f(1) > 0$ (simple exclusion), if one exists; otherwise
2. $\lambda_l = \max$ of the roots of $f$ over the planes with $f(0) > 0$ (or 0), with $N_l$ the plane that gives it, and $\lambda_u = \min$ of the roots over the planes with $f(1) > 0$ (or 1), with $N_u$.

Then $e(\lambda) \in VR(v)$ exactly for $\lambda \in [\lambda_l, \lambda_u]$, and the plane $N_l$ is violated by $e(\lambda)$ for all $\lambda \in [0, \lambda_l)$, and $N_u$ for all $\lambda \in (\lambda_u, 1]$.

*Proof.* Each half-plane $f \le 0$ meets the segment in an interval: $[0, 1]$ if $f(0), f(1) \le 0$, $[\text{root}, 1]$ if $f(0) > 0 \ge f(1)$, $[0, \text{root}]$ if $f(0) \le 0 < f(1)$, and the empty set if both are positive. The intersection of the intervals of the two planes is $[\lambda_l, \lambda_u]$ when no plane excludes all. The plane that gives $\lambda_l$ has $f(0) > 0$ and $f(\lambda_l) = 0$, so $f > 0$ on $[0, \lambda_l)$ by linearity. The same holds for $\lambda_u$. $\square$

**Lemma 2 (the derivative tests).** Let $g(\lambda) = |e(\lambda) - v|^2$ and $\lambda^* = \arg\min_{[0, 1]} g$, so $e(\lambda^*) = \pi_e(v)$. Then $g'(\lambda) = 2 (e(\lambda) - v) \cdot d$, and:

- if $\lambda_l > 0$ and $g'(\lambda_l) > 0$, then $\lambda^* < \lambda_l$;
- if $\lambda_u < 1$ and $g'(\lambda_u) < 0$, then $\lambda^* > \lambda_u$;
- if $[\lambda_l, \lambda_u]$ is not empty and neither test fires, then $\lambda^* \in [\lambda_l, \lambda_u]$.

*Proof.* $g$ is a convex quadratic with $g'' = 2|d|^2 > 0$, so it has one minimizer $\lambda^*$ on $[0, 1]$, and $g' < 0$ before the unconstrained minimizer and $g' > 0$ after it. The first two claims follow. For the third, suppose $\lambda^* < \lambda_l$. Then $\lambda_l > 0$, and $g$ is increasing on $[\lambda^*, 1]$, so $g'(\lambda_l) > 0$ unless $\lambda_l$ is the unconstrained minimizer, which would give $\lambda^* = \lambda_l$. So the first test fires, a contradiction. The case $\lambda^* > \lambda_u$ is symmetric. $\square$

**The potential.** As for Lin-Canny, let $\Phi = d(f_A, f_B)$, let $\delta$ be the sum of the dimensions, and order $(\Phi, \delta)$ lexicographically.

**Lemma 3 (each move lowers the potential).** Every move of lines L3, L4, L8, L10, L11, L13, L14, L15 and L16 gives a state with a smaller $(\Phi, \delta)$.

*Proof.*

- L3 and L4: by (F4), $\Phi$ drops.
- L8: two disjoint segments have a closest pair with an end point of one of them (the squared distance is a convex quadratic on the parameter square whose minimum is on the boundary). So $\Phi$ is unchanged and $\delta$ drops from 2 to 1.
- L10: if $(v - e_0) \cdot d < 0$, then $g$ increases on $[0, 1]$ and $\pi_e(v) = e_0$. So $\Phi$ is unchanged and $\delta$ drops. The same holds for $e_1$.
- L11: $v$ is in the slab of $e$ with $s_e(v) \le 0$. If HANDLE-LOCAL-MIN returns $k$, then $s_k(v) > 0$, so $v \notin Q$ and by (F3) $d(v, k) = d(v, Q) \le d(v, e)$. Equality would put $\pi_Q(v)$ on $e$ at the foot of the perpendicular, with $v - \pi_Q(v) = s_e(v) n_e$ and $s_e(v) < 0$, which has a positive dot product with $y - \pi_Q(v)$ for inner points $y$ of $Q$. This contradicts the projection property. So $\Phi$ drops.
- L13: every point of $e$ violates the plane, in particular $\pi_e(v)$. By (F4) the new edge has a point closer to $\pi_e(v)$ than $v$, so $\Phi$ drops.
- L14: the clipped interval is empty, so no point of $e$ is in $VR(v)$, and $\pi_e(v)$ violates some plane. By (F4), $\Phi$ drops.
- L15 and L16: by Lemma 2, $\lambda^* < \lambda_l$, and by Lemma 1 the plane $N_l$ is violated by $e(\lambda^*) = \pi_e(v)$. By (F4), $\Phi$ drops. L16 is symmetric. $\square$

**Theorem.** V-CLIP ends after at most $4|A||B|$ moves, for every input pair of strictly convex polygons and every start pair of features. If it returns DISJOINT, the returned points are a closest pair, they lie on the returned features, and their distance is $d(A, B) > 0$. It returns PENETRATION exactly when $A \cap B \ne \emptyset$, and then the returned features meet: two edges that intersect, or a vertex inside the other polygon, or two equal vertices.

*Proof.* By Lemma 3 no state repeats, and there are $4|A||B|$ states.

L5 with $a \ne b$: $b \in VR(a)$ and $a \in VR(b)$, so by (F1) the points are mutual closest points, and (F2) gives the claim. With $a = b$ the return is PENETRATION with a common vertex.

L17: the vertex passed L10 and L11, so $v \in VR(e)$ with $s_e(v) > 0$, and by (F1) $q = \pi_e(v)$ is the closest point of the polygon of $e$ to $v$. By Lemma 2, $q = e(\lambda^*)$ with $\lambda^* \in [\lambda_l, \lambda_u]$, so by Lemma 1, $q \in VR(v)$, and by (F1) $v$ is the closest point of its polygon to $q$. By (F2) the answer is right, and $|v - q| \ge s_e(v) > 0$.

L7 returns two edges that intersect. L19 returns a vertex with all signed distances $\le 0$, which is inside the other polygon by (F3). So every PENETRATION answer has a witness and is right. Conversely, if $A \cap B \ne \emptyset$, then (F2) rules out a DISJOINT answer, and since the walk ends, it returns PENETRATION. $\blacksquare$

**Remark.** No step of the proof uses a tolerance. Each test is a sign of a polynomial in the input, with a strict or a weak inequality, and the proof holds for each choice that the code makes at a tie. This is the 2D form of the robustness claim of Mirtich (1998): the walk needs no tolerances and cannot cycle, also on degenerate input. In floating point a sign can be wrong, and then this proof does not apply. The implementation bounds the number of moves, so that it stops with an error instead of a loop.
