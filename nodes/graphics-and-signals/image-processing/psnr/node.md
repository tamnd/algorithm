---
tag: T7XT8F
kind: definition
slug: psnr
name: Peak signal-to-noise ratio
aliases:
- PSNR
area: graphics-and-signals/image-processing
level: intro
summary: Ten times the base-10 log of the squared peak value over the mean squared error of an image against its reference, in decibels; higher is closer, infinite for equal images.
prereqs: [mean-squared-error, digital-image]
see_also: [structural-similarity-index, image-quality-assessment, image-noise, lossy-image-compression, jensens-inequality, scalar-quantization, image-denoising]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 8.1, Fidelity Criteria, page 603 (the root-mean-square error and the mean-square signal-to-noise ratio)
  - paper: doi:10.1049/el:20080522
    title: Quan Huynh-Thu and Mohammed Ghanbari, Scope of validity of PSNR in image/video quality assessment, Electronics Letters 44(13), 2008
    locator: pages 800 to 801 (PSNR tracks quality for a fixed content and codec, but not across different contents)
  - paper: doi:10.1109/MSP.2008.930649
    title: "Zhou Wang and Alan C. Bovik, Mean squared error: love it or leave it? A new look at signal fidelity measures, IEEE Signal Processing Magazine 26(1), 2009"
    locator: pages 98 to 117 (the definition of PSNR from MSE, its properties, and its limits as a quality measure)
---

The peak signal-to-noise ratio (PSNR) of an image $y$ against a reference $x$ of the same size is $10\log_{10}(P^2/\text{MSE})$ decibels, where MSE is the [mean squared error](/mean-squared-error/) of the pixel values and $P$ is the largest possible value, 255 for 8-bit images. It is MSE on a log scale, normalized by the value range, so it can be compared across bit depths; higher is closer, a factor of 10 in MSE is 10 dB, and equal images have infinite PSNR. It differs from [SSIM](/structural-similarity-index/), which compares local structure, and from a signal-to-noise ratio, which divides by the power of the signal and not by the squared peak.

## Definition

**The model.** $x$ and $y$ are [digital images](/digital-image/) of $W \times H$ pixels with $C$ channels, and the values are compared as stored, so 8-bit codes are usually gamma encoded. Each pixel is compared with the pixel at the same position, so positions must align, and no border rule is needed. Let $N = WHC$, let $i$ run over all pixels and channels, and

$$\text{MSE}(x, y) = \frac{1}{N} \sum_{i=1}^{N} (x_i - y_i)^2.$$

For a peak value $P > 0$, the PSNR in decibels is

$$\text{PSNR}(x, y) = 10 \log_{10} \frac{P^2}{\text{MSE}(x, y)} = 20 \log_{10} P - 10\log_{10} \text{MSE}(x, y),$$

and $\text{PSNR} = +\infty$ when $\text{MSE} = 0$. The peak is $P = 2^b - 1$ for $b$-bit integer values, so 255 for 8 bits, and $P = 1$ for values in $[0, 1]$. Gonzalez and Woods define the root-mean-square error $\sqrt{\text{MSE}}$ and a mean-square signal-to-noise ratio as fidelity criteria; PSNR is the peak form in decibels.

**Properties that follow.**

- PSNR is a strictly decreasing function of MSE, so the two always rank pairs of images in the same order. It is symmetric in $x$ and $y$.
- Scaling both images and the peak by the same factor does not change it.
- Halving the error at every pixel divides MSE by 4 and adds $20\log_{10} 2 \approx 6.02$ dB.
- It is a mean over pixels: it does not see where the errors are or whether they form a pattern.

## Examples and non-examples

- **An error of 1 at every pixel.** For 8-bit images, $\text{MSE} = 1$ gives $10\log_{10} 65025 \approx 48.1308$ dB.
- **Rounding.** Rounding a busy image to integer codes adds an error that is close to uniform in $[-1/2, 1/2)$, so $\text{MSE} \approx 1/12$ and PSNR is about 58.9 dB. Any 8-bit image therefore carries about 59 dB of rounding error against the continuous image.
- **Gaussian noise.** With $\sigma = 10$, the expected MSE is 100 and the PSNR is $10\log_{10}(65025/100) \approx 28.13$ dB. On a $64 \times 64$ gray image with rounding and `random.Random(6)` the measured value was 28.09 dB (see [image noise](/image-noise/)).
- **Equal PSNR, different look.** On a $48 \times 48$ test image, adding 10 to every pixel and adding $\pm 10$ with random signs both give MSE 100 and 28.13 dB, but the first looks like the same picture slightly brighter and the second looks noisy. [SSIM](/structural-similarity-index/) gives 0.9967 and 0.7740.
- **A sequence of frames.** For two frames with MSE 1 and 100, the mean of the per-frame PSNR values is $(48.13 + 28.13)/2 = 38.13$ dB, but the PSNR of the mean MSE, 50.5, is 31.10 dB. Because $-\log$ is convex, the first is never smaller than the second by [Jensen's inequality](/jensens-inequality/), so a video report must say which average it uses.
- **The peak for other bit depths.** A 16-bit image made from an 8-bit one by multiplying by 257 has errors 257 times larger and peak 65535 = 255 · 257, so the PSNR is unchanged. Data with 12 significant bits stored in 16-bit words gives a 24 dB higher PSNR if $P = 65535$ is used instead of $P = 4095$, which is a common source of wrong comparisons.
- **Not a signal-to-noise ratio.** $10\log_{10}(\sum x_i^2/\sum (x_i - y_i)^2)$ divides by the energy of the signal and so depends on the content; PSNR uses the fixed peak and does not.
- **Not shift invariant.** Moving the whole image by one pixel can lower PSNR by many decibels, although the content is the same. PSNR assumes that the images are aligned.

## Related definitions

PSNR is a log form of the [mean squared error](/mean-squared-error/), the most used full-reference measure of [image quality assessment](/image-quality-assessment/). [SSIM](/structural-similarity-index/) compares local means, variances and covariance instead and often follows the judgment of viewers better; Huynh-Thu and Ghanbari show that PSNR follows viewer scores well only when the content and the kind of distortion are fixed. In [lossy image compression](/lossy-image-compression/), PSNR against the bit rate is the usual rate-distortion curve, and the error of [scalar quantization](/scalar-quantization/) with step $\Delta$ gives MSE $\Delta^2/12$. In [image denoising](/image-denoising/), PSNR against the clean image is the standard score. For color images, PSNR is reported either over all RGB channels, as above, or on the luma channel $Y'$ of a [color space](/color-spaces/) only; the two give different numbers.

## References
