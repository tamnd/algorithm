---
tag: KFMF0H
kind: technique
slug: image-based-lighting
name: Image-based lighting
aliases:
- IBL
area: graphics-and-signals/real-time-rendering
level: core
summary: Light a scene with a captured high dynamic range image of the real surroundings, treating each texel as a distant light source.
prereqs: [environment-mapping, rendering-equation, monte-carlo-integration]
see_also: [irradiance-environment-map, split-sum-approximation, spherical-harmonic-lighting, cube-map, importance-sampling, precomputed-radiance-transfer, irradiance-volume, tone-mapping]
sources:
  - paper: doi:10.1145/280814.280864
    title: Paul Debevec, Rendering synthetic objects into real scenes, bridging traditional and image-based graphics with global illumination and high dynamic range photography, SIGGRAPH 98, 189 to 198
    locator: the light probe image of the real scene, its use as distant illumination in a global illumination renderer, and the differential rendering that composites synthetic objects into photographs (general locator)
  - url: https://www.pauldebevec.com/ReflectionMapping/illumap.pdf
    title: Gene S. Miller and C. Robert Hoffman, Illumination and Reflection Maps, Simulated Objects in Simulated and Real Environments, SIGGRAPH 84 course notes, Advanced Computer Graphics Animation
    locator: maps of real surroundings photographed at several exposures and convolved for diffuse and glossy reflection
  - url: https://cdn2.unrealengine.com/Resources/files/2013SiggraphPresentationsNotes-26915738.pdf
    title: Brian Karis, Real Shading in Unreal Engine 4, SIGGRAPH 2013 course Physically Based Shading in Theory and Practice
    locator: the section on image-based lighting (importance sampling of the GGX lobe, the split sum, the prefiltered environment map and the environment BRDF)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 10, Local Illumination (the parts on environment lighting and its prefiltering)
---

Image-based lighting lights a scene with a picture of real or rendered surroundings. The picture is a high dynamic range map of the radiance that arrives at one point from every direction, often made from photos of a mirror ball or from a panoramic camera at several exposures. Each texel acts as a light source at infinite distance. The light that a surface reflects toward the eye is then the integral, over all directions, of that radiance times the [BRDF](/brdf/) times the cosine, the local part of the [rendering equation](/rendering-equation/) with the environment as the only source. An offline renderer estimates the integral by [Monte Carlo integration](/monte-carlo-integration/), with [importance sampling](/importance-sampling/) of the BRDF or of the bright parts of the map. A real-time renderer precomputes it: an [irradiance environment map](/irradiance-environment-map/) for the diffuse part, and the [split sum approximation](/split-sum-approximation/) for the glossy part. Debevec (1998) made the method common for placing synthetic objects into photographs.

## In plain words

To make a computer object look like it belongs in a real place, light it with the light of that place. Take photos in every direction from where the object should stand, at several exposures, so that both the dark corners and the bright sun are recorded. This gives one image of all the light that arrives at that spot. Then treat every pixel of that image as a small lamp very far away. A matte part of the object sums the light from the half of the image it faces. A shiny part mostly shows the image in its mirror direction. Doing this sum for every pixel is slow, so games do most of the work once, ahead of time, and store the results in small textures.

## When it applies

- The light comes mostly from far away, compared to the size of the lit objects: outdoors under a sky, or a small object in a large room.
- A record of that light exists, or can be made: a photographed light probe, a rendered [cube map](/cube-map/), or an analytic sky.
- The renderer needs light from every direction, including soft light from the sky and colored bounce light from the ground, which a few point lights do not give.
- The lighting is about the same over the object, so one map can serve all of its points. Where it is not, several maps are placed in space, as probes.

## The template

```pseudo id=main
IBL-SHADE(p, n, v, L_env, f)
L1  L_env ← linear HDR radiance map of the surroundings of p     ▷ hole: capture or render
L2  reference: L_o ← (1/N) Σ_k L_env(l_k) f(l_k, v) max(n · l_k, 0) / pdf(l_k)   ▷ N samples l_k
L3  real time, diffuse: D ← (ρ / π) · E(n)                         ▷ E from an irradiance map
L4  real time, specular: S ← P(r, α) · (F_0 · A(α, n · v) + B(α, n · v))   ▷ split sum
L5  return V · (D + S)                                             ▷ hole: occlusion V
```

**The map (line L1).** The map must hold linear radiance, not display values, and its range must include the sun and lamps; a map clipped at the brightest texels loses most of the energy of a sunny day. Photos at several exposures are merged into one HDR image. The map is valid at the point where it was taken.

**The reference estimate (line L2).** This is Monte Carlo integration of the reflected radiance. The sample directions $l_k$ come from a density that follows the BRDF lobe, the cosine, or the brightness of the map; [multiple importance sampling](/multiple-importance-sampling/) combines these. The estimate is unbiased for any density that is positive wherever the integrand is not zero (a proved property of importance sampling), and its noise falls as $1/\sqrt N$.

**The diffuse part (line L3).** For a [Lambertian](/lambertian-reflectance/) surface with albedo $\rho$, the integral is $(\rho / \pi) E(n)$, with $E(n)$ the irradiance for the normal $n$. It depends only on $n$, so it can be stored per normal: as a convolved cube map, or as nine spherical harmonic coefficients.

**The specular part (line L4).** For a glossy [microfacet BRDF](/microfacet-brdf/), the integral depends on $v$, $n$ and the roughness $\alpha$. The split sum approximation stores a map $P$ prefiltered by the lobe per roughness, looked up at the reflected direction $r$, and a 2D table of the scale $A$ and the bias $B$ of $F_0$.

**Occlusion (line L5).** The map does not know about the object itself, so parts of the object that hide the sky from a point are ignored. A factor $V$ from [ambient occlusion](/ambient-occlusion/) darkens such points (a heuristic). [Precomputed radiance transfer](/precomputed-radiance-transfer/) includes the shadowing in the precomputation instead.

## Classic examples

- **Synthetic objects in photographs.** Debevec (1998) lit objects with a light probe of a real scene in a global illumination renderer, and composited them with differential rendering: the photo plus the difference between renders of a local scene model with and without the objects, which adds their shadows and reflections.
- **Diffuse light in games.** The [irradiance environment map](/irradiance-environment-map/) turns line L3 into a quadratic form in the normal, a few multiply-adds per pixel.
- **Glossy reflections in games.** The [split sum approximation](/split-sum-approximation/) turns line L4 into one cube map lookup and one 2D table lookup.
- **Probes in space.** An [irradiance volume](/irradiance-volume/) stores many small diffuse maps on a grid, so that the light can change across a level.
- **Shadows from the environment.** [Precomputed radiance transfer](/precomputed-radiance-transfer/) precomputes how each point of a static object sees the map, including its own shadows.

## Variations

- **Sampling the map.** For maps with a small bright sun, sampling by the brightness of the map, with a 2D table of its distribution, removes most of the noise of line L2. For rough surfaces, sampling the BRDF is better; multiple importance sampling uses both.
- **Extracting the sun.** Remove the brightest texels into one directional light with a sharp shadow map, and light the rest with the smooth map. This keeps hard shadows, which a map alone gives only at high sample counts.
- **Spherical harmonics.** Store the whole map as a few [spherical harmonic](/spherical-harmonic-lighting/) coefficients. This is enough for diffuse light and cheap to rotate and blend, but too blurry for glossy reflection.
- **Local maps.** Render maps at several points of a level and blend them by position, with a box or sphere proxy to correct the parallax of reflections, see [environment mapping](/environment-mapping/).
- **Dynamic maps.** Render the map from the scene at run time and prefilter it on the GPU, so that the lighting follows changes in the scene or the time of day.

## Pitfalls

- **Clipped range at line L1.** A map stored in 8 bits, or a photo with a saturated sun, loses the strongest light. The scene then looks flat and has no clear shadows. Merge several exposures, or add the sun back as a separate light.
- **Display values at line L1.** A map in sRGB or tone mapped values is not radiance. Decode it to linear values before any integral, see [gamma correction](/gamma-correction/), and apply [tone mapping](/tone-mapping/) only to the final image.
- **Noise at line L2.** A few BRDF samples of a map with a small bright source give fireflies. Sample the map as well, or use more samples.
- **Double counting at line L5.** If the sun is extracted as a separate light, remove it from the map, or the surfaces get its light twice.
- **Units and scale.** The map of a real place has an absolute brightness that the exposure of the camera sets. Mixing it with analytic lights in other units gives the wrong balance; calibrate the map, for example with a gray card or a light meter reading.
- **The distant light assumption.** A map taken at one point is wrong for points far from it, and for objects close to the walls. Use several probes, or a local correction, when the object moves through the scene.

## Exercises

1. A white Lambertian surface ($\rho = 1$) sits under a uniform environment of radiance $L$. Show that it reflects radiance $L$ for every normal. *Answer:* $E(n) = \int_{\Omega} L \max(n \cdot l, 0)\, dl = \pi L$, so $L_o = (\rho/\pi)\pi L = L$. This is the white furnace test of a renderer.
2. In line L2 for the surface of Exercise 1, take the density $\text{pdf}(l) = \max(n \cdot l, 0) / \pi$. Show that every sample gives exactly $L$, so the estimate has no variance. *Answer:* each term is $L \cdot (1/\pi) \cdot \cos / (\cos / \pi) = L$.
3. The sun covers about $6.8 \times 10^{-5}$ sr of the sky. With BRDF sampling of a diffuse surface, about what fraction of the samples hit the sun when it is straight above? *Answer:* the cosine density near the normal is $1/\pi$ per steradian, so about $6.8 \times 10^{-5} / \pi \approx 2.2 \times 10^{-5}$, one sample in about 46000. This is why the sun is sampled or extracted separately.

## References
