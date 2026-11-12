---
tag: DR3SGB
kind: algorithm
slug: ray-marching
name: Ray marching
area: graphics-and-signals/ray-tracing
level: intro
summary: Sample a field at fixed steps along a ray. For a surface, stop at the first sign change and refine it by bisection; for a volume, sum the density. Features thinner than a step can be missed.
solves: [ray-object-intersection]
model: real-ram
complexity:
  vars: {m: "the number of steps, ⌈(t1 - t0)/Δ⌉", k: the number of bisection steps, c: the cost of one evaluation of the field}
  time: {worst: O((m + k) c), best: O(c)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, iterative: true, needs_lipschitz_bound: false}
history:
  year: 1984
  people: [James T. Kajiya, Brian P. Von Herzen, Ken Perlin, Eric M. Hoffert, Marc Levoy]
  note: Kajiya and Von Herzen integrated volume densities along rays in 1984. Levoy (1988) and Perlin and Hoffert (1989) sampled density fields at even steps along each ray, the fixed-step marching of this page.
prereqs: [ray-casting, bisection-method]
see_also: [sphere-tracing, signed-distance-function, implicit-surface, participating-media, delta-tracking, amanatides-woo-traversal, interval-arithmetic, aliasing]
sources:
  - paper: doi:10.1109/38.511
    title: Marc Levoy, Display of surfaces from volume data, IEEE Computer Graphics and Applications 8(3), 1988, pages 29 to 37
    locator: the casting of rays through the volume with samples at evenly spaced points and the front-to-back composition of the samples
  - paper: doi:10.1145/74334.74359
    title: Ken Perlin and Eric M. Hoffert, Hypertexture, SIGGRAPH 1989, Computer Graphics 23(3), pages 253 to 262
    locator: the rendering section (marching along each ray through the density function at a fixed step and accumulating density)
  - paper: doi:10.1145/964965.808594
    title: James T. Kajiya and Brian P. Von Herzen, Ray tracing volume densities, SIGGRAPH 1984, Computer Graphics 18(3), pages 165 to 174
    locator: the integration of the density along each ray through a grid of densities
  - paper: doi:10.1007/s003710050084
    title: John C. Hart, Sphere tracing, a geometric method for the antialiased ray tracing of implicit surfaces, The Visual Computer 12(10), 1996, pages 527 to 545
    locator: Section 1.1 (the blind ray marching of Hypertexture, and the thin region between two samples that any root finder that uses only values can miss)
---

Ray marching evaluates a field at evenly spaced points $t_0, t_0 + \Delta, t_0 + 2\Delta, \ldots$ along a ray $r(t) = o + t d$. For a surface given as the zero set of a function $f$, it stops at the first sample where the sign of $F(t) = f(r(t))$ changes from positive to non-positive and then refines the root with [bisection](/bisection-method/). For a volume such as fog or smoke, it adds the density times the step at each sample to estimate the optical depth. The method needs nothing from $f$ except values, so it works for any [implicit surface](/implicit-surface/), not only for a [signed distance function](/signed-distance-function/). The price is that a part of the surface thinner than one step can lie between two samples and be missed. [Sphere tracing](/sphere-tracing/) is the variant that sets each step from a distance bound, and it cannot miss; this page is about the fixed step.

## In plain words

You walk along a straight line in the dark with a stick of fixed length. At each step you check whether you are inside something. When you first find yourself inside, you know that the edge is somewhere in your last step, so you go back half a step, check again, and keep halving until you know the edge well enough.

The weak point is the step length. If a thin wall stands between two of your footprints, you never stand inside it, and you walk through it without noticing. Shorter steps make this less likely but cost more checks. If you also know how fast the field can change, you can at least tell which steps might have hidden a wall.

## The problem

Given a continuous function $F : [t_0, t_1] \to \mathbb{R}$ with $F(t_0) > 0$ (the ray starts outside), find the first root $t^* = \min\{t \ge t_0 : F(t) \le 0\}$, or report that $F > 0$ on $[t_0, t_1]$. Here $F(t) = f(o + t d)$ for a field $f$ that is negative inside the shape. The field is a black box: the algorithm only evaluates it. A related problem is the volume integral $\tau = \int_{t_0}^{t_1} \sigma(r(t))\,dt$ of a density $\sigma$; the transmittance along the ray is $e^{-\tau}$.

## The algorithm

```pseudo id=main
L1  t ← t0, j ← 0
L2  if F(t) ≤ 0 then return t                    ▷ the ray starts inside
L3  while t < t1 do
L4      j ← j + 1, t' ← min(t0 + jΔ, t1)        ▷ next sample, no running sum
L5      evaluate F(t')
L6      if F(t') ≤ 0 then                        ▷ sign change in [t, t']
L7          a ← t, b ← t'
L8          repeat k times
L9              m ← (a + b) / 2
L10             if F(m) > 0 then a ← m else b ← m
L11         return b                             ▷ F(b) ≤ 0, a root in [a, b]
L12     t ← t'
L13 return none
```

Line L11 returns the right end of the bracket, the point that is known to be inside. A shading step that needs a point on the surface can use $(a + b)/2$. The volume version replaces lines L6 to L11 by $\tau \leftarrow \tau + \sigma(r(t + \Delta/2))\,\Delta$, the midpoint rule, and returns $e^{-\tau}$ after the loop.

**Lipschitz certificate.** If $|F(x) - F(y)| \le L |x - y|$ and both ends of a step are outside, then

$$F(t) + F(t') > L (t' - t) \implies F > 0 \text{ on } [t, t'],$$

because a root $r$ in the step would give $F(t) \le L(r - t)$ and $F(t') \le L(t' - r)$, and the sum would be at most $L(t' - t)$. The implementation records whether each skipped step passed this test. A step that fails it might hide a thin feature. For a [signed distance function](/signed-distance-function/), $L = 1$.

## Example

The scene is the union of two spheres, written as the minimum of their distance functions. Sphere $A$ has center $(0.6, 0, 5)$ in the frame of the ray and radius 1. Sphere $B$ is thin: center $(0.25, 0, 2.5)$, radius $0.3$. The ray starts at the origin along the $z$ axis, so $F(t) = \min(\sqrt{0.36 + (t - 5)^2} - 1,\ \sqrt{0.0625 + (t - 2.5)^2} - 0.3)$. The ray meets $B$ on $[2.3342, 2.6658]$, a chord of length $0.33$, and meets $A$ first at $t = 5 - 0.8 = 4.2$.

With $\Delta = 1$:

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $F(t)$ | 2.2125 | 1.2207 | 0.2590 | 0.2590 | 0.1662 | −0.4000 |
| $F(t) + F(t + 1)$ | 3.4332 | 1.4797 | 0.5180 | 0.4252 | | |

The first sign change is in $[4, 5]$. Bisection then runs:

| step | $a$ | $b$ | $m$ | $F(m)$ |
|---|---|---|---|---|
| 1 | 4 | 5 | 4.5 | −0.2190 |
| 2 | 4 | 4.5 | 4.25 | −0.0395 |
| 3 | 4 | 4.25 | 4.125 | 0.0610 |
| 4 | 4.125 | 4.25 | 4.1875 | 0.0100 |
| 5 | 4.1875 | 4.25 | 4.21875 | −0.0149 |
| 6 | 4.1875 | 4.21875 | 4.203125 | −0.0025 |

After six steps the bracket is $[4.1875, 4.203125]$ and contains the root $4.2$ of sphere $A$. But this is the wrong surface: the thin sphere $B$ lies between the samples 2 and 3, where $F = 0.2590$ at both ends, and the march walked through it. The certificate shows the risk: $F(2) + F(3) = 0.518 \le 1 = L\Delta$, so the step $[2, 3]$ is not certified free of roots. The step $[3, 4]$ also fails the test ($0.4252 \le 1$) but holds no root; the test is conservative.

With $\Delta = 0.25$ the samples are $F(2.25) = 0.0536$ and $F(2.5) = -0.05$, so the march stops in $[2.25, 2.5]$ and bisection converges to the true first root $2.3342$.

## Correctness

The returned value is always inside the shape, and a root lies within $\Delta/2^k$ to its left. If the first inside part of the ray is at least one step long, that root is the first root. The full proof is in [the correctness proof](proofs/correctness.md); here is the outline.

*Safety.* Line L11 returns $b$ with $F(b) \le 0$, and the [loop invariant](/loop-invariant/) $F(a) > 0 \ge F(b)$ of lines L8 to L10 gives a root in $[a, b]$ by the intermediate value theorem. Since $t^*$ is the first point with $F \le 0$, $t^* \le b$: the march never reports a hit before the first root.

*First root.* Let $I = [t^*, e]$ be the first maximal interval where $F \le 0$. If $e - t^* \ge \Delta$ or $e = t_1$, then $I$ contains a sample, and the first sample with $F \le 0$ is in $I$. Then on the bracket, $F(m) > 0$ exactly when $m < t^*$, so bisection keeps $a < t^* \le b$, and $b - t^* < \Delta / 2^k$.

*Thin features.* If $e - t^* < \Delta$, the samples can all miss $I$. The example above shows this. No fixed step avoids it for every field: for each $\Delta$, the field $|t - c| - \varepsilon$ with $2\varepsilon < \Delta$ has an inside interval of length $2\varepsilon$ that fits between two samples. Hart makes the same point for every method that only evaluates the function: a function can dip to zero and back between any two samples. More information, such as a Lipschitz bound or interval bounds, is necessary for a guarantee.

## Complexity

Each pass of the loop evaluates $F$ one time, and there are at most $m = \lceil (t_1 - t_0)/\Delta \rceil$ passes. Bisection adds $k$ evaluations. So the time is $O((m + k)c)$, where $c$ is the cost of one evaluation, and $O(c)$ in the best case, when the ray starts inside. For a scene that is the minimum of $n$ primitive fields, $c = O(n)$, and the march is $O((m + k) n)$ per ray. This is a proved bound. In practice an acceleration structure makes $c$ much smaller than $n$, but that is measured, not proved. The extra space is $O(1)$.

The step trades cost against safety. Halving $\Delta$ doubles $m$ and halves the thickness of the thinnest feature that is sure to be found. The volume sum is the midpoint rule, with error $O(\Delta^2)$ for a density with a bounded second derivative along the ray, and no error for a density that is linear on each step.

## Properties

- **Black box.** Only values of $f$ are needed, no gradient and no distance bound. This is why the method works for noise, fractals and measured volume data.
- **Never early.** A reported hit is never in front of the true first root; the error is always a miss or a hit on a farther part of the surface.
- **Not complete.** Features thinner than $\Delta$, and grazing hits where the ray only touches the surface, can be missed. A tangent touch is an inside interval of length zero.
- **Uniform cost.** The number of steps depends on the length of the ray and on $\Delta$, not on the distance to the surface. Empty space costs as much as space near the surface.
- **Deterministic.** The same ray gives the same samples. With a random offset of the first sample per pixel, the misses become noise in place of regular bands.

## Variants and improvements

- **Sphere tracing.** Use a distance bound as the step. [Sphere tracing](/sphere-tracing/) takes large steps in empty space and never passes the surface, but it needs a Lipschitz bound.
- **Certified steps.** With a Lipschitz bound $L$, refine only the steps that fail the test $F(t) + F(t') > L\Delta$. This gives a correct first root at the cost of more evaluations near the surface.
- **Interval methods.** Evaluate $F$ on a whole step with [interval arithmetic](/interval-arithmetic/). If the interval excludes zero, the step is safe; if not, split it. This finds the first root without a step size, at the cost of interval evaluation.
- **Regula falsi and secant refinement.** Replace bisection by [regula falsi](/regula-falsi/) or the [secant method](/secant-method/) for faster convergence on smooth simple roots.
- **Volume marching.** For [participating media](/participating-media/), sum density and in-scattered light at each step. A random offset (jitter) per ray turns the bias into noise. Unbiased estimators such as [delta tracking](/delta-tracking/) avoid the fixed step altogether.
- **Grid-aligned steps.** For data on a voxel grid, step exactly from cell to cell with the [Amanatides and Woo traversal](/amanatides-woo-traversal/), so no cell is skipped.

## When to use it

Use fixed-step ray marching when the field has no useful distance bound: procedural noise, measured densities, fluid simulations, clouds, and implicit surfaces built from arbitrary functions. Choose $\Delta$ smaller than the thinnest feature that must appear, and add jitter to hide the banding. Use [sphere tracing](/sphere-tracing/) when the field is a [signed distance function](/signed-distance-function/) or a Lipschitz bound is known, because it is both faster in empty space and safe. Use an analytic intersection such as [ray-sphere intersection](/ray-sphere-intersection/) when one exists.

## Pitfalls

- **A step larger than the thinnest feature.** Thin walls, fine hair, and sharp edges disappear, and grazing rays leak through silhouettes. Show the certificate failures in a debug image to find them.
- **A running sum for $t$.** Computing $t \leftarrow t + \Delta$ in floating point drifts by about $m$ ulps after $m$ steps (see [machine epsilon](/machine-epsilon/)). Line L4 computes $t_0 + j\Delta$ directly.
- **Banding.** A fixed grid of sample positions shared by all pixels gives visible bands on smooth surfaces and in fog, a form of [aliasing](/aliasing/). Offset the first sample by a random fraction of $\Delta$ per pixel.
- **Returning the left end.** Returning $a$ in line L11 gives a point that is outside the surface. A shadow ray that starts there can hit the same surface again. Return $b$, or move the start along the normal.
- **Starting inside.** A ray that starts inside a shape returns $t_0$ at line L2. Secondary rays that start on a surface must start a small distance away, or they report a hit at once.
- **Confusing it with sphere tracing.** Some authors call sphere tracing "ray marching". The two have different guarantees: the fixed step can miss, the distance step cannot.

## Implementations

## History

Rendering of volume densities by sampling along rays goes back to Kajiya and Von Herzen (1984), who integrated scattering through a grid of densities. Levoy (1988) cast rays through volume data and composited samples taken at evenly spaced points, and Perlin and Hoffert (1989) marched along rays through procedural density functions to render hypertexture such as fur and fire. For implicit surfaces, fixed steps with a root refinement were the simple alternative to the root isolation methods of the 1980s. Hart (1996) discusses those methods and replaces the fixed step by a step from a distance bound, which gives sphere tracing.

## References
