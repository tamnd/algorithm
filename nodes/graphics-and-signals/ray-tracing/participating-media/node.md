---
tag: VFZ0CZ
kind: concept
slug: participating-media
name: Participating media
aliases:
- volumetric media
area: graphics-and-signals/ray-tracing
level: advanced
summary: Media such as fog, smoke, clouds and skin that absorb, scatter and emit light along a ray, not only at surfaces. The radiative transfer equation describes them.
prereqs: [rendering-equation, albedo]
see_also: [delta-tracking, volumetric-path-tracing, ray-marching, bssrdf, path-tracing, photon-mapping, monte-carlo-integration, inverse-transform-sampling]
sources:
  - book: isbn:9780486605906
    title: Subrahmanyan Chandrasekhar, Radiative Transfer, Oxford University Press, 1950; Dover reprint, 1960
    locator: the opening chapter, on the equation of transfer, the extinction and scattering coefficients, the phase function and the albedo for single scattering
  - paper: doi:10.1145/964965.808594
    title: James T. Kajiya and Brian P. Von Herzen, Ray tracing volume densities, Computer Graphics (SIGGRAPH '84 Proceedings) 18(3), 1984, 165 to 174
    locator: the transfer equation for rendering, and the single scattering approximation for volume densities on a grid
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, Morgan Kaufmann, 2016
    locator: Sections 11.1 to 11.3, volume scattering processes, phase functions and media, and Section 15.1, the equation of transfer
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, AK Peters, 2006
    locator: Section 8.1, participating media
  - paper: doi:10.1111/cgf.13383
    title: Jan Novák, Iliyan Georgiev, Johannes Hanika and Wojciech Jarosz, Monte Carlo methods for volumetric light transport simulation, Computer Graphics Forum 37(2), 2018
    locator: the survey of the radiative transfer equation, transmittance estimation and free-path sampling
---

A participating medium is a volume that interacts with light at every point, not only at its boundary. Fog, smoke, clouds, fire, water, milk, skin and the atmosphere are examples. Along a ray, a medium does three things. It **absorbs** light, with the absorption coefficient $\sigma_a(x)$. It **scatters** light into other directions, with the scattering coefficient $\sigma_s(x)$ and a *phase function* $p(\omega, \omega')$ that gives the distribution of the new direction. It can **emit** light, as fire does. The sum $\sigma_t = \sigma_a + \sigma_s$ is the extinction coefficient, and $\alpha = \sigma_s/\sigma_t$ is the single-scattering [albedo](/albedo/). The radiance in a medium obeys the *radiative transfer equation* of Chandrasekhar (1950), which adds a volume term to the [rendering equation](/rendering-equation/). Light that crosses the distance $d$ without a collision keeps the fraction $T = \exp\left(-\int_0^d \sigma_t\, dt\right)$, the *transmittance*.

## In plain words

On a clear day, light goes straight from the sun to a wall and then to the eye. The air hardly changes it. In fog, each bit of the air takes part. Some light is lost in the fog, some is pushed aside into new directions, and some light from elsewhere is pushed into the line of sight.

So a renderer cannot only look at the surfaces. It must also follow what happens inside the volume along each ray.

Three numbers at each point describe the medium: how much light it swallows, how much it scatters, and how the scattered light spreads, mostly forward or in all directions. Thick fog scatters a lot and swallows little, which is why it looks white and bright. Smoke from a fire swallows more, so it looks dark.

## The idea

**Extinction and transmittance.** Along a ray $x_t = x + t\omega$, the radiance that is not scattered or absorbed falls like $dL/dt = -\sigma_t(x_t) L$. So light that travels from $x_0$ to $x_d$ is multiplied by

$$T(0, d) = \exp\left(-\tau(0, d)\right), \qquad \tau(0, d) = \int_0^d \sigma_t(x_t)\, dt,$$

where $\tau$ is the *optical depth*. This is the Beer-Lambert law. In a homogeneous medium $T = e^{-\sigma_t d}$, and the mean free path is $1/\sigma_t$. Transmittance is multiplicative: $T(0, d) = T(0, s)\, T(s, d)$.

**Free flight.** The distance to the first collision has the density $\sigma_t(x_t)\, T(0, t)$ and the survival function $T(0, t)$. In a homogeneous medium it is exponential, and $t = -\ln(1 - u)/\sigma_t$ samples it by [inverse transform sampling](/inverse-transform-sampling/). In a heterogeneous medium, the inverse of $\tau$ has no closed form in general. [Delta tracking](/delta-tracking/) samples the collision exactly with a constant majorant $\bar\sigma \ge \sigma_t$ and fictitious collisions, and [ray marching](/ray-marching/) approximates $\tau$ with a quadrature.

**The phase function.** At a scattering event, the new direction $\omega'$ has the density $p(\omega, \omega')$, which integrates to 1 over the sphere. Isotropic scattering has $p = 1/(4\pi)$. The Henyey-Greenstein phase function

$$p_{\mathrm{HG}}(\cos\theta) = \frac{1}{4\pi}\, \frac{1 - g^2}{(1 + g^2 - 2g\cos\theta)^{3/2}}$$

has the mean cosine $g \in (-1, 1)$. A positive $g$ scatters forward, as in clouds and skin, and $g = 0$ is isotropic. The phase function plays the role of the BRDF, but it has no cosine factor and is normalized to 1, so the energy that it loses is described by $\alpha$, not by $p$.

**The radiative transfer equation.** For the radiance $L(x, \omega)$ in the direction $\omega$,

$$(\omega \cdot \nabla) L(x, \omega) = -\sigma_t(x) L(x, \omega) + \sigma_a(x) L_e(x, \omega) + \sigma_s(x) \int_{S^2} p(\omega', \omega) L(x, \omega')\, d\omega'.$$

The three terms are extinction, emission and in-scattering. Integrated along the ray back to the first surface point $x_d$ at the distance $d$, it gives the *volume rendering equation*

$$L(x, \omega) = T(0, d)\, L_o(x_d, \omega) + \int_0^d T(0, t)\Big[\sigma_a L_e + \sigma_s \int_{S^2} p\, L\, d\omega'\Big](x - t\omega, \omega)\, dt,$$

with $L_o$ the radiance that leaves the surface. This is an integral equation like the rendering equation, now over paths whose vertices can lie inside volumes. A Monte Carlo estimator samples the distance of the next vertex with the free-flight density, chooses between scattering and absorption with the probabilities $\alpha$ and $1 - \alpha$, and samples the new direction from $p$. This is [volumetric path tracing](/volumetric-path-tracing/).

**Single and multiple scattering.** Light that scatters once inside the medium before it reaches the eye is single scattering. It has a closed form in simple cases and dominates in thin media. In dense media with an albedo near 1, such as clouds or milk, light scatters hundreds of times, and the result looks diffuse. Then the diffusion approximation applies, which is the basis of the dipole model of subsurface scattering in a [BSSRDF](/bssrdf/).

## Examples

- **A homogeneous slab.** A beam crosses 1 unit of a medium with $\sigma_t = 2$. The transmittance is $e^{-2} = 0.135335$. With 100000 samples of the free flight, $-\ln(1 - u)/2$ has the sample mean 0.50187 with seed 1, close to the mean free path $1/2$.
- **A heterogeneous medium.** With $\sigma_t(t) = 1 + 2t$ on $[0, 1]$, the optical depth is $\int_0^1 (1 + 2t)\, dt = 2$, so the transmittance is again $e^{-2} = 0.135335$. Transmittance depends only on the optical depth, not on where along the ray the density lies. Delta tracking estimates such a transmittance without computing the integral.
- **The fate of a beam.** A beam enters a slab of optical thickness $\tau = 1$ with $\alpha = 0.8$. A fraction $e^{-1} = 0.367879$ crosses it without a collision. At the first collision, a fraction $0.8(1 - e^{-1}) = 0.505696$ scatters and $0.2(1 - e^{-1}) = 0.126424$ is absorbed. The scattered part may leave the slab or collide again.
- **Henyey-Greenstein lobes.** The ratio of the forward value $p(1)$ to the backward value $p(-1)$ is $\left(\frac{1 + g}{1 - g}\right)^3$. It is 1 for $g = 0$, 27 for $g = 0.5$, and 1876.04 for $g = 0.85$, a typical value for clouds. A midpoint rule with 200000 points over $\cos\theta$ gives a total of 1.000000 and a mean cosine of $g$ for each value.
- **Sky color.** Air molecules are much smaller than the wavelength, and their Rayleigh scattering coefficient grows like $\lambda^{-4}$. Blue light scatters more than red, so the sky is blue and the setting sun, seen through a long path of air, is red.

## Where it is used

- **Rendering of fog, smoke, fire, clouds and explosions** in film and games, with heterogeneous densities stored in grids such as OpenVDB. Production renderers use delta tracking and its variants for free-flight sampling.
- **Subsurface scattering** in skin, marble, wax and milk, either by volumetric path tracing inside the object or by a BSSRDF that approximates the multiple scattering.
- **Atmospheric scattering** for skies, aerial perspective and planets, with Rayleigh and Mie scattering.
- **Underwater rendering** and light shafts, where single scattering in a thin medium dominates.
- **Physics and engineering.** The same transfer equation describes neutron transport in reactors, where Woodcock tracking was first used, radiative heat transfer in furnaces, light in biological tissue for medical optics, and radiation in stellar atmospheres, the subject of Chandrasekhar's book.
- **Global illumination algorithms** that have volume versions: photon mapping with volume photons and beams, irradiance caching of in-scattered light, and VCM with points, beams and paths.

## References
