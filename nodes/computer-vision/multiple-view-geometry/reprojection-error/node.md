---
tag: SHPECC
kind: definition
slug: reprojection-error
name: Reprojection error
aliases:
- reprojection residual
area: computer-vision/multiple-view-geometry
level: intro
summary: The image distance between a measured point and the projection of its estimated 3D point by the estimated camera, the usual cost in geometric vision.
prereqs: [camera-projection-matrix, maximum-likelihood-estimation]
see_also: [bundle-adjustment, algebraic-and-geometric-error, sampson-distance, optimal-triangulation, perspective-n-point, cheirality, brown-conrady-distortion-model, homography-estimation]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.2, Different cost functions (the reprojection error in both images and its geometric interpretation) and Section 4.3, Statistical cost functions and maximum likelihood estimation"
  - paper: doi:10.1007/3-540-44480-7_21
    title: "Bill Triggs, Philip McLauchlan, Richard Hartley and Andrew Fitzgibbon, Bundle adjustment - a modern synthesis, Vision Algorithms: Theory and Practice, LNCS 1883, Springer, 2000, 298-372"
    locator: the sum of squared image residuals as the cost of bundle adjustment, its statistical meaning and its robust forms
---

The reprojection error of an image point is the distance in the image between where the point was measured and where the estimated camera projects the estimated 3D point. Summed in squares over all observations, it is the cost that [bundle adjustment](/bundle-adjustment/), [optimal triangulation](/optimal-triangulation/) and the refinement step of most pose and homography methods minimize. Under independent isotropic Gaussian noise on the image points it is, up to a constant factor and offset, the negative log-likelihood, so its minimizer is the maximum likelihood estimate. The page [algebraic and geometric error](/algebraic-and-geometric-error/) compares it with the residuals of linear methods, and the [Sampson distance](/sampson-distance/) is its first-order approximation when the 3D point is eliminated.

## Definition

Let $P_j$ be the estimated $3 \times 4$ [camera matrix](/camera-projection-matrix/) of view $j$, let $\mathbf{X}_i$ be the estimated 3D point $i$ in homogeneous form, and let $\mathbf{x}_{ij} \in \mathbb{R}^2$ be the measured image of point $i$ in view $j$. Write $\pi(u, v, w) = (u/w, v/w)$ for the map from homogeneous to pixel coordinates. The **reprojection residual** and the **reprojection error** of this observation are

$$\mathbf{r}_{ij} = \mathbf{x}_{ij} - \pi(P_j\mathbf{X}_i), \qquad d_{ij} = \|\mathbf{r}_{ij}\| .$$

The **total reprojection error** over the set $\mathcal{O}$ of observed pairs $(i, j)$ is

$$E = \sum_{(i, j) \in \mathcal{O}} \|\mathbf{x}_{ij} - \pi(P_j\mathbf{X}_i)\|^2 .$$

The **root mean square (RMS) reprojection error** is $\sqrt{E / |\mathcal{O}|}$, in pixels. Some programs divide by $2|\mathcal{O}|$, the number of scalar residuals, which gives a value smaller by the factor $\sqrt2$; say which one you report.

If the camera model has lens distortion, $\pi$ includes it (for example the [Brown-Conrady model](/brown-conrady-distortion-model/)). If the calibration $K$ is known, the error can also be measured in normalized image coordinates, and then it is the pixel error divided by the focal length, for square pixels.

**Two views of a plane.** For a [homography](/homography/) the same idea gives the cost $\sum_i d(\mathbf{x}_i, \hat{\mathbf{x}}_i)^2 + d(\mathbf{x}'_i, H\hat{\mathbf{x}}_i)^2$, minimized over $H$ and corrected points $\hat{\mathbf{x}}_i$ (HZ Section 4.2). The corrected points play the part of the 3D points.

**Maximum likelihood.** Suppose each measured point is the true projection plus independent Gaussian noise with covariance $\sigma^2 I$. The likelihood of the data is $\prod (2\pi\sigma^2)^{-1} \exp(-d_{ij}^2 / 2\sigma^2)$, and its negative logarithm is $E / 2\sigma^2$ plus a constant. So the cameras and points that minimize $E$ are the [maximum likelihood estimate](/maximum-likelihood-estimation/). If the noise of each point has its own covariance $\Sigma_{ij}$, the right cost is the sum of $\mathbf{r}_{ij}^{\mathsf T}\Sigma_{ij}^{-1}\mathbf{r}_{ij}$.

**Residual at the optimum.** With $N$ scalar measurements and $d$ free parameters, the minimum of $E$ is, to first order in the noise, $\sigma^2$ times a chi-square variable with $N - d$ degrees of freedom, with mean $\sigma^2(N - d)$. This gives a check of the noise level and of the model.

## Examples and non-examples

- **One observation.** Let $K = \begin{pmatrix} 500 & 0 & 320 \\ 0 & 500 & 240 \\ 0 & 0 & 1 \end{pmatrix}$, $P = K[I \mid \mathbf{0}]$ and $\mathbf{X} = (0.2, -0.1, 2, 1)^{\mathsf T}$. Then $P\mathbf{X} = (740, 430, 2)^{\mathsf T}$ and $\pi(P\mathbf{X}) = (370, 215)$. If the point was measured at $(371.5, 213)$, the residual is $(1.5, -2)$, the reprojection error is $2.5$ pixels and the squared error is $6.25$.
- **RMS over a set.** Three observations with errors $1$, $2$ and $2$ pixels give $E = 9$ and an RMS error of $\sqrt{9/3} = \sqrt3 \approx 1.73$ pixels.
- **Non-example: the algebraic residual.** $\|\mathbf{x}_{ij} \times P_j\mathbf{X}_i\|$ with $\mathbf{x}_{ij}$ in homogeneous form is 0 exactly when the reprojection error is 0, but otherwise it is the reprojection error times the depth factor $w$ of $P_j\mathbf{X}_i$ (up to the scale of $P_j$ and $\mathbf{X}_i$). It is not a distance in pixels.
- **Non-example: error in 3D.** The distance in space between $\mathbf{X}_i$ and the ray through $\mathbf{x}_{ij}$ is a different cost. It grows with depth for the same image error, so it gives far points too much weight.
- **Non-example: a point behind the camera.** $\pi(P\mathbf{X}) = \pi(-P\mathbf{X})$, so a point behind the camera can have a reprojection error of 0. The error does not check [cheirality](/cheirality/); a method that minimizes it must check the sign of the depth on its own.

## Related definitions

- [Algebraic and geometric error](/algebraic-and-geometric-error/): the reprojection error is the main geometric error; the residuals of linear methods are algebraic.
- [Sampson distance](/sampson-distance/): a first-order estimate of the reprojection error of a match without solving for the 3D point or the corrected points.
- [Bundle adjustment](/bundle-adjustment/): minimizes the total reprojection error over all cameras and points, often with a robust loss such as the Huber loss in place of the square.
- [Optimal triangulation](/optimal-triangulation/) minimizes it over one 3D point with two known cameras; [perspective-n-point](/perspective-n-point/) refinement minimizes it over one camera pose with known 3D points.
- [Homography estimation](/homography-estimation/): the Gold Standard method minimizes the two-view form above.

## References
