---
tag: 81WJP3
kind: theorem
slug: local-delaunay-criterion
name: Local Delaunay criterion
aliases:
- local Delaunay property
- Delaunay lemma
- legal triangulation theorem
area: geometry/voronoi-and-delaunay
level: core
summary: A triangulation whose every edge is locally Delaunay is globally Delaunay.
prereqs: [delaunay-triangulation, triangulation-of-point-set, in-circle-test, edge-flip]
see_also: [lawson-flip-algorithm, delaunay-max-min-angle, empty-circle-property, paraboloid-lifting-map, delaunay-triangulation-uniqueness, constrained-delaunay-triangulation, higher-dimensional-delaunay, regular-triangulation]
sources:
  - paper: "B. Delaunay, Sur la sphère vide, Bulletin de l'Académie des Sciences de l'URSS, Classe des sciences mathématiques et naturelles 6, 1934, 793-800"
    locator: the lemma that a triangulation whose adjacent simplices have empty spheres in the local sense is a Delaunay triangulation
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 9.2 (legal edges, and a triangulation is legal if and only if it is a Delaunay triangulation)
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 2 (the Delaunay lemma, proved with the lifting map) and Chapter 4 (the version for Delaunay triangulations in higher dimensions)
  - paper: "C. L. Lawson, Software for C1 surface interpolation, in J. R. Rice (editor), Mathematical Software III, Academic Press, 1977"
    locator: the local optimization of the diagonals of convex quadrilaterals by flips
---

The local Delaunay criterion says that to check whether a triangulation of a point set is a [Delaunay triangulation](/delaunay-triangulation/), it is enough to check each interior edge against the one point across it. If for every interior edge the opposite point of the next triangle is not strictly inside the [circumcircle](/circumcircle/) of the triangle on this side, then no point at all is strictly inside any circumcircle. So a global condition on all pairs of triangles and points reduces to $O(n)$ local [in-circle tests](/in-circle-test/). The theorem holds without any general position assumption, and in every dimension. It is the reason why the [Lawson flip algorithm](/lawson-flip-algorithm/) and every flip-based insertion stop at a Delaunay triangulation.

## Statement

**Setting.** $P$ is a finite set of $n$ points $p = (x, y)$ in the plane, not all on one line, and $H$ is its convex hull. $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise. For a counterclockwise triangle $a, b, c$, $\mathrm{incircle}(a, b, c, d)$ is positive when $d$ is strictly inside the circumcircle of $a, b, c$, zero when $d$ is on it, and negative when $d$ is outside. A **triangulation** $T$ of $P$ is a finite set of triangles, each with three vertices in $P$ not on one line, such that the union of the triangles is $H$, any two triangles meet in a common edge, in a common vertex or not at all, and every point of $P$ is a vertex of some triangle. An edge of $T$ is **interior** if it is a side of two triangles; the other edges are on the boundary of $H$.

An interior edge $ab$ with triangles $abc$ and $bad$, where $\mathrm{orient}(a, b, c) > 0$, is **locally Delaunay** if $\mathrm{incircle}(a, b, c, d) \le 0$, and **strictly locally Delaunay** if $\mathrm{incircle}(a, b, c, d) < 0$. $T$ is **Delaunay** if no point of $P$ is strictly inside the circumcircle of any triangle of $T$.

**Theorem.** Let $P$ and $T$ be as above.

1. $T$ is Delaunay if and only if every interior edge of $T$ is locally Delaunay.
2. If every interior edge of $T$ is strictly locally Delaunay, then for every triangle $\Delta$ of $T$, every point of $P$ that is not a vertex of $\Delta$ is strictly outside the circumcircle of $\Delta$. Then $T$ is the only Delaunay triangulation of $P$.

No assumption of general position is made: three or more points may lie on one line, and four or more on one circle. The two conditions in the definition of a triangulation, that two triangles meet in a common face and that every point of $P$ is a vertex, are both needed, and so is the convexity of the domain $H$; see Tightness.

## In plain words

Join dots into triangles. Each inner side is shared by two triangles. Look at one side, draw the circle through the corners of one of its triangles, and check that the far corner of the other triangle is not inside it. Do this for every inner side.

If every side passes, then no dot anywhere is inside any of the circles. You never have to compare a triangle with dots that are far away.

If every side passes with room to spare, so that no far corner is on the circle, then this way of joining the dots is the only good one.

## Proof

The proof uses the [lifting map](/paraboloid-lifting-map/) $x \mapsto (x, |x|^2)$ to the paraboloid.

**Notation.** For a triangle $\Delta$ with vertices $u, v, w$ not on one line, $f_\Delta$ is the affine function on the plane with $f_\Delta(u) = |u|^2$, $f_\Delta(v) = |v|^2$ and $f_\Delta(w) = |w|^2$. Its graph is the plane through the three lifted vertices. $F_T : H \to \mathbb{R}$ is the function that equals $f_\Delta$ on each triangle $\Delta$ of $T$. It is well defined, because two triangles that meet share a vertex or an edge, and on a common edge both functions are the affine interpolation of $|x|^2$ at its two ends.

**Lemma 1 (lifting).** Let $\Delta$ have circumcenter $c$ and circumradius $\rho$. Then $|q|^2 - f_\Delta(q) = |q - c|^2 - \rho^2$ for every point $q$. So $q$ is strictly inside the circumcircle of $\Delta$ exactly when $|q|^2 < f_\Delta(q)$, on it exactly when $|q|^2 = f_\Delta(q)$, and strictly outside exactly when $|q|^2 > f_\Delta(q)$.

*Proof.* The function $g(q) = 2 c \cdot q + \rho^2 - |c|^2$ is affine, and $|q|^2 - g(q) = |q - c|^2 - \rho^2$, which is zero at the three vertices of $\Delta$. An affine function is fixed by its values at three points not on one line, so $g = f_\Delta$. $\square$

**Lemma 2 (pencil).** Let $\Delta_1 = abc$ and $\Delta_2 = bad$ be triangles with the common edge $ab$ on the line $L$, with $c$ and $d$ strictly on opposite sides of $L$. Then $f_{\Delta_2} - f_{\Delta_1}$ is affine and zero on $L$, and these are equivalent: (i) $d$ is not strictly inside the circumcircle of $\Delta_1$; (ii) $f_{\Delta_2} \ge f_{\Delta_1}$ on the closed half-plane of $L$ that holds $d$; (iii) $c$ is not strictly inside the circumcircle of $\Delta_2$. With strict signs, these are equivalent: (i') $d$ is strictly outside the circumcircle of $\Delta_1$; (ii') $f_{\Delta_2} > f_{\Delta_1}$ on the open half-plane of $L$ that holds $d$; (iii') $c$ is strictly outside the circumcircle of $\Delta_2$.

*Proof.* Both functions equal $|x|^2$ at $a$ and at $b$, so their difference is an affine function that is zero at two points of $L$, hence on $L$. So it is zero everywhere, or it has one strict sign on each open side of $L$ and the opposite sign on the other side. At $d$ the difference is $|d|^2 - f_{\Delta_1}(d)$, so by Lemma 1, (i) says that it is $\ge 0$ at $d$, which is (ii). At $c$ the difference is $f_{\Delta_2}(c) - |c|^2$, and by Lemma 1, (iii) says that it is $\le 0$ at $c$; by the sign rule, this is again (ii). The strict list has the same proof with strict signs. $\square$

By Lemma 2 the local test of an edge gives the same answer with either of its two triangles, so "locally Delaunay" is a property of the edge.

**Lemma 3 (the lifted surface is convex along generic segments).** Assume every interior edge of $T$ is locally Delaunay. Let $\Delta$ be a triangle of $T$, let $p$ be a point in the interior of $\Delta$ that lies on no line through two distinct points of $P$, and let $q \in H$. Put $g(t) = F_T(p + t(q - p))$ for $t \in [0, 1]$ and $\ell(t) = f_\Delta(p + t(q - p))$. Then $g(t) \ge \ell(t)$ for all $t \in [0, 1]$. If moreover every interior edge is strictly locally Delaunay and $q \notin \Delta$, then $g(1) > \ell(1)$.

*Proof.* Write $x(t) = p + t(q - p)$. The segment from $p$ to $q$ lies in $H$, because $H$ is convex. It passes through no point of $P$ other than possibly $q$, and it does not run along any edge, because each of these would put $p$ on a line through two points of $P$. Let $0 < t_1 < \cdots < t_k$ be the values of $t$ in $(0, 1)$ at which $x(t)$ crosses an edge of $T$; there are finitely many, since the segment meets each edge line at most once. Each crossing is at an inner point of an edge, and the edge is interior: if it were a boundary edge of $H$, the segment would leave $H$ on one side of it. Between two crossings, $x(t)$ stays in the interior of one triangle, so $g$ is affine there, and $g$ is continuous on $[0, 1]$.

At $t_j$ the segment passes from a triangle $\Delta_1$ to a triangle $\Delta_2$ through their common edge $e$. Just after $t_j$, the point $x(t)$ is in $\Delta_2$, on the open side of the line of $e$ that holds the third vertex of $\Delta_2$. The slope of $g$ jumps at $t_j$ by the derivative along the segment of $f_{\Delta_2} - f_{\Delta_1}$. That function is affine, zero on the line of $e$, and $\ge 0$ on the side of $\Delta_2$ by Lemma 2, because $e$ is locally Delaunay. So the slope does not decrease at $t_j$. If $e$ is strictly locally Delaunay, the function is $> 0$ on the open side of $\Delta_2$ by the strict form of Lemma 2, and as $x(t)$ moves into that side the slope strictly increases.

A continuous, piecewise affine function whose slope never decreases is convex. So $g$ is convex on $[0, 1]$. It equals the affine function $\ell$ on $[0, t_1]$ (or on all of $[0, 1]$ if $k = 0$), and a convex function lies above the line of any of its affine pieces, so $g \ge \ell$ on $[0, 1]$.

For the strict part, let $q \notin \Delta$. Then the segment leaves $\Delta$, so $k \ge 1$. Let $s_0$ be the slope of $g$ on $[0, t_1]$ and $s_1 > s_0$ its slope on $[t_1, t_2]$ (or on $[t_1, 1]$). By convexity, $g(1) \ge g(t_1) + s_1 (1 - t_1) > g(t_1) + s_0 (1 - t_1) = \ell(t_1) + s_0 (1 - t_1) = \ell(1)$. $\square$

**Lemma 4 (no hidden points).** A triangle $\Delta$ of $T$ holds no point of $P$ other than its three vertices.

*Proof.* Let $v \in P$ lie in $\Delta$. By the definition, $v$ is a vertex of some triangle $t$ of $T$. If $t = \Delta$ we are done. Otherwise $t \cap \Delta$ holds $v$, so it is a common vertex or a common edge of $t$ and $\Delta$. A corner of $t$ that lies on a vertex or an edge of $t$ is that vertex or an end of that edge. So $v$ is a vertex of $\Delta$ or an end of an edge of $\Delta$, that is, a vertex of $\Delta$. $\square$

**Proof of part 1.** If $T$ is Delaunay, then for an interior edge $ab$ with triangles $abc$ and $bad$, the point $d \in P$ is not strictly inside the circumcircle of $abc$, so the edge is locally Delaunay. Conversely, assume every interior edge is locally Delaunay. Let $\Delta$ be a triangle of $T$ and $q \in P$. There are finitely many lines through two points of $P$, and none of them holds the interior of $\Delta$, so a point $p$ as in Lemma 3 exists. By Lemma 3 at $t = 1$, $F_T(q) \ge f_\Delta(q)$. Since $q$ is a vertex of $T$, $F_T(q) = |q|^2$. So $|q|^2 \ge f_\Delta(q)$, and by Lemma 1, $q$ is not strictly inside the circumcircle of $\Delta$. $\square$

**Proof of part 2.** Assume every interior edge is strictly locally Delaunay, let $\Delta$ be a triangle of $T$, and let $q \in P$ not be a vertex of $\Delta$. By Lemma 4, $q \notin \Delta$. Choose $p$ as before. By the strict part of Lemma 3, $|q|^2 = F_T(q) > f_\Delta(q)$, so by Lemma 1, $q$ is strictly outside the circumcircle of $\Delta$.

By part 1, $T$ is Delaunay. Let $T'$ be any Delaunay triangulation of $P$ and $t'$ a triangle of $T'$. The interior of $t'$ is an open subset of $H$, and the triangles of $T$ cover $H$, so the interior of $t'$ meets the interior of some triangle $\Delta$ of $T$; let $U$ be the intersection of the two interiors, a nonempty open set. The vertices $z$ of $\Delta$ are points of $P$, not strictly inside the circumcircle of $t'$, so $f_\Delta(z) = |z|^2 \ge f_{t'}(z)$ by Lemma 1. Two affine functions that compare in this way at the three vertices compare in the same way on the whole triangle, so $f_\Delta \ge f_{t'}$ on $\Delta$. In the same way, the vertices $z$ of $t'$ are points of $P$, each a vertex of $\Delta$ or strictly outside its circumcircle, so $f_{t'}(z) = |z|^2 \ge f_\Delta(z)$, with equality only when $z$ is a vertex of $\Delta$. So $f_{t'} \ge f_\Delta$ on $t'$. On $U$ both inequalities hold, so the affine function $f_\Delta - f_{t'}$ is zero on a nonempty open set, hence everywhere. Then $|z|^2 = f_\Delta(z)$ at each vertex $z$ of $t'$, so each vertex of $t'$ is a vertex of $\Delta$, and $t' = \Delta$. So every triangle of $T'$ is a triangle of $T$. The triangles of $T'$ cover $H$ and those of $T$ have disjoint interiors, so $T' = T$. $\blacksquare$

## Consequences

- **Flip algorithms stop at a Delaunay triangulation.** The [Lawson flip algorithm](/lawson-flip-algorithm/) flips edges until every interior edge is locally Delaunay; by part 1 the result is Delaunay. The incremental algorithms that insert a point and then flip the edges around it, as in the method of Guibas, Knuth and Sharir, use the same fact, and only need to test the edges that the insertion touched.
- **Existence of Delaunay triangulations.** Every finite point set not on one line has a triangulation, and Lawson's flips stop after finitely many steps, so part 1 shows that a Delaunay triangulation exists. The [max-min angle theorem](/delaunay-max-min-angle/) uses part 1 in this way.
- **A linear-time check.** A triangulation with $m$ interior edges is checked to be Delaunay with $m$ in-circle tests, that is in $O(n)$ time, instead of testing every triangle against every point in $O(n^2)$ time. With integer coordinates the test is an exact determinant.
- **Uniqueness test.** If every interior edge has $\mathrm{incircle} < 0$, part 2 shows that the triangulation is the unique Delaunay triangulation. If some edge has $\mathrm{incircle} = 0$, its four points are on one empty circle and flipping that edge gives another Delaunay triangulation; see [Delaunay triangulation uniqueness](/delaunay-triangulation-uniqueness/).
- **Higher dimensions.** The same statement holds for a triangulation of a finite point set in $\mathbb{R}^d$ by simplices: if every interior facet is locally Delaunay, that is, the vertex of one neighbour is not strictly inside the circumsphere of the other, then no point is strictly inside any circumsphere. The proof is the same, with $f_\Delta$ the affine function through the $d + 1$ lifted vertices, and with $p$ chosen off the finitely many hyperplanes through $q$ and $d - 1$ points of $P$, so that the segment meets facets only at their relative interiors. This is the base of [higher-dimensional Delaunay](/higher-dimensional-delaunay/) algorithms. What fails in higher dimensions is not the criterion but the flip algorithm, because a non-locally-Delaunay facet need not be flippable.
- **Weighted form.** With $f_\Delta$ through the points $(v, |v|^2 - w_v)$ for weights $w_v$, the same proof shows that a triangulation whose interior edges are locally regular is a [regular triangulation](/regular-triangulation/), provided every weighted point is a vertex.

## Tightness

- **Every point must be a vertex.** Let $P = \{(0,0), (4,0), (0,4), (1,1)\}$ and let $T$ be the single triangle $(0,0), (4,0), (0,4)$. $T$ has no interior edges, so the local condition holds, but $(1,1)$ is strictly inside its circumcircle, with center $(2, 2)$ and squared radius $8$, since $(1,1)$ has squared distance $2$ from the center. Here $T$ is not a triangulation of $P$, since $(1,1)$ is not a vertex; the condition is used in the last step of the proof of part 1.
- **The domain must be convex.** For a triangulation of a non-convex polygon the local condition does not give the global one. Take the simple polygon with counterclockwise vertices $(0,0)$, $(4,0)$, $(2,1)$, $(-2,1)$, $(-2,-3)$, $(2,-3)$, $(2,-2)$, $(-1,-2)$, a flat triangle with a hook that bends around below it. Its triangulation with the triangles $(0,0), (4,0), (2,1)$; $(0,0), (2,1), (-2,1)$; $(-1,-2), (0,0), (-2,1)$; $(-1,-2), (-2,1), (-2,-3)$; $(-1,-2), (-2,-3), (2,-3)$ and $(2,-3), (2,-2), (-1,-2)$ has every interior edge locally Delaunay. But the circumcircle of $(0,0), (4,0), (2,1)$ has center $(2, -3/2)$ and squared radius $25/4$, and the vertices $(2,-2)$ and $(2,-3)$ are strictly inside it, at squared distances $1/4$ and $9/4$. The proof fails because the segment from the flat triangle to $(2,-2)$ leaves the polygon. This is why the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) uses a weaker emptiness, with only the points that are visible from the triangle.
- **Every interior edge must be checked.** One edge that fails the test is enough to make the triangulation not Delaunay, as the definition of locally Delaunay at that edge already shows.
- **Strictness is needed for uniqueness.** For the square $(0,0), (2,0), (2,2), (0,2)$, both diagonals give a triangulation whose only interior edge has $\mathrm{incircle} = 0$. Both triangulations are Delaunay, so part 2 cannot be extended to edges that are only locally Delaunay. In a grid of $k \times k$ points, every triangulation that splits each unit square by one of its diagonals is Delaunay, and every interior edge in it has $\mathrm{incircle} \le 0$, with equality on the diagonals.
- **Proper triangulations.** If two triangles may meet in a part of an edge, so that a point of $P$ lies inside an edge of a neighbour, the local test along that edge is not defined, and $F_T$ need not be well defined. The common-face condition of the definition rules this out.

## History

B. Delaunay proved in 1934 that a triangulation whose neighbouring simplices satisfy the empty sphere condition locally is a Delaunay triangulation, and used it to define what is now called the Delaunay triangulation; the lemma is often called the Delaunay lemma. C. L. Lawson used local tests and flips of diagonals for surface interpolation in 1977, and R. Sibson linked the local angle rule to the Delaunay property in 1978. Textbooks state the planar case as "a triangulation is legal if and only if it is Delaunay", as in de Berg, Cheong, van Kreveld and Overmars. The proof with the lifting map and the convexity of the lifted surface along a line is the form in the book of Cheng, Dey and Shewchuk.

## References
