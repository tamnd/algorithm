---
tag: C7K88C
kind: algorithm
slug: volumetric-path-tracing
name: Volumetric path tracing
area: graphics-and-signals/ray-tracing
level: advanced
summary: Path tracing extended to participating media. Sample free flights with delta tracking, scatter at real collisions, and connect each collision to a light with a transmittance estimate.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {n: the number of paths, k: the mean number of collisions on a path, m: "the mean number of tracking steps for one flight or one shadow ray"}
  time: {total: "O(n k m) expected"}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true, recursive: false, exact: false}
history:
  year: 1984
  people: [James T. Kajiya, Brian P. Von Herzen]
  note: Kajiya and Von Herzen ray traced volume densities with the equation of transfer in 1984. Unbiased Monte Carlo random walks with null collisions became the standard volume renderer in the 2010s.
prereqs: [path-tracing, participating-media, delta-tracking]
see_also: [next-event-estimation, russian-roulette, multiple-importance-sampling, bidirectional-path-tracing, photon-mapping, ray-marching, monte-carlo-integration, rendering-equation]
sources:
  - paper: doi:10.1145/964965.808594
    title: James T. Kajiya and Brian P. Von Herzen, Ray tracing volume densities, SIGGRAPH 1984, Computer Graphics 18(3), 165 to 174
    locator: the scattering equation for volume densities in graphics and its approximate solution
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 15, Section 15.1 The Equation of Transfer, Section 15.2 Sampling Volume Scattering and Section 15.3 Volumetric Light Transport
  - url: https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, fourth edition, MIT Press, 2023
    locator: Chapter 14, Section 14.1 The Equation of Transfer and Section 14.2 Volume Scattering Integrators
  - paper: doi:10.1111/cgf.13383
    title: Jan Novák, Iliyan Georgiev, Johannes Hanika and Wojciech Jarosz, Monte Carlo methods for volumetric light transport simulation, Computer Graphics Forum 37(2), 2018, 551 to 576
    locator: the volume rendering equation in integral form, free-flight sampling, transmittance estimation and the construction of volumetric paths
  - title: Subrahmanyan Chandrasekhar, Radiative Transfer, Oxford University Press, 1950 (Dover reprint 1960)
    locator: the H-functions and the exact law of diffuse reflection from a semi-infinite plane-parallel atmosphere with isotropic scattering
---

Volumetric path tracing is [path tracing](/path-tracing/) for scenes with [participating media](/participating-media/) such as smoke, clouds, skin or murky water. A path from the camera goes through the medium in straight flights. The length of each flight is sampled with [delta tracking](/delta-tracking/), so that the path stops at a real collision with the correct probability. At each collision the path connects to a light, with an estimate of the transmittance along the connection, and then it scatters in a new direction sampled from the phase function. The method is an unbiased Monte Carlo estimator of the radiative transfer equation. Its error falls as $N^{-1/2}$ in the number of paths $N$.

## In plain words

A path tracer follows one path of light backward from the camera. In empty space the path goes straight until it hits a surface. In smoke the path can also stop in the air, where a particle of smoke sends the light in a new direction.

So at each step the tracer asks two questions. First, where does the path hit a particle? Delta tracking picks this point with the correct chance, also in smoke whose thickness changes. Second, how much light from the lamp comes to this point? The tracer sends a test ray to the lamp and estimates how much of the lamp light the smoke lets through. It adds this light, multiplied by the share that the particle sends toward the camera. Then the path goes on in a random new direction. The average of many paths is the pixel.

## The problem

The medium has an absorption coefficient $\sigma_a(x)$, a scattering coefficient $\sigma_s(x)$, the extinction $\sigma_t = \sigma_a + \sigma_s$, the single-scattering albedo $\alpha = \sigma_s/\sigma_t$ and a phase function $p(\omega, \omega')$ that integrates to 1 over $\omega'$. Let $L(x, \omega)$ be the radiance that arrives at $x$ from the direction $\omega$, so the light moves in the direction $-\omega$. With no emission in the medium and vacuum at the boundary, the integral form of the [radiative transfer equation](/participating-media/) is

$$L(x, \omega) = \int_0^{s} T(x, x_t)\, \sigma_s(x_t)\, S(x_t, \omega)\, dt + T(x, x_s)\, L_{\text{b}}(x_s, \omega), \qquad x_t = x + t\omega,$$

$$S(y, \omega) = \int_{S^2} p(\omega, \omega')\, L(y, \omega')\, d\omega',$$

where $s$ is the distance to the boundary or to a surface along $\omega$, $T(x, y) = e^{-\int \sigma_t}$ is the transmittance on the segment, and $L_{\text{b}}$ is the radiance that leaves the boundary or surface point $x_s$. The input is the medium, the lights and the camera ray. The output is an estimate of $L$ for the ray. The direct light from a light source is the first part of the in-scattered term $S$, and next event estimation samples it apart from the rest.

## The algorithm

The path starts at the camera point $x$ in the direction $\omega$, with the throughput $\beta = 1$. Let $K$ be a cap on the number of collisions.

```pseudo id=main
VOLUMETRIC-PATH-TRACE(x, ω)
L1  β ← 1, L ← 0
L2  for k ← 1 to K do
L3      t ← DELTA-TRACKING(x, ω)                  ▷ free flight with a majorant
L4      if t = ESCAPE then return L + β · (the surface or boundary term at x_s)
L5      x ← x + t ω                                ▷ a real collision
L6      β ← β · α(x)                               ▷ the weight σs / σt
L7      L ← L + β · (direct light at x from a light sample, times RATIO-TRACKING to the light)
L8      ω ← a direction sampled from p(ω, ·)       ▷ weight p / pdf = 1
L9      Russian roulette: with q = min(1, β), stop with probability 1 − q, else β ← β / q
L10 return L
```

Line L3 samples the distance $t$ with the density $\sigma_t(x_t)\,T(x, x_t)$ on $[0, s)$, and returns ESCAPE with probability $T(x, x_s)$. Line L6 then corrects the weight from $\sigma_t$ to $\sigma_s$, so the path continues only through scattering. For an absorbing medium with $\alpha < 1$, the factor $\alpha$ shrinks the throughput. An equal estimator, called *analog absorption*, ends the path with probability $1 - \alpha$ instead. Line L7 is [next event estimation](/next-event-estimation/). For a point light at $y$ the direct term is $p(\omega, \omega_y)\,I_y\,T(x, y)/\lVert y - x \rVert^2$. For a directional light with irradiance $E$ on a plane normal to the beam it is $p\,E\,T$. In both cases $T$ is replaced by a ratio tracking estimate. Line L9 is [Russian roulette](/russian-roulette/).

## Example

The scene is a plane-parallel slab of depth $Z$, with $\sigma_t(z) = 1 + 0.5 \sin^2(3z)$ for $0 \le z \le Z$, a constant albedo $\alpha = 0.9$ and an isotropic phase function $p = 1/(4\pi)$. A directional light with $E = \pi$ shines down with direction cosine $\mu_0 = 0.6$. The camera looks down with cosine $\mu = 0.8$ and sees the radiance that leaves the top. The bottom is black. The majorant is $1.5$.

**Single scattering.** For a constant albedo the single-scattered radiance depends only on the total optical depth $\tau^*$, also when $\sigma_t$ varies with depth:

$$L_1 = \frac{\alpha E}{4\pi} \cdot \frac{\mu_0}{\mu_0 + \mu}\left(1 - e^{-\tau^*(1/\mu_0 + 1/\mu)}\right).$$

With $Z = 2$, $\tau^* = 2.52236$ and $L_1 = 0.0963670$. The algorithm with $K = 1$ gives, with seed 1:

| paths $N$ | estimate | standard error |
|---|---|---|
| 100 | 0.0831 | 0.0100 |
| 1000 | 0.0903 | 0.0032 |
| 10000 | 0.09617 | 0.00101 |
| 100000 | 0.09628 | 0.00032 |

**All orders of scattering.** For a semi-infinite medium Chandrasekhar's H-function gives the exact answer

$$L = \frac{\alpha E}{4\pi} \cdot \frac{\mu_0}{\mu_0 + \mu}\, H(\mu)\, H(\mu_0), \qquad \frac{1}{H(\mu)} = \sqrt{1 - \alpha} + \frac{\alpha}{2}\int_0^1 \frac{\mu' H(\mu')}{\mu + \mu'}\, d\mu'.$$

For $\alpha = 0.9$, $H(0.6) = 1.62588$ and $H(0.8) = 1.74740$, so $L = 0.273960$. Single scattering, $L_1 = 0.096429$ for a semi-infinite medium, is only $0.352$ of this. A slab with $Z = 20$ has $\tau^* = 24.98$ and acts as semi-infinite. The full algorithm gives, with seed 2:

| paths $N$ | estimate | standard error |
|---|---|---|
| 100 | 0.268 | 0.028 |
| 1000 | 0.2810 | 0.0084 |
| 10000 | 0.2729 | 0.0027 |
| 100000 | 0.27351 | 0.00083 |

A cap of $K$ collisions gives, with 40000 paths, 0.0956 for $K = 1$, 0.1495 for $K = 2$, 0.1833 for $K = 3$, 0.2211 for $K = 5$ and 0.2586 for $K = 10$. A cap on the path length is a bias that cuts the higher orders of scattering.

## Correctness

Write the solution as a Neumann series $L = \sum_{j \ge 1} L_j$, where $L_j$ is the light that has scattered exactly $j$ times. By [delta tracking](/delta-tracking/), line L3 has the density $\sigma_t T$, so after the factor $\alpha$ of line L6 the expected weight at a collision is $\sigma_s T\,dt$, the kernel of the integral equation. Ratio tracking in line L7 is an unbiased estimate of the transmittance to the light and is independent of the rest of the path given $x$. Sampling the direction from $p$ gives the weight 1. Russian roulette keeps each expectation. By induction on $j$, the expected contribution of line L7 at the $j$-th collision is $L_j$, and the sum is $L$. All terms are nonnegative, so the expectations add. The proof is in the proof file.

Without a cap, the estimator is unbiased. With a cap $K$ it estimates $\sum_{j \le K} L_j$. With $\alpha \le 1$ the throughput stays at most 1, and after Russian roulette it is exactly 1, so each contribution is bounded and the variance is finite.

## Complexity

One path makes $k$ collisions on average. For an albedo $\alpha < 1$ in an infinite medium, the number of collisions is geometric with mean $1/(1 - \alpha)$. Each flight and each shadow ray costs $O(1 + \mu \ell)$ expected steps of tracking, where $\mu$ is the majorant and $\ell$ is the length of the segment, and the shadow ray costs $\mu \ell$ steps on average with ratio tracking. So $N$ paths take $O(N k m)$ expected time and $O(1)$ extra space per path. The standard error of the pixel is $\sqrt{v/N}$, with $v$ the variance of one path, so it is $O(N^{-1/2})$. In the tables a factor of 100 in $N$ divides the error by about 10.

## Properties

- **Unbiased.** Without a cap on the path length, the expected value is the exact radiance of the radiative transfer equation.
- **No step size.** Unlike ray marching, null-collision tracking needs only point values of $\sigma_t$ and has no discretization error.
- **Local.** Each path needs only point queries of the medium and of the lights. Paths are independent, so the method is easy to run in parallel.
- **Slow in dense, bright media.** In a medium with a high albedo and a large optical depth, paths make many collisions before they leave, and the work per path grows as $1/(1 - \alpha)$.

## Variants and improvements

- **Analog absorption.** End the path with probability $1 - \alpha$ at each collision instead of multiplying by $\alpha$. It is also unbiased.
- **Multiple importance sampling of the light.** Sample both the light and the phase function at each collision and combine them with [multiple importance sampling](/multiple-importance-sampling/). This helps for large lights and peaked phase functions.
- **Equiangular sampling.** For a point light inside a medium, sample the distance along the ray in proportion to the inverse squared distance to the light. Kulla and Fajardo described it in 2012.
- **Spectral tracking.** Use one majorant for all wavelengths and weights for the wavelengths that were not used to sample.
- **Bidirectional methods.** [Bidirectional path tracing](/bidirectional-path-tracing/) and [photon mapping](/photon-mapping/) with volume photons, or photon beams, handle caustics in media that unidirectional paths find slowly.
- **Diffusion and similarity theory.** For dense media with a high albedo, a diffusion approximation or a BSSRDF can replace many collisions, with a bias.

## When to use it

Use volumetric path tracing as the reference renderer for heterogeneous media, clouds, smoke and subsurface scattering, when an unbiased result is necessary. It works best for media of low or medium optical depth and for lights that are easy to reach with next event estimation. For media lit only through specular surfaces, or for very dense media, use a bidirectional or a photon method, or an approximation.

## Pitfalls

- **A majorant that is too small.** Delta tracking is then biased toward too little extinction. Compute the majorant from the data of each cell.
- **The albedo weight on the wrong event.** If the free flight is sampled with $\sigma_t$, the scattering weight is $\sigma_s/\sigma_t$. If the code samples with $\sigma_s$ and also multiplies by $\sigma_s/\sigma_t$, it counts the absorption two times.
- **A binary shadow transmittance.** A shadow ray with delta tracking gives 0 or 1. Ratio tracking has a lower variance at the same cost.
- **A hard cap on the path length.** A cap cuts the high orders of scattering. In the example the cap $K = 10$ still loses 6 percent of the light. Use Russian roulette.
- **The phase function convention.** Some codes write $p(\omega, \omega')$ with $\omega$ pointing toward the viewer and some with it pointing along the light. For the Henyey-Greenstein function, a sign error turns forward scattering into backward scattering.
- **Index-matched boundaries.** If the medium is inside a surface with no refraction, the path must cross the boundary without a surface event. Otherwise the boundary acts as a surface that reflects.

## Implementations

## History

Chandrasekhar wrote the theory of radiative transfer for stellar atmospheres in 1950, with exact results for plane-parallel media such as the H-function. Kajiya and Von Herzen brought the equation of transfer into computer graphics in 1984 for clouds and other volume densities. Kajiya's path tracing of 1986 and the Monte Carlo methods of neutron transport, including Woodcock tracking of 1965, gave the parts of the modern method. Production renderers moved to unbiased volumetric path tracing with null-collision tracking in the 2010s. The survey of Novák, Georgiev, Hanika and Jarosz of 2018 describes this family of methods.

## References
