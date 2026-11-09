---
tag: TGEMGN
kind: algorithm
slug: seidel-point-location
name: Seidel's randomized point location
aliases:
- randomized incremental trapezoidal map point location
- randomized incremental point location
area: geometry/point-location
level: advanced
summary: Build a trapezoidal map by randomized incremental insertion and answer queries with a search DAG.
solves: [planar-point-location, vertical-ray-shooting]
model: real-ram
complexity:
  vars: {n: the number of segments of the subdivision}
  time: {build: O(n log n) expected, query: O(log n) expected, query-with-rebuild: O(log n) worst case}
  space: {extra: O(n) expected}
properties: {online: false, deterministic: false, recursive: false, static: true}
history:
  year: 1991
  people: [Raimund Seidel]
  note: Seidel published the randomized incremental construction of trapezoidal decompositions in Computational Geometry, Theory and Applications in 1991, with point location and the triangulation of simple polygons as applications.
prereqs: [trapezoidal-map, randomized-incremental-construction, backwards-analysis, planar-point-location]
see_also: [seidel-polygon-triangulation, slab-method-point-location, sarnak-tarjan-point-location, kirkpatrick-point-location, chazelle-monotone-point-location, vertical-ray-shooting, random-permutation]
sources:
  - paper: doi:10.1016/0925-7721(91)90012-4
    title: Raimund Seidel, A simple and fast incremental randomized algorithm for computing trapezoidal decompositions and for triangulating polygons, Computational Geometry 1(1), 1991
    locator: the whole paper (DOI to be checked)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 6, Sections 6.2 (the algorithm and its expected analysis) and 6.4 (the tail estimate and the worst-case query bound)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, Section 38.3 and Table 38.3.1
  - book: isbn:9780133363630
    title: Ketan Mulmuley, Computational Geometry, An Introduction Through Randomized Algorithms, Prentice Hall, 1994
    locator: Chapter 3, Incremental algorithms (trapezoidal decompositions and their history), to be checked
---

Seidel's algorithm solves [planar point location](/planar-point-location/) by building the [trapezoidal map](/trapezoidal-map/) of the $n$ segments of the subdivision, inserting the segments one at a time in a uniformly random order. The history of the construction is a DAG that answers queries. For every input and every fixed query point, the expected query time is $O(\log n)$, the expected size of the DAG is $O(n)$, and the expected build time is $O(n \log n)$. Rebuilding with a new random order whenever the DAG is too deep makes the query time $O(\log n)$ in the worst case, with the same expected build time.

## In plain words

Put the streets of a map on the table one at a time, in an order chosen by shuffling. Each new street cuts some of the old pieces of the map into new pieces. Keep a record of every cut: "this old piece was cut by this street into an upper and a lower part". To locate a person, follow the record from the beginning: at each cut, ask which side of the street or of the corner they are on.

The shuffle is what makes this fast. A new street in a random position usually cuts only a few pieces, so the record stays small. And the piece that holds a fixed person is cut only rarely, so the person goes through few questions. A bad order, for example from the bottom street to the top, can make the record grow much faster.

## The problem

**Notation.** $P$ is the set of end points, $n$ the number of segments, $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. A query has output size $h = 1$. $H_n = 1 + 1/2 + \cdots + 1/n$. The predicate $\mathrm{incircle}$ is not used.

The input is a set $S$ of $n$ segments that meet only at shared end points, which is a [planar subdivision](/planar-subdivision/) given by its edges. A query point $q$ gets the vertex $q$, or the segment that contains $q$, or the face answer (top, bottom): the segments directly above and below $q$. This is [vertical ray shooting](/vertical-ray-shooting/).

**Degenerate input.** The symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$ of de Berg et al., Section 6.3, makes the sheared $x$-coordinates of distinct points distinct and removes vertical segments. In code, points are compared in lexicographic order and $\mathrm{orient}$ decides above and below. Vertical segments, end points with equal $x$, and query points on segments or vertices are handled by the same code.

## The algorithm

```pseudo id=main
SEIDEL-BUILD(S, L)                ▷ L is the bound on the DAG depth, or ∞
L1  repeat
L2      π ← a uniformly random permutation of S
L3      T, D ← one unbounded trapezoid, and a DAG with one leaf for it
L4      for i ← 1 to n do TM-INSERT(T, D, π(i))
L5  until the longest root-to-leaf path of D has at most L inner nodes
SEIDEL-QUERY(q)
L6  return TM-QUERY(D, q)
```

- **Line L2.** The random order is the only source of randomness. The bounds hold for every input, and do not assume random input.
- **Lines L3 and L4** are the construction of the [trapezoidal map](/trapezoidal-map/): each insertion finds the trapezoid that contains the left end point of the new segment by a search in $D$, walks along the segment through the trapezoids it crosses, replaces them, and turns their leaves into X- and Y-nodes.
- **Line L5.** With $L = \infty$ the loop runs once and the bounds are expected bounds. With $L = c \ln(n + 1)$ for a suitable constant $c$, every query takes at most $L$ steps. The longest path of the DAG bounds the search path of every query point from above, so the test is safe.
- **Line L6** descends the DAG with lexicographic comparisons at X-nodes and orientation tests at Y-nodes.

The Python implementation takes a seed, so that each run is repeatable, and an optional bound $L$.

## Example

The subdivision is the four segments $s_0 = (0,0)(8,2)$, $s_1 = (4,6)(8,2)$, $s_2 = (0,0)(4,6)$ and $s_3 = (2,8)(10,6)$, with $m = 5$ end points. Every order gives the same final map, with $1 + n + m = 10$ trapezoids, but the DAG depends on the order. The test file runs all $4! = 24$ orders.

| order | trapezoids created | longest DAG path | path of $q = (5, 3)$ |
|---|---|---|---|
| $s_0, s_3, s_1, s_2$ | 16 | 7 | 7 |
| $s_1, s_0, s_2, s_3$ | 17 | 6 | 4 |
| $s_1, s_0, s_3, s_2$ | 18 | 6 | 4 |
| average over all 24 orders | $50/3 \approx 16.7$ | $19/3 \approx 6.3$ | $17/3 \approx 5.7$ |
| proved bound on the average | $12n + 4H_n = 169/3 \approx 56.3$ | | $12 H_n = 25$ |

For $q = (5, 3)$ every order returns the face between $s_0$ (bottom) and $s_1$ (top). On a random subdivision with $n = 60$ segments on a grid, 40 random orders gave on average $329$ created trapezoids against the bound $738.7$, search paths between $8.3$ and $14.8$ for four fixed query points against the bound $12 H_{60} \approx 56.2$, and a longest DAG path between $16$ and $25$. These are observed values, not proved ones.

## Correctness

**Theorem.** For every set $S$ of segments that meet only at shared end points, every order $\pi$ and every query point $q$, SEIDEL-QUERY returns the vertex $q$, the segment that contains $q$, or the segments directly above and below $q$ in the sheared plane. If line L5 ends, every query visits at most $L$ inner nodes.

The order only affects the cost. The correctness is the invariant of the [trapezoidal map](/trapezoidal-map/proofs/correctness/): after each insertion, the records are the faces of the trapezoidal map with correct neighbors, and the region of the leaf of each face in $D$ is that face. Seidel's contribution is the analysis of the random order. The full proof is in [the correctness proof](proofs/correctness/), and the probabilistic analysis in [the complexity proof](proofs/complexity/).

## Complexity

All bounds are on the [real RAM](/real-ram/), and "expected" is over the random order only, for any fixed input and any fixed query point.

- **Space.** The map has $1 + n + m \le 3n + 1$ trapezoids in the worst case. By [backwards analysis](/backwards-analysis/), each trapezoid of the map of the first $i$ segments is destroyed by removing the last one with probability at most $4/i$, so step $i$ creates at most $4(3i+1)/i = 12 + 4/i$ trapezoids in expectation. In total at most $12n + 4H_n$ trapezoids are created, and the DAG has $O(n)$ expected size.
- **Query.** The search path of a fixed point gains at most $3$ nodes in step $i$, and only when the trapezoid that contains the point is new, which has probability at most $4/i$. So its expected length is at most $12 H_n = O(\log n)$.
- **Build.** The search for the left end point in step $i$ costs $O(\log i)$ expected, and the rest of the step costs $O(1)$ expected, so the build takes $O(n \log n)$ expected time.
- **Worst-case query.** de Berg et al. (Section 6.4) prove a tail bound: for $\lambda > 0$, the search path of a fixed point has more than $3 \lambda \ln(n+1)$ nodes with probability at most $1 / (n+1)^{\lambda \ln 1.25 - 1}$. The plane splits into $O(n^2)$ cells whose points have the same search path, and a union bound over the cells gives the bound $2 / (n+1)^{\lambda \ln 1.25 - 3}$ for the longest search path. For a large constant $\lambda$ this is less than $1/2$, so the expected number of rounds of line L5 is at most $2$, and the query time becomes $O(\log n)$ in the worst case, with $O(n \log n)$ expected build time. The code tests the longest DAG path, which is at least the longest search path; the tests show that $L = \lceil 6 \ln(n+1) \rceil$ succeeds after few rounds, but this constant is only observed.
- **Bad orders.** A fixed bad order can give a DAG of size $\Theta(n^2)$ and queries of length $\Theta(n)$. The random order is essential.
- **Lower bound.** In the [algebraic decision tree](/algebraic-decision-tree/) model, every query structure needs $\Omega(\log n)$ tests in the worst case; see [planar point location](/planar-point-location/).

## Properties

- **Randomized, Las Vegas.** The answers are always correct. Only the running time and the size are random.
- **No preprocessing of the subdivision.** It needs only the segments: no triangulation, no faces, no sweep.
- **Insertions.** New segments can be inserted later with the same procedure, but the expected bounds assume that the whole sequence is in random order.
- **Exact.** It uses lexicographic comparisons and the orientation test only.

## Variants and improvements

- **Triangulating polygons.** Seidel used the same construction for [simple polygons](/simple-polygon/). Inserting the edges in random order, in $O(\log^* n)$ phases that locate the remaining end points by walking along the polygon, gives the trapezoidal decomposition in $O(n \log^* n)$ expected time and then a triangulation; see [Seidel's polygon triangulation](/seidel-polygon-triangulation/).
- **Conflict lists.** Clarkson and Shor (1989) and Mulmuley (1990) obtained the same expected bounds by keeping, for each trapezoid, the end points not yet inserted that lie in it. The history DAG of Seidel answers queries online and needs no conflict lists.
- **Rebuilding for a size bound.** Line L5 can also restart when the DAG has more than $c n$ nodes. By Markov's inequality this happens with probability at most $1/2$ for $c$ twice the expected constant, so the space becomes $O(n)$ in the worst case.
- **Optimal constants.** Seidel and Adamy (2000) found the optimal number of comparisons for planar point location in linear space, which is $\log_2 n$ plus lower-order terms of order $\sqrt{\log n}$.

## When to use it

Use it as the default practical point location structure for a static or growing set of segments. It is short to code, it uses only the input segments, and its constants are small. If the application cannot accept a randomized build or needs a proved worst-case bound without a rebuild loop, use [Sarnak and Tarjan](/sarnak-tarjan-point-location/) or [Kirkpatrick's hierarchy](/kirkpatrick-point-location/). If the subdivision is already a triangulation and queries come in batches with spatial locality, a [walk](/triangle-walk-point-location/) from the previous answer can be faster.

## Pitfalls

- **Inserting in input order.** If line L2 is skipped and the input is sorted, for example from bottom to top, the DAG grows to $\Theta(n^2)$ nodes. Always shuffle in line L2, with a fresh random permutation for each round.
- **Testing the wrong quantity in line L5.** The expected query bound is for a fixed point. A bound for all query points at once needs the tail estimate and the union bound over cells, or the test on the longest path. A test on the path of a few sample points does not bound the others.
- **Reusing a seed in the rebuild.** If line L2 uses the same seed in every round, the loop never ends once the depth test fails. Draw a new permutation from one generator that continues across rounds.
- **Treating the expected bound as worst case.** Without line L5, a single query can take $\Theta(n)$ time with small probability. Say which bound is meant.

## Implementations

## History

Kenneth Clarkson and Peter Shor (1989) introduced randomized incremental construction with conflict lists, and Ketan Mulmuley (1990) used it for trapezoidal decompositions. Raimund Seidel's 1991 paper gave the simple version with the history DAG, which needs no conflict lists and answers point location queries in $O(\log n)$ expected time, and he used it to triangulate simple polygons in $O(n \log^* n)$ expected time. The book of de Berg, van Kreveld, Overmars and Schwarzkopf (first edition 1997) gave the tail estimate and the worst-case query bound by rebuilding, and made this the textbook method for point location.

## References
