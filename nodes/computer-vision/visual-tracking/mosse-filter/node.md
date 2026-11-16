---
tag: Q4156Y
kind: algorithm
slug: mosse-filter
name: MOSSE filter
aliases:
- minimum output sum of squared error filter
area: computer-vision/visual-tracking
level: advanced
summary: A correlation filter fitted in closed form in the Fourier domain so that it gives a Gaussian peak on training patches, then updated online with running averages.
solves: [visual-object-tracking]
model: real-ram
complexity:
  vars: {P: the number of pixels in the patch, T: the number of training patches at the start, N: the number of frames tracked}
  time: {worst: Θ((T + N) P log P), average: Θ((T + N) P log P), best: Θ((T + N) P log P)}
  space: {extra: Θ(P)}
properties: {deterministic: true, exact: false, local: true, iterative: false, online: true}
history:
  year: 2010
  people: [David S. Bolme, J. Ross Beveridge, Bruce A. Draper, Yui Man Lui]
  note: Bolme, Beveridge, Draper and Lui fitted a correlation filter to many training outputs in closed form and updated it online, which gave a tracker that ran at several hundred frames per second on the hardware of 2010.
prereqs: [correlation-filter-tracking, fast-fourier-transform]
see_also: [kernelized-correlation-filter, cross-correlation, discrete-fourier-transform, ridge-regression, template-matching, normalized-cross-correlation, siamese-tracking, visual-object-tracking]
sources:
  - paper: doi:10.1109/CVPR.2010.5539960
    title: David S. Bolme, J. Ross Beveridge, Bruce A. Draper and Yui Man Lui, Visual object tracking using adaptive correlation filters, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2010, 2544 to 2550
    locator: the whole paper (the closed-form filter, the preprocessing with log, normalization and cosine window, the Gaussian outputs, the random affine perturbations at the start, the running update with the learning rate, and the peak to sidelobe ratio)
  - paper: doi:10.1109/TPAMI.2014.2345390
    title: João F. Henriques, Rui Caseiro, Pedro Martins and Jorge Batista, High-speed tracking with kernelized correlation filters, IEEE Transactions on Pattern Analysis and Machine Intelligence 37(3), 2015, 583 to 596
    locator: the whole paper (the link between correlation filters and ridge regression on cyclic shifts)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, 2nd edition, Springer, 2022
    locator: Chapter 3 (Fourier transforms and the correlation theorem)
---

The MOSSE filter (minimum output sum of squared error) is a [correlation filter](/correlation-filter-tracking/) for tracking. It learns a small image $h$, the filter, such that the [cross-correlation](/cross-correlation/) of $h$ with each training patch of the target is as close as possible, in the sum of squared errors, to a desired output: a narrow Gaussian peak at the target center. In the Fourier domain this least squares problem splits into one scalar problem per frequency, so the filter has a closed form that costs a few [fast Fourier transforms](/fast-fourier-transform/). In a new frame the tracker correlates the filter with the patch at the old position and moves to the peak of the response. It then updates the numerator and denominator of the filter with running averages. Bolme, Beveridge, Draper and Lui published it in 2010; they measured several hundred frames per second on their hardware, and the method started the line of correlation filter trackers that includes the [kernelized correlation filter](/kernelized-correlation-filter/).

## In plain words

We want a stencil that, when we slide it over the target, gives one bright spot exactly at the target center and darkness elsewhere. We do not guess the stencil; we compute it from examples of the target, so that sliding it over each example gives a picture as close as possible to the bright spot we want. Sliding a stencil over a picture is slow, but after a change to frequencies it is one multiplication per frequency, and then the best stencil is one division per frequency. In the next picture we slide the stencil over the area where the target was and move to the brightest spot. If the spot is not much brighter than its surroundings, the target is probably hidden, and we wait.

## The problem

Patches are $n \times n$ real arrays with $n$ a power of two, indexed by $x$ modulo $n$, and $P = n^2$. The center of the patch is the pixel $c = (n/2, n/2)$, and pixel $(u, v)$ has its center at the point $(u, v)$. Correlation is circular,

$$
g(y) = \sum_x f(x + y)\, h(x),
$$

and by the correlation theorem its [discrete Fourier transform](/discrete-fourier-transform/) is $\hat g = \hat f \odot H^*$ with $H^* = \overline{\hat h}$, where $\odot$ is the entry-by-entry product and the bar is the complex conjugate. Given training patches $f_1, \ldots, f_N$ and desired outputs $g_1, \ldots, g_N$ (each a Gaussian of standard deviation $\sigma = 2$ pixels centered at $c$), the filter minimizes

$$
\sum_{i=1}^N \sum_k \big| \hat f_i(k) H^*(k) - \hat g_i(k) \big|^2 + \varepsilon \sum_k |H^*(k)|^2 ,
$$

which by Parseval's identity is a constant times the output sum of squared error in the image domain plus a small penalty on the size of $h$. The minimizer is

$$
H^* = \frac{A}{B + \varepsilon}, \qquad A = \sum_i \hat g_i \odot \overline{\hat f_i}, \qquad B = \sum_i \hat f_i \odot \overline{\hat f_i},
$$

with the division taken entry by entry. Each patch is preprocessed: take $\log(1 + \text{value})$, subtract the mean and divide by the norm, and multiply by a cosine window that goes to 0 at the border, so that the circular wrap of the transform does not create strong edges.

## The algorithm

```pseudo id=main
INIT(F₀, p)
L1   for each of T patches: the patch at p in F₀ and T - 1 small random affine warps of it do
L2       f ← PREPROCESS(patch);  A ← A + Ĝ ⊙ conj(f̂);  B ← B + f̂ ⊙ conj(f̂)

TRACK(F_t)
L3   f̂ ← FFT(PREPROCESS(patch of F_t at p))
L4   g ← IFFT(f̂ ⊙ A / (B + ε))                           ▷ the response
L5   (y, s) ← the peak of g and its peak to sidelobe ratio
L6   if s < s_min then return p, LOST                      ▷ keep p and the filter
L7   p ← p + (y - c)
L8   f̂ ← FFT(PREPROCESS(patch of F_t at p))
L9   A ← η Ĝ ⊙ conj(f̂) + (1 - η) A;  B ← η f̂ ⊙ conj(f̂) + (1 - η) B
L10  return p
```

Bolme and colleagues start with 8 random small affine perturbations of the first patch, use the learning rate $\eta = 0.125$, and add a small $\varepsilon$ to the denominator. The peak to sidelobe ratio of line L5 is

$$
s = \frac{g_{\max} - \mu}{\sigma_s},
$$

where $\mu$ and $\sigma_s$ are the mean and standard deviation of the response outside an $11 \times 11$ window around the peak. They report values between 20 and 60 under normal tracking and values near 7 when the target is lost or occluded; the threshold is a heuristic, and it depends on the patch size.

## Example

**One dimension by hand.** Take $n = 4$, the patch $f = (1, 2, 0, -1)$ and the desired output $g = (1, 0, 0, 0)$, a peak at index 0. Then $\hat f = (2, 1 - 3i, 0, 1 + 3i)$ and $\hat g = (1, 1, 1, 1)$. The filter is

$$
H^* = \frac{\hat g \odot \overline{\hat f}}{|\hat f|^2 + \varepsilon} \approx \Big( \tfrac12, \tfrac{1 + 3i}{10}, 0, \tfrac{1 - 3i}{10} \Big).
$$

The middle frequency of $f$ is 0, so the filter can do nothing there, and without $\varepsilon$ it would divide 0 by 0. The response to $f$ is $\hat f \odot H^* \approx (1, 1, 0, 1)$, whose inverse transform is $(0.75, 0.25, -0.25, 0.25)$: the peak is in the right place but the missing frequency spreads part of it. This is why one patch is not enough and the perturbed copies are added.

**Tracking.** The frames are $64 \times 64$, with a background of Gaussian blobs and a $33 \times 33$ square target with another blob texture, which moves by $(2.4, 1.7)$ per frame. The patch is $32 \times 32$ ($P = 1024$), $\sigma = 2$, $\eta = 0.125$, $\varepsilon = 10^{-5}$, and the start uses the patch and 8 perturbations (rotations up to 0.15 radian and scales from 0.9 to 1.1). Over 6 frames the tracked centers are $(26, 27)$, $(29, 29)$, $(31, 31)$, $(33, 33)$, $(36, 34)$, $(38, 36)$, against the true $(26.4, 27.7)$ up to $(38.4, 36.2)$. The errors are between 0.22 and 0.81 pixel, which is the rounding to the integer peak. The ratios are between 11.7 and 15.7. Then the target is replaced by a different texture: the ratio drops to 3.0, line L6 reports LOST, and the position and the filter stay as they were.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: correlation theorem.** For real patches, the transform of the circular correlation of $f$ with $h$ is $\hat f \odot \overline{\hat h}$.
- **Theorem: the closed form is optimal.** $A / (B + \varepsilon)$ is the unique minimizer of the regularized output error above, because the objective separates into one strictly convex quadratic per frequency.
- **Theorem: the running update is optimal for a weighted objective.** $A_t / (B_t + \varepsilon)$ minimizes the same error with weights $\eta (1 - \eta)^{t - s}$ on frame $s$, so old frames fade at a geometric rate.
- **Theorem: shifts.** A circular shift of the input by $d$ moves the response by $d$, so a target that moved by $d$ gives a peak at $c + d$ if the new patch is a circular shift of the old one.

A real patch is not a circular shift of the old one, so line L7 is a heuristic that works when the motion is small compared to the patch. The peak to sidelobe test is a heuristic with no guarantee.

## Complexity

A 2D FFT of $P$ points costs $\Theta(P \log P)$. A frame uses three transforms (lines L3, L4 and L8) and $\Theta(P)$ entry-by-entry work, so it costs $\Theta(P \log P)$. The start costs $\Theta(T P \log P)$ for the $T$ training patches, so $N$ frames cost $\Theta((T + N) P \log P)$ in all. The extra space is $\Theta(P)$ for $A$, $B$ and the target transform $\hat G$. The cost depends on the patch, not on the frame, which is why the method is fast.

## Properties

- **Closed form.** No iterative training; the filter is a quotient of two running sums.
- **Fast.** A few FFTs of a small patch per frame.
- **Integer shifts.** The peak is on the pixel grid; subpixel accuracy needs interpolation of the peak.
- **Fixed scale.** The plain filter does not change its size; scale needs a separate search.
- **Circular boundary.** The training implicitly treats the patch as periodic, so shifted copies of the target wrap around at the border. The cosine window hides this, but it also limits the motion that can be found to a part of the patch.
- **Single channel.** The original works on gray values; multichannel features need a sum over channels.

## Variants and improvements

- **ASEF.** The earlier average of synthetic exact filters by Bolme and colleagues averages the exact filter of each image instead of summing numerators and denominators; MOSSE is more stable when a frequency is weak.
- **[Kernelized correlation filter](/kernelized-correlation-filter/).** Henriques and colleagues showed that the filter is [ridge regression](/ridge-regression/) on all cyclic shifts of the patch, and used kernels and multichannel features such as HOG.
- **Scale filters.** A second 1D filter over a few scales of the patch estimates the size.
- **Spatial regularization.** Penalize filter values far from the center to reduce the boundary effect of the circular model.
- **Subpixel peaks.** Fit a parabola to the peak and its neighbors.

## When to use it

Use MOSSE when you need a very fast single-target tracker with modest accuracy, for example on a small device or as a component that runs many times per frame. It needs only an FFT. For better accuracy at a similar cost, use the [kernelized correlation filter](/kernelized-correlation-filter/) with HOG features. For large changes of appearance or scale, use a learned tracker such as [siamese tracking](/siamese-tracking/).

## Pitfalls

- **No regularization.** A frequency where all training patches are near 0 gives a huge or undefined filter entry, as in the example. Always add $\varepsilon$.
- **No window.** Without the cosine window, the border of the patch is a strong edge after the circular wrap, and the filter learns it.
- **Patch sizes.** The radix-2 FFT needs a power of two; with other sizes, use a mixed-radix FFT or pad the patch.
- **A threshold copied from the paper.** The PSR values depend on the patch size, the exclusion window and the preprocessing. Calibrate the threshold on your own data, as the example shows with values near 15 instead of 20 to 60.
- **Updating while lost.** Training on an occluder teaches the filter the occluder. Skip the update when the ratio is low, as line L6 does.
- **Sign of the shift.** Whether the peak moves by $+d$ or $-d$ depends on which of $f$ and $h$ is conjugated. Check it with a known shift.

## Implementations

## History

Correlation filters for pattern recognition go back to the matched filter and to the synthetic discriminant functions and minimum average correlation energy filters of the optical pattern recognition literature of the 1980s. Bolme, Draper and Beveridge introduced the average of synthetic exact filters (ASEF) for eye localization in 2009. In 2010 Bolme, Beveridge, Draper and Lui gave MOSSE: a single filter fitted to all training outputs at once, with the running update and the peak to sidelobe ratio as a failure test. Their tracker ran at several hundred frames per second. Henriques, Caseiro, Martins and Batista explained the filter as ridge regression on cyclic shifts (2012, 2015), which led to the [kernelized correlation filter](/kernelized-correlation-filter/) and to many later correlation filter trackers.

## References
