---
tag: E3H34D
kind: problem
slug: all-segment-intersections
name: Reporting all segment intersections
aliases: [all intersections of segments, line segment intersection reporting, segment-intersection-reporting]
area: geometry/intersections
level: core
summary: Report every intersection point of n segments with the segments through it, or every intersecting pair; the optimal bound is Θ(n log n + k) for output size k.
prereqs: [segment-intersection-detection, segment-intersection-point]
see_also: [bentley-ottmann-algorithm, chazelle-edelsbrunner-algorithm, red-blue-intersection, orthogonal-segment-intersection, line-arrangement, randomized-incremental-construction, trapezoidal-map, doubly-connected-edge-list]
sources:
  - paper: doi:10.1109/TC.1979.1675432
    title: Jon L. Bentley and Thomas A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9), 1979, 643-647
    locator: the reporting sweep in O((n + k) log n) time
  - paper: doi:10.1145/147508.147511
    title: Bernard Chazelle and Herbert Edelsbrunner, An optimal algorithm for intersecting line segments in the plane, Journal of the ACM 39(1), 1992, 1-54
    locator: the deterministic O(n log n + k) time and O(n + k) space algorithm, and the Ω(n log n + k) lower bound
  - paper: doi:10.1145/220279.220302
    title: Ivan J. Balaban, An optimal algorithm for finding segments intersections, Proceedings of the 11th Annual Symposium on Computational Geometry (SoCG 1995), 211-219
    locator: the deterministic O(n log n + k) time algorithm in O(n) space
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4(5), 1989, 387-421
    locator: the randomized incremental trapezoidal decomposition that reports all intersections in O(n log n + k) expected time
  - paper: doi:10.1016/s0747-7171(08)80064-8
    title: Ketan Mulmuley, A fast planar partition algorithm, I, Journal of Symbolic Computation 10(3-4), 1990, 253-280
    locator: the randomized O(n log n + k) expected time construction of the partition induced by segments
  - paper: doi:10.1016/0022-0000(86)90025-5
    title: Bernard Chazelle, Reporting and counting segment intersections, Journal of Computer and System Sciences 32(2), 1986, 156-182
    locator: reporting in O(n log^2 n / log log n + k) time and the first subquadratic counting algorithm
  - paper: doi:10.1137/0220029
    title: János Pach and Micha Sharir, On vertical visibility in arrangements of segments and the queue size in the Bentley-Ottmann line sweeping algorithm, SIAM Journal on Computing 20(3), 1991, 460-470
    locator: the size of the event queue of the sweep
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Section 2.1, Line segment intersection (the sweep, its degenerate cases and the O((n + I) log n) bound)
---

Reporting all segment intersections asks for every point where two or more of $n$ given segments meet, or for every pair of segments that meet. The output can have $k = \Theta(n^2)$ items, so a good algorithm is output-sensitive: its time depends on $n$ and $k$. The classic [Bentley-Ottmann sweep](/bentley-ottmann-algorithm/) takes $O((n + k) \log n)$ time, and the optimal bound $\Theta(n \log n + k)$ was reached by the deterministic [Chazelle-Edelsbrunner algorithm](/chazelle-edelsbrunner-algorithm/), by the randomized methods of Clarkson and Shor and of Mulmuley, and in linear space by Balaban.

## In plain words

You have a drawing made of straight strokes, and you want a list of all the places where strokes touch or cross, with the strokes at each place. Some drawings have no crossings at all, and some have a crossing for almost every pair of strokes.

Checking every pair always costs about the square of the number of strokes, even when there are no crossings. The good methods spend a small amount of work for each stroke, about the cost of sorting, plus a small amount for each crossing they report. A sweep line that moves across the drawing and stops at every end point and every crossing does this, with an extra factor for its search structure on each crossing. The best methods remove even this factor.

## Definition

**Input.** A list $S = (s_0, \dots, s_{n-1})$ of closed segments in the plane. Vertical segments, segments of length zero, shared end points, several segments through one point and collinear overlaps are allowed.

**Output, point form.** Every point $p$ that lies on at least two segments, with the set $S(p)$ of the segments through $p$. If two segments overlap in a segment, the convention of this site reports the end points of the overlap, which are where the overlap starts and stops; another common convention reports the overlap as a segment.

**Output, pair form.** Every pair $\{i, j\}$ with $s_i \cap s_j \ne \emptyset$.

**Notation.** $n$ is the number of segments, $I$ the number of intersection points and $K$ the number of intersecting pairs. Without overlaps, $I \le K \le \binom{n}{2}$, and a point on $m$ segments adds 1 to $I$ and $\binom{m}{2}$ to $K$. A bound written with $k$ uses the size of the output of the form at hand.

**Model.** Algorithms run on the [real RAM](/real-ram/). With integer input, every test is exact with integers, and the intersection points are rational, with a numerator of about $3b$ bits and a denominator of about $2b$ bits for $b$-bit input; the [segment intersection point](/segment-intersection-point/) page computes them as fractions.

## Variants

- **Detection.** Is the output empty? See [segment intersection detection](/segment-intersection-detection/) and [intersecting segment pair search](/intersecting-segment-pair-search/).
- **Counting.** Compute $K$ only. This is easier than reporting when $K$ is large: Chazelle (1986) gave the first $o(n^2)$ method, and with cuttings the bound is about $n^{4/3}$ up to polylogarithmic factors.
- **Red-blue intersection.** Two sets of segments, each without crossings inside it: report the red-blue pairs. See [red-blue intersection](/red-blue-intersection/), which has simpler optimal algorithms.
- **Orthogonal segments.** Horizontal against vertical segments, in $\Theta(n \log n + k)$ time with a simple sweep: [orthogonal segment intersection](/orthogonal-segment-intersection/).
- **Lines instead of segments.** All $\binom{n}{2}$ pairs of non-parallel lines meet, and the interesting output is the [arrangement](/line-arrangement/) of the lines.
- **The induced subdivision.** Build the [planar subdivision](/planar-subdivision/) cut out by the segments, as a [DCEL](/doubly-connected-edge-list/) or a [trapezoidal map](/trapezoidal-map/). This is the map overlay of geographic systems, and its size is $O(n + I)$.
- **Curves.** The sweep extends to $x$-monotone curve pieces that meet in $O(1)$ points per pair, such as circular arcs.

## Examples

**Five segments.** Take $s_0 = (0,0)$-$(6,6)$, $s_1 = (0,6)$-$(6,0)$, $s_2 = (0,3)$-$(6,3)$, $s_3 = (1,0)$-$(5,4)$ and the vertical $s_4 = (4,0)$-$(4,6)$. The point form of the output is

| point | segments through it |
| --- | --- |
| $(3, 3)$ | $s_0, s_1, s_2$ |
| $(7/2, 5/2)$ | $s_1, s_3$ |
| $(4, 2)$ | $s_1, s_4$ |
| $(4, 3)$ | $s_2, s_3, s_4$ |
| $(4, 4)$ | $s_0, s_4$ |

so $I = 5$ and $K = 3 + 1 + 1 + 3 + 1 = 9$. Two points lie on three segments; for example $s_3$ passes through $(4, 3) = (1, 0) + 3 \cdot (1, 1)$, where it meets $s_2$ and $s_4$. The [Bentley-Ottmann](/bentley-ottmann-algorithm/) page traces the sweep on this input.

**Quadratic output.** $n/2$ long segments of slope $1$ and $n/2$ of slope $-1$ that all cross one square give $K = n^2/4$ proper crossings, so any reporting algorithm needs $\Omega(n^2)$ time on this input.

**Empty output.** $n$ disjoint horizontal segments give $k = 0$. An output-sensitive algorithm takes $O(n \log n)$ time here, while the test of all pairs takes $\Theta(n^2)$.

## Known algorithms

| algorithm | time | space | notes |
| --- | --- | --- | --- |
| all pairs | $\Theta(n^2)$ | $O(1)$ extra | optimal when $k = \Theta(n^2)$ |
| [Bentley-Ottmann](/bentley-ottmann-algorithm/), 1979 | $O((n + I) \log n)$ | $O(n + I)$, or $O(n)$ with Brown's change | sweep line; crossings become events |
| Chazelle, 1986 | $O(n \log^2 n / \log \log n + K)$ | $O(n + K)$ | first algorithm with a linear term in $K$ |
| [Chazelle-Edelsbrunner](/chazelle-edelsbrunner-algorithm/), 1988 and 1992 | $O(n \log n + K)$ | $O(n + K)$ | deterministic and optimal; builds the vertical map of the segments |
| Clarkson-Shor, 1989 | $O(n \log n + I)$ expected | $O(n + I)$ | randomized incremental [trapezoidal map](/trapezoidal-map/) |
| Mulmuley, 1988 and 1990 | $O(n \log n + I)$ expected | $O(n + I)$ | randomized incremental partition |
| Balaban, 1995 | $O(n \log n + K)$ | $O(n)$ | deterministic, optimal in time and space |

The randomized incremental method is the one usually taught: insert the segments in a random order into a [trapezoidal map](/trapezoidal-map/), and by [backwards analysis](/backwards-analysis/) the expected total work is $O(n \log n + I)$. It is described on the [randomized incremental construction](/randomized-incremental-construction/) page.

## Bounds

- **Lower bound.** $\Omega(n \log n + k)$ in the algebraic decision tree model: $\Omega(k)$ to write the output, and $\Omega(n \log n)$ because the case $k = 0$ is [detection](/segment-intersection-detection/). Chazelle and Edelsbrunner prove the combined bound.
- **Upper bound.** $O(n \log n + k)$ time, reached by the algorithms in the table, and in $O(n)$ space by Balaban.
- **The extra factor of the sweep.** The Bentley-Ottmann bound is $\Theta((n + I) \log n)$ in the worst case. For $I = \Theta(n^2)$ it is $\Theta(n^2 \log n)$, a factor $\log n$ more than the test of all pairs.
- **Space of the sweep.** If every crossing found stays in the queue until it is processed, the queue can hold many crossings at once; Pach and Sharir (1991) studied how large it can grow. Brown's change, which removes the crossing of two segments when they stop being neighbors, keeps the queue at $O(n)$.

## Reductions

- **From detection.** Detection is the special case "is $k = 0$?", so the lower bound of [detection](/segment-intersection-detection/) carries over.
- **Red-blue as a special case.** If the input is the union of two sets without inner crossings, the reporting problem is the [red-blue problem](/red-blue-intersection/) plus the shared end points.
- **Map overlay.** The overlay of two planar subdivisions with $n$ edges in total is the subdivision of the union of their edges; computing it is reporting all red-blue intersections and then linking the pieces.
- **Arrangements.** For lines, all pairs meet unless parallel, and the arrangement has $\Theta(n^2)$ size; it is built by an incremental method in $O(n^2)$ time, see [line arrangement construction](/line-arrangement-construction/).

## Applications

- **Geographic information systems.** Overlay of maps, such as roads with rivers, to find bridges, and polygon operations on large maps.
- **Boolean operations on polygons.** [Polygon clipping](/polygon-clipping/) and [polygon union](/polygon-union/) start with all intersections of the edges of the two polygons.
- **Computer graphics and CAD.** Hidden-line removal, the cleaning of drawings and the construction of meshes from line drawings.
- **Robotics and motion planning.** The free space of a robot among polygonal obstacles is built from the intersections of their edges.

## References
