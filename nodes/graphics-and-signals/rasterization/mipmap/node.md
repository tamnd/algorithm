---
tag: 6V0FBJ
kind: data-structure
slug: mipmap
name: Mipmap
aliases:
- mipmapping
area: graphics-and-signals/rasterization
level: advanced
summary: Precomputed chain of progressively halved textures for filtered texture lookup.
model: real-ram
complexity:
  vars: {W: base texture width in texels, H: base texture height in texels}
  time: {worst: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, static: true}
history:
  year: 1983
  people: [Lance Williams]
  note: Williams named the structure MIP, for multum in parvo, and introduced the lookup that interpolates within two levels and between them.
prereqs: [texture-mapping, bilinear-filtering]
see_also: [anisotropic-filtering, antialiasing, reconstruction-filter, image-pyramid, gaussian-pyramid, laplacian-pyramid, image-resampling, supersampling-antialiasing]
sources:
  - paper: doi:10.1145/964967.801126
    title: Lance Williams, Pyramidal parametrics, SIGGRAPH 1983, Computer Graphics 17(3), pages 1 to 11
    locator: the whole paper (the pyramid of prefiltered images, the memory layout and the interpolation between levels)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, 2016
    locator: Chapter 10, Section 10.4.3 (MIPMaps, the pyramid construction and the trilinear lookup)
  - url: https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf
    title: Mark Segal and Kurt Akeley, The OpenGL Graphics System, A Specification, version 4.6 (Core Profile), Khronos Group
    locator: Chapter 8, the sections on mipmapping and texture minification (the level of detail λ, the scale factor ρ and the LINEAR_MIPMAP_LINEAR filter)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 6, Texturing, the section on minification (mipmapping and trilinear interpolation)
  - paper: "Paul S. Heckbert, Fundamentals of Texture Mapping and Image Warping, MS thesis, University of California, Berkeley, report UCB/CSD 89/516, June 1989"
    locator: the chapter on texture filtering (prefiltering by pyramids)
---

A mipmap stores a texture together with a chain of smaller copies of it, each copy half the width and half the height of the one before, down to a single texel. Each texel of a smaller copy is the box average of a $2 \times 2$ block of the copy above, so the texel of level $k$ is the average of a $2^k \times 2^k$ block of the original. A [texture](/texture-mapping/) lookup for a pixel that covers about $\rho$ texels then reads a few texels from the level near $\log_2 \rho$ in place of averaging $\rho^2$ texels, in constant time. For a square texture the whole chain takes $(4WH - 1)/3$ texels, less than $4/3$ of the original.

## In plain words

When a textured wall is far from the camera, one pixel of the screen covers many texels of its texture. If the pixel reads only the texel at its center, the picture flickers and shows false patterns, because nearby pixels jump to unrelated texels. The right color is the average of all texels under the pixel, but computing that average for every pixel is too slow. A mipmap computes the averages once, before rendering. It makes a copy of the texture at half size, where each texel is the average of four texels, then a copy of that copy at half size again, and so on, down to one texel. At render time, a pixel that covers a large area reads from a small copy, where one texel already holds the average of that area. All the copies together take only one third more memory than the texture.

## The abstract type

The mipmap is a static structure for one texture $T$ of $W \times H$ texels, with values that are linear in light. It supports these operations.

- **BUILD(T)** makes the levels $M_0 = T, M_1, \dots, M_L$.
- **LOOKUP(u, v, λ)** returns an estimate of the texture prefiltered to the scale $2^\lambda$ texels at the normalized point $(u, v)$. The *level of detail* $\lambda = \log_2 \rho$ comes from the size $\rho$ of the pixel's footprint in base texels. The trilinear lookup of this page is the standard choice.
- **UPDATE(s, t, c)** changes one base texel. It changes one texel in each level, the one whose block contains $(s, t)$.

What the type promises is precise for the levels: texel $(s, t)$ of level $k$ is the mean of the base texels in its $2^k \times 2^k$ block. The lookup is an approximation of the ideal filter, and the page says where it differs.

## Representation

Let $W = 2^a$ and $H = 2^b$, and $L = \max(a, b)$. Level $k$ has $W_k = \max(1, W/2^k)$ columns and $H_k = \max(1, H/2^k)$ rows, and the levels are separate arrays. Texel $(s, t)$ of every level has its center at $(s + 1/2, t + 1/2)$ in the texel units of that level, as in OpenGL and Direct3D 10. With this convention, the center of a texel of level $k$ lies at the center of its block in base texel units, so the same normalized coordinates $(u, v) \in [0, 1]^2$ address the same point on every level. Williams packed the levels of a color texture into one array of $2W \times 2H$: the red, green and blue channels of level 0 fill three quadrants, and the fourth quadrant holds the same layout for the next level, recursively. GPUs store the levels one after the other in memory, often in a tiled order.

## Operations

```pseudo id=main
BUILD-MIPMAP(T)                     ▷ W × H texels, W and H powers of two
L1  M_0 ← T, k ← 0
L2  while M_k has more than one texel do
L3      w ← max(1, W_k / 2), h ← max(1, H_k / 2)
L4      for each texel (s, t) of a new w × h level M_{k+1} do
L5          M_{k+1}[s, t] ← mean of M_k[s', t'] over s' ∈ {2s, 2s+1}, t' ∈ {2t, 2t+1} inside M_k
L6      k ← k + 1
L7  return M_0, …, M_L
```

Line L3 halves each side that is larger than 1. Line L5 averages a $2 \times 2$ block, or a $2 \times 1$ block once one side has reached 1. The averages are taken on linear values. Line L6 moves to the new level, and the loop stops at the $1 \times 1$ level, which holds the mean of the whole texture.

```pseudo id=lookup
TRILINEAR(M, u, v, λ)               ▷ λ = log2 ρ, ρ the footprint in base texels
L8  if λ ≤ 0 then
L9      return BILINEAR(M_0, u, v)          ▷ magnification: no prefiltering needed
L10 if λ ≥ L then
L11     return BILINEAR(M_L, u, v)
L12 d ← ⌊λ⌋, f ← λ − d
L13 c_0 ← BILINEAR(M_d, u, v), c_1 ← BILINEAR(M_{d+1}, u, v)
L14 return (1 − f) c_0 + f c_1
```

BILINEAR is the [bilinear filter](/bilinear-filtering/) of one level, with the half-texel centers and a wrap mode at the border. Lines L12 to L14 blend the two levels whose texel sizes bracket the footprint, so the result changes continuously as a surface moves away from the camera; this is *trilinear* filtering. A renderer computes $\rho$ from the screen derivatives of $(u, v)$: with $\rho_x = \sqrt{(W\,\partial u/\partial x)^2 + (H\,\partial v/\partial x)^2}$ and the same $\rho_y$ for $y$, OpenGL takes $\rho = \max(\rho_x, \rho_y)$ and $\lambda = \log_2 \rho$ plus an optional bias.

UPDATE of a base texel recomputes, for $k = 1$ to $L$, the one texel of level $k$ whose block contains it, by line L5.

## Example

Take this $4 \times 4$ texture, one channel, row $t$ by column $s$:

| | $s = 0$ | $s = 1$ | $s = 2$ | $s = 3$ |
|---|---|---|---|---|
| $t = 0$ | 0 | 4 | 8 | 12 |
| $t = 1$ | 4 | 0 | 12 | 8 |
| $t = 2$ | 16 | 20 | 0 | 4 |
| $t = 3$ | 20 | 16 | 4 | 0 |

Level 1 is $2 \times 2$: the four block means are $2$ and $10$ in its row 0 and $18$ and $2$ in its row 1. Level 2 is the single texel $(2 + 10 + 18 + 2)/4 = 8$, the mean of all 16 texels. The three levels hold $16 + 4 + 1 = 21 = (4 \cdot 16 - 1)/3$ texels.

Look up the point $(u, v) = (3/8, 5/8)$. On level 0 it is $(1, 2)$ in texel units after the half-texel shift, a texel center, so BILINEAR returns $T_{1,2} = 20$. On level 1 it is $(1/4, 3/4)$, which gives the weights $3/16$, $1/16$, $9/16$ and $3/16$ on the texels $2$, $10$, $18$ and $2$, so the value is $23/2$. On level 2 it is $8$. If the pixel covers about $\rho = 2^{3/2} \approx 2.83$ texels, then $\lambda = 3/2$, $d = 1$, $f = 1/2$, and the trilinear result is $(23/2 + 8)/2 = 39/4$. For $\rho = 2^{1/2}$ the result is $(20 + 23/2)/2 = 63/4$. The single texel 20 is a point value; the prefiltered values move toward the local mean as the footprint grows.

A checkerboard of 0 and 1 texels shows the point. Seen at $\rho = 4$, a point lookup on level 0 returns 0 or 1 depending on where the sample falls, and the image shows false stripes. Level 2 holds $1/2$ in every texel, the correct average, and the stripes are gone.

## Correctness

The proof is by induction on the level. A texel of level $k+1$ is the mean of 1, 2 or 4 texels of level $k$. By induction these are the means of disjoint base blocks of the same size, and the union of these blocks is the block of the new texel, so the mean of the means is the mean over the union. The half-texel convention places the center of each texel at the center of its block, which justifies passing the same $(u, v)$ to every level. For the storage, the levels of a square texture have $WH/4^k$ texels, and the geometric series gives $(4WH - 1)/3$. For a $2^a \times 2^b$ texture with $a \ge b$ and $r = 2^{a-b}$, the total is $(4WH + 2r - 3)/3$, which is always less than $2WH$. The trilinear result is a convex combination of base texels, and it is continuous in $\lambda$. The full proofs are below.

## Complexity

- **BUILD.** Level $k+1$ costs $\Theta(W_{k+1} H_{k+1})$, so the whole build takes time proportional to the storage, which is $\Theta(W H)$.
- **Space.** Exactly $(4WH - 1)/3$ texels for a square texture, so the levels above level 0 add less than $WH/3$. A long thin texture needs more, but always less than $2WH$ in total.
- **LOOKUP.** Trilinear filtering reads 8 texels, two bilinear lookups of 4, and the cost is $\Theta(1)$ for any $\lambda$. The exact box average over a footprint of $\rho \times \rho$ texels would read $\Theta(\rho^2)$ texels.
- **UPDATE.** One texel per level, $\Theta(L) = \Theta(\log \max(W, H))$.

## Variants

- **Filter modes.** OpenGL names the combinations: NEAREST_MIPMAP_NEAREST reads one texel of the nearest level, LINEAR_MIPMAP_NEAREST does one bilinear lookup in the nearest level, and LINEAR_MIPMAP_LINEAR is the trilinear lookup of this page.
- **Better downsampling filters.** The box filter of line L5 lets some aliasing through into the coarse levels. Tools often build the levels with a wider filter, such as a Kaiser, Lanczos or Gaussian kernel applied to the base texture, at a higher build cost. The lookup does not change. See [reconstruction filters](/reconstruction-filter/).
- **Non-power-of-two sizes.** OpenGL rounds each side down, $\max(1, \lfloor n/2 \rfloor)$. A side of odd length then has no exact $2 \times 2$ blocks, and a correct build uses a 3-tap filter with weights that follow the texel overlap.
- **Ripmaps.** Prefilter separately in $u$ and $v$ to all $2^i \times 2^j$ reductions. This handles footprints stretched along an axis, and costs $4WH$ texels for a square texture.
- **Anisotropic filtering.** [Anisotropic filtering](/anisotropic-filtering/) takes several trilinear probes along the long axis of the footprint, at the level of the short axis.
- **Clipmaps and virtual textures.** Very large textures keep only a window of each fine level in memory, or page in tiles of the levels on demand.
- **Image pyramids in image processing.** The [image pyramid](/image-pyramid/), the [Gaussian pyramid](/gaussian-pyramid/) and the [Laplacian pyramid](/laplacian-pyramid/) use the same halving chain for analysis, with a smoothing filter wider than the box, and are not tied to texture lookup.

## When to use it

Use a mipmap for every texture that can appear smaller than its own resolution on screen, which is almost every texture in a 3D scene. It costs a third more memory and a build pass, and it removes most texture aliasing under minification at a constant lookup cost. Use it with anisotropic filtering for surfaces seen at a grazing angle. A texture drawn only at exactly one texel per pixel, such as a user interface element, does not need it.

## Pitfalls

- **Building in sRGB.** Averaging sRGB codes darkens the coarse levels. Decode to linear values, average, and encode again.
- **Overblur at grazing angles.** $\rho = \max(\rho_x, \rho_y)$ picks the level for the long side of the footprint, so the short side is blurred too. This is what anisotropic filtering fixes.
- **Alpha-tested textures.** Averaging alpha shrinks the area that passes a fixed alpha threshold at coarse levels, so foliage and fences thin out at a distance. Scaling alpha per level to keep the coverage fixes it.
- **Normal maps.** The average of unit normals is shorter than one, and renormalizing it loses the information that the surface is rough at that scale.
- **Texture atlases.** Coarse levels average texels across the borders of the charts in an atlas, and colors bleed into neighbor charts. Leave padding between charts, or stop the chain early.
- **Derivatives in 2 × 2 quads.** GPUs estimate $\partial u/\partial x$ from neighbor pixels in a quad. At a discontinuity of $(u, v)$, such as a wrap seam, the estimate is huge, and the lookup jumps to the coarsest level for one line of pixels.

## Implementations

## History

Williams (1983) introduced the pyramid of prefiltered texture images and the interpolation within and between two levels, and called it MIP, from multum in parvo, many things in a small place. Heckbert's 1989 thesis analyzed the pyramid as an approximation of the ideal space-variant filter, together with elliptical filters. The structure became a standard part of the OpenGL and Direct3D texture units.

## References
