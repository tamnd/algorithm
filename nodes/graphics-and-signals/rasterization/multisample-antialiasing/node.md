---
tag: X9CB9D
kind: algorithm
slug: multisample-antialiasing
name: Multisample antialiasing
aliases:
- MSAA
area: graphics-and-signals/rasterization
level: advanced
summary: Shades once per pixel but tests coverage and depth at several samples per pixel.
solves: [antialiasing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, s: samples per pixel, n: number of triangles}
  time: {worst: Θ(n W H s), best: Θ(W H s)}
  space: {extra: Θ(W H s)}
properties: {deterministic: true, in_place: false}
history:
  year: 1993
  people: [Kurt Akeley]
  note: The RealityEngine of Silicon Graphics stored several subsamples per pixel with their own depth and resolved them, while it computed one color per pixel and polygon.
prereqs: [supersampling-antialiasing, z-buffer, triangle-rasterization]
see_also: [antialiasing, top-left-fill-rule, edge-function, a-buffer, morphological-antialiasing, temporal-antialiasing, reconstruction-filter, mipmap]
sources:
  - paper: doi:10.1145/166117.166131
    title: Kurt Akeley, RealityEngine graphics, SIGGRAPH 1993
    locator: the sections on the fragment generators and the image engines (subsample coverage masks, the per-subsample depth test and the resolve)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, Section 5.4, Aliasing and Antialiasing (the part on multisampling, sample patterns, centroid sampling and the resolve)
  - url: https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf
    title: Mark Segal and Kurt Akeley, The OpenGL Graphics System, A Specification, version 4.6 (Core Profile), Khronos Group
    locator: the rasterization chapter, the section on multisampling (the coverage of each sample, one set of fragment values per pixel and the per-sample tests)
  - url: https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ne-d3d11-d3d11_standard_multisample_quality_levels
    title: Microsoft, D3D11_STANDARD_MULTISAMPLE_QUALITY_LEVELS, Direct3D 11 documentation
    locator: the remarks (the standard sample patterns for 2, 4, 8 and 16 samples, required for Direct3D 10.1 and 11 hardware)
---

Multisample antialiasing (MSAA) keeps $s$ samples per [pixel](/pixel/), each with its own color and depth, but runs the shader only once for each pixel and triangle that covers at least one of the samples. The single color is written to the covered samples that pass a per-sample depth test, and the samples of each pixel are averaged at the end. For geometry edges, the result is the same as [supersampling](/supersampling-antialiasing/) with the same sample points, while the shading cost stays close to that of one sample per pixel. It does not antialias what happens inside a triangle, such as texture and shading detail.

## In plain words

Most of the jagged look of a rendered image comes from the edges of triangles, not from their insides. Supersampling fixes the edges by computing the full color at many points of each pixel, which is slow because computing a color is the expensive part. Multisampling notices that the color of one triangle hardly changes inside a small pixel. So it still checks many points of each pixel to find which triangle covers which point and which one is in front, but it computes the color of each triangle only once per pixel. A pixel half covered by a red triangle and half by a blue one gets two color computations and ends up purple, the same as with supersampling. A pixel in the middle of one triangle gets one color computation instead of many.

## The problem

The input is a list of $n$ triangles in screen space, with vertices $(x, y, z)$ in pixel units ($y$ down, smaller $z$ nearer), a shader, a background color, an image size $W \times H$, and a sample pattern of $s$ offsets in the unit square. Pixel $(i, j)$ is the point sample at its center $(i + 1/2, j + 1/2)$, and its box filter covers $[i, i+1] \times [j, j+1]$; sample $m$ of the pixel is at $(i, j)$ plus offset $m$. Depth is interpolated linearly in screen space. Colors are linear values. A sample on an edge belongs to the triangle that the [top-left fill rule](/top-left-fill-rule/) gives it, and triangles of zero area draw nothing. The output is the resolved image, the [antialiasing](/antialiasing/) estimate with a box filter over the samples of each pixel.

## The algorithm

```pseudo id=main
MSAA(triangles, W, H, pattern)            ▷ s samples per pixel
L1  set every sample color to the background and every sample depth to ∞
L2  for each triangle t in order do
L3      for each pixel (i, j) in the bounding box of t do
L4          mask ← the samples m of (i, j) that t owns, with their depths z_m
L5          if mask is empty then continue
L6          c ← SHADE(t, i + 1/2, j + 1/2)              ▷ once per pixel and triangle
L7          for each m in mask do
L8              if z_m < depth[i, j, m] then
L9                  depth[i, j, m] ← z_m, color[i, j, m] ← c
L10 P[i, j] ← the mean of color[i, j, 1..s] for each pixel
L11 return P
```

Line L4 is the coverage test: the [edge functions](/edge-function/) of $t$ are evaluated at each of the $s$ sample points, and the result is a bit mask, the *coverage mask*. The depth is interpolated at each covered sample, not at the pixel center, so two triangles that cross inside a pixel split its samples correctly. Line L6 is the single shader call; it is made at the pixel center even if the center is outside the triangle. Lines L8 and L9 are a [z-buffer](/z-buffer/) at the sample level. Line L10 is the *resolve*.

## Example

The white triangle with corners $(3/5, 2/5)$, $(7/2, 1)$ and $(1, 3)$ of the [supersampling](/supersampling-antialiasing/) page lies on a black image of $4 \times 3$ pixels. Use 4 samples per pixel in a rotated grid, at the offsets $(3/8, 1/8)$, $(7/8, 3/8)$, $(1/8, 5/8)$ and $(5/8, 7/8)$, so that the four samples have four different $x$ and four different $y$ positions.

| row | exact coverage | MSAA, 4 samples |
|---|---|---|
| 0 | 0.196, 0.414, 0.207, 0.026 | 0, 1/2, 1/4, 0 |
| 1 | 0.231, 1, 0.775, 0.1 | 1/4, 1, 3/4, 0 |
| 2 | 0.077, 0.6, 0.025, 0 | 0, 1/2, 0, 0 |

The triangle owns 13 samples in 6 pixels. Supersampling with the same samples calls the shader 13 times and gives the same image. MSAA calls it 6 times, once per touched pixel.

**Depth per sample.** In the single pixel $[0, 1]^2$, a red triangle with corners $(0, 0, 0)$, $(2, 0, 4)$, $(0, 2, 0)$ has depth $z = 2x$, and a blue triangle with the same corners at depth 1 is drawn after it. Both cover all four samples, and each is shaded once. Red is nearer where $2x < 1$, so the samples at $x = 3/8$ and $x = 1/8$ keep red and the samples at $x = 7/8$ and $x = 5/8$ take blue. The resolved pixel is $(1/2, 0, 1/2)$ in (red, green, blue) order. A method that tested depth once per pixel would make the whole pixel red or blue.

## Correctness

The proof follows the z-buffer invariant at each sample. After the first $t$ triangles, the stored depth of a sample is the least depth among those triangles that own it, and the stored color is the shade, at the pixel center, of the first triangle that reaches this least depth. Each (triangle, pixel) pair with a nonempty mask gets exactly one shader call. If the shade of each triangle is a constant color, the stored sample colors are exactly those of supersampling with the same samples and a per-sample depth test, so the edge error bounds of supersampling hold. For a mesh, the top-left rule assigns every sample on a shared edge or vertex to exactly one triangle: the rule is the same as moving the sample by an infinitely small step $(\varepsilon, \varepsilon^2)$, and the moved point lies inside exactly one triangle. The full proofs are below.

## Complexity

- **Shading.** One call per pixel and triangle that touches it, so at most $n W H$ calls and, for a mesh of large triangles, close to $W H$ plus the pixels on the edges. Supersampling calls the shader once per covered sample, up to $s$ times as often.
- **Coverage and depth.** Line L4 evaluates three edge functions and one depth plane at $s$ samples, so this version takes $\Theta(s)$ per pixel of each bounding box, $\Theta(n W H s)$ in the worst case, and $\Theta(W H s)$ to clear and resolve the buffers in the best case. Hardware does the $s$ tests in parallel.
- **Memory.** $\Theta(W H s)$ extra: $s$ colors and $s$ depths per pixel, the same as supersampling. GPUs compress the color samples of pixels that one triangle covers fully, which saves bandwidth but not the allocation.

## Properties

- **Exact visibility at the samples.** Coverage and depth use the true sample positions, so edges and intersections of triangles get the same coverage as supersampling.
- **No antialiasing inside a triangle.** Texture, specular highlights and other shading detail are sampled once per pixel, so they alias as without antialiasing. Mipmapped textures limit the texture part.
- **Linear in light.** The resolve is a mean, which is correct only on linear values.
- **Shading outside the triangle.** The shader input at the pixel center can lie outside the triangle when the triangle covers only some samples, so interpolated attributes are extrapolated.

## Variants and improvements

- **Centroid sampling.** Evaluate the shader at a point inside the covered samples, such as their centroid, when the pixel center is not covered. This avoids extrapolated attributes at the cost of irregular derivatives.
- **Sample shading.** Run the shader once per covered sample when needed, which turns MSAA back into supersampling for chosen materials.
- **Alpha to coverage.** Turn the alpha of a cutout texture into a coverage mask, so that foliage and fences get antialiased edges without sorting.
- **Coverage sampling.** Store more coverage bits than color samples (the CSAA and EQAA hardware modes), so that a pixel with few triangles gets a finer coverage estimate.
- **Custom resolves.** A resolve with a wider [reconstruction filter](/reconstruction-filter/) than the box, or a resolve after tone mapping, which keeps bright edges from aliasing.
- **Coverage masks without depth.** The [A-buffer](/a-buffer/) keeps a coverage mask with each fragment and resolves a list of fragments per pixel.
- **Post-process and temporal methods.** [Morphological antialiasing](/morphological-antialiasing/) works on the final image only, and [temporal antialiasing](/temporal-antialiasing/) spreads samples over frames. Both replaced MSAA in many engines with deferred shading.

## When to use it

Use MSAA in a forward renderer when geometric edges are the main source of aliasing and the shader is expensive, for example in virtual reality, in CAD views and in games with forward shading. Four samples per pixel give a large improvement at a moderate memory cost. It fits badly with deferred shading, where the G-buffer of every sample must be stored and lit, and it does nothing for shading aliasing, for which supersampling, mipmapping or temporal accumulation is needed.

## Pitfalls

- **Resolving in sRGB, or before tone mapping.** The average must be taken on linear values. Resolving HDR values before tone mapping, however, lets a very bright sample dominate the pixel, and many engines tone map each sample first.
- **Centroid derivatives.** Centroid sampling moves the shading point, so the screen derivatives that pick a mipmap level become irregular along edges.
- **Depth at the center.** An implementation that tests depth once at the pixel center loses the intersections of triangles inside a pixel.
- **Inclusive edge rules.** Without the top-left rule, a sample on a shared edge is written by both triangles, and with blending enabled it is blended twice.
- **Memory with many render targets.** Every render target is $s$ times larger, which limits MSAA with deferred shading.

## Implementations

## History

Coverage masks inside a pixel came with the A-buffer (Carpenter, 1984), which resolved visibility per fragment. Akeley's RealityEngine (1993) stored 4, 8 or 16 subsamples per pixel, each with its own depth, computed one color per pixel and polygon, and resolved the subsamples for display; this is the scheme of MSAA. OpenGL added multisampling as an extension and later to the core specification, and Direct3D 10.1 fixed standard sample patterns.

## References
