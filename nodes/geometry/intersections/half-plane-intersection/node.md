---
tag: GQ6PG3
kind: problem
slug: half-plane-intersection
name: Half-plane intersection
aliases: [intersection-of-half-planes, intersection of n half-planes]
area: geometry/intersections
level: core
summary: Compute the convex region, possibly empty or unbounded, formed by the intersection of n closed half-planes; Θ(n log n) time is necessary and sufficient when the boundary is output in order.
prereqs: [convex-polygon, convex-set, line-representation, cross-product]
see_also: [half-plane-intersection-deque, convex-polygon-intersection, polygon-kernel, seidel-linear-programming, linear-programming-problem, convex-hull-problem, convex-hull-trick, megiddo-fixed-dimension-lp]
sources:
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the O(n log n) intersection of n half-planes by divide and conquer, and its optimality
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.4, Intersection of half-planes (the reduction from sorting and the duality with convex hulls)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 4, Section 4.2, Half-plane intersection, and Chapter 8 on duality
  - paper: doi:10.1145/322139.322142
    title: D. T. Lee and Franco P. Preparata, An optimal algorithm for finding the kernel of a polygon, Journal of the ACM 26(3), 1979, 415-421
    locator: the kernel of a polygon as a half-plane intersection in linear time
---

Half-plane intersection asks for the intersection of $n$ closed half-planes in the plane. The result is a convex region, which can be a bounded convex polygon, an unbounded convex region, a segment, a point or the empty set, and the task is to list its boundary in order. Sorting reduces to it, so it needs $\Omega(n \log n)$ time in the algebraic decision tree model, and the [sort-and-deque method](/half-plane-intersection-deque/) and the divide-and-conquer method of Shamos and Hoey reach this bound. Under point-line duality it is the [convex hull problem](/convex-hull-problem/) in disguise.

## In plain words

Each half-plane is one straight fence with a "good side". You want the region that is on the good side of every fence at the same time.

This region never has dents, because any two points that satisfy all the fences are joined by a straight path that satisfies them too. So it is a convex polygon, or it is empty, or it runs off to infinity. Many fences are useless because other fences already cut off more. The work is to find which fences really form the border, and in which order. Sorting the fences by their direction makes this a single walk.

## Definition

**Input.** $n$ closed half-planes $h_i = \{x \in \mathbb{R}^2 : \alpha_i \cdot x \le \beta_i\}$ with $\alpha_i \ne 0$, or, as on the algorithm pages of this site, a point $p_i$ and a direction $d_i$ with $h_i = \{x : \operatorname{cross}(d_i, x - p_i) \ge 0\}$, the points on or left of the directed line.

**Output.** The region $R = h_1 \cap \dots \cap h_n$, given by the boundary in counterclockwise order: the list of vertices if $R$ is a bounded polygon, a chain of vertices with two rays if $R$ is unbounded, or a mark that $R$ is empty, a point or a segment. Half-planes that do not touch the boundary in a segment of positive length are redundant and do not appear in the output.

**Notation.** $n$ is the number of half-planes and $h$ the number of edges of $R$, with $h \le n$.

**Model.** The [real RAM](/real-ram/). With integer input, every test is the sign of a polynomial of low degree in the input, and the vertices are rational, so the result can be exact with integer or `Fraction` arithmetic.

## Variants

- **Bounded version.** Assume, or force by four extra half-planes for a large box, that $R$ is bounded. Most implementations do this, since it removes the cases with rays.
- **Emptiness and feasibility.** Decide whether $R \ne \emptyset$, or find one point of $R$. This is a [linear program](/linear-programming-problem/) in two variables, solved in $O(n)$ time by [Megiddo's method](/megiddo-fixed-dimension-lp/) or in expected $O(n)$ time by [Seidel's algorithm](/seidel-linear-programming/).
- **Optimization.** Find the point of $R$ that minimizes a linear function, again a linear program.
- **Upper or lower envelope.** If all half-planes are of the form $y \ge a_i x + b_i$, the boundary is the upper envelope of $n$ lines, the structure of the [convex hull trick](/convex-hull-trick/).
- **Two convex polygons.** If the half-planes come as the edges of two convex polygons in boundary order, the intersection takes $O(n)$ time: [convex polygon intersection](/convex-polygon-intersection/).
- **Polygon kernel.** The [kernel](/polygon-kernel/) of a polygon is the intersection of the inner half-planes of its edges, found in $O(n)$ time because the edges come in boundary order.
- **Higher dimensions.** The intersection of $n$ half-spaces in $\mathbb{R}^3$ is a [convex polytope](/convex-polytope/), dual to the [3D convex hull](/convex-hull-3d/), with $O(n \log n)$ algorithms. In $\mathbb{R}^d$ the result can have $\Theta(n^{\lfloor d/2 \rfloor})$ faces.

## Examples

**Eight half-planes.** For $y \ge 0$, $y \ge 1$, $y \ge x - 2$, $x \le 4$, $x + y \le 7$, $y \le 4$, $x \ge 0$ and $x + y \ge 5$, the region is the pentagon with vertices $(4, 2), (4, 3), (3, 4), (1, 4), (7/2, 3/2)$ in counterclockwise order. The half-planes $y \ge 0$, $y \ge 1$ and $x \ge 0$ are redundant, so $n = 8$ and $h = 5$. The [sort-and-deque](/half-plane-intersection-deque/) page traces this example.

**Degenerate results.** $x \ge 0$, $x \le 0$, $y \ge 0$, $y \le 1$ give the segment from $(0, 0)$ to $(0, 1)$. $x \ge 1$ and $x \le 0$ give the empty set. $y \ge 0$ alone gives an unbounded region with no vertex.

**Many redundant half-planes.** The $n$ half-planes $x \cos \theta_j + y \sin \theta_j \le 1 + j$ for $\theta_j = 2 \pi j / n$ and the $n$ half-planes of a fixed square of side 1 around the origin give the square, so $h = 4$ and $n - 4$ half-planes are redundant.

## Known algorithms

| algorithm | time | idea |
| --- | --- | --- |
| all pairs of lines | $O(n^3)$ | test each of the $O(n^2)$ meets of two boundary lines against all $n$ half-planes, then sort the survivors around their center |
| incremental cutting | $O(n^2)$ | cut the current polygon by each new half-plane, $O(n)$ per cut |
| divide and conquer (Shamos and Hoey, 1976) | $O(n \log n)$ | split in two, solve each half, intersect two convex polygons in linear time |
| [sort and deque](/half-plane-intersection-deque/) | $O(n \log n)$, $O(n)$ after the sort | sort by angle, one pass with a [deque](/deque/) |
| duality and convex hull | $O(n \log n)$ | split into upper and lower half-planes, compute two hulls of the dual points, cut the two chains |
| output-sensitive, by duality with [Chan's algorithm](/chan-algorithm/) | $O(n \log h)$ | the hull algorithms in terms of the output size $h$ carry over |
| [Seidel](/seidel-linear-programming/), [Megiddo](/megiddo-fixed-dimension-lp/) | $O(n)$, expected or worst case | emptiness and one optimal point only |

## Bounds

- **Lower bound.** $\Omega(n \log n)$ in the algebraic decision tree model for the ordered output. Reduction from sorting: for numbers $x_1, \dots, x_n$, take the half-planes above the tangents $y \ge 2 x_i x - x_i^2$ of the parabola $y = x^2$, and the half-plane $y \le M$ for a large $M$. Every tangent gives an edge, and the edges come in the order of their slopes $2 x_i$, so the output sorts the numbers.
- **Output-sensitive bound.** $\Theta(n \log h)$ in the algebraic computation tree model, by duality with the output-sensitive [convex hull](/convex-hull-problem/) bounds.
- **Upper bounds.** $O(n \log n)$ in general; $O(n)$ when the half-planes come sorted by angle, or as the edges of a polygon in boundary order for the kernel.

## Reductions

- **Duality with convex hulls.** The duality $y = a x + b \leftrightarrow (a, -b)$ maps a point above a line to a point above the dual line. The boundary of $\bigcap \{y \ge a_i x + b_i\}$ is the upper envelope of the lines, and its edges, from left to right, correspond to the vertices of the lower hull of the dual points, from left to right. Half-planes of the form $y \le a x + b$ give the upper hull. So two hull computations and one cut of the two chains solve the problem.
- **From sorting.** The tangent construction above.
- **To linear programming.** Emptiness and optimization are linear programs in two variables, which need only $O(n)$ time; the full boundary needs $\Omega(n \log n)$.
- **Polygon intersection.** The intersection of $m$ convex polygons with $n$ edges in total is a half-plane intersection of all their edges.

## Applications

- **Polygon kernel and visibility.** The [kernel of a polygon](/polygon-kernel/), the set of points that see the whole polygon, is a half-plane intersection.
- **Voronoi cells.** The Voronoi cell of a site is the intersection of the $n - 1$ half-planes of its bisectors with the other sites.
- **Linear programming in two variables.** The whole feasible region, for display or for many objective functions.
- **Robotics and games.** The safe region of a robot that must keep away from several walls, and velocity obstacles for collision avoidance.
- **Competitive programming.** Standard tasks ask for the area of the kernel of a polygon, or for the largest circle inside a convex region, by binary search on the radius and moving each edge inward.

## References
