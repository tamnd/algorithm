---
tag: JWYC5Y
kind: concept
slug: rendering-equation
name: Rendering equation
aliases:
- light transport equation
area: graphics-and-signals/ray-tracing
level: core
summary: The integral equation of light at surfaces. Outgoing radiance equals emitted radiance plus the integral of the BRDF times incoming radiance times the cosine.
prereqs: [brdf, neumann-series]
see_also: [global-illumination, path-integral-formulation, path-tracing, radiosity, helmholtz-reciprocity, albedo, participating-media, closest-hit-query]
sources:
  - paper: doi:10.1145/15886.15902
    title: James T. Kajiya, The rendering equation, Computer Graphics (SIGGRAPH 86) 20(4), 1986, 143 to 150
    locator: the equation in its two-point form with the geometry term, the emission and the scattering terms, and its solution by the Neumann series
  - paper: doi:10.1145/15886.15901
    title: David S. Immel, Michael F. Cohen and Donald P. Greenberg, A radiosity method for non-diffuse environments, Computer Graphics (SIGGRAPH 86) 20(4), 1986, 133 to 142
    locator: an equivalent balance of light between patches over discretized directions, for surfaces that are not Lambertian
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 3, Radiometry and Light Transport, and Chapter 4, A General Operator Formulation of Light Transport
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 14.4, The Light Transport Equation (the hemispherical form, the analytic solution for a closed enclosure, and the surface form)
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, A K Peters, 2006
    locator: the chapter on the physics of light transport (radiance, the BRDF and the rendering equation)
---

The rendering equation says how much light leaves each point of a scene in each direction, once the light has settled: the light a point emits, plus the light it reflects, where the reflected light is the light that arrives from every other point, which is in turn given by the same equation. In the form this page uses, for a point $x$ with the normal $n$ and a direction $\omega_o$,

$$L_o(x, \omega_o) = L_e(x, \omega_o) + \int_{\Omega} f_r(x, \omega_i, \omega_o)\, L_i(x, \omega_i) \cos\theta_i \, d\omega_i,$$

where $\Omega$ is the hemisphere around $n$, $f_r$ is the [BRDF](/brdf/), $\theta_i$ is the angle between $\omega_i$ and $n$, and the incoming radiance $L_i(x, \omega_i) = L_o(r(x, \omega_i), -\omega_i)$ is the outgoing radiance of the first surface point $r(x, \omega_i)$ that a ray from $x$ in the direction $\omega_i$ meets. The unknown $L_o$ appears on both sides, so this is an integral equation: a Fredholm equation of the second kind. Kajiya (1986) named it and wrote it in a different but equal form, with two points and a geometry term; Immel, Cohen and Greenberg gave an equal balance the same year. Every physically based renderer estimates its solution, which is the [global illumination](/global-illumination/) problem.

## In plain words

Light leaves a lamp, hits a wall, bounces to the floor, bounces to the ceiling, and so on. Each surface you look at sends you two kinds of light. It may glow by itself, like a lamp. And it sends back some of the light that falls on it from everything else around it.

The rendering equation writes this down for every point and every direction at once. The light leaving a point is its own glow plus a sum over all directions above it: the light coming in from that direction, times how much of it the surface sends your way, times how directly it falls on the surface.

The catch is that the light coming in is the light leaving some other point, which is what you are trying to find. So the equation refers to itself, and solving it means following light through bounce after bounce.

## The idea

**The terms.** Radiance $L(x, \omega)$ is the power per unit area and per unit solid angle at $x$ in the direction $\omega$; it stays the same along a ray in empty space, which is why $L_i(x, \omega_i)$ is just $L_o$ at the other end of the ray. The emitted radiance $L_e$ is given. The BRDF $f_r(x, \omega_i, \omega_o)$ is the ratio of the radiance reflected toward $\omega_o$ to the irradiance from $\omega_i$. The factor $\cos\theta_i$ turns radiance into irradiance: light that falls at a slant spreads over more area. The function $r$ is the [closest-hit query](/closest-hit-query/) of a ray tracer. For a refracting surface, the integral runs over the whole sphere and $f_r$ becomes the BSDF.

**The surface form.** Change the variable from the direction $\omega_i$ to the point $x'' = r(x', \omega_i)$ that it hits, with $d\omega_i = \cos\theta''\, dA(x'') / \lVert x' - x'' \rVert^2$. Write $L(x' \to x)$ for the radiance from $x'$ toward $x$. Then

$$L(x' \to x) = L_e(x' \to x) + \int_M f(x'' \to x' \to x)\, L(x'' \to x')\, G(x'' \leftrightarrow x')\, dA(x''),$$

where $M$ is the set of all surfaces and the geometry term is $G(x'' \leftrightarrow x') = V(x'', x') \cos\theta'' \cos\theta' / \lVert x'' - x' \rVert^2$, with the visibility $V \in \{0, 1\}$. Kajiya wrote the equation in this two-point form, as $I(x, x') = g(x, x') [\epsilon(x, x') + \int_S \rho(x, x', x'') I(x', x'')\, dx'']$, where his $g$ holds the visibility and the inverse square of the distance, $\epsilon$ is the emission and $\rho$ is the scattering term, with the cosines inside it. The two forms are the same equation; the hemispherical form suits renderers that trace rays from a point, and the surface form suits methods that connect points, such as [bidirectional path tracing](/bidirectional-path-tracing/), and leads to the [path integral formulation](/path-integral-formulation/).

**An operator equation.** Write the integral as an operator $T$, so that $(TL)(x, \omega_o) = \int_\Omega f_r\, L(r(x, \omega_i), -\omega_i) \cos\theta_i \, d\omega_i$. The equation is

$$L = L_e + T L.$$

This is a Fredholm integral equation of the second kind: the unknown appears once outside the integral and once inside, with the kernel $f_r \cos\theta_i$ composed with the ray casting. If $T$ has the norm $\lVert T \rVert < 1$, the solution is unique and it is the [Neumann series](/neumann-series/)

$$L = (I - T)^{-1} L_e = L_e + T L_e + T^2 L_e + \cdots.$$

The term $T^k L_e$ is the light that has bounced exactly $k$ times. In the supremum norm, $\lVert T \rVert \le \sup_{x, \omega_o} \int_\Omega f_r(x, \omega_i, \omega_o) \cos\theta_i \, d\omega_i$, the largest directional [albedo](/albedo/) in the scene, so the series converges when every albedo is below $1$. The error of the sum up to $T^k L_e$ is $T^{k+1} L$, at most $\lVert T \rVert^{k+1} \lVert L \rVert$. Physical BRDFs have albedo at most $1$ by the conservation of energy, and they obey [Helmholtz reciprocity](/helmholtz-reciprocity/), $f_r(x, \omega_i, \omega_o) = f_r(x, \omega_o, \omega_i)$.

**What a pixel measures.** A camera measures $I_j = \int W_j(x, \omega) L_i(x, \omega) \cos\theta \, dA\, d\omega$ over its sensor, where $W_j$ is the response of pixel $j$. So the renderer needs only some weighted integrals of $L$, not all of $L$, which is what Monte Carlo methods use.

**What it leaves out.** The equation assumes geometric optics, a steady state and light that moves only between surfaces. Light that scatters inside smoke, fog or skin follows the radiative transfer equation of [participating media](/participating-media/). Each wavelength is solved on its own, so fluorescence, which moves light between wavelengths, needs a coupled version, and polarization needs a vector version.

**The Lambertian case.** If every surface is Lambertian, $f_r = \rho / \pi$, and the radiance is constant on each of $n$ patches, the equation becomes the linear system $B_i = E_i + \rho_i \sum_j F_{ij} B_j$ of [radiosity](/radiosity/), where $F_{ij}$ is the form factor, the share of the cosine-weighted hemisphere of patch $i$ that patch $j$ covers.

## Examples

**The furnace.** A closed sphere, inside which every point emits the radiance $L_e$ and has the Lambertian albedo $\rho < 1$. By symmetry $L$ is the same constant everywhere, the integral is $\rho L$, and the equation is $L = L_e + \rho L$, so $L = L_e / (1 - \rho)$. The Neumann series is the geometric series $L_e (1 + \rho + \rho^2 + \cdots)$. The sum up to $k$ bounces has the relative error $\rho^{k+1}$, so for an error of 1 percent it needs $k = 6$ bounces for $\rho = 0.5$, $k = 43$ for $\rho = 0.9$ and $k = 458$ for $\rho = 0.99$. A white room needs many bounces. For $\rho = 1$ and $L_e > 0$ there is no finite solution, and for $\rho = 1$ and $L_e = 0$ every constant is a solution, so the condition $\rho < 1$ is needed.

**A sphere in zones, solved exactly.** For two points $x, x'$ on the inside of a sphere of radius $R$, both cosines equal $\lVert x - x' \rVert / (2R)$, so $G = 1 / (4R^2)$ for every pair: each point sees every piece of the sphere in proportion to its area. Cut the unit sphere by the planes $z = -\tfrac12, 0, \tfrac12$ into four zones. By Archimedes' theorem, each zone has a quarter of the area. Give the zones, from the bottom, the emitted radiance $E = (0, 0, 0, 4)$ and the Lambertian albedo $\rho = (\tfrac12, \tfrac14, \tfrac34, \tfrac12)$. Then the radiance is constant on each zone, and the equation becomes the linear system $L_i = E_i + \rho_i \cdot \tfrac14 \sum_j L_j$. Gaussian elimination with exact fractions gives $L = (1, \tfrac12, \tfrac32, 5)$. The Neumann series gives the same values one bounce at a time:

| bounces $k$ | zone 1 | zone 2 | zone 3 | zone 4 |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 4 |
| 1 | 0.5 | 0.25 | 0.75 | 4.5 |
| 2 | 0.75 | 0.375 | 1.125 | 4.75 |
| 3 | 0.875 | 0.4375 | 1.3125 | 4.875 |
| 6 | 0.984 | 0.492 | 1.477 | 4.984 |
| exact | 1 | 0.5 | 1.5 | 5 |

Here the mean albedo is $\tfrac12$, so each bounce adds half of what the one before added, and the error halves at each step. The bound $\lVert T \rVert^{k+1} \lVert L \rVert = (\tfrac34)^{k+1} \cdot 5$, from the largest albedo, is true but loose: after two bounces it gives $2.11$, and the true largest error is $0.375$. The row for $k = 1$ is the direct light only, which leaves the three dark zones at half of their true brightness. The tests of [path tracing](/path-tracing/) and of its relatives use zoned spheres like this one as their exact reference.

**An open scene.** A floor with albedo $\rho$ under a sky of constant radiance $L_s$, with nothing else. A ray up from the floor always meets the sky, and the sky does not reflect, so the series stops after one term: $L_{\text{floor}} = \rho L_s$. In an open scene, most paths leave quickly, and $\lVert T^k L_e \rVert$ falls faster than the albedo alone says.

## Where it is used

- **Monte Carlo renderers.** [Path tracing](/path-tracing/) estimates the Neumann series by random walks. [Russian roulette](/russian-roulette/) ends the walks without bias, [next event estimation](/next-event-estimation/) samples the emission term directly, and [multiple importance sampling](/multiple-importance-sampling/) combines ways to sample the integral.
- **Methods built on the surface form.** [Light tracing](/light-tracing/), [bidirectional path tracing](/bidirectional-path-tracing/) and [Metropolis light transport](/metropolis-light-transport/) work with the [path integral formulation](/path-integral-formulation/), which expands the series into one integral over paths.
- **Finite element methods.** [Radiosity](/radiosity/) solves the Lambertian case as a linear system with Jacobi or Gauss-Seidel iterations, which are the Neumann series and a faster cousin of it.
- **Caching and density estimation.** [Photon mapping](/photon-mapping/), [irradiance caching](/irradiance-caching/) and [instant radiosity](/instant-radiosity/) approximate parts of the integral to save work, with some bias.
- **Approximations.** [Ambient occlusion](/ambient-occlusion/) and the ambient term of local shading models replace the integral by a constant, and are exact only in special cases.

## References
