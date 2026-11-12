---
tag: T7YP2Q
kind: definition
slug: brdf
name: Bidirectional reflectance distribution function
aliases:
- BRDF
area: graphics-and-signals/ray-tracing
level: intro
summary: The function f(ωi, ωo) that gives, for light from ωi, the radiance reflected toward ωo per unit of irradiance. It is measured in inverse steradians and describes how a surface looks.
prereqs: [dot-product]
see_also: [lambertian-reflectance, microfacet-brdf, bsdf, bssrdf, albedo, helmholtz-reciprocity, rendering-equation, phong-shading]
sources:
  - paper: doi:10.6028/NBS.MONO.160
    title: Fred E. Nicodemus, Joseph C. Richmond, Jack J. Hsia, Irving W. Ginsberg and Thomas Limperis, Geometrical considerations and nomenclature for reflectance, NBS Monograph 160, National Bureau of Standards, 1977
    locator: the definition of the BRDF as the ratio of reflected radiance to incident irradiance, its units, the reciprocity relation, and the reflectances obtained by integrating it
  - paper: doi:10.1364/AO.4.000767
    title: Fred E. Nicodemus, Directional reflectance and emissivity of an opaque surface, Applied Optics 4(7), 1965, 767 to 775
    locator: the first statement of the bidirectional reflectance of a surface element, and the link of reflectance and emissivity by reciprocity and Kirchhoff's law
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 3 (the BSDF in the projected solid angle measure) and Section 6.3 (Theorem 6.2, the energy bound on the integral of the BSDF)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 5.6.1, The BRDF, and Chapter 8, Reflection Models
---

The bidirectional reflectance distribution function, or BRDF, of an opaque surface is a function $f_r(\omega_i, \omega_o)$ of two directions. For light that arrives from the direction $\omega_i$, it gives the radiance that the surface reflects toward $\omega_o$, per unit of irradiance that the light delivers. It is the local description of how a material looks: a [Lambertian](/lambertian-reflectance/) surface has a constant BRDF, a mirror has a BRDF that is a delta, and a rough metal has a lobe around the mirror direction, as in a [microfacet model](/microfacet-brdf/). The BRDF is the kernel of the reflection integral and so of the [rendering equation](/rendering-equation/). Nicodemus defined it in 1965 and fixed the nomenclature in 1977. A BRDF is a reflection model; shading methods such as [Phong shading](/phong-shading/) and [Gouraud shading](/gouraud-shading/) only decide where on a polygon a reflection model is evaluated.

## Definition

Let $x$ be a point of a surface with the unit normal $n$, and let $H^2$ be the hemisphere of directions with $n \cdot \omega > 0$. Write $\theta$ for the angle of a direction to $n$. Light of radiance $L_i(\omega_i)$ that arrives from a small solid angle $d\omega_i$ around $\omega_i$ delivers the irradiance $dE(\omega_i) = L_i(\omega_i) \cos\theta_i \, d\omega_i$. Part of it is reflected, and adds $dL_o(\omega_o)$ to the radiance that leaves toward $\omega_o$. For a surface that reflects linearly, $dL_o$ is proportional to $dE$, and the BRDF is the ratio

$$f_r(\omega_i, \omega_o) = \frac{dL_o(\omega_o)}{dE(\omega_i)} = \frac{dL_o(\omega_o)}{L_i(\omega_i) \cos\theta_i \, d\omega_i}.$$

Its unit is the inverse steradian, $\mathrm{sr}^{-1}$. Here $\omega_i$ points from $x$ toward the light, as $\omega_o$ points from $x$ toward the viewer. Summed over all incident directions, this gives the reflection equation

$$L_o(\omega_o) = \int_{H^2} f_r(\omega_i, \omega_o)\, L_i(\omega_i) \cos\theta_i \, d\omega_i.$$

In general $f_r$ also depends on the point $x$ and on the wavelength $\lambda$; a renderer stores it per wavelength or per RGB channel, and a texture can vary it over the surface.

A BRDF is **physically plausible** when it has three properties:

1. **Positivity.** $f_r(\omega_i, \omega_o) \ge 0$.
2. **Reciprocity.** $f_r(\omega_i, \omega_o) = f_r(\omega_o, \omega_i)$. This is [Helmholtz reciprocity](/helmholtz-reciprocity/), which follows from the second law of thermodynamics and detailed balance for an opaque surface without magnetic fields.
3. **Energy conservation.** For every $\omega_i$, $\rho(\omega_i) = \int_{H^2} f_r(\omega_i, \omega_o) \cos\theta_o \, d\omega_o \le 1$. The value $\rho(\omega_i)$ is the directional [albedo](/albedo/). With reciprocity, the bound for each $\omega_i$ is the same as the bound $\int f_r \cos\theta_i \, d\omega_i \le 1$ for each $\omega_o$ (Veach 1997, Theorem 6.2).

A BRDF has four arguments, two angles per direction. It is **isotropic** if it does not change when the surface turns about its normal; then it depends only on $\theta_i$, $\theta_o$ and the difference $\phi_o - \phi_i$ of the azimuths. Brushed metal and satin are **anisotropic**.

### Notation

Some texts write $f_r(\omega_i \to \omega_o)$ to make the direction of light flow explicit, which matters for the [BSDF](/bsdf/), where the two orders are not equal under refraction. Some write $f_r(\omega_o, \omega_i)$ with the outgoing direction first. Veach writes the BSDF with respect to the projected solid angle $d\sigma^\perp(\omega) = |\cos\theta|\,d\omega$, so the reflection equation becomes $L_o = \int f_s\,L_i\,d\sigma^\perp$; the function is the same.

## Examples and non-examples

**The Lambertian BRDF.** $f_r = \rho / \pi$ with $0 \le \rho \le 1$. It is positive, reciprocal, and its albedo is exactly $\rho$; see [Lambertian reflectance](/lambertian-reflectance/).

**The perfect mirror.** A mirror reflects all light from $\omega_i$ into the mirror direction $R(\omega_i) = 2 (n \cdot \omega_i)\,n - \omega_i$. Its BRDF is not a function but a distribution,

$$f_r(\omega_i, \omega_o) = F(\theta_i)\,\frac{\delta(\omega_o - R(\omega_i))}{\cos\theta_i},$$

with the Dirac delta on the sphere and the [Fresnel](/fresnel-equations/) reflectance $F$. The $1/\cos\theta_i$ cancels the cosine of the reflection equation, so $L_o(R(\omega_i)) = F\,L_i(\omega_i)$. A renderer handles it as a special case and never evaluates it at a sampled direction.

**A microfacet BRDF.** $f_r = D F G / (4 \cos\theta_i \cos\theta_o)$ for a rough surface; see [microfacet BRDF](/microfacet-brdf/). For GGX with the roughness $\alpha = 0.05$, $F = 1$ and light and view along the normal, the value is $f_r = G/(4 \pi \alpha^2) \approx 31.8\ \mathrm{sr}^{-1}$. A BRDF is a density over directions, not a fraction, and values far above 1 are normal for glossy surfaces.

**The modified Phong lobe.** The lobe $f_r = k_s \frac{s + 2}{2\pi} (R(\omega_i) \cdot \omega_o)^s$, clamped at 0, is reciprocal, since $R(\omega_i) \cdot \omega_o = R(\omega_o) \cdot \omega_i$. The factor $(s + 2)/(2\pi)$ makes its albedo $k_s$ at normal incidence. Lewis (1994) proposed lobes of this kind to make the Phong model physically plausible.

**Non-example: the original Phong reflection model.** Phong (1975) added to a diffuse term a specular term $k_s (R(\omega_i) \cdot \omega_o)^s$ times the intensity of the light, with no factor $\cos\theta_i$. As a BRDF this is $k_s (R(\omega_i) \cdot \omega_o)^s / \cos\theta_i$, which is not reciprocal. With $k_s = 1$, $s = 10$, $\theta_i = 30°$ and $\theta_o = 60°$ on the other side of the normal in the same plane, $R(\omega_i) \cdot \omega_o = \cos 30° = 0.866$, and the value is $0.866^{10} / \cos 30° = 0.274$ one way and $0.866^{10} / \cos 60° = 0.475$ the other way. Its albedo also grows without bound as $\theta_i \to 90°$. It is a useful shading formula, but a path tracer that uses it as a BRDF gives different images when it traces from the camera and from the light.

**Non-example: a BRDF that creates energy.** $f_r = 1.2 / \pi$ is positive and reciprocal, but its albedo is 1.2. In a closed room of such walls, the Neumann series of the rendering equation diverges, and a path tracer does not converge.

**Non-example: translucent and layered materials.** Light that enters skin or marble leaves at another point. The BRDF assumes that light leaves where it arrives, so it cannot describe such a material; the [BSSRDF](/bssrdf/) can. Light that passes through glass is not reflected; it needs the transmission part of a [BSDF](/bsdf/).

**Non-example: shading methods.** [Gouraud shading](/gouraud-shading/) and [Phong shading](/phong-shading/) are interpolation schemes over polygons. They use a reflection model but do not define one.

## Related definitions

- [Albedo](/albedo/): the integral of the BRDF times the cosine over one of its directions, the fraction of light reflected.
- [BSDF](/bsdf/): the BRDF together with the bidirectional transmittance distribution function (BTDF) on the lower hemisphere, for surfaces that let light through.
- [BSSRDF](/bssrdf/): the generalization in which light may leave at another point than where it entered. The BRDF is the BSSRDF of a surface with no lateral transport.
- [Lambertian reflectance](/lambertian-reflectance/) and [microfacet BRDF](/microfacet-brdf/): the two models that most physically based materials combine.
- [Helmholtz reciprocity](/helmholtz-reciprocity/): the symmetry property 2, and its form with the factor $\eta^2$ for refraction.
- [Rendering equation](/rendering-equation/): the integral equation of light transport whose kernel is the BRDF.
- [Fresnel equations](/fresnel-equations/): the reflectance of a smooth boundary, a factor of most specular BRDFs.

### History

Nicodemus introduced the bidirectional reflectance of a surface element in 1965, in a paper that also tied it to the emissivity by reciprocity. The 1977 monograph by Nicodemus, Richmond, Hsia, Ginsberg and Limperis fixed the name, the symbol $f_r$ and the family of derived reflectances, and became the standard reference in radiometry. In graphics, Blinn (1977) and Cook and Torrance (1982) used physically based reflection functions, and Kajiya (1986) put the BRDF into the rendering equation.

## References
