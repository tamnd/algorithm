---
tag: T23R2B
kind: problem
slug: homography-estimation
name: Homography estimation
aliases:
- planar homography fitting
area: computer-vision/multiple-view-geometry
level: core
summary: Find the homography that best maps one set of image points to another, from at least four point pairs in general position.
prereqs: [homography]
see_also: [dlt-homography, hartley-normalization, algebraic-and-geometric-error, ransac, levenberg-marquardt, image-stitching, zhang-calibration-method, direct-image-alignment]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 4, Estimation - 2D projective transformations (Section 4.1 the DLT, Section 4.2 the cost functions, Section 4.3 maximum likelihood, Section 4.4 normalization, Section 4.5 iterative minimization, Sections 4.7 and 4.8 robust and automatic estimation)"
  - paper: doi:10.1109/34.601246
    title: "Richard I. Hartley, In defense of the eight-point algorithm, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(6), 1997, 580-593"
    locator: the normalization of the points before a linear estimate
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 8.1, Pairwise alignment (least squares fitting of 2D motion models, including the homography)"
---

Homography estimation is the problem of finding the [homography](/homography/) $H$ that maps a set of points of one image to their matches in another image, with $\mathbf{x}'_i \sim H\mathbf{x}_i$. Four pairs with no three points on a line fix $H$ exactly; with more pairs and noise, the answer depends on the cost that is minimized. This page states the problem, its costs and its methods. The [DLT for homographies](/dlt-homography/) is the linear method, [Hartley normalization](/hartley-normalization/) is the step that makes it accurate, and [algebraic and geometric error](/algebraic-and-geometric-error/) compares the costs.

## In plain words

You have two photos of a flat poster, taken from different places, and you have marked the same corners and spots in both. You want the one rule that moves every point of the first photo to its place in the second. A rule of this kind has eight free numbers, and each marked pair gives two equations, so four pairs are enough if no three of the spots are on one line. Real marks are a little wrong, so you use more pairs and look for the rule that fits them best. Some marks can be plain wrong; then you also need a way to find and ignore them.

## Definition

**Input.** Pairs of image points $(\mathbf{x}_i, \mathbf{x}'_i)$, $i = 1, \ldots, n$, with $n \ge 4$, in [homogeneous coordinates](/homogeneous-coordinates/) or in pixels.

**Output.** An invertible $3 \times 3$ matrix $H$, up to a nonzero factor, that minimizes a chosen cost. The usual costs, from the cheapest to the most meaningful:

- **Algebraic error.** $\|A\mathbf{h}\|^2$ with $\|\mathbf{h}\| = 1$, where $\mathbf{h}$ is $H$ as a 9-vector and $A$ is the $2n \times 9$ matrix of the DLT. Each row is linear in $\mathbf{h}$.
- **Transfer error.** $\sum_i d(\mathbf{x}'_i, H\mathbf{x}_i)^2$, with $d$ the image distance. This is the maximum likelihood cost when only the second image has noise.
- **Symmetric transfer error.** $\sum_i d(\mathbf{x}_i, H^{-1}\mathbf{x}'_i)^2 + d(\mathbf{x}'_i, H\mathbf{x}_i)^2$.
- **Reprojection error.** Minimize over $H$ and corrected points $\hat{\mathbf{x}}_i$ the sum $\sum_i d(\mathbf{x}_i, \hat{\mathbf{x}}_i)^2 + d(\mathbf{x}'_i, H\hat{\mathbf{x}}_i)^2$. Under independent isotropic Gaussian noise in both images this is the maximum likelihood estimate (HZ Section 4.3); Hartley and Zisserman call the method that minimizes it the Gold Standard algorithm. See [reprojection error](/reprojection-error/).
- **Sampson error.** A first-order approximation of the reprojection error that needs no corrected points (see [Sampson distance](/sampson-distance/)).

**Number of solutions.** If the data are exact and come from an invertible $H$:

- $n = 4$ with no three of the $\mathbf{x}_i$ on a line: exactly one $H$. Then no three of the $\mathbf{x}'_i$ are on a line either.
- $n \ge 4$ with four of the points in that general position: exactly one $H$, and every cost above is 0 at it.
- Three of four points on a line, or all points on a line: infinitely many solutions, and the DLT matrix loses rank.

With noise and $n > 4$ no $H$ fits exactly, and the costs have different minimizers.

## Variants

- **With outliers.** Some pairs are wrong matches. Fit a homography to random minimal samples of 4 pairs and keep the one with the largest consensus, as in [RANSAC](/ransac/), then refit on the inliers. This is the usual setting with automatic [feature matching](/feature-matching/) (HZ Section 4.8).
- **From lines.** Lines map as $\mathbf{l}' \sim H^{-\mathsf T}\mathbf{l}$, so matched lines give the same kind of linear equations for $H^{-\mathsf T}$. Points and lines can be mixed.
- **Fewer degrees of freedom.** If the camera only turns and $K$ is known, $H = K R K^{-1}$ has 3 degrees of freedom, and two pairs fix it. An affine model has 6 and needs three pairs. Fit the smaller model when it is true: it needs fewer pairs and is less sensitive to noise (see the [hierarchy of planar transformations](/planar-transformation-hierarchy/)).
- **From pixel values.** Instead of points, minimize the difference of the image intensities after warping by $H$. This is [direct image alignment](/direct-image-alignment/), for example by [inverse compositional alignment](/inverse-compositional-alignment/).

## Examples

- **Exact, four pairs.** The unit square $(0, 0)$, $(1, 0)$, $(1, 1)$, $(0, 1)$ and the trapezoid $(0, 0)$, $(4, 0)$, $(3, 2)$, $(1, 2)$ give the unique answer $H \sim \begin{pmatrix} 4 & 2 & 0 \\ 0 & 4 & 0 \\ 0 & 1 & 1 \end{pmatrix}$, as the [DLT page](/dlt-homography/) works out.
- **Degenerate, three collinear points.** Map $(0, 0)$, $(1, 0)$, $(2, 0)$, $(0, 1)$ to themselves. The identity fits, but so does $H_b = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 + b & 0 \\ 0 & b & 1 \end{pmatrix}$ for every $b \ne -1$: on the line $y = 0$ the third row gives $w = 1$, so the three collinear points stay fixed, and $(0, 1, 1)^{\mathsf T} \mapsto (0, 1 + b, 1 + b)^{\mathsf T} \sim (0, 1, 1)^{\mathsf T}$. So the four pairs do not fix $H$, and the DLT matrix has a null space of dimension 2.
- **Different costs, different answers.** With noise, the algebraic error weights each pair by a factor that depends on its position and on the coordinate frame, while the transfer and reprojection errors count pixels. So the DLT on raw pixel coordinates and the Gold Standard method return different $H$; [Hartley normalization](/hartley-normalization/) brings the DLT answer close to the Gold Standard one in practice.

## Known algorithms

- **Normalized DLT** (HZ Algorithm 4.2): normalize each image, solve $A\mathbf{h} = \mathbf{0}$ in the least squares sense by the [SVD](/singular-value-decomposition/), and undo the normalization. Linear, with no iterations. See [DLT for homographies](/dlt-homography/).
- **Gold Standard method** (HZ Section 4.5): start from the normalized DLT and minimize the reprojection error over $H$ and the corrected points with [Levenberg-Marquardt](/levenberg-marquardt/). The normal equations have a sparse structure, so each iteration costs $O(n)$.
- **Sampson minimization.** Minimize the Sampson error over the 9 entries of $H$ only, with Gauss-Newton or Levenberg-Marquardt. It is close to the Gold Standard result when the noise is small.
- **Robust estimation.** [RANSAC](/ransac/) and its variants with the 4-point DLT as the minimal solver, followed by one of the methods above on the inliers (HZ Section 4.8, automatic computation of a homography). The general setting is [robust model fitting](/robust-model-fitting/).
- **Direct methods.** [Direct image alignment](/direct-image-alignment/) estimates $H$ from pixel values by Gauss-Newton on the photometric error, from a good start.

## Bounds

- **Minimal data.** $H$ has 8 degrees of freedom and each pair gives 2 independent equations, so 4 pairs are the minimum. This also sets the size of the minimal sample in RANSAC.
- **Cost.** Any method reads all $n$ pairs, so $\Omega(n)$. The DLT forms a $2n \times 9$ matrix and finds its smallest singular vector in $O(n)$ time, since the number of columns is fixed. One Levenberg-Marquardt step of the Gold Standard method costs $O(n)$ with the sparse structure.
- **Robust sampling.** If a fraction $w$ of the pairs are inliers, RANSAC needs $N = \log(1 - p) / \log(1 - w^4)$ samples to draw one sample of 4 inliers with probability $p$. For $w = 0.5$ and $p = 0.99$, $N = 72$.

## Reductions

- The algebraic problem reduces to finding the unit vector that minimizes $\|A\mathbf{h}\|$, which is the right singular vector of $A$ for its smallest singular value.
- The Gold Standard problem is a [nonlinear least squares](/nonlinear-least-squares/) problem in $8 + 2n$ unknowns.
- Estimating the pose of a calibrated camera that sees a plane reduces to homography estimation followed by [homography decomposition](/homography-decomposition/); this is the planar case of [perspective-n-point](/perspective-n-point/).
- [Zhang's calibration method](/zhang-calibration-method/) reduces camera calibration to estimating one homography per view of a planar target.

## Applications

- [Image stitching](/image-stitching/): one homography per pair of overlapping photos, or a rotation per photo.
- Camera calibration from a planar target ([Zhang's method](/zhang-calibration-method/)).
- Rectification of a photo of a document, a facade or a sports field to a front view.
- Augmented reality on planar markers, and the pose of a drone or a robot above flat ground.
- [Image registration](/image-registration/) of nearly flat scenes, such as aerial photos and document scans.

## References
