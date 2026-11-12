---
tag: DYEFKR
kind: concept
slug: snells-law
name: Snell's law
aliases:
- law of refraction
- Snell-Descartes law
area: graphics-and-signals/ray-tracing
level: intro
summary: Light that crosses from one medium into another bends so that n1 sin θ1 = n2 sin θ2. Ray tracers use a vector form that also detects total internal reflection.
prereqs: [dot-product]
see_also: [fresnel-equations, bsdf, whitted-ray-tracing, helmholtz-reciprocity, spectral-rendering, path-tracing, photon-mapping, point-projection-and-reflection]
sources:
  - book: isbn:9780521642224
    title: Max Born and Emil Wolf, Principles of Optics, seventh edition, Cambridge University Press, 1999
    locator: Section 1.5.1 (the laws of reflection and refraction from the boundary conditions of a plane wave) and Section 3.3.2 (the principle of Fermat)
  - paper: doi:10.1145/358876.358882
    title: Turner Whitted, An improved illumination model for shaded display, Communications of the ACM 23(6), 1980, 343 to 349
    locator: Section 2, Improved Model (the vector formulas for the reflected direction R and the transmitted direction P, and T = 0 when the root is imaginary)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 8.2, Specular Reflection and Transmission (Snell's law, the Refract function and total internal reflection)
  - paper: doi:10.1086/355456
    title: Roshdi Rashed, A pioneer in anaclastics, Ibn Sahl on burning mirrors and lenses, Isis 81(3), 1990, 464 to 491
    locator: the whole paper (the law of refraction in the treatise of Ibn Sahl of about 984)
---

Snell's law says how a ray of light bends when it crosses the boundary between two transparent media, such as air and glass. If $n_1$ and $n_2$ are the refractive indices of the two media and $\theta_1$ and $\theta_2$ are the angles of the incident and the refracted ray to the surface normal, then $n_1 \sin\theta_1 = n_2 \sin\theta_2$, and the two rays and the normal lie in one plane. A ray tracer uses the law in a vector form that computes the refracted direction from the incident direction and the normal with a few [dot products](/dot-product/) and one square root. When $n_1 > n_2$ and the incident angle is large, the law has no solution: all the light is reflected. This is total internal reflection. Snell's law gives only the direction; the [Fresnel equations](/fresnel-equations/) give how much of the light goes in that direction.

## In plain words

Light moves more slowly in glass or water than in air. The refractive index of a medium tells how much more slowly. When a ray goes from a fast medium into a slow one, it bends toward the line that stands straight up from the surface. When it goes from a slow medium into a fast one, it bends away from that line.

Think of a lifeguard who runs on sand and then swims to a person in the water. The fastest route is not a straight line, because running is faster than swimming. Light takes the fastest route too, and Snell's law describes the bend of that route.

If light inside glass hits the surface at a shallow angle, the bend would have to be more than a right angle. That is not possible, so the light cannot get out, and the surface acts as a perfect mirror.

## The idea

**The law.** The refractive index of a medium is $n = c / v$, the speed of light in vacuum divided by its speed in the medium. Air has $n \approx 1.000$, water $n \approx 1.333$ and common glass $n \approx 1.5$. At a smooth boundary, an incident ray at the angle $\theta_1$ from the normal continues on the other side at the angle $\theta_2$ with

$$n_1 \sin\theta_1 = n_2 \sin\theta_2,$$

and the refracted ray lies in the plane of the incident ray and the normal, on the other side of the normal. The reflected ray lies in the same plane at the angle $\theta_1$. In wave optics both facts follow from the boundary conditions on the electric and magnetic fields: the phase of the incident, the reflected and the transmitted wave must agree along the whole boundary, so the three waves have the same tangential component of the wave vector, and the length of the wave vector is proportional to $n$ (Born and Wolf, Section 1.5.1).

**Fermat's principle.** In geometrical optics the law follows from the principle that light takes a path of stationary travel time. Put the boundary on the line $y = 0$, a point $A = (0, a)$ above it in medium 1 and a point $B = (\ell, -b)$ below it in medium 2. A path that crosses the boundary at $(x, 0)$ takes the time

$$T(x) = \frac{1}{c}\left(n_1 \sqrt{x^2 + a^2} + n_2 \sqrt{(\ell - x)^2 + b^2}\right).$$

Each term is a strictly convex function of $x$, so $T$ has exactly one minimum, where

$$T'(x) = \frac{1}{c}\left(n_1 \frac{x}{\sqrt{x^2 + a^2}} - n_2 \frac{\ell - x}{\sqrt{(\ell - x)^2 + b^2}}\right) = \frac{1}{c}\,(n_1 \sin\theta_1 - n_2 \sin\theta_2) = 0.$$

The quantity $n$ times the length is the optical path length, and the law says that the optical path length of the real path is stationary. For a flat boundary the stationary point is the minimum; for curved mirrors and lenses it can be a saddle or a maximum.

**The vector form.** Let $d$ be the unit direction of the incident ray, $n$ the unit normal on the side of the incident ray, so that $n \cdot d < 0$, and $\eta = n_1 / n_2$. Write $c = \cos\theta_1 = -n \cdot d$. The direction $d$ splits into a part $d_\parallel = d + c\,n$ along the surface, of length $\sin\theta_1$, and the part $-c\,n$ along the normal. By the law, the part of the refracted direction $t$ along the surface has length $\sin\theta_2 = \eta \sin\theta_1$ and the same direction, so it is $\eta\,d_\parallel$. The part along the normal points into medium 2 and has length $\cos\theta_2 = \sqrt{1 - \sin^2\theta_2}$. Together,

$$t = \eta\,d + \left(\eta\,c - \sqrt{k}\right) n, \qquad k = 1 - \eta^2 (1 - c^2).$$

The vector $t$ has unit length, since $|\eta\,d_\parallel|^2 + k = \eta^2 (1 - c^2) + 1 - \eta^2 (1 - c^2) = 1$. The formula needs no trigonometric function, which is why ray tracers use it. Whitted (1980, Section 2) wrote the same direction in another form: with $V' = V / |V \cdot N|$ and $k_n = n_2 / n_1$, the transmitted direction is $P = k_f (N + V') - N$ with $k_f = (k_n^2 |V'|^2 - |V' + N|^2)^{-1/2}$. His $P$ does not have unit length, but it points along $t$.

**Total internal reflection.** The value $k = \cos^2\theta_2$ is negative exactly when $\eta \sin\theta_1 > 1$. This needs $n_1 > n_2$ and an incident angle above the critical angle

$$\theta_c = \arcsin\frac{n_2}{n_1}.$$

Then no refracted ray exists, and the Fresnel equations give a reflectance of exactly 1. A ray tracer returns "no refraction" for $k < 0$ and follows only the [reflected ray](/point-projection-and-reflection/) $d - 2 (n \cdot d)\,n$.

**Reversibility.** If $t$ is the refracted direction of $d$, then the refracted direction of $-t$ from the other side, with the normal $-n$ and the ratio $1 / \eta$, is $-d$. Light can run the same path backward. The path is reversible, but the radiance along it is not the same on the two sides: it scales by $n^2$, which the page on [Helmholtz reciprocity](/helmholtz-reciprocity/) treats.

**Dispersion.** The index depends on the wavelength. For glass it decreases from blue to red, so blue light bends more. A renderer that traces one direction for all colors cannot show the rainbow edges of a prism or a diamond; [spectral rendering](/spectral-rendering/) traces each wavelength on its own direction.

**Floating point.** Four mistakes are common in code. First, the formula assumes that $d$ and $n$ have unit length; a direction that is not normalized gives a wrong $c$ and a wrong bend. Second, a surface normal from a mesh points outward, but a ray inside a glass object meets it with $n \cdot d > 0$. The code must then flip the normal and swap $n_1$ and $n_2$, else it refracts the wrong way. Third, near the critical angle $k$ is a difference of two numbers close to 1, and rounding can make it slightly negative or slightly positive; the code must treat the sign of the computed $k$ as the decision, and use the same decision for the Fresnel term. Fourth, the refracted ray starts on the surface, so its origin must move a small distance to the far side, along $-n$, or the ray hits the same surface again at $t \approx 0$.

## Examples

**Air into glass at 45 degrees.** With $n_1 = 1$, $n_2 = 1.5$ and $\theta_1 = 45°$, $\sin\theta_2 = 0.7071 / 1.5 = 0.4714$, so $\theta_2 = 28.13°$. In vector form, take $n = (0, 1, 0)$ and $d = (0.7071, -0.7071, 0)$. Then $c = 0.7071$, $\eta = 2/3$, $k = 1 - \tfrac49 \cdot \tfrac12 = \tfrac79 = 0.7778$, and

$$t = \tfrac23 (0.7071, -0.7071, 0) + (0.4714 - 0.8819)(0, 1, 0) = (0.4714, -0.8819, 0),$$

a unit vector at $28.13°$ from $-n$.

**The critical angle.** From glass of index 1.5 into air, $\theta_c = \arcsin(1/1.5) = 41.81°$. From water of index 1.333 into air, $\theta_c = 48.61°$. A ray inside a glass block that meets its face at $60°$ has $k = 1 - 2.25 \cdot 0.75 = -0.6875 < 0$, so it is reflected in full. Optical fibres and the bright edges of a glass of water come from this effect.

**Least time.** Take $A = (0, 1)$ in air and $B = (1, -1)$ in glass of index 1.5. The time $T(x)$ is least at $x = 0.6232$. There $\sin\theta_1 = 0.6232 / \sqrt{0.6232^2 + 1} = 0.5289$ and $\sin\theta_2 = 0.3768 / \sqrt{0.3768^2 + 1} = 0.3526$, and $1.5 \cdot 0.3526 = 0.5289$, as the law says. The tests of the implementation compare the vector form with this least-time search for 600 random pairs of points and indices.

**Apparent depth.** Looked at from straight above, the bottom of a pool of water seems nearer than it is. For small angles $\sin\theta \approx \tan\theta$, and the law gives an apparent depth of the real depth times $1 / 1.333 = 0.75$.

**Not refraction.** A mirror changes the direction of a ray by the law of reflection, and the index plays no part. A rough surface such as frosted glass refracts at each tiny facet by Snell's law, but the facets point in many directions, so the light leaves in a spread of directions. A [microfacet model](/microfacet-brdf/) describes that spread with a distribution of facet normals; Snell's law holds for each facet.

## Where it is used

- [Whitted ray tracing](/whitted-ray-tracing/) spawns a refracted ray at each hit on a transparent surface, in the direction of the vector form, and stops the branch at total internal reflection.
- A [BSDF](/bsdf/) for smooth glass is a pair of delta lobes in the mirror direction and the Snell direction. Rough glass uses Snell's law in reverse: the half vector of a refraction is the facet normal that maps the incident direction to the outgoing one.
- The [Fresnel equations](/fresnel-equations/) need $\cos\theta_2$, which is $\sqrt{k}$ of the vector form.
- [Path tracing](/path-tracing/) and [photon mapping](/photon-mapping/) follow refracted paths through glass and water; caustics under a glass or at the bottom of a pool are light focused by refraction.
- [Spectral rendering](/spectral-rendering/) uses a wavelength-dependent index for dispersion.
- Lens models such as the [thin-lens camera](/thin-lens-camera/) are the paraxial result of Snell's law at two curved surfaces.

### History

Ptolemy measured angles of refraction from air into water and glass but found no law. Ibn Sahl stated the law correctly in a treatise on burning mirrors and lenses of about 984, in a geometric form with a fixed ratio of lengths (Rashed 1990). Thomas Harriot found it again in 1602 and Willebrord Snellius in 1621; neither published it. René Descartes published it in La Dioptrique in 1637, which is why French texts call it the law of Descartes. Pierre de Fermat derived it from the principle of least time in 1662, under the assumption that light is slower in the denser medium; Descartes had assumed the opposite.

## References
