---
tag: 09YP53
kind: algorithm
slug: richardson-lucy-deconvolution
name: Richardson-Lucy deconvolution
aliases:
- Lucy-Richardson deconvolution
area: graphics-and-signals/image-processing
level: advanced
summary: Deblur an image with a known PSF by a multiplicative update that is EM for Poisson counts, keeps values nonnegative and, for a normalized PSF with a periodic border, keeps the total flux.
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, K: the number of PSF entries, n: the number of iterations}
  time: {worst: Θ(n W H K), average: Θ(n W H K), best: Θ(n W H K)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, iterative: true, nonnegative: true, flux_preserving: true, monotone_likelihood: true, needs_early_stopping: true}
history:
  year: 1972
  people: [William Hadley Richardson, Leon B. Lucy, Lawrence A. Shepp, Yehuda Vardi]
  note: Richardson (1972) and Lucy (1974) derived the iteration from Bayes' rule; Shepp and Vardi (1982) showed that the same update is the EM algorithm for Poisson data.
prereqs: [point-spread-function, convolution, poisson-distribution, expectation-maximization]
see_also: [image-deblurring, wiener-filter, tikhonov-regularization, maximum-likelihood-estimation, jensens-inequality, total-variation-denoising, fast-fourier-transform, image-noise]
sources:
  - paper: doi:10.1364/JOSA.62.000055
    title: William Hadley Richardson, Bayesian-based iterative method of image restoration, Journal of the Optical Society of America 62(1), 1972
    locator: pages 55 to 59
  - paper: doi:10.1086/111605
    title: Leon B. Lucy, An iterative technique for the rectification of observed distributions, The Astronomical Journal 79(6), 1974
    locator: pages 745 to 754
  - paper: doi:10.1109/TMI.1982.4307558
    title: Lawrence A. Shepp and Yehuda Vardi, Maximum likelihood reconstruction for emission tomography, IEEE Transactions on Medical Imaging 1(2), 1982
    locator: pages 113 to 122 (the EM derivation of the multiplicative update for Poisson data)
  - paper: doi:10.1080/01621459.1985.10477119
    title: Yehuda Vardi, Lawrence A. Shepp and Linda Kaufman, A statistical model for positron emission tomography, Journal of the American Statistical Association 80(389), 1985
    locator: pages 8 to 20 (the model and the convergence of the EM iteration)
---

Richardson-Lucy deconvolution is an iterative method for [image deblurring](/image-deblurring/) when the [point spread function](/point-spread-function/) $p$ is known and the noise is Poisson, as in photon counts from a telescope, a microscope or a camera in low light. From the observed image $d$ it repeats the update $u \leftarrow u \cdot \big(\tilde p \star (d / (p \ast u))\big)$: blur the estimate, divide the data by it, spread the ratio back with the mirrored PSF, and multiply. William Richardson (1972) and Leon Lucy (1974) found it from Bayes' rule, and Shepp and Vardi (1982) showed that it is the [expectation-maximization](/expectation-maximization/) algorithm for the Poisson likelihood. So the likelihood never goes down, the estimate stays nonnegative, and for a normalized PSF with a periodic border the total of the image stays equal to the total of the data. It is not a regularized method: run long enough, it fits the noise, so the number of iterations acts as the regularization parameter. One iteration costs $\Theta(WHK)$ directly for a $W \times H$ image and a PSF with $K$ entries, or $O(WH \log(WH))$ with the [FFT](/fast-fourier-transform/).

## In plain words

A blurred photo is the sharp photo with the light of each point smeared over its neighbors in a known pattern. Richardson-Lucy starts from a flat gray guess. It blurs the guess in the same way the camera blurred the scene and compares the result with the real photo, pixel by pixel, as a ratio. Where the blurred guess is too dark, the ratio is above one, and where it is too bright, below one. Each pixel of the guess is then multiplied by an average of the ratios of the pixels that its light reached. Brightness is never subtracted, so no pixel becomes negative, and the total light stays the same. Each round fits the photo better. After many rounds it starts to fit the grain of the noise too, so you stop early.

## The problem

The unknown is a $W \times H$ image $u \ge 0$ of linear intensities, for example expected photon counts; gamma encoded values break the model, because the blur adds light linearly. One channel is used, and a color image is handled per channel. Pixel centers are at integer coordinates, and each pixel is a point sample of the intensity. The PSF $p$ is a small array of $K$ entries with $p \ge 0$ and $\sum p = 1$, centered at its middle entry. The blur is circular convolution,

$$b(x) = (p \ast u)(x) = \sum_{t} p(t)\, u(x - t),$$

with indices taken modulo $W$ and $H$; this periodic border is the one rule under which every pixel of $u$ spreads all of its light into the image. The data $d$ are counts, independent and Poisson with mean $b_{\text{true}} = p \ast u_{\text{true}}$ (see [Poisson distribution](/poisson-distribution/) and [image noise](/image-noise/)). Richardson-Lucy looks for the [maximum likelihood](/maximum-likelihood-estimation/) estimate: up to a constant that does not depend on $u$, the log likelihood is

$$L(u) = \sum_x \big(d(x) \log b(x) - b(x)\big), \qquad b = p \ast u,$$

with $0 \log 0 = 0$, to be maximized over $u \ge 0$. The output is the estimate after $n$ iterations, not the exact maximizer.

## The algorithm

```pseudo id=main
RICHARDSON-LUCY(d, p, n, u₀)                   ▷ d ≥ 0, p ≥ 0, Σp = 1, u₀ > 0
L1  u ← u₀                                      ▷ default: the constant Σd / (WH)
L2  repeat n times
L3      b ← p ∗ u                               ▷ circular convolution: predicted data
L4      for each pixel x: r(x) ← d(x) / b(x) if d(x) > 0, else 0
L5      c ← p̃ ∗ r                               ▷ correlation: c(y) = Σₓ p(x − y) r(x)
L6      u ← u · c                               ▷ pixel by pixel
L7  return u
```

Line L3 predicts the data from the current estimate. Line L4 forms the ratio of the data to the prediction. Line L5 applies the adjoint of the blur, which is correlation with $p$, or convolution with the mirrored PSF $\tilde p(t) = p(-t)$. Line L6 multiplies. Where the prediction is right, $r = 1$ on all the pixels that a source pixel reaches, so $c = \sum p = 1$ and the pixel does not change.

In matrix form, with $A$ the blur matrix, $A_{xy} = p(x - y)$, the update is $u_y \leftarrow u_y \sum_x A_{xy}\, d_x / (Au)_x$. For a general nonnegative $A$, as with a zero border or a PSF that changes over the image, the EM update divides by the column sum: $u_y \leftarrow (u_y / s_y) \sum_x A_{xy}\, d_x / (Au)_x$ with $s_y = \sum_x A_{xy}$. Under the periodic border every $s_y$ is 1.

## Example

Take one row, $W = 6$ and $H = 1$, the PSF $(1/4, 1/2, 1/4)$ with a periodic border, and a true image with all its light in one pixel, $u_{\text{true}} = (0, 0, 8, 0, 0, 0)$. Without noise the data are $d = p \ast u_{\text{true}} = (0, 2, 4, 2, 0, 0)$, with total 8. Start from the mean, $u_0 = 4/3$ at every pixel. In exact arithmetic:

| iteration | estimate $u$ | $L(u)$ | total |
|---|---|---|---|
| 0 | $(4/3, 4/3, 4/3, 4/3, 4/3, 4/3)$ | $-5.6985$ | 8 |
| 1 | $(1/2, 2, 3, 2, 1/2, 0)$ | $-1.8204$ | 8 |
| 2 | $(2/15, 28/15, 4, 28/15, 2/15, 0)$ | $-0.9901$ | 8 |
| 3 | $(2/59, 1029/649, 3090/649, 1029/649, 2/59, 0)$ | $-0.6253$ | 8 |

Step 1 in detail: line L3 gives $b = 4/3$ everywhere, line L4 gives $r = (0, 3/2, 3, 3/2, 0, 0)$, and line L5 gives, at pixel 2, $c = \frac14 \cdot \frac32 + \frac12 \cdot 3 + \frac14 \cdot \frac32 = \frac94$, so $u(2) = \frac43 \cdot \frac94 = 3$. At pixel 5 the three ratios it reaches are all 0, so $u(5) = 0$, and it stays 0 from then on. The total is 8 at each step and the likelihood rises toward its largest value $12 \ln 2 - 8 \approx 0.3178$, reached at $u_{\text{true}}$. In floating point, iteration 10 gives $(0, 0.2863, 7.4274, 0.2863, 0, 0)$, and after 50 iterations the estimate equals $u_{\text{true}}$ to four decimals.

With noise the picture changes. Take a row of 64 samples with value 40 on samples 20 to 27, a spike of 120 at sample 40, a ramp $10, 15, \ldots, 45$ on samples 48 to 55 and 0 elsewhere; blur it with a 9-tap Gaussian of standard deviation 1.5, normalized; and draw Poisson counts with Python's `random.Random(2024)`. The root mean square error of the estimate against the true row, and the log likelihood, are:

| iterations | 1 | 10 | 50 | 100 | 500 | 2000 |
|---|---|---|---|---|---|---|
| RMS error | 14.446 | 9.735 | 6.177 | 7.137 | 14.519 | 17.218 |
| $L(u)$ | 1430.959 | 1491.421 | 1496.034 | 1496.590 | 1497.213 | 1497.303 |

The noisy data themselves have an RMS error of 12.264. The likelihood rises at every step, but the error is least near 50 iterations and then grows, because the estimate starts to fit the noise.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Write $A_{xy} = p(x - y)$, so each column of $A$ sums to 1. The proof shows four facts for an iterate $u \ge 0$ with $b = Au > 0$ wherever $d > 0$.

- **Well defined.** The next iterate again has $b > 0$ wherever $d > 0$, so line L4 never divides by zero if $u_0 > 0$.
- **Nonnegative.** Every factor in lines L3 to L6 is nonnegative.
- **Flux.** $\sum_y u_y^{+} = \sum_x r_x (Au)_x = \sum_{x : d_x > 0} d_x = \sum_x d_x$.
- **Likelihood.** $L(u^{+}) \ge L(u)$. By [Jensen's inequality](/jensens-inequality/) for the logarithm, with the weights $w_{xy} = A_{xy} u_y / b_x$, the function $L$ is bounded below by a separable concave function $Q$ that touches $L$ at $u$, and the maximizer of $Q$ is exactly the update of line L6. This is the E step and the M step of EM for the complete data "counts from source pixel $y$ seen at detector pixel $x$".

The likelihood is concave in $u$, so a limit of the iteration is a maximum likelihood estimate; Vardi, Shepp and Kaufman (1985) treat the convergence. In the noisy case the maximizer itself is bad, as the second example shows.

## Complexity

- Lines L3 and L5 are a convolution and a correlation with a PSF of $K$ entries: $\Theta(WHK)$ each, directly.
- Lines L4 and L6 are $\Theta(WH)$.

One iteration costs $\Theta(WHK)$, and $n$ iterations $\Theta(nWHK)$, the same in every case. The extra space is $\Theta(WH)$ for $b$, $r$ and $c$. With the [FFT](/fast-fourier-transform/), the transform of $p$ is computed once, and each iteration costs $O(WH \log(WH))$, which is better once $K$ is larger than about $\log(WH)$. For a PSF that is a product of a row and a column, a separable pass costs $\Theta(WH\sqrt{K})$ per convolution for a square PSF.

The number of iterations needed is not bounded by a formula. In practice it is tens to hundreds, and it grows as the PSF gets wider, because the iteration recovers high frequencies slowly.

## Properties

- **Nonnegative.** Every iterate is $\ge 0$. A linear filter such as the [Wiener filter](/wiener-filter/) can give negative values and ringing next to a bright point.
- **Flux preserving.** With a normalized PSF and a periodic border, $\sum u = \sum d$ after every step, and exactly so in exact arithmetic. With other borders it is the total of the predicted image, $\sum_x (Au)_x$, that equals $\sum d$, if the update divides by the column sums.
- **Monotone likelihood.** The Poisson log likelihood does not go down from one step to the next.
- **Zeros stay zero.** A pixel with $u = 0$ never becomes positive. This is why $u_0$ must be positive everywhere, and why the support of the estimate can only shrink.
- **Fixed point at an exact fit.** If $d = p \ast u$ with no noise, then $u$ is a fixed point.
- **Not regularized.** The maximum likelihood estimate fits the noise, so the iterates first improve and then get worse. The output depends on $n$.
- **Linear in scale.** Multiplying $d$ and $u_0$ by a constant multiplies every iterate by it.

## Variants and improvements

- **Early stopping.** Stop when the residual $d - p \ast u$ looks like Poisson noise, for example when $\sum_x (d_x - b_x)^2 / b_x$ reaches the number of pixels, or by cross-validation over split data.
- **Damped and regularized forms.** Add a penalty to the likelihood, such as total variation (see [total variation denoising](/total-variation-denoising/)) or a Tikhonov term (see [Tikhonov regularization](/tikhonov-regularization/)), and solve the penalized problem with a modified multiplicative step. A common form divides the update of line L6 by $1 + \lambda g$, where $g$ is the gradient of the penalty at $u$; this needs $1 + \lambda g > 0$, which limits $\lambda$, and the monotone likelihood is then no longer guaranteed.
- **Background and read noise.** With a known background $\beta$, use $b = p \ast u + \beta$ at line L3. With Gaussian read noise added, a shifted Poisson model is a common approximation.
- **Acceleration.** Extrapolate along the last steps, or use ordered subsets of the data, as in emission tomography. These save iterations but can lose the monotone likelihood.
- **Blind deconvolution.** Alternate Richardson-Lucy steps in $u$ with Richardson-Lucy steps in $p$, which is the same update with the roles of image and PSF swapped. This does not have the guarantees of the known-PSF case.
- **Spatially varying PSF.** Use the matrix form with the column-sum division; only the cost changes.

## When to use it

Use Richardson-Lucy for counts: astronomy, fluorescence microscopy, low-light imaging, and emission tomography, where the data are nonnegative and Poisson, the PSF is measured, and the result should stay nonnegative with the right total light. Do not use it when the PSF is unknown or wrong, because the error in $p$ turns into ringing and false structure. When the noise is Gaussian and stationary, a [Wiener filter](/wiener-filter/) or [Tikhonov](/tikhonov-regularization/) solve is faster, needs no stopping rule, and is the better match to that noise model. For strong noise, add a regularizer instead of relying on the stopping point alone.

## Pitfalls

- **Running to convergence.** The maximum likelihood estimate of a noisy image is a field of sharp spikes. The second example shows the error growing from 6.177 at 50 iterations to 17.218 at 2000 while the likelihood keeps rising.
- **A start with zeros.** A zero in $u_0$ stays zero, and if $d > 0$ there and all around, line L4 divides by zero. Start from a positive constant such as the mean of $d$.
- **Gamma encoded data.** Applying the update to sRGB values instead of linear intensities breaks the blur model and the Poisson model.
- **Unnormalized PSF.** If $\sum p \neq 1$, the estimate is scaled by $1 / \sum p$ and the flux property is lost. Normalize $p$ first.
- **Zero padding without the column sums.** With a zero border, the pixels near the edge send part of their light out of the image. Without the division by $s_y$, the update is not EM, and the estimate near the border is wrong.
- **Wrong PSF center or orientation.** Convolving at line L5 instead of correlating, or using a PSF whose center is off by one sample, shifts the result or makes it blurry. For an asymmetric PSF, line L5 must use the mirror of the PSF of line L3.
- **Division by tiny numbers.** In floating point, $b$ can underflow where $u$ is almost zero. Add a small floor to $b$, or use the convention of line L4, which skips pixels with $d = 0$.

## Implementations

## History

William Hadley Richardson published the iteration in 1972 for the restoration of images, deriving it from Bayes' theorem by treating the image and the data as distributions. Leon Lucy derived the same method in 1974 for the rectification of astronomical distributions and studied its convergence on examples. In 1982 Lawrence Shepp and Yehuda Vardi showed that for Poisson data the expectation-maximization algorithm gives this multiplicative update, as part of their work on emission tomography, where it is called ML-EM; Vardi, Shepp and Kaufman gave the statistical model and the convergence in 1985. The method became the standard deconvolution step for the images of the Hubble Space Telescope before its optics were corrected in 1993, and it is still standard in fluorescence microscopy.

## References
