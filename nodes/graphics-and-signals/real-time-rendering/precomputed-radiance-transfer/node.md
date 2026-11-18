---
tag: G3ZSSD
kind: technique
slug: precomputed-radiance-transfer
name: Precomputed radiance transfer
aliases:
- PRT
area: graphics-and-signals/real-time-rendering
level: research
summary: Precompute how each point of a static object transfers low-frequency incident light, including shadows and interreflection, in a spherical harmonic basis.
prereqs: [spherical-harmonic-lighting, ambient-occlusion]
see_also: [spherical-harmonic-lighting, irradiance-environment-map, image-based-lighting, light-mapping, irradiance-volume, principal-component-analysis, haar-wavelet, global-illumination]
sources:
  - paper: doi:10.1145/566654.566612
    title: Peter-Pike Sloan, Jan Kautz and John Snyder, Precomputed radiance transfer for real-time rendering in dynamic, low-frequency lighting environments, ACM Transactions on Graphics 21(3), 2002, 527 to 536
    locator: the transfer function per point for diffuse surfaces with and without shadows and interreflections, its projection onto spherical harmonics, the transfer matrices for glossy surfaces, and shading as a dot product with the projected lighting (general locator)
  - url: http://www.cs.umd.edu/class/spring2005/cmsc828v/papers/spherical-harmonic-lighting.pdf
    title: Robin Green, Spherical Harmonic Lighting, The Gritty Details, Game Developers Conference 2003
    locator: the shadowed and interreflected diffuse transfer and its precomputation by ray casting (general locator)
  - paper: doi:10.1145/383259.383317
    title: Ravi Ramamoorthi and Pat Hanrahan, An efficient representation for irradiance environment maps, SIGGRAPH 2001, 497 to 500
    locator: Section 2, the coefficients of the clamped cosine, which are the unshadowed diffuse transfer
---

Precomputed radiance transfer (PRT) shades a static object under distant lighting that changes every frame, with soft shadows and bounced light, at the cost of a dot product per vertex. The light that leaves a point of a diffuse object is the integral, over all directions, of the incoming radiance times a transfer function: the albedo over $\pi$, the clamped cosine, and the visibility of the environment from that point. The transfer function depends only on the object, so it can be computed once, offline, and projected onto [spherical harmonics](/spherical-harmonic-lighting/). The lighting is projected onto the same basis each frame. Because the basis is orthonormal, the integral becomes the dot product of the two coefficient vectors. Interreflections are added to the transfer function by an offline simulation, and the run time cost does not change. Sloan, Kautz and Snyder introduced the method in 2002. It works for low frequency lighting only: a few bands cannot represent the sharp shadow of a small sun.

## In plain words

Some spots of a statue see the whole sky. Others hide in a fold and see only a small part of it, and some also get light that bounces off a nearby part of the statue. All of that depends on the shape of the statue, not on what the sky looks like today. So, ahead of time, record for every spot how it responds to light from each direction, in a compact form of a few numbers. At run time, write the current sky in the same compact form. The brightness of each spot is then a short sum of products of the two lists of numbers. The sky can change, turn or move, and the statue gets soft shadows and bounce light at once. Sharp shadows need too many numbers.

## When it applies

- The object is static, or moves only rigidly, since a rigid motion is a rotation of the lighting relative to the object.
- The lighting is distant and the same over the object, such as an environment map or a sky, and it changes at run time.
- The lighting is smooth enough for a few bands of spherical harmonics, or the result is allowed to be soft.
- Soft shadows, ambient occlusion and bounced light matter, and per-frame ray tracing is too expensive.

## The template

1. **Define the transfer function.** For a diffuse point $p$ with normal $n$ and albedo $\rho$: $T(p, \omega) = (\rho/\pi)\, V(p, \omega) \max(n \cdot \omega, 0)$, with $V$ equal to 1 where the environment is visible and 0 where the object blocks it. Without $V$ this is unshadowed transfer, and the result is the [irradiance environment map](/irradiance-environment-map/).
2. **Project it offline.** $T_{lm}(p) = \int T(p, \omega) Y_{lm}(\omega)\, d\omega$, by casting rays from each vertex in many directions.
3. **Add interreflections offline.** Run more passes in which each point gathers the transfer vectors of the points that its rays hit, weighted by their albedo, and adds them to its own vector.
4. **Project the lighting at run time.** Compute $L_{lm}$ for the current lighting, and rotate it into the frame of the object.
5. **Shade.** $B(p) = \sum_{lm} L_{lm} T_{lm}(p)$ per vertex, interpolated over triangles.

```pseudo id=main
PRT(object, L)
L1  offline, for each vertex p and each sample direction ω_j with weight Δω_j:
L2      t ← (ρ/π) · VISIBLE(p, ω_j) · max(n_p · ω_j, 0)   ▷ hole: visibility by ray casting
L3      for each (l, m):  T[p][l, m] ← T[p][l, m] + t · Y_lm(ω_j) · Δω_j
L4  offline: add interreflection passes to T             ▷ hole: optional
L5  each frame:  c ← the coefficients of L, rotated into the object frame
L6  for each vertex p:  B[p] ← Σ_{l, m} c[l, m] · T[p][l, m]
L7  return B, interpolated over the triangles
```

**Precomputation (lines L1 to L4).** For each vertex, rays in many directions test visibility; each visible direction adds its weighted cosine to the projection. With $n^2$ coefficients, the cost is the number of vertices times the number of directions times $n^2$, plus the rays. Interreflection passes reuse the same rays and add, for each blocked direction, the transfer of the hit point.

**Run time (lines L5 to L7).** Projecting the lighting costs the same as for an irradiance map, once per frame. Each vertex then costs one dot product of $n^2$ numbers per color channel. Rotating the lighting instead of the object keeps the transfer vectors fixed.

**Glossy surfaces.** For a view dependent BRDF, the transfer is a matrix per point: it maps the lighting coefficients to the coefficients of the transferred incident radiance, which the shader then convolves with the BRDF and evaluates at the view direction. The cost per point grows from $n^2$ to $n^4$.

## Classic examples

- **Unshadowed diffuse.** With $V = 1$, $T_{lm}(p) = (\rho/\pi) \hat A_l Y_{lm}(n_p)$, and the method is the [irradiance environment map](/irradiance-environment-map/).
- **Ambient occlusion.** The band 0 coefficient of the shadowed transfer is proportional to the cosine weighted [ambient occlusion](/ambient-occlusion/) of the point; PRT keeps the direction of the visible part too.
- **Light maps of transfer.** Store transfer vectors in a texture instead of per vertex, like a [light map](/light-mapping/) that can be relit.
- **Probes.** Store per probe of an [irradiance volume](/irradiance-volume/) the transfer of the static scene, so that the probe light follows a moving sun.

## Variations

- **Compression.** Many vertices have similar transfer vectors or matrices. Clustering with [principal component analysis](/principal-component-analysis/) per cluster stores each as a few weights of basis vectors, and the shader works on the small basis.
- **All frequencies.** A wavelet basis on a cube map, such as the [Haar wavelet](/haar-wavelet/), keeps only the largest coefficients of the lighting each frame. This gives sharper shadows than spherical harmonics, but rotation of the lighting is no longer cheap.
- **Neighborhood transfer.** Precompute how an object shadows the space around it, so that it can cast soft shadows on other objects that move.
- **Deformable objects.** Approximate the visibility by simple proxies such as spheres, and recompute the transfer each frame with a cheap formula.
- **Local lights.** Sample the lighting at a few points of the object and interpolate, when the lights are too close for one distant map.

## Pitfalls

- **Wrong frame at line L5.** The lighting must be rotated into the frame in which line L3 projected the transfer. Forgetting the rotation of the object makes the shadows stay fixed while the object turns.
- **Too few directions at line L1.** Few rays per vertex give noisy transfer, visible as blotches that change with the lighting. Use stratified directions and enough of them for the chosen order.
- **Self-intersection at line L2.** Rays that start exactly on the surface hit the triangle they start from. Offset the origin along the normal.
- **Under-tessellated meshes.** Transfer is stored per vertex, so a shadow smaller than a triangle is lost or smeared. Subdivide, or store transfer in textures.
- **Ringing.** A bright, small light projected onto a few bands gives negative light in shadowed areas. Window the lighting coefficients, see [spherical harmonic lighting](/spherical-harmonic-lighting/).
- **Expecting sharp shadows.** With order 4 or 5, shadows are blurred over tens of degrees. A sun needs a separate shadow map, with PRT for the sky and the bounce light.

## Exercises

1. Show that with $V = 1$ and $\rho = \pi$, the result of line L6 is the irradiance $E(n_p)$ of the irradiance map for band-limited lighting. *Answer:* then $T(p, \omega) = \max(n_p \cdot \omega, 0)$, whose coefficients are $\hat A_l Y_{lm}(n_p)$, and $\sum_{lm} L_{lm} \hat A_l Y_{lm}(n_p) = \sum_{lm} E_{lm} Y_{lm}(n_p) = E(n_p)$.
2. A mesh of 100000 vertices stores order 4 transfer vectors, one per vertex, as 32-bit floats. How much memory is that, and for order 4 transfer matrices? *Answer:* $16$ floats per vertex give 6.4 MB; matrices of $16 \times 16$ give 102.4 MB per color channel, which is why compression matters for glossy PRT.
3. Show that the shadowed transfer of a point is never larger than its unshadowed transfer in band 0. *Answer:* $T_{00} = Y_{00} \int (\rho/\pi) V \max(n \cdot \omega, 0)\, d\omega$, and $0 \le V \le 1$.

## References
