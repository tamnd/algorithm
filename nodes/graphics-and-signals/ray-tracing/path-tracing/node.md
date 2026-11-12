---
tag: PCC896
kind: algorithm
slug: path-tracing
name: Path tracing
aliases:
- Monte Carlo ray tracing
- Kajiya path tracing
area: graphics-and-signals/ray-tracing
level: core
summary: Estimate each pixel by random light paths traced back from the camera, one sampled bounce at a time, with Russian roulette to stop. The mean is unbiased for the rendering equation.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {N: the number of samples per pixel, P: the number of pixels, k: the mean number of vertices of a path, c: the cost of one closest-hit query}
  time: {expected: Θ(N P k c)}
  space: {extra: Θ(P)}
properties: {deterministic: false, recursive: false, online: true, in_place: false}
history:
  year: 1986
  people: [James T. Kajiya]
  note: Kajiya introduced the rendering equation and path tracing, a Monte Carlo solution that follows one random ray at each bounce, in his SIGGRAPH 86 paper.
prereqs: [rendering-equation, monte-carlo-integration, importance-sampling]
see_also: [russian-roulette, next-event-estimation, multiple-importance-sampling, bidirectional-path-tracing, metropolis-light-transport, distributed-ray-tracing, photon-mapping, volumetric-path-tracing]
sources:
  - paper: doi:10.1145/15886.15902
    title: James T. Kajiya, The rendering equation, Computer Graphics (SIGGRAPH 86) 20(4), 1986, 143 to 150
    locator: the rendering equation in two-point form, its Neumann series, and the Monte Carlo solution that traces one ray per bounce
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 13.7 Russian Roulette and Splitting, Section 14.4 The Light Transport Equation, Section 14.5 Path Tracing
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 2 (Monte Carlo integration and Russian roulette), Chapter 3 (the light transport equation) and Chapter 8 (the path integral form)
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, A K Peters, 2006
    locator: Chapter 5, Stochastic Path-Tracing Algorithms
  - paper: doi:10.1145/97879.97886
    title: James Arvo and David Kirk, Particle transport and image synthesis, Computer Graphics (SIGGRAPH 90) 24(4), 1990, 63 to 66
    locator: Russian roulette and splitting taken from particle transport into image synthesis
---

Path tracing computes an image by [Monte Carlo integration](/monte-carlo-integration/) of the [rendering equation](/rendering-equation/). For each pixel it shoots random rays from the camera, and at each surface hit it adds the emitted light, picks one new direction at random, and goes on, until [Russian roulette](/russian-roulette/) stops the path. The mean of many such paths is an unbiased estimate of the pixel, so the error falls as $1/\sqrt{N}$ in the number $N$ of paths and no part of the light transport is left out. Kajiya introduced it in 1986, and it is the base of most methods for [global illumination](/global-illumination/).

## In plain words

Light leaves a lamp, hits a wall, then a floor, then enters the camera. Path tracing follows such a chain in the other direction. It starts at the camera and goes into the scene. At each surface it asks two things: does this surface give off light, and where did the light that it reflects come from? It cannot follow every direction, so it picks one at random and follows only that. The light found along the chain, weighted by how much each surface reflects, is one guess for the pixel.

One guess is noisy. The average of many guesses is correct on average, and it gets closer to the true value as the number of guesses grows. To stop a chain, the method flips a biased coin at each surface. When a chain survives the coin, it counts for more, so that the average stays correct.

## The problem

A scene has surfaces with an emitted radiance $L_e(x, \omega)$ and a [BRDF](/brdf/) $f(x, \omega_i, \omega_o)$. The outgoing radiance solves the rendering equation

$$L(x, \omega_o) = L_e(x, \omega_o) + \int_{H^2(x)} f(x, \omega_i, \omega_o)\, L(h(x, \omega_i), -\omega_i) \cos\theta_i \, d\omega_i,$$

where $h(x, \omega)$ is the first surface point that the ray from $x$ in the direction $\omega$ hits, and $\theta_i$ is the angle between $\omega_i$ and the normal at $x$. A ray that hits nothing brings no light. A pinhole camera at $c$ gives pixel $j$ the value

$$I_j = \int W_j(\omega)\, L(h(c, \omega), -\omega)\, d\omega,$$

with a weight $W_j$ that is not negative. The page uses the hemisphere form of the equation and a pinhole camera; the [path integral formulation](/path-integral-formulation/) gives the same pixel as one integral over paths. The output is an estimate $\hat I_j$ with $E[\hat I_j] = I_j$, and its standard error.

## The algorithm

PATH-TRACE returns one estimate of the radiance that arrives at $o$ from the direction $d$. The throughput $\beta$ is the weight that turns the emission at the current vertex into a contribution to the estimate.

```pseudo id=main
PATH-TRACE(o, d)
L1  L ← 0;  β ← 1;  k ← 0
L2  loop
L3      x ← CLOSEST-HIT(o, d);  if there is no hit then return L
L4      L ← L + β · Le(x, −d)
L5      sample a direction ω at x with the density p(ω)
L6      β ← β · f(x, ω, −d) · cos θ / p(ω)
L7      q ← a survival probability in [0, 1]          ▷ for example min(1, albedo at x)
L8      draw u uniform in [0, 1);  if u ≥ q then return L
L9      β ← β / q
L10     o ← x;  d ← ω;  k ← k + 1

RENDER(c, N)
L11 for each pixel j: repeat N times: sample ω with the density pj(ω); add Wj(ω) · PATH-TRACE(c, ω) / pj(ω) to Sj
L12 for each pixel j: Ij ← Sj / N, and its standard error from the sample variance
```

Line L3 is a [closest-hit query](/closest-hit-query/). Line L5 is [importance sampling](/importance-sampling/) of the integral of the equation: for a Lambertian surface with albedo $\rho$, $f = \rho / \pi$, and cosine sampling $p(\omega) = \cos\theta / \pi$ makes the factor of line L6 equal to $\rho$. Lines L7 to L9 are Russian roulette. The division of line L9 is what keeps the mean exact; without it the method is biased dark. A survival probability that follows $\beta$ or the albedo keeps the weights near 1 and stops paths that would add little.

## Example

The scene is the inside of a unit sphere with the camera at its center. The lower half ($z < 0$) has albedo $\tfrac34$ and no emission. The upper half has albedo $\tfrac14$ and emits radiance $2$. Pixel 0 holds the directions with $z < 0$ and pixel 1 those with $z \ge 0$, each with $W_j = 1 / (2\pi)$ and $p_j$ uniform, so each pixel is the radiance of the half it sees.

This scene has an exact answer. Inside a sphere of radius $R$, two wall points $x, y$ have $\cos\theta_x \cos\theta_y / |x - y|^2 = 1 / (4 R^2)$, so a cosine sampled ray from any wall point lands uniformly by area on the wall: each half with probability $\tfrac12$. The incident radiance $C$ is then the same everywhere, with $C = \tfrac12 (\tfrac34 C) + \tfrac12 (2 + \tfrac14 C)$, so $C = 2$. The pixels are $L_0 = \tfrac34 \cdot 2 = \tfrac32$ and $L_1 = 2 + \tfrac14 \cdot 2 = \tfrac52$. The [Neumann series](/neumann-series/) of the equation sums the light by the number of bounces:

| bounces at most | 0 | 1 | 2 | 3 | all |
|---|---|---|---|---|---|
| $L_0$ | $0$ | $\tfrac34$ | $\tfrac98$ | $\tfrac{21}{16}$ | $\tfrac32$ |
| $L_1$ | $2$ | $\tfrac94$ | $\tfrac{19}{8}$ | $\tfrac{39}{16}$ | $\tfrac52$ |

Each added bounce halves the remaining error, a [geometric series](/geometric-series/) with ratio $\tfrac12$.

One path for pixel 0, with cosine sampling and $q = $ albedo, so that $\beta$ stays at $1$:

| vertex $k$ | hit point $z$ | $L_e$ | $L$ after L4 | $q$ | $u$ | result of L8 |
|---|---|---|---|---|---|---|
| 0 | $-0.676$ | $0$ | $0$ | $0.75$ | $0.536$ | go on |
| 1 | $0.415$ | $2$ | $2$ | $0.25$ | $0.507$ | stop |

The estimate of this path is $2$. Each estimate is twice the number of upper vertices on its path, a whole number, and only the mean is near $\tfrac32$. The mean over $N$ paths per pixel (seed 1):

| $N$ | pixel 0 | pixel 1 |
|---|---|---|
| 100 | $1.4400 \pm 0.1533$ | $2.5800 \pm 0.1112$ |
| 1000 | $1.5080 \pm 0.0480$ | $2.5760 \pm 0.0407$ |
| 10000 | $1.4992 \pm 0.0151$ | $2.4962 \pm 0.0113$ |

Each value after $\pm$ is one standard error. All six means are within 2 standard errors of $\tfrac32$ and $\tfrac52$, and the standard error falls by about $\sqrt{10}$ for each factor of 10 in $N$.

## Correctness

PATH-TRACE is an unbiased estimator of $L(o', -d)$ at the first hit $o'$, under three conditions: $p(\omega) > 0$ wherever $f \cos\theta > 0$, $q > 0$ wherever the albedo is positive, and a Neumann series that converges (for example every albedo is at most some $\rho_{\max} < 1$). The contribution added at vertex $k$ has the expected value $(K^k L_e)$, where $K$ is the integral operator of the equation, because each bounce replaces the integral by one sample divided by its density, and each roulette step divides by the probability that it keeps. The sum over $k$ is the Neumann series $\sum_k K^k L_e = L$. All terms are not negative, so the expected value of the sum is the sum of the expected values. RENDER then averages $N$ independent unbiased estimates.

With a depth limit of $B$ bounces in place of roulette, the same argument gives $\sum_{k \le B} K^k L_e$, which is less than $L$: the method is then biased dark, as the table of the example shows. The full proof is in the proofs folder.

## Complexity

Each vertex costs one closest-hit query, of cost $c$, and a constant amount of other work, so one path costs $\Theta(k c)$ on average, where $k$ is the mean number of vertices. With $q = \min(1, \rho)$ and every albedo at most $\rho_{\max} < 1$, the number of vertices is at most a geometric variable, so $k \le 1 / (1 - \rho_{\max})$. The image costs $\Theta(N P k c)$ time, where $P$ is the number of pixels. Memory is $\Theta(P)$ for the image and $O(1)$ for each path, because the loop needs no stack.

The error is statistical. If one estimate has the variance $\sigma^2$, the mean of $N$ has the standard error $\sigma / \sqrt{N}$, so a 10 times smaller error needs 100 times more paths. $\sigma$ depends on the scene: it is small for large lights and diffuse surfaces, and large when light reaches the camera through small lights, narrow openings or caustics. For an ideal mirror that reflects a point light, no random path finds the light, and plain path tracing gives $0$ for that light.

## Properties

- **Unbiased and consistent.** With roulette and no depth limit, the expected value is exact and the mean converges to it with probability 1 by the [law of large numbers](/law-of-large-numbers/).
- **Error estimate.** The sample variance gives a standard error, and the [central limit theorem](/central-limit-theorem/) makes the mean nearly normal for large $N$.
- **Progressive.** More samples can be added at any time to an image, and each pixel is independent, so the method runs in parallel with no shared state other than the scene.
- **General.** It handles any BRDF that can be evaluated and sampled, and with small changes also refraction, volumes and spectra.
- **Noise.** The error shows as noise at the pixel level, often with rare very bright pixels from paths with a low density and a large contribution.

## Variants and improvements

- **[Next event estimation](/next-event-estimation/).** At each vertex, also sample a point on a light and test its visibility. This finds small lights that a random direction rarely hits. Kajiya's own method did this.
- **[Multiple importance sampling](/multiple-importance-sampling/).** Combine the light sample and the BRDF sample with weights that sum to 1, so that both small lights and glossy surfaces are handled well.
- **[Light tracing](/light-tracing/) and [bidirectional path tracing](/bidirectional-path-tracing/).** Start paths at the lights, or at both ends, for scenes where the camera sees only light that went through a hard path.
- **[Metropolis light transport](/metropolis-light-transport/).** Mutate paths that carry much light with a Markov chain.
- **[Path guiding](/path-guiding/).** Learn the incident light during rendering and sample line L5 from it.
- **Better samples.** [Stratified sampling](/stratified-sampling/) and [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/) replace the independent random numbers and lower the error for the same $N$.
- **[Volumetric path tracing](/volumetric-path-tracing/).** Paths also scatter inside [participating media](/participating-media/).
- **Splitting.** Trace several directions at the first bounce, the opposite of roulette, where a path has a high weight.

## When to use it

Use path tracing when the image must include all light transport, without tuning, and a time of many paths per pixel is acceptable, as in offline rendering and as a reference to test faster methods. It is simple, it takes few parameters, and its only error is noise that goes away with more samples. Add next event estimation and MIS in nearly every case. Use bidirectional methods, [photon mapping](/photon-mapping/) or Metropolis light transport when much of the light arrives through caustics or small openings. For real-time rendering with a few samples per pixel, use it with a denoiser or with [ReSTIR](/restir/).

## Pitfalls

- **No division by $q$.** Ending a path at line L8 without the division of line L9 loses the expected light of the paths that stop, and the image is too dark.
- **A depth limit as the only stop.** A fixed maximum depth cuts the tail of the Neumann series, a bias that is large for bright scenes with high albedo, as the example shows.
- **$q = 1$ for albedo 1.** If $q = \min(1, \rho)$ and a closed scene has $\rho = 1$, no path ever stops. Cap $q$ below 1.
- **Self-intersection.** A new ray from $x$ can hit the surface of $x$ at $t \approx 0$ by rounding. Start it with a small $t_{\min}$ or move the origin along the normal.
- **The wrong side of the normal.** The cosine and the hemisphere of line L5 must use the normal on the side of the incoming ray. A flipped normal sends rays into the surface.
- **Double counting.** With next event estimation, the emission at line L4 must be left out for vertices after the first, or weighted by MIS; otherwise direct light is counted twice.
- **Clamping.** Clamping bright contributions removes the bright pixels but makes the method biased.
- **Correlated random numbers.** Paths that share a random generator state, or a bad seed per pixel, give patterns in place of noise and a wrong standard error.

## Implementations

## History

Cook, Porter and Carpenter showed in 1984 with [distributed ray tracing](/distributed-ray-tracing/) that random rays give soft shadows, blur and glossy reflection. In 1986 Kajiya wrote the [rendering equation](/rendering-equation/) as one integral equation and solved it by Monte Carlo with a single random ray per bounce, which he called path tracing. He noted that branching at each bounce, as in earlier methods, spends most of the work on deep bounces that matter least. Arvo and Kirk brought Russian roulette and splitting from particle transport into image synthesis in 1990. Veach's thesis of 1997 gave the path integral view and the methods that most path tracers now use with it, among them multiple importance sampling. With these additions and faster ray queries, path tracing became the main method of offline film renderers.

## References
