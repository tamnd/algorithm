---
tag: 698GJR
kind: algorithm
slug: determinant-of-hessian-detector
name: Determinant of Hessian detector
aliases:
- Hessian blob detector
- DoH detector
area: computer-vision/local-features
level: advanced
summary: Find blobs as scale-space maxima of the scale-normalized determinant of the Hessian of the smoothed image.
solves: [feature-detection]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, K: the number of scales, r: the radius of the largest Gaussian kernel}
  time: {worst: O(K W H r), average: O(K W H r), best: O(K W H r)}
  space: {extra: Θ(K W H)}
properties: {deterministic: true, exact: false, approximately_scale_invariant: true, rotation_invariant_response: true, heuristic: true}
history:
  year: 1998
  people: [Tony Lindeberg]
  note: Beaudet proposed the determinant of the Hessian as an interest operator in 1978; Lindeberg added the scale normalization and the selection of scales in his 1998 paper on automatic scale selection.
prereqs: [scale-space-representation, automatic-scale-selection]
see_also: [difference-of-gaussians-detector, laplacian-of-gaussian, surf, harris-affine-detector, harris-laplace-detector, sift, integral-image, detector-repeatability]
sources:
  - paper: doi:10.1023/A:1008045108935
    title: Tony Lindeberg, Feature detection with automatic scale selection, International Journal of Computer Vision 30(2), 79-116, 1998
    locator: the sections on blob detection (the scale-normalized Laplacian and the scale-normalized determinant of the Hessian, and the scale selected for a Gaussian blob)
  - paper: doi:10.1016/j.cviu.2007.09.014
    title: Herbert Bay, Andreas Ess, Tinne Tuytelaars and Luc Van Gool, Speeded-up robust features (SURF), Computer Vision and Image Understanding 110(3), 346-359, 2008
    locator: the section on the fast Hessian detector (box filters on an integral image)
  - paper: doi:10.1007/s11263-005-3848-x
    title: Krystian Mikolajczyk, Tinne Tuytelaars, Cordelia Schmid, Andrew Zisserman, Jiri Matas, Frederik Schaffalitzky, Timor Kadir and Luc Van Gool, A comparison of affine region detectors, International Journal of Computer Vision 65(1-2), 43-72, 2005
    locator: the section on the Hessian-affine detector
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the part on blob detectors (the Hessian detector)
---

The determinant of Hessian detector, or DoH detector, solves [feature detection](/feature-detection/) for blobs. It smooths the image with Gaussians of variance $t$ over a range of scales, computes at each point and scale the Hessian matrix of second derivatives, and takes the scale-normalized determinant $t^2 (L_{xx} L_{yy} - L_{xy}^2)$ as the response. The points are the positive maxima of the response in space and scale, and the scale of the maximum gives the size of the blob. The determinant is large only where the image curves strongly in two directions, so it does not respond to straight edges and needs no edge test, unlike the [DoG detector](/difference-of-gaussians-detector/). It is the second of the two blob measures in Lindeberg's theory of [automatic scale selection](/automatic-scale-selection/), next to the [Laplacian of Gaussian](/laplacian-of-gaussian/). [SURF](/surf/) computes an approximation of it with box filters. The cost is $O(KWHr)$ for $K$ scales and kernels of radius at most $r$.

## In plain words

Blur the image by several amounts. At each point and each blur, measure how the brightness bends: how much it curves left to right, top to bottom, and diagonally. Combine these three numbers into one, the determinant, which is large only when the brightness bends the same way in every direction, as on the top of a hill or the bottom of a bowl. A bright spot is a hill and a dark spot is a bowl, so both give a large value. An edge bends in one direction only and gives zero. Multiply by the square of the blur, so that small and large spots can be compared fairly. A spot is found where this value is larger than at all neighbours, in the image and across the blurs. The blur at that point gives the size of the spot.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows of real values. A pixel has coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down, and $x$ and $y$ name the derivatives along $u$ and $v$. The [scale space](/scale-space-representation/) is $L(\cdot, t) = g_t \ast I$, where $g_t$ is the Gaussian of variance $t = \sigma^2$; this page uses a sampled Gaussian cut at $3\sigma$ and the clamp border rule. The parameters are an increasing list of scales $t_1 < \dots < t_K$, best with a constant ratio, and a threshold $\tau \ge 0$.

The Hessian of $L$ is $\mathcal H L = \begin{pmatrix} L_{xx} & L_{xy} \\ L_{xy} & L_{yy} \end{pmatrix}$, and the scale-normalized determinant is

$$D(u, v, t) = t^2 \det \mathcal H L = t^2 \big(L_{xx} L_{yy} - L_{xy}^2\big).$$

The factor $t^2$ is $t^{\gamma}$ for each of the two derivatives, with $\gamma = 1$: each derivative of order 2 is multiplied by $t$. With this factor, a pattern and the same pattern magnified by $s$ give the same maximum value, at scales that differ by $s^2$. The output is the list of samples where $D > \tau$ and $D$ is larger than at all 26 neighbours in space and scale, refined to sub-sample position and scale.

## The algorithm

```pseudo id=main
DOH(I, t_1, …, t_K, τ)                ▷ I is W × H, t_1 < … < t_K
L1  for i ← 1 to K do L_i ← g_(t_i) ∗ I                    ▷ separable Gaussian, clamp border
L2      D_i(u, v) ← t_i² (L_xx L_yy - L_xy²) at each pixel, with central second differences
L3  blobs ← ∅
L4  for each sample (u, v, i) with 2 ≤ i ≤ K - 1, off the border, D_i(u, v) > τ and larger than all 26 neighbours do
L5      refine u, v and log t by a parabola through the sample and its two neighbours in each direction
L6      add (x̂, ŷ, t̂) to blobs
L7  return blobs
```

Line L2 uses $L_{xx} \approx L(u + 1, v) - 2L(u, v) + L(u - 1, v)$, the same in $v$ for $L_{yy}$, and $L_{xy} \approx \frac14 \big(L(u + 1, v + 1) - L(u - 1, v + 1) - L(u + 1, v - 1) + L(u - 1, v - 1)\big)$. Line L4 keeps only positive maxima. A positive determinant means that both curvatures have the same sign: a bright blob, with both negative, and a dark blob, with both positive, are both maxima of $D$. A negative determinant is a saddle. Line L5 fits a parabola in each of the three directions separately; in scale it uses $\log t$, since the scales are spaced by a constant ratio.

## Example

Take a $32 \times 32$ image of a Gaussian blob $I = \exp(-((u - 16)^2 + (v - 16)^2) / (2 t_0))$ with $t_0 = 4$, and the scales $t_i = 2^{i/2}$ for $i = 0, \dots, 8$, from $1$ to $16$. The smoothed blob is a Gaussian of variance $t_0 + t$, and in the continuous case the center value of $D$ is

$$D(16, 16, t) = \frac{t_0^2\, t^2}{(t_0 + t)^4},$$

which is largest at $t = t_0$, with the value $1/16 = 0.0625$. The discrete values at the center are:

| $t$ | 1 | 1.41 | 2 | 2.83 | 4 | 5.66 | 8 | 11.3 | 16 |
|---|---|---|---|---|---|---|---|---|---|
| computed $D$ | 0.0232 | 0.0340 | 0.0455 | 0.0548 | 0.0590 | 0.0560 | 0.0475 | 0.0361 | 0.0251 |
| continuous $D$ | 0.0256 | 0.0372 | 0.0494 | 0.0589 | 0.0625 | 0.0589 | 0.0494 | 0.0372 | 0.0256 |

The largest computed value is at $t = 4$, and the parabola in $\log t$ gives $\hat t = 4.12$. The detector returns one blob, at $(16, 16)$ with $\hat t = 4.12$. The computed values are about 5 percent low because the second differences of a sampled Gaussian are smaller than the derivatives. For $t_0 = 2$ and $t_0 = 8$ the selected scales are $2.12$ and $8.13$. A dark blob on a white background gives the same point with the same value, and a straight edge gives $D = 0$ everywhere, since $L_{yy} = L_{xy} = 0$ across a vertical edge.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that line L4 returns exactly the strict positive maxima among the 26 neighbours, that the parabola step returns the exact vertex of a parabola, and that for a Gaussian blob of variance $t_0$ the continuous response at the center has its single maximum over $t$ at $t = t_0$, so the selected scale equals the size of the blob. It also shows the reason for the normalization: under a magnification of the image by $s$, $D$ at the corresponding point and the scale $s^2 t$ is the same, so maxima over scale move with the size of the pattern.

That the maxima are useful points on real images is measured, not proved. In the comparison of Mikolajczyk and others, the Hessian based detectors are among the most repeatable; see [detector repeatability](/detector-repeatability/).

## Complexity

The model is the real RAM. Let $r$ be the radius of the largest kernel, $3\sqrt{t_K}$.

- Line L1 is a separable blur, $O(WHr)$ per scale.
- Line L2 costs $O(WH)$ per scale.
- Line L4 makes at most 26 comparisons per sample, $O(KWH)$.
- Line L5 is $O(1)$ per blob.

The total time is $O(KWHr)$, and the stack takes $\Theta(KWH)$ space. Two things lower the cost in practice. A pyramid halves the image when $t$ grows by 4, so the larger kernels run on smaller images. SURF replaces the Gaussian second derivatives by box filters, which an [integral image](/integral-image/) evaluates in $O(1)$ per pixel for any size, so the cost is $O(KWH)$.

## Properties

- **No edge response.** On a straight edge one curvature is zero and so is $D$. The DoG and the Laplacian respond to edges and need a separate edge test.
- **Both polarities.** Bright and dark blobs both give positive maxima. The sign of the Laplacian $L_{xx} + L_{yy}$ at the point tells them apart.
- **Scale.** The normalization makes the selected scale proportional to the size of the pattern. For a Gaussian blob it is exactly $t_0$.
- **Rotation.** The determinant of the Hessian does not change under a rotation of the coordinates. On the pixel grid it changes slightly; for rotations by $90°$ it is exact.
- **Brightness.** An offset does not change $D$. A gain $g$ multiplies $D$ by $g^2$.
- **Corners.** $D$ is also positive near the corners of objects, where the smoothed image bends in two directions. On a square of side 12, the scales up to 16 give maxima near the four corners and none at the center, whose scale is larger.

## Variants and improvements

- **Fast Hessian.** SURF approximates $L_{xx}$, $L_{yy}$ and $L_{xy}$ by box filters on an integral image, and uses $D_{xx} D_{yy} - (0.9 D_{xy})^2$, where the factor corrects for the box approximation.
- **Hessian-Laplace.** Choose the position by the determinant of the Hessian and the scale by the Laplacian, as in the [Harris-Laplace detector](/harris-laplace-detector/) with the Hessian in place of the Harris measure.
- **Hessian-affine.** Adapt an elliptical shape to each Hessian point by the second moment matrix, as in the [Harris-affine detector](/harris-affine-detector/).
- **Laplacian.** Use $t(L_{xx} + L_{yy})$, the trace instead of the determinant, which is the [Laplacian of Gaussian](/laplacian-of-gaussian/) blob detector, or its DoG approximation.
- **Better localization.** Fit a full quadratic in $(u, v, \log t)$, as the DoG detector does, instead of three separate parabolas.

## When to use it

Use it to find blobs at all scales when straight edges must not give points, for example on images of man-made scenes. With box filters it is the detector of SURF and is among the fastest scale invariant detectors. For matching under large changes of viewpoint, add affine adaptation (Hessian-affine) or use [MSER](/maximally-stable-extremal-regions/).

## Pitfalls

- **Missing normalization.** Without the factor $t^2$, $D$ decreases with $t$ for every pattern, and the largest value is always at the smallest scale.
- **Taking minima.** Negative values of $D$ are saddles, not blobs. Search for positive maxima only.
- **Too few scales.** A maximum needs a scale below and above. The smallest and largest scales cannot hold a blob, so the range must extend past the sizes of interest.
- **Unequal steps in scale.** The parabola in $\log t$ assumes a constant ratio between scales. With unequal steps, fit with the actual spacing.
- **Sampling.** For small $t$, the sampled Gaussian and the differences are poor, and the selected scale is biased. Start at $t \ge 1$ or upsample the image.

## Implementations

## History

Paul Beaudet proposed the determinant of the Hessian as a rotation invariant interest operator in 1978, at a single scale. Tony Lindeberg built the theory of scale selection in the 1990s and showed in his 1998 paper that the scale-normalized determinant and the scale-normalized Laplacian, with $\gamma = 1$, select the scale of a blob, and he used both as blob detectors. Mikolajczyk and Schmid used the Hessian in the Hessian-Laplace and Hessian-affine detectors, and Bay and others made it fast with box filters in SURF in 2006, with the journal version in 2008.

## References
