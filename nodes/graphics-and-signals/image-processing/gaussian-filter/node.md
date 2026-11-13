---
tag: T1ZJ15
kind: algorithm
slug: gaussian-filter
name: Gaussian filter
aliases:
- Gaussian blur
- Gaussian smoothing
area: graphics-and-signals/image-processing
level: intro
summary: Smooth an image with a kernel sampled from a Gaussian of standard deviation σ, cut at about 3σ and normalized, applied as a row pass and a column pass.
solves: [image-smoothing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, R: kernel radius (about 3σ)}
  time: {worst: Θ(W H R)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: true, rotation_symmetric: true, in_place: false}
history:
  year: 1983
  people: [Andrew P. Witkin]
  note: Witkin's scale-space filtering smoothed signals by Gaussians of growing width and followed features across the scales; Iijima in Japan had derived the Gaussian from axioms of this kind earlier.
prereqs: [linear-filtering, separable-filter]
see_also: [box-blur, image-smoothing, gaussian-pyramid, laplacian-of-gaussian, bilateral-filter, unsharp-masking, central-limit-theorem, convolution-via-fft]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.5, Smoothing (Lowpass) Spatial Filters, the subsection Lowpass Gaussian Filter Kernels
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2, Linear filtering, and Section 3.2.1, Separable filtering
  - paper: doi:10.1109/TPAMI.1986.4767776
    title: William M. Wells, Efficient synthesis of Gaussian filters by cascaded uniform filters, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(2), 234 to 239, 1986
    locator: the whole paper (cascades of uniform filters that approach a Gaussian)
  - paper: doi:10.1016/0165-1684(95)00020-E
    title: Ian T. Young and Lucas J. van Vliet, Recursive implementation of the Gaussian filter, Signal Processing 44(2), 139 to 151, 1995
    locator: the whole paper (a recursive filter whose cost per pixel does not depend on σ)
  - paper: "Andrew P. Witkin, Scale-space filtering, Proceedings of the 8th International Joint Conference on Artificial Intelligence (IJCAI), 1983"
    locator: the whole paper (Gaussian smoothing at a continuum of scales)
---

The Gaussian filter smooths an image with the kernel $G_\sigma(u, v) = e^{-(u^2+v^2)/(2\sigma^2)}$, sampled at the integer offsets, cut at the radius $R = \lceil 3\sigma \rceil$ and divided by its sum. It is the standard [linear filter](/linear-filtering/) for [image smoothing](/image-smoothing/). Its weights fall off smoothly with distance, its frequency response is again a Gaussian with no negative lobes, and it treats all directions alike. Because $e^{-(u^2+v^2)/(2\sigma^2)} = e^{-u^2/(2\sigma^2)} \, e^{-v^2/(2\sigma^2)}$, the 2D kernel is [separable](/separable-filter/): a pass along the rows and a pass along the columns with the same 1D kernel give the same result as the 2D kernel, at $2(2R+1)$ in place of $(2R+1)^2$ multiplications per pixel. Repeated [box blurs](/box-blur/) and recursive filters give close approximations at a cost per pixel that does not depend on $\sigma$.

## In plain words

To blur a pixel, take a weighted average of the pixels around it. Close neighbors get large weights and far neighbors get small ones, and the weights follow the bell curve. One number, the width of the bell, sets how strong the blur is. A wide bell mixes in pixels from far away and gives a strong blur. A narrow bell gives a light blur.

The bell curve has a useful property: the weight for a pixel that is a steps to the right and b steps down is the weight for a steps times the weight for b steps. So you can first blur every row with a short list of weights, and then blur every column of the result with the same list. This gives exactly the same picture as the full square of weights, with much less work.

## The problem

The input is a gray image $f$ with $W$ columns and $H$ rows, pixel centers at the integers, the standard deviation $\sigma > 0$ in pixels, and a border rule that extends each axis: clamp, mirror (the edge pixel repeated), wrap, or zero. The output is

$$g(x, y) = \sum_{v=-R}^{R} \sum_{u=-R}^{R} k[u]\, k[v]\, \tilde f(x+u, y+v), \qquad k[u] = \frac{e^{-u^2/(2\sigma^2)}}{\sum_{t=-R}^{R} e^{-t^2/(2\sigma^2)}},$$

where $\tilde f$ is the image extended by the border rule and $R = \lceil 3\sigma \rceil$. The values should be linear in light; for sRGB images decode first.

## The algorithm

```pseudo id=main
GAUSSIAN-FILTER(f, σ)                      ▷ the border rule extends each axis
L1  R ← ⌈3σ⌉
L2  for u ← −R to R do k[u] ← exp(−u² / (2σ²))
L3  k ← k / Σ_u k[u]                       ▷ the weights now sum to 1
L4  h[y][x] ← Σ_{u=−R}^{R} k[u] f̃(x + u, y)     for every pixel
L5  g[y][x] ← Σ_{v=−R}^{R} k[v] h̃(x, y + v)     for every pixel
L6  return g
```

Lines L1 to L3 build the 1D kernel. The cut at $3\sigma$ drops at most about $0.27\%$ of the weight of the continuous 1D Gaussian, and line L3 puts it back by renormalizing, so a constant image stays constant. Line L4 filters each row of the extended image. Line L5 filters each column of $h$, extended by the same rule along $y$. Because the 2D kernel is the outer product $k[v]\,k[u]$ and the border rule acts on each axis on its own, the two passes give exactly the double sum of the problem.

## Example

Take $\sigma = 1$, so $R = 3$, and the clamp rule. Lines L2 and L3 give the weights

| $u$ | $\pm 3$ | $\pm 2$ | $\pm 1$ | $0$ |
|---|---|---|---|---|
| $k[u]$ | 0.00443 | 0.05401 | 0.24204 | 0.39905 |

Filter the one-row image $f = (10, 12, 10, 50, 48, 50)$, a noisy step. For one row the column pass of line L5 changes nothing, because under the clamp rule every row above and below is a copy of the row, and the weights sum to 1. The row pass at $x = 2$ reads the extended pixels $\tilde f(-1) \dots \tilde f(5) = 10, 10, 12, 10, 50, 48, 50$:

| $u$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|---|---|---|
| $\tilde f(2+u)$ | 10 | 10 | 12 | 10 | 50 | 48 | 50 |
| $k[u]\,\tilde f(2+u)$ | 0.044 | 0.540 | 2.904 | 3.991 | 12.102 | 2.592 | 0.222 |

The sum is $22.395$. All six outputs are

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $f$ | 10 | 12 | 10 | 50 | 48 | 50 |
| $g$ | 10.661 | 13.127 | 22.395 | 37.605 | 46.873 | 49.339 |

The noise of $\pm 2$ is gone, and so is the sharp step: it is now a ramp over about four pixels. An [edge preserving filter](/bilateral-filter/) keeps the step. With the zero rule the same row gives $3.1, 5.0, 8.9, 14.9, 17.5, 13.7$, because the missing rows above and below count as black.

## Correctness

The kernel of line L3 is the 1D kernel $k$ of the problem. The proof is the one for any separable kernel: by the definition of line L4, $h(x, j) = \sum_u k[u] \tilde f(x+u, j)$ for every row $j$ of the image, and for a row $j$ outside the image the border rule gives $\tilde h(x, j) = \sum_u k[u] \tilde f(x+u, j)$ as well, because the rule acts on each axis on its own. Line L5 then gives $\sum_v k[v] \sum_u k[u] \tilde f(x+u, y+v)$, which is the double sum. The full proof is below, together with the variance $n r(r+1)/3$ of $n$ repeated boxes of radius $r$.

## Complexity

- **Time.** Lines L1 to L3 cost $\Theta(R)$. Each of lines L4 and L5 costs $2R+1$ multiplications per pixel, $\Theta(WHR)$ together, which is $\Theta(WH\sigma)$. The direct 2D sum costs $\Theta(WHR^2)$.
- **Space.** The intermediate image $h$, $\Theta(WH)$, or one row buffer if the column pass runs in strips.
- **Independent of $\sigma$.** Three box passes cost $\Theta(WH)$ for any $\sigma$, and so do the recursive filters of Deriche and of Young and van Vliet, which use a fixed number of multiplications per pixel. The FFT route, [convolution via FFT](/convolution-via-fft/), costs $\Theta(WH \log(WH))$ and handles the wrap rule exactly.

## Properties

- **Linear.** The output depends linearly on the image, and under the wrap rule it is also shift invariant.
- **Normalized.** The weights sum to 1, so a constant image stays constant under the clamp, mirror and wrap rules.
- **Smooth frequency response.** The continuous Gaussian has the Fourier transform $e^{-2\pi^2\sigma^2\omega^2}$ at the frequency $\omega$ in cycles per pixel. It is positive at every frequency, so no pattern is inverted, unlike the [box blur](/box-blur/).
- **Rotation symmetric.** The weight depends only on the distance $\sqrt{u^2+v^2}$. Among positive kernels that are continuous, the Gaussian is the only one that is both rotation symmetric and separable.
- **Cascades.** In the continuous setting, a Gaussian of $\sigma_1$ followed by a Gaussian of $\sigma_2$ is a Gaussian of $\sqrt{\sigma_1^2 + \sigma_2^2}$. The sampled kernels satisfy this only approximately, and the error is largest for small $\sigma$.

## Variants and improvements

- **Repeated boxes.** $n$ box blurs of radius $r$ form a kernel of variance $n r(r+1)/3$ that tends to the Gaussian shape by the [central limit theorem](/central-limit-theorem/) (Wells 1986). Three passes of radius 1 give $(1, 3, 6, 7, 6, 3, 1)/27$ along each axis, with $\sigma = \sqrt 2$. The cost is $\Theta(WH)$ per pass for any radius, but only some values of $\sigma$ are reachable with equal radii; mixing two radii fills the gaps.
- **Binomial kernels.** The rows of Pascal's triangle divided by $2^n$, such as $(1, 2, 1)/4$ and $(1, 4, 6, 4, 1)/16$, are exact integer kernels of variance $n/4$, the repeated box of width 2.
- **Recursive filters.** Deriche (1993) and Young and van Vliet (1995) approximate the Gaussian with a causal and an anticausal [IIR filter](/iir-filter/) along each axis, at a fixed cost per pixel for any $\sigma$.
- **Derivatives of the Gaussian.** Sampling $\partial G_\sigma / \partial x$ gives a smoothed gradient, used by the [Canny edge detector](/canny-edge-detector/), and the second derivatives give the [Laplacian of Gaussian](/laplacian-of-gaussian/).
- **Pyramids.** Blurring and then dropping every second pixel, again and again, gives the [Gaussian pyramid](/gaussian-pyramid/), which reaches large $\sigma$ at a small cost.
- **FFT.** For very large $\sigma$ on the wrap rule, multiply in the frequency domain, by the [convolution theorem](/convolution-theorem/).

## When to use it

Use the Gaussian filter as the default smoothing step: before edge and corner detection, before downsampling, to model optical blur, and to remove fine noise. It is linear and predictable, and its cost is low with the separable form. Use the [box blur](/box-blur/) or repeated boxes when $\sigma$ is large and speed matters. Use the [median filter](/median-filter/) for impulse noise, and the [bilateral filter](/bilateral-filter/), the [guided filter](/guided-filter/) or [non-local means](/non-local-means/) when edges must stay sharp.

## Pitfalls

- **No renormalization.** Leaving out line L3, or normalizing before the cut, gives weights that sum to less than 1, and the image grows darker with each pass. Divide by the sum of the weights that are kept.
- **A radius that is too small.** Writing $R \leftarrow \lceil \sigma \rceil$ at line L1 cuts off about a third of the weight, and the renormalized kernel is closer to a box than to a Gaussian. Use $R = \lceil 3\sigma \rceil$ or more.
- **Rounding between the passes.** Storing $h$ of line L4 as 8-bit integers adds a rounding error before the second pass. Keep $h$ in floating point or in fixed point with extra bits.
- **The zero rule.** Under the zero rule the border grows dark, as in the example. Use clamp or mirror, or renormalize by the weight that falls inside the image.
- **σ in the wrong units.** $\sigma$ is in pixels. When an image is resized, a blur with the same visual effect needs $\sigma$ scaled by the same factor.
- **Repeated boxes at the border.** Each box pass applies the border rule again, so the cascade equals one filter with the composite kernel only under the wrap rule, or at a distance of at least $nr$ from the border.

## Implementations

## History

The Gaussian function is due to Gauss and Laplace. In image processing it became the standard smoothing kernel with the theory of scale space: Iijima derived it from axioms in Japan around 1960, Witkin (1983) introduced scale-space filtering in the West, and Koenderink (1984) showed that the Gaussian is the kernel that creates no new structure as the scale grows. Marr and Hildreth (1980) used it before the Laplacian to find edges. Wells (1986) approximated it by cascaded box filters, and Deriche (1993) and Young and van Vliet (1995) by recursive filters.

## References
