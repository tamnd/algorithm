---
tag: 8KJPQ2
kind: problem
slug: image-denoising
name: Image denoising
aliases:
- noise removal
area: graphics-and-signals/image-processing
level: advanced
summary: Recover the clean image from a noisy observation.
prereqs: [digital-image, image-noise, mean-squared-error]
see_also: [total-variation-denoising, non-local-means, median-filter, bilateral-filter, image-smoothing, signal-denoising, image-deblurring, image-quality-assessment]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: the chapter on image restoration and reconstruction (noise models, and restoration by spatial filtering when noise is the only degradation)
  - paper: doi:10.1016/0167-2789(92)90242-F
    title: Leonid I. Rudin, Stanley Osher and Emad Fatemi, Nonlinear total variation based noise removal algorithms, Physica D 60:259-268, 1992
    locator: the total variation model for noise removal
  - paper: doi:10.1093/biomet/81.3.425
    title: David L. Donoho and Iain M. Johnstone, Ideal spatial adaptation by wavelet shrinkage, Biometrika 81(3):425-455, 1994
    locator: wavelet shrinkage and its risk compared with an oracle
  - paper: doi:10.1109/CVPR.2005.38
    title: Antoni Buades, Bartomeu Coll and Jean-Michel Morel, A non-local algorithm for image denoising, IEEE Conference on Computer Vision and Pattern Recognition, 2005, volume 2, pages 60-65
    locator: the method noise, and non-local means
---

Image denoising is the problem of estimating a clean image $u$ from an observation $f$ that is $u$ corrupted by random noise, such as $f = u + n$ with independent Gaussian noise $n$ at each pixel. Noise and fine detail both make the image vary from pixel to pixel, so every method needs a model of what clean images look like: smooth, piecewise constant, sparse in a wavelet basis, made of repeated patches, or learned from data. A method trades the noise it removes against the detail and edges it loses, and its quality is measured against a known clean image by the [mean squared error](/mean-squared-error/), the PSNR, or the measures of [image quality assessment](/image-quality-assessment/). Without a model there is no answer: the observation itself is the only unbiased estimate of each pixel. Denoising of one-dimensional signals is the separate problem of [signal denoising](/signal-denoising/); the image problem differs in its two-dimensional structure, its edges, and its repeated textures.

## In plain words

A photo taken in low light looks grainy: each pixel is a little too bright or too dark, at random. Denoising tries to get back the photo without the grain. The grain changes from one pixel to the next, but so do real details such as hair or text. So a method has to guess which changes are real. Averaging each pixel with its neighbors removes grain but also blurs edges. Better methods average only with pixels that look alike, keep sharp edges where the image jumps, or use the fact that photos contain many similar small pieces. No method can be best for every photo, because what counts as a real detail depends on what photos are expected to look like.

## Definition

A gray [digital image](/digital-image/) is an array $u$ of $W \times H$ values. An observation model gives the distribution of the observed image $f$ given $u$. The common models, described on the [image noise](/image-noise/) page, are:

- additive white Gaussian noise, $f = u + n$ with $n$ independent at each pixel, of mean 0 and variance $\sigma^2$;
- Poisson noise, $f(x) \sim \operatorname{Poisson}(u(x))$, for photon counts;
- impulse (salt-and-pepper) noise, where each pixel is replaced with a small probability by the darkest or brightest value;
- multiplicative noise, $f = u \cdot n$, as speckle in radar and ultrasound images.

The problem is to compute an estimate $\hat u = D(f)$ that is close to $u$. The usual criteria are the mean squared error $\frac{1}{WH} \sum_x (\hat u(x) - u(x))^2$ and the peak signal-to-noise ratio $10 \log_{10}(M^2 / \text{MSE})$ for values in $[0, M]$, averaged over test images. These criteria need a clean reference, so they compare methods but cannot be computed on a real noisy photo. Bayesian formulations add a prior distribution on $u$: the posterior mean minimizes the expected squared error, and the posterior mode is the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/), which is the minimizer of a data term plus a regularizer, as in [total variation denoising](/total-variation-denoising/).

## Variants

- Known or unknown noise level: most methods need $\sigma$, and blind denoising estimates it from the image first.
- Signal-dependent noise, such as Poisson noise and the mixed Poisson and Gaussian noise of camera sensors; a variance-stabilizing transform can turn it into nearly Gaussian noise of constant variance.
- Color images, where the noise of the channels can be correlated and a change of color space helps.
- Video and bursts of photos, where several frames of the same scene give more samples per point after alignment.
- Denoising combined with other tasks, such as [deblurring](/image-deblurring/), demosaicing and [inpainting](/image-inpainting/), all inverse problems of the same form.

## Examples

Take a $16 \times 16$ image that is 0 on the left half and 1 on the right half, and add Gaussian noise with $\sigma = 0.2$ from Python's `random.Random(7)`. A $3 \times 3$ mean, a $3 \times 3$ median, both with clamp-to-edge borders, and [total variation denoising](/total-variation-denoising/) with $\lambda = 0.2$ give these mean squared errors against the clean image:

| | noisy | $3 \times 3$ mean | $3 \times 3$ median | total variation |
|---|---|---|---|---|
| Gaussian noise, $\sigma = 0.2$ | 0.0409 | 0.0191 | 0.0130 | 0.00277 |
| impulse noise | 0.04688 | 0.02556 | 0.00781 | 0.01143 |

The second row uses the same clean image with impulse noise: with `random.Random(8)`, each pixel is set with probability 0.1 to 0 or 1 at random, which changes 12 of the 256 pixels. The mean spreads each impulse over its neighbors and blurs the edge. The [median filter](/median-filter/) removes isolated impulses and keeps the straight edge, so it wins on impulse noise. Total variation fits this piecewise constant image best under Gaussian noise. On a textured photo the ranking can change, which is why no single method is best.

## Known algorithms

- Linear smoothing: the [box blur](/box-blur/) and the [Gaussian filter](/gaussian-filter/) average neighbors. They are fast and optimal for some smooth image models, but they blur edges. The [Wiener filter](/wiener-filter/) chooses the linear filter of least expected squared error from the power spectra of the image and the noise.
- Order statistics: the [median filter](/median-filter/) for impulse noise.
- Edge-preserving local filters: the [bilateral filter](/bilateral-filter/), the [guided filter](/guided-filter/), and [anisotropic diffusion](/anisotropic-diffusion/), which average less across strong differences.
- Variational methods: [total variation denoising](/total-variation-denoising/), the ROF model, which keeps edges but turns smooth slopes into flat steps.
- Transform shrinkage: transform the image into wavelets with the [discrete wavelet transform](/discrete-wavelet-transform/), shrink the small coefficients toward 0, and transform back. Donoho and Johnstone showed that soft thresholding comes close to an oracle that knows which coefficients to keep.
- Patch methods: [non-local means](/non-local-means/) averages pixels whose surrounding patches are similar, anywhere in the image; BM3D, by Dabov, Foi, Katkovnik and Egiazarian, groups similar patches into stacks and filters each stack in a transform domain.
- Learned methods: neural networks trained on pairs of clean and noisy images give the best results on standard test sets, at a high cost in training and computation.

## Bounds

- Without a prior there is no gain: for Gaussian noise, $\hat u = f$ is the unbiased estimate of least variance for each pixel taken alone, with error $\sigma^2$. Every method that does better uses assumptions about $u$, and fails on images that break them.
- For a given prior, the posterior mean is the estimate of least expected squared error, so it is a lower bound for every method under that prior; for natural images the prior is not known exactly, and studies estimate such bounds from large sets of patches.
- Removing noise also removes some signal: for a linear filter, the error is the sum of the squared bias, which grows with the smoothing, and the noise variance that remains, which falls with it.
- Running time: the local filters take $O(WH)$ time for a fixed window, non-local means $O(WH s^2 p^2)$ for a search window of side $s$ and patches of side $p$, and iterative variational methods $O(WH)$ per iteration.

## Reductions

- A $3 \times 3$ mean, a Gaussian filter or a Wiener filter is a [linear filtering](/linear-filtering/) step, a [discrete convolution](/discrete-convolution/).
- Total variation and other regularized methods are convex optimization problems, solved by methods such as the [proximal gradient method](/proximal-gradient-method/) and [FISTA](/fista/).
- Wavelet shrinkage is the proximal step of the $\ell_1$ norm in an orthonormal basis, the step of the [iterative shrinkage-thresholding algorithm](/iterative-shrinkage-thresholding/).
- Denoising is a building block of other inverse problems: "plug-and-play" methods solve [deblurring](/image-deblurring/), [super-resolution](/super-resolution/) and [inpainting](/image-inpainting/) by alternating a data step with a call to a denoiser.

## Applications

- Photos taken in low light and with small camera sensors, where each image of a burst is noisy.
- Medical images: low-dose CT, MRI, ultrasound speckle.
- Astronomy and microscopy, with Poisson photon noise.
- Scanned documents and old films.
- A step before edge detection, segmentation or compression, which all work worse on noisy input.

## References
