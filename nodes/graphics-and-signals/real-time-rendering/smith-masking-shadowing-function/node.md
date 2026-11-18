---
tag: 0245JB
kind: model
slug: smith-masking-shadowing-function
name: Smith masking-shadowing function
aliases:
- Smith G term
- Smith shadowing function
- height-correlated Smith G
area: graphics-and-signals/real-time-rendering
level: advanced
summary: "The G factor of a microfacet BRDF. It assumes facet heights and normals are uncorrelated and gives G1 = 1/(1+Lambda), with a closed form for GGX and a separable and a height-correlated G2."
prereqs: [microfacet-brdf, ggx-distribution]
see_also: [schlick-fresnel-approximation, physically-based-shading, disney-principled-brdf, split-sum-approximation, brdf, albedo, helmholtz-reciprocity, monte-carlo-integration]
sources:
  - paper: doi:10.1109/TAP.1967.1138991
    title: B. Smith, Geometrical shadowing of a random rough surface, IEEE Transactions on Antennas and Propagation 15(5), 1967, 668 to 671
    locator: the shadowing probability of a random rough surface with uncorrelated heights and slopes (general locator)
  - url: http://jcgt.org/published/0003/02/03/
    title: Eric Heitz, Understanding the masking-shadowing function in microfacet-based BRDFs, Journal of Computer Graphics Techniques 3(2), 2014, 48 to 107
    locator: Sections 2.3 and 2.4 (the conservation of projected area as a constraint on G1), Section 3.5 (the weak white furnace test), Section 4 (the Smith and the V-cavity microsurface profiles), Section 5 (stretch invariance, with GGX in Equations 71 and 72), Section 6 (the separable form, Equation 98, and the height-correlated form, Equation 99)
  - paper: doi:10.2312/EGWR/EGSR07/195-206
    title: Bruce Walter, Stephen R. Marschner, Hongsong Li and Kenneth E. Torrance, Microfacet models for refraction through rough surfaces, Eurographics Symposium on Rendering, 2007, 195 to 206
    locator: the Smith G1 for the GGX and Beckmann distributions and its use in the separable G
  - paper: "Brian Karis, Real shading in Unreal Engine 4, course notes, SIGGRAPH 2013 course Physically Based Shading in Theory and Practice"
    locator: the specular G (Schlick's form with k = alpha / 2, and k = (roughness + 1)^2 / 8 for analytic lights only), Equation 4
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 9, Physically Based Shading (the section on microfacet theory, masking and shadowing)
---

The Smith masking-shadowing function is the $G$ factor of a [microfacet BRDF](/microfacet-brdf/). A facet that faces both the light and the viewer can still be hidden from the viewer by other facets (masking) or be in the shadow of other facets (shadowing). The Smith model assumes that the height of a facet does not depend on its normal. Under that assumption the visible fraction from a direction $\omega$ has the form

$$G_1(\omega, m) = \frac{\chi^+(\omega \cdot m)}{1 + \Lambda(\omega)},$$

where $\chi^+$ is 1 for a positive argument and 0 otherwise, and $\Lambda$ depends only on the distribution of slopes. For [GGX](/ggx-distribution/), $\Lambda$ has a closed form. Smith derived the shadowing of a random rough surface in 1967 for radar. Walter and others brought it to rendering. Heitz (2014) showed that the Smith function and the V-cavity function are both exact for the microsurfaces that they assume, and that the Smith microsurface gives better results at grazing angles. This page gives the factor $G$; the [GGX page](/ggx-distribution/) gives $D$ and [Schlick's approximation](/schlick-fresnel-approximation/) gives $F$.

## The machine

**The microsurface.** A height field over the macro surface, with the macro normal $n$ as the $z$ axis and a distribution $D$ of facet normals normalized by projected area. A direction $\omega$ makes the angle $\theta$ with $n$, and $\mu = \cos\theta > 0$.

**The masking function $G_1(\omega, m)$.** The fraction of the facets with normal $m$ that a ray from the direction $\omega$ sees, with no other facet in between. Facets that face away, $\omega \cdot m \le 0$, are never visible.

**The constraint.** Seen from $\omega$, the visible facets project onto exactly the projected area of the macro surface. With projected areas normalized per unit macro area,

$$\int_{H^2} G_1(\omega, m)\, \max(0, \omega \cdot m)\, D(m)\, d\omega_m = \cos\theta.$$

Heitz (2014, Sections 2.4 and 3.5) derives this constraint and uses it as the weak white furnace test: a masking function that fails it does not describe any microsurface.

**The Smith assumption.** If the heights and the normals of the facets are not correlated, the masking does not depend on $m$ except through $\chi^+$, so $G_1 = \chi^+(\omega \cdot m)\, g(\omega)$. Putting this into the constraint gives

$$g(\omega) = \frac{\cos\theta}{\int \max(0, \omega \cdot m)\, D(m)\, d\omega_m} = \frac{1}{1 + \Lambda(\omega)}, \qquad \Lambda(\omega) = \frac{1}{\cos\theta} \int \max(0, \omega \cdot m)\, D(m)\, d\omega_m - 1.$$

$\Lambda$ is the projected area of the facets that face $\omega$ but are hidden, per unit of visible area. For GGX with the parameter $\alpha$ (Heitz 2014, Equation 72),

$$\Lambda(\omega) = \frac{-1 + \sqrt{1 + \alpha^2 \tan^2\theta}}{2}, \qquad G_1(\omega) = \frac{2}{1 + \sqrt{1 + \alpha^2 \tan^2\theta}},$$

the second form being the one of Walter et al. (2007). For an anisotropic GGX, $\alpha$ is replaced by $\sqrt{\alpha_x^2 \cos^2\phi + \alpha_y^2 \sin^2\phi}$ for the azimuth $\phi$ of $\omega$, by the stretch invariance of Heitz's Section 5.

**The joint function $G_2(l, v, m)$.** A BRDF needs the fraction of facets that are visible from $v$ and lit from $l$. Two forms are common (Heitz 2014, Section 6):

$$G_2^{\text{sep}} = G_1(l, m)\, G_1(v, m), \qquad G_2^{\text{hc}} = \frac{\chi^+(l \cdot m)\, \chi^+(v \cdot m)}{1 + \Lambda(l) + \Lambda(v)}.$$

The separable form treats masking and shadowing as independent. In fact both are more likely on low facets, so they are positively correlated, and the separable form counts too much shadowing. The height-correlated form takes the correlation through the height into account. This page uses the height-correlated form, which Heitz suggests for practice because it is more accurate at the same cost. Both forms are symmetric in $l$ and $v$, so the BRDF stays reciprocal.

## What it counts

$G_1$ counts the visible fraction of facet area, and $G_2$ the fraction that is both visible and lit. Both are in $[0, 1]$. $G_1 = 1$ at normal view, because $\tan\theta = 0$, and $G_1 \to 0$ at grazing view, because $\tan\theta \to \infty$. A smoother surface ($\alpha \to 0$) hides less.

**Example.** $G_1$ for GGX:

| $\alpha$ | 0° | 30° | 45° | 60° | 75° | 80° | 85° | 89° |
|---|---|---|---|---|---|---|---|---|
| 0.1 | 1 | 0.9992 | 0.9975 | 0.9926 | 0.9674 | 0.9304 | 0.7941 | 0.2934 |
| 0.25 | 1 | 0.9948 | 0.9848 | 0.9571 | 0.8447 | 0.7313 | 0.4966 | 0.1302 |
| 0.5 | 1 | 0.9800 | 0.9443 | 0.8610 | 0.6416 | 0.4992 | 0.2940 | 0.0674 |
| 1.0 | 1 | 0.9282 | 0.8284 | 0.6667 | 0.4112 | 0.2959 | 0.1603 | 0.0343 |

For $l$ and $v$ both at 60° with $\alpha = 0.5$, the separable $G_2$ is $0.8610^2 = 0.7413$ and the height-correlated one is $1 / (1 + 2 \cdot 0.1614) = 0.7559$. For $\alpha = 1$ they are $0.4444$ and $0.5$. The gap grows with roughness and at grazing angles.

**The Schlick-GGX fit.** Real-time code often replaces $G_1$ by Schlick's form $\mu / (\mu (1 - k) + k)$. Karis (2013) sets $k = \alpha / 2$ and notes that this matches Smith exactly at $\alpha = 1$: there $\Lambda = (1 / \mu - 1) / 2$, so both give $G_1 = 2\mu / (1 + \mu)$. For other $\alpha$ it is a fit. Over all $\mu \in (0, 1]$, the largest error of the fit is $0.066$ at $\alpha = 0.5$, $0.110$ at $\alpha = 0.25$ and $0.140$ at $\alpha = 0.1$, always toward too much masking near grazing angles. For analytic lights only, Karis uses $k = (r + 1)^2 / 8$ with the perceptual roughness $r$, a tuning that reduces the brightness of smooth surfaces; for image-based light it makes grazing angles too dark. The values above come from the code of this page, which also checks the weak white furnace test by quadrature to $2 \cdot 10^{-3}$ and by Monte Carlo with a fixed seed.

## Relation to other models

- **[Microfacet BRDF](/microfacet-brdf/).** $G_2$ is the $G$ in $f = D F G / (4 (n \cdot l)(n \cdot v))$. Many shaders fold $G_2$ and the denominator into one visibility term $V = G_2 / (4 (n \cdot l)(n \cdot v))$, which for the height-correlated GGX form has a cheap expression.
- **The V-cavity model.** The $G$ of Torrance and Sparrow and of Cook and Torrance, $\min(1, 2 (n \cdot h)(n \cdot v) / (v \cdot h), 2 (n \cdot h)(n \cdot l) / (v \cdot h))$, models the surface as V-shaped grooves. Heitz (2014, Section 4) shows that it is also exact for its own microsurface, but that this microsurface misses the effect of occlusion, which gives wrong glossy highlights at grazing view angles.
- **Beckmann.** The Smith $\Lambda$ of Beckmann needs the error function, $\Lambda = (\operatorname{erf}(a) - 1) / 2 + e^{-a^2} / (2 a \sqrt\pi)$ with $a = 1 / (\alpha \tan\theta)$; real-time code uses a rational fit.
- **Disney.** The [Disney principled BRDF](/disney-principled-brdf/) of 2012 used the GGX Smith $G$ with the remapped $\alpha_g = (0.5 + r / 2)^2$; the 2014 revision of the notes removed the remap for the main lobe after Heitz's analysis.
- **Multiple scattering.** The Smith model counts only single scattering. Light blocked by a facet is lost, so the albedo of a rough surface is too low. The microfacet BRDF page gives the loss, and multiple scattering models add it back.

## Known results in the model

- **Range (proved).** $0 \le G_1 \le 1$ and $0 \le G_2^{\text{sep}} \le G_2^{\text{hc}} \le 1$, because $(1 + \Lambda(l))(1 + \Lambda(v)) = 1 + \Lambda(l) + \Lambda(v) + \Lambda(l)\Lambda(v) \ge 1 + \Lambda(l) + \Lambda(v)$ for $\Lambda \ge 0$.
- **Exact for its microsurface (proved by Heitz 2014).** The Smith $G_1$ is the exact masking function of a microsurface with no correlation between heights and normals, and it passes the weak white furnace test for every $D$.
- **Reciprocity (proved).** Both $G_2$ forms are symmetric in $l$ and $v$.
- **Closed form for GGX (proved).** The $\Lambda$ above, from the slope distribution of GGX.
- **Schlick-GGX (fit).** Exact at $\alpha = 1$ only, with the errors above.
- **The real surface (measurement).** Whether a material has uncorrelated heights and normals is a measurement. Real surfaces can differ, and the model then has an error that the test above cannot show.

## References
