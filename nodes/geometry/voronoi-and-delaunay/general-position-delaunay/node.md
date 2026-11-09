---
tag: B97033
kind: concept
slug: general-position-delaunay
name: General position
aliases:
- general position assumption
- general position for Delaunay
- nondegenerate point set
area: geometry/voronoi-and-delaunay
level: core
summary: Assumption that no three sites are collinear and no four are cocircular, so the Delaunay triangulation is unique.
prereqs: [general-position, in-circle-test, delaunay-triangulation]
see_also: [delaunay-triangulation-uniqueness, paraboloid-lifting-map, regular-triangulation, empty-circle-property, voronoi-diagram, fortunes-algorithm, lawson-flip-algorithm, voronoi-complexity-theorem]
sources:
  - paper: "H. Edelsbrunner and E. P. Mücke, Simulation of Simplicity, a technique to cope with degenerate cases in geometric algorithms, ACM Transactions on Graphics 9(1), 1990, 66-104"
    locator: symbolic perturbation of the input by powers of a small parameter, and the sign of a perturbed determinant as the first nonzero coefficient
  - paper: "R. Seidel, The nature and meaning of perturbations in geometric computing, Discrete and Computational Geometry 19(1), 1998, 1-17"
    locator: what a perturbation scheme guarantees about the output for the unperturbed input
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 2 (generic point sets, uniqueness of the Delaunay triangulation, Delaunay subdivisions of cocircular points)
---

A set of sites is in general position for Delaunay and Voronoi computations when no three sites are on one line and no four sites are on one circle. Under the second condition the [Delaunay triangulation](/delaunay-triangulation/) is unique, and every vertex of the [Voronoi diagram](/voronoi-diagram/) has exactly three edges. Many papers state their algorithms under this assumption, because it removes the ties in the [in-circle test](/in-circle-test/). Real input, such as points on a grid, breaks it all the time, so a correct program needs either exact predicates with a rule for ties or a symbolic perturbation.

## In plain words

Most ways to scatter points at random give no three points on a line and no four points on a circle. Such a scatter has exactly one best triangle mesh, the Delaunay one, and the nearest-site map has exactly three regions meeting at each corner.

Points typed by people or taken from a grid are not like that. Four corners of a square are on one circle, and either diagonal of the square gives a correct mesh. A program that assumes this never happens can loop, make crossing edges, or crash.

There are two cures. The first is to compute every test exactly and to use a fixed rule when a test says "on the circle". The second is to pretend that every point is moved by a tiny, carefully chosen amount, so that no test ever says "on the circle", and to keep the answer for the moved points.

## The idea

Notation: $P$ is a finite set of $n$ points in the plane, not all on one line, with $h$ of them on the boundary of the convex hull; a point is $p = (x, y)$ with $|p|^2 = x^2 + y^2$; $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise; $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside the circle through $a$, $b$, $c$.

**The two conditions.**

- (G1) No three points of $P$ are on one line, so $\mathrm{orient}(a, b, c) \ne 0$ for distinct $a, b, c \in P$. This is the [general position](/general-position/) of convex hull algorithms.
- (G2) No four points of $P$ are on one circle, so $\mathrm{incircle}(a, b, c, d) \ne 0$ for distinct $a, b, c, d \in P$ with $\mathrm{orient}(a, b, c) \ne 0$.

Only (G2) matters for the Delaunay triangulation itself. Three points on one line are not on one circle, and the triangulation handles them without trouble. (G1) is added in many papers to simplify the description of algorithms such as [Fortune's sweep](/fortunes-algorithm/) or divide and conquer.

**The exact condition for uniqueness.** By the [lifting map](/paraboloid-lifting-map/), the Delaunay triangulations of $P$ are exactly the ways to cut each face of the Delaunay subdivision into triangles with the face's own corners, and the corners of each face are the points of $P$ on one circle with no point of $P$ inside. A convex polygon with $m \ge 4$ corners $v_1, \ldots, v_m$ has at least two such cuttings: the fan from $v_1$ uses the diagonal $v_1 v_3$, and the fan from $v_2$ uses the diagonal $v_2 v_4$, which crosses $v_1 v_3$. So:

> The Delaunay triangulation of $P$ is unique exactly when no circle with no point of $P$ inside passes through four or more points of $P$.

(G2) implies this condition, but it is not needed: four points on a circle with a fifth point inside do not break uniqueness. On the Voronoi side, the same condition says that every Voronoi vertex has exactly three edges, since a vertex is the center of a circle with no site inside and with all its nearest sites on it ([Voronoi complexity theorem](/voronoi-complexity-theorem/)). The full proof of uniqueness is on [Delaunay triangulation uniqueness](/delaunay-triangulation-uniqueness/).

**Random points.** For points with coordinates drawn from a continuous distribution, (G1) and (G2) hold with probability $1$: each fails only when a nonzero polynomial in the coordinates, $\mathrm{orient}$ or the in-circle determinant, is zero, and the zero set of a nonzero polynomial has measure zero. Points with integer or rounded coordinates have no such guarantee.

**Cure 1: exact predicates and tie rules.** Compute $\mathrm{orient}$ and $\mathrm{incircle}$ exactly, for example with integers. Then decide each tie by a fixed rule that keeps the algorithm's invariant. For example, the [Lawson flip algorithm](/lawson-flip-algorithm/) flips an edge only when the in-circle value is strictly positive, and the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/) removes only the triangles whose circle holds the new point strictly inside. Both then stop with a valid Delaunay triangulation, one of the several. The pages of this area use this cure, and their tests run on grids.

**Cure 2: symbolic perturbation.** Number the points $p_1, \ldots, p_n$ and, for a small number $\varepsilon$ with $0 < \varepsilon < 1$, lift $p_i$ to the height $z_i = |p_i|^2 + \varepsilon^i$ in place of $|p_i|^2$. The in-circle test of the lifted points is the $4 \times 4$ determinant with rows $(x, y, z, 1)$; it is linear in each $z_i$, so for the points $p_i, p_j, p_k, p_l$ with distinct indices it is

$$I_\varepsilon = I_0 + \sum_{m \in \{i, j, k, l\}} \pm \varepsilon^m \, D_m,$$

where $I_0$ is the exact value and $D_m$ is $D$ of the three points other than $p_m$, with a sign fixed by the place of $p_m$ in the row order. The four powers of $\varepsilon$ are different. So for all small enough $\varepsilon$, the sign of $I_\varepsilon$ is the sign of $I_0$ when $I_0 \ne 0$, and otherwise the sign of the term with the smallest power whose $D_m$ is not zero. If $p_i$, $p_j$, $p_k$ are not on one line, $D_l \ne 0$, so this sign is never zero. The program evaluates these few exact determinants in this order and never sees a tie.

**What the perturbation returns.** Let $\delta > 0$ be the smallest squared distance between two points of $P$, and take $\varepsilon^1 < \delta$, small enough for the signs above. Then:

1. Every lifted point stays a vertex of the lower hull: the tangent plane $q \mapsto 2 p_i \cdot q - |p_i|^2 + \varepsilon^i$ passes through the new lifted $p_i$, and every other new lifted point $p_j$ is above it by $|p_j - p_i|^2 + \varepsilon^j - \varepsilon^i > \delta - \varepsilon > 0$.
2. All lower faces are triangles. For small $\varepsilon$, no three new lifted points are on one line, because without the perturbation the middle one of three collinear points is strictly below the segment of the other two. So four corners of one lower face would include three points that are not on one line in the plane, and their perturbed in-circle value would be zero, which does not happen.
3. Each such triangle $t$ is Delaunay for $P$: no point $p$ has $\mathrm{incircle}(t, p) > 0$, since an exact positive value keeps its sign under the perturbation, and the perturbed values for the points outside $t$ are negative.

So the projection of the perturbed lower hull is one of the Delaunay triangulations of $P$, chosen by the numbering of the points, and the same for all small $\varepsilon$. Simulation of Simplicity by Edelsbrunner and Mücke is a general form of this scheme.

## Examples

**Four cocircular points, two answers.** The square $(0,0)$, $(1,0)$, $(1,1)$, $(0,1)$ has $\mathrm{incircle} = 0$ for every triangle and the fourth corner. Both diagonals give a Delaunay triangulation. The Voronoi diagram has one vertex at $(\frac{1}{2}, \frac{1}{2})$ with four edges.

**Four cocircular points, one answer.** Add the center $(1,1)$ to the square $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$. The circle through the four corners now holds a point, so it is not a Delaunay circle. The triangle formed by the center and the side from $(0,0)$ to $(2,0)$ has circumcenter $(1,0)$ and radius $1$, and the two other corners are at distance $\sqrt{5}$; the other three sides are the same by symmetry. The Delaunay triangulation is the unique fan of four triangles around the center.

**Three collinear points, one answer.** For $(0,0)$, $(1,0)$, $(2,0)$, $(1,1)$, the circle of $(0,0)$, $(1,0)$, $(1,1)$ has center $(\frac{1}{2}, \frac{1}{2})$ and squared radius $\frac{1}{2}$, and $(2,0)$ is at squared distance $\frac{5}{2}$, outside; by symmetry the same holds on the other side. The unique Delaunay triangulation has the two triangles that share the edge from $(1,0)$ to $(1,1)$. (G1) fails, (G2) holds, and the answer is unique.

**The perturbation on the square.** Number the square $(0,0)$, $(1,0)$, $(1,1)$, $(0,1)$ as $p_1, \ldots, p_4$. The perturbed in-circle value of $p_4$ against the counterclockwise triangle $p_1 p_2 p_3$ is $\varepsilon - \varepsilon^2 + \varepsilon^3 - \varepsilon^4 > 0$: raising $p_1$ by the largest amount raises the plane of $p_1 p_2 p_3$ above the lifted $p_4$. So that triangle fails, and the perturbation picks the diagonal from $(1,0)$ to $(0,1)$, the one that avoids $p_1$.

**A grid.** The $k \times k$ integer grid has $(k - 1)^2$ unit squares, each a Delaunay face with four corners, so it has $2^{(k - 1)^2}$ Delaunay triangulations; $16$ for $k = 3$. It is the standard test input for the tie rules.

## Where it is used

- **Algorithm descriptions.** [Fortune's sweep](/fortunes-algorithm/), divide and conquer, and randomized incremental construction are usually stated under (G1) and (G2); their correct versions for all input use one of the two cures.
- **Uniqueness statements.** Facts such as the [max-min angle](/delaunay-max-min-angle/) theorem and the count of $2n - 2 - h$ triangles hold for every Delaunay triangulation, but statements about "the" Delaunay triangulation need (G2).
- **Regular triangulations.** The same perturbation applied to the weights gives a unique [regular triangulation](/regular-triangulation/), used in 3D mesh codes where cospherical points are common.
- **Testing.** Grids and points on one circle are the inputs where the Delaunay triangulation is not unique, so tests check the [empty circle property](/empty-circle-property/) of the output, not equality with a fixed triangulation.

## References
