---
tag: 22XP7T
kind: algorithm
slug: precomputed-atmospheric-scattering
name: Precomputed atmospheric scattering
aliases:
- Bruneton atmospheric scattering
area: graphics-and-signals/real-time-rendering
level: advanced
summary: "Precompute transmittance and single and multiple Rayleigh and Mie scattering into 2D and 4D tables, so that sky and aerial perspective render from any altitude with a few lookups."
model: real-ram
complexity:
  vars: {t: the number of entries of the transmittance table, q: the number of quadrature steps along one ray}
  time: {transmittance_table: Θ(t q), single_scattering_ray: Θ(q)}
  space: {table: Θ(t)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2008
  people: [Eric Bruneton, Fabrice Neyret]
  note: Bruneton and Neyret precomputed the transmittance, the single scattering and the multiple scattering of a spherical Rayleigh and Mie atmosphere into tables indexed by altitude and angles, so that a GPU could draw the sky and aerial perspective from any viewpoint, from the ground to space, in real time.
prereqs: [participating-media, trapezoidal-rule]
see_also: [preetham-sky-model, ray-marching, volumetric-path-tracing, image-based-lighting, irradiance-environment-map, tone-mapping, beer-lambert-law, numerical-integration]
sources:
  - paper: doi:10.1111/j.1467-8659.2008.01245.x
    title: Eric Bruneton and Fabrice Neyret, Precomputed atmospheric scattering, Computer Graphics Forum 27(4), 2008, 1079 to 1086 (Eurographics Symposium on Rendering)
    locator: the atmosphere model (Rayleigh and Mie scattering coefficients, scale heights, phase functions), the parameterization of the 2D and 4D tables, and the precomputation of multiple scattering orders
  - url: https://ebruneton.github.io/precomputed_atmospheric_scattering/
    title: Eric Bruneton, Precomputed Atmospheric Scattering, a new implementation (2017), documented source code
    locator: the file atmosphere/functions.glsl, with the transmittance computation, the mapping from (r, mu) to texture coordinates, the phase functions and the transmittance between two points from two lookups
  - paper: doi:10.1145/166117.166140
    title: Tomoyuki Nishita, Takao Sirai, Katsumi Tadamura and Eihachiro Nakamae, Display of the earth taking into account atmospheric scattering, SIGGRAPH 93, 175 to 182
    locator: the single scattering model of sunlight in a spherical atmosphere with exponential density (general locator)
  - paper: doi:10.1111/cgf.14050
    title: Sébastien Hillaire, A Scalable and Production Ready Sky and Atmosphere Rendering Technique, Computer Graphics Forum 39(4), 2020, 13 to 22
    locator: the smaller lookup tables and the approximation of multiple scattering that replace the 4D table (general locator)
---

Precomputed atmospheric scattering draws the color of a clear sky, and the haze between the camera and distant objects, from tables that are computed once for a given atmosphere. The atmosphere is a spherical shell around the planet, with air molecules that scatter by the Rayleigh law and aerosols that scatter by the Mie law, each with a density that falls exponentially with altitude. Bruneton and Neyret (2008) store the transmittance in a 2D table over altitude and view angle, and the single and multiple scattered light in a 4D table over altitude, view angle, sun angle and the angle between the view and the sun. A pixel then costs a few texture reads, from any altitude and for any sun position. This page explains the method and gives a toy version in code: the code builds the transmittance table and computes single scattering along one view ray by quadrature with it. The toy does not build the 4D table and has no multiple scattering, and its numbers are those of a toy atmosphere.

## In plain words

Sunlight that enters the air bounces off molecules and small particles. Blue light bounces much more than red light, which is why the sky looks blue, and why the sun looks red near the horizon, when its light crosses much more air. To find the color of the sky in one direction, you would add up the light that bounces toward you from every point along that direction, weakened by the air it crosses on its way. That sum is slow. But in a round planet with layered air, the answer only depends on a few numbers: how high you are, where you look and where the sun is. So the method works out the answer for many such cases ahead of time and stores them in tables. At run time it reads the tables.

## The problem

The input is an atmosphere: the ground radius $R_g$, the top radius $R_t$, the scattering and extinction coefficients of molecules and aerosols at sea level, their scale heights, and the phase functions. The output is the radiance $L(x, v)$ that reaches a point $x$ from the direction $-v$, for the sun at a fixed direction $\ell$ with irradiance $E_{\text{sun}}$, and the transmittance $T(x, y)$ between two points. The standing assumptions are physical laws of the model, stated as such:

- **Extinction.** Light along a segment is attenuated by $T(x, y) = \exp(-\int_x^y \sigma)$, the [Beer-Lambert law](/beer-lambert-law/), with $\sigma(h) = \beta_R(h) + \beta_M^{\text{ext}}(h)$.
- **Density.** $\beta_R(h) = \beta_R(0) e^{-h/H_R}$ and $\beta_M(h) = \beta_M(0) e^{-h/H_M}$ at altitude $h$. Bruneton and Neyret use $H_R = 8$ km and $H_M = 1.2$ km, and $\beta_R(0) = (5.8, 13.5, 33.1) \times 10^{-3}$ per km at 680, 550 and 440 nm. These ratios follow the $\lambda^{-4}$ law of Rayleigh scattering within 1%.
- **Phase functions.** Rayleigh $P_R(\nu) = \frac{3}{16\pi}(1 + \nu^2)$ and the Cornette-Shanks function $P_M(\nu) = \frac{3}{8\pi} \frac{1 - g^2}{2 + g^2} \frac{1 + \nu^2}{(1 + g^2 - 2g\nu)^{3/2}}$ for Mie, with $\nu$ the cosine of the angle between the view and the sun.
- **Symmetry.** The atmosphere depends only on altitude. Then $L$ depends only on $r = |x|$, $\mu = v \cdot x / r$, $\mu_s = \ell \cdot x / r$ and $\nu = v \cdot \ell$, four numbers. This is why a 4D table is enough.

The single scattered part is

$$L_1(x, v) = E_{\text{sun}} \int_0^D T(x, y_s)\, V(y_s)\, T_{\text{sun}}(y_s) \big(\beta_R(y_s) P_R(\nu) + \beta_M(y_s) P_M(\nu)\big)\, ds,$$

with $y_s = x + s v$, $D$ the distance to the ground or to the top, $V$ the visibility of the sun and $T_{\text{sun}}$ the transmittance from $y_s$ toward the sun. Higher orders replace $E_{\text{sun}} T_{\text{sun}}$ by the light of the previous order that arrives at $y_s$ from all directions.

## The algorithm

The full method of Bruneton and Neyret has these steps:

1. **Transmittance.** Compute $T(r, \mu)$ to the top of the atmosphere on a 2D grid, by quadrature of the optical depth.
2. **Single scattering.** Compute $L_1(r, \mu, \mu_s, \nu)$ on a 4D grid, by quadrature along each ray, with every transmittance read from step 1. Implementations usually keep the single scattering phase functions out of the table and apply them per pixel, so that the sharp forward peak of Mie scattering does not need a fine angular grid (a design choice, not a requirement).
3. **Ground irradiance.** Compute the irradiance on the ground as a function of $r$ and $\mu_s$, for light that the ground reflects back into the air.
4. **Higher orders.** For each order $k = 2, \dots, o$: at every 4D grid point, integrate the order $k - 1$ light over $m$ incoming directions with the phase functions, which gives the scattering density; then integrate that density along each ray with the transmittance, and add the result to the 4D table.
5. **Rendering.** For a sky pixel, read the 4D table at the camera and multiply by the phase functions. For a surface at $y$ seen from $x$, the aerial perspective is $L(x) - T(x, y) L(y)$, two 4D lookups and one transmittance, and the surface color is attenuated by $T(x, y)$.

The toy code covers step 1 and step 2 for one view ray:

```pseudo id=main
SINGLE-SCATTERING(r, μ, μs, ν)
L1  for each table entry (x_r, x_μ): T[x_r][x_μ] ← exp(-optical depth from (r, μ) to the top)   ▷ once
L2  D ← distance to the ground if the ray hits it, else to the top
L3  S ← 0
L4  for k ← 0 to q:  s ← k D / q;  w ← 1/2 at the two ends, 1 inside
L5      r_s ← sqrt(r² + s² + 2 r μ s);  μ_s,y ← (r μs + s ν) / r_s
L6      T_view ← T(r, μ) / T(r_s, μ_y), or T(r_s, -μ_y) / T(r, -μ) if the ray hits the ground
L7      if the sun is below the horizon at r_s, skip this step;  else T_sun ← T(r_s, μ_s,y)
L8      S ← S + w · T_view · T_sun · (β_R(r_s) P_R(ν) + β_M(r_s) P_M(ν))
L9  return S · D / q
```

Line L1 fills the transmittance table at the rays given by the mapping of Bruneton's 2017 code: $x_r = \rho / H$ with $\rho = \sqrt{r^2 - R_g^2}$ and $H = \sqrt{R_t^2 - R_g^2}$, and $x_\mu$ the distance $d$ to the top scaled between its least value $R_t - r$ (looking up) and its largest value $\rho + H$ (along the horizon). Lookups are bilinear in $(x_r, x_\mu)$. Line L2 gives the length of the ray in the atmosphere. Line L5 uses the law of cosines for the point at distance $s$. Line L6 gets the transmittance of the part of the ray up to $s$ from two table entries, because transmittance multiplies along a ray. Line L7 checks whether the planet hides the sun at that point. Line L8 adds the light scattered toward the camera, and line L9 finishes the trapezoidal rule.

## Example

The toy atmosphere uses the Rayleigh values above, $R_g = 6360$ km, $R_t = 6420$ km, $\beta_M(0) = 4 \times 10^{-3}$ per km, an albedo of 0.9 for the aerosols and $g = 0.8$; these last values are tuning of the toy. The table has $32 \times 64$ entries with 200 steps each, and single scattering uses $q = 100$. The three numbers are red, green and blue, per unit sun irradiance.

| view from the ground | quantity | red | green | blue |
|---|---|---|---|---|
| straight up | transmittance to the top | 0.9496 | 0.8929 | 0.7633 |
| along the horizon (876 km of air) | transmittance to the top | 0.1192 | 0.0135 | 0.0001 |
| straight up, sun at the zenith | single scattering, 1/sr | 0.0242 | 0.0293 | 0.0393 |
| straight up, sun 60 degrees from the zenith | single scattering, 1/sr | 0.0033 | 0.0069 | 0.0133 |
| 78 degrees from the zenith, toward a setting sun ($\mu_s = 0.05$, $\nu = 0.9$) | single scattering, 1/sr | 0.0190 | 0.0216 | 0.0135 |

These are measurements of the toy. The zenith is blue when the sun is high, by a factor of 4 between blue and red, and the light near a low sun is yellow and red, because the blue part of the sunlight is lost on the long path to each scattering point. The table lookups agree with direct quadrature to within $1.7 \times 10^{-3}$ in transmittance over random rays, and the single scattering values to within 1% for the five test rays. With a table that is linear in $\mu$ instead of in the distance $d$, the largest transmittance error grew to $4.6 \times 10^{-2}$, all of it near the horizon.

## Correctness

The [proof](proofs/correctness.md) shows that line L5 gives the altitude and the sun angle at each point of the ray, that the ground test of lines L2 and L7 is exact, that the table mapping of line L1 is a bijection with the stated inverse, that line L6 equals the transmittance of the segment (because optical depth adds along a ray and does not depend on the direction), that the phase functions integrate to 1 over the sphere for any $g$, and that lines L3 to L9 are the trapezoidal rule for the single scattering integral, which converges as $q$ grows. These are proved properties. The model itself (exponential layers, Rayleigh and Mie laws, single and multiple scattering) is physical law applied to an idealized atmosphere. The error of the bilinear table is not bounded by the proof; it is a measurement of the tests.

## Complexity

The model is the real RAM, with $t$ table entries and $q$ quadrature steps per ray. The transmittance table costs $\Theta(t q)$ once. One view ray of single scattering costs $\Theta(q)$, with three $O(1)$ table lookups per step, independent of $t$. The table needs $\Theta(t)$ space, three numbers per entry.

For the full method, let $t$ be the number of entries of the 4D table, $m$ the number of directions for the scattering density and $o$ the number of orders. Each order costs $\Theta(t m)$ for the density and $\Theta(t q)$ for the integration along rays, so the precomputation costs $\Theta(o t (m + q))$. Rendering costs $\Theta(1)$ per pixel. With a few dozen entries along each of the four axes, the 4D table has a few hundred thousand to a few million entries; the cost is paid again whenever the atmosphere changes, but not when the sun or the camera moves.

## Properties

- **Exact symmetry reduction.** For a spherically layered atmosphere, two configurations with the same $(r, \mu, \mu_s, \nu)$ differ by a rotation about the center of the planet, which maps the atmosphere to itself, so the four numbers determine the radiance exactly (a proved property). The tables lose information only through their resolution.
- **Linearity.** The result is linear in $E_{\text{sun}}$, and single scattering is linear in the scattering coefficients for a fixed transmittance.
- **No dependence on the camera path.** The tables are the same for every viewpoint, from the ground to space; only a change of the atmosphere needs a new precomputation.
- **Only the planet casts shadows.** The tables assume that nothing but the planet blocks the sun inside the air, so light shafts behind mountains or clouds need separate methods.

## Variants and improvements

- **Fewer tables.** Hillaire (2020) replaces the 4D table by a sky view table for the current camera, a small 3D table for aerial perspective in the view frustum and a 2D table for multiple scattering, recomputed each frame, which lets artists change the atmosphere at run time.
- **Better parameterizations.** Bruneton's 2017 reimplementation maps the angles with the distance to the boundary, as in line L1, to put more entries near the horizon and to avoid extrapolation at the ends of the table.
- **Ozone.** An absorbing layer in the middle atmosphere changes the color of the twilight sky; later implementations add it as one more extinction term.
- **Analytic fits.** For a camera on the ground only, the [Preetham sky model](/preetham-sky-model/) and its successors fit formulas to simulated skies and need no tables.
- **Path tracing.** [Volumetric path tracing](/volumetric-path-tracing/) of the same atmosphere gives reference images, at a cost far from real time.

## When to use it

Use precomputed scattering when the camera can be anywhere from the ground to space, the sun moves, and the atmosphere is the same for long periods, as in flight simulators, planet renderers and open world games. Use an analytic sky model when the camera stays on the ground and only the sky dome is needed. Use per frame methods such as Hillaire's when the atmosphere parameters change often. For clouds, fog banks and other local media, use [ray marching](/ray-marching/) of [participating media](/participating-media/), since the tables assume a layered, clear atmosphere.

## Pitfalls

- **Units.** Kilometers and meters mixed between the radii and the scattering coefficients change every result by orders of magnitude. Line L1 must use the same length unit for both.
- **The horizon.** Transmittance changes fastest near the horizon. A table that is linear in $\mu$ undersamples it, as the example measured, and gives a dark or bright band at the horizon. Use the distance mapping of line L1.
- **Division in line L6.** Near the horizon both table values in line L6 are small and their ratio is unstable; the result can exceed 1. Clamp it to 1, and use the reversed form for rays that hit the ground, since the direct form would read the table for rays that are not in it.
- **Too few steps in line L4.** A horizontal ray crosses about 876 km of air in the toy atmosphere, while the Mie layer has a scale height of 1.2 km. A fixed number of steps that works for upward rays misses most of the haze along the horizon.
- **The shadow of the planet.** Without the test of line L7, points in the shadow of the planet still scatter sunlight, and the sky stays bright after sunset.
- **Phase in the table.** Putting the Mie phase function into the 4D table blurs the bright halo around the sun, because the table has a coarse grid in $\nu$.
- **Display.** The output is linear radiance with a large range; it needs [tone mapping](/tone-mapping/) before display.

## Implementations

## History

Nishita, Sirai, Tadamura and Nakamae (1993) computed single scattering of sunlight in a spherical atmosphere with exponential density, to display the Earth from space. Preetham, Shirley and Smits (1999) fitted an analytic model to simulated skies seen from the ground. Bruneton and Neyret (2008) reduced the radiance of a layered atmosphere to four parameters, precomputed single and multiple scattering into tables, and rendered sky and aerial perspective from any altitude on the GPU. Bruneton published a documented reimplementation in 2017. Hillaire (2020) moved most of the work back to each frame with smaller tables, so that the atmosphere can change while the program runs.

## References
