---
title: The 2D Lin-Canny walk terminates at a closest pair of features, or reports that the polygons intersect
proves: [correctness, termination]
status: full
---

Let $A$ and $B$ be strictly convex polygons with vertices in counterclockwise order. A feature is a vertex or a closed edge. For a point $x$ and a closed convex set $C$, write $\pi_C(x)$ for the unique point of $C$ closest to $x$, and $d(X, Y)$ for the distance between two sets. For an edge $e = [e_0, e_1]$ of a polygon $P$, let $n_e$ be its outward unit normal and $s_e(x) = n_e \cdot (x - e_0)$ the signed distance of $x$ to its line. Since $P$ is strictly convex, $s_e(y) \le 0$ for all $y \in P$, with equality only for $y \in e$.

The Voronoi regions used by the walk are

- for a vertex $a$ with neighbors $a^-$ and $a^+$: $VR(a) = \{x : (x - a) \cdot (a^- - a) \le 0,\ (x - a) \cdot (a^+ - a) \le 0\}$;
- for an edge $e$: $VR(e) = \{x : (x - e_0) \cdot (e_1 - e_0) \ge 0,\ (x - e_1) \cdot (e_0 - e_1) \ge 0,\ s_e(x) \ge 0\}$.

**Lemma 1 (Voronoi regions).** If $x \in VR(f)$ for a feature $f$ of $P$, then $\pi_P(x) = \pi_f(x)$.

*Proof.* It suffices to find $c \in f$ with $(x - c) \cdot (y - c) \le 0$ for all $y \in P$, because then $|x - y|^2 = |x - c|^2 + |y - c|^2 - 2 (x - c) \cdot (y - c) \ge |x - c|^2$. For a vertex, take $c = a$. Each $y \in P$ is $a + \alpha (a^- - a) + \beta (a^+ - a)$ with $\alpha, \beta \ge 0$, because $P$ lies in the angle of $P$ at $a$. So $(x - a) \cdot (y - a) \le 0$ by the two inequalities of $VR(a)$. For an edge, the two slab inequalities say that the foot $c$ of the perpendicular from $x$ to the line of $e$ lies on $e$. Then $x - c = s_e(x)\, n_e$ with $s_e(x) \ge 0$, and $(x - c) \cdot (y - c) = s_e(x)\, s_e(y) \le 0$. $\square$

**Lemma 2 (mutual closest points).** If $p \in A$, $q \in B$, $p = \pi_A(q)$ and $q = \pi_B(p)$, then $|p - q| = d(A, B)$. If moreover $p \ne q$, then $A \cap B = \emptyset$.

*Proof.* Let $u = q - p$. The projection property gives $u \cdot (x - p) \le 0$ for $x \in A$ and $u \cdot (y - q) \ge 0$ for $y \in B$. So $u \cdot (y - x) \ge u \cdot (q - p) = |u|^2$ and, by Cauchy-Schwarz, $|y - x| \ge |u|$ for all $x \in A$, $y \in B$ when $u \ne 0$. If $u \ne 0$, also $u \cdot (y - x) > 0$, so $x \ne y$. $\square$

**Lemma 3 (the largest signed distance).** Let $v$ be a point and let $k$ maximize $s_k(v)$ over the edges of $B$. If $s_k(v) \le 0$, then $v \in B$. If $s_k(v) > 0$, then $\pi_B(v) \in k$.

*Proof.* $B$ is the intersection of the inner half-planes of its edges, which gives the first claim. Now let $v \notin B$, $c = \pi_B(v)$ and $u = v - c \ne 0$. For each edge $j$, $s_j(v) = n_j \cdot u + s_j(c)$. If $c$ is inside an edge $k_0$, then $u = |u| n_{k_0}$, so $s_{k_0}(v) = |u|$, while for $j \ne k_0$ we have $s_j(c) < 0$ and $s_j(v) < |u|$. If $c$ is a vertex between the edges $k_1$ and $k_2$, then $u$ is in the cone spanned by $n_{k_1}$ and $n_{k_2}$, whose angle is less than $\pi$. The outward normals of a convex polygon are in angular order, so for every other edge $j$ the shorter arc of the unit circle from $u / |u|$ to $n_j$ passes through $n_{k_1}$ or $n_{k_2}$. Hence $n_j \cdot u \le \max(n_{k_1} \cdot u, n_{k_2} \cdot u)$. Strict convexity gives $s_j(c) < 0$ for an edge $j$ that does not contain $c$. So $s_j(v) < \max(s_{k_1}(v), s_{k_2}(v))$. In both cases a maximizing edge contains $c$. $\square$

**The potential.** For a state $(f_A, f_B)$ let $\Phi = d(f_A, f_B)$ and $\delta = \dim f_A + \dim f_B$, with dimension 0 for a vertex and 1 for an edge. Order the pairs $(\Phi, \delta)$ lexicographically.

**Lemma 4 (each move lowers the potential).** Every move of lines L3, L4, L7, L11, L13 and L16 replaces the state by one with a smaller pair $(\Phi, \delta)$.

*Proof.* A general fact first: if $c$ is a point, $a$ a vertex and $a'$ a neighbor of $a$ with $(c - a) \cdot (a' - a) > 0$, then the edge $[a, a']$ has a point closer to $c$ than $a$, because $\frac{d}{dt} |c - a - t(a' - a)|^2 = -2 (c - a) \cdot (a' - a) < 0$ at $t = 0$.

- L3 and L4. The point $b$ violates a plane of $VR(a)$, so by the fact the new edge $f$ has $d(f, b) < |a - b| = \Phi$.
- L7. Here $(v - e_0) \cdot (e_1 - e_0) < 0$. The function $t \mapsto |v - e_0 - t (e_1 - e_0)|^2$ is convex and increases at $t = 0$, so $\pi_e(v) = e_0$. So $\Phi$ is unchanged and $\delta$ drops by 1. The other end is the same.
- L11. The vertex $v$ is in the slab of $e$ with $s_e(v) \le 0$, and the move is taken only when $s_k(v) > 0$, so $v \notin B$. By Lemma 3, the new feature $k$ has $d(v, k) = d(v, B) \le d(v, e) = \Phi$. Equality would give $\pi_B(v) \in e$, and then $\pi_B(v)$ is the foot of the perpendicular from $v$ to the line of $e$, so $v - \pi_B(v) = s_e(v)\, n_e$ with $s_e(v) < 0$ (it is not 0, because $v \notin B$). This vector would have a positive dot product with $y - \pi_B(v)$ for points $y$ inside $B$, which contradicts the projection property. So $\Phi$ drops.
- L13. With $q = \pi_e(v)$ and a violated plane toward $v'$, the fact gives a point of the edge $[v, v']$ closer to $q$ than $v$. So the new distance is at most that, which is less than $|v - q| = \Phi$.
- L16. The two edges do not meet. The squared distance $|p(s) - q(t)|^2$ over $[0, 1]^2$ is a convex quadratic. If the lines are not parallel, its only minimum in the plane is at the crossing point of the lines, which is outside the square because the segments do not meet, so the minimum over the square is on the boundary of the square. If the lines are parallel, the function is constant along a direction in the parameter plane, and a minimizer can be moved along it to the boundary. A point on the boundary of the square has an end point on one of the two segments. So the smallest of the four end point distances equals $\Phi$, and $\delta$ drops from 2 to 1. $\square$

**Theorem.** The walk ends after at most $4|A||B|$ moves. If it returns at L5 or L14 with a positive distance, the two returned points are a closest pair of $A$ and $B$, the returned features contain them, and $A \cap B = \emptyset$. It returns at L10, at L15 or with distance 0 exactly when $A \cap B \ne \emptyset$.

*Proof.* By Lemma 4, the potential strictly decreases at each move, so no state repeats. There are $2|A| \cdot 2|B|$ states, which bounds the number of moves.

At L5, $b \in VR(a)$ and $a \in VR(b)$, so by Lemma 1 $a = \pi_A(b)$ and $b = \pi_B(a)$. At L14, $v$ passed L7 and L8, so $v \in VR(e)$ with $s_e(v) > 0$, and by Lemma 1 $q = \pi_e(v)$ is the closest point of the polygon of $e$ to $v$. Also $q \in VR(v)$, so $v$ is the closest point of its polygon to $q$. In both cases Lemma 2 gives the claim, and at L14 the distance is $s_e(v) > 0$. At L5 the distance is 0 only if $a = b$, which is a common point.

At L10, Lemma 3 gives $v \in B$ (or $v \in A$ in the symmetric case), and at L15 two edges meet. So these answers are correct. Conversely, if $A \cap B \ne \emptyset$, Lemma 2 rules out a return with a positive distance, so the walk returns one of the intersecting answers. $\blacksquare$

**Remark on floating point.** The proof assumes exact arithmetic, which the implementation has for integer and rational input. In floating point the comparisons of lines L3 to L13 can disagree with each other near the boundaries of the regions, and the potential can then fail to decrease. The implementation stops with an error after $4|A||B| + 1$ moves, which cannot happen with exact input.
