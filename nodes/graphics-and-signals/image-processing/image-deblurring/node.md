---
tag: 82TQZW
kind: problem
slug: image-deblurring
name: Image deblurring
aliases:
- image deconvolution
- blind deconvolution
area: graphics-and-signals/image-processing
level: advanced
summary: Recover a sharp image given a blur kernel, or estimate both image and kernel.
prereqs: [point-spread-function, discrete-convolution, convolution-theorem, image-noise]
see_also: [richardson-lucy-deconvolution, wiener-filter, tikhonov-regularization, total-variation-denoising, image-denoising, image-sharpening, condition-number, super-resolution]
sources:
  - book: isbn:9780898716184
    title: Per Christian Hansen, James G. Nagy and Dianne P. O'Leary, Deblurring Images, Matrices, Spectra, and Filtering, SIAM, 2006
    locator: the chapters on the blurring model and boundary conditions, structured matrices and the FFT, spectral filtering (truncated SVD and Tikhonov), and choice of the regularization parameter
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: the chapter on image restoration and reconstruction (inverse filtering, minimum mean square error filtering, constrained least squares filtering)
  - paper: doi:10.1145/1179352.1141956
    title: Rob Fergus, Barun Singh, Aaron Hertzmann, Sam T. Roweis and William T. Freeman, Removing camera shake from a single photograph, ACM SIGGRAPH 2006 Papers, pages 787-794
    locator: blind estimation of a camera shake kernel with a prior on image gradients
---

Image deblurring is the problem of recovering a sharp image $u$ from a blurred and noisy observation $f = k * u + n$, where $k$ is the [point spread function](/point-spread-function/) of the blur, $*$ is convolution and $n$ is noise. When $k$ is known the problem is called deconvolution, and when $k$ must be estimated as well it is blind deconvolution. Blur is a low-pass filter: by the [convolution theorem](/convolution-theorem/) it multiplies each frequency of the image by the transfer function $\hat k$, which is small or zero at high frequencies. Dividing by $\hat k$, the inverse filter, undoes the blur exactly when there is no noise, but it multiplies the noise at those frequencies by $1/|\hat k|$, which can be thousands. So the problem is ill posed, and every practical method regularizes: it gives up some sharpness to keep the noise bounded, with [Tikhonov regularization](/tikhonov-regularization/), the [Wiener filter](/wiener-filter/), a total variation prior, or the early stopping of an iteration such as [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/).

## In plain words

A photo is blurred when the camera shook, the lens was out of focus, or the air moved. Each point of the scene was spread into a small smudge, and the smudges of nearby points overlap. Deblurring tries to undo that spreading. If the shape of the smudge is known, a computer can work backward exactly, but only in a perfect world. Real photos also have a little grain, and working backward turns that grain into huge stripes and speckles, because the finest details were almost erased by the blur and must be boosted a lot to come back. So good methods boost the fine details only as far as the grain allows. If the shape of the smudge is unknown, it has to be guessed from the photo too, which is much harder.

## Definition

The model is $f = Ku + n$, where $u$ is the unknown image, $f$ the observation, $n$ noise, and $K$ the linear blur operator. For a blur that is the same everywhere, $K u = k * u$ is a [discrete convolution](/discrete-convolution/) with the point spread function $k$, with a rule for the pixels outside the image: zero, periodic, reflected or clamped. With periodic borders, $K$ is diagonal in the [discrete Fourier transform](/discrete-fourier-transform/): $\widehat{Ku}(\omega) = \hat k(\omega)\, \hat u(\omega)$.

- Non-blind deconvolution: given $f$ and $k$, find $u$.
- Blind deconvolution: given $f$, find both $u$ and $k$, usually with $k \ge 0$ and $\sum k = 1$.

The problem is ill posed in the sense of Hadamard. If $\hat k(\omega) = 0$ at some frequency, $K$ has a null space and the data say nothing about $\hat u(\omega)$. If $\hat k$ is only small, $K$ is invertible but its [condition number](/condition-number/) $\max|\hat k| / \min|\hat k|$ is large, so a small error in $f$ makes a large error in $K^{-1} f$. A regularized method computes, for example,

$$\hat u = \arg\min_u \; \lVert Ku - f\rVert_2^2 + \alpha\, R(u),$$

with $R(u) = \lVert u \rVert_2^2$ or $\lVert \nabla u \rVert_2^2$ (Tikhonov), $R(u) = \mathrm{TV}(u)$ (total variation), or the negative log of a prior; under Poisson noise the data term is the Poisson negative log-likelihood.

## Variants

- Uniform blur, the convolution model above; spatially varying blur, where the point spread function changes across the image, as with a rotating camera or depth-dependent defocus.
- Known kernel, kernel from a model (defocus disk, Gaussian, motion along a line), kernel measured from a star or a calibration target, or kernel unknown (blind).
- Gaussian noise or Poisson noise, the second for low-light imaging, astronomy and fluorescence microscopy.
- Several observations with different blurs, which can fill each other's zeros of $\hat k$.
- Three-dimensional deconvolution of microscope image stacks.

## Examples

A blur that erases a pattern. With periodic borders, the three-pixel mean $k = (1/3, 1/3, 1/3)$ on a row of 6 pixels maps the pattern $(1, -\tfrac12, -\tfrac12, 1, -\tfrac12, -\tfrac12)$ to all zeros, because each window of three consecutive values sums to 0. So $u$ and $u$ plus any multiple of this pattern give the same blurred image, and no method can tell them apart from $f$ alone. In Fourier terms, $\hat k(\omega) = \tfrac13 + \tfrac23 \cos \omega$ is zero at $\omega = 2\pi/3$, and the pattern is a cosine at that frequency.

A blur that is invertible but amplifies noise. The kernel $(0.2, 0.6, 0.2)$ on a row of 8 pixels has $|\hat k(2\pi j/8)| = 1, 0.8828, 0.6, 0.3172, 0.2$ for $j = 0, \ldots, 4$, so the inverse filter multiplies noise at the highest frequency by 5.

A measured case. A row of 64 pixels is 1 on pixels 20 to 39 and 0 elsewhere. It is blurred with periodic borders by the normalized 9-tap Gaussian with standard deviation 1.5, and Gaussian noise with $\sigma = 0.01$ from Python's `random.Random(1)` is added. The least $|\hat k|$ is $3.44 \cdot 10^{-4}$, so the inverse filter can multiply noise by up to 2907. The root mean squared error against the sharp row is:

| estimate | blurred, no noise | blurred and noisy | inverse filter | Tikhonov, $\alpha = 10^{-4}$ | $10^{-3}$ | $10^{-2}$ | $10^{-1}$ |
|---|---|---|---|---|---|---|---|
| RMSE | 0.0999 | 0.1013 | 6.089 | 0.1594 | 0.0898 | 0.0750 | 0.1032 |

Here the Tikhonov estimate is $\hat u = \mathcal F^{-1}\big[\overline{\hat k}\, \hat f / (|\hat k|^2 + \alpha)\big]$, the minimizer of $\lVert k * u - f\rVert^2 + \alpha \lVert u\rVert^2$. On the same row without noise the inverse filter is exact up to rounding, with RMSE $2.5 \cdot 10^{-12}$. With noise of size 0.01 it is 60 times worse than doing nothing. A good $\alpha$ beats the blurred data, and a too small or too large $\alpha$ does not.

## Known algorithms

- The inverse filter, $\hat u = \mathcal F^{-1}[\hat f / \hat k]$: exact without noise, useless with noise wherever $|\hat k|$ is small.
- Spectral filtering: truncated SVD, which drops the components with small $|\hat k|$, and [Tikhonov regularization](/tikhonov-regularization/), which damps them. With periodic borders both cost $O(N \log N)$ for $N$ pixels with the [fast Fourier transform](/fast-fourier-transform/).
- The [Wiener filter](/wiener-filter/), the linear filter of least expected squared error given the power spectra of image and noise; it is Tikhonov with a frequency-dependent weight.
- [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/), a multiplicative iteration that keeps the estimate nonnegative and maximizes the Poisson likelihood; it is stopped early, because the noise grows when it runs long.
- Iterative methods for large or spatially varying blur: [conjugate gradient](/conjugate-gradient-method/) on the normal equations (also stopped early), and the Landweber iteration.
- Edge-preserving priors: total variation deconvolution, solved by splitting methods or by the [proximal gradient method](/proximal-gradient-method/) and [FISTA](/fista/), and sparse priors on image gradients.
- Blind methods: alternate between the image and the kernel, or first estimate the kernel from the statistics of image gradients, as Fergus, Singh, Hertzmann, Roweis and Freeman did for camera shake, then deconvolve with the kernel; learned methods train networks on pairs of blurred and sharp images.

## Bounds

- Frequencies where $\hat k = 0$ cannot be recovered from one observation; only a prior can fill them.
- For linear methods with periodic borders, the noise variance in the estimate at frequency $\omega$ is the noise variance times $|g(\omega)|^2$ for the filter $g$; the inverse filter has $|g| = 1/|\hat k|$, so the error grows without bound as $|\hat k| \to 0$.
- Blind deconvolution has trivial solutions: $u = f$ with $k$ a single 1 explains the data exactly, as does any shift of $u$ with the opposite shift of $k$, so blind methods need priors on both $u$ and $k$, and they recover $k$ only up to such ambiguities.
- With FFT-based filtering the cost is $O(N \log N)$; iterative methods cost one or two convolutions per step.

## Reductions

- Deconvolution with periodic borders reduces to $N$ independent scalar problems, one per frequency, by the [discrete Fourier transform](/discrete-fourier-transform/).
- Tikhonov deconvolution is a [least squares problem](/least-squares-problem/) with a penalty, solved through its [normal equations](/normal-equations/) $(K^\top K + \alpha I) u = K^\top f$; the same problem in statistics is [ridge regression](/ridge-regression/).
- With $K = I$, deblurring is [image denoising](/image-denoising/); with $K$ a blur followed by subsampling, it is [super-resolution](/super-resolution/); with $K$ a mask, it is [inpainting](/image-inpainting/).
- Unsharp masking and other [image sharpening](/image-sharpening/) filters are crude one-step approximations of an inverse filter with a fixed gain.

## Applications

- Astronomy, where deconvolution of telescope images with a measured point spread function is a standard step.
- Fluorescence microscopy, with three-dimensional point spread functions and Poisson noise.
- Removing camera shake and defocus from photos.
- Reading license plates and text from blurred images.
- Medical imaging and remote sensing, where the system response is known from calibration.

## References
