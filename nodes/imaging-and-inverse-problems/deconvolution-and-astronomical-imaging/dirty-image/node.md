---
tag: TD62QQ
kind: definition
slug: dirty-image
name: Dirty image
aliases:
- dirty map
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: core
summary: "The inverse Fourier transform of the weighted visibilities, equal to the true sky convolved with the dirty beam set by the uv sampling."
prereqs: [aperture-synthesis, convolution-theorem, point-spread-function]
see_also: [hogbom-clean, cotton-schwab-clean, multiscale-clean, w-projection, van-cittert-zernike-theorem, nonuniform-fft, density-compensation, image-deblurring]
sources:
  - book: isbn:9783319444314
    title: "A. Richard Thompson, James M. Moran and George W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, third edition, Springer, 2017"
    locator: "Chapter 10, Calibration and Imaging, pp. 485 to 549 (the Fourier transformation of the visibility data, the weighting of the samples and the synthesized beam); Chapter 11, Further Imaging Techniques, pp. 551 to 598 (deconvolution of the dirty image)"
  - paper: "J. A. Hogbom, Aperture synthesis with a non-regular distribution of interferometer baselines, Astronomy and Astrophysics Supplement Series 15, 1974"
    locator: "pp. 417 to 426 (the map from incomplete baselines as the sky convolved with the beam of the array, and its deconvolution by CLEAN)"
---

The dirty image is the image that an interferometer gives before any deconvolution: the inverse Fourier transform of the measured visibilities, each with a weight, and with zero at every point of the Fourier plane that was not measured. Because only some Fourier samples are known, it equals the true sky convolved with the dirty beam, the inverse transform of the weighted sampling pattern, plus the transformed noise. [Aperture synthesis](/aperture-synthesis/) is the technique that measures the samples; [Hogbom CLEAN](/hogbom-clean/) and the other deconvolution methods start from the dirty image and the dirty beam and try to remove the beam.

## Definition

Let $(u_k, v_k)$, $k = 1, \dots, M$, be the sample points in the Fourier plane, in wavelengths, closed under $(u, v) \mapsto (-u, -v)$, with measured visibilities $V_k$ that satisfy $V_{-k} = \overline{V_k}$ for the conjugate sample $-k$. Let $w_k \ge 0$ be weights with $w_{-k} = w_k$ and $W = \sum_k w_k > 0$. The **dirty image** and the **dirty beam** are the functions of the direction $(l, m)$

$$I_D(l, m) = \frac1W \sum_{k=1}^M w_k\, V_k\, e^{2\pi i (u_k l + v_k m)}, \qquad B(l, m) = \frac1W \sum_{k=1}^M w_k\, e^{2\pi i (u_k l + v_k m)} .$$

Both are real, by the conjugate symmetry. The dirty beam is the dirty image of a point source of flux 1 at the phase center, and $B(0, 0) = 1$. In words, $B$ is the inverse Fourier transform of the sampling function $\frac1W \sum_k w_k\, \delta(u - u_k, v - v_k)$, and $I_D$ is the inverse Fourier transform of the sampling function times the visibilities.

**The convolution form.** Suppose the visibilities are samples of the 2D Fourier transform of the sky $I'$ (the small-field form of the [Van Cittert-Zernike theorem](/van-cittert-zernike-theorem/)) plus noise: $V_k = \widehat{I'}(u_k, v_k) + n_k$. Put $\widehat{I'}(u_k, v_k) = \iint I'(l', m')\, e^{-2\pi i (u_k l' + v_k m')}\, dl'\, dm'$ into the definition and change the order of the sum and the integral:

$$I_D(l, m) = \iint I'(l', m')\, B(l - l', m - m')\, dl'\, dm' + N_D(l, m) = (B * I')(l, m) + N_D(l, m),$$

where $N_D$ is the dirty image of the noise alone. So the dirty beam is the [point spread function](/point-spread-function/) of the whole measurement. By the [convolution theorem](/convolution-theorem/) the same statement in the Fourier plane is that the transform of $I_D$ is the sky transform times the sampling function.

**The weights.** The weights are a choice. Natural weighting uses $w_k = 1/\sigma_k^2$, where $\sigma_k^2$ is the noise variance of $V_k$. Uniform weighting divides each weight by the number of samples in its cell of a grid, so that densely sampled regions of the Fourier plane, usually the short baselines, do not dominate. Robust weighting is a mix of the two. Each choice gives a different dirty beam from the same data.

**In practice.** Programs do not evaluate the sum at every pixel. They spread the weighted samples onto a regular grid with a gridding kernel, apply the FFT, and divide by the transform of the kernel; this is a [nonuniform FFT](/nonuniform-fft/) and gives the sum to a known accuracy on a pixel grid. For a wide field the samples also need the w term, which [w-projection](/w-projection/) handles.

## Examples and non-examples

Examples:

- **Two samples.** With the samples $u = \pm a$, $v = 0$ and equal weights, $B(l, m) = \cos 2\pi a l$. A point source of flux $S$ at $l_0$ has $V = S e^{\mp 2\pi i a l_0}$, so $I_D(l, m) = S \cos 2\pi a (l - l_0)$. The dirty image has a maximum at $l_0$ and also at $l_0 + 1/a$, $l_0 + 2/a$ and so on, and it does not depend on $m$. One baseline cannot tell these positions apart.
- **Natural weighting gives the least noise.** If the noise of different baselines is independent, with variance $\sigma_k^2$ for sample $k$ and $n_{-k} = \overline{n_k}$, the variance of $N_D$ at a point is proportional to $\sum_k w_k^2 \sigma_k^2 / W^2$. By the Cauchy-Schwarz inequality this is smallest when $w_k \propto 1/\sigma_k^2$, which is natural weighting. Uniform weighting gives a narrower dirty beam at the price of more noise.
- **The east-west array of the aperture synthesis page.** Three antennas at 0, 100 and 300 wavelengths observe a source at declination 30 degrees every hour from $H = -6$ h to 6 h, which gives 78 samples. With equal weights, the dirty beam falls to half at $l = 0.00124$ and $m = 0.00225$, and its sidelobes reach 0.535 within $|l|, |m| \le 0.06$. Take a sky of two point sources, 1 at $(0, 0)$ and 0.5 at $(0.004, 0.006)$. Then $B(0.004, 0.006) = -0.08952$, and the dirty image is $1 + 0.5 \cdot (-0.08952) = 0.9552$ at the first source and $0.5 - 0.08952 = 0.4105$ at the second. Each source changes the value at the other one through the sidelobes, which is why the peak of a dirty image is not the flux of a source.
- **The snapshot of the same array.** At $H = 0$ alone, all samples lie on the $u$ axis at multiples of 100. The dirty beam is 1 at $l = 0.01$ and at every $m$, so the dirty image repeats every 0.01 in $l$ and has no structure in $m$.
- **Full coverage.** If every Fourier coefficient of a periodic grid image is measured with equal weights, the dirty beam is a delta and the dirty image is the sky. This is the limit that aperture synthesis tries to approach.

Non-examples:

- **A restored CLEAN image.** It is the CLEAN model convolved with a clean beam, usually a Gaussian, plus the residual image. It is not the inverse transform of the samples, and its beam has no sidelobes.
- **The image of a single dish.** It is also the sky convolved with a beam, but that beam is the power pattern of a filled aperture, which is nonnegative. A dirty beam has negative sidelobes, because the zero spacing and many other points are not measured.
- **An image from the maximum entropy method or another regularized fit.** Such an image fits the samples and fills the gaps by a prior. It is not a linear function of the data.
- **The inverse FFT of gridded samples without the correction for the gridding kernel.** It is the dirty image multiplied by the transform of the kernel, with some aliasing from outside the grid. The correction step is part of the definition.

## Related definitions

- [Point spread function](/point-spread-function/): the dirty beam is the point spread function of the array with its sampling and weights.
- **Clean beam and residual image.** CLEAN replaces the dirty beam by a clean beam, a Gaussian fitted to the main lobe of $B$, and the residual image is the dirty image of the data minus the model visibilities. See [Hogbom CLEAN](/hogbom-clean/) and [Cotton-Schwab CLEAN](/cotton-schwab-clean/).
- **Primary beam.** The pattern of a single antenna, which multiplies the sky before it is measured. It sets the field of view, not the resolution.
- [Density compensation](/density-compensation/): the same weighting problem in MRI, where nonuniform samples of k-space are also inverted by a Fourier transform.
- [Image deblurring](/image-deblurring/): the general problem of undoing a known point spread function, of which the deconvolution of a dirty image is a hard case, because the transform of the dirty beam is zero at most frequencies.

## References
