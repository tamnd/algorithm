---
tag: TTFZZ6
kind: model
slug: microfacet-brdf
name: Microfacet BRDF
aliases:
- Cook-Torrance model
- microfacet model
area: graphics-and-signals/ray-tracing
level: advanced
summary: A rough surface as many tiny mirrors. The BRDF D F G / (4 cos θi cos θo) multiplies the density of facet normals, the Fresnel reflectance and the fraction of facets not shadowed or masked.
prereqs: [brdf, fresnel-equations]
see_also: [lambertian-reflectance, bsdf, helmholtz-reciprocity, albedo, importance-sampling, phong-shading, path-tracing, multiple-importance-sampling]
sources:
  - paper: doi:10.1145/357290.357293
    title: Robert L. Cook and Kenneth E. Torrance, A reflectance model for computer graphics, ACM Transactions on Graphics 1(1), 1982, 7 to 24
    locator: the specular term F D G over the product of the cosines, the Beckmann distribution, the V-cavity factor G, and the spectral Fresnel term
  - paper: doi:10.1364/JOSA.57.001105
    title: Kenneth E. Torrance and Ephraim M. Sparrow, Theory for off-specular reflection from roughened surfaces, Journal of the Optical Society of America 57(9), 1967, 1105 to 1114
    locator: the model of a surface as randomly tilted mirror facets with V-groove shadowing and masking
  - paper: doi:10.1364/JOSA.65.000531
    title: T. S. Trowbridge and K. P. Reitz, Average irregularity representation of a rough surface for ray reflection, Journal of the Optical Society of America 65(5), 1975, 531 to 536
    locator: the distribution of facet normals that graphics later named GGX
  - paper: doi:10.2312/EGWR/EGSR07/195-206
    title: Bruce Walter, Stephen R. Marschner, Hongsong Li and Kenneth E. Torrance, Microfacet models for refraction through rough surfaces, Eurographics Symposium on Rendering, 2007, 195 to 206
    locator: the general microfacet BRDF and BTDF with the Jacobian of the half vector, the GGX distribution with its Smith G1, and the sampling of D cos θm
  - url: http://jcgt.org/published/0003/02/03/
    title: Eric Heitz, Understanding the masking-shadowing function in microfacet-based BRDFs, Journal of Computer Graphics Techniques 3(2), 2014, 48 to 107
    locator: the projected area of the facets, the Smith masking function from Λ, the weak white furnace test, and the separable and height-correlated forms of G2
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.4, Microfacet Models (distributions, masking and shadowing, the Torrance-Sparrow model)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 9.7, Microfacet Theory, and Section 9.8, BRDF Models for Surface Reflection
---

A microfacet BRDF models a rough surface as a field of tiny flat mirrors, the facets, with normals that point in many directions. Light from a direction $\omega_i$ reaches a direction $\omega_o$ only by the facets whose normal is the half vector $h$ of the two directions, so the [BRDF](/brdf/) is the density $D(h)$ of such facets times the [Fresnel](/fresnel-equations/) reflectance $F$ of a facet times the fraction $G$ of facets that are neither in shadow nor hidden, divided by $4 \cos\theta_i \cos\theta_o$. Torrance and Sparrow (1967) built the model in optics, Cook and Torrance (1982) brought it to graphics, and Walter et al. (2007) gave the form with the GGX distribution that most physically based renderers now use. A smooth surface has $D$ close to a delta and is a mirror; a rough one spreads the highlight. It is a reflection model. The [Phong shading](/phong-shading/) method, which interpolates normals across a polygon, can evaluate it, but is a different thing from it.

## The machine

**The surface.** The macro surface has the normal $n$, the $z$ axis of a local frame. At a scale far below a pixel and far above the wavelength of light, it is a height field of facets. Each facet is a perfect mirror with the Fresnel reflectance of the material. Light reflects once from one facet and then leaves; light that would hit another facet is lost. This is the single-scattering model.

**The half vector.** A mirror with the normal $m$ reflects $\omega_i$ into $\omega_o$ only if $m$ is the half vector

$$h = \frac{\omega_i + \omega_o}{|\omega_i + \omega_o|}.$$

**The distribution $D$.** $D(m)$ is the density of facet area per unit macro area and per unit solid angle of facet normals. Projected onto the macro surface, the facets cover it exactly once, so

$$\int_{H^2} D(m)\,(n \cdot m)\,d\omega_m = 1.$$

Two distributions are common. With the roughness $\alpha > 0$ and $\theta_m$ the angle of $m$ to $n$,

$$D_{\mathrm{GGX}}(m) = \frac{\alpha^2}{\pi\,\big((n \cdot m)^2 (\alpha^2 - 1) + 1\big)^2}, \qquad D_{\mathrm{Beckmann}}(m) = \frac{\exp(-\tan^2\theta_m / \alpha^2)}{\pi\,\alpha^2 \cos^4\theta_m}.$$

The GGX form is the distribution of Trowbridge and Reitz (1975); Walter et al. named it GGX. It has a sharper peak and longer tails than Beckmann at the same $\alpha$, which gives the glow around highlights that measured metals show. Many renderers expose a perceptual roughness $r$ and set $\alpha = r^2$.

**The masking-shadowing function $G$.** Some facets that face the light are hidden from the viewer by other facets (masking), and some are in the shadow of others (shadowing). The Smith model assumes that the heights of the facets are not correlated with their normals. For a direction $\omega$ it gives the fraction of visible facets $G_1(\omega, m) = \chi^+(\omega \cdot m) / (1 + \Lambda(\omega))$, where $\chi^+$ is 1 for a positive argument and 0 otherwise, and $\Lambda$ depends on $D$. For GGX,

$$\Lambda(\omega) = \frac{\sqrt{1 + \alpha^2 \tan^2\theta} - 1}{2}.$$

For two directions, the separable form is $G_2 = G_1(\omega_i, m)\,G_1(\omega_o, m)$, and the height-correlated form is $G_2 = \chi^+ / (1 + \Lambda(\omega_i) + \Lambda(\omega_o))$. The height-correlated form is the more accurate one, since a facet high up is likely to be both lit and seen (Heitz 2014). Cook and Torrance used the V-cavity form $\min\big(1, \tfrac{2 (n \cdot h)(n \cdot \omega_o)}{\omega_o \cdot h}, \tfrac{2 (n \cdot h)(n \cdot \omega_i)}{\omega_o \cdot h}\big)$ of Torrance and Sparrow.

**The BRDF.** With $F(\omega_i \cdot h)$ the Fresnel reflectance at the angle between the light and the facet,

$$f(\omega_i, \omega_o) = \frac{D(h)\,F(\omega_i \cdot h)\,G_2(\omega_i, \omega_o, h)}{4\,(n \cdot \omega_i)(n \cdot \omega_o)}.$$

**Where the 4 comes from.** Take a unit area of the macro surface and a beam of radiance $L_i$ in the small solid angle $d\omega_i$. The facets with normals in $d\omega_h$ have the area $D(h)\,d\omega_h$, and they receive the power $L_i\,d\omega_i\,(\omega_i \cdot h)\,D(h)\,d\omega_h$. They reflect the fraction $F G_2$ of it into the solid angle $d\omega_o$. The map from $\omega_o$ to the half vector has the Jacobian $d\omega_h / d\omega_o = 1 / (4\,|\omega_o \cdot h|)$. The reflected radiance is the power over $(n \cdot \omega_o)\,d\omega_o$, and with $\omega_i \cdot h = \omega_o \cdot h$ this gives $dL_o = L_i\,d\omega_i\,D F G_2 / (4\,n \cdot \omega_o)$. Divide by $L_i (n \cdot \omega_i)\,d\omega_i$ to get $f$. The 1982 paper writes $\pi$ in place of 4 in the denominator, with a $D$ that is not normalized in the same way; the form with 4 and a normalized $D$ is the one that Walter et al. derived and that the albedo results below use.

## What it counts

The model predicts the reflected radiance of the surface layer for each pair of directions. One evaluation costs a constant number of operations, among them one square root per $\Lambda$ and the Fresnel term. In a renderer the BRDF goes into the reflection integral, which a [Monte Carlo](/monte-carlo-integration/) estimator with $N$ samples evaluates with an error of order $N^{-1/2}$.

**Sampling.** The density $D(m)(n \cdot m)$ is a normalized density of facet normals, and its distribution function in $\theta_m$ inverts in closed form. For GGX, draw $u, v$ uniform in $[0, 1)$ and set

$$\tan^2\theta_m = \frac{\alpha^2 u}{1 - u}, \qquad \phi_m = 2\pi v.$$

Reflect $\omega_o$ about $m$ to get $\omega_i = 2 (\omega_o \cdot m)\,m - \omega_o$. By the Jacobian above, $\omega_i$ has the density $p(\omega_i) = D(m)\,(n \cdot m) / (4\,|\omega_o \cdot m|)$. The estimator $f \cos\theta_i\,L_i / p$ is unbiased, and its weight $F G_2 |\omega_o \cdot m| / ((n \cdot \omega_o)(n \cdot m))$ has no $D$ in it, so it stays bounded as $\alpha \to 0$. Sampling the distribution of the normals that $\omega_o$ sees, $G_1(\omega_o, m) \max(0, \omega_o \cdot m) D(m) / (n \cdot \omega_o)$, wastes fewer samples on facets that face away from the viewer (Heitz 2014).

**What it leaves out.** Light that bounces between facets more than once is lost, so the albedo with $F = 1$ is below 1 and falls as $\alpha$ grows. Wave effects such as diffraction and thin-film colors are outside the model, which is geometric optics. The model has no diffuse part: a material with a diffuse base adds a [Lambertian](/lambertian-reflectance/) or other diffuse term.

## Relation to other models

- **The Phong and Blinn-Phong reflection models.** These are empirical lobes, $(r \cdot \omega_o)^s$ and $(n \cdot h)^s$. Blinn (1977) pointed out that $(n \cdot h)^s$ acts as a distribution of facet normals and brought the Torrance-Sparrow model to graphics. A normalized Blinn-Phong lobe is a usable $D$. The original Phong lobe is not reciprocal as a BRDF; the microfacet form is.
- **Phong shading and Gouraud shading.** [Phong shading](/phong-shading/) and [Gouraud shading](/gouraud-shading/) are ways to evaluate a reflection model on a polygon, not reflection models. A microfacet highlight is narrow, so Gouraud shading, which evaluates it only at the vertices, can miss it.
- **Lambertian reflection.** The [Lambertian model](/lambertian-reflectance/) is the usual base under a microfacet layer. Oren and Nayar used Lambertian facets in place of mirror facets for rough diffuse surfaces.
- **Rough transmission.** Walter et al. (2007) extended the model to a microfacet BTDF for rough glass, with the generalized half vector $-(\eta_i \omega_i + \eta_o \omega_o)$ and [Snell's law](/snells-law/) at each facet. The BRDF and the BTDF together form a [BSDF](/bsdf/), whose transmission part has the $\eta^2$ factor of [Helmholtz reciprocity](/helmholtz-reciprocity/).
- **Multiple scattering.** Later models add the energy that single scattering drops, by a random walk on the facets or by a precomputed compensation lobe. They keep $D$ and $G$ of this model.

## Known results in the model

**Normalization.** For both distributions the integral of $D(m)(n \cdot m)$ over the hemisphere is 1 for every $\alpha$. The tests compute it by Gauss-Legendre quadrature in $\theta$ to within $10^{-9}$ for $\alpha = 0.1$, 0.3, 0.5 and 1.

**The weak white furnace test.** For each direction $\omega_o$ the visible projected area of the facets equals the projected area of the macro surface:

$$\int_{H^2} G_1(\omega_o, m)\,\max(0, \omega_o \cdot m)\,D(m)\,d\omega_m = n \cdot \omega_o.$$

This is the equation that defines $\Lambda$ from $D$ in the Smith model (Heitz 2014). For GGX with $\alpha = 0.3$ and $\omega_o$ at $80°$, quadrature gives 0.173648 against $\cos 80° = 0.173648$.

**Reciprocity.** $D(h)$ depends only on $h$, which is symmetric in the two directions; $\omega_i \cdot h = \omega_o \cdot h$, so $F$ is the same both ways; $G_2$ in both forms is symmetric; and so is the denominator. So $f(\omega_i, \omega_o) = f(\omega_o, \omega_i)$, as [Helmholtz reciprocity](/helmholtz-reciprocity/) requires.

**Energy conservation and energy loss.** With $F = 1$ and the height-correlated $G_2$, the directional [albedo](/albedo/) $\int f \cos\theta_i\,d\omega_i$ of GGX is, by quadrature,

| $\alpha$ | $\theta_o = 0°$ | $\theta_o = 45°$ | $\theta_o = 80°$ |
|---|---|---|---|
| 0.1 | 0.988 | 0.982 | 0.888 |
| 0.3 | 0.877 | 0.845 | 0.848 |
| 0.5 | 0.688 | 0.683 | 0.805 |
| 1.0 | 0.307 | 0.377 | 0.668 |

All values are at most 1, so the model conserves energy, but a rough perfect reflector loses up to 70% of the light, which is the light of the missing bounces. The separable $G_2$ gives smaller values, for example 0.747 in place of 0.805 at $\alpha = 0.5$ and $80°$, because it counts a facet as hidden or shadowed too often. The case $\alpha = 1$ and $\theta_o = 0$ has a closed form: then $D = 1/\pi$ and $G_2 = 2\mu/(1 + \mu)$ with $\mu = \cos\theta_i$, so $f \cos\theta_i = G_2 / (4\pi)$ and the albedo is $\frac{2\pi}{4\pi} \int_0^1 \frac{2\mu}{1 + \mu}\,d\mu = 1 - \ln 2 = 0.3069$. With the Fresnel term of glass ($\eta = 1.5$) and $\alpha = 0.3$, the albedo at $\theta_o = 0$ is 0.036, close to the 0.04 of a smooth surface.

**A worked evaluation.** Take GGX with $\alpha = 0.3$, glass ($\eta = 1.5$), and $\omega_i$ at $30°$ from the normal. In the mirror direction $\omega_o$, $h = n$, $D = 1/(\pi \alpha^2) = 3.537$, $F = 0.0415$ at $30°$, $\Lambda(\omega_i) = \Lambda(\omega_o) = 0.0074$ and $G_2 = 1/(1 + 0.0149) = 0.985$, so $f = 3.537 \cdot 0.0415 \cdot 0.985 / (4 \cdot 0.75) = 0.0482$. For $\omega_o$ at $60°$ on the other side, $h$ is $15°$ from $n$, $D = 1.257$, $F = 0.0502$ at $\omega_i \cdot h = \cos 45°$, $G_2 = 0.934$ and $f = 0.0340$, the same value for the swapped pair.

**A Monte Carlo check.** With $\alpha = 0.5$, $\theta_o = 45°$ and $F = 1$, $N = 20000$ samples of the sampling scheme above give $0.6842$ with a standard error of $0.0038$, against the quadrature value $0.6828$. The tests run this and two other cases with a fixed seed and accept four standard errors.

**Floating point.** The half vector is undefined when $\omega_i = -\omega_o$, which happens only at grazing angles; return 0 there. As $\alpha \to 0$, $D$ at $h = n$ grows like $1/\alpha^2$ and the lobe becomes narrower than the grid of any quadrature or the precision of $h$; clamp $\alpha$ from below, or switch to a delta mirror. $\tan^2\theta$ is infinite at $\theta = 90°$, so code computes $\Lambda$ from $\cos^2\theta$ and $1 - \cos^2\theta$ and returns 0 for directions below the horizon. A normal from a normal map can make $n \cdot \omega_o < 0$ for a visible point, and the code must not divide by it.

## References
