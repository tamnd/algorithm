---
tag: 6TMK66
kind: problem
slug: image-smoothing
name: Image smoothing
aliases:
- blurring
area: graphics-and-signals/image-processing
level: intro
summary: Reduce high-frequency detail and fine variation in an image.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H)}
prereqs: [digital-image, linear-filtering]
see_also: [box-blur, gaussian-filter, bilateral-filter, guided-filter, anisotropic-diffusion, non-local-means, image-denoising, image-sharpening]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.5, Smoothing (Lowpass) Spatial Filters
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2, Linear filtering, and Section 3.3.1, Non-linear filtering
  - paper: doi:10.1137/040616024
    title: Antoni Buades, Bartomeu Coll and Jean-Michel Morel, A review of image denoising algorithms, with a new one, Multiscale Modeling and Simulation 4(2), 2005
    locator: the comparison of smoothing filters through their method noise
---

Image smoothing is the problem of reducing the fine variation of an image, its noise, texture and small detail, while keeping its broad structure. It has no single right answer: each method is defined by its own operator, and methods differ in what they keep. Linear methods, such as the [box blur](/box-blur/) and the [Gaussian filter](/gaussian-filter/), weaken all high frequencies alike and so also blur edges. Edge preserving methods, such as the [bilateral filter](/bilateral-filter/), the [guided filter](/guided-filter/), [anisotropic diffusion](/anisotropic-diffusion/) and [non-local means](/non-local-means/), let the weights depend on the image, so that strong edges stay sharp. Every method must write $WH$ output values, and the box and the guided filter reach this bound of $\Theta(WH)$ for any amount of smoothing, as do repeated boxes or recursive filters that approximate the Gaussian.

## In plain words

A smooth picture has gentle changes. Smoothing takes a picture with small, fast changes, such as grain, noise or fine texture, and makes it more gentle. The simple way is to replace each pixel by an average of the pixels near it. This removes the grain, but it also makes the edges soft, because the average mixes the two sides of an edge.

Better methods look before they average. They give less weight to neighbors that look very different, so the two sides of an edge are not mixed. They cost more, but they keep the shapes in the picture sharp.

## Definition

The input is an image $f$ with $W$ columns and $H$ rows and a scale parameter, such as a radius $R$, a standard deviation $\sigma$ or a number of steps. The output is an image $g$ of the same size such that:

- **Local averaging.** Each $g(p)$ is a weighted mean of values of $f$ near $p$, with nonnegative weights that sum to 1, so $g$ stays in the range of $f$ and a constant image is kept.
- **Less fine variation.** A measure of high-frequency content, such as the energy of the differences between neighbors or of the high frequencies of the spectrum, is smaller for $g$ than for $f$, and it falls further as the scale grows.
- **A border rule.** The values outside the image are fixed by a stated rule: clamp, mirror, wrap or zero padding, or a cut window that drops the outside pixels and renormalizes.

Smoothing is a means more than an end. When the input is a clean image plus noise and the aim is to recover the clean image, the problem is [image denoising](/image-denoising/); smoothing methods are one class of answers to it.

## Variants

- **Linear smoothing.** The weights are fixed, $g = K * f$ with a lowpass kernel $K$. The result is a [linear filter](/linear-filtering/) and is characterized by its frequency response.
- **Edge preserving smoothing.** The weights depend on the image, so that the filter smooths inside regions and not across their edges.
- **Scale space.** A one parameter family $g_t$ with $g_0 = f$, in which detail only disappears as $t$ grows: the Gaussian scale space, solutions of the heat equation, and nonlinear families from diffusion.
- **Smoothing by optimization.** $g$ minimizes a data term plus a penalty on its variation, as in [total variation denoising](/total-variation-denoising/) or weighted least squares smoothing.
- **Rank order smoothing.** The output is an order statistic of the window, as in the [median filter](/median-filter/), which is treated on its own page.

## Examples

- On the step $(10, 12, 10, 50, 48, 50)$, a Gaussian of $\sigma = 1$ with the clamp rule gives $(10.66, 13.13, 22.40, 37.60, 46.87, 49.34)$: the noise of size 2 is gone, and the step has become a ramp.
- On the same row, the bilateral filter with $\sigma_s = 1$, $\sigma_r = 10$ and a radius of 1, with the same clamp rule, gives $(10.54, 10.91, 10.75, 49.25, 49.09, 49.46)$: the noise is reduced, and the step stays a step.
- A box blur of radius 1 of the checkerboard of 0 and 1, with the wrap rule, gives $5/9$ at the pixels of value 1 and $4/9$ at the others: the pattern is weakened, not removed, because the box keeps $1/9$ of the amplitude at this frequency. A Gaussian of $\sigma = 1$, cut at $3\sigma$, keeps only about $0.0002$ of it.

## Known algorithms

| Method | Linear | Edges | Time |
|---|---|---|---|
| [Box blur](/box-blur/) by running sums | yes | blurred | $\Theta(WH)$ |
| [Integral image](/integral-image/) box mean | yes | blurred | $\Theta(WH)$ |
| [Gaussian filter](/gaussian-filter/), separable | yes | blurred | $\Theta(WH\sigma)$ |
| Gaussian by repeated boxes or recursive passes | yes | blurred | $\Theta(WH)$ |
| [Bilateral filter](/bilateral-filter/), direct | no | kept | $\Theta(WHR^2)$ |
| [Guided filter](/guided-filter/) | in the input | kept | $\Theta(WH)$ |
| [Anisotropic diffusion](/anisotropic-diffusion/), $n$ steps | no | kept | $\Theta(nWH)$ |
| [Non-local means](/non-local-means/), search radius $S$ | no | kept | $\Theta(WHS^2)$ |

## Bounds

- **Lower bound.** Every method that writes all $WH$ output values costs $\Omega(WH)$, and so does reading the input, since each output depends on the pixel itself.
- **Upper bounds.** The box blur, the integral image, the approximations of the Gaussian by repeated boxes or by recursive passes, and the guided filter all reach $\Theta(WH)$ for any radius, so the bound is tight for linear smoothing and for guided smoothing.
- **Direct filtering.** A $k \times k$ kernel costs $\Theta(WHk^2)$ directly, $\Theta(WHk)$ when it is separable, and $\Theta(WH \log(WH))$ by the FFT.

## Reductions

- **Smoothing as diffusion.** A Gaussian of $\sigma$ equals the solution at time $\sigma^2/2$ of the [heat equation](/heat-equation/) started from the image, so linear smoothing reduces to solving a PDE, and anisotropic diffusion changes the PDE.
- **Smoothing as regression.** Each output of a weighted mean is the least squares fit of a constant to the window with those weights; the guided filter fits a line in the guide instead.
- **Box sums to prefix sums.** A box mean reduces to four lookups in the [two-dimensional prefix sums](/two-dimensional-prefix-sums/) of the image.
- **Sharpening from smoothing.** Any smoothing operator $S$ gives a sharpening operator $f + \lambda(f - Sf)$, which is [unsharp masking](/unsharp-masking/).

## Applications

Smoothing removes noise before further analysis; prevents aliasing before downsampling, as in the [Gaussian pyramid](/gaussian-pyramid/); sets the scale of [edge detection](/edge-detection/) and of feature detectors; splits an image into a base layer and a detail layer for tone mapping and detail editing; makes background blur and depth of field effects in photography; and gives the blurred image that [unsharp masking](/unsharp-masking/) subtracts.

## References
