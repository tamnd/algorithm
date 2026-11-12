---
tag: H67QFK
kind: algorithm
slug: moller-trumbore
name: Möller-Trumbore ray-triangle intersection
aliases:
- Möller-Trumbore test
area: graphics-and-signals/ray-tracing
level: advanced
summary: Intersect a ray with a triangle by solving for the ray parameter and two barycentric coordinates with Cramer's rule, written with cross and dot products and no stored plane.
solves: [ray-object-intersection]
model: real-ram
complexity:
  time: {worst: Θ(1)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1997
  people: [Tomas Möller, Ben Trumbore]
  note: Möller and Trumbore published the test in the Journal of Graphics Tools as a fast ray-triangle test that stores only the three vertices.
prereqs: [ray-object-intersection, cramers-rule, cross-product]
see_also: [watertight-ray-triangle-intersection, plucker-ray-triangle-test, ray-plane-intersection, edge-function, closest-hit-query, bounding-volume-hierarchy, orientation-test]
sources:
  - paper: doi:10.1080/10867651.1997.10487468
    title: Tomas Möller and Ben Trumbore, Fast, minimum storage ray-triangle intersection, Journal of Graphics Tools 2(1), 1997, 21 to 28
    locator: the derivation by Cramer's rule with scalar triple products, and the code with and without back-face culling
  - url: http://jcgt.org/published/0002/01/05/
    title: Sven Woop, Carsten Benthin and Ingo Wald, Watertight ray/triangle intersection, Journal of Computer Graphics Techniques 2(1), 2013, 65 to 82
    locator: Section 2 (why tests with u + v at most 1 are not watertight) and Table 2 (rays that miss a closed mesh, among them with the Möller-Trumbore test)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 22, Intersection Test Methods, Section 22.8 Ray/Triangle Intersection
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 3.6.2 Triangle Intersection and its Further Reading (a watertight test in place of this one)
---

The Möller-Trumbore algorithm tests whether a ray $o + t\,d$ hits a triangle $v_0 v_1 v_2$, and gives the ray parameter $t$ and two barycentric coordinates $(u, v)$ of the hit. It solves the $3 \times 3$ linear system $o + t\,d = (1 - u - v)\,v_0 + u\,v_1 + v\,v_2$ by [Cramer's rule](/cramers-rule/), with each determinant written as a [cross product](/cross-product/) and a [dot product](/dot-product/), so the triangle needs no stored plane equation. It solves [ray-object intersection](/ray-object-intersection/) for triangles in a constant number of operations. In floating point it is not watertight: a ray through an edge that two triangles share can miss both.

## In plain words

A point inside a triangle is a mix of its three corners, with weights that are not negative and add up to one. The ray hits the triangle when one of its points is such a mix. So the test asks for three unknown numbers: how far along the ray the point is, and two of the weights. The third weight is one minus the other two.

These three numbers solve three linear equations, one for each coordinate. The test solves them with determinants, and it computes each determinant from a few products of the edge vectors of the triangle. It checks each weight as soon as it has it, so most misses stop early. It keeps nothing but the three corners, which is the "minimum storage" of the title of the paper.

## The problem

The input is a ray $o + t\,d$ with $d \ne 0$, an open interval $(t_{\min}, t_{\max})$ of the ray parameter, and a triangle with the vertices $v_0, v_1, v_2$. The output is the triple $(t, u, v)$ with

$$o + t\,d = (1 - u - v)\,v_0 + u\,v_1 + v\,v_2, \qquad u \ge 0,\ v \ge 0,\ u + v \le 1,\ t_{\min} < t < t_{\max},$$

or MISS when no such triple exists. The triangle is closed: a point on an edge counts as a hit. A ray that is parallel to the plane of the triangle, or a triangle with collinear vertices, gives MISS; the case of a ray inside the plane, where the hits form a segment, is out of scope.

## The algorithm

Write $e_1 = v_1 - v_0$, $e_2 = v_2 - v_0$ and $s = o - v_0$. The system is $-t\,d + u\,e_1 + v\,e_2 = s$, a linear system with the columns $-d$, $e_1$, $e_2$. By Cramer's rule each unknown is a ratio of two determinants, and each $3 \times 3$ determinant is a scalar triple product $\det[a, b, c] = a \cdot (b \times c)$.

```pseudo id=main
MOLLER-TRUMBORE(o, d, v0, v1, v2, tmin, tmax)
L1  e1 ← v1 − v0;  e2 ← v2 − v0
L2  p ← d × e2
L3  det ← e1 · p                                  ▷ det = −d · (e1 × e2)
L4  if det = 0 then return MISS                   ▷ ray parallel to the plane
L5  inv ← 1 / det
L6  s ← o − v0
L7  u ← (s · p) · inv;  if u < 0 or u > 1 then return MISS
L8  q ← s × e1
L9  v ← (d · q) · inv;  if v < 0 or u + v > 1 then return MISS
L10 t ← (e2 · q) · inv;  if not (tmin < t < tmax) then return MISS
L11 return (t, u, v)
```

The four determinants of Cramer's rule are $\det[-d, e_1, e_2] = e_1 \cdot (d \times e_2)$ for the system, $\det[-d, s, e_2] = s \cdot (d \times e_2)$ for $u$, $\det[-d, e_1, s] = d \cdot (s \times e_1)$ for $v$, and $\det[s, e_1, e_2] = e_2 \cdot (s \times e_1)$ for $t$. So two cross products suffice: $p = d \times e_2$ of line L2 serves the system and $u$, and $q = s \times e_1$ of line L8 serves $v$ and $t$. Line L7 checks $u$ before line L8 computes $q$, and line L9 checks $v$ before line L10 computes $t$, so a ray that misses the triangle costs less than a hit.

The sign of det tells the side of the triangle that the ray comes from: $\det = -d \cdot n$ for the normal $n = e_1 \times e_2$, so $\det > 0$ when the vertices run counterclockwise as seen from the ray origin. A renderer that culls back faces returns MISS when $\det < 0$ at line L4; the original paper also gives this version, where the division of line L5 moves to the end.

## Example

The triangle $v_0 = (0, 0, 0)$, $v_1 = (1, 0, 0)$, $v_2 = (0, 1, 0)$ lies in the plane $z = 0$. The ray starts at $o = (\tfrac14, \tfrac14, 1)$ and goes straight down, $d = (0, 0, -1)$, with $(t_{\min}, t_{\max}) = (0, \infty)$.

| line | value | check |
|---|---|---|
| L1 | $e_1 = (1, 0, 0)$, $e_2 = (0, 1, 0)$ | |
| L2 | $p = d \times e_2 = (1, 0, 0)$ | |
| L3 | $\det = e_1 \cdot p = 1$ | not 0, and positive: a front face |
| L6 | $s = (\tfrac14, \tfrac14, 1)$ | |
| L7 | $u = s \cdot p = \tfrac14$ | in $[0, 1]$ |
| L8 | $q = s \times e_1 = (0, 1, -\tfrac14)$ | |
| L9 | $v = d \cdot q = \tfrac14$ | $v \ge 0$ and $u + v = \tfrac12 \le 1$ |
| L10 | $t = e_2 \cdot q = 1$ | in $(0, \infty)$ |

The hit is $o + 1 \cdot d = (\tfrac14, \tfrac14, 0) = \tfrac12 v_0 + \tfrac14 v_1 + \tfrac14 v_2$.

**A ray through a shared edge.** Two triangles $T_1 = (P, A, Q)$ and $T_2 = (P, Q, B)$ share the edge $PQ$, with the double precision vertices $P = (0.1, 0.2, 0.3)$, $Q = (0.7, 0.9, 0.4)$, $A = (0.9, 0.1, 0.2)$ and $B = (0.2, 0.8, 0.6)$. The ray starts at $o = (1, 1, 2)$ and aims at the point $P + 0.1\,(Q - P)$ of the edge, so $d = (-0.84, -0.73, -1.69)$ after rounding.

| triangle | $u$ in double precision | $v$ in double precision | exact answer for the same inputs |
|---|---|---|---|
| $T_1$ | $-5.57 \times 10^{-17}$ | $0.09999999999999992$ | hit, $u = 1.96 \times 10^{-17}$ |
| $T_2$ | $0.10000000000000005$ | $-1.13 \times 10^{-16}$ | miss |

The exact answer, computed with rational numbers on the same rounded inputs, is a hit in $T_1$ just inside the edge. In double precision line L7 rejects $T_1$ because $u < 0$, and line L9 rejects $T_2$ because $v < 0$. The ray leaks through the surface. The [watertight test](/watertight-ray-triangle-intersection/) hits $T_1$ for this ray.

## Correctness

The algorithm returns $(t, u, v)$ exactly when the triple solves the system and meets the constraints of the problem. The system matrix $[-d, e_1, e_2]$ is singular exactly when $d$ lies in the span of $e_1$ and $e_2$ or when $e_1$ and $e_2$ are parallel, which are the two cases that the problem maps to MISS. Otherwise the system has one solution, and lines L5 to L10 compute it by Cramer's rule, because the four triple products are the four determinants. Each early return of line L7 or L9 rejects only a value that breaks a constraint of the problem: $u > 1$ with $v \ge 0$ already breaks $u + v \le 1$. The full proof is in the proofs folder.

This holds in exact arithmetic (the [real RAM](/real-ram/), or rational inputs). In floating point, the computed $u$ and $v$ carry rounding errors, and the sign decisions of lines L7 and L9 can be wrong for points within a few rounding errors of an edge, as the example shows.

## Complexity

Each step is a fixed number of operations on 3-vectors, so the test takes $\Theta(1)$ time and $O(1)$ extra space. In detail: the subtractions of lines L1 and L6 cost 9 additions, the two cross products cost 12 multiplications and 6 additions, the four dot products cost 12 multiplications and 8 additions, and the scaling by inv costs 3 multiplications. With the sum $u + v$, a hit costs 27 multiplications, 24 additions, 1 division and a few comparisons. A miss at line L7 costs less.

The triangle needs 9 numbers of storage, its vertices. A test that first intersects the plane of the triangle (with [ray-plane intersection](/ray-plane-intersection/)) and then does a 2D inside test needs a stored normal, or it must compute it for each ray.

A ray against a scene of $n$ triangles costs $n$ such tests by a linear scan. A [bounding volume hierarchy](/bounding-volume-hierarchy/) cuts the number of tests on typical scenes, but it is $O(n)$ per ray in the worst case.

## Properties

- **Two-sided.** Without culling, the test hits the triangle from both sides; the sign of det tells which.
- **Barycentric output.** The values $(1 - u - v, u, v)$ interpolate normals, texture coordinates and colors at the hit.
- **Exact with rational inputs.** With rational arithmetic, every step is exact and the answer is the exact one.
- **Not watertight in floating point.** The test for the edge $v_0 v_1$ is $v \ge 0$, the test for $v_0 v_2$ is $u \ge 0$, and the third edge is $u + v \le 1$. Two triangles with a shared edge compute these values from different vertices and different edge vectors, so the rounding errors on the two sides differ, and a ray within a few rounding errors of the edge can fail both tests. The method is only usually correct near edges and vertices. Woop, Benthin and Wald count such misses for rays shot at closed meshes from the inside (their Table 2).
- **Not conservative.** Rounding can also give a hit in both triangles of an edge. A ray that hits two triangles at the same $t$ is harmless for the [closest hit](/closest-hit-query/), but a leak is not.

## Variants and improvements

- **Back-face culling.** Return MISS when $\det < 0$, and compare the unscaled values $s \cdot p$ and $d \cdot q$ with $0$ and det, so that one division at the end gives $t$, $u$ and $v$.
- **A ray segment.** A segment from $a$ to $b$ is the ray $o = a$, $d = b - a$ with $(t_{\min}, t_{\max}) = (0, 1)$.
- **Precomputed forms.** Some tests store a transformed triangle or its plane with each triangle, and use fewer operations per ray at the cost of memory. They suit static scenes that many rays hit.
- **The watertight test.** The [watertight ray-triangle intersection](/watertight-ray-triangle-intersection/) of Woop, Benthin and Wald moves the ray to the $z$ axis and evaluates three 2D [edge functions](/edge-function/) that agree between neighbor triangles, so no ray leaks through a shared edge.
- **Plücker coordinates.** The [Plücker ray-triangle test](/plucker-ray-triangle-test/) decides the hit by the signs of three products of lines, one for each edge, which a mesh can share between neighbor triangles.

## When to use it

Use Möller-Trumbore when the memory per triangle must stay small or the triangles move from frame to frame, because the test needs no per-triangle data other than the vertices. It is a good default for a simple ray tracer, collision queries and picking. Use the [watertight test](/watertight-ray-triangle-intersection/) when rays must not leak through closed meshes, as in path tracing of glass or in a point-in-mesh test that counts crossings. Use a precomputed form when many rays hit a static mesh and memory is not a concern.

## Pitfalls

- **A fixed epsilon on det.** The test `if |det| < 1e-6 then return MISS` at line L4 rejects every small triangle, because det scales with $|d|\,|e_1|\,|e_2|$. Test `det = 0` at line L4, as above; a tiny nonzero det gives large $u$ or $v$ that lines L7 and L9 reject. If a threshold is needed, scale it by $|d|\,|e_1|\,|e_2|$.
- **Self-intersection of secondary rays.** A shadow or reflection ray that starts on the triangle can hit the same triangle at $t \approx 0$. With $t_{\min} = 0$ at line L10, the surface shadows itself (shadow acne). Use a $t_{\min}$ that is larger than the error of the hit point, or move the origin along the normal.
- **Leaks through shared edges.** Line L7 tests $u < 0$ and line L9 tests $v < 0$ and $u + v > 1$, so the two triangles of an edge do not evaluate the same expression for it. Do not count crossings with this test to decide whether a point is inside a closed mesh; use the watertight test.
- **The culling sign.** Culling at line L4 with `det > 0` in place of `det < 0` culls the front faces. With $\det = -d \cdot (e_1 \times e_2)$, a front face, with counterclockwise vertices as seen from the ray, has $\det > 0$.

## Implementations

## History

Tomas Möller (later Tomas Akenine-Möller) and Ben Trumbore published the test in the Journal of Graphics Tools in 1997. Earlier tests intersected the plane of the triangle first and then tested the hit point in 2D; the new test used Cramer's rule directly, stored only the vertices, and was fast on the machines of the time. It became one of the most used ray-triangle tests. In 2013 Woop, Benthin and Wald showed that it and most other tests are not watertight in floating point, and gave a test that is.

## References
