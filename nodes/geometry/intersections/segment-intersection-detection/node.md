---
tag: DEG1N2
kind: problem
slug: segment-intersection-detection
name: Segment intersection detection
aliases: [any segments intersect, any-segment-intersection, detecting-segment-intersections, line segment intersection detection]
area: geometry/intersections
level: core
summary: Decide whether any two of n closed line segments in the plane have a common point; Θ(n log n) time is necessary and sufficient in the algebraic decision tree model.
prereqs: [segment-intersection-point, orientation-test, element-distinctness]
see_also: [shamos-hoey-algorithm, intersecting-segment-pair-search, all-segment-intersections, segment-intersection-lower-bound, polygon-simplicity-test, red-blue-intersection, sweep-line-technique, orthogonal-segment-intersection]
sources:
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the decision problem for n segments, its O(n log n) sweep and the matching lower bound
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 33, Sections 33.1 (segment intersection by cross products) and 33.2 (determining whether any pair of segments intersects)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.3, Intersection of line segments (the test and its lower bound)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Section 2.1, Line segment intersection
---

Segment intersection detection asks whether any two of $n$ closed line segments in the plane have a common point. The answer is one bit, but no algorithm on the [real RAM](/real-ram/) can find it with fewer than $\Omega(n \log n)$ operations in the algebraic decision tree model, and the [Shamos-Hoey algorithm](/shamos-hoey-algorithm/) reaches this bound with a sweep line. The test of a single pair is exact with [orientation tests](/orientation-test/), and the version that also returns a witness pair is [intersecting segment pair search](/intersecting-segment-pair-search/).

## In plain words

You have a drawing made of straight strokes. Do two strokes touch or cross anywhere? Touching at an end point counts, and so does lying on top of each other.

You can check every pair of strokes, but with many strokes that is slow. A better way moves a vertical line across the drawing and keeps the strokes that it cuts in order from bottom to top. Two strokes that meet must be next to each other in this order just before the first meeting point, so it is enough to check neighbors. This is about as fast as sorting the end points, and no method that only compares and computes with coordinates can do better.

## Definition

**Input.** A list $S = (s_1, \dots, s_n)$ of closed segments $s_i = [a_i, b_i]$ with end points in $\mathbb{R}^2$. A segment can be vertical, and it can have length zero ($a_i = b_i$). Two segments can share end points or lie on one line.

**Output.** "Yes" if there are $i \ne j$ with $s_i \cap s_j \ne \emptyset$, else "no".

**Pairwise test.** Two segments meet if and only if the [orientation](/orientation-test/) signs $\operatorname{orient}(a_i, b_i, a_j)$ and $\operatorname{orient}(a_i, b_i, b_j)$ are not both of the same non-zero sign, the same holds with the roles exchanged, and, when all four signs are zero (collinear segments), the two $x$-ranges and the two $y$-ranges overlap. The cases with a zero sign cover touching end points and T-junctions. See [segment intersection point](/segment-intersection-point/), which also computes the common point or the common segment exactly.

**Model.** Upper bounds are on the real RAM. With integer input coordinates of $b$ bits, every test is the sign of an integer of about $2b + 1$ bits, so the decision is exact without rational numbers. Lower bounds are in the [algebraic decision tree](/algebraic-decision-tree/) model.

## Variants

- **Proper crossings only.** Count only pairs whose relative interiors cross at one point. Shared end points, as at the corners of a polygon, are then allowed.
- **Witness pair.** Return two segments that meet: [intersecting segment pair search](/intersecting-segment-pair-search/). The sweep finds one with no extra cost.
- **Report or count all pairs.** See [reporting all segment intersections](/all-segment-intersections/); counting is the same problem with a number as output.
- **Two colors.** Segments are red or blue, the segments of one color do not cross each other, and the question is about red-blue pairs: [red-blue intersection](/red-blue-intersection/).
- **Polygon simplicity.** The edges of a closed polygon, where neighbors share an end point by design: [polygon simplicity test](/polygon-simplicity-test/).
- **Axis-parallel segments.** For horizontal and vertical segments, see [orthogonal segment intersection](/orthogonal-segment-intersection/).
- **Other shapes.** Shamos and Hoey also gave the $O(n \log n)$ test for $n$ circles; the same sweep works for any $x$-monotone curves for which two curves meet in $O(1)$ points.

## Examples

**Four segments.** Take $s_0 = (0,0)$-$(6,2)$, $s_1 = (1,4)$-$(7,5)$, $s_2 = (2,3)$-$(5,0)$ and $s_3 = (3,6)$-$(8,3)$. The answer is yes: $s_0$ and $s_2$ cross at $(15/4, 5/4)$, and $s_1$ and $s_3$ cross at $(119/23, 108/23)$. The [Shamos-Hoey algorithm](/shamos-hoey-algorithm/) page traces the sweep on this input; it stops at the first pair it finds.

**Degenerate pairs.** $(0,0)$-$(2,2)$ and $(2,2)$-$(3,0)$ meet at a shared end point. $(0,0)$-$(4,0)$ and $(2,0)$-$(2,3)$ meet at a T-junction. $(0,0)$-$(2,0)$ and $(1,0)$-$(5,0)$ overlap in the segment $(1,0)$-$(2,0)$. $(0,0)$-$(1,0)$ and $(2,0)$-$(3,0)$ are collinear but do not meet, so for these two the answer is no, although all four orientation signs are zero.

**No pair.** $n$ horizontal segments $(0, i)$-$(1, i)$ for $i = 1, \dots, n$ give the answer no. Every pair has to be ruled out, and the sweep does this with $O(n)$ neighbor tests after sorting.

## Known algorithms

| algorithm | time | idea |
| --- | --- | --- |
| all pairs | $\Theta(n^2)$ | the pairwise test on each of the $\binom{n}{2}$ pairs |
| [Shamos-Hoey](/shamos-hoey-algorithm/), 1976 | $\Theta(n \log n)$ | sweep line; test only segments that become neighbors in the vertical order |
| [Bentley-Ottmann](/bentley-ottmann-algorithm/), 1979, stopped at the first report | $O(n \log n)$ | the reporting sweep, which reports at its first crossing event |
| [orthogonal sweep](/orthogonal-segment-intersection-sweep/) | $O(n \log n)$ | for horizontal and vertical segments only |

The Shamos-Hoey sweep needs only the orientation test and comparisons of coordinates. It never computes an intersection point, so with integer coordinates it runs on integers of about twice the input size.

## Bounds

- **Lower bound.** $\Omega(n \log n)$ in the algebraic decision tree model, and also in the algebraic computation tree model, by reduction from [element distinctness](/element-distinctness/). See [segment intersection lower bound](/segment-intersection-lower-bound/).
- **Upper bound.** $O(n \log n)$ time and $O(n)$ space in the worst case, by the Shamos-Hoey sweep. So the problem has complexity $\Theta(n \log n)$ in these models.
- **Integer inputs.** On a word RAM with integer coordinates the lower bound does not apply, because the model allows operations such as indexing by a coordinate.

## Reductions

- **From element distinctness.** For numbers $x_1, \dots, x_n$, take the vertical segments $\{x_i\} \times [0, 1]$. Two of them meet if and only if two numbers are equal. This takes $O(n)$ time and proves the lower bound. A version of the reduction with segments that cross only properly is on the [lower bound](/segment-intersection-lower-bound/) page.
- **To reporting.** Run any reporting algorithm and stop at its first output. The [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) then takes $O(n \log n)$ time: every crossing event reports, so before its first report it handles only the at most $2n$ end point events.
- **Polygon simplicity.** A closed polygon is simple exactly when no two non-neighboring edges meet and each two neighboring edges meet only at their shared end point; this is detection with a rule for neighbors.

## Applications

- **Checking input.** Many algorithms on polygons need a [simple polygon](/simple-polygon/) as input, and a [simplicity test](/polygon-simplicity-test/) is the first step of a robust program.
- **Map data.** Before an overlay of two maps or the construction of a [planar subdivision](/planar-subdivision/), check that the edges of each map do not cross.
- **Circuit layout.** Wires on one layer of a chip must not touch.
- **Motion planning and drawing.** A path of straight pieces must not cross itself, and a straight-line drawing of a graph is planar exactly when no two edges cross away from shared end points.

## References
