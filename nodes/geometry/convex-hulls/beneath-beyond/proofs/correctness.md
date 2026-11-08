---
title: For points in general position, the beneath-beyond method returns the facets of the hull with their conflict lists maintained
proves: [correctness, termination]
status: full
---

**Claim.** Let $P \subset \mathbb{R}^3$ be a finite set in general position: no three points on a line and no four points on a plane. If $|P| \ge 4$, BENEATH-BEYOND returns the facets of $\mathrm{conv}(P)$, each once, as triangles oriented with the outward normal $(b - a) \times (c - a)$. If $|P| \le 3$, it returns the empty set.

**Facts on polytopes.** We use these standard facts about a finite set $S$ in general position with $|S| \ge 4$ (see [convex polytope](/convex-polytope/) and [facet](/facet/)). $\mathrm{conv}(S)$ is a 3-dimensional polytope whose facets are triangles with vertices in $S$.

- (F1) Three points $x, y, z \in S$ form a facet exactly when all points of $S \setminus \{x, y, z\}$ lie strictly on one side of the plane through $x, y, z$. If the facet is oriented so that these points are beneath it, then $\mathrm{conv}(S)$ is the set of points that are beneath or on every facet.
- (F2) Two points $u, v \in S$ form an edge exactly when some plane through $u$ and $v$ has all points of $S \setminus \{u, v\}$ strictly on one side. Each edge lies in exactly two facets, and the outward orientations of these two facets run through the edge in opposite directions. So each directed edge $(u, v)$ of a facet appears in exactly one facet, and $(v, u)$ appears in exactly one other facet.

**The reduction to the plane.** Fix two distinct points $u, v$. For vectors $X, Y$ write $[X, Y] = ((v - u) \times X) \cdot Y$, so that $\mathrm{orient}(u, v, x, y) = [x - u, y - u]$. The form $[\cdot, \cdot]$ is bilinear and antisymmetric, and $[X, Y] = 0$ when $X$ or $Y$ is parallel to $v - u$. So it depends only on the components of $X$ and $Y$ perpendicular to $v - u$, and on that plane it is a nonzero multiple of the planar cross product. In particular, if $[X, Y] \ne 0$, the components of $X$ and $Y$ perpendicular to $v - u$ are a basis of that plane. We write $X$ for $x - u$, $Y$ for $y - u$ and so on.

**Lemma 1 (the wedge).** Let $f = (u, v, w)$ and $g = (v, u, z)$ be two triangles with $z$ strictly beneath $f$ and $w$ strictly beneath $g$. Let $p$ be beyond $f$ and beneath $g$, and let $t = (u, v, p)$.

1. If a point $q$ is beneath or on $f$ and beneath or on $g$, then $q$ is beneath or on $t$, and it is on $t$ only if $q$ is on the line $uv$.
2. If a point $q$ is beyond $t$, then $q$ is beyond $f$ or beyond $g$.

*Proof.* Since $\mathrm{orient}(v, u, z, q) = -\mathrm{orient}(u, v, z, q)$, the hypotheses read: $[W, Z] < 0$ ($z$ beneath $f$), $[W, P] > 0$ ($p$ beyond $f$), $[Z, P] > 0$ ($p$ beneath $g$). Since $[W, Z] \ne 0$, write the perpendicular component of $Q$ as $\alpha W + \beta Z$. The point $q$ is beneath or on $f$: $[W, Q] = \beta [W, Z] \le 0$, so $\beta \ge 0$. It is beneath or on $g$: $-[Z, Q] = -\alpha [Z, W] = \alpha [W, Z] \le 0$, so $\alpha \ge 0$. Then $[P, Q] = \alpha [P, W] + \beta [P, Z] = -\alpha [W, P] - \beta [Z, P] \le 0$, with equality only for $\alpha = \beta = 0$, that is, for $q$ on the line $uv$. This proves part 1, and part 2 is its contrapositive. $\square$

**Lemma 2 (beneath and beyond).** Let $S$ be in general position with $|S| \ge 4$, let $p \notin \mathrm{conv}(S)$, and let $S \cup \{p\}$ be in general position. Then the facets of $\mathrm{conv}(S \cup \{p\})$ are exactly:

- (a) the facets of $\mathrm{conv}(S)$ that $p$ is beneath, and
- (b) the triangles $(u, v, p)$, where $(u, v)$ is a directed edge of a facet $f$ of $\mathrm{conv}(S)$ that $p$ is beyond, and the other facet $g$ at the edge $uv$ has $p$ beneath it.

The orientations given are the outward ones.

*Proof.* By general position, $p$ is on no plane through three points of $S$, so for each facet $p$ is either beyond or beneath. By (F1) applied to $S \cup \{p\}$, a triangle of points of $S \cup \{p\}$ is a facet exactly when all other points of $S \cup \{p\}$ are strictly on one side of it.

*Triangles $x, y, z$ of points of $S$.* All other points of $S \cup \{p\}$ are strictly on one side exactly when $xyz$ is a facet of $\mathrm{conv}(S)$ (by (F1) for $S$) and $p$ is on the same side as $S \setminus \{x, y, z\}$, which is the beneath side. This is case (a).

*Triangles $u, v, p$.* Suppose first that $uv$ is an edge as in (b), with $f = (u, v, w)$ and $g = (v, u, z)$. All of $S$ is beneath or on $f$ and $g$, so by Lemma 1, each $s \in S \setminus \{u, v\}$ is strictly beneath $t = (u, v, p)$, because general position excludes $s$ on the line $uv$. So $t$ is a facet with the outward orientation $(u, v, p)$.

Conversely, suppose that all points of $S \setminus \{u, v\}$ are strictly on one side of the plane through $u, v, p$. By (F2), $uv$ is an edge of $\mathrm{conv}(S)$; let $f = (u, v, w)$ and $g = (v, u, z)$ be its two facets. Then $[W, Z] < 0$, and $W$ and $Z$ are on the same side of the plane: $[P, W]$ and $[P, Z]$ are nonzero with the same sign. Write $P = \alpha W + \beta Z$ (perpendicular components). Then $[P, W] = \beta [Z, W]$ and $[P, Z] = \alpha [W, Z]$, so $\alpha$ and $\beta$ have opposite signs. Now $p$ is beyond $f$ exactly when $[W, P] = \beta [W, Z] > 0$, that is, $\beta < 0$, and $p$ is beyond $g$ exactly when $-[Z, P] = -\alpha [Z, W] = \alpha [W, Z] > 0$, that is, $\alpha < 0$. Since exactly one of $\alpha, \beta$ is negative, $p$ is beyond exactly one of $f$ and $g$. Exchanging the names of $u$ and $v$ if needed, $p$ is beyond $f$ and beneath $g$, which is case (b).

Each facet of $\mathrm{conv}(S \cup \{p\})$ either avoids $p$ or contains it, so the list is complete. $\square$

**Invariant.** Before each iteration of line L5, let $S$ be the set of points processed so far (the four points of line L2 and the points already taken by line L5), and $R = P \setminus S$ the waiting points. Then:

- (J1) $T$ is the set of facets of $\mathrm{conv}(S)$, each with its outward orientation;
- (J2) the edge map sends each directed edge of each facet of $T$ to that facet, and has no other entries;
- (J3) for each $t \in T$, the list $C(t)$ is the set of points of $R$ beyond $t$, and for each $q \in R$ the set of $q$ is $\{t \in T : q \in C(t)\}$.

*Initialization.* By general position the first four points of the order are not on one plane, so line L2 succeeds when $|P| \ge 4$; for $|P| \le 3$ there are no four such points and the empty set is returned. Each triangle of the tetrahedron has the fourth vertex strictly on one side, so by (F1) the four triangles are the facets, and line L3 orients each so that the fourth vertex is beneath. This gives (J1). Each directed edge of the tetrahedron is in one facet, which gives (J2). Line L4 tests each pair, which gives (J3).

*Maintenance.* Let $p$ be the point of line L5, and $V$ the set read by line L6. By (J3), $V$ is the set of facets that $p$ is beyond.

- If $V$ is empty, $p$ is beneath or on every facet, so $p \in \mathrm{conv}(S)$ by (F1), and $\mathrm{conv}(S \cup \{p\}) = \mathrm{conv}(S)$. In general position $p$ is beneath every facet, so no facet of $S \cup \{p\}$ contains $p$ and (J1) and (J2) still hold. The point $p$ was in no conflict list, so (J3) holds for the new $R$.
- If $V$ is not empty, $p \notin \mathrm{conv}(S)$. Line L8 lists the directed edges $(u, v)$ of facets $f \in V$ such that the facet $g$ of $(v, u)$, found by (J2), is not in $V$; then $p$ is beneath $g$. These are exactly the edges of case (b) of Lemma 2, each listed once, from the side of $f$. Lines L9 and L10 add the triangles of case (b), and line L12 removes the facets of $V$, which leaves case (a). So (J1) holds for $S \cup \{p\}$.

For (J2): line L10 maps the three directed edges of each new facet to it. The directed edge $(u, v)$ was mapped to $f$, and is now mapped to $t$. Line L12 removes an entry of a deleted facet only if the entry still points to that facet. By (F2) for $S \cup \{p\}$, each directed edge of the new facet set is in exactly one facet. An old directed edge whose facet survives keeps its entry. An old directed edge whose facet is deleted either is a horizon edge, now mapped to its new facet, or has both facets in $V$, and then neither direction is an edge of a new facet: such an edge has $p$ beyond both facets, so it is not an edge of the new hull by Lemma 2. Its entry is removed. So (J2) holds.

For (J3): a surviving facet has $p$ beneath it, so $p$ was not in its list, and the list is unchanged. For a new facet $t = (u, v, p)$ with neighbours $f$ and $g$, Lemma 1 part 2 shows that each waiting point beyond $t$ is beyond $f$ or $g$, so it is in $C(f) \cup C(g)$ by (J3). Line L11 tests all of these points, so $C(t)$ is correct. Line L12 removes the deleted facets from the sets of their waiting points, and line L6 removed the set of $p$. So (J3) holds.

*Termination and output.* The loop of line L5 runs once for each point. At the end $S = P$, and by (J1) line L13 returns the facets of $\mathrm{conv}(P)$, each once, with the outward orientation. $\blacksquare$
