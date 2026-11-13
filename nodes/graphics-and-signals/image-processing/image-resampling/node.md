---
tag: ZHSZ9B
kind: problem
slug: image-resampling
name: Image resampling
aliases:
- image scaling
- image interpolation
area: graphics-and-signals/image-processing
level: intro
summary: Compute new pixel values on a different sampling grid, as needed for resizing and warping.
prereqs: [digital-image, sampling-theorem, nearest-neighbor-interpolation, bilinear-interpolation]
see_also: [image-warping, bicubic-interpolation, reconstruction-filter, aliasing, mipmap, sample-rate-conversion, super-resolution, seam-carving]
sources:
  - book: isbn:9780818689444
    title: George Wolberg, Digital Image Warping, IEEE Computer Society Press, 1990
    locator: the chapters on sampling theory, image resampling and antialiasing
  - paper: doi:10.1109/TASSP.1981.1163711
    title: Robert G. Keys, Cubic convolution interpolation for digital image processing, IEEE Transactions on Acoustics, Speech, and Signal Processing 29(6):1153-1160, 1981
    locator: the cubic convolution kernel and the choice a = -1/2
  - paper: "Don P. Mitchell and Arun N. Netravali, Reconstruction filters in computer graphics, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4) (1988) 221-228"
    locator: the two-parameter family of cubic filters and the trade between blur, ringing and anisotropy
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 3, Image processing (interpolation, decimation and geometric transformations)
---

Image resampling is the problem of computing the values of an image on a new grid of sample points, given its values on the old grid. Resizing is the simplest case, where the new grid is the old one stretched or shrunk; [image warping](/image-warping/) is the general case, where the new sample points can be anywhere. A digital image does not say what lies between its samples, so every solution chooses a model: it reconstructs a continuous image from the samples with a kernel, and evaluates that continuous image at the new points. When the image gets smaller, the new grid cannot hold the fine detail of the old one, and the reconstruction must also remove that detail first, or it shows up as [aliasing](/aliasing/). The usual answers are a weighted sum of nearby pixels, with a nearest-neighbor, linear or cubic kernel, widened by the scale factor when the image shrinks.

## In plain words

To make a photo bigger, you need pixel values at places where the photo has none. The simplest answer copies the nearest pixel, which gives blocks. A better answer blends the nearby pixels, giving more weight to the closer ones, which gives smooth results. Blending over a wider area keeps edges sharper but can add faint light and dark bands next to them. To make a photo smaller, you have the opposite problem: many old pixels fall into each new pixel. Picking one of them makes fine patterns, such as a striped shirt, turn into wrong coarse patterns. So when shrinking, blend over all the old pixels that each new pixel covers.

## Definition

A gray [digital image](/digital-image/) with $W \times H$ pixels gives samples $I[i, j]$ at the integer points $(i, j)$, $0 \le i < W$, $0 \le j < H$, which are the pixel centers. A reconstruction kernel is a function $k$ on the real line with $\sum_{i \in \mathbb Z} k(t - i) = 1$ for all $t$. The separable reconstruction of $I$ is

$$\tilde I(x, y) = \frac{\sum_{i, j} k\big((x - i)/s_x\big)\, k\big((y - j)/s_y\big)\, I[\operatorname{c}(i), \operatorname{c}(j)]}{\sum_{i, j} k\big((x - i)/s_x\big)\, k\big((y - j)/s_y\big)},$$

where $\operatorname{c}$ clamps an index to the image, and $s_x, s_y \ge 1$ widen the kernel. The resampling problem asks for $\tilde I$ at a given set of points. To resize to $W' \times H'$ pixels, the center of new pixel $(i', j')$ maps to

$$x = (i' + \tfrac12)\,\frac{W}{W'} - \tfrac12, \qquad y = (j' + \tfrac12)\,\frac{H}{H'} - \tfrac12,$$

so that the outer edges of the two images line up. With antialiasing, $s_x = \max(1, W/W')$ and $s_y = \max(1, H/H')$. With $s_x = s_y = 1$ and an interpolating kernel ($k(0) = 1$ and $k(n) = 0$ for other integers $n$), $\tilde I$ passes through the samples, and the normalization has no effect away from the border.

Three kernels are standard:

- box, $k(t) = 1$ for $-\tfrac12 \le t < \tfrac12$ and 0 elsewhere, which gives [nearest-neighbor interpolation](/nearest-neighbor-interpolation/);
- tent, $k(t) = \max(0, 1 - |t|)$, which gives [bilinear interpolation](/bilinear-interpolation/);
- the Keys cubic with $a = -\tfrac12$: $k(t) = \tfrac32 |t|^3 - \tfrac52 |t|^2 + 1$ for $|t| < 1$, $k(t) = -\tfrac12 |t|^3 + \tfrac52 |t|^2 - 4|t| + 2$ for $1 \le |t| < 2$, and 0 elsewhere, which gives the "bicubic" filter of image software; see [bicubic interpolation](/bicubic-interpolation/).

The ideal kernel for a band-limited image is the sinc function of the [sampling theorem](/sampling-theorem/), which has infinite support; practical kernels are short and trade sharpness against blocks, blur and ringing. The [reconstruction filter](/reconstruction-filter/) page compares them.

## Variants

- Resizing by a factor, in one axis or both, which is the separable case above.
- Resampling at arbitrary points, as in [image warping](/image-warping/), where the scale can change across the image and the footprint of an output pixel in the input is a general shape, not a square.
- Integer factors: halving with a box of width 2 averages pairs of pixels, and repeated halving builds an [image pyramid](/image-pyramid/) or a [mipmap](/mipmap/).
- Color: each channel is resampled the same way. Averaging gamma-encoded values darkens fine bright detail; resampling in linear light avoids that.
- One-dimensional signals: the same problem for sound is [sample rate conversion](/sample-rate-conversion/), where filter design dominates and the scale is a rational number $L/M$.
- [Super-resolution](/super-resolution/) asks for more than resampling: true detail above the old sampling rate, from several images or from a learned model.

## Examples

Enlarge the row $(0, 0, 80, 80)$ from 4 to 8 samples. The new centers map to $x = -0.25, 0.25, 0.75, \ldots, 3.25$. The three kernels give:

| kernel | output |
|---|---|
| box | 0, 0, 0, 0, 80, 80, 80, 80 |
| tent | 0, 0, 0, 20, 60, 80, 80, 80 |
| Keys cubic | 0, $-15/8$, $-45/8$, $65/4$, $255/4$, $685/8$, $655/8$, 80 |

The box copies pixels, the tent blends them linearly, and the cubic makes the step steeper but goes below 0 and above 80 next to it: the ringing of a kernel with negative lobes.

Shrink a row of 8 samples to 4 with the tent and antialiasing. The scale is 2, so the tent is widened to support $(-2, 2)$, and the second output pixel, at $x = 2.5$, gets the weights $1/8, 3/8, 3/8, 1/8$ on input pixels 1 to 4.

Aliasing: shrink the row $0, 100, 0, 100, \ldots$ of 12 samples to 5. The pattern is finer than the new grid can show, so the best answer is gray, about 50 everywhere. Without antialiasing, the box gives $100, 100, 0, 0, 0$ and the tent gives $70, 90, 50, 10, 30$: false coarse patterns. With the kernel widened by $12/5$, the tent gives $38.6, 52.54, 50, 47.46, 61.4$, and the cubic gives $40.45, 50.87, 50, 49.13, 59.55$.

## Known algorithms

- Direct evaluation of the weighted sum for each output pixel, with a kernel of support $c$ taps per axis, takes $O(c^2)$ work per pixel.
- Separable resampling first resamples every row and then every column, as in the implementation on this page; it costs $O(c)$ per output sample and pass. The weights depend only on the output index, so they are computed once per row or column.
- [Bilinear interpolation](/bilinear-interpolation/) and [bicubic interpolation](/bicubic-interpolation/) are the tent and the Keys cubic, with $2 \times 2$ and $4 \times 4$ pixels per output value when enlarging.
- [Sinc interpolation](/sinc-interpolation/) and windowed sinc kernels, such as the Lanczos kernel, come closer to the ideal low-pass filter at the cost of more taps.
- Fourier methods resample a periodic image exactly for its band limit by padding or cutting its discrete Fourier transform.
- Pyramids and [mipmaps](/mipmap/) prefilter at sizes that halve, so that a shrink by any factor reads from a level that is close in size.

## Bounds

- The sampling theorem limits what any method can recover: detail above half the sampling rate of the input is not in the samples, so enlarging cannot add it without a prior model.
- For a smooth function sampled at spacing $h$, linear interpolation has error $O(h^2)$ when the second derivative is bounded, and the Keys cubic with $a = -\tfrac12$ has error $O(h^3)$ when the third derivative is bounded; Keys showed that other values of $a$ give only $O(h)$.
- The cost is $\Theta(W'H')$ output values times the kernel work, and every output value must be computed, so $\Omega(W'H')$ is a lower bound.
- A kernel with negative lobes gives, for some input, an output outside the range of the input values, as in the cubic example above; nonnegative kernels such as the box and the tent never do.

## Reductions

- Resizing is the special case of [image warping](/image-warping/) with an axis-aligned scale, and every warp by inverse mapping needs a resampling step.
- Separable resampling of an image reduces to one-dimensional resampling of its rows and its columns.
- Resampling with a fixed rational factor is a discrete convolution with a polyphase filter, the same structure as [sample rate conversion](/sample-rate-conversion/).

## Applications

- Display of images at a size other than their own, in viewers, web browsers and printers.
- Thumbnails and the levels of image pyramids.
- Geometric correction and registration of images, through warping.
- [Texture mapping](/texture-mapping/) in rendering, where [bilinear filtering](/bilinear-filtering/) and [mipmaps](/mipmap/) do the resampling.
- Changing the aspect ratio of an image, where [content-aware resizing](/content-aware-resizing/) is an alternative that keeps important objects unscaled.

## References
