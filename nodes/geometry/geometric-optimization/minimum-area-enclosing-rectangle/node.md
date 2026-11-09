---
tag: DGGM41
kind: problem
slug: minimum-area-enclosing-rectangle
name: Minimum-area enclosing rectangle
aliases:
- minimum bounding box
- smallest enclosing rectangle
- minimum-area bounding rectangle
- oriented bounding box in the plane
area: geometry/geometric-optimization
level: core
summary: Find the rectangle of smallest area, in any orientation, that contains a convex polygon or a point set. One side lies on a hull edge, so rotating calipers solve it in O(n) time.
prereqs: [convex-polygon, rotating-calipers, antipodal-pairs, support-function]
see_also: [polygon-width, polygon-diameter, minimum-enclosing-circle, minimum-area-enclosing-triangle, minimum-volume-enclosing-ellipsoid, convex-hull-problem, collision-detection, bounding-volume-hierarchy]
sources:
  - paper: doi:10.1145/360881.360919
    title: Herbert Freeman and Ruth Shapira, Determining the minimum-area encasing rectangle for an arbitrary closed curve, Communications of the ACM 18(7), 1975
    locator: the whole paper (a minimum-area enclosing rectangle has a side collinear with an edge of the convex hull, and the O(n^2) method that tries each edge)
  - paper: "Godfried T. Toussaint, Solving geometric problems with the rotating calipers, Proceedings of IEEE MELECON 1983, Athens"
    locator: the O(n) algorithm with four calipers for the minimum-area and the minimum-perimeter enclosing rectangle
  - paper: "Joseph O'Rourke, Finding minimal enclosing boxes, International Journal of Computer and Information Sciences 14(3), 1985"
    locator: the O(n^3) algorithm for the minimum-volume enclosing box in three dimensions, and the flush-face property
  - paper: "Gill Barequet and Sariel Har-Peled, Efficiently approximating the minimum-volume bounding box of a point set in three dimensions, Journal of Algorithms 38(1), 2001"
    locator: (1 + ε)-approximation of the minimum-volume box in three dimensions
---

The minimum-area enclosing rectangle of a [convex polygon](/convex-polygon/), or of a finite point set, is the rectangle of smallest area, in any orientation, that contains it. Freeman and Shapira proved in 1975 that one side of an optimal rectangle lies on an edge of the [convex hull](/convex-hull/), which reduces the search to $n$ orientations. Toussaint's four [rotating calipers](/rotating-calipers/) then visit all $n$ orientations in $O(n)$ total time. The answer is the tight oriented bounding box used in graphics, collision tests and shape analysis.

## In plain words

Draw a shape on paper and put a rectangular frame around it, as tight as possible. If the frame must stay level with the page, there is only one answer. If you may turn the frame, a turned frame is often much smaller. The question is which turn gives the smallest frame.

The answer is always a turn in which one side of the frame lies flat along one side of the shape. So you can try each side of the shape in turn. For each try you need the farthest points of the shape in four directions. When you move from one side of the shape to the next, those four points only move forward around the shape, so one trip around it is enough to try all sides.

## Definition

Notation: $P$ is the input point set or the vertex set of a convex polygon, $n = |P|$, a point is $p = (x, y)$, and $u(\theta) = (\cos \theta, \sin \theta)$. When $P$ is a convex polygon its vertices are in counterclockwise order with no three collinear.

**Input.** A finite set $P \subset \mathbb{R}^2$ with $n \ge 1$.

**Output.** An angle $\theta$ and the rectangle with sides parallel to $u(\theta)$ and $u(\theta + \pi/2)$ that contains $P$, with smallest area

$$A^* = \min_{\theta \in [0, \pi/2)} w(\theta)\, w(\theta + \pi/2), \qquad w(\theta) = \max_{p \in P} \langle u(\theta), p \rangle - \min_{p \in P} \langle u(\theta), p \rangle .$$

For a fixed $\theta$ the smallest enclosing rectangle is the product of the two directional widths, so this is the whole problem. If $P$ lies on a line, $A^* = 0$.

**Theorem (Freeman and Shapira).** If $P$ is not contained in a line, some optimal rectangle has a side that contains an edge of $\operatorname{conv} P$.

*Proof.* The four contact vertices (the extremes in directions $u(\theta)$, $u(\theta + \pi/2)$ and their opposites) stay the same on each closed interval between consecutive angles at which some caliper meets a hull edge. On such an interval, $w(\theta) = \langle u(\theta), a \rangle = |a| \cos x$ and $w(\theta + \pi/2) = |b| \cos y$, for fixed vectors $a$, $b$ between contact vertices, with $x = \theta - \alpha$ and $y = \theta + \pi/2 - \beta$, where $\alpha$, $\beta$ are the angles of $a$, $b$. Both widths are positive, so $x, y \in (-\pi/2, \pi/2)$ and $x + y \in (-\pi, \pi)$. Then

$$f(\theta) = |a||b| \cos x \cos y = \tfrac{1}{2}|a||b| \big(\cos(x + y) + \cos(x - y)\big),$$

and $x - y$ is constant, so $f'(\theta) = -|a||b| \sin(x + y)$. On the interval $x + y$ moves in $(-\pi, \pi)$, so $f'$ is positive while $x + y < 0$ and negative while $x + y > 0$: $f$ rises and then falls, and its minimum on the closed interval is at an end point. At an end point a caliper lies on a hull edge. $\square$

The same proof with $f = w(\theta) + w(\theta + \pi/2)$, a sum of two concave functions, shows that a minimum-perimeter enclosing rectangle also has a side on a hull edge.

**Exact arithmetic.** For an edge with integer vector $e$, the two side lengths are $\Delta_1 / |e|$ and $\Delta_2 / |e|$, where $\Delta_1$ is the range of $\langle e, p \rangle$ and $\Delta_2$ the range of $e \times p$ over $P$. So the area is the rational number $\Delta_1 \Delta_2 / |e|^2$, and areas can be compared exactly.

## Variants

- **Axis-parallel box.** With $\theta = 0$ fixed, the box is the range of $x$ times the range of $y$: $O(n)$ time. Its area can be arbitrarily larger than the optimum: a thin rectangle turned by 45 degrees has an axis-parallel box of almost half the square of its length.
- **Minimum perimeter.** Same flush-edge property, same $O(n)$ walk.
- **Three dimensions.** O'Rourke shows that an optimal box has two adjacent faces that each contain an edge of the hull, and his algorithm takes $O(n^3)$ time. Barequet and Har-Peled give a $(1 + \varepsilon)$-approximation in near-linear time.
- **Other enclosing shapes.** The [minimum enclosing circle](/minimum-enclosing-circle/), the [minimum-area enclosing triangle](/minimum-area-enclosing-triangle/) and the [minimum-volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/).
- **Largest inscribed rectangle.** The dual question, the largest rectangle inside a convex polygon, is a different problem.

## Examples

**The pentagon** $(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)$, one rectangle per edge:

| flush edge | squared side lengths | area |
|---|---|---|
| (0, 0) to (4, 0) | 25 and 25 | 25 |
| (4, 0) to (5, 3) | 162/5 and 128/5 | 144/5 |
| (5, 3) to (3, 5) | 32 and 32 | 32 |
| (3, 5) to (0, 4) | 162/5 and 128/5 | 144/5 |
| (0, 4) to (0, 0) | 25 and 25 | 25 |

$A^* = 25$: the axis-parallel square $[0, 5] \times [0, 5]$. A scan of $10^5$ angles finds no smaller product.

**Not the width direction.** For $P = (0, 5), (1, 4), (7, 2), (7, 5), (2, 7)$, the five areas are $35, 24, 35, 697/29, 35$. The minimum $24$ comes from the edge $(1, 4)$ to $(7, 2)$, with squared sides $288/5$ and $10$. The [width](/polygon-width/) comes from a different edge, $(7, 5)$ to $(2, 7)$, with squared width $289/29 \approx 9.97$ against $10$, and its rectangle has area $697/29 \approx 24.03$. So the narrowest strip does not give the smallest rectangle.

**The axis-parallel trap.** The square $(1, 0), (2, 1), (1, 2), (0, 1)$ has area 2, while its axis-parallel box $[0, 2] \times [0, 2]$ has area 4.

## Known algorithms

| algorithm | time |
|---|---|
| hull, then each edge with a scan of all vertices (Freeman and Shapira 1975) | $O(n^2)$ after the hull |
| hull, then four [rotating calipers](/rotating-calipers/) (Toussaint 1983) | $O(n)$ after the hull |
| a dense set of angles | approximate only, and misses the exact optimum |

The calipers walk keeps four pointers: the vertex farthest along the edge direction, the farthest from the edge line, and the farthest against the edge direction, plus the edge itself. When the edge advances to the next hull edge, each pointer advances while the next vertex is farther in its direction, which one cross product or dot product decides. Each pointer goes around the polygon once, so the walk is $O(n)$, and with integer vertices every comparison is exact.

## Bounds

- **Convex polygon.** $\Theta(n)$: each vertex must be read, and the calipers take $O(n)$.
- **Point sets.** $O(n \log n)$ by the hull and the walk, and $O(n \log h)$ for $h$ hull vertices.
- **Quality of simple boxes.** For a convex polygon $K$, $|K| \le A^* \le 2|K|$: the lower bound is containment, and the upper bound comes from the rectangle with one side along a diameter, whose area is at most twice that of $K$.

## Reductions

- **To $n$ one-dimensional problems.** The theorem turns the problem into $n$ pairs of directional widths, one pair per hull edge.
- **To antipodal pairs.** The contacts on opposite sides of the rectangle are [antipodal pairs](/antipodal-pairs/), so the walk is the antipodal-pair walk with two more calipers at right angles.
- **To the convex hull.** Only hull vertices can touch the rectangle, so the problem for point sets reduces to the [convex hull problem](/convex-hull-problem/) plus a linear walk.

## Applications

- **Oriented bounding boxes.** A tight box makes a better first test in [collision detection](/collision-detection/) and in a [bounding volume hierarchy](/bounding-volume-hierarchy/) than an axis-parallel box.
- **Shape analysis.** The orientation and the aspect ratio of the box describe the orientation and the elongation of a shape in image processing, which was the use in Freeman and Shapira's paper.
- **Packing and cutting.** The box fixes how to turn a part before it is placed on a sheet or in a container.
- **Map labeling and GIS.** Oriented boxes summarize the extent of buildings and other features.

## References
