---
tag: 7YRN0Y
kind: concept
slug: reconstruction-filter
name: Reconstruction filter
aliases:
- resampling filter
area: graphics-and-signals/rasterization
level: advanced
summary: Kernel that turns discrete samples back into a continuous image; sinc is ideal, box and tent are practical.
prereqs: [sampling-theorem, convolution]
see_also: [sinc-interpolation, aliasing, image-resampling, bilinear-filtering, nearest-neighbor-interpolation, catmull-rom-spline, b-spline, gibbs-phenomenon]
sources:
  - paper: doi:10.1145/54852.378514
    title: Don P. Mitchell and Arun N. Netravali, Reconstruction filters in computer graphics, Computer Graphics 22(4), SIGGRAPH 1988, pages 221 to 228
    locator: Section 2 (prealiasing and postaliasing), Section 3 (sample-frequency ripple, anisotropy, ringing and blurring), Section 4 (equations 7 and 8, the cubic family, Figure 13 and equation 9) and Section 5 (the notch filter)
  - paper: doi:10.1109/TASSP.1981.1163711
    title: Robert G. Keys, Cubic convolution interpolation for digital image processing, IEEE Transactions on Acoustics, Speech, and Signal Processing 29(6), 1981, pages 1153 to 1160
    locator: the whole paper (the interpolating cubic kernel and the choice a = -1/2 for third-order accuracy)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, 2016
    locator: Chapter 7, Sections 7.1 (sampling theory) and 7.8 (image reconstruction and the box, triangle, Gaussian, Mitchell and windowed sinc filters)
  - paper: "Paul S. Heckbert, Fundamentals of Texture Mapping and Image Warping, MS thesis, University of California, Berkeley, report UCB/CSD 89/516, June 1989"
    locator: the chapter on resampling filters (reconstruction, prefiltering and their combination)
---

A reconstruction filter is a kernel $h$ that turns samples $f[k]$ back into a function of a continuous position, $\tilde f(x) = \sum_k f[k]\, h(x - k)$. Displays, texture lookups, image scaling and renderers that place samples at arbitrary points all need one. The [sampling theorem](/sampling-theorem/) makes the sinc kernel ideal for bandlimited signals, but sinc has infinite support and rings at edges, so practical systems use short kernels: the box, the tent, cubic kernels such as Catmull-Rom and Mitchell-Netravali, and windowed sincs such as Lanczos. This page is about the choice of kernel; the formula with the sinc kernel itself is on the [sinc interpolation](/sinc-interpolation/) page.

## In plain words

A digital image stores colors only at points. To show it bigger, to rotate it, or to read it between those points, we need values in the gaps. A reconstruction filter is the recipe for these values: each stored point spreads its color over its neighborhood in a fixed shape, and the value at any position is the sum of what the nearby points spread there. A flat block shape gives a picture made of blocks. A tent shape gives straight ramps between points. Smooth bell shapes give smooth pictures, but they blur. The perfect shape for smooth signals is very wide and waves above and below zero, and it makes ripples next to sharp edges. Good filters for pictures are a compromise between blur, ripples and jagged edges, and a well-tuned small cubic shape is the usual choice.

## The idea

**Reconstruction as convolution.** With unit spacing, the sampled signal is $f_s(x) = f(x) \sum_n \delta(x - n)$, and reconstruction is the [convolution](/convolution/) $\tilde f = f_s * h$, so $\tilde f(x) = \sum_n f[n]\, h(x - n)$. In frequency, sampling repeats the spectrum $F$ at every integer frequency, and reconstruction multiplies the result by $H$, the Fourier transform of $h$. An ideal filter keeps the copy at zero frequency and removes all others: $H = 1$ for $|\nu| < 1/2$ and $0$ elsewhere. That is the sinc kernel $h(x) = \sin(\pi x)/(\pi x)$, and it reconstructs every signal with no energy at or above the Nyquist frequency $1/2$ exactly. In two dimensions, a separable filter uses $h(x)\, h(y)$, and a radial one uses $h(\sqrt{x^2 + y^2})$.

**Two kinds of aliasing.** Mitchell and Netravali separate *prealiasing*, which comes from sampling a signal with too much high frequency, from *postaliasing*, which comes from a reconstruction filter that lets parts of the spectral copies through. A good sampler with a poor reconstruction filter still shows moire patterns. Prefiltering before sampling is the cure for the first, the choice of $h$ for the second; see [aliasing](/aliasing/) and [antialiasing](/antialiasing/).

**Properties that matter.**

- *Interpolation.* If $h(0) = 1$ and $h(n) = 0$ for the other integers, then $\tilde f(n) = f[n]$, and the samples are kept exactly. Box, tent, sinc, Lanczos and Catmull-Rom interpolate; the Gaussian, the cubic B-spline and the Mitchell filter do not, and they blur.
- *Partition of unity.* If $\sum_n h(x - n) = 1$ for all $x$, constant images stay constant. Otherwise a flat area shows a pattern at the sample frequency, which Mitchell and Netravali call *sample-frequency ripple*. The condition is the same as $H(m) = 0$ for every nonzero integer $m$, which removes the copies of the zero-frequency part.
- *Polynomial reproduction.* A kernel that reproduces all polynomials of degree below $p$ makes the error $O(h^p)$ for smooth signals with sample spacing $h$. The tent reproduces linear functions; Catmull-Rom reproduces quadratics.
- *Ringing.* Negative lobes sharpen edges but make overshoot and ripples next to them, and clamping the overshoot of a bright edge to the display range makes dark spots. The sinc kernel, with lobes that decay only like $1/x$, rings most; this is the [Gibbs phenomenon](/gibbs-phenomenon/).
- *Anisotropy.* A separable kernel is not radially symmetric, and with poor parameters the sample grid shows in the image as horizontal and vertical structure.
- *Support.* A kernel of width $w$ reads about $w$ samples per output in one dimension and $w^2$ in two; a separable kernel needs $O(w)$ work per output in each of two passes.

**The common kernels.**

| Kernel | $h(x)$ | Width | Interpolates | Partition of unity |
|---|---|---|---|---|
| Box | $1$ for $-1/2 \le x < 1/2$ | 1 | yes | yes |
| Tent | $\max(0, 1 - \lvert x \rvert)$ | 2 | yes | yes |
| Gaussian | $e^{-x^2 / (2 \sigma^2)} / (\sigma \sqrt{2\pi})$, cut off | about $6\sigma$ | no | only approximately |
| Cubic B-spline | $(B, C) = (1, 0)$ below | 4 | no | yes |
| Catmull-Rom | $(B, C) = (0, 1/2)$ below | 4 | yes | yes |
| Mitchell | $(B, C) = (1/3, 1/3)$ below | 4 | no | yes |
| Lanczos $a$ | $\mathrm{sinc}(x)\,\mathrm{sinc}(x/a)$ for $\lvert x \rvert < a$ | $2a$ | yes | no, normalize the weights |
| Sinc | $\mathrm{sinc}(x)$ | infinite | yes | yes |

The box is [nearest-neighbor interpolation](/nearest-neighbor-interpolation/) and the tent in two dimensions is [bilinear filtering](/bilinear-filtering/). The frequency response of the box is $\mathrm{sinc}(\nu)$ and that of the tent is $\mathrm{sinc}^2(\nu)$, both far from the ideal step.

**The Mitchell-Netravali family.** Mitchell and Netravali asked for a symmetric piecewise cubic of width 4 that has a continuous value and first derivative and satisfies the partition of unity. These conditions leave two parameters:

$$h(x) = \frac16 \begin{cases} (12 - 9B - 6C)\lvert x \rvert^3 + (-18 + 12B + 6C)\lvert x \rvert^2 + (6 - 2B) & \lvert x \rvert < 1, \\ (-B - 6C)\lvert x \rvert^3 + (6B + 30C)\lvert x \rvert^2 + (-12B - 48C)\lvert x \rvert + (8B + 24C) & 1 \le \lvert x \rvert < 2, \\ 0 & \text{otherwise.} \end{cases}$$

$(B, C) = (1, 0)$ is the cubic [B-spline](/b-spline/), $B = 0$ gives the cardinal cubics, which interpolate, and $(0, 1/2)$ among them is the [Catmull-Rom spline](/catmull-rom-spline/), the cubic convolution kernel of Keys with $a = -1/2$. A Taylor analysis gives the error $(2C + B - 1)\, h f'(x)\, r(x) + O(h^2)$, so the filters on the line $B + 2C = 1$ reproduce linear functions and converge quadratically, and Catmull-Rom converges cubically. In a test with nine observers, Mitchell and Netravali mapped the $(B, C)$ plane into regions where blurring, ringing or anisotropy dominate, with a satisfactory region around the line $B + 2C = 1$, and they recommended $(1/3, 1/3)$. They also gave a notch filter, $(3/2, -1/4)$, whose response vanishes at the half-integer frequencies and which removes postaliasing well but blurs.

**Reconstruction in rendering.** A renderer that takes samples at irregular points $x_i$ computes each pixel $p$ as the normalized weighted mean $\sum_i h(x_i - p)\, L(x_i) / \sum_i h(x_i - p)$. Here the kernel acts both as the pixel's antialiasing filter and as the reconstruction of the image; the normalization makes the partition of unity hold for any sample positions. Physically Based Rendering offers the box, the tent, the Gaussian, the Mitchell filter and a windowed sinc for this step.

## Examples

**Kernel values.** For the three cubics, the values at $0$, $1/2$, $1$ and $3/2$ are:

| Kernel | $h(0)$ | $h(1/2)$ | $h(1)$ | $h(3/2)$ |
|---|---|---|---|---|
| B-spline $(1, 0)$ | $2/3$ | $23/48$ | $1/6$ | $1/48$ |
| Mitchell $(1/3, 1/3)$ | $8/9$ | $77/144$ | $1/18$ | $-5/144$ |
| Catmull-Rom $(0, 1/2)$ | $1$ | $9/16$ | $0$ | $-1/16$ |

In each row $h(0) + 2h(1) = 1$ and $2h(1/2) + 2h(3/2) = 1$: the partition of unity at an integer and at a half-integer position.

**A step edge.** Take the samples $f[n] = 0$ for $n \le 0$ and $f[n] = 1$ for $n \ge 1$, and reconstruct at $x = -1/2$, $1/2$ and $3/2$. The value at $x = 3/2$ is $1 - h(3/2)$ for any cubic of the family, by the partition of unity.

| Kernel | $\tilde f(-1/2)$ | $\tilde f(1/2)$ | $\tilde f(3/2)$ |
|---|---|---|---|
| Tent | $0$ | $1/2$ | $1$ |
| B-spline | $1/48$ | $1/2$ | $47/48$ |
| Mitchell | $-5/144$ | $1/2$ | $149/144$ |
| Catmull-Rom | $-1/16$ | $1/2$ | $17/16$ |
| Sinc | $1/2 - 2/\pi \approx -0.137$ | $1/2$ | $1/2 + 2/\pi \approx 1.137$ |

The B-spline blurs the edge and never overshoots, since it is nonnegative. Catmull-Rom overshoots by $1/16$, the Mitchell filter by $5/144 \approx 0.035$, and the sinc by almost $14\%$ of the step: $\sum_{n \ge 1} \mathrm{sinc}(3/2 - n) = 1/2 + \frac2\pi(1 - \frac13 + \frac15 - \dots) = 1/2 + 2/\pi$. This is why the ideal filter is a poor choice for images with sharp edges.

**Reproducing a parabola.** With $f[n] = n^2$, Catmull-Rom returns exactly $x^2$ at every $x$. The other filters on the line $B + 2C = 1$ reproduce linear functions but return $x^2 + B/3$ for this parabola: $x^2 + 1/9$ for the Mitchell filter and $x^2 + 1/3$ for the B-spline. Filters off the line, such as $(0, 1)$, do not even reproduce $f[n] = n$.

**Ripple from missing normalization.** A Gaussian with $\sigma = 1/2$, normalized to integral 1, gives $\sum_n h(x - n) \approx 1.0144$ at the integers and $0.9856$ at the half-integers, so a flat gray image gets a pattern of about $\pm 1.4\%$. Lanczos with $a = 2$ gives $1$ at the integers and about $1.019$ at the half-integers. Dividing by the sum of the weights, as in the rendering formula above, removes this ripple.

## Where it is used

- Texture lookups in GPUs: the box (nearest) and the tent ([bilinear filtering](/bilinear-filtering/)), and the tent across two [mipmap](/mipmap/) levels.
- [Image resampling](/image-resampling/) and [image warping](/image-warping/): scaling, rotation and the correction of lens distortion in image editors, video scalers and photo pipelines, with Catmull-Rom, Mitchell and Lanczos kernels.
- The pixel filter of offline renderers, which weights the samples of [supersampling](/supersampling-antialiasing/) into pixels.
- Digital to analog conversion and [sample rate conversion](/sample-rate-conversion/) of audio, where long windowed sincs approximate the ideal filter.
- Display hardware, where the shape of a pixel on the screen is itself a reconstruction filter.

## References
