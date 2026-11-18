---
tag: W0ZH9M
kind: technique
slug: schlick-fresnel-approximation
name: Schlick's Fresnel approximation
aliases:
- Schlick approximation
area: graphics-and-signals/real-time-rendering
level: core
summary: "Approximate the Fresnel reflectance by F0 + (1 - F0)(1 - cos theta)^5, where F0 is the reflectance at normal incidence. It is exact at 0 and 90 degrees and off by a few hundredths between."
prereqs: [fresnel-equations]
see_also: [microfacet-brdf, ggx-distribution, smith-masking-shadowing-function, physically-based-shading, disney-principled-brdf, split-sum-approximation, brdf, albedo]
sources:
  - paper: doi:10.1111/1467-8659.1330233
    title: Christophe Schlick, An inexpensive BRDF model for physically-based rendering, Computer Graphics Forum 13(3), 1994, 233 to 246
    locator: the approximation of the Fresnel factor by a fifth power of (1 - cos theta) (general locator)
  - paper: "Brian Karis, Real shading in Unreal Engine 4, course notes, SIGGRAPH 2013 course Physically Based Shading in Theory and Practice"
    locator: the section Specular F, Equation 5 (Schlick's form with a spherical Gaussian in place of the fifth power)
  - paper: "Brent Burley, Physically-based shading at Disney, course notes, SIGGRAPH 2012 course Practical Physically Based Shading in Film and Game Production, revised 2014"
    locator: Section 5.5, Specular F details (Schlick with the angle theta_d between l and h), and Section 5.3 for the diffuse term with the same fifth power
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.2.1, Fresnel Reflectance (the exact formulas for dielectrics and conductors that serve as the reference here)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 9, Physically Based Shading (the section on Fresnel reflectance and the Schlick approximation)
---

Schlick's approximation replaces the [Fresnel equations](/fresnel-equations/) by one short formula. With $c = \cos\theta$ for the angle of incidence and $F_0$ the reflectance at normal incidence,

$$F(c) \approx F_0 + (1 - F_0)(1 - c)^5.$$

For a dielectric with relative index $\eta$, $F_0 = ((\eta - 1) / (\eta + 1))^2$, which is 0.04 for glass with $\eta = 1.5$. Christophe Schlick proposed the form in 1994 as part of a cheap BRDF model. It is now the $F$ of nearly every real-time [microfacet BRDF](/microfacet-brdf/), where $c = v \cdot h$, the cosine between the view direction and the half vector. It is exact at normal and at grazing incidence, it rises monotonically between them, and it costs four multiplications. In between it is a fit, with errors up to about 0.04 for glass and larger for water, diamond and metals.

## In plain words

A shiny surface reflects more light when you look at it at a low angle. A lake is clear at your feet and a mirror near the horizon. The exact physics of this effect needs square roots and depends on polarization. Schlick noticed that a simple curve does almost as well. You need one number, the reflectance when you look straight at the surface. The curve starts at that number and rises to full reflection at a grazing angle, and it rises fast only near the end. For glass and water the curve is close to the exact one. For metals and inside glass it can be noticeably wrong, and the sections below show how and how much.

## When it applies

- **A dielectric seen from the less dense side.** Glass, water, plastic and paint seen from air. $F_0$ comes from the index of refraction, and the error is a few hundredths at most (measured below).
- **A metal, per color channel.** The Fresnel reflectance of a conductor has a complex index $n + ik$. Real-time code stores $F_0$ as an RGB color and uses the same formula. This keeps $F_0$ exact and the grazing value 1, but it misses the dip of the exact curve below $F_0$ near 80°.
- **Inside the dense medium only with a change.** From inside glass toward air, total internal reflection starts at the critical angle, $41.8°$ for $\eta = 1.5$. The plain formula does not see it. The fix in the template below uses the cosine of the transmitted angle.
- **A microfacet BRDF.** Each facet is a mirror with normal $h$, so the angle is between $v$ (or $l$) and $h$. Using $n \cdot v$ instead is a different model, a common mistake.

## The template

The inputs are the cosine $c$ of the angle of incidence, the reflectance $F_0$ at normal incidence, an optional grazing value $F_{90}$ (1 for the Fresnel case), and for a dielectric the index ratio $\eta = n_t / n_i$ of the far side over the near side.

```pseudo id=main
SCHLICK(c, F0, F90)
L1  c ← clamp(c, 0, 1)                         ▷ c = v·h in a microfacet BRDF
L2  m ← 1 - c
L3  return F0 + (F90 - F0) · m^5               ▷ m^5 as (m²)² · m: three products

SCHLICK-DIELECTRIC(c, η)
L4  F0 ← ((η - 1) / (η + 1))²
L5  if η < 1 then                              ▷ light leaves the denser medium
L6      s ← (1 - c²) / η²                      ▷ sin² of the transmitted angle
L7      if s ≥ 1 then return 1                 ▷ total internal reflection
L8      c ← sqrt(1 - s)                        ▷ use the transmitted cosine
L9  return SCHLICK(c, F0, 1)
```

Line L3 is the formula. At $c = 1$ it gives $F_0$ and at $c = 0$ it gives $F_{90}$, and in between it is a monotone blend, because $(1 - c)^5$ decreases with $c$. Lines L5 to L8 use a proved symmetry of the exact equations: the reflectance from inside at the angle $\theta_i$ equals the reflectance from outside at the transmitted angle $\theta_t$, so the inside error equals the outside error. The cost is $O(1)$ per evaluation, with one square root only for light inside the dense medium.

## Classic examples

**Glass from air.** $\eta = 1.5$, $F_0 = 0.04$. The table gives the exact reflectance and the error of Schlick's formula.

| Angle | 0° | 30° | 45° | 60° | 70° | 80° | 85° | 89° |
|---|---|---|---|---|---|---|---|---|
| Exact | 0.0400 | 0.0415 | 0.0502 | 0.0892 | 0.1710 | 0.3877 | 0.6128 | 0.9042 |
| Schlick | 0.0400 | 0.0400 | 0.0421 | 0.0700 | 0.1584 | 0.4099 | 0.6485 | 0.9191 |
| Error | 0 | -0.0015 | -0.0082 | -0.0192 | -0.0126 | +0.0222 | +0.0357 | +0.0149 |

The formula is too low at medium angles and too high near grazing angles. The largest error is $0.0357$ near 85°.

**Other indices.** The largest error over all angles depends on $\eta$ and is not monotone in it.

| Material | $\eta$ | $F_0$ | Largest error | At |
|---|---|---|---|---|
| Water | 1.33 | 0.020 | 0.0599 | 83.8° |
| Glass | 1.5 | 0.040 | 0.0357 | 85.0° |
| Dense flint glass | 2.0 | 0.111 | 0.0444 | 85.2° |
| Diamond | 2.4 | 0.170 | 0.0740 | 84.5° |

**Inside glass.** With $\eta = 1 / 1.5$ the critical angle is $41.81°$. At 40° the exact reflectance is $0.2453$, while the plain formula with $c = \cos 40°$ gives $0.0407$. With the transmitted cosine of lines L5 to L8 it gives $0.2456$, and past $41.81°$ both give 1.

**A metal.** For the complex index $1 + 6.7i$, chosen as an example near aluminum in green light, $F_0 = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2) = 0.9182$. The exact reflectance falls to $0.8627$ at $80.9°$ before it rises to 1, while Schlick's curve only rises. The largest error is $0.0947$ near 83°.

**The hemispherical average.** Weighted by the cosine, the average of the formula is $2 \int_0^1 F(c)\, c\, dc = F_0 + (1 - F_0) / 21$, because $2 \int_0^1 (1 - c)^5 c\, dc = 1 / 21$. For glass this is $0.0857$; the exact average is $0.0918$. Split sum and energy compensation tables use such averages.

All numbers on this page come from the code of this page, which tests the formula against the exact Fresnel equations for dielectrics and conductors.

## Variations

- **A grazing value other than 1.** $F_0 + (F_{90} - F_0)(1 - c)^5$. Burley's diffuse term uses the same fifth power with $F_{90} = 0.5 + 2 r \cos^2\theta_d$ for the roughness $r$, which is a tuned shape, not a Fresnel factor.
- **A spherical Gaussian power.** Karis (2013) replaces $(1 - c)^5$ by $2^{(-5.55473 c - 6.98316) c}$, a fit that is cheaper on some hardware. The two weights differ by at most $0.0038$, near $c = 0.055$.
- **Tinted metals.** $F_0$ as an RGB color in linear space, with the base color of a metal used as $F_0$ in metal-rough workflows.
- **Per-lobe use.** The [Disney principled BRDF](/disney-principled-brdf/) uses the fifth power for the specular $F$, for the sheen and for the clear coat with $F_0 = 0.04$.
- **Corrections for metals.** An extra term that is zero at $c = 0$ and $c = 1$, such as a multiple of $c (1 - c)^6$, can make the curve dip like the exact one (Exercise 6). Its weight is a fit per material, so it is tuning.

## Pitfalls

- **The wrong cosine.** In a microfacet BRDF, $c$ is $v \cdot h$ (equal to $l \cdot h$), not $n \cdot v$. For a rough surface, $v \cdot h$ is often larger than $n \cdot v$ at grazing view, so with $n \cdot v$ the reflection there is usually too bright.
- **Inside the medium.** Without lines L5 to L8, a refractive object shows no total internal reflection. At 40° inside glass the error is $0.20$.
- **Gamma.** $F_0$ is a reflectance in linear RGB. A value of 0.04 stored in an sRGB texture without decoding is a different number.
- **Metals near 80°.** The formula has no dip, so a metal looks slightly too bright near grazing angles. The error is about 0.09 for the example above.
- **Rounding near $c = 1$.** $1 - c$ is small and the fifth power makes it tiny; this is fine, since the term then does not matter. Clamping $c$ to $[0, 1]$ matters more, because a negative $c$ from interpolated normals gives a value above $F_{90}$.
- **Claims of accuracy.** The error figures above are measurements against the exact Fresnel equations of a smooth interface. Real materials have coatings, oxides and dispersion, and the exact formula is itself a model.

## Exercises

1. Show that $F(c)$ is monotone in $c$ and that $F_0 \le F(c) \le 1$ for $0 \le F_0 \le 1$.
2. Prove that $2 \int_0^1 (1 - c)^5 c\, dc = 1 / 21$, and compute the cosine-weighted average of the formula for water.
3. Invert $F_0 = ((\eta - 1) / (\eta + 1))^2$ to get $\eta$ from $F_0$. What $\eta$ gives $F_0 = 0.08$, the upper end of the Disney specular parameter?
4. Prove that the exact unpolarized reflectance satisfies $R(\theta_i, \eta) = R(\theta_t, 1 / \eta)$, and explain why this makes lines L5 to L8 have the same error as the outside case.
5. Find the angle where the exact reflectance of glass equals Schlick's value, between 70° and 80°.
6. For the index $1 + 6.7i$, plot the exact reflectance and the formula, and find a constant $a$ such that $F(c) - a\, c (1 - c)^6$ reduces the largest error.

## References
