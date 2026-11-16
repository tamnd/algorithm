---
tag: 832KGB
kind: algorithm
slug: difference-of-gaussians-detector
name: Difference-of-Gaussians detector
aliases:
- DoG detector
- DoG keypoint detector
area: computer-vision/local-features
level: core
summary: Find blobs as extrema in space and scale of the difference of adjacent Gaussian smoothed images, a cheap approximation of the scale-normalized Laplacian.
solves: [feature-detection]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, s: the number of scales per octave}
  time: {worst: O(s W H), average: O(s W H), best: O(s W H)}
  space: {extra: Θ(s W H)}
properties: {deterministic: true, exact: false, approximately_scale_invariant: true, rotation_invariant_response: true, heuristic: true}
history:
  year: 2004
  people: [David G. Lowe]
  note: Lowe used DoG extrema as the keypoints of SIFT in 1999 and gave the full detector, with the quadratic fit and the edge test, in his 2004 journal paper.
prereqs: [scale-space-representation, automatic-scale-selection, laplacian-of-gaussian, gaussian-pyramid]
see_also: [sift, determinant-of-hessian-detector, harris-laplace-detector, maximally-stable-extremal-regions, detector-repeatability, invariant-local-features, gaussian-filter, surf]
sources:
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: Section 3 (the DoG and its relation to the scale-normalized Laplacian, the 26 neighbours, the choice of 3 scales per octave and sigma = 1.6), Section 4 (the quadratic fit and the contrast threshold 0.03), Section 4.1 (the edge test with r = 10)
  - paper: doi:10.1023/A:1008045108935
    title: Tony Lindeberg, Feature detection with automatic scale selection, International Journal of Computer Vision 30(2), 79-116, 1998
    locator: the sections on blob detection with the scale-normalized Laplacian
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the part on blob detectors (the Laplacian, the DoG and the Hessian)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Section 7.1.1, Feature detectors (scale invariance and the DoG)
---

The Difference-of-Gaussians detector, or DoG detector, solves [feature detection](/feature-detection/) for blobs at all scales. It blurs the image with [Gaussians](/gaussian-filter/) of growing width $\sigma$, subtracts each blurred image from the next, and keeps the points that are larger or smaller than all 26 neighbours in space and in scale. Each kept point is refined to sub-pixel position and sub-level scale by a quadratic fit, and points with low contrast or on edges are dropped. The difference of two Gaussians of widths $\sigma$ and $k\sigma$ is close to $(k - 1)$ times the scale-normalized [Laplacian of Gaussian](/laplacian-of-gaussian/), so the detector is a fast form of Lindeberg's [automatic scale selection](/automatic-scale-selection/) with the Laplacian. This page is the detector only. The [SIFT](/sift/) page covers the whole pipeline, which adds an orientation and a descriptor to each DoG keypoint and matches them. The cost is $O(sWH)$ for $s$ scales per octave.

## In plain words

Blur the image a little, then a little more, and so on. Subtract each blurred copy from the next one. What is left is strong where the image has a spot about the size of the blur: a bright spot gives a deep valley, a dark spot a high peak. A spot of a given size gives its strongest answer at the blur that matches its size. So look for the points that are stronger than everything around them, both in the image and in the list of blurs. Each such point gives a position and a size. Then throw away the weak ones and the ones that lie along an edge, because their position along the edge is not well defined. To save time, halve the image each time the blur doubles.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows and values in $[0, 1]$. A pixel has coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down, and its center is at the integer point $(u, v)$. The blur uses the clamp border rule. The parameters are the number $s$ of scales per octave, the base scale $\sigma_0$, the number of octaves $O$, the contrast threshold $c$, and the edge ratio $r$. Lowe uses $s = 3$, $\sigma_0 = 1.6$, $c = 0.03$ and $r = 10$, and he assumes that the input already has a blur of $0.5$.

The Gaussian [scale space](/scale-space-representation/) is $L(\cdot, \sigma) = G_\sigma \ast I$, and the difference of Gaussians is

$$D(u, v, \sigma) = L(u, v, k\sigma) - L(u, v, \sigma), \qquad k = 2^{1/s}.$$

Since the Gaussian solves the [heat equation](/heat-equation/) $\partial G / \partial \sigma = \sigma \nabla^2 G$, the difference quotient gives

$$G_{k\sigma} - G_\sigma \approx (k - 1)\, \sigma^2 \nabla^2 G_\sigma ,$$

so $D$ is the scale-normalized Laplacian $\sigma^2 \nabla^2 L$ times the constant $k - 1$. The constant is the same at all scales and does not move the extrema. The output is a list of keypoints $(x, y, \sigma)$ in the pixel units of the input, each with the value of $D$ at the point.

## The algorithm

```pseudo id=main
DOG-DETECTOR(I, s, σ0, O, c, r)       ▷ I is W × H with values in [0, 1]
L1  base ← I blurred from the assumed 0.5 to σ0
L2  for o ← 0 to O - 1 do
L3      G_i ← base blurred to σ0 k^i for i = 0, …, s + 2        ▷ k = 2^(1/s), in the pixels of octave o
L4      D_i ← G_(i+1) - G_i for i = 0, …, s + 1
L5      for each sample (u, v, i) with 1 ≤ i ≤ s, off the border, larger than all 26 neighbours or smaller than all of them do
L6          fit a quadratic to D at the sample; while an offset is above 0.5, move to the neighbour sample and fit again (at most 5 times)
L7          if |D(fitted point)| ≥ c and tr(H)² · r < (r + 1)² · det(H) with det(H) > 0 then
L8              add (2^o x̂, 2^o ŷ, σ0 2^(o + î/s)) to keypoints
L9      base ← G_s sampled at every second pixel
L10 return keypoints
```

Lines L3 and L4 build one octave: $s + 3$ Gaussian images and $s + 2$ DoG images. Line L5 looks for extrema only in the $s$ middle DoG images, because each needs a level above and below, and these $s$ levels cover one doubling of $\sigma$. A sample is compared with its 8 neighbours in its own level and the 9 neighbours in each of the two levels next to it.

Line L6 is the fit of Brown and Lowe. With the gradient $g$ and the $3 \times 3$ Hessian $\mathcal H$ of $D$ in $(u, v, i)$, taken by central differences, the second order Taylor expansion $D(\mathbf x) \approx D + g^{\mathsf T} \mathbf x + \tfrac12 \mathbf x^{\mathsf T} \mathcal H \mathbf x$ has its vertex at $\hat{\mathbf x} = -\mathcal H^{-1} g$, with the value $D + \tfrac12 g^{\mathsf T} \hat{\mathbf x}$. If any component of $\hat{\mathbf x}$ is above $0.5$, the vertex is nearer to another sample, and the fit moves there. Line L7 drops points with low contrast and points on edges. The edge test uses the $2 \times 2$ spatial Hessian $H = \begin{pmatrix} D_{uu} & D_{uv} \\ D_{uv} & D_{vv} \end{pmatrix}$: its eigenvalues are the curvatures of $D$ across and along the point, and the ratio $\operatorname{tr}(H)^2 / \det H = (\alpha + \beta)^2 / (\alpha\beta)$ grows with the ratio of the eigenvalues. The test keeps the point when the ratio of the curvatures is below $r$, without an eigenvalue computation. Line L9 starts the next octave. Image $s$ of the octave has blur $2\sigma_0$, so every second pixel of it has blur $\sigma_0$ in the new pixel units.

The implementation blurs each $G_i$ directly from the base by $\sqrt{\sigma_i^2 - \sigma_0^2}$. Lowe blurs each image from the previous one; the two agree because blurs add in squares, up to the cut of the kernels.

## Example

Take a $32 \times 32$ image of a bright Gaussian blob of width $\sigma_b = 3$ and height $1$, centered at $(16, 16)$, on a black background. Use $s = 3$, $\sigma_0 = 1.6$ and two octaves. The levels of the first octave have $\sigma_i = 1.6, 2.016, 2.540, 3.2, 4.032$. At the center the five DoG values are

$$-0.0933, \; -0.1096, \; -0.1186, \; -0.1141, \; -0.0993 .$$

The smallest is at $i = 2$, and it is smaller than all 26 neighbours, so $(16, 16, 2)$ is a candidate. The fit stays at $(16, 16)$ by symmetry and moves the level to $\hat\imath = 2.166$, so $\sigma = 1.6 \cdot 2^{2.166/3} = 2.639$, with $D = -0.1188$. The contrast is above $0.03$ and the blob is round, so the point passes. It is the only keypoint. An inverted image, a dark blob on white, gives the same point with $D = +0.1188$.

The scale is not $3$, and the reason is exact. The blurred blob has variance $t_0 + t$ with $t_0 = \sigma_b^2 - 0.5^2 = 8.75$, since the detector assumes the input blur $0.5$. At the center, $D$ is proportional to $\frac{1}{t_0 + t} - \frac{1}{t_0 + k^2 t}$ with $t = \sigma^2$, and the derivative in $t$ is zero at $t = t_0 / k$. So the DoG between $\sigma$ and $k\sigma$ peaks when the geometric mean $\sigma \sqrt{k}$ of the two widths matches the blob: $\sigma = \sqrt{8.75 / 2^{1/3}} = 2.635$, close to the fitted $2.639$.

Three other inputs show the limits. A straight vertical edge gives candidates along the edge, and all fail the edge test. The same blob with height $0.2$ gives $|D| < 0.03$ and no keypoint. A blob with $\sigma_b = 2$ peaks at $\sigma = 1.73$, below the first searched level $\sigma_0 k = 2.016$, and is not found; this is why Lowe doubles the input image before the first octave.

## Correctness

The detector finds what it defines: the samples of $D$ that are strict extrema among their 26 neighbours, refined by the fit and filtered by the two tests. The proof in [proofs/correctness.md](proofs/correctness.md) shows that line L5 finds exactly those samples, that the fit of line L6 returns the exact vertex when $D$ is a quadratic near the point, and that the edge test keeps exactly the points with $\det H > 0$ and a ratio of curvatures below $r$.

Why the extrema are the right points is a result of scale-space theory. Lindeberg showed that the extrema over scale of the scale-normalized Laplacian select a scale proportional to the size of a blob, and the derivation above shows that $D$ is that operator up to a constant. For a Gaussian blob the selection is exact, as the example computes. That the points are repeatable on real images is measured, not proved; see [detector repeatability](/detector-repeatability/).

## Complexity

The model is the real RAM. Let $N = WH$.

- With $\sigma_0$ fixed, each blur uses a kernel of constant size, so lines L3 and L4 cost $O(sN)$ in the first octave.
- Line L5 makes at most 26 comparisons per DoG sample, $O(sN)$.
- Lines L6 to L8 cost $O(1)$ per candidate, at most 5 solves of a $3 \times 3$ system.
- Each octave has a quarter of the pixels of the one before, so the octaves together cost at most $\frac{4}{3}$ times the first one.

The total time is $O(sWH)$, and the space is $\Theta(sWH)$ for the images of one octave. Doubling the input before the first octave, as Lowe does, multiplies the cost by about 4.

## Properties

- **Approximately scale invariant.** A change of scale of the image by $2^{j/s}$ moves the extrema $j$ levels, up to the sampling of space. Other factors fall between levels, where the fit finds them.
- **Rotation.** The Gaussian and the Laplacian are isotropic, so the response does not change under rotation, up to the sampling grid.
- **Brightness.** An offset does not change $D$. A gain multiplies $D$ and so changes which points pass the contrast threshold.
- **Blobs, not corners.** The response is large at the center of a spot of the matching size. Corners give a weaker response near the corner, and edges are removed by the edge test.
- **Both polarities.** Bright blobs give minima and dark blobs give maxima, and both are kept.
- **Approximation.** The DoG is close to the scale-normalized Laplacian only for $k$ near $1$. For the Gaussian blob the peak is at $\sigma^2 = t_0/k$ instead of $t_0$, a fixed factor that is the same for every blob and so does not hurt the invariance.

## Variants and improvements

- **Laplacian of Gaussian.** Compute $\sigma^2 \nabla^2 L$ directly, as in Lindeberg's blob detector. It is more costly and the extrema are almost the same.
- **Determinant of the Hessian.** Use $\sigma^4 \det \mathcal H L$, which does not respond to edges and needs no edge test. See the [DoH detector](/determinant-of-hessian-detector/), and [SURF](/surf/) for a fast box-filter form.
- **Harris-Laplace.** Choose the position by the Harris response and only the scale by the Laplacian. See the [Harris-Laplace detector](/harris-laplace-detector/).
- **Affine shape.** Adapt an ellipse to each point by the second moment matrix, as in the [Harris-affine detector](/harris-affine-detector/).
- **Nonlinear scale space.** KAZE replaces the Gaussian by a nonlinear diffusion that keeps edges sharp.

## When to use it

Use it to find keypoints for matching between images taken at different scales and rotations: panoramas, structure from motion, object recognition. It is the standard choice when the SIFT descriptor follows. For real-time work FAST or a box-filter Hessian is faster. For large viewpoint changes, add affine adaptation or use [MSER](/maximally-stable-extremal-regions/).

## Pitfalls

- **Missing small blobs.** The first searched level is $\sigma_0 k$, so blobs smaller than that are lost. Double the image before the first octave, as Lowe does.
- **Wrong input range.** The threshold $0.03$ assumes values in $[0, 1]$ and $s = 3$. For 8-bit values, scale it by 255, and for other $s$, by $(k - 1)$ relative to $2^{1/3} - 1$.
- **Strict comparison.** The test must be strict: on a flat area every sample equals its neighbours, and a test with $\ge$ would return every sample.
- **Skipping the move in the fit.** If an offset is above $0.5$ and the fit does not move, the refined point can be far from the sample and wrong.
- **Wrong blur of the next octave.** The next octave starts from image $s$, the one with blur $2\sigma_0$, not from the last image $s + 2$.

## Implementations

## History

The difference of Gaussians was used as a model of center-surround receptive fields in the retina, and as a band-pass pyramid in early image analysis. Lindeberg's scale-space theory of the 1990s gave the scale-normalized Laplacian and the rule to select scales at its extrema. Lowe used the DoG as a fast approximation of that operator for the keypoints of SIFT, first at ICCV 1999 and in full in his 2004 journal paper, which also added the quadratic fit, after Brown and Lowe (2002), and the edge test. The DoG detector became the most used scale invariant keypoint detector of the next decade.

## References
