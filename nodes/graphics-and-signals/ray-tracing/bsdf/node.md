---
tag: QTX7EG
kind: definition
slug: bsdf
name: Bidirectional scattering distribution function
aliases:
- BSDF
- BTDF
- bidirectional transmittance distribution function
area: graphics-and-signals/ray-tracing
level: core
summary: The BRDF extended to the whole sphere of directions, so that a surface can also transmit light. Its transmission part, the BTDF, is not symmetric, since radiance scales with the squared index ratio.
prereqs: [brdf, snells-law]
see_also: [fresnel-equations, microfacet-brdf, helmholtz-reciprocity, bssrdf, albedo, path-tracing, bidirectional-path-tracing, photon-mapping]
sources:
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 3 (the BSDF with respect to the projected solid angle and the scattering equation), Chapter 5 (Section 5.2, non-symmetry due to refraction, and Section 5.3, shading normals) and Section 6.2 (Theorem 6.1, the reciprocity of the BSDF with the factor η²)
  - paper: doi:10.2312/EGWR/EGSR07/195-206
    title: Bruce Walter, Stephen R. Marschner, Hongsong Li and Kenneth E. Torrance, Microfacet models for refraction through rough surfaces, Eurographics Symposium on Rendering, 2007, 195 to 206
    locator: the BSDF as the sum of a BRDF and a BTDF, the generalized half vector of refraction, and the microfacet BTDF with its Jacobian
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.1, Basic Interface (BxDFs), and Section 8.2, Specular Reflection and Transmission (the radiance scaling by the squared ratio of the indices)
---

The bidirectional scattering distribution function, or BSDF, of a surface gives, for light that arrives from one direction, the radiance that leaves in another direction per unit of irradiance, for all pairs of directions on the whole sphere. When both directions are on the same side of the surface it is the [BRDF](/brdf/); when they are on opposite sides it is the bidirectional transmittance distribution function, the BTDF. Glass, water, leaves and thin cloth need the BTDF. The BSDF is the kernel that [path tracing](/path-tracing/) samples at each vertex of a path. Unlike the BRDF, the BTDF is not symmetric in its two directions: radiance that crosses into a denser medium is concentrated into a smaller cone and grows by the square of the ratio of the refractive indices, a fact that [bidirectional](/bidirectional-path-tracing/) methods must respect.

## Definition

Let $x$ be a point of a surface with the unit normal $n$, and let $S^2$ be the sphere of all directions. Directions point away from $x$: $\omega_i$ toward the source of the light and $\omega_o$ toward its destination. The BSDF is the function $f_s(\omega_i \to \omega_o)$ with

$$f_s(\omega_i \to \omega_o) = \frac{dL_o(\omega_o)}{L_i(\omega_i)\,|\cos\theta_i|\,d\omega_i}, \qquad \omega_i, \omega_o \in S^2,$$

where $\theta$ is the angle to $n$. The arrow shows the direction in which light flows, from $\omega_i$ to $\omega_o$; it matters because $f_s$ is not symmetric in general. The scattering equation sums over all incident directions:

$$L_o(\omega_o) = \int_{S^2} f_s(\omega_i \to \omega_o)\,L_i(\omega_i)\,|\cos\theta_i|\,d\omega_i.$$

Veach (1997) writes $d\sigma^\perp(\omega) = |\cos\theta|\,d\omega$ for the projected solid angle, so that the equation is $L_o = \int f_s L_i \, d\sigma^\perp$.

The BSDF splits into two parts. If $(n \cdot \omega_i)(n \cdot \omega_o) > 0$, the directions are on the same side and $f_s = f_r$, the BRDF of that side; a surface has one BRDF for each side. If $(n \cdot \omega_i)(n \cdot \omega_o) < 0$, $f_s = f_t$, the BTDF. Let $\eta_i$ and $\eta_o$ be the refractive indices on the sides of $\omega_i$ and $\omega_o$. A physically plausible BSDF has three properties:

1. **Positivity.** $f_s \ge 0$.
2. **Generalized reciprocity.** For a surface between media that do not absorb, and without external magnetic fields,
$$\frac{f_s(\omega_i \to \omega_o)}{\eta_o^2} = \frac{f_s(\omega_o \to \omega_i)}{\eta_i^2}$$
(Veach 1997, Theorem 6.1). For the BRDF part $\eta_i = \eta_o$ and this is ordinary symmetry. For the BTDF part the two orders differ by the factor $\eta_o^2 / \eta_i^2$. The page on [Helmholtz reciprocity](/helmholtz-reciprocity/) gives the proof.
3. **Energy conservation.** For every $\omega_i$, $\int_{S^2} f_s(\omega_i \to \omega_o)\,|\cos\theta_o|\,d\omega_o \le 1$ (Veach 1997, Theorem 6.2). The integral is over the outgoing direction: the reflected and transmitted power is at most the incident power. The integral over the incident direction, at a fixed $\omega_o$, can exceed 1 for transmission into a denser medium, because the radiance grows.

**Radiance and importance.** Light transport carries radiance with $f_s(\omega_i \to \omega_o)$. Transport of importance from the camera, as in light tracing and [photon mapping](/photon-mapping/), uses the adjoint BSDF $f_s^*(\omega_i \to \omega_o) = f_s(\omega_o \to \omega_i)$. For a symmetric BRDF the two are the same; for a BTDF they differ by $\eta^2$, and a method that uses the same function in both directions gets the wrong brightness behind glass.

## Examples and non-examples

**A smooth dielectric.** A flat boundary between air ($\eta = 1$) and glass ($\eta = 1.5$) reflects the [Fresnel](/fresnel-equations/) fraction $F(\theta_i)$ into the mirror direction and transmits $1 - F$ into the direction $T(\omega_i)$ of [Snell's law](/snells-law/). In the projected solid angle measure, the étendue $\eta^2\,d\sigma^\perp$ is the same on both sides of the boundary, so the beam of transmitted power fills a cone of projected solid angle smaller by $\eta_i^2 / \eta_o^2$, and the radiance grows by $\eta_o^2 / \eta_i^2$:

$$L_o(\omega_o) = \frac{\eta_o^2}{\eta_i^2}\,(1 - F)\,L_i(\omega_i), \qquad \omega_o = T(\omega_i).$$

Light that enters glass at normal incidence has the radiance $2.25 \cdot 0.96 = 2.16$ times the radiance of the incident light. When it leaves through the far face of a slab, the factor $1/2.25$ undoes the gain, and the slab passes $0.96 \cdot 0.96 = 0.9216$ of the radiance on the first pass. With all internal reflections summed, the slab transmits $(1 - R)^2 / (1 - R^2) = (1 - R)/(1 + R) = 0.96 / 1.04 = 0.923$ of the light, for $R = 0.04$ at both faces. The BSDF of the boundary is a sum of two deltas, one per lobe, and its reciprocity holds once the Jacobian of the delta is included: for the refraction delta, $d\sigma^\perp(\omega_o) / d\sigma^\perp(\omega_i) = \eta_i^2 / \eta_o^2$.

**Rough glass.** Walter et al. (2007) give the microfacet BTDF. With the generalized half vector $h = -(\eta_i \omega_i + \eta_o \omega_o) / |\eta_i \omega_i + \eta_o \omega_o|$, which is the facet normal that refracts $\omega_i$ into $\omega_o$,

$$f_t(\omega_i \to \omega_o) = \frac{|\omega_i \cdot h|\,|\omega_o \cdot h|}{|\omega_i \cdot n|\,|\omega_o \cdot n|} \cdot \frac{\eta_o^2\,(1 - F(\omega_i \cdot h))\,D(h)\,G(\omega_i, \omega_o, h)}{(\eta_i\,(\omega_i \cdot h) + \eta_o\,(\omega_o \cdot h))^2},$$

with $D$ and $G$ of the [microfacet BRDF](/microfacet-brdf/). The factor $\eta_o^2$ in the numerator is the radiance gain of property 2.

**A thin sheet.** Paper, leaves and lamp shades are thin enough that light leaves on the other side near the point where it entered. A diffuse transmitter $f_t = \tau / \pi$ for opposite sides, with a diffuse reflector $f_r = \rho / \pi$ and $\rho + \tau \le 1$, is a simple BSDF for them; with the same medium on both sides it is symmetric.

**Non-example: shading normals.** A renderer that bends the normal for bump mapping or interpolated normals evaluates the BSDF with a normal that differs from the true one. The result is not symmetric, and its integral can exceed 1. Veach (1997, Section 5.3) shows how to correct the adjoint BSDF for this.

**Non-example: subsurface scattering.** In skin or marble, light leaves at a point other than the point where it entered. The BSDF relates directions at one point, so it cannot describe this; the [BSSRDF](/bssrdf/) can.

**Non-example: a phase function.** Inside a [participating medium](/participating-media/), a phase function gives the distribution of the scattered direction at a point of the volume. It plays the role of the BSDF but has no surface, no normal and no cosine, and it integrates to 1 over the sphere.

## Related definitions

- [BRDF](/brdf/): the reflection part of the BSDF.
- [BSSRDF](/bssrdf/): the BSDF extended to light that leaves at another point.
- [Albedo](/albedo/): the integral of the BSDF times the cosine; for a BSDF it splits into a reflected and a transmitted part.
- [Helmholtz reciprocity](/helmholtz-reciprocity/): property 2 and its proof.
- [Snell's law](/snells-law/) and the [Fresnel equations](/fresnel-equations/): the direction and the weight of the lobes of a smooth boundary.
- [Microfacet BRDF](/microfacet-brdf/): the rough reflection model, which Walter et al. extended to the BTDF above.
- [Participating media](/participating-media/): the phase function, the analog of the BSDF in a volume.

### History

The BTDF and the BSDF extend the BRDF of Nicodemus (1965, 1977) to transmission. In graphics, Whitted (1980) traced a transmitted ray in the Snell direction with a constant weight. The asymmetry of the BSDF under refraction and the adjoint BSDF for importance transport were worked out by Veach in his thesis of 1997, together with the generalized reciprocity relation. Walter et al. (2007) gave the microfacet BTDF that renderers use for rough glass.

## References
