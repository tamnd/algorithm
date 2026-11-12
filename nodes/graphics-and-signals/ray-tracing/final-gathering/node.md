---
tag: 9YA41P
kind: technique
slug: final-gathering
name: Final gathering
area: graphics-and-signals/ray-tracing
level: advanced
summary: Get the indirect light at a visible point by tracing one bounce of rays over the hemisphere, and read the coarse global solution, such as a photon map, only where those rays hit.
prereqs: [photon-mapping, monte-carlo-integration, stratified-sampling]
see_also: [irradiance-caching, photon-map, progressive-photon-mapping, path-tracing, radiosity, instant-radiosity, next-event-estimation, vertex-connection-and-merging]
sources:
  - paper: doi:10.1007/978-3-7091-7484-5_3
    title: Henrik Wann Jensen, Global illumination using photon maps, Rendering Techniques '96 (Proceedings of the Eurographics Workshop on Rendering), Springer, 1996, 21 to 30
    locator: the two-pass method, in which the indirect diffuse light is computed by Monte Carlo ray tracing that reads the global photon map at the secondary hits
  - book: isbn:9781568811475
    title: Henrik Wann Jensen, Realistic Image Synthesis Using Photon Mapping, AK Peters, 2001
    locator: the chapter A Practical Two-Pass Algorithm, on the split into direct light, specular reflection, caustics and multiple diffuse reflection, and the final gathering of the last one
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, AK Peters, 2006
    locator: Chapter 7, Hybrid Algorithms, on final gathering for radiosity solutions and for photon maps
---

Final gathering is a technique for using a coarse global illumination solution without showing its errors. A photon map, a radiosity solution or another precomputed estimate of the light is often blotchy or blurred, and reading it at the points that the camera sees puts these errors straight into the image. Final gathering reads it one bounce later instead. At a visible diffuse point $x$ it traces many rays over the hemisphere, finds the points $y$ that they hit, and reads the coarse estimate of the outgoing radiance $\hat L(y \to x)$ there. The estimate of the indirect irradiance is $\pi$ times the mean of these values, with cosine-weighted rays. Each error of the coarse solution enters with the small weight of one ray among hundreds, so the errors are averaged over the hemisphere. Direct light and caustics at $x$ are computed separately, because they change fast and the gather would sample them badly.

## In plain words

Suppose there is a rough map of how bright each wall is. To light a spot on the floor, the renderer could look up the map right at that spot. Then every flaw of the map shows on the floor.

Final gathering asks each surface around the spot instead. It sends hundreds of rays out from the spot, and where each ray lands, it reads the rough map there. Then it adds up what the rays found.

The flaws of the map do not line up across all those rays, so they mostly cancel out. The floor looks smooth, even though the map is rough. The cost is the hundreds of rays at each spot.

## When it applies

- A coarse estimate of the outgoing radiance $\hat L$ is available at every surface point: a global photon map, a radiosity mesh, a set of virtual point lights, or a precomputed irradiance at the photons.
- The receiving point $x$ is diffuse or nearly so, so the gather is an integral of $\hat L$ against the cosine over the hemisphere.
- The light that the gather samples changes slowly over the hemisphere. Small bright sources and caustics do not, so they are handled apart.
- The errors of $\hat L$ are local, such as noise and blur at the scale of a photon radius, so that many gather rays average them.

## The template

The reflected radiance at a Lambertian point $x$ with the albedo $\rho_x$ is $\frac{\rho_x}{\pi} E(x)$, with

$$E(x) = \int_{H^2(n)} L(y(x, \omega) \to x) \cos\theta\, d\omega,$$

where $y(x, \omega)$ is the first surface that the ray from $x$ in the direction $\omega$ hits. Final gathering estimates this integral with $m^2$ stratified cosine-weighted directions and puts the coarse estimate $\hat L$ in place of $L$:

```pseudo id=main
FINAL-GATHER(x, n, m)
L1  total ← 0
L2  for each of the m × m strata (i, j) do
L3      ω ← a cosine-weighted direction about n, from a random point of the stratum (i, j)
L4      y ← the first hit of the ray from x in the direction ω
L5      if y is on an emitter then
L6          skip it                               ▷ direct light at x is computed apart
L7      total ← total + the coarse radiance estimate L̂(y → x), from the photon map
L8  return π · total / m²
```

With the density $\cos\theta/\pi$, each sample of the integrand $L \cos\theta$ divided by the density is $\pi L$, which gives line L8. In a photon map renderer, line L7 is the density estimate $\hat L(y) = \frac{\rho_y}{\pi}\cdot\frac{1}{\pi r^2}\sum_p \Phi_p$ over the photons near $y$, or the $k$ nearest photons in the [photon map](/photon-map/).

**Why it helps.** Let $\hat L = L + e$, where $e$ is the error of the coarse solution. The gather returns $\pi\cdot\frac{1}{m^2}\sum_{s}(L(y_s) + e(y_s))$. The first part is an unbiased estimate of $E(x)$, with the variance of a stratified Monte Carlo estimate. The second part is an average of $m^2$ values of the error at points spread over the scene. If the error has a mean of 0 and is uncorrelated at the scale of the spread, its contribution shrinks like $1/m$. A systematic error, such as the bias of the density estimate in a corner, does not shrink; it is weighted by the solid angle of the region where it occurs.

**The split of the light.** Jensen's two-pass method computes the radiance at $x$ as the sum of four parts: direct light from [next event estimation](/next-event-estimation/), specular and glossy reflection by ray tracing, caustics from a separate caustic photon map read at $x$, and the multiple diffuse reflection by final gathering of the global photon map. The gather rays skip emitters (line L6), because direct light is the first part. The photon map read at $y$ holds all the light that $y$ receives, direct and indirect, because for $x$ that is all indirect.

## Classic examples

**The photon map, one bounce away.** The room is the box $[0, 2]\times[0, 2]\times[0, 1]$ with an emitter $[0.75, 1.25]^2$ of radiance 1 on the ceiling and four side walls of albedo $\frac12$. The photons are emitted from the light, and the direct map stores their first hits. One-bounce indirect irradiance at the floor center has the exact value 0.0106765, from Gauss-Legendre quadrature of Lambert's formula over the walls. The direct irradiance there is 0.230837. The same photons give two estimates: the *direct lookup*, the density of the photons that land on the floor near the center after one bounce off a wall, and the *final gather*, 256 stratified rays that read the direct map of the walls. Over 10 seeds:

| photons | radius | gather: mean error | gather: rms error | direct lookup: mean error | direct lookup: rms error |
|---|---|---|---|---|---|
| 10000 | 0.1 | −1.8% | 4.1% | +0.7% | 50.3% |
| 10000 | 0.05 | −0.5% | 3.7% | +21.8% | 127.9% |
| 40000 | 0.1 | −1.3% | 2.7% | −2.2% | 23.2% |
| 40000 | 0.05 | +0.4% | 3.4% | −4.0% | 51.9% |
| 160000 | 0.05 | +0.1% | 2.4% | +9.5% | 18.4% |

With 10000 photons and the radius 0.1, the disc of the direct lookup holds about 4 bounced photons on average, so its relative error is near $1/\sqrt 4$. The gather reads 256 discs on the walls, each with many direct photons, and its error is mostly the noise of the 256 rays. With the exact radiance at the hit points, 64 gather rays have a relative standard deviation of 8.0%, and the mean of 200 gathers agrees with the exact value.

**Radiosity with a final gather.** A coarse radiosity solution on a mesh has shading errors along the mesh edges and at shadow boundaries. A final gather from each pixel, which reads the radiosity of the patches that the rays hit, removes the mesh from the image. Two-pass and multi-pass radiosity renderers of the early 1990s used this step.

**Gathering with an irradiance cache.** A full gather at every pixel costs hundreds of rays each. Jensen's practical renderer computes the gather only at the records of an [irradiance cache](/irradiance-caching/) and interpolates between them.

**Precomputed irradiance.** Christensen (1999) computed the irradiance at a subset of the photons in a preprocess, so that each gather ray reads one precomputed value instead of running a density estimate.

## Variations

- **A distance threshold.** Gather rays that hit a surface very close to $x$ read the photon map where its blur is most visible. Trace one more bounce for them, or use a higher photon density, as in Jensen's practical method.
- **Importance-driven gathering.** Sample the gather directions with a density proportional to an estimate of the incoming light, for example from the photons near $x$, as in Jensen's 1995 importance sampling with photon maps.
- **Final gathering of virtual point lights.** In [instant radiosity](/instant-radiosity/), connecting each pixel to every VPL is a gather over a discrete set of sources.
- **Progressive gathering.** In [progressive photon mapping](/progressive-photon-mapping/) the hit points are the points where the gather would end, and the photon statistics are kept there instead.
- **Path tracing.** With no coarse solution at all, the gather becomes a recursive estimate, which is [path tracing](/path-tracing/).

## Pitfalls

- **Double counting.** If the gather adds the emission at $y$ and the direct light at $x$ is also computed by light sampling, the direct light is counted twice. Skip emitters in the gather, as in line L6. In the same way, do not read the caustic photons at $y$ and also read the caustic map at $x$.
- **Corners and short rays.** Near a corner many gather rays are short and land where the photon density estimate has its boundary bias. The blotches of the photon map then show through. Use a distance threshold or more photons.
- **Too few gather rays.** The gather has the noise of a Monte Carlo estimate with $m^2$ samples. With few rays the image is noisy, not blotchy, and the gather has only moved the error.
- **Gathering specular light.** A gather ray that hits a mirror or glass should continue, and the specular paths seen through the gather need their own treatment. Light that reaches $x$ by a specular bounce from a small light is a caustic, and the caustic map handles it.
- **Cost.** Hundreds of rays at each pixel, each with a photon lookup, dominate the cost of the method. Cache the results or gather only where needed.

## Exercises

1. Show that with cosine-weighted directions the gather of line L8 is an unbiased estimate of $E(x)$ when $\hat L = L$, and write the estimator for directions that are uniform over the hemisphere.
2. Let the error $e(y)$ of the coarse solution have the mean 0 and the variance $\sigma^2$, independently at the $m^2$ hit points. Show that the error term of the gather has the variance $\pi^2 \sigma^2/m^2$.
3. In the example, the direct lookup at the floor center with $N$ photons and the radius $r$ holds about $\lambda = E_{\text{ind}}\,\pi r^2 N/\Phi$ photons, where $\Phi = \pi\cdot 0.25$ is the emitted power. Compute $\lambda$ for $N = 10000$ and $r = 0.1$, and explain the rms error of 50% in the table.
4. Explain why a gather ray that hits the emitter is skipped, but the photon map read at a wall point includes the direct photons there.
5. A corner of a room has two walls at a right angle. Describe the bias of a disc density estimate of radius $r$ at a wall point at the distance $t < r$ from the corner, and explain why the gather from a point near the corner shows it more than a gather from the center of the room.

## References
