---
tag: 2W87VM
kind: algorithm
slug: sutherland-hodgman
name: Sutherland-Hodgman algorithm
aliases:
- Sutherland-Hodgman clipping
- Sutherland-Hodgman polygon clipping
- reentrant polygon clipping
area: geometry/polygons
level: intro
summary: Clips a polygon against a convex window one half-plane at a time; the subject may be nonconvex, the clip must be convex.
solves: [polygon-clipping]
model: real-ram
complexity:
  vars: {n: the number of subject vertices, m: the number of clip vertices}
  time: {worst: O(n m^2), best: Θ(n + m)}
  space: {extra: O(n m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1974
  people: [Ivan E. Sutherland, Gary W. Hodgman]
  note: Published as reentrant polygon clipping, a pipeline of identical stages, one per clip plane, meant for hardware.
prereqs: [polygon, convex-polygon, orientation-test, line-line-intersection]
see_also: [polygon-clipping, weiler-atherton-algorithm, greiner-hormann-algorithm, vatti-clipping, line-clipping, convex-polygon-intersection, polygon-kernel, winding-number-algorithm]
sources:
  - paper: doi:10.1145/360767.360802
    title: Ivan E. Sutherland and Gary W. Hodgman, Reentrant polygon clipping, Communications of the ACM 17(1), 32 to 42 (1974)
    locator: the whole paper (the clipping of a polygon against one plane at a time, and the pipeline of clippers)
  - paper: doi:10.1145/274363.274364
    title: Günther Greiner and Kai Hormann, Efficient clipping of arbitrary polygons, ACM Transactions on Graphics 17(2), 71 to 83 (1998)
    locator: Section 1, introduction (Sutherland-Hodgman needs a convex clip polygon and can leave degenerate edges)
  - book: isbn:9780201848403
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.14, clipping polygons (the four cases of an edge against a clip edge)
---

The Sutherland-Hodgman algorithm clips a subject [polygon](/polygon/) $S$ with $n$ vertices to a [convex polygon](/convex-polygon/) $C$ with $m$ vertices. It cuts $S$ with one half-plane at a time: for each edge of $C$ it walks around the current polygon once, keeps the vertices on the inner side of the edge's line, and adds a new vertex where an edge crosses the line. After the $m$ passes the result is $S \cap C$, given as one closed vertex list. The subject can be concave or even self-intersecting; the clip polygon must be convex. Each pass is a short loop with one [orientation test](/orientation-test/) per vertex, which made the method a standard stage of the graphics pipeline, where the window is a rectangle or a view volume.

## In plain words

Think of the window as a few straight fences. Take the first fence and walk around the subject shape. Every corner on the good side of the fence stays. Every time your walk crosses the fence, you drop a new corner at the crossing. Corners on the bad side vanish. What you get is the shape cut by that one fence. Then do the same with the next fence, using the new shape, and so on until every fence has cut it.

Because each fence is a straight line, cutting by it is easy. The window must be convex, because only then is the inside of the window the same as the good side of all its fences at once. If the subject leaves the window and comes back, the walk returns along the fence, so the result can contain thin slivers of zero width along the window edges.

## The problem

The input is a closed polygon $S$ given by its vertex list $u_0, \ldots, u_{n-1}$ and a convex polygon $C$ given by $c_0, \ldots, c_{m-1}$ with $m \ge 3$ and nonzero area. The output is a closed vertex list $Q$, possibly empty, such that for every point $q$ off the boundaries of $S$ and $C$, the winding number of $Q$ around $q$ is the winding number of $S$ around $q$ when $q$ is inside $C$, and 0 when $q$ is outside $C$. For a simple subject this means that $Q$ bounds $S \cap C$.

Notation: $\mathrm{orient}(a, b, x) = (b - a) \times (x - a)$, positive when $x$ is to the left of the directed line $ab$. Orient $C$ counterclockwise; then its interior is the set of points to the left of every edge. No general position is needed: vertices of $S$ on a clip line, edges along a clip line, repeated vertices and collinear vertices are all allowed.

## The algorithm

```pseudo id=main
SUTHERLAND-HODGMAN(S, C)                   ▷ C convex and counterclockwise
L1  out ← S
L2  for each edge (c, d) of C do
L3      in ← out;  out ← empty list
L4      for i ← 0 to |in| − 1 do
L5          p ← in[i − 1];  s ← in[i]          ▷ the edge from p to s, cyclically
L6          if orient(c, d, p) and orient(c, d, s) are nonzero with opposite signs then append INTERSECT(ps, line cd) to out
L7          if orient(c, d, s) ≥ 0 then append s to out
L8  return out
```

- **Line L2.** Each edge of $C$ defines the closed half-plane to its left. The passes can run in any order; the original paper runs them as a pipeline of identical stages, one per clip plane, each stage passing vertices to the next as soon as it has them.
- **Line L6.** The crossing point is $p + t(s - p)$ with $t = \mathrm{orient}(c, d, p) / (\mathrm{orient}(c, d, p) - \mathrm{orient}(c, d, s))$. The test is strict, so a vertex exactly on the line does not create a second point at the same place.
- **Line L7.** The vertices on the line count as inside. A pass that starts with an empty list returns an empty list, so the implementation stops early.

The four textbook cases of an edge $ps$ against one clip line are: both inside (emit $s$), leaving (emit the crossing), both outside (emit nothing), entering (emit the crossing and $s$). Lines L6 and L7 cover all four, and the points on the line, in two tests.

## Example

Clip the concave pentagon $S = (0,0), (6,0), (6,6), (3,2), (0,6)$ to the square $C = (1,1), (5,1), (5,5), (1,5)$. The vertex $(3,2)$ is reflex, and the notch above it cuts into the square.

| pass | clip edge | keeps | output |
|---|---|---|---|
| 1 | $(1,1) \to (5,1)$ | $y \ge 1$ | $(0,1), (6,1), (6,6), (3,2), (0,6)$ |
| 2 | $(5,1) \to (5,5)$ | $x \le 5$ | $(0,1), (5,1), (5, \tfrac{14}{3}), (3,2), (0,6)$ |
| 3 | $(5,5) \to (1,5)$ | $y \le 5$ | $(0,5), (0,1), (5,1), (5, \tfrac{14}{3}), (3,2), (\tfrac{3}{4}, 5)$ |
| 4 | $(1,5) \to (1,1)$ | $x \ge 1$ | $(1,1), (5,1), (5, \tfrac{14}{3}), (3,2), (1, \tfrac{14}{3})$ |

In pass 1, the edge from $(0,6)$ to $(0,0)$ leaves the half-plane at $(0,1)$, the edge from $(0,0)$ to $(6,0)$ lies outside, and the edge from $(6,0)$ to $(6,6)$ comes back at $(6,1)$, so $(0,0)$ and $(6,0)$ are replaced by $(0,1)$ and $(6,1)$. In pass 3, the edge from $(3,2)$ to $(0,6)$ leaves at $(\tfrac{3}{4}, 5)$ and the edge from $(0,6)$ to $(0,1)$ comes back at $(0,5)$. The result is a pentagon with a notch, and the [shoelace formula](/shoelace-formula/) gives its area: $\tfrac{44}{3} - \tfrac{16}{3} = \tfrac{28}{3}$.

A subject that leaves the window and comes back gives a zero-width bridge. Clip the U shape $(0,0), (6,0), (6,10), (4,10), (4,2), (2,2), (2,10), (0,10)$ to the band $-1 \le x \le 7$, $4 \le y \le 8$. The output is the single list $(0,8), (0,4), (6,4), (6,8), (4,8), (4,4), (2,4), (2,8)$. It covers the two arms, each a 2 by 4 rectangle, but its edges $(0,4) \to (6,4)$ and $(4,4) \to (2,4)$ overlap: the boundary runs along $y = 4$ under the gap between the arms twice, in opposite directions. The area, 16, and the winding number at every point off the boundary are right, but the output is not a simple polygon.

## Correctness

**Theorem.** For every point $q$ off the boundaries of $S$ and $C$, the output $Q$ has winding number $\operatorname{wind}(S, q)$ around $q$ when $q$ is inside $C$ and 0 when $q$ is outside. So the signed area of $Q$ is $\iint_C \operatorname{wind}(S, q)\, dq$.

The proof is in [proofs/correctness.md](proofs/correctness.md). It first shows what one pass produces: the edges of the output are the parts $e \cap H$ of the input edges, in their own direction, plus segments that lie on the clip line. Then take a ray from $q$. If $q$ is outside the half-plane, a ray pointing away from the line misses the output, so the winding number is 0. If $q$ is inside, a ray that never gets closer to the line stays inside, misses every segment on the line, and crosses the output exactly where it crosses the input, so the winding number is unchanged. Induction over the $m$ passes gives the winding number of $S$ inside the intersection of the $m$ half-planes and 0 outside it. For a convex counterclockwise $C$ that intersection is $C$.

## Complexity

- **One pass.** A pass reads its input once and does $O(1)$ work per vertex, so it costs time linear in the size of its input. The output can be longer than the input: each edge that crosses the line adds a vertex.
- **Convex subject.** The intermediate polygons are convex, and after $k$ passes there are at most $n + k$ vertices. The total time is $O(m(n + m))$.
- **General subject.** The output of pass $k$ consists of at most $n$ pieces of subject edges, plus segments on the clip lines. A pass enters the half-plane at most once per piece of a subject edge on the outside and at most once per run of clip-line segments, so it adds $O(n)$ new edges, and after $k$ passes there are $O(n k)$ vertices. Summing over the passes gives $O(n m^2)$ time and an output of $O(n m)$ vertices. Both can happen: a subject that leaves the window, goes around it on the outside and comes back $t$ times makes $t$ bridges, and each bridge picks up one window corner per pass, so the output has $\Theta(t m)$ vertices and the passes do $\Theta(t m^2)$ work.
- **Best case.** The convexity check reads $C$ once, and the first pass reads $S$ once; if it returns an empty list the rest is skipped. So the time is $\Theta(n + m)$ in the best case.
- **Space.** The two lists of the current pass, $O(n m)$ in the worst case. The pipelined version of the paper keeps only $O(1)$ vertices per stage and so $O(m)$ in all.

## Properties

- **Exact.** On integer or rational input every output coordinate is a rational number computed by one division per crossing. No point is snapped and no tolerance is used.
- **One output list.** The result is always a single closed list. When $S \cap C$ has several components, they are joined by bridges along the boundary of $C$.
- **Order and orientation.** The output keeps the orientation of the subject. Its starting vertex depends on the last clip edge.
- **Online.** Each pass consumes vertices in order and emits them in order, so the passes can run as a pipeline, which was the point of the original design.
- **Clipping order.** The result, as a point set with winding numbers, does not depend on the order of the clip edges, but the vertex list does.

## Variants and improvements

- **Three dimensions.** The same loop clips a polygon against the planes of a convex view volume, with $\mathrm{orient}$ replaced by the signed distance to each plane. This is the form used for clipping before perspective division, with the homogeneous planes $-w \le x \le w$ and so on.
- **Rectangle windows.** For an axis-aligned window, the four orientation tests become coordinate comparisons, and the crossing points need only one division each.
- **Arbitrary clip polygons.** For a concave or self-intersecting clip polygon, or for union and difference, use the [Weiler-Atherton](/weiler-atherton-algorithm/), [Greiner-Hormann](/greiner-hormann-algorithm/) or [Vatti](/vatti-clipping/) algorithms. See [polygon clipping](/polygon-clipping/).
- **Convex subject and convex clip.** The intersection of two convex polygons can be found in $O(n + m)$ time by the sweep of [convex polygon intersection](/convex-polygon-intersection/).
- **Removing bridges.** A post-pass can split the output at overlapping edges on the clip boundary to get separate simple polygons, when the subject is simple.

## When to use it

Use Sutherland-Hodgman when the clip polygon is convex and small, such as a viewport, a view frustum, or a cell of a grid, and when one output list per subject is acceptable. It is short, has no special cases, and handles a concave or self-intersecting subject correctly in the winding number sense. It suits rendering, where the output is filled with a fill rule and zero-width bridges cover no pixels. It does not suit tasks that need the separate pieces of $S \cap C$ as simple polygons, or a concave clip polygon.

## Pitfalls

- **Concave clip polygon.** The passes compute $S$ clipped to the intersection of the edge half-planes, which for a concave $C$ is its [kernel](/polygon-kernel/), not $C$. The result is wrong without any error. The implementation checks convexity and raises an error; a self-intersecting clip polygon like a pentagram passes a local turn test but turns around twice, and the check rejects it by counting the turns.
- **Clockwise clip polygon.** With the wrong orientation every pass keeps the outside, and the result is empty. Fix the orientation with the [shoelace formula](/shoelace-formula/) first.
- **Bridges.** When $S$ leaves and reenters $C$, the output runs along the boundary of $C$ in both directions. Code that expects a simple polygon, for example to compute a perimeter or to triangulate, has to split the output first.
- **Duplicate points.** Testing $\sigma \ge 0$ on one side and $\sigma \le 0$ on the other in line L6 emits a crossing at a vertex that lies on the line, next to the vertex itself. The strict test of line L6 avoids that.
- **Floating point.** In floating point a vertex near a clip line can be classified differently in two passes, and the computed crossing can lie a little outside the window. With integer or rational input and exact arithmetic, as in the implementation, neither happens; the price is that coordinates grow, since each pass adds a division.

## Implementations

The Python version uses exact integers and fractions. It checks that the clip polygon has positive or negative area and is convex, reverses a clockwise clip polygon, and runs the passes. The tests check the worked example, the bridge of the U shape, the rejection of concave, star-shaped and degenerate clip polygons, clockwise clip polygons, empty and fully inside subjects, vertices on a clip line, and, on random lattice subjects that may cross themselves and random convex clip polygons, the signed area against an exact slab integration of the winding number over $C$ and the winding number at many rational sample points.

## History

Ivan Sutherland and Gary Hodgman published the algorithm in 1974 under the name reentrant polygon clipping. They designed it for hardware: a chain of identical clipping stages, one per plane of the view volume, through which the vertices flow. It became the standard polygon clipper of graphics pipelines and textbooks. Its two limits, a convex clip polygon and the bridges in the output, led to the [Weiler-Atherton algorithm](/weiler-atherton-algorithm/) in 1977, to [Vatti's algorithm](/vatti-clipping/) in 1992 and to the [Greiner-Hormann algorithm](/greiner-hormann-algorithm/) in 1998.

## References
