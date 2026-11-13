---
tag: FHD8S0
kind: problem
slug: image-sharpening
name: Image sharpening
aliases:
- edge enhancement
area: graphics-and-signals/image-processing
level: intro
summary: Increase the apparent contrast of edges and fine detail.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H)}
prereqs: [digital-image, image-smoothing]
see_also: [unsharp-masking, image-deblurring, laplacian-of-gaussian, contrast-enhancement, guided-filter, bilateral-filter, richardson-lucy-deconvolution, super-resolution]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.6, Sharpening (Highpass) Spatial Filters (the Laplacian, unsharp masking and highboost filtering, and the gradient)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2, Linear filtering (sharpening by unsharp masking)
  - paper: doi:10.1109/TPAMI.2012.213
    title: Kaiming He, Jian Sun and Xiaoou Tang, Guided image filtering, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(6), 2013
    locator: the application to detail enhancement
---

Image sharpening is the problem of making edges and fine detail look crisper, by raising their contrast against their surroundings. Unlike [deblurring](/image-deblurring/), it does not try to undo a known blur and recover the true image; it only boosts the detail that is still there, guided by how sharp the result looks. Nearly every method splits the image into a smooth part and a detail part with some [smoothing](/image-smoothing/) operator $S$, and adds back more detail: $g = f + \lambda(f - Sf)$. With a Gaussian for $S$ this is [unsharp masking](/unsharp-masking/), a linear filter that costs $\Theta(WH\sigma)$, or $\Theta(WH)$ with a box or a recursive blur. With an edge preserving $S$, such as the [guided filter](/guided-filter/), strong edges are left out of the detail part and are not overshot.

## In plain words

A sharp picture has crisp edges: the brightness changes quickly from one side to the other. A slightly soft picture has the same edges, but they are a little smeared. Sharpening makes the dark side of each edge a bit darker and the bright side a bit brighter, just near the edge. Our eyes read this as a crisper edge.

It does not bring back detail that is lost. Very fine detail and noise get stronger too, so too much sharpening makes the picture look harsh and gives bright and dark rims along edges.

## Definition

The input is an image $f$ with $W$ columns and $H$ rows and a strength parameter $\lambda \ge 0$, and usually a scale, such as the $\sigma$ of the blur that defines what counts as detail. The output is an image $g$ of the same size such that:

- **Flat regions are kept.** A constant image, and in practice each smooth region, is unchanged.
- **More local contrast.** Across an edge or in a texture, the differences between neighbors in $g$ are larger than in $f$, by a factor that grows with $\lambda$.
- **A border rule.** The values outside the image are fixed by a stated rule, clamp, mirror, wrap or zero padding, for every filter the method uses.
- **A value range.** The output is clipped to the range of the pixel format, or the method says that it is not.

The aim is visual, so methods are compared by the overshoot and halos they make, by how much they boost noise, and by measures of perceived sharpness.

## Variants

- **Linear sharpening.** $g = f + \lambda(f - K * f)$ for a lowpass kernel $K$, or $g = f - \lambda \nabla^2 f$ with a discrete Laplacian. Both are [linear filters](/linear-filtering/) whose gain is 1 at the frequency 0 and above 1 for high frequencies.
- **Adaptive sharpening.** The amount depends on the place: a threshold that leaves small differences alone, a gain that is lower in flat or noisy areas, or a detail part from an edge preserving filter.
- **Multiscale sharpening.** The detail bands of a [Laplacian pyramid](/laplacian-pyramid/) are boosted with separate amounts.
- **Sharpening for display.** After resizing or before printing, sharpening makes up for the blur of the resampling filter or of the print, with a scale fixed by the output device.
- **Deblurring.** When the blur kernel is known or estimated and the aim is the true image, the problem is deconvolution, [image deblurring](/image-deblurring/), with methods such as the [Wiener filter](/wiener-filter/) and [Richardson-Lucy](/richardson-lucy-deconvolution/).

## Examples

- The step $(10, 10, 10, 50, 50, 50)$ with unsharp masking, the blur $[1, 2, 1]/4$, $\lambda = 1$ and the clamp rule becomes $(10, 10, 0, 60, 50, 50)$: the dark side of the edge gets darker and the bright side brighter. Clipping to $[0, 50]$ gives $(10, 10, 0, 50, 50, 50)$.
- The Laplacian sharpening $g = f - \nabla^2 f$ of the same row, with the clamp rule and the 1D Laplacian $f(x-1) - 2f(x) + f(x+1)$, gives $(10, 10, -30, 90, 50, 50)$: the same shape with a larger overshoot, because this kernel boosts the highest frequencies by a factor of 5.
- A constant image is unchanged by both, because both kernels sum to 1.

## Known algorithms

| Method | Linear | Halos at strong edges | Time |
|---|---|---|---|
| [Unsharp masking](/unsharp-masking/), Gaussian blur | yes | yes | $\Theta(WH\sigma)$ |
| Unsharp masking, box or recursive blur | yes | yes | $\Theta(WH)$ |
| Laplacian sharpening, 3 by 3 kernel | yes | yes | $\Theta(WH)$ |
| Unsharp masking with a threshold | no | yes | as the blur |
| Detail boost with the [guided filter](/guided-filter/) | no | few | $\Theta(WH)$ |
| Detail boost with the [bilateral filter](/bilateral-filter/) | no | few, with gradient reversal | $\Theta(WHR^2)$ |

## Bounds

- **Lower bound.** Every method that writes all $WH$ output values costs $\Omega(WH)$.
- **Upper bound.** Unsharp masking with a box blur by running sums or with a recursive Gaussian, and guided detail boosting, cost $\Theta(WH)$ for any scale, so the bound is tight.
- **No recovery of lost frequencies.** A linear sharpening filter multiplies each frequency by its gain. A frequency that the blur removed completely stays at zero, so no amount of sharpening brings it back; only methods with prior knowledge, as in [super-resolution](/super-resolution/) and deblurring with priors, can fill it in.

## Reductions

- **Sharpening from smoothing.** Any smoothing operator $S$ gives the sharpening operator $f + \lambda(f - Sf)$, so each method of [image smoothing](/image-smoothing/) gives one of sharpening, linear or edge aware as $S$ is.
- **Laplacian and unsharp masking.** For a Gaussian of small $\sigma$, $f - K * f \approx -\tfrac{\sigma^2}{2} \nabla^2 f$, so unsharp masking with a small blur is Laplacian sharpening with $\lambda \sigma^2/2$ in place of the Laplacian weight.
- **Sharpening as one step of deblurring.** For a blur $K$ close to the identity, $(1 + \lambda)\delta - \lambda K$ with $\lambda = 1$ is the first two terms of the series $K^{-1} = \sum_{i \ge 0} (\delta - K)^i$ of the inverse blur, so unsharp masking is a crude one-step deconvolution.

## Applications

Sharpening is applied in camera pipelines after demosaicing and noise reduction, in scanners and printer drivers, after resizing images for the web or for print, in medical and astronomical imaging to make structures easier to see, and in photo editors as the unsharp mask tool with its amount, radius and threshold. Edge aware detail boosting is used for HDR tone mapping and for local contrast editing, where it works together with [contrast enhancement](/contrast-enhancement/).

## References
