---
tag: Z5NHPG
kind: algorithm
slug: distributed-ray-tracing
name: Distributed ray tracing
aliases:
- stochastic ray tracing
- Cook ray tracing
- distribution ray tracing
area: graphics-and-signals/ray-tracing
level: advanced
summary: Whitted ray tracing with each ray replaced by jittered samples over the pixel, the lens, the shutter time, the light area and the gloss lobe, so that one average renders blur, soft shadows and gloss.
model: real-ram
complexity:
  vars: {P: the number of pixels, N: the number of samples per pixel, n: the number of objects, m: the number of lights, D: the maximum depth of the ray tree}
  time: {worst: Θ(2^D P N n (m + 1))}
  space: {extra: O(N + D)}
properties: {deterministic: false, randomized: true, recursive: false}
history:
  year: 1984
  people: [Robert L. Cook, Thomas Porter, Loren Carpenter]
  note: Cook, Porter and Carpenter, at Lucasfilm, spread the rays of a ray tracer over time, the lens, the lights and the reflection directions, and rendered motion blur, depth of field, penumbrae, gloss and translucency with one method.
prereqs: [whitted-ray-tracing, monte-carlo-integration, stratified-sampling]
see_also: [depth-of-field, thin-lens-camera, path-tracing, antialiasing, latin-hypercube-sampling, next-event-estimation, cone-tracing, quasi-monte-carlo-integration]
sources:
  - paper: doi:10.1145/800031.808590
    title: Robert L. Cook, Thomas Porter and Loren Carpenter, Distributed ray tracing, Computer Graphics (SIGGRAPH 84 Proceedings) 18(3), 1984, 137 to 145
    locator: the distribution of rays over the reflection directions, the lights, the lens and time, and the gloss, penumbra, depth of field and motion blur that they give
  - paper: doi:10.1145/7529.8927
    title: Robert L. Cook, Stochastic sampling in computer graphics, ACM Transactions on Graphics 5(1), 1986, 51 to 72
    locator: Section 4 on jittering and Section 5 on distributed ray tracing (nonspatial jittering with prototype patterns, weighted distributions, and the summary of the algorithm)
  - paper: doi:10.1145/15886.15902
    title: James T. Kajiya, The rendering equation, Computer Graphics (SIGGRAPH 86) 20(4), 1986, 143 to 150
    locator: distributed ray tracing as a Monte Carlo solution of the rendering equation, and the waste of branching that path tracing removes
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 7.3, Stratified Sampling, and the sections on the thin lens camera and on sampling light sources
---

Distributed ray tracing renders the effects that a single ray cannot: blurred reflections, soft shadows, depth of field and motion blur. Each of them is an integral: a glossy surface averages the light over a lobe of reflection directions, a point in a penumbra sees part of an area light, a lens averages over its aperture, and a shutter averages over time. Cook, Porter and Carpenter (1984) kept the ray tree of [Whitted ray tracing](/whitted-ray-tracing/) but replaced each fixed ray by one random sample of its integral: the reflected ray goes in a random direction of the lobe, the shadow ray to a random point of the light, the primary ray from a random point of the lens at a random time. With several rays per pixel, the average is a [Monte Carlo](/monte-carlo-integration/) estimate of all the integrals at once, and [stratified](/stratified-sampling/) jitter in each dimension keeps the noise low. The cost of an effect is then only the samples, not a special algorithm.

## In plain words

A plain ray tracer sends one ray per pixel and one ray for each mirror or shadow. That gives perfect mirrors, razor sharp shadows, and a camera that sees everything sharp and frozen in time.

Real things are fuzzy. A lamp has a size, so a shadow has a soft edge. Brushed metal blurs what it reflects. A camera lens blurs what is out of focus, and a fast ball smears during the exposure.

Each fuzzy effect is an average: over the points of the lamp, the directions near the mirror direction, the points of the lens, or the moments the shutter is open. Distributed ray tracing sends many rays per pixel and gives each one a different random point of the lamp, a different direction, a different point of the lens and a different moment. The average of the rays is the fuzzy picture.

## The problem

The scene is as in Whitted ray tracing, with four additions: lights that are disks of radius $R_\ell$ and radiance $L_\ell$; a Phong lobe exponent for the reflection of a glossy material and for the transmission of a translucent one; spheres that move with a constant velocity during the shutter interval $[0, 1)$; and a thin-lens camera with the lens radius $a$ and the focus distance $s$. The value of pixel $(i, j)$ is the average over the pixel square $Q$, the lens disk $U$ and the shutter interval,

$$\bar V_{ij} = \frac{1}{|U|} \int_Q \int_U \int_0^1 V_D\big(\mathrm{ray}(x, u), t\big)\,dt\,du\,dx,$$

where the ray from the lens point $u$ passes through the point in focus of the film point $x$, as for the [thin-lens camera](/thin-lens-camera/), and the value of a ray with $k$ levels left, at the time $t$, with the hit $p$ and the normal $n$, is

$$V_k = k_a + k_d \sum_{\text{point } \ell} E_\ell \cos\theta_\ell + \frac{k_d}{\pi} \sum_{\text{disk } \ell} \int_{A_\ell} L_\ell\,\frac{\cos\theta \cos\theta_\ell}{|q - p|^2}\,\mathrm{vis}(p, q)\,dq + [k > 0] \Big( k_s \int g_s(\omega)\,V_{k-1}(\omega)\,d\omega + k_t \int g_t(\omega)\,V_{k-1}(\omega)\,d\omega \Big).$$

Here $g_s$ is the normalized lobe $\frac{e + 1}{2\pi}\cos^e\alpha$ around the mirror direction, restricted to the directions above the surface, and $g_t$ is the lobe around the refracted direction, restricted to the directions below it. The disk term is $k_d/\pi$, the [Lambertian](/lambertian-reflectance/) BRDF, times the irradiance from the visible part of the light. With all lobes sharp, a pinhole and no motion, $V_k$ is the Whitted value.

## The algorithm

```pseudo id=main
DISTRIBUTED(scene, camera, q, D, rng)
L1  for each pixel (i, j) of the image
L2      draw q × q jittered points for the film, the lens, the light and the lobe, and q² jittered times; shuffle each set on its own
L3      sum ← 0
L4      for s = 1 to q²
L5          (o, d) ← the ray from lens point u_s through the point in focus of film point (i, j) + x_s
L6          sum ← sum + TRACE((o, d), t_s, D, light point and lobe point s)
L7      image[i, j] ← sum / q²

TRACE((o, d), t, D, ξ)
L8  I ← 0;  S ← a stack holding (o, d, 1, 0)                ▷ ray, weight, depth
L9  while S is not empty
L10     pop (o, d, w, k);  find the closest hit with the objects at their places at time t
L11     if there is none then I ← I + w · background;  continue
L12     p, n and η as in Whitted ray tracing;  I ← I + w · ka
L13     for each point light ℓ visible from p: I ← I + w · kd · E_ℓ · cos θ_ℓ
L14     for each disk light ℓ: pick q on ℓ uniformly (from ξ at depth 0); if p sees q then I ← I + w · kd · L_ℓ · A_ℓ · cos θ · cos θ_ℓ / (π |q − p|²)
L15     if k = D then continue
L16     if ks > 0: draw ω from the gloss lobe around the mirror direction (from ξ at depth 0); if n · ω > 0 then push (p, ω, w · ks, k + 1)
L17     if kt > 0 and the refracted direction r exists: draw ω from the lobe around r; if n · ω < 0 then push (p, ω, w · kt, k + 1)
L18 return I
```

Line L2 is Cook's nonspatial jittering. Each two-dimensional choice of the first hit gets its own jittered $q \times q$ grid of the unit square, one uniform point per cell, and the shutter interval is cut into $q^2$ slices with one uniform time each. Each set is shuffled on its own, so that sample $s$ pairs a random cell of each dimension with random cells of the others; Cook did this with random prototype patterns. In each dimension the samples are stratified, and between dimensions they are uncorrelated, as in [Latin hypercube sampling](/latin-hypercube-sampling/).

Line L5 maps the lens point to the disk by $r = a\sqrt{u_1}$, $\phi = 2\pi u_2$, and aims the ray at the point where the pinhole ray of the film point meets the plane of focus. The [depth of field](/depth-of-field/) follows: points on that plane are sharp, and others blur over their circle of confusion. Line L10 places each moving object at its position at the time $t$ of the primary ray, and all rays of the tree, the shadow rays too, use that time.

Line L14 is a shadow ray to a uniform point of the light, the [next-event estimation](/next-event-estimation/) of a path tracer: with the density $1/A_\ell$, the term $L_\ell A_\ell \cos\theta \cos\theta_\ell / |q - p|^2$ is an unbiased estimate of the integral over the light. Line L16 samples the Phong lobe exactly, by $\cos\alpha = u_1^{1/(e + 1)}$ and $\phi = 2\pi u_2$; this is [importance sampling](/importance-sampling/) of the lobe, so the weight is just $k_s$. A direction below the surface is dropped, which is the restriction of $g_s$. Line L17 does the same for translucency. Deeper hits draw fresh uniform numbers.

## Example

**One point of a penumbra.** A diffuse floor $y = 0$ with $k_d = 1$, a disk light of radius 0.8 and radiance 1 at the height 2, facing down, and a sphere of radius 0.3 at $(0.3, 1, 0)$ that blocks part of it. At the floor point $p = (0, 0, 0)$, the whole light would give $R^2/(h^2 + R^2) = 0.64/4.64 = 0.1379$, and a fine quadrature over the visible part gives $0.0884$, 64 percent of it. With $q = 2$ the four stratified light samples are

| sample | point of the unit square | point $q$ on the light | blocked | value |
|---|---|---|---|---|
| 1 | (0.835, 0.654) | (−0.602, 2, 0.414) | no | 0.1245 |
| 2 | (0.478, 0.474) | (0.090, 2, 0.546) | no | 0.1381 |
| 3 | (0.918, 0.368) | (0.565, 2, 0.518) | yes | 0 |
| 4 | (0.028, 0.542) | (−0.035, 2, 0.130) | no | 0.1586 |

Each value is $0.64 \cos\theta \cos\theta_\ell / |q - p|^2$; for sample 4, $|q - p|^2 = 4.018$ and both cosines are $0.998$. The mean is $0.1053$, against the exact $0.0884$.

**Stratified against independent samples.** The root mean square error of the pixel at $p$, relative to $0.0884$, over 400 pixels with each number of samples:

| samples $N$ | 1 | 4 | 16 | 64 | 256 |
|---|---|---|---|---|---|
| independent | 0.758 | 0.402 | 0.185 | 0.093 | 0.045 |
| stratified, $q \times q$ | 0.750 | 0.243 | 0.119 | 0.042 | 0.015 |

The independent error falls as $N^{-1/2}$. The stratified one falls about as $N^{-3/4}$, the rate of jittered sampling for an integrand with a discontinuity along a curve: only the cells that the edge of the shadow crosses add variance, and there are about $q$ of them among $q^2$. At 256 samples, stratification gives the accuracy of about 2500 independent samples.

**Motion blur.** A sphere of radius 0.2 moves along $x$ with the speed 1 per shutter interval, from $x = -0.5$, across the line of sight of a pixel. Its center is at $x(t) = -0.5 + t$, and it covers the pixel while $|x(t)| < 0.2$, that is for $t \in (0.3, 0.7)$, so the pixel value is $0.4$ of the sphere's brightness. With $q^2$ jittered times every slice inside the interval counts exactly and at most two slices are cut by its ends, so the estimate is within $2/q^2$ of $0.4$ for every choice of the jitter.

## Correctness

Each sample of line L6 is an unbiased estimate of $\bar V_{ij}$, so their mean, stored at line L7, is too. The proof, in [the correctness proof](proofs/correctness.md), has two parts. First, the stack walk returns the same sum as the recursive estimator that adds the local estimate of a node and the weighted estimates of its children, by the linearity argument of Whitted ray tracing. Second, by induction on the depth from the leaves up, the conditional expectation of the estimate of a node, given its ray and the time, is $V_k$: the disk sample is uniform with the density $1/A_\ell$, the lobe samples have the densities $g_s$ and $g_t$, and the children draw their numbers independently. At the top, each of the film, lens and time samples of sample $s$ is uniform on its domain, because a uniformly random member of a jittered set is uniform, and the sets are independent of each other because each is drawn and shuffled on its own.

## Complexity

Each primary ray has a tree of at most $2^{D+1} - 1$ rays, as in Whitted ray tracing, since each hit spawns at most one reflected and one transmitted ray. Each ray costs a closest-hit query and $m$ shadow queries of $\Theta(n)$ each by a scan, so a pixel with $N = q^2$ samples costs $O(2^D N n (m + 1))$ and the image $\Theta(2^D P N n (m + 1))$ in the worst case. That is $N$ times the cost of Whitted ray tracing, for any number of effects at once: the same $N$ rays sample the pixel, the lens, the time, the lights and the lobes. Cook found that 16 samples per pixel were enough in most scenes, and more were needed only for extreme blur. The patterns of line L2 take $O(N)$ space, and the stack $O(D)$.

The error is random. For a smooth integrand, independent samples give the standard deviation $\sigma/\sqrt N$, and jittered ones less; a discontinuity of the integrand along a curve, such as the edge of a shadow or of an object, gives $O(N^{-3/4})$ with jitter in two dimensions.

## Properties

- **Randomized and unbiased.** Every pixel value is an unbiased estimate of the pixel integral, and the error shows as noise, not as aliasing. Cook's point was that noise of the right average is much less visible than the regular patterns of aliasing.
- **Antialiasing for free.** The jittered film points of line L2 sample the pixel area, which is the stochastic form of [supersampling](/supersampling-antialiasing/) and replaces aliasing by noise, as the theory of [aliasing](/aliasing/) predicts for nonuniform samples.
- **All effects share the samples.** Depth of field, motion blur, soft shadows and gloss all cost the same $N$ rays per pixel, not $N$ each, because each sample draws one value in every dimension.
- **Still a Whitted tree.** Diffuse interreflection is not sampled: only the light that reaches a diffuse surface straight from a light is counted. Each ray still branches into a reflected and a transmitted ray, so deep levels get many rays of small weight.

## Variants and improvements

- **Path tracing.** Kajiya (1986) showed that distributed ray tracing is a Monte Carlo solution of the [rendering equation](/rendering-equation/) that leaves out indirect diffuse light, and that the branching wastes work on deep, faint rays. [Path tracing](/path-tracing/) follows one random branch at each hit, samples diffuse reflection as well, and stops paths by [Russian roulette](/russian-roulette/).
- **Better sample patterns.** Poisson disk patterns, which Cook approximated by jitter, and low-discrepancy points in [quasi-Monte Carlo](/quasi-monte-carlo-integration/) sampling, such as the [Halton sequence](/halton-sequence/), lower the error further.
- **Adaptive sampling.** Add samples to a pixel while the variance of its samples is high, as Lee, Redner and Uselton (1985) proposed for distributed ray tracing. The estimate then has a small bias, because the number of samples depends on the samples.
- **Multiple importance sampling.** A glossy surface under a large light can be sampled through the lobe or through the light; [multiple importance sampling](/multiple-importance-sampling/) combines both with low variance in either case.
- **Deterministic alternatives.** [Cone tracing](/cone-tracing/) (Amanatides, 1984) and [beam tracing](/beam-tracing/) replace the many rays by one volume per pixel, which gives blur without noise but needs special intersection tests. The accumulation buffer of Haeberli and Akeley (1990) renders whole images for a few lens points, times or light points and averages them.

## When to use it

Use distributed ray tracing when a Whitted renderer needs depth of field, motion blur, soft shadows or glossy reflection, and indirect diffuse light does not matter. It needs no change to the scene or the intersection code, only sampled rays and an average. For full global illumination, use path tracing, which contains it. For a fixed time budget on the GPU, a rasterizer with postprocess blur, soft shadow maps and prefiltered reflections is faster but only approximate.

## Pitfalls

- **Correlated dimensions.** Using one order for all the sets at line L2, so that the sample in the first film cell also gets the first time slice, ties time to position: Cook's example is an object that moves from right to left and is missed by every sample of a pixel, while one moving the other way is hit by all. Shuffle each set on its own, as line L2 does.
- **The lens ray.** Starting the ray at line L5 from the lens point but in the direction of the pinhole ray shifts the image instead of blurring it, and nothing is in focus. Aim the ray from the lens point through the point in focus, as line L5 does.
- **One time per tree.** Drawing a new time for each shadow or reflected ray at lines L10 to L17 detaches the shadow and the reflection of a moving object from the object. Use the time of the primary ray for the whole tree, as line L10 does.
- **The weight of an area light.** Writing $L_\ell \cos\theta$ at line L14, without the area $A_\ell$ and the factor $\cos\theta_\ell / |q - p|^2$ of the change from solid angle to area, makes large lights too dark and near ones too bright. Use the full weight of line L14.
- **Directions below the surface.** Following a lobe direction with $n \cdot \omega \le 0$ at line L16 sends the ray into the object and lets light leak through it. Drop the sample, as line L16 does, or sample a lobe that is clipped to the hemisphere.
- **Reusing a pattern at depth.** Using the stratified point of sample $s$ again at a deeper hit at line L14 or L16 correlates the choices along one path, which biases the result. Use the patterns at the first hit only, and fresh numbers below it, as lines L14 and L16 do.

## Implementations

## History

Before 1984, ray-traced images had sharp shadows, perfect mirrors, pinhole cameras and an instant shutter. Potmesil and Chakravarty (1981) and Amanatides (1984) addressed some of the blur by other means. Robert Cook, Thomas Porter and Loren Carpenter, at Lucasfilm, presented distributed ray tracing at SIGGRAPH 1984, with the image "1984" by Porter of motion-blurred pool balls. Cook (1986) explained the method through the theory of stochastic sampling, and Dippé and Wold (1985) studied stochastic sampling at the same time. Kajiya (1986) put it in the frame of the rendering equation and replaced it by path tracing. Cook later suggested the name distribution ray tracing, since the rays sample distributions and the method is not a parallel algorithm.

## References
