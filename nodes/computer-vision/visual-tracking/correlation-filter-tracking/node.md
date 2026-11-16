---
tag: 5K2YEP
kind: technique
slug: correlation-filter-tracking
name: Correlation filter tracking
aliases:
- discriminative correlation filters
area: computer-vision/visual-tracking
level: advanced
summary: Learn a filter whose correlation with the target patch gives a sharp peak, solved and applied in the Fourier domain, and move the target to the response peak.
prereqs: [visual-object-tracking, discrete-fourier-transform, cross-correlation]
see_also: [mosse-filter, kernelized-correlation-filter, siamese-tracking, ridge-regression, fast-fourier-transform, template-matching, normalized-cross-correlation, convolution]
sources:
  - paper: doi:10.1109/CVPR.2010.5539960
    title: David S. Bolme, J. Ross Beveridge, Bruce A. Draper and Yui Man Lui, Visual object tracking using adaptive correlation filters, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2010, 2544 to 2550
    locator: the whole paper (the filter fitted to a desired output in the Fourier domain, the running update and the peak to sidelobe ratio)
  - paper: doi:10.1109/TPAMI.2014.2345390
    title: João F. Henriques, Rui Caseiro, Pedro Martins and Jorge Batista, High-speed tracking with kernelized correlation filters, IEEE Transactions on Pattern Analysis and Machine Intelligence 37(3), 2015, 583 to 596
    locator: the whole paper (ridge regression on all cyclic shifts, its diagonalization by the discrete Fourier transform, kernels and multichannel features)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, 2nd edition, Springer, 2022
    locator: Chapter 3 (Fourier transforms and the correlation theorem)
---

Correlation filter tracking follows a target by learning a filter $h$ whose [cross-correlation](/cross-correlation/) with an image patch around the target gives a sharp peak at the target center and low values elsewhere. In each new frame the tracker correlates the filter with the patch at the old position and moves the target to the peak of the response, then updates the filter with the new patch. The filter is the solution of a regularized least-squares problem in which the training set is every cyclic shift of one patch. Its data matrix is circulant, so the [discrete Fourier transform](/discrete-fourier-transform/) makes it diagonal. Training and detection then cost $O(P \log P)$ for a patch of $P$ pixels, where a direct solve over all $P$ shifts would cost $O(P^3)$. The [MOSSE filter](/mosse-filter/) of Bolme and colleagues (2010) and the [kernelized correlation filter](/kernelized-correlation-filter/) of Henriques and colleagues are the basic forms. Scale filters, spatial regularization and learned features build on them. The method is fast and accurate for a short time, but the circular model and the online update are its two weak points.

## In plain words

We want a stencil that lights up at the center of the target when we slide it over a picture. We build it from the target itself: we ask for a picture with one bright spot at the center when the stencil sits on the target, and dark everywhere else, and solve for the stencil that comes closest. Sliding a stencil to every place costs a lot, but after a change to frequencies it is one multiplication per frequency, and so is the solving. In each new picture we slide the stencil over the area where the target was, move to the brightest spot, and adjust the stencil a little with what we see now.

## When it applies

- The target changes little between frames, so a patch around the old position contains the target and looks like the training patch.
- The motion between frames is a translation that is smaller than the patch. Rotation and scale change need extra steps.
- The appearance can be described by a few feature channels per pixel, such as gray values, color names or gradient histograms, or features of a network.
- The time budget is small. With $P$ pixels and $C$ channels, training and detection cost $\Theta(C P \log P)$ per frame with the [fast Fourier transform](/fast-fourier-transform/).

## The template

Notation: a patch has $P$ pixels and $C$ feature channels $x_1, \ldots, x_C$, indexed modulo the patch size, with a cosine window applied. The desired output $y$ is a Gaussian peak at the center. A hat is the discrete Fourier transform, a bar is the complex conjugate, and $\odot$ and the fraction bar act entry by entry. The regularization is $\lambda > 0$ and the learning rate is $\eta$.

```pseudo id=main
DCF-TRACK(F_0, ..., F_N, box b_0)
L1  x ← FEATURES(F_0, b_0) ⊙ window;  y ← the Gaussian peak at the center
L2  for c ← 1 to C do A_c ← ŷ ⊙ conj(x̂_c);   B ← Σ_c x̂_c ⊙ conj(x̂_c)        ▷ numerator and denominator
L3  for t ← 1 to N do
L4      z ← FEATURES(F_t, b_{t-1}) ⊙ window
L5      r ← IFFT(Σ_c ẑ_c ⊙ conj(A_c) / (B + λ))                               ▷ the response map
L6      b_t ← b_{t-1} moved by the offset of the largest value of r from the center
L7      x ← FEATURES(F_t, b_t) ⊙ window
L8      A_c ← (1 - η) A_c + η ŷ ⊙ conj(x̂_c);   B ← (1 - η) B + η Σ_c x̂_c ⊙ conj(x̂_c)
L9  return b_1, ..., b_N
```

**Why the Fourier domain.** Let $X$ be the $P \times P$ matrix whose rows are all cyclic shifts of one channel $x$. Ridge regression for a filter $w$ minimizes $\|X w - y\|^2 + \lambda \|w\|^2$, with solution $w = (X^\top X + \lambda I)^{-1} X^\top y$. Every circulant matrix is diagonalized by the discrete Fourier transform, with the transform of its first row on the diagonal. So the solution becomes one division per frequency, $\hat w = \hat y \odot \overline{\hat x} / (\overline{\hat x} \odot \hat x + \lambda)$, up to the conjugation convention. This is a theorem, proved on the [kernelized correlation filter](/kernelized-correlation-filter/) page. With $C$ channels, lines L2 and L5 use one common denominator. For one patch this is still exact, because the system at each frequency has rank one plus $\lambda I$. For a running average of many patches it is an approximation. Line L8 is a running average of numerator and denominator, as in MOSSE, which weights old frames by $(1 - \eta)^k$.

**What is not a theorem.** That the peak of the response is at the new target position is a property of the images, not of the method. It fails when the target changes quickly, when it leaves the patch, or when the background inside the patch dominates the filter.

**Cost.** Each frame does $O(C)$ transforms of size $P$ and $O(C P)$ other work, so $\Theta(C P \log P)$ time, and stores $\Theta(C P)$ numbers.

## Classic examples

**A filter by hand.** One dimension, $P = 4$, one channel, no window: $x = (1, 2, 0, -1)$, $y = (1, 0, 0, 0)$ and $\lambda = 0.1$. Then $\hat x = (2, 1 - 3i, 0, 1 + 3i)$, $\hat y = (1, 1, 1, 1)$, and the filter in the Fourier domain is

$$
\frac{\hat y \odot \overline{\hat x}}{|\hat x|^2 + \lambda} \approx (0.488, 0.099 + 0.297i, 0, 0.099 - 0.297i).
$$

The response to $x$ itself is $(0.739, 0.244, -0.251, 0.244)$, with the peak at offset 0. The response to the cyclic shift $(-1, 1, 2, 0)$ is $(0.244, 0.739, 0.244, -0.251)$: the peak has moved to offset 1, as it should.

**The boundary effect.** A real translation is not a cyclic shift. If the signal around the patch is $(\ldots, 5, 1, 2, 0, -1, \ldots)$ and it moves right by one, the patch at the old place becomes $(5, 1, 2, 0)$: a new value comes in instead of the $-1$ that wraps around. The response is $(1.27, 0.58, 0.68, 1.37)$, and the peak is at offset 3, a shift of one to the wrong side. With the value 3 instead of 5 the peak is at offset 0. The filter was trained on shifts that never happen. Real trackers reduce this with a patch two or three times as large as the target and a cosine window that sets the border to 0, so that the values that wrap are small.

**MOSSE.** The [MOSSE filter](/mosse-filter/) is the template with $C = 1$, preprocessed gray values, a start from the first patch and several random warps of it, and the peak to sidelobe ratio of the response as a test for failure. Its page tracks a textured square over 6 frames with errors below one pixel and reports the loss when the texture changes.

**KCF and DCF.** The [kernelized correlation filter](/kernelized-correlation-filter/) replaces the linear products by a kernel between the patch and its shifts, such as a Gaussian kernel, which keeps the circulant structure and so the cost. With the linear kernel and multichannel gradient histograms it is the DCF tracker. Both were standard baselines for fast tracking around 2015.

**Scale filters.** Danelljan and colleagues (2014) added a second, one-dimensional correlation filter over a pyramid of patches at a few tens of scales, which estimates the size of the target after the position filter has found its center.

## Variations

- **Kernels.** Any kernel that depends only on the products of a patch with its shifts, or only on their distances, keeps the circulant structure (the [kernelized correlation filter](/kernelized-correlation-filter/)).
- **Multichannel features.** Gradient histograms, color names and network features replace gray values. The cost grows linearly in the number of channels.
- **Spatial regularization.** A penalty that grows with the distance from the center lets the patch be large without a large filter. The problem is then no longer diagonal and needs an iterative solver, as in the SRDCF tracker of Danelljan and colleagues (2015).
- **Background-aware training.** Train on real shifts of a larger image area, cropped to the filter size, instead of cyclic shifts. This also needs an iterative solver.
- **Learned features and end-to-end training.** Valmadre and colleagues (2017) put a correlation filter layer inside a network and trained the features through it, which connects the method to [siamese tracking](/siamese-tracking/).
- **Subpixel peak.** Fit a parabola to the peak and its neighbors, or interpolate the response in the Fourier domain.

## Pitfalls

- **Circular wrap.** Without padding and a window, the filter learns the wrapped edges of the patch, as in the boundary example. With a window, the target must stay near the center of the patch.
- **Fast motion.** A motion of more than about half the patch, minus the size of the target, puts the target outside the patch. The tracker then follows the best match in the background.
- **Drift from the update.** Line L8 learns from the tracker's own output. A small error at each frame, an occluder or a similar object enters the filter and can take it away from the target. Lower $\eta$, or stop the update when the peak is weak.
- **Weak frequencies.** A frequency where the patch has almost no energy gets the large factor $1 / \lambda$. A $\lambda$ that is too small makes the filter noisy, and one that is too large blurs the peak.
- **Scale and rotation.** The basic filter finds a translation only. A target that grows quickly is lost, because the filter fits only part of it.
- **Integer peaks.** Without subpixel refinement, the position is rounded to the grid of the response, which can be coarse when features are pooled over cells.

## Exercises

1. Show that the matrix of all cyclic shifts of a vector $x$ of length $P$ is diagonalized by the discrete Fourier transform, and give its eigenvalues in terms of $\hat x$.
2. Derive the one-channel solution $\hat w = \hat y \odot \overline{\hat x} / (|\hat x|^2 + \lambda)$ from the ridge regression problem, and state the convention for correlation that it uses.
3. In the hand example, compute the response to the cyclic shift $(0, -1, 1, 2)$ and check that the peak is at offset 2.
4. With $C$ channels, the exact ridge solution solves a $C \times C$ system per frequency. Show with the Sherman-Morrison formula that for one patch it equals the common denominator of lines L2 and L5, and find a two-patch case where the two differ.
5. The patch has $64 \times 64$ pixels and the target $32 \times 32$. Bound the largest motion between frames that keeps the whole target inside the patch, and explain why the window makes the usable range smaller.

## References
