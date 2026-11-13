---
tag: 7P7W0Q
kind: problem
slug: texture-mapping
name: Texture mapping
aliases:
- texture mapping problem
area: graphics-and-signals/rasterization
level: core
summary: Assign surface detail from a texture image to the pixels covering a surface.
prereqs: [pixel, digital-image, triangle-rasterization]
see_also: [bilinear-filtering, mipmap, anisotropic-filtering, perspective-correct-interpolation, reconstruction-filter, image-warping, integral-image, antialiasing]
sources:
  - paper: "Edwin Catmull, A Subdivision Algorithm for Computer Display of Curved Surfaces, PhD thesis, University of Utah, report UTEC-CSc-74-133, December 1974"
    locator: the part on mapping pictures onto the subdivided bicubic patches
  - paper: "Paul S. Heckbert, Survey of texture mapping, IEEE Computer Graphics and Applications 6(11), 1986, pages 56 to 67"
    locator: the sections on the mapping, on the screen footprint of a pixel and on the filtering methods
  - paper: "Paul S. Heckbert, Fundamentals of Texture Mapping and Image Warping, MS thesis, University of California, Berkeley, report UCB/CSD 89/516, June 1989"
    locator: the chapters on the mappings (affine, bilinear and projective) and on resampling filters
  - paper: doi:10.1145/964967.801126
    title: Lance Williams, Pyramidal parametrics, Computer Graphics 17(3), SIGGRAPH 1983, pages 1 to 11
    locator: the statement of the minification problem and the pyramid
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, 2016
    locator: Chapter 10, Sections 10.1 (sampling and antialiasing of textures) and 10.4 (image texture)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 6, Texturing (the texturing pipeline, magnification and minification)
---

Texture mapping is the problem of giving each [pixel](/pixel/) of a rendered surface a value read from a texture image, through a map from points of the surface to texture coordinates $(u, v)$. Edwin Catmull introduced it in his 1974 thesis, to put photographs and patterns on curved patches. The problem has two parts: find the texture coordinates of each pixel, and filter the texture over the region that the pixel covers in the texture. When the pixel covers less than one texel the filter interpolates; when it covers many texels the filter must average them, or the texture aliases.

## In plain words

A texture is a picture that you glue onto a surface, like wallpaper on a wall or a label on a can. Each corner of a triangle says which point of the picture it gets. To draw the triangle, the renderer must find, for each screen dot, which point of the picture is there, and read a color from the picture. Two things make this hard. First, in a perspective view the picture is squeezed more where the surface is far away, so the positions must be computed with care. Second, one screen dot rarely matches one dot of the picture. Close up, a dot of the picture covers many screen dots, and the renderer must blend between picture dots to hide the blocks. Far away, one screen dot covers many dots of the picture, and the renderer must average them, or the result shimmers.

## Definition

**Texture.** A texture $T$ is a $W_t \times H_t$ grid of texels, with the texel $(s, t)$ centered at $(s + 1/2, t + 1/2)$ in texel units, as in OpenGL and Direct3D 10. Normalized coordinates $(u, v) \in [0, 1]^2$ map to texel coordinates $(u W_t, v H_t)$. A *wrap mode* defines $T$ outside the grid: repeat (wrap the index modulo the size), clamp to the edge texel, mirror, or a fixed border color. Values are reals in $[0, 1]$, decoded to linear light before filtering if the texture is stored in sRGB.

**Mapping.** Each vertex of a triangle carries $(u, v)$. Inside a triangle drawn with a perspective camera, the screen-to-texture map $\varphi(x, y) = (u, v)$ is projective: $u$ and $v$ are ratios of two affine functions of the screen position $(x, y)$. Computing it is [perspective-correct interpolation](/perspective-correct-interpolation/).

**Footprint.** The derivatives of $\varphi$ at a pixel center give two vectors in texel units,

$$d_x = \big(\partial (u W_t)/\partial x,\ \partial (v H_t)/\partial x\big), \qquad d_y = \big(\partial (u W_t)/\partial y,\ \partial (v H_t)/\partial y\big).$$

To first order, the pixel's filter region maps to the parallelogram spanned by $d_x$ and $d_y$, or to an ellipse when the screen filter is a Gaussian. This is the *footprint*.

**Task.** For each pixel, output an estimate of

$$p = \iint h\big(x - x_0,\ y - y_0\big)\ \tilde T\big(\varphi(x, y)\big)\, dx\, dy,$$

where $(x_0, y_0)$ is the pixel center, $h$ is the screen filter and $\tilde T$ is the continuous texture made from the texels by a [reconstruction filter](/reconstruction-filter/). The *magnification* case has a footprint smaller than a texel. The *minification* case has a footprint that covers many texels.

## Variants

- **What the texture changes.** Color is the first use. Textures also hold normals (normal maps and bump maps), heights (displacement), reflections of the environment, shadow depths and lookup tables.
- **Filtering quality.** Point lookup, interpolation for magnification, and prefiltered lookup for minification, isotropic or anisotropic.
- **Texture dimension.** 1D, 2D, 3D (volume) and cube textures. This page uses 2D.
- **Procedural textures.** $T$ is a function, not a grid, and the filter must be applied to the function or approximated by sampling.
- **Texture mapping as image warping.** Rendering a textured plane is an [image warp](/image-warping/) of the texture by a projective map, followed by resampling, as Heckbert framed it.

## Examples

**Perspective.** A segment on the screen runs from a vertex at depth $z = 1$ with $u = 0$ to a vertex at depth $z = 3$ with $u = 1$. At the screen midpoint, linear interpolation of $u$ in screen space gives $u = 1/2$. Interpolating $u/z$ and $1/z$ and dividing gives $(1/6)/(2/3) = 1/4$, which is the right value. The error of the affine version is what makes the texture of a large floor bend at triangle edges.

**Magnification.** A $16 \times 16$ texture on a square of $64 \times 64$ pixels has $|d_x| = |d_y| = 1/4$ texel. Nearest-texel lookup shows each texel as a $4 \times 4$ block. [Bilinear filtering](/bilinear-filtering/) blends the four nearest texels and removes the blocks.

**Minification.** A $256 \times 256$ texture on a square of $64 \times 64$ pixels has $|d_x| = |d_y| = 4$ texels. A point lookup reads 1 of the 16 texels under each pixel, so a fine pattern can turn into a false coarse pattern. A [mipmap](/mipmap/) lookup at level $\log_2 4 = 2$ reads a $64 \times 64$ image whose texels are the averages of $4 \times 4$ blocks.

**Anisotropy.** On a floor seen at a grazing angle, a pixel can have $|d_x| = 1$ and $|d_y| = 8$ texels. An isotropic mipmap lookup uses the larger length, level 3, and blurs the image along $x$ by a factor of 8. [Anisotropic filtering](/anisotropic-filtering/) takes 8 probes along $d_y$ at level 0.

## Known algorithms

- Coordinates: [perspective-correct interpolation](/perspective-correct-interpolation/) of $(u, v)$ inside each triangle, after [triangle rasterization](/triangle-rasterization/).
- Magnification: nearest-texel lookup, which is [nearest-neighbor interpolation](/nearest-neighbor-interpolation/), and [bilinear filtering](/bilinear-filtering/). Higher order filters such as [bicubic interpolation](/bicubic-interpolation/) are used in image viewers more than in real-time texturing.
- Minification: the [mipmap](/mipmap/) with trilinear lookup; [anisotropic filtering](/anisotropic-filtering/) with several probes or with the elliptical weighted average; summed-area tables, which are an [integral image](/integral-image/) of the texture and give the exact box average over any axis-aligned rectangle with 4 lookups.
- Brute force: [supersampling](/supersampling-antialiasing/) of the screen, with a point or bilinear lookup at each sample.

## Bounds

The costs are per pixel and count texel reads.

| method | texel reads | what it computes |
|---|---|---|
| nearest texel | 1 | $T$ at the nearest texel center |
| bilinear | 4 | the tent-filtered texture at one point |
| trilinear mipmap | 8 | a blend of two bilinear lookups in two box-filtered levels |
| $N$ anisotropic probes | $8N$ | an average of $N$ trilinear lookups along the footprint |
| summed-area table | 4 per channel | the exact box average over an axis-aligned rectangle |
| direct average | $\Theta(A)$ | the exact average over a footprint of $A$ texels |

A mipmap of a square texture uses less than $4/3$ times the memory of the texture, and of any power-of-two texture less than twice, and a summed-area table needs wider integers or floats than the texels, because its entries grow with the image size. No method with a fixed number of reads per pixel computes the exact filtered value of every footprint; the prefiltered methods trade this for a fixed cost.

## Reductions

- Magnification reduces to 2D interpolation on a grid: [bilinear interpolation](/bilinear-interpolation/) and its relatives in numerical analysis.
- Minification reduces to [image resampling](/image-resampling/) with a space-variant filter, because the footprint changes from pixel to pixel.
- Texture mapping of a plane is an [image warp](/image-warping/) by a projective map.

## Applications

- Real-time rendering, where nearly every surface is textured, and the GPU has fixed units for the lookups.
- Film rendering, with large textures streamed from disk and filtered by ray footprints such as [ray differentials](/ray-differentials/).
- Terrain and map rendering from aerial images.
- Text, where glyphs are stored in a texture atlas.

## References
