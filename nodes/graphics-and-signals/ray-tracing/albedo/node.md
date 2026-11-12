---
tag: 71ACF7
kind: concept
slug: albedo
name: Albedo
aliases:
- reflectance
- directional albedo
- single-scattering albedo
area: graphics-and-signals/ray-tracing
level: intro
summary: The fraction of the incident light that a surface reflects in total, over all outgoing directions. It is the integral of the BRDF times the cosine, and it lies between 0 and 1.
prereqs: [brdf]
see_also: [lambertian-reflectance, microfacet-brdf, fresnel-equations, rendering-equation, russian-roulette, participating-media, bssrdf, neumann-series]
sources:
  - paper: doi:10.6028/NBS.MONO.160
    title: Fred E. Nicodemus, Joseph C. Richmond, Jack J. Hsia, Irving W. Ginsberg and Thomas Limperis, Geometrical considerations and nomenclature for reflectance, NBS Monograph 160, National Bureau of Standards, 1977
    locator: the directional-hemispherical and bihemispherical reflectances as integrals of the BRDF
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Section 6.3 (Theorem 6.2, the bound on the integral of the BSDF, which is the albedo bound)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.1.1, Reflectance (the hemispherical-directional and hemispherical-hemispherical reflectances), and Section 11.1 for the single-scattering albedo of a medium
  - paper: doi:10.1145/383259.383319
    title: Henrik Wann Jensen, Stephen R. Marschner, Marc Levoy and Pat Hanrahan, A practical model for subsurface light transport, SIGGRAPH 2001, 511 to 518
    locator: the reduced scattering albedo and the total diffuse reflectance of the dipole model as a function of it
---

The albedo of a surface is the fraction of the light that falls on it that it reflects, summed over all directions in which it leaves. A black velvet has an albedo near 0, fresh snow near 1. In rendering the word has a precise form: the directional albedo $\rho(\omega_i)$ is the integral of the [BRDF](/brdf/) times the cosine over the outgoing hemisphere, for light from one direction. For a [Lambertian](/lambertian-reflectance/) surface it is the constant $\rho$ of the BRDF $\rho/\pi$; for glossy surfaces it depends on the direction. The same word names a second quantity in volumes: the single-scattering albedo of a [participating medium](/participating-media/) is the probability that a collision scatters the light and does not absorb it. Every albedo below 1 means that light loses energy at each bounce, which is what makes the light transport equations converge.

## In plain words

Shine a flashlight on a wall. Some light comes back from the wall into the room, and the rest turns into heat in the paint. The albedo is the share that comes back, counted in all directions together. It does not say where the light goes, only how much of it.

A white wall sends back most of the light, a dark road little. A mirror sends back almost all of it, but into one direction only.

The albedo can depend on where the light comes from. Glass sends back little light that hits it straight on and much more that hits it at a shallow angle.

In smoke, fog or milk, light hits tiny particles. Each time, the particle either sends the light on in a new direction or swallows it. The albedo of the medium is the chance that it sends it on.

## The idea

**Directional albedo.** For a surface with the BRDF $f_r$ and light from the direction $\omega_i$, the directional-hemispherical reflectance is

$$\rho(\omega_i) = \int_{H^2} f_r(\omega_i, \omega_o) \cos\theta_o \, d\omega_o.$$

It is the ratio of the reflected power to the incident power for a narrow beam from $\omega_i$. By [Helmholtz reciprocity](/helmholtz-reciprocity/) it is also the hemispherical-directional reflectance $\int f_r(\omega_i, \omega_o) \cos\theta_i\,d\omega_i$ with the roles of the two directions swapped: the radiance that a surface under a uniform white sky of radiance 1 sends toward $\omega_o$. Energy conservation is $\rho(\omega) \le 1$ for every $\omega$.

**Hemispherical albedo.** The average over a uniform incident radiance, the bihemispherical reflectance, is

$$\bar\rho = \frac{1}{\pi} \int_{H^2} \rho(\omega_i) \cos\theta_i \, d\omega_i = 2 \int_0^1 \rho(\mu)\,\mu\,d\mu$$

for an isotropic surface, with $\mu = \cos\theta_i$. It is the fraction of the light of a diffuse sky that the surface reflects. Remote sensing calls it the white-sky albedo.

**Albedo and base color.** Texture maps in real-time engines are often called albedo maps. They store the parameter $\rho$ of the diffuse part, or a base color from which the engine derives the diffuse $\rho$ and the specular $R_0$. The real albedo of such a material is the sum of the diffuse part, weighted by the light that the specular layer lets through, and the specular part, and it varies with the angle.

**Why albedo bounds the transport.** The [rendering equation](/rendering-equation/) is $L = L_e + K L$, where the operator $K$ applies one bounce. If every directional albedo in the scene is at most $\rho_{\max} < 1$, then $K$ has the norm at most $\rho_{\max}$ in the sup norm on radiance, the [Neumann series](/neumann-series/) $L = \sum_k K^k L_e$ converges, and the energy that reaches bounce $k$ is at most $\rho_{\max}^k$ times the emitted energy. A path tracer can stop paths with [Russian roulette](/russian-roulette/) at a probability that follows the albedo, so that dark surfaces end paths early and bright ones keep them alive.

**Single-scattering albedo.** In a medium with the absorption coefficient $\sigma_a$ and the scattering coefficient $\sigma_s$, the extinction coefficient is $\sigma_t = \sigma_a + \sigma_s$ and the single-scattering albedo is

$$\alpha = \frac{\sigma_s}{\sigma_t}.$$

At each collision a photon scatters with the probability $\alpha$, so in an unbounded medium it scatters $\alpha / (1 - \alpha)$ times on average before it is absorbed: once for $\alpha = 0.5$, 99 times for $\alpha = 0.99$. Clouds and milk have $\alpha$ very close to 1, which is why they look white although each particle absorbs a little. [Volumetric path tracing](/volumetric-path-tracing/) uses $\alpha$ as the weight or as the probability of a scattering event. In subsurface scattering the reduced albedo $\alpha' = \sigma_s' / (\sigma_a + \sigma_s')$, with $\sigma_s' = (1 - g)\sigma_s$ for the mean cosine $g$ of the phase function, decides the total diffuse reflectance of the material: in the dipole model of Jensen et al. (2001) it is $\tfrac{\alpha'}{2}\big(1 + e^{-\frac43 A \sqrt{3(1 - \alpha')}}\big)\,e^{-\sqrt{3(1 - \alpha')}}$, see [BSSRDF](/bssrdf/).

**Other meanings.** In astronomy the Bond albedo of a planet is the fraction of all sunlight it reflects, and the geometric albedo compares its brightness at zero phase angle to that of a flat Lambertian disk. These are integrals of the same kind over a whole body. The alias "reflectance" is broader than albedo: in radiometry a reflectance is any ratio of reflected to incident flux for given incident and reflected geometries, of which the albedo is the one with the whole outgoing hemisphere.

## Examples

**Lambertian surface.** For $f_r = \rho/\pi$, $\rho(\omega_i) = \frac{\rho}{\pi} \int \cos\theta_o\,d\omega_o = \rho$ for every $\omega_i$, and $\bar\rho = \rho$. Common values are about 0.04 for black paint, 0.18 for the gray card of photography, and 0.8 to 0.9 for white paper and fresh snow.

**Smooth glass.** A smooth dielectric reflects only in the mirror direction, with the Fresnel reflectance, so $\rho(\omega_i) = R(\theta_i)$. For glass of index 1.5 seen from air this is 0.040 at normal incidence, 0.050 at $45°$, 0.089 at $60°$, 0.388 at $80°$ and 1 at grazing incidence ([Fresnel equations](/fresnel-equations/)). The hemispherical albedo is $\bar\rho = 2\int_0^1 R(\mu)\mu\,d\mu = 0.092$. For light inside the glass that meets the surface from all directions it is 0.596, because every direction beyond the critical angle of $41.8°$ is reflected in full. The same integral gives 0.066 and 0.475 for water of index 1.333.

**Rough metal.** A [microfacet BRDF](/microfacet-brdf/) with the Fresnel term set to 1, a perfect reflector at the scale of each facet, has with the GGX distribution and the roughness $\alpha = 0.5$ the directional albedo 0.688 at normal incidence and 0.805 at $80°$; with $\alpha = 1$ it falls to $1 - \ln 2 = 0.307$ at normal incidence. The missing energy is the light that would bounce more than once between the facets, which the single-scattering model drops. Such a surface looks darker when it is rougher, which a real metal does not.

**Interreflection.** In a closed room of Lambertian walls with albedo 0.8 that emit the radiance $L_e$ uniformly, each point sees only walls, so $L = L_e + 0.8 L$ and $L = 5 L_e$: four fifths of the light come from bounces. With albedo 0.5 the factor is 2.

**A translucent material.** With $\sigma_a = 0.01$ and $\sigma_s' = 1$ per millimeter and the index 1.3, made-up values of the order of a milky material, $\alpha' = 0.990$ and the dipole model gives a total diffuse reflectance of 0.646. With $\alpha' = 0.9$ it is 0.299 and with $\alpha' = 0.5$ only 0.075. A small amount of absorption removes much light, because the light travels a long way inside before it gets out.

## Where it is used

- [Lambertian reflectance](/lambertian-reflectance/) has the albedo as its only parameter, and the [microfacet BRDF](/microfacet-brdf/) is tested against the bound $\rho \le 1$.
- The furnace test of a renderer puts an object of known albedo under a uniform sky and checks that its radiance is the albedo times the sky.
- [Russian roulette](/russian-roulette/) and the throughput weights of [path tracing](/path-tracing/) use the albedo of the sampled BSDF.
- [Radiosity](/radiosity/) uses one albedo per patch as the reflectance of its linear system.
- [Participating media](/participating-media/) and [volumetric path tracing](/volumetric-path-tracing/) use the single-scattering albedo, and [BSSRDF](/bssrdf/) models express their total reflectance through the reduced albedo.
- The convergence of the [rendering equation](/rendering-equation/) by the [Neumann series](/neumann-series/) rests on albedos below 1.

## References
