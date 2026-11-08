---
tag: ACJQR7
kind: algorithm
slug: melkman-algorithm
name: Melkman's algorithm
aliases:
- Melkman's convex hull of a simple polyline
- Melkman's deque algorithm
- convex hull of a simple polygon
area: geometry/convex-hulls
level: advanced
summary: Online O(n) hull of a simple polyline using a deque and no sorting.
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of polyline vertices, h: the number of hull vertices}
  time: {best: Θ(n), worst: Θ(n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false, output-sensitive: false}
history:
  year: 1987
  people: [Avraham A. Melkman]
  note: Melkman gave the deque method in Information Processing Letters in 1987, after several earlier linear-time methods for simple polygons, some of which were later found to fail on special inputs.
prereqs: [convex-hull-problem, orientation-test, deque, simple-polygon]
see_also: [graham-scan, andrew-monotone-chain, convex-polygon, polygon-simplicity-test, convex-hull-lower-bound, funnel-algorithm, upper-and-lower-hull, dynamic-convex-hull]
sources:
  - paper: doi:10.1016/0020-0190(87)90086-X
    title: Avraham A. Melkman, On-line construction of the convex hull of a simple polyline, Information Processing Letters 25(1), 1987
    locator: the whole paper (the deque, the two tests at its ends, and the correctness argument)
  - paper: "Ronald L. Graham and F. Frances Yao, Finding the convex hull of a simple polygon, Journal of Algorithms 4(4), 1983"
    locator: the earlier linear-time stack method for simple polygons
  - paper: "D. T. Lee, On finding the convex hull of a simple polygon, International Journal of Computer and Information Sciences 12(2), 1983"
    locator: the linear-time method for simple polygons that starts at an extreme vertex
---

Melkman's algorithm computes the [convex hull](/convex-hull/) of a simple polyline, a path of segments that does not cross itself, in $O(n)$ time for $n$ vertices. It reads the vertices in their path order, needs no sorting, and keeps the hull of the part read so far in a [deque](/deque/), so it is an online algorithm. A new vertex is tested only against the two hull edges at the ends of the deque. It is the standard way to get the hull of a [simple polygon](/simple-polygon/) in linear time, which beats the $\Omega(n \log n)$ bound for unordered points because the path order already carries much of the needed information.

## In plain words

You walk along a path that never crosses itself, and you keep a fence around everything you have seen so far. The fence is stored as a list whose two ends are the same corner: the last corner you added.

At each new point, look only at the two fence sides that touch that corner. If the point is on the inner side of both, it is inside the fence, and you go on. If not, the point is outside. Then remove fence corners from the front end while the point makes them useless, do the same at the back end, and put the new point at both ends.

Why are two sides enough? Because the path cannot cross itself, it can only leave the fence near the last corner. Other parts of the fence are blocked by the earlier path.

## The problem

The input is a list $V = v_0, \ldots, v_{n-1}$ of points that forms a **simple polyline**: two segments $[v_a, v_{a+1}]$ and $[v_b, v_{b+1}]$ with $a < b$ meet only when $b = a + 1$, and then only at $v_{a+1}$. A vertex equal to the one before it is ignored. The vertices of a simple polygon, listed once around in either direction without repeating the first one, form a simple polyline. The output is the list of the vertices of $\operatorname{conv}(V)$ in counterclockwise order, starting at the lexicographically smallest one. A point in the middle of a hull edge is not reported. With all points on one line the output is the two end points.

Notation: $n$ is the number of vertices and $h$ the number of hull vertices. $D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$ is the [orientation test](/orientation-test/); $D > 0$ means that $r$ is strictly left of the directed line $pq$. The deque is written $Q = \langle d_b, \ldots, d_t \rangle$, bottom first. It always has $d_b = d_t$, the **top**, and $d_b, \ldots, d_{t-1}$ is the hull in counterclockwise order. General position is not assumed: collinear vertices, points on hull edges and a collinear start are all handled, with exact integer arithmetic. The simple-polyline condition is required and is not checked.

## The algorithm

```pseudo id=main
MELKMAN(V)
L1  ignore every vertex of V that equals the vertex before it
L2  k ← the smallest index with v_0, v_{k−1}, v_k not collinear; if there is none, return the two end points of V (or its one point)
L3  if D(v_0, v_{k−1}, v_k) > 0 then Q ← ⟨v_k, v_0, v_{k−1}, v_k⟩ else Q ← ⟨v_k, v_{k−1}, v_0, v_k⟩
L4  for i ← k + 1 to n − 1 do
L5      v ← v_i
L6      if D(d_{t−1}, d_t, v) ≥ 0 and D(d_b, d_{b+1}, v) ≥ 0 then continue
L7      while D(d_{t−1}, d_t, v) ≤ 0 do pop d_t
L8      push v on the top
L9      while D(d_b, d_{b+1}, v) ≤ 0 do pop d_b
L10     push v on the bottom
L11 return d_b, ..., d_{t−1}, rotated to start at the lexicographically smallest point
```

- **Line L2.** A simple polyline that starts on one line moves in one direction along it, since turning back would overlap the previous segment. So the hull of the collinear start is the segment from $v_0$ to $v_{k-1}$.
- **Line L3.** The first triangle is stored counterclockwise, with the new vertex $v_k$ at both ends.
- **Line L6.** The two edges at the top are $(d_{t-1}, d_t)$ and $(d_b, d_{b+1})$. A point on the inner side of both, or on one of their lines, is inside the hull and is skipped. The test is non-strict, so points on the boundary are skipped too.
- **Lines L7 and L9.** A vertex is popped while the new point is on or right of its edge toward the top. This removes the vertices that are inside the new hull or in the middle of a new edge.
- **Lines L8 and L10.** The new point becomes the top, at both ends.

## Example

Take the simple polyline $(0,0)$, $(6,0)$, $(3,2)$, $(2,1)$, $(1,3)$, $(5,5)$, $(-1,4)$, $(0,2)$. The first three points are not collinear, so $k = 2$ and $D((0,0), (6,0), (3,2)) = 12 > 0$. The columns "top" and "bottom" give $D(d_{t-1}, d_t, v)$ and $D(d_b, d_{b+1}, v)$ at line L6.

| $i$ | $v$ | top | bottom | action | $Q$ after the step |
| --- | --- | --- | --- | --- | --- |
| 2 | (3,2) | | | line L3 | (3,2), (0,0), (6,0), (3,2) |
| 3 | (2,1) | 5 | 1 | inside, skip | (3,2), (0,0), (6,0), (3,2) |
| 4 | (1,3) | 1 | −7 | pop (3,2) at the bottom | (1,3), (0,0), (6,0), (3,2), (1,3) |
| 5 | (5,5) | −8 | 10 | pop (1,3) and (3,2) at the top | (5,5), (1,3), (0,0), (6,0), (5,5) |
| 6 | (−1,4) | 31 | −8 | pop (5,5) and (1,3) at the bottom | (−1,4), (0,0), (6,0), (5,5), (−1,4) |
| 7 | (0,2) | 13 | 2 | inside, skip | (−1,4), (0,0), (6,0), (5,5), (−1,4) |

At step 4, the point $(1,3)$ is outside only across the bottom edge $(3,2) \to (0,0)$; the top copy of $(3,2)$ stays, as it is still a hull vertex. At step 5, the point $(5,5)$ removes two vertices at the top. The last point $(0,2)$ lies in a pocket: it is inside the hull but not inside the polyline's region. Line L11 drops the repeated top and starts at the smallest point, which gives $(-1,4)$, $(0,0)$, $(6,0)$, $(5,5)$.

## Correctness

**Theorem.** For a simple polyline, after each step the deque holds the hull of the vertices read so far, counterclockwise, with the last added hull vertex at both ends. So MELKMAN returns the hull vertices of $V$, each once, in counterclockwise order.

The main fact is that only the two top edges need a test. Look at the parts into which the polyline cuts the hull. Every hull vertex lies on the polyline, so each part touches the hull boundary inside at most one edge. The invariant says that the parts that touch the current vertex open only onto the top edges. The next segment starts at the current vertex and cannot cross the polyline, so if it leaves the hull, it leaves through a top edge, and line L6 sees that. When a point is added, the new top edges are the ones at the new point, and the invariant holds again. The pops of lines L7 and L9 remove exactly the vertices whose two edges both face the new point. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

All costs are on the [real RAM](/real-ram/); with integer input every test is exact.

- **Time $\Theta(n)$.** Each vertex is pushed at most twice and line L3 pushes four entries, so there are at most $2n + 4$ pops in total. Every other line costs $O(1)$ per vertex. The bound is the same in the best and the worst case, as each vertex is read once.
- **One step can be slow.** A single vertex can pop $\Theta(n)$ entries, so the bound per vertex is $O(1)$ amortized, not in the worst case.
- **Space.** The deque holds at most $h + 1$ entries at the end, but it can hold up to $n + 1$ entries during the run, so the extra space is $O(n)$.
- **No conflict with the lower bound.** The [lower bound](/convex-hull-lower-bound/) $\Omega(n \log n)$ is for points in arbitrary order. For a simple polyline the order is part of the input, and the hull is found in linear time.

## Properties

- **Online.** After each vertex the deque is the hull of the prefix, and asking for it costs $O(h)$.
- **Exact.** Only orientation tests on input points are used, so integer input needs no rounding.
- **Works from any start.** The first vertex need not be extreme, unlike several earlier methods for polygons.
- **Both directions.** A clockwise or counterclockwise polygon gives the same result; the deque is always counterclockwise.

## Variants and improvements

- **Earlier stack methods.** For a simple polygon, the methods of Lee and of Graham and Yao (1983) start at an extreme vertex and use a stack. Melkman's deque removes the need for the extreme start and makes the method online.
- **Hull of a sorted point set.** Distinct points in lexicographic order form a simple polyline (a monotone one). So Melkman's algorithm also gives the hull of sorted points, like [Andrew's monotone chain](/andrew-monotone-chain/).
- **Funnels.** The [funnel algorithm](/funnel-algorithm/) for shortest paths in a simple polygon keeps two convex chains in a deque and updates them at both ends in a similar way.

## When to use it

Use it when the points come as a simple polygon or a simple polyline, such as the outline of a shape, a drawn stroke or a path that is known not to cross itself. It is also the natural choice when the points arrive one at a time along the path and the hull is needed after each one. For points in arbitrary order, use [Andrew's monotone chain](/andrew-monotone-chain/) or [Graham's scan](/graham-scan/) instead. If simplicity is not known, test it first, see [polygon simplicity test](/polygon-simplicity-test/).

## Pitfalls

- **Input that crosses itself.** The algorithm silently gives a wrong hull. For the path $(0,0)$, $(10,0)$, $(5,10)$, $(5,1)$, $(5,-5)$, the last segment crosses the first one, and the point $(5,-5)$ is on the inner side of both top edges, so it is skipped although it is a hull vertex.
- **Closing the polygon.** Repeating $v_0$ at the end makes the last segment touch $v_0$, which is not a simple polyline. Give each vertex once.
- **A collinear start.** With $v_0, v_1, v_2$ collinear, line L3 cannot form a triangle. Skip to the first vertex off the line, as line L2 does, and use the two end points of the collinear start.
- **Strict tests.** With a strict test in line L6, a point on a top edge is not skipped, and the pops put it into the deque as a vertex in the middle of an edge. For the path $(0,0)$, $(4,0)$, $(0,4)$, $(0,2)$, the strict version returns $(0,2)$ as a vertex on the edge from $(0,4)$ to $(0,0)$. Keep line L6 non-strict and lines L7 and L9 non-strict in the other direction.
- **Floating point.** Near-collinear triples can get the wrong sign. With integer or rational input, use exact orientation tests.

## Implementations

## History

The hull of a simple polygon in linear time was studied from the 1970s on. Several early methods were later shown to fail on some simple polygons, and D. T. Lee and, separately, Ronald Graham and Frances Yao gave correct linear-time methods in 1983. Their methods start at an extreme vertex. In 1987 Avraham Melkman published "On-line construction of the convex hull of a simple polyline" in Information Processing Letters. His deque version works from any start vertex and processes each vertex as it arrives, and it became the standard method.

## References
