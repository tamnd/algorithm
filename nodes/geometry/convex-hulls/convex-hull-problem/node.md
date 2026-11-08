---
tag: NP0Q33
kind: problem
slug: convex-hull-problem
name: Convex hull problem
aliases:
- 2D convex hull
- computing the convex hull
- planar convex hull
area: geometry/convex-hulls
level: intro
summary: Given n points in the plane, output the vertices of their convex hull in order.
prereqs: [convex-hull, extreme-point, orientation-test]
see_also: [andrew-monotone-chain, graham-scan, jarvis-march, quickhull, chan-algorithm, convex-hull-lower-bound, convex-hull-3d, dynamic-convex-hull]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 1, Computational Geometry, Introduction (the planar convex hull problem, the brute-force edge test, the incremental upper and lower hull algorithm and degenerate cases)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, Convex hulls, basic algorithms (problem statements, lower bound, Graham, Jarvis, quickhull, divide and conquer, dynamic hulls), and Chapter 4, extensions and applications
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, 2nd edition, Cambridge University Press, 1998
    locator: Chapter 3, Convex hulls in two dimensions
  - paper: doi:10.1137/0215021
    title: David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1), 1986
    locator: the O(n log h) algorithm and the matching lower bound in terms of the output size
  - paper: doi:10.1007/BF02712873
    title: Timothy M. Chan, Optimal output-sensitive convex hull algorithms in two and three dimensions, Discrete and Computational Geometry 16(4), 1996
    locator: the planar O(n log h) algorithm by grouping and gift wrapping
  - paper: doi:10.1016/0022-0000(81)90012-X
    title: Mark H. Overmars and Jan van Leeuwen, Maintenance of configurations in the plane, Journal of Computer and System Sciences 23(2), 1981
    locator: the fully dynamic planar convex hull with O(log^2 n) time per insertion or deletion
  - paper: doi:10.1109/SFCS.2002.1181985
    title: Gerth Stølting Brodal and Riko Jacob, Dynamic planar convex hull, Proceedings of the 43rd IEEE Symposium on Foundations of Computer Science, 2002
    locator: the dynamic hull with O(log n) amortized time per update
---

The convex hull problem asks for the [convex hull](/convex-hull/) of $n$ points in the plane: list the corners of the smallest convex polygon that contains all the points, in counterclockwise order. It is the first problem of most computational geometry courses, because it has many algorithms with different trade-offs, a clean $\Omega(n \log n)$ lower bound, and an output-sensitive version whose best bound $O(n \log h)$ depends on the number $h$ of hull corners. The hull is also a building block: the diameter, the width, the smallest enclosing rectangle and collision tests of convex shapes all start from it. The 3D and $d$-dimensional versions are the [3D convex hull problem](/convex-hull-3d/).

## In plain words

You have a set of points on a sheet of paper. Hammer a nail into each point, put a rubber band around all the nails and let it snap tight. The band touches some of the nails. The problem is to name those nails in the order the band goes around them.

The answer is easy to check by eye, but a computer must find it with simple questions such as "does this point lie to the left of the line through these two points?" Some methods sort the points first and then walk along them once. Others wrap around the outside one nail at a time, which is fast when only a few nails touch the band. No method based on such questions can beat the cost of sorting when many nails touch the band.

## Definition

**Input.** A finite list $S = (p_1, \ldots, p_n)$ of points in $\mathbb{R}^2$. Points may repeat, and three or more may lie on one line. Coordinates are integers or rationals when the algorithm must be exact.

**Output.** The [extreme points](/extreme-point/) of $S$, that is, the vertices of the convex polygon $\mathrm{conv}(S)$, each listed once, in counterclockwise order around the boundary, starting at any vertex. A common convention starts at the lexicographically smallest point. If all points are on one line, the output is the two end points, and if all points are equal, the single point. The output size is $h$, the number of hull vertices, with $1 \le h \le n$.

**Model.** Algorithms are analyzed on the [real RAM](/real-ram/), with exact arithmetic on coordinates. For points with integer coordinates, all algorithms on this page need only the sign of the [orientation test](/orientation-test/) $\mathrm{orient}(a, b, c) = (b_x - a_x)(c_y - a_y) - (b_y - a_y)(c_x - a_x)$ and comparisons of coordinates, so they can be implemented exactly with integers of about twice the input word size. Lower bounds use [algebraic decision trees](/algebraic-decision-tree/) or [algebraic computation trees](/algebraic-computation-tree/).

**What counts as correct.** A list $v_1, \ldots, v_h$ is the hull if (a) every $v_i$ is a point of $S$, (b) every point of $S$ is on or to the left of each directed edge $v_i \to v_{i+1}$ (indices modulo $h$), and (c) every corner turns strictly left, $\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) > 0$. These three conditions can be checked in $O(nh)$ time with exact integers, and the tests of the hull pages use a brute-force version of them.

## Variants

- **Keeping collinear boundary points.** Some applications want all points of $S$ on the boundary, not only the corners. The algorithms change one comparison (pop on a right turn only) and need a tie rule on the first and last edge.
- **Extreme points only (EXT).** Report the set of hull vertices in any order. The [lower bound](/convex-hull-lower-bound/) for this weaker output is still $\Omega(n \log n)$, in the algebraic computation tree model.
- **Hull size.** Compute only $h$. This still needs $\Omega(n \log n)$ time in the algebraic computation tree model: for the lifted points $(x_i, x_i^2)$, $h$ is the number of distinct $x_i$, and deciding whether $h = n$ is [element distinctness](/element-distinctness/).
- **Upper and lower hull.** Compute only the part of the boundary seen from above or below, as in [Andrew's algorithm](/andrew-monotone-chain/) and the [upper and lower hull](/upper-and-lower-hull/) page. Under the duality $(a, b) \mapsto \{y = ax - b\}$, the upper hull of the points corresponds to the lower envelope of the dual lines.
- **Hull of a simple polygon.** If the input is the vertex sequence of a [simple polygon](/simple-polygon/) or a simple polyline, the [Melkman algorithm](/melkman-algorithm/) finds the hull in $O(n)$ time.
- **Online and dynamic hulls.** Points arrive one at a time and the hull must be kept up to date after each insertion, or points are also deleted. See [dynamic convex hull](/dynamic-convex-hull/).
- **Convex layers.** Peel the hull, then the hull of the rest, and so on: [convex layers](/convex-layers/).
- **Higher dimensions.** Output the facets of the hull of points in $\mathbb{R}^3$ or $\mathbb{R}^d$: the [3D convex hull problem](/convex-hull-3d/).

## Examples

**Twelve points.** For $S = \{(0,0), (6,9), (3,2), (11,5), (1,5), (9,8), (5,4), (12,0), (3,8), (8,3), (6,-2), (10,2)\}$ the hull, counterclockwise from the smallest point, is

$$(0,0),\ (6,-2),\ (12,0),\ (11,5),\ (9,8),\ (6,9),\ (3,8),\ (1,5),$$

so $n = 12$ and $h = 8$. The four points $(3,2)$, $(5,4)$, $(8,3)$ and $(10,2)$ are inside. A script confirmed this list with [Andrew's monotone chain](/andrew-monotone-chain/) and with a brute-force test that declares a point non-extreme when it lies in a triangle of three other points or strictly inside a segment between two others; the two agreed here and on 300 random small inputs with many repeated and collinear points. The [Chan algorithm](/chan-algorithm/) page traces its rounds on the same set.

**Degenerate inputs.** For $\{(0,0), (1,1), (2,2), (3,3)\}$ all points are on one line, and the output is $(0,0), (3,3)$. For $\{(0,0), (2,0), (4,0), (2,3)\}$ the hull is the triangle $(0,0), (4,0), (2,3)$; the point $(2, 0)$ is on the boundary but is not a corner. For $\{(1,1), (1,1)\}$ the output is the single point $(1, 1)$.

**Worst case for gift wrapping.** If all $n$ points are on a circle (or on the parabola $y = x^2$ with integer $x$), every point is a hull vertex, $h = n$, and the [Jarvis march](/jarvis-march/) takes $\Theta(n^2)$ time, while [Graham's scan](/graham-scan/) and Andrew's algorithm take $\Theta(n \log n)$.

## Known algorithms

All bounds are worst case on the real RAM unless marked otherwise.

| algorithm | time | idea |
| --- | --- | --- |
| brute force over triangles | $O(n^4)$ | a point is not extreme if it is in a triangle of three others |
| brute force over edges | $O(n^3)$ | $pq$ is a hull edge if all other points are on its left |
| [Jarvis march](/jarvis-march/) (gift wrapping), 1973 | $O(nh)$ | from each corner find the next one by a scan |
| [Graham's scan](/graham-scan/), 1972 | $O(n \log n)$ | [angular sort](/angular-sort/) around a pivot, then a stack |
| [Andrew's monotone chain](/andrew-monotone-chain/), 1979 | $O(n \log n)$, $O(n)$ after sorting | sort by $x$, build lower and upper hull with a stack |
| [quickhull](/quickhull/) | $O(n^2)$ worst, $O(n \log n)$ on many inputs | split by the farthest point from a line, recurse |
| [divide and conquer](/divide-and-conquer-convex-hull/) (Preparata and Hong, 1977) | $O(n \log n)$ | split by $x$, merge two hulls with two tangents |
| [Kirkpatrick-Seidel](/kirkpatrick-seidel/), 1986 | $O(n \log h)$ | find the bridge over the median by [prune and search](/prune-and-search/), recurse |
| [Chan's algorithm](/chan-algorithm/), 1996 | $O(n \log h)$ | small hulls of groups, then gift wrapping with binary search, guessing $h$ by squaring |
| [Melkman](/melkman-algorithm/), 1987 | $O(n)$ | input is a simple polyline; a deque |

For the dynamic problem, Overmars and van Leeuwen (1981) keep the hull under insertions and deletions in $O(\log^2 n)$ worst-case time per update with $O(n)$ space; Brodal and Jacob (2002) reduce the update time to $O(\log n)$ amortized. Insertions alone can be handled in $O(\log n)$ time each with a balanced search tree on the hull vertices.

## Bounds

- **Sorting lower bound.** Any algorithm that outputs the hull vertices in order needs $\Omega(n \log n)$ time in the algebraic decision tree model, because it can sort: lift numbers $x_1, \ldots, x_n$ to $(x_i, x_i^2)$, all of which are hull vertices, and read the sorted order off the hull. For the unordered output EXT the same bound holds in the algebraic computation tree model, by Ben-Or's theorem. See [convex hull lower bound](/convex-hull-lower-bound/).
- **Output-sensitive lower bound.** For each $h \le n$, computing the hull of inputs whose hull has $h$ vertices needs $\Omega(n \log h)$ time in the algebraic computation tree model (Kirkpatrick and Seidel). So the $O(n \log h)$ algorithms are optimal for every $h$. See [output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/).
- **Upper bounds.** $O(n \log n)$ in the worst case and $O(n \log h)$ in terms of the output, both reached, and $O(n)$ when the points come sorted by $x$ or as a simple polygon.
- **Random inputs.** For $n$ points drawn independently and uniformly from a convex polygon with $k$ corners, the expected hull size is $\frac{2k}{3} \ln n + O(1)$; from a disk it is $\Theta(n^{1/3})$ (Rényi and Sulanke). Then $\log h$ is much smaller than $\log n$ on average, and the output-sensitive algorithms or a simple filter that discards points inside a quadrilateral of four extreme points (the Akl-Toussaint heuristic) save most of the work. These are expected-case statements about the input distribution, not worst-case bounds.
- **Beyond the comparison models.** On a word RAM with integer coordinates, the sort in Andrew's algorithm can be replaced by an integer sort, and the hull takes the time of integer sorting. The lower bounds above do not apply to that model.

## Reductions

- **Sorting reduces to the hull.** The lifting $x \mapsto (x, x^2)$ above turns $n$ numbers into $n$ hull vertices in sorted order, in linear time. So any hull algorithm sorts, which gives the lower bound.
- **The hull reduces to sorting.** Andrew's algorithm sorts and then spends $O(n)$ time. So in the comparison-based models the two problems have the same complexity, $\Theta(n \log n)$.
- **Duality with half-plane intersection.** Under the point-line duality $(a, b) \mapsto y = ax - b$, a point lies above a line exactly when the dual point lies above the dual line. So the upper hull of points corresponds to the lower envelope of the dual lines, and the boundary of the intersection of the half-planes $y \ge a_i x - b_i$, which is the upper envelope of the lines, corresponds to the lower hull of the points $(a_i, b_i)$. See [half-plane intersection](/half-plane-intersection/).
- **Delaunay triangulation.** Lifting points to the paraboloid $z = x^2 + y^2$ turns the [Delaunay triangulation](/delaunay-triangulation/) of planar points into the lower hull of points in $\mathbb{R}^3$, a reduction to the 3D problem. See [paraboloid lifting map](/paraboloid-lifting-map/).
- **Maximal points.** The points not dominated in both coordinates are a staircase, not a hull, but the same $\Omega(n \log h)$ argument applies, and [Kung's algorithm](/kung-algorithm/) is the analogue of the hull algorithms for this problem.

## Applications

- **Diameter and farthest pair.** The two farthest points of $S$ are hull vertices, and [rotating calipers](/rotating-calipers/) find them in $O(h)$ time after the hull. See [farthest pair](/farthest-pair/) and [polygon diameter](/polygon-diameter/).
- **Width and enclosing shapes.** The [width](/polygon-width/) of a point set and the [smallest enclosing rectangle](/minimum-area-enclosing-rectangle/) depend only on the hull and are found by rotating calipers.
- **Collision detection.** Tests between convex shapes, such as the [GJK algorithm](/gjk-algorithm/), work on hulls, and many systems replace a complex object by its hull for a first quick test. See [convex collision detection](/convex-collision-detection/).
- **Linear optimization over a point set.** The maximum of a linear function over $S$ is reached at a hull vertex, and after the hull a binary search over the edge directions answers each query in $O(\log h)$ time.
- **Statistics and data summaries.** [Convex layers](/convex-layers/) order points from the outside in, which is used for robust estimates of the center of a point cloud.
- **Shape description.** The hull is the coarsest convex description of a shape; a [concave hull](/concave-hull/) gives a tighter, non-convex one.

## References
