---
tag: 85PFVB
kind: concept
slug: bilinear-filtering
name: Bilinear filtering
area: graphics-and-signals/rasterization
level: intro
summary: Texture filtering that interpolates the four nearest texels by their fractional distances.
prereqs: [texture-mapping, bilinear-interpolation]
see_also: [mipmap, anisotropic-filtering, nearest-neighbor-interpolation, bicubic-interpolation, reconstruction-filter, image-resampling, tensor-product-interpolation, temporal-antialiasing]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 6, Texturing, the section on magnification (nearest and bilinear filtering, texel centers)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, 2016
    locator: Chapter 10, Section 10.4 (image texture, the bilinear lookup and the wrap modes)
  - url: https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf
    title: Mark Segal and Kurt Akeley, The OpenGL Graphics System, A Specification, version 4.6 (Core Profile), Khronos Group
    locator: Chapter 8, the sections on texture minification and magnification (the LINEAR filter, the texel coordinates i0 and j0, and the wrap modes)
  - paper: "Paul S. Heckbert, Fundamentals of Texture Mapping and Image Warping, MS thesis, University of California, Berkeley, report UCB/CSD 89/516, June 1989"
    locator: the chapter on resampling filters (the triangle filter as reconstruction)
---

Bilinear filtering is the texture lookup that returns a weighted average of the four texels nearest to a sample point, with weights that come from the point's fractional position between the texel centers. It is the magnification filter of GPUs, and the building block of the [mipmap](/mipmap/) and [anisotropic](/anisotropic-filtering/) lookups. In signal terms it reconstructs the texture with the separable tent filter. The mathematics of interpolation on a grid is on the [bilinear interpolation](/bilinear-interpolation/) page; this page covers the lookup in a texture: the texel center rule, the wrap modes at the border, the cost, and what the filter does and does not remove.

## In plain words

A texture is a grid of colored squares, the texels. When a surface is close to the camera, one texel covers many pixels. If each pixel takes the color of the nearest texel, the texture looks like a set of blocks. Bilinear filtering instead finds the four texels whose centers surround the point, and mixes their colors. A point close to one texel center gets mostly that texel's color. A point halfway between two centers gets half of each. The mix is done first along one direction, then along the other. The blocks turn into smooth ramps. The method reads four texels for each lookup, so it is cheap, and graphics hardware does it in fixed circuits. It does not help when the texture is far away and one pixel covers many texels; that case needs a mipmap.

## The idea

**Coordinates.** A texture of $W \times H$ texels has the texel $(s, t)$ centered at $(s + 1/2, t + 1/2)$ in texel units, as in OpenGL and Direct3D 10. A lookup at normalized coordinates $(u, v)$ computes

$$x = uW - \tfrac12, \quad y = vH - \tfrac12, \quad i_0 = \lfloor x \rfloor, \quad j_0 = \lfloor y \rfloor, \quad \alpha = x - i_0, \quad \beta = y - j_0,$$

and returns

$$T(u, v) = (1-\alpha)(1-\beta)\, T_{i_0, j_0} + \alpha(1-\beta)\, T_{i_0+1, j_0} + (1-\alpha)\beta\, T_{i_0, j_0+1} + \alpha\beta\, T_{i_0+1, j_0+1},$$

where the four indices are first mapped into the grid by the wrap mode. The values must be linear: an sRGB texture is decoded before the four texels are mixed.

**The tent filter.** With $\Lambda(t) = \max(0, 1 - |t|)$, the same value is

$$T(u, v) = \sum_{i} \sum_{j} \Lambda\big(uW - i - \tfrac12\big)\, \Lambda\big(vH - j - \tfrac12\big)\, T_{i, j},$$

summed over all integers, with $T_{i,j}$ extended outside the grid by the wrap mode. The reason: $\Lambda(x - i)$ is zero unless $|x - i| < 1$, which leaves only $i = i_0$ and $i = i_0 + 1$, with weights $1 - \alpha$ and $\alpha$; the $y$ factor is the same. So bilinear filtering is reconstruction with the separable tent filter, one of the [reconstruction filters](/reconstruction-filter/).

**Properties.** The weights are nonnegative and sum to 1, so the result lies between the smallest and the largest of the four texels. At a texel center the result is that texel. The result is continuous in $(u, v)$, but its derivative jumps on the lines through the texel centers, which shows as a faint diamond pattern under strong magnification. It reproduces every affine function of $x$ and $y$ exactly. Along a diagonal it is quadratic, not linear: the surface over one cell is a hyperbolic paraboloid.

**Wrap modes.** Near the border, $i_0$ can be $-1$ or $i_0 + 1$ can be $W$. *Clamp to edge* replaces them by $0$ and $W - 1$, so the edge texel extends outward. *Repeat* takes them modulo $W$, so the left edge blends with the right edge, which is right for a tiling texture. *Mirror* reflects the grid at each edge. A fixed border color is a fourth choice in many APIs.

**Cost.** Four texel reads and three linear interpolations per channel. GPUs often fetch the four texels of a $2 \times 2$ quad together and compute the weights in fixed point with a few fractional bits.

**What it does not do.** Bilinear filtering is an interpolation of point samples. When one pixel covers many texels (minification), it reads only 4 of them, so the texture still aliases. The [mipmap](/mipmap/) fixes this by doing the lookup in a prefiltered smaller image, and trilinear filtering blends two bilinear lookups in two mipmap levels.

## Examples

**An interior lookup.** Take a $4 \times 4$ texture with $T_{s,t} = 10s + 40t$ (one channel). At $u = 0.3$, $v = 0.6$: $x = 1.2 - 0.5 = 0.7$ and $y = 2.4 - 0.5 = 1.9$, so $i_0 = 0$, $\alpha = 0.7$, $j_0 = 1$, $\beta = 0.9$. The four texels are $T_{0,1} = 40$, $T_{1,1} = 50$, $T_{0,2} = 80$, $T_{1,2} = 90$, with weights $0.03$, $0.07$, $0.27$ and $0.63$. The result is $1.2 + 3.5 + 21.6 + 56.7 = 83$. The texture is an affine function, and $10 \cdot 0.7 + 40 \cdot 1.9 = 83$, as the reproduction property says. Nearest-texel lookup at the same point returns $T_{1,2} = 90$.

**The border.** At $u = 0.05$, $v = 0.625$: $x = -0.3$, so $i_0 = -1$ and $\alpha = 0.7$, and $y = 2$, so $\beta = 0$. With clamp, both columns map to column 0 and the result is $T_{0,2} = 80$. With repeat, column $-1$ is column 3, and the result is $0.3 \cdot 110 + 0.7 \cdot 80 = 89$. With mirror, column $-1$ is column 0 and the result is 80.

**The half-texel mistake.** Code that uses $x = uW$ without the $-1/2$ treats the texel corners as the sample points. The image shifts by half a texel, and a texture drawn at one texel per pixel gets blurred, because every pixel center then falls halfway between two texel centers.

**A non-example.** Averaging all texels under the footprint of a pixel is a box prefilter, not bilinear filtering. Bilinear filtering uses a fixed $2 \times 2$ support, whatever the footprint.

## Where it is used

- The magnification filter of GPU texture units (the LINEAR filter of OpenGL), and each probe of trilinear and [anisotropic filtering](/anisotropic-filtering/).
- Image scaling in viewers and video players, as one choice of [image resampling](/image-resampling/).
- Fetching the reprojected history in [temporal antialiasing](/temporal-antialiasing/), and other reads of a buffer at non-integer positions.
- Hardware shadow map lookups that filter four depth comparisons.

## References
