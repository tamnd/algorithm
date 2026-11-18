---
tag: 3J4E53
kind: model
slug: blinn-phong-reflection-model
name: Blinn-Phong reflection model
aliases:
- Blinn-Phong model
- modified Phong model
area: graphics-and-signals/real-time-rendering
level: intro
summary: "An empirical reflection model that adds ambient, diffuse and a specular lobe built on the half vector between the light and view directions."
prereqs: [brdf]
see_also: [phong-shading, gouraud-shading, lambertian-reflectance, microfacet-brdf, ggx-distribution, physically-based-shading, gooch-shading, toon-shading]
sources:
  - paper: doi:10.1145/965141.563893
    title: James F. Blinn, Models of light reflection for computer synthesized pictures, Computer Graphics (SIGGRAPH 77) 11(2), 1977, 192 to 198
    locator: the specular term with the half vector H and the exponent of N.H, and its comparison with the Phong term and the Torrance-Sparrow model (general locator)
  - paper: doi:10.1145/360825.360839
    title: Bui Tuong Phong, Illumination for computer generated pictures, Communications of the ACM 18(6), 1975, 311 to 317
    locator: the reflection model with the power of the cosine between the reflected direction and the view direction (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 5, Shading Basics, and Chapter 9, Physically Based Shading (the Blinn-Phong distribution as a microfacet D) (general locator)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.4, Microfacet Models (the microfacet framework into which a normalized Blinn-Phong D fits)
---

The Blinn-Phong reflection model shades a point as the sum of an ambient term, a [Lambertian](/lambertian-reflectance/) diffuse term and a specular highlight. For a light in the direction $l$, a view direction $v$ and the unit normal $n$, all pointing away from the surface, the highlight uses the half vector $h = (l + v) / \lVert l + v \rVert$:

$$I = k_a + E \big(k_d \max(0, n \cdot l) + k_s \max(0, n \cdot h)^s\big),$$

where $E$ is the light intensity and $s$ the shininess exponent. Bui Tuong Phong (1975) used the power of $r \cdot v$, the cosine between the mirror direction $r$ of $l$ and the view. James Blinn (1977) replaced it by the power of $n \cdot h$, which is cheaper when $l$ and $v$ are constant over a surface and which has a better shape at grazing angles. It was the fixed-function lighting model of OpenGL and Direct3D and is still common where cost matters. The model is a heuristic: its terms were chosen to look plausible, not derived from optics. A normalized form fits into the [microfacet](/microfacet-brdf/) framework, where it is close to the Beckmann distribution.

## The machine

**Inputs.** Unit vectors $n$, $l$ and $v$; the ambient, diffuse and specular coefficients $k_a$, $k_d$ and $k_s$ in linear RGB; the exponent $s \ge 0$; the intensity $E$ of each light. For several lights the light terms are summed.

**The classic form.** The equation above. The specular term is set to zero when $n \cdot l \le 0$, so a light behind the surface does not cause a highlight. The ambient term $k_a$ is a constant that stands in for all indirect light. No term has a unit; the coefficients are tuned by eye.

**The half vector.** $h$ is the normal that a mirror facet must have to reflect $l$ into $v$. The highlight is brightest when $h = n$, which is exactly when $v$ is the mirror direction of $l$. This is the link to microfacet theory: $(n \cdot h)^s$ measures how many facets are oriented to reflect $l$ into $v$.

**The normalized BRDF.** To use the model with physically based lights, replace the coefficients by reflectances and divide by solid angle:

$$f(l, v) = \frac{k_d}{\pi} + k_s \frac{s + 8}{8 \pi} (n \cdot h)^s.$$

The factor $(s + 8) / (8\pi)$ is a common choice that keeps the specular albedo near $k_s$ for all $s$; it is a convenient approximation, not an exact normalization (see below). The units of $f$ are 1/sr.

**The distribution form.** As a microfacet $D$, the normalized lobe is $D(h) = \frac{s + 2}{2\pi} (n \cdot h)^s$, and this one is exact: $\int D (n \cdot h)\, d\omega_h = 1$ for every $s \ge 0$. It goes into $f = D F G / (4 (n \cdot l)(n \cdot v))$ like [GGX](/ggx-distribution/).

## What it counts

The classic form counts nothing physical. It gives a brightness in $[0, k_a + E(k_d + k_s)]$, which the display code clamps. The normalized BRDF is a ratio of reflected radiance to incoming irradiance, and its directional albedo $\int f\, (n \cdot l)\, d\omega_l$ is the fraction of light that it reflects.

**Example.** The specular albedo of $\frac{s + 8}{8\pi} (n \cdot h)^s$, computed by the code of this page:

| $s$ | 1 | 4 | 16 | 64 | 256 |
|---|---|---|---|---|---|
| View at 0° | 1.0243 | 1.0625 | 1.0669 | 1.0267 | 1.0075 |
| View at 60° | 0.8388 | 0.5938 | 0.3702 | 0.2811 | 0.2578 |

At normal view the albedo has the closed form $(s + 8)\big(2 (1 - c_0^{s + 4}) / (s + 4) - (1 - c_0^{s + 2}) / (s + 2)\big)$ with $c_0 = 1 / \sqrt 2$. It is 1 at $s = 0$, tends to 1 as $s \to \infty$, and peaks at $1.0752$ near $s = 8.76$. So the factor reflects up to 7.5 percent more light than it receives at normal view. At 60° the albedo falls well below 1, because the lobe of $(n \cdot h)^s$ is cut off by the horizon and there is no Fresnel or masking term. Both effects are small next to the errors of the classic model, but they show that the factor is a heuristic.

**Example of the shape.** For $v$ at 75° from the normal, $s = 40$, and a light 0.2 radians from the mirror direction: in the plane of incidence, the lobe is $0.818$; across that plane, at the same angular distance, it is $0.062$. The Phong lobe $(r \cdot v)^{10}$ gives $0.818$ in both directions, because it is round around $r$. The Blinn highlight on a flat floor at a grazing view is therefore stretched toward the viewer, much like the long reflections of street lights on a wet road. The code of this page tests these values.

## Relation to other models

- **Phong.** $\max(0, r \cdot v)^p$ with $r = 2 (n \cdot l) n - l$. At normal view, $r \cdot v = \cos 2\theta_h$ and $n \cdot h = \cos\theta_h$, and $\cos^p 2\theta \approx e^{-2 p \theta^2}$, $\cos^{4p}\theta \approx e^{-2 p \theta^2}$ for small $\theta$, so $s \approx 4p$ gives about the same highlight. This rule holds only near normal view and near the peak. The Phong reflection model is a different thing from [Phong shading](/phong-shading/), which interpolates normals across a triangle; both can be used together or apart, and [Gouraud shading](/gouraud-shading/) interpolates the result instead.
- **Lambert.** The diffuse term $k_d \max(0, n \cdot l)$ is Lambert's cosine law, and $k_d / \pi$ is the [Lambertian BRDF](/lambertian-reflectance/).
- **Microfacet models.** The normalized $D = \frac{s + 2}{2\pi} (n \cdot h)^s$ is a valid microfacet distribution. Near its peak it is close to Beckmann with $s \approx 2 / \alpha^2 - 2$, a common fit. GGX has a much longer tail than both.
- **Physically based shading.** [Physically based shading](/physically-based-shading/) replaced the classic model in most engines after about 2010, with GGX for $D$, a Smith $G$ and Schlick's $F$. Some engines keep Blinn-Phong as a cheap $D$.
- **Stylized shading.** [Gooch shading](/gooch-shading/) and [toon shading](/toon-shading/) replace the diffuse term and often keep a Blinn-Phong highlight.

## Known results in the model

- **Reciprocity (proved).** $h$ is symmetric in $l$ and $v$, so the normalized BRDF is symmetric. The Phong lobe is also symmetric, because $r(l) \cdot v = 2 (n \cdot l)(n \cdot v) - l \cdot v = r(v) \cdot l$.
- **Normalization of $D$ (proved).** $\int_{H^2} \frac{s + 2}{2\pi} (n \cdot h)^{s + 1}\, d\omega_h = (s + 2) \int_0^1 \mu^{s + 1}\, d\mu = 1$.
- **Albedo of the $(s + 8) / (8\pi)$ factor (proved at normal view, measured elsewhere).** The closed form above, with a largest value of $1.0752$; at other angles the values in the table are quadrature results.
- **No energy conservation of the classic form (proved).** For $k_d + k_s > 1$ the classic form can return more light than it receives; nothing in the model prevents it.
- **Lobe shape (measured).** The highlight is round at normal view and stretched in the plane of incidence at grazing views, while Phong's stays round.
- **Fit to real materials (measurement).** How well the model fits a material is a measurement for that material. With a Fresnel and a masking term in the microfacet form, it behaves like Beckmann.

## References
