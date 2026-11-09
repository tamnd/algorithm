---
tag: RBTAEV
kind: algorithm
slug: greedy-triangulation
name: Greedy triangulation
aliases:
- Greedy edge triangulation
- shortest-edge-first triangulation
area: geometry/triangulations
level: core
summary: Repeatedly add the shortest segment that does not cross existing edges.
solves: [triangulation-of-point-set]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: O(n^3)}
  space: {extra: Θ(n^2)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1979
  people: [Peter D. Gilbert, Glenn K. Manacher, Albert L. Zobrist]
  note: The greedy rule was used for contouring and surface interpolation in the 1970s. In 1979 Gilbert gave an O(n^2 log n) implementation, and Manacher and Zobrist showed that the greedy triangulation does not always have minimum weight.
prereqs: [triangulation-of-point-set, triangulation, orientation-test]
see_also: [min-weight-triangulation, delaunay-triangulation, polygon-triangulation-dp, triangulation-counting-theorem, euclidean-minimum-spanning-tree, edge-flip, flip-graph, max-min-angle-triangulation]
sources:
  - paper: "Glenn K. Manacher and Albert L. Zobrist, Neither the greedy nor the Delaunay triangulation of a planar point set approximates the optimal triangulation, Information Processing Letters 9(1), 31 to 34 (1979)"
    locator: point sets on which the greedy and the Delaunay triangulation are far from minimum weight
  - paper: "Peter D. Gilbert, New results in planar triangulations, report R-850, Coordinated Science Laboratory, University of Illinois at Urbana-Champaign (1979)"
    locator: the O(n^2 log n) time computation of the greedy triangulation (report number to be checked)
  - paper: "Christos Levcopoulos and Drago Krznaric, The greedy triangulation can be computed from the Delaunay triangulation in linear time, Computational Geometry 14(4), 197 to 220 (1999)"
    locator: the O(n log n) algorithm through the Delaunay triangulation
  - paper: "Christos Levcopoulos, An Ω(n^(1/2)) lower bound for the nonoptimality of the greedy triangulation, Information Processing Letters 25(4), 247 to 251 (1987)"
    locator: the lower bound on the ratio to the minimum weight (volume and pages to be checked)
  - paper: "Matthew T. Dickerson, Robert L. Scot Drysdale, Scott A. McElfresh and Emo Welzl, Fast greedy triangulation algorithms, Computational Geometry 8(2), 67 to 86 (1997)"
    locator: practical algorithms with expected O(n log n) time on uniform points
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 6, the section on triangulations (greedy and Delaunay triangulations; section number to be checked)
---

The greedy triangulation of a point set looks at all segments between pairs of points from the shortest to the longest, and keeps each segment that does not cross a segment kept before. What is left at the end is a [triangulation of the point set](/triangulation-of-point-set/), and among all triangulations it is the one whose sorted list of edge lengths is lexicographically smallest. It is a natural heuristic for the [minimum weight triangulation](/min-weight-triangulation/), but it is not always optimal, and on bad inputs it is worse by a factor that grows like $\sqrt{n}$. The direct method takes $O(n^3)$ time; with care it takes $O(n \log n)$.

## In plain words

Scatter some nails on a board and stretch rubber bands between them. Always take the shortest band you have not tried yet. If it would cross a band already on the board, throw it away; otherwise put it on. Keep going until every pair of nails has been tried. The bands then cut the board into triangles.

Short bands go first, so the result tends to have short edges. But one short band can block two others that together would have been cheaper, so the total length is not always the smallest possible.

## The problem

The input is a set $S$ of $n$ distinct points in the plane, with integer or rational coordinates. Collinear points are allowed. The output is a list of edges, pairs of indices, that triangulate the convex hull of $S$: the edges do not cross, and they cut the hull into triangles whose corners are exactly the points of $S$. If all points are collinear, the output is the path through them.

A **candidate** is a segment between two points of $S$ that contains no other point of $S$. Only candidates can be edges, since a triangulation uses every point as a vertex. Two candidates **cross** if they share no end point and meet. $|pq|^2$ is the squared length, which is exact for integer input.

## The algorithm

```pseudo id=main
GREEDY-TRIANGULATION(S)
L1  C ← the pairs {p, q} ⊆ S with no other point of S on the segment pq
L2  sort C by |pq|^2, breaking ties by the index pair
L3  E ← empty list
L4  for each candidate pq in C, in sorted order do
L5      if pq crosses no edge of E then
L6          append pq to E
L7  return E
```

- **Line L1** drops pairs with a point in between. Without it, the collinear points $(0,0), (1,0), (2,0)$ would yield the long segment from $(0,0)$ to $(2,0)$, which is not an edge of any triangulation.
- **Line L2** compares squared lengths, so no square roots are needed and the order is exact. The tie rule makes the result unique.
- **Line L5** is the only geometric test: two candidates with distinct end points cross exactly when each separates the end points of the other, which takes four [orientation tests](/orientation-test/).
- **The result.** Line L6 never adds a crossing, and a rejected candidate stays blocked forever, so $E$ is a maximal non-crossing set, which is a triangulation.

## Example

Take $p_0 = (0,4)$, $p_1 = (1,8)$, $p_2 = (3,0)$, $p_3 = (1,7)$, $p_4 = (6,0)$. The hull is $p_0 p_2 p_4 p_1$ and $p_3$ is inside, so $n = 5$, $h = 4$, and every triangulation has $3n - h - 3 = 8$ edges and $2n - h - 2 = 4$ triangles. The ten candidates in sorted order:

| candidate | $\lvert pq \rvert^2$ | decision |
|---|---|---|
| $p_1 p_3$ | 1 | add |
| $p_2 p_4$ | 9 | add |
| $p_0 p_3$ | 10 | add |
| $p_0 p_1$ | 17 | add |
| $p_0 p_2$ | 25 | add |
| $p_0 p_4$ | 52 | add |
| $p_2 p_3$ | 53 | reject, crosses $p_0 p_4$ |
| $p_1 p_2$ | 68 | reject, crosses $p_0 p_4$ |
| $p_3 p_4$ | 74 | add |
| $p_1 p_4$ | 89 | add |

The greedy triangulation has the triangles $p_0 p_2 p_4$, $p_0 p_4 p_3$, $p_3 p_4 p_1$, $p_0 p_3 p_1$. This point set has 3 triangulations in all. The triangulation with the diagonals $p_1 p_2$ and $p_2 p_3$ in place of $p_0 p_4$ and $p_3 p_4$ is lighter: $\sqrt{68} + \sqrt{53} \approx 15.53$ against $\sqrt{52} + \sqrt{74} \approx 15.81$, so the total lengths are about $41.25$ and $41.53$. The greedy rule took $p_0 p_4$ because it is shorter than $p_2 p_3$ by a hair, and that one choice blocked both cheaper edges.

## Correctness

**Theorem.** GREEDY-TRIANGULATION returns a triangulation of $S$. Its edge list, sorted by length with the tie rule, is lexicographically smallest among the sorted edge lists of all triangulations of $S$.

The proof is in [proofs/correctness.md](proofs/correctness.md). No two edges of $E$ cross, by line L5. Every rejected candidate crosses an edge that was added before it, so no candidate can be added to $E$. A maximal non-crossing set of candidates is a triangulation, because any face that is not an empty triangle could be cut by one more candidate. For the second part, compare $E$ with any triangulation $T$ at the first position where their sorted lists differ. If the edge of $T$ there were shorter, it would have been rejected for crossing an earlier greedy edge, which is also in $T$, and $T$ would contain a crossing.

## Complexity

- **Candidates.** Line L1 tests each of the $\binom{n}{2}$ pairs against the $n$ points: $O(n^3)$.
- **Sorting.** $O(n^2 \log n)$.
- **Crossing tests.** $E$ never has more than $3n - 6$ edges, and each candidate is tested against all of them: $O(n^3)$.
- **Total.** $O(n^3)$ time and $\Theta(n^2)$ space for the candidate list. The implementation follows this bound exactly.

Faster methods exist. Gilbert computed the greedy triangulation in $O(n^2 \log n)$ time. Dickerson, Drysdale, McElfresh and Welzl gave methods that run in expected $O(n \log n)$ time on uniformly random points. Levcopoulos and Krznaric showed that the greedy triangulation can be computed from the [Delaunay triangulation](/delaunay-triangulation/) in linear time, so $O(n \log n)$ suffices in the worst case.

## Properties

- **Lexicographically shortest.** No other triangulation has a smaller sorted edge length list. In particular, the greedy triangulation contains the shortest candidate.
- **Not minimum weight.** The example above has a lighter triangulation. Manacher and Zobrist gave inputs on which the ratio to the [minimum weight](/min-weight-triangulation/) is large, and Levcopoulos showed that the ratio can grow like $\sqrt{n}$; this is also the worst case.
- **Good for convex polygons.** For points in convex position, the greedy triangulation weighs at most a constant times the minimum (Levcopoulos and Lingas).
- **Exact.** All tests are signs of integer polynomials of degree 2.
- **Deterministic.** With the tie rule, the output is a function of the input.
- **Not the Delaunay triangulation.** Short edges do not ensure empty circumcircles, and the greedy triangulation can have very thin triangles.

## Variants and improvements

- **Greedy triangulation of a polygon.** Use only the diagonals of a [simple polygon](/simple-polygon/) as candidates. The same proof shows the result is a triangulation of the polygon.
- **Constrained greedy.** Put required segments into $E$ first, then run the loop. The result is a [constrained triangulation](/constrained-triangulation/).
- **Other weights.** Any total order on the candidates works for correctness. Sorting by a different weight gives a different triangulation, but only the length order has the approximation results above.
- **Quasi-greedy triangulation.** Levcopoulos and Krznaric modify the greedy rule so that the result weighs at most a constant times the minimum weight.

## When to use it

Use the greedy triangulation when short edges matter more than triangle shape, as a starting point for local improvement toward the minimum weight, and as a test case: its lexicographic property makes it easy to check against enumeration. For triangles with good angles, use the [Delaunay triangulation](/delaunay-triangulation/). For a guaranteed weight, use the [polygon dynamic program](/polygon-triangulation-dp/) on polygons, or the quasi-greedy method on point sets.

## Pitfalls

- **Segments through other points.** Without line L1, collinear points produce long edges that pass through a vertex.
- **Comparing lengths with floats.** Two lengths can be equal or nearly equal, and float square roots can order them differently on different machines. Compare squared lengths exactly and break ties by indices.
- **Crossing tests that count touching.** Two candidates that share an end point do not cross. A test that treats any contact as a crossing rejects valid edges.
- **Expecting minimum weight.** The greedy triangulation is a heuristic. It is not the optimum, and it is not within a constant factor of it in the worst case.

## Implementations

The Python version builds the candidates, sorts them by exact squared length, and keeps a plain list of accepted edges. A second function lists the triangles of the result. The tests check every output with a brute-force validator: no two edges cross, every rejected candidate crosses a chosen edge, there are $3n - h - 3$ edges and $2n - h - 2$ triangles, and the doubled triangle areas add up exactly to the doubled hull area. For up to 8 points they enumerate every triangulation and check that the greedy one has the lexicographically smallest sorted edge list. Inputs include collinear points, grids, `Fraction` coordinates and very large integers.

## History

The shortest-edge-first rule was used in the 1970s to build triangulated surfaces for contour maps. It was an early candidate for the minimum weight triangulation. Gilbert in 1979 gave an $O(n^2 \log n)$ algorithm, and in the same year Manacher and Zobrist showed that neither the greedy nor the Delaunay triangulation is always optimal. Levcopoulos proved the $\sqrt{n}$ lower bound on the ratio in 1987, and with Krznaric he later gave the linear-time reduction from the Delaunay triangulation and the quasi-greedy approximation.

## References
