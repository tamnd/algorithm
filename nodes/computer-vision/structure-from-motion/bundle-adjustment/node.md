---
tag: A8YY0S
kind: problem
slug: bundle-adjustment
name: Bundle adjustment
aliases:
- photogrammetric bundle adjustment
area: computer-vision/structure-from-motion
level: core
summary: Refine all camera parameters and 3D points together to minimize the total reprojection error, a large sparse nonlinear least squares problem.
prereqs: [nonlinear-least-squares, reprojection-error]
see_also: [sparse-bundle-adjustment, inexact-newton-bundle-adjustment, reduced-camera-system, gauge-freedom, structure-from-motion-problem, incremental-structure-from-motion, pose-graph-optimization, optimal-triangulation]
sources:
  - paper: doi:10.1007/3-540-44480-7_21
    title: "Bill Triggs, Philip F. McLauchlan, Richard I. Hartley and Andrew W. Fitzgibbon, Bundle adjustment, a modern synthesis, in Vision Algorithms, Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 298-372"
    locator: "the whole survey: the problem and its cost functions (Sections 2 to 4), the network structure (Section 6), gauge freedom (Section 9) and the historical appendix"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 18, N-view computational methods (bundle adjustment and the affine factorization algorithm) and Appendix 6, Iterative estimation methods (sparse Levenberg-Marquardt)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM (bundle adjustment, exploiting sparsity, uncertainty and ambiguities)"
  - paper: doi:10.1145/1486525.1486527
    title: "Manolis I. A. Lourakis and Antonis A. Argyros, SBA: A software package for generic sparse bundle adjustment, ACM Transactions on Mathematical Software 36(1), 2009"
    locator: "the problem statement and the sparse structure of the Jacobian"
  - paper: doi:10.1007/978-3-642-15552-9_3
    title: "Sameer Agarwal, Noah Snavely, Steven M. Seitz and Richard Szeliski, Bundle adjustment in the large, Computer Vision ECCV 2010, Lecture Notes in Computer Science 6312, Springer, 2010, 29-42"
    locator: "the problem statement for large photo collections and the experiments"
---

Bundle adjustment is the problem of refining a 3D reconstruction, all camera parameters and all 3D points together, so that the predicted image positions of the points agree as well as possible with the measured ones. The cost is the sum of the squared [reprojection errors](/reprojection-error/), possibly weighted or made robust, over all observations. The name comes from photogrammetry: each camera has a bundle of light rays through its center, and the problem adjusts the bundles until the rays meet the points. It is a [nonlinear least squares](/nonlinear-least-squares/) problem with a special structure: each residual depends on one camera and one point only, so the Jacobian is very sparse and the normal equations have an arrow shape. Under Gaussian pixel noise its solution is the maximum likelihood reconstruction. It is the final, and usually the most accurate, step of [structure from motion](/structure-from-motion-problem/), and it runs repeatedly inside [incremental structure from motion](/incremental-structure-from-motion/) and visual SLAM. The cost is unchanged by a global similarity transformation (or a projective one, for uncalibrated cameras), which is the subject of [gauge freedom](/gauge-freedom/). The algorithms are pages of their own: [sparse bundle adjustment](/sparse-bundle-adjustment/) and [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/), both built on the [reduced camera system](/reduced-camera-system/).

## In plain words

You have many photos of a scene, and in each photo you have marked where some scene points appear. You also have a rough guess of where each camera stood, where it looked, and where each point is in 3D. Bundle adjustment improves all these guesses at once. For every mark, it computes where the guessed point would appear in the guessed camera, and it measures the distance to the real mark. It then moves the cameras and the points together until the total of these squared distances is as small as possible. The result is the reconstruction that best explains the photos. Moving or turning the whole scene, or making it bigger, does not change any distance, so one camera and the scale must be fixed to get a single answer.

## Definition

**Input.**
- $N$ cameras with start values. In the calibrated case, camera $i$ has a rotation $R_i \in SO(3)$ and a translation $t_i$, and a known intrinsic matrix $K_i = \begin{pmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix}$. In the self-calibrating case, $K_i$ and lens distortion terms are unknowns too.
- $n$ points $X_j \in \mathbb{R}^3$ with start values.
- $m$ observations $(i, j, x_{ij})$: point $j$ is measured at pixel $x_{ij}$ in camera $i$, optionally with a $2 \times 2$ covariance $\Sigma_{ij}$.

The camera frame has $X$ right, $Y$ down and $Z$ forward, a world point maps to $X_c = R_i X_j + t_i$, it is in front of the camera if $Z > 0$, and its pixel is $\pi(K_i X_c)$ with $\pi(u, v, w) = (u / w, v / w)$ and pixel centers at integer coordinates.

**Output.** Parameters that minimize
$$F = \frac12 \sum_{(i, j)} \rho\left( \| \pi(K_i (R_i X_j + t_i)) - x_{ij} \|^2_{\Sigma_{ij}} \right),$$
where $\|e\|^2_\Sigma = e^{\mathsf T} \Sigma^{-1} e$ and $\rho$ is the identity for the plain least squares cost or a robust function such as the [Huber](/huber-m-estimator/) cost. In practice a local minimizer near the start is found.

**Structure.** With 6 parameters per camera and 3 per point, there are $2m$ residuals and $6N + 3n$ unknowns. The residual $r_{ij}$ depends only on camera $i$ and point $j$, so each row pair of the Jacobian has one $2 \times 6$ block and one $2 \times 3$ block. The normal matrix $J^{\mathsf T} J = \begin{pmatrix} U & W \\ W^{\mathsf T} & V \end{pmatrix}$ has block diagonal $U$ and $V$; the block $W_{ij}$ is nonzero only where camera $i$ sees point $j$.

**Gauge.** For calibrated cameras, $F$ does not change under a similarity transformation of the world: $X_j \to s Q X_j + c$, $R_i \to R_i Q^{\mathsf T}$, $t_i \to s t_i - R_i Q^{\mathsf T} c$, with 7 degrees of freedom. For uncalibrated projective cameras the invariance group is the projective group, with 15 degrees of freedom. So the minimizer is never unique, and $J^{\mathsf T} J$ is singular; see [gauge freedom](/gauge-freedom/).

## Variants

- **Calibrated or self-calibrating.** Intrinsics fixed, shared by all cameras, or one set per camera; often with radial and tangential distortion.
- **Projective bundle adjustment.** Unknown $3 \times 4$ camera matrices $P_i$ and homogeneous points; the gauge has 15 degrees of freedom.
- **Robust bundle adjustment.** A robust $\rho$, such as Huber or Cauchy, limits the effect of wrong matches; it is solved by reweighting, see [M-estimators](/m-estimator/).
- **Motion only and structure only.** Fix the points and refine the cameras ([perspective-n-point](/perspective-n-point/) refinement), or fix the cameras and refine the points ([optimal triangulation](/optimal-triangulation/) for two views). Each splits into independent small problems.
- **Local and windowed.** Refine only recent cameras and the points they see, as in [sliding window bundle adjustment](/sliding-window-bundle-adjustment/) and the local bundle adjustment of [ORB-SLAM](/orb-slam/).
- **With other measurements.** Add residuals for GPS positions, inertial measurements, known distances or control points.
- **Other features and camera models.** Lines, points at infinity in homogeneous form, inverse depth points, rolling shutter cameras, and fisheye or spherical cameras.
- **Photometric bundle adjustment.** Minimize differences of pixel intensities instead of feature positions, as in direct visual odometry.

## Examples

**A small synthetic scene.** Four cameras with $f_x = f_y = 800$ and $(c_x, c_y) = (320, 240)$ look from a distance of about 5 at 20 points in a cube of side 2. Every camera sees every point: $m = 80$ observations, 160 residuals. With camera 0 fixed, there are $18 + 60 = 78$ unknowns, of which one direction (the scale) is still a gauge freedom. Starting from cameras and points perturbed to an RMS reprojection error of 34.1 pixels, sparse Levenberg-Marquardt reaches $4.6 \cdot 10^{-13}$ pixels in 12 accepted steps on exact data, and the result equals the truth up to a scale of $0.99695$. With 1 pixel of Gaussian noise, the minimum cost is $52.9$, lower than the cost $95.4$ of the true scene. The minimizer fits the noise better than the truth, as any maximum likelihood estimate does. These are measurements from the test of [sparse bundle adjustment](/sparse-bundle-adjustment/).

**Counting.** For calibrated cameras, the reconstruction is locally determined, up to the gauge, only if the number of residuals is at least the number of unknowns minus the gauge: $2m \ge 6N + 3n - 7$. The example has $160 \ge 77$. Two calibrated views of five points give $20 = 12 + 15 - 7$: the count of the minimal [five-point problem](/five-point-algorithm/).

**Large photo collections.** Reconstructions from internet photos have thousands of cameras and millions of points, with each point seen by only a few cameras. Agarwal, Snavely, Seitz and Szeliski (2010) studied problems of this size.

## Known algorithms

| algorithm | cost per iteration | note |
|---|---|---|
| [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/), dense | $O((6N + 3n)^3)$ | only for tiny problems |
| [Sparse bundle adjustment](/sparse-bundle-adjustment/) | $O(m + \sum_j c_j^2 + N^3)$ | exact damped step via the [reduced camera system](/reduced-camera-system/) |
| Sparse bundle adjustment with sparse Cholesky of $S$ | depends on the fill of $S$ | for sparse camera graphs |
| [Powell's dog leg](/powell-dogleg/), sparse | as sparse bundle adjustment | fewer factorizations after rejected steps |
| [Inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/) | $O(k (m + N))$ for $k$ CG iterations | very large problems |
| [Iteratively reweighted least squares](/iteratively-reweighted-least-squares/) around any of these | as the inner method | robust costs |

Here $c_j$ is the number of cameras that see point $j$. All of these find a local minimizer from a good start. The start comes from [incremental](/incremental-structure-from-motion/) or [global structure from motion](/global-structure-from-motion/), or from a [factorization method](/tomasi-kanade-factorization/).

## Bounds

- **No global guarantee.** The cost is nonconvex, and the standard methods find a local minimizer only. No polynomial time algorithm for the global minimum of general bundle adjustment is known. The [nonlinear least squares](/nonlinear-least-squares/) page shows that the general problem is NP-hard, but that proof uses residuals of another form and does not carry over to bundle adjustment.
- **Accuracy bound (theorem).** With independent Gaussian pixel noise of standard deviation $\sigma$, the covariance of any unbiased estimate of the gauge-fixed parameters is at least $\sigma^2 (J^{\mathsf T} J)^{-1}$ restricted to those parameters, the [Cramér-Rao bound](/cramer-rao-bound/), and the maximum likelihood estimate reaches it to first order for small noise. Because of the gauge, the bound is stated for gauge-invariant quantities or for a fixed gauge; Kanatani and Morris (2001) treat this in detail.
- **Expected residual.** At the minimizer, $2F / \sigma^2$ is approximately chi-squared with $2m - (6N + 3n - 7)$ degrees of freedom, so the RMS residual per coordinate is a little below $\sigma$. This is used to check the noise model.
- **Cost of a step.** Any exact method must at least read the $m$ observations, so a step costs $\Omega(m)$. With the reduced camera system, the extra cost is that of solving a $6N \times 6N$ system.

## Reductions

- **To nonlinear least squares.** Bundle adjustment is an instance of nonlinear least squares, with the rotation updated on $SO(3)$ by a local parametrization, for example $R \leftarrow \exp([\omega]_\times) R$.
- **To the reduced camera system.** Each Gauss-Newton or Levenberg-Marquardt step reduces exactly to a linear system in the camera parameters, followed by independent $3 \times 3$ solves for the points.
- **Affine cameras.** For affine cameras with every point seen in every view, the maximum likelihood solution under isotropic Gaussian noise is given in closed form by the [factorization method](/tomasi-kanade-factorization/) of Tomasi and Kanade, a truncated SVD (theorem; Hartley and Zisserman, Chapter 18).
- **To pose graph optimization.** Eliminating the points, or approximating their effect by relative pose constraints, gives a [pose graph optimization](/pose-graph-optimization/) problem, which is smaller and often used to start or to replace bundle adjustment in SLAM.

## Applications

- Structure from motion: the final refinement, and repeated refinements during incremental reconstruction.
- Visual SLAM and visual odometry: local bundle adjustment over a window of key frames, as in [ORB-SLAM](/orb-slam/) and [visual odometry](/visual-odometry/) systems.
- Aerial and close range photogrammetry, mapping and surveying, where the method comes from.
- Camera calibration: the final refinement of [Zhang's method](/zhang-calibration-method/) is a bundle adjustment with a known planar target.
- Multi-camera rigs and augmented reality, where the camera poses must be accurate to a fraction of a pixel.

## References
