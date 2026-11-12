---
tag: H80DBM
kind: algorithm
slug: instant-radiosity
name: Instant radiosity
area: graphics-and-signals/ray-tracing
level: research
summary: Trace random walks from the lights, turn each vertex into a virtual point light, and light the scene with all of them. The geometry term must be clamped near each light, and the clamp adds bias.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {N: the number of light paths, V: the number of virtual point lights, p: the number of camera points}
  time: {light_pass: O(V), gather: O(p V)}
  space: {total: Θ(V)}
properties: {deterministic: false, randomized: true, recursive: false, exact: false}
history:
  year: 1997
  people: [Alexander Keller]
  note: Keller presented instant radiosity at SIGGRAPH 1997. He rendered the image of each point light with graphics hardware and shadows and summed the images in the accumulation buffer.
prereqs: [light-tracing, lambertian-reflectance, monte-carlo-integration]
see_also: [radiosity, photon-mapping, bidirectional-path-tracing, russian-roulette, halton-sequence, shadow-mapping, final-gathering, restir]
sources:
  - paper: doi:10.1145/258734.258769
    title: Alexander Keller, Instant radiosity, Proceedings of SIGGRAPH 97, ACM, 1997, 49 to 56
    locator: the quasi-random walk from the lights, the point lights at its vertices, and the hardware rendering of their contributions
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, AK Peters, 2006
    locator: Chapter 7, Hybrid Algorithms, Section 7.7, Instant Radiosity
---

Instant radiosity approximates [global illumination](/global-illumination/) with many point lights. A light pass traces $N$ random walks from the lights, as in [light tracing](/light-tracing/). Each vertex of each walk becomes a *virtual point light* (VPL) with the power that the walk carries there. A second pass lights each point that the camera sees by all the VPLs, with a shadow ray or a shadow map for each one. A VPL on a diffuse surface sends light like a small Lambertian emitter. Its contribution has the geometry term $\cos\theta_x \cos\theta_y / |x - y|^2$, which is unbounded near the VPL, so points near a VPL get bright spots. Renderers **clamp** this term. The clamp removes energy near the VPLs, so it **adds bias**, which shows as dark corners. Despite the name, the method does not solve a [radiosity](/radiosity/) system.

## In plain words

Light in a room bounces from the lamp to a wall, from the wall to the floor, and on. Instant radiosity fakes the bounces with many small lamps.

First it follows a few hundred paths of light from the real lamp. At each place where a path hits a surface, it puts a small virtual lamp. The brightness of that lamp is the light that the path brought there. Then it lights the picture with all the virtual lamps, the same way it lights it with the real lamp.

A virtual lamp very close to a surface makes a too bright spot on it. So the method limits the light from each lamp to a maximum. The limit hides the spots, but it also removes some light that is really there, so corners look a little too dark.

## The problem

The goal is the reflected radiance

$$L_r(x, \omega_o) = \int_{\mathcal M} f_r(x, y \to x, \omega_o)\, L(y \to x)\, G(x, y)\, V(x, y)\, dA(y), \qquad G(x, y) = \frac{\cos\theta_x \cos\theta_y}{|x - y|^2},$$

at each visible point $x$, written over the surfaces $\mathcal M$ of the scene, with $L$ the solution of the [rendering equation](/rendering-equation/). Instant radiosity replaces the outgoing radiance $L(y \to x)$ of the scene by the sum of the radiances of a finite set of point lights at $y_1, \dots, y_V$, chosen so that the expected value of the sum is the true light. The output is an estimate of $L_r$ for each camera point. The method works best for diffuse surfaces.

## The algorithm

A VPL is a position $y$, a normal $n_y$, a power $\beta$ and a factor $f$. A VPL on a Lambertian surface with reflectance $\rho$ has $f = \rho/\pi$, and its radiant intensity toward $x$ is $\beta f \cos\theta_y$. A VPL on a Lambertian emitter has $f = 1/\pi$.

```pseudo id=main
INSTANT-RADIOSITY(scene, N, G_max)
L1  V ← an empty list of VPLs
L2  for j ← 1 to N do                                  ▷ the light pass
L3      sample a point y on a light; β ← Φ_lights / N; f ← the emission factor
L4      loop: append the VPL (y, n_y, β, f) to V
L5          if y is not on a light then survive with probability ρ(y); if not, break
L6          sample ω about n_y with the density cos θ/π; let y′ be the nearest hit; if none, break
L7          y ← y′; f ← ρ(y′)/π                         ▷ β stays the same
L8  for each camera point x and each VPL v ∈ V that x sees do     ▷ the gather pass
L9      G ← min(cos θ_x cos θ_y / |x − y_v|², G_max)
L10     S(x) ← S(x) + β_v f_v G
L11 L_r(x) ← f_r(x) · S(x)
```

Line L5 is [Russian roulette](/russian-roulette/). With the survival probability $\rho$, the power $\beta$ of the walk stays the same, so all the VPLs of a walk have the same power. The VPLs at line L3 give the direct light, and the VPLs after $k$ bounces give the light after $k + 1$ bounces. Keller used a [Halton sequence](/halton-sequence/) for the walks, which spreads the VPLs evenly, and drew the image of each VPL with hardware [shadow maps](/shadow-mapping/). The same VPLs serve all the pixels, so the noise of the method is correlated over the image. It shows as smooth blotches and not as grain.

## Example

**The furnace.** The inside of the unit sphere emits the exitance $B_e = 1$ and has the reflectance $\rho = 0.5$. The exact irradiance is $E = B_e/(1 - \rho) = 2$ at every point, and the reflected radiance is $L_r = \rho E/\pi = 1/\pi = 0.318310$. Inside a sphere, $G(x, y) = 1/4$ for every pair of points, so every VPL adds the same amount to every point and the clamp never acts if $G_{\max} \ge 1/4$. The $N$ light vertices add $1/N$ each, and each of the $S$ surface vertices adds $\rho/N$, so the estimate is $\frac{\rho}{\pi}(1 + \rho S/N)$. The number of surface vertices of a walk is geometric with the mean $1/(1 - \rho) = 2$, so the estimate is unbiased. For $N = 1000$ walks its standard deviation is $\frac{\rho^2}{\pi}\sqrt{\rho/((1 - \rho)^2 N)} = 0.0036$.

**The clamp.** A point light of power $\Phi = 1$ is at height $h = 1$ over a floor with $\rho = 0.5$. A sensor point at the height $a$ on the axis faces down to the floor, and its reflectance is 1. It gets only the light that the floor reflects once. The exact reflected radiance is

$$L_r(a) = \frac{1}{\pi}\int_0^\infty \frac{\rho}{\pi}\, \frac{\Phi h}{4\pi (h^2 + r^2)^{3/2}}\, \min\!\left(\frac{a^2}{(a^2 + r^2)^2}, G_{\max}\right) 2\pi r\, dr,$$

with $G_{\max} = \infty$ for the unclamped value. For $a = h$ it is $\rho\Phi/(10\pi^2 a^2)$. The table uses Simpson's rule for the integral, $G_{\max} = 4$, and the mean of 20 runs of 2000 walks, with seeds 0 to 19 and the standard error:

| $a$ | exact | clamped exact | bias | unclamped estimate | clamped estimate |
|---|---|---|---|---|---|
| 1 | 0.0050661 | 0.0050661 | 0 | 0.005152 ± 0.000055 | the same |
| 0.5 | 0.0080940 | 0.0080940 | 0 | 0.008343 ± 0.000135 | the same |
| 0.2 | 0.0109835 | 0.0065245 | −40.6 % | 0.011476 ± 0.000392 | 0.006812 ± 0.000149 |
| 0.1 | 0.0120145 | 0.0040001 | −66.7 % | 0.012321 ± 0.000803 | 0.004227 ± 0.000134 |
| 0.05 | 0.0124398 | 0.0022280 | −82.1 % | 0.012919 ± 0.001721 | 0.002362 ± 0.000102 |

The largest geometry term on the axis is $1/a^2$, so the clamp acts only for $a < 0.5$. Each estimate agrees with its own exact value. Without the clamp, the standard error grows like $1/a$ as the sensor nears the floor. With the clamp it stays small, but the estimate converges to the wrong value, and the error grows as the point comes nearer to the VPLs. This is the dark corner of instant radiosity.

## Correctness

**Without the clamp, the estimate is unbiased.** Russian roulette with the survival probability $\rho$ keeps the expected power: a walk that reaches $y$ with the power $\beta$ reaches the next vertex with the power $\beta$ with the probability $\rho(y)$, and the expected power of the next vertex is $\rho(y)\beta$, the power that the surface reflects. The direction is sampled with the cosine density of a Lambertian surface. By induction over the bounces, as for [photon mapping](/photon-mapping/), the expected sum over the VPLs of $\beta_v f_v\, g(y_v, \omega)$ is the integral of $g$ against the outgoing radiance of the scene, for each weight $g$. Take $g = f_r(x)\,G(x, \cdot)\,V(x, \cdot)$. Then the expected value of line L11 is $L_r(x)$, the same equation as in the problem.

**The clamp makes it biased.** With the clamp, line L9 replaces $G$ by $\min(G, G_{\max}) \le G$, so the expected value is the same integral with the smaller kernel. It is less than $L_r(x)$ when $G(x, y) > G_{\max}$ on a part of the surfaces with light. This part is near $x$, so the missing light is short-range light, as in corners. The missing part is a well-defined integral, and bias compensation methods estimate it with a separate path tracing step.

**The variance without the clamp is unbounded.** Near a VPL at the distance $d$, the term $G$ can be as large as $1/d^2$. In the sensor example the second moment of one VPL's contribution is proportional to $\int G^2\, dA = \int_0^\infty \frac{a^4}{(a^2 + r^2)^4}\, 2\pi r\, dr = \frac{\pi}{3a^2}$, so the variance grows without bound as the sensor comes near the floor, and the standard error in the table doubles each time $a$ is halved. The clamp bounds the second moment by $G_{\max}$ times the first.

## Complexity

The light pass casts one ray for each VPL, $V \approx N/(1 - \bar\rho)$ rays with the mean reflectance $\bar\rho$. The gather pass costs $O(V)$ for each camera point, one shadow test for each VPL, so $O(pV)$ in all. With shadow maps, the cost is one render of the scene from each VPL and one shading pass of the image with each map. The memory holds the VPLs, $\Theta(V)$, plus the shadow maps if they are kept. Many-light methods such as Lightcuts reduce the gather to a sublinear number of VPLs for each point.

## Properties

- **Biased with the clamp, unbiased without it.** The unclamped estimate is unbiased, but its variance grows without bound near the VPLs.
- **Consistent only in a limit.** If the clamp bound grows with $N$ but $G_{\max}/N \to 0$, both the bias and the variance go to 0.
- **Smooth noise.** All pixels share the same VPLs, so the error is correlated over the image. A small number of VPLs gives smooth, plausible images, which makes the method popular for real-time and preview rendering.
- **Fits rasterization.** Each VPL is a point light with a shadow map, which graphics hardware draws fast.
- **Poor for glossy surfaces.** A glossy BRDF at the VPL or at $x$ makes the contribution of each VPL a sharp highlight, so many more VPLs are needed.

## Variants and improvements

- **Quasi-random walks.** Keller's original method uses low discrepancy points for the walks, so the VPLs cover the scene evenly.
- **Bias compensation.** Kollig and Keller estimated the light removed by the clamp with a path tracing step that runs only where the clamp acts. The result is unbiased again.
- **Many lights.** Lightcuts (Walter and others, 2005) groups the VPLs in a tree and uses one representative for each group, with an error bound. Matrix row column sampling picks the VPLs that matter for the whole image.
- **Virtual spherical lights.** Spread each VPL over a small sphere to remove the singularity for glossy surfaces.
- **Bidirectional instant radiosity.** Choose the VPLs where the camera sees them, by tracing paths from the camera as well.
- **Reservoir resampling.** [ReSTIR](/restir/) picks a few VPLs or light samples for each pixel by resampling, and reuses them over pixels and frames.

## When to use it

Use instant radiosity for diffuse indirect light in previews, in interactive applications and with a rasterizer that draws shadow maps fast. Use it when smooth, slightly darkened corners are acceptable. For glossy scenes, caustics or a correct reference image, use [path tracing](/path-tracing/), [bidirectional path tracing](/bidirectional-path-tracing/) or [photon mapping](/photon-mapping/) instead.

## Pitfalls

- **Splotches.** Without a clamp, a VPL close to a surface makes a bright spot on it. Clamp $G$, or the full contribution, or use a bias compensation.
- **Dark corners.** The clamp removes the short-range light. The table shows that the loss grows to more than 80 percent near the floor for a large clamp. Choose $G_{\max}$ with the scene size in mind, or compensate the bias.
- **A VPL on the light itself.** If the direct light comes from the VPLs of line L3 and also from an explicit light sample, it is counted two times.
- **Counting the BRDF of the VPL two times.** The factor $f = \rho/\pi$ of a surface VPL is the BRDF at the VPL. Do not multiply the power by $\rho$ at the bounce as well, when Russian roulette with the probability $\rho$ already accounts for the absorption.
- **Glossy VPLs.** A VPL that stores only a diffuse factor gives wrong light on glossy surfaces. Store the incoming direction and evaluate the full BRDF.
- **Temporal flicker.** New random walks in each frame move the VPLs and make the image flicker. Keep the walks fixed or use the same quasi-random points.

## Implementations

## History

Keller presented instant radiosity at SIGGRAPH 1997. He traced quasi-random walks from the lights, placed a point light at each vertex, and rendered the image with each point light by graphics hardware with shadows, summed in the accumulation buffer. The name comes from the radiosity community, since the first target was diffuse light at interactive rates. Later work made the idea scale and removed its artifacts. Lightcuts grouped millions of VPLs in 2005, virtual spherical lights handled glossy surfaces, and bias compensation methods restored the light that the clamp removes. Many-light methods based on VPLs became common in film and games for baked and real-time indirect light.

## References
