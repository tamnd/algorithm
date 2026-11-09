---
tag: BG3ZFX
kind: algorithm
slug: minkowski-sum-convex-polygons
name: Minkowski sum of convex polygons
aliases:
- merge of edge sequences
- merging edge sequences
- convolution of convex polygons
- Minkowski addition of convex polygons
area: geometry/polygons
level: core
summary: Merges the sorted edge directions of two convex polygons in O(n + m) time.
solves: [minkowski-sum]
model: real-ram
complexity:
  vars: {n: the number of vertices of the first polygon, m: the number of vertices of the second polygon}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1983
  people: [Leonidas J. Guibas, Lyle Ramshaw, Jorge Stolfi, Tomás Lozano-Pérez]
  note: Guibas, Ramshaw and Stolfi described the sum of convex polygons as a merge of edge sequences in their 1983 kinetic framework, and Lozano-Pérez used such sums for configuration space obstacles in the same year.
prereqs: [convex-polygon, minkowski-sum, cross-product]
see_also: [configuration-space, convex-collision-detection, gjk-algorithm, support-function, rotating-calipers, convex-hull, motion-planning, offset-curve]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 13, Section 13.3, Minkowski Sums (the algorithm MinkowskiSum for convex polygons, its O(n + m) bound, and sums of nonconvex polygons)
  - paper: "Leonidas J. Guibas, Lyle Ramshaw and Jorge Stolfi, A kinetic framework for computational geometry, Proceedings of the 24th IEEE Symposium on Foundations of Computer Science, 1983, 100 to 111"
    locator: the convolution of polygonal tracings, and the merge of the edge sequences for convex polygons
  - paper: "Tomás Lozano-Pérez, Spatial planning: a configuration space approach, IEEE Transactions on Computers C-32(2), 1983, 108 to 120"
    locator: the configuration space obstacles of a translating convex polygon, computed by sorting edge directions
  - url: https://cp-algorithms.com/geometry/minkowski.html
    title: cp-algorithms, Minkowski sum of convex polygons
    locator: the whole article (the lowest vertex as the start, the merge by polar angle, and the distance between two convex polygons)
---

The Minkowski sum of two convex polygons $P$ and $Q$ is the convex polygon $P \oplus Q = \{p + q : p \in P, q \in Q\}$. This algorithm computes it in $O(n + m)$ time, for polygons with $n$ and $m$ vertices. It uses one fact: the edges of $P \oplus Q$ are the edges of $P$ and of $Q$, taken in the order of their directions. So the algorithm starts at the sum of the two lowest vertices and walks around, always taking the next edge, from either polygon, with the smaller angle, as in the merge step of [merge sort](/merge-sort/). The result has at most $n + m$ vertices. It is the basic step of [configuration space](/configuration-space/) planning for a translating robot and of [collision detection](/convex-collision-detection/) between convex shapes.

## In plain words

Take a convex shape and slide a second convex shape all around it, with a fixed point of the second shape always on the first. The region that the second shape sweeps out is the sum.

The outline of the sum is made of the sides of both shapes. Each side of the first shape appears once, and each side of the second shape appears once, and they appear in the order of the direction they point. So you can build the outline the way you would merge two sorted lists: start at the bottom, look at the next side of each shape, take the one that turns less, and repeat. Two sides that point the same way join into one longer side.

## The problem

The input is two convex polygons $P = p_0, \ldots, p_{n-1}$ and $Q = q_0, \ldots, q_{m-1}$ in counterclockwise order, with $n, m \ge 1$. Points are $p = (x, y)$, and $\operatorname{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn. The polygons may have collinear or repeated consecutive vertices, and they may be degenerate: a single point ($n = 1$), or a segment given by its two endpoints. The output is $P \oplus Q$ as a strictly convex polygon in counterclockwise order that starts at its *lowest* vertex, the one with the least $y$ and, among those, the least $x$. If the sum is a segment, the output is its two endpoints, and if it is a point, that point.

**Angle order.** For a nonzero vector $d$, let $\operatorname{half}(d) = 0$ if $d_y > 0$ or ($d_y = 0$ and $d_x > 0$), and $1$ otherwise. Then $d \preceq d'$ (the angle of $d$ in $[0, 2\pi)$ is at most that of $d'$) if and only if $\operatorname{half}(d) < \operatorname{half}(d')$, or the halves are equal and $d \times d' \ge 0$. Two vectors have the *same direction* if their halves are equal and $d \times d' = 0$. These tests are exact with integer or rational input.

## The algorithm

```pseudo id=main
MINKOWSKI-SUM-CONVEX(P[0 .. n − 1], Q[0 .. m − 1])
L1  rotate P and Q so that P[0] and Q[0] are their lowest vertices (least y, then least x)
L2  E ← the nonzero vectors P[i+1] − P[i], F ← the nonzero vectors Q[j+1] − Q[j]   (indices mod n and mod m)
L3  D ← empty list, i ← 0, j ← 0
L4  while i < |E| or j < |F| do
L5      if j = |F| or (i < |E| and E[i] ⪯ F[j]) then d ← E[i], i ← i + 1
L6      else d ← F[j], j ← j + 1
L7      if D is not empty and d has the same direction as the last vector of D then add d to it else append d to D
L8  R ← [P[0] + Q[0]]; for each vector d of D except the last, append (last point of R) + d to R
L9  return R
```

After line L1, the edge vectors of each polygon, read in order from its lowest vertex, have angles that never decrease in $[0, 2\pi)$: the first edge leaves the lowest vertex upward or to the right, and the last one arrives from above. Lines L4 to L6 merge the two sorted lists, and line L7 joins vectors with the same direction, so $D$ lists the edges of the sum with strictly increasing angles. Line L8 walks along $D$ from the lowest vertex of the sum, which is $P[0] + Q[0]$. The last vector of $D$ leads back to the start, so it adds no new vertex.

## Example

Let $P = (0,0), (2,0), (0,2)$, a triangle, and let $Q = (4,2), (3,2), (3,1), (4,1)$, a unit square given from its top right corner. Line L1 rotates $Q$ to start at $(3,1)$. Then $E = (2,0), (-2,2), (0,-2)$ and $F = (1,0), (0,1), (-1,0), (0,-1)$, with angles $0°, 135°, 270°$ and $0°, 90°, 180°, 270°$.

| step | $E[i]$ | $F[j]$ | taken | $D$ after the step |
|---|---|---|---|---|
| 1 | (2,0) | (1,0) | $E$: equal angles, $E$ first | (2,0) |
| 2 | (-2,2) | (1,0) | $F$ | (3,0) |
| 3 | (-2,2) | (0,1) | $F$ | (3,0), (0,1) |
| 4 | (-2,2) | (-1,0) | $E$ | (3,0), (0,1), (-2,2) |
| 5 | (0,-2) | (-1,0) | $F$ | (3,0), (0,1), (-2,2), (-1,0) |
| 6 | (0,-2) | (0,-1) | $E$: equal angles | (3,0), (0,1), (-2,2), (-1,0), (0,-2) |
| 7 | none | (0,-1) | $F$ | (3,0), (0,1), (-2,2), (-1,0), (0,-3) |

In steps 2 and 7 the new vector has the direction of the last one, so line L7 adds them. Line L8 starts at $(0,0) + (3,1) = (3,1)$ and adds the first four vectors: $R = (3,1), (6,1), (6,2), (4,4), (3,4)$. The last vector $(0, -3)$ leads from $(3,4)$ back to $(3,1)$. This is the convex hull of the twelve sums $p + q$, a pentagon with $3 + 4 - 2 = 5$ vertices, because two pairs of edges were parallel.

## Correctness

For a direction $u$, let $F_K(u)$ be the set of points of $K$ where $u \cdot x$ is largest. As $\max_{p + q} u \cdot (p + q) = \max_p u \cdot p + \max_q u \cdot q$, the maximum over the sum is reached exactly at sums of maximizers: $F_{P \oplus Q}(u) = F_P(u) \oplus F_Q(u)$. For $u$ the outward normal of a direction $d$, $F_K(u)$ is a segment parallel to $d$, possibly a single point, and the edge of $K$ with direction $d$ is that segment. Sums of parallel segments add their lengths, so the edge of $P \oplus Q$ with direction $d$ is the sum of the edges of $P$ and $Q$ with direction $d$, and it exists if and only if one of them does. The lowest vertex of the sum is the sum of the lowest vertices, by the same argument for the lexicographic order. Walking around a convex polygon from its lowest vertex meets its edges in increasing angle order, so the walk of line L8 traces exactly the boundary of $P \oplus Q$. The [full proof](proofs/correctness/) gives the details and the degenerate cases.

## Complexity

- **Time.** Line L1 finds the lowest vertices in $O(n + m)$ time, and line L2 builds at most $n + m$ vectors. Each iteration of the loop consumes one vector, so lines L4 to L7 run $|E| + |F| \le n + m$ times, and line L8 takes $O(n + m)$ time. The total is $\Theta(n + m)$.
- **Space.** $\Theta(n + m)$ for $E$, $F$, $D$ and the output. With index arithmetic in place of the lists $E$ and $F$, the extra space is $O(1)$ besides the output.
- **Output size.** The sum has at most $n + m$ vertices, and exactly $n + m$ when the two polygons are strictly convex and have no parallel edges with the same direction.
- **Arithmetic.** The angle tests have degree 2, and the output coordinates are sums of input coordinates. With integer input, every value is exact.

## Properties

- **Exact.** No angles and no trigonometric functions are computed; the merge uses only signs of cross products.
- **Commutative and translation-equivariant.** $P \oplus Q = Q \oplus P$, and translating $P$ by $t$ translates the sum by $t$.
- **Strictly convex output.** Line L7 joins collinear edges, so the output has no straight vertices, even when the inputs have them.
- **Area.** The area of $P \oplus Q$ is $\operatorname{area}(P) + \operatorname{area}(Q) + 2 V(P, Q)$, where the mixed area $V(P, Q) \ge 0$. In particular the area of the sum is at least the sum of the areas.

## Variants and improvements

- **Collision detection.** $P$ and $Q$ intersect if and only if the origin is in $P \oplus (-Q)$, where $-Q$ is $Q$ reflected through the origin. The distance between two disjoint convex polygons is the distance from the origin to $P \oplus (-Q)$. The [GJK algorithm](/gjk-algorithm/) uses the same idea without building the sum.
- **Configuration space.** For a robot $Q$ that translates with reference point at the origin, the positions where it hits the obstacle $P$ form $P \oplus (-Q)$; see [configuration space](/configuration-space/) and [motion planning](/motion-planning/).
- **Many polygons.** The sum of $k$ convex polygons with $N$ vertices in all is a $k$-way merge of their edge lists, in $O(N \log k)$ time with a heap.
- **Nonconvex polygons.** Split each polygon into convex pieces, add every pair of pieces with this algorithm, and take the union of the results; see [Minkowski sum](/minkowski-sum/) for the bounds.
- **Offsetting.** The sum with a disk of radius $r$ rounds every vertex with a circular arc and moves every edge out by $r$; see [offset curve](/offset-curve/).
- **Support functions.** In terms of [support functions](/support-function/), $h_{P \oplus Q} = h_P + h_Q$. Algorithms that work only through support queries can use the sum without computing it.

## When to use it

Use it to build the sum of two convex polygons explicitly, for configuration space obstacles, for computing the distance or the penetration depth between two convex polygons, or as a building block for sums of nonconvex polygons. If only one question is asked of the sum, such as whether two convex polygons intersect, a direct test such as the [separating axis theorem](/separating-axis-theorem/) or GJK is simpler.

## Pitfalls

- **Different start vertices.** Both polygons must start at the vertex that comes first for the same direction, here the lowest. Starting $P$ at its lowest vertex and $Q$ at an arbitrary vertex gives a polygon of the right shape at the wrong place, or a self-intersecting one.
- **Clockwise input.** The edge directions then decrease, and the merge produces garbage. Check the orientation once with the [signed area](/polygon-area/).
- **Ties in the angle order.** Parallel edges with the same direction must become one edge of the sum. If they are not joined, the output has a straight vertex, which breaks later code that needs strict convexity.
- **Angles in floating point.** Sorting by `atan2` can order two nearly parallel edges the wrong way, which makes a reflex vertex in the output. The half-plane and cross product test is exact.
- **The closing vector.** The vectors of $D$ sum to zero, and adding the last one returns to the start. Appending that point gives a duplicate vertex.
- **Degenerate inputs.** A point has no edges and a segment has two opposite edges; both work with the algorithm above, but code that assumes $n \ge 3$ fails on them.

## Implementations

## History

The sum of sets of vectors goes back to Hermann Minkowski's work on convex bodies around 1900. In computational geometry, Guibas, Ramshaw and Stolfi (1983) described the convolution of polygonal tracings, which for convex polygons is the merge of the two edge sequences by angle. In the same year Lozano-Pérez used such sums to build the configuration space obstacles of a translating robot. The textbook form with the lowest vertices as start points is in de Berg, Cheong, van Kreveld and Overmars.

## References
