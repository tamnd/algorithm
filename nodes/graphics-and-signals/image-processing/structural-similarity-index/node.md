---
tag: N7A0E4
kind: algorithm
slug: structural-similarity-index
name: Structural similarity index
aliases:
- SSIM
- mean structural similarity
area: graphics-and-signals/image-processing
level: advanced
summary: Compare two images window by window through their local means, variances and covariance, and average the scores into one index in (-1, 1].
solves: [image-quality-assessment]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, k: the window width in pixels}
  time: {worst: Θ(W H k), average: Θ(W H k), best: Θ(W H k)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, symmetric: true, full_reference: true, at_most_one: true, one_only_for_equal_images: true, separable_window: true}
history:
  year: 2004
  people: [Zhou Wang, Alan C. Bovik, Hamid R. Sheikh, Eero P. Simoncelli]
  note: Wang, Bovik, Sheikh and Simoncelli defined SSIM with stabilizing constants and an 11 by 11 Gaussian window in IEEE Transactions on Image Processing in 2004.
prereqs: [image-quality-assessment, variance, gaussian-filter]
see_also: [psnr, mean-squared-error, normalized-cross-correlation, separable-filter, integral-image, box-blur, image-noise, catastrophic-cancellation]
sources:
  - paper: doi:10.1109/TIP.2003.819861
    title: "Zhou Wang, Alan C. Bovik, Hamid R. Sheikh and Eero P. Simoncelli, Image quality assessment: from error visibility to structural similarity, IEEE Transactions on Image Processing 13(4), 2004"
    locator: Section III.B, equations (6) to (13), the three terms and the index; Section III.C, equations (14) to (17), the Gaussian window, K1 = 0.01, K2 = 0.03 and the mean over windows; Fig. 2, images with equal MSE
  - paper: doi:10.1109/MSP.2008.930649
    title: "Zhou Wang and Alan C. Bovik, Mean squared error: love it or leave it? A new look at signal fidelity measures, IEEE Signal Processing Magazine 26(1), 2009"
    locator: pages 98 to 117 (the limits of MSE and the structural similarity approach)
---

The structural similarity index (SSIM) compares a test image $y$ with a reference image $x$ in small windows. In each window it multiplies a luminance term from the two local means with a contrast and structure term from the two local variances and the covariance, and it averages the window scores into one number in $(-1, 1]$ that is 1 only when the images are equal. With a separable window of $k$ taps it costs $\Theta(WHk)$ time for a $W \times H$ image. It differs from [PSNR](/psnr/), which adds up the pixel errors and ignores where they are: two distortions with the same [mean squared error](/mean-squared-error/) can get very different SSIM scores.

## In plain words

Put a small window on the same place in both images and ask three questions. Is the window equally bright in both? Does it have the same amount of variation? Do the two windows rise and fall together, pixel by pixel? Each answer is a score that is 1 for a perfect match. SSIM multiplies the scores, slides the window over the whole image, and takes the average. A small change of the overall brightness keeps the pattern, so the score stays high. Noise of the same total size breaks the pattern, so the score falls. Two small constants keep the scores stable in dark or flat windows, where the questions would otherwise divide by nearly zero. The result follows what people see better than a plain pixel error does, but it is still only a model of vision.

## The problem

The input is two gray [digital images](/digital-image/) $x$ and $y$ of $W \times H$ pixels, one channel each, with values in $[0, L]$, where $L$ is the dynamic range, 255 for 8-bit codes. The values are used as stored, so for 8-bit images they are gamma encoded, as in the paper. Pixels are at integer positions. The window is a list of $k \le \min(W, H)$ weights $w_0, \ldots, w_{k-1} \ge 0$ with $\sum_a w_a = 1$, and the weight of offset $(a, b)$ is $w_a w_b$. The border rule is "valid windows only": a window is used only if it lies fully inside the image, so there are $M = (W - k + 1)(H - k + 1)$ positions and no padding. For a position $P$, write $E_P[f]$ for the weighted mean of $f$ over its window. Then

$$\mu_x = E_P[x], \quad \sigma_x^2 = E_P[(x - \mu_x)^2], \quad \sigma_{xy} = E_P[(x - \mu_x)(y - \mu_y)],$$

and the same for $y$. With $C_1 = (K_1 L)^2$ and $C_2 = (K_2 L)^2$, the index at $P$ is

$$S(P) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)},$$

and the output is the map $S$ and its mean, $\text{MSSIM} = \frac{1}{M}\sum_P S(P)$. The defaults of the paper are $K_1 = 0.01$, $K_2 = 0.03$ and an $11 \times 11$ Gaussian window with standard deviation 1.5. SSIM is a full-reference method for [image quality assessment](/image-quality-assessment/).

## The algorithm

```pseudo id=main
SSIM(x, y, W, H, w, L, K1, K2)                  ▷ w has k weights with sum 1
L1  C1 ← (K1 · L)²;  C2 ← (K2 · L)²
L2  μx, μy, Exx, Eyy, Exy ← FILTER-VALID(f, w) for f = x, y, x², y², x·y
L3  total ← 0
L4  for each position P = (i, j) with 0 ≤ i ≤ H − k and 0 ≤ j ≤ W − k do
L5      mx ← μx[P];  my ← μy[P]
L6      vx ← Exx[P] − mx²;  vy ← Eyy[P] − my²;  cxy ← Exy[P] − mx · my
L7      S[P] ← (2 mx my + C1)(2 cxy + C2) / ((mx² + my² + C1)(vx + vy + C2))
L8      total ← total + S[P]
L9  return total / ((W − k + 1)(H − k + 1)), S
```

FILTER-VALID at line L2 computes the weighted window sum at every valid position in two one-dimensional passes: first $R(r, j) = \sum_b w_b f(r, j + b)$ along each row, then $\sum_a w_a R(i + a, j)$ down each column. This is a [separable filter](/separable-filter/), and with the Gaussian weights it is a [Gaussian filter](/gaussian-filter/) without padding. Line L6 turns the raw second moments into the central ones with $E[xy] - \mu_x\mu_y$, so the five filtered images are all the loop needs.

## Example

Take $L = 255$, the uniform window $w = (1/3, 1/3, 1/3)$, so $k = 3$, and $3 \times 3$ images. There is one valid position. $C_1 = 2.55^2 = 6.5025$ and $C_2 = 7.65^2 = 58.5225$. The reference has the rows $(10, 20, 30)$:

$$x = \begin{pmatrix} 10 & 20 & 30 \\ 10 & 20 & 30 \\ 10 & 20 & 30 \end{pmatrix}, \qquad \mu_x = 20, \quad E[x^2] = \tfrac{1400}{3}, \quad \sigma_x^2 = \tfrac{1400}{3} - 400 = \tfrac{200}{3}.$$

| test image $y$ | $\mu_y$ | $\sigma_y^2$ | $\sigma_{xy}$ | luminance term | contrast and structure term | SSIM | MSE |
|---|---|---|---|---|---|---|---|
| rows $(20, 30, 40)$, $x + 10$ | 30 | 200/3 | 200/3 | $1206.5025 / 1306.5025$ | 1 | $482601/522601 \approx 0.9235$ | 100 |
| rows $(30, 20, 10)$, mirrored | 20 | 200/3 | −200/3 | 1 | $(-400/3 + C_2)/(400/3 + C_2)$ | $-89773/230227 \approx -0.3899$ | 266.7 |

For the shifted image, line L6 gives $\sigma_{xy} = (10 \cdot 20 + 20 \cdot 30 + 30 \cdot 40)/3 - 20 \cdot 30 = 200/3$, the pattern is the same, so only the luminance term is below 1. For the mirrored image the means and variances match, so the luminance term is 1, but $\sigma_{xy} = (10 \cdot 30 + 20 \cdot 20 + 30 \cdot 10)/3 - 400 = -200/3$, the pattern is reversed, and the score is negative. If instead only the last pixel 30 of $x$ becomes 31, SSIM is about 0.999476. These values are exact fractions from the implementation, which agrees with a direct computation of the central moments.

The same contrast holds on a larger image. On the $48 \times 48$ test image $x(r, q) = 40 + 2q + r + 30 \cdot ((\lfloor q/8 \rfloor + \lfloor r/8 \rfloor) \bmod 2)$, with the default window and $L = 255$, adding 10 to every pixel and adding $\pm 10$ with random signs from `random.Random(2026)` both give MSE 100 and PSNR 28.13 dB. MSSIM is 0.9967 for the shift and 0.7740 for the noise.

## Correctness

The proof is below. The weights $w_a w_b$ form a probability distribution on the window, so line L2 gives the weighted means of $x$, $y$, $x^2$, $y^2$ and $xy$, and line L6 gives the central moments by $E[(x - \mu_x)(y - \mu_y)] = E[xy] - \mu_x\mu_y$. Line L7 equals the product of the luminance, contrast and structure terms of the paper with $C_3 = C_2/2$. Each of the two factors is in $(-1, 1]$: the luminance factor is at most 1 because $(\mu_x - \mu_y)^2 \ge 0$ and above $-1$ because $(\mu_x + \mu_y)^2 + 2C_1 > 0$, and the second factor in the same way with $E[((x - \mu_x) \mp (y - \mu_y))^2]$. So $S$ is symmetric, lies in $(-1, 1]$, and is 1 only when $x = y$ at every pixel with a positive weight in the window.

## Complexity

In the [word RAM](/word-ram/), counting arithmetic on numbers as one step:

- Line L2 makes five filtered images. Each row pass costs $\Theta(W H k)$ and each column pass $\Theta((W - k + 1) H k)$, so line L2 costs $\Theta(W H k)$.
- Lines L4 to L8 run $M \le W H$ times at $\Theta(1)$ each.

The total is $\Theta(WHk)$ time and $\Theta(WH)$ extra space for the filtered images. A direct two-dimensional sum over each window costs $\Theta(WHk^2)$; for the default $k = 11$ the separable passes do about 11 times less work. With the uniform window, an [integral image](/integral-image/) of each of the five inputs gives every window sum in $\Theta(1)$, for $\Theta(WH)$ time in total, independent of $k$ (see also [box blur](/box-blur/)).

## Properties

- **Symmetric.** $S(x, y) = S(y, x)$ at each window, so it does not matter which image is the reference in the formula, only in the interpretation.
- **Bounded, with a unique maximum.** $-1 < S \le 1$, and $S = 1$ at a window only when the two windows are equal where the weights are positive. With a Gaussian window all weights are positive, so MSSIM is 1 only for equal images.
- **Negative for reversed patterns.** A negative score means the local covariance is negative enough to outweigh $C_2$, as in the mirrored example.
- **Not a sum over pixels.** Each window score is a ratio of window statistics, not an average of per-pixel terms, so the index cannot be split into pixel contributions as MSE can. The map $S$ shows where the loss is, one value per window.
- **Insensitive to a shift of brightness, sensitive in flat regions.** A constant shift changes only the luminance term, which stays near 1 when the means are large. In a flat window, $\sigma_x = 0$, and the second factor is $C_2/(\sigma_y^2 + C_2)$, so even weak noise lowers it a lot. On a $64 \times 64$ image of constant gray 128 with Gaussian noise of standard deviation 10 from `random.Random(6)`, MSE was 101.05, PSNR 28.09 dB and MSSIM 0.3836, close to $C_2/(100 + C_2) \approx 0.37$.
- **Same shape as cross-correlation.** With $C_2 = 0$, the structure term $\sigma_{xy}/(\sigma_x\sigma_y)$ is the local [normalized cross-correlation](/normalized-cross-correlation/).

## Variants and improvements

- **General exponents.** The paper defines $l^\alpha c^\beta s^\gamma$ with a free $C_3$. The common form, used here, is $\alpha = \beta = \gamma = 1$ and $C_3 = C_2/2$, which joins the contrast and structure terms into one fraction.
- **The constants set to zero.** With $C_1 = C_2 = 0$ the formula is an earlier universal quality index of Wang and Bovik. It is undefined in flat windows with equal means of zero, which is why the constants were added.
- **Window shape.** Earlier work used an $8 \times 8$ square window, which the 2004 paper reports gives blocking artifacts in the map; the Gaussian window with $\sigma = 1.5$ makes the map smooth. A uniform $7 \times 7$ window is a common faster choice in libraries.
- **Multiscale SSIM (MS-SSIM).** Wang, Simoncelli and Bovik combined the contrast and structure terms at several scales of a low-pass pyramid with the luminance term at the coarsest scale, to account for the viewing distance (see [Gaussian pyramid](/gaussian-pyramid/)).
- **Color and video.** A common practice is SSIM on the luma channel of [YCbCr](/color-spaces/), or a weighted average of per-channel scores. For video, per-frame scores are averaged.
- **Pooling.** The plain mean is one choice; weighted pooling gives more weight to windows with more detail or to the worst windows.

## When to use it

Use SSIM to compare a processed image with an undistorted reference of the same size and alignment: to compare compression codecs and settings, denoising or super-resolution results, or as a training loss where a pixel loss blurs textures. Report it together with [PSNR](/psnr/), and always state the window, the constants, $L$, the border rule and the channel, because each changes the number. Do not use it without a reference, for images that are shifted by even a pixel, or as the only judge of perceived quality: it is a model of local structure, not a full model of vision.

## Pitfalls

- **The wrong dynamic range.** For float images in $[0, 1]$, line L1 needs $L = 1$. With $L = 255$ the constants are $255^2$ times too large, they dominate every denominator, and almost every score is close to 1.
- **Different library defaults.** Window shape and size, the $1/N$ or $1/(N - 1)$ factor in the variance, the border rule, and a downsampling step all differ between implementations, so scores from two tools are often not comparable. This page uses weights with sum 1 and no correction factor, as in equations (14) to (16) of the paper.
- **Padding at the border.** Padding with zeros or by reflection adds windows that the valid rule leaves out, and zero padding creates false edges at the border. The map then has size $W \times H$ instead of $(W - k + 1) \times (H - k + 1)$, and the mean changes.
- **Cancellation in the variance.** Line L6 subtracts two large, nearly equal numbers when the window is bright and flat. In floating point the result can be slightly negative, and with 16-bit or offset data the error can be larger than $C_2$ (see [catastrophic cancellation](/catastrophic-cancellation/)). Use exact arithmetic for integers, or subtract the window mean before squaring.
- **Averaging color channels without care.** SSIM of R, G and B separately, averaged, is not the same as SSIM of the luma, and neither is the same as a color-aware index. State which one is used.
- **Reading the scale as linear.** Equal differences of SSIM do not mean equal differences of seen quality, and the same score means different things on different content. Compare scores only on the same content and settings.

## Implementations

## History

Zhou Wang, Alan Bovik, Hamid Sheikh and Eero Simoncelli published SSIM in IEEE Transactions on Image Processing in 2004. They framed image quality as the loss of structural information instead of the visibility of errors, and defined the index from the luminance, contrast and structure of local windows, with constants $C_1$ and $C_2$ for stability and a Gaussian window for a smooth quality map. In the paper, images with the same MSE of 210 get very different SSIM scores, which became the standard argument for the index. In 2009 Wang and Bovik reviewed the limits of MSE as a fidelity measure and the structural similarity approach in IEEE Signal Processing Magazine.

## References
