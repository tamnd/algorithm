---
tag: NVZ11Z
kind: algorithm
slug: ray-plane-intersection
name: Ray-plane intersection
area: graphics-and-signals/ray-tracing
level: intro
summary: Find where a ray crosses a plane by substituting the ray into the plane equation and solving one linear equation for the ray parameter.
solves: [ray-object-intersection]
model: real-ram
complexity:
  time: {worst: Θ(1)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [ray-object-intersection, dot-product]
see_also: [ray-sphere-intersection, moller-trumbore, plucker-ray-triangle-test, slab-method, line-line-intersection, catastrophic-cancellation, cramers-rule, back-face-culling]
sources:
  - book: isbn:9780122861604
    title: Andrew S. Glassner (editor), An Introduction to Ray Tracing, Academic Press, 1989
    locator: Chapter 2, Essential Ray Tracing Algorithms, by Eric Haines (the ray-plane and ray-polygon tests)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 4, Ray Tracing (ray-object intersection)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 22, Intersection Test Methods
---

Ray-plane intersection finds the point where a ray $o + t\,d$ crosses the plane $n \cdot x = h$. Substituting the ray into the plane equation gives the linear equation $n \cdot o + t\,(n \cdot d) = h$, so $t = (h - n \cdot o) / (n \cdot d)$ when $n \cdot d \ne 0$. It is the simplest case of [ray-object intersection](/ray-object-intersection/), and the first step of many others: a ray-polygon test intersects the plane of the polygon and then asks whether the point is inside, and the [slab method](/slab-method/) for boxes is three pairs of ray-plane tests.

## In plain words

A plane is everything at the same height above a reference, measured along a fixed direction, the normal. Moving along the ray changes that height at a constant rate. So the question "when does the ray reach the plane?" is the question "how long until the height reaches the right value?". The answer is the height still to climb divided by the rate.

If the rate is zero, the ray runs parallel to the plane and never reaches it. If the answer is negative, the plane is behind the start of the ray. If the rate is positive, the ray comes from the back side of the plane, which a renderer can use to skip back faces.

## The problem

The input is a ray $o + t\,d$ with $d \ne 0$, an open interval $(t_{\min}, t_{\max})$ of the ray parameter, and a plane given by a normal $n \ne 0$ and an offset $h$: the plane is the set of points $x$ with $n \cdot x = h$. The normal need not have unit length. The output is the parameter $t$ with $t_{\min} < t < t_{\max}$ and $n \cdot (o + t\,d) = h$, or MISS. A ray parallel to the plane is a MISS, also when it lies in the plane, where every point is a solution; a caller that needs that case tests $n \cdot o = h$ separately.

A plane is also given by a point $p_0$ on it and a normal, with $h = n \cdot p_0$, or by three points, with $n = (p_1 - p_0) \times (p_2 - p_0)$.

## The algorithm

```pseudo id=main
RAY-PLANE(o, d, n, h, tmin, tmax)
L1  den ← n · d                     ▷ the rate at which the ray climbs along n
L2  if den = 0 then return MISS      ▷ parallel; with back-face culling also MISS when den > 0
L3  t ← (h − n · o) / den
L4  if not (tmin < t < tmax) then return MISS
L5  return t
```

Line L1 measures how fast the signed height $n \cdot x$ changes along the ray. Line L2 rejects a parallel ray, for which the height never changes. Line L3 solves the linear equation: $h - n \cdot o$ is the height still to climb. Line L4 keeps only hits in front of the origin and inside the interval. The hit point is $o + t\,d$.

The sign of den tells the side: with $\mathrm{den} < 0$ the ray goes against the normal, so it comes from the front, the side the normal points to. A renderer that culls back faces also returns MISS at line L2 when $\mathrm{den} > 0$.

For a plane given by a point $p_0$, line L3 can be written $t \leftarrow n \cdot (p_0 - o) / \mathrm{den}$. In exact arithmetic it is the same; in floating point it is more accurate when the plane and the origin are far from the coordinate origin, as the second example shows.

## Example

**A floor.** The plane $z = 0$ has $n = (0, 0, 1)$ and $h = 0$. The ray starts at $o = (0, 0, 3)$ with $d = (1, 0, -2)$, and $(t_{\min}, t_{\max}) = (0, \infty)$.

| line | value | check |
|---|---|---|
| L1 | $\mathrm{den} = n \cdot d = -2$ | not zero, negative: the ray comes from the front |
| L3 | $t = (0 - 3) / (-2) = 1.5$ | |
| L4 | $0 < 1.5 < \infty$ | in the interval |
| L5 | $t = 1.5$, the hit point $o + 1.5\,d = (1.5, 0, 0)$ | |

**Far from the origin.** Take the double precision values $p_0 = (10^8 + 0.2,\ 10^8 - 0.4,\ 10^8 + 0.1)$, $n = (0.3, 0.7, 1.0)$, $o = (10^8 + 0.3,\ 10^8 + 0.7,\ 10^8 - 1.0)$ and $d = (0, 0, 1)$, so $\mathrm{den} = 1$.

| form of line L3 | computed $t$ in double precision |
|---|---|
| $h - n \cdot o$ with $h = n \cdot p_0$ | $0.30000001192092896$ |
| $n \cdot (p_0 - o)$ | $0.2999999895691873$ |
| exact, with rational arithmetic on the same inputs | $0.2999999895691872\ldots$ |

The values $h$ and $n \cdot o$ are both about $2 \times 10^8$, and each carries a rounding error of a few times $10^{-8}$. Their difference is $0.3$, so most of its digits are rounding error: this is [catastrophic cancellation](/catastrophic-cancellation/). The point-normal form subtracts the coordinates first, where the subtraction of nearby numbers is exact, and keeps 15 digits.

## Correctness

The points of the ray satisfy $n \cdot (o + t\,d) = n \cdot o + t\,(n \cdot d)$ by the linearity of the [dot product](/dot-product/). So the point with parameter $t$ is on the plane if and only if $n \cdot o + t\,\mathrm{den} = h$. If $\mathrm{den} \ne 0$, this linear equation has exactly the one solution of line L3, and line L4 returns it exactly when it is in the interval. If $\mathrm{den} = 0$, either no $t$ or every $t$ solves it, and both cases are MISS by the definition of the problem. The full proof is in the proofs folder.

In floating point the computed $t$ has a small relative error when $|h - n \cdot o|$ is not small compared with $|h|$ and $|n \cdot o|$. Near $\mathrm{den} = 0$, for a ray that grazes the plane, $t$ is large and very sensitive to the inputs; that is a property of the problem, whose [condition number](/condition-number/) grows like $1 / |\mathrm{den}|$, not of the method.

## Complexity

Line L1 is one dot product, 3 multiplications and 2 additions. Line L3 is another dot product, a subtraction and a division. Lines L2 and L4 are comparisons. So the test takes $\Theta(1)$ time and $O(1)$ extra space. A plane needs 4 numbers of storage, $n$ and $h$. When many planes are tested against one ray, as in the [slab method](/slab-method/) with axis-aligned planes, the dot products reduce to single coordinates and the division to a multiplication by a precomputed $1 / d_k$.

## Properties

- **Exact with rational inputs.** All steps are rational operations, so rational inputs give the exact $t$.
- **One hit at most.** A ray that is not parallel to a plane crosses it once, and the answer is unique.
- **Oriented.** The sign of den gives the side of the plane that the ray comes from.
- **Scale invariant.** Multiplying $n$ and $h$ by the same nonzero number does not change $t$, so the normal need not be normalized.

## Variants and improvements

- **Point-normal form.** $t = n \cdot (p_0 - o) / (n \cdot d)$ keeps the digits that $h - n \cdot o$ loses far from the coordinate origin, at the cost of 3 subtractions.
- **Back-face culling.** Return MISS when $\mathrm{den} > 0$, as in [back-face culling](/back-face-culling/) for rasterization.
- **Ray-polygon tests.** Intersect the plane of a polygon, then test the hit point in 2D, by projecting onto the coordinate plane where the polygon has the largest area and running [point in polygon](/point-in-polygon/). For triangles, the [Möller-Trumbore test](/moller-trumbore/) avoids the stored plane.
- **Ray-disk and ray-quad.** Intersect the plane, then test the distance to the center or two coordinates of the hit point.
- **Boxes.** The [slab method](/slab-method/) intersects the ray with three pairs of parallel planes and intersects the intervals.
- **Line-plane in homogeneous form.** A line and a plane in projective coordinates meet at a point given by a single product, the 3D analog of [line-line intersection](/line-line-intersection/) in the plane.

## When to use it

Use the test for floors, walls, water surfaces, clipping planes, and as the first step of a ray-polygon or ray-box test. Prefer the point-normal form when the scene is far from the coordinate origin, as in large outdoor or planetary scenes, or move the coordinate origin near the camera. For triangles, use a dedicated test such as [Möller-Trumbore](/moller-trumbore/) or the [watertight test](/watertight-ray-triangle-intersection/), which also give barycentric coordinates and handle shared edges.

## Pitfalls

- **Dividing before the parallel test.** Computing `t ← (h − n · o) / (n · d)` before line L2 divides by zero for a parallel ray. In floating point it gives an infinity or a NaN, and a NaN fails every comparison of line L4, so the bug can stay hidden. Test $\mathrm{den} = 0$ at line L2 first.
- **Hits behind the origin.** Returning $t$ from line L3 without the check of line L4 reports planes behind the camera. Keep `tmin < t < tmax` at line L4.
- **Self-intersection.** A reflected or shadow ray that starts on the plane has $h - n \cdot o \approx 0$ and finds the same plane at $t \approx 0$. Use $t_{\min} > 0$ at line L4, larger than the error of the origin.
- **Precision far from the origin.** The form $h - n \cdot o$ at line L3 loses digits when $|h|$ is large; use $n \cdot (p_0 - o)$ when a point of the plane is known.

## Implementations

## History

The formula is elementary analytic geometry, much older than computer graphics: it is the substitution of a parametric line into the equation of a plane. Ray tracers used it from the start, because polygons were intersected through their planes. The ray tracing texts of the 1980s, such as the chapter by Eric Haines in Glassner's An Introduction to Ray Tracing (1989), wrote down the test together with the ray-polygon test that builds on it. Later work on [triangles](/moller-trumbore/) and on [boxes](/slab-method/) refined how the planes are stored and how the divisions are shared.

## References
