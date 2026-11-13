---
tag: 5T1SXZ
kind: problem
slug: corner-detection
name: Corner detection
area: graphics-and-signals/image-processing
level: advanced
summary: Find the image points where the intensity changes strongly in two directions, so that a small patch around the point changes for every direction of shift.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, r: window radius in pixels}
  time: {worst: O(W H r)}
prereqs: [feature-detection, digital-image]
see_also: [harris-corner-detector, feature-detection, edge-detection, eigenvalue, lucas-kanade-method, non-maximum-suppression, sobel-operator, gaussian-filter]
sources:
  - paper: doi:10.5244/C.2.23
    title: Chris Harris and Mike Stephens, A combined corner and edge detector, Proceedings of the Alvey Vision Conference 1988, Manchester
    locator: the sections Moravec revisited and Corner/edge response function (the local autocorrelation and its matrix)
  - paper: doi:10.1109/CVPR.1994.323794
    title: Jianbo Shi and Carlo Tomasi, Good features to track, IEEE Conference on Computer Vision and Pattern Recognition, 593-600, 1994
    locator: the whole paper (the smaller eigenvalue as the criterion, from the conditions for tracking)
  - paper: doi:10.1016/0262-8856(88)90007-8
    title: J. Alison Noble, Finding corners, Image and Vision Computing 6(2), 121-128, 1988
    locator: the whole paper
  - paper: doi:10.1007/11744023_34
    title: Edward Rosten and Tom Drummond, Machine learning for high-speed corner detection, European Conference on Computer Vision 2006, Lecture Notes in Computer Science 3951, 430-443
    locator: the whole paper (the segment test on a circle of 16 pixels)
  - paper: "Hans P. Moravec, Obstacle avoidance and navigation in the real world by a seeing robot rover, PhD thesis, Stanford University, 1980"
    title: Hans P. Moravec, Obstacle avoidance and navigation in the real world by a seeing robot rover, 1980
    locator: the whole thesis (the interest operator of shifted windows)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 12.6, The Harris-Stephens corner detector
---

Corner detection is the problem of finding the points of an image where the intensity changes strongly in two different directions, such as the corner of a window, the tip of a letter or the point where two edges meet. Such points are the easiest kind of [feature](/feature-detection/) to find again in a second image: a small patch around a corner changes when it is shifted in any direction, so its position is fixed in both coordinates. A point on a straight edge is fixed only across the edge, and a point in a flat region is not fixed at all. Most detectors measure this with the $2 \times 2$ matrix of summed gradient products over a window and test its two [eigenvalues](/eigenvalue/). Others test the pixels on a small circle directly. The problem has no single formal answer: each detector fixes a response and a threshold, and the thresholds are a heuristic choice.

## In plain words

Put a small square frame on a photo and look at the patch inside it. Now slide the frame a little, up, down, left or right. In a flat region, such as a clear sky, the patch looks the same after any slide. On a straight edge, such as the side of a door, it looks the same when you slide along the edge but changes when you slide across it. At a corner it changes for every slide. Corner detection finds the places where every slide changes the patch, so that the place can be pointed to exactly. A good detector does this fast, does not mark noise as corners, and finds the same corners after the photo is turned or made darker.

## Definition

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows and one channel of values, for example 0 to 255, used as they are stored with no gamma step. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. Reads outside the image use the clamp rule. Let $w(i, j) \ge 0$ be a window of radius $r$, for example a Gaussian, and let $\nabla I = (I_x, I_y)$ be a discrete gradient, for example from the [Sobel operator](/sobel-operator/).

The *local autocorrelation* at a point $p$ measures how much the patch changes under a shift $u \in \mathbb{R}^2$:

$$E_p(u) = \sum_{q} w(q - p) \big(I(q + u) - I(q)\big)^2 \approx u^{\mathsf T} M_p\, u, \qquad M_p = \sum_q w(q - p) \begin{pmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{pmatrix}(q),$$

where the approximation is the first-order Taylor step $I(q + u) \approx I(q) + \nabla I(q) \cdot u$. The matrix $M_p$ is the *second-moment matrix* of the gradients in the window. It is symmetric and positive semidefinite, with eigenvalues $\lambda_1 \ge \lambda_2 \ge 0$. The smallest change of the patch for a shift of length 1 is $\lambda_2$, and the largest is $\lambda_1$. The three cases are:

- $\lambda_1 \approx \lambda_2 \approx 0$: a flat region.
- $\lambda_1 \gg \lambda_2 \approx 0$: an edge, with the gradient along the eigenvector of $\lambda_1$.
- $\lambda_1 \ge \lambda_2 \gg 0$: a corner.

A *corner detector* computes a response $R(p)$ from $M_p$ or from the pixels near $p$, and returns the points where $R$ is a local maximum above a threshold $\tau$, usually after [non-maximum suppression](/non-maximum-suppression/). The output is a set of points, sometimes with a position finer than the grid.

## Variants

- **Response functions on $M$.** Harris and Stephens use $\det M - k (\operatorname{tr} M)^2$ with a small $k$, which avoids the square root of the eigenvalues; see the [Harris corner detector](/harris-corner-detector/). Shi and Tomasi use $\lambda_2$ directly. Noble uses $\det M / \operatorname{tr} M = \lambda_1 \lambda_2 / (\lambda_1 + \lambda_2)$, half of the harmonic mean, and Förstner uses a similar ratio.
- **Shifted windows.** Moravec's operator, the first of this kind, computes $E_p(u)$ itself for 8 shifts by one pixel and takes the smallest. It is not invariant to turns, because only the 4 directions of the rows, the columns and the two diagonals are tested.
- **Segment tests.** FAST compares the 16 pixels on a circle of radius 3 around $p$ with $I(p)$, and calls $p$ a corner when $n$ contiguous pixels of the circle are all brighter than $I(p) + t$ or all darker than $I(p) - t$. It needs no derivatives and is fast, but has no scale.
- **Contour-based corners.** Edges are first found and linked into curves, and the corners are the points of high curvature on the curves.
- **Subpixel position.** The corner is refined to a position finer than the grid, by the least squares step in the Reductions or by a fit of the response.
- **Several scales.** The window and the gradient filter are applied at several scales, and each corner keeps the scale at which a normalized response is largest.

## Examples

**Three windows.** Take a window with weight 1 at each pixel and gradients from a mask.

- On a vertical edge, five pixels have the gradient $(2, 0)$ and the rest have $0$. Then $M = \begin{pmatrix} 20 & 0 \\ 0 & 0 \end{pmatrix}$, with $\lambda = 20, 0$.
- On a diagonal edge, five pixels have the gradient $(1, 1)$. Then $M = \begin{pmatrix} 5 & 5 \\ 5 & 5 \end{pmatrix}$, with $\lambda = 10, 0$ and the eigenvector $(1, 1)/\sqrt 2$ of $\lambda_1$ along the gradient. The off-diagonal entries matter: the diagonal of $M$ alone would look like a corner.
- At a corner, three pixels have the gradient $(2, 0)$ and two have $(0, 2)$. Then $M = \begin{pmatrix} 12 & 0 \\ 0 & 8 \end{pmatrix}$, with $\lambda = 12, 8$.

**Three responses.** For eigenvalue pairs, the three response functions on $M$ give, with $k = 0.04$ for Harris:

| $\lambda_1, \lambda_2$ | kind | Harris | Shi and Tomasi | Noble |
|---|---|---|---|---|
| $20, 0$ | edge | $-16$ | $0$ | $0$ |
| $12, 8$ | corner | $80$ | $8$ | $4.8$ |
| $10, 10$ | corner | $84$ | $10$ | $5$ |
| $10, 1$ | weak corner | $5.16$ | $1$ | $0.909$ |
| $100, 1$ | strong edge | $-308.04$ | $1$ | $0.990$ |

The last two rows have the same $\lambda_2$, so Shi and Tomasi rank them the same, and Noble ranks the strong edge slightly higher. Harris gives the strong edge a large negative value, because its response falls with the ratio $\lambda_2 / \lambda_1$ and not only with $\lambda_2$. Which ranking is better depends on the use.

## Known algorithms

| Algorithm | Response | Cost | Notes |
|---|---|---|---|
| [Harris corner detector](/harris-corner-detector/) | $\det M - k (\operatorname{tr} M)^2$ | $O(WHr)$ | turn invariant, a standard choice |
| Shi and Tomasi | $\lambda_2$ | $O(WHr)$ | the criterion for good tracking |
| Noble, Förstner | $\det M / \operatorname{tr} M$ and similar | $O(WHr)$ | no parameter $k$ |
| Moravec | least $E_p(u)$ over 8 shifts | $O(WHr^2)$ | not turn invariant |
| FAST | segment test on 16 pixels | $O(WH)$ | no derivatives, no scale |
| Harris-Laplace | Harris over scales, scale by the Laplacian | $O(WHr)$ per scale | scale covariant |

Here $r$ is the radius of the window. A separable window gives $O(WHr)$ for the sums of gradient products, and a box window with an [integral image](/integral-image/) gives $O(WH)$. These costs are worst-case bounds. The number of corners found depends on the image and the threshold.

## Bounds

- **Reading the input.** Every pixel can change whether a corner is near it, so $\Omega(WH)$ time is needed in the worst case. A box window meets this bound.
- **Edges have a singular matrix.** $M_p$ is singular exactly when all nonzero gradients of the window with positive weight are parallel. Proof: $u^{\mathsf T} M_p u = \sum w (\nabla I \cdot u)^2$ is zero exactly when $u$ is perpendicular to every such gradient, and a nonzero $u$ of this kind exists exactly when the gradients span at most one direction. So no detector of the form $R = f(\lambda_1, \lambda_2)$ with $f(\lambda, 0) \le 0$ and a threshold $\tau \ge 0$ marks a pure edge or a flat window as a corner.
- **Tracking needs the same matrix.** The [Lucas-Kanade method](/lucas-kanade-method/) finds the shift $d$ of a window from $M_p\, d = -\sum w\, \nabla I\, I_t$, where $I_t$ is the change in time. It has a unique solution exactly when $M_p$ is invertible, and it is stable to noise when $\lambda_2$ is not small. This is the argument of Shi and Tomasi for $\lambda_2$ as the response.
- **Thresholds are heuristic.** No threshold separates corners from edges for every image, because $M$ scales by $c^2$ under a gain $c$ of the image. Responses that depend only on $\lambda_2 / \lambda_1$ remove the gain, at the price of marking weak corners in noise.

## Reductions

- **To a $2 \times 2$ eigenvalue problem.** $\lambda_{1,2} = \frac{1}{2}\big(\operatorname{tr} M \pm \sqrt{(\operatorname{tr} M)^2 - 4 \det M}\big)$, so every response on $M$ costs $O(1)$ per pixel after the sums.
- **To filtering.** The sums in $M$ are three [linear filters](/linear-filtering/), such as a [Gaussian filter](/gaussian-filter/), of the images $I_x^2$, $I_y^2$ and $I_x I_y$.
- **Subpixel corner to least squares.** At an ideal corner $c$, every pixel $q$ near it lies on an edge through $c$, and its gradient is perpendicular to that edge, so $\nabla I(q)^{\mathsf T}(c - q) = 0$. Minimizing $\sum_q w\, (\nabla I(q)^{\mathsf T}(c - q))^2$ over $c$ gives the linear system $M c = \sum_q w\, \nabla I(q) \nabla I(q)^{\mathsf T} q$, which has the exact corner as its solution when $M$ is invertible.
- **To edge detection.** The same gradients serve [edge detection](/edge-detection/): a pixel with $\lambda_1$ large and $\lambda_2$ small is an edge pixel, so one pass gives both maps, which was the aim of Harris and Stephens.

## Applications

- Points to track in video and in visual odometry, where the corners of one frame are followed into the next.
- Point pairs for [image registration](/image-registration/), panoramas and camera calibration, where the corners of a checkerboard are found to subpixel accuracy.
- Structure from motion, where corners seen in many images give 3D points.
- A cheap first step before a descriptor is computed, in systems that need many features per frame on small devices.

## References
