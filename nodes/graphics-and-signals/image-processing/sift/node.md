---
tag: P9C537
kind: algorithm
slug: sift
name: Scale-invariant feature transform
aliases:
- SIFT
area: graphics-and-signals/image-processing
level: advanced
summary: Find keypoints at the extrema of a difference of Gaussians over scale and space, give each an orientation, and describe it by 128 gradient histograms for matching.
solves: [feature-detection]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, m: the number of keypoints in the first image, n: the number of keypoints in the second image}
  time: {worst: O(W H + m n), average: O(W H + m n), best: O(W H + m n)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, approximately_scale_invariant: true, approximately_rotation_invariant: true, heuristic: true}
history:
  year: 1999
  people: [David G. Lowe]
  note: Lowe presented the method at ICCV 1999 and gave the full form in the International Journal of Computer Vision in 2004. The University of British Columbia held US patent 6,711,293 on it.
prereqs: [feature-detection, gaussian-pyramid, laplacian-of-gaussian]
see_also: [harris-corner-detector, corner-detection, image-registration, kd-tree-nearest-neighbor-search, approximate-nearest-neighbor-search, hough-transform, normalized-cross-correlation, gaussian-filter]
sources:
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: Section 3 (scale-space extrema, 3.1 local extrema, 3.3 the prior blur and image doubling); Section 4 (keypoint localization, 4.1 edge responses); Section 5 (orientation); Section 6.1 (the descriptor); Section 7.1 (the ratio test); Section 7.2 (best bin first search)
  - paper: doi:10.1109/ICCV.1999.790410
    title: David G. Lowe, Object recognition from local scale-invariant features, Proceedings of the Seventh IEEE International Conference on Computer Vision, 1150-1157, 1999
    locator: the whole paper (the first form of the method)
  - url: https://patents.google.com/patent/US6711293B1
    title: David G. Lowe, Method and apparatus for identifying scale invariant features in an image and use of same for locating an object in an image, US patent 6,711,293
    locator: the claims and the description of the preferred embodiment
  - paper: doi:10.1023/A:1008045108935
    title: Tony Lindeberg, Feature detection with automatic scale selection, International Journal of Computer Vision 30(2), 1998
    locator: the whole paper (scale-normalized derivatives and the selection of scale)
  - paper: doi:10.1109/TPAMI.2005.188
    title: Krystian Mikolajczyk and Cordelia Schmid, A performance evaluation of local descriptors, IEEE Transactions on Pattern Analysis and Machine Intelligence 27(10), 2005
    locator: the whole paper
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 12.7, Scale-invariant feature transform (SIFT)
---

The scale-invariant feature transform (SIFT) finds points in an image that can be found again in another image of the same scene, and it gives each point a vector of 128 numbers that describes the image around it. It is a method for [feature detection](/feature-detection/) and description. It builds a [Gaussian pyramid](/gaussian-pyramid/) with several blur levels per octave, takes the difference of neighbouring levels as an approximation of the scale-normalized [Laplacian of Gaussian](/laplacian-of-gaussian/), and keeps the samples that are larger or smaller than all 26 neighbours in space and scale. It refines each point by a quadratic fit, removes points of low contrast and points on edges, gives each point one or more orientations from a histogram of gradient directions, and builds the descriptor from gradient histograms in a $4 \times 4$ grid that is turned to that orientation. Two images are matched by nearest neighbours of the descriptors with a ratio test. For fixed parameters, detection costs $O(WH)$ for a $W \times H$ image, and exact matching costs $O(mn)$ for $m$ and $n$ keypoints. David Lowe published the method in 1999 and in full in 2004. The steps are deterministic, but the invariance to scale, rotation and viewpoint is approximate, and the thresholds were set by experiment; the method is a well tested heuristic, not an algorithm with a guarantee.

## In plain words

You want to find the same small spots in two photos of one object, even if one photo is taken from farther away or with the camera turned. SIFT makes many blurred copies of the photo, from a little blur to a lot, and also smaller copies. A spot is interesting if it stands out from its surroundings at some amount of blur, like a dark dot on a light wall. The amount of blur at which it stands out most tells how big the spot is. SIFT then looks at which way the brightness changes most around the spot and turns its view to match. Finally it writes down a short summary of the edges around the spot. Spots with similar summaries in the two photos are taken as the same place, but only if the best match is clearly better than the second best.

## The problem

The input is a gray [digital image](/digital-image/) with $W$ columns and $H$ rows, one channel, with values in $[0, 1]$. The contrast threshold $0.03$ of Lowe assumes this range. The values are used as they are stored, without a gamma step; a change of encoding changes the contrast of the DoG and so the points that pass the threshold. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. The border rule for the blur is clamp. Extrema are not looked for within one pixel of the border of an octave, and gradient samples within one pixel of the border are skipped.

The output is a list of keypoints $(x, y, \sigma, \theta, \mathbf{d})$: a position in image pixels, a scale, an orientation and a unit vector $\mathbf{d} \in \mathbb{R}^{128}$. For two images, the output of matching is a list of pairs of keypoints. The aim is that a point of the scene that is visible in both images gives a keypoint in each, with descriptors that are close. That aim is not a property that can be proved for all images; it is what the design and the tests of Lowe try to achieve.

The Gaussian scale space is $L(x, y, \sigma) = G_\sigma \ast I$, and the difference of Gaussians (DoG) is $D(x, y, \sigma) = L(x, y, k\sigma) - L(x, y, \sigma)$. Lowe notes that $D \approx (k - 1)\sigma^2 \nabla^2 G \ast I$, so the DoG is the scale-normalized Laplacian of Gaussian up to the constant factor $k - 1$, which is the same for all scales and does not move the extrema.

## The algorithm

```pseudo id=main
SIFT(I)                       ▷ s = 3, σ0 = 1.6, r = 10; octave o samples every 2^o th pixel
L1  for each octave o: G[o][0] has blur σ0; G[o][i] ← blur G[o][i − 1] up to σ0 2^(i/s), for 1 ≤ i ≤ s + 2;
    the next octave starts from every second pixel of G[o][s]
L2  D[o][i] ← G[o][i + 1] − G[o][i] for 0 ≤ i ≤ s + 1
L3  for each octave o, each 1 ≤ i ≤ s and each pixel (x, y) at least one pixel from the border do
L4      if D[o][i](x, y) is larger than all 26 neighbours or smaller than all 26 neighbours then
L5          fit D(z) ≈ D + gᵀz + ½ zᵀHz at the sample; z ← −H⁻¹g; while some |z_c| > 0.5, move to the next sample and fit again (at most 5 times)
L6          reject if |D + ½ gᵀz| < 0.03, or det H_xy ≤ 0, or (tr H_xy)² r ≥ (r + 1)² det H_xy
L7          h ← 36-bin histogram of gradient directions near the point, weights: magnitude × Gaussian with 1.5 σ
L8          for each local peak of h that is at least 0.8 max h, refined by a parabola, as θ do
L9              d ← 4 × 4 × 8 histogram of gradient directions relative to θ, on a grid turned by θ, trilinear weights
L10             d ← d / ‖d‖;  d ← min(d, 0.2);  d ← d / ‖d‖;  emit the keypoint (x, y, σ, θ, d)

MATCH(A, B)
L11 for each descriptor a in A do
L12     find the nearest b1 and the second nearest b2 in B by Euclidean distance
L13     if ‖a − b1‖ < 0.8 ‖a − b2‖ then report the pair (a, b1)
```

Line L1 builds $s + 3$ Gaussian images per octave, with $\sigma_i = \sigma_0 2^{i/s}$ in the pixel units of the octave. Each image is the previous one blurred by $\sqrt{\sigma_i^2 - \sigma_{i-1}^2}$, because blurs add in squares. The input is assumed to have a blur of $0.5$ already, so the first blur is $\sqrt{1.6^2 - 0.5^2} \approx 1.520$. Image $s$ of an octave has blur $2\sigma_0$, so every second pixel of it is a correct start of the next octave with blur $\sigma_0$ in the new pixel units. Line L2 gives $s + 2$ DoG images, and line L3 can look for extrema at the $s$ middle ones, which cover one octave of scale.

Line L4 is the test of Section 3.1 of Lowe: 8 neighbours at the same scale and 9 in each of the two neighbouring scales. The implementation also skips samples with $|D| \le 0.5 \cdot 0.03 / s$ before the test, to save time; this choice follows common implementations and is not in the paper. Line L5 is the fit of Section 4: $g$ and $H$ are the central difference gradient and Hessian of $D$ in $(x, y, \sigma)$, and $z$ is the offset of the extremum of the fitted quadratic. If the offset is larger than half a sample in some direction, the extremum is closer to another sample, so the fit moves there. Line L6 rejects low contrast with the value of the fit at the extremum. It also applies the edge test of Section 4.1: $H_{xy}$ is the $2 \times 2$ spatial part of $H$, and a ratio of principal curvatures larger than $r = 10$ marks an edge, where the position along the edge is not stable.

Lines L7 and L8 are Section 5. The gradient at a pixel of the Gaussian image of the keypoint is $(L(x + 1, y) - L(x - 1, y), \, L(x, y + 1) - L(x, y - 1))$. A peak at bin $b$ with neighbours $\ell$, $c$, $\rho$ is refined to bin $b + \frac{1}{2} + \frac{1}{2}\frac{\ell - \rho}{\ell - 2c + \rho}$. Each peak within $80\%$ of the highest gives a separate keypoint, so one location can have several orientations. Lines L9 and L10 are Section 6.1. The samples are weighted by a Gaussian with $\sigma$ equal to half the width of the grid, and each sample is spread over the two nearest cells in each direction and the two nearest orientation bins. The clip at $0.2$ reduces the effect of a few large gradients, for example from a change of lighting that is not linear. Lowe describes the grid as a $16 \times 16$ array of samples with $4 \times 4$ samples per cell, and he does not state the cell width as a multiple of $\sigma$; the implementation uses a cell width of $3\sigma$, as common open implementations do. It also spreads each sample of the orientation histogram over two bins, which the paper does not ask for.

Lines L11 to L13 are Section 7.1. On the test data of Lowe the threshold $0.8$ removed $90\%$ of the false matches and less than $5\%$ of the correct ones. The implementation searches exactly, with early abandoning: the sum for one candidate stops when it is already larger than the second best squared distance.

## Example

A full run is too large to show, so here are the pieces with their numbers for $s = 3$ and $\sigma_0 = 1.6$.

**The scales of one octave.** $\sigma_i = 1.6 \cdot 2^{i/3}$ gives $1.6, 2.016, 2.540, 3.2, 4.032, 5.080$ for $i = 0, \ldots, 5$. The blurs applied between neighbours are $\sqrt{\sigma_i^2 - \sigma_{i-1}^2} = 1.226, 1.545, 1.947, 2.453, 3.090$. Image $i = 3$ has $\sigma = 3.2 = 2\sigma_0$ and starts the next octave. On a $41 \times 33$ image ($W = 41$, $H = 33$), the octaves have the sizes $41 \times 33$, $21 \times 17$ and $11 \times 9$.

**The fit, in one direction.** Say that $D$ at $x - 1$, $x$, $x + 1$ is $0.02$, $0.05$, $0.04$. Then $g = (0.04 - 0.02)/2 = 0.01$ and $H = 0.04 - 2 \cdot 0.05 + 0.02 = -0.04$, so $z = -g/H = 0.25$. The value at the extremum is $0.05 + \frac{1}{2} \cdot 0.01 \cdot 0.25 = 0.05125$, which is above $0.03$, and $|z| \le 0.5$, so the point stays at this sample with the position $x + 0.25$. The parabola through the three values has its vertex at exactly this point.

**The edge test.** For $H_{xy}$ with $D_{xx} = 10$, $D_{yy} = 1$ and $D_{xy} = 0$, the trace is $11$ and the determinant is $10$. Then $(\operatorname{tr})^2 / \det = 12.1 = (r + 1)^2 / r$ for $r = 10$: the ratio of the curvatures is exactly $10$, so the strict test of line L6 rejects the point. With $D_{xx} = 9$ the ratio is $9$, and $(10)^2 / 9 \approx 11.1 < 12.1$ keeps it.

**The orientation.** Say the histogram has $2$, $4$, $3$ in bins $4$, $5$, $6$ of $10°$ each, and bin $5$ is the highest. The refined bin is $5 + 0.5 + 0.5 \cdot \frac{2 - 3}{2 - 8 + 3} = 5.5 + \frac{1}{6}$, so $\theta = 56\tfrac{2}{3}°$.

**The clip.** A descriptor with one entry $3$ and 24 entries $1$ (and zeros elsewhere) has norm $\sqrt{33}$. After the first normalization the large entry is $3/\sqrt{33} \approx 0.522$, which is clipped to $0.2$, and the others are $1/\sqrt{33} \approx 0.174$, which stay. After the second normalization the ratio of the large entry to a small one is $0.2\sqrt{33} \approx 1.149$ instead of $3$.

**A full run.** On the $41 \times 33$ test image of the implementation, with smooth blobs, two octaves give 6 keypoints. The same image turned by $90°$ gives the same 6 keypoints at the turned positions, with orientations that differ by $90°$ and descriptors that agree to $10^{-9}$.

## Correctness

SIFT has no correctness theorem of the form "it finds the same points in two views", because that depends on the scene. The proof in [proofs/correctness.md](proofs/correctness.md) shows what each step does exactly. Line L1 gives the blur $\sigma_0 2^{i/s}$ at level $i$ because Gaussian blurs add in squares, and the start of each octave has blur $\sigma_0$ in its own pixel units. Line L4 returns exactly the strict 26-neighbour extrema. Line L5 returns the extremum of the quadratic that has the measured gradient and Hessian, and this is the true extremum when $D$ is a quadratic near the sample. The edge test of line L6 holds exactly when the ratio of the eigenvalues of $H_{xy}$ is below $r$ and they have the same sign. Line L10 gives a unit vector that does not change when all gradients are multiplied by a positive constant. Lines L11 to L13 report a pair exactly when the ratio test holds for the true nearest and second nearest descriptors.

## Complexity

Let $N = WH$. For fixed parameters ($s$, $\sigma_0$, the size of the descriptor grid), every constant below is fixed.

- **Pyramid (L1, L2).** Octave $o$ has about $N/4^o$ pixels, and each of its $s + 2$ blurs costs $O(\sigma)$ per pixel with a separable kernel of radius $\lceil 3\sigma \rceil$; the largest blur here is $3.09$, so the radius is at most $10$. Over all octaves the geometric sum gives $\Theta(N)$ time, and the pyramid needs $\Theta(N)$ space.
- **Extrema (L3, L4).** At most $26$ comparisons for each of $s$ DoG samples per pixel per octave, so $O(N)$.
- **Refinement and description (L5 to L10).** The fit is a $3 \times 3$ solve, repeated at most $5$ times. The orientation window and the descriptor window have a size that is a fixed multiple of $\sigma$ in octave pixels, and $\sigma \le 2\sigma_0$ there, so each keypoint costs $O(1)$. The number of keypoints is at most the number of DoG samples times the number of orientation peaks ($\le 18$), so $O(N)$.
- **Matching (L11 to L13).** Each of the $m$ descriptors is compared with all $n$, at a cost of $128$ operations each, so $\Theta(mn)$ in the worst case. Early abandoning lowers the observed cost but not the bound.

The total is $O(WH + mn)$ in the worst case. The constant of the detection part is large: tens of blurred copies and window sums per pixel. Lowe used approximate nearest neighbour search instead of the exact search of line L12, with a [k-d tree](/kd-tree-nearest-neighbor-search/) searched in best bin first order and stopped after $200$ candidates. He notes that exact search in $128$ dimensions is not known to be faster than a full scan (see [approximate nearest neighbor search](/approximate-nearest-neighbor-search/)).

## Properties

- **Scale.** A change of scale by $2^{j/s}$ for an integer $j$ moves the DoG extrema to the level $j$ higher, up to the sampling of space. Other factors fall between levels and are found by the fit. This is approximate: the sampling of scale and space, the assumed input blur and the border all limit it.
- **Rotation.** The orientation of line L8 turns with the image, and the descriptor is built relative to it, so a rotation changes the descriptor only by the sampling of the grid. In the implementation a turn by $90°$ gives the same descriptors exactly when $W$ and $H$ are odd, because every second pixel then maps to every second pixel.
- **Brightness.** The DoG does not change when a constant is added. A gain $c$ multiplies $D$ by $c$, so the contrast threshold of line L6 then selects other points; the descriptor itself does not change because of the normalization at line L10.
- **Viewpoint.** A small change of viewpoint is close to an affine map on a small patch, and the descriptor is designed to tolerate small shifts of gradients between cells. A large change of viewpoint is not handled.
- **Distinctive.** A descriptor of 128 values is distinctive enough to match against a large database. In the comparison of local descriptors by Mikolajczyk and Schmid (2005), SIFT and their extension of it were among the best.
- **Several orientations.** About $15\%$ of the points in Lowe's experiments got more than one orientation, which he reports adds to the stability of matching.

## Variants and improvements

- **Image doubling.** Lowe first doubles the input by linear interpolation, assumes that the doubled image has a blur of $1.0$, and so applies $\sqrt{1.6^2 - 1.0^2} \approx 1.249$ first. He reports that this gives almost four times as many stable keypoints. The implementation does not double, to keep the tests small.
- **SURF.** Bay, Ess, Tuytelaars and Van Gool (2008) replace the Gaussian derivatives by box filters on an [integral image](/integral-image/), detect at the maxima of the determinant of an approximate Hessian, and use a descriptor of 64 sums of Haar wavelet responses. The aim is speed.
- **Binary descriptors.** Descriptors made of bit comparisons of pixel pairs are matched by Hamming distance and are much cheaper to store and compare.
- **Learned features.** CNN based detectors and descriptors now replace SIFT in many systems, but SIFT remains a common baseline.
- **Verification.** Lowe groups the matches by a [Hough transform](/hough-transform/) over position, scale and orientation, and then checks each group with a least squares fit of an affine map. Matching alone does not give an object or a transform; this step does.
- **Color.** SIFT works on one channel. Color variants compute descriptors on several channels or color invariants and join them.

## When to use it

Use SIFT to match points between images of the same scene that differ by scale, rotation, a moderate change of viewpoint or lighting: [image registration](/image-registration/) and mosaics, recognition of a known object in a cluttered scene, structure from motion and visual localization. Use [NCC](/normalized-cross-correlation/) or [phase correlation](/phase-correlation/) when the images differ only by a translation and a change of brightness, because they are cheaper and give dense, exact positions. Use a corner detector such as [Harris](/harris-corner-detector/) with a tracker for consecutive video frames.

## Pitfalls

- **Value range.** The threshold $0.03$ assumes values in $[0, 1]$. With 8-bit values in $[0, 255]$ it accepts almost every extremum. Scale the input or the threshold.
- **The blur steps.** Blurring each level from the base by the full $\sigma_i$, instead of the increment $\sqrt{\sigma_i^2 - \sigma_{i-1}^2}$ from the previous level, gives too much blur. Starting the next octave from a level other than the one with $2\sigma_0$ gives the wrong scale.
- **Scale units.** $\sigma$ is in the pixel units of the octave during detection. Multiply positions and scales by $2^o$ to report them in image pixels, and do not mix the two in the descriptor window.
- **Ratio test direction.** The test compares distances, not squared distances, with $0.8$; with squared distances the threshold is $0.64$.
- **Edge responses.** Without the test of line L6 many keypoints lie along edges, where the position along the edge is not stable, and they match badly.
- **Repeated texture.** On a regular pattern, many descriptors are alike and the ratio test rejects most true matches. This is a correct result of the test, but it can leave too few matches.
- **Determinism across libraries.** Implementations differ in the kernel size, the border rule, the cell width and the interpolation, so two libraries give different keypoints on the same image. Do not compare descriptors from different implementations.

## Implementations

## History

The base of SIFT is scale-space theory: Witkin and Koenderink described the Gaussian scale space in the early 1980s, and Lindeberg (1998) showed how to select a scale automatically from the extrema of scale-normalized derivatives such as the Laplacian. David Lowe at the University of British Columbia presented SIFT at ICCV 1999 for object recognition, with a staged filter to find stable points and a local descriptor. The 2004 paper in the International Journal of Computer Vision added the quadratic localization, the edge test and the final descriptor with clipping, and it explained the matching and verification steps. The University of British Columbia held the US patent 6,711,293 on the method, which limited its commercial use until the patent expired in 2020. SIFT became one of the most used local features in computer vision and is still a standard baseline.

## References
