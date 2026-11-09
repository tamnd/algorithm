---
tag: T6VRZV
kind: algorithm
slug: slab-method-point-location
name: Slab method
aliases:
- Dobkin-Lipton slab method
- slab decomposition
- slab method point location
area: geometry/point-location
level: advanced
summary: Cut the plane into vertical slabs at each vertex x-coordinate and binary search the slab, then the segments within it.
solves: [planar-point-location, vertical-ray-shooting]
model: real-ram
complexity:
  vars: {n: the number of segments of the subdivision}
  time: {build: O(n^2) worst case, query: O(log n) worst case}
  space: {extra: Θ(n^2) worst case}
properties: {online: false, deterministic: true, recursive: false, static: true}
history:
  year: 1976
  people: [David Dobkin, Richard J. Lipton]
  note: Dobkin and Lipton described the slab decomposition in their 1976 paper on multidimensional searching problems, as the first point location method with O(log n) query time.
prereqs: [planar-point-location, vertical-ray-shooting, binary-search, orientation-test]
see_also: [sarnak-tarjan-point-location, trapezoidal-map, seidel-point-location, kirkpatrick-point-location, chazelle-monotone-point-location, sweep-line-technique, degeneracy-in-sweeps, persistent-binary-search-tree]
sources:
  - paper: doi:10.1137/0205015
    title: David Dobkin and Richard J. Lipton, Multidimensional searching problems, SIAM Journal on Computing 5(2), 1976
    locator: the slab method for planar point location (DOI to be checked)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Section 2.2.2.1, The slab method
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 6, Section 6.1, Point location and trapezoidal maps (the slab partition and its quadratic size)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, Section 38.3
---

The slab method answers [planar point location](/planar-point-location/) queries. Draw a vertical line through every vertex of the subdivision. The lines cut the plane into slabs, and inside one slab no segment starts or ends, so the segments that cross the slab are totally ordered from bottom to top. A query does two [binary searches](/binary-search/): one over the slab boundaries and one over the segments of its slab. The query takes $O(\log n)$ time in the worst case, but the slabs together can hold $\Theta(n^2)$ segment entries.

## In plain words

Think of a city map with many straight streets. Cut the map into narrow vertical strips. Each cut goes through a street corner, so inside one strip no street ends. In each strip, the streets cross it from the left side to the right side and lie one above the other, like the floors of a building.

To find where a person stands, first find the strip that contains them. The strips are in order from left to right, so this is a search in a sorted list. Then find the two streets just below and just above the person. The streets of the strip are also in order, so this is a second search in a sorted list. The two streets name the block. The drawback is the cost of the strips: a long street can cross almost every strip, so it is stored many times.

## The problem

**Notation.** $P$ is the set of vertices (segment end points), $n$ the number of segments, $p = (x, y)$ a point, and $d = 2$ the dimension. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$: positive when $p, q, r$ turn counterclockwise. The output size $h$ of a query is $1$. The in-circle predicate $\mathrm{incircle}$ is not used.

The input is a set $S$ of $n$ segments in the plane with integer or rational end points. Two segments may share an end point, and otherwise they are disjoint. This is a [planar subdivision](/planar-subdivision/) given by its edges. Vertical segments, several end points with one $x$, and query points on edges or vertices are all allowed.

A query point $q$ gets one of three answers: the vertex $q$ if $q$ is an end point, the segment that contains $q$ in its relative interior, or the face that contains $q$, named by the segments hit by the upward and the downward vertical rays from $q$ (each possibly none). This is [vertical ray shooting](/vertical-ray-shooting/), and the face follows from the segment above $q$ by one pointer in a [doubly connected edge list](/doubly-connected-edge-list/).

**Degenerate input.** All comparisons use a symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$ for an infinitely small $\varepsilon > 0$. The shear has determinant $1$, so $\mathrm{orient}$ does not change. After the shear, point $p$ lies to the left of point $q$ exactly when $(p_x, p_y) < (q_x, q_y)$ in lexicographic order, so no two vertices have the same $x$ and no segment is vertical. The algorithm compares points as pairs in lexicographic order and never computes $\varepsilon$. This is the method of de Berg et al., Section 6.3; see also [degeneracy in sweeps](/degeneracy-in-sweeps/).

## The algorithm

Each segment $s = (a, b)$ is stored with $a <_{\mathrm{lex}} b$. Segment $s$ *spans* the open interval $(u, v)$ of lexicographic order if $a \le_{\mathrm{lex}} u$ and $v \le_{\mathrm{lex}} b$.

```pseudo id=main
SLAB-BUILD(S)
L1  X[0 .. m−1] ← the distinct end points of S, in lexicographic order
L2  for i ← 0 to m − 2 do
L3      L[i] ← the segments that span (X[i], X[i+1]), sorted from bottom to top
SLAB-QUERY(q)
L4  if q = X[j] for some j then return the vertex X[j]
L5  find i with X[i] < q < X[i+1]; if there is none then return the face with no segment above or below
L6  binary search L[i] for k = the number of segments s = (a, b) with orient(a, b, q) > 0
L7  if a probed segment has orient(a, b, q) = 0 then return that segment
L8  return the face between L[i][k−1] (below) and L[i][k] (above)
```

- **Line L1** sorts the vertices in the sheared $x$-order. The slab $i$ is the open strip between the sheared vertical lines through $X[i]$ and $X[i+1]$.
- **Line L3** is a sweep from left to right. At $X[i]$, the segments that end at $X[i]$ leave the active list, and then the segments that start at $X[i]$ enter it at the place found by binary search. The order of two segments $s = (a, b)$ and $t = (c, d)$ that span a common slab, with $a \le_{\mathrm{lex}} c$, is the sign of $\mathrm{orient}(a, b, c)$, or of $\mathrm{orient}(a, b, d)$ when $c$ lies on $s$ (then $c = a$). A copy of the active list is the slab list $L[i]$. Each slab costs $O(n)$, so the sweep costs $O(n^2)$.
- **Line L5** is a binary search in $X$. Points left of $X[0]$ or right of $X[m-1]$ lie in the unbounded face, and no segment is above or below them.
- **Lines L6 and L7.** Inside the slab, each segment of $L[i]$ crosses the sheared vertical line through $q$, and their order on that line is the order of $L[i]$. So the test "$q$ is above $s$" is true for a prefix of $L[i]$, and binary search finds the length $k$ of that prefix. A zero orientation means that $q$ lies on the line of $s$, and since $q$ is inside the slab, also on $s$.

The code returns the triple ("face", above, below) with segment indices, which is the canonical answer shared by all the point location pages.

## Example

The subdivision has four segments: $s_0 = (0,0)(8,2)$, $s_1 = (4,6)(8,2)$, $s_2 = (0,0)(4,6)$, which bound a triangle, and $s_3 = (2,8)(10,6)$ above it. The sorted vertices are $X = [(0,0), (2,8), (4,6), (8,2), (10,6)]$, so there are four slabs.

| slab $i$ | interval | $L[i]$, bottom to top |
|---|---|---|
| 0 | $(0,0)$ to $(2,8)$ | $s_0, s_2$ |
| 1 | $(2,8)$ to $(4,6)$ | $s_0, s_2, s_3$ |
| 2 | $(4,6)$ to $(8,2)$ | $s_0, s_1, s_3$ |
| 3 | $(8,2)$ to $(10,6)$ | $s_3$ |

The slabs hold $9$ entries for $4$ segments. The query $q = (5, 3)$ lies in slab 2, since $(4,6) < (5,3) < (8,2)$.

| step | lo | hi | probe | orient(a, b, q) | decision |
|---|---|---|---|---|---|
| 1 | 0 | 3 | $s_1 = (4,6)(8,2)$ | $-8$ | $q$ below, hi ← 1 |
| 2 | 0 | 1 | $s_0 = (0,0)(8,2)$ | $14$ | $q$ above, lo ← 1 |

So $k = 1$, and $q$ lies in the face above $s_0$ and below $s_1$: the triangle. Other queries, checked by the test file:

| query | answer | reason |
|---|---|---|
| $(4, 6)$ | vertex $(4,6)$ | line L4 |
| $(6, 7)$ | edge $s_3$ | $\mathrm{orient} = 0$ in slab 2 |
| $(4, 7)$ | face, above $s_3$, below $s_1$ | same $x$ as the vertex $(4,6)$ but lexicographically larger, so slab 2 |
| $(1, 5)$ | face, above none, below $s_2$ | slab 0, above both segments |
| $(9, 4)$ | face, above $s_3$, below none | slab 3 |

## Correctness

**Theorem.** For every set $S$ of segments that meet only at shared end points and every query point $q$, SLAB-QUERY returns the vertex $q$ if $q \in P$; otherwise the segment that contains $q$, if one exists; otherwise the lowest segment above $q$ and the highest segment below $q$ in the sheared plane.

The key facts are two. First, two segments that span one slab do not cross inside it, so the order of line L3 is a total order on the slab, and the sweep keeps the invariant "the active list is the set of segments that span the next slab, in that order". Second, within a slab, every segment of $L[i]$ meets the sheared vertical line through $q$, so "$q$ lies above $s$" is monotone along $L[i]$. The full proof, with the shear argument, is in [the correctness proof](proofs/correctness/).

## Complexity

- **Build time.** Line L1 sorts $m \le 2n$ points in $O(n \log n)$. The sweep of line L3 does $O(n)$ work per slab for the deletions, the insertions and the copy, and there are $m - 1 < 2n$ slabs, so the build takes $O(n^2)$ time in the worst case on the [real RAM](/real-ram/).
- **Space.** Each slab holds at most $n$ segments, so the total is $O(n^2)$. The bound is tight: take $n/2$ long nearly horizontal segments stacked one above the other and $n/2$ short segments below them with distinct $x$. Then about $n$ slabs each hold all $n/2$ long segments, which is $\Theta(n^2)$ entries. The test file checks this family.
- **Query time.** Line L5 is one binary search over $m - 1$ slabs, and line L6 one binary search over at most $n$ segments, each step one comparison of points or one orientation test. So a query takes $O(\log n)$ time in the worst case.
- **Lower bound.** In the [algebraic decision tree](/algebraic-decision-tree/) model, any query procedure needs $\Omega(\log n)$ tests, since a subdivision with $n$ edges can have $\Theta(n)$ faces and each test has three outcomes. So the query time is optimal; see [planar point location](/planar-point-location/).

With integer coordinates of absolute value at most $M$, each orientation determinant has absolute value at most $8M^2$, so the predicates are exact in Python integers.

## Properties

- **Static.** The structure is built once. An insertion of a long segment can change $\Theta(n)$ slabs.
- **Exact.** The only predicates are lexicographic comparison and the orientation test, both exact on integers or `fractions.Fraction`.
- **Simple queries.** The query is two binary searches over arrays, with good cache behavior, which is why the slab method is still used when $n$ is small.
- **Answers vertical ray shooting directly.** The segments above and below $q$ are the neighbors of the insertion position in $L[i]$.

## Variants and improvements

- **Persistent slabs.** Consecutive slab lists differ by the segments that start or end at one vertex. [Sarnak and Tarjan](/sarnak-tarjan-point-location/) store all slab lists as versions of one persistent search tree, which cuts the space to $O(n)$ with node copying and keeps the $O(\log n)$ query.
- **Trapezoidal map.** Extend vertical lines only up to the first segment above and below each vertex. The [trapezoidal map](/trapezoidal-map/) has $O(n)$ trapezoids, and [Seidel's randomized incremental construction](/seidel-point-location/) builds a search structure for it in $O(n \log n)$ expected time.
- **Monotone chains.** The chain method of Lee and Preparata and its fractional cascading version by Edelsbrunner, Guibas and Stolfi organize the segments by separating chains instead of slabs; see [monotone point location](/chazelle-monotone-point-location/).
- **Higher dimensions.** Dobkin and Lipton apply the same idea recursively, by projection, to arrangements of hyperplanes in $d$ dimensions. The query stays logarithmic in $n$ for fixed $d$, and the space grows very fast with $d$.

## When to use it

Use the slab method for small static subdivisions, or for subdivisions where few segments cross many slabs, for example maps whose edges are short. Its query is the simplest of all $O(\log n)$ methods. For large $n$, the quadratic space rules it out: use [Sarnak and Tarjan's](/sarnak-tarjan-point-location/) persistent version, [Kirkpatrick's hierarchy](/kirkpatrick-point-location/) or the [trapezoidal map](/trapezoidal-map/), all with $O(n)$ space.

## Pitfalls

- **Slabs at equal $x$.** If line L1 keeps only distinct $x$ values, two vertices with one $x$ share a slab boundary, and a vertical segment has no slab at all. Sort the full points in lexicographic order, as line L1 does, which is the symbolic shear.
- **The comparator at shared end points.** Two segments that start at the same vertex have $\mathrm{orient}(a, b, c) = 0$ in line L3. Compare by the other end point, $\mathrm{orient}(a, b, d)$, or the insertion order is wrong.
- **Deleting before inserting.** At a vertex, remove the segments that end there before inserting those that start there. The comparator of line L3 is valid only for segments that span a common slab.
- **Floating-point slopes.** Sorting by $y$ at the slab midpoint in floating point can swap two segments that meet at a vertex. Use the orientation test with exact arithmetic, never a tolerance.
- **Query on a boundary.** A query with the $x$ of a vertex is not on a slab boundary after the shear. Locate it with lexicographic comparison in line L5, not with $x$ alone, or it is assigned to the wrong slab.

## Implementations

## History

David Dobkin and Richard Lipton described the slab decomposition in 1976, in their paper on multidimensional searching problems in the SIAM Journal on Computing. It gave the first $O(\log n)$ query time for planar point location, at the cost of $O(n^2)$ space. The question of $O(\log n)$ query time with $O(n)$ space was then solved by Lipton and Tarjan (1977, with the planar separator theorem), Kirkpatrick (1983), Edelsbrunner, Guibas and Stolfi (1986) and Sarnak and Tarjan (1986). The last of these keeps the slabs and makes them persistent.

## References
