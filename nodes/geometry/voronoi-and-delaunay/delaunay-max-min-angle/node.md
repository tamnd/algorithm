---
tag: TZTHSY
kind: theorem
slug: delaunay-max-min-angle
name: Delaunay max-min angle property
aliases:
- max-min angle property
- angle optimality of the Delaunay triangulation
- equiangularity of the Delaunay triangulation
area: geometry/voronoi-and-delaunay
level: core
summary: The Delaunay triangulation maximizes the minimum angle over all triangulations of the same points.
prereqs: [delaunay-triangulation, local-delaunay-criterion, triangulation-of-point-set, edge-flip]
see_also: [max-min-angle-triangulation, lawson-flip-algorithm, circumcircle, delaunay-triangulation-uniqueness, general-position-delaunay, constrained-delaunay-triangulation, mesh-generation, flip-graph]
sources:
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 9.1 (angle vectors, illegal edges and the Thales lemma) and Section 9.2 (any angle-optimal triangulation is Delaunay, and any Delaunay triangulation maximizes the minimum angle)
  - paper: doi:10.1093/comjnl/21.3.243
    title: R. Sibson, Locally equiangular triangulations, The Computer Journal 21(3), 1978, 243-245
    locator: the whole paper (a triangulation that is locally equiangular at every edge is the Delaunay triangulation)
  - paper: "C. L. Lawson, Software for C1 surface interpolation, in J. R. Rice (editor), Mathematical Software III, Academic Press, 1977"
    locator: the max-min angle rule for the diagonal of a convex quadrilateral and the flip procedure
  - paper: doi:10.1137/0913058
    title: H. Edelsbrunner, T. S. Tan and R. Waupotitsch, An O(n^2 log n) time algorithm for the minmax angle triangulation, SIAM Journal on Scientific and Statistical Computing 13(4), 1992, 994-1008
    locator: the minmax angle problem, for which the Delaunay triangulation is not optimal
---

Among all triangulations of a finite set of points in the plane, a [Delaunay triangulation](/delaunay-triangulation/) has the largest smallest angle. More is true: a triangulation that is best for the whole sorted list of its angles is always Delaunay, and when no four points lie on a circle it is the Delaunay triangulation. This is the main reason why Delaunay triangulations are used for interpolation and for [mesh generation](/mesh-generation/), where thin triangles cause large errors. The proof uses only the inscribed angle theorem and [edge flips](/edge-flip/).

## Statement

**Setting.** $P$ is a finite set of $n$ points in the plane, not all on one line. A [triangulation](/triangulation-of-point-set/) $T$ of $P$ is a set of triangles with vertices in $P$ whose interiors are disjoint, whose union is the convex hull of $P$, and which has every point of $P$ as a vertex. All triangulations of $P$ have the same number $m$ of triangles. The **angle vector** $A(T)$ is the list of the $3m$ angles of the triangles of $T$, sorted from small to large. We write $A(T) > A(T')$ when $A(T)$ is larger in the lexicographic order, and $T$ is **angle-optimal** when $A(T) \ge A(T')$ for every triangulation $T'$ of $P$. A triangulation is **Delaunay** when no point of $P$ is strictly inside the [circumcircle](/circumcircle/) of any of its triangles.

**Theorem.** Let $P$ be a finite set of points in the plane, not all on one line.

1. Every angle-optimal triangulation of $P$ is a Delaunay triangulation. In particular, $P$ has a Delaunay triangulation.
2. Every Delaunay triangulation of $P$ has the same smallest angle, and this angle is the largest smallest angle of all triangulations of $P$: for every Delaunay triangulation $D$ and every triangulation $T$, $\min A(D) \ge \min A(T)$.
3. If no four points of $P$ lie on one circle, the Delaunay triangulation is unique and it is the unique angle-optimal triangulation.

The converse of part 2 is false: a triangulation that is not Delaunay can have the same smallest angle as $D$. Part 1 needs the full angle vector; maximizing only the smallest angle does not force the Delaunay property.

## In plain words

There are many ways to join a set of dots into triangles. Some ways give thin triangles with very sharp corners. The Delaunay way never does worse than any other way on the sharpest corner: its sharpest corner is as blunt as possible.

The reason is a fact about circles. Look at two triangles that share a side and form a four-sided shape. If one corner is inside the circle through the other three, swapping the shared side for the other diagonal makes every new corner wider than some old corner. So swaps of this kind only help, and when no swap is possible, the triangles are Delaunay.

When dots sit on a common circle, several Delaunay ways exist, and they all have the same sharpest corner.

## Proof

**Notation.** For points $u, v, w$ with $v \ne u \ne w$, $\angle uvw$ is the angle at $v$ in $(0, \pi)$ between the rays to $u$ and to $w$. $\mathrm{orient}(p, q, r) > 0$ means that $p, q, r$ turn counterclockwise.

**Lemma 1 (inscribed angles).** Let $C$ be the circle through $a$, $b$, $c$, and let $d$ be a point strictly on the same side of the line $ab$ as $c$. If $d$ is strictly inside $C$, then $\angle adb > \angle acb$. If $d$ is on $C$, the two angles are equal.

*Proof.* The second statement is the inscribed angle theorem: points of the same arc see the chord $ab$ under the same angle. For the first, let $d'$ be the point where the ray from $a$ through $d$ leaves the closed disk. Then $d'$ is on $C$, strictly beyond $d$, and on the same side of $ab$ as $d$, so $\angle ad'b = \angle acb$. In the triangle $b d d'$, the angle $\angle adb$ is the exterior angle at $d$, since $a$, $d$, $d'$ lie on a line in this order. So $\angle adb = \angle d d' b + \angle d b d' > \angle d d' b = \angle a d' b = \angle acb$. $\square$

**Lemma 2 (a flip raises the angle vector).** Let $abc$ and $bad$ be triangles of a triangulation $T$ with $\mathrm{orient}(a, b, c) > 0$, and let $d$ be strictly inside the circle through $a$, $b$, $c$. Then the quadrilateral $adbc$ is strictly convex, the flip of $ab$ gives a triangulation $T'$ with the triangles $adc$ and $dbc$ in place of $abc$ and $bad$, and $A(T') > A(T)$.

*Proof.* The points $c$ and $d$ are strictly on opposite sides of the line $ab$, so $cd$ meets that line at a point $q$ strictly between $c$ and $d$. The point $q$ is a convex combination of $c$, on the circle, and $d$, strictly inside, with a positive weight on $d$, so $q$ is strictly inside the circle. The open disk meets the line $ab$ only in the open segment $ab$, so $q$ is strictly between $a$ and $b$. The two diagonals cross at an inner point of both, so the quadrilateral is strictly convex and the flip gives two triangles that cover it. Also $c$ is strictly inside the circle through $b$, $a$, $d$, since $\mathrm{incircle}(a, b, c, d) = \mathrm{incircle}(b, a, d, c)$ by two row swaps of the determinant. The six old angles are $\angle cab$, $\angle bad$, $\angle abc$, $\angle dba$, $\angle acb$ and $\angle adb$. Each of the six new angles is strictly larger than one old angle.

- At $a$: $\angle cad = \angle cab + \angle bad > \angle cab$, because $b$ is strictly inside the angle $cad$ of the convex quadrilateral. In the same way, at $b$: $\angle cbd > \angle abc$.
- At $c$, the angle $\angle acd$ of the triangle $adc$ sees the chord $ad$. The points $c$ and $b$ are on the same side of the line $ad$, a side of the convex quadrilateral, and $c$ is strictly inside the circle through $a$, $b$, $d$. By Lemma 1, $\angle acd > \angle abd$. In the same way, $\angle dcb > \angle dab$ for the chord $db$.
- At $d$: $d$ and $b$ are on the same side of the line $ac$ and $d$ is strictly inside the circle through $a, b, c$, so $\angle adc > \angle abc$. For the chord $cb$, $\angle cdb > \angle cab$.

So every new angle is strictly larger than $\mu$, the smallest of the six old angles. All other angles of $T$ and $T'$ are the same. Let $j'$ be the number of these common angles that are at most $\mu$. The angles of $T'$ that are at most $\mu$ are exactly these $j'$ angles, while $T$ has them and at least one more angle equal to $\mu$. Since $\mu$ is at least each of the $j'$ common angles, the first $j'$ entries of $A(T)$ and $A(T')$ are the same, entry $j' + 1$ of $A(T)$ is $\mu$, and entry $j' + 1$ of $A(T')$ is larger than $\mu$. So $A(T') > A(T)$. $\square$

**Proof of part 1.** $P$ has finitely many triangulations, and at least one, so an angle-optimal triangulation $T^*$ exists. Assume an interior edge $ab$ of $T^*$, with triangles $abc$ and $bad$, has $d$ strictly inside the circle through $a, b, c$. Lemma 2 gives a triangulation with a larger angle vector, which is false. So every edge of $T^*$ is locally Delaunay. By the [local Delaunay criterion](/local-delaunay-criterion/), a triangulation in which every edge is locally Delaunay is a Delaunay triangulation. $\square$

**Lemma 3 (Delaunay circles).** Call a circle $C$ a *Delaunay circle* of $P$ if no point of $P$ is strictly inside $C$ and at least three points of $P$ are on $C$, and let $Q_C = P \cap C$. Let $D$ be any Delaunay triangulation of $P$. Then the circumcircles of the triangles of $D$ are exactly the Delaunay circles, and for each Delaunay circle $C$ the triangles of $D$ with circumcircle $C$ form a triangulation of the convex polygon $\mathrm{conv}(Q_C)$.

*Proof.* Use the [lifting map](/paraboloid-lifting-map/): for a circle $C$ let $f_C$ be the affine function with $|z|^2 < f_C(z)$ inside $C$, $=$ on $C$ and $>$ outside. A circumcircle of a triangle of $D$ is a Delaunay circle by the definition of $D$. Let $C$ be a Delaunay circle and let $t$ be a triangle of $D$ whose interior meets the interior of $\mathrm{conv}(Q_C)$; such a triangle exists, since the triangles cover the hull of $P$. The vertices $z$ of $t$ are in $P$, so $|z|^2 \ge f_C(z)$, and with $|z|^2 = f_t(z)$ we get $f_t \ge f_C$ at the vertices, so on all of $t$. The points $q \in Q_C$ have $|q|^2 = f_C(q)$ and are not strictly inside the circumcircle of $t$, so $f_C(q) = |q|^2 \ge f_t(q)$, and $f_C \ge f_t$ on $\mathrm{conv}(Q_C)$. So the affine function $f_t - f_C$ is zero on the intersection of the two interiors, an open set, so it is zero everywhere and $C$ is the circumcircle of $t$. This shows that every Delaunay circle is a circumcircle. It also shows that every triangle whose interior meets the interior of $\mathrm{conv}(Q_C)$ has circumcircle $C$; such a triangle has its vertices on $C$, so it lies in $\mathrm{conv}(Q_C)$. Every triangle with circumcircle $C$ also lies in $\mathrm{conv}(Q_C)$. So these triangles cover $\mathrm{conv}(Q_C)$, with disjoint interiors, and since the points of $Q_C$ are in convex position, each is a vertex of one of them. $\square$

**Lemma 4 (inscribed polygons).** Let $q_1, \ldots, q_k$, with $k \ge 3$, be points on a circle in circular order, and let $\theta_i$ be the central angle of the arc from $q_i$ to $q_{i+1}$ (indices mod $k$) that holds no other $q_j$. Every triangulation of the polygon $q_1 \ldots q_k$ has smallest angle $\frac{1}{2} \min_i \theta_i$.

*Proof.* An angle of a triangle at the vertex $q_j$ that sees the chord $q_r q_s$ equals half of the central angle of the arc from $q_r$ to $q_s$ that does not hold $q_j$, by the inscribed angle theorem. That arc is a union of arcs between neighbours, so the angle is at least $\frac12 \min_i \theta_i$. The side $q_i q_{i+1}$ with the smallest $\theta_i$ is an edge of the polygon, so it is a side of one triangle, and the angle opposite to it equals $\frac12 \theta_i$, since the opposite vertex is not on the short arc. $\square$

**Proof of part 2.** Let $D$ be a Delaunay triangulation. By Lemma 3 the triangles of $D$ fall into groups, one for each Delaunay circle $C$, and each group triangulates $\mathrm{conv}(Q_C)$. By Lemma 4 the smallest angle in the group of $C$ is a number $\mu_C$ that depends only on $Q_C$. So $\min A(D) = \min_C \mu_C$, where $C$ runs over the Delaunay circles of $P$, and this number depends only on $P$. By part 1 an angle-optimal $T^*$ is Delaunay, so $\min A(D) = \min A(T^*) \ge \min A(T)$ for every triangulation $T$, because the first entry of the angle vector is its smallest angle. $\square$

**Proof of part 3.** If no four points are on a circle, every Delaunay circle has $|Q_C| = 3$ and the group of $C$ is the single triangle $\mathrm{conv}(Q_C)$. So by Lemma 3 the triangles of every Delaunay triangulation are exactly the triangles $\mathrm{conv}(Q_C)$, and the Delaunay triangulation is unique. By part 1, every angle-optimal triangulation is this one. $\blacksquare$

## Consequences

- **Lawson's flip algorithm ends.** Each flip of an edge that is not locally Delaunay raises the angle vector (Lemma 2). There are finitely many triangulations, so the [Lawson flip algorithm](/lawson-flip-algorithm/) stops, and it stops at a Delaunay triangulation. The lifting map gives the sharper bound of $\binom{n}{2}$ flips.
- **Existence.** Part 1 gives a proof that every point set has a Delaunay triangulation that does not use the [Voronoi diagram](/voronoi-diagram/) or the lifting map.
- **The max-min angle problem is solved in $O(n \log n)$ time.** Any Delaunay construction solves the [max-min angle triangulation](/max-min-angle-triangulation/) problem; see [Delaunay triangulation construction](/delaunay-triangulation-construction/).
- **Constrained form.** For a set of segments that must be edges, the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) maximizes the smallest angle among the triangulations that hold the segments, by the same flip argument with the segments locked.
- **Example.** For $a = (0,0)$, $b = (6,0)$, $c = (3,5)$ and $d = (3,-1)$, the point $d$ is inside the circle through $a, b, c$ (center $(3, 8/5)$, squared radius $289/25$, and $d$ is at squared distance $169/25$). With the diagonal $ab$ the smallest angle is at $a$ in $abd$, with tangent $1/3$, about $18.43$ degrees. After the flip to $cd$, the smallest angle is at $c$, with tangent $3/5$, about $30.96$ degrees.

## Tightness

- **The converse of part 2 fails.** For the convex pentagon $(4,0), (4,1), (3,6), (0,5), (1,3)$, with no four points on a circle, the Delaunay triangulation has the triangles $(4,0), (4,1), (1,3)$, then $(4,1), (3,6), (1,3)$ and $(0,5), (1,3), (3,6)$. The triangulation with $(4,0), (4,1), (1,3)$, then $(4,1), (0,5), (1,3)$ and $(4,1), (3,6), (0,5)$ is not Delaunay but has the same smallest angle, the angle at $(1,3)$ in the common triangle, with tangent $1/5$, about $11.31$ degrees. Only the full angle vector of part 1 tells them apart.
- **Cocircular points.** With four or more points on an empty circle, as in a grid, all Delaunay triangulations have the same smallest angle (part 2), but their angle vectors can differ, and the angle-optimal one need not be unique. For the corners of a square, both diagonals give the same angle vector.
- **Other angle measures.** The Delaunay triangulation does not minimize the largest angle. For the points $(4,8), (3,3), (7,8), (8,7)$, the Delaunay triangulation uses the diagonal from $(4,8)$ to $(8,7)$ and has an angle of $135$ degrees at $(7,8)$; the other diagonal gives a largest angle of about $101.31$ degrees, but a smallest angle of about $12.68$ degrees against $14.04$ degrees for the Delaunay one. Edelsbrunner, Tan and Waupotitsch solve the minmax angle problem in $O(n^2 \log n)$ time by a different method.
- **Higher dimensions.** In three dimensions the Delaunay tetrahedralization does not maximize the smallest dihedral angle or the smallest solid angle; it can contain flat tetrahedra, called slivers, even when good tetrahedralizations exist.

## History

C. L. Lawson proposed in 1977 to choose the diagonal of each convex quadrilateral that gives the larger smallest angle, and to flip edges until no choice can be improved. R. Sibson showed in 1978 that a triangulation that is locally optimal in this sense at every edge is the Delaunay triangulation, which links the angle rule to Delaunay's empty sphere of 1934. The statement with angle vectors, with the cocircular case, is the form given in the textbook of de Berg, Cheong, van Kreveld and Overmars. The minmax angle algorithm of Edelsbrunner, Tan and Waupotitsch (1992) showed that other angle criteria need other methods.

## References
