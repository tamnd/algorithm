---
tag: 77Q05F
kind: algorithm
slug: visvalingam-whyatt
name: Visvalingam-Whyatt algorithm
aliases:
- Visvalingam algorithm
- effective area line simplification
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Simplifies a polyline by repeatedly removing the point whose triangle with its two neighbors has the least area. O(n log n) with a heap.
solves: [curve-simplification, polygon-simplification]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: O(n log n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1993
  people: [Maheswari Visvalingam, James D. Whyatt]
  note: Visvalingam and Whyatt published the method in The Cartographic Journal in 1993, for the generalization of map lines.
prereqs: [binary-heap, doubly-linked-list, oriented-triangle-area]
see_also: [ramer-douglas-peucker, curve-simplification, polygon-simplification, shoelace-formula, priority-queue, indexed-priority-queue, mesh-simplification, hausdorff-distance]
sources:
  - paper: doi:10.1179/000870493786962263
    title: M. Visvalingam and J. D. Whyatt, Line generalisation by repeated elimination of points, The Cartographic Journal 30(1), 46-51 (1993)
    locator: the effective area of a point, the repeated elimination of the point with the least effective area, and the rule that a recomputed area below the area of the last eliminated point takes that area
---

The Visvalingam-Whyatt algorithm makes a [polyline](/polygon/) with fewer points by removing one point at a time. The *effective area* of an inner point is the area of the triangle that it makes with its two current neighbors, and the algorithm always removes the point with the least effective area. After each removal only the two neighbors get a new area, so a [binary heap](/binary-heap/) and a [doubly linked list](/doubly-linked-list/) give $O(n \log n)$ time. One run ranks all points, so it gives the result for every threshold and every number of points at once.

## In plain words

Look at each point of the line together with the point before it and the point after it. The three points make a small triangle. A point whose triangle is small adds very little to the shape, because the line without it looks almost the same.

So find the point with the smallest triangle and remove it. Its two neighbors now have new neighbors, so their triangles change, and you measure them again. Then remove the next smallest, and go on. Stop when every triangle is larger than the size you accept, or when the number of points is small enough. Small wiggles go first, and the large bends stay.

## The problem

The input is a polyline $P_0, \dots, P_{n-1}$ of points in the plane and an area threshold $A \ge 0$. The output is a subsequence of the points that keeps $P_0$ and $P_{n-1}$. It is the solution to the area form of [curve simplification](/curve-simplification/): the tolerance is an area, not a distance. There is no guarantee on the number of points or on the distance to the input.

The model is the [real RAM](/real-ram/). The unit of work is one triangle area or one heap operation. The implementation works with twice the area, $|(P_{i-1} - P_i) \times (P_{i+1} - P_i)|$, the absolute value of the [oriented triangle area](/oriented-triangle-area/) times two, so for integer or rational points it is exact.

## The algorithm

The array $a$ holds the doubled effective area of each inner point. The heap $H$ can hold old entries for a point. An entry $(v, i)$ is *stale* if $P_i$ is removed or $v \ne a[i]$, and the loop skips it.

```pseudo id=main
VISVALINGAM-WHYATT(P_0, ..., P_(n−1), A)
L1  prev[i] ← i−1, next[i] ← i+1 for all i; a[i] ← 2·area(P_(i−1), P_i, P_(i+1)) for 0 < i < n−1
L2  H ← a min-heap of the pairs (a[i], i) for 0 < i < n−1, ordered by area and then by index
L3  while H is not empty do
L4      (v, i) ← pop-min(H)
L5      if P_i is removed or v ≠ a[i] then go to the next pass of the loop
L6      if v ≥ 2A then stop the loop
L7      mark P_i removed; next[prev[i]] ← next[i]; prev[next[i]] ← prev[i]
L8      for each j in {prev[i], next[i]} with 0 < j < n−1 do
L9          a[j] ← 2·area(P_prev[j], P_j, P_next[j]); push (a[j], j) on H
L10 return the points that are not removed, in the order of their index
```

The heap has no decrease-key operation, so line L9 pushes a new entry and line L5 drops the old one later. This is lazy deletion. An [indexed priority queue](/indexed-priority-queue/) with decrease-key also works, and keeps the heap at $n - 2$ entries.

## Example

Take the same $n = 8$ points as on the [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) page:

$$P_0 = (0, 0),\ P_1 = (2, 1),\ P_2 = (4, 0),\ P_3 = (6, 3),\ P_4 = (8, 1),\ P_5 = (10, 6),\ P_6 = (12, 5),\ P_7 = (14, 7).$$

Line L1 gives the doubled areas $4, 8, 10, 14, 12, 6$ for $P_1, \dots, P_6$. The table shows the valid pops with $A$ larger than every area, so the run removes all inner points. The real area is half of each value.

| Step | Removed | Doubled area | New neighbors | Recomputed doubled areas |
|---|---|---|---|---|
| 1 | $P_1$ | 4 | $P_0, P_2$ | $P_2$: 12 |
| 2 | $P_6$ | 6 | $P_5, P_7$ | $P_5$: 18 |
| 3 | $P_3$ | 10 | $P_2, P_4$ | $P_2$: 4, $P_4$: 18 |
| 4 | $P_2$ | 4 | $P_0, P_4$ | $P_4$: 38 |
| 5 | $P_5$ | 18 | $P_4, P_7$ | $P_4$: 42 |
| 6 | $P_4$ | 42 | $P_0, P_7$ | none |

The heap also pops 6 stale entries: $(8, 2)$ before step 3, the entries $(12, 2)$, $(12, 5)$, $(14, 4)$ and $(18, 4)$ before step 5, and $(38, 4)$ before step 6. So there are 12 pushes and 12 pops in total.

The order gives every result:

- $A = 3$: the run stops at step 2, because $6 \ge 6$. The output is $P_0, P_2, P_3, P_4, P_5, P_6, P_7$.
- $A = 4$: steps 1 and 2 run, and step 3 stops, because $10 \ge 8$. The output is $P_0, P_2, P_3, P_4, P_5, P_7$.
- $A = 8$: steps 1 to 4 run, and step 5 stops. The output is $P_0, P_4, P_5, P_7$.
- Keep 5 points: remove the first 3 of the order. The output is $P_0, P_2, P_4, P_5, P_7$. Ramer-Douglas-Peucker with $\varepsilon = 2$ also keeps 5 points, but it keeps $P_3$ where this keeps $P_2$.

Step 4 removes $P_2$ with the area 4, which is smaller than the area 10 of step 3. So the recorded areas do not increase. If you keep the recorded areas and later filter them by "remove the points with doubled area below $8$", you remove $P_1$, $P_6$ and $P_2$ and get $P_0, P_3, P_4, P_5, P_7$. That is not the output for $A = 4$, because the run stopped before $P_2$. The 1993 paper fixes this: a recomputed area below the last removed area takes that area. Then step 4 records 10 instead of 4, the recorded areas never decrease, and a filter by area gives the same output as a run with that threshold in this example.

## Correctness

The proof in the proof file shows three things. First, the heap loop removes the same points in the same order as the direct rule: remove the inner point with the least current effective area, the smallest index on ties. The reason is that a removal changes the links of only its two neighbors, and the area of a point depends only on its links, so line L9 keeps the stored area of every alive point correct. Second, the output for a threshold $A$ is the input without the longest prefix of the order whose areas are below $A$. The end points are never in the heap, so they are kept. Third, a larger threshold gives a subset of the output of a smaller one, because the order does not depend on $A$.

## Complexity

- **Time, worst case $O(n \log n)$.** Line L2 builds the heap in $O(n)$. Each removal pushes at most 2 entries, so there are at most $3(n - 2)$ pushes and pops in total, each $O(\log n)$. Each area is $O(1)$.
- **Time, best case $\Theta(n)$.** If the threshold is below every area, the loop stops at the first pop, after $\Theta(n)$ work for line L1 and line L2.
- **Space, $\Theta(n)$.** The links, the areas and the heap. With lazy deletion the heap holds at most $3(n - 2)$ entries.

Lazy deletion does not change the bound, because the number of stale entries is at most the number of pushes.

## Properties

- **Both ends stay**, and the output is a subsequence of the input.
- **Nested results.** The output for a larger threshold is a subset of the output for a smaller one, and the output for $k$ points is a subset of the output for $k + 1$ points. So one run gives a hierarchy of all levels of detail, which is useful for zoom levels of a map.
- **No distance guarantee.** A narrow spike has a small area. In $(0, 0), (1, 100), (2, 0)$ the inner point has area 100, so with $A = 101$ it is removed, and the output is 100 away from the input. In the other direction, $(0, 0), (500, 1), (1000, 0)$ has area 500, so with $A = 100$ the point stays although it is only 1 from the chord. If the error must be a distance, use [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) or the optimal methods of [polygon simplification](/polygon-simplification/).
- **Not minimal.** The method is greedy and never puts a point back, so another subset can meet the same area test with fewer points.
- **Not simple.** The output of a simple polyline can cross itself.
- **Collinear points first.** A point on the line through its neighbors has area 0, so it goes before all others.
- **Any dimension.** The area of a triangle is defined in any dimension, with $|u \times v|$ replaced by $\sqrt{|u|^2 |v|^2 - (u \cdot v)^2}$, so the method also works in $\mathbb{R}^3$. The implementation of this page is for the plane.

## Variants and improvements

- **Monotone areas (Visvalingam and Whyatt 1993).** If a recomputed area is below the area of the last removed point, use that area. The recorded areas then never decrease, so the order can be stored with the points, and a filter by area gives nested results. This changes the order when both raised neighbors get the same value, and then the tie rule decides which goes first.
- **A fixed number of points.** Remove the first $n - k$ points of the order. This gives $k$ points with the same run.
- **Weighted areas.** Some map tools multiply the area by a factor that depends on the shape of the triangle, for example its angle at the point, so that flat or sharp triangles go first or last. This changes the ranking, not the algorithm.
- **Closed curves.** For a ring, every point has two neighbors, and the heap holds all of them. Stop at 3 points, or keep one fixed point.
- **Shared borders.** When polygons share a border, simplify each shared chain once, with its end points fixed, so that the borders stay identical.
- **Meshes.** Removing the vertex or edge with the least local error, and updating only the neighbors in a heap, is also the pattern of [mesh simplification](/mesh-simplification/) with [quadric error metrics](/quadric-error-metrics/).

## When to use it

Use it to make map lines and outlines for display at many scales, where the result must look smooth and the small wiggles must go first. It is a good choice when you need a ranking of all points, for example for progressive drawing or for zoom levels, because one run gives all levels. Use [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) when the error must be a distance bound, and an optimal method when the number of points must be the smallest.

## Pitfalls

- **Forgetting stale entries.** Without the test of line L5, a point is removed twice or with an old area, and the order is wrong. In the example, the entry $(8, 2)$ is popped while the true area of $P_2$ is 12.
- **Filtering stored areas without the monotone rule.** The areas of the plain run can go down, as in step 4 of the example. A filter by the stored areas then does not give the output of a run with that threshold. To get the exact output of every threshold from one plain run, store the running maximum of the recorded areas instead: the run for $A$ removes a point exactly when the running maximum at its step is below $2A$.
- **Half or twice the area.** The code compares twice the area with $2A$. Mixing the two halves the threshold.
- **Integer overflow.** In languages with fixed-size integers, the cross product of coordinates near $2^{31}$ overflows a 32-bit integer. Use 64-bit integers or floating point.
- **A distance threshold.** An area is not a length. A threshold of 1 square unit removes a spike of height 100 on a base of 0.01, as the example in the properties shows.
- **Recomputing all areas.** Rescanning all areas after each removal is $O(n^2)$. Only the two neighbors change.

## Implementations

The Python file in this folder has `vw_order(points, monotone=False, stop=None)`, which returns the removal order with the doubled areas, `visvalingam_whyatt(points, min_area)`, which follows the pseudocode, and `vw_keep(points, k)`. They use `heapq` with lazy deletion and exact arithmetic for integer and rational input. The tests check the example, the area against the shoelace formula, the heap order against a direct $O(n^2)$ rule that rescans all areas after each removal, the threshold output against the prefix of the order, the running maximum filter against a run for each threshold, the nesting of outputs, the monotone values, and rational input.

## History

Maheswari Visvalingam and James Whyatt published the method in The Cartographic Journal in 1993, for the generalization of map lines. They called the area of the triangle the effective area, and they gave the rule that keeps the recorded areas monotone. The method is now common in web map tools, because it gives smooth outlines and a ranking of all points from one run.

## References
