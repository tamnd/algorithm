---
tag: SP0023
kind: technique
slug: visibility-buffer
name: Visibility buffer
aliases:
- deferred texturing
area: graphics-and-signals/real-time-rendering
level: research
summary: A deferred method that stores only the triangle and instance id of the visible surface per pixel, and computes the attributes and their derivatives again from the vertex data when it shades.
prereqs: [deferred-shading, perspective-correct-interpolation]
see_also: [g-buffer, deferred-shading, mipmap, multisample-antialiasing, warp-divergence, memory-coalescing, triangle-rasterization, texture-mapping]
sources:
  - url: http://jcgt.org/published/0002/02/04/
    title: "Christopher A. Burns and Warren A. Hunt, The visibility buffer: a cache-friendly approach to deferred shading, Journal of Computer Graphics Techniques 2(2), 55-69, 2013"
    locator: the buffer of triangle and instance ids, the reconstruction of the attributes and their derivatives in the shading pass, and the memory and bandwidth comparison with a G-buffer
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 20, Efficient Shading (the part on decoupling visibility from shading)
  - paper: doi:10.1145/97880.97901
    title: "Takafumi Saito and Tokiichiro Takahashi, Comprehensible rendering of 3-D shapes, SIGGRAPH 1990, Computer Graphics 24(4), 197-206"
    locator: the G-buffer that the visibility buffer replaces
---

A visibility buffer is a deferred rendering method that stores almost nothing per pixel. The geometry pass writes only the depth and an id of the visible triangle, made of the id of the instance (the drawn object) and the index of the triangle in its mesh. The shading pass then reads the id, fetches the three vertices of that triangle, computes the barycentric coordinates of the pixel, interpolates the attributes such as the normal and the texture coordinates, computes their screen-space derivatives for texture filtering, and shades. Burns and Hunt described it in 2013 and argued that it uses memory and caches better than a [G-buffer](/g-buffer/) when the buffer is large, for example at high resolution or with many samples per pixel. The general two-pass scheme is on the [deferred shading](/deferred-shading/) page. This page is the variant that keeps visibility and attributes apart.

## In plain words

A G-buffer writes down everything about the surface at each pixel: its direction, color and roughness. That is a lot of memory per pixel, and with antialiasing it is multiplied by the number of samples. The visibility buffer writes down only a name tag: which triangle of which object is visible. Later, when it lights the pixel, it looks the triangle up, takes its three corners, works out where in the triangle the pixel lies, and blends the corner values to get the normal and the texture position. This repeats work that the G-buffer did once, but it reads and writes much less memory, and memory is often the slower part.

## When it applies

The technique fits when:

- **The G-buffer traffic is the limit.** High resolutions, MSAA with many samples, or a thick G-buffer make the write and read of attributes cost more than the vertex work saved.
- **Triangles are larger than pixels on average.** Many pixels share a triangle, so its vertex data stays in the cache. With very small triangles, each pixel fetches and transforms its own three vertices.
- **The vertex data is available in the shading pass.** The shading pass needs the positions and attributes of all visible triangles, and the transforms of all instances, in buffers that it can index. Animated meshes must keep their transformed positions or transform them again.
- **The shading can be grouped by material.** All pixels of a material run the same shader. Pixels of different materials in one warp cause [warp divergence](/warp-divergence/).

The cost model uses $p$ pixels, $m$ samples per pixel, $b_V$ bytes per sample for the visibility buffer (often 4 or 8) and $b_G$ bytes per sample for a G-buffer. The geometry pass writes $O(f\, b_V)$ bytes for $f$ fragments that pass the depth test, against $O(f\, b_G)$ for a G-buffer. The shading pass reads $O(p\, b_V)$ bytes plus the vertex data of the visible triangles, and does $O(1)$ extra arithmetic per pixel for the barycentrics and the interpolation.

## The template

The camera looks along $-z$. Pixel centers are at $(i + 1/2, j + 1/2)$. The id is packed into one integer, for example 32 bits split between the instance and the triangle index; the split is a choice of the engine.

```pseudo id=main
VISIBILITY-BUFFER(instances, lights)
L1  clear V to none and the depth buffer D to the background
L2  for each instance g and each triangle t of g, and each fragment at q   ▷ geometry pass
L3      if the fragment depth < D[q] then D[q] ← depth;  V[q] ← PACK(g, t)
L4  for each pixel q with V[q] ≠ none                                      ▷ shading pass
L5      (g, t) ← UNPACK(V[q]);  fetch the three vertices of t, transform them by the matrix of g and project them
L6      (b0, b1, b2) ← the perspective-correct barycentric coordinates of the center of q in the projected triangle
L7      a ← b0 a0 + b1 a1 + b2 a2 for each attribute;  ∂a/∂x, ∂a/∂y from the barycentrics at q + (1, 0) and q + (0, 1)
L8      out[q] ← SHADE(the material of g at a, with the texture lookups filtered by the derivatives, lights)
```

**The geometry pass (lines L1 to L3).** The fragment shader does no texture reads and writes one integer. The depth test keeps the nearest fragment, as in the [z-buffer](/z-buffer/). The pass is cheap enough that a depth pre-pass is not needed.

**The barycentrics (line L6).** Let the projected vertices have the screen positions $s_0, s_1, s_2$ and the clip-space $w$ values $w_0, w_1, w_2$. The 2D barycentrics $\lambda_i$ of the pixel center in the screen triangle are areas of sub-triangles divided by the area of the triangle. The perspective-correct ones are $b_i = (\lambda_i / w_i) / \sum_k (\lambda_k / w_k)$, see [perspective-correct interpolation](/perspective-correct-interpolation/). An equivalent way intersects the view ray of the pixel with the triangle in view space.

**The derivatives (line L7).** In a forward or G-buffer pass, the hardware finds $\partial a / \partial x$ by differences inside a 2 by 2 quad of pixels. Here neighboring pixels can belong to other triangles, so the derivatives are computed from the triangle itself: evaluate the barycentrics at the centers of the pixels to the right and above, as if the triangle covered them, and take the differences of the interpolated attributes. The barycentrics are rational functions of the screen position, so closed-form derivatives are also possible. These derivatives select the [mipmap](/mipmap/) level.

**Grouping (line L8).** One way is to classify the pixels by material in a first compute pass, then run one shading pass per material over its list of pixels. Another is one shader with a branch per material, which is simpler but diverges.

## Classic examples

- **Burns and Hunt (2013).** The paper defines the buffer of triangle and instance ids, reconstructs the attributes and their derivatives per pixel in the shading pass, and compares memory traffic and run time with a G-buffer. Its results are measurements on its test scenes and hardware.
- **A worked size.** At 1920 by 1080 pixels with 4 samples per pixel, a 4-byte id costs $4 \cdot 4 \cdot 2\,073\,600 = 33\,177\,600$ bytes, about 31.6 MiB, plus the depth buffer. A 16-byte G-buffer at the same sample count costs 126.6 MiB plus depth. The shading pass of the visibility buffer reads one id per pixel and the vertex data of the visible triangles, which is shared by many pixels when triangles are large.
- **Edges of the image.** A pixel on the silhouette of a triangle gets its barycentrics from the same triangle as its center sample, even if its neighbors show other triangles. The derivatives are therefore those of the visible triangle, without the wrong values that a 2 by 2 quad gives across a triangle edge.

## Variations

- **Attribute storage.** A related method stores the texture coordinates, their derivatives and a material id per pixel, so that the shading pass does no vertex work but still avoids reading textures in the geometry pass. It sits between a G-buffer and a visibility buffer in size.
- **Visibility buffer with MSAA.** Store an id per sample, shade once per pixel when all samples share the id, and per sample at edges. Edge detection is a comparison of ids.
- **Software rasterization.** For very small triangles, a compute shader rasterizes and writes the depth and the id together with one 64-bit atomic minimum, the depth in the high bits. Virtualized geometry systems use this form.
- **Material classification.** A tile pass counts the materials per screen tile, so that each tile runs only the shaders that it needs.

## Pitfalls

- **Small triangles.** When most triangles cover one pixel or less, the vertex fetch and transform are repeated per pixel and the cache helps little. The G-buffer may then be faster.
- **Wrong derivatives.** Hardware derivatives across a 2 by 2 quad mix triangles at edges. Compute the derivatives from the barycentrics of the visible triangle.
- **Precision of the barycentrics.** For long thin triangles or triangles that cross the near plane, the screen-space barycentrics lose precision. Intersect the pixel ray with the triangle in view space, or clip in the geometry pass and store the clipped data.
- **Animated geometry.** The shading pass must see the same positions as the geometry pass. Keep the skinned positions of the frame in a buffer, or run the same transform twice.
- **Id range.** The split of the id between instance and triangle limits the number of each. Check the limits for the largest scene.
- **Transparency.** Like a G-buffer, the buffer holds one surface per pixel, see [order-independent transparency](/order-independent-transparency/).

## Exercises

1. Compute the bytes written by the geometry pass and read by the shading pass for a 4-byte visibility buffer and a 16-byte G-buffer at 3840 by 2160 pixels with 1 and 8 samples per pixel.
2. Derive the perspective-correct barycentrics $b_i = (\lambda_i / w_i) / \sum_k (\lambda_k / w_k)$ from the fact that $1/w$ and $a / w$ are linear in screen space.
3. Show that the attribute derivative obtained by evaluating the barycentrics at $q + (1, 0)$ is the forward difference of a rational function of $x$, and compare it with the exact derivative at the pixel center.
4. A scene has $n$ triangles of the same screen area $A$ pixels each. Estimate the vertex fetches per pixel of the shading pass as a function of $A$ with and without a vertex cache.

## References
