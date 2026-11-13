---
tag: CBGD3J
kind: algorithm
slug: scharr-operator
name: Scharr operator
aliases:
- Scharr filter
area: graphics-and-signals/image-processing
level: intro
summary: Estimate the image gradient with 3x3 kernels that smooth with [3, 10, 3] and take a central difference. The weights make the gradient direction much more accurate than Sobel's.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: true, exact: true, integer_only: true, in_place: false}
history:
  year: 2000
  people: [Hanno Scharr]
  note: Scharr derived derivative filters with optimal rotation invariance in his PhD thesis at the University of Heidelberg in 2000, after joint work with Bernd Jähne and Stefan Körkel in 1999.
prereqs: [sobel-operator, edge-detection, linear-filtering]
see_also: [prewitt-operator, roberts-cross-operator, separable-filter, frequency-response, canny-edge-detector, harris-corner-detector, gaussian-filter]
sources:
  - paper: "Hanno Scharr, Optimale Operatoren in der Digitalen Bildverarbeitung, PhD thesis, Interdisciplinary Center for Scientific Computing (IWR), University of Heidelberg, 2000"
    locator: the chapters on the design of derivative filters with optimal rotation invariance
  - paper: "Bernd Jähne, Hanno Scharr and Stefan Körkel, Principles of filter design, in Bernd Jähne, Horst Haussecker and Peter Geissler (editors), Handbook of Computer Vision and Applications, Volume 2, Academic Press, 1999"
    locator: the chapter as a whole (filter design by optimization of the transfer function, and the optimized 3x3 derivative filters)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.2, Edges and contours
---

The Scharr operator estimates the gradient of a gray [digital image](/digital-image/) with two $3 \times 3$ integer kernels, like the [Sobel operator](/sobel-operator/). The difference is the smoothing weights across the derivative: $[3, 10, 3]$ instead of $[1, 2, 1]$. Hanno Scharr chose these weights so that the estimated direction of the gradient depends as little as possible on the direction of the edge. At the same cost as Sobel, the largest direction error on a plane wave is 4 to 11 times smaller. It is used where the gradient direction matters, for example in optical flow and in orientation features.

## In plain words

The Sobel operator measures how fast the brightness changes from left to right by comparing the column on the right of a pixel with the column on the left. It counts the middle pixel of each column two times. This choice works well, but an edge at 30 degrees gets a direction that is a little wrong, and the error changes with the angle of the edge. Scharr found weights that make this error much smaller: count the middle pixel ten times and the two others three times. The cost does not change. Only three numbers in the kernel change.

## The problem

The input is a gray image $I$ with $H$ rows and $W$ columns. Pixel $(x, y)$ is a point sample at integer coordinates, with $x$ to the right and $y$ downward. There is one channel, with integer values from 0 to 255 that we treat as linear. A read outside the image returns the nearest border pixel (the clamp rule). The output is a pair of integer images $g_x$ and $g_y$ that estimate $32\, \partial I / \partial x$ and $32\, \partial I / \partial y$, such that the direction $\operatorname{atan2}(g_y, g_x)$ is accurate for every edge direction. This is the gradient step of [edge detection](/edge-detection/).

The operator is the [correlation](/cross-correlation/) of $I$ with

$$S_x = \begin{pmatrix} -3 & 0 & 3 \\ -10 & 0 & 10 \\ -3 & 0 & 3 \end{pmatrix} = [3, 10, 3]^T [-1, 0, 1], \qquad S_y = S_x^T.$$

## The algorithm

```pseudo id=main
SCHARR(I)                                   ▷ I is H × W, reads use the clamp rule
L1  for each pixel (x, y): s(x, y) ← 3 I(x, y − 1) + 10 I(x, y) + 3 I(x, y + 1)
L2  for each pixel (x, y): d(x, y) ← 3 I(x − 1, y) + 10 I(x, y) + 3 I(x + 1, y)
L3  for each pixel (x, y): g_x(x, y) ← s(x + 1, y) − s(x − 1, y)
L4  for each pixel (x, y): g_y(x, y) ← d(x, y + 1) − d(x, y − 1)
L5  return (g_x, g_y)
```

Lines L1 and L2 smooth the columns and the rows with the Scharr weights. Lines L3 and L4 take the central differences. The reads of $s$ and $d$ also use the clamp rule. The direction is $\operatorname{atan2}(g_y, g_x)$ and the magnitude is $\sqrt{g_x^2 + g_y^2}$.

## Example

Take the image with 4 rows and 5 columns where a dark region (10) meets a bright region (80), and the boundary moves one column to the left between rows 1 and 2:

$$I = \begin{pmatrix} 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \end{pmatrix}.$$

At pixel $(2, 1)$, line L1 gives $s(3, 1) = 240 + 800 + 240 = 1280$ and $s(1, 1) = 30 + 100 + 30 = 160$, so $g_x(2, 1) = 1120$. Line L2 gives $d(2, 2) = 30 + 800 + 240 = 1070$ and $d(2, 0) = 30 + 100 + 240 = 370$, so $g_y(2, 1) = 700$. The full outputs are

$$g_x = \begin{pmatrix} 0 & 0 & 1120 & 1120 & 0 \\ 0 & 210 & 1120 & 910 & 0 \\ 0 & 910 & 1120 & 210 & 0 \\ 0 & 1120 & 1120 & 0 & 0 \end{pmatrix}, \qquad g_y = \begin{pmatrix} 0 & 0 & 0 & 0 & 0 \\ 0 & 210 & 700 & 210 & 0 \\ 0 & 210 & 700 & 210 & 0 \\ 0 & 0 & 0 & 0 & 0 \end{pmatrix}.$$

At $(2, 1)$ the direction is $\operatorname{atan2}(700, 1120) \approx 32.0°$. The [Sobel operator](/sobel-operator/) gives $26.6°$ and the [Prewitt operator](/prewitt-operator/) gives $18.4°$ at the same pixel. A step of height 70 gives $g_x = 16 \cdot 70 = 1120$ next to it.

## Correctness

The [proof](proofs/correctness.md) shows that the separable passes equal the direct correlation with $S_x$ and $S_y$ at every pixel, and that on an affine image $I = a x + b y + c$ the output is exactly $g_x = 32a$ and $g_y = 32b$ at each pixel whose neighborhood is inside the image. It then proves the direction error formula for any smoothing weights $[a, b, a]$. For a plane wave of frequency $\omega$ at the angle $\theta$, the estimated angle is

$$\hat\theta = \theta + \left( \frac{1}{6} - \frac{a}{b + 2a} \right) \frac{|\omega|^2}{4} \sin 4\theta + O(|\omega|^4).$$

The factor $\tfrac{1}{6} - \tfrac{a}{b + 2a}$ is $-\tfrac{1}{6}$ for Prewitt, $-\tfrac{1}{12}$ for Sobel and only $-\tfrac{1}{48}$ for Scharr. This is the reason for the weights.

## Complexity

Lines L1 and L2 each do 2 additions and 3 multiplications by small constants per pixel, and lines L3 and L4 each do 1 subtraction. The time is $\Theta(W H)$ in the worst case and in the best case, with a constant cost per pixel that is the same as Sobel's up to the multiplications. The temporary images and the outputs take $\Theta(W H)$ extra space. With 8-bit input, $|g_x| \le 16 \cdot 255 = 4080$, which fits in a signed 16-bit integer, and $g_x^2 + g_y^2 \le 33\,292\,800$ fits in a signed 32-bit integer.

## Properties

- **Exact and integer.** All weights are integers, so the output has no rounding error. Divide by 32 for the slope in intensity units per pixel.
- **Direction error.** The largest error of $\hat\theta$ over all directions of a plane wave, computed from the exact response $g_x \propto \sin \omega_x (10 + 6 \cos \omega_y)$, is 0.045 degrees at the frequency radius $\pi/8$, 0.16 degrees at $\pi/4$ and 0.29 degrees at $\pi/2$. For Sobel the values are 0.19, 0.75 and 3.2 degrees. These values come from the formula, not from measured images.
- **Not the leading order optimum.** The weights $[1, 4, 1]$ make the factor of the leading error term 0, so they are better than Scharr's weights at low frequencies (0.002 degrees at $\pi/8$). At $\pi/2$ their error is 0.64 degrees, more than twice Scharr's. Scharr's weights come from an optimization over a band of frequencies, not from the leading term alone.
- **Smoothing.** The smoothing $[3, 10, 3] / 16$ is weaker than Sobel's $[1, 2, 1] / 4$, so the operator suppresses less noise across the edge.

## Variants and improvements

- **Other optimized weights.** The same design method gives other integer versions. One with the smoothing $[47, 162, 47]$, whose sum is 256, suits 8-bit fixed point arithmetic. By the same formula its largest error is 0.036 degrees at $\pi/8$ and 0.11 degrees at $\pi/2$.
- **Larger optimized kernels.** The method extends to $5 \times 5$ kernels and to derivatives along time for optical flow, with more accurate directions again.
- **Derivative of Gaussian.** A sampled derivative of a Gaussian with a large $\sigma$, as in [Canny's detector](/canny-edge-detector/), is also nearly free of direction error, but it costs more and smooths more.

## When to use it

Use the Scharr operator in place of the [Sobel operator](/sobel-operator/) when the direction of the gradient is used, not only its size: in orientation histograms, in the gradient products of the [Harris corner detector](/harris-corner-detector/), in optical flow, and in the direction step of [non-maximum suppression](/non-maximum-suppression/). The cost is the same. Use Sobel when you need more smoothing or compatibility with thresholds tuned for Sobel.

## Pitfalls

- **Normalization.** The output is 32 times the slope. Some texts normalize the kernel by $1/32$, some by $1/16$ and some not at all. Thresholds do not carry over between these forms.
- **Correlation and convolution.** True [convolution](/discrete-convolution/) flips the masks, which changes the sign of the output.
- **Accuracy at the border.** The direction error result holds only where the $3 \times 3$ neighborhood is inside the image. Near the border, the clamp rule changes the response.
- **Gamma encoded input.** The direction is not affected by a monotone change of the intensities on a straight edge, but the magnitude is. Convert sRGB to linear values when the magnitude must be physical.
- **Noise.** Better direction accuracy on clean images does not mean a better result on noisy images. Smooth first with a [Gaussian filter](/gaussian-filter/) when the noise is strong.

## Implementations

## History

Bernd Jähne, Hanno Scharr and Stefan Körkel described the design of filters by optimization of their [transfer function](/frequency-response/) in the Handbook of Computer Vision and Applications in 1999. Scharr's PhD thesis at the University of Heidelberg in 2000 developed derivative filters that are optimal for rotation invariance, with the $3 \times 3$ kernel that now has his name. The integer weights $[3, 10, 3]$ are the form in common use in libraries. It was a late improvement of the $3 \times 3$ gradient masks of Prewitt (1970) and of Sobel and Feldman (1968).

## References
