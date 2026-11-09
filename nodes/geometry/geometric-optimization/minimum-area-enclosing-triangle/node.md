---
tag: 00446R
kind: problem
slug: minimum-area-enclosing-triangle
name: Minimum area enclosing triangle
aliases:
- smallest enclosing triangle
- minimum area circumscribing triangle
- minimal enclosing triangle
area: geometry/geometric-optimization
level: advanced
summary: Find the triangle of least area that contains a convex polygon. Each side's midpoint touches the polygon, one side is flush with an edge, and O(n) time suffices.
prereqs: [convex-polygon, convex-hull, rotating-calipers]
see_also: [minimum-area-enclosing-rectangle, maximum-area-inscribed-triangle, minimum-enclosing-circle, minimum-volume-enclosing-ellipsoid, polygon-width, polygon-diameter, antipodal-pairs, two-pointers]
sources:
  - paper: "Victor Klee and Michael C. Laskowski, Finding the smallest triangles containing a given convex polygon, Journal of Algorithms 6(3), 1985"
    locator: the midpoint property of locally minimal triangles, the flush side, and the O(n log^2 n) algorithm
  - paper: "Joseph O'Rourke, Alok Aggarwal, Sanjeev Maddila and Michael Baldwin, An optimal algorithm for finding minimal enclosing triangles, Journal of Algorithms 7(2), 1986"
    locator: the O(n) algorithm that moves the flush side around the polygon while the other two sides advance monotonically
  - paper: "Ovidiu Pârvu and David Gilbert, Implementation of linear minimum area enclosing triangle algorithm, Computational and Applied Mathematics 35, 2016"
    locator: a complete description and implementation of the linear algorithm, with the cases left implicit in the 1986 paper
  - paper: "Alok Aggarwal, J. S. Chang and Chee K. Yap, Minimum area circumscribing polygons, The Visual Computer 1(2), 1985"
    locator: the generalization to enclosing k-gons of minimum area
  - paper: "Wilhelm Gross, Über affine Geometrie XIII: Eine Minimumeigenschaft der Ellipse und des Ellipsoids, Berichte über die Verhandlungen der Sächsischen Akademie der Wissenschaften zu Leipzig, Mathematisch-Physische Klasse 70, 1918"
    locator: the bound that every plane convex body lies in a triangle of at most twice its area
---

The minimum area enclosing triangle problem asks for the triangle of least area that contains a given [convex polygon](/convex-polygon/) with $n$ vertices, or the [convex hull](/convex-hull/) of a point set. Klee and Laskowski (1985) proved two structural facts: the midpoint of every side of an optimal triangle touches the polygon, and at least one side is flush with a polygon edge. They gave an $O(n \log^2 n)$ algorithm, and O'Rourke, Aggarwal, Maddila and Baldwin (1986) improved it to $O(n)$ by moving the flush side once around the polygon while the other two sides advance in the same direction, in the style of [rotating calipers](/rotating-calipers/). It is the triangular counterpart of the [minimum area enclosing rectangle](/minimum-area-enclosing-rectangle/).

## In plain words

You have a convex shape, such as a piece of card, and want to wrap it in the smallest possible triangle.

The best triangle has two simple signs. Each of its three sides touches the shape at the middle of that side. If a side touched it off-center, you could tilt that side around the touching point and save more area at one end than you add at the other. Also, at least one side lies along a whole edge of the shape.

So you can slide one side around the shape from edge to edge and, for each edge, adjust the other two sides until their middles touch. The best of these triangles wins. Because the other sides only move forward as the first side goes around, the whole search takes one pass.

## Definition

Notation: $K$ is a convex polygon with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order and positive area, and $w$ is its width. A triangle $T$ *encloses* $K$ if $K \subseteq T$. For a non-convex polygon or a point set, $K$ is its convex hull, since a triangle is convex.

**Input.** $K$, given by its vertices in order, with exact coordinates.

**Output.** A triangle $T^*$ with $K \subseteq T^*$ and the least area $A^*$.

**Theorem (Klee and Laskowski 1985).** (a) An optimal triangle exists. (b) If $T$ is a locally minimal enclosing triangle, the midpoint of each side of $T$ lies in $K$. (c) Some optimal triangle has a side that contains an edge of $K$.

*Why (a) holds.* Every height of an enclosing triangle is at least $w$, so with $A = \mathrm{area}(K)$ a triangle of area at most $2A$ has every side at most $4A/w$. Such triangles that contain $K$ form a compact set, and area is continuous on it.

*Why (b) holds.* Every side of $T$ touches $K$, or a parallel shift of that side would shrink $T$. Let $AB$ be a side, let $c$ be a point where it touches $K$, and turn the line of $AB$ about $c$ by a small angle $\theta$, with the other two sides fixed. The triangle loses a thin triangle with apex $c$ at one end and gains one at the other. Their areas are $\frac{1}{2}|cA|^2\theta$ and $\frac{1}{2}|cB|^2\theta$ up to $O(\theta^2)$, so the area changes by $\pm\frac{1}{2}\theta(|cA|^2 - |cB|^2) + O(\theta^2)$. If the side touches $K$ in a segment $[p, q]$ with $p$ nearer to $A$, the line may turn about $q$ so that the end near $B$ moves inward, and about $p$ so that the end near $A$ moves inward, without cutting $K$. If the midpoint of $AB$ lies beyond $q$, then $|qB| > |qA|$ and turning about $q$ reduces the area; beyond $p$ is symmetric. A single touching point is the case $p = q$. So at a local minimum the midpoint lies in $[p, q]$, hence in $K$.

For (c) see Klee and Laskowski, and O'Rourke et al.

**Degeneracies.** The optimal triangle need not be unique. For the unit square, every triangle with apex $(x_0, 2)$, $0 \le x_0 \le 1$, base on $y = 0$, and sides through $(0,1)$ and $(1,1)$ has area 2 and is optimal. Collinear vertices of $K$ may be removed first. If $K$ is itself a triangle, $T^* = K$.

## Variants

- **Enclosing $k$-gons.** The least area convex $k$-gon that contains $K$; Aggarwal, Chang and Yap (1985) gave a polynomial algorithm, and later work improved it.
- **Least perimeter.** Minimize the perimeter instead of the area; the optimality conditions change.
- **Triangles of a given shape.** Enclose $K$ in the smallest triangle similar to a given one. The free parameters are the scale, the rotation and two translations.
- **Inscribed triangle.** The largest triangle inside $K$, the [maximum area inscribed triangle](/maximum-area-inscribed-triangle/), whose vertices are vertices of $K$.
- **Simplices in higher dimensions.** The least volume simplex that contains a point set in $\mathbb{R}^d$, a harder problem studied for spectral unmixing.
- **Other enclosing shapes.** The [minimum area enclosing rectangle](/minimum-area-enclosing-rectangle/), the [minimum enclosing circle](/minimum-enclosing-circle/), and the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/).

## Examples

| polygon $K$ | area of $K$ | an optimal triangle | $A^*$ | ratio |
|---|---|---|---|---|
| unit square $(0,0), (1,0), (1,1), (0,1)$ | 1 | $(0,0), (2,0), (0,2)$ | 2 | 2 |
| regular hexagon with side 1 | $3\sqrt{3}/2$ | the equilateral triangle of side 3 made by three alternate edges | $9\sqrt{3}/4$ | $3/2$ |
| pentagon $(0,0), (4,0), (5,2), (3,4), (0,3)$ | $31/2$ | $(-1,0), (7,0), (1,6)$ | 24 | $48/31 \approx 1.548$ |

For the square, the side from $(2,0)$ to $(0,2)$ has midpoint $(1,1)$, a corner of the square, and the other two sides contain whole edges with midpoints $(1,0)$ and $(0,1)$. For the pentagon, the side on $y = 0$ has midpoint $(3,0)$ on the edge from $(0,0)$ to $(4,0)$. The side on $x + y = 7$ has midpoint $(4,3)$ on the edge from $(5,2)$ to $(3,4)$. The side from $(-1,0)$ to $(1,6)$ has midpoint $(0,3)$, a vertex. So all three midpoints touch, two sides are flush, and the area is $\frac{1}{2} \cdot 8 \cdot 6 = 24$. A numerical search over all flush edges and the directions of the other two sides finds no smaller triangle.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| each edge as the flush side, then the other two sides | $O(n^2)$ | uses (b) and (c); for each edge the other two contact points are found by a scan |
| Klee and Laskowski (1985) | $O(n \log^2 n)$ | (b) and (c) with nested binary searches |
| O'Rourke, Aggarwal, Maddila and Baldwin (1986) | $O(n)$ | the flush side goes once around $K$; the contact points of the other two sides only move forward, as with [two pointers](/two-pointers/) |
| for a point set | $O(n \log n)$ | [convex hull](/convex-hull/) first, then the linear algorithm |

The $O(n)$ algorithm is a case of the rotating calipers pattern: three supporting lines move around $K$ together, and each contact point advances monotonically. Its case analysis, where a side stops being flush and starts to touch at a vertex only, is delicate. Pârvu and Gilbert (2016) wrote it out in full with an implementation.

## Bounds

- **Time.** $\Theta(n)$ for a convex polygon given in order. An algorithm must read every vertex, because moving one vertex outward can change the answer.
- **Area ratio.** $\mathrm{area}(K) \le A^* \le 2\,\mathrm{area}(K)$. The upper bound, credited to Gross (1918), is reached by every parallelogram; the lower bound by every triangle. A weaker bound follows from (b): the three side midpoints lie in $K$, so by convexity $K$ contains the medial triangle, whose area is $A^*/4$, hence $A^* \le 4\,\mathrm{area}(K)$.
- **Disk.** For a disk of radius $r$, the optimal triangle is equilateral with area $3\sqrt{3}\, r^2$, which is $3\sqrt{3}/\pi \approx 1.654$ times the disk.

## Reductions

- **Point set to polygon.** Only the convex hull matters, because triangles are convex.
- **Fixed flush edge.** With one side fixed on an edge of $K$, the other two sides are supporting lines of $K$, and the midpoint conditions locate their contact points on the boundary of $K$.
- **Affine invariance.** An invertible affine map multiplies all areas by the same factor and maps triangles to triangles, so it maps optimal triangles to optimal triangles. One may normalize $K$ first.

## Applications

- **Cutting stock.** Cutting a convex part from triangular stock with the least waste.
- **Shape description.** The ratio $A^*/\mathrm{area}(K)$, between 1 and 2, measures how close a shape is to a triangle.
- **Bounding shapes.** A triangle with three edges is a cheap bound for intersection tests on convex shapes.
- **Mixtures.** If each data point is a mix of three pure components, the data lie in a triangle, and a minimal enclosing triangle estimates the three components. The higher dimensional form uses simplices.

## References
