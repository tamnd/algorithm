---
title: The planar advancing front with exact tests and a fallback always finishes with a conforming triangulation of the polygon
proves: [correctness, termination]
status: full
---

**Claim.** Let $D$ be a closed region bounded by a simple polygon with rational corners in counterclockwise order, and let $h > 0$ be rational. Then ADVANCING-FRONT$(D, h)$ stops, and its output is a set of counterclockwise triangles that have pairwise disjoint interiors, whose union is $D$, and in which no vertex lies on a triangle other than at its corners. All tests are exact. Nothing is claimed about the angles.

**What the proof does not give.** The proof gives validity, not quality. The smallest angle depends on the order of the front, the ideal point and the meeting of fronts, and nothing in the method bounds it. In the tests, a random convex polygon with all corners above $89°$ gets a triangle with angles of about $4.4°$, $5.4°$ and $170°$ where two parts of the front close up. In three dimensions Step 3 fails: a polyhedral region such as the [Schönhardt polyhedron](/schonhardt-polyhedron/) has no tetrahedralization without new vertices, so the 3D method can stall.

**Notation.** At any moment, $F$ is the front, a set of directed segments, $V$ the set of vertices made so far, and $\mathcal{T}$ the set of triangles. Let $R$ be the closure of $D \setminus \bigcup \mathcal{T}$, the unmeshed region. A front vertex is an endpoint of a front edge.

**Invariant.** Before each test of L3:

- (I1) two front edges meet at most in a common endpoint;
- (I2) $R$ is a finite union of closed polygonal regions whose boundary is the union of the front edges, and for each front edge $ab$ the points just to the left of $ab$ are in $R$ and the points just to the right are not;
- (I3) the triangles of $\mathcal{T}$ are counterclockwise, have disjoint interiors, lie in $D$, and their interiors do not meet $R$;
- (I4) every vertex of $V$ that is not a front vertex lies outside $R$, and no vertex of $V$ lies on a triangle of $\mathcal{T}$ other than at its corners.

At the start, $F$ is the boundary of $D$, cut into pieces at points on the sides, $\mathcal{T} = \emptyset$ and $R = D$. (I1) holds because the polygon is simple, (I2) because it is counterclockwise, and (I3) and (I4) hold trivially.

**Step 1 (VALID means that the triangle lies in $R$).** Let $ab \in F$ and let $c$ pass VALID: ORIENT2D$(a, b, c) > 0$ (L12), no front vertex other than $a, b, c$ lies in the closed triangle $T = abc$ (L14), and no front edge other than $bc$ or $ca$ themselves shares with $bc$ or $ca$ a point that is not a common endpoint (L15). We show that no front edge $e$ meets the interior of $T$.

Suppose it does, at a point $q$. Follow $e$ from $q$ in both directions until it leaves the closed triangle or ends. An end of $e$ inside the closed triangle is a front vertex, so by L14 it is $a$, $b$ or $c$, which lie on the boundary of $T$. So in both directions $e$ reaches a point of the boundary of $T$, say $q_1$ and $q_2$, with $q$ strictly between them. They are distinct. They are not both corners of $T$, because the segment between two corners is a side of $T$ and does not pass through its interior. So one of them, say $q_1$, lies inside a side of $T$, not at a corner.

- If $q_1$ is inside the side $ab$, then $e$ and $ab$ share a point that is not an endpoint of $ab$, against (I1).
- If $q_1$ is inside the side $bc$ or $ca$, then $e$ shares with that side a point that is not an endpoint of the side, which L15 rejects. The exception of L15 does not apply, because $e$ passes through the interior of $T$ and so is not the side itself.

Both cases are impossible, so no front edge meets the interior of $T$.

The interior of $T$ is connected and does not meet the boundary of $R$, which by (I2) is the union of the front edges. Points of $T$ just to the left of $ab$ are in $R$ by (I2). So the interior of $T$ lies in the interior of $R$, and $T \subseteq R \subseteq D$.

**Step 2 (the update keeps the invariant).** L10 removes $ab$, and for each of the new sides $bc$ and $ca$ either removes the front edge with the same direction, whose left side was the interior of $T$, or adds the reversed side, whose left side is the rest of $R$. The new front is therefore the boundary of $R' = \overline{R \setminus T}$ with $R'$ on the left, which is (I2). By L15, the added edges $cb$ and $ac$ meet old front edges at most in common endpoints, and they meet each other only at $c$, which is (I1). The new triangle is counterclockwise, lies in $R$ with its interior in the interior of $R$, so its interior misses the old triangles and $R'$, which is (I3). For (I4): a vertex that stops being a front vertex has all of its neighbourhood in the union of triangles, so it is not in $R'$. A vertex of $V$ on $T$ other than $a, b, c$ would be a front vertex by (I4), and L14 excludes it; a vertex of $V$ inside $bc$ or $ca$ is excluded the same way. A new point $c$ is in the interior of $R$, so it lies on no old triangle.

**Step 3 (a valid choice always exists).** Let $ab \in F$. The front edges form a planar straight line graph by (I1). Every such graph has a triangulation of the convex hull of its vertices that contains all its edges, for example its [constrained Delaunay triangulation](/constrained-delaunay-triangulation/), and every triangle of it contains no vertex of the graph except its corners. Let $abc$ be the triangle of this triangulation on the left of $ab$. It exists, because by (I2) the points just left of $ab$ are in $R \subseteq D$, which lies in the convex hull. Its corner $c$ is a front vertex strictly left of $ab$. No front vertex other than $a, b, c$ lies in it, and its sides do not cross front edges, because the front edges are edges of the triangulation. So VALID$(a, b, c)$ holds, and L7 puts every front vertex strictly left of $ab$ into the candidate list, so L8 finds a valid candidate.

**Step 4 (termination).** A new point $p$ is accepted only if it is at distance at least $h_{\min}$ from every vertex of $V$ (L13), and it lies in $D$ by Step 1. So the new points are pairwise at distance at least $h_{\min}$, and the open disks of radius $h_{\min}/2$ around them are disjoint and lie in the set of points within $h_{\min}/2$ of $D$. That set has finite area $A$, so at most $4A / (\pi h_{\min}^2)$ new points are ever made, and $|V| \le n_b + 4A / (\pi h_{\min}^2)$, where $n_b$ is the number of boundary points.

Each iteration adds one triangle. By (I3) and (I4) the triangles have disjoint interiors, corners in $V$, and no vertex of $V$ on them except their corners. Their sides form a planar straight line graph on $V$, which extends to a triangulation of $V$, and each of our triangles is then a face of it, since it contains no other vertex and its sides are edges. A triangulation of $N \ge 3$ points, not all on a line, has at most $2N - 5$ triangles. So the number of iterations is at most $2|V| - 5$, which is bounded, and the loop stops.

**Step 5 (the output).** The loop stops only when $F = \emptyset$, because Step 3 shows that each iteration with $F \ne \emptyset$ adds a triangle. Then by (I2) $R$ has no boundary, and as a bounded closed polygonal region it has no interior, so the triangles cover $D$ up to a set of zero area, and since they are closed and $D$ is the closure of its interior, they cover $D$. With (I3) and (I4) this is the claim. Every test in L12 to L15 uses ORIENT2D, comparisons of squared distances, and set membership on Fraction coordinates, so every decision is exact. Floats are used only in L5 and L6, to propose candidates, and a bad proposal fails VALID. $\blacksquare$
