---
tag: FFZ2TD
kind: algorithm
slug: dwyer-algorithm
name: Dwyer's algorithm
aliases:
- Dwyer's divide-and-conquer Delaunay
- strip divide and conquer
area: geometry/voronoi-and-delaunay
level: research
summary: Divide-and-conquer Delaunay construction with fast expected running time on uniformly distributed points.
solves: [delaunay-triangulation-construction]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: O(n log n), average: O(n log log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1987
  people: [Rex A. Dwyer]
  note: Dwyer changed the order of the cuts of the Guibas-Stolfi algorithm and proved an O(n log log n) average time for uniform points.
prereqs: [guibas-stolfi-algorithm, delaunay-triangulation, quad-edge-data-structure, in-circle-test]
see_also: [delaunay-triangulation-construction, fortunes-algorithm, bowyer-watson-algorithm, merge-sort, lexicographic-order, voronoi-construction-lower-bound]
sources:
  - paper: doi:10.1007/BF01840356
    title: R. A. Dwyer, A faster divide-and-conquer algorithm for constructing Delaunay triangulations, Algorithmica 2, 1987
    locator: the strip method, its O(n log n) worst case and its O(n log log n) average time for points uniform in the unit square
  - paper: doi:10.1145/282918.282923
    title: L. Guibas and J. Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 1985
    locator: the merge loop of the divide-and-conquer Delaunay algorithm, used here without change
  - paper: doi:10.1016/S0925-7721(96)00025-9
    title: P. Su and R. L. S. Drysdale, A comparison of sequential Delaunay triangulation algorithms, Computational Geometry 7, 1997
    locator: the experiments that compare Dwyer's algorithm with incremental and sweep methods
---

Dwyer's algorithm builds the [Delaunay triangulation](/delaunay-triangulation/) of $n$ points with the merge of the [Guibas-Stolfi algorithm](/guibas-stolfi-algorithm/), but in a different order. It cuts the points into about $(n / \log n)^{1/2}$ vertical strips, triangulates each strip by recursive cuts across the strip, and then merges the strips. The worst-case time stays $O(n \log n)$. For points uniform in a square, Dwyer proved an average time of $O(n \log \log n)$, because the cuts are short and each merge changes few edges.

## In plain words

The plain divide-and-conquer method always cuts the points by a vertical line. For points spread evenly in a square, the late cuts make very tall and thin pieces, and joining two thin pieces along a long line is a lot of work.

Dwyer first cuts the square into tall strips. Inside one strip he cuts across, so that the pieces stay close to square. Joining two pieces that are near squares needs only a little work along the short cut. Then he joins the strips side by side, two at a time.

The joining step is the same as in the plain method. Only the order of the cuts changes, so the result is the same triangulation.

## The problem

The input is a finite list $P$ of points $p = (x, y)$ with integer coordinates; repeats are allowed. The output is the list of triangles of a Delaunay triangulation of the distinct points of $P$, each a counterclockwise triple, or the empty list if all points lie on one line.

Notation: $n = |P|$, $h$ is the number of convex hull vertices, $k$ is the number of strips, $\prec$ is the [lexicographic order](/lexicographic-order/) on $(x, y)$, $\mathrm{orient}(a, b, c)$ is the sign of $(b - a) \times (c - a)$ (positive for a counterclockwise turn), and for counterclockwise $a, b, c$, $\mathrm{incircle}(a, b, c, d)$ is positive when $d$ is strictly inside the circle through $a, b, c$, zero on it and negative outside. BUILD and MERGE are the recursion and the merge of the Guibas-Stolfi page, on the [quad-edge structure](/quad-edge-data-structure/). The correctness proof assumes that no four points lie on one circle; collinear points are allowed, and with cocircular points the code returns one of the Delaunay triangulations.

## The algorithm

```pseudo id=main
DWYER(P)
L1  S ← the distinct points of P sorted by ≺; n ← |S|
L2  k ← about (n / log n)^(1/2), with at most n/2 strips
L3  for each of the k runs of consecutive points of S do
L4      sort the run by the key (-y, x)
L5      build its triangulation with BUILD, which now cuts by y
L6      walk its outer face to find the handles for the order ≺
L7  while more than one run is left do
L8      merge the runs in pairs, first with second, third with fourth, with MERGE
L9  return the triangles of the structure
```

- **Line L1.** Dwyer uses bucket sorting by $x$, which takes $O(n)$ average time on uniform points. The code uses a comparison sort.
- **Line L2.** Each strip has at least two points, which MERGE needs.
- **Line L3.** The code cuts the sorted list into runs of equal size. Dwyer cuts the square into strips of equal width; for uniform points the two choices give about the same strips.
- **Line L4.** The key $(-y, x)$ is the lexicographic order of the rotated point $(-y, x)$. A rotation by a quarter turn does not change the two predicates, so BUILD works without change and cuts the strip by horizontal lines.
- **Line L6.** BUILD returns handles at the top and bottom points of the strip. The walk around the hull finds the hull edges out of the leftmost and the rightmost points, which MERGE needs.
- **Line L8** is the Guibas-Stolfi merge of two neighbouring runs. A run with no partner waits for the next round.

## Example

Take $n = 8$ points and $k = 2$ strips: $A = \{(0,0), (1,4), (2,1), (3,3)\}$ and $B = \{(4,0), (5,4), (6,2), (7,5)\}$.

- Line L4 sorts $A$ as $(1,4), (3,3), (2,1), (0,0)$. BUILD cuts it into the top pair and the bottom pair, makes the edges $(1,4)$-$(3,3)$ and $(2,1)$-$(0,0)$, and merges them into the triangles $(0,0)(2,1)(1,4)$ and $(1,4)(2,1)(3,3)$.
- Strip $B$ in the same way gives $(4,0)(6,2)(5,4)$ and $(5,4)(6,2)(7,5)$.
- Line L8 merges $A$ and $B$. The lower common tangent is $(0,0)$-$(4,0)$. The merge adds the cross edges $(2,1)$-$(4,0)$, $(3,3)$-$(4,0)$, $(3,3)$-$(6,2)$, $(3,3)$-$(5,4)$, $(1,4)$-$(5,4)$ and $(1,4)$-$(7,5)$, and deletes the edge $(4,0)$-$(5,4)$ of $B$, which crosses $(3,3)$-$(6,2)$.

The result has $9$ triangles: the four triangles above, less $(4,0)(6,2)(5,4)$, plus $(0,0)(4,0)(2,1)$, $(2,1)(4,0)(3,3)$, $(3,3)(4,0)(6,2)$, $(3,3)(6,2)(5,4)$, $(1,4)(3,3)(5,4)$ and $(1,4)(5,4)(7,5)$. There are $h = 5$ hull vertices and $2n - 2 - h = 9$ triangles, as [Euler's formula](/euler-formula/) requires.

## Correctness

**Theorem.** If no four of the distinct points lie on one circle, DWYER returns the unique Delaunay triangulation of the points for every number of strips, or the empty list when they lie on one line.

The proof uses two results of the Guibas-Stolfi correctness proof: BUILD on a sorted list returns the Delaunay edges with hull handles at the two ends, and MERGE of two such structures whose point sets are separated in the order $\prec$ returns the same kind of structure for the union. The rotation $(x, y) \mapsto (-y, x)$ keeps both predicates, so the strip builds of line L5 are correct in the rotated frame, and line L6 moves the handles to the leftmost and rightmost points. The runs are consecutive in $\prec$ and have at least two points, so every merge of line L8 meets the conditions of the merge lemma. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Worst case.** Each strip costs $O(m \log m)$ for $m$ points, and each of the $\lceil \log_2 k \rceil$ rounds of line L8 costs $O(n)$. So the total is $O(n \log n)$ for every input, which is optimal by the [lower bound](/voronoi-construction-lower-bound/). This is proved in [the complexity proof](proofs/complexity/).
- **Average case.** For $n$ points independent and uniform in the unit square, with bucket sorting in line L1, Dwyer proved $O(n \log \log n)$ average time. This bound is cited, not proved on this page.
- **Observed.** On uniform random integer points the code makes about $7.8n$, $8.5n$ and $8.8n$ in-circle tests for $n = 1000$, $4000$ and $16000$, against about $16.6n$, $20.6n$ and $24.5n$ with one strip, which is the Guibas-Stolfi order.
- **Space.** $O(n)$, with deleted edge records reused.

## Properties

- **Exact.** The same two predicates as Guibas-Stolfi, on integers.
- **Deterministic.** The average bound is over the input distribution, not over random choices of the algorithm.
- **Same output.** In general position the result does not depend on $k$.

## Variants and improvements

- **Alternating cuts.** Cutting alternately by $x$ and by $y$ at each level of the recursion also gives short cuts, and is used in practice.
- **Higher dimensions.** Dwyer later showed that for points uniform in a ball in $d$ dimensions, the expected size of the Delaunay triangulation is linear in $n$; see [higher-dimensional Delaunay](/higher-dimensional-delaunay/).

## When to use it

Use it for a static set of points that is spread fairly evenly, when a deterministic $O(n \log n)$ worst case and a fast average are both needed. In the comparison of Su and Drysdale it was the fastest of the methods they tested on uniform data. For points that arrive one at a time, use [Bowyer-Watson](/bowyer-watson-algorithm/).

## Pitfalls

- **Strips with one point in line L3.** MERGE needs at least two points on each side. Keep $k \le n/2$.
- **Forgetting the handle walk of line L6.** BUILD in the rotated frame returns handles at the top and the bottom of the strip. MERGE with these handles walks the wrong chains and can pass the tangent.
- **Equal $x$ across strips in line L3.** Cut the $\prec$-sorted list, not the $x$ range, or points with the same $x$ can fall on both sides of a cut and the hulls of the strips can overlap.
- **Expecting the average bound on clustered data.** The $O(n \log \log n)$ bound needs points spread evenly. For clustered points the time is still $O(n \log n)$, with no gain.

## Implementations

## History

Rex Dwyer published the algorithm in Algorithmica in 1987, in the same volume as Fortune's sweep. He kept the merge of Guibas and Stolfi and changed only the order of the cuts, and he proved the $O(n \log \log n)$ average time for uniform points. Su and Drysdale compared it with incremental and sweep methods in 1997 and found it the fastest on their uniform test data.

## References
