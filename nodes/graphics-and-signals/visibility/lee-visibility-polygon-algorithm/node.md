---
tag: V14M2Q
kind: algorithm
slug: lee-visibility-polygon-algorithm
name: Lee's visibility polygon algorithm
area: graphics-and-signals/visibility
level: advanced
summary: Compute the visibility polygon of a point inside a simple polygon in O(n) time by one scan of the boundary with a stack (Lee 1983, corrected by Joe and Simpson 1987).
solves: [visibility-polygon]
model: real-ram
complexity:
  vars: {n: the number of vertices of the polygon}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, in_place: false, online: false}
history:
  year: 1983
  people: [D. T. Lee, Barry Joe, R. B. Simpson]
  note: Lee published a one-stack linear algorithm in 1983. Joe and Simpson showed in 1987 that it fails when the boundary winds around the viewpoint, and gave a corrected version.
prereqs: [visibility-polygon, simple-polygon, stack, orientation-test]
see_also: [visibility-polygon, weak-visibility-polygon, star-shaped-polygon, polygon-kernel, art-gallery-problem, visibility-graph-of-polygon, funnel-algorithm, angular-sort]
sources:
  - paper: doi:10.1016/0734-189X(83)90065-8
    title: D. T. Lee, Visibility of a simple polygon, Computer Vision, Graphics, and Image Processing 22(2), 1983, pages 207 to 221
    locator: the one-stack linear scan of the boundary
  - paper: doi:10.1007/BF01937271
    title: Barry Joe and R. B. Simpson, Corrections to Lee's visibility polygon algorithm, BIT 27(4), 1987, pages 458 to 473
    locator: the polygons that wind around the viewpoint, on which the algorithms of Lee and of ElGindy and Avis fail, and the corrected algorithm
  - paper: doi:10.1016/0196-6774(81)90019-5
    title: Hossam ElGindy and David Avis, A linear algorithm for computing the visibility polygon from a point, Journal of Algorithms 2(2), 1981, pages 186 to 197
    locator: the first linear algorithm, with three stacks
  - book: isbn:9780195039658
    title: Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987
    locator: Chapter 8, Section 8.2 (Push, Pop and Wait, the angle with winding, the linear time bound)
  - book: isbn:9780521875745
    title: Subir Kumar Ghosh, Visibility Algorithms in the Plane, Cambridge University Press, 2007
    locator: Chapter 2, Section 2.2 (visibility polygon of a point in a simple polygon)
  - url: https://doc.cgal.org/latest/Visibility_2/index.html
    title: CGAL 2D Visibility Computation package, user manual
    locator: the class Simple_polygon_visibility_2, which implements the algorithm of Joe and Simpson
---

Lee's visibility polygon algorithm computes the set of points that a viewpoint $z$ sees inside a [simple polygon](/simple-polygon/) $P$ of $n$ vertices, in $O(n)$ time. It walks once around the boundary and keeps the part seen so far on a [stack](/stack/). D. T. Lee published it in 1983. Barry Joe and R. B. Simpson showed in 1987 that the original rules give wrong output when the boundary winds around $z$ more than once, and they gave a corrected version; that corrected version is the one on this page. The [visibility polygon](/visibility-polygon/) page states the problem and compares the other methods. This page is the linear scan for one point in a polygon without holes.

## In plain words

Stand in a room with many walls and turn around once. You see some walls and not others. The algorithm walks along the walls in order and keeps a list of the wall parts you see so far. When a wall moves away from you, it adds the wall to the list. When a wall comes toward you and covers parts that are already in the list, it takes those parts off. When a wall goes behind a part that you already see, the algorithm skips walls until the boundary comes back into view, and it notes the place where it comes back. The walls can spiral around you, so the algorithm also notes when the boundary passes behind the place where the walk started. At the end the list is the outline of what you see.

## The problem

The input is a simple polygon $P$ with vertices $p_0, \dots, p_{n-1}$ and a point $z$ strictly inside $P$. A point $q$ of $P$ is *visible* from $z$ if the closed segment $zq$ lies in $P$; the segment may touch the boundary. The output is the visibility polygon $V(z)$, the set of visible points, given as its vertices in counterclockwise order. $V(z)$ is a star-shaped polygon with $z$ in its kernel (see [star-shaped polygon](/star-shaped-polygon/)). Its vertices are vertices of $P$ and points where a ray from $z$ through a reflex vertex of $P$ hits the boundary again. The model is the real RAM; the only tests are [orientation tests](/orientation-test/) and intersections of segments, so integer or rational input can be handled exactly.

## The algorithm

Orient $P$ counterclockwise, so that the interior is on the left of each edge. Shoot a ray up from $z$ and let $v_0$ be the first boundary point it hits; $z$ sees $v_0$. List the boundary from $v_0$ as $v_0, v_1, \dots, v_m = v_0$, where $m = n$ if $v_0$ is a vertex and $m = n + 1$ otherwise. The stack $S = s_0, \dots, s_t$ holds the visible chain found so far, with $s_0 = v_0$ at the bottom. The corrected algorithm, in the form that CGAL implements, has six states:

- **LEFT.** The boundary moves counterclockwise around $z$ in full view. Push each new vertex.
- **RIGHT.** The boundary moves clockwise around $z$, so it hides points on the stack. Pop them.
- **SCANA.** The boundary went behind the top $s_t$. Skip edges until one crosses the ray from $z$ through $s_t$.
- **SCANB.** The boundary crossed the ray from $z$ through $v_0$, so it is behind the start. Skip edges until one crosses the window from $s_t$ to $v_0$.
- **SCANC.** The boundary is in front of the stack and moves away from a hidden window. Skip edges until one crosses the window from $s_t$ to $w$.
- **SCAND.** The boundary is behind the window from $s_t$ to $w$. Skip edges until one crosses it.

"Right of $a b$" means that the point is to the right of the directed line from $a$ through $b$.

```pseudo id=main
LEE-VISIBILITY(P, z)            ▷ P counterclockwise, z strictly inside P
L1  v0 ← the first point of ∂P on the ray up from z
L2  v1, ..., v(m-1) ← the rest of ∂P after v0, counterclockwise; v(m) ← v0
L3  S ← [v0]; i ← 1
L4  if v1 is not right of z v0 then push v1; state ← LEFT else state ← SCANA
L5  while state ≠ FINISH do                ▷ s(t) is the top of S
L6      if state = LEFT then
L7          if i = m then state ← FINISH
L8          else if v(i+1) is not right of z v(i) then push v(i+1); i ← i + 1
L9          else if v(i+1) is right of s(t-1) v(i) then state ← SCANA; i ← i + 1
L10         else state ← RIGHT; i ← i + 1
L11     else if state = RIGHT then
L12         pop S down to the first s(j-1) s(j) that the ray z v(i) passes between, or that v(i-1) v(i) crosses at u
L13         if the edge crossed then pop s(j); w ← u; state ← SCAND
L14         else if v(i+1) is right of z v(i) then i ← i + 1        ▷ stay in RIGHT
L15         else replace s(j) by u ← (ray z v(i)) ∩ s(j-1) s(j)
L16              if v(i+1) is right of v(i-1) v(i) then push v(i), v(i+1); state ← LEFT
L17              else w ← v(i); state ← SCANC
L18              i ← i + 1
L19     else if state = SCANA then
L20         v(k) v(k+1) ← the first edge with k ≥ i that meets the ray z s(t), at u; i ← k + 1
L21         if v(k+1) is not right of z v(k) then push u, v(k+1); state ← LEFT
L22         else if u is beyond s(t) on the ray then w ← u; state ← SCAND
L23         else state ← RIGHT
L24     else if state = SCANB then
L25         if i = m then state ← FINISH
L26         else v(k) v(k+1) ← the first edge with k ≥ i that meets the segment s(t) v0, at u
L27              if k + 1 = m and u = v0 then push v0; state ← FINISH
L28              else i ← k + 1; state ← RIGHT
L29     else                                         ▷ SCANC or SCAND
L30         v(k) v(k+1) ← the first edge with k ≥ i that meets the segment s(t) w, at u; i ← k + 1
L31         if state = SCANC then state ← RIGHT else push u, v(k+1); state ← LEFT
L32     if state = LEFT and s(t-1) is right of z v0 and s(t) is left of z v0 then
L33         replace s(t) by y ← (ray z v0) ∩ s(t-1) s(t); state ← SCANB
L34 return S without repeated points and without points inside straight runs
```

Lines L32 and L33 are the correction of Joe and Simpson. The vertices are processed in boundary order, not in angular order, so the boundary can turn around $z$ and pass behind the start $v_0$. When the top edge of the stack crosses the ray from $z$ through $v_0$ from right to left, everything after it until the boundary returns through the window $y v_0$ is hidden. O'Rourke describes the same check with the angle $\alpha(v)$ of a vertex around $z$ counted with winding: only vertices with $0 \le \alpha(v) < 2\pi$ can be visible. In O'Rourke's names, LEFT is Push, RIGHT is Pop and the four scan states are Wait with different windows.

The scans of L20, L26 and L30 look for an edge whose end changes side with respect to the ray or segment and that meets it. The point $u$ is that meeting point, or $v(k+1)$ if the edge lies along the ray.

## Example

Take the room $P = (0,0), (8,0), (8,6), (5,6), (5,3), (3,3), (3,6), (0,6)$, a rectangle with a notch cut down from the top wall between $x = 3$ and $x = 5$, and the viewpoint $z = (4, 1)$ below the notch. The ray up from $z$ hits the bottom of the notch at $v_0 = (4,3)$, so the boundary list is $(4,3), (3,3), (3,6), (0,6), (0,0), (8,0), (8,6), (5,6), (5,3), (4,3)$ with $m = 9$.

| step | state | $i$ | action | stack after the step |
|---|---|---|---|---|
| L4 | | 1 | $v_1 = (3,3)$ is left of $z v_0$ | $(4,3), (3,3)$ |
| L9 | LEFT | 1 | $v_2 = (3,6)$ is right of $z v_1$ and of $s_0 v_1$: the wall goes behind the corner | unchanged |
| L21 | SCANA | 2 | edge $(3,6)(0,6)$ meets the ray $z (3,3)$ at $u = (3/2, 6)$ | $\dots, (3,3), (3/2, 6), (0,6)$ |
| L8 | LEFT | 3 to 6 | push $(0,0)$, $(8,0)$, $(8,6)$, $(5,6)$ | $\dots, (0,6), (0,0), (8,0), (8,6), (5,6)$ |
| L10 | LEFT | 7 | $v_8 = (5,3)$ is right of $z v_7$ but left of $s_{t-1} v_7$: the wall comes toward $z$ | unchanged |
| L12 | RIGHT | 8 | the ray $z (5,3)$ passes between the top two points $(8,6)$ and $(5,6)$, so nothing is popped | unchanged |
| L16 | RIGHT | 8 | replace $(5,6)$ by $u = (13/2, 6)$; $v_9$ is right of $v_7 v_8$; push $(5,3)$, $(4,3)$ | $\dots, (8,6), (13/2, 6), (5,3), (4,3)$ |
| L7 | LEFT | 9 | $i = m$ | finish |

The output, after removing the repeated $v_0$ and the point $(4,3)$ in the middle of the straight edge, is

$$V(z) = (3,3), (3/2, 6), (0,6), (0,0), (8,0), (8,6), (13/2, 6), (5,3).$$

The two new vertices are where the rays from $z$ through the notch corners $(3,3)$ and $(5,3)$ hit the top wall: the ray through $(3,3)$ has direction $(-1, 2)$ and reaches $y = 6$ at $x = 4 - 5/2 = 3/2$, and the ray through $(5,3)$ reaches it at $x = 4 + 5/2 = 13/2$. The parts of the top wall between $x = 3/2$ and $3$ and between $5$ and $13/2$, and the inner walls of the notch, are hidden.

For the viewpoint $z = (7,1)$ in the same room, the ray up hits the top wall at $(7,6)$. The scan pushes $(5,6)$, $(5,3)$ and $(3,3)$, goes behind the corner $(3,3)$ (SCANA) and comes out on the left wall at $(0, 9/2)$, then pushes the rest. The output is $(5,6), (5,3), (3,3), (0, 9/2), (0,0), (8,0), (8,6)$.

A case that needs line L32: for the polygon $(0,4), (11,3), (11,8), (2,8), (8,6)$ and $z = (5, 19/4)$, the ray up hits the edge $(8,6)(0,4)$ at $v_0 = (5, 21/4)$. After the stack reaches $(11,8)$, the next edge goes left along the top and crosses the ray from $z$ through $v_0$ at $(5,8)$. Line L33 puts $(5,8)$ on the stack and enters SCANB. The edge $(2,8)(8,6)$ then comes back through the window from $(5,8)$ to $v_0$ and hides the top wall, and the output is $(0,4), (11,3), (11, 29/4), (8,6)$.

## Correctness

The proof keeps one invariant. Let $C_i$ be the chain $v_0 v_1 \dots v_i$ of the boundary scanned so far. In states LEFT and RIGHT, the stack is the part of $C_i$ that $z$ would see if $C_i$ were the only obstacle, cut to the angles in $[0, 2\pi)$ around $z$ measured from $v_0$ with winding, and listed in angular order. The new points on the stack are the points where a ray from $z$ through a stack vertex leaves that vertex and meets $C_i$ again. In a scan state, the stack is the same set for the chain up to the last visible point, and the boundary since then lies in a region that a window hides: behind $s_t$ (SCANA), behind the segment $s_t v_0$ (SCANB), or behind or in front of the segment $s_t w$ (SCAND, SCANC).

Each line keeps the invariant. In LEFT, an edge that turns counterclockwise around $z$ cannot hide anything already on the stack, so L8 pushes. An edge that turns clockwise either goes behind the top (L9) or comes back toward $z$ in front of the stack (L10). In RIGHT, the popped points are exactly those that the new edge hides, because the stack is in angular order and the new edge blocks the rays that it crosses. A scan state ends at the first edge that passes through the window, because the boundary is a closed curve that does not cross itself: to become visible again it must cross the window, and the first crossing is the next visible point. The check of L32 handles the only way the angle can reach $2\pi$: the top edge crosses the ray $z v_0$, and then the boundary is hidden behind the window $y v_0$ until it comes back through it. When the scan returns to $v_0 = v_m$, the chain is the whole boundary, so the stack is $V(z)$.

Lee's 1983 rules did not track the angle past $2\pi$. On a polygon that spirals around $z$, a part of the boundary that is hidden behind the start can look visible to a local test, and the original algorithm pushes it. The proof, with each case, is below.

## Complexity

The index $i$ only grows, from 1 to $m \le n + 1$. Each step of LEFT and of the scans advances $i$ by at least one or ends the loop, and each scan examines each edge once. Each step pushes at most two points: one vertex and one intersection point. A step of RIGHT pops points, and a popped point is never pushed again, so the total number of pops is at most the total number of pushes, which is at most $2m$. Each test is an orientation test or the intersection of two segments, in $O(1)$ time. So the time is $\Theta(n)$, and the stack holds at most $2m$ points, so the extra space is $\Theta(n)$. The bound is optimal: the output can have $\Theta(n)$ vertices, and every vertex must be read.

With exact rational arithmetic, each intersection point is a ratio of $2 \times 2$ determinants of input coordinates, so the numbers stay small. A point pushed on the stack can be an intersection point, but the tests in later steps still use it as an endpoint of an edge or a ray.

## Properties

- **Linear and without sorting.** The vertices are used in boundary order. An angular sort (see [angular sort](/angular-sort/)) would cost $\Omega(n \log n)$ in the algebraic decision tree model.
- **One stack.** ElGindy and Avis used three stacks for the same bound. Lee reduced this to one.
- **Exact predicates.** Every branch depends on the sign of a $2 \times 2$ determinant. With integer or rational input, the result is exact.
- **Output size.** $V(z)$ has at most $n + r$ vertices, where $r$ is the number of reflex vertices of $P$, because each reflex vertex can add at most one new vertex where its shadow ray ends.
- **Star-shaped output.** The output contains $z$ in its kernel, so each ray from $z$ meets its boundary once.

## Variants and improvements

- **Viewpoint on the boundary or at a vertex.** The same scan works if $v_0$ is chosen next to $z$. CGAL's implementation handles a query point on an edge or at a vertex.
- **Viewpoint outside the polygon.** O'Rourke notes that the same scan computes the part of the boundary seen from an exterior point.
- **Polygons with holes.** A rotational sweep around $z$ with a balanced tree of the edges that the ray crosses takes $O(n \log n)$ time (Asano 1985), and this is optimal for polygons with holes. This is the source of the bound "$O(n \log n)$ by angular sorting"; it is not the bound for a simple polygon.
- **Many queries.** Triangular expansion (Bungiu, Hemmer, Hershberger, Huang and Kröller 2014) walks a triangulation of $P$ from the triangle that holds $z$. It is fast on typical input but has a quadratic worst case. With polynomial preprocessing, a query can take $O(\log n + k)$ time for an output of $k$ vertices (Bose, Lubiw and Munro 2002).
- **Weak visibility.** The set seen from some point of an edge is the [weak visibility polygon](/weak-visibility-polygon/), computed by other methods.

## When to use it

Use it to compute what one point sees in a simple polygon: the region a guard covers in an [art gallery](/art-gallery-problem/) solution, the part of a floor plan that a sensor or camera covers, or a step of a visibility graph or shortest path method. It is the method of choice for one query with exact arithmetic. For many queries in the same polygon, or for polygons with holes, use triangular expansion or a rotational sweep. For a scene of segments or polygons without one outer boundary, use a rotational sweep.

## Pitfalls

- **Using Lee's 1983 rules as published.** On a polygon that spirals around $z$, they can push points that are hidden behind the start. Track the angle with winding, or use the check of L32.
- **Wrong orientation.** The tests assume a counterclockwise boundary. A clockwise polygon must be reversed first.
- **Starting at a hidden vertex.** $v_0$ must be visible from $z$. The first point on a ray from $z$ is visible; an arbitrary vertex is not.
- **Collinear cases.** If $z$ lies on the line of two vertices, a ray grazes a reflex vertex and a window has length zero. With floating point arithmetic, the sign of the orientation test can be wrong near such cases, and the scan can skip the true exit. Use exact predicates.
- **Spikes and repeated points.** Intersection points can coincide with vertices. Remove repeated points from the stack and points in the middle of a straight run before using the output as a polygon.

## Implementations

## History

Several algorithms slower than linear were published before 1980, and O'Rourke reports that at least one proposed linear algorithm was shown not to work. ElGindy and Avis found the first linear algorithm in 1980 and published it in 1981; it uses three stacks. Lee's 1983 paper reduced it to one stack. Joe and Simpson wrote a University of Waterloo technical report in 1985 and published the result in BIT in 1987: both algorithms can fail on polygons that wind around the viewpoint, and they gave a corrected and simpler organization. O'Rourke's 1987 book follows their 1985 presentation. CGAL's visibility package implements the corrected algorithm with the states LEFT, RIGHT and SCANA to SCAND.

## References
