---
tag: HY3PQF
kind: technique
slug: spherical-harmonic-lighting
name: Spherical harmonic lighting
aliases:
- SH lighting
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Project lighting and transfer functions onto low-order spherical harmonics, so that integrals over the sphere become dot products of coefficients.
prereqs: [image-based-lighting]
see_also: [irradiance-environment-map, precomputed-radiance-transfer, irradiance-volume, legendre-polynomials, gibbs-phenomenon, image-based-lighting, lambertian-reflectance, monte-carlo-integration]
sources:
  - paper: doi:10.1145/383259.383317
    title: Ravi Ramamoorthi and Pat Hanrahan, An efficient representation for irradiance environment maps, SIGGRAPH 2001, 497 to 500
    locator: Section 2, the real spherical harmonics up to order 2 and the coefficients of the clamped cosine
  - paper: doi:10.1145/566654.566612
    title: Peter-Pike Sloan, Jan Kautz and John Snyder, Precomputed radiance transfer for real-time rendering in dynamic, low-frequency lighting environments, ACM Transactions on Graphics 21(3), 2002, 527 to 536
    locator: the projection of lighting and transfer onto spherical harmonics, the dot product of coefficients and the rotation of the lighting (general locator)
  - url: http://www.cs.umd.edu/class/spring2005/cmsc828v/papers/spherical-harmonic-lighting.pdf
    title: Robin Green, Spherical Harmonic Lighting, The Gritty Details, Game Developers Conference 2003
    locator: the definition of the real basis, Monte Carlo projection, the dot product of coefficients and rotation (general locator)
  - url: https://www.ppsloan.org/publications/StupidSH36.pdf
    title: Peter-Pike Sloan, Stupid Spherical Harmonics (SH) Tricks, Game Developers Conference 2008
    locator: the ringing of truncated projections and windowing with sigma factors or a Hanning window, and the remark that bright lights need windowing even for irradiance
---

Spherical harmonic lighting stores functions on the sphere of directions, such as the light that arrives at a point or the way a surface responds to light, as a few coefficients in the basis of real spherical harmonics. The basis is orthonormal, so the integral of the product of two functions over the sphere becomes the dot product of their coefficient vectors. With order 3 (bands 0, 1 and 2, nine coefficients), a light probe costs nine numbers per color channel, and the diffuse light for any normal is a short polynomial in the normal, which is the [irradiance environment map](/irradiance-environment-map/). With more coefficients and a precomputed transfer function per point, the dot product also includes shadows and bounced light, which is [precomputed radiance transfer](/precomputed-radiance-transfer/). The basis suits smooth, low frequency light. Sharp light such as a small sun needs many bands, and a truncated projection rings.

## In plain words

Any pattern of light around a point can be written as a sum of standard patterns, like a sound is a sum of tones. The first pattern is the same in all directions. The next three are brighter on one side and darker on the other, along each axis. The next five have more lobes, and so on. A smooth light, like an overcast sky, needs only the first few patterns, so you store only how much of each it has, a short list of numbers. The useful trick is that you can do the same for the response of a surface, and then the total light the surface sends out is the sum of the products of the two lists. A sharp light, like the sun, needs many patterns, and cutting the list short gives ripples.

## When it applies

- An integral over the sphere of the product of two functions must be computed many times, for example light times a response, at every pixel or vertex.
- Both functions are smooth, or at least one of them is, so that a few bands capture what matters. The clamped cosine of a diffuse surface is such a function.
- The lighting changes over time or space, so that precomputing the full integral for each lighting is not possible, but projecting the lighting each frame is cheap.
- Rotations of the lighting, blends between probes and sums of lights are needed, since each of them acts on the coefficients directly.

## The template

1. **Choose the order.** Order $n$ means bands $l = 0, \dots, n - 1$ and $n^2$ coefficients. Order 3 (9 coefficients) is common for irradiance; orders 4 to 6 for precomputed transfer.
2. **Project the lighting.** $L_{lm} = \int L(\omega) Y_{lm}(\omega)\, d\omega$, by a sum over the texels of a map weighted by their solid angle, by Monte Carlo, or in closed form for simple lights.
3. **Project the transfer function.** For a diffuse surface without shadows this is the clamped cosine, with known coefficients. With shadows or bounces it is precomputed per point.
4. **Optionally window.** Multiply band $l$ by a factor $w_l \le 1$ to reduce ringing.
5. **Shade.** Take the dot product of the two coefficient vectors.

```pseudo id=main
SH-SHADE(L, T)
L1  for each texel j of the map, with direction d_j and solid angle Δω_j:
L2      for each (l, m) with l < n:  c[l, m] ← c[l, m] + L(d_j) · Y_lm(d_j) · Δω_j
L3  t ← the coefficients of the transfer function   ▷ hole: analytic or precomputed
L4  for each l:  c[l, ·] ← w_l · c[l, ·]             ▷ hole: the window, w_l = 1 for none
L5  return Σ_{l, m} c[l, m] · t[l, m]
```

**Projection (lines L1 and L2).** The real spherical harmonics $Y_{lm}$, for $l \ge 0$ and $-l \le m \le l$, are orthonormal on the sphere. Up to band 2, they are polynomials in the components $x, y, z$ of the direction: a constant, three linear terms and five quadratic terms. The sum is a quadrature of the projection integral; a [cube map](/cube-map/) must weight each texel by its solid angle.

**Transfer (line L3).** For an unshadowed diffuse surface with normal $n$, the transfer is $\max(n \cdot \omega, 0)$, and its coefficients are $\hat A_l Y_{lm}(n)$ with $\hat A_0 = \pi$, $\hat A_1 = 2\pi/3$ and $\hat A_2 = \pi/4$. This follows from the Funk-Hecke theorem, because the function depends only on the angle to $n$.

**Windowing (line L4).** A truncated projection of a sharp light rings, the [Gibbs phenomenon](/gibbs-phenomenon/) on the sphere, and can give negative light. Sloan (2008) describes windows such as sigma factors and the Hanning window, which damp the high bands, at the cost of blur.

**Shading (line L5).** By orthonormality, $\int \tilde L \tilde T\, d\omega = \sum_{lm} L_{lm} T_{lm}$ for the projected functions $\tilde L$ and $\tilde T$ (a proved property). If one of the two functions lies in the span of the first $n^2$ harmonics, the dot product equals the exact integral of the other times it.

## Classic examples

- **Diffuse light from an environment map.** The [irradiance environment map](/irradiance-environment-map/) uses nine coefficients and the clamped cosine; the error is at most $3/32$ of the total light, a proved bound.
- **Probes in a level.** An [irradiance volume](/irradiance-volume/) stores nine coefficients per probe of a grid and blends them by position.
- **Shadows and bounces.** [Precomputed radiance transfer](/precomputed-radiance-transfer/) projects the visibility and the bounced light of a static object per vertex, and shades by the dot product with the projected lighting.
- **Many small lights.** Project each point light at its direction and add their coefficients; a point light of power $\Phi$ in direction $d$ has the coefficients $\Phi Y_{lm}(d)$. The sum then shades like one light probe, for the cost of one.
- **Ambient light in [image-based lighting](/image-based-lighting/).** The diffuse part of a captured map is stored as nine coefficients.

## Variations

- **Rotation.** Each band is closed under rotation, so a rotation acts by a $(2l + 1) \times (2l + 1)$ matrix per band. Band 1 rotates like a vector. Zonal harmonics, the functions symmetric about an axis, rotate by evaluating $Y_{lm}$ at the new axis.
- **Products.** The product of two functions with $n^2$ coefficients each has more bands. Its projection back to $n^2$ coefficients needs the triple product tensor of the basis, not a dot product, and costs much more.
- **Other bases.** The hemisphere-only bases, the ambient cube of six colors, spherical Gaussians and wavelets on a cube map trade the smoothness and rotation properties of spherical harmonics for sharper features. Wavelets such as the [Haar wavelet](/haar-wavelet/) represent all frequencies with a sparse set of coefficients.
- **Two bands.** Order 2 (four coefficients) stores a constant and a direction, which captures the main direction of the light; it is cheaper, and often enough for small or distant probes.
- **Deringing.** Fit coefficients by least squares with a positivity constraint, or apply windows per band.

## Pitfalls

- **Missing solid angles in line L2.** A sum over cube map texels with equal weights overweights the face corners and gives wrong coefficients. Use the exact texel solid angle.
- **Sign and order conventions.** Libraries differ in the order of the coefficients, the sign of the terms with odd $m$ (the Condon-Shortley phase) and the axis taken as the pole. Mixing two conventions in lines L2 and L3 gives wrong results that are hard to see. Test with a single directional light, whose result is known.
- **Ringing at line L4.** Without a window, a bright small light gives negative values on the far side of the sphere. With a window that is too strong, the light loses its direction. Choose $w_l$ for the brightest light of the scene.
- **Too few bands for the job.** Nine coefficients give good irradiance but not glossy reflection; a sharp shadow from the sun cannot be represented by a few bands at all.
- **Applying the cosine twice.** If the coefficients already contain the clamped cosine factors $\hat A_l$ (irradiance), multiplying again at line L5 by the cosine transfer blurs twice. Keep track of whether a vector stores radiance or irradiance.

## Exercises

1. Project the uniform environment $L(\omega) = 1$. *Answer:* $L_{00} = \int Y_{00}\, d\omega = 4\pi / (2\sqrt\pi) = 2\sqrt\pi$, and every other coefficient is 0 by orthogonality to the constant.
2. A unit directional light from $+z$ has coefficients $Y_{lm}(+z)$. Give the three that are not zero up to band 2. *Answer:* $Y_{00} = 0.2821$, $Y_{10} = \sqrt{3/(4\pi)} = 0.4886$ and $Y_{20} = \sqrt{5/(16\pi)} \cdot 2 = 0.6308$; all the others vanish at the pole.
3. Evaluate the order 3 projection of the light of Exercise 2 at $+z$. Why is it not infinite like the true light, and what is it? *Answer:* by the addition theorem, $\sum_m Y_{lm}(d)^2 = (2l + 1)/(4\pi)$, so the value is $(1 + 3 + 5)/(4\pi) = 9/(4\pi) \approx 0.716$. A truncated projection of a delta function is a smooth lobe of finite height.
4. Show that the diffuse result of a directional light from $+z$ on a surface with normal $+z$ is $17/16$ of the exact cosine result $1$ with nine coefficients. *Answer:* $\sum_l \hat A_l \sum_m Y_{lm}(z)^2 = \pi/(4\pi) + (2\pi/3)(3/(4\pi)) + (\pi/4)(5/(4\pi)) = 1/4 + 1/2 + 5/16 = 17/16$.

## References
