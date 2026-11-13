---
tag: V5CTT9
kind: problem
slug: image-warping
name: Image warping
aliases:
- geometric transformation of images
area: graphics-and-signals/image-processing
level: advanced
summary: Map pixels from one image geometry to another using a parametric or dense transform.
prereqs: [image-resampling, bilinear-interpolation, digital-image]
see_also: [bicubic-interpolation, image-registration, optical-flow, texture-mapping, mipmap, aliasing, lucas-kanade-method, seam-carving]
sources:
  - book: isbn:9780818689444
    title: George Wolberg, Digital Image Warping, IEEE Computer Society Press, 1990
    locator: the chapters on spatial transformations, image resampling, antialiasing and scanline algorithms
  - paper: "Paul S. Heckbert, Fundamentals of texture mapping and image warping, Master's thesis, University of California, Berkeley, Report UCB/CSD 89/516, 1989"
    locator: the chapters on affine and projective mappings, and on resampling with forward and inverse mapping
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 3, Image processing (geometric transformations, parametric and mesh-based warping); Chapter 2 (2D transformations)
---

Image warping is the problem of making a new image whose pixel at each point $u$ shows what the input image shows at another point $T^{-1}(u)$, for a given geometric transform $T$ from input coordinates to output coordinates. Rotation, scaling, shear, perspective correction, lens undistortion and morphing are all warps. A transform can be parametric, such as an affine map with 6 numbers or a projective map with 8, or dense, with a displacement vector for every pixel. The standard method is inverse mapping: for each output pixel, apply $T^{-1}$ to its center and read the input there by [image resampling](/image-resampling/), usually with [bilinear interpolation](/bilinear-interpolation/). Forward mapping, which sends each input pixel through $T$, leaves holes where $T$ stretches the image and overlaps where it squeezes it. When $T$ shrinks a region, the input must also be low-pass filtered over the footprint of each output pixel, or the output has [aliasing](/aliasing/).

## In plain words

Think of the image printed on a rubber sheet. A warp stretches, turns or bends the sheet, and the job is to make a new grid of pixels that shows the bent sheet. The natural idea is to take each old pixel and drop it where the warp sends it. That leaves gaps where the sheet was stretched, because the dropped pixels land too far apart. The better idea works backward: for each new pixel, ask where on the old image it came from. That point is usually between old pixels, so blend the nearest old pixels to get its value. Every new pixel then gets exactly one value, and there are no gaps. Where the warp makes things smaller, blend over a larger area to keep fine patterns from turning into wrong ones.

## Definition

The input is a [digital image](/digital-image/) $I$ with samples at integer pixel centers $(x, y)$, $0 \le x < W$, $0 \le y < H$, an output size $W' \times H'$, and an invertible map $T$ from the input plane to the output plane, given by $T$ or by $T^{-1}$. Let $\tilde I$ be a continuous reconstruction of $I$ by a kernel, as defined on the [image resampling](/image-resampling/) page. The warped image is

$$J(u, v) = \tilde I\big(T^{-1}(u, v)\big) \quad \text{for } 0 \le u < W',\ 0 \le v < H',$$

with a fill value, or a border rule, where $T^{-1}(u, v)$ falls outside the input. Common classes of $T$, with points written as columns $(x, y, 1)^\top$ in homogeneous coordinates:

- translation (2 parameters), rigid motion (3), similarity (4) and affine map (6), $(x, y) \mapsto (ax + by + c,\ dx + ey + f)$;
- projective map or homography (8), $(x, y) \mapsto \big((h_{00}x + h_{01}y + h_{02})/z,\ (h_{10}x + h_{11}y + h_{12})/z\big)$ with $z = h_{20}x + h_{21}y + h_{22}$, the map between two photos of a plane;
- polynomial and radial maps, used for lens distortion;
- dense maps, with a displacement $(\Delta x, \Delta y)$ stored for each output pixel, such as an [optical flow](/optical-flow/) field, or maps made by interpolating a few control points with splines or a triangle mesh.

When $T$ shrinks the image near a point, the footprint of one output pixel in the input covers many input pixels, and $\tilde I$ must use a kernel widened to that footprint: by the scale factor for a uniform scale, or by an ellipse given by the Jacobian of $T^{-1}$ for a general map.

## Variants

- Image to image with a given map, as above.
- Warping with an unknown map: the map must first be estimated, which is [image registration](/image-registration/) or [optical flow](/optical-flow/).
- Morphing: two images are warped toward each other along a family of maps and blended.
- Texture mapping in rendering, where the warp is the perspective map from texture space to the screen; see [texture mapping](/texture-mapping/).
- Content-aware warps, which deform the image so that important regions keep their shape, are one way to do [content-aware resizing](/content-aware-resizing/).
- Warps that are not invertible, or that fold, need a rule for overlapping parts, such as a depth order.

## Examples

Enlarge a $3 \times 3$ image by $3/2$ into a $4 \times 4$ image with $T(x, y) = (3x/2,\ 3y/2)$.

```text
input           forward mapping        inverse mapping, bilinear
10 20 30        10  .  20  30          10    50/3   70/3   30
40 50 60         .  .   .   .          30   110/3  130/3   50
70 80 90        40  .  50  60          50   170/3  190/3   70
                70  .  80  90          70   230/3  250/3   90
```

Forward mapping sends input columns 0, 1, 2 to output columns 0, 1.5 and 3, which round to 0, 2 and 3, so output column 1 and row 1 get no pixel: 7 of the 16 output pixels are holes, shown as dots. Inverse mapping reads output pixel $(1, 0)$ from the input point $(2/3, 0)$, which is $1/3$ of the way from 10 to 20 and gives $50/3$. Every output pixel gets a value.

Rotate a $16 \times 16$ image by 30 degrees about its center $(7.5, 7.5)$. For 200 of the 256 output pixels the inverse map lands inside the input. Forward mapping to the nearest output pixel leaves 24 of these 200 pixels empty, because the rotated grid of input centers does not hit every output center, while 24 other output pixels are hit by two input pixels each. Inverse mapping fills all 200.

A rotation by 90 degrees, with $T^{-1}(u, v) = (v,\ H - 1 - u)$ for an output of $H \times W$ pixels, maps pixel centers to pixel centers. Then every interpolation weight is 0 or 1, and the warp only moves pixels, with no loss; four such rotations give back the input exactly. A rotation by any other angle resamples, and each resampling with a short kernel blurs a little, so a chain of small rotations loses more detail than one rotation by the total angle.

## Known algorithms

- Inverse mapping with nearest-neighbor, [bilinear](/bilinear-interpolation/) or [bicubic](/bicubic-interpolation/) interpolation: one evaluation of $T^{-1}$ and one interpolation per output pixel. This is the method of the implementation on this page.
- Inverse mapping with a filtered footprint for shrinking warps: a fixed kernel widened by the local scale, the levels of a [mipmap](/mipmap/), or an elliptical weighted average over the footprint given by the Jacobian.
- Forward mapping with splatting: each input pixel spreads its value over the output pixels near $T(x, y)$ with weights, and the output divides by the sum of weights. It suits maps that are hard to invert, such as some depth-based view warps, at the cost of holes where the splats are too small.
- Separable two-pass warps: an affine or some nonlinear warps split into a pass along rows and a pass along columns, each a one-dimensional resampling, as in the scanline algorithms of Catmull and Smith; a rotation splits into three shears.
- Mesh and spline warps: a dense map built from control points by triangles with affine maps, or by smooth splines, then applied by inverse mapping.

## Bounds

- There are $W'H'$ output values, so any method needs $\Omega(W'H')$ work; inverse mapping with a kernel of $c \times c$ taps does $\Theta(W'H'c^2)$, or less with separable passes.
- A warp cannot add detail: where $T$ enlarges, the output has no more detail than the reconstruction $\tilde I$; where $T$ shrinks, detail above the new sampling rate must be removed, by the sampling theorem.
- Bilinear interpolation keeps each output value between the least and the largest of its four input pixels, so it adds no new extremes; kernels with negative lobes can overshoot.
- An inverse map that is only approximate, such as an inverse found by iteration for a lens model, adds its own position error to each output pixel.

## Reductions

- [Image resampling](/image-resampling/) for resizing is the warp by a scale. Every warp by inverse mapping reduces to resampling the input at the $W'H'$ points $T^{-1}(u, v)$.
- Composing two warps $T_2 \circ T_1$ and resampling once is better than resampling twice, because each resampling blurs; parametric maps compose exactly as matrices.
- Estimating the map from two images, which is [image registration](/image-registration/), reduces to optimizing the difference between one image and the warped other, as in the [Lucas-Kanade method](/lucas-kanade-method/).

## Applications

- Correcting lens distortion and perspective in photos and scanned documents.
- Stitching panoramas, where each photo is warped by a homography or onto a cylinder before blending.
- Registering medical and satellite images to a common frame.
- Texture mapping and view synthesis in graphics.
- Morphing and other visual effects, and retargeting an image to a new aspect ratio.

## References
