---
tag: HT21YA
kind: theorem
slug: voronoi-complexity-theorem
name: Voronoi diagram complexity theorem
aliases:
- size of the Voronoi diagram
- Voronoi diagram has linear size
area: geometry/voronoi-and-delaunay
level: core
summary: A Voronoi diagram of n sites has at most 2n-5 vertices and 3n-6 edges, so its size is O(n).
prereqs: [voronoi-diagram, voronoi-cell, euler-formula, convex-hull]
see_also: [voronoi-diagram-construction, voronoi-delaunay-duality, delaunay-triangulation, general-position-delaunay, fortunes-algorithm, planar-subdivision, higher-dimensional-delaunay, triangulation-of-point-set]
sources:
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 7.1 (the diagram is connected unless the sites are collinear, and the bounds of 2n - 5 vertices and 3n - 6 edges by Euler's formula)
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the linear bound on the number of Voronoi vertices and edges
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapter 2 (the counts of vertices and edges with the number of hull sites and degenerate vertices)
---

The Voronoi complexity theorem says that the [Voronoi diagram](/voronoi-diagram/) of $n$ point sites in the plane has linear size. If $n \ge 3$ and the sites are not all on one line, it has at most $2n - 5$ vertices and at most $3n - 6$ edges, and both bounds are reached exactly when three sites span the convex hull and no four sites lie on an empty circle. The exact counts are $2n - 2 - h - X$ vertices and $3n - 3 - h - X$ edges, where $h$ is the number of sites on the boundary of the convex hull and $X$ measures the vertices of degree more than $3$. So every algorithm that writes out the diagram writes $O(n)$ items, and the bound on the time of [Voronoi construction](/voronoi-diagram-construction/) is not driven by the output size.

## Statement

**Setting.** $P$ is a set of $n$ distinct sites $p = (x, y)$ in the plane. The [cell](/voronoi-cell/) of $p$ is $V_p = \{x : |x - p| \le |x - s| \text{ for all } s \in P\}$. A **Voronoi vertex** is a point with three or more nearest sites. For two sites $p \ne q$, the set $V_p \cap V_q$ lies on their bisector; when it has positive length, its relative interior is a **Voronoi edge**, a segment, a ray or a line. $h$ is the number of sites on the boundary of the convex hull of $P$, counting the sites inside hull edges, not only the corners. The **degree** of a vertex $x$ is the number $k_x$ of sites on the circle around $x$ through its nearest sites; this circle is empty, that is, no site is strictly inside it. Let $X = \sum_x (k_x - 3)$ over all vertices.

**Theorem.** Let $n \ge 3$ and let the sites not all lie on one line. Let $v$ be the number of Voronoi vertices and $e$ the number of Voronoi edges. Then

$$v = 2n - 2 - h - X, \qquad e = 3n - 3 - h - X.$$

Since $h \ge 3$ and $X \ge 0$, $v \le 2n - 5$ and $e \le 3n - 6$. Both bounds hold with equality if and only if $h = 3$ and no four sites lie on one empty circle. If no four sites lie on one empty circle, $X = 0$ and the counts are $2n - 2 - h$ and $3n - 3 - h$.

**Collinear sites.** If all $n \ge 2$ sites lie on one line, the diagram has no vertex and $n - 1$ edges, the parallel bisectors of consecutive sites. For $n \ge 3$ this also satisfies the two bounds.

Notation used elsewhere in this area: $\mathrm{orient}(p, q, r)$ is positive when $p, q, r$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle. The theorem itself needs neither predicate, and it assumes no general position.

## In plain words

Split the plane into regions, one for each site, by the nearest site. The borders form a network of straight pieces that meet at corners. The theorem says that this network is small: it has fewer than two corners and fewer than three border pieces for each site.

The reason is a counting rule for drawings in the plane, Euler's rule, together with the fact that at least three border pieces meet at each corner. The outer sites of the set have regions that go on forever, and each of them takes away one corner and one border piece from the count. Corners where four or more regions meet also lower the count.

## Proof

**Lemma 1 (edges and vertices).** For sites $p \ne q$, the set $V_p \cap V_q$ is convex and lies on the bisector of $p$ and $q$. A point in its relative interior has exactly the two nearest sites $p$ and $q$. Its ends, if any, are Voronoi vertices.

*Proof.* Both cells are intersections of closed half-planes, so they are convex and so is their intersection; on it, $|x - p| = |x - q|$. Let $x$ be in the relative interior and assume that a third site $s$ is as near to $x$ as $p$. The function $\phi(y) = |y - s|^2 - |y - p|^2 = |s|^2 - |p|^2 - 2 y \cdot (s - p)$ is affine, $\ge 0$ on $V_p \cap V_q$, and $0$ at $x$. An affine function on a segment that is $\ge 0$ and is zero at an inner point is zero on the whole segment. So the segment lies on the bisector of $p$ and $s$ as well as on that of $p$ and $q$, two lines with a common segment, so they are equal, and $s = q$, a contradiction. An end $x$ of $V_p \cap V_q$ is in the closed set $V_p \cap V_q$; beyond $x$ on the bisector, points are not in $V_p \cap V_q$, so some site $s \ne p, q$ is strictly nearer there; by continuity $|x - s| \le |x - p|$, and so $s$ is a third nearest site of $x$. $\square$

**Lemma 2 (degree of a vertex).** Let $x$ be a vertex with the $k = k_x$ nearest sites $s_1, \ldots, s_k$, in counterclockwise order around $x$. Then exactly $k$ Voronoi edges have $x$ as an end, one between each pair $s_i, s_{i+1}$ (indices mod $k$), and no edge passes through $x$.

*Proof.* The sites lie on the circle of radius $r$ around $x$, so they are distinct points of one circle. All other sites are at distance more than $r$, so for $\varepsilon$ small and $y = x + \varepsilon u$ with $|u| = 1$, the nearest sites of $y$ are among $s_1, \ldots, s_k$. For these, $|y - s_i|^2 = r^2 - 2 \varepsilon u \cdot (s_i - x) + \varepsilon^2$, so the nearest are those that maximize $u \cdot (s_i - x)$, that is, whose direction from $x$ is nearest in angle to $u$. As $u$ turns once around, the nearest site changes exactly at the $k$ directions of the angle bisectors between $s_i - x$ and $s_{i+1} - x$, and there $y$ is on the bisector of $s_i$ and $s_{i+1}$ with these two sites nearest. So near $x$ the diagram consists of $k$ short segments from $x$, one on the bisector of each consecutive pair, and these pairs are distinct because $k \ge 3$. By Lemma 1, $x$ is not in the relative interior of an edge, so each of the $k$ segments starts a different edge at its end $x$. $\square$

**Lemma 3 (unbounded cells).** $V_p$ is unbounded if and only if $p$ lies on the boundary of the convex hull $H$ of $P$.

*Proof.* Let $p$ be on the boundary of $H$, with an outer unit normal $u$ of a supporting line of $H$ at $p$, so $u \cdot (s - p) \le 0$ for all $s$. For $x = p + t u$ with $t \ge 0$, $|x - s|^2 = t^2 - 2 t u \cdot (s - p) + |s - p|^2 \ge t^2 = |x - p|^2$. So the whole ray is in $V_p$. Let $p$ be in the interior of $H$. Then for every unit vector $u$ some site $s$ has $u \cdot (s - p) > 0$, and for $x = p + t u$, $|x - s|^2 - |x - p|^2 = |s - p|^2 - 2 t u \cdot (s - p) < 0$ for large $t$. So $V_p$ holds no ray from $p$. A closed convex set that is unbounded holds a ray from each of its points, so $V_p$ is bounded. $\square$

**Lemma 4 (shape of a cell).** If the sites are not on one line, no Voronoi edge is a whole line, and the boundary of each cell is a closed polygon, if the cell is bounded, or a connected polygonal chain whose two end pieces are rays, if it is unbounded.

*Proof.* Assume the edge between $p$ and $q$ is a whole line $L$. For any other site $s$, the affine function $\phi(y) = |y - s|^2 - |y - p|^2$ is $\ge 0$ on all of $L$, so it is constant on $L$, and its gradient $2 (p - s)$ is orthogonal to $L$, that is, parallel to $q - p$. So every $s$ lies on the line through $p$ and $q$, which is false. A cell $V_p$ is a closed convex polygonal region with nonempty interior, not the whole plane since $n \ge 2$. Its boundary is a closed convex polygon, or a single line (a half-plane), or two parallel lines (a strip), or a chain of two or more sides whose two end sides are rays. Every side of the boundary is a union of edges and vertices of the diagram. If a side is a whole line $L$, every edge on $L$ lies on the bisector of $p$ and some site $q$, and the bisector is $L$, which fixes $q$; so $L$ is one edge, a whole line, which is excluded. So only the first and the last case remain, with rays at the ends. $\square$

**Lemma 5 (connected).** Let $D$ be the union of the Voronoi vertices and edges, together with a point $\infty$ that is the end of every ray. If the sites are not on one line, $D$ is connected.

*Proof.* By Lemma 4, the boundary of an unbounded cell, with $\infty$ added at its two rays, is connected and contains $\infty$, and the boundary of a bounded cell is a closed polygon. Every boundary point of a cell has a second nearest site, so it lies in $D$, and $D$ is the union of the cell boundaries. Let $V_p$ be bounded. Take a ray from $p$ that passes through none of the finitely many vertices. It meets finitely many edges, each at one point, and passes through a chain of cells, and two consecutive cells of the chain share the crossing point on their boundaries. The last cell is unbounded. So the boundary of $V_p$ is joined within $D$ to the boundary of an unbounded cell, and so to $\infty$. $\square$

**Proof of the theorem.** Put $\infty$ on the sphere by stereographic projection. The vertices of the diagram and $\infty$, with the edges as arcs (a ray becomes an arc that ends at $\infty$), form a graph $G$ drawn on the sphere without crossings. By Lemma 4, every edge has at least one finite end, so $G$ has no loops; it can have parallel edges, as for $n = 3$. $G$ has $v + 1$ vertices and $e$ edges, and it is connected by Lemma 5. Its faces are the components of the complement of $D$. A point off $D$ has one nearest site, so the complement is the union of the $n$ open sets $\{x : |x - p| < |x - s| \text{ for all } s \ne p\}$, each convex, nonempty (it holds $p$) and so connected. So $G$ has $n$ faces. [Euler's formula](/euler-formula/) for connected plane multigraphs gives

$$(v + 1) - e + n = 2.$$

Each edge has two ends, so the sum of the degrees in $G$ is $2e$. A finite vertex $x$ has degree $k_x$ by Lemma 2. The degree of $\infty$ is the number $r$ of rays. Each ray lies on the boundary of two cells, which are unbounded, and by Lemma 4 each unbounded cell has exactly two rays on its boundary. By Lemma 3 there are $h$ unbounded cells, so $2r = 2h$ and $r = h$. So

$$\sum_x k_x + h = 3 v + X + h = 2e.$$

From Euler's formula, $v = e - n + 1$; putting this in gives $3e - 3n + 3 + X + h = 2e$, so $e = 3n - 3 - h - X$ and $v = 2n - 2 - h - X$.

The sites are not on one line, so $H$ is a polygon with at least $3$ corners, and $h \ge 3$; also $X \ge 0$. So $v \le 2n - 5$ and $e \le 3n - 6$, with equality in either one exactly when $h = 3$ and $X = 0$. Finally $X = 0$ means that every vertex has $k_x = 3$. A circle with no site strictly inside and with four or more sites on it has a center whose nearest sites are exactly those sites, so the center is a vertex with $k_x \ge 4$; conversely a vertex with $k_x \ge 4$ gives such a circle. So $X = 0$ if and only if no four sites lie on an empty circle.

For collinear sites, sorted along their line as $p_1, \ldots, p_n$, the cell of $p_i$ is the strip between the bisectors of $p_{i-1} p_i$ and $p_i p_{i+1}$, so the diagram is the $n - 1$ bisectors of consecutive sites, with no vertex. $\blacksquare$

## Consequences

- **Linear output.** The diagram, stored as a [planar subdivision](/planar-subdivision/) with all adjacencies, has $O(n)$ size, so [Fortune's algorithm](/fortunes-algorithm/) and the other $O(n \log n)$ algorithms are not slowed by the output.
- **Average cell.** The sum of the numbers of edges of all cells is $2e \le 6n - 12$, so the average cell has fewer than $6$ edges. A single cell can still have $n - 1$ edges, as for a site at the center of a circle of other sites.
- **Delaunay counts.** By [duality](/voronoi-delaunay-duality/), the vertices and edges of the diagram match the faces and edges of the Delaunay subdivision. In general position, every [Delaunay triangulation](/delaunay-triangulation/) of $P$ has $2n - 2 - h$ triangles and $3n - 3 - h$ edges, the counts for any [triangulation of the point set](/triangulation-of-point-set/).
- **Proximity graphs.** The Delaunay graph has at most $3n - 6$ edges, so the minimum spanning tree, the Gabriel graph and the relative neighbourhood graph, which are its subgraphs, are found by looking at $O(n)$ candidate pairs.
- **Geometric graphs in general.** The same Euler argument gives the bound $3n - 6$ for every plane straight-line graph on $n \ge 3$ points.

## Tightness

- **Both bounds are reached.** For the six sites $(0,0)$, $(6,0)$, $(0,6)$, $(1,1)$, $(2,3)$, $(3,1)$, the hull has $h = 3$ sites and no four sites lie on an empty circle. The diagram has $7 = 2n - 5$ vertices, among them $(2, 7/4)$, $(-13/14, 45/14)$ and $(23/2, 23/2)$, and $12 = 3n - 6$ edges.
- **Hull sites lower the count.** For six sites $(2,8)$, $(6,7)$, $(0,4)$, $(4,5)$, $(8,3)$, $(3,0)$, where $h = 5$, the diagram has $5 = 2n - 2 - h$ vertices and $10 = 3n - 3 - h$ edges; see [Voronoi diagram construction](/voronoi-diagram-construction/).
- **Cocircular sites lower the count.** For the $k \times k$ grid, $n = k^2$ and $h = 4(k - 1)$. Every unit square gives a vertex at its center with $4$ sites on its circle, so $X = (k - 1)^2$, and the diagram has $(k - 1)^2$ vertices and $2k(k - 1)$ edges, the lines $x = i + 1/2$ and $y = j + 1/2$ cut into pieces. For $k = 3$ this is $4$ vertices and $12$ edges, against $2n - 2 - h = 8$ and $3n - 3 - h = 16$ in general position.
- **The hypothesis on collinear sites is needed.** For $n = 2$ the diagram has $1$ edge, more than $3n - 6 = 0$. For $n \ge 3$ collinear sites the bounds hold, but the formulas with $h$ fail: $n$ sites on a line give $n - 1$ edges and no vertex, while $3n - 3 - h$ with $h = n$ gives $2n - 3$.
- **Higher dimensions.** The linear bound is special to the plane. In $\mathbb{R}^d$ the diagram of $n$ sites can have $\Theta(n^{\lceil d/2 \rceil})$ faces, for example $\Theta(n^2)$ vertices in $\mathbb{R}^3$ for sites on two skew lines; see [higher-dimensional Delaunay](/higher-dimensional-delaunay/).

## History

M. I. Shamos and D. Hoey showed in 1975 that the Voronoi diagram of $n$ points in the plane has $O(n)$ vertices and edges, by Euler's formula, and used this for their $O(n \log n)$ divide and conquer algorithm. The bounds $2n - 5$ and $3n - 6$ with the argument through a vertex at infinity are the form in the textbook of de Berg, Cheong, van Kreveld and Overmars. The counts with the number of hull sites and degenerate vertices are in the book of Okabe, Boots, Sugihara and Chiu.

## References
