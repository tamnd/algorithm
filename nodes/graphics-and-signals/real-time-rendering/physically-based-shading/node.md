---
tag: FJ8RDV
kind: concept
slug: physically-based-shading
name: Physically based shading
aliases:
- PBR shading
area: graphics-and-signals/real-time-rendering
level: core
summary: "Shading with reflectance models that aim to obey reciprocity and energy conservation, such as microfacet BRDFs, so that one set of material parameters works under all lights."
prereqs: [brdf, rendering-equation]
see_also: [microfacet-brdf, ggx-distribution, smith-masking-shadowing-function, schlick-fresnel-approximation, disney-principled-brdf, image-based-lighting, tone-mapping, deferred-shading]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 9, Physically Based Shading (general locator)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 5.6.1, The BRDF (reciprocity and energy conservation), and Chapter 8, Reflection Models
  - paper: "Brent Burley, Physically-based shading at Disney, course notes, SIGGRAPH 2012 course Practical Physically Based Shading in Film and Game Production, revised 2014"
    locator: Section 4 (observations of the MERL 100 measured materials, with the directional albedo) and Section 5.1 (the principles of an artist-friendly model)
  - paper: "Brian Karis, Real shading in Unreal Engine 4, course notes, SIGGRAPH 2013 course Physically Based Shading in Theory and Practice"
    locator: the goals of the shading model, the sections Shading Model and Material Model
  - paper: "Eric Heitz, Johannes Hanika, Eugene d'Eon and Carsten Dachsbacher, Multiple-scattering microfacet BSDFs with the Smith model, ACM Transactions on Graphics 35(4), 2016"
    locator: the energy lost by single-scattering microfacet models at high roughness (general locator)
  - paper: "Christopher Kulla and Alejandro Conty, Revisiting physically based shading at Imageworks, course notes, SIGGRAPH 2017 course Physically Based Shading in Theory and Practice"
    locator: the energy compensation of rough microfacet lobes (general locator)
---

Physically based shading is a way to build the materials of a renderer from reflectance models that respect the main laws of light reflection, instead of from formulas tuned by eye for each scene. The core object is the [BRDF](/brdf/) $f(l, v)$, which the [rendering equation](/rendering-equation/) integrates against the incoming light. A physically based BRDF is reciprocal and does not reflect more light than it receives, and its specular part is usually a [microfacet BRDF](/microfacet-brdf/) with a normal distribution, a masking term and a Fresnel term. The materials then have parameters such as a base color, a metal flag and a roughness. Because the model, not the artist, decides how a material reacts to light, one material is meant to keep its look under a sun, a lamp or an environment map. Burley (2012) for Disney and Karis (2013) for Unreal Engine 4 describe two production systems of this kind.

## In plain words

Older shading used a few tricks that each artist tuned until the picture looked right. When the light changed, the tricks often needed new tuning. Physically based shading starts from two facts about real surfaces. Light that goes in one way and out the other way is reflected the same amount if you reverse the path. And a surface that is not a light source cannot send out more light than it gets. On top of those facts, the shiny part of a surface is treated as many tiny mirrors that point in slightly different directions. The artist then sets a few simple values, such as the color and how rough the surface is, and the model works out the rest. The same material then works in many scenes.

## The idea

**Two properties of a BRDF.** For a surface that does not emit or fluoresce, these hold (laws, see [BRDF](/brdf/)):

- Reciprocity: $f(l, v) = f(v, l)$ ([Helmholtz reciprocity](/helmholtz-reciprocity/)).
- Energy conservation: the directional albedo $E(v) = \int_{H^2} f(l, v)\, (n \cdot l)\, d\omega_l$ is at most 1 for every $v$.

A shading model is physically based when it is built to satisfy these two properties and $f \ge 0$. Many models used in practice satisfy them only approximately; the examples below give numbers.

**The microfacet form.** The specular part is

$$f_s(l, v) = \frac{D(h)\, F(v \cdot h)\, G(l, v)}{4\, (n \cdot l)(n \cdot v)},$$

where $h$ is the half vector, $D$ is the density of facet normals ([GGX](/ggx-distribution/) in most engines), $G$ is the fraction of facets that are visible from both directions ([Smith](/smith-masking-shadowing-function/)) and $F$ is the Fresnel reflectance of one facet ([Schlick's approximation](/schlick-fresnel-approximation/)). The derivation is on the [microfacet BRDF](/microfacet-brdf/) page. A diffuse term, often [Lambertian](/lambertian-reflectance/), is added for the light that enters the material and leaves it again.

**Parameters.** Instead of a specular power and a specular color, the material has a base color, a metallic value and a roughness, as in the [Disney principled BRDF](/disney-principled-brdf/). Roughness sets the width of $D$, usually through $\alpha = r^2$. Dielectrics get a small, gray reflectance at normal incidence, about 0.04 for an index of refraction of 1.5, and metals get a colored one equal to the base color and no diffuse term. These parameters are artist controls on a 0 to 1 scale, not measured quantities (Burley 2012, Section 5.1).

**Linear light.** The model computes radiance, so all lighting is done in linear values with high dynamic range. [Tone mapping](/tone-mapping/) and then [gamma correction](/gamma-correction/) turn the result into display values at the end.

**What "physically based" does not mean.** The models are fits and approximations. Their constants are tuning, and how close a model is to a real material is a measurement for that material.

## Examples

**Normalization.** The old Blinn-Phong lobe $(n \cdot h)^s$, used as a BRDF with no factor, reflects at normal view a fraction 2.86 of the incoming light for $s = 1$, 1.12 for $s = 16$ and 0.096 for $s = 256$ (closed form on the [Blinn-Phong](/blinn-phong-reflection-model/) page). So an artist who sharpens the highlight also makes the material much darker. With the factor $(s + 8) / (8\pi)$ the same fractions are 1.024, 1.067 and 1.008, and the highlight gets brighter as it gets smaller, while the total stays near the light received.

**Fresnel.** Glass with $F_0 = 0.04$ reflects 4 percent of the light at normal incidence and about 39 percent at 80°. A material with a Fresnel term shows this rise at grazing angles with no extra parameter.

**Energy loss of single scattering.** A white metal with the GGX $D$, the separable Smith $G$ and $F = 1$ reflects about 0.998 of the light at roughness 0.2 but only about 0.31 at roughness 1, for a normal view (measured by Monte Carlo on the [Disney](/disney-principled-brdf/) page). The light that the model loses is the light that bounces more than once between facets. Heitz, Hanika, d'Eon and Dachsbacher (2016) model these bounces, and Kulla and Conty (2017) add a compensation term for them. So "energy conserving" for a single-scattering model means "at most 1", not "equal to 1 for a white material".

**Energy gain.** The empirical Burley diffuse term reflects up to 1.40 of the light at roughness 1 and grazing view. It is reciprocal but not energy conserving, by design: it fits measured data.

## Where it is used

- **Film.** Disney used a physically based model with artist parameters for Wreck-It Ralph (Burley 2012). Offline renderers such as the one in Pharr, Jakob and Humphreys use the same BRDF properties for path tracing.
- **Games.** Unreal Engine 4 adopted a reduced Disney model with base color, metallic, roughness and a cavity value (Karis 2013). The same parameters are stored in the G-buffer of [deferred shading](/deferred-shading/).
- **Image-based lighting.** [Image-based lighting](/image-based-lighting/) with the [split-sum approximation](/split-sum-approximation/) applies the same microfacet BRDF to an environment map, so analytic lights and environment light agree.
- **Material authoring.** Because the parameters are on 0 to 1 scales and blend well, studios build materials by masking between a library of presets.

## References
