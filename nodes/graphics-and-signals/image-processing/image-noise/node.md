---
tag: NRJXEJ
kind: concept
slug: image-noise
name: Image noise
aliases:
- salt-and-pepper noise
- Gaussian noise
- speckle
- impulse noise
- shot noise
area: graphics-and-signals/image-processing
level: intro
summary: Random errors in pixel values and their standard models, additive Gaussian, Poisson shot noise, salt-and-pepper impulses, multiplicative speckle and quantization, with how to estimate them.
prereqs: [digital-image, variance, poisson-distribution]
see_also: [image-denoising, median-filter, gaussian-filter, wiener-filter, non-local-means, total-variation-denoising, psnr, scalar-quantization]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 5.2, Noise Models, from page 366 (Gaussian, page 367; Rayleigh, page 368; Erlang and exponential, page 369; uniform, page 369; salt-and-pepper, page 370; periodic noise, page 372; estimating noise parameters, page 373)
  - paper: doi:10.1109/TIP.2008.2001399
    title: Alessandro Foi, Mejdi Trimeche, Vladimir Katkovnik and Karen Egiazarian, Practical Poissonian-Gaussian noise modeling and fitting for single-image raw-data, IEEE Transactions on Image Processing 17(10), 2008
    locator: pages 1737 to 1754 (the Poisson and Gaussian model of raw sensor data, with a variance that is an affine function of the signal, and its fit from one image)
  - paper: doi:10.1093/biomet/35.3-4.246
    title: F. J. Anscombe, The transformation of Poisson, binomial and negative-binomial data, Biometrika 35(3-4), 1948
    locator: pages 246 to 254 (the square root transform with the constant 3/8 that makes the variance of Poisson data nearly constant)
---

Image noise is the random part of the pixel values: the difference between the image that was recorded and the image that an ideal, noiseless device would have made of the same scene. Models of noise describe this difference with a few parameters, so that methods can be designed and tested against it: additive Gaussian noise with a standard deviation $\sigma$, Poisson shot noise whose variance equals the mean photon count, salt-and-pepper impulses that set a fraction $p$ of pixels to black or white, multiplicative speckle, and the rounding error of quantization. Each model has its matching removal method; this page covers the models and their estimation, and [image denoising](/image-denoising/) covers the removal.

## In plain words

Take two photos of the same still scene with the same camera, and the pixel values still differ a little. Light arrives as single photons, and the number that hits each sensor cell in a short time varies by chance. The electronics add their own small errors, and rounding to whole numbers adds a little more. This random variation is noise. In a dark photo it shows as grain, because there are few photons and the chance part is large next to the signal. A broken sensor cell or a transmission error gives a different kind, single white or black dots. Radar and ultrasound images have a grainy pattern that scales with the brightness. Knowing which kind of noise is in an image tells you which tool removes it best.

## The idea

**The model.** On this page an image is one channel. $f(x, y)$ is the noiseless image and $g(x, y)$ the recorded one, both either real values or integer codes in $\{0, \ldots, L-1\}$. Physical models, such as shot noise, act on the linear sensor values; synthetic tests usually add noise to the stored codes, which for 8-bit images are gamma encoded (see [gamma correction](/gamma-correction/)). Unless stated, the noise at different pixels is independent and has the same distribution, so pixel positions and borders do not matter.

**Additive Gaussian noise.** $g = f + n$ with $n \sim \mathcal{N}(0, \sigma^2)$ independent of $f$. It models the electronic and thermal noise of a sensor, and it is the standard test model, because many denoising methods are optimal or nearly optimal for it. The [mean squared error](/mean-squared-error/) of $g$ against $f$ has the expected value $\sigma^2$, so with peak 255 the expected [PSNR](/psnr/) is $10\log_{10}(255^2/\sigma^2)$, 28.13 dB for $\sigma = 10$. When $g$ is stored as integer codes, it is rounded and clipped to $[0, L-1]$, and both steps change the noise near black and white.

**Poisson shot noise.** If a pixel collects photons at the mean rate $\lambda$, the count is a [Poisson](/poisson-distribution/) random variable with mean and [variance](/variance/) both $\lambda$. So the noise depends on the signal: the standard deviation is $\sqrt\lambda$, and the signal-to-noise ratio $\lambda/\sqrt\lambda = \sqrt\lambda$ grows with the light. Real raw data is close to a Poisson part plus a Gaussian part, which Foi and coauthors model as a variance $a f + b$ that is an affine function of the signal. Anscombe's transform $2\sqrt{g + 3/8}$ makes the variance of Poisson data nearly 1 when the counts are not small, so that a method for Gaussian noise can be applied and the result transformed back.

**Salt-and-pepper (impulse) noise.** Each pixel is, independently, set to $L - 1$ with probability $p_s$, to 0 with probability $p_p$, and kept otherwise. It models dead or stuck sensor cells and bit errors in transmission. Since the bad pixels carry no information about $f$, a mean filter only spreads them; the [median filter](/median-filter/) removes them, because an impulse is an outlier in its window.

**Speckle.** $g = f\,(1 + n)$ or $g = f \cdot n$ with $n$ of mean 1: the noise is multiplicative, so bright regions have stronger noise. It comes from the interference of coherent waves in synthetic aperture radar, ultrasound and laser images. A log transform turns it into additive noise.

**Quantization noise.** Rounding to a step $\Delta$ adds an error in $[-\Delta/2, \Delta/2)$, which for a busy signal behaves like uniform noise with variance $\Delta^2/12$ (see [scalar quantization](/scalar-quantization/)). For 8-bit codes, $\Delta = 1$ gives an MSE of $1/12$, about 58.9 dB of PSNR. It is not independent of $f$ in smooth gradients, where it shows as bands instead of grain.

**Other models.** Gonzalez and Woods also list the Rayleigh, Erlang (gamma), exponential and uniform densities, and periodic noise from electrical interference, which appears as bright spikes in the Fourier spectrum and is removed in the frequency domain.

**Estimating the noise.** In a region where $f$ is constant, the histogram of $g$ is the noise distribution shifted by $f$, so its mean and variance estimate the parameters; Gonzalez and Woods use such a flat patch. Without a flat patch, the differences $g(x+1, y) - g(x, y)$ remove most of a smooth $f$ and have the variance $2\sigma^2$ for independent Gaussian noise. A robust estimate uses the median absolute deviation: for Gaussian data, $\sigma \approx \operatorname{MAD}/0.6745$, which is not moved much by edges. For signal-dependent noise, the variance is estimated as a function of the local mean.

## Examples

- **Salt-and-pepper on a gray image.** On a $64 \times 64$ image of constant gray 128, set each pixel with probability 0.05 to 0 or 255 with equal chance, using `random.Random(5)`: draw a uniform number for the pixel, and if it is below 0.05, draw a second one and use 0 if it is below 0.5, else 255. The expected MSE is $0.05 \cdot (128^2 + 127^2)/2 = 812.825$; the measured MSE was 801.77, 1.4 percent lower. The number of changed pixels is binomial with mean 204.8 and standard deviation about 13.9, so the MSE of one draw varies by about 7 percent around the expectation.
- **Gaussian noise with clipping.** On the same gray image, $g = \operatorname{round}(128 + n)$ with $n \sim \mathcal{N}(0, 10^2)$ from `random.Random(6)`, clipped to $[0, 255]$, gave MSE 101.05 and PSNR 28.09 dB, near the expected values of about 100.08 (with the rounding term $1/12$) and 28.13 dB. Clipping did not matter here, because 128 is far from both ends. [SSIM](/structural-similarity-index/) of the same pair is only 0.3836, because the reference is flat.
- **Shot noise in the dark.** A pixel with a mean of 4 photons has a standard deviation of 2, half the signal. A pixel with 10,000 photons has a standard deviation of 100, one percent of the signal. This is why dark images look grainier.
- **Anscombe's transform.** For a Poisson count with mean 100, $2\sqrt{g + 3/8}$ changes by about $1/\sqrt{100} = 0.1$ per unit of $g$, and the standard deviation of $g$ is 10, so the transformed standard deviation is about 1. For a mean of 10,000 it is also about 1.

## Where it is used

Noise models are the basis of [image denoising](/image-denoising/): the [Gaussian filter](/gaussian-filter/), the [Wiener filter](/wiener-filter/), [non-local means](/non-local-means/) and [total variation denoising](/total-variation-denoising/) assume additive, mostly Gaussian noise, and the [median filter](/median-filter/) targets impulses. Benchmarks add Gaussian noise of known $\sigma$ to clean images and report [PSNR](/psnr/) and [SSIM](/structural-similarity-index/) of the results. Camera pipelines estimate the Poisson and Gaussian parameters of each sensor to set the strength of denoising and sharpening. [Image restoration](/image-deblurring/) methods, such as Wiener deconvolution, need the noise power. In [edge detection](/edge-detection/), the noise level sets the smoothing scale and the thresholds.

## References
