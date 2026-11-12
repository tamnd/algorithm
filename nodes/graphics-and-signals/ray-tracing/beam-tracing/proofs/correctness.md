---
title: Every ray of a beam follows the beam tree to the same hits as a ray traced alone
proves: [correctness, termination]
status: full
---

**Setting.** This is the planar version of the implementation. The scene is a finite set of pairwise disjoint closed segments. A beam has an apex $A$, edge directions $d_l, d_r$ with $\operatorname{cross}(d_l, d_r) > 0$ (a wedge narrower than a half turn), and possibly a window, a segment $W$ on a line $\ell_W$ with $A \notin \ell_W$. The region of the beam is the set $R$ of points $A + \lambda v(s)$ with $\lambda > 0$, $s \in [0, 1]$, $v(s) = d_l + s(d_r - d_l)$, and, if there is a window, on the far side of $\ell_W$ from $A$ or on it. For a point $x \ne A$ in the wedge, $s(x)$ is its direction parameter and $\lambda(x)$ its distance parameter, so $x = A + \lambda(x) v(s(x))$. We use exact arithmetic.

The ray of direction $s$ in the beam is the set of points of $R$ in direction $s$. Its first hit is the point with the smallest $\lambda$ on a segment of the scene other than the window's segment.

**Lemma 1 (pieces are graphs).** Each clipped piece $c$ of line L2 is a segment in $R$. If it is not contained in a line through $A$, the map $x \mapsto s(x)$ is a bijection from $c$ onto a closed interval $I_c$, and $g_c(s) = \lambda$ of the point of $c$ in direction $s$ is continuous and positive on $I_c$.

*Proof.* $R$ is convex, as an intersection of half-planes (the two edges of the wedge, and the window side) with the open half-plane $\lambda > 0$, which the wedge condition gives. So the clip of a segment is a segment. A segment not on a line through $A$ meets each ray from $A$ at most once, and $s$ varies continuously and monotonically along it. $\square$

Pieces on a line through $A$ have an interval of length 0. The implementation drops them, which changes the answer only for the single direction of that line.

**Lemma 2 (constant order on overlaps).** If the open interiors of $I_a$ and $I_b$ meet, then $g_a - g_b$ has a constant, nonzero sign on $I_a \cap I_b$.

*Proof.* $g_a(s) = g_b(s)$ would mean that both pieces contain the point $A + g_a(s) v(s)$, but the segments are disjoint. $g_a - g_b$ is continuous on the interval $I_a \cap I_b$ and never zero, so its sign is constant. $\square$

Write $a \prec b$ if the interiors of $I_a, I_b$ meet and $g_a < g_b$ there: $a$ hides $b$. The implementation tests the sign at the midpoint of the overlap, which by Lemma 2 decides it.

**Lemma 3 (an order exists).** The relation $\prec$ has no cycle, so the topological sort of line L4 succeeds.

*Proof.* Suppose there is a cycle $a_1 \prec a_2 \prec \dots \prec a_k \prec a_1$, and take one of minimal length $k$. Lemma 2 rules out $k \le 2$. Let $a_i$ be the member whose interval has the smallest right end $r$, and write $p = a_{i-1}$, $q = a_{i+1}$ (indices modulo $k$). The interiors of $I_p$ and $I_{a_i}$ meet, and the right end of $I_p$ is at least $r$, so $I_p$ contains $(r - \delta, r)$ for some $\delta > 0$; the same holds for $I_q$. For $s$ in that interval, $g_p(s) < g_{a_i}(s) < g_q(s)$, so $p \prec q$ by Lemma 2. Removing $a_i$ gives a cycle of length $k - 1$, against minimality. $\square$

**Lemma 4 (one beam).** Let $s \in (0, 1)$ be a direction that is not an endpoint of any interval $I_c$. If the ray of direction $s$ has a first hit, on a segment $P$, then the beam has a fragment of $P$ whose open interval contains $s$, and the point of that fragment in direction $s$ is the first hit. If the ray has no hit in $R$, then no fragment contains $s$.

*Proof.* The ray's points on scene segments, other than the window's segment, are the points of the pieces whose interval contains $s$, at distances $g_c(s)$. Since $s$ is not an endpoint, it lies in the interior of each such interval, and by Lemma 2 the nearest one, $c^*$, satisfies $c^* \prec c$ for every other such $c$. Line L5 keeps the invariant that $remaining$ is the set of directions not covered by the pieces already processed, and gives each piece the part of $remaining$ inside its interval. Every piece containing $s$ comes after $c^*$ in the order, so when $c^*$ is processed, $s$ is still in $remaining$ and goes to $c^*$; after that it is not in $remaining$, so no later piece gets it. If no piece contains $s$, no fragment does. $\square$

**Lemma 5 (reflection).** Let the ray of direction $s$ hit the mirror $P$ at the point $h$, and let $A'$ be the mirror image of $A$ in the line of $P$. The reflected ray $\{h + \mu r : \mu > 0\}$ is the set of points of the child beam's region in the direction of $h$ from $A'$, and the order of points by $\mu$ is their order by distance from $A'$.

*Proof.* Reflection in the line of $P$ is an isometry that fixes $h$ and maps $A$ to $A'$, so it maps the incoming ray, which arrives at $h$ from $A$, to the segment from $A'$ to $h$. The law of reflection says that the outgoing direction $r$ is the mirror image of the incoming direction $d$, which makes $r$ parallel to $h - A'$ with the same sense. So $h + \mu r = A' + (1 + \mu/\kappa)(h - A')$ for $\kappa = \lVert h - A'\rVert / \lVert r\rVert$, and $\mu > 0$ corresponds exactly to the points beyond $h$, that is, beyond the window line, on the far side from $A'$. The child wedge is spanned by the directions from $A'$ to the ends of the fragment, which contains $h$, so these points are in the child region. Distance from $A'$ grows with $\mu$. $\square$

**Theorem.** TRACE-BEAM stops. For every direction $s$ of the root beam outside the finite set of fragment endpoints of the tree, the chain of segments and hit points obtained by following $s$ through the beam tree, as the function `beam_path` does, equals the chain obtained by tracing the single ray in direction $s$ with reflections up to the same depth.

*Proof.* Termination: each call processes finitely many pieces, the depth grows by one at each recursive call, and calls stop at the maximum depth. Correctness by induction on the depth. At the root, Lemma 4 gives the first hit. If it is on a mirror and the depth allows a reflection, the fragment has a child beam; by Lemma 5 the reflected ray is the ray of the child beam in the direction $s' = s(h)$ measured from $A'$, the window's segment is excluded in both, and by Lemma 4 applied to the child, the next hit agrees. The directions $s'$ that are fragment endpoints in the child correspond to finitely many directions $s$ of the root, which the hypothesis excludes. $\blacksquare$

**Remark (3D).** In space the same argument works with polygons in place of segments and polygons of directions in place of intervals, with one change: Lemma 3 fails, because polygons can overlap cyclically. A BSP tree, which splits polygons until an order exists from every point, restores it.
