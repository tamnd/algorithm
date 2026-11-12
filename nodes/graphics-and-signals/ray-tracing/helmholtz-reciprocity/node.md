---
tag: BZ1TF8
kind: theorem
slug: helmholtz-reciprocity
name: Helmholtz reciprocity
aliases:
- reciprocity principle
- BSDF reciprocity
area: graphics-and-signals/ray-tracing
level: advanced
summary: A physical BSDF satisfies fs(ωi→ωo)/ηo² = fs(ωo→ωi)/ηi², so a BRDF is symmetric in its two directions. The proof uses Kirchhoff's radiance law and detailed balance.
prereqs: [brdf, bsdf]
see_also: [snells-law, fresnel-equations, microfacet-brdf, albedo, bidirectional-path-tracing, photon-mapping, path-tracing, phong-shading]
sources:
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 6, Section 6.1 (Kirchhoff's equilibrium radiance law and detailed balance), Section 6.2 (Theorem 6.1 and the rotated mirror), Appendix 6.A (Helmholtz' original statement), Appendix 6.B (Rayleigh) and Appendix 6.D (magnetic fields and absorbing media)
  - paper: "Hermann von Helmholtz, Handbuch der physiologischen Optik, volume 1, Leopold Voss, Leipzig, 1856"
    locator: the reciprocity statement for a beam that passes through a system of mirrors and lenses
  - paper: "Lord Rayleigh, On the law of reciprocity in diffuse reflexion, Philosophical Magazine, series 5, volume 49, 1900"
    locator: the statement that exchanging a point source and a receiver near a reflecting surface leaves the received intensity unchanged
  - paper: doi:10.6028/NBS.MONO.160
    title: Fred E. Nicodemus, Joseph C. Richmond, Jack J. Hsia, Irving W. Ginsberg and Thomas Limperis, Geometrical considerations and nomenclature for reflectance, NBS Monograph 160, National Bureau of Standards, 1977
    locator: the reciprocity relation of the BRDF and its use for the derived reflectances
---

Helmholtz reciprocity is the rule that a physical surface scatters light in the same way when the light runs backward. For an opaque surface it says that the [BRDF](/brdf/) is symmetric, $f_r(\omega_i, \omega_o) = f_r(\omega_o, \omega_i)$. For a surface between two media of refractive indices $\eta_i$ and $\eta_o$, the general form for the [BSDF](/bsdf/) is $f_s(\omega_i \to \omega_o) / \eta_o^2 = f_s(\omega_o \to \omega_i) / \eta_i^2$. The rule is what allows a renderer to trace paths from the camera, from the lights or from both, as in [bidirectional path tracing](/bidirectional-path-tracing/) and [photon mapping](/photon-mapping/), and get the same image. The name honors Helmholtz, whose principle of 1856 covers only beams through mirrors and lenses; the general form and its proof from thermodynamics are due to Veach (1997).

## Statement

Fix a frequency $\nu$, and let $f_s$ be the BSDF at $\nu$ of a surface that is either the boundary of an opaque object or the interface between two media that do not absorb. For a direction $\omega$ at the surface, let $\eta(\omega)$ be the refractive index of the medium on the side of $\omega$. All directions point away from the surface. Assume:

- **(A1) The BSDF is a property of the material.** It does not depend on the light field that falls on the surface, nor on the temperature of the surroundings.
- **(A2) Kirchhoff's equilibrium radiance law.** In a closed enclosure at one temperature $T > 0$ that contains a black body, the spectral radiance at $\nu$ of every ray $(x, \omega)$ is $L(x, \omega) = c\,\eta(x, \omega)^2$, for a constant $c > 0$ that depends only on $T$ and $\nu$.
- **(A3) Detailed balance.** In such an enclosure, with no external magnetic field, each process that moves energy has a reverse process, and the two run at the same rate.

**Theorem** (Veach 1997, Theorem 6.1). For all directions $\omega_i$ and $\omega_o$,

$$\frac{f_s(\omega_i \to \omega_o)}{\eta(\omega_o)^2} = \frac{f_s(\omega_o \to \omega_i)}{\eta(\omega_i)^2}.$$

If $\omega_i$ and $\omega_o$ are on the same side of the surface, $\eta(\omega_i) = \eta(\omega_o)$ and the theorem is the symmetry $f_r(\omega_i, \omega_o) = f_r(\omega_o, \omega_i)$ of the BRDF. If they are on opposite sides, the two orders of the BTDF differ by the factor $(\eta_o / \eta_i)^2$. For spectral radiance per unit of wavelength instead of frequency, the wavelength itself changes across the interface, and the factor $\eta^2$ becomes $\eta^3$ (Veach 1997, eq. 6.4).

## In plain words

Shine a lamp at a sheet of paper and look at it from a second spot. Then swap the lamp and your eye. The paper looks just as bright both times. This holds for any real material, no matter how complex its surface is: the path from the lamp to the eye is as easy to travel one way as the other.

Glass adds a twist. Light that goes into glass gets squeezed into a narrower cone, so it looks brighter inside. When it comes out, it spreads again. The rule still holds, but only after this squeeze is counted.

The reason is heat. In a closed box where everything has the same temperature, light flows in every direction at once. If a surface sent more light one way than it took back, the balance in the box would break.

## Proof

Put a small area $dA(x)$ of the surface inside an enclosure as in (A2) and (A3), and fix two directions $\omega_i$ and $\omega_o$ with small cones of projected solid angle $d\sigma^\perp(\omega_i)$ and $d\sigma^\perp(\omega_o)$, where $d\sigma^\perp(\omega) = |\cos\theta|\,d\omega$. By (A1) the BSDF in the enclosure is the same function $f_s$ as anywhere else.

**Forward process.** Light arrives at $x$ from the cone around $\omega_i$ with the radiance $L(\omega_i)$. By the definition of the BSDF, it adds the radiance $dL_o(\omega_o) = f_s(\omega_i \to \omega_o)\,L(\omega_i)\,d\sigma^\perp(\omega_i)$ toward $\omega_o$. The power that this radiance carries through $dA(x)$ into the cone around $\omega_o$ is

$$d\Phi_1 = dL_o(\omega_o)\,d\sigma^\perp(\omega_o)\,dA(x) = f_s(\omega_i \to \omega_o)\,L(\omega_i)\,d\sigma^\perp(\omega_i)\,d\sigma^\perp(\omega_o)\,dA(x).$$

**Reverse process.** In the same way, the light that arrives from the cone around $\omega_o$ and is scattered into the cone around $\omega_i$ carries the power

$$d\Phi_2 = f_s(\omega_o \to \omega_i)\,L(\omega_o)\,d\sigma^\perp(\omega_o)\,d\sigma^\perp(\omega_i)\,dA(x).$$

**Detailed balance.** The second process is the reverse of the first, so by (A3) $d\Phi_1 = d\Phi_2$. The factors $d\sigma^\perp(\omega_i)$, $d\sigma^\perp(\omega_o)$ and $dA(x)$ are positive and the same on both sides, so

$$f_s(\omega_i \to \omega_o)\,L(\omega_i) = f_s(\omega_o \to \omega_i)\,L(\omega_o).$$

**Equilibrium radiance.** By (A2), $L(\omega_i) = c\,\eta(\omega_i)^2$ and $L(\omega_o) = c\,\eta(\omega_o)^2$ with the same $c > 0$. Substitute and divide by $c\,\eta(\omega_i)^2\,\eta(\omega_o)^2 > 0$:

$$\frac{f_s(\omega_i \to \omega_o)}{\eta(\omega_o)^2} = \frac{f_s(\omega_o \to \omega_i)}{\eta(\omega_i)^2}.$$

The directions were arbitrary, and by (A1) the identity, which holds for the BSDF in the enclosure, holds for the BSDF everywhere. $\blacksquare$

The proof needs an enclosure at a uniform temperature only as a thought experiment. Every body at a temperature above zero radiates a little at every frequency, so $c > 0$ at visible frequencies even at room temperature.

## Consequences

**Symmetric BRDFs.** Every physically plausible BRDF is symmetric. Models are tested for it: the [Lambertian](/lambertian-reflectance/) BRDF and the [microfacet BRDF](/microfacet-brdf/) are symmetric, because the half vector, the Fresnel factor at the half vector and the Smith masking term are all symmetric in the two directions.

**The two directions of the BTDF.** For the microfacet BTDF of Walter et al. (2007) with the GGX roughness $\alpha = 0.3$, the height-correlated Smith term, $\eta_i = 1$ and $\eta_o = 1.5$, light from $30°$ in air toward one direction in the glass gives $f_s(\omega_i \to \omega_o) = 4.139$ and the reverse $f_s(\omega_o \to \omega_i) = 1.839$. The ratio is $2.25 = 1.5^2$ to machine precision, as the theorem requires. For a smooth interface, the transmittance $1 - F$ is the same in both directions by the Stokes relations of the [Fresnel equations](/fresnel-equations/), and the Jacobian of the refraction map in [Snell's law](/snells-law/), $d\sigma^\perp(\omega_o) / d\sigma^\perp(\omega_i) = \eta_i^2 / \eta_o^2$, supplies the rest of the factor.

**Radiance and importance.** A camera ray that is traced backward carries importance, and the BSDF it must use is the adjoint $f_s^*(\omega_i \to \omega_o) = f_s(\omega_o \to \omega_i)$. By the theorem $f_s^* = f_s$ for reflection, so a renderer can use one BSDF in both directions. For refraction $f_s^* = (\eta_i / \eta_o)^2 f_s$, and light tracing and [photon mapping](/photon-mapping/) must apply this factor, or caustics seen through glass come out too bright or too dark by $\eta^2$.

**Two reflectances are one.** The directional [albedo](/albedo/) $\int f_r(\omega_i, \omega_o) \cos\theta_o\,d\omega_o$, the fraction of a beam from $\omega_i$ that is reflected, equals by symmetry the radiance $\int f_r(\omega_o, \omega_i) \cos\theta_o\,d\omega_o$ that the surface sends toward $\omega_i$ under a uniform sky of radiance 1. This is the basis of the furnace test of a renderer.

**Rayleigh's form.** Put a small source and a small receiver at two places near a surface, and swap them. The received irradiance is the same, because the BRDF is symmetric and the geometric factors of the two configurations are equal. This is the form in which Rayleigh stated the rule in 1900.

**Energy bound in one direction only.** For a fixed $\omega_i$, the energy bound $\int f_s(\omega_i \to \omega_o)\,|\cos\theta_o|\,d\omega_o \le 1$ holds (Veach 1997, Theorem 6.2). For a fixed $\omega_o$, the integral over $\omega_i$ is the bound for the adjoint, which by the theorem differs by $\eta^2$ for transmission and can exceed 1. For the rough glass above, at normal incidence the transmitted fraction is $0.911$, while the integral over all incident directions in air, for the direction straight down in the glass, is $1.958$, against the value $2.25 \cdot 0.96 = 2.16$ of smooth glass.

## Tightness

**The second law alone does not give it.** Veach (1997, Section 6.2) gives a surface that is not reciprocal but that no experiment in an isothermal enclosure can tell apart from a mirror. It reflects each incident direction into the direction obtained by turning it by $90°$ about the normal, not by $180°$. It maps a uniform incident radiance to a uniform reflected radiance, so it keeps the equilibrium and does not break the second law of thermodynamics. Its BRDF is not symmetric, since turning by $90°$ twice does not give the identity. The proof needs detailed balance (A3), which compares a path with its reverse, and not only the balance of total flows.

**The factor $\eta^2$ cannot be dropped.** The BTDF above has $f_s(\omega_i \to \omega_o) / f_s(\omega_o \to \omega_i) = 2.25$, so a symmetric BTDF is wrong for glass. The symmetric form holds only when both directions lie in media of the same index.

**Magnetic fields.** Detailed balance fails in an external magnetic field. By the Faraday effect, the plane of polarization of light in a magnetized medium turns by an angle that depends on the field and not on the direction of travel. Rayleigh's light trap puts such a medium between two polarizers at $45°$ to each other: light passes one way and is blocked the other way. A thin magnetized film coated with polarizers is a surface whose BSDF breaks the theorem (Veach 1997, Appendix 6.D.1). Optical isolators in lasers and fiber networks work in this way.

**Absorbing media.** If the medium on one side absorbs, as for transmission into a metal, the theorem fails: the path of a refracted beam need not be reversible, and the fraction transmitted can differ in the two directions (Veach 1997, Appendix 6.D.2). The theorem covers the reflection from a metal, which is the boundary of an opaque object, but not the transmission into it.

**Models that are not physical.** The original Phong specular term, used as a BRDF, is $k_s (R(\omega_i) \cdot \omega_o)^s / \cos\theta_i$. With $k_s = 1$, $s = 10$, $\theta_i = 30°$ and $\theta_o = 60°$ on the other side of the normal, its value is $0.274$ one way and $0.475$ the other. [Phong shading](/phong-shading/) and [Gouraud shading](/gouraud-shading/) are interpolation methods over polygons and are not affected; the asymmetry is in the reflection formula. Shading normals from bump maps also make a BSDF asymmetric. Such models do not break physics; they are not models of a physical surface, and the theorem says nothing about them.

**Other frequencies.** The theorem is about scattering at one frequency. A fluorescent material absorbs light at one frequency and emits it at another; it needs a matrix of BSDFs over frequencies, and the theorem as stated does not cover it.

## History

Helmholtz stated his reciprocity principle in the first volume of the Handbuch der physiologischen Optik (1856). It concerns a beam that passes through an optical system by reflections and refractions: if a fraction of the power of a beam from $A$ reaches $B$, the same fraction of a beam sent back from $B$ reaches $A$. His reflections are mirror reflections, his principle is stated for power, so it holds across media of different indices, and he excluded media that turn the plane of polarization, after Faraday. He gave no proof. Kirchhoff derived the equilibrium radiance law with the factor $\eta^2$ around 1860. Rayleigh (1900) seems to have been the first to state reciprocity for diffuse reflection, again without a proof from more basic laws. Minnaert (1941) showed how Helmholtz's statement can be read more generally. Nicodemus (1965) and Nicodemus et al. (1977) used the symmetry of the BRDF and attributed it to Helmholtz, and graphics took the name from them. Veach (1997) pointed out that Helmholtz's principle does not imply the symmetry of the BRDF, proved the general form with $\eta^2$ from Kirchhoff's law and detailed balance, showed by the rotated mirror that the second law alone does not suffice, and drew the consequences for the adjoint BSDF in bidirectional rendering.

## References
