---
tag: GPS316
kind: concept
slug: algebraic-and-geometric-error
name: Algebraic and geometric error
aliases:
- algebraic distance
- geometric distance
area: computer-vision/multiple-view-geometry
level: core
summary: The residual of a linear equation such as Ah = 0 is cheap to minimize but has no geometric meaning; the image distance is meaningful but needs nonlinear optimization.
prereqs: [homography-estimation, reprojection-error]
see_also: [dlt-homography, sampson-distance, hartley-normalization, maximum-likelihood-estimation, levenberg-marquardt, linear-triangulation, optimal-triangulation, bundle-adjustment]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.2, Different cost functions (algebraic distance, geometric distance, reprojection error in both images, the geometric interpretation of the reprojection error and the Sampson error), Section 4.3, Statistical cost functions and maximum likelihood estimation, and Section 4.4, Transformation invariance and normalization"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 8.1, Pairwise alignment (linear and iterative least squares for 2D motion models)"
---

In the estimation problems of multiple view geometry two kinds of cost are minimized. The algebraic error is the residual $\|A\mathbf{h}\|$ of a system of linear equations in the unknown entries of a matrix; the geometric error is a sum of squared distances in the image, in pixels. The algebraic error has a closed-form minimizer by the [SVD](/singular-value-decomposition/), but it weights the points in a way that depends on the data and on the coordinate frame. The geometric error is the statistically right cost, but it needs an iterative method and a starting point. This page compares the two; the [reprojection error](/reprojection-error/) is the main geometric error and has its own page, and the [Sampson distance](/sampson-distance/) is a first-order approximation that sits between them.

## In plain words

There are two ways to ask how wrong a guess is. The first plugs the guess into the equations and looks at how far each equation is from zero. This is easy to make as small as possible, with one standard matrix step and no guessing. But an equation can be far from zero only because its numbers are large, so this way counts some points more than others for no good reason, and the count changes if you move the origin of the image. The second way measures, on the image, how far each predicted point is from where it was seen. This is what you really care about, and with typical camera noise it gives the most likely answer. But it can only be reduced step by step from a starting guess. So the usual recipe is to start with the first way and finish with the second.

## The idea

**Algebraic error.** For a homography, each pair $\mathbf{x}_i \leftrightarrow \mathbf{x}'_i$ gives two linear equations $A_i\mathbf{h} = \mathbf{0}$, the first two entries of $\mathbf{x}'_i \times H\mathbf{x}_i$ (see [DLT for homographies](/dlt-homography/)). The algebraic distance of the pair is $d_{\mathrm{alg}}(\mathbf{x}'_i, H\mathbf{x}_i) = \|A_i\mathbf{h}\|$, and the [DLT](/dlt-homography/) minimizes $\sum_i \|A_i\mathbf{h}\|^2 = \|A\mathbf{h}\|^2$ subject to $\|\mathbf{h}\| = 1$. The constraint is needed, since $\mathbf{h} = \mathbf{0}$ would give 0.

**Geometric error.** It uses $d(\cdot, \cdot)$, the Euclidean distance between two image points. The common forms for a homography are:

- the transfer error $\sum_i d(\mathbf{x}'_i, H\mathbf{x}_i)^2$, with the error in the second image only;
- the symmetric transfer error $\sum_i d(\mathbf{x}_i, H^{-1}\mathbf{x}'_i)^2 + d(\mathbf{x}'_i, H\mathbf{x}_i)^2$;
- the [reprojection error](/reprojection-error/) $\sum_i d(\mathbf{x}_i, \hat{\mathbf{x}}_i)^2 + d(\mathbf{x}'_i, H\hat{\mathbf{x}}_i)^2$, minimized also over corrected points $\hat{\mathbf{x}}_i$.

**How they relate.** Write $\mathbf{x}'_i = (x'_i, y'_i, 1)^{\mathsf T}$ and $H\mathbf{x}_i = (a_i, b_i, c_i)^{\mathsf T}$. The two equations are $y'_i c_i - b_i$ and $a_i - x'_i c_i$, so

$$d_{\mathrm{alg}}(\mathbf{x}'_i, H\mathbf{x}_i) = |c_i| \, d(\mathbf{x}'_i, H\mathbf{x}_i) .$$

The algebraic distance is the transfer distance multiplied by the weight $|c_i| = |\mathbf{h}^{3\mathsf T}\mathbf{x}_i|$, the third entry of $H\mathbf{x}_i$. The weight changes from point to point when $H$ is projective, and it depends on how $H$ is scaled. For an affine $H$, the third row is $(0, 0, h_{33})$, the weight is the same for all points, and the DLT minimizes the transfer error (HZ Section 4.2.5).

**Frame dependence.** Change the coordinates of the two images by similarities $T$ and $T'$. Distances in pixels change by fixed factors, so the minimizer of a geometric error moves with the data: the best $H$ becomes $T' H T^{-1}$. The algebraic error with the constraint $\|\mathbf{h}\| = 1$ does not behave like this, because $\|T' H T^{-1}\|_F$ is not a fixed multiple of $\|H\|_F$ when $T'$ contains a translation. So the DLT on raw coordinates gives an answer that depends on where the origin of each image is. [Hartley normalization](/hartley-normalization/) fixes the frame in a canonical way and removes this dependence.

**Statistics.** If the measured points have independent isotropic Gaussian noise, the [maximum likelihood estimate](/maximum-likelihood-estimation/) minimizes the reprojection error (HZ Section 4.3). With noise only in the second image it minimizes the transfer error. The algebraic error has no such meaning.

**Cost.** The algebraic minimizer is one SVD of a matrix with a fixed number of columns, $O(n)$ for $n$ pairs, with no start and no iterations. The geometric minimizer needs an iterative method such as [Levenberg-Marquardt](/levenberg-marquardt/), a good start, and it can stop in a local minimum. This is why the usual pipeline is: algebraic estimate on normalized points, then geometric refinement.

## Examples

- **Same pixel error, different algebraic error.** Let $H = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 1 & 0 & 1 \end{pmatrix}$. The point $(0, 0)$ maps to $(0, 0, 1)^{\mathsf T}$, so $c = 1$; the point $(1, 0)$ maps to $(1, 0, 2)^{\mathsf T} \sim (0.5, 0)$, so $c = 2$. Suppose the measured matches are $(1, 0)$ and $(1.5, 0)$. Both are 1 pixel from their predictions. The algebraic distances are $1 \cdot 1 = 1$ and $2 \cdot 1 = 2$: the second point counts four times as much in the squared sum.
- **The origin changes the answer.** For $H = I$, $\|H\|_F = \sqrt3$. Move the origin of image 2 by 100 pixels along $x$: the same map is now $\begin{pmatrix} 1 & 0 & 100 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$, with Frobenius norm $\sqrt{10003}$. Under the constraint $\|\mathbf{h}\| = 1$ the first form is divided by $\sqrt3 \approx 1.7$ and the second by about 100, so the weights $|c_i|$ of this map drop by a factor of about 58 when the origin moves. A candidate matrix with other entries changes its norm by another factor, so the ranking of the candidates, and with it the minimizer, depends on the frame.
- **Affine case.** For $H = \begin{pmatrix} 2 & 0 & 1 \\ 0 & 2 & 3 \\ 0 & 0 & 1 \end{pmatrix}$, $c_i = 1$ for every point, so the algebraic distance of every pair equals its transfer distance.
- **Triangulation.** The [linear triangulation](/linear-triangulation/) method minimizes an algebraic error and is not invariant to projective changes of frame; the [optimal triangulation](/optimal-triangulation/) method minimizes the reprojection error of the point in both images.

## Where it is used

- **Linear initialization.** The [DLT](/dlt-homography/), [DLT resectioning](/dlt-camera-resectioning/), the [eight-point algorithm](/eight-point-algorithm/) and linear triangulation all minimize an algebraic error.
- **Refinement.** The Gold Standard method for homographies, [bundle adjustment](/bundle-adjustment/) and optimal triangulation minimize a geometric error.
- **Scoring in robust fitting.** [RANSAC](/ransac/) tests each match against a threshold in pixels, so it needs a geometric distance or the [Sampson distance](/sampson-distance/), not the algebraic one.
- **Reporting accuracy.** Results are reported in pixels, as root mean square transfer or reprojection error, because those numbers have a meaning that does not depend on the frame.

## References
