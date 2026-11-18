---
tag: TGP977
kind: model
slug: oren-nayar-reflectance-model
name: Oren-Nayar reflectance model
aliases:
- Oren-Nayar model
area: graphics-and-signals/real-time-rendering
level: advanced
summary: "A diffuse model for rough surfaces made of Lambertian V-cavity facets. Compared with Lambert, it scatters more light back toward the light source and gives rough objects a flatter look."
prereqs: [lambertian-reflectance]
see_also: [brdf, microfacet-brdf, disney-principled-brdf, physically-based-shading, smith-masking-shadowing-function, blinn-phong-reflection-model, albedo, helmholtz-reciprocity]
sources:
  - paper: doi:10.1145/192161.192213
    title: Michael Oren and Shree K. Nayar, Generalization of Lambert's reflectance model, SIGGRAPH 94, 1994, 239 to 246
    locator: Section 3 (the V-cavity roughness model), Section 4.3 (the model for a Gaussian slope-area distribution and its functional approximation, Equation 27), Section 4.4 (the qualitative model, Equation 30), Section 5 (experiments) and Section 6 (implications for graphics)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.4.1, Oren-Nayar Diffuse Reflection
  - paper: "Brent Burley, Physically-based shading at Disney, course notes, SIGGRAPH 2012 course Practical Physically Based Shading in Film and Game Production, revised 2014"
    locator: Section 5.3, Diffuse model details (an empirical rough diffuse term used in place of Oren-Nayar)
---

The Oren-Nayar model describes the diffuse reflection of rough matte surfaces such as clay, plaster, concrete, sand and cloth. A [Lambertian](/lambertian-reflectance/) surface has a constant BRDF, so a Lambertian sphere lit from the viewer is bright in the center and dark at the rim. Real rough objects do not look like that: Oren and Nayar (1994) showed a clay vase that is almost equally bright over its whole surface, and the full moon is a well-known case of the same effect. They modeled the surface as many small V-shaped cavities whose faces are Lambertian, and computed the reflection with masking, shadowing and interreflection between the faces. The result has a roughness parameter $\sigma$; at $\sigma = 0$ it is Lambert's model. Their qualitative model, the form used in most renderers, is

$$f(l, v) = \frac{\rho}{\pi}\Big(A + B \max\big(0, \cos(\phi_v - \phi_l)\big) \sin\alpha \tan\beta\Big),$$

with $A = 1 - 0.5\, \sigma^2 / (\sigma^2 + 0.33)$, $B = 0.45\, \sigma^2 / (\sigma^2 + 0.09)$, $\alpha = \max(\theta_l, \theta_v)$ and $\beta = \min(\theta_l, \theta_v)$. The roughness lowers the reflection near the normal and adds a term that is large when the viewer is near the light (backscatter).

## The machine

**The surface.** A height field made of long symmetric V-cavities, each with two flat Lambertian faces of albedo $\rho$. The slopes of the faces have a Gaussian distribution with mean 0 and standard deviation $\sigma$ (in radians), and the cavities have all orientations in the plane (Oren and Nayar 1994, Sections 3 and 4.3). The cavities are much larger than the wavelength, so geometric optics applies, and much smaller than a pixel.

**Directions.** $l$ and $v$ have the polar angles $\theta_l$ and $\theta_v$ from the normal and the azimuths $\phi_l$ and $\phi_v$. All vectors point away from the surface.

**The full model.** For one cavity orientation the paper computes the radiance of each face with masking and shadowing, plus a two-bounce interreflection term, and averages over the Gaussian distribution. The average has no closed form, so the paper fits a functional approximation (Equation 27) with three coefficients $C_1$, $C_2$, $C_3$ and a separate interreflection term.

**The qualitative model.** Section 4.4 drops $C_3$ and the interreflection term, which numerical tests showed to be small, and keeps the formula above (Equation 30). The constants 0.33, 0.09 and 0.45 are fitted to the numerical model, so they are tuning, not derived values. For rendering with unit vectors, $\sin\alpha \tan\beta = \sin\theta_l \sin\theta_v / \max(\cos\theta_l, \cos\theta_v)$ and $\cos(\phi_v - \phi_l) \sin\theta_l \sin\theta_v = l \cdot v - (n \cdot l)(n \cdot v)$, so

$$f = \frac{\rho}{\pi}\Big(A + B\, \frac{\max\big(0,\ l \cdot v - (n \cdot l)(n \cdot v)\big)}{\max(n \cdot l,\ n \cdot v)}\Big)$$

needs no trigonometric functions.

## What it counts

$f$ is a BRDF in 1/sr: reflected radiance per unit irradiance. The $A$ term is a Lambertian term scaled down. The $B$ term counts light that the faces turned toward the light reflect back toward it. When $v$ is on the same side as $l$, the faces that the viewer sees are mostly the lit ones; on the far side, the viewer sees mostly the faces in shadow, and the term is 0.

**Example.** With $\rho = 1$:

| $\sigma$ | $A$ | $B$ | $\pi f$, both at 60°, same side | $\pi f$, both at 60°, opposite sides |
|---|---|---|---|---|
| 0 | 1 | 0 | 1 | 1 |
| 0.25 | 0.9204 | 0.1844 | 1.1970 | 0.9204 |
| 0.5 | 0.7845 | 0.3309 | 1.2808 | 0.7845 |
| 1 | 0.6241 | 0.4128 | 1.2433 | 0.6241 |

**The flat look.** For a sphere lit from the viewer, $l = v$ and the radiance at the angle $\theta$ from the center is proportional to $\cos\theta\, (A + B \sin\theta \tan\theta)$:

| $\sigma$ | 0° | 30° | 60° | 80° |
|---|---|---|---|---|
| 0 (Lambert) | 1 | 0.866 | 0.5 | 0.1736 |
| 0.5 | 0.7845 | 0.7621 | 0.6404 | 0.4571 |
| 1 | 0.6241 | 0.6437 | 0.6217 | 0.5088 |

At $\sigma = 1$ the brightness changes by about 20 percent between the center and 80°, while the Lambertian sphere loses 83 percent. The paper reports the same flattening for its rendered spheres (Section 6).

**The albedo.** With $\rho = 1$ and the light at the angle $\theta_l$, the directional albedo $\int f \cos\theta_v\, d\omega_v$ is:

| $\sigma$ | 0° | 30° | 60° | 80° | 89° |
|---|---|---|---|---|---|
| 0.25 | 0.9204 | 0.9428 | 0.9754 | 1.0012 | 1.0116 |
| 0.5 | 0.7845 | 0.8247 | 0.8831 | 0.9295 | 0.9481 |
| 1 | 0.6241 | 0.6743 | 0.7472 | 0.8049 | 0.8282 |

At normal incidence the albedo is exactly $A$, because $\tan\beta = 0$ for every $v$. The qualitative model loses light at high roughness, partly because it drops the interreflections, and it gives slightly more than 1 for small $\sigma$ at grazing light. These values come from the code of this page, which checks the 2D quadrature against a 1D integral.

## Relation to other models

- **[Lambertian reflectance](/lambertian-reflectance/).** $\sigma = 0$ gives $A = 1$, $B = 0$ and $f = \rho / \pi$ for all directions.
- **[Microfacet BRDFs](/microfacet-brdf/).** The same idea, a statistical surface of flat faces with masking and shadowing, but with diffuse faces instead of mirrors. The masking and shadowing come from V-cavities, as in the $G$ of Torrance and Sparrow, not from the [Smith model](/smith-masking-shadowing-function/).
- **Burley diffuse.** The [Disney principled BRDF](/disney-principled-brdf/) uses an empirical diffuse term instead, which also changes with roughness and gives rough surfaces a brighter grazing response. Burley chose it because it gave a reasonable match to measured materials. Many real-time engines use Lambert or Burley diffuse instead of Oren-Nayar.
- **Moon reflectance.** The paper lists older models of lunar reflectance and Smith's shadowing of rough surfaces as earlier work on backscatter.

## Known results in the model

- **Lambert limit (proved).** At $\sigma = 0$ the model is Lambert's.
- **Reciprocity (proved).** $\alpha$, $\beta$ and $\cos(\phi_v - \phi_l)$ are symmetric in $l$ and $v$, so $f(l, v) = f(v, l)$.
- **Backscatter (proved for the formula).** For fixed $\theta_l$ and $\theta_v$, $f$ is largest when the azimuths are equal and is $\rho A / \pi$ whenever they differ by 90° or more.
- **Albedo at normal incidence (proved).** Equal to $\rho A$, which is below $\rho$ for $\sigma > 0$.
- **Accuracy of the qualitative model (measurement).** Oren and Nayar compare the model with measured samples such as wall plaster and report a close match, with larger errors where interreflection matters (Section 5). How well it fits another material is a measurement for that material.
- **The constants (tuning).** 0.33, 0.09 and 0.45 are fitted to numerical evaluations of the full model.

## References
