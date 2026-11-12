---
tag: H8V6CC
kind: definition
slug: pixel
name: Pixel
aliases:
- picture element
area: graphics-and-signals/rasterization
level: intro
summary: One sample of an image on a regular grid, with integer indices and a value, taken at a point, the pixel center; it is not a little square.
prereqs: []
see_also: [digital-image, frame-buffer, sampling-theorem, aliasing, reconstruction-filter, viewport-transform, antialiasing]
sources:
  - url: https://alvyray.com/Memos/CG/Microsoft/6_pixel.pdf
    title: Alvy Ray Smith, A Pixel Is Not A Little Square, A Pixel Is Not A Little Square, A Pixel Is Not A Little Square! (And a Voxel is Not a Little Cube), Microsoft Technical Memo 6, July 17, 1995
    locator: the whole memo (a pixel is a point sample, and a display or a resampler reconstructs a continuous image from the samples with a filter)
  - book: isbn:9780122861666
    title: Andrew S. Glassner (editor), Graphics Gems, Academic Press, 1990
    locator: Paul S. Heckbert, What Are the Coordinates of a Pixel?, pages 246 to 248 (continuous coordinate = discrete index + 1/2)
  - paper: doi:10.1117/12.644941
    title: Richard F. Lyon, A brief history of 'pixel', Proceedings of SPIE 6069, Digital Photography II, 606901 (2006)
    locator: the first uses of the words pixel (1965) and pel (1967)
  - url: https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm
    title: Microsoft, Direct3D 11.3 Functional Specification
    locator: Section 3.3.1, Pixel Coordinate System (the origin at the top left corner and the pixel centers at offsets of 0.5)
---

A pixel, short for picture element, is one sample of an image on a regular grid: it has integer indices $(i, j)$, which give its column and row, and a value, such as a color or an intensity. The value belongs to one point of the plane, the pixel center, which in the convention of OpenGL, Direct3D 10 and later, and most texts is $(i + \tfrac12, j + \tfrac12)$. As Alvy Ray Smith put it in 1995, a pixel is a point sample and not a little square: the picture between the centers comes from a reconstruction filter, and the square is one choice of that filter.

## Definition

Let $f$ be a continuous image, a function from the plane to a set $V$ of values, for example colors with three channels. Let $h$ be a prefilter: a weight function on the plane with integral 1, or the Dirac delta. A $W$ by $H$ image sampled from $f$ is the array of values

$$p_{ij} = (h * f)\!\left(i + \tfrac12,\ j + \tfrac12\right), \qquad 0 \le i < W, \quad 0 \le j < H,$$

where $*$ is convolution. The pixel $(i, j)$ is the pair of the index $(i, j)$ and the value $p_{ij}$, and the point $(i + \tfrac12, j + \tfrac12)$ is its center. With the Dirac delta, $p_{ij}$ is the value of $f$ at the center itself. The index $i$ counts columns from the left, and $j$ counts rows from the top in Direct3D, in most window systems and in image files, and from the bottom in the window coordinates of OpenGL. The continuous coordinate of a pixel center is its index plus $\tfrac12$, and the index of the pixel that contains the point $x$ is $\lfloor x \rfloor$.

The grid can have a spacing $s_x$ in $x$ and $s_y$ in $y$; with $s_x \ne s_y$ the pixels are non-square, and the ratio $s_x / s_y$ is the pixel aspect ratio. In the values, each channel is most often an integer of 8 to 16 bits, or a 16-bit or 32-bit float. A display or a resampler turns the samples back into a continuous image $\sum_{i,j} p_{ij}\, r(x - i - \tfrac12, y - j - \tfrac12)$ with a reconstruction filter $r$. By the [sampling theorem](/sampling-theorem/), $f$ comes back exactly only if it has no detail finer than half the grid frequency; finer detail appears as [aliasing](/aliasing/).

The word "pixel" was first printed in 1965, in work by Fred C. Billingsley at the Jet Propulsion Laboratory, and the shorter "pel" in 1967, by William F. Schreiber.

## Examples and non-examples

- **A full HD image.** An image of 1920 by 1080 pixels has 2,073,600 pixels, about 2.1 megapixels. Pixel $(0, 0)$ has its center at $(0.5, 0.5)$, and pixel $(1919, 1079)$ at $(1919.5, 1079.5)$.
- **A pixel of a frame buffer.** In a [frame buffer](/frame-buffer/) with 4 bytes per pixel, the value of pixel $(i, j)$ is the 4 bytes at offset $jP + 4i$, for the row pitch $P$.
- **Coverage in rasterization.** [Triangle rasterization](/triangle-rasterization/) gives pixel $(i, j)$ to a triangle when its center is inside the triangle, and the [top-left fill rule](/top-left-fill-rule/) decides for a center on an edge. In ray tracing, the [primary ray](/primary-ray-generation/) of a pixel goes through its center.
- **A box-filtered pixel.** With $h$ the box of width 1 around the center, $p_{ij}$ is the mean of $f$ over the unit square around the center. This is area sampling, a choice of prefilter; the pixel is still one value at one point.
- **Not a little square.** The unit square around the center is not the pixel. Drawing each sample as a square of constant color is reconstruction with a box filter $r$, which shows blocky edges when the image is enlarged. Bilinear or cubic reconstruction of the same samples gives smooth images.
- **Not a display subpixel.** A color display makes one pixel from separate red, green and blue emitters at slightly different places. These subpixels are parts of the hardware, not samples of the image.
- **Not a sensor photosite.** A camera sensor with a Bayer color filter measures one color at each site. A demosaicing step computes the pixels, each with all three colors, from neighboring sites.
- **Not a texel.** A texel is a sample of a texture. [Texture mapping](/texture-mapping/) maps texels to positions on the screen and filters them into pixels, and one pixel can cover many texels or a fraction of one.
- **Not a voxel.** A voxel is a sample on a grid in three dimensions, of a volume, not of an image.
- **The center at an integer point.** Direct3D 9 put pixel centers at integer coordinates, half a pixel away from the centers of Direct3D 10. This is a different convention for the same samples, and code that moves between the two must shift by half a pixel.

## Related definitions

A [digital image](/digital-image/) is the whole array of pixels. The [viewport transform](/viewport-transform/) maps normalized device coordinates to window coordinates, in which the pixel centers are at $i + \tfrac12$. A [reconstruction filter](/reconstruction-filter/) turns pixels back into a continuous image, and [antialiasing](/antialiasing/) chooses the prefilter $h$, or takes several samples per pixel, to reduce aliasing. A [frame buffer](/frame-buffer/) stores the pixels of a displayed image, and a [z-buffer](/z-buffer/) stores one depth per pixel.

## References
