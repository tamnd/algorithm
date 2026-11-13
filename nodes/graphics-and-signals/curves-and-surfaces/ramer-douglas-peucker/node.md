---
tag: 81WHGP
kind: algorithm
slug: ramer-douglas-peucker
name: Ramer-Douglas-Peucker algorithm
aliases:
- Douglas-Peucker algorithm
- RDP
- iterative end-point fit algorithm
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: Simplifies a polyline by keeping the point farthest from the chord when it lies more than a tolerance away, then splitting there. Θ(n^2) worst case.
solves: [curve-simplification, polygon-simplification]
model: real-ram
complexity:
  vars: {n: the number of input points, d: the dimension of the points}
  time: {worst: Θ(n^2 d), best: Θ(n d)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1972
  people: [Urs Ramer, David H. Douglas, Thomas K. Peucker]
  note: Ramer published the method for pattern recognition in 1972, and Douglas and Peucker published it for cartography in 1973.
prereqs: [point-to-segment-distance, stack]
see_also: [curve-simplification, polygon-simplification, visvalingam-whyatt, hausdorff-distance, frechet-distance, convex-hull, polygon-simplicity-test, priority-queue]
sources:
  - paper: doi:10.1016/S0146-664X(72)80017-0
    title: Urs Ramer, An iterative procedure for the polygonal approximation of plane curves, Computer Graphics and Image Processing 1(3), 244-256 (1972)
    locator: the split at the point of maximum distance from the chord, repeated until all distances are within the tolerance; the paper says the result has a small but not a minimum number of vertices
  - paper: doi:10.3138/FM57-6770-U75U-7727
    title: David H. Douglas and Thomas K. Peucker, Algorithms for the reduction of the number of points required to represent a digitized line or its caricature, The Canadian Cartographer 10(2), 112-122 (1973)
    locator: the farthest point method with a tolerance band, for digitized map lines
  - paper: "John Hershberger and Jack Snoeyink, Speeding up the Douglas-Peucker line-simplification algorithm, Proceedings of the 5th International Symposium on Spatial Data Handling, Charleston, volume 1, 134-143 (1992)"
    locator: the quadratic worst case of the classic method, and the path hull that finds each farthest point in logarithmic time, for O(n log n) in the worst case
  - paper: doi:10.1145/177424.178097
    title: John Hershberger and Jack Snoeyink, An O(n log n) implementation of the Douglas-Peucker algorithm for line simplification, Proceedings of the 10th Annual Symposium on Computational Geometry, 383-384 (1994)
    locator: the short version of the path hull method
---

The Ramer-Douglas-Peucker algorithm makes a [polyline](/polygon/) with fewer points. It draws the chord between the two end points, finds the point farthest from the chord, and keeps it if its distance is more than a tolerance $\varepsilon$. Then it does the same on the two parts, until every removed point is within $\varepsilon$ of the chord that replaces it. It is the most used method for [curve simplification](/curve-simplification/), it is short to code, and its output is within Hausdorff distance $\varepsilon$ of the input, but it does not give the smallest number of points.

## In plain words

Pin the first and the last point of the line, and stretch a straight thread between them. Look for the point of the line that is farthest from the thread. If it is close enough, the thread is a good copy of the whole line, and you drop all the points between the pins. If it is too far, pin that point too. Now you have two shorter pieces, each with a pin at both ends, and you do the same on each piece.

The work stops when every piece is close to its thread. The pins are the new line. Each dropped point is near the thread that replaced it, so the new line stays near the old one. But a cleverer choice of pins can sometimes use fewer of them.

## The problem

The input is a polyline $P_0, \dots, P_{n-1}$ of points in $\mathbb{R}^d$ and a tolerance $\varepsilon \ge 0$. The output is a subsequence $P_{k_0}, \dots, P_{k_r}$ with $k_0 = 0$ and $k_r = n - 1$, such that each removed point $P_m$ with $k_s < m < k_{s+1}$ is within distance $\varepsilon$ of the segment $P_{k_s} P_{k_{s+1}}$. This is the tolerance zone form of [polygon simplification](/polygon-simplification/). The algorithm finds a valid output, but not one with the fewest points.

The model is the [real RAM](/real-ram/). The unit of work is one [point-to-segment distance](/point-to-segment-distance/), which costs $O(d)$ operations. The implementation compares squared distances, so with integer or rational points it is exact.

## The algorithm

The distance $\delta(m; i, j)$ is the distance from $P_m$ to the closed segment $P_i P_j$. A stack holds the pairs $(i, j)$ of kept indices whose inner points are not yet tested.

```pseudo id=main
RDP(P_0, ..., P_(n−1), ε)
L1  keep[0] ← keep[n−1] ← true, keep[m] ← false for 0 < m < n−1
L2  S ← a stack that holds the pair (0, n−1)
L3  while S is not empty do
L4      (i, j) ← pop(S)
L5      k ← the index i < k < j with the largest δ(k; i, j), the first on ties; d ← δ(k; i, j), or d ← 0 if j = i + 1
L6      if d > ε then
L7          keep[k] ← true
L8          push (k, j) and then (i, k) on S
L9  return the points P_m with keep[m] true, in the order of m
```

Line L8 pushes $(i, k)$ last, so it is popped first, and the order of the work is the same as in the recursive form of the papers. The order does not change the output, because the test of a pair looks only at the points between its two ends. The stack replaces the recursion, whose depth can reach $n - 2$.

## Example

Take $n = 8$ points and $\varepsilon = 2$, so the test of line L6 is $\delta^2 > 4$:

$$P_0 = (0, 0),\ P_1 = (2, 1),\ P_2 = (4, 0),\ P_3 = (6, 3),\ P_4 = (8, 1),\ P_5 = (10, 6),\ P_6 = (12, 5),\ P_7 = (14, 7).$$

| Pop | Pair $(i, j)$ | Farthest $k$ | $\delta^2$ | $\delta$ | Action |
|---|---|---|---|---|---|
| 1 | $(0, 7)$ | 4 | $36/5$ | 2.683 | keep $P_4$, push $(4, 7)$, $(0, 4)$ |
| 2 | $(0, 4)$ | 3 | $324/65$ | 2.233 | keep $P_3$, push $(3, 4)$, $(0, 3)$ |
| 3 | $(0, 3)$ | 2 | $16/5$ | 1.789 | finished |
| 4 | $(3, 4)$ | none | | | finished |
| 5 | $(4, 7)$ | 5 | $9/2$ | 2.121 | keep $P_5$, push $(5, 7)$, $(4, 5)$ |
| 6 | $(4, 5)$ | none | | | finished |
| 7 | $(5, 7)$ | 6 | $36/17$ | 1.455 | finished |

The output is $P_0, P_3, P_4, P_5, P_7$, which is 5 of the 8 points. In pop 1 the other squared distances are $0$ for $P_1$ and $P_3$, $16/5$ for $P_2$ and $4/5$ for $P_5$ and $P_6$. With $\varepsilon = 1$ the output keeps 7 points and drops only $P_1$, and with $\varepsilon = 3$ it is the single segment $P_0 P_7$.

The output is not the smallest. For $\varepsilon = 2$, the 3 points $P_0, P_2, P_7$ also meet the tolerance: $P_1$ is at distance 1 from the segment $P_0 P_2$, and $P_3, \dots, P_6$ are within 2 of the segment $P_2 P_7$. RDP cannot find this answer, because its first step keeps $P_4$, and it never removes a kept point. The shortcut graph method on the [polygon simplification](/polygon-simplification/) page finds the minimum.

## Correctness

The invariant of the loop is: every pair of consecutive kept indices is on the stack once, or all points between its two ends are within $\varepsilon$ of its segment. Line L1 and line L2 make it true. A pop either finishes the pair, when the largest distance is at most $\varepsilon$, or splits it at a new kept index and pushes both new pairs. Each split keeps one more point, so there are at most $n - 2$ splits, and the loop stops after at most $2n - 3$ pops. At the end the stack is empty, so every removed point is within $\varepsilon$ of the output segment over it.

A corollary is a bound on the Hausdorff distance: each point of the input polyline is within $\varepsilon$ of the output, and each point of the output is within $\varepsilon$ of the input. The full proofs are in the proof file below.

## Complexity

A pop of the pair $(i, j)$ computes $j - i - 1$ distances. The total is the sum of $j - i - 1$ over all popped pairs.

- **Worst case, $\Theta(n^2 d)$.** If every split is at $k = j - 1$, the pairs $(0, n-1), (0, n-2), \dots$ cost $(n-2) + (n-3) + \dots + 1 = (n-1)(n-2)/2$ distances. The points $P_k = (k, 1000^k)$ for $k < 32$ do this with $\varepsilon = 0$: each chord is almost vertical, and the point before its upper end is the farthest, so the run takes all $465 = 31 \cdot 30 / 2$ distances. There is also an upper bound of $n^2$: a point $m$ is tested once in each pair that contains it, and these pairs are nested, with a new kept point at each level.
- **Best case, $\Theta(n d)$.** If all inner points are within $\varepsilon$ of the first chord, one pop does $n - 2$ distances and the loop stops.
- **Balanced splits, $O(n d \log n)$.** If each split is near the middle of its pair, the cost satisfies $T(n) = 2 T(n/2) + O(n)$, and the [master theorem](/master-theorem/) gives $O(n \log n)$ distances. This is the usual case on map data and smooth curves, and it is an observation, not a bound. The points $P_k = (k, k^2)$ with $\varepsilon = 0$ give 315 distances for $n = 64$, against 1953 in the worst case.

The array $keep$ takes $\Theta(n)$ space. The stack holds at most one pair per kept point plus one, so it is $O(n)$, and it does not grow the call stack.

## Properties

- **Both ends stay.** The first and the last point are never removed, and the output is a subsequence of the input. So it keeps the end points of the line where lines meet, which matters for the map lines and the meshes that share them.
- **Hausdorff guarantee.** The input and the output are within [Hausdorff distance](/hausdorff-distance/) $\varepsilon$ of each other. The [Fréchet distance](/frechet-distance/) can be larger: the input $(0, 0), (10, 0), (5, 0), (20, 0)$ goes back on itself, RDP with $\varepsilon = 1$ returns the segment from $(0, 0)$ to $(20, 0)$, and the Fréchet distance is $2.5$.
- **Not minimal.** The output can have more points than needed, as the example shows. Ramer wrote that the result is small but not a minimum.
- **Not simple.** The output of a simple polyline can cross itself, or cross another line of the same map. Testing for this is the [polygon simplicity test](/polygon-simplicity-test/).
- **Nested results.** If each kept point is given the distance at which it was kept, the points with values above $\varepsilon'$ form the RDP output for $\varepsilon'$ only when the values decrease down the split tree. They do not always: a point kept in a later split can have a larger distance than its parent. For a strict hierarchy, keep the running minimum along the path from the root.
- **Any dimension.** The method needs only a distance to a segment, so it works for curves in $\mathbb{R}^3$ and higher.
- **Deterministic.** With the rule for ties of line L5, the output is a function of the input.

## Variants and improvements

- **Path hulls (Hershberger and Snoeyink 1992).** For planar input and the distance to the line of the chord, the farthest point is a vertex of the [convex hull](/convex-hull/) of the subpath. They keep the hulls of the two halves of the subpath, find the farthest point by a tangent search in $O(\log n)$, and get $O(n \log n)$ in the worst case. The 1994 note gives the same result in short form.
- **A fixed number of points.** Keep the pairs in a [priority queue](/priority-queue/) keyed by their largest distance, and always split the pair with the largest key. Stop after $k$ points. This gives the best RDP answer for each $k$ and a ranking of all points.
- **Distance measures.** The perpendicular distance to the line, the vertical distance for time series, and the segment distance of this page give different outputs. Only the segment distance gives the guarantee of the proof for every input.
- **Closed curves.** A closed polyline has $P_0 = P_{n-1}$, so the first chord is one point. The segment distance then measures the distance to $P_0$, and the first split is at the point farthest from $P_0$. Another common start is to cut the ring at two far apart points.
- **Optimal answers.** The minimum number of points for a tolerance comes from a shortest path in the shortcut graph, with $O(n^2)$ or more time. See [polygon simplification](/polygon-simplification/).
- **Area instead of distance.** The [Visvalingam-Whyatt algorithm](/visvalingam-whyatt/) removes points one at a time by the area of the triangle they form with their neighbors. It removes small features first and keeps the general shape, where RDP keeps the sharp peaks.

## When to use it

Use it to thin map lines, GPS tracks, digitized contours and stroke input, when the error bound must hold point by point, and when the end points must stay. It is a good default for a one time simplification with a given tolerance. Use the path hull version for long planar lines with bad splits. Use an optimal method when the number of points matters more than speed, and the Visvalingam-Whyatt algorithm when the result must look smooth at small scales. Add a simplicity check when the output must not cross itself.

## Pitfalls

- **The line distance instead of the segment distance.** With the distance to the infinite line, a point outside the chord can lie on the line and be removed. For $(0, 0), (5, 0), (-10, 0)$ the line version removes $(5, 0)$ for every $\varepsilon$, but it is 5 away from the output.
- **A closed polyline.** If $P_0 = P_{n-1}$, the line through the chord is not defined, and a formula that divides by its length fails. The segment distance handles it.
- **Recursion depth.** The recursive form can go $n - 2$ calls deep, as in the worst case above. In Python this passes the default limit of 1000 calls for long tracks. Use an explicit stack.
- **Square roots.** Compare $\delta^2$ with $\varepsilon^2$. This saves a square root per point and keeps integer input exact.
- **Expecting a minimum.** The output depends on the first split, and RDP never takes a point back. For a fixed tolerance, its count can be far from the optimum.
- **Ties in floating point.** Two points with equal distances can swap their order after rounding. This changes the output, but not the guarantee.

## Implementations

The Python file in this folder has `rdp_indices(points, epsilon)` and `ramer_douglas_peucker(points, epsilon)`, which follow the pseudocode with an explicit stack and an exact squared distance to the segment. The tests check the example, the segment distance against a direct minimization in fractions, the tolerance for every removed point with exact distances, and the output against the recursive form on random integer and rational polylines in two and three dimensions.

## History

Urs Ramer described the method in 1972 for the polygonal approximation of plane curves in pattern recognition. David Douglas and Thomas Peucker published it independently in 1973 for the reduction of digitized map lines, in The Canadian Cartographer. That journal was later renamed Cartographica, and some citations give the later name. In cartography the method became the standard for line generalization. In 1992 John Hershberger and Jack Snoeyink showed that the usual implementation is quadratic in the worst case, and they gave the path hull method with $O(n \log n)$ worst case time.

## References
