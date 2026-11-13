---
tag: EFE9E0
kind: algorithm
slug: photon-mapping
name: Photon mapping
area: graphics-and-signals/ray-tracing
level: advanced
summary: A two-pass global illumination method. Trace photons from the lights and store their hits in a kd-tree, then estimate the radiance at each visible point from the density of the nearest photons.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {n: the number of photon paths, l: the mean number of stored hits per path, p: the number of camera points, k: the number of photons per estimate}
  time: {photon_pass: O(n l), build: "O(n l log(n l)) expected", estimate: O(p n l log k)}
  space: {total: "Θ(n l)"}
properties: {deterministic: false, randomized: true, recursive: false, exact: false}
history:
  year: 1996
  people: [Henrik Wann Jensen]
  note: Jensen presented the two-pass method with a global photon map and a caustic map at the Eurographics Workshop on Rendering in 1996, and described it in full in a book in 2001.
prereqs: [photon-map, rendering-equation, light-tracing, monte-carlo-integration]
see_also: [progressive-photon-mapping, vertex-connection-and-merging, final-gathering, irradiance-caching, path-tracing, bidirectional-path-tracing, russian-roulette, bias-variance-tradeoff]
sources:
  - paper: doi:10.1007/978-3-7091-7484-5_3
    title: Henrik Wann Jensen, Global illumination using photon maps, Rendering Techniques '96 (Proceedings of the 7th Eurographics Workshop on Rendering), Springer, 1996, 21 to 30
    locator: the photon tracing pass, the global and caustic photon maps, and the radiance estimate from the nearest photons
  - book: isbn:9781568811475
    title: Henrik Wann Jensen, Realistic Image Synthesis Using Photon Mapping, AK Peters, 2001
    locator: Chapter 5 Photon Tracing, Chapter 6 The Photon Map Data Structure, and the chapters The Radiance Estimate and A Practical Two-Pass Algorithm
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, AK Peters, 2006
    locator: Chapter 7, Hybrid Algorithms, the section on photon mapping
  - paper: doi:10.1145/1966394.1966404
    title: Claude Knaus and Matthias Zwicker, Progressive photon mapping, a probabilistic approach, ACM Transactions on Graphics 30(3), 2011, article 25
    locator: the bias and the variance of the radiance estimate as functions of the radius and the number of photons
---

Photon mapping is a two-pass method for [global illumination](/global-illumination/). The first pass traces photons from the lights, as in [light tracing](/light-tracing/), and stores each hit on a diffuse surface in a [photon map](/photon-map/), a balanced [kd-tree](/kd-tree/). The second pass traces rays from the camera. At each visible diffuse point it finds the $k$ nearest photons and estimates the reflected radiance as their BRDF-weighted power divided by the area $\pi r^2$ of the disc that holds them. This is a density estimate, so the method is **biased**: its expected value is the light averaged over a disc, not the light at the point. With a fixed radius it is also **not consistent**, because more photons do not remove that average. It handles caustics and indirect light that [path tracing](/path-tracing/) finds slowly.

## In plain words

A path tracer starts at the camera and hopes to find the lamp. This is hard when the light comes through a glass or off a mirror, as in the bright pattern at the bottom of a pool.

Photon mapping works from both ends. First it shoots many small packets of light from the lamps. Each packet bounces around the scene, and the method writes down each place where it lands on a matte surface. Then it looks from the camera. At each point it sees, it counts the packets that landed close to that point. Many packets in a small area mean a bright spot.

The count uses a small area, not a point. So the result is a little blurred. More packets make the blur less only if the area also gets smaller.

## The problem

The scene has surfaces with BRDFs $f_r$ and lights with emitted radiance $L_e$. The goal is the outgoing radiance $L(x, \omega_o)$ of the [rendering equation](/rendering-equation/) at each visible point. At a diffuse point it splits as

$$L(x, \omega_o) = L_e(x, \omega_o) + L_r(x, \omega_o), \qquad L_r(x, \omega_o) = \int_{H^2} f_r(x, \omega_i, \omega_o)\, L_i(x, \omega_i) \cos\theta_i\, d\omega_i.$$

Photon mapping estimates $L_r$ from the incident flux near $x$. The output is an approximation of $L$ for each camera ray.

## The algorithm

```pseudo id=main
PHOTON-MAPPING(scene, N, k, r_max)
L1  M ← an empty list of photons
L2  for j ← 1 to N do                              ▷ pass 1: photon tracing
L3      sample a light point y and a direction ω; β ← L_e(y, ω) cos θ / (p(y, ω) · N)
L4      loop
L5          x ← the nearest surface hit of the ray (y, ω); if there is none then break
L6          if the surface at x is not purely specular then append (x, β, ω) to M
L7          sample ω′ from the BSDF and survive with probability q; if not, break; β ← β · f cos θ′ / (p(ω′) · q)
L8          y ← x, ω ← ω′
L9  build the photon map of M
L10 for each camera ray, with nearest diffuse hit x and direction ω_o do    ▷ pass 2
L11     find the k nearest photons to x within r_max; r ← the distance to the farthest
L12     L ← L_e(x, ω_o) + Σ_p f_r(x, ω_p, ω_o) ΔΦ_p / (π r²)
```

In line L3 the power $\beta$ is the light's contribution divided by the probability of the sample, so the expected total power of the photons is the power of the lights. Line L7 is [Russian roulette](/russian-roulette/). When $q$ equals the reflectance of a Lambertian surface, the power of a surviving photon stays the same. In line L12 the direction $\omega_p$ points to where the photon came from.

Jensen's practical renderer splits the light into parts. Direct light is computed by ray tracing to the lights. Caustics, the paths light, specular, diffuse, come from a separate *caustic map* with many photons, viewed directly. The rest of the indirect light comes from a *global map* viewed through [final gathering](/final-gathering/), one bounce of rays from $x$ before the lookup. Specular reflection is traced recursively from the camera.

## Example

**Furnace sphere.** The inside of the unit sphere is Lambertian with reflectance $\rho = 0.5$ and emits the exitance $B_e = 1$ everywhere. By symmetry the radiosity is $B = B_e/(1 - \rho) = 2$ and the radiance is $L = B/\pi = 0.636620$ everywhere. A point and a cosine-weighted direction from it give a hit point that is uniform on the sphere, so photons are spread uniformly. The part of the sphere within the chord distance $r$ of a point on it has area exactly $\pi r^2$, by Archimedes' hat-box theorem, and the irradiance is constant. So in this scene the fixed-radius estimate is unbiased.

With $N = 5000$ paths and seed 1996, pass 1 stores 9857 photons, close to $N/(1 - \rho) = 10000$. The mean of the estimate of $L$ over evenly spread points:

| estimate | points | mean | standard error | reflected part / exact |
|---|---|---|---|---|
| fixed radius $r = 0.15$ | 100 | 0.63328 | 0.00401 | 0.990 |
| $k = 10$ nearest | 400 | 0.66481 | 0.00614 | 1.089 |
| $k = 50$ nearest | 100 | 0.63885 | 0.00438 | 1.007 |

The $k$-nearest estimate is high by the factor $k/(k - 1)$ in the mean, 1.111 for $k = 10$, because the radius $r_k$ is set by the photons themselves. The fixed-radius estimate is within one standard error of the exact value.

**Point light over a plane.** A point light of power $\Phi = 1$ is at height $h = 1$ over an absorbing plane. The irradiance at distance $s$ from the foot is $E(s) = \Phi h / (4\pi (h^2 + s^2)^{3/2})$, so $E(0) = 0.0795775$. The mean of $E$ over the disc of radius $R$ is

$$\bar E_R = \frac{\Phi}{2\pi R^2}\left(1 - \frac{h}{\sqrt{h^2 + R^2}}\right),$$

which is 0.0672097 for $R = 0.5$ and 0.0760315 for $R = 0.25$. The fixed-radius estimate at the foot, with $N$ photons emitted:

| $N$ | $R = 0.5$ | $R = 0.25$ |
|---|---|---|
| 10000 | 0.0648 ± 0.0028 | 0.0738 ± 0.0062 |
| 40000 | 0.0674 ± 0.0014 | 0.0749 ± 0.0031 |
| 160000 | 0.06702 ± 0.00071 | 0.0750 ± 0.0015 |

The estimates converge to $\bar E_R$, not to $E(0)$. The bias is $-15.5$ percent for $R = 0.5$ and $-4.5$ percent for $R = 0.25$, at every $N$. For a small radius the relative bias is about $-3R^2/(4h^2)$.

## Correctness

Photon tracing is unbiased for flux. For a region $A$ of surface and a weight $g(x, \omega)$, the expected sum of $g(x_p, \omega_p)\,\Delta\Phi_p$ over the photons in $A$ is the incident flux $\int_A \int g\, L_i \cos\theta\, d\omega\, dA$. This follows from the Neumann series of the transport, by induction on the number of bounces, as for path tracing. The estimate of line L12 with a fixed radius $r$ on a flat surface therefore has the expected value

$$E[\hat L_r(x)] = \frac{1}{\pi r^2} \int_{D_r(x)} \int f_r(x, \omega_i, \omega_o)\, L_i(x', \omega_i) \cos\theta_i\, d\omega_i\, dA(x'),$$

the mean of the reflected radiance over the disc $D_r(x)$, with the BRDF at $x$. This differs from $L_r(x)$ unless the light is constant on the disc. As $N \to \infty$ with $r$ fixed, the estimate converges to this mean, by the law of large numbers, so it is not consistent. If $E$ is twice differentiable, the mean over the disc is

$$\bar E_r = E(x) + \frac{r^2}{8}\, \Delta E(x) + o(r^2),$$

so the bias is $O(r^2)$. For the point light, $\Delta E(0) = -6E(0)/h^2$, which gives the relative bias $-3r^2/(4h^2)$. The proofs are in the proof file.

## Complexity

Pass 1 traces $N$ paths with $l$ stored hits each on average, so it makes $O(Nl)$ ray casts. With Russian roulette at reflectance $\rho$, $l = 1/(1 - \rho)$ for a closed scene. Building the photon map takes $O(Nl \log(Nl))$ expected time. Each estimate in pass 2 is a k-nearest search, which costs $O(k \log k + \log(Nl))$ in practice. In the worst case it visits all $Nl$ photons and keeps the $k$ nearest in a heap, $O(Nl \log k)$, so the $p$ estimates cost $O(pNl \log k)$, the bound in the summary. The memory holds all $Nl$ photons, and memory is often the limit of the method.

The estimate with a fixed radius has the variance $O(1/(N r^2))$, because a photon falls in the disc with probability proportional to $r^2$ and has the weight $1/(N \pi r^2)$. With the bias $O(r^2)$, the mean squared error is

$$\text{MSE} = O(r^4) + O\!\left(\frac{1}{N r^2}\right),$$

which is smallest for $r \propto N^{-1/6}$, with $\text{MSE} = O(N^{-2/3})$. This is the [bias-variance tradeoff](/bias-variance-tradeoff/). An unbiased Monte Carlo estimator has $\text{MSE} = O(N^{-1})$ when its variance is finite. But for a caustic from a point light seen in a mirror by a pinhole camera, a path of the form light, specular, diffuse, specular, camera, the local path sampling of path tracing and bidirectional path tracing finds the path with probability 0. Then a density estimate such as photon mapping is the practical method.

## Properties

- **Biased.** The estimate blurs the light over the disc of radius $r$.
- **Not consistent with a fixed radius.** More photons reduce the noise but not the blur. [Progressive photon mapping](/progressive-photon-mapping/) makes the radius shrink and is consistent.
- **Consistent only in a limit.** If $r \to 0$ and $N r^2 \to \infty$, the estimate converges to $L_r(x)$ at points where the light is continuous.
- **View independent first pass.** The photon map depends only on the scene and the lights, so it can serve many views.
- **Low noise, low frequency errors.** The error looks like a smooth blotchy pattern rather than high frequency noise.

## Variants and improvements

- **Caustic map and global map.** Store caustic photons apart and with more photons. View the global map only through final gathering.
- **Final gathering.** Shoot rays from $x$ and look up the photon map at their hits. The blur moves one bounce away from the eye, where it is not visible.
- **Irradiance caching.** With final gathering, compute the gathered value at a sparse set of points and interpolate, as in [irradiance caching](/irradiance-caching/).
- **Filters.** A cone or Gaussian weight on the photons sharpens edges of caustics, with a normalization so that the estimate stays correct for a constant density.
- **Volume photon map.** Store photons at scattering events inside a [participating medium](/participating-media/) and divide by the volume of a sphere, $\frac{4}{3}\pi r^3$.
- **Progressive and stochastic progressive photon mapping.** Shrink the radius over passes, for a consistent result with bounded memory.
- **Vertex connection and merging.** Combine photon density estimation with bidirectional path tracing under multiple importance sampling, as in [vertex connection and merging](/vertex-connection-and-merging/).
- **Importance-driven photon tracing.** Send photons toward the parts of the scene that the camera sees.

## When to use it

Use photon mapping for scenes with caustics, and for light that reaches the camera through specular surfaces, where path tracing and bidirectional path tracing converge slowly or not at all. Use it when a small blur is acceptable in exchange for low noise. When an exact reference is necessary, use a consistent variant, or use an unbiased method where one works.

## Pitfalls

- **Viewing the global map directly.** Without final gathering, the low frequency blotches of the global map are visible on walls. Jensen views only the caustic map directly.
- **The bias of the k-nearest radius.** The plain $k$-nearest estimate is high by the factor $k/(k - 1)$ for a uniform density. The furnace table shows it.
- **Leaks near corners and edges.** The search sphere collects photons from another surface near a corner, and at the edge of a surface the disc is partly empty, so the estimate is too low there. Use a disc in the tangent plane and test the photon normal.
- **Storing photons on specular surfaces.** A mirror has a delta BRDF, so a density estimate there is meaningless. Store photons only on surfaces with a non-specular part.
- **Counting the direct light two times.** If direct light is computed by ray tracing to the lights, do not store the first photon hit in the map that is used for the same light. The global map then holds only photons after at least one bounce, or the first hits are skipped at lookup.
- **Power units.** Each photon carries flux in watts, not radiance. Divide by $N$, the number of emitted photon paths, not the number of stored photons.

## Implementations

## History

Jensen and Christensen used photon maps in a bidirectional Monte Carlo ray tracer in 1995. Jensen's paper at the Eurographics Workshop on Rendering in 1996 gave the two-pass method, with a global photon map, a caustic map and the radiance estimate from the nearest photons in a balanced kd-tree. His book of 2001 describes photon tracing, the data structure, the radiance estimate, the practical two-pass renderer and photon maps for participating media. Hachisuka, Ogaki and Jensen made the method consistent with progressive photon mapping in 2008. Georgiev and others, and in parallel Hachisuka, Pantaleoni and Jensen, combined it with bidirectional path tracing in 2012.

## References
