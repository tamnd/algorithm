---
tag: PDYSMM
kind: problem
slug: line-arrangement-construction
name: Line arrangement construction
aliases:
- arrangement-of-lines-construction
- constructing an arrangement of lines
area: geometry/intersections
level: advanced
summary: Build the full combinatorial structure of the arrangement of n lines, its vertices, edges and faces with their incidences; Θ(n^2) time is optimal and is reached by incremental zone walks.
prereqs: [line-arrangement, doubly-connected-edge-list]
see_also: [edelsbrunner-o-rourke-seidel-algorithm, bentley-ottmann-algorithm, all-segment-intersections, randomized-incremental-construction, trapezoidal-map, general-position, half-plane-intersection, euler-formula]
sources:
  - paper: doi:10.1137/0215024
    title: Herbert Edelsbrunner, Joseph O'Rourke and Raimund Seidel, Constructing arrangements of lines and hyperplanes with applications, SIAM Journal on Computing 15(2), 1986, 341-363
    locator: the O(n^2) construction for lines and O(n^d) for hyperplanes, and the applications by duality
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 8, Arrangements and Duality (Section 8.3 on the construction and the zone theorem, Sections 8.1 and 8.2 on discrepancy and duality)
  - paper: doi:10.1016/0022-0000(89)90038-x
    title: Herbert Edelsbrunner and Leonidas J. Guibas, Topologically sweeping an arrangement, Journal of Computer and System Sciences 38(1), 1989, 165-194
    locator: the topological sweep over all faces in O(n^2) time and O(n) space
  - paper: doi:10.1007/bf01934990
    title: Bernard Chazelle, Leonidas J. Guibas and D. T. Lee, The power of geometric duality, BIT 25(1), 1985, 76-90
    locator: problems on point sets solved in the dual arrangement of lines
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3), 1995, 165-185
    locator: 3SUM-hardness of deciding whether three of n points are collinear, that is whether the dual arrangement is degenerate
---

Line arrangement construction asks for the complete structure of the [arrangement](/line-arrangement/) of $n$ lines in the plane: all vertices, edges and faces, and which of them touch which. The answer is usually a [doubly connected edge list](/doubly-connected-edge-list/). A simple arrangement has $\binom{n}{2}$ vertices, $n^2$ edges and $\binom{n}{2} + n + 1$ faces, so the output has size $\Theta(n^2)$, and the [Edelsbrunner-O'Rourke-Seidel algorithm](/edelsbrunner-o-rourke-seidel-algorithm/) builds it in matching $\Theta(n^2)$ time. The problem is the base of many algorithms on point sets, which become problems on lines by point-line duality.

## In plain words

You draw many straight lines on a plane. They cut it into pieces. The task is to write down the whole map: every crossing point, every piece of line between two crossings, and every piece of the plane, with the information of which piece is next to which.

The map itself is large. Every two lines cross once, so the number of crossings grows like the square of the number of lines. A good method spends only a fixed amount of work on each item of the map. The best known method adds the lines one by one and, for each new line, looks only at the pieces of the plane that the line cuts.

## Definition

**Input.** $n$ distinct lines $\ell_i : a_i x + b_i y = c_i$ with $(a_i, b_i) \ne (0, 0)$. Parallel lines and lines through a common point are allowed.

**Output.** The arrangement $\mathcal{A}(L)$ as a planar subdivision: its vertices with their points, its edges with their end points (or a direction for the unbounded ones), its faces, and the incidences between them, for example as a doubly connected edge list clipped to a box that holds every vertex, with one face of the box for every face of $\mathcal{A}(L)$.

**Notation.** $n$ is the number of lines. For a vertex $v$, $m_v$ is the number of lines through $v$. The size of $\mathcal{A}(L)$ is $V + E + F$ with $E = n + \sum_v m_v$ and $F = 1 + n + \sum_v (m_v - 1)$, as proved on the [line arrangement](/line-arrangement/) page.

**Model.** The [real RAM](/real-ram/). With integer input every vertex is a pair of rationals, and every decision is the sign of a small polynomial, so exact computation is cheap.

## Variants

- **Hyperplane arrangements.** $n$ hyperplanes in $\mathbb{R}^d$; the output has size $\Theta(n^d)$ in the simple case and is built in $O(n^d)$ time.
- **Visit the faces, do not store them.** Report every face once with little memory: the topological sweep of Edelsbrunner and Guibas takes $O(n^2)$ time and $O(n)$ space.
- **Segments and curves.** For $n$ segments with $k$ crossings, the arrangement has size $\Theta(n + k)$; see [all segment intersections](/all-segment-intersections/).
- **Parts of the arrangement.** One face, which is a [half-plane intersection](/half-plane-intersection/) in $O(n \log n)$ time; the zone of one extra line, in $O(n)$ time after the arrangement is built; or a single level, the boundary of the region with exactly $k$ lines above.
- **Degeneracy test.** Decide whether the arrangement is simple, that is, whether three lines meet in a point or two are parallel.

## Examples

**Three lines in general position.** $y = 0$, $x = 0$ and $x + y = 1$ give $3$ vertices, $9$ edges and $7$ faces: one bounded triangle and six unbounded faces.

**Five lines with degeneracies.** For $y = 0$, $x = 0$, $y = x$, $x + y = 2$ and $y = 2$, two vertices have three lines and two lines are parallel; the arrangement has $5$ vertices, $17$ edges and $13$ faces, against $10$, $25$ and $16$ for five lines in general position. The [incremental algorithm](/edelsbrunner-o-rourke-seidel-algorithm/) page traces its construction.

**Extreme cases.** $n$ parallel lines give no vertex, $n$ edges and $n + 1$ faces. $n$ lines through one point give $1$ vertex, $2n$ edges and $2n$ faces.

## Known algorithms

| algorithm | time | space | idea |
| --- | --- | --- | --- |
| sort along lines and around vertices | $O(n^2 \log n)$ | $O(n^2)$ | compute all crossings, sort them along each line, sort the edges around each vertex; the build on the [arrangement](/line-arrangement/) page |
| [Bentley-Ottmann](/bentley-ottmann-algorithm/) sweep | $O(n^2 \log n)$ | $O(n^2)$ | sweep the $n$ lines clipped to a box as segments with $\binom{n}{2}$ crossings |
| [Edelsbrunner-O'Rourke-Seidel](/edelsbrunner-o-rourke-seidel-algorithm/) (1986) | $\Theta(n^2)$ | $\Theta(n^2)$ | insert lines one by one, walk the zone of each; the zone theorem bounds each walk by $O(n)$ |
| topological sweep (Edelsbrunner and Guibas, 1989) | $O(n^2)$ | $O(n)$ | sweep with a curve that crosses each line once; visits all faces in order |
| [randomized incremental construction](/randomized-incremental-construction/) | expected $O(n^2)$ | $O(n^2)$ | insert in random order with a [trapezoidal map](/trapezoidal-map/); more useful for segments, where it gives $O(n \log n + k)$ |

The incremental algorithm is the standard one. All of them must handle lines through common points and parallel lines; with exact predicates, these cases fit into the normal steps.

## Bounds

- **Lower bound.** $\Omega(n^2)$ time for the full structure, because a simple arrangement has $\Theta(n^2)$ vertices, edges and faces, and every output item costs at least one step.
- **Upper bound.** $O(n^2)$ time and space, by the incremental algorithm; $O(n^2)$ time and $O(n)$ working space if the faces are only visited.
- **Degeneracy.** Deciding whether three lines pass through one point is, by duality, deciding whether three of $n$ points are collinear. Gajentaan and Overmars (1995) showed that this problem is 3SUM-hard, so an $o(n^2)$ algorithm for it would give a subquadratic algorithm for 3SUM. The full construction answers it in $O(n^2)$ time.
- **Hyperplanes.** $\Theta(n^d)$ time in $\mathbb{R}^d$ for fixed $d$.

## Reductions

- **Point-line duality.** The map from the point $(p_x, p_y)$ to the line $y = p_x x - p_y$ keeps the relation "above" between a point and a line. A set of $n$ points becomes $n$ lines, and the faces of their arrangement are the classes of lines that split the points in the same way. So questions about all lines through or between the points, such as the line that leaves the fewest points on one side, become walks over the faces.
- **To segment intersection.** Clipped to a box that holds all crossings, the $n$ lines become $n$ segments with $\binom{n}{2}$ crossings in the simple case, so any algorithm for the [arrangement of segments](/all-segment-intersections/) applies; the general bounds then give $O(n^2 \log n)$ or $O(n^2)$ with the optimal methods.
- **Sorting along every line.** The edges of each line in the arrangement list its crossings in order. So the construction sorts $n$ lists of $n - 1$ numbers each; this is possible in $O(n^2)$ total only because the lists come from lines.

## Applications

- **Minimum-area triangle.** The triangle of least area with vertices among $n$ points, in $O(n^2)$ time by a walk over the dual arrangement (Chazelle, Guibas and Lee, 1985).
- **Degeneracy testing.** Whether three of $n$ points are collinear, in $O(n^2)$ time.
- **Discrepancy and ham-sandwich cuts.** De Berg et al. compute the half-plane discrepancy of a point set from its dual arrangement; the ham-sandwich cut of two point sets is found from the median levels of two arrangements.
- **Sorting points by angle around every point.** All $n$ angular orders of a set of $n$ points, in $O(n^2)$ time instead of $O(n^2 \log n)$.
- **Visibility graphs.** The visibility graph of $n$ disjoint segments in $O(n^2)$ time uses the arrangement of the dual lines of the end points.

## References
