---
tag: KB6KXW
kind: algorithm
slug: point-in-convex-polygon
name: Point in convex polygon
aliases:
- binary search point location in convex polygon
- wedge method
- fan binary search
- point in convex polygon test
area: geometry/polygons
level: core
summary: Test a point against a convex polygon in O(log n) by binary search over a fan triangulation from a vertex.
solves: [point-in-polygon]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(log n)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1978
  people: [Michael Ian Shamos]
  note: The wedge method appears in Shamos's 1978 thesis on computational geometry and in the 1985 book by Preparata and Shamos.
prereqs: [convex-polygon, orientation-test, binary-search, point-in-polygon]
see_also: [crossing-number-algorithm, winding-number-algorithm, convex-polygon-point-location, planar-point-location, convex-hull, gjk-algorithm, separating-axis-theorem, geometry-primitives]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.2 (inclusion in a convex polygon by binary search on the angular wedges around an interior point, in O(log n) time)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Section 7.4, Point in Polygon (the remarks on convex polygons)
  - url: https://cp-algorithms.com/geometry/point-in-convex-polygon.html
    title: cp-algorithms, Check if point belongs to the convex polygon in O(log N)
    locator: the whole article (the fan from the first vertex, the binary search on the orientation, and the boundary cases)
---

Point in convex polygon decides in $O(\log n)$ time whether a query point $q$ is inside, outside or on the boundary of a [convex polygon](/convex-polygon/) with $n$ vertices. It draws the diagonals from one vertex $v_0$ to all others, which cut the polygon into a fan of triangles, finds by [binary search](/binary-search/) the wedge of the fan that contains the direction from $v_0$ to $q$, and tests $q$ against the one edge that closes that wedge. Every step is an exact [orientation test](/orientation-test/), and there is no preprocessing: the array of vertices in counterclockwise order is the search structure. A general [point in polygon](/point-in-polygon/) test needs $\Theta(n)$ time.

## In plain words

Stand at one corner of a convex room and look into it. The other corners are spread out in front of you from right to left, in order. Lines from your corner to each other corner cut the room into thin triangles, like slices of a fan.

To find out whether a point is in the room, first find which slice its direction falls into. Because the corners are in order, you can do this by halving: look at the middle corner, decide whether the point is to its left or its right, and throw away half of the slices. Then only one wall can separate the point from you, the far wall of that slice. Check which side of that wall the point is on.

## The problem

The input is a strictly convex polygon $V = v_0, \ldots, v_{n-1}$ with $n \ge 3$, in counterclockwise order, and a query point $q$. Points are $p = (x, y)$, and $\operatorname{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn; below we also write $\operatorname{orient}$ for the value of the cross product itself, which has the same sign. *Strictly convex* means that $\operatorname{orient}(v_{i-1}, v_i, v_{i+1}) > 0$ for every $i$, indices modulo $n$, and that the polygon is [convex](/convex-polygon/); so no three consecutive vertices are collinear. The output is BOUNDARY if $q$ is on an edge or a vertex, INSIDE if $q$ is in the interior, and OUTSIDE otherwise. The algorithm does not check the precondition, as that would take $\Theta(n)$ time.

## The algorithm

```pseudo id=main
POINT-IN-CONVEX-POLYGON(V[0 .. n − 1], q)
L1  if orient(v0, v1, q) < 0 or orient(v0, v_{n−1}, q) > 0 then return OUTSIDE   ▷ outside the wedge at v0
L2  lo ← 1, hi ← n − 1
L3  while hi − lo > 1 do
L4      mid ← ⌊(lo + hi)/2⌋
L5      if orient(v0, v_mid, q) ≥ 0 then lo ← mid else hi ← mid
L6  s ← orient(v_lo, v_hi, q)                                                    ▷ the far edge of the wedge
L7  if s < 0 then return OUTSIDE
L8  if s = 0 or (lo = 1 and orient(v0, v1, q) = 0) or (hi = n − 1 and orient(v0, v_{n−1}, q) = 0) then return BOUNDARY
L9  return INSIDE
```

Line L1 rejects every point that is not in the closed angle of the polygon at $v_0$, between the rays from $v_0$ through $v_1$ and through $v_{n-1}$. This angle is less than $\pi$, so the two tests describe it exactly. Lines L2 to L5 keep the invariant that $q$ is left of or on the ray $v_0 v_{lo}$ and, unless $hi = n - 1$, strictly right of the ray $v_0 v_{hi}$. When they stop, $hi = lo + 1$ and $q$ is in the closed wedge between the rays through $v_{lo}$ and $v_{lo+1}$. Line L6 tests $q$ against the edge $v_{lo} v_{hi}$, which closes the triangle $v_0 v_{lo} v_{hi}$ of the fan. The two sides $v_0 v_{lo}$ and $v_0 v_{hi}$ of that triangle are diagonals, except that $v_0 v_1$ and $v_{n-1} v_0$ are edges of the polygon; line L8 checks whether $q$ is on one of those two edges.

## Example

Take the hexagon $V = (2,0), (5,1), (6,4), (4,6), (1,5), (0,2)$, which is strictly convex (all six turns are 8), and $q = (3, 3)$. Line L1 computes $\operatorname{orient}(v_0, v_1, q) = 8 \ge 0$ and $\operatorname{orient}(v_0, v_5, q) = -8 \le 0$, so $q$ is in the wedge at $v_0 = (2, 0)$.

| step | $lo$ | $hi$ | $mid$ | $v_{mid}$ | $\operatorname{orient}(v_0, v_{mid}, q)$ | action |
|---|---|---|---|---|---|---|
| start | 1 | 5 | | | | |
| 1 | 1 | 5 | 3 | (4,6) | 0 | $lo \leftarrow 3$ |
| 2 | 3 | 5 | 4 | (1,5) | -8 | $hi \leftarrow 4$ |
| end | 3 | 4 | | | | |

Line L6 gives $s = \operatorname{orient}((4,6), (1,5), (3,3)) = 8 > 0$, and neither special edge applies, so $q$ is INSIDE. In step 1, $q$ lies on the diagonal from $v_0$ to $v_3$; the test $\ge 0$ in line L5 sends it to the wedge on the left of that diagonal, and the answer is the same either way.

Other queries on the same hexagon:

- $q = (5, 5)$: the search ends with $lo = 2$, $hi = 3$ and $s = 0$, so $q$ is on the edge $(6,4)$ to $(4,6)$: BOUNDARY.
- $q = (1, 1)$: line L1 finds $\operatorname{orient}(v_0, v_5, q) = 0$, the search ends with $hi = 5$ and $s = 4 > 0$, and line L8 reports BOUNDARY, on the edge $(0,2)$ to $(2,0)$.
- $q = (3, 0)$: $\operatorname{orient}(v_0, v_1, q) = -1 < 0$, so line L1 returns OUTSIDE.
- $q = (8, 2)$: on the line through the edge $v_0 v_1$, beyond $v_1$. Line L1 passes it, the search ends with $lo = 1$, $hi = 2$, and $s < 0$: OUTSIDE.

## Correctness

Let $W$ be the closed angle at $v_0$, $\{q : \operatorname{orient}(v_0, v_1, q) \ge 0 \text{ and } \operatorname{orient}(v_0, v_{n-1}, q) \le 0\}$. The polygon lies in $W$, and the rays from $v_0$ through $v_1, \ldots, v_{n-1}$ appear in counterclockwise order and cut $W$ into $n - 2$ wedges, one for each fan triangle $v_0 v_i v_{i+1}$. The binary search keeps the invariant above and halves $hi - lo$, so it ends with $q$ in the wedge of $v_0 v_{lo} v_{lo+1}$. Inside that wedge, the polygon is exactly the fan triangle, so $q$ is in the polygon if and only if it is on the left of or on the edge $v_{lo} v_{lo+1}$, and on the boundary if and only if it is also on that edge or on one of the triangle sides that are polygon edges. The [full proof](proofs/correctness/) also covers the points on the diagonals and the point $v_0$ itself.

## Complexity

- **Time.** Lines L1, L2 and L6 to L9 take constant time. The loop starts with $hi - lo = n - 2$ and replaces it by $\lceil (hi - lo)/2 \rceil$ or $\lfloor (hi - lo)/2 \rfloor$, so it runs at most $\lceil \log_2 (n - 2) \rceil$ times. The total is $\Theta(\log n)$ orientation tests in the worst case.
- **Space.** $O(1)$ besides the input array.
- **Arithmetic.** Each test has degree 2 in the coordinates. With integer coordinates of absolute value below $B$, the values have absolute value at most $8B^2$.
- **Lower bound.** In a decision tree whose tests are signs of linear functions of $q$, $\Omega(\log n)$ tests are needed for a regular $n$-gon. Each leaf is reached by an intersection of half-planes, a convex set. A convex set that answers OUTSIDE misses the interior of the polygon, so it lies in a closed half-plane that misses the interior. For small $\varepsilon$, such a half-plane cannot contain the points at distance $\varepsilon$ outside the midpoints of two different edges, so there are at least $n$ OUTSIDE leaves and the depth is at least $\log_2 n$.

## Properties

- **Exact.** With integer or rational input, the answer is exact, with no division and no tolerance.
- **No preprocessing.** The counterclockwise vertex array is the search structure; the algorithm only reads $O(\log n)$ of the vertices.
- **Any start vertex.** Any vertex can play the role of $v_0$; rotating the array does not change the answers.
- **Boundary included or excluded.** The three-way answer lets the caller treat the polygon as closed or open.

## Variants and improvements

- **Collinear vertices.** If the polygon is convex but not strictly convex, first delete each vertex $v_i$ with $\operatorname{orient}(v_{i-1}, v_i, v_{i+1}) = 0$. This takes $O(n)$ time once, and the region and its boundary do not change. Without it, a fan triangle can be degenerate and the search can stop in the wrong wedge.
- **Clockwise input.** Reverse the array, or swap the roles of left and right in every test.
- **Interior center.** Preparata and Shamos use a point $c$ strictly inside the polygon, such as the centroid of three vertices, and binary search on the angle of $q - c$. The wedges then cover the whole plane, so there is no line L1, but the angular comparison must handle the wrap around $2\pi$.
- **Many queries, sorted.** If the queries are sorted by angle around $v_0$, a single merge-like scan answers all $m$ of them in $O(n + m)$ time.
- **Tangents and extreme points.** The same binary search idea finds the tangent lines from an outside point and the extreme vertex in a direction in $O(\log n)$ time, which [convex hull](/convex-hull/) maintenance and collision detection use.
- **General subdivisions.** For a subdivision into many convex cells, see [planar point location](/planar-point-location/) and [convex polygon point location](/convex-polygon-point-location/).

## When to use it

Use it for many queries against one convex polygon that is stored as a counterclockwise array, for example a [convex hull](/convex-hull/) or a convex game object. For a single query on a small polygon, the linear test against every edge is simpler and just as fast in practice. For a polygon that is not convex, use the [crossing number](/crossing-number-algorithm/) or [winding number](/winding-number-algorithm/) algorithm, which do not need convexity.

## Pitfalls

- **Non-strict convexity.** A vertex in the middle of a straight edge makes a fan triangle with zero area. Remove such vertices before the first query.
- **Clockwise order.** With clockwise input every test has the wrong sign, and every interior point is reported OUTSIDE. Check the orientation once with the [signed area](/polygon-area/).
- **Points on the boundary rays at $v_0$.** A point on the line of the edge $v_0 v_1$ but beyond $v_1$ passes line L1 and must be rejected by line L6; a point on that line behind $v_0$ is rejected by line L1. Both cases need the exact tests in the right order.
- **Forgetting the two edges at $v_0$.** Line L6 tests only the far edge of the wedge. A point on the edge $v_0 v_1$ or $v_{n-1} v_0$ is on a fan triangle side that is a polygon edge, and line L8 must report it as BOUNDARY, not INSIDE.
- **Floating-point orientation.** In floating point, $\operatorname{orient}$ can have the wrong sign near an edge or a diagonal. A wrong sign near a diagonal only picks the neighboring wedge, but a wrong sign at line L6 gives a wrong answer.

## Implementations

## History

Testing a point against a convex polygon in logarithmic time by searching the angular order of the vertices is one of the first results of computational geometry. It appears in Michael Shamos's 1978 thesis and in the book by Preparata and Shamos (1985), in the form with an interior center point. The form with the fan from a vertex, used here, avoids computing an interior point and is the one usually taught in programming contest material.

## References
