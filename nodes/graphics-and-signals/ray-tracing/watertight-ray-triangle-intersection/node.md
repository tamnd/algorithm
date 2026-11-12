---
tag: Y50EDX
kind: algorithm
slug: watertight-ray-triangle-intersection
name: Watertight ray-triangle intersection
aliases:
- Woop-Benthin-Wald test
area: graphics-and-signals/ray-tracing
level: advanced
summary: Ray-triangle test that shears the ray onto the z axis and decides the hit by 2D edge functions that neighbor triangles evaluate the same way, so no ray leaks through a shared edge.
solves: [ray-object-intersection]
model: floating-point-model
complexity:
  time: {worst: Θ(1)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2013
  people: [Sven Woop, Carsten Benthin, Ingo Wald]
  note: Woop, Benthin and Wald published the test in the Journal of Computer Graphics Techniques, with a count of the rays that other tests lose on closed meshes.
prereqs: [moller-trumbore, edge-function, ieee-754]
see_also: [plucker-ray-triangle-test, ray-object-intersection, orientation-test, top-left-fill-rule, bvh-traversal, polygon-mesh, error-free-transformations]
sources:
  - url: http://jcgt.org/published/0002/01/05/
    title: Sven Woop, Carsten Benthin and Ingo Wald, Watertight ray/triangle intersection, Journal of Computer Graphics Techniques 2(1), 2013, 65 to 82
    locator: Section 3 (the algorithm), Section 3.1 (monotone rounding and the sign of an edge function), Section 3.2 (the fallback to double precision), Section 3.3 (enlarged bounds for the hierarchy), Table 2 and Appendix A (pseudocode)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 3.6.2 Triangle Intersection, and Section 3.9 Managing Rounding Error
  - paper: doi:10.1080/10867651.1997.10487468
    title: Tomas Möller and Ben Trumbore, Fast, minimum storage ray-triangle intersection, Journal of Graphics Tools 2(1), 1997, 21 to 28
    locator: the test that this one replaces when rays must not leak
---

The watertight ray-triangle intersection of Woop, Benthin and Wald tests whether a ray hits a triangle in floating point, in a way that never lets a ray pass between two triangles that share an edge. It moves the triangle so that the ray origin is at the origin, permutes the axes and shears space so that the ray becomes the $z$ axis, and then decides the hit by the signs of three 2D [edge functions](/edge-function/) of the projected vertices. The transformed position of a vertex depends only on the vertex and the ray, so two neighbor triangles compute the same numbers for their shared edge, with opposite signs. A rare fallback to higher precision makes each sign exact. It solves [ray-object intersection](/ray-object-intersection/) for triangle meshes.

## In plain words

Look along the ray, so that the ray becomes a single point in the middle of your view. The ray hits the triangle when that point is inside the flat picture of the triangle. A point is inside when it is on the inner side of each of the three edges, and the side is the sign of a small 2D determinant.

The trick is to compute each edge's determinant from the two edge endpoints only, after a change of view that is the same for every triangle. Two triangles that share an edge then compute the same value, one with a minus sign. A ray that is on one side for one triangle is on the other side for the other, and a ray exactly on the edge counts for both. If a value comes out zero, the test redoes it more precisely, so it never guesses.

## The problem

The input is a ray $o + t\,d$ with floating point coordinates and $d \ne 0$, an upper bound $t_{\max}$, and a triangle $A B C$ with floating point vertices. The output is $(t, u, v, w)$ with $u + v + w = 1$ and $u, v, w \ge 0$, where $u A + v B + w C$ is the hit point and $0 \le t \le t_{\max}$, or MISS.

In exact arithmetic this is the problem that the [Möller-Trumbore test](/moller-trumbore/) solves. The extra requirement is about floating point: for a mesh in which neighbor triangles share vertices, a ray through the inside of a shared edge, or through a vertex inside the mesh, must hit at least one of the triangles. A test with this property is called watertight.

## The algorithm

Lines L1 to L4 depend only on the ray, so a renderer computes them once per ray and reuses them for every triangle the ray meets. For a vector $P$, write $P_x, P_y, P_z$ for its components on the permuted axes $k_x, k_y, k_z$.

```pseudo id=main
WATERTIGHT(o, d, A, B, C, tmax)
L1  kz ← the axis of the largest |d[k]|;  kx ← (kz + 1) mod 3;  ky ← (kx + 1) mod 3
L2  if d[kz] < 0 then swap kx and ky                    ▷ keep the winding order
L3  Sx ← d[kx] / d[kz];  Sy ← d[ky] / d[kz]
L4  Sz ← 1 / d[kz]
L5  A ← A − o;  B ← B − o;  C ← C − o
L6  for P in A, B, C:  P′x ← P[kx] − Sx · P[kz];  P′y ← P[ky] − Sy · P[kz]
L7  U ← C′x · B′y − C′y · B′x;  V ← A′x · C′y − A′y · C′x;  W ← B′x · A′y − B′y · A′x
L8  if U = 0 or V = 0 or W = 0 then recompute U, V, W in higher precision
L9  if (U < 0 or V < 0 or W < 0) and (U > 0 or V > 0 or W > 0) then return MISS
L10 det ← U + V + W;  if det = 0 then return MISS
L11 T ← U · Sz · A[kz] + V · Sz · B[kz] + W · Sz · C[kz]
L12 if sign(det) · T < 0 or sign(det) · T > tmax · |det| then return MISS
L13 return (T / det, U / det, V / det, W / det)
```

After line L6 the ray lies on the $z$ axis of the sheared space: the shear maps $o + t\,d$ to $(0, 0, t\,d[k_z])$. So the ray meets the triangle exactly when the 2D point $(0, 0)$ lies in the 2D triangle $A' B' C'$. The value $U$ of line L7 is the 2D cross product of $C'$ and $B'$, which is the edge function of the edge $B C$ at the origin, and $V$ and $W$ are those of the edges $C A$ and $A B$. They are also twice the signed areas of the triangles that the origin forms with each edge, so $U / \det$, $V / \det$ and $W / \det$ are the barycentric coordinates of the hit.

Line L9 is a two-sided test: it rejects the ray when the signs are mixed, and accepts all three values of one sign, with zeros allowed. A renderer that culls back faces rejects any negative value. Line L10 rejects a triangle whose projection has zero area, which includes a ray in the plane of the triangle. Line L11 interpolates the $z$ values, scaled by $S_z$ so that they become ray parameters, and line L12 compares $T$ with the interval without a division; the single division comes at the end, for a hit.

The swap of line L2 keeps the orientation of the projected triangle the same as seen from the ray, so the sign of det tells front from back for every ray direction.

**Why the edges agree.** The values $P'_x$ and $P'_y$ of a vertex depend only on the vertex and the ray, not on the triangle. The neighbor triangle across the edge $B C$ lists the edge as $C B$ and computes $B'_x C'_y - B'_y C'_x$. The two products are the same as in $U$, in the other order, and rounding is symmetric, so the computed value is exactly $-U$. Under the round-to-nearest rule of [IEEE 754](/ieee-754/), rounding is monotone, so the computed difference of two products has the sign of the exact difference or is zero (Section 3.1 of the paper). A zero is the only case in which the sign is not known, and line L8 handles it by an exact recomputation: the paper falls back from single to double precision, which is exact for products of single precision numbers.

## Example

**A hit.** The triangle $A = (0, 0, 0)$, $B = (1, 0, 0)$, $C = (0, 1, 0)$ and the ray from $o = (\tfrac14, \tfrac14, 1)$ with $d = (0, 0, -1)$, as on the page of the [Möller-Trumbore test](/moller-trumbore/).

| line | value |
|---|---|
| L1 | $k_z = 2$ (the $z$ axis), $k_x = 0$, $k_y = 1$ |
| L2 | $d[k_z] = -1 < 0$, so $k_x = 1$, $k_y = 0$ |
| L3, L4 | $S_x = 0$, $S_y = 0$, $S_z = -1$ |
| L5, L6 | $A' = (-\tfrac14, -\tfrac14)$, $B' = (-\tfrac14, \tfrac34)$, $C' = (\tfrac34, -\tfrac14)$, and $A[k_z] = B[k_z] = C[k_z] = -1$ |
| L7 | $U = \tfrac{9}{16} - \tfrac{1}{16} = \tfrac12$, $V = \tfrac{1}{16} + \tfrac{3}{16} = \tfrac14$, $W = \tfrac{1}{16} + \tfrac{3}{16} = \tfrac14$ |
| L9 | all three positive: inside |
| L10 | $\det = 1$ |
| L11 | $T = \tfrac12 \cdot 1 + \tfrac14 \cdot 1 + \tfrac14 \cdot 1 = 1$ |
| L13 | $(t, u, v, w) = (1, \tfrac12, \tfrac14, \tfrac14)$ |

**The ray that leaks through Möller-Trumbore.** The triangles $T_1 = (P, A, Q)$ and $T_2 = (P, Q, B)$ share the edge $PQ$, with $P = (0.1, 0.2, 0.3)$, $Q = (0.7, 0.9, 0.4)$, $A = (0.9, 0.1, 0.2)$, $B = (0.2, 0.8, 0.6)$, and the ray from $o = (1, 1, 2)$ aims at $P + 0.1\,(Q - P)$, so that $d = (-0.84, -0.73, -1.69)$ in double precision. The ray constants are $k_z = 2$, $k_x = 1$, $k_y = 0$, $S_x \approx 0.43195$, $S_y \approx 0.49704$, $S_z \approx -0.59172$.

| triangle | Möller-Trumbore in double precision | watertight test in double precision | exact answer |
|---|---|---|---|
| $T_1$ | MISS ($u \approx -5.6 \times 10^{-17}$) | hit, $t = 1$, weights $(0.9, 3.5 \times 10^{-17}, 0.1)$ | hit |
| $T_2$ | MISS ($v \approx -1.1 \times 10^{-16}$) | MISS | miss |

The watertight test agrees with the exact answer for the rounded inputs. In the tests of the implementation (seed 7), 4000 rays aimed at the shared edges and inner vertices of random height-field meshes all hit at least one triangle.

## Correctness

The invariant is that lines L7 and L8 give each of $U$, $V$, $W$ the exact sign of the edge function of the transformed, rounded vertices $A'$, $B'$, $C'$. So the decision of line L9 is the exact closed point-in-triangle test of the origin against the 2D triangle $A' B' C'$. Since a shared vertex has the same transformed coordinates in every triangle, all triangles of the mesh are tested exactly against one 2D mesh, and a point on an edge between two projected triangles is in both closed triangles. Hence a ray through an inner edge or an inner vertex hits at least one triangle. The full proof is in the proofs folder.

The guarantee is about the decision, not about $t$: the hit distance and the barycentric coordinates carry ordinary rounding errors. It also needs the edge to have its two triangles on opposite sides in the projection. At a silhouette edge, where both triangles project to the same side of the edge, a ray that grazes the edge can miss both, and the exact answer is a touch at a single point.

## Complexity

Lines L1 to L4 cost one comparison of three numbers, two divisions and one reciprocal per ray. Per triangle, line L5 costs 9 subtractions, line L6 costs 6 multiplications and 6 subtractions, line L7 costs 6 multiplications and 3 subtractions, line L10 costs 2 additions, line L11 costs 6 multiplications and 2 additions, and a hit adds one reciprocal and 4 multiplications. So the test takes $\Theta(1)$ time and $O(1)$ extra space, with about 22 multiplications and 22 additions for a hit, which is close to the [Möller-Trumbore test](/moller-trumbore/). The fallback of line L8 runs only when a computed edge value is exactly zero, which is rare for rays in general position (Section 3.2 of the paper), so it does not change the cost on average; it is $O(1)$ in the worst case too.

## Properties

- **Watertight.** No ray through an inner shared edge or an inner vertex of a mesh misses all of its triangles, under the conditions above.
- **Conservative at edges.** A ray exactly on a shared edge hits both triangles. For a closest hit this is harmless, because both hits have the same $t$ up to rounding. A counter of crossings must break the tie, for example with a rule like the [top-left fill rule](/top-left-fill-rule/) of rasterization.
- **Exact decision, inexact distance.** The decision is exact for the rounded transformed vertices; $t$ and the weights are not exact.
- **Depends on the ray, not on the triangle order.** The axis choice, the shear and the vertex transform are the same for all triangles that one ray meets.
- **Front and back.** The sign of det gives the orientation of the triangle as seen from the ray, for every direction, because of the swap of line L2.

## Variants and improvements

- **Single precision with a double fallback.** This is the form of the paper. The products of single precision numbers are exact in double precision, so the fallback gives exact signs.
- **Fused multiply-add.** A [fused multiply-add](/fused-multiply-add/) with an [error-free transformation](/error-free-transformations/) of the products also gives the exact sign of a $2 \times 2$ determinant, without a wider type.
- **Exact predicates.** An [orientation test](/orientation-test/) with adaptive arithmetic, as in the [expansion sums of Shewchuk](/shewchuk-expansion-sum/), decides the same signs from the original vertices, at a higher cost per test.
- **Back-face culling.** Reject any negative value at line L9.
- **Hierarchy bounds.** A watertight test is only watertight in a renderer if traversal does not cull the triangle first. The paper enlarges the bounds of the boxes of the [bounding volume hierarchy](/bounding-volume-hierarchy/) by a few rounding errors so that the [slab test](/slab-method/) is conservative (Section 3.3).
- **The Plücker test.** The [Plücker ray-triangle test](/plucker-ray-triangle-test/) is watertight along edges when it shares the edge values, but not at vertices; this test is watertight at both.

## When to use it

Use the watertight test when a ray must not pass through a closed mesh: path tracing with glass and other refractive objects, where one lost hit puts a path on the wrong side of a surface; inside tests that count the crossings of a ray with a mesh; and collision and visibility queries in which a gap would be a real error. It is the triangle test of PBRT from the third edition on. For a ray tracer without these needs, the [Möller-Trumbore test](/moller-trumbore/) is a little simpler and is fine.

## Pitfalls

- **Per-triangle shear.** Computing the shear or the axis choice of lines L1 to L4 from the triangle, for example from its normal, gives neighbor triangles different transforms, so the edge values no longer agree and the test leaks. Compute lines L1 to L4 from the ray only.
- **Dropping the swap.** Without line L2, rays with $d[k_z] < 0$ see every triangle with the opposite orientation, and back-face culling culls the wrong faces. Keep the swap of $k_x$ and $k_y$.
- **Dropping the fallback.** Without line L8, a computed zero can hide a value with the wrong sign, and the test can miss at an edge or a vertex. Keep the recomputation when any of $U$, $V$, $W$ is zero.
- **A strict inside test.** Writing line L9 as `if U <= 0 or V <= 0 or W <= 0 then return MISS` rejects a ray exactly on the edge in both triangles, which is a leak. Allow zeros, as in line L9 above.
- **Culling in the hierarchy.** A slab test in plain floating point can reject the box of a triangle that the watertight test would hit. Enlarge the bounds as in Section 3.3 of the paper.

## Implementations

## History

Möller and Trumbore (1997) and most other fast tests decide the hit with expressions that differ between neighbor triangles, so in floating point a ray can pass between them. Woop, Benthin and Wald published the watertight test in the Journal of Computer Graphics Techniques in 2013. They counted the rays that miss closed meshes when shot from the inside, for several known tests, and found misses for all of them except their own. The test went into PBRT (third edition, 2016) and into production ray tracers.

## References
