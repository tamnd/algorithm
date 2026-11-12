---
tag: M37D8N
kind: definition
slug: bssrdf
name: Bidirectional scattering-surface reflectance distribution function
aliases:
- BSSRDF
- subsurface scattering function
area: graphics-and-signals/ray-tracing
level: advanced
summary: The function S(xi, ωi; xo, ωo) that gives the radiance leaving a surface at xo per unit of flux entering at xi. It describes skin, marble and milk, where light exits at another point.
prereqs: [bsdf]
see_also: [brdf, albedo, participating-media, volumetric-path-tracing, fresnel-equations, lambertian-reflectance, path-tracing, monte-carlo-integration]
sources:
  - paper: doi:10.6028/NBS.MONO.160
    title: Fred E. Nicodemus, Joseph C. Richmond, Jack J. Hsia, Irving W. Ginsberg and Thomas Limperis, Geometrical considerations and nomenclature for reflectance, NBS Monograph 160, National Bureau of Standards, 1977
    locator: the bidirectional scattering-surface reflectance distribution function, and the BRDF as its special case for a uniform surface with no lateral transport
  - paper: doi:10.1145/383259.383319
    title: Henrik Wann Jensen, Stephen R. Marschner, Marc Levoy and Pat Hanrahan, A practical model for subsurface light transport, SIGGRAPH 2001, 511 to 518
    locator: the BSSRDF in the rendering equation, the dipole diffusion term Rd(r), the diffuse BSSRDF with the two Fresnel transmission factors, the single-scattering term, and the total diffuse reflectance
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 5.6.2, The BSSRDF, and Chapters 11 and 15 for volume scattering and the sampling of subsurface reflection
---

The bidirectional scattering-surface reflectance distribution function, or BSSRDF, describes surfaces into which light enters at one point and from which it leaves at another. It is a function $S(x_i, \omega_i; x_o, \omega_o)$ of two points and two directions: for light that enters at $x_i$ from $\omega_i$, it gives the radiance that leaves at $x_o$ toward $\omega_o$, per unit of the incident flux. Skin, marble, milk, wax, leaves and many plastics scatter light below their surface over distances of millimeters. A [BRDF](/brdf/) puts all of that light back at the point of entry, which gives these materials a hard, dry look; the BSSRDF lets light bleed across edges and into shadows, which gives them their soft, translucent look. Nicodemus et al. defined it in 1977. Jensen et al. (2001) made it practical in rendering with a closed form from the diffusion theory of [participating media](/participating-media/).

## Definition

Let $A$ be the surface of an object, with the unit normal $n(x)$ at each point $x$. Light of radiance $L_i(x_i, \omega_i)$ that arrives at $x_i$ from a small solid angle $d\omega_i$ around $\omega_i$, through a small area $dA(x_i)$, carries the flux $d\Phi_i(x_i, \omega_i) = L_i(x_i, \omega_i) \cos\theta_i \, d\omega_i \, dA(x_i)$. The BSSRDF is the ratio

$$S(x_i, \omega_i; x_o, \omega_o) = \frac{dL_o(x_o, \omega_o)}{d\Phi_i(x_i, \omega_i)}.$$

Its unit is $\mathrm{m}^{-2}\,\mathrm{sr}^{-1}$: one inverse area more than the BRDF. Summed over all points and incident directions, this gives the scattering equation

$$L_o(x_o, \omega_o) = \int_A \int_{H^2(x_i)} S(x_i, \omega_i; x_o, \omega_o)\, L_i(x_i, \omega_i) \cos\theta_i \, d\omega_i \, dA(x_i).$$

A physically plausible BSSRDF has the analogs of the properties of a BRDF:

1. **Positivity.** $S \ge 0$.
2. **Reciprocity.** For an object in one medium, without magnetic fields, $S(x_i, \omega_i; x_o, \omega_o) = S(x_o, \omega_o; x_i, \omega_i)$. The [Helmholtz reciprocity](/helmholtz-reciprocity/) of the light paths inside the material gives it.
3. **Energy conservation.** For every $x_i$ and $\omega_i$, $\int_A \int_{H^2(x_o)} S(x_i, \omega_i; x_o, \omega_o) \cos\theta_o \, d\omega_o \, dA(x_o) \le 1$. The left side is the [albedo](/albedo/) of the object for light that enters at $x_i$.

**The BRDF as a special case.** If no light moves sideways, $S(x_i, \omega_i; x_o, \omega_o) = f_r(\omega_i, \omega_o)\,\delta(x_o - x_i)$ with the Dirac delta on the surface, and the scattering equation turns into the reflection equation of the BRDF. Nicodemus et al. (1977) define the BRDF in this way, for a surface that is uniform and lit uniformly over an area large compared to the distance that light travels inside.

**The dipole BSSRDF.** Jensen et al. (2001) split $S = S^{(1)} + S_d$ into a single-scattering term $S^{(1)}$, for light that scatters once below the surface, and a diffuse term $S_d$ for light that scatters many times. For a flat, semi-infinite, homogeneous medium of index $\eta$, with the absorption coefficient $\sigma_a$, the reduced scattering coefficient $\sigma_s' = (1 - g)\sigma_s$ and the reduced extinction coefficient $\sigma_t' = \sigma_a + \sigma_s'$, the diffuse term is

$$S_d(x_i, \omega_i; x_o, \omega_o) = \frac{1}{\pi}\, F_t(\eta, \omega_i)\, R_d(\lVert x_i - x_o \rVert)\, F_t(\eta, \omega_o),$$

where $F_t = 1 - F$ is the [Fresnel](/fresnel-equations/) transmittance at each crossing of the surface and $R_d(r)$ is the diffuse reflectance profile. The diffusion approximation replaces the source below $x_i$ by a positive point source at the depth $z_r = 1/\sigma_t'$ and a negative mirror source at the height $z_v = z_r (1 + \tfrac43 A)$ above the surface, chosen so that the fluence meets the boundary condition. With $r$ the distance on the surface, $d_r = \sqrt{r^2 + z_r^2}$, $d_v = \sqrt{r^2 + z_v^2}$, the effective transport coefficient $\sigma_{tr} = \sqrt{3 \sigma_a \sigma_t'}$ and the reduced albedo $\alpha' = \sigma_s' / \sigma_t'$,

$$R_d(r) = \frac{\alpha'}{4\pi} \left[ z_r (\sigma_{tr} d_r + 1) \frac{e^{-\sigma_{tr} d_r}}{d_r^3} + z_v (\sigma_{tr} d_v + 1) \frac{e^{-\sigma_{tr} d_v}}{d_v^3} \right].$$

The constant $A = (1 + F_{dr}) / (1 - F_{dr})$ accounts for the light that the surface reflects back inside, and $F_{dr}$ is the internal diffuse Fresnel reflectance, which Jensen et al. fit as $F_{dr} \approx -1.440/\eta^2 + 0.710/\eta + 0.668 + 0.0636\,\eta$. The integral of $R_d$ over the plane has the closed form

$$R_{\mathrm{tot}} = 2\pi \int_0^\infty R_d(r)\, r \, dr = \frac{\alpha'}{2} \left(1 + e^{-\frac43 A \sqrt{3(1 - \alpha')}}\right) e^{-\sqrt{3(1 - \alpha')}},$$

the total diffuse reflectance. The diffuse term is symmetric in its two ends and depends on the two points only through their distance.

## Examples and non-examples

**A translucent material.** Take $\sigma_a = 0.01$ and $\sigma_s' = 1$ per millimeter and $\eta = 1.3$, made-up values of the order of a milky material. Then $\alpha' = 0.990$, $F_{dr} = 0.445$, $A = 2.60$, $z_r = 0.990$ mm, $z_v = 4.43$ mm and $1/\sigma_{tr} = 5.75$ mm. The profile is

| $r$ (mm) | 0 | 1 | 5 | 10 |
|---|---|---|---|---|
| $R_d(r)$ (mm$^{-2}$) | 0.0826 | 0.0303 | 0.00125 | 0.000152 |

and the total diffuse reflectance is $R_{\mathrm{tot}} = 0.646$, with half of it from within $2.18$ mm of the point of entry. A numeric integral of $R_d$ over the plane agrees with the closed form to six digits. Light that enters at the edge of a shadow comes out inside the shadow, across a distance of the order of millimeters, which a BRDF cannot do.

**The effect of absorption.** With the same $A$, the closed form gives $R_{\mathrm{tot}} = 0.864$ for $\alpha' = 0.999$, $0.645$ for $0.99$, $0.299$ for $0.9$ and $0.075$ for $0.5$. A little absorption removes much light, because light that scatters many times travels a long way before it leaves. This is why the [albedo](/albedo/) of a medium must be close to 1 for it to look white.

**The BRDF limit.** If $\sigma_t'$ grows while $\alpha'$ stays fixed, $z_r$, $z_v$ and $1/\sigma_{tr}$ shrink, $R_d$ concentrates at $r = 0$, and $S_d$ approaches $\frac{1}{\pi} F_t(\omega_i)\, R_{\mathrm{tot}}\, F_t(\omega_o)\,\delta(x_o - x_i)$. That is a BRDF with a nearly [Lambertian](/lambertian-reflectance/) shape, darkened toward grazing angles by the two Fresnel factors. Dense white paint behaves like this: it scatters below the surface, but over a distance smaller than a pixel.

**Non-example: a BSDF.** A [BSDF](/bsdf/) relates two directions at one point. A thin sheet with a BTDF transmits light to the other side at the same point; it does not move light sideways. Rough glass needs a BSDF, not a BSSRDF.

**Non-example: a volume.** In a [participating medium](/participating-media/) such as fog, light scatters at points of the volume, not of a surface, and [volumetric path tracing](/volumetric-path-tracing/) samples those points directly. A BSSRDF is a summary of the medium inside a closed surface, which is exact only for the geometry for which it was derived. The dipole assumes a flat, semi-infinite, homogeneous medium; on thin parts, corners and layered materials such as skin it is only an approximation.

**Non-example: a blurred texture.** Blurring the lit image of a surface over the screen spreads light sideways, but with a kernel in pixels that does not follow the profile $R_d$ in millimeters, and it ignores the geometry. Screen-space methods in real-time engines use $R_d$ or a fit to it as the kernel to come closer.

## Related definitions

- [BRDF](/brdf/) and [BSDF](/bsdf/): the special cases with light leaving at the point of entry.
- [Albedo](/albedo/): the single-scattering and reduced albedos, and the total diffuse reflectance $R_{\mathrm{tot}}$ as the albedo of a semi-infinite medium.
- [Participating media](/participating-media/): the absorption, scattering and phase function of the material below the surface, from which a BSSRDF is derived.
- [Fresnel equations](/fresnel-equations/): the transmittance $F_t$ at the two crossings and the internal diffuse reflectance $F_{dr}$.
- [Helmholtz reciprocity](/helmholtz-reciprocity/): the symmetry of $S$ in its two ends.
- [Path tracing](/path-tracing/) and [Monte Carlo integration](/monte-carlo-integration/): a renderer evaluates the double integral over points and directions by sampling $x_i$ near $x_o$ with a density close to $R_d$, or it replaces the BSSRDF by a random walk inside the volume.

### History

Nicodemus et al. defined the BSSRDF in 1977 as the most general function of their nomenclature, from which the BRDF follows for a surface without lateral transport. In graphics, Hanrahan and Krueger (1993) modeled subsurface scattering in layered surfaces by single scattering, which keeps the light at the point of entry. Jensen, Marschner, Levoy and Hanrahan (2001) brought the dipole of medical physics and atmospheric optics into rendering and made translucent materials practical. Later models refined the profile: multipoles for thin layers by Donner and Jensen (2005), quantized diffusion by d'Eon and Irving (2011), and empirical fits by Christensen and Burley (2015). Production renderers now often trace a random walk in the volume instead.

## References
