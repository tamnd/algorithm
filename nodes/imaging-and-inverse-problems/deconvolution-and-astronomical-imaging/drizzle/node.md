---
tag: GWCHWD
kind: algorithm
slug: drizzle
name: Drizzle
aliases:
- variable-pixel linear reconstruction
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Combine dithered undersampled images by shrinking each input pixel to a smaller drop and adding its value to the output pixels it overlaps, weighted by overlap area. It keeps flux."
solves: [multiframe-super-resolution]
model: real-ram
complexity:
  vars: {n: the number of pixels per input frame, K: the number of frames, m: the number of output pixels, c: the most output pixels one drop overlaps}
  time: {worst: Θ(K n c + m), average: Θ(K n c + m), best: Θ(K n c + m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, iterative: false, linear: true, keeps_flux: true, handles_bad_pixels: true}
history:
  year: 2002
  people: [Andrew S. Fruchter, Richard N. Hook]
  note: "Fruchter and Hook developed drizzle to combine the dithered images of the Hubble Deep Field taken with the undersampled WFPC2 camera, and published it in 2002."
prereqs: [multiframe-super-resolution, image-resampling, aliasing]
see_also: [iterative-back-projection-super-resolution, super-resolution, image-registration, bilinear-interpolation, supersampling-antialiasing, lucky-imaging, sampling-theorem, point-spread-function]
sources:
  - paper: doi:10.1086/338393
    title: "Andrew S. Fruchter and Richard N. Hook, Drizzle: a method for the linear reconstruction of undersampled images, Publications of the Astronomical Society of the Pacific 114(792), 2002, 144 to 152"
    locator: "the drizzle algorithm (drops, pixfrac, output scale, weights and overlap areas), the conservation of flux and surface brightness, and the correlated noise of the output"
  - paper: doi:10.1109/TIP.2004.834669
    title: "Sina Farsiu, M. Dirk Robinson, Michael Elad and Peyman Milanfar, Fast and robust multiframe super resolution, IEEE Transactions on Image Processing 13(10), 2004, 1327 to 1344"
    locator: shift-and-add as the least squares and median fits for pure translation
---

Drizzle, formally variable-pixel linear reconstruction, combines several dithered images of the same field into one image on a finer grid. Fruchter and Hook built it for the Hubble Deep Field, whose camera pixels were too large for the PSF of the telescope. Each input pixel is mapped onto the output grid by the known geometric transform of its frame and shrunk to a smaller square, the *drop*, with the same center. The drop adds its value to each output pixel that it overlaps, weighted by the overlap area and by a per-pixel weight; at the end each output pixel is divided by its total weight. The result is a weighted mean, so the surface brightness and the weighted flux are kept exactly, bad pixels and cosmic rays are left out by a zero weight, and the output is a linear function of the data. The ratio of the drop size to the input pixel, the *pixfrac*, trades resolution against holes and noise. With a pixfrac of 1 and integer shifts drizzle is shift-and-add; with a small pixfrac and a complete set of subpixel dithers it is interlacing. It does not deblur: it removes the extra blur of the large pixel only as far as the dithers allow, and it does not undo the PSF of the optics. It solves a version of [multi-frame super-resolution](/multiframe-super-resolution/) where photometric accuracy matters more than sharpness.

## In plain words

Think of each pixel of a camera image as a square tile with a number on it, its brightness. You have several photos of the same sky, each moved by a fraction of a pixel. Lay out a fine grid of small output squares. Take each tile of each photo, shrink it around its center to a smaller drop, and place it on the fine grid where it belongs. Each small square that the drop touches gets a share of the brightness, in proportion to how much of the square the drop covers. Keep a second count of how much drop each small square received. At the end, divide the first sum by the second. Small drops keep the picture sharp but can leave empty squares; large drops fill every square but blur the picture a little.

## The problem

There are $K$ input frames of the same scene, each with $n$ pixels. Pixel $i$ of a frame has the value $d_i$ in counts and a weight $w_i \ge 0$ (an inverse variance, or $0$ for a bad pixel or a cosmic ray hit). The geometric transform of each frame to the output frame is known; it comes from the pointing of the telescope or from [image registration](/image-registration/), and it may include the distortion of the camera. The output is an image on a grid of square pixels of side $s$, in units of the input pixel side, with $s < 1$ for a finer grid. The goal is an output image in counts per output pixel that keeps the flux of the input and is as sharp as the dithers allow.

## The algorithm

The code and the pseudocode use a shift for each frame, so each drop stays an axis-aligned square. The general method maps the four corners of each drop through the transform and computes the area of overlap of a quadrilateral with each output pixel.

```pseudo id=main
DRIZZLE(frames, shifts, weights, s, p)       ▷ s: output pixel side, p: drop side (pixfrac)
L1  W ← 0, V ← 0 on the output grid
L2  for each frame k and each input pixel i with value d and weight w > 0
L3      drop ← square of side p around the center of pixel i, shifted by shift_k
L4      for each output pixel o that the drop overlaps
L5          a ← area(drop ∩ o)
L6          W_o ← W_o + a·w,  V_o ← V_o + a·w·d
L7  for each output pixel o
L8      I_o ← s² · V_o / W_o if W_o > 0, else 0       ▷ counts per output pixel
L9  return I, W
```

Line L8 turns counts per input pixel into counts per output pixel with the factor $s^2$, the ratio of the pixel areas. The weight image $W$ is an output too: it shows where the output is well covered, and it is the weight for a later drizzle or for photometry.

## Example

Take two frames of one row with three pixels each, $A = (2, 6, 2)$ shifted by $1/4$ and $B = (4, 4, 0)$ shifted by $3/4$ along the row. The output pixels have the side $s = 1/2$, so the output has two rows, and the two rows are equal. The drop of pixel $j$ of $A$ is centered at $j + 3/4$ and that of $B$ at $j + 5/4$. One output row (columns $0$ to $7$, in counts per output pixel) for three pixfracs, computed in exact arithmetic:

| $p$ | output $I$ | weight $W$ per column |
|---|---|---|
| $1$ | $1/2,\ 2/3,\ 1,\ 5/4,\ 1,\ 1/2,\ 1/6,\ 0$ | $1/8,\ 3/8,\ 1/2,\ 1/2,\ 1/2,\ 1/2,\ 3/8,\ 1/8$ |
| $3/4$ | $1/2,\ 3/5,\ 1,\ 4/3,\ 1,\ 1/2,\ 1/10,\ 0$ | $3/64,\ 15/64,\ 9/32,\ 9/32,\ 9/32,\ 9/32,\ 15/64,\ 3/64$ |
| $1/2$ | $0,\ 1/2,\ 1,\ 3/2,\ 1,\ 1/2,\ 0,\ 0$ | $0,\ 1/8,\ 1/8,\ 1/8,\ 1/8,\ 1/8,\ 1/8,\ 0$ |

With $p = 1/2$ each drop covers exactly one output column. The output is the interlaced sequence $A_0, B_0, A_1, B_1, A_2, B_2$ divided by $4$, and the peak $3/2$ is the sharpest. With $p = 1$ each drop covers three output pixels, the peak falls to $5/4$, and the edges of the field get partial coverage. In each case $\sum_o W_o I_o = s^2 p^2 \sum_i d_i$: the totals over both output rows are $9/2$, $81/32$ and $9/8$ for $p = 1, 3/4, 1/2$, and the input total is $18$.

## Correctness

The full proof is in `proofs/correctness.md`. The facts, all theorems about the computation:

1. **Overlap.** For axis-aligned squares, the overlap area is the product of the overlaps of the two side intervals, and the loop of line L4 finds every output pixel with a positive overlap.
2. **Weighted mean.** Where $W_o > 0$, $I_o/s^2$ is a convex combination of the values of the drops that touch $o$. A flat input of $c$ counts per pixel gives $c s^2$ counts per output pixel everywhere it is covered: the surface brightness is kept.
3. **Weighted flux.** When every drop lies inside the output grid, $\sum_o W_o I_o = s^2p^2\sum_i w_i d_i$ and $\sum_o W_o = p^2 \sum_i w_i$.
4. **Linearity.** For fixed geometry and weights, $I$ is linear in the data.
5. **Special cases.** With $s = p = 1$ and integer shifts drizzle is shift-and-add. With $s = p = 1/2$ and four dithers at half-pixel offsets, each drop is one output pixel and the result is the interlaced image divided by $4$.

## Complexity

In the real-RAM model, each drop overlaps at most $c = (\lceil p/s \rceil + 1)^2$ output pixels, and each overlap costs $O(1)$ for a square. So the $Kn$ drops cost $\Theta(Knc)$, and the final division costs $\Theta(m)$ for $m$ output pixels: $\Theta(Knc + m)$ in total, with $\Theta(m)$ extra space for $W$ and $V$. A general transform needs the area of a quadrilateral clipped to a square, still $O(1)$ per pair. There is no iteration, so the cost is fixed in advance.

## Properties

- **Keeps flux and surface brightness** (Claims 2 and 3). This is why astronomers use it for photometry.
- **Linear.** The output is a fixed linear map of the input for fixed geometry and weights, so noise and artifacts can be traced. It does not fit a model and does not deconvolve.
- **Bad pixels drop out.** A zero weight removes a pixel from every sum. The output stays correct where other frames cover the same place.
- **Correlated noise.** A drop larger than an output pixel puts the same input noise into several output pixels, so neighbor output pixels have correlated noise. Fruchter and Hook give a correction factor for the noise measured in an aperture.
- **The pixfrac is a choice.** A smaller pixfrac gives less smoothing and less correlated noise, but more variation in the weight and holes where no drop lands. The choice depends on the number of dithers and their pattern; it is tuned, not derived.

## Variants and improvements

- **General geometry.** Map the corners of each drop through the full transform, including the distortion of the camera, and clip polygons. Production codes for the Hubble Space Telescope do this.
- **Blot and cosmic ray rejection.** Drizzle each frame alone, take a median of the drizzled frames, map the median back to the frame of each input ("blot"), and mark the pixels that differ much from it as cosmic rays with weight $0$. Then drizzle again.
- **Kernels.** Replace the square drop by a point (the limit $p \to 0$, interlacing), a Gaussian or a Lanczos kernel. Only the square and the point give the exact flux identity of Claim 3 with an exact overlap area.
- **Deconvolution after drizzle.** Drizzle does not undo the optical PSF. A deconvolution step, or a joint method such as [iterative back-projection](/iterative-back-projection-super-resolution/), can follow.

## When to use it

Use drizzle to combine dithered, undersampled frames when the flux must be kept for photometry, when there are bad pixels and cosmic rays, and when the frames have different weights or a distorted geometry. It is the standard way to combine Hubble images. When the goal is maximum sharpness and the noise is low, a deconvolving method such as iterative back-projection or a regularized least squares fit gives sharper results, at the cost of a nonlocal and less predictable noise. When the frames are not undersampled, plain [resampling](/image-resampling/) and averaging are enough.

## Pitfalls

- **Holes.** With a small pixfrac and few dithers, some output pixels get no drop. Check the weight image $W$, and raise the pixfrac until $W$ has no zeros in the area of interest.
- **Wrong geometry.** An error in a shift moves the drops of a whole frame and blurs or doubles every source.
- **Reading the output as uncorrelated.** The noise of neighbor output pixels is correlated when $p > s$. Error bars from the pixel to pixel scatter are too small.
- **Units.** The output is in counts per output pixel. Forgetting the factor $s^2$ changes every flux by $1/s^2$.
- **Edges.** The plain sum $\sum_o I_o$ equals the input flux only where the coverage is uniform. Near the edge of the field use the weighted identity, or cut the edge.

## Implementations

## History

The Hubble Deep Field was imaged in 1995 with the WFPC2 camera, whose wide field pixels were large compared with the PSF of the telescope. The observers took many frames with small offsets. Fruchter and Hook developed drizzle to combine them without the extra blur of interpolation, and described it in their 2002 paper. Drizzle then became part of the standard processing of Hubble images. The idea of shift-and-add, the case $p = s = 1$, is older and is the basis of many multiframe methods; Farsiu et al. (2004) showed that it is the least squares fit, and its median version the L1 fit, for pure translation.

## References
