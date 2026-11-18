---
tag: C9A0AG
kind: technique
slug: split-sum-approximation
name: Split sum approximation
aliases:
- prefiltered environment map with BRDF lookup
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Split the specular image-based lighting integral into a prefiltered environment map and a precomputed two-dimensional BRDF table.
prereqs: [image-based-lighting, ggx-distribution, schlick-fresnel-approximation, mipmap]
see_also: [image-based-lighting, irradiance-environment-map, cube-map, microfacet-brdf, smith-masking-shadowing-function, importance-sampling, screen-space-reflections, physically-based-shading]
sources:
  - url: https://cdn2.unrealengine.com/Resources/files/2013SiggraphPresentationsNotes-26915738.pdf
    title: Brian Karis, Real Shading in Unreal Engine 4, SIGGRAPH 2013 course Physically Based Shading in Theory and Practice
    locator: the section Image-Based Lighting, with Equation 7 (the split sum), the prefiltered environment map with n = v = r, Equation 8 and the environment BRDF table of a scale and a bias to F0
  - paper: doi:10.1145/2504435.2504457
    title: Dimitar Lazarov, Getting More Physical in Call of Duty, Black Ops II, SIGGRAPH 2013 course Physically Based Shading in Theory and Practice
    locator: the split of the environment lighting into a prefiltered map and an environment BRDF, and the analytic fit of the environment BRDF (course notes at blog.selfshadow.com)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 10, Local Illumination (the part on prefiltered environment maps for glossy reflection)
---

The split sum approximation computes the glossy reflection of an environment map with two texture reads. The exact reflected radiance is the integral, over all light directions, of the environment radiance times a [microfacet BRDF](/microfacet-brdf/) times the cosine. It depends on the view direction, the normal, the roughness and the Fresnel reflectance at normal incidence $F_0$, too many inputs for a table. Karis (2013), for Unreal Engine 4, wrote the importance sampled estimate of this integral as the product of two sums: the average of the environment over the lobe, and the integral of the BRDF times the cosine alone. The first sum is stored in a prefiltered [cube map](/cube-map/), one [mipmap](/mipmap/) level per roughness, under the extra assumption that the normal, the view and the reflected direction coincide. The second sum, with the [Schlick approximation](/schlick-fresnel-approximation/) of the Fresnel term, becomes $F_0 A + B$ with $A$ and $B$ in a 2D table over the roughness and $n \cdot v$. The split is exact for a constant environment and a heuristic otherwise. Lazarov (2013) used the same split, with an analytic fit of the table, in Call of Duty: Black Ops II.

## In plain words

A rough metal ball reflects a blurred picture of the room. How blurred depends on the roughness, and how bright depends on the angle you look at it from. Doing the full blur for every pixel needs hundreds of samples of the room. The trick is to do the two parts apart. First, blur the picture of the room ahead of time, once for each roughness, and store the blurred copies. Second, work out ahead of time how strong the reflection is for each roughness and each viewing angle, and store that in a small table. At run time, read the blurred room in the mirror direction, read the table, and multiply. The answer is right for a room of one flat color, and close for most rooms.

## When it applies

- The surface uses a microfacet BRDF with the [GGX distribution](/ggx-distribution/) or a similar lobe, and the Schlick Fresnel term.
- The lighting is a distant environment map, as in [image-based lighting](/image-based-lighting/), and the map changes rarely enough that prefiltering it is affordable.
- The budget per pixel is a few texture reads, not hundreds of samples.
- Errors at grazing angles and on very rough surfaces are acceptable, because the method assumes the shape of the lobe at normal incidence.

## The template

1. **Write the estimate.** With $N$ directions $l_k$ sampled from the lobe, $L_o \approx \frac{1}{N} \sum_k L(l_k) f(l_k, v) \cos\theta_{l_k} / p(l_k)$.
2. **Split it.** Replace this by $\big(\frac{1}{N} \sum_k L(l_k)\big) \cdot \big(\frac{1}{N} \sum_k f(l_k, v) \cos\theta_{l_k} / p(l_k)\big)$, Karis's Equation 7.
3. **Prefilter the environment.** Compute the first factor per roughness and per reflected direction $r$, assuming $n = v = r$, and weight each sample by $\cos\theta_{l_k}$, which Karis reports gives better results.
4. **Tabulate the BRDF.** With Schlick, the second factor is $F_0 A + B$, where $A$ and $B$ depend only on the roughness and $n \cdot v$.
5. **Shade.** Multiply the two lookups.

```pseudo id=main
SPLIT-SUM(n, v, α, F_0)
L1  offline: for each mip level m and each texel direction r:  P[m](r) ← Σ_k L(l_k) (r · l_k)⁺ / Σ_k (r · l_k)⁺,  l_k from GGX(α_m) around n = v = r
L2  offline: for each (α, μ) of a 2D grid:  (A, B) ← (1/N) Σ_k G_vis,k · ((1 - F_c,k), F_c,k),  F_c = (1 - v · h_k)^5
L3  r ← 2 (n · v) n - v
L4  pre ← P sampled at r, at the mip level of α
L5  (A, B) ← table(α, n · v)
L6  return pre · (F_0 · A + B)
```

**Prefiltering (line L1).** Each texel of level $m$ stores the average of the environment over the GGX lobe of roughness $\alpha_m$ around its direction. The lobe is sampled at normal incidence ($n = v = r$), so the result depends only on $r$ and $\alpha$ and fits in a cube map. Karis stores the levels in the mip chain of one cube map, with roughness growing with the level.

**The table (line L2).** The half vectors $h_k$ are sampled from the GGX distribution, and for this density the weight of a sample is $G_{\text{vis}} = G (v \cdot h) / ((n \cdot h)(n \cdot v))$, with $G$ the [Smith masking-shadowing function](/smith-masking-shadowing-function/). With Schlick, $F = F_0 + (1 - F_0) F_c = F_0 (1 - F_c) + F_c$, so $F_0$ comes out of the sum, and two numbers per entry remain: a scale and a bias of $F_0$. Karis stores them in a two channel texture of 16 bits per channel.

**Shading (lines L3 to L6).** The reflected direction picks the texel of the prefiltered map, the roughness picks the level, and the table gives the scale and bias. The cost is two filtered texture reads and a few multiply-adds per pixel.

## Classic examples

- **Unreal Engine 4.** Karis (2013) introduced the split, the prefiltered cube map with $n = v = r$ and the 2D table, as the glossy part of [image-based lighting](/image-based-lighting/). He reports that the $n = v = r$ assumption, which loses the long stretched reflections at grazing angles, is the larger source of error of the method.
- **Call of Duty: Black Ops II.** Lazarov (2013) split the environment lighting the same way, and replaced the 2D table by an analytic function fitted to it, which saves a texture on older hardware.
- **Diffuse partner.** Engines that use the split sum for the specular part use an [irradiance environment map](/irradiance-environment-map/) or a convolved [cube map](/cube-map/) for the diffuse part.
- **Probe systems.** Each reflection probe of a level is a prefiltered cube map as in line L1; the diffuse part comes from an [irradiance volume](/irradiance-volume/).

## Variations

- **Energy compensation.** The table also gives the directional albedo of the BRDF, $A + B$ for $F_0 = 1$, which is below 1 for rough surfaces, because a single scattering microfacet BRDF loses the light that bounces between facets. Scaling by its inverse adds back an estimate of that light (a heuristic).
- **Analytic table.** Fit $A$ and $B$ by simple functions of $\alpha$ and $n \cdot v$, as Lazarov did, to save the texture and the read.
- **Better lobes for the prefilter.** Fetch along a direction bent from $r$ toward $n$ for rough surfaces, which follows the peak of the real lobe better than $r$ (a heuristic).
- **Real-time prefiltering.** For maps rendered at run time, prefilter on the GPU each frame or each few frames, with fewer samples per texel and filtered importance sampling, which reads lower mip levels of the source to reduce noise.
- **Other BRDFs.** The same split works for cloth or sheen lobes with their own tables, and a third channel of the table can hold a second lobe.

## Pitfalls

- **Wrong mip level at line L4.** The map between roughness and mip level must be the same in line L1 and in line L4. A mismatch makes reflections too sharp or too blurry, worst at mid roughness.
- **The wrong k at line L2.** Karis uses $k = \alpha/2$ in the Schlick form of $G$ for image-based lighting. The remapped $k = (\text{roughness} + 1)^2 / 8$, which he uses for analytic lights, makes the results at glancing angles much too dark when it is used for the table.
- **Seams at line L1.** A per-face blur of the cube map gives visible lines at the edges at high roughness. Sample in direction space across faces, and use seamless filtering at line L4.
- **Bright pixels in line L1.** Few samples of a map with a small bright source give speckles in the prefiltered levels. Use more samples, or sample lower mip levels of the source for samples with a low density.
- **Expecting exactness.** The product of two averages equals the average of the product only when one factor is constant over the lobe. Errors grow for rough surfaces in environments with strong contrast, and at grazing angles, where the real lobe is stretched and the prefiltered lobe is not.
- **Linear values.** Prefilter linear radiance in high range. Prefiltering sRGB values or clamped values gives the wrong averages.

## Exercises

1. Show that the split is exact when the environment is constant, $L(l) = c$. *Answer:* with the cosine weights, the first factor of line L1 is $c \sum_k \cos / \sum_k \cos = c$, so the product is $c$ times the second factor, which is the estimate of $\int f \cos$; the full estimate is $c$ times the same sum.
2. Show that $F = F_0 + (1 - F_0) F_c$ gives $\int f \cos = F_0 A + B$ with $A = \int (f / F)(1 - F_c) \cos$ and $B = \int (f / F) F_c \cos$. *Answer:* $F = F_0 (1 - F_c) + F_c$; the factor $f / F$ does not depend on $F_0$, so the integral is linear in $F_0$ with these two coefficients.
3. In the limit of a perfect mirror ($\alpha \to 0$), what does the table give? *Answer:* every half vector equals $n$ and $G \to 1$, so $G_{\text{vis}} \to 1$ and $v \cdot h = n \cdot v$. Then $A = 1 - (1 - n \cdot v)^5$, $B = (1 - n \cdot v)^5$, and $F_0 A + B$ is the Schlick Fresnel term at $n \cdot v$, as it should be for a mirror.

## References
