---
tag: GW9GYD
kind: algorithm
slug: kanade-lucas-tomasi-tracker
name: Kanade-Lucas-Tomasi tracker
aliases:
- KLT tracker
- KLT feature tracker
area: computer-vision/visual-tracking
level: core
summary: Select corners whose window matrix has a large smaller eigenvalue, follow each one from frame to frame by pyramidal Lucas-Kanade steps, and drop a point that fails a check.
solves: [optical-flow]
model: real-ram
complexity:
  vars: {N: the number of frames, n: the number of points, W: image width, H: image height, L: the number of pyramid levels above level 0, k: the iteration limit per level, m: the number of pixels in a window}
  time: {worst: Θ(W H m + N (W H + n (L + 1) k m)), average: Θ(W H m + N (W H + n (L + 1) k m)), best: Θ(W H m + N (W H + n (L + 1) m))}
  space: {extra: Θ(W H + n N)}
properties: {deterministic: true, exact: false, local: true, iterative: true, online: true}
history:
  year: 1991
  people: [Bruce D. Lucas, Takeo Kanade, Carlo Tomasi, Jianbo Shi]
  note: Tomasi and Kanade joined the registration step of Lucas and Kanade (1981) with a rule for choosing the windows to track; Shi and Tomasi (1994) justified the rule and added a check of the window by an affine model.
prereqs: [lucas-kanade-method, shi-tomasi-corner-detector, gaussian-pyramid]
see_also: [forward-backward-error, inverse-compositional-alignment, feature-track, optical-flow, visual-odometry, tracking-learning-detection, harris-corner-detector, image-pyramid]
sources:
  - paper: "Carlo Tomasi and Takeo Kanade, Detection and tracking of point features, Technical Report CMU-CS-91-132, Carnegie Mellon University, 1991"
    locator: the whole report (tracking a window by its translation, and choosing windows where both eigenvalues of the 2 by 2 gradient matrix are large)
  - paper: doi:10.1109/CVPR.1994.323794
    title: Jianbo Shi and Carlo Tomasi, Good features to track, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 1994, 593 to 600
    locator: the whole paper (the selection rule by the smaller eigenvalue, and the check of each feature by an affine model of the window)
  - paper: "Jean-Yves Bouguet, Pyramidal implementation of the Lucas Kanade feature tracker, description of the algorithm, Intel Corporation, Microprocessor Research Labs, technical report distributed with OpenCV, 2000"
    locator: the whole report (the pyramid, the propagation of the guess from level to level, and the iteration with the gradient of the first image)
  - paper: "Bruce D. Lucas and Takeo Kanade, An iterative image registration technique with an application to stereo vision, Proceedings of the 7th International Joint Conference on Artificial Intelligence (IJCAI), Vancouver, 1981, volume 2, pages 674 to 679"
    locator: the whole paper (the registration step that the tracker repeats)
  - paper: doi:10.1023/B:VISI.0000011205.11775.fd
    title: Simon Baker and Iain Matthews, Lucas-Kanade 20 years on, a unifying framework, International Journal of Computer Vision 56(3), 2004, 221 to 255
    locator: Section 3 (the compositional and inverse compositional updates, which for a translation give the step used here)
---

The Kanade-Lucas-Tomasi tracker (KLT) follows a set of small image windows through a video. It chooses the windows in the first frame with the rule of the [Shi-Tomasi corner detector](/shi-tomasi-corner-detector/): keep the pixels where the smaller [eigenvalue](/eigenvalue/) of the 2 by 2 gradient matrix of the window is large. It then finds the shift of each window from one frame to the next with the [Lucas-Kanade method](/lucas-kanade-method/), run from coarse to fine on a [Gaussian pyramid](/gaussian-pyramid/) so that shifts of many pixels stay inside the range of the linearization. A point is dropped when its window loses texture, leaves the image or fails a [forward-backward](/forward-backward-error/) check. The output is a sparse [optical flow](/optical-flow/) in the form of point tracks, one [feature track](/feature-track/) for each window.

## In plain words

A video is a sequence of pictures. We want to follow some small patches from picture to picture. Not every patch can be followed: a patch on a blank wall looks the same everywhere, and a patch on a straight edge can slide along the edge without any visible change. So the tracker first picks patches that look like corners, where the picture changes in every direction, and keeps them a minimum distance apart. For each patch, it then asks where the same pattern is in the next picture. It answers with a few small correction steps, first on blurred and shrunk copies of the pictures, where a large motion looks small, and then on sharper copies. A patch that becomes flat, moves out of the picture, or cannot find its way back to its start when tracked backward is dropped.

## The problem

The input is a sequence of gray frames $F_0, \ldots, F_N$ of $W$ columns and $H$ rows, given as [digital images](/digital-image/). We use the convention of the computer vision pages: the pixel $(u, v)$ is the value $F[v][u]$, $u$ points right, $v$ points down, and the center of the pixel is the point $(u, v)$. (The [Lucas-Kanade method](/lucas-kanade-method/) page puts the center at $x + 1/2$; the two conventions differ by a constant shift and give the same displacements.) Off-grid values come from [bilinear interpolation](/bilinear-interpolation/) with clamped indices. A window of radius $r$ around a point $p$ is the set of $m = (2r + 1)^2$ points $p + (i, j)$ with integers $|i|, |j| \le r$.

The output is a set of tracks. A track is a list of points $p_0, p_1, \ldots$ with $p_t$ in frame $t$, such that the window around $p_t$ in $F_t$ shows the same pattern as the window around $p_{t-1}$ in $F_{t-1}$ up to a translation. For two frames $I$ and $J$ and a point $p$, the shift is the $d$ that minimizes

$$
\varepsilon(d) = \sum_{x \in \text{window}(p)} \big( J(x + d) - I(x) \big)^2 .
$$

The gradient matrix of the window, the structure tensor, is

$$
G(p) = \sum_{x \in \text{window}(p)} \nabla I(x)\, \nabla I(x)^{\mathsf T}, \qquad \lambda_{\min}(p) = \text{the smaller eigenvalue of } G(p).
$$

If $\lambda_{\min}(p)$ is near zero, the window has texture in at most one direction and $d$ is not determined (the aperture problem of [optical flow](/optical-flow/)).

## The algorithm

The tracker has three parts: SELECT picks the points, PYR-LK finds one shift, and KLT runs them over the video. A pyramid with levels $0, \ldots, L$ is built once per frame; level $\ell$ is level $\ell - 1$ blurred with the binomial filter $(1, 4, 6, 4, 1)/16$ in both directions and then sampled at even $u$ and even $v$. So the pixel $(u, v)$ of level $\ell$ is the point $(2^\ell u, 2^\ell v)$ of level 0.

```pseudo id=main
KLT(F₀, ..., F_N, r, L, k, τ, λ_min, ε_fb)
L1   P ← SELECT(F₀)
L2   for t ← 1 to N do
L3       for each point p in P do
L4           d ← PYR-LK(F_{t-1}, F_t, p)                     ▷ LOST if the window is flat
L5           b ← PYR-LK(F_t, F_{t-1}, p + d)                 ▷ track back
L6           if d or b is LOST or |d + b| > ε_fb then remove p from P
L7           else append p + d to the track of p;  p ← p + d
L8   return the tracks

SELECT(I)                                                     ▷ quality q, minimum distance δ
L9   for each pixel x whose window lies inside I do λ(x) ← λ_min(x)
L10  C ← the pixels with λ(x) ≥ q · max λ, sorted by decreasing λ
L11  P ← empty;  for each c in C do if |c - p| ≥ δ for every p in P then add c to P
L12  return P

PYR-LK(I, J, p)                                               ▷ pyramids I⁰..I^L and J⁰..J^L
L13  g ← (0, 0)
L14  for ℓ ← L down to 0 do
L15      q ← p / 2^ℓ;  G ← Σ_{x ∈ window(q)} ∇I^ℓ(x) ∇I^ℓ(x)ᵀ
L16      if the smaller eigenvalue of G < λ_min then return LOST
L17      ν ← (0, 0)
L18      repeat up to k times
L19          b ← Σ_{x ∈ window(q)} ∇I^ℓ(x) (I^ℓ(x) - J^ℓ(x + g + ν))
L20          η ← G⁻¹ b;  ν ← ν + η
L21          if |η| < τ then leave the loop
L22      if ℓ > 0 then g ← 2 (g + ν) else g ← g + ν
L23  return g
```

Lines L15 to L21 are one Lucas-Kanade solve at level $\ell$, started from the guess $g$ that the coarser levels give. Two details follow Bouguet's description. First, the gradient and the matrix $G$ come from the first image $I$, at the fixed window, so $G$ and its inverse are computed once per level and not once per iteration. For a translation this is the [inverse compositional](/inverse-compositional-alignment/) step of Baker and Matthews. Second, line L22 doubles the guess when it goes one level down, because one pixel at level $\ell$ is two pixels at level $\ell - 1$. The gradient at an off-grid point is the central difference $(I(x + e_1) - I(x - e_1))/2$ of interpolated values, and likewise in $v$.

## Example

**Selection on numbers.** A window with $G = \begin{pmatrix} 10 & 6 \\ 6 & 10 \end{pmatrix}$ has eigenvalues 4 and 16, so $\lambda_{\min} = 4$: there is texture in both directions. A window on a vertical step edge has all gradients of the form $(g_u, 0)$, so $G = \begin{pmatrix} a & 0 \\ 0 & 0 \end{pmatrix}$ and $\lambda_{\min} = 0$. Line L16 rejects it at any positive threshold; a shift along the edge cannot be measured there.

**A shift of 6 pixels.** Frame $F_0$ is a $48 \times 48$ texture made of 14 Gaussian blobs (seeded positions, widths from 2 to 3.5 pixels, heights from 60 to 200), and $F_1$ is the same texture moved by $(6, 4)$. The windows have $r = 3$ ($m = 49$), the pyramid has $L = 2$ (sizes 48, 24 and 12), $\tau = 0.01$. SELECT with $q = 0.05$ and $\delta = 6$ keeps 10 points, the first at $(22, 24)$, which has the largest $\lambda_{\min}$ of the image, about 32135. PYR-LK at this point gives:

| Level $\ell$ | Window center $q$ | Guess $g$ on entry | Result $\nu$ | Iterations |
|---|---|---|---|---|
| 2 | $(5.5, 6)$ | $(0, 0)$ | $(1.5053, 0.9881)$ | 5 |
| 1 | $(11, 12)$ | $(3.0106, 1.9762)$ | $(-0.0106, 0.0238)$ | 2 |
| 0 | $(22, 24)$ | $(6.0000, 4.0000)$ | $(0.0000, 0.0000)$ | 1 |

The result is $(6.000002, 3.999998)$. The shift is $(1.5, 1)$ at level 2, inside the range of one linearization, and each level down only corrects the doubled guess. Without the pyramid ($L = 0$), the solve starts 7.2 pixels from the answer: of the 6 selected points that lie at least 8 pixels inside the image, 4 still converge, but two stop 7.7 and 102.5 pixels from the true position. With $L = 2$ all 6 are within 0.01 pixel.

**A subpixel shift.** With $F_1$ moved by $(1.3, -0.7)$ instead, the same 6 points are found with errors from 0.011 to 0.049 pixel. The error does not go to zero because bilinear interpolation of the blobs is not exact between pixels; for the whole-pixel shift $(6, 4)$ it is at most 0.0012 pixel, and the iteration stops at $\tau = 0.01$ before the last digits settle.

**The backward check.** In $F_1$ the texture moves by $(1, 0.5)$, and a $17 \times 17$ block with $29 \le u \le 45$, $19 \le v \le 35$ is replaced by another texture, an occluder. The point at $(37, 27)$, under the occluder, moves to a wrong place, $(4.68, 11.17)$ away; tracked back, it misses its start by 2.54 pixels, so line L6 drops it at $\varepsilon_{fb} = 0.5$. The point at $(22, 24)$ is outside the occluder at level 0, but its window at level 2 covers it, and the result is 18 pixels off; the backward error is 18.5, and it is dropped too. The point at $(28, 23)$, at the edge of the occluder, ends 0.395 pixel from the truth with a backward error of only 0.11, so it is kept. The check is a [heuristic](/forward-backward-error/), not a guarantee. The four points far from the occluder are kept with errors below 0.02 pixel.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts.

- **Selection.** The output of SELECT has three properties: every point passes the threshold, any two points are at least $\delta$ apart, and every rejected pixel above the threshold is within $\delta$ of a kept point with $\lambda$ at least as large. The proof is by the order of the greedy loop.
- **The step.** For a translation, line L20 is the Gauss-Newton step of the inverse compositional formulation: it minimizes the linearization of $\sum_x (I(x - \eta) - J(x + g + \nu))^2$ with respect to $\eta$, whose normal matrix is the fixed $G$. When $G$ is nonsingular the step is unique.
- **Fixed point and local convergence.** If $J(x + d^*) = I(x)$ on the window for a shift $d^*$, then $d^*$ is a fixed point of lines L19 and L20. For a smooth image model the Jacobian of the iteration map is zero at $d^*$, so the iteration converges to $d^*$ from every start close enough to it, faster than any fixed linear rate.
- **The pyramid.** If level $\ell$ returns $\nu_\ell$, the final shift is $\sum_\ell 2^\ell \nu_\ell$, and a translation by $d$ at level 0 is a translation by $d / 2^\ell$ at level $\ell$ in the continuous model. So each level solves the same problem at a scale where the shift is smaller.

No result gives convergence from a far start: the range depends on the image content, as the example of the 7.2 pixel start shows. The forward-backward check of line L6 is a heuristic test with no guarantee.

## Complexity

- **Selection.** Line L9 computes $G$ at $W H$ pixels. With a direct sum over each window, this is $\Theta(W H m)$; with box sums (an [integral image](/integral-image/) of each of the three products) it is $\Theta(W H)$. Sorting the candidates costs $O(W H \log(W H))$, and the distance test in line L11 is $O(|C| \cdot |P|)$ in the direct form.
- **One PYR-LK call.** Line L15 reads $m$ points per level, and each of at most $k$ iterations reads $m$ points of $J$. So the cost is $\Theta((L + 1) k m)$ in the worst case and $\Theta((L + 1) m)$ when each level stops after one step.
- **Pyramids.** Level $\ell$ has about $W H / 4^\ell$ pixels, so a pyramid costs at most $\frac{4}{3} W H$ times a constant: $\Theta(W H)$ per frame.
- **Total.** For $n$ points and $N$ frames, with the backward check (which doubles the PYR-LK calls), the time is $\Theta(W H m + N(W H + n (L + 1) k m))$ in the [real RAM](/real-ram/). The extra space is $\Theta(W H)$ for two pyramids and $\Theta(n N)$ for the tracks.

## Properties

- **Sparse.** It gives motion only at the selected points. The selection rule is the same quantity that decides whether the solve is well posed, so the tracker tracks only where it can.
- **Subpixel.** Positions are real numbers, and the error on a pure translation of a smooth image is limited by the interpolation.
- **Translation only.** Each step assumes that the window only moves. Rotation, scaling and perspective change the window, and over many frames the pattern drifts. Shi and Tomasi check the window against the first frame with an affine model to find such failures.
- **Local and independent.** Each point is tracked alone, so the cost is linear in the number of points and the points can be tracked in parallel.
- **Not robust to occlusion by itself.** An occluder that covers part of a window pulls the solution. The backward check and the window residual detect many of these cases but not all.

## Variants and improvements

- **Affine KLT.** Track with an affine warp of the window (6 parameters), or use the affine model only to check the translation result, as Shi and Tomasi do.
- **Gain and bias.** Add a scale and an offset of brightness to the unknowns, so that a change of exposure does not bias the shift.
- **Weighted windows.** Weight the pixels of the window with a Gaussian, so that pixels near the border of the window count less.
- **Robust losses.** Replace the squared difference by a robust function and solve by reweighted least squares, which reduces the pull of occluded pixels.
- **Median flow.** Track a grid of points inside a box, drop the half with the largest backward error, and move the box by the median of the remaining shifts; this is the tracker of [tracking-learning-detection](/tracking-learning-detection/).
- **Replenishing.** Run SELECT again every few frames in the regions without points, so that the number of tracks stays about constant; this is common in [visual odometry](/visual-odometry/).
- **Direct methods.** Align whole images or many pixels at once with a camera motion model instead of independent windows; see [direct image alignment](/direct-image-alignment/).

## When to use it

Use KLT when you need many point tracks over a short video with small motion between frames, for example for [visual odometry](/visual-odometry/), structure from motion, video stabilization or as the motion part of an object tracker. It is fast, needs no training and gives subpixel positions. Use descriptor matching instead when the frames are far apart in time or viewpoint, when the motion is larger than the pyramid can absorb, or when the scene changes in brightness or scale.

## Pitfalls

- **Too few levels.** A shift larger than about the radius of the window at the top level makes the solve converge to a wrong place, as in the example. Choose $L$ so that the largest expected shift divided by $2^L$ is a few pixels.
- **Too many levels.** At a coarse level the window covers a large part of the image, and other objects enter it. The occluder example shows a window that is clean at level 0 but wrong at level 2.
- **A threshold without a scale.** $\lambda_{\min}$ grows with the square of the contrast and with the window size. Make the threshold relative to the largest value, as SELECT does, or normalize the images.
- **Points at the border.** A window that leaves the image reads clamped values, which do not move with the scene. Drop points whose window leaves the image.
- **Drift.** Frame-to-frame tracking adds a small error at each frame. Over hundreds of frames the error grows; compare the window with its first appearance to detect it.
- **Coordinate conventions.** The pixel center is at $(u, v)$ here and at $(u + 1/2, v + 1/2)$ in some code. The pyramid map $u \mapsto 2u$ is right only for the first convention; with the second, it is $u + 1/2 \mapsto 2(u + 1/2)$. Mixing them biases every track by a fraction of a pixel per level.

## Implementations

## History

Lucas and Kanade (1981) gave the registration step: a Newton-type iteration on the squared difference between a window and its shifted copy. Tomasi and Kanade (1991), in a Carnegie Mellon technical report, used this step to track point features and chose the features where both eigenvalues of the 2 by 2 gradient matrix are large, because those are the windows where the step is well conditioned. Shi and Tomasi (1994) justified this rule and added a test of each feature against its first appearance with an affine model, to drop features that change. Bouguet described the pyramidal form with the propagation of the guess between levels in an Intel technical report that came with the OpenCV library, and that form is the one most programs use. Baker and Matthews (2004) put the step with the template gradient into their framework as the inverse compositional algorithm.

## References
