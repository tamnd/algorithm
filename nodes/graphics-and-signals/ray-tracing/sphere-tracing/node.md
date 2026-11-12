---
tag: W0Z18J
kind: algorithm
slug: sphere-tracing
name: Sphere tracing
area: graphics-and-signals/ray-tracing
level: advanced
summary: Step along a ray by the value of a signed distance bound. Each step stays inside a ball free of surface, so the trace never passes the first hit, but it converges slowly at grazing angles.
solves: [ray-object-intersection]
model: real-ram
complexity:
  vars: {c: the cost of one evaluation of the distance bound, D: the maximum ray length, e: the stopping threshold}
  time: {worst: O((D/e) c), best: O(c)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, iterative: true, needs_lipschitz_bound: true, never_overshoots: true}
history:
  year: 1996
  people: [John C. Hart]
  note: Hart, Sandin and Kauffman used distance bounds (unbounding spheres) to ray trace 3D fractals in 1989. Hart's 1996 paper in The Visual Computer named sphere tracing, proved its convergence and gave distance bounds for many primitives and operations.
prereqs: [signed-distance-function, ray-marching]
see_also: [implicit-surface, fixed-point-iteration, newton-raphson-method, interval-arithmetic, ray-sphere-intersection, cone-tracing, ambient-occlusion, eikonal-equation]
sources:
  - paper: doi:10.1007/s003710050084
    title: John C. Hart, Sphere tracing, a geometric method for the antialiased ray tracing of implicit surfaces, The Visual Computer 12(10), 1996, pages 527 to 545
    locator: Section 2.1 (Definitions 2 and 3 and Theorem 1, distance bounds from Lipschitz bounds), Section 2.2 and Figure 1 (the algorithm and unbounding spheres), Section 2.3 (Theorem 2 and Corollary 2.1, linear convergence), Section 2.6 (enhancements) and Section 3 (antialiasing with cones)
  - paper: doi:10.1145/74334.74363
    title: John C. Hart, Daniel J. Sandin and Louis H. Kauffman, Ray tracing deterministic 3-D fractals, SIGGRAPH 1989, Computer Graphics 23(3), pages 289 to 296
    locator: the distance bound for quaternion Julia sets and its use as the step along the ray (unbounding spheres)
  - paper: doi:10.2312/stag.20141233
    title: Benjamin Keinert, Henry Schäfer, Johann Korndörfer, Urs Ganse and Marc Stamminger, Enhanced sphere tracing, Smart Tools and Apps for Graphics, Eurographics Italian Chapter Conference 2014, pages 1 to 8
    locator: the over-relaxed step with the overlap test that keeps it safe, and the faster test for convex objects
  - book: isbn:9780387954820
    title: Stanley Osher and Ronald Fedkiw, Level Set Methods and Dynamic Implicit Surfaces, Springer, 2003
    locator: Chapter 2, Signed Distance Functions (the 1-Lipschitz property and |∇φ| = 1)
---

Sphere tracing finds the first point where a ray $r(t) = o + t d$, with $\lVert d \rVert = 1$, meets a surface given by a *signed distance bound* $f$: a function with $|f(x)| \le \operatorname{dist}(x, f^{-1}(0))$ that is positive outside the shape. It repeats one step, $t \leftarrow t + f(r(t))$, and stops when $f(r(t)) < \varepsilon$. The value $f(r(t))$ is the radius of a ball around the current point that contains no surface, so the step can never jump over the first hit. A [signed distance function](/signed-distance-function/) is the best bound, and any function with Lipschitz constant $\lambda$ becomes a bound after division by $\lambda$. John Hart named and analyzed the method in 1996. It differs from fixed-step [ray marching](/ray-marching/), which uses only values, can use any field, and can miss thin features; sphere tracing needs the bound and cannot miss.

## In plain words

You stand somewhere outside a shape, and a helper tells you how far the nearest point of the shape is, in any direction. If the answer is 3, you can walk 3 units straight ahead and be sure that you did not walk through anything. Then you ask again and walk again.

When you head straight at a wall, the first answer is the whole distance, and you arrive in one step. When you walk almost parallel to a wall, the answers are small, because the wall is close to your side, so you take many short steps along it. When the helper only gives a safe underestimate, you are still safe, just slower. If the helper ever overestimates, you can walk through a thin wall without noticing.

## The problem

Given a continuous $f : \mathbb{R}^3 \to \mathbb{R}$, a ray origin $o$ with $f(o) > 0$, a unit direction $d$ and a maximum distance $D$, find the first root $t^* = \min\{t \ge 0 : f(r(t)) \le 0\}$ up to a tolerance, or report that the ray has no root in $[0, D]$. The method needs the bound condition $f(x) \le \operatorname{dist}(x, f^{-1}(0))$ at every point outside the shape. Hart's Definition 2 calls such an $f$ a signed distance bound, and his Theorem 1 shows that $f/\lambda$ is one whenever $\lambda$ bounds the Lipschitz constant of $f$.

## The algorithm

```pseudo id=main
L1  t ← 0
L2  repeat at most N times
L3      if t > D then return none                ▷ the ray left the scene
L4      δ ← f(o + t d)                           ▷ radius of a ball with no surface
L5      if δ < ε then return t                   ▷ close enough to the surface
L6      t ← t + δ                                ▷ the step stays inside the ball
L7  return none                                  ▷ too many steps, usually a grazing ray
```

This is Hart's Figure 1 with an explicit step limit $N$. The limit is not part of the guarantee: a ray that comes close to a surface without touching it takes many small steps, and the limit stops it.

## Example

The surface is the unit sphere with center $(0.6, 0, 5)$, the ray starts at the origin along the $z$ axis, $f(p) = \lVert p - c \rVert - 1$ and $\varepsilon = 10^{-4}$. The first hit is $t^* = 5 - \sqrt{1 - 0.36} = 4.2$. At the hit, the cosine between the ray and the surface normal is $0.8$.

| step | $t$ | $\delta = f(r(t))$ | gap $t^* - t$ | gap ratio |
|---|---|---|---|---|
| 0 | 0 | 4.035871 | 4.2 | |
| 1 | 4.035871 | 0.135581 | 0.164129 | 0.039 |
| 2 | 4.171452 | 0.022982 | 0.028548 | 0.174 |
| 3 | 4.194434 | 0.004458 | 0.005566 | 0.195 |
| 4 | 4.198892 | 0.000886 | 0.001108 | 0.199 |
| 5 | 4.199779 | 0.000177 | 0.000221 | 0.199 |
| 6 | 4.199956 | 0.000035 | 0.000044 | 0.200 |

The trace stops at step 6 with $\delta < \varepsilon$, after 7 evaluations. Every $t$ is below $t^*$. The gap shrinks by the factor $1 - \cos\theta = 1 - 0.8 = 0.2$ per step, the linear rate of the analysis below.

Move the sphere to $(0.99, 0, 5)$, so the ray hits near the silhouette with $\cos\theta = \sqrt{1 - 0.99^2} \approx 0.141$. Now the gap shrinks by about $0.859$ per step, and the trace needs 39 evaluations. At $(1, 0, 5)$ the ray is tangent to the sphere: the trace needs 138 evaluations and stops at $t = 4.9859$, a point within $10^{-4}$ of the surface but $0.014$ short of the touching point along the ray. At $(1.05, 0, 5)$ the ray misses; the trace slows down near the sphere and leaves after 22 evaluations, when $t > D = 12$.

## Correctness

Let $S = f^{-1}(0)$ and suppose the ray has a first root $t^*$. Then $r(t^*) \in S$ by continuity. For any $t < t^*$, the point $r(t)$ is outside, so

$$f(r(t)) \le \operatorname{dist}(r(t), S) \le \lVert r(t) - r(t^*) \rVert = t^* - t,$$

and the next value $t + f(r(t))$ is at most $t^*$. By induction, the trace never passes the first root. Each step that does not stop adds at least $\varepsilon$, so the trace stops after at most $D/\varepsilon + 1$ evaluations. As $\varepsilon \to 0$ the sequence increases, is bounded by $t^*$, and its limit is a root, so it converges to $t^*$ (Hart, Theorem 2). The full proof, with the rate of convergence, is in [the correctness proof](proofs/correctness.md).

The rate is linear. Near a simple root with an exact distance function, $f(r(t)) \approx \cos\theta\,(t^* - t)$, so the gap is multiplied by $1 - \cos\theta$ per step. Hart writes this as $g'(r) = 1 + F'(r)/\lambda$ for the map $g(t) = t + F(t)/\lambda$, and his Corollary 2.1 says that convergence is quadratic exactly when the ray meets the surface at the steepest possible angle. For a plane the factor is exact at every step. At a tangent point $\cos\theta = 0$, the factor tends to 1, and convergence becomes slower than linear, which is the 138-step case above.

## Complexity

Each iteration costs one evaluation of $f$, of cost $c$. For a scene that is the minimum of $n$ primitive distances, $c = O(n)$. The proved worst case is $O((D/\varepsilon)\,c)$ per ray, from the minimum step $\varepsilon$; it is reached by rays that run parallel to a surface at a distance just above $\varepsilon$. The best case is $O(c)$, when the ray starts within $\varepsilon$ of the surface. A head-on hit on an exact distance function takes one step and a second evaluation to stop. For a hit at angle $\theta$, about $\log(\varepsilon / t^*) / \log(1 - \cos\theta)$ steps are necessary; the typical count of a few tens of steps per ray in SDF renderers is measured, not proved. The extra space is $O(1)$.

## Properties

- **Never overshoots.** With a true distance bound, each point of the trace is in front of the first hit. This holds for every scene, not only on average.
- **No missed features.** A thin feature at distance $\delta$ from the ray limits the step to $\delta$, so it cannot be skipped. Compare with the fixed step of [ray marching](/ray-marching/).
- **Linear convergence.** The rate is $1 - \cos\theta$, fast for head-on rays and slow for grazing rays. It is like a [fixed-point iteration](/fixed-point-iteration/) whose derivative at the fixed point is $1 - \cos\theta$, and unlike [Newton's method](/newton-raphson-method/), which converges quadratically at simple roots but can jump past the first one.
- **Works with bounds.** Union, intersection and subtraction by min and max, and division by a Lipschitz constant, give bounds, not exact distances. The trace stays safe and takes more steps.
- **Stops near, not on, the surface.** The result is a point with $f < \varepsilon$. It is within $\varepsilon$ of the surface for an exact distance function, but along the ray it can be farther from the hit, by $\varepsilon/\cos\theta$ for a plane and more near a tangent point.

## Variants and improvements

- **Over-relaxation.** Keinert and others step by $\omega\,\delta$ with $1 < \omega < 2$. If the ball at the new point does not overlap the ball at the old point, the step was too long, and the trace goes back to the safe step $\delta$. This saves steps on long flat approaches.
- **Lipschitz scaling.** For a function $f$ that is not a distance, such as the algebraic sphere $x^2 + y^2 + z^2 - 1$, divide by a bound $\lambda$ on its gradient over the region of interest. In the implementation, $\lambda = 12$ on the ball of radius 6 gives a safe trace, but it needs more than 20 steps where the exact distance needs one.
- **Relative stopping threshold.** Stop when $\delta < \varepsilon t$ so that the tolerance grows with the distance, which matches the size of a pixel.
- **Cone tracing for antialiasing.** Hart's Section 3 joins the method with [cone tracing](/cone-tracing/). Along a ray that passes near a silhouette, the balls shrink inside the cone of the pixel and then grow out of it. Hart traces the inner cover $f + r_p$, with $r_p$ the radius of a pixel, takes the center of the smallest ball inside the cone as the sample, and estimates the coverage of the pixel from the radius of that ball.
- **Bounding volumes and convex objects.** Trace a cheap bound until close, then switch to the detailed field. For convex shapes, Hart's Theorem 4 allows larger steps.
- **Soft shadows and ambient occlusion.** Along a shadow ray, the ratio of $\delta$ to the distance travelled gives an estimate of how close the ray came to an occluder. Renderers use it for a penumbra and for [ambient occlusion](/ambient-occlusion/). These are approximations, not physical estimates.

## When to use it

Use sphere tracing for shapes given by a [signed distance function](/signed-distance-function/) or by a function with a known Lipschitz bound: scenes built from primitives with min, max and blends, fractals with distance estimators, offset and rounded shapes, and stored distance fields. It needs no mesh, no root bracketing and no derivative. Use fixed-step [ray marching](/ray-marching/) when no bound is known, and [interval arithmetic](/interval-arithmetic/) when the first root must be certified for an arbitrary function. Use analytic intersections such as [ray-sphere intersection](/ray-sphere-intersection/) when the shape is simple.

## Pitfalls

- **A function that is not a bound.** If $f$ overestimates the distance anywhere, for example after a non-uniform scale, a twist or a noise displacement, the trace can jump through thin parts. In the tests, three times the distance to a thin shell jumps past the shell in the first step. Divide by the Lipschitz constant, or by a safe bound of it.
- **Grazing rays.** Rays near silhouettes take many steps, and tangent rays stop short of the touching point. Set the step limit $N$ high enough, and treat a ray that ends at the limit as a hit near the silhouette or as a miss, by a fixed rule.
- **A fixed absolute threshold.** With $\varepsilon$ fixed, distant surfaces get the same tolerance as near ones, which wastes steps far away. Near large $t$, adding a small $\delta$ to $t$ in floating point does nothing once $\delta$ is below half an ulp of $t$ (see [machine epsilon](/machine-epsilon/)), and the trace stalls. Use $\varepsilon$ proportional to $t$, or above the ulp of $t$.
- **Self-intersection of secondary rays.** A reflection or shadow ray that starts at the returned point is already within $\varepsilon$ of the surface and stops at once. Start it at a distance of a few $\varepsilon$ along the normal.
- **A wrong sign inside.** The step uses $f$ directly. If $f$ is negative because the ray starts inside, the step goes backward. Trace with $-f$ for rays that start inside a shape, for example refracted rays.
- **Normals from the gradient.** The normal at the hit is $\nabla f$, often from central differences. A difference step much smaller than $\varepsilon$ gives noise from [catastrophic cancellation](/catastrophic-cancellation/); a step much larger blurs sharp edges.

## Implementations

## History

In 1989, Hart, Sandin and Kauffman ray traced quaternion Julia sets with a distance estimate: they stepped along each ray by a lower bound of the distance to the fractal, and called the ball with that radius an unbounding sphere. Hart's 1996 paper in The Visual Computer generalized the idea to any implicit surface with a Lipschitz bound and named it sphere tracing. It proved that the trace converges linearly to the first root (Theorem 2), gave distance bounds for primitives, for union and intersection (Theorem 3), and for blends and deformations, and used cones for antialiasing. Since the 2000s the method has been the standard way to render distance-function scenes on the GPU, and Keinert and others (2014) added the over-relaxed step.

## References
