---
tag: 2ZMWQH
kind: algorithm
slug: polygon-triangulation-dp
name: Dynamic programming for minimum-weight polygon triangulation
aliases:
- Optimal convex polygon triangulation
- Klincsek dynamic program
- optimal simple polygon triangulation
area: geometry/triangulations
level: core
summary: Computes the minimum-weight triangulation of a convex polygon in O(n^3) time.
solves: [optimal-polygon-triangulation, polygon-triangulation]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Peter D. Gilbert, G. T. Klincsek]
  note: Gilbert (1979) and Klincsek (1980) found the cubic dynamic program for minimum weight triangulations of a polygon, valid for simple polygons once the valid diagonals are known.
prereqs: [polygon-triangulation, interval-dp, simple-polygon, orientation-test]
see_also: [optimal-polygon-triangulation, min-weight-triangulation, catalan-triangulation-theorem, number-of-triangulations, matrix-chain-multiplication, greedy-triangulation, ear-clipping]
sources:
  - paper: "G. T. Klincsek, Minimal triangulations of polygonal domains, Annals of Discrete Mathematics 9, 121 to 123 (1980)"
    locator: the O(n^3) dynamic program for a simple polygon
  - paper: "Peter D. Gilbert, New results in planar triangulations, Report R-850, Coordinated Science Laboratory, University of Illinois (1979)"
    locator: the dynamic program and the greedy triangulation; report number to be checked
  - paper: doi:10.1145/1346330.1346336
    title: Wolfgang Mulzer and Günter Rote, Minimum-weight triangulation is NP-hard, Journal of the ACM 55(2), Article 11 (2008)
    locator: the introduction (the polygon case is polynomial by dynamic programming, the point set case is NP-hard)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.6 (the diagonal test with InCone) and the exercises on optimal triangulations; to be checked
---

The interval dynamic program finds, among all triangulations of a polygon, one of least total weight. The classic weight is the total length of the diagonals, which gives the minimum weight triangulation of the polygon; any weight that adds up over triangles works. For a polygon with $n$ vertices it runs in $\Theta(n^3)$ time and $\Theta(n^2)$ space, even though the number of triangulations can be the [Catalan number](/catalan-triangulation-theorem/) $C_{n-2} \approx 4^n$. It works for any [simple polygon](/simple-polygon/), not only convex ones: the only change is that segments which are not diagonals are left out. This page gives the full algorithm for simple polygons; the [optimal polygon triangulation](/optimal-polygon-triangulation/) page covers the convex case as an interval DP problem, with its link to matrix chains.

## In plain words

Look at one side of the polygon, the one from the first corner to the last. In every way of cutting the polygon into triangles, that side belongs to exactly one triangle, and its third corner sits somewhere in between. That triangle splits the polygon into two smaller polygons, which can be cut independently. So for every stretch of corners, from some corner to a later one, work out the cheapest way to cut that piece, starting with the shortest stretches. Each piece tries every possible middle corner and keeps the cheapest.

## The problem

**Input.** A simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in order, and a weight $w(v_a, v_b, v_c)$ for each triangle of three vertices.

**Output.** A triangulation $T$ of $P$ by diagonals that minimizes $\sum_{t \in T} w(t)$, and that minimum.

With $w$ equal to the perimeter of the triangle, each diagonal is counted twice and each polygon side once, so the total is twice the diagonal length plus the fixed perimeter of $P$: the minimum is the **minimum weight triangulation** of the polygon. For point sets in general, the same problem is NP-hard; see [minimum weight triangulation](/min-weight-triangulation/). Replacing min by sum gives the **number of triangulations** of $P$.

## The algorithm

For $i < j$, call $(i, j)$ admissible if $v_i v_j$ is a polygon side or a diagonal. For an admissible pair, $P(i, j)$ is the sub-polygon $v_i, v_{i+1}, \ldots, v_j$ closed by the segment $v_j v_i$, and $\mathrm{cost}[i][j]$ is the least weight of a triangulation of it. The answer is $\mathrm{cost}[0][n-1]$, since $P(0, n-1) = P$.

```pseudo id=main
POLYGON-TRIANGULATION-DP(P, w)                ▷ P = v[0 .. n − 1], simple, n ≥ 3
L1  if the signed area of P is negative then reverse the vertex order
L2  for 0 ≤ i < j ≤ n − 1 do ok[i][j] ← (j = i + 1) or (i, j) = (0, n − 1) or IS-DIAGONAL(i, j)
L3  for i ← 0 to n − 2 do cost[i][i + 1] ← 0
L4  for d ← 2 to n − 1 do
L5      for i ← 0 to n − 1 − d do  j ← i + d; skip unless ok[i][j]
L6          cost[i][j] ← min over i < k < j with ok[i][k] and ok[k][j] of cost[i][k] + cost[k][j] + w(v_i, v_k, v_j); split[i][j] ← the best k
L7  rebuild the triangles from split, starting at (0, n − 1)
L8  return cost[0][n − 1] and the triangles

IS-DIAGONAL(i, j)
L9  if a vertex other than v_i, v_j lies on the closed segment v_i v_j, or an edge crosses it properly, return false
L10 return true if v_j lies strictly inside the angle of P at v_i
```

- **Line L2** tests $O(n^2)$ pairs at $O(n)$ each. Line L9 uses only the [orientation test](/orientation-test/). Line L10 is O'Rourke's InCone test: at a convex corner, $v_j$ must be strictly left of both $v_{i-1} \to v_i$ and $v_i \to v_{i+1}$; at a reflex or flat corner, strictly left of at least one.
- **Line L6** is the recurrence. The side $v_i v_j$ of $P(i, j)$ lies in exactly one triangle $v_i v_k v_j$, and that triangle splits $P(i, j)$ into $P(i, k)$ and $P(k, j)$. A diagonal of $P(i, j)$ is the same as a diagonal of $P$ with ends in $v_i, \ldots, v_j$, so the table ok computed once for $P$ serves every sub-polygon.
- **Line L7** walks the split table with an explicit stack and outputs $n - 2$ triangles.
- **Counting.** The same loops with $\mathrm{cnt}[i][i+1] = 1$ and $\mathrm{cnt}[i][j] = \sum_k \mathrm{cnt}[i][k] \cdot \mathrm{cnt}[k][j]$ count the triangulations of $P$ exactly.

## Example

Take the notched rectangle $v_0 = (0,0)$, $v_1 = (6,0)$, $v_2 = (6,4)$, $v_3 = (4,4)$, $v_4 = (3,1)$, $v_5 = (2,4)$, $v_6 = (0,4)$ and the weight that makes the cost the total diagonal length. The reflex vertex $v_4$ at the bottom of the notch blocks most segments; for example, $v_0 v_2$ passes through the notch at $(3, 2)$, outside the polygon. The admissible diagonals are $v_0 v_4$, $v_1 v_4$, $v_1 v_3$, $v_2 v_4$, $v_0 v_5$ and $v_4 v_6$.

Every triangulation uses $v_0 v_4$ and $v_1 v_4$ (the triangle on the side $v_0 v_1$ must be $v_0 v_1 v_4$), and then splits the quadrilaterals $v_1 v_2 v_3 v_4$ and $v_4 v_5 v_6 v_0$ by one of two diagonals each. So there are $2 \cdot 2 = 4$ triangulations, which the counting version reports.

| quadrilateral | choices | lengths | best |
|---|---|---|---|
| $v_1 v_2 v_3 v_4$ | $v_1 v_3$ or $v_2 v_4$ | $\sqrt{20}$ or $\sqrt{18}$ | $v_2 v_4$ |
| $v_4 v_5 v_6 v_0$ | $v_0 v_5$ or $v_4 v_6$ | $\sqrt{20}$ or $\sqrt{18}$ | $v_4 v_6$ |

In the DP, the triangle on the side $v_0 v_6$ is $v_0 v_4 v_6$ or $v_0 v_5 v_6$ ($k = 4$ or $5$). The sub-polygon $P(0, 4)$ has only $k = 1$ on its side $v_0 v_4$, and then $P(1, 4)$ chooses $k = 2$ or $k = 3$. The optimum has the diagonals $v_0 v_4$, $v_1 v_4$, $v_2 v_4$, $v_4 v_6$ with total length $2\sqrt{10} + 6\sqrt{2} \approx 14.81$, and the triangles $v_0 v_1 v_4$, $v_1 v_2 v_4$, $v_2 v_3 v_4$, $v_4 v_5 v_6$, $v_0 v_4 v_6$. The worst triangulation, with $v_1 v_3$ and $v_0 v_5$, has length $2\sqrt{10} + 4\sqrt{5} \approx 15.27$.

## Correctness

**Theorem.** For a simple polygon with $n \ge 3$ vertices and any real triangle weights, POLYGON-TRIANGULATION-DP returns the least total weight over all triangulations and a triangulation with $n - 2$ triangles that attains it.

The proof is in [proofs/correctness.md](proofs/correctness.md). Lemma 1 shows that lines L9 and L10 accept exactly the diagonals. Lemma 2 shows that each $P(i, j)$ for an admissible pair is a simple polygon whose diagonals are the diagonals of $P$ between its vertices. Lemma 3 is the recurrence: the triangle on the side $v_i v_j$ splits every triangulation of $P(i, j)$ into triangulations of $P(i, k)$ and $P(k, j)$, and every such combination is a triangulation. Induction on $j - i$ then shows that $\mathrm{cost}[i][j]$ is optimal.

## Complexity

- **Diagonal table.** $\binom{n}{2}$ pairs, each tested against $n$ edges and $n$ vertices: $O(n^3)$ time, $O(n^2)$ space.
- **Recurrence.** $O(n^2)$ pairs, each with at most $n - 2$ choices of $k$: $O(n^3)$ time and at most that many weight evaluations.
- **Rebuild.** $O(n)$.
- **Total.** $\Theta(n^3)$ time in the worst case (on a convex polygon every pair is admissible and every $k$ is tried) and $\Theta(n^2)$ space. Each step is a constant number of exact arithmetic operations on the [real RAM](/real-ram/).

## Properties

- **Any additive weight.** Only addition and comparison of weights are used; max in place of the sum gives bottleneck triangulations (minimize the worst triangle).
- **Exact on integers.** The diagonal test uses orientation signs only. Weights given as integers or fractions keep the whole computation exact. Euclidean lengths are square roots; comparing sums of square roots exactly is an open problem in the bit model, so practical code compares floating-point sums.
- **Deterministic.** Ties are broken by the smallest $k$.
- **Not output-sensitive.** The cubic time is spent even when the polygon has a single triangulation.

## Variants and improvements

- **Convex polygons.** All pairs are admissible, so line L2 is trivial; see [optimal polygon triangulation](/optimal-polygon-triangulation/). For the matrix chain weight $p_i p_k p_j$, Hu and Shing solve it in $O(n \log n)$.
- **Point sets.** For $n$ points with no polygon, minimum weight triangulation is NP-hard (Mulzer and Rote 2008). The polygon DP is still used inside exact point set methods: once enough edges are known to be in every optimal triangulation (the LMT skeleton, or the $\beta$-skeleton), the remaining polygonal holes are filled by this DP.
- **Few interior points.** Hoffmann and Okamoto (2004) extend the DP to point sets with $k$ interior points in time exponential only in $k$.
- **Counting.** The sum version counts triangulations of a simple polygon in $O(n^3)$; for point sets counting is much harder; see [number of triangulations](/number-of-triangulations/).
- **Other measures.** Max-min angle, min-max angle and min-max edge length triangulations of a polygon all fit the same recurrence with max or min in place of the sum.

## When to use it

Use the DP when the polygon has at most a few hundred vertices and the triangulation must be optimal for a cost that adds up over triangles, or when the number of triangulations of a polygon is wanted. For large polygons where any triangulation will do, use [ear clipping](/ear-clipping/) or the [monotone method](/monotone-polygon-triangulation/). For good triangle shapes on point sets, the [Delaunay triangulation](/delaunay-triangulation/) is optimal for the max-min angle and faster. The [greedy triangulation](/greedy-triangulation/) is a cheaper heuristic for short total length.

## Pitfalls

- **Using all chords of a non-convex polygon.** The recurrence over all $k$ without the admissibility test triangulates the convex hull of the vertex order, not the polygon; the output then has triangles outside $P$.
- **Collinear vertices.** A segment that passes through another vertex is not a diagonal, even if it lies inside the polygon. Without the vertex check in line L9, a flat corner like $(1,0)$ in $(0,0), (1,0), (2,0), (1,2)$ gives a triangle of zero area.
- **Orientation.** The InCone test of line L10 assumes counterclockwise order; on a clockwise polygon it accepts exterior segments unless line L1 runs.
- **Recursive memoization.** A top-down version recurses to depth $n$; with Python's default limit that fails near $n = 1000$, and it is also slower. The loops by length avoid this.
- **Floating-point ties.** With Euclidean weights, two triangulations of equal length can be ordered differently by rounding. If ties matter, use exact integer surrogate weights or accept any optimum.

## Implementations

The Python version computes the diagonal table once, fills the cost table by increasing length $d$, and rebuilds the triangulation with an explicit stack. It takes any weight function on triangle index triples, so the tests can use exact integer weights. The tests enumerate every triangulation of small random simple polygons by brute force (all sets of $n - 3$ pairwise non-crossing diagonals) and check the minimum cost and the number of triangulations against the DP. Each returned triangulation is checked for exact area, non-crossing edges and the count $n - 2$. Convex polygons on a parabola give the Catalan numbers.

## History

The cubic dynamic program for minimum weight triangulations of a polygon appeared in the late 1970s, in Gilbert's 1979 report and in Klincsek's 1980 paper, and it was the main evidence that the problem might be easy. For point sets, whether minimum weight triangulation is NP-hard stayed one of the open problems listed by Garey and Johnson in 1979, until Mulzer and Rote proved NP-hardness in 2006 (journal version 2008). For convex polygons the same recurrence is the triangulation form of matrix chain ordering, used by Hu and Shing in 1982.

## References
