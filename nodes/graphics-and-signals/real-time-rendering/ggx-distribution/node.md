---
tag: CCM8S7
kind: model
slug: ggx-distribution
name: GGX microfacet distribution
aliases:
- Trowbridge-Reitz distribution
- GGX
- GGX normal distribution function
area: graphics-and-signals/real-time-rendering
level: core
summary: "The density of microfacet normals D(h) = alpha^2 / (pi ((n.h)^2 (alpha^2 - 1) + 1)^2), normalized over projected area. It has a sharp peak and a long tail, and is the usual D of microfacet BRDFs."
prereqs: [microfacet-brdf]
see_also: [smith-masking-shadowing-function, schlick-fresnel-approximation, physically-based-shading, disney-principled-brdf, blinn-phong-reflection-model, split-sum-approximation, importance-sampling, brdf]
sources:
  - paper: doi:10.2312/EGWR/EGSR07/195-206
    title: Bruce Walter, Stephen R. Marschner, Hongsong Li and Kenneth E. Torrance, Microfacet models for refraction through rough surfaces, Eurographics Symposium on Rendering, 2007, 195 to 206
    locator: the GGX distribution, its Smith masking function and its sampling, fitted to measured rough glass
  - paper: doi:10.1364/JOSA.65.000531
    title: T. S. Trowbridge and K. P. Reitz, Average irregularity representation of a rough surface for ray reflection, Journal of the Optical Society of America 65(5), 1975, 531 to 536
    locator: the distribution of facet normals from ellipsoidal irregularities, the same function as GGX (general locator)
  - url: http://jcgt.org/published/0003/02/03/
    title: Eric Heitz, Understanding the masking-shadowing function in microfacet-based BRDFs, Journal of Computer Graphics Techniques 3(2), 2014, 48 to 107
    locator: Section 5.3, Isotropic Shape-Invariant Distributions of Slopes (GGX in Equation 71 and its Lambda in Equation 72), and Section 5 on stretching for the anisotropic form
  - paper: "Brent Burley, Physically-based shading at Disney, course notes, SIGGRAPH 2012 course Practical Physically Based Shading in Film and Game Production, revised 2014"
    locator: Section 5.4, Specular D details (the GTR family with GGX as gamma = 2, and the remap alpha = roughness^2), and Appendix B
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 9, Physically Based Shading (the section on normal distribution functions)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.4, Microfacet Models (the Trowbridge-Reitz distribution)
---

The GGX distribution gives the density $D(h)$ of microfacet normals in a [microfacet BRDF](/microfacet-brdf/): how much facet area per unit surface area has its normal in a small cone around the direction $h$. With the parameter $\alpha > 0$ and $\cos\theta_h = n \cdot h$,

$$D(h) = \frac{\alpha^2}{\pi\,\big((n \cdot h)^2 (\alpha^2 - 1) + 1\big)^2} \quad \text{for } n \cdot h > 0, \qquad D(h) = 0 \text{ otherwise}.$$

Trowbridge and Reitz derived this function in optics in 1975. Walter, Marschner, Li and Torrance used it again in 2007, named it GGX, and showed that it fits measured rough glass better than the Beckmann distribution. Compared with Beckmann at the same $\alpha$, it has a similar peak and a much longer tail, which gives a highlight with a bright core and a wide soft halo. It is now the default $D$ of real-time and offline [physically based shading](/physically-based-shading/). This page gives the factor $D$ only; [Smith masking-shadowing](/smith-masking-shadowing-function/) gives $G$ and [Schlick's approximation](/schlick-fresnel-approximation/) gives $F$.

## The machine

**The surface.** A rough surface with the macro normal $n$, the $z$ axis of a local frame. At a scale far below a pixel it is a height field of flat facets. $D$ is a density on the hemisphere of facet normals $m$, in units of 1/sr.

**The normalization.** The facets, projected onto the macro surface, cover it exactly once:

$$\int_{H^2} D(m)\, (n \cdot m)\, d\omega_m = 1.$$

For GGX this holds for every $\alpha > 0$. With $\mu = \cos\theta_m$ and $d\omega_m = 2\pi\, d\mu$ after the integral over the azimuth, and then $u = \mu^2$:

$$\int_0^1 \frac{2 \alpha^2 \mu}{(\mu^2 (\alpha^2 - 1) + 1)^2}\, d\mu = \alpha^2 \int_0^1 \frac{du}{(u (\alpha^2 - 1) + 1)^2} = \frac{\alpha^2}{\alpha^2 - 1} \Big(1 - \frac{1}{\alpha^2}\Big) = 1,$$

for $\alpha \ne 1$; for $\alpha = 1$, $D = 1 / \pi$ and the integral is $2 \int_0^1 \mu\, d\mu = 1$. This is a proved property of the formula.

**The slope form.** With $\tan\theta_h$ the slope of the facet,

$$D(h) = \frac{\alpha^2}{\pi \cos^4\theta_h\, (\alpha^2 + \tan^2\theta_h)^2}.$$

This is the form of Walter et al. In slope space it is the density $\alpha^2 / (\pi (\alpha^2 + |s|^2)^2)$ of the 2D slope $s$, which falls like $|s|^{-4}$. The Beckmann distribution has Gaussian slopes instead. Heitz (2014) calls both shape invariant: changing $\alpha$ only stretches the slopes. Stretching the two slope axes by different factors gives the anisotropic form

$$D(h) = \frac{1}{\pi \alpha_x \alpha_y \big((h_x / \alpha_x)^2 + (h_y / \alpha_y)^2 + h_z^2\big)^2},$$

which is the isotropic one when $\alpha_x = \alpha_y = \alpha$.

**The parameter.** $\alpha$ is the width of the distribution of slopes. At the peak $D(n) = 1 / (\pi \alpha^2)$. As $\alpha \to 0$, $D$ tends to a delta at $n$ and the surface is a mirror. At $\alpha = 1$, $D = 1 / \pi$ is constant on the hemisphere. Many renderers expose a roughness $r \in [0, 1]$ and set $\alpha = r^2$. Burley (2012) chose this remap because it made the change of roughness look more even to artists. It is a convention, not physics. This page uses $\alpha$ itself everywhere.

**Sampling.** The density $D(h)\,(n \cdot h)$ has the CDF $F(\theta) = \tan^2\theta / (\alpha^2 + \tan^2\theta)$ in $\theta_h$, so inversion gives $\tan^2\theta_h = \alpha^2 u / (1 - u)$ for $u$ uniform, with a uniform azimuth. The change from $h$ to the reflected direction is on the microfacet BRDF page.

## What it counts

$D$ counts facet area: $D(m)\, d\omega_m\, dA$ is the area of the facets with normals in $d\omega_m$ over the patch $dA$. The normalization counts projected area, not facet area: the facet area is larger, by the factor $\int D\, d\omega_m \ge 1$. In a BRDF, $D(h)$ weights the facets that act as mirrors between $l$ and $v$. Its integral against $(v \cdot m)$ over the visible facets enters the masking function.

**Example.** For $\alpha = 0.3$, the peak is $D(n) = 1 / (0.09 \pi) = 3.5368$. Beckmann with the same $\alpha$ has the same peak.

| $\theta_h$ | 0° | 10° | 20° | 30° | 45° | 60° | 75° |
|---|---|---|---|---|---|---|---|
| GGX | 3.5368 | 2.0771 | 0.7423 | 0.2842 | 0.0965 | 0.0480 | 0.0325 |
| Beckmann | 3.5368 | 2.6618 | 1.0409 | 0.1549 | 0.00021 | 0.0000 | 0.0000 |

Near the peak GGX falls faster than Beckmann, and past about 25° it is far above it: at 45° by a factor of 456. Far from the peak, $D \sin^4\theta_h \to \alpha^2 / \pi$, a power law, while Beckmann decays like $e^{-\tan^2\theta / \alpha^2}$. These numbers come from the code of this page, which also checks the normalization by Gauss-Legendre quadrature to $10^{-6}$ for $\alpha$ from 0.02 to 2, the anisotropic normalization, and the sampling CDF with a Kolmogorov test.

## Relation to other models

- **[Microfacet BRDF](/microfacet-brdf/).** GGX is the $D$ in $f = D F G / (4 (n \cdot l)(n \cdot v))$. The derivation of the factor 4 and the albedo loss of the single scattering model are on that page.
- **Beckmann.** The other common $D$, with Gaussian slopes. It was the $D$ of Cook and Torrance. At small $\alpha$ the two are close near the peak.
- **[Blinn-Phong](/blinn-phong-reflection-model/).** The normalized lobe $(s + 2) / (2\pi)\, (n \cdot h)^s$ is also a valid $D$, with a short tail like Beckmann's. The match $s \approx 2 / \alpha^2 - 2$ to Beckmann is a common fit near the peak.
- **GTR.** Burley's generalized Trowbridge-Reitz family $D \propto 1 / (\alpha^2 \cos^2\theta_h + \sin^2\theta_h)^\gamma$ has GGX at $\gamma = 2$. The [Disney principled BRDF](/disney-principled-brdf/) uses $\gamma = 2$ for the main lobe and $\gamma = 1$ for the clear coat, with a longer tail.
- **[Smith masking](/smith-masking-shadowing-function/).** Each $D$ has its own $\Lambda$. For GGX, $\Lambda$ has a closed form, which is one reason for its use.

## Known results in the model

- **Normalization (proved).** $\int D (n \cdot m)\, d\omega_m = 1$ for all $\alpha > 0$, shown above, and for the anisotropic form for all $\alpha_x, \alpha_y > 0$.
- **Long tail (proved).** In slopes, the density falls like $|s|^{-4}$, so its second moment is infinite. The variance of the slopes is not a useful roughness measure for GGX; $\alpha$ is a scale, not a standard deviation.
- **Fit to measurements (measurement).** Walter et al. fitted GGX and Beckmann to measured transmission through rough glass and found that GGX matched the long tails better. Which $D$ fits a given material best is a measurement for that material.
- **Energy loss (proved for the model).** With single scattering and Smith $G$, the albedo of a white GGX conductor drops as $\alpha$ grows, because light that would scatter more than once is lost. The microfacet BRDF page gives the numbers. Multiple scattering models correct this.

## References
