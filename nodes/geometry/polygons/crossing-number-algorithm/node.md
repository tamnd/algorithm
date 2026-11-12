---
tag: 6ADJ3H
kind: algorithm
slug: crossing-number-algorithm
name: Crossing number algorithm
aliases:
- ray crossing test
- parity test for point in polygon
area: geometry/polygons
level: intro
summary: Cast a ray from the query point and count edge crossings; an odd count means inside. O(n) per query.
solves: [point-in-polygon]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1962
  people: [M. Shimrat]
  note: Shimrat published the ray crossing test as Algorithm 112 in the Communications of the ACM in 1962, and Hacker's certification later that year corrected a flaw in it.
prereqs: [point-in-polygon, orientation-test, simple-polygon, jordan-curve-theorem]
see_also: [winding-number-algorithm, point-in-convex-polygon, polygon, geometry-primitives, planar-point-location, slab-method-point-location, polygon-clipping]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Section 7.4, Point in Polygon (the procedure InPoly, the half-open straddle rule, and the second ray to the left that detects the boundary)
  - paper: doi:10.1016/S0925-7721(01)00012-8
    title: Kai Hormann and Alexander Agathos, The point in polygon problem for arbitrary polygons, Computational Geometry 20(3), 2001
    locator: the whole paper (crossing number and winding number, the degenerate cases, and the signed crossing count)
  - book: "Eric Haines, Point in polygon strategies, in Paul S. Heckbert (editor), Graphics Gems IV, Academic Press, 1994"
    locator: the whole article (the crossings test with the half-open rule, compared with angle summation and other methods)
  - paper: "M. Shimrat, Algorithm 112: Position of point relative to polygon, Communications of the ACM 5(8), 1962"
    locator: the algorithm (the ray crossing test)
---

The crossing number algorithm decides whether a point $q$ lies inside, outside or on the boundary of a polygon. It follows a horizontal ray from $q$ to the right and counts the edges that the ray crosses: an odd count means inside, an even count means outside. It solves [point in polygon](/point-in-polygon/) in $\Theta(n)$ time and $O(1)$ extra space, and with a half-open rule for vertices on the ray and an exact [orientation test](/orientation-test/) it is correct on every degenerate input, including rays through vertices and along horizontal edges. On a self-intersecting polygon it computes the even-odd fill rule.

## In plain words

Stand at the point and walk to the right in a straight line, for ever. Each time you cross the fence of the region, you change from inside to outside or from outside to inside. Far away you are surely outside. So if you cross the fence an odd number of times, you started inside; if an even number, outside.

The hard part is the special cases. Your path can pass exactly through a corner of the fence, or run along a piece of fence. The fix is to pretend that each corner at the height of your path is a tiny bit lower than the path. Then the path never touches a corner, and the count is always right. Before counting, check whether the point is on the fence itself.

## The problem

The input is a polygon $V = v_0, \ldots, v_{n-1}$, a cyclic list of points with edges $v_i v_{i+1}$ (indices modulo $n$), and a query point $q$. Points are $p = (x, y)$, and $\operatorname{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn. The output is BOUNDARY if $q$ lies on an edge or a vertex, INSIDE if $q$ is in the interior, and OUTSIDE otherwise. For a [simple polygon](/simple-polygon/) the interior is the bounded component of the complement of the boundary, which exists by the [Jordan curve theorem](/jordan-curve-theorem/). For any other closed polygon, the algorithm uses the even-odd rule: $q$ is inside if the crossing count is odd. The vertex order (clockwise or counterclockwise) does not matter, and no general position is assumed.

## The algorithm

```pseudo id=main
CROSSING-NUMBER(V[0 .. n − 1], q)
L1  c ← 0                                        ▷ parity of the crossings so far
L2  for i ← 0 to n − 1 do
L3      a ← V[i], b ← V[(i + 1) mod n]
L4      if q lies on the closed segment ab then return BOUNDARY
L5      if (a.y > q.y) ≠ (b.y > q.y) then          ▷ ab straddles the line y = q.y
L6          s ← (b − a) × (q − a)
L7          if (s > 0) = (b.y > a.y) then c ← 1 − c    ▷ the crossing is right of q
L8  if c = 1 then return INSIDE else return OUTSIDE
```

Line L4 is the on-segment test: $(b - a) \times (q - a) = 0$ and $(q - a) \cdot (q - b) \le 0$. Line L5 is the *half-open rule*: an endpoint with $y = q_y$ counts as below the ray, so an edge is used only when exactly one endpoint is strictly above the line $y = q_y$. A horizontal edge never straddles. A vertex on the ray counts for both of its edges when they go up from it, for neither when they go down, and for exactly one when the boundary passes through it from below to above. Line L7 tests whether the crossing point lies to the right of $q$ without a division: for an upward edge, $q$ is left of the edge exactly when $s > 0$; for a downward edge, the opposite holds.

## Example

Take $V = (0,0), (10,0), (10,8), (7,4), (5,4), (4,8), (2,4), (0,8)$ and $q = (1, 4)$. The top of the polygon has a V-shaped notch with its tip at $(2, 4)$ and a flat notch with bottom edge $(7,4)$ to $(5,4)$, both at the height of $q$. So the ray passes through a vertex and along a horizontal edge.

| $i$ | edge | straddles $y = 4$? | $s$ | crossing $x^*$ | counted | $c$ |
|---|---|---|---|---|---|---|
| 0 | (0,0) to (10,0) | no | | | | 0 |
| 1 | (10,0) to (10,8) | yes | 72 | 10 | yes | 1 |
| 2 | (10,8) to (7,4) | yes | -24 | 7 | yes | 0 |
| 3 | (7,4) to (5,4) | no (horizontal) | | | | 0 |
| 4 | (5,4) to (4,8) | yes | 16 | 5 | yes | 1 |
| 5 | (4,8) to (2,4) | yes | -4 | 2 | yes | 0 |
| 6 | (2,4) to (0,8) | yes | 4 | 2 | yes | 1 |
| 7 | (0,8) to (0,0) | yes | 8 | 0 | no | 1 |

The final $c = 1$, so $q$ is INSIDE. The tip $(2, 4)$ of the V-notch is counted twice, by edges 5 and 6, which is right: the ray only touches the boundary there. The endpoints $(7,4)$ and $(5,4)$ of the horizontal edge each count once, through edges 2 and 4. Other queries on the same polygon: $(6, 6)$, in the flat notch, gives OUTSIDE; $(3, 4)$ gives INSIDE; $(6, 4)$ and $(2, 4)$ give BOUNDARY at line L4; $(11, 4)$ gives OUTSIDE.

## Correctness

The proof has two parts. Line L4 returns exactly when $q$ is on the boundary, and line L7 flips $c$ exactly for the straddling edges whose crossing point is right of $q$, because $s = (b_y - a_y)(x^* - q_x)$. The half-open rule gives the same count as a ray at height $q_y + \varepsilon$ for every small $\varepsilon > 0$, which passes through no vertex. The parity of that count is constant on each component of the complement of the boundary and flips across an edge, so for a simple polygon it is 1 exactly on the bounded component. The [full proof](proofs/correctness/) gives each step and the case of non-simple polygons.

## Complexity

- **Time.** The loop runs at most $n$ times, and each iteration does a constant number of additions, multiplications and comparisons, so the time is $O(n)$. When $q$ is not on the boundary, all $n$ edges are read, so the worst case is $\Theta(n)$. In the [real RAM](/real-ram/) this is optimal for a single query without preprocessing: an algorithm that does not read some edge can be fooled by a polygon with a thin spike at that edge that reaches around $q$.
- **Space.** $\Theta(1)$ besides the input: the parity bit and two vertices.
- **Arithmetic.** Each predicate has degree 2. With integer coordinates of absolute value below $B$, every intermediate value has absolute value at most $8B^2$.
- **Many queries.** With $\Theta(n \log n)$ preprocessing (a [slab](/slab-method-point-location/) or [trapezoidal map](/trapezoidal-map/) structure), each query takes $O(\log n)$ time; see [planar point location](/planar-point-location/).

## Properties

- **Exact.** With integer or rational input, all decisions are exact; no division and no tolerance is needed.
- **Orientation-free.** The answer does not depend on whether the polygon is given clockwise or counterclockwise.
- **Even-odd semantics.** On a self-intersecting polygon it returns the even-odd rule, which differs from the nonzero winding rule where the boundary winds twice around a region, as in the middle of a pentagram.
- **Streaming.** It reads the edges once, in any order, so it works on a polygon given as an unordered list of edges, or on a polygon with holes given as several rings.

## Variants and improvements

- **Winding number.** Count $+1$ for each upward crossing right of $q$ and $-1$ for each downward one. The sum is the winding number, and the [winding number algorithm](/winding-number-algorithm/) uses it for the nonzero fill rule. It costs the same.
- **Two rays for the boundary.** O'Rourke's InPoly counts crossings of the ray to the right and of the ray to the left. If the two parities differ, $q$ is on the boundary. This replaces the on-segment test of line L4.
- **Polygons with holes.** Run the loop over the edges of all rings. The parity counts crossings of every ring, which gives the even-odd interior of the polygon with holes.
- **Convex polygons.** For a convex polygon, [point in convex polygon](/point-in-convex-polygon/) needs only $O(\log n)$ time.
- **Grid acceleration.** Graphics code often buckets the edges by $y$, so a query visits only the edges that straddle its height. The worst case stays $\Theta(n)$.

## When to use it

Use it for one query, or for a few queries, on a polygon of any shape, including polygons with holes and self-intersecting outlines when the even-odd rule is the intended meaning. Use the winding number instead when the polygon can wind around a region more than once and the nonzero rule is wanted. For many queries on one polygon, build a [point location](/planar-point-location/) structure; for a convex polygon, use binary search.

## Pitfalls

- **A ray through a vertex.** Testing $a_y \le q_y \le b_y$ (closed on both sides) in line L5 counts the vertex twice when the boundary passes through it, and gives the wrong parity. Line L5 must be half-open: an endpoint at height $q_y$ counts as below.
- **Horizontal edges.** Computing $x^*$ with a division by $b_y - a_y$ fails for a horizontal edge. With the half-open rule such an edge never straddles, so line L6 is never reached for it.
- **Points on the boundary.** Without line L4, a point on an edge gets an arbitrary answer: the bottom edge of a square is "inside" and the top edge "outside". Decide whether the boundary belongs to the polygon, and test it first.
- **Floating-point crossings.** Computing $x^* = a_x + (b_x - a_x)(q_y - a_y)/(b_y - a_y)$ in floating point and comparing it with $q_x$ can give the wrong side when $q$ is very close to an edge. The sign test of line L7 is exact with integer or rational input.
- **Strict test in line L7.** Using $s \ge 0$ in line L7 counts an edge through $q$ as a crossing, which is wrong without line L4.

## Implementations

## History

The parity rule follows from the [Jordan curve theorem](/jordan-curve-theorem/) for polygons. Shimrat published it as Algorithm 112 in the Communications of the ACM in 1962, and Richard Hacker's certification later that year corrected a flaw in it. Haines (1994) compared the crossings test with angle summation, half-plane tests and grid methods for use in graphics. O'Rourke's book gives the half-open rule in the form used here. Hormann and Agathos (2001) treated the degenerate cases and the winding number together for arbitrary polygons.

## References
