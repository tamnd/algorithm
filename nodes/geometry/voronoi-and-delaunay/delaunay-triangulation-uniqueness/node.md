---
tag: A081XE
kind: theorem
slug: delaunay-triangulation-uniqueness
name: Delaunay triangulation uniqueness
aliases:
- uniqueness of the Delaunay triangulation
- strongly Delaunay edges are in every Delaunay triangulation
area: geometry/voronoi-and-delaunay
level: core
summary: Under general position the Delaunay triangulation of a point set is unique.
prereqs: [delaunay-triangulation, circumcircle, empty-circle-property]
see_also: [general-position-delaunay, local-delaunay-criterion, paraboloid-lifting-map, voronoi-delaunay-duality, bowyer-watson-algorithm]
sources:
  - paper: "B. Delaunay, Sur la sphère vide, Bulletin de l'Académie des Sciences de l'URSS, Classe des sciences mathématiques et naturelles 6, 1934, 793-800"
    locator: the empty sphere tiling and its uniqueness for points with no d + 2 on a sphere
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 9.2 (Delaunay faces and edges described by empty circles, and the unique triangulation in general position)
---

The uniqueness theorem says that a finite set $P$ of points in the plane, not all on one line, with no four points on a circle, has exactly one [Delaunay triangulation](/delaunay-triangulation/). Its triangles are the triples of points whose [circumcircle](/circumcircle/) holds no other point of $P$, inside or on it. Without the hypothesis, the theorem still says that every triangle and every edge with a "strongly empty" circle is in every Delaunay triangulation.

## Statement

**Notation.** $P$ is a finite set of points $p = (x, y)$ in the plane, $n = |P|$. A circle $C$ is **strongly empty** for a set $A \subseteq P$ of points on it if every point of $P \setminus A$ is strictly outside $C$. A triangle $abc$ with vertices in $P$ is **strongly Delaunay** if its circumcircle is strongly empty for $\{a, b, c\}$, and a segment $pq$ with $p, q \in P$ is **strongly Delaunay** if some circle through $p$ and $q$ is strongly empty for $\{p, q\}$.

**Theorem.** Let $P$ be a finite set of points in the plane, not all on one line.

1. $P$ has a Delaunay triangulation.
2. Every strongly Delaunay triangle is a triangle of every Delaunay triangulation of $P$, and every strongly Delaunay segment is an edge of every Delaunay triangulation of $P$.
3. If no four points of $P$ lie on one circle, then $P$ has exactly one Delaunay triangulation, and its triangles are exactly the strongly Delaunay triangles.

No assumption about three points on a line is made.

## In plain words

If no four dots lie on a common circle, there is only one way to join the dots into triangles with empty circles. Each triangle in it has a circle that touches its three corners and keeps every other dot strictly outside. More generally, a triangle or a side with such a strictly empty circle must appear in every answer, whatever the other dots look like. Only groups of four or more dots on one empty circle allow a choice.

## Proof

We use the [lifting map](/paraboloid-lifting-map/). For a point $q$ write $|q|^2 = x^2 + y^2$. For a circle $C$ with center $c$ and radius $\rho$, let $f_C(q) = 2\, c \cdot q + \rho^2 - |c|^2$, an affine function of $q$. Expanding $|q - c|^2$ gives

$$|q - c|^2 - \rho^2 = |q|^2 - f_C(q),$$

so $q$ is strictly inside, on, or strictly outside $C$ exactly when $|q|^2 - f_C(q)$ is negative, zero, or positive. For a triangle $t$ with vertices not on a line, write $f_t$ for $f_C$ of its circumcircle; it is the affine function equal to $|\cdot|^2$ at the three vertices. In a triangulation of $P$, the vertices are exactly the points of $P$, so a point of $P$ in a closed triangle is one of its vertices.

**Part 1.** $P$ is not on one line, so the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/) applies; its correctness proof shows that it returns a triangulation of $P$ with no point of $P$ strictly inside any circumcircle.

**Part 2, triangles.** Let $\Delta = abc$ be strongly Delaunay and let $D$ be any Delaunay triangulation. The interior of $\Delta$ is open and not empty, and the edges of $D$ are finitely many segments, so there is a point $z$ in the interior of $\Delta$ on no edge of $D$. As $\Delta \subseteq \operatorname{conv} P$, the point $z$ is in the interior of a triangle $t = uvw$ of $D$. Let $g = f_t - f_\Delta$, an affine function.

- At the vertices of $\Delta$: $g(a) = f_t(a) - |a|^2 \le 0$, because $D$ is Delaunay and so $a$ is not strictly inside the circle of $t$. The same holds at $b$ and $c$. As $z$ is a convex combination of $a, b, c$, $g(z) \le 0$.
- At the vertices of $t$: $g(u) = |u|^2 - f_\Delta(u) \ge 0$, with equality only if $u \in \{a, b, c\}$, because $\Delta$ is strongly Delaunay. The same holds at $v$ and $w$. Write $z = \lambda_u u + \lambda_v v + \lambda_w w$ with all three weights positive, as $z$ is interior to $t$. Then $g(z) = \lambda_u g(u) + \lambda_v g(v) + \lambda_w g(w) \ge 0$.

So $g(z) = 0$, and since all weights are positive, $g(u) = g(v) = g(w) = 0$. Then $u, v, w \in \{a, b, c\}$, and they are three different points, so $t = \Delta$. So $\Delta$ is a triangle of $D$.

**Part 2, segments.** Let $C$ be a circle through $p$ and $q$ with every other point of $P$ strictly outside, and let $D$ be a Delaunay triangulation. Assume $pq$ is not an edge of $D$. The points of the open segment $pq$ are strictly inside $C$, as it is a chord, so none of them is in $P$. Move from $p$ toward $q$. The segment does not run along an edge $pu$ of $D$: then $u$ would be on the ray from $p$ through $q$, not strictly between $p$ and $q$, and not equal to $q$; so $q$ would be inside the edge $pu$, which is impossible for a vertex. So the segment enters the interior of a triangle $t = puv$ of $D$. It cannot end in the closed triangle, as $q$ is not a vertex of $t$. It cannot leave through $u$ or $v$, as these are not on the open segment. So it leaves at a point $x$ strictly inside the side $uv$, and $q$ is beyond $x$ on the line from $p$ through $x$. Let $g = f_t - f_C$. Then $g(p) = 0$, and $g(u) = |u|^2 - f_C(u) > 0$ and $g(v) > 0$, so $g(x) > 0$. As $g$ is affine on the line through $p$, $x$ and $q$, and $g(p) = 0 < g(x)$, also $g(q) > 0$. So $f_t(q) > f_C(q) = |q|^2$, which says that $q$ is strictly inside the circle of $t$. This is false, as $D$ is Delaunay. So $pq$ is an edge of $D$.

**Part 3.** Assume no four points of $P$ are on one circle, and let $D$ and $D'$ be Delaunay triangulations, which exist by Part 1. Let $t = abc$ be a triangle of $D$. No point of $P$ is strictly inside its circumcircle, and no point other than $a, b, c$ is on it, by the hypothesis. So $t$ is strongly Delaunay, and by Part 2 it is a triangle of $D'$. So every triangle of $D$ is in $D'$. If $D'$ had another triangle $t'$, its interior would meet the interior of a triangle of $D$, because the triangles of $D$ cover $\operatorname{conv} P$; that triangle is also in $D'$, and two triangles of $D'$ would overlap. So $D = D'$. The triangles of $D$ are strongly Delaunay, as just shown, and every strongly Delaunay triangle is in $D$ by Part 2. $\blacksquare$

## Consequences

- **Algorithms agree.** In general position, every correct algorithm, such as [Bowyer-Watson](/bowyer-watson-algorithm/), [Lawson flips](/lawson-flip-algorithm/), [Fortune's sweep](/fortunes-algorithm/) or [Guibas-Stolfi](/guibas-stolfi-algorithm/), returns the same triangles. This makes the triangulation a good test oracle: compare the sorted triangle lists.
- **Backwards analysis.** The randomized incremental analysis on the [Delaunay triangulation](/delaunay-triangulation/) page needs that the triangulation of each prefix depends only on the set of points, not on their order. Part 3 gives this.
- **Edges common to all answers.** By Part 2, the edges of the [Gabriel graph](/gabriel-graph/), whose diameter circle is strongly empty, and so the closest pair and the edges of the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) in general, are in every Delaunay triangulation. The strongly Delaunay segments are exactly the pairs of points whose [Voronoi cells](/voronoi-cell/) share an edge of positive length ([duality](/voronoi-delaunay-duality/)).
- **Ties.** When points are cocircular, the strongly Delaunay edges cut $\operatorname{conv} P$ into convex polygons inscribed in empty circles, the Delaunay subdivision. Every Delaunay triangulation is obtained by triangulating each of these polygons. This follows from the [lifting map](/paraboloid-lifting-map/): the polygons are the lower faces of the lifted hull.

## Tightness

The hypothesis is needed. For the four corners of a square, both diagonals give a Delaunay triangulation, and for the $k \times k$ grid of points there are $2^{(k-1)^2}$ of them, one choice of diagonal for each of the $(k-1)^2$ unit squares. The hypothesis is not necessary: the four corners of a square are on one circle, but if the center is added, it is strictly inside that circle, and the Delaunay triangulation, with four triangles at the center, is unique. Points on one line are excluded because they have no triangulation at all. No hypothesis on collinear triples is needed: the points $(3,-1)$, $(3,2)$, $(3,5)$, $(0,0)$, $(6,0)$ have three on a line and a unique Delaunay triangulation.

## History

Boris Delaunay (Delone) introduced the empty sphere condition in 1934. He showed that for points in general position the empty spheres define a unique tiling, dual to the Voronoi tiling. The form with strongly Delaunay edges and the Delaunay subdivision for degenerate input is standard in computational geometry textbooks; the proof here with affine functions follows the lifting map view, which goes back to the link between Voronoi diagrams and convex hulls found by K. Q. Brown in 1979.

## References
