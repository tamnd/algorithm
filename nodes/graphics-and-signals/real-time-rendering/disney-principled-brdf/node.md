---
tag: X3TDVD
kind: model
slug: disney-principled-brdf
name: Disney principled BRDF
aliases:
- principled BRDF
- Burley BRDF
area: graphics-and-signals/real-time-rendering
level: advanced
summary: "A BRDF with a few intuitive parameters such as base color, metallic and roughness that blends diffuse, specular, sheen and clearcoat lobes."
prereqs: [physically-based-shading, ggx-distribution, schlick-fresnel-approximation]
see_also: [microfacet-brdf, smith-masking-shadowing-function, oren-nayar-reflectance-model, lambertian-reflectance, blinn-phong-reflection-model, split-sum-approximation, albedo, helmholtz-reciprocity]
sources:
  - paper: "Brent Burley, Physically-based shading at Disney, course notes, SIGGRAPH 2012 course Practical Physically Based Shading in Film and Game Production, revised 2014"
    locator: Section 4 (observations of the MERL 100 measured materials), Section 5.1 (the principles), Section 5.2 (the parameters), Sections 5.3 to 5.6 (the diffuse, D, F and G terms), Section 5.7 (layering and parameter blending), Appendix B (normalization of GTR) and the 2014 Addenda (sheen details, specular G revisited)
  - paper: "Brian Karis, Real shading in Unreal Engine 4, course notes, SIGGRAPH 2013 course Physically Based Shading in Theory and Practice"
    locator: the sections Shading Model (Diffuse BRDF) and Material Model (BaseColor, Metallic, Roughness and Cavity, and the parameters left out)
  - url: http://jcgt.org/published/0003/02/03/
    title: Eric Heitz, Understanding the masking-shadowing function in microfacet-based BRDFs, Journal of Computer Graphics Techniques 3(2), 2014, 48 to 107
    locator: Section 3.5 (the weak white furnace test) and Section 6 (the Smith G2 forms), the analysis that led to the 2014 change of the specular G
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 9, Physically Based Shading (general locator)
---

The Disney principled BRDF is the material model that Brent Burley and Walt Disney Animation Studios built for the film Wreck-It Ralph (2012). The team first studied the MERL 100, a set of 100 measured isotropic materials, and then wrote a model that an artist controls with one color and ten scalar parameters. Each parameter goes from 0 to 1 over its plausible range and has a visible meaning, such as roughness or metallic, instead of a physical quantity such as an index of refraction. The model is a sum of lobes: an empirical diffuse term, a [GGX](/ggx-distribution/) specular lobe with [Schlick's Fresnel](/schlick-fresnel-approximation/) and a [Smith](/smith-masking-shadowing-function/) G, a sheen lobe for cloth and a second specular lobe for a clear coat. Epic Games used a reduced form of it in Unreal Engine 4 (Karis 2013). This page describes one color channel of the model with the 2014 revision of the specular G.

## The machine

**Directions.** $n$ is the normal, $l$ the light direction and $v$ the view direction, all unit vectors that point away from the surface. $h$ is the unit half vector of $l$ and $v$. The angles are $\theta_l$ and $\theta_v$ from $n$, $\theta_h$ between $n$ and $h$, and $\theta_d$ between $l$ and $h$, which is also the angle between $v$ and $h$.

**The parameters (Burley 2012, Section 5.2).** baseColor; subsurface; metallic, which the notes call "a linear blend between two different models"; specular, used "in lieu of an explicit index-of-refraction"; specularTint; roughness; anisotropic; sheen, "primarily intended for cloth"; sheenTint; clearcoat; and clearcoatGloss, with 0 for satin and 1 for gloss. The principles of Section 5.1 are these: the parameters are intuitive rather than physical, there are as few as possible, each goes from 0 to 1 over its plausible range, a parameter may go past that range where it makes sense, and all combinations must be as robust and plausible as possible.

**The BRDF.** With $b$ the base color, $m$ metallic, $r$ roughness, $s$ sheen and $c$ clearcoat, the page uses

$$f = (1 - m)\big(f_d + s\, F_H\big) + f_s + f_c, \qquad F_H = (1 - \cos\theta_d)^5.$$

**Diffuse (Section 5.3).**

$$f_d = \frac{b}{\pi}\big(1 + (F_{D90} - 1)(1 - \cos\theta_l)^5\big)\big(1 + (F_{D90} - 1)(1 - \cos\theta_v)^5\big), \qquad F_{D90} = 0.5 + 2 r \cos^2\theta_d.$$

At grazing angles a smooth surface keeps half of the Lambertian value in each factor, and a rough one gains up to a factor of 2.5. The notes describe it as an empirical model for diffuse retroreflection and say that the Lambert model is often "too dark on the edges". It ignores the index of refraction and assumes no diffuse loss at entry, so the artist sets the diffuse color directly.

**Specular (Sections 5.4 to 5.6).** The distribution is the generalized Trowbridge-Reitz (GTR) family

$$D_\gamma(\theta_h) = \frac{c_\gamma}{(\alpha^2 \cos^2\theta_h + \sin^2\theta_h)^\gamma},$$

with $c_\gamma$ set so that $\int D \cos\theta_h\, d\omega = 1$ (Appendix B). $\gamma = 2$ is GGX with $c_2 = \alpha^2 / \pi$, and $\gamma = 1$ has the longer tail with $c_1 = (\alpha^2 - 1) / (\pi \ln \alpha^2)$. The primary lobe uses $\gamma = 2$ and $\alpha = r^2$, a remap that the notes found more perceptually linear. Its Fresnel term is Schlick's form in $\theta_d$,

$$F = F_0 + (1 - F_0)F_H, \qquad F_0 = (1 - m)\, 0.08\, \text{specular} + m\, b.$$

The specular range [0, 0.08] is the reflectance at normal incidence for an index of refraction from 1.0 to about 1.8, and the default 0.5 gives 0.04, the value for an index of 1.5. G is the separable Smith G of GGX, $G = G_1(l) G_1(v)$ with $G_1(w) = 2 / (1 + \sqrt{1 + \alpha^2 \tan^2\theta_w})$. Then

$$f_s = \frac{D_2(\theta_h)\, F\, G}{4 \cos\theta_l \cos\theta_v}.$$

**Clear coat.** A second, isotropic and non-metallic lobe with $\gamma = 1$, a fixed $F_0 = 0.04$ (an index of 1.5, as for polyurethane) and the GGX G at a fixed roughness of 0.25:

$$f_c = 0.25\, c\, \frac{D_1(\theta_h; \alpha_c)\, F_{0.04}\, G_{0.25}}{4 \cos\theta_l \cos\theta_v}.$$

The factor 0.25 maps the clearcoat range [0, 1] to a strength of [0, 0.25]. The notes take no energy from the base layer for the coat, and the coat costs nothing when $c = 0$. clearcoatGloss sets $\alpha_c$; the notes do not give that map, so the code of this page takes $\alpha_c$ as a direct input.

**Sheen (2014 Addenda).** The lobe $s (1 - \cos\theta_d)^5$, with an optional tint toward the base color. This page puts it with the diffuse, so a metal has no sheen.

**The 2012 G and the 2014 change.** The 2012 notes computed G with $\alpha_g = (0.5 + r / 2)^2$ instead of $r^2$, because the specular of smooth surfaces was "too hot" against the measured data and in the opinion of the artists. For $r = 0.2$ this is $\alpha_g = 0.36$ instead of $\alpha = 0.04$. After Heitz (2014) the Addenda removed this remap for the primary lobe and kept it only for the clear coat. The code has a flag for the old form.

**Left out here.** One color channel means that specularTint and sheenTint have no effect. The subsurface parameter (a blend toward a shape inspired by the Hanrahan-Krueger model) and the anisotropic parameter (Addenda: aspect $= \sqrt{1 - 0.9\, \text{anisotropic}}$, $\alpha_x = r^2 / \text{aspect}$, $\alpha_y = r^2 \cdot \text{aspect}$) are also not in the code.

## What it counts

$f$ is a BRDF in 1/sr, the reflected radiance per unit irradiance from one direction. The directional albedo $E(\theta_v) = \int f \cos\theta_l\, d\omega_l$ is the fraction of light from one direction that leaves the surface. The notes state that the albedo of a real material must be below 1, and they show that the measured albedo of most MERL materials is almost flat for the first 70 degrees. The model does not hold to that bound in every case.

**Example: the diffuse term alone.** With $b = 1$, the albedo of $f_d$ for the view angle $\theta_v$, by quadrature in the code of this page:

| $r$ | 0° | 45° | 60° | 75° | 85° |
|---|---|---|---|---|---|
| 0 | 0.9762 | 0.9751 | 0.9609 | 0.8670 | 0.6668 |
| 0.25 | 0.9911 | 0.9899 | 0.9845 | 0.9435 | 0.8418 |
| 0.5 | 1.0060 | 1.0047 | 1.0083 | 1.0220 | 1.0224 |
| 1 | 1.0357 | 1.0344 | 1.0569 | 1.1853 | 1.4006 |

A smooth surface is darker at grazing angles than a Lambertian one, and a rough surface is brighter. At $r = 1$ the diffuse term alone reflects 40 percent more light than it receives at 85°.

**Example: a white dielectric.** With $b = 1$, specular 0.5 and $r = 1$, the full albedo is 1.0480 at 0°, 1.0756 at 60° and 1.3074 at 80°. The diffuse and specular lobes are added and the specular takes no energy from the diffuse.

**Example: a white metal.** With $b = 1$ and $m = 1$, $F = 1$, so the albedo is the single-scattering albedo of GGX with the separable Smith G. By Monte Carlo with 20000 samples:

| $r$ | 0° | 60° | 80° |
|---|---|---|---|
| 0.2 | 0.998 | 0.994 | 0.970 |
| 0.5 | 0.916 | 0.853 | 0.828 |
| 1 | 0.305 | 0.405 | 0.525 |

A smooth metal keeps almost all the light. A rough one loses much of it, because the model counts only one bounce on the microsurface.

## Relation to other models

- **[Microfacet BRDFs](/microfacet-brdf/).** The specular and clear coat lobes are microfacet lobes $DFG / (4 \cos\theta_l \cos\theta_v)$. The diffuse and sheen lobes are not derived from a microsurface; they are fits to measured data.
- **[GGX](/ggx-distribution/).** GTR with $\gamma = 2$. The notes say that GGX is equivalent to Trowbridge-Reitz and that GTR with $\gamma = 1$ comes from a form used by Berry (1923).
- **[Smith G](/smith-masking-shadowing-function/).** The 2014 revision uses the Smith G of GGX with no remap, after the weak white furnace test of Heitz showed that the Smith and V-cavity models are the plausible ones among those known.
- **[Lambertian reflectance](/lambertian-reflectance/).** If $F_{D90} = 1$ the diffuse term is $b / \pi$. Karis (2013) tested Burley diffuse for Unreal Engine 4, saw only small differences from Lambert and kept Lambert, which is also easier to use with image-based and spherical harmonic lighting.
- **[Oren-Nayar](/oren-nayar-reflectance-model/).** Another rough diffuse model, derived from V-cavities. Burley diffuse has a different shape and was chosen because it matched the MERL data and the artists liked it.
- **[Blinn-Phong](/blinn-phong-reflection-model/).** An older empirical model. Its exponent has no 0 to 1 range, it has no Fresnel term, and its normalized form is still not energy conserving.
- **Unreal Engine 4.** Karis (2013) kept BaseColor, Metallic and Roughness, replaced Specular with a constant $F_0 = 0.04$ for nonmetals and a Cavity parameter for small-scale shadowing, and treated subsurface, anisotropy, clear coat and sheen as special shading models. With the [split-sum approximation](/split-sum-approximation/) it lights the same material with analytic lights and with environment maps.

## Known results in the model

- **GTR normalization (proved).** For $\gamma = 1$ and $\gamma = 2$, the constants above give $\int D \cos\theta_h\, d\omega = 1$ for all $\alpha \in (0, 1]$; $\gamma = 1$ tends to the constant $1 / \pi$ as $\alpha \to 1$.
- **Reciprocity (proved).** Each lobe is symmetric in $l$ and $v$, so $f(l, v) = f(v, l)$, as [Helmholtz reciprocity](/helmholtz-reciprocity/) asks.
- **Metallic is a blend (proved).** Because the specular lobe is affine in $F_0$, mixing $F_0$ by $m$ gives the same specular as $(1 - m)$ times the dielectric lobe plus $m$ times the metal lobe. So the full model with the coat removed is the linear blend of a dielectric model and a metal model that the notes describe.
- **Lambert limit of the diffuse (proved).** $F_{D90} = 1$ gives $f_d = b / \pi$.
- **No energy bound (measurement).** The diffuse term alone has an albedo up to 1.40 for $r = 1$, and a white rough dielectric reaches 1.31 at 80°. Principle 5 asks for plausible combinations, not for energy conservation, and Burley lists "should we be perfectly energy conserving?" as an open design question.
- **Energy loss of rough metals (measurement).** With one bounce on the microsurface, a white metal reflects only about 0.31 of the light at normal view for $r = 1$.
- **The constants (tuning).** 0.5 and 2 in $F_{D90}$, the range 0.08 of specular, the strength 0.25 and fixed roughness 0.25 of the coat, the 2012 G remap and the map $\alpha = r^2$ are chosen to match the MERL data and to please the artists.
- **Layering (measurement of practice).** Because the parameters are normalized and close to perceptually linear, two materials blend well by interpolating their parameters, and the studio made all spatial variation with masks between material presets (Section 5.7).

## References
