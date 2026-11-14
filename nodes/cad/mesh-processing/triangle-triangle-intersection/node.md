---
tag: QR3KY9
kind: algorithm
slug: triangle-triangle-intersection
name: Triangle-triangle intersection test
aliases:
- Moller triangle intersection test
area: cad/mesh-processing
level: core
summary: Tests whether two triangles in 3D meet. It finds the side of each plane on which the vertices of the other triangle lie, then compares two intervals on the common line.
model: real-ram
complexity:
  vars: {n: "none, the input is two triangles"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1997
  people: [Tomas Möller]
  note: Möller published the plane-side and interval test in the Journal of Graphics Tools. Guigue and Devillers gave a version with orientation predicates only in 2003.
prereqs: [orientation-test, cross-product]
see_also: [separating-axis-theorem, mesh-self-intersection, bounding-volume-hierarchy, collision-detection, mesh-boolean-operations, moller-trumbore, shewchuk-expansion-sum, exact-geometric-computation]
sources:
  - paper: doi:10.1080/10867651.1997.10487472
    title: Tomas Möller, A fast triangle-triangle intersection test, Journal of Graphics Tools 2(2), 1997, 25 to 30
    locator: the description of the test (plane rejection, the intervals on the line of intersection and the coplanar case)
  - paper: doi:10.1080/10867651.2003.10487580
    title: Philippe Guigue and Olivier Devillers, Fast and robust triangle-triangle overlap test using orientation predicates, Journal of Graphics Tools 8(1), 2003, 25 to 32
    locator: the overlap test that uses only orientation predicates, and its coplanar case
  - paper: doi:10.1007/PL00009321
    title: Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3), 1997, 305 to 363
    locator: the sections on the orient3d predicate and its adaptive evaluation
---

The triangle-triangle intersection test decides whether two closed triangles in 3D have a common point. It is the test of Möller (1997). First it computes on which side of the plane of each triangle the three vertices of the other triangle lie, with the [orientation test](/orientation-test/) ORIENT3D. If all three vertices are on one side, the triangles do not meet. If not, each triangle cuts the plane of the other in a segment, both segments lie on the line where the two planes meet, and the triangles meet if and only if the two segments overlap. Two triangles in one plane go to a separate test in 2D. The test takes a constant number of operations. It is the inner test of a [mesh self-intersection](/mesh-self-intersection/) check and of [mesh Boolean operations](/mesh-boolean-operations/).

## In plain words

Take two flat triangles in space. Each one lies in a flat sheet that goes on forever. If all three corners of the second triangle are above the sheet of the first, or all are below, the two triangles cannot touch. The same is true the other way round.

If the corners are on both sides, the first triangle cuts the sheet of the second along a short piece of a line. The second triangle cuts the sheet of the first along a piece of the same line, because both sheets meet on that line. The triangles touch exactly when these two pieces overlap. To compare them, measure where each piece starts and ends along the line.

If the two triangles lie in the same sheet, the test looks at them as flat shapes: they touch if two edges cross, or if one triangle holds a corner of the other.

## The problem

The input is two triangles $P = (p_0, p_1, p_2)$ and $Q = (q_0, q_1, q_2)$ in $\mathbb{R}^3$. Each triangle has three vertices that are not collinear. The output is true if the closed triangles (the [convex hulls](/convex-hull/) of the vertices, with the boundary) have a common point, and false if not. A shared vertex, a shared edge and a touch at one point all count as a meeting. A mesh check must then decide which of these meetings are allowed, see [mesh self-intersection](/mesh-self-intersection/).

## The algorithm

ORIENT3D$(a, b, c, d) = \big((b - a) \times (c - a)\big) \cdot (d - a)$ is the [determinant](/determinant/) of the three edge vectors from $a$. It is positive when $d$ is on the side of the normal of $(a, b, c)$, negative on the other side, and zero when the four points are in one plane. The normal of a triangle is $n_P = (p_1 - p_0) \times (p_2 - p_0)$, with the [cross product](/cross-product/).

```pseudo id=main
TRI-TRI(P, Q)
L1  dq_i ← ORIENT3D(p0, p1, p2, q_i) for i = 0, 1, 2      ▷ sides of Q's vertices
L2  if all dq_i > 0 or all dq_i < 0 then return false
L3  dp_i ← ORIENT3D(q0, q1, q2, p_i) for i = 0, 1, 2      ▷ sides of P's vertices
L4  if all dp_i > 0 or all dp_i < 0 then return false
L5  if dq = (0, 0, 0) then return COPLANAR-TRI-TRI(P, Q)
L6  D ← n_P × n_Q                                          ▷ direction of the common line
L7  [a, b] ← SPAN(P, dp, D); [c, e] ← SPAN(Q, dq, D)
L8  return max(a, c) ≤ min(b, e)

SPAN(T, s, D)                    ▷ projections on D of T ∩ (other plane)
L9  X ← { D · t_i : s_i = 0 }
L10 for each edge (t_i, t_j) of T with s_i · s_j < 0 do
L11     X ← X ∪ { D · t_i + (D · t_j − D · t_i) · s_i / (s_i − s_j) }
L12 return [min X, max X]

COPLANAR-TRI-TRI(P, Q)
L13 drop the coordinate k where |n_P[k]| is largest
L14 if a closed edge of P' meets a closed edge of Q' then return true
L15 return p0' ∈ Q' or q0' ∈ P'
```

Line L11 is the point where the edge from $t_i$ to $t_j$ crosses the other plane, measured along $D$. The fraction $s_i / (s_i - s_j)$ is between 0 and 1, because $s_i$ and $s_j$ have opposite signs. Line L13 projects both triangles onto the axis plane where they have the largest area. The projection is one to one on their common plane, so it does not change whether they meet. Line L14 uses [orientation tests](/orientation-test/) in 2D for each of the 9 pairs of edges, and line L15 tests one vertex of each triangle against the other with three 2D orientation tests.

**Degenerate cases.** A vertex of one triangle can lie in the plane of the other, the triangles can share an edge or a vertex, and they can lie in one plane. These cases are common in meshes, because neighbouring faces share vertices. The test does not assume [general position](/general-position/). A zero $dq_i$ goes to line L9, all zeros go to line L5, and the comparison $\le$ of line L8 counts a touch at one point. With integer or rational coordinates, every sign is exact, so each of these cases gets the correct answer.

## Example

Let $P = (0,0,0), (4,0,0), (0,4,0)$ in the plane $z = 0$, and $Q = (1,1,-1), (1,1,3), (3,3,1)$ in the plane $x = y$.

| step | value |
|---|---|
| L1 | $dq = (-16, 48, 16)$: $q_0$ is below the plane of $P$, $q_1$ and $q_2$ are above |
| L3 | $dp = (0, -32, 32)$: $p_0$ is in the plane of $Q$, $p_1$ and $p_2$ are on opposite sides |
| L6 | $n_P = (0, 0, 16)$, $n_Q = (-8, 8, 0)$, $D = (-128, -128, 0)$ |
| L9 for $P$ | $p_0$ has $dp_0 = 0$, so $X = \{D \cdot p_0\} = \{0\}$ |
| L11 for $P$ | edge $p_1 p_2$: $D \cdot p_1 = D \cdot p_2 = -512$, so $X = \{0, -512\}$ and $[a, b] = [-512, 0]$ |
| L11 for $Q$ | edge $q_0 q_1$ gives $-256$, edge $q_2 q_0$ gives $-768 + 512 \cdot 16/32 = -512$, so $[c, e] = [-512, -256]$ |
| L8 | $\max(-512, -512) = -512 \le -256 = \min(0, -256)$, so true |

The common line is $x = y$, $z = 0$, and the point $(t, t, 0)$ has $D \cdot x = -256\,t$. So the overlap $[-512, -256]$ is the segment from $(1, 1, 0)$ to $(2, 2, 0)$, which is the part of $Q$ that lies in $P$.

Move $Q$ to $(5,5,-1), (5,5,3), (7,7,1)$. The signs do not change, but now $[c, e] = [-1536, -1280]$, which ends before $a = -512$. So the triangles do not meet: $Q$ cuts the plane of $P$ outside the hypotenuse. For $Q = (2,2,0), (2,2,3), (5,5,3)$, $dq = (0, 48, 48)$, the interval of $Q$ is the one point $[-576, -576]$, and $[a, b] = [-576, 0]$. The test returns true, because $Q$ touches the hypotenuse of $P$ at the point $(2, 2, 0)$.

**When the arithmetic is floating point.** The signs of line L1 decide everything, and in floating point they can be wrong. Let $b = (12, 12, 0)$, $c = (24, 24, 0)$, $d = (0, 0, 1)$ and $a = (0.5 + 41u, 0.5 + 48u, 0)$ with $u = 2^{-53}$, that is $a \approx (0.5000000000000046, 0.5000000000000053, 0)$. The point $a$ is very near the line through $b$ and $c$. ORIENT3D$(a, b, c, d)$ is about $+9.3 \times 10^{-15}$ in exact arithmetic, but the same formula in IEEE double gives about $-5.7 \times 10^{-14}$, with the wrong sign. The products are large and almost equal, so their difference loses all correct digits. This is [catastrophic cancellation](/catastrophic-cancellation/). A wrong sign at line L2 can reject two triangles that touch, or send a pair to the wrong branch, and a mesh check then reports a crossing that is not there or misses one that is. The fix is exact signs: integer or rational coordinates as in the code of this page, adaptive filtered predicates as in [Shewchuk's expansion arithmetic](/shewchuk-expansion-sum/), or the [exact geometric computation](/exact-geometric-computation/) model in general.

## Correctness

If all three vertices of $Q$ are strictly on one side of the plane of $P$, then the whole of $Q$ is on that side, because the signed distance is an affine function and $Q$ is the convex hull of its vertices. So lines L2 and L4 reject correctly. In the general case the planes are different and not parallel, so they meet in a line $L$ with direction $D \ne 0$. The part of each triangle in the other plane is the convex hull of its vertices with sign zero and of the edge crossings, and this is what SPAN collects. Both parts lie on $L$, and $P \cap Q$ is their intersection. The map $x \mapsto D \cdot x$ is one to one and keeps the order on $L$, so the parts meet if and only if their intervals overlap. In the coplanar case the projection is one to one on the plane, and two plane triangles meet if and only if two edges meet or one triangle holds a vertex of the other. The full proof is below.

## Complexity

The test does a fixed number of operations: 6 ORIENT3D calls, two cross products, at most 6 interval points, and in the coplanar case 9 segment tests and 2 point tests. So it takes $\Theta(1)$ time and $\Theta(1)$ extra space in the [real RAM](/real-ram/) model.

The cost of exact arithmetic depends on the size of the numbers. With integer coordinates of $b$ bits, ORIENT3D is a polynomial of degree 3 and needs about $3b + 3$ bits. The values $D \cdot t_i$ have degree 5, and the interval ends of line L11 are fractions of degree about 8 over degree 3. These values are constructions, not only signs, so the interval part is the most expensive part of an exact version. The variant of Guigue and Devillers below avoids it.

## Properties

- **Exact.** With integer or rational coordinates, each branch takes the true answer, also on all degenerate inputs.
- **Symmetric.** The result does not depend on the order of the two triangles or on the order of the vertices of each one.
- **Closed sets.** A shared vertex, a shared edge or a touch at one point counts as a meeting.
- **Early exit.** Most pairs of far-apart triangles stop at line L2 after 3 orientation tests.
- **Construction, not only predicates.** Lines L6 to L11 compute new numbers. A version with only signs needs a different method.

## Variants and improvements

- **Möller's float version.** The original code uses floating point and sets each signed distance with a small absolute value to zero, to treat nearly coplanar cases as coplanar. The threshold is a heuristic. It removes some wrong answers and causes others, and no value is correct for all inputs.
- **Guigue and Devillers (2003).** After the same rejection by signs, it permutes the vertices so that one vertex of each triangle is alone on its side, and it decides the overlap of the two intervals with two more ORIENT3D signs. It uses no constructions, so it is exact with filtered predicates such as Shewchuk's, and it is fast in floating point.
- **Separating axes.** Two triangles are disjoint if and only if their projections are disjoint on one of a finite list of axes: the two normals, the 9 cross products of an edge of one with an edge of the other, and, for flat triangles in one plane, the 6 edge normals in that plane. See the [separating axis theorem](/separating-axis-theorem/). This test is simple, but it does many more dot products.
- **Edge against triangle.** Two closed triangles meet if and only if an edge of one meets the other triangle. So six segment-triangle tests also decide the question. The ray form of such a test is [Möller-Trumbore](/moller-trumbore/), which is a ray-triangle test.
- **The segment of intersection.** Mesh Boolean operations need the segment itself, not only a yes or no. The overlap interval of line L8 gives its two ends on the common line.

## When to use it

Use it as the exact pair test after a broad phase, such as a [bounding volume hierarchy](/bounding-volume-hierarchy/) or a uniform grid, has found the pairs of triangles whose boxes overlap. This is the setting of a [mesh self-intersection](/mesh-self-intersection/) check, of [collision detection](/collision-detection/) between triangle meshes, and of [mesh Boolean operations](/mesh-boolean-operations/). If only a yes or no is needed and robust floating point predicates are available, the Guigue-Devillers form is a better choice. If you test a ray, not a triangle, use a ray-triangle test.

## Pitfalls

- **Neighbours always meet.** Two faces of a mesh that share a vertex or an edge meet by this test. A self-intersection check must ignore the shared part and look for any other common point.
- **Epsilon tests.** A threshold on the signed distances is not a fix. It changes which inputs fail, and it makes the test depend on the scale of the model.
- **The wrong coplanar projection.** Drop the coordinate where the normal is largest. If you drop a coordinate where the normal is zero, the projected triangles are segments, and the 2D test is wrong.
- **Degenerate triangles.** A triangle with collinear vertices has a zero normal, and the test does not apply. Remove such faces first, or test them as segments.
- **Mixed precision.** Signs from exact arithmetic and interval ends from floating point can disagree. Compute the whole test in one exact model.

## Implementations

## History

Tomas Möller published the test in 1997, in the Journal of Graphics Tools, as a fast test for collision detection and for the intersection of meshes. Philippe Guigue and Olivier Devillers published a version in 2003 that uses only orientation predicates, so that it can be made robust with exact predicates. The exact predicates come from the work of Jonathan Shewchuk in 1997 on adaptive floating point arithmetic.

## References
