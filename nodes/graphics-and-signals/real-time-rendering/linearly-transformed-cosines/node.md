---
tag: QF6BT4
kind: technique
slug: linearly-transformed-cosines
name: Linearly transformed cosines
aliases:
- LTC area lighting
area: graphics-and-signals/real-time-rendering
level: research
summary: Shade with polygonal area lights in real time by fitting each BRDF lobe as a clamped cosine distribution under a 3x3 linear transform.
prereqs: [ggx-distribution, microfacet-brdf]
see_also: [microfacet-brdf, ggx-distribution, split-sum-approximation, sutherland-hodgman, polygon-clipping, lambertian-reflectance, physically-based-shading, clustered-shading]
sources:
  - paper: doi:10.1145/2897824.2925895
    title: Eric Heitz, Jonathan Dupuy, Stephen Hill and David Neubelt, Real-time polygonal-light shading with linearly transformed cosines, ACM Transactions on Graphics 35(4), 2016 (SIGGRAPH 2016)
    locator: the definition of linearly transformed distributions and their Jacobian, the integration over polygons by transforming the polygon, the fit of GGX lobes per roughness and view angle, and the clipping to the upper hemisphere (general locator)
  - paper: doi:10.1145/218380.218467
    title: James Arvo, Applications of irradiance tensors to the simulation of non-Lambertian phenomena, SIGGRAPH 95, 335 to 342
    locator: the closed form integral of the cosine over a spherical polygon as a sum over its edges (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 10, Local Illumination (the part on area lights and polygonal lights)
---

Linearly transformed cosines (LTCs) give the light that a glossy surface reflects from a polygonal area light, in closed form, in a shader. The integral of a clamped cosine over a polygon on the sphere has an exact formula, a sum over the edges, known since Lambert. A [microfacet BRDF](/microfacet-brdf/) lobe has no such formula. Heitz, Dupuy, Hill and Neubelt (2016) observed that applying a $3 \times 3$ matrix $M$ to the directions of a clamped cosine distribution gives a family of distributions that can stretch, skew and scale the cosine into shapes close to [GGX](/ggx-distribution/) lobes, and that the integral of such a distribution over a polygon equals the integral of the plain cosine over the polygon transformed by $M^{-1}$. So the shader transforms the corners of the light by $M^{-1}$, clips the polygon to the upper hemisphere, and applies the edge formula. The matrices are fitted offline per roughness and view angle and read from a small table. The integration is exact for the fitted distribution, a proved property; how well the fit matches the BRDF is a measured property of the fit.

## In plain words

A lamp shaped like a rectangle, such as a TV screen or a window, lights a shiny floor. To find the brightness at one spot, you would add up the reflected light from every point of the rectangle, which is slow. For a matte floor there is a neat exact formula: walk around the corners of the rectangle and add one simple term per side. A shiny floor has a more complex shape of reflection. The trick is to bend space so that the shiny shape turns into the matte shape. You bend the corners of the lamp the same way, and then use the neat formula on the bent lamp. The bending for each roughness and angle is found ahead of time and stored in a small table.

## When it applies

- The lights are polygons (rectangles, quads, triangles) or shapes that can be written as polygons, with constant radiance, and the shading needs their exact shape, not a point.
- The BRDF lobe is smooth enough that one transformed cosine fits it well, such as GGX for a range of roughness, or a diffuse lobe.
- The view direction enters only through the angle to the normal, so that an isotropic lobe needs a 2D table over the roughness and that angle.
- Shadows from the light are handled separately, or ignored, since the method integrates the light without visibility.

## The template

1. **Fit offline.** For each roughness $\alpha$ and view angle $\theta_v$ of a grid, find a matrix $M$ such that the distribution $D(\omega) = D_o(\omega_o) \left|\partial \omega_o / \partial \omega\right|$, with $D_o(\omega_o) = \max(z_o, 0)/\pi$ and $\omega_o = M^{-1}\omega / \|M^{-1}\omega\|$, is close to the normalized BRDF lobe times the cosine. Store $M^{-1}$, and the magnitude of the lobe, in textures.
2. **Transform the light.** In a frame with $z$ along the normal and $x$ in the plane of the normal and the view, transform each corner of the polygon, relative to the shaded point, by $M^{-1}$.
3. **Clip.** Clip the transformed polygon to $z \ge 0$, because the cosine is clamped.
4. **Integrate.** Apply the edge formula of the cosine to the clipped polygon.
5. **Scale.** Multiply by the radiance of the light and the magnitude of the BRDF, with the Fresnel term.

```pseudo id=main
LTC-SHADE(x, n, v, α, P, L_light)
L1  frame: z ← n;  x̂ ← normalize(v - (n · v) n);  ŷ ← z × x̂
L2  M⁻¹ ← table(α, n · v);  (A, B) ← magnitude table(α, n · v)    ▷ fitted offline
L3  for each corner p_i of P:  q_i ← M⁻¹ · (the coordinates of p_i - x in the frame)
L4  Q ← CLIP(q, z ≥ 0)                                               ▷ polygon clipping
L5  I ← (1 / 2π) Σ over the edges (a, b) of Q:  acos(â · b̂) · (normalize(â × b̂))_z
L6  return L_light · I · (F_0 · A + B)
```

**The frame (line L1).** An isotropic lobe is symmetric about the plane of the normal and the view, so in this frame the matrix depends only on $\alpha$ and $n \cdot v$, and it has few free entries.

**The table (line L2).** The fitted matrices go in a 2D texture over roughness and $n \cdot v$. A second table holds the scale and bias of $F_0$, as in the [split sum approximation](/split-sum-approximation/), since the LTC itself is normalized.

**The transform (line L3).** The integral of $D$ over the polygon $P$ equals the integral of $D_o$ over the polygon $M^{-1} P$, by the change of variables $\omega_o = M^{-1}\omega / \|M^{-1}\omega\|$, a proved property. Directions are only defined up to a positive scale, so the corners need not be normalized here.

**Clipping (line L4).** The edge formula is the integral of $z$ over the polygon, which is the clamped cosine only when the polygon lies in $z \ge 0$. Clipping a polygon by a plane through the origin is the [Sutherland-Hodgman](/sutherland-hodgman/) step for one plane.

**The edge formula (line L5).** For a spherical polygon in the upper hemisphere, $\int \max(z, 0)/\pi\, d\omega = \frac{1}{2\pi} \sum_{\text{edges}} \theta_e\, (\gamma_e)_z$, where $\theta_e$ is the angle that the edge spans seen from the origin and $\gamma_e$ the unit normal of the plane through the edge and the origin (Lambert's formula; Arvo gives it in the language of irradiance tensors). The sign depends on the winding of the polygon, which also tells whether a one sided light faces the point.

## Classic examples

- **Rectangular lights on GGX.** The main case of Heitz and coauthors: a quad light on a [GGX](/ggx-distribution/) surface, four corners, clipping, and at most five edges after clipping.
- **Diffuse area lights.** For a [Lambertian](/lambertian-reflectance/) surface, $M$ is the identity and lines L3 to L5 are Lambert's formula itself.
- **Many area lights in a scene.** Engines combine LTC shading with [clustered shading](/clustered-shading/) to evaluate many polygon lights per pixel.
- **Textured lights.** For a light that shows an image, such as a screen, the result of line L5 is multiplied by a lookup in a prefiltered version of the image, at a level chosen from the size of the lobe on the light (a heuristic).

## Variations

- **Other shapes.** Disks, spheres and line lights have their own closed forms or approximations under the same transform.
- **Anisotropic lobes.** An anisotropic BRDF needs more parameters, a 3D or 4D table, or a fit per pixel.
- **Sampling.** Sampling an LTC is easy: sample the cosine and transform the direction by $M$. This makes LTCs useful as importance sampling densities, and for combining the analytic result with ray traced shadows.
- **Shadows.** Ray trace or shadow map the light, and multiply the analytic unshadowed result by the ratio of shadowed to unshadowed estimates from a few samples, a common form of ratio estimator.
- **Multiple lobes.** Fit a sum of two LTCs for lobes with a long tail, at twice the cost.

## Pitfalls

- **Skipping the clip at line L4.** Without clipping, the parts of the polygon below the horizon add negative light, and lights that cross the horizon of the surface give dark bands. Clip before line L5; a quad gives at most five corners after one clip.
- **The wrong frame at line L1.** The matrix was fitted in a frame with $x$ in the plane of the normal and the view. Using another tangent frame rotates the lobe around the normal, and the highlight moves.
- **Numerical problems in line L5.** For nearly parallel corners, `acos` loses precision and the cross product is close to zero. Use a stable form of $\theta / \sin\theta$ for short edges.
- **Interpolating the table.** The entries of $M^{-1}$ are interpolated bilinearly, which is fine where they change smoothly, but very low roughness gives matrices with large entries that interpolate badly. Clamp the roughness to the range of the fit.
- **Expecting exact BRDF results.** The fit is not the BRDF. The error is small for moderate roughness and grows for extreme roughness and grazing angles; it is a measured property of the fit.
- **Ignoring visibility.** The result has no shadows from the light. Add them separately, or accept that occluded lights still light the surface.

## Exercises

1. Show that $M$ and $sM$ for $s > 0$ give the same distribution. *Answer:* $(sM)^{-1}\omega / \|(sM)^{-1}\omega\| = M^{-1}\omega / \|M^{-1}\omega\|$, and the Jacobian $|M^{-1}| / \|M^{-1}\omega\|^3$ gains $s^{-3}$ in both the numerator and the denominator. So one entry of $M$ can be fixed to 1.
2. Apply the formula of line L5 to the polygon with corners $+x$, $+y$, $-x$, $-y$ on the horizon, wound counterclockwise seen from above. *Answer:* each edge spans $\pi/2$, and the plane of each edge is the horizon plane with normal $+z$, so $I = \frac{1}{2\pi} \cdot 4 \cdot \frac{\pi}{2} = 1$, the integral of $\max(z, 0)/\pi$ over the hemisphere.
3. With $M$ the identity, a small light straight above the normal covers a solid angle $\Omega$. Give the result of line L5 to first order. *Answer:* the integrand is about $1/\pi$ near the normal, so $I \approx \Omega / \pi$.

## References
