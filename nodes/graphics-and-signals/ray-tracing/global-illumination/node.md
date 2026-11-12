---
tag: 1XTEFB
kind: problem
slug: global-illumination
name: Global illumination
aliases:
- light transport simulation
area: graphics-and-signals/ray-tracing
level: core
summary: Compute the image of a scene with all the light that reaches the camera, direct and after any number of bounces, by solving the rendering equation for the pixel values.
prereqs: [rendering-equation]
see_also: [path-tracing, radiosity, photon-mapping, bidirectional-path-tracing, metropolis-light-transport, ambient-occlusion, whitted-ray-tracing, monte-carlo-integration]
sources:
  - paper: doi:10.1145/15886.15902
    title: James T. Kajiya, The rendering equation, Computer Graphics (SIGGRAPH 86) 20(4), 1986, 143 to 150
    locator: the rendering equation as the common frame of the rendering methods of the time, and path tracing as a solution
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: the measurement equation, the path integral, and the limits of local path sampling for specular paths with point lights and pinhole cameras
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 14, Light Transport I, Surface Reflection, and Chapter 16, Light Transport III, Bidirectional Methods
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, A K Peters, 2006
    locator: the chapters on strategies for computing light transport, stochastic path tracing and stochastic radiosity
  - paper: "John H. Reif, J. D. Tygar and Akitoshi Yoshida, The computability and complexity of optical beam tracing, 31st Annual Symposium on Foundations of Computer Science (FOCS), 1990"
    locator: the undecidability of ray tracing in some optical systems, and its PSPACE-hardness in simpler ones
---

Global illumination is the problem of computing what a camera sees in a scene when all the paths of light count: light that comes straight from a lamp, and light that has bounced off any number of surfaces on the way. Formally, each pixel value is an integral of the solution of the [rendering equation](/rendering-equation/). The word "global" is in contrast with *local illumination*, where each point is shaded from the lights alone, as if the rest of the scene were not there. Exact solutions exist only for special scenes, so the methods are estimators: some are unbiased, some are only consistent, and some are biased on purpose to be fast. This page states the problem and its limits; the algorithms have their own pages.

## In plain words

Shine a red lamp at a white wall, and the floor in front of the wall turns slightly red. No lamp shines red light on the floor; it comes from the wall. A room lit by one window is bright in the corners that the window cannot see, because light bounces off the walls into them.

Global illumination means making a picture that gets all of this right. For each pixel, you must add up the light from every route it could take from a lamp to the camera: straight, or off one surface, or off two, or off a hundred.

There are too many routes to follow them all. So the methods pick routes at random and average, or they store light on surfaces and reuse it. They trade time, noise and small errors against each other.

## Definition

**Input.** A scene: a set $M$ of surfaces, a BSDF at each surface point, the emitted radiance $L_e$, and optionally [participating media](/participating-media/). A camera: for each pixel $j = 1, \dots, P$, a response function $W_j(x, \omega)$ on the sensor.

**Output.** The pixel values

$$I_j = \int W_j(x, \omega)\, L_i(x, \omega) \cos\theta \, dA(x)\, d\omega,$$

where $L$ is the solution of the rendering equation $L = L_e + TL$ and $L_i$ is the radiance arriving at the sensor. In a *view-independent* version, the output is $L$ itself, or an approximation of it on all surfaces, for example one value per patch.

**The cost model.** A real RAM that can also ask a ray tracer two kinds of queries: the first surface that a ray meets (a [closest-hit query](/closest-hit-query/)) and whether a segment is blocked (an [any-hit query](/any-hit-query/)). The cost is the number of queries and the other work per pixel.

**What counts as a solution.** Exact values are out of reach in general, as the bounds below show. A method returns an estimate $\hat I_j$. It is *unbiased* if $E[\hat I_j] = I_j$ for every scene, *consistent* if $\hat I_j \to I_j$ as the work grows, and biased otherwise. The error is measured as the root mean square error, or its ratio to $I_j$.

## Variants

- **Direct illumination only.** Light from the lamps after one reflection, with shadows. This is [shadow determination](/shadow-determination/) plus one integral per point, and [next event estimation](/next-event-estimation/) solves it well.
- **Diffuse only.** Every surface is Lambertian. With piecewise constant radiance, the problem becomes the linear system of [radiosity](/radiosity/), and the solution does not depend on the camera.
- **Specular paths only.** Perfect mirrors and glass with point lights, as in [Whitted ray tracing](/whitted-ray-tracing/), where each path is found by following deterministic rays.
- **With participating media.** Light that scatters in smoke, fog or skin, where the radiative transfer equation replaces the rendering equation; see [volumetric path tracing](/volumetric-path-tracing/).
- **Real time.** A fixed budget of a few rays per pixel and frame, often with reuse between frames and pixels and a denoiser, at the cost of bias.
- **Spectral and time-dependent.** Many wavelengths ([spectral rendering](/spectral-rendering/)) or a moving scene with motion blur, which add dimensions to each integral.

## Examples

**Direct and indirect light in a closed sphere.** The sphere of the [rendering equation](/rendering-equation/) page has four zones of equal area with the emitted radiance $(0, 0, 0, 4)$ and the albedo $(\tfrac12, \tfrac14, \tfrac34, \tfrac12)$. The exact radiance is $(1, \tfrac12, \tfrac32, 5)$. Local illumination, with one reflection of the emitter, gives $(\tfrac12, \tfrac14, \tfrac34, \tfrac92)$. So in the three zones that do not emit, half of the light is indirect, and local shading would show them at half of their brightness.

**How many bounces.** In a furnace, a closed scene with the albedo $\rho$ everywhere, the share of the light that has bounced more than $k$ times is $\rho^{k+1}$. For a 1 percent error, the sum must go to $k = 6$ bounces for $\rho = 0.5$ and to $k = 43$ for $\rho = 0.9$. Bright interiors need long paths, which is why [Russian roulette](/russian-roulette/) ends paths at random and not at a fixed depth.

**A small light makes noise.** Close the sphere again with black walls, and let one cap with the area share $a$ emit the radiance $L_e / a$, so that the light power does not depend on $a$. A cosine-weighted ray from a wall point hits the cap with the probability $a$, because inside a sphere every point sees each piece of the sphere in proportion to its area. So the one-bounce estimate is $L_e / a$ with the probability $a$ and $0$ otherwise: its mean is $L_e$, the right value, and its relative variance is $1/a - 1$. For a cap of 1 percent of the area, a single sample has a relative standard deviation near $10$, and 10000 samples per pixel are needed for 10 percent. Sampling the light directly, as next event estimation does, removes this problem for direct light but not for light that reaches a point only through a small opening.

**Caustics in a mirror.** Light paths are often classified by the kinds of their vertices, as strings like $L D S E$: from the light $L$, through diffuse $D$ or specular $S$ surfaces, to the eye $E$. A caustic, the bright pattern that a glass sphere throws on a table, is a path $L S S D E$. Seen in a mirror, it is $L S S D S E$. With a point light and a pinhole camera, no method that builds paths by sampling one vertex at a time from the light or from the camera can produce such a path with a positive probability, as Veach (1997) points out; such paths need some smoothing, which adds bias, or other sampling.

## Known algorithms

Unbiased Monte Carlo methods:

- **[Path tracing](/path-tracing/).** Random walks from the camera, with [next event estimation](/next-event-estimation/) and [multiple importance sampling](/multiple-importance-sampling/) in practice. Simple and general; weak for caustics and small openings.
- **[Light tracing](/light-tracing/).** Random walks from the lights, connected to the camera. Good for caustics seen directly.
- **[Bidirectional path tracing](/bidirectional-path-tracing/).** Walks from both ends, connected in all ways and weighted by MIS.
- **[Metropolis light transport](/metropolis-light-transport/).** A Markov chain over paths that stays near paths that carry much light. Good for hard visibility; its error is correlated.
- **[Volumetric path tracing](/volumetric-path-tracing/)** with [delta tracking](/delta-tracking/) for participating media.

Consistent and biased methods:

- **[Photon mapping](/photon-mapping/)** and **[progressive photon mapping](/progressive-photon-mapping/).** Store photons from the lights and estimate the density near each camera path vertex. Biased; the progressive version is consistent. [Vertex connection and merging](/vertex-connection-and-merging/) combines it with bidirectional path tracing.
- **[Radiosity](/radiosity/).** A finite element solution for diffuse scenes.
- **[Instant radiosity](/instant-radiosity/), [irradiance caching](/irradiance-caching/) and [final gathering](/final-gathering/).** Reuse a small set of lights or of cached values over many pixels.
- **Learned and reused sampling.** [Path guiding](/path-guiding/) learns where light comes from, and [ReSTIR](/restir/) reuses light samples between pixels and frames; both can be unbiased or biased, by choice.

Approximations that do not solve the problem but are used in its place: [ambient occlusion](/ambient-occlusion/), constant ambient terms, and [Whitted ray tracing](/whitted-ray-tracing/), which follows only specular paths and direct light.

## Bounds

**No exact algorithm in general.** Reif, Tygar and Yoshida (1990) showed that for some optical systems of reflecting and refracting surfaces, whether a ray ever reaches a given region is undecidable, and PSPACE-hard for some simpler systems. Global illumination includes such questions, so there is no exact general algorithm, and the practical methods are numerical.

**The Monte Carlo rate.** An unbiased estimator with the variance $\sigma^2$ per sample has the root mean square error $\sigma / \sqrt N$ with $N$ independent samples. The rate $N^{-1/2}$ does not depend on the dimension of the integral, which is the reason for using [Monte Carlo integration](/monte-carlo-integration/): a path with $k$ bounces is a point in a space of dimension about $2k$, and product quadrature rules would need a number of points exponential in $k$. [Quasi-Monte Carlo](/quasi-monte-carlo-integration/) points can do better in practice, but the integrands have jumps at the edges of shadows and objects, which weakens its error bounds.

**No bound on the variance.** For any fixed sampling method, the constant $\sigma^2 / I_j^2$ can be made as large as you like by the scene, as the small cap example shows with $1/a - 1$. The speedups of better methods are proved only for particular families, such as the bound of Veach and Guibas on the [balance heuristic](/multiple-importance-sampling/), or measured on test scenes.

**The truncation error.** A method that stops all paths after $k$ bounces has the bias $T^{k+1} L$, at most $\rho_{\max}^{k+1} \lVert L \rVert$ in the supremum norm, where $\rho_{\max} < 1$ is the largest albedo. Russian roulette removes this bias at the cost of variance.

## Reductions

- **To an integral over paths.** The [path integral formulation](/path-integral-formulation/) writes each $I_j$ as one integral over light paths of all lengths, so global illumination is a high-dimensional integration problem, and every Monte Carlo method on paths is a choice of path densities.
- **To a linear system.** In the diffuse case with constant radiance on $n$ patches, it is the system $(I - \rho F) B = E$ of size $n$, which [Gaussian elimination](/gaussian-elimination/) solves in $O(n^3)$ and the [Jacobi method](/jacobi-method/) approximates, because $\rho F$ has row sums below $1$ when every $\rho_i < 1$.
- **To ray queries.** Every method reduces its geometric work to [closest-hit](/closest-hit-query/) and [any-hit](/any-hit-query/) queries, so the speed of [bounding volume hierarchies](/bounding-volume-hierarchy/) sets much of the cost.
- **Direct light as a sub-problem.** The term with one bounce is the direct illumination problem, which many methods solve separately and well.

## Applications

- **Film and animation.** Production renderers are path tracers with many of the methods above.
- **Architecture and lighting design.** Predicting the light in a building before it is built, where the physical values matter.
- **Product images and virtual prototypes.** Images of cars, furniture and devices that must look like the real object.
- **Games and interactive graphics.** Real-time versions with a few rays per pixel, reuse, and denoising.
- **Radiative heat transfer.** The diffuse version, with view factors in place of form factors, is the same balance of energy between surfaces that thermal engineers solve.

## References
