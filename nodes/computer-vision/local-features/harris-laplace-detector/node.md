---
tag: B4GHVB
kind: algorithm
slug: harris-laplace-detector
name: Harris-Laplace detector
aliases:
- scale-adapted Harris detector
area: computer-vision/local-features
level: advanced
summary: Find Harris corners at each scale and keep those whose scale is a maximum of the normalized Laplacian, giving scale-covariant corner points.
solves: [feature-detection]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, K: the number of scales, r: the radius of the largest Gaussian kernel}
  time: {worst: O(K W H r), average: O(K W H r), best: O(K W H r)}
  space: {extra: Θ(K W H)}
properties: {deterministic: true, exact: false, approximately_scale_invariant: true, rotation_invariant_response: true, heuristic: true}
history:
  year: 2001
  people: [Krystian Mikolajczyk, Cordelia Schmid]
  note: Mikolajczyk and Schmid presented the detector at ICCV 2001 and gave the full description, with the iterative and the simplified forms, in their 2004 journal paper.
prereqs: [harris-corner-detector, automatic-scale-selection]
see_also: [harris-affine-detector, determinant-of-hessian-detector, difference-of-gaussians-detector, laplacian-of-gaussian, scale-space-representation, sift, detector-repeatability, shi-tomasi-corner-detector]
sources:
  - paper: doi:10.1109/ICCV.2001.937561
    title: Krystian Mikolajczyk and Cordelia Schmid, Indexing based on scale invariant interest points, Proceedings of the Eighth IEEE International Conference on Computer Vision (ICCV 2001), 525-531, 2001
    locator: the sections on the scale-adapted Harris measure and the selection of the characteristic scale by the Laplacian
  - paper: doi:10.1023/B:VISI.0000027790.02288.f2
    title: Krystian Mikolajczyk and Cordelia Schmid, Scale and affine invariant interest point detectors, International Journal of Computer Vision 60(1), 63-86, 2004
    locator: Section 2 (Eq. 1 to 3 and Section 2.2, the Harris-Laplace detector)
  - paper: doi:10.1023/A:1008045108935
    title: Tony Lindeberg, Feature detection with automatic scale selection, International Journal of Computer Vision 30(2), 79-116, 1998
    locator: the sections on scale-normalized derivatives and the selection of scales
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the part on corner detectors (Harris-Laplace)
---

The Harris-Laplace detector solves [feature detection](/feature-detection/) for corner points that come with a scale. At each scale of a [scale space](/scale-space-representation/) it computes the [Harris](/harris-corner-detector/) measure from a second moment matrix built with derivatives at a differentiation scale and summed over an integration scale. It keeps the points that are spatial maxima of this measure. Then it keeps only the points where the scale-normalized [Laplacian of Gaussian](/laplacian-of-gaussian/) at the same pixel is larger than at the scale below and the scale above. The Harris measure places the point precisely on a corner, and the Laplacian picks the scale, by the rule of [automatic scale selection](/automatic-scale-selection/). When the image is magnified, the points move with the pattern and their scales grow by the same factor. The cost is $O(KWHr)$ for $K$ scales and kernels of radius at most $r$.

## In plain words

Look at the image through several blurs, from fine to coarse. At each blur, find the corners with the Harris test: places where the brightness changes in two directions. A corner at one blur may also show up at the next blur, a little moved. To choose the right size for each corner, use a second measure that says how much the area around the point looks like a spot of that size. Keep a corner only at the blur where this second measure is larger than at the blur just below and just above it. Each kept corner then has a position and a size. If the same scene is photographed closer, the same corners come back, with sizes that grow in step with the zoom.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows of real values in $[0, 1]$. A pixel has coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down, and $x$ and $y$ name the derivatives along $u$ and $v$. $L(\cdot, \sigma)$ is $I$ smoothed by a Gaussian of standard deviation $\sigma$; this page uses a sampled Gaussian cut at $3\sigma$, separable, with the clamp border rule.

The parameters are the first scale $\sigma_0$, the ratio $\xi > 1$ between scales, the number of scales $K \ge 3$, the factor $s \in (0, 1]$ between the differentiation and the integration scale, the Harris constant $\alpha$, and two thresholds $\tau_H$ and $\tau_L$. Mikolajczyk and Schmid use $\xi = 1.4$ and $s = 0.7$. They do not fix $\alpha$; this page uses $\alpha = 0.06$, $\sigma_0 = 1$, $K = 6$, $\tau_H = 10^{-5}$ and $\tau_L = 0.05$.

The scales are $\sigma_n = \sigma_0 \xi^n$. At scale $\sigma_n$ the integration scale is $\sigma_I = \sigma_n$ and the differentiation scale is $\sigma_D = s\sigma_n$. The scale-adapted second moment matrix is

$$\mu_n = \sigma_D^2\, g(\sigma_I) \ast \begin{pmatrix} L_x^2 & L_x L_y \\ L_x L_y & L_y^2 \end{pmatrix},$$

where $L_x$ and $L_y$ are derivatives of $L(\cdot, \sigma_D)$ and $g(\sigma_I) \ast$ is a Gaussian sum with standard deviation $\sigma_I$. The factor $\sigma_D^2$ makes the values at different scales comparable. The Harris measure is $R_n = \det \mu_n - \alpha (\operatorname{tr} \mu_n)^2$ and the normalized Laplacian is $F_n = \sigma_n^2 \lvert L_{xx} + L_{yy} \rvert$, both at scale $\sigma_n$. The output is the list of points $(u, v, \sigma_n)$ that pass the two tests of line L7 below.

## The algorithm

```pseudo id=main
HARRIS-LAPLACE(I, σ_0, ξ, K, s, α, τ_H, τ_L)
L1  for n ← 0 to K - 1 do σ_n ← σ_0 ξ^n
L2      μ_n ← σ_D² g(σ_n) ∗ [L_x², L_x L_y; L_x L_y, L_y²] with L = g(σ_D) ∗ I and σ_D = s σ_n
L3      R_n ← det μ_n - α (tr μ_n)²
L4      F_n ← σ_n² |L_xx + L_yy| with L = g(σ_n) ∗ I
L5  points ← ∅
L6  for each (u, v, n) with 1 ≤ n ≤ K - 2 and (u, v) off the border do
L7      if R_n(u, v) > τ_H, R_n(u, v) > R_n at the 8 neighbours, F_n(u, v) > τ_L, F_n(u, v) > F_(n-1)(u, v) and F_n(u, v) > F_(n+1)(u, v) then
L8          add (u, v, σ_n) to points
L9  return points
```

Line L2 uses central differences, $L_x \approx \frac12\big(L(u + 1, v) - L(u - 1, v)\big)$ and the same in $v$. Line L4 uses the five-point Laplacian $L(u + 1, v) + L(u - 1, v) + L(u, v + 1) + L(u, v - 1) - 4L(u, v)$. Line L7 joins the two parts of the detector: the Harris test is spatial, at one scale, and the Laplacian test is over scale, at one pixel. The point need not be a spatial maximum of $F$, and it need not be a maximum of $R$ over scale.

This is the simplified form of the detector. The iterative form of the 2004 paper starts from the same points and, for each point, searches a finer range of scales around $\sigma_n$ for the extremum of the Laplacian, then moves the point to the Harris maximum at the new scale, and repeats until the point and the scale stop changing.

## Example

Take a $28 \times 28$ image that is $0$ except for a white square of side 9, with $10 \le u, v \le 18$. The scales are $\sigma_n = 1.4^n$ for $n = 0, \dots, 5$: $1$, $1.4$, $1.96$, $2.744$, $3.842$ and $5.378$. At two pixels the values are:

| $\sigma_n$ | 1 | 1.4 | 1.96 | 2.744 | 3.842 | 5.378 |
|---|---|---|---|---|---|---|
| $R_n(11, 11) \times 10^4$ | 2.607 | 5.081 | 6.553 | 7.605 | 6.706 | 2.892 |
| $F_n(11, 11)$ | 0.3541 | **0.3996** | 0.3468 | 0.2991 | 0.3259 | 0.3356 |
| $R_n(14, 14) \times 10^4$ | 0.000 | 0.043 | 1.722 | 8.441 | 9.737 | 3.840 |
| $F_n(14, 14)$ | 0.0000 | 0.0339 | 0.2639 | 0.6139 | **0.7135** | 0.5620 |

The pixel $(11, 11)$ is one step inside the top left corner. It is a spatial maximum of $R_1$, and $F_1 = 0.3996$ is larger than $F_0$ and $F_2$, so it is kept with $\sigma = 1.4$. It is also a spatial maximum of $R$ at larger scales, but there $F$ is not a maximum over scale. The center $(14, 14)$ has $R = 0$ at the smallest scale, where the square looks flat inside. At $\sigma_4 = 3.842$ the whole square fits in the window, $R_4$ is a spatial maximum and $F_4 = 0.7135$ is a maximum over scale. The detector returns five points: the four corners $(11, 11)$, $(17, 11)$, $(11, 17)$ and $(17, 17)$ at $\sigma = 1.4$, and the center $(14, 14)$ at $\sigma = 3.842$, which marks the square as a whole.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that lines L6 to L8 return exactly the points with the two properties of line L7. It shows that under a magnification of the image by $f$, in the continuous setting, $\mu$, $R$ and $F$ at the corresponding point and the scale $f\sigma$ are the same as before, so a selected point $(\mathbf x, \sigma)$ becomes $(f\mathbf x, f\sigma)$. It also shows that for a Gaussian blob of standard deviation $\sigma_b$ the normalized Laplacian at the center has its single maximum over scale at $\sigma = \sigma_b$. On the grid, a blob with $\sigma_b = 1.4^n$ for $n = 1, \dots, 4$ gives one point, at its center, with exactly that scale.

That the points are repeatable on real images is measured, not proved. In the experiments of the 2004 paper, on 160 images, Harris-Laplace finds 68 percent of its points again at a scale factor of 1.4; see [detector repeatability](/detector-repeatability/).

## Complexity

The model is the real RAM. Let $r = \lceil 3\sigma_{K-1} \rceil$ be the radius of the largest kernel.

- Lines L2 and L4 are four blurs for $\mu_n$ and one for $F_n$, each separable, $O(WHr)$ per scale.
- Line L3 is $O(WH)$ per scale.
- Lines L6 to L8 make at most 10 comparisons per sample, $O(KWH)$.

The total time is $O(KWHr)$, and the stacks of $R$ and $F$ take $\Theta(KWH)$ space. A pyramid that halves the image when the scale doubles makes the large kernels run on small images. The iterative form adds a small search in scale for each point.

## Properties

- **Scale.** Under a magnification by $f$ the points move to $f$ times their position, with $f$ times their scale, up to the sampling of scales by $\xi$.
- **Rotation.** $\det \mu$, $\operatorname{tr}\mu$ and the Laplacian do not change under a rotation of the coordinates, so neither do $R$ and $F$. On the grid this is exact for rotations by $90°$.
- **Brightness.** An offset changes neither $R$ nor $F$. A gain $g$ multiplies $R$ by $g^4$ and $F$ by $g$, so it changes only which points pass the thresholds.
- **Localization.** The point is a Harris maximum, so it sits near the corner. A blob detector such as the [DoG](/difference-of-gaussians-detector/) puts its point at the center of a region instead.
- **Fewer points per corner.** A corner is a Harris maximum at many scales, but usually the Laplacian has a maximum over scale at only one or two of them.
- **Not affine invariant.** The window is a circle. Under a change of viewpoint it covers different parts of the scene; the [Harris-affine detector](/harris-affine-detector/) adapts the window to an ellipse.

## Variants and improvements

- **Iterative form.** Search a finer set of scales around each point, from $0.7\sigma_n$ to $1.4\sigma_n$ in the paper, and move the point to the Harris maximum at the new scale until it is stable. This gives more accurate scales at a higher cost.
- **Hessian-Laplace.** Use the [determinant of the Hessian](/determinant-of-hessian-detector/) for the position and the Laplacian for the scale. It finds blobs, not corners.
- **Harris-affine.** Start from Harris-Laplace points and adapt the shape of the window to the local structure.
- **Scale-space maxima of the Harris measure.** Take maxima of $R$ in space and scale together. At the square corner of the example $R$ has its maximum over scale at $\sigma = 2.744$, two levels away from the scale the Laplacian picks; Mikolajczyk and Schmid chose the Laplacian for the scale.

## When to use it

Use it when points must be found again after a change of scale and should sit on corners rather than at the centers of blobs, for example on images of buildings and objects with straight edges. For large changes of viewpoint use the Harris-affine or [MSER](/maximally-stable-extremal-regions/) detector. When speed matters more than localization on corners, the DoG detector of [SIFT](/sift/) is a common choice.

## Pitfalls

- **Sharp corners have no scale of their own.** A straight corner looks the same at every magnification, so in the continuous case the Laplacian at its apex has no maximum over scale. On the grid the only size left is the pixel: a lone corner of a quarter plane gives a point one pixel inside the corner, at $\sigma = 1.4$, the same as each corner of the square in the example. The selected scale of such a corner depends on the sampling, not on the scene.
- **Missing normalization.** Without the factors $\sigma_D^2$ and $\sigma_n^2$ the values fall with the scale and the selection always takes the finest scale.
- **Equal neighbours.** The spatial test is strict. A symmetric pattern of even width can give two equal neighbours, and then neither is kept. Break ties by a fixed order if this matters.
- **Too few scales.** The finest and coarsest scales cannot hold a point, because the test needs a scale on each side.
- **Thresholds depend on the range.** $\tau_H$ scales with the fourth power of the contrast and $\tau_L$ with the contrast. Set them for the range of the image values.
- **Small $s$.** A differentiation scale much smaller than the integration scale makes the derivatives noisy; a value near 1 smooths the corner away. Values from 0.5 to 0.75 are usual.

## Implementations

## History

Krystian Mikolajczyk and Cordelia Schmid presented the detector at ICCV 2001, for indexing images under changes of scale. It joins two older ideas: the corner measure of Harris and Stephens from 1988, and the scale selection by maxima of normalized derivatives that Tony Lindeberg developed in the 1990s. Their 2004 journal paper gave the iterative and the simplified forms, the parameters $\xi = 1.4$ and $s = 0.7$, and the extension to affine shapes, the Harris-affine detector. The Harris-affine detector was one of the detectors in the comparison of affine region detectors of 2005.

## References
