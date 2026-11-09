---
tag: 25RNN7
kind: data-structure
slug: weighted-voronoi-diagram
name: Weighted Voronoi diagram
aliases:
- additively weighted Voronoi diagram
- multiplicatively weighted Voronoi diagram
- Apollonius diagram
- Voronoi diagram of circles
area: geometry/voronoi-and-delaunay
level: advanced
summary: Voronoi diagram in which each site has a weight that shifts or scales its distance function.
model: real-ram
complexity:
  vars: {n: the number of sites}
  time: {build: O(n log n), query: O(log n)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [voronoi-diagram, fortunes-algorithm]
see_also: [power-diagram, regular-triangulation, medial-axis, order-k-voronoi-diagram, farthest-point-voronoi-diagram, voronoi-cell, planar-point-location, k-nearest-neighbor-search]
sources:
  - paper: doi:10.1007/BF01840357
    title: S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2, 1987, 153-174
    locator: the extension of the sweep to additively weighted sites (circles) and its O(n log n) time
  - paper: "F. Aurenhammer and H. Edelsbrunner, An optimal algorithm for constructing the weighted Voronoi diagram in the plane, Pattern Recognition 17(2), 1984, 251-257"
    locator: the multiplicatively weighted diagram, its quadratic worst-case size and an O(n^2) construction
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapter 3 (multiplicatively and additively weighted Voronoi diagrams)
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Toth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: the chapter on Voronoi diagrams and Delaunay triangulations (generalized distance functions)
---

A weighted Voronoi diagram gives each site $p$ a weight $w_p$ that changes how its distance is measured, and splits the plane into the regions where each site is nearest under these distances. In the **additively weighted** diagram the distance is $|x - p| - w_p$, the distance from $x$ to the circle of radius $w_p$ around $p$, so the diagram is the [Voronoi diagram](/voronoi-diagram/) of circles, also called the Apollonius diagram; its borders are branches of hyperbolas, each cell is star-shaped around its site, and it is built in $O(n \log n)$ time by a [sweep](/fortunes-algorithm/). In the **multiplicatively weighted** diagram the distance is $|x - p| / w_p$; its borders are circles, a cell can split into several pieces, and the whole diagram can have size $\Theta(n^2)$. The [power diagram](/power-diagram/), with $|x - p|^2 - w_p$, is the third common weighting and has straight borders.

## In plain words

Think of shops. In the usual map, each house goes to the closest shop. Now some shops are more attractive.

In the first kind, a shop gets a head start: its distance counts as a fixed amount shorter. This is like growing a circle around each shop and measuring the distance to the edge of the circle. Borders between two shops bend toward the weaker shop. A weak shop very close to a strong one gets no houses at all.

In the second kind, a strong shop makes every distance shorter by the same factor. The border between two shops is then a circle around the weaker one. The weaker shop keeps a round island, and the strong shop takes everything outside it. Regions can break into several islands.

## The abstract type

The structure holds distinct sites $p = (x, y)$ with integer coordinates and integer weights, and one mode: additive with $w_p \ge 0$, or multiplicative with $w_p > 0$. It supports:

- $\mathrm{insert}(p, w)$: add a site; return false if $p$ is already a site, and keep the first weight.
- $\mathrm{nearest}(q)$: the sites at the smallest weighted distance from a point $q$ with rational coordinates; several only on a border.
- $\mathrm{hasCell}(p)$: whether the cell of the site $p$ has nonempty interior.
- $\mathrm{bisector}(p, r)$: the set of points at equal weighted distance from $p$ and $r$, as a line, a circle, a hyperbola branch, a ray, or empty.

Notation: $P$ is the set of sites, $n = |P|$, $h$ is the number of sites on the boundary of the convex hull, $d$ is the number of edges of a cell, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle.

**Definitions.** The additive distance is $\delta_p(x) = |x - p| - w_p$, and the multiplicative distance is $\mu_p(x) = |x - p| / w_p$. The cell of $p$ is the set of points $x$ whose distance to $p$ is at most the distance to every other site. The bisector of two sites is the set of points at equal distance.

**Properties.** These are proved in [the correctness proof](proofs/correctness/), except the sizes, which are cited.

- **Equal weights.** If all weights are equal, both diagrams are the ordinary Voronoi diagram, and every bisector is the perpendicular bisector line.
- **Additive bisectors.** For $p \ne r$ with $k = w_p - w_r$, the bisector is $\{x : |x - p| - |x - r| = k\}$. It is a line if $k = 0$, one branch of the hyperbola with foci $p$ and $r$, bent around the lighter site, if $0 < |k| < |p - r|$, a ray from the lighter site away from the heavier one if $|k| = |p - r|$, and empty if $|k| > |p - r|$.
- **Hidden sites.** In the additive diagram, the cell of $p$ has nonempty interior exactly when $|p - r| > w_r - w_p$ for every other site $r$, that is, when the closed disc of $p$ is not inside the closed disc of another site. Otherwise the cell is empty or a ray.
- **Star-shaped cells.** A nonempty additive cell holds its site and contains the segment from its site to each of its points. So it is connected.
- **Multiplicative bisectors.** For $w_p < w_r$, the region where $p$ is at least as near as $r$ is the closed disc bounded by the Apollonius circle with center $\frac{w_r^2 p - w_p^2 r}{w_r^2 - w_p^2}$ and radius $\frac{w_p w_r |p - r|}{w_r^2 - w_p^2}$; it holds $p$. Every multiplicative cell has nonempty interior, since the distance to $p$ tends to $0$ near $p$.
- **Sizes (cited).** The additive diagram has $O(n)$ vertices and edges. The multiplicative diagram has $O(n^2)$ vertices and edges, and some inputs need $\Omega(n^2)$.

**General position.** No assumption is made. The predicates compare sums of square roots exactly. Three or more sites can be equally near a point, and $\mathrm{nearest}$ then returns all of them. Equal weights give straight bisectors. A site whose disc touches a larger disc from inside has an additive cell that is at most a ray, with empty interior.

## Representation

The code keeps the list of sites and their weights, and answers queries by comparing distances. A full structure stores the diagram as a [doubly connected edge list](/doubly-connected-edge-list/) whose edges are arcs of the bisectors, with a [planar point location](/planar-point-location/) structure over it. For the additive diagram the dual graph, the Apollonius graph, plays the role of the Delaunay triangulation and is kept with incremental insertion.

**Exact comparison.** For the additive mode, $\delta_p(q) < \delta_r(q)$ is the sign of $\sqrt{a} - \sqrt{b} - c$ with $a = |q - p|^2$, $b = |q - r|^2$ and $c = w_p - w_r$, all rational. The code finds the sign of $\sqrt{b} + c$ first. If it is $\le 0$, the answer is positive unless $a = 0$ and $\sqrt{b} + c = 0$. Otherwise both sides are positive, and it compares the squares: the sign of $(a - b - c^2) - 2 c \sqrt{b}$, which is found by comparing signs and then squaring once more. For the multiplicative mode, the sign of $|q - p|^2 w_r^2 - |q - r|^2 w_p^2$ needs no root.

## Operations

```pseudo id=main
NEAREST(P, w, q)
L1  for each site p_i in P do
L2      c ← the sign of dist(q, p_i) - dist(q, p_best), or -1 if there is no best site yet
L3      if c < 0 then best ← [p_i]
L4      else if c = 0 then append p_i to best
L5  return best
```

- **Lines L1 to L4.** One exact comparison per site, in $O(1)$ time with numbers of bounded size, so $O(n)$ time per query. With the diagram and point location, a query takes $O(\log n)$ time.
- **hasCell(p).** Additive mode: the test $|p - r| > w_r - w_p$ for every other $r$, in $O(n)$ time, with the same exact square root sign. Multiplicative mode: always true.
- **bisector(p, r).** Additive mode: compare $k^2$ with $|p - r|^2$ for $k = w_p - w_r$. Multiplicative mode: the circle above, with rational center and squared radius. Both in $O(1)$ time.

**Building the additive diagram.** Fortune's sweep extends to circles, with a beach line of curves and the same two kinds of events, and takes $O(n \log n)$ time. Incremental construction of the Apollonius graph, as in the Delaunay case, is used in practice.

## Example

Additive mode with the circles of radius $3$ around $(0,0)$, radius $1$ around $(8,0)$, radius $2$ around $(4,6)$, and the point $(1,1)$ with weight $0$.

- **hasCell((1,1)).** $|(1,1) - (0,0)| = \sqrt{2} \le 3 - 0$, so the point $(1,1)$ is inside the disc of $(0,0)$, and its cell is empty. In the ordinary Voronoi diagram it would own a region near the origin.
- **Bisector of $(0,0)$ and $(8,0)$.** $k = 3 - 1 = 2 < 8$, so it is the branch $|x| - |x - (8,0)| = 2$ of a hyperbola, bent around the lighter site $(8,0)$. It crosses the $x$-axis at $(5, 0)$, where $5 - 3 = 3 - 1$, while the ordinary bisector crosses at $(4, 0)$.
- **nearest((4,0)).** The distances are $4 - 3 = 1$, $4 - 1 = 3$, $6 - 2 = 4$ and $\sqrt{10}$, so the answer is $[(0,0)]$.
- **nearest((5,0)).** The distances to $(0,0)$ and $(8,0)$ are both $2$; the others are $\sqrt{37} - 2$ and $\sqrt{17}$. The answer is $[(0,0), (8,0)]$, a point of the bisector.

Multiplicative mode with $(0,0)$ of weight $1$ and $(6,0)$ of weight $2$: the bisector is the circle with center $(-2, 0)$ and radius $4$, through $(2, 0)$ and $(-6, 0)$. At $(2, 0)$ the distances are $2/1$ and $4/2$. The lighter site $(0,0)$ owns the disc, and $(6,0)$ owns all the plane outside it.

## Correctness

**Theorem.** For distinct integer sites with integer weights in either mode, $\mathrm{nearest}(q)$ returns exactly the sites at the smallest weighted distance from $q$, $\mathrm{hasCell}$ is right, and $\mathrm{bisector}$ returns the bisector with the stated shape.

The comparison is exact: in the additive mode the sign of $\sqrt{a} - \sqrt{b} - c$ is reduced, by case analysis on signs, to comparisons of squares of nonnegative numbers, which keep the order. The cell test follows from the triangle inequality: if the disc of $p$ is inside the disc of $r$, then $\delta_r \le \delta_p$ everywhere, with equality only on a ray; otherwise $p$ itself is strictly nearest to $p$. The full proof, with the bisector shapes and the star-shaped cells, is in [the correctness proof](proofs/correctness/).

## Complexity

- **Query in this code.** $O(n)$ worst-case time for $\mathrm{nearest}$ and the additive $\mathrm{hasCell}$, $O(1)$ for $\mathrm{insert}$ and $\mathrm{bisector}$.
- **Additive diagram.** $O(n)$ size and $O(n \log n)$ worst-case build time by the sweep (cited). The lower bound $\Omega(n \log n)$ in the algebraic computation tree model holds because zero weights give the Voronoi diagram ([lower bound](/voronoi-construction-lower-bound/)).
- **Multiplicative diagram.** $\Theta(n^2)$ worst-case size and an $O(n^2)$ construction (cited).
- **Query with the diagram.** $O(\log n)$ with point location over a diagram of size $O(n)$.
- **Space.** $O(n)$ for the code and for the additive diagram.

## Variants

- **Power diagram.** The distance $|x - p|^2 - w_p$ gives straight bisectors and convex cells, and the dual is the [regular triangulation](/regular-triangulation/) ([power diagram](/power-diagram/)).
- **Voronoi diagram of segments and polygons.** Sites that are segments give bisectors made of line pieces and parabola arcs; inside a polygon this gives the [medial axis](/medial-axis/). Fortune's sweep and incremental methods also handle segments.
- **Compoundly weighted.** The distance $|x - p| / w_p - v_p$ mixes both weights and contains both diagrams as special cases.
- **Furthest and higher order.** Weighted versions of the [farthest-point](/farthest-point-voronoi-diagram/) and [order-k](/order-k-voronoi-diagram/) diagrams use the same distances.
- **Crystal growth.** The multiplicative diagram models seeds that grow at different speeds from the same start time; the additive diagram models equal speeds with different start times.

## When to use it

Use the additive diagram for disks or circles: the nearest disk boundary, clearance maps among round obstacles, and ball packings. Use the multiplicative diagram when sites act with different strengths, as in market areas with different attractiveness or growth at different speeds. If straight borders and convex cells are wanted, or a triangulation dual is needed, use the power diagram instead.

## Pitfalls

- **Additive distance is not to the disc.** For points inside the disc of $p$, $|x - p| - w_p$ is negative. This is right for the diagram, but it is not the distance to the disc.
- **Hidden sites.** An additive site inside another site's disc has no cell; code that expects one cell per site breaks.
- **Wrong branch.** The additive bisector is one branch of a hyperbola, around the lighter site; the other branch is not part of it.
- **Disconnected cells.** Multiplicative cells can have several pieces and holes, so a walk from the site does not find the whole cell.
- **Floating-point roots.** Comparing $\sqrt{a} - \sqrt{b}$ with rounding fails near borders; exact comparison by squaring needs care with the signs before each squaring.

## Implementations

## History

Weighted distances appear in early work on growth models and in geography, where Voronoi-like regions with different attractiveness were used for market areas. F. Aurenhammer and H. Edelsbrunner gave an optimal $O(n^2)$ algorithm for the multiplicatively weighted diagram in 1984. S. Fortune showed in 1987 that his sweep also builds the additively weighted diagram in $O(n \log n)$ time. M. Sharir and others studied the Voronoi diagram of disks, and later work gave incremental and dynamic algorithms for the Apollonius graph, which are now in standard geometry libraries.

## References
