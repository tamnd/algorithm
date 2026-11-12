---
tag: K8919H
kind: model
slug: lambertian-reflectance
name: Lambertian reflectance
aliases:
- Lambert's cosine law
- diffuse reflection
- Lambertian BRDF
area: graphics-and-signals/ray-tracing
level: intro
summary: The ideal matte surface, whose BRDF is the constant ρ/π. It looks equally bright from every direction, and it reflects the fraction ρ of the light that falls on it.
prereqs: [brdf]
see_also: [albedo, microfacet-brdf, gouraud-shading, phong-shading, radiosity, path-tracing, importance-sampling, monte-carlo-integration]
sources:
  - paper: "Johann Heinrich Lambert, Photometria, sive de mensura et gradibus luminis, colorum et umbrae, Augsburg, 1760"
    locator: the cosine law for the light that a surface receives and emits, and the brightness of matte surfaces
  - paper: doi:10.6028/NBS.MONO.160
    title: Fred E. Nicodemus, Joseph C. Richmond, Jack J. Hsia, Irving W. Ginsberg and Thomas Limperis, Geometrical considerations and nomenclature for reflectance, NBS Monograph 160, National Bureau of Standards, 1977
    locator: the definition of the BRDF and the perfectly diffuse reflector, whose BRDF is the reflectance divided by π
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.3, Lambertian Reflection; Section 8.4.1, Oren-Nayar Diffuse Reflection; Section 13.6.3, Cosine-Weighted Hemisphere Sampling (Malley's method)
  - paper: doi:10.1145/192161.192213
    title: Michael Oren and Shree K. Nayar, Generalization of Lambert's reflectance model, SIGGRAPH 94, 1994, 239 to 246
    locator: the rough surface of Lambertian facets, and why such a surface is not Lambertian
---

Lambertian reflectance is the reflection model of an ideal matte surface. Such a surface scatters the light that falls on it so that its radiance is the same in every direction of view: its [BRDF](/brdf/) is the constant $f = \rho / \pi$, where $\rho$ in $[0, 1]$ is its [albedo](/albedo/). Chalk, matte paint and paper are close to Lambertian over a wide range of angles. The model is the diffuse part of almost every shading model, from the $k_d (N \cdot L)$ term of the Phong reflection model and of Whitted (1980) to the base layer of physically based materials. It is a reflection model, not a shading method: [Gouraud shading](/gouraud-shading/) and [Phong shading](/phong-shading/) decide where on a polygon a model like this one is evaluated, at the vertices or at each pixel.

## The machine

**The BRDF.** At a point with the unit normal $n$, for an incident direction $\omega_i$ and an outgoing direction $\omega_o$ on the upper hemisphere $H^2$,

$$f(\omega_i, \omega_o) = \frac{\rho}{\pi}, \qquad \text{and } f = 0 \text{ if } n \cdot \omega_i \le 0 \text{ or } n \cdot \omega_o \le 0.$$

$\rho$ is a number per wavelength, or three numbers for an RGB renderer, and it is the only parameter. The model assumes that light leaves the surface at the point where it arrives, that the surface does not polarize it, and that the reflected light has no memory of the incident direction.

**The reflected radiance.** With the BRDF in the reflection integral, the outgoing radiance is

$$L_o(\omega_o) = \int_{H^2} f\,L_i(\omega_i) \cos\theta_i \, d\omega_i = \frac{\rho}{\pi}\,E,$$

where $E = \int L_i \cos\theta_i\,d\omega_i$ is the irradiance. $L_o$ does not depend on $\omega_o$, so a renderer needs one number per point for all views. For a point light of intensity $I$ at the distance $r$ in the unit direction $l$,

$$L_o = \frac{\rho}{\pi} \cdot \frac{I \max(0, n \cdot l)}{r^2}.$$

**Two cosines.** The model has two cosine laws, and they are easy to mix up. The first is about light that arrives: a beam that meets the surface at the angle $\theta_i$ spreads over an area larger by $1/\cos\theta_i$, so the irradiance is $\cos\theta_i$ times the irradiance of the same beam at normal incidence. This holds for every surface and is the factor $\cos\theta_i$ in the integral above. The second, Lambert's cosine law proper, is about light that leaves: a flat Lambertian patch of area $A$ and radiance $L$ sends the intensity $I(\theta_o) = L A \cos\theta_o$ in the direction at the angle $\theta_o$, because its projected area shrinks by $\cos\theta_o$ while its radiance stays the same. This is why a Lambertian sphere has a uniformly bright disk at a fixed irradiance, and why the radiance, and not the intensity, is the quantity that is the same in all directions.

**Units.** Many shading formulas write the diffuse term as $k_d\,(n \cdot l)$ with no $\pi$. That is the same model with $k_d = \rho$ and the light given as the radiance that a white surface would reflect, which hides $I/(\pi r^2)$ in the light color. A physically based renderer must keep the $1/\pi$, or energy is not conserved.

## What it counts

The model predicts one number per wavelength: the outgoing radiance of a point, the same in all directions. One evaluation is a single multiplication. Under $\ell$ point lights a renderer evaluates $\ell$ terms, each with one shadow ray if shadows matter, so the cost of direct light is $O(\ell)$ rays per point. Under area lights and indirect light the reflection integral has no closed form, and a renderer estimates it by [Monte Carlo integration](/monte-carlo-integration/).

**The estimator.** Draw $N$ directions $\omega_j$ with a density $p$ on the hemisphere and use

$$\hat L_o = \frac{1}{N}\sum_{j=1}^{N} \frac{f\,L_i(\omega_j)\cos\theta_j}{p(\omega_j)}.$$

It is unbiased for every density that is positive where the integrand is not zero. Its standard deviation falls as $N^{-1/2}$. The variance depends on $p$, and the Lambertian BRDF has a density that fits it exactly, as the results below show.

## Relation to other models

- **The BRDF.** The model is the constant member of the family of [BRDFs](/brdf/). It is the only reciprocal BRDF whose outgoing radiance does not depend on the view for every incident light: that property forces $f$ to be independent of $\omega_o$, and reciprocity then makes it independent of $\omega_i$ too.
- **The Phong and Blinn-Phong reflection models.** These add a specular lobe to a Lambertian term. The diffuse term $k_d (N \cdot L)$ in Phong (1975), Blinn (1977) and Whitted (1980) is this model.
- **Shading methods.** [Polygon shading](/polygon-shading/), [Gouraud shading](/gouraud-shading/) and [Phong shading](/phong-shading/) are ways to evaluate a reflection model across a polygon. Gouraud evaluates it at the vertices and interpolates colors; Phong shading interpolates normals and evaluates it at each pixel. Either can use the Lambertian model, alone or with a specular term.
- **Rough diffuse surfaces.** Oren and Nayar (1994) modeled a rough surface as a set of tilted Lambertian facets. Shadowing and masking between the facets make such a surface brighter toward the light and flatter at grazing view, so it is not Lambertian. The full moon is the common example: its disk is nearly uniform, not darker at the rim as a Lambertian sphere lit from the front would be. The model reduces to the Lambertian one when the roughness is 0.
- **Microfacet models.** A [microfacet BRDF](/microfacet-brdf/) describes the specular reflection of a rough surface. A common material is a microfacet lobe over a Lambertian base, with the base weighted by the part of the light that the Fresnel term lets through.
- **Subsurface scattering.** A Lambertian surface is the limit of a [BSSRDF](/bssrdf/) for a medium that scatters a great deal at a scale below one pixel: the light enters, scatters many times, and leaves with no memory of its direction. When the scattering distance is visible, as in skin or marble, the model is not enough.
- **Radiosity.** The [radiosity](/radiosity/) method assumes that all surfaces are Lambertian, so that each patch has one radiance for all directions and the [rendering equation](/rendering-equation/) becomes a linear system with one unknown per patch.

## Known results in the model

**Reciprocity.** $f(\omega_i, \omega_o) = f(\omega_o, \omega_i)$, trivially, so the model obeys [Helmholtz reciprocity](/helmholtz-reciprocity/), and light can be traced from the camera or from the light with the same BRDF.

**Albedo and energy conservation.** For every $\omega_o$ the directional albedo is

$$\int_{H^2} \frac{\rho}{\pi} \cos\theta_i \, d\omega_i = \frac{\rho}{\pi} \int_0^{2\pi}\!\!\int_0^{\pi/2} \cos\theta \sin\theta \, d\theta \, d\phi = \frac{\rho}{\pi} \cdot \pi = \rho.$$

So the model conserves energy exactly when $\rho \le 1$, and $\rho$ is both its parameter and its albedo. The constant $1/\pi$ is the value that makes this true.

**The furnace test.** Under a uniform environment of radiance $L$, $E = \pi L$ and $L_o = \rho L$ in every direction. A renderer that shows a Lambertian sphere under a white sky with a radiance other than $\rho L$, or with visible shading, has a bug. This is the white furnace test of path tracers.

**Cosine-weighted sampling.** The density $p(\omega) = \cos\theta / \pi$ is a normalized density on the hemisphere, by the albedo integral with $\rho = 1$. Malley's method draws from it: draw a point uniform on the unit disk and lift it to the hemisphere, $z = \sqrt{1 - x^2 - y^2}$. The disk has the density $1/\pi$ per unit area, and the projection of a small solid angle $d\omega$ onto the disk has the area $\cos\theta \, d\omega$, so the lifted direction has the density $\cos\theta / \pi$. Under it, the angle satisfies $P(\theta \le a) = \sin^2 a$ and $E[\cos\theta] = 2/3$.

**Zero variance for the albedo.** With $p = \cos\theta/\pi$ and $L_i = 1$, each sample of the estimator is $(\rho/\pi)\cos\theta / (\cos\theta / \pi) = \rho$, so the estimate of the albedo is exact for any $N$. Under a general $L_i$ each sample is $\rho\,L_i(\omega_j)$, so the variance is $\rho^2 \operatorname{Var}[L_i]$ and comes only from the light. With uniform sampling, $p = 1/(2\pi)$, each sample of the albedo is $2\rho\cos\theta$ with the mean $\rho$ and the variance $4\rho^2 E[\cos^2\theta] - \rho^2 = \rho^2/3$. For $\rho = 0.7$ and $N = 100$ the standard error is $0.7 / \sqrt{300} = 0.040$, against 0 for cosine sampling. This is [importance sampling](/importance-sampling/) with a density proportional to the BRDF times the cosine.

**Interreflection in a closed room.** Inside a sphere whose wall has albedo $\rho$ and emits the radiance $L_e$ uniformly, each point of the wall sees the whole wall, so the irradiance from the wall is $\pi L$ and $L = L_e + \rho L$. The solution is $L = L_e / (1 - \rho)$, the sum $L_e (1 + \rho + \rho^2 + \cdots)$ of the bounces. For $\rho = 0.9$ the wall is 10 times as bright as its own emission, and a path tracer needs about 10 bounces per path on average before the paths stop contributing; with [Russian roulette](/russian-roulette/) at the probability $\rho$ the expected path length is $1/(1 - \rho) = 10$. This is the principle of the integrating sphere of photometry.

**A worked point light.** A surface with $\rho = 0.5$, lit by a point light of intensity $I = 100$ at the distance $r = 2$ with $n \cdot l = 0.8$, has the irradiance $E = 100 \cdot 0.8 / 4 = 20$ and the radiance $L_o = (0.5/\pi) \cdot 20 = 3.183$ in every direction.

**Limits.** No real material is Lambertian at all angles. Matte surfaces become more specular toward grazing angles, where the Fresnel reflectance of their outer layer rises, and rough surfaces scatter back toward the light. Pressed powders of barium sulfate or sintered PTFE come close and are used as reflectance standards. The tests of the implementation check reciprocity, the albedo integral by Gauss-Legendre quadrature in $\cos\theta$, the zero variance of cosine sampling, and the distribution of the sampled angles, with a fixed seed and bounds of four standard errors.

## References
