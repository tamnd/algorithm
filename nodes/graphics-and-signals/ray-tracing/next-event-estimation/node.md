---
tag: WJBAKB
kind: technique
slug: next-event-estimation
name: Next event estimation
aliases:
- direct light sampling
area: graphics-and-signals/ray-tracing
level: advanced
summary: At each vertex of a path, sample a point on a light, test its visibility with a shadow ray and add its direct light. Hits on emitters by the next ray are then not counted again.
prereqs: [path-tracing]
see_also: [multiple-importance-sampling, restir, bidirectional-path-tracing, light-tracing, any-hit-query, importance-sampling, instant-radiosity]
sources:
  - paper: doi:10.1145/15886.15902
    title: James T. Kajiya, The rendering equation, Computer Graphics (SIGGRAPH 86) 20(4), 1986, 143 to 150
    locator: the path tracing method, which sends a ray to a random point on a light at each vertex
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 14.2 Sampling Light Sources, Section 14.3 Direct Lighting, Section 14.5 Path Tracing
  - paper: doi:10.1145/226150.226151
    title: Peter Shirley, Changyaw Wang and Kurt Zimmerman, Monte Carlo techniques for direct lighting calculations, ACM Transactions on Graphics 15(1), 1996, 1 to 36
    locator: sampling points on area lights and choosing among many lights
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 9, Multiple Importance Sampling (light sampling and BSDF sampling of direct light compared and combined)
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, A K Peters, 2006
    locator: Chapter 5, Stochastic Path-Tracing Algorithms (direct illumination and the split of the integral into direct and indirect parts)
---

Next event estimation adds, at each vertex $x$ of a [path tracing](/path-tracing/) path, the light that arrives at $x$ straight from a light source: it samples a point $y$ on a light, tests by a shadow ray whether $y$ is visible from $x$, and adds the reflected light divided by the density of $y$. The next random direction then carries only indirect light, so emission that it happens to hit is not counted again. A small light that a random direction would almost never hit is found at every vertex, which lowers the [variance](/variance/) by a large factor, and point lights, which a random direction never hits, become possible at all. It is a form of [importance sampling](/importance-sampling/) of the direct part of the [rendering equation](/rendering-equation/).

## In plain words

Plain path tracing finds a lamp only when a random bounce happens to go toward it. A small lamp is hit by few bounces, so its light comes in rare, very bright samples, and the image is noisy.

Next event estimation asks the lamp directly. At each point of the path, it picks a random point on a lamp and checks whether anything blocks the straight line between the two. If nothing blocks it, the light from that point is added now. Then the path goes on with a random bounce as before. If that bounce lands on a lamp by chance, its light is not added a second time, because the direct light of the lamp was already counted at the step before.

## When it applies

- **The light comes from emitters that can be sampled.** There is a way to pick a point on the lights with a known density, by area or by solid angle, and to evaluate the emission there. Point and directional lights also work.
- **The surface reflects light from a range of directions.** The BRDF can be evaluated for a given pair of directions. For an ideal mirror or glass, the BRDF of a sampled light direction is $0$, and the method does nothing.
- **Lights are small or the scene is dark.** The gain is large when the lights cover a small solid angle. When a light fills most of the sky of a glossy surface, sampling the BRDF is better, and [multiple importance sampling](/multiple-importance-sampling/) combines the two.

## The template

The integral at a vertex is split into direct light, from emitters, and indirect light, from the light that other surfaces reflect. For direct light, the integral over directions is written over the area of the lights:

$$L_{\text{direct}}(x, \omega_o) = \int_{A_e} f(x, \omega_y, \omega_o)\, L_e(y, -\omega_y)\, V(x, y)\, \frac{\cos\theta_x \cos\theta_y}{|y - x|^2}\, dA(y),$$

with $\omega_y$ the unit vector from $x$ to $y$ and $V$ the visibility. One sample $y$ with the area density $p_A(y)$ gives the estimate $f\, L_e\, V\, G / p_A(y)$, where $G = \cos\theta_x \cos\theta_y / |y - x|^2$.

```pseudo id=main
NEE-PATH-TRACE(o, d)
L1  L ← 0;  β ← 1;  k ← 0
L2  x ← CLOSEST-HIT(o, d);  if there is no hit then return L
L3  L ← L + Le(x, −d)                              ▷ emission only on the camera ray
L4  loop while the path may go on
L5      sample y on the lights with the area density pA(y)       ▷ hole: the light sampler
L6      ω ← unit(y − x);  G ← cos θx · cos θy / |y − x|²
L7      if cos θx > 0, cos θy > 0 and VISIBLE(x, y) then L ← L + β · f(x, ω, −d) · Le(y, −ω) · G / pA(y)
L8      sample ω′ with the density p(ω′);  β ← β · f(x, ω′, −d) · cos θ′ / p(ω′)      ▷ hole: the BSDF sampler
L9      Russian roulette with a survival q: stop if u ≥ q, else β ← β / q
L10     d ← ω′;  x ← CLOSEST-HIT(x, ω′);  if there is no hit then return L
L11     k ← k + 1
```

Line L7 is an [any-hit query](/any-hit-query/) between $x$ and $y$, usually cheaper than a closest hit. The holes are the light sampler of line L5, the BRDF and its sampler of line L8, and the survival rule of line L9 (see [Russian roulette](/russian-roulette/)).

**Why it is unbiased.** Write $L = L_e + K L = L_e + K L_e + K (L - L_e)$, where $K$ is the transport operator. Line L7 is an unbiased estimate of $K L_e$ at $x$, because the change of variables from directions to light area has the Jacobian $\cos\theta_y / |y - x|^2$, and the density $p_A$ is positive on every emitter. The next ray of line L8 estimates $K (L - L_e)$, the reflected light without the emission of the next vertex, and that is what lines L5 to L7 at the next vertex supply. Each light path with $k \ge 1$ bounces is counted once: by the light sample at its last surface vertex. The proof of [path tracing](/path-tracing/) carries over term by term.

**A common light sampler.** Choose a light with probability proportional to its power, then a point uniform on its area. For emitters with the radiance $E_i$ and the area $A_i$, this gives $p_A(y) = E(y) / \Phi$ with $\Phi = \sum_i E_i A_i$, so the estimate of line L7 is $f\, \Phi\, V\, G$.

## Classic examples

**A small light in a closed sphere.** The inside of a unit sphere has three zones: $z < 0$ with albedo $\tfrac34$, $0 \le z < 0.9$ with albedo $\tfrac12$, and a cap $z \ge 0.9$ that emits radiance $20$. A cosine sampled ray from any wall point lands uniformly by area on the sphere, so it hits the cap with probability $\tfrac{1}{20}$. The incident radiance $C$ is the same everywhere and solves $C = \tfrac{1}{20} \cdot 20 + (\tfrac12 \cdot \tfrac34 + \tfrac{9}{20} \cdot \tfrac12)\, C = 1 + \tfrac35 C$, so $C = \tfrac52$, and the camera at the center sees $\tfrac{15}{8}$ on the lower zone, $\tfrac54$ on the middle zone and $20$ on the cap. For the lower pixel with seed 1 and 1000 paths:

| method | mean | standard error |
|---|---|---|
| path tracing, no light sampling | $1.7600$ | $0.1793$ |
| next event estimation | $1.8735$ | $0.0418$ |

Both are within 1 standard error of $\tfrac{15}{8} = 1.875$. The ratio of the variances is about $18$, at a cost of one shadow ray per vertex. In this scene, $G / p_A$ is the same for every light point and every point is visible, so each light sample has zero variance; the noise that is left comes from the random length of the path.

**Occlusion.** A sphere of radius $2$ that reflects with albedo $\tfrac45$ holds an emitting sphere of radius $\tfrac35$ with radiance $1$ at its center. From a point of the outer wall at distance $2$, only the cap of the inner sphere that faces it is visible, a fraction $(1 - \tfrac{0.6}{2}) / 2 = 0.35$ of its area. So 65 percent of the uniform light samples fall on hidden points and line L7 adds $0$ for them. The mean of the direct light is the albedo times the form factor $(\tfrac{r}{R})^2 = \tfrac{9}{100}$ times the radiance, $\tfrac45 \cdot \tfrac{9}{100} \cdot 1 = 0.072$, and the light sample now has a positive variance.

**[Path tracing](/path-tracing/) as Kajiya wrote it.** Kajiya's method of 1986 sent a ray to a random point of a light at each vertex. Most production path tracers do the same, with MIS.

**[Bidirectional path tracing](/bidirectional-path-tracing/).** Next event estimation is the strategy with one light vertex, $s = 1$. Connecting a light path vertex to the camera, as [light tracing](/light-tracing/) does, is the same idea at the other end of the path.

**[ReSTIR](/restir/).** It improves the light sample of line L5 by resampling many candidate lights and reusing samples between pixels.

**[Instant radiosity](/instant-radiosity/).** It treats the vertices of light paths as virtual point lights and connects each camera vertex to them with shadow rays.

## Variations

- **Several light samples per vertex.** Average $m$ light samples at line L5, a form of splitting. It helps when the shadow ray is cheap compared with the path.
- **Solid angle sampling.** For a spherical light, sample the cone that it subtends from $x$; this avoids the points on its far side, which waste shadow rays.
- **Many lights.** Choose a light by a tree that bounds the power and the direction of groups of lights, so that the chosen light is likely bright at $x$.
- **MIS with BSDF sampling.** Count the emitter that line L10 hits, weighted by a [multiple importance sampling](/multiple-importance-sampling/) weight, and weight line L7 to match. This is the usual form in renderers.
- **Delta lights.** For a point light of intensity $I$ at $y$, the integral of line L7 collapses to $f\, I\, V \cos\theta_x / |y - x|^2$.
- **Participating media.** In [volumetric path tracing](/volumetric-path-tracing/), a light sample at a scattering point in a medium uses the phase function in place of $f \cos\theta_x$ and the transmittance in place of $V$.

## Pitfalls

- **Double counting.** If line L3 also adds the emission of later vertices, every light path is counted twice, once by the light sample and once by the hit. Count it only on the camera ray, or weight both with MIS.
- **No emission on the camera ray.** Skipping line L3 makes the lights black in the image.
- **The density in the wrong measure.** $p_A$ is per unit area. Dividing by a solid angle density without the factor $\cos\theta_y / |y - x|^2$, or applying it twice, gives a wrong brightness that depends on the distance to the light.
- **Shadow ray limits.** The shadow ray must stop just before $y$ and start just after $x$. A ray that ends at $y$ hits the light itself and reports a blocked path.
- **One-sided lights.** A light point that faces away from $x$, with $\cos\theta_y \le 0$, emits nothing toward $x$. Test the sign of both cosines.
- **Specular surfaces.** At an ideal mirror or glass, the light sample adds $0$, so the emission that line L10 hits must be counted there, with weight 1. A renderer that drops it loses the reflections of lights in mirrors.
- **Lights of zero density.** A light that the sampler never picks is missing from the direct light, and it is not counted on later hits either.

## Exercises

1. Prove that the light sample of line L7 is unbiased for the direct light, by the change of variables $d\omega = \cos\theta_y\, dA / |y - x|^2$.
2. Inside a sphere of radius $R$ with uniform area sampling on a zone of area $A$, show that $G / p_A = A / (4 R^2)$ for every pair of points, so that the light sample has zero variance.
3. Show that with the light sampler of the template, the estimate of line L7 is $f\, \Phi\, V\, G$, and that for a Lambertian surface it is at most $\rho\, \Phi / (\pi\, d_{\min}^2)$, where $d_{\min}$ is the smallest distance from $x$ to a light.
4. Write the estimator for a light that is a point at $y$ with intensity $I$, and explain why plain path tracing gives $0$ for it.
5. A scene has two equal lights, one in full view of $x$ and one behind a wall. Compare the variance of the light sample when the lights are chosen with probability $\tfrac12$ each and when the visible light is chosen with probability $\tfrac{9}{10}$.

## References
