---
tag: HMSXK5
kind: algorithm
slug: divide-and-conquer-convex-hull
name: Divide-and-conquer convex hull
aliases:
- Preparata-Hong algorithm
- merge hull
- MergeHull
area: geometry/convex-hulls
level: core
summary: Splits points by x, computes two hulls and merges them with bridge finding in O(n log n).
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {best: Θ(n log n), worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: true, output-sensitive: false}
history:
  year: 1977
  people: [Franco P. Preparata, Se June Hong]
  note: Preparata and Hong gave O(n log n) divide-and-conquer hulls in the plane and in three dimensions in Communications of the ACM in 1977.
prereqs: [convex-hull-problem, orientation-test, upper-and-lower-hull, divide-and-conquer-paradigm]
see_also: [graham-scan, andrew-monotone-chain, quickhull, kirkpatrick-seidel, chan-algorithm, convex-hull-3d, convex-hull-lower-bound, merge-sort]
sources:
  - paper: doi:10.1145/359423.359430
    title: F. P. Preparata and S. J. Hong, Convex hulls of finite sets of points in two and three dimensions, Communications of the ACM 20(2), 1977
    locator: the whole paper (the planar merge by supporting lines, and the three-dimensional merge)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, the divide-and-conquer hull algorithms in the plane and in three dimensions
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 3, the divide-and-conquer hull in two dimensions, and Chapter 4, the divide-and-conquer hull in three dimensions
---

The divide-and-conquer convex hull, due to Preparata and Hong, computes the [convex hull](/convex-hull/) of $n$ points in the plane the way [merge sort](/merge-sort/) sorts. It sorts the points by $x$, splits them into a left and a right half, computes the hull of each half recursively, and merges the two hulls by finding the two **bridges**, the hull edges that join them. A bridge is found by a two-pointer walk in time linear in the sizes of the two hulls, so the total time is $\Theta(n \log n)$, which is optimal. The same scheme works in three dimensions, where it gave the first $O(n \log n)$ algorithm.

## In plain words

Sort the points from left to right and cut the list in the middle. Build the hull of the left half and the hull of the right half, each in the same way. Now the two hulls sit side by side, and they must be joined into one.

To join them, find a line that touches both hulls from below, with every point above it. Start with the rightmost corner of the left hull and the leftmost corner of the right hull. Walk the left end to the left while the line can still drop, and walk the right end to the right while it can still drop. When neither end can move, the line is the lower bridge. Do the same from above.

The corners above the lower bridge and below the upper bridge are cut away, and what is left is the hull of all the points.

## The problem

The input is a finite list $P$ of points $p = (x, y)$, with repeats allowed. The output is the list of the vertices of $\operatorname{conv}(P)$ in counterclockwise order, starting at the lexicographically smallest point. A point in the middle of a hull edge is not reported. With all points on one line the output is the two end points.

Notation: $n = |P|$, and $h$ is the number of hull vertices. $\mathrm{orient}(p, q, r)$ is the sign of

$$D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x),$$

positive for a left (counterclockwise) turn and zero for collinear points; see [orientation test](/orientation-test/). Points are compared lexicographically. The **lower hull** of a sorted set is the part of the hull boundary from its first to its last point, going counterclockwise, and the **upper hull** is the rest; see [upper and lower hull](/upper-and-lower-hull/). No general position is assumed. Points with equal $x$ are ordered by $y$, and every test is an orientation test, so collinear points, vertical edges and a split inside a column of equal $x$ need no special case.

## The algorithm

The version below builds the lower hull by divide and conquer and gets the upper hull by running the same procedure on the points rotated by $\pi$, that is, $p \mapsto -p$. Preparata and Hong merge whole hulls and find both bridges in one merge; the two forms do the same work.

```pseudo id=main
DC-HULL(P)
L1  S ← the distinct points of P, sorted lexicographically
L2  if |S| ≤ 1 then return S
L3  L ← LOWER(S); U ← the points of LOWER(the list −S in reverse order), negated
L4  return L without its last point + U without its last point

LOWER(T)
L5  if |T| ≤ 2 then return T
L6  A ← LOWER(first half of T); B ← LOWER(second half of T)
L7  i ← |A| − 1; j ← 0                        ▷ indices from 0
L8  repeat
L9      while i > 0 and orient(A[i], B[j], A[i − 1]) ≤ 0 do i ← i − 1
L10     while j < |B| − 1 and orient(A[i], B[j], B[j + 1]) ≤ 0 do j ← j + 1
L11 until neither loop changed i or j
L12 return A[0..i] + B[j..|B| − 1]
```

- **Line L3.** Negating every point is a rotation by $\pi$. It keeps orientation signs and reverses the lexicographic order, so the lower hull of the rotated points is the upper hull of the original points, from the last point back to the first.
- **Line L6.** The two halves are split by position in the sorted list, so every point of the first half comes before every point of the second, even when both contain points with the same $x$.
- **Lines L7 to L11** walk the lower bridge. The line through $A[i]$ and $B[j]$ must have all points on or above it. Line L9 moves the left end down the left hull while the next point $A[i-1]$ is on or below the line, and line L10 does the same on the right hull. The test is $\le 0$, so collinear points are skipped and the bridge ends are vertices.
- **Line L12.** The lower hull of the union is the left chain up to $A[i]$, then the bridge, then the right chain from $B[j]$.

## Example

Take the ten points $(0,0)$, $(4,0)$, $(2,1)$, $(5,3)$, $(2,2)$, $(3,5)$, $(0,4)$, $(1,2)$, $(2,4)$, $(4,4)$. Sorted, they are $(0,0)$, $(0,4)$, $(1,2)$, $(2,1)$, $(2,2)$, $(2,4)$, $(3,5)$, $(4,0)$, $(4,4)$, $(5,3)$, and line L6 splits them into the first five and the last five. The split falls inside the column $x = 2$. The recursion returns the lower hulls $A = (0,0), (2,1), (2,2)$ and $B = (2,4), (4,0), (5,3)$; $A$ ends with a vertical edge. The top-level merge walks as follows:

| step | line | test | value | move | pair $(A[i], B[j])$ |
| --- | --- | --- | --- | --- | --- |
| start | L7 | | | | (2,2), (2,4) |
| 1 | L9 | orient((2,2), (2,4), (2,1)) | 0 | $i$ left | (2,1), (2,4) |
| 2 | L9 | orient((2,1), (2,4), (0,0)) | 6 | stop | (2,1), (2,4) |
| 3 | L10 | orient((2,1), (2,4), (4,0)) | −6 | $j$ right | (2,1), (4,0) |
| 4 | L10 | orient((2,1), (4,0), (5,3)) | 7 | stop | (2,1), (4,0) |
| 5 | L9 | orient((2,1), (4,0), (0,0)) | −4 | $i$ left | (0,0), (4,0) |
| 6 | L10 | orient((0,0), (4,0), (5,3)) | 12 | stop | (0,0), (4,0) |

Step 5 is in the second run of the loop of line L8: moving $j$ made the line steeper, so the left end could drop again. A third run moves nothing. The lower bridge is $(0,0)$ to $(4,0)$, and line L12 returns $L = (0,0), (4,0), (5,3)$. In the same way, the upper merge joins the upper hull $(5,3), (3,5), (2,4)$ of the right half to the upper hull $(2,2), (0,4), (0,0)$ of the left half with the bridge from $(3,5)$ to $(0,4)$, so $U = (5,3), (3,5), (0,4), (0,0)$. Line L4 returns $(0,0), (4,0), (5,3), (3,5), (0,4)$.

## Correctness

**Theorem.** For every finite list $P$, DC-HULL terminates and returns the vertices of $\operatorname{conv}(P)$, each once, in counterclockwise order from the lexicographically smallest point; for collinear input with at least two distinct points it returns the two end points.

The core is the merge lemma. During the walk, every point of the left chain to the right of $A[i]$ and every point of the right chain to the left of $B[j]$ stays on or above the line through $A[i]$ and $B[j]$: a move of one end pivots the line around the other end and only lowers it on the side where those points are. When the walk stops, the neighbours $A[i-1]$ and $B[j+1]$ are strictly above the line, and by the convexity of each chain so are all points further out. So the line supports all points from below and touches them only on the segment from $A[i]$ to $B[j]$, which makes it a hull edge, and the chain edges kept by line L12 are hull edges as well. Points with equal $x$ are handled by a small shear $(x, y) \mapsto (x + \varepsilon y, y)$, which keeps every orientation sign and turns the lexicographic order into the order by $x$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

All costs are on the [real RAM](/real-ram/).

- **Merge.** In lines L7 to L11, $i$ only decreases and $j$ only increases, and each run of the loop of line L8 except the last moves one of them. So a merge of chains of sizes $s$ and $t$ makes $O(s + t)$ orientation tests. Line L12 copies $O(s + t)$ points.
- **Recursion.** With $T(m)$ the time of LOWER on $m$ points, $T(m) = T(\lfloor m/2 \rfloor) + T(\lceil m/2 \rceil) + O(m)$ and $T(2) = O(1)$, so $T(n) = O(n \log n)$, as for [merge sort](/merge-sort/). The recursion depth is $\lceil \log_2 n \rceil$.
- **Total.** Sorting in line L1 takes $O(n \log n)$, and line L3 runs LOWER twice, so the total is $\Theta(n \log n)$ in the worst case. The sort alone costs $\Omega(n \log n)$ comparisons in the worst case, and the merge steps also add up to $\Theta(n \log n)$ on inputs where all points are on the hull.
- **Space.** $\Theta(n)$ for the sorted list and the chains of the current path of the recursion.

The bound is optimal: in the [algebraic decision tree](/algebraic-decision-tree/) model the planar hull needs $\Omega(n \log n)$ operations in the worst case, by a reduction from sorting ([lower bound](/convex-hull-lower-bound/)). It is not output-sensitive: even with $h = 3$ the sort costs $\Theta(n \log n)$.

## Properties

- **Exact with integer input.** The only predicate is the orientation test.
- **Sort first, then linear merges.** After the sort every merge is linear, with no sort inside the recursion, unlike a top-down hull that splits by the median $x$.
- **Strictly convex output.** The $\le 0$ tests in lines L9 and L10 skip collinear points, so the bridges and the chains have only vertices.
- **Parallel.** The two recursive calls are independent and can run in parallel; the merge is a short sequential walk, and parallel hull algorithms use this structure.
- **Extends to three dimensions.** The same split and merge give an $O(n \log n)$ hull in $\mathbb{R}^3$.

## Variants and improvements

- **Merge of whole hulls.** Preparata and Hong keep each hull as one cyclic list and find the upper and lower bridges as the two common tangents of two convex polygons separated by a vertical line. This is the same walk run twice, once on each side.
- **Three dimensions.** The merge of two 3D hulls separated by a plane wraps a band of new triangles around both, found by gift wrapping around an edge as in the [Jarvis march](/jarvis-march/), and deletes the facets that the band hides. With careful bookkeeping the merge takes $O(n)$ time, so the whole algorithm is $O(n \log n)$; see [3D convex hull](/convex-hull-3d/). This version is known to be hard to implement correctly.
- **Linear expected time.** Bentley and Shamos (1978) split the input without sorting it and merged the two hulls, which may overlap, in time linear in their sizes. When the expected hull size of $m$ random points is $O(m^c)$ for some $c < 1$, the expected time is $O(n)$.
- **Median split, bridge first.** The [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) finds the bridge over the median $x$ before recursing and drops the points under it, which gives $O(n \log h)$.
- **Online merge.** Merging a hull with a single point is the step of an incremental hull; with balanced trees for the chains, bridges can be found in $O(\log n)$ time, which is the base of the [dynamic convex hull](/dynamic-convex-hull/).

## When to use it

Use it when the input is already sorted or split by $x$, in parallel or external-memory settings where independent halves help, or as a template for the 3D hull. For a plain sequential planar hull, [Andrew's monotone chain](/andrew-monotone-chain/) has the same $O(n \log n)$ bound with less code. When the hull is expected to be small, use an output-sensitive method such as [Chan's algorithm](/chan-algorithm/) or [Quickhull](/quickhull/).

## Pitfalls

- **Stopping the walk too early.** Moving $i$ once and then $j$ once is not enough: in the example, the left end must move again after the right end moved. Repeat until neither end moves.
- **Strict tests at the bridge.** With $< 0$ instead of $\le 0$ in lines L9 and L10, a bridge can end at a point in the middle of a hull edge. For the points $(0,0)$, $(1,0)$, $(2,0)$, $(3,5)$, split two and two, the walk stops at once with the bridge from $(1,0)$ to $(2,0)$, and the lower hull keeps both middle points.
- **Splitting by $x$ value.** Splitting at a value of $x$ instead of at a list position can leave one half empty when many points share an $x$, and the recursion does not shrink.
- **Starting at the wrong ends.** The walk for the lower bridge starts at the last point of the left chain and the first point of the right chain. Starting elsewhere can stop at a local tangent that is not the bridge.
- **Floating-point tests.** Near-collinear points can make the walk stop at the wrong pair. Use exact orientation tests.

## Implementations

## History

Franco Preparata and Se June Hong published the divide-and-conquer hull for the plane and for three dimensions in Communications of the ACM in 1977. In the plane it matched the $O(n \log n)$ of Graham's scan; in three dimensions it was the first $O(n \log n)$ algorithm, and the bound is optimal there too. Bentley and Shamos analysed a divide-and-conquer hull on random inputs in 1978. The merge by bridges reappears in the dynamic hull of Overmars and van Leeuwen (1981) and in the output-sensitive algorithm of Kirkpatrick and Seidel (1986).

## References
