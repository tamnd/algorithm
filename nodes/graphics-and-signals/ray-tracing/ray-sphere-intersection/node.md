---
tag: F1JA6J
kind: algorithm
slug: ray-sphere-intersection
name: Ray-sphere intersection
area: graphics-and-signals/ray-tracing
level: intro
summary: Find where a ray enters and leaves a sphere by solving a quadratic in the ray parameter, with a stable root formula and discriminant that avoid catastrophic cancellation.
solves: [ray-object-intersection]
model: floating-point-model
complexity:
  time: {worst: Θ(1)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [ray-object-intersection, quadratic-formula, catastrophic-cancellation]
see_also: [ray-plane-intersection, moller-trumbore, closest-hit-query, implicit-surface, signed-distance-function, sphere-tracing, bounding-volume, numerical-stability]
sources:
  - paper: doi:10.1007/978-1-4842-4427-2_7
    title: Eric Haines, Johannes Günther and Tomas Akenine-Möller, Precision improvements for ray/sphere intersection, in Ray Tracing Gems, Apress, 2019, 87 to 94
    locator: Chapter 7 (the stable roots and the discriminant from the closest point of the line)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 3.2 Spheres (the quadratic and its roots), and Section 3.9 Managing Rounding Error
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 22, Intersection Test Methods, Section 22.6 Ray/Sphere Intersection
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 4, Ray Tracing (ray-sphere intersection)
---

Ray-sphere intersection finds the parameters at which a ray $o + t\,d$ enters and leaves a sphere with center $c$ and radius $r$. Substituting the ray into $|x - c|^2 = r^2$ gives a quadratic equation in $t$, whose real roots are the two hits, one double root for a tangent ray, or none for a miss. The textbook root formula loses digits in two places, and the stable form here avoids both: it takes the root without a difference of nearly equal numbers, as the [quadratic formula](/quadratic-formula/) page explains, and it computes the discriminant from the closest point of the line to the center. It solves [ray-object intersection](/ray-object-intersection/) for spheres.

## In plain words

Along the ray, the distance to the center of the sphere first shrinks and then grows. The ray is inside the sphere while that distance is less than the radius. Squared, the distance is a quadratic function of $t$, so the two moments when it equals the radius are the two roots of a quadratic equation: the entry and the exit.

The usual formula for the roots subtracts two numbers that are almost equal when one root is much smaller than the other, which happens when the ray starts near the sphere or the sphere is large. The difference then keeps only a few correct digits. The stable form computes the large root first, without such a subtraction, and gets the small one from it by a division.

## The problem

The input is a ray $o + t\,d$ with $d \ne 0$, an open interval $(t_{\min}, t_{\max})$, and a sphere with center $c$ and radius $r > 0$, all in floating point. The output is the smallest $t$ in the interval with $|o + t\,d - c| = r$, or MISS. A renderer also uses both roots, for example to find where a ray inside the sphere leaves it, or as the interval of a [bounding volume](/bounding-volume/).

With $f = o - c$, the condition $|f + t\,d|^2 = r^2$ expands to

$$a t^2 + 2 b t + k = 0, \qquad a = d \cdot d,\quad b = f \cdot d,\quad k = f \cdot f - r^2,$$

with the reduced discriminant $\Delta = b^2 - a k$ and the roots $t = (-b \pm \sqrt{\Delta}) / a$.

## The algorithm

```pseudo id=main
RAY-SPHERE(o, d, c, r, tmin, tmax)
L1  f ← o − c
L2  a ← d · d;  b ← f · d;  k ← f · f − r²
L3  l ← f − (b / a) · d;  disc ← a · (r² − l · l)      ▷ equals b² − a k
L4  if disc < 0 then return MISS
L5  q ← −(b + sign(b) · √disc)                       ▷ no cancellation: both terms have one sign
L6  t0 ← k / q;  t1 ← q / a                          ▷ the two roots, by Vieta: t0 · t1 = k / a
L7  if t0 > t1 then swap t0 and t1
L8  return the first of t0, t1 in (tmin, tmax), or MISS if neither is
```

Line L2 writes the quadratic with the half coefficient $b$, so no factor 2 or 4 appears. Line L3 computes the discriminant in a form that does not cancel: $l$ is the vector from the center to the point of the ray line closest to it, and $\Delta = a\,(r^2 - |l|^2)$, because $|l|^2 = f \cdot f - b^2 / a$. The textbook form $b^2 - a k$ subtracts two numbers of size $|f|^2 |d|^2$ to get a number that can be much smaller, for a sphere that is far away compared with its radius.

Line L5 adds two numbers of the same sign, so $q$ is accurate. It equals $a$ times the root of larger magnitude, so line L6 gets that root as $q / a$ and the other as $k / q$, from the product of the roots, $t_0 t_1 = k / a$. The textbook formula computes the root of smaller magnitude as $(-b \pm \sqrt{\Delta}) / a$ with opposite signs, which cancels when $|a k| \ll b^2$. If $q = 0$, then $b = 0$ and $\Delta = 0$, which forces $k = 0$: the origin is on the sphere and the ray is tangent there, so both roots are 0.

Line L8 returns the entry $t_0$ when it is in the interval. When the origin is inside the sphere, $t_0 < 0 < t_1$ and line L8 returns the exit $t_1$.

## Example

**A unit sphere.** The sphere has $c = (0, 0, 0)$ and $r = 1$, and the ray starts at $o = (0, 0, -5)$ with $d = (0, 0, 1)$.

| line | value |
|---|---|
| L1 | $f = (0, 0, -5)$ |
| L2 | $a = 1$, $b = -5$, $k = 24$ |
| L3 | $b / a = -5$, $l = (0, 0, -5) + 5\,(0, 0, 1) = (0, 0, 0)$, $\mathrm{disc} = 1 \cdot (1 - 0) = 1$ |
| L4 | $\mathrm{disc} \ge 0$ |
| L5 | $q = -(-5 - 1) = 6$ |
| L6 | $t_0 = 24 / 6 = 4$, $t_1 = 6 / 1 = 6$ |
| L8 | $t = 4$: the ray enters at $(0, 0, -1)$ and leaves at $(0, 0, 1)$ |

**The small root of a large sphere.** A sphere with $c = 0$ and $r = 10^6$, and a ray from $o = (0, 0.5, -1000001)$ with $d = (0, 0, 1)$, one unit outside the sphere. In double precision:

| method | near root | relative error |
|---|---|---|
| textbook, $(-b - \sqrt{\Delta}) / a$ | $1.0000001250300556$ | $3 \times 10^{-11}$ |
| stable, $k / q$ | $1.000000125$ | $9 \times 10^{-17}$ |
| exact | $1.000000125000000000008\ldots$ | |

The textbook formula subtracts $\sqrt{\Delta} \approx 1000000$ from $-b = 1000001$, and keeps about 11 digits of 16.

**The discriminant of a far sphere.** A unit sphere at the origin and a ray from $o = (0, 0.5, -10^8)$ with $d = (0, 0, 1)$. The textbook discriminant $b^2 - a k$ subtracts two numbers near $10^{16}$, whose rounding errors are about 1, from each other, to get the true value $0.75$; it computes 0, as if the ray were tangent, and both roots become $10^8$. The stable discriminant gives $0.75$ and the roots $99999999.13397460$ and $100000000.86602540$, correct to the last digit. With $o = (0, 1.1, -10^8)$ the ray misses; the textbook discriminant is again 0 and reports a touch, while the stable form reports a miss.

## Correctness

In exact arithmetic, the identity $|l|^2 = f \cdot f - b^2 / a$ gives $\mathrm{disc} = a r^2 - a\,f \cdot f + b^2 = b^2 - a k$, so line L4 rejects exactly the rays whose quadratic has no real root. Line L5 gives $q = -(b + \mathrm{sign}(b)\sqrt{\Delta})$, which is $a$ times one root, and $k / q$ is the other root by Vieta's formula. Line L8 then returns the smallest root in the interval. The full proof is in the proofs folder.

In floating point, each of $q$ and the discriminant is computed without cancellation, so the roots have small relative errors in the cases that break the textbook formula. One loss remains: $k = f \cdot f - r^2$ itself cancels when the origin is close to the surface of a large sphere. Its absolute error is about $\varepsilon\,|f|^2$ for the unit roundoff $\varepsilon$ of the [machine epsilon](/machine-epsilon/) page, which moves the small root by about $\varepsilon\,|f| / |d|$. When that matters, as for a secondary ray that starts on the sphere, the fixes are a $t_{\min}$ larger than this error, or a hit point refined by one more step, or the error bounds of PBRT (its Section 3.9). The method is accurate in the stable form, but not exact: a ray within a few rounding errors of tangent can be reported as a hit or a miss.

## Complexity

Line L1 is 3 subtractions; line L2 is three dot products and a subtraction; line L3 is a division, 3 multiplications and subtractions, a dot product and a multiplication; lines L5 and L6 are a square root, two divisions and an addition. So the test takes $\Theta(1)$ time and $O(1)$ extra space. The stable discriminant costs one division and about 10 more operations than the textbook one. A sphere needs 4 numbers of storage.

## Properties

- **Two roots.** The test gives both the entry and the exit, so it serves as an interval for constructive solid geometry and for volumes.
- **Hits from the inside.** A ray that starts inside gets the exit, at line L8.
- **Scale invariant.** Scaling $d$ by a positive factor scales both roots by its inverse and does not change the hit points.
- **Stable.** In floating point, $q$ and the discriminant have small relative errors; the textbook formula does not.
- **Tangent rays.** A tangent ray has one double root; rounding can turn it into a close pair of roots or a miss.

## Variants and improvements

- **Normalized directions.** With $|d| = 1$, $a = 1$ and the divisions by $a$ disappear.
- **The geometric test.** Project the center onto the ray first: $t_c = -b / a$ is the closest approach, and $r^2 - |l|^2$ decides the hit. This is the same computation as lines L3 to L6 in another order, and allows early exits when the sphere is behind the origin and the origin is outside.
- **Other quadrics.** Cylinders, cones and ellipsoids give quadratics in $t$ in the same way, with the same stable root formula.
- **Implicit surfaces.** For a general [implicit surface](/implicit-surface/) no closed form exists, and the hit is found numerically, for example by [sphere tracing](/sphere-tracing/) of a [signed distance function](/signed-distance-function/).
- **Rounding error bounds.** PBRT carries a bound on the error of the hit point with each intersection, and offsets the origin of secondary rays by it (its Section 3.9).

## When to use it

Use the test for spheres in a scene, for bounding spheres, and as the first test of a ray tracer, since the sphere has the simplest exact intersection of a curved surface. Always use the stable form: it costs a few operations more, and the textbook formula fails for large spheres such as planets and for rays that start near a surface, which are common for secondary rays. For a sphere that is very far from both the origin and the coordinate origin, translate the scene so that the camera is near the coordinate origin as well.

## Pitfalls

- **The textbook root.** Writing line L6 as `t0 ← (−b − √disc) / a` loses digits when $|a k| \ll b^2$, as in the second example. Use $q$ and $t_0 = k / q$.
- **The textbook discriminant.** Writing line L3 as `disc ← b · b − a · k` reports far rays as tangent or as hits that miss. Use $a\,(r^2 - |l|^2)$.
- **The sign of b.** Writing line L5 as `q ← −(b + √disc)` without the sign of $b$ cancels for $b > 0$. Use $\mathrm{sign}(b)$, with $\mathrm{sign}(0) = 1$.
- **Only the entry.** Returning $t_0$ without the test of line L8 reports a hit behind the origin when the origin is inside the sphere. Test both roots against the interval.
- **The factor of four.** Mixing the full form $B = 2 f \cdot d$ with the reduced discriminant $b^2 - a k$ gives wrong roots. Use the half coefficient $b$ throughout, as at line L2.

## Implementations

## History

Spheres were among the first objects in ray traced images: Turner Whitted's 1980 paper on recursive ray tracing showed reflecting and refracting spheres, and the intersection by a quadratic equation was standard in the ray tracing texts of the 1980s. The numerical side was noted many times; in 2019 Eric Haines, Johannes Günther and Tomas Akenine-Möller collected the two fixes, the stable root of the quadratic formula and the discriminant from the closest point of the line, in a chapter of Ray Tracing Gems.

## References
