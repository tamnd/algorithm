---
tag: S05FMF
kind: concept
slug: fresnel-equations
name: Fresnel equations
aliases:
- Fresnel reflectance
- Fresnel formulae
area: graphics-and-signals/ray-tracing
level: intro
summary: The fractions of light that a smooth boundary between two media reflects and transmits, by angle and polarization. Reflectance rises to 1 at grazing angles and under total internal reflection.
prereqs: [snells-law]
see_also: [microfacet-brdf, bsdf, whitted-ray-tracing, brdf, albedo, path-tracing, russian-roulette, catastrophic-cancellation]
sources:
  - book: isbn:9780521642224
    title: Max Born and Emil Wolf, Principles of Optics, seventh edition, Cambridge University Press, 1999
    locator: Section 1.5.2 (the Fresnel formulae), Section 1.5.3 (reflectivity, transmissivity and the Brewster angle) and Section 1.5.4 (total reflection); the chapter on the optics of metals for the complex index
  - paper: doi:10.1111/1467-8659.1330233
    title: Christophe Schlick, An inexpensive BRDF model for physically-based rendering, Computer Graphics Forum 13(3), 1994, 233 to 246
    locator: the approximation of the Fresnel factor by R0 + (1 − R0)(1 − cos θ)^5
  - paper: doi:10.1145/357290.357293
    title: Robert L. Cook and Kenneth E. Torrance, A reflectance model for computer graphics, ACM Transactions on Graphics 1(1), 1982, 7 to 24
    locator: the Fresnel term F of the specular component, and its dependence on angle and wavelength
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.2.1, Fresnel Reflectance (dielectrics and conductors)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 9.5, Fresnel Reflectance (external and internal reflection, typical values of R0, and the Schlick approximation)
---

The Fresnel equations give the fraction of light that a smooth, flat boundary between two media reflects, and the fraction that it transmits. The fractions depend on the angle of incidence, on the two refractive indices and on the polarization of the light. [Snell's law](/snells-law/) gives the direction of the transmitted ray; the Fresnel equations give its share of the power. For glass in air the reflectance is 4% at normal incidence and rises to 100% at grazing incidence, and inside the glass it is 100% beyond the critical angle. Renderers use the equations in the reflection and transmission of glass and water, and in the factor $F$ of every [microfacet model](/microfacet-brdf/). Real-time renderers often use Schlick's approximation in their place.

## In plain words

Look at a window. From straight in front you see through it and see only a faint reflection. Look along the glass at a shallow angle and it becomes a mirror. A lake does the same: near your feet you see the bottom, far away you see the sky. The Fresnel equations describe this change exactly.

Light is a wave that swings across its direction of travel. The equations treat two ways of swinging, one along the surface and one partly across it, and give a different answer for each. Ordinary light is an even mix of both, so a renderer usually takes the average. At one angle the second way does not reflect at all; this is why sunglasses that block the first way remove glare from water.

What is not reflected goes into the second medium, so the two fractions always add up to one.

## The idea

**Setup.** Light goes from a medium of index $n_1$ into a medium of index $n_2$. Write $\theta_1$ for the angle of incidence, $\theta_2$ for the angle of refraction, $c_1 = \cos\theta_1$ and $c_2 = \cos\theta_2$, where $n_1 \sin\theta_1 = n_2 \sin\theta_2$. The plane of incidence holds the ray and the normal. The electric field of a plane wave splits into an s component, normal to the plane of incidence (also called TE), and a p component, in the plane (also called TM). The boundary conditions of Maxwell's equations, for media that do not absorb and are not magnetic, give the ratios of the reflected and transmitted amplitudes to the incident amplitude:

$$r_s = \frac{n_1 c_1 - n_2 c_2}{n_1 c_1 + n_2 c_2}, \qquad t_s = \frac{2 n_1 c_1}{n_1 c_1 + n_2 c_2},$$

$$r_p = \frac{n_2 c_1 - n_1 c_2}{n_2 c_1 + n_1 c_2}, \qquad t_p = \frac{2 n_1 c_1}{n_2 c_1 + n_1 c_2}.$$

With Snell's law they take the angle form $r_s = -\sin(\theta_1 - \theta_2) / \sin(\theta_1 + \theta_2)$ and $r_p = \tan(\theta_1 - \theta_2) / \tan(\theta_1 + \theta_2)$ of Born and Wolf (Section 1.5.2). Books differ in the sign of $r_p$, because they choose different reference directions for the p field. The reflectance does not depend on that choice.

**Power.** The reflectance is $R = r^2$. The transmittance is not $t^2$: the transmitted beam has another speed and another cross section, and the ratio of the powers is

$$T = \frac{n_2 c_2}{n_1 c_1}\, t^2.$$

With $a = n_1 c_1$ and $b = n_2 c_2$, energy is conserved for the s wave,

$$R_s + T_s = \frac{(a - b)^2 + \frac{b}{a}(2a)^2}{(a + b)^2} = \frac{a^2 + 2ab + b^2}{(a + b)^2} = 1,$$

and the same steps with $p = n_2 c_1$, $q = n_1 c_2$ and $pq = ab$ give $R_p + T_p = 1$. Natural light from a lamp or the sun is unpolarized, with equal power in the two components, so its reflectance is

$$R = \tfrac12 (R_s + R_p), \qquad T = 1 - R.$$

**Normal incidence.** At $\theta_1 = 0$ the two components agree, and

$$R_0 = \left(\frac{n_1 - n_2}{n_1 + n_2}\right)^2.$$

Air and glass of index 1.5 give $R_0 = 0.04$, air and water give $0.020$, and air and diamond (index 2.42) give $0.172$. $R_0$ is the same for both directions of travel.

**Grazing incidence.** As $\theta_1 \to 90°$, $c_1 \to 0$ and both $r_s$ and $r_p$ tend to $-1$ when $n_1 < n_2$, so $R \to 1$. Every smooth dielectric is a perfect mirror at grazing angles.

**The Brewster angle.** $r_p = 0$ when $n_2 c_1 = n_1 c_2$. With Snell's law this holds at the angle $\theta_B$ with $\tan\theta_B = n_2 / n_1$, where the reflected and the refracted ray are at a right angle. For air and glass $\theta_B = 56.31°$. At this angle the reflected light is fully s polarized, and polarizing filters remove it.

**Total internal reflection.** For $n_1 > n_2$ and $\theta_1$ above the critical angle $\arcsin(n_2 / n_1)$, there is no real $c_2$. The reflected amplitudes become complex numbers of modulus 1, so $R_s = R_p = 1$ and $T = 0$. A field still exists on the far side, but it decays within about a wavelength and carries no power away. Just below the critical angle $c_2$ is small and $R$ rises steeply to 1.

**Reversal.** For light from the other side at the angle $\theta_2$, the coefficients $r'$ and $t'$ satisfy the Stokes relations $r' = -r$ and $t\,t' = 1 - r^2$, for each component. So the reflectance is the same for the two directions of one ray path: $R(n_1 \to n_2, \theta_1) = R(n_2 \to n_1, \theta_2)$.

**Conductors.** Metals absorb light, and their index is a complex number $\hat n = n + i\kappa$ with an extinction coefficient $\kappa$. The same formulas hold with complex arithmetic and a complex $c_2$, and the reflectance is $|r|^2$. At normal incidence from air, $R_0 = ((n - 1)^2 + \kappa^2) / ((n + 1)^2 + \kappa^2)$; for example $\hat n = 1 + 6i$ gives $R_0 = 36/40 = 0.9$. Metals have a high reflectance at all angles, which varies with the wavelength and gives gold and copper their color. A renderer stores $n$ and $\kappa$ per wavelength, or a measured $R_0$ in RGB.

**Schlick's approximation.** Schlick (1994) replaced the exact formula by

$$R \approx R_0 + (1 - R_0)(1 - c)^5,$$

which costs a few multiplications and needs only $R_0$. It is exact at $c = 1$ and $c = 0$. The cosine $c$ must be the cosine in the medium with the lower index. For light that enters the denser medium that is $c_1$. For light inside glass it is $c_2$, and the approximation must return 1 under total internal reflection; with $c_1$ inside glass the formula does not see the critical angle at all, and its error reaches 0.96. The examples below give the error with the right cosine.

**Floating point.** The value $1 - (n_1/n_2)^2 (1 - c_1^2)$ under the root loses its relative accuracy near the critical angle, where two numbers close to 1 cancel. Its sign decides between refraction and total internal reflection, and the code must use the same decision for the direction of [Snell's law](/snells-law/) and for $R$, or a ray can refract with $R = 1$. A cosine computed from a dot product can be slightly above 1 or below 0, and must be clamped to $[0, 1]$ before the root.

## Examples

**Air into glass.** For $n_1 = 1$ and $n_2 = 1.5$:

| $\theta_1$ | $\theta_2$ | $R_s$ | $R_p$ | $R$ | $T$ |
|---|---|---|---|---|---|
| $0°$ | $0°$ | 0.0400 | 0.0400 | 0.0400 | 0.9600 |
| $30°$ | $19.47°$ | 0.0578 | 0.0253 | 0.0415 | 0.9585 |
| $45°$ | $28.13°$ | 0.0920 | 0.0085 | 0.0502 | 0.9498 |
| $56.31°$ | $33.69°$ | 0.1479 | 0.0000 | 0.0740 | 0.9260 |
| $60°$ | $35.26°$ | 0.1766 | 0.0018 | 0.0892 | 0.9108 |
| $80°$ | $41.04°$ | 0.5386 | 0.2368 | 0.3877 | 0.6123 |
| $89°$ | $41.80°$ | 0.9395 | 0.8689 | 0.9042 | 0.0958 |

The reflectance stays near 4% up to about $45°$ and then climbs fast. At $45°$, $r_s = -0.3033$ and $t_s = 0.6967$, so $T_s = (1.5 \cdot 0.8819 / 0.7071) \cdot 0.6967^2 = 0.9080$ and $R_s + T_s = 0.0920 + 0.9080 = 1$. The row $56.31°$ is the Brewster angle, where $R_p = 0$.

**Glass into air.** For $n_1 = 1.5$ and $n_2 = 1$ at $\theta_1 = 30°$, $\theta_2 = 48.59°$ and $R = 0.0552$. This equals the reflectance of the reversed path, air into glass at $48.59°$. At $45°$ the ray is past the critical angle $41.81°$, and $R = 1$.

**Schlick against the exact value.** For air into glass, at $45°$ the exact $R$ is 0.0502 and Schlick gives 0.0421; at $60°$ the values are 0.0892 and 0.0700; at $80°$ they are 0.3877 and 0.4099. The largest absolute error, on a grid of angles with a step of 0.001 degree, is

| $n_2$ (from air) | largest error of Schlick | at $\theta_1$ |
|---|---|---|
| 1.333 (water) | 0.0592 | $83.8°$ |
| 1.5 (glass) | 0.0357 | $85.0°$ |
| 2.4 (diamond) | 0.0740 | $84.5°$ |

For light inside glass, with $c_2$ as the cosine and $R = 1$ beyond the critical angle, the largest error is the same 0.0357, at $41.6°$, close to the critical angle. The error is largest at grazing angles, where both values are large, so the image error is small for most materials. The tests of the implementation compute these numbers and check $R + T = 1$, total internal reflection, the Brewster angle and the Stokes relations against the angle form.

## Where it is used

- [Whitted ray tracing](/whitted-ray-tracing/) weights the reflected and the transmitted ray by $k_s$ and $k_t$. Whitted kept them constant and only suggested that they should follow the Fresnel law; later ray tracers use $R$ and $1 - R$.
- A [BSDF](/bsdf/) of smooth glass has a reflection lobe of weight $R$ and a transmission lobe of weight $1 - R$, with the $1/\eta^2$ radiance factor of [Helmholtz reciprocity](/helmholtz-reciprocity/) for the transmitted part. A [path tracer](/path-tracing/) picks one of the two with the probabilities $R$ and $1 - R$, which keeps one path per sample; the chosen ray has the weight $R / R = 1$ or $(1 - R)/(1 - R) = 1$, so the estimate stays unbiased.
- The [microfacet BRDF](/microfacet-brdf/) of Cook and Torrance multiplies by $F(\theta_h)$, the Fresnel reflectance at the angle between the light and the facet normal. Real-time renderers use Schlick's form with $R_0$ as the specular color.
- Layered materials, such as a varnish over a diffuse base, use $1 - R$ to find how much light reaches the base. A [Lambertian](/lambertian-reflectance/) base under a clear coat loses light at grazing angles, so the [albedo](/albedo/) of the layered surface depends on the angle.

### History

Augustin-Jean Fresnel derived the equations from 1821 to 1823, from his theory of light as a transverse wave in an elastic ether. David Brewster had found the angle of full polarization by experiment in 1815. James Clerk Maxwell's theory of the electromagnetic field gave the same equations from the boundary conditions on the fields, which is the derivation in Born and Wolf. In graphics, Cook and Torrance (1982) brought the Fresnel term, with its variation in angle and wavelength, into a reflection model, and Schlick (1994) gave the approximation that most real-time renderers use.

## References
