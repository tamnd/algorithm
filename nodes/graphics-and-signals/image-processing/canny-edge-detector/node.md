---
tag: XAAHCF
kind: algorithm
slug: canny-edge-detector
name: Canny edge detector
aliases:
- Canny edge detection
area: graphics-and-signals/image-processing
level: intro
summary: Find thin, linked edges. Take the gradient of a Gaussian smoothed image, thin it with non-maximum suppression, and link the edges with hysteresis thresholding.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, r: radius ceil(3 sigma) of the Gaussian kernel}
  time: {worst: Θ(W H r), best: Θ(W H r)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: false, separable: true, exact: false, in_place: false}
history:
  year: 1986
  people: [John Canny]
  note: Canny stated three criteria for an edge detector and derived the detector from them, in his 1983 master's thesis at MIT and in his 1986 paper in IEEE PAMI.
prereqs: [gaussian-filter, sobel-operator, non-maximum-suppression, hysteresis-thresholding]
see_also: [laplacian-of-gaussian, scharr-operator, separable-filter, hough-transform, line-detection, active-contours, corner-detection, image-segmentation]
sources:
  - paper: doi:10.1109/TPAMI.1986.4767851
    title: John Canny, A computational approach to edge detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(6), 679 to 698, 1986
    locator: the three criteria, the derivation of the optimal step edge filter and its approximation by the first derivative of a Gaussian, non-maximum suppression and thresholding with hysteresis
  - paper: "John Canny, Finding edges and lines in images, Master's thesis, Massachusetts Institute of Technology, 1983 (MIT Artificial Intelligence Laboratory Technical Report 720)"
    locator: the whole report
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsection The Canny Edge Detector
  - book: isbn:9780132611084
    title: Emanuele Trucco and Alessandro Verri, Introductory Techniques for 3-D Computer Vision, Prentice Hall, 1998
    locator: Chapter 4, Image Features, the section on the Canny edge detector
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.2, Edges and contours
---

The Canny edge detector finds the edges of a gray image as thin, connected curves. It has three steps. First, it takes the gradient of the image after smoothing with a Gaussian of scale $\sigma$, which is the same as a correlation with the derivatives of a Gaussian. Second, [non-maximum suppression](/non-maximum-suppression/) keeps only the pixels where the gradient magnitude is a maximum along the gradient direction. Third, [hysteresis thresholding](/hysteresis-thresholding/) keeps the strong edge pixels and the weak ones that connect to them. John Canny derived the method in 1986 from three criteria for a detector of step edges in noise: good detection, good localization and a single response per edge. It is the standard answer to the [edge detection](/edge-detection/) problem, and it costs time linear in the number of pixels for a fixed $\sigma$.

## In plain words

First the detector blurs the image a little, so that the noise of single pixels does not look like edges. Then, at each pixel, it measures how fast the brightness changes and in which direction. Across an edge, this measure rises and falls like a ridge. The detector keeps only the top line of each ridge, so each edge is one pixel wide. Last, it removes the weak parts that are probably noise. A pixel on a very strong ridge is always kept. A pixel on a weaker ridge is kept only if it is part of a line that leads to a strong pixel. The amount of blur sets the size of the details the detector sees.

## The problem

The input is a gray image $I$ with $H$ rows and $W$ columns, a scale $\sigma > 0$ and two thresholds $0 < t_\ell \le t_h$. Pixel $(x, y)$ is a point sample at integer coordinates, with $x$ to the right and $y$ downward. There is one channel, with values that we treat as linear. A read outside the image returns the nearest border pixel (the clamp rule). The thresholds are on the gradient magnitude, in intensity units per pixel. The output is a mask $E$ of edge pixels. This is the variant of [edge detection](/edge-detection/) that asks for thin, linked edges.

## The algorithm

Let $r = \lceil 3\sigma \rceil$. The smoothing kernel is the sampled Gaussian $g[k] = e^{-k^2 / (2\sigma^2)} / Z$ for $|k| \le r$, where $Z$ makes the sum 1, as in the [Gaussian filter](/gaussian-filter/). The derivative kernel is $d[k] = k\, g[k] / \mu_2$ with $\mu_2 = \sum_k k^2 g[k]$. The factor $\mu_2$ makes $\sum_k k\, d[k] = 1$, so the derivative of the ramp $I(x) = x$ is exactly 1. Both kernels are 1D, so each 2D derivative is a [separable filter](/separable-filter/): $g_x$ is the correlation with $d$ along the rows and then with $g$ along the columns, and $g_y$ is the same with the two axes exchanged.

```pseudo id=main
CANNY(I, σ, t_ℓ, t_h)
L1  (g_x, g_y) ← (I ⋆ d along x ⋆ g along y, I ⋆ d along y ⋆ g along x)
L2  m ← NON-MAXIMUM-SUPPRESSION(g_x, g_y)   ▷ squared magnitudes of the kept pixels
L3  return HYSTERESIS(m, t_ℓ², t_h²)
```

Line L2 rounds the gradient direction to one of 0, 45, 90 and 135 degrees, and keeps $p$ if $m(p) > m(p - d)$ and $m(p) \ge m(p + d)$, where $d$ is the step to the neighbor in the rounded direction and $m = g_x^2 + g_y^2$. Line L3 keeps each pixel with $m \ge t_h^2$, and each pixel with $m \ge t_\ell^2$ that a path of such pixels, each an 8-neighbor of the next, joins to one with $m \ge t_h^2$. The thresholds are squared because $m$ is a squared magnitude. The pages on [non-maximum suppression](/non-maximum-suppression/) and [hysteresis thresholding](/hysteresis-thresholding/) give these two steps in full.

## Example

Take 12 rows of 16 pixels, each row $0, \ldots, 0, 100, \ldots, 100$ with 8 zeros, so the step is between columns 7 and 8, at $x = 7.5$. Let $\sigma = 1.5$, so $r = 5$, $t_\ell = 4$ and $t_h = 10$.

Line L1: every row is the same, so $g_y = 0$. Rounded to two places, $g_x$ in each row is

$$0, 0, 0, 0.23, 1.58, 6.40, 16.15, 25.64, 25.64, 16.15, 6.40, 1.58, 0.23, 0, 0, 0.$$

The response is spread over 10 columns by the smoothing, and it has two equal maxima, at columns 7 and 8, because the step is halfway between them.

Line L2: every pixel with $g_x \ne 0$ has the direction 0 degrees, so it is compared with its left and right neighbors. Column 7 has $m = 25.64^2$, more than column 6 and equal to column 8, so it stays. Column 8 is not more than column 7, so it goes. Every other column has a larger neighbor. The border rows 0 and 11 go. So each of the rows 1 to 10 keeps only column 7.

Line L3: column 7 has $25.64 \ge t_h = 10$, so all 10 pixels are strong and stay. The output is one vertical line at column 7, half a pixel from the true edge. With noise of standard deviation 8 added to a step of 100 at $\sigma = 2$, the test of the implementation still finds one pixel per row, at one of the two columns next to the step.

## Correctness

Edge detection has no single correct output, so the [proof](proofs/correctness.md) shows what the detector does on the inputs where the answer is clear. On an affine image $a x + b y + c$, away from the border, line L1 gives $g_x = a$ and $g_y = b$ exactly. On a vertical step of height $A > 0$ between columns $c$ and $c + 1$, the output in each interior row is exactly the pixel $c$, half a pixel from the step, when $A S \ge t_h$ for a constant $S$ that depends only on $\sigma$. So the detector gives one response at the right place, which is Canny's single response and localization criteria on this input. The other parts of the output follow from the pages on suppression and hysteresis: the kept pixels are maxima along the rounded gradient direction, and each one connects to a strong pixel.

The single response holds along the gradient direction. It does not hold for every edge direction on the grid. On a step at 45 degrees, the neighbors along $(1, 1)$ skip every other anti-diagonal, and two adjacent anti-diagonals can both stay. The test of the implementation shows this: with the step on the anti-diagonal $x + y = 40$, the rounded form keeps 2 pixels per row, and the interpolated form keeps 1.

## Complexity

Line L1 does four 1D correlations with kernels of $2r + 1$ taps, so it costs $4 (2r + 1) W H$ multiplications and additions, $\Theta(W H r)$ in the worst case and in the best case. A direct 2D correlation would cost $\Theta(W H r^2)$. Line L2 costs $\Theta(W H)$, and line L3 costs $\Theta(W H)$ in the worst case, because each pixel is pushed at most once. So the total time is $\Theta(W H r)$ with $r = \lceil 3\sigma \rceil$. The gradient images and the mask take $\Theta(W H)$ extra space. Recursive filters, as in the variant of Deriche, make line L1 cost $\Theta(W H)$ for every $\sigma$.

## Properties

- **Thin edges.** Each kept pixel is a maximum along its rounded gradient direction, so the edges are about one pixel wide.
- **Linked edges.** Each kept pixel is joined by a path of kept pixels to a strong pixel, so short isolated noise responses go.
- **Scale.** The parameter $\sigma$ sets a trade-off. A larger $\sigma$ removes more noise, but it moves corners and merges near edges.
- **Not linear.** Steps L2 and L3 are selections.
- **Invariance.** The output does not change when a constant is added to $I$. When $I$ and both thresholds are multiplied by the same positive number, the output does not change.
- **Open contours.** Unlike the zero crossings of the [Laplacian of Gaussian](/laplacian-of-gaussian/), Canny edges stop at corners and at junctions, where the gradient direction changes fast.

## Variants and improvements

- **Interpolated suppression.** Compare the magnitude with values interpolated at $p \pm u$ for the unit gradient $u$. This gives one pixel per row on diagonal steps through pixel centers. The implementation on this page has both forms.
- **Other gradients.** Many libraries use a [Sobel](/sobel-operator/) or [Scharr](/scharr-operator/) operator after a separate [Gaussian filter](/gaussian-filter/). The results are close, but the thresholds have a different scale: a Sobel output is 8 times the slope.
- **Recursive filters.** Rachid Deriche derived in 1987 a filter for Canny's criteria with an infinite support, and implemented it with recursive filters at a cost that does not depend on the scale.
- **Several scales.** Canny proposed to run the detector at several values of $\sigma$ and to combine the edges, which he called feature synthesis.
- **Thresholds from the image.** Canny suggested a high threshold 2 or 3 times the low one. A common rule takes $t_h$ from a high percentile of the gradient magnitudes. [Otsu's method](/otsu-thresholding/) on the magnitudes is another choice.
- **Color images.** Take the gradient of each channel and keep, at each pixel, the direction of the largest change over all channels.
- **Subpixel edges.** Fit a parabola across each kept pixel along the gradient to place the edge to a fraction of a pixel.

## When to use it

Use the Canny detector when you need thin, connected edges in a gray image: as input to the [Hough transform](/hough-transform/) for [line detection](/line-detection/), to contour following, to shape measurement, or to start [active contours](/active-contours/). Choose $\sigma$ from the noise and from the size of the smallest detail that matters. If you only need the strength of the edges, for example as a feature, a [Sobel operator](/sobel-operator/) is cheaper. If you need closed region boundaries, use [image segmentation](/image-segmentation/). For corners, use [corner detection](/corner-detection/).

## Pitfalls

- **The scale of the thresholds.** The thresholds compare with the gradient magnitude, which depends on the normalization of the derivative kernel and on the range of the image. Thresholds that work for one library or one image range can be wrong by a factor of 8 or 255 in another.
- **Squared magnitudes.** If line L2 returns squared magnitudes, square the thresholds too.
- **Too little smoothing.** With small $\sigma$ on a noisy image, noise makes many short edges, and some of them reach the high threshold.
- **Corners and junctions.** Near a corner, the gradient direction changes fast, so the suppression removes pixels and the edges have gaps there.
- **Kernel truncation.** A radius below about $3\sigma$ cuts off the tails of the Gaussian and the derivative stops being close to the derivative of a Gaussian.
- **Correlation and convolution.** With true [convolution](/discrete-convolution/) the derivative kernel is flipped, and the sign of the gradient changes. The magnitude is the same, but code that uses the sign, such as the check $g_x g_y > 0$ in the suppression, must use one convention throughout.

## Implementations

## History

John Canny developed the detector in his master's thesis "Finding edges and lines in images" at MIT in 1983, and published it in 1986 as "A computational approach to edge detection" in IEEE Transactions on Pattern Analysis and Machine Intelligence. He stated three criteria for a detector of step edges in white noise: good detection, good localization and only one response to each edge. He expressed them as functionals of the filter, and solved for the best filter by numerical optimization. The first derivative of a Gaussian came close to the best filter, and it is simple to compute, so he used it. The paper also introduced non-maximum suppression along the gradient direction and thresholding with hysteresis. The detector replaced the earlier operators of Roberts, Prewitt and Sobel and the zero crossings of Marr and Hildreth as the standard method, and it is in most image processing libraries.

## References
