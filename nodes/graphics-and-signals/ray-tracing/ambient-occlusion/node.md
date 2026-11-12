---
tag: HNQCM9
kind: algorithm
slug: ambient-occlusion
name: Ambient occlusion
aliases:
- AO
area: graphics-and-signals/ray-tracing
level: intro
summary: Estimate the cosine-weighted share of the hemisphere above a point that no surface blocks within a distance, by tracing random rays, and use it to darken ambient light in creases.
model: real-ram
complexity:
  vars: {N: the number of rays per point, c: the cost of one any-hit query}
  time: {worst: Θ(N c)}
  space: {extra: Θ(1)}
properties: {deterministic: false, recursive: false, online: false, in_place: true}
history:
  year: 1998
  people: [Sergey Zhukov, Andrei Iones, Grigorij Kronin]
  note: Zhukov, Iones and Kronin defined obscurance, a cosine-weighted mean of a function of the distance to the nearest surface. The binary form with a cutoff distance, called ambient occlusion, became common in film production in the early 2000s.
prereqs: [monte-carlo-integration, any-hit-query]
see_also: [path-tracing, rendering-equation, radiosity, shadow-determination, importance-sampling, stratified-sampling, quasi-monte-carlo-integration, lambertian-reflectance]
sources:
  - paper: doi:10.1007/978-3-7091-6453-2_5
    title: Sergey Zhukov, Andrei Iones and Grigorij Kronin, An ambient light illumination model, Rendering Techniques '98 (Proceedings of the Eurographics Workshop on Rendering), Springer, 1998
    locator: the obscurance of a point as a cosine-weighted integral of a function of the free distance
  - paper: "Hayden Landis, Production-ready global illumination, SIGGRAPH 2002 course notes, RenderMan in Production"
    locator: ambient occlusion and bent normals in film production
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 11.3, Ambient Occlusion
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: the chapter on Monte Carlo integration, cosine-weighted hemisphere sampling by Malley's method
---

Ambient occlusion gives each point $x$ of a surface a number $A(x)$ between $0$ and $1$: the share of the hemisphere above $x$ that is open, with each direction weighted by the cosine of its angle to the normal. A direction is open if a ray from $x$ in that direction meets no surface within a distance $d_{\max}$. The algorithm here estimates $A(x)$ by [Monte Carlo integration](/monte-carlo-integration/): it sends $N$ rays in random directions with the density $\cos\theta / \pi$, asks an [any-hit query](/any-hit-query/) for each, and returns the fraction that are open. A renderer then multiplies the ambient light at $x$ by $A(x)$, so creases, corners and contact points get darker. It is cheap and stable, and it gives an image depth, but it is not physically based: the value is the light of a uniform sky over black surroundings, not a solution of the [rendering equation](/rendering-equation/).

## In plain words

Stand at a point on a surface and look up at the sky. Out in an open field you see the whole sky. In a corner you see half of it or less. At the bottom of a narrow crack you see almost none.

Ambient occlusion puts a number on this. It sends a few random rays up from the point and counts how many get away without hitting anything nearby. If 6 of 8 rays get away, the point is three quarters open, and it gets three quarters of the soft light that comes from everywhere.

Rays near the top count more than rays near the horizon, because light from straight above falls on the surface more strongly. The method picks more rays near the top for that reason, so it can simply count.

## The problem

**Input.** A point $x$ on a surface, its unit normal $n$, the scene, a distance $d_{\max} \in (0, \infty]$, and a number of rays $N$.

**Output.** An estimate of

$$A(x) = \frac1\pi \int_\Omega V(x, \omega) \cos\theta \, d\omega,$$

where $\Omega$ is the hemisphere of directions with $\cos\theta = \omega \cdot n \ge 0$, and $V(x, \omega) = 1$ if the ray $x + t\omega$ meets no surface for $0 < t \le d_{\max}$ and $0$ otherwise. Because $\int_\Omega \cos\theta\, d\omega = \pi$, an open point has $A = 1$. Some texts call $1 - A$ the occlusion and some call $A$ itself the ambient occlusion; this page uses $A$, the open share.

**Obscurance.** Zhukov, Iones and Kronin (1998) defined the more general *obscurance* $W(x) = \frac1\pi \int_\Omega \rho(L(x, \omega)) \cos\theta\, d\omega$, where $L$ is the distance to the first surface in the direction $\omega$, and $\rho$ rises from $0$ at distance $0$ to $1$ at $d_{\max}$ and beyond. The step function $\rho$ gives back $A$.

## The algorithm

```pseudo id=main
AMBIENT-OCCLUSION(x, n, N, d_max)
L1  open ← 0
L2  for i ← 1 to N:
L3      draw u₁, u₂ uniform in [0, 1);  r ← √u₁;  φ ← 2π u₂
L4      ω ← r cos φ · t + r sin φ · b + √(1 − u₁) · n      ▷ (t, b, n) an orthonormal frame; density cos θ / π
L5      if no surface meets x + sω for 0 < s ≤ d_max then open ← open + 1   ▷ an any-hit query
L6  return open / N
```

Lines L3 and L4 are Malley's method: pick a uniform point of the unit disk and lift it straight up to the hemisphere. A disk point is uniform when its radius is $\sqrt{u_1}$, not $u_1$. Lifting it makes the density over directions $\cos\theta / \pi$, which cancels the cosine in the integral, so each ray adds exactly $0$ or $1$. Line L5 needs only to know whether something is hit before $d_{\max}$, not what is hit first, so it can stop at the first hit in any order.

## Example

**Eight rays next to a wall.** The point is the origin on a floor with $n = (0, 0, 1)$, a wall is the plane $p_1 = \tfrac12$, and $d_{\max} = 1$. A direction with $\omega_1 > 0$ meets the wall at the distance $\tfrac12 / \omega_1$. Eight rays from the implementation, with seed 3:

| ray | $u_1$ | $u_2$ | $\omega$ | wall at $t$ | blocked |
|---|---|---|---|---|---|
| 1 | 0.238 | 0.544 | (−0.134, 0.469, 0.873) | none | no |
| 2 | 0.370 | 0.604 | (−0.370, 0.483, 0.794) | none | no |
| 3 | 0.626 | 0.066 | (0.317, −0.725, 0.612) | 1.579 | no |
| 4 | 0.013 | 0.837 | (−0.098, −0.060, 0.993) | none | no |
| 5 | 0.259 | 0.234 | (0.507, −0.050, 0.861) | 0.987 | yes |
| 6 | 0.996 | 0.470 | (0.185, 0.980, 0.066) | 2.698 | no |
| 7 | 0.836 | 0.476 | (0.135, 0.905, 0.404) | 3.693 | no |
| 8 | 0.639 | 0.151 | (0.649, −0.467, 0.601) | 0.771 | yes |

Rays 3, 6 and 7 go toward the wall but meet it beyond $d_{\max}$, so they count as open. The estimate is $6 / 8 = 0.75$.

**The exact value.** By Lemma 1 of the proof, the projection $(\omega_1, \omega_2)$ of a ray is uniform on the unit disk, so $A$ is the open area of the disk divided by $\pi$. Here a ray is blocked when $\omega_1 \ge c = \tfrac12 / d_{\max}$, so $A = 1 - \operatorname{seg}(c)/\pi$ with $\operatorname{seg}(c) = \arccos c - c\sqrt{1 - c^2}$. For $d_{\max} = 1$, $c = \tfrac12$ and $A = 0.8045$. The eight rays above have the standard error $\sqrt{A(1 - A)/8} = 0.14$, and the estimate $0.75$ is well within it.

| $d_{\max}$ | 0.5 | 0.6 | 1 | 2 | 5 | $\infty$ |
|---|---|---|---|---|---|---|
| exact $A$ | 1 | 0.9602 | 0.8045 | 0.6575 | 0.5636 | 0.5 |

The value depends strongly on $d_{\max}$, which is a free parameter. With $d_{\max} = \infty$, the wall hides half of the sky, by weight, at every distance.

**Cosine against uniform directions.** For a sphere of radius $\tfrac12$ centered at the distance $1$ straight above the point, $A = 1 - (r/d)^2 = \tfrac34$. The cosine estimator has the variance $A(1 - A) = 0.1875$ per ray. The estimator with uniform directions, $2\cos\theta\, V$, has the variance $\tfrac43\cos^3\alpha - \cos^4\alpha = 0.3035$ per ray, where $\sin\alpha = r/d$. Measured root mean square errors over 2000 runs agree with $\sqrt{\text{variance} / N}$:

| $N$ | 16 | 64 | 256 | 1024 |
|---|---|---|---|---|
| cosine, measured | 0.108 | 0.054 | 0.028 | 0.014 |
| cosine, $\sqrt{0.1875 / N}$ | 0.108 | 0.054 | 0.027 | 0.014 |
| uniform, measured | 0.135 | 0.069 | 0.034 | 0.018 |
| uniform, $\sqrt{0.3035 / N}$ | 0.138 | 0.069 | 0.034 | 0.017 |

The error falls as $N^{-1/2}$, as for any plain Monte Carlo estimate.

## Correctness

By Lemma 1 of the [proof](proofs/correctness.md), the direction of lines L3 and L4 has the density $\cos\theta / \pi$. So each ray is a Bernoulli variable with the mean $\int_\Omega V \frac{\cos\theta}{\pi} d\omega = A(x)$, and the returned fraction has the mean $A(x)$ and the variance $A(1 - A)/N$. The estimate is unbiased for every scene and every $d_{\max}$. The proof also derives the closed forms that the tests use: $A = 1 - \operatorname{seg}(a / d_{\max})/\pi$ for a wall at the distance $a$, $A = 1 - (r/d)^2\cos\theta_c$ for a sphere above the horizon at the angle $\theta_c$, and $A = 1 - (d_{\max} / 2R)^2$ inside a closed sphere of radius $R$. It also gives a closed form for the obscurance with a linear $\rho$ next to a wall. The tests check each of these within 4 standard errors, and check that the uniform estimator has the larger variance.

**What $A$ is, physically.** If every other surface is black and emits nothing, $d_{\max} = \infty$, and the light from every open direction has the same radiance $L$, then the irradiance at $x$ is $\pi L A(x)$. This is the only case where ambient occlusion shading is exact. Inside a closed room with $d_{\max} = \infty$, $A = 0$ at every point, but light that bounces off the walls makes the room bright: in a closed sphere with emission $L_e$ and albedo $\rho < 1$, the radiance is $L_e / (1 - \rho)$ everywhere. Ambient occlusion ignores this light from other surfaces, which is the subject of [global illumination](/global-illumination/).

## Complexity

Each ray costs $O(1)$ for the direction and one any-hit query of cost $c$. So one point costs $\Theta(N c)$ time and $O(1)$ extra space. With a [bounding volume hierarchy](/bounding-volume-hierarchy/) and a short $d_{\max}$, the query visits few nodes, and a short $d_{\max}$ also lets it stop early. The error is $\sqrt{A(1 - A)/N} \le 1 / (2\sqrt N)$, so halving the error costs four times the rays.

## Properties

- **Unbiased for its own integral.** The estimate is unbiased for $A(x)$, with an error that is at most $1/(2\sqrt N)$ in standard deviation. It is biased as an estimate of the true light.
- **Bounded.** Each ray adds $0$ or $1$, so the estimate lies in $[0, 1]$ and has no fireflies, unlike [path tracing](/path-tracing/).
- **View independent.** $A(x)$ does not depend on the camera or on the lights, so it can be computed once for a static object and stored in a texture or at the vertices.
- **Local.** With a finite $d_{\max}$, only nearby geometry matters, which makes it fast and keeps a large ground plane from darkening everything.
- **Not physically based.** It is not a solution of the rendering equation, except in the special case above.

## Variants and improvements

- **Obscurance.** A function $\rho$ of the distance in place of the step, as Zhukov, Iones and Kronin first defined it. It removes the hard edge at $d_{\max}$; the tests check one closed form.
- **Bent normals.** Also average the open directions. Shading with this mean open direction in place of the normal looks up the environment light in the right place.
- **Stratified or low discrepancy rays.** [Stratified sampling](/stratified-sampling/) or [quasi-Monte Carlo](/quasi-monte-carlo-integration/) points in place of $(u_1, u_2)$ lower the error for the same $N$.
- **Screen-space ambient occlusion.** Real-time renderers estimate a similar value from the depth buffer only, by testing points near the pixel against the stored depths. It is fast and misses everything that the camera does not see.
- **Horizon-based methods.** In screen space, march in a few directions to find the horizon angle and integrate the cosine in closed form over each slice.
- **Precomputed and stored.** Compute $A$ once per vertex or per texel and store it, for static objects.
- **Denoised.** Use few rays per pixel and filter the result; the values are smooth, which makes this work well.

## When to use it

Use ambient occlusion where a cheap, stable cue of shape and contact is worth more than the right answer: real-time rendering, previews, technical and scientific images, and as an extra pass in production renders that artists can adjust. Use [path tracing](/path-tracing/) or another solution of the [global illumination](/global-illumination/) problem when the light from other surfaces matters, for example in interiors and for colored light that bounces off a wall. If the true lighting is computed, do not also multiply it by ambient occlusion: the darkening is then counted twice.

## Pitfalls

- **Uniform disk radius.** Taking $r = u_1$ in place of $\sqrt{u_1}$ puts too many rays near the normal, and the estimate is biased high near walls.
- **Self-intersection.** The first ray from $x$ can hit the surface that $x$ is on, at a distance near zero, and every ray then looks blocked. Start the ray at a small offset along the normal, or ignore hits below a small $\epsilon$.
- **No $d_{\max}$ in closed scenes.** Indoors, every ray eventually hits a wall, and $A = 0$ everywhere. Choose $d_{\max}$ by the size of the features you want to show.
- **Treating it as light.** $A$ multiplies ambient light; it does not add light. Applied to direct light, it darkens places that the light reaches.
- **The hard cutoff.** A ray that meets a surface at $0.99\,d_{\max}$ counts fully and one at $1.01\,d_{\max}$ does not count, which can show bands when $d_{\max}$ is close to the scale of the scene. Obscurance with a smooth $\rho$ fixes this.
- **Two conventions.** Some code returns $A$ and some returns $1 - A$. Check which one before multiplying.

## Implementations

## History

Zhukov, Iones and Kronin (1998) introduced obscurance as a cheap model of ambient light: a cosine-weighted integral over the hemisphere of a function of the free distance. The binary form with a cutoff, under the name ambient occlusion, became common in film production in the early 2000s, and Landis's SIGGRAPH 2002 course notes on its use at Industrial Light and Magic are often cited for this. Malley's method of sampling cosine-weighted directions through the disk is from Malley's 1988 thesis. Real-time renderers adopted screen-space versions from the late 2000s on.

## References
