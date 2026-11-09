---
tag: 6V6WVR
kind: problem
slug: polygon-width
name: Polygon width
aliases:
- minimum width of a point set
- minimum-width strip
- width of a convex polygon
area: geometry/geometric-optimization
level: core
summary: Find the narrowest strip between two parallel lines that contains a convex polygon or a point set. One line holds an edge of the hull, so rotating calipers solve it in O(n) time.
prereqs: [convex-polygon, antipodal-pairs, rotating-calipers, support-function]
see_also: [polygon-diameter, minimum-area-enclosing-rectangle, minimum-width-annulus, farthest-pair, convex-hull-problem, coreset, minimum-enclosing-circle, maximum-area-inscribed-triangle]
sources:
  - paper: doi:10.1109/34.6790
    title: Michael E. Houle and Godfried T. Toussaint, Computing the width of a set, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(5), 1988
    locator: the whole paper (the width is attained by an antipodal edge and vertex pair, the O(n) algorithm for a convex polygon, and the O(n^2) algorithm in three dimensions)
  - paper: "Godfried T. Toussaint, Solving geometric problems with the rotating calipers, Proceedings of IEEE MELECON 1983, Athens"
    locator: the width among the applications of the rotating calipers
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 4, antipodal pairs of a convex polygon
  - paper: "Pankaj K. Agarwal and Micha Sharir, Efficient randomized algorithms for some geometric optimization problems, Discrete and Computational Geometry 16, 1996"
    locator: the width of a point set in three dimensions in O(n^(3/2+ε)) expected time
---

The width of a [convex polygon](/convex-polygon/), or of a finite point set, is the smallest distance between two parallel lines that have the whole shape between them. The narrowest such strip always has one line through an edge of the [convex hull](/convex-hull/) and the other through an [antipodal](/antipodal-pairs/) vertex, so the [rotating calipers](/rotating-calipers/) find it in $O(n)$ time from the hull. The width measures how thin a shape is, and the strip is the best fit of a line in the minimax sense.

## In plain words

Push a flat shape between two parallel rulers and close them until they touch it. The gap between the rulers depends on how you turn the shape. The width is the smallest gap over all turns.

At the smallest gap, one ruler lies flat along a side of the shape, and the other touches a corner on the other side. The reason is that while both rulers touch only corners, a small turn one way or the other makes the gap smaller or keeps a side flat. So you only need to try each side of the shape as the flat side, find the farthest corner from it, and keep the smallest distance. A caliper that turns once around the shape finds all these farthest corners in one pass.

## Definition

Notation: $P$ is the input point set or the vertex set of a convex polygon, $n = |P|$, a point is $p = (x, y)$, and $u(\theta) = (\cos \theta, \sin \theta)$. When $P$ is a convex polygon, its vertices $p_0, \ldots, p_{n-1}$ are in counterclockwise order with no three collinear.

**Input.** A finite set $P$ with $n \ge 2$, or a convex polygon.

**Output.** The width

$$w(P) = \min_{\theta \in [0, \pi)} \Big( \max_{p \in P} \langle u(\theta), p \rangle - \min_{p \in P} \langle u(\theta), p \rangle \Big),$$

and a direction $\theta$ that attains it. The function inside the minimum is the *directional width* $w(\theta)$; it is the [support function](/support-function/) in direction $u$ plus the support function in direction $-u$. The width of $P$ equals the width of its hull.

**Theorem (Houle and Toussaint).** If $P$ has at least two points and is not contained in a line, the minimum is attained at a direction $u$ that is normal to an edge of $\operatorname{conv} P$. So $w(P) = \min_{e} \max_{p \in P} \mathrm{dist}(p, \text{line}(e))$ over the hull edges $e$.

*Proof.* Order the outer edge normals of the hull by angle. Between two consecutive normals (and their opposites), the maximizing vertex $p_i$ and the minimizing vertex $p_j$ stay the same, so on that closed interval $w(\theta) = \langle u(\theta), p_i - p_j \rangle = |p_i - p_j| \cos(\theta - \varphi)$, where $\varphi$ is the angle of $p_i - p_j$. Since $P$ is not in a line, $w(\theta) > 0$ everywhere, so on the interval $\theta - \varphi$ stays in $(-\pi/2, \pi/2)$, where the cosine is concave. A concave function on a closed interval attains its minimum at an end point, and the end points are edge normals. At the normal of edge $e$, the directional width is the largest distance of a point of $P$ to the line of $e$. $\square$

If all points of $P$ lie on one line, $w(P) = 0$, attained at the normal of that line. With integer input, compare squared widths $h_e^2 = (e \times (p - a))^2 / |e|^2$ as exact fractions, where $a$ is the start of edge $e$ and $e$ is its vector.

## Variants

- **Width in a fixed direction.** $w(\theta)$ for one $\theta$ is two support-function queries: $O(n)$ time, or $O(\log n)$ on a convex polygon by binary search.
- **Higher dimensions.** The width of $n$ points in $\mathbb{R}^3$ is attained by a face and a vertex or by two edges. Houle and Toussaint give $O(n^2)$ time, and Agarwal and Sharir give $O(n^{3/2 + \varepsilon})$ expected time for every $\varepsilon > 0$.
- **Minimum-width annulus.** Replace the strip by a ring between two concentric circles: the [minimum-width annulus](/minimum-width-annulus/), used to test roundness.
- **Approximate width.** A $(1 + \varepsilon)$-approximation in any fixed dimension comes from an $\varepsilon$-kernel, a kind of [coreset](/coreset/).
- **Width with outliers.** The narrowest strip that contains all but $k$ points.

## Examples

**The pentagon** $(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)$. For each edge, the farthest vertex and its squared distance to the line of the edge are

| edge | farthest vertex | squared distance |
|---|---|---|
| (0, 0) to (4, 0) | (3, 5) | 25 |
| (4, 0) to (5, 3) | (0, 4) | 128/5 |
| (5, 3) to (3, 5) | (0, 0) | 32 |
| (3, 5) to (0, 4) | (4, 0) | 128/5 |
| (0, 4) to (0, 0) | (5, 3) | 25 |

so $w(P) = 5$, attained by the horizontal and by the vertical strip. A scan of $10^5$ directions in $[0, \pi)$ finds no smaller value.

**The hexagon** $(0, 0), (4, 0), (6, 2), (6, 4), (2, 4), (0, 2)$ has squared heights $16, 18, 36$ for its three pairs of parallel edges, so $w = 4$, the gap between $y = 0$ and $y = 4$. Here the far side of the strip touches a whole edge.

**A trap.** For the triangle $(0, 0), (4, 0), (1, 3)$, the shortest side has length $\sqrt{10} \approx 3.162$ and the height over the horizontal side is 3. But the width is the height over the longest side, from $(4, 0)$ to $(1, 3)$ of length $\sqrt{18}$: twice the area divided by that side, $12 / \sqrt{18} = 2\sqrt{2} \approx 2.828$. Neither a vertex distance nor the first edge tried gives the answer.

## Known algorithms

| algorithm | input | time |
|---|---|---|
| each edge against each vertex | convex polygon | $\Theta(n^2)$ |
| [rotating calipers](/rotating-calipers/) (Houle and Toussaint 1988) | convex polygon | $\Theta(n)$ |
| hull, then calipers | $n$ points in the plane | $O(n \log n)$, or $O(n \log h)$ with $h$ hull vertices |
| Houle and Toussaint | $n$ points in $\mathbb{R}^3$ | $O(n^2)$ |
| Agarwal and Sharir (1996) | $n$ points in $\mathbb{R}^3$ | $O(n^{3/2 + \varepsilon})$ expected |

The calipers walk: for each hull edge $p_i p_{i+1}$ in order, advance a pointer $j$ while $(p_{i+1} - p_i) \times (p_{j+1} - p_j) > 0$. Then $p_j$ is the vertex farthest from the line of the edge, and the height is $(p_{i+1} - p_i) \times (p_j - p_i) / |p_{i+1} - p_i|$. The pointer moves forward only, so the walk takes $O(n)$ time. It is the same walk as for the [polygon diameter](/polygon-diameter/), with a different value at each step.

## Bounds

- **Convex polygon.** $\Theta(n)$: every vertex must be read, and the walk takes $O(n)$.
- **Point sets in the plane.** $O(n \log n)$ by the hull and the walk, and $O(n \log h)$ in output-sensitive form.
- **Relations.** $w(P) \le \operatorname{diam}(P)$, since the strip normal to a diameter direction has width $\operatorname{diam}(P)$. For points not in a line, $w(P) > 0$.

## Reductions

- **To antipodal pairs.** The theorem reduces the width to the $O(n)$ edge and vertex antipodal pairs.
- **To a minimax line fit.** The center line of the narrowest strip is the line that minimizes the largest distance to the points: the Chebyshev ($L_\infty$) line fit in the orthogonal sense.

## Applications

- **Straightness and flatness tolerance.** In metrology, the width of measured points on an edge or a face is its straightness or flatness error.
- **Robot motion.** A convex robot can pass through a straight corridor iff its width is at most the corridor width.
- **Shape description.** The ratio of width to diameter measures how elongated a shape is.
- **Packing and cutting.** The thinnest strip gives the best orientation to place a part on a narrow sheet.

## References
