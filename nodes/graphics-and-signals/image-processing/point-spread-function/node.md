---
tag: X6BN5N
kind: definition
slug: point-spread-function
name: Point spread function
aliases:
- PSF
- blur kernel
area: graphics-and-signals/image-processing
level: intro
summary: The response of an imaging system to a point source, which models blur.
prereqs: [digital-image, discrete-convolution]
see_also: [image-deblurring, richardson-lucy-deconvolution, wiener-filter, convolution-theorem, gaussian-filter, box-blur, linear-filtering, super-resolution]
sources:
  - book: isbn:9780898716184
    title: Per Christian Hansen, James G. Nagy and Dianne P. O'Leary, Deblurring Images, Matrices, Spectra, and Filtering, SIAM, 2006
    locator: the chapter on the image blurring problem and the point spread function, with examples of point spread functions and boundary conditions
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: the chapter on image restoration and reconstruction (the degradation model, linear position-invariant degradations, and estimation of the degradation function)
---

The point spread function of an imaging system is the image it makes of a single point of light. A perfect system would map a point to a point; a real lens, a moving camera, the air and the sensor spread it into a small patch, and the shape of that patch is the point spread function, or PSF. When the system is linear, every object is a sum of points, so its image is the sum of the spread copies of those points, each placed at its point and scaled by its brightness. When the PSF is the same at every position, this sum is the convolution of the object with the PSF, so the PSF is the impulse response of the blur, and the same array is called the blur kernel. The PSF is the input to [image deblurring](/image-deblurring/) and to [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/), and its Fourier transform, the optical transfer function, tells which spatial frequencies the system passes.

## Definition

Let an imaging system be linear: it maps an object $o$ to an image $g = \mathcal H o$, and the image of a sum is the sum of the images. The point spread function is the image of a point source:

$$h(x, y) = (\mathcal H \delta_y)(x),$$

the brightness at position $x$ of the image of a unit point source at position $y$. Then $g(x) = \int h(x, y)\, o(y)\, dy$ for every object. The system is shift invariant if moving the source moves its image the same way, $h(x, y) = k(x - y)$; then

$$g = k * o,$$

and the function $k$ is the point spread function. For a [digital image](/digital-image/), $k$ is a small array, and the blurred image is the [discrete convolution](/discrete-convolution/) $g[i, j] = \sum_{m, n} k[m, n]\, o[i - m, j - n]$, with a rule for the pixels outside the image.

A PSF of blur by incoherent light is nonnegative, $k \ge 0$. It is usually normalized, $\sum k = 1$, so that the blur moves light but neither adds nor removes it, and a constant image stays constant. By the [convolution theorem](/convolution-theorem/), $\hat g = \hat k\, \hat o$: the Fourier transform $\hat k$ of the PSF, the optical transfer function, multiplies each spatial frequency of the object; its modulus is the modulation transfer function. Normalization means $\hat k(0) = 1$.

## Examples and non-examples

Examples:

- A $5 \times 5$ image that is 0 except for a 1 at the center, blurred with the kernel $\tfrac{1}{16}\begin{pmatrix}1 & 2 & 1\\ 2 & 4 & 2\\ 1 & 2 & 1\end{pmatrix}$, gives that kernel back around the center, with total 1: the blurred image of a point is the PSF.
- Gaussian PSF, $k(x) \propto e^{-|x|^2 / (2\sigma^2)}$, a model of the combined blur of the air, the optics and the sensor, and the kernel of the [Gaussian filter](/gaussian-filter/).
- Defocus: a lens out of focus spreads a point into a disk, so the PSF is uniform on a disk of a radius that depends on the depth, and zero outside.
- Motion blur: a camera that moves at constant speed in a straight line during the exposure spreads a point along a segment, so the PSF is uniform on that segment. A horizontal motion over 5 pixels gives the row $(\tfrac15, \tfrac15, \tfrac15, \tfrac15, \tfrac15)$, a one-dimensional [box blur](/box-blur/).
- Diffraction: a perfect lens with a circular aperture of diameter $D$, in light of wavelength $\lambda$, images a point as the Airy pattern, with intensity proportional to $(2 J_1(v)/v)^2$ for $v = \pi D \sin\theta / \lambda$ at angle $\theta$, where $J_1$ is the Bessel function of the first kind. Its first dark ring is at the first zero of $J_1$, $v \approx 3.8317$, that is $\sin\theta \approx 1.22\, \lambda / D$. This sets the finest detail that the lens can resolve.
- In astronomy, the image of a star far from the target is a measured PSF of the telescope and the atmosphere.

Non-examples:

- The [median filter](/median-filter/) is not linear, so it has no PSF in this sense: a $3 \times 3$ median maps an image with a single bright pixel to all zeros, yet it keeps a straight edge, so the response to a point does not predict the response to other images.
- A blur that changes across the image, as from a camera that rotates during the exposure or from objects at different depths, has a response $h(x, y)$ for each point, but no single kernel $k$, so it is not a convolution.
- A sharpening kernel such as $\begin{pmatrix}0 & -1 & 0\\ -1 & 5 & -1\\ 0 & -1 & 0\end{pmatrix}$ is the impulse response of a linear filter, but it has negative entries, so it does not describe the blur of an incoherent imaging system.
- A sensor that saturates, or that applies a gamma curve, is not linear in the light; its output for two points is not the sum of its outputs for each point, so the PSF must be applied before such a step.

## Related definitions

- [Discrete convolution](/discrete-convolution/) and [linear filtering](/linear-filtering/): the PSF is the kernel of a convolution, and the impulse response of a linear shift-invariant filter.
- [Convolution theorem](/convolution-theorem/): blur by the PSF is multiplication by its Fourier transform, the optical transfer function.
- [Reconstruction filter](/reconstruction-filter/): the kernel that maps samples to a continuous image, the counterpart of the PSF, which maps a continuous scene to samples.
- [Image deblurring](/image-deblurring/): the inverse problem of recovering the object from the image and the PSF, or both from the image alone.
- [Wiener filter](/wiener-filter/) and [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/): two methods that undo a known PSF.
- [Image noise](/image-noise/): the other part of the usual degradation model, $g = k * o + n$.

## References
