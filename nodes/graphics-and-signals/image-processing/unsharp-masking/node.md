---
tag: JCQW4C
kind: algorithm
slug: unsharp-masking
name: Unsharp masking
aliases:
- unsharp mask
- highboost filtering
area: graphics-and-signals/image-processing
level: intro
summary: Sharpen an image by adding a multiple of the detail image, the image minus a blurred copy of it. Without a threshold this is one linear filter with the kernel (1 + λ)δ − λK.
solves: [image-sharpening]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, R: blur kernel radius}
  time: {worst: Θ(W H R)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: false, in_place: false}
history:
  year: 1970
  people: [William F. Schreiber]
  note: Schreiber applied unsharp masking electronically to improve wirephoto pictures. The name comes from darkroom photography, where a blurred positive copy of a negative served as a mask during printing.
prereqs: [gaussian-filter, linear-filtering]
see_also: [image-sharpening, box-blur, laplacian-of-gaussian, bilateral-filter, guided-filter, image-deblurring, laplacian-pyramid, frequency-response]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.6, Sharpening (Highpass) Spatial Filters, the subsection Unsharp Masking and Highboost Filtering
  - paper: "William F. Schreiber, Wirephoto quality improvement by unsharp masking, Pattern Recognition 2(2), 1970"
    locator: the whole paper (unsharp masking applied to wirephoto transmission)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2, Linear filtering (sharpening by unsharp masking)
---

Unsharp masking sharpens an image $f$ by adding a multiple of its detail. A blur $b = K * f$, usually a [Gaussian filter](/gaussian-filter/), removes the fine detail; the difference $f - b$ is the detail alone; and the output is

$$g = f + \lambda (f - b)$$

with an amount $\lambda > 0$. This is one [linear filter](/linear-filtering/) with the kernel $(1 + \lambda)\delta - \lambda K$, where $\delta$ is the unit impulse. Its gain is 1 for a flat image and grows toward $1 + \lambda$ for fine detail, so edges and texture gain contrast while flat regions stay as they are. The cost is that of the blur, $\Theta(WHR)$ with a separable kernel of radius $R$. It is the most common answer to the [image sharpening](/image-sharpening/) problem, in photo editors, printer drivers and camera pipelines.

## In plain words

Make a blurred copy of the picture. The blur removes the fine detail and keeps the broad shapes. Now subtract the blurred copy from the original. What is left is only the fine detail: the edges, the texture and the noise. Add this detail back to the original, a little more strongly than it was. The edges now stand out more, and the picture looks sharper.

The amount says how much detail is added back. The size of the blur says what counts as detail: a small blur picks thin lines and texture, a large blur picks broad edges. Too much amount makes bright and dark rims along the edges.

## The problem

The input is a gray image $f$ with $W$ columns and $H$ rows, a blur kernel $K$ that sums to 1 (here a separable Gaussian of $\sigma$ or a 1D kernel $k$ of radius $R$ used along both axes), an amount $\lambda \ge 0$, and a border rule for the blur: clamp, mirror (the edge pixel repeated), wrap or zero. Optional inputs are a threshold $t \ge 0$ and a value range $[\mathit{lo}, \mathit{hi}]$. The output is $g(p) = f(p) + \lambda (f(p) - (K * \tilde f)(p))$ at each pixel $p$, where $\tilde f$ is the image extended by the border rule. With a threshold, the pixels with $|f(p) - b(p)| < t$ keep $g(p) = f(p)$. With a range, $g$ is clipped to it.

## The algorithm

```pseudo id=main
UNSHARP-MASK(f, K, λ, t, lo, hi)
L1  b ← K * f̃                              ▷ the blur, with the border rule
L2  for each pixel p do
L3      d ← f[p] − b[p]                     ▷ the detail
L4      if |d| ≥ t then g[p] ← f[p] + λ d else g[p] ← f[p]
L5  return g clipped to [lo, hi]
```

Line L1 is the expensive step: two passes of the [separable filter](/separable-filter/) for a Gaussian, or two passes of running sums for a [box blur](/box-blur/). Line L3 forms the detail image, which is positive on the bright side of an edge and negative on the dark side. Line L4 adds $\lambda$ times the detail. With $t = 0$ every pixel is changed and the whole algorithm is linear; with $t > 0$ small differences, which are mostly noise, are left alone. Line L5 keeps the result in the range of the pixel format.

## Example

Take the one-row image $f = (10, 10, 10, 50, 50, 50)$, a clean step, the blur kernel $(1, 2, 1)/4$ along both axes, $\lambda = 1$ and the clamp rule. For one row under the clamp rule the column pass changes nothing.

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $f$ | 10 | 10 | 10 | 50 | 50 | 50 |
| $b$ (line L1) | 10 | 10 | 20 | 40 | 50 | 50 |
| $d = f - b$ (line L3) | 0 | 0 | $-10$ | 10 | 0 | 0 |
| $g = f + d$ (line L4) | 10 | 10 | 0 | 60 | 50 | 50 |
| clipped to $[0, 50]$ | 10 | 10 | 0 | 50 | 50 | 50 |

The step from 10 to 50 becomes a step from 0 to 60: the dark side gets darker and the bright side brighter, just at the edge. This overshoot is what makes the edge look sharper, and with a large $\lambda$ or a wide blur it shows as a halo. With the threshold $t = 11$ no pixel has $|d| \ge t$, and the image is unchanged.

## Correctness

Without a threshold or a range, $g = f + \lambda(f - K * \tilde f) = ((1+\lambda)\delta - \lambda K) * \tilde f$, because the center tap of $\delta$ reads the pixel itself under every border rule. So the algorithm equals direct 2D filtering with the combined kernel and the same border rule. Under the wrap rule its frequency response is $1 + \lambda(1 - \hat K(\omega))$, where $\hat K$ is the frequency response of the blur; for a symmetric nonnegative blur it lies in $[1, 1 + 2\lambda]$ and equals 1 at the frequency 0. The full proof is below.

## Complexity

- **Time.** Line L1 costs $\Theta(WHR)$ for a separable kernel of radius $R$, or $\Theta(WH)$ for a box blur by running sums. Lines L2 to L5 cost $\Theta(1)$ per pixel. The total is $\Theta(WHR)$ with a Gaussian.
- **Space.** The blurred image $b$, $\Theta(WH)$. The detail can be computed on the fly.
- **Direct form.** Filtering with the combined kernel costs $\Theta(WHR^2)$, because $(1 + \lambda)\delta - \lambda K$ is not separable even when $K$ is: it is the sum of two separable kernels.

## Properties

- **Linear without a threshold**, and shift invariant under the wrap rule. The threshold and the clipping make it nonlinear.
- **Flat regions are kept.** The kernel sums to $1 + \lambda - \lambda = 1$, so a constant image stays constant under clamp, mirror and wrap.
- **High-frequency gain.** For a Gaussian blur, $\hat K$ falls from 1 to near 0, so the gain rises from 1 at the frequency 0 to nearly $1 + \lambda$ for fine detail.
- **Close to Laplacian sharpening.** For a Gaussian of small $\sigma$, $f - K * f \approx -\tfrac{\sigma^2}{2} \nabla^2 f$, so unsharp masking is close to $f - c \nabla^2 f$, the sharpening with a Laplacian kernel.
- **Not a deblurring method.** It raises the contrast of detail that is still present, but it does not invert a known blur, as [deblurring](/image-deblurring/) does, and it amplifies noise in the same band as the detail.

## Variants and improvements

- **Highboost filtering.** Gonzalez and Woods call the case $\lambda = 1$ unsharp masking and $\lambda > 1$ highboost filtering. Some texts write the same filter as $A f - b$ with $A = 1 + \lambda$, divided by $A - 1$ or not.
- **Threshold.** Photo editors expose the amount, the radius $\sigma$ and the threshold $t$ of line L4. A soft threshold, which scales $d$ by a smooth function of $|d|$, avoids visible steps.
- **Edge aware blur.** Replacing the Gaussian of line L1 by a [bilateral filter](/bilateral-filter/) or a [guided filter](/guided-filter/) gives a detail image without the large edges, so detail is boosted without halos along them.
- **Several scales.** Boost the detail bands of a [Laplacian pyramid](/laplacian-pyramid/) with different amounts, to sharpen fine and coarse detail separately.
- **Luminance only.** For color images, sharpen only the luminance channel, so that the colors along edges do not shift.

## When to use it

Use unsharp masking for general sharpening of photographs, scans and prints, and to make up for the mild blur of lenses, resizing and printing. Choose $\sigma$ near the size of the detail to boost, and $\lambda$ between about $0.5$ and $2$. Use a threshold when the image is noisy. Use a deconvolution method, such as [Richardson-Lucy](/richardson-lucy-deconvolution/), when the blur kernel is known and must be undone. Use an edge aware blur in line L1 when halos along strong edges are a problem.

## Pitfalls

- **Overflow in 8-bit arithmetic.** Computing $f + \lambda d$ at line L4 in unsigned 8-bit integers wraps 260 to 4 and $-10$ to 246, so bright edges turn black. Compute in a signed wider type and clip once at line L5.
- **Halos.** A large $\lambda$ at line L4 with a wide blur at line L1 makes bright and dark rims along strong edges. Lower $\lambda$ or $\sigma$, or use an edge aware blur.
- **The sign of the detail.** Writing $d \leftarrow b[p] - f[p]$ at line L3 subtracts detail and blurs the image. The detail is $f - b$.
- **Noise amplification.** With $t = 0$, the noise is boosted along with the detail. Use a threshold, or smooth the noise first.
- **Sharpening encoded values.** Sharpening sRGB codes in place of linear values makes the rims of bright and dark edges unequal. Decide which one is wanted, and say so.

## Implementations

## History

The method comes from darkroom photography. A slightly blurred positive copy of a negative, the unsharp mask, was placed on the negative during printing, which reduced the broad contrast and so raised the fine detail relative to it. Schreiber (1970) did the same operation electronically to improve wirephoto pictures. The digital form with a Gaussian blur, an amount, a radius and a threshold is the standard sharpening tool of image editors.

## References
