---
tag: KVVV4N
kind: problem
slug: self-calibration
name: Self-calibration
aliases:
- autocalibration
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "Find the intrinsic parameters of a moving camera, and a metric reconstruction, from images of an unknown rigid scene alone, using only assumptions such as constant K or zero skew."
prereqs: [image-of-the-absolute-conic, kruppa-equations, projective-reconstruction-theorem]
see_also: [stratified-reconstruction, camera-calibration, bundle-adjustment, structure-from-motion-problem, critical-configurations, vanishing-point-calibration, image-stitching, sturm-triggs-factorization]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Chapter 19, Auto-calibration (Section 19.2 the algebraic framework, Section 19.3 the absolute dual quadric, Section 19.4 the Kruppa equations, Section 19.5 the stratified solution, Section 19.6 rotating cameras, Sections 19.8 and 19.9 planar motion and turntables)
  - paper: doi:10.1109/CVPR.1997.609388
    title: Bill Triggs, Autocalibration and the absolute quadric, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 1997, 609-614
    locator: the absolute dual quadric, its projection omega* = P Q* P^T in each view, and the autocalibration methods built on it
  - paper: doi:10.1023/A:1008109111715
    title: Marc Pollefeys, Reinhard Koch and Luc Van Gool, Self-calibration and metric reconstruction inspite of varying and unknown intrinsic camera parameters, International Journal of Computer Vision 32(1), 1999, 7-25
    locator: the counting argument for known, fixed and varying intrinsics, and the linear and nonlinear methods for a camera with a varying focal length
  - paper: doi:10.1109/CVPR.1997.609467
    title: Peter Sturm, Critical motion sequences for monocular self-calibration and uncalibrated Euclidean reconstruction, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 1997, 1100-1105
    locator: the classification of motion sequences for which self-calibration with a constant camera is not unique
  - paper: "Stephen J. Maybank and Olivier D. Faugeras, A theory of self-calibration of a moving camera, International Journal of Computer Vision 8(2), 1992, 123-151"
    title: Stephen J. Maybank and Olivier D. Faugeras, A theory of self-calibration of a moving camera, International Journal of Computer Vision 8(2), 1992, 123-151
    locator: the first theory of self-calibration from point matches, by the Kruppa equations
---

Self-calibration is the problem of finding the intrinsic parameters of a camera from images of an unknown, rigid scene, with no calibration object. The only inputs are point matches between the images and some assumptions on the cameras, for example that $K$ is the same in all views, or that the pixels have zero skew. From the matches alone, the [projective reconstruction theorem](/projective-reconstruction-theorem/) gives the cameras and the points only up to a projective transformation of space. The assumptions on $K$ select the metric reconstruction among them, and so also give $K$. This is different from [camera calibration](/camera-calibration/), where the scene has known geometry, and from [calibration from vanishing points](/vanishing-point-calibration/), where the scene has known right angles. The main tools are the [Kruppa equations](/kruppa-equations/), the absolute dual quadric, and the [stratified](/stratified-reconstruction/) approach through the plane at infinity.

## In plain words

You film a street with a camera whose settings you do not know. From the video you can match points from frame to frame. These matches give a 3D model, but a strange one: straight lines stay straight, yet angles and parallel lines can be wrong, as if seen in a distorting mirror.

Self-calibration fixes the model by using what you assume about the camera: for example that it kept the same settings all the time, or that its pixels are square. Of all the distorted models, only the true shape makes these assumptions hold in every frame. Finding it also gives the camera settings. It fails for some kinds of motion, for example when the camera only slides sideways without turning.

## Definition

**Input.** $N$ images of a static scene, with point matches. Equivalently, a projective reconstruction: cameras $P_1, \ldots, P_N$ and points $X_j$ with $x_{ij} \sim P_i X_j$. Also a set of assumptions on the intrinsic matrices $K_i$. Each parameter of $K_i$ can be known (for example zero skew, or a known principal point), unknown but the same in all views, or unknown and varying.

**Output.** The matrices $K_i$, and a projective transformation $H$ of space, a $4 \times 4$ invertible matrix, such that
$$P_i H = K_i [R_i \mid t_i] \quad \text{up to scale, for all } i,$$
with rotations $R_i$. Then the points $H^{-1} X_j$ form a metric reconstruction: correct up to a similarity (rotation, translation and global scale).

**Unknowns.** $H$ has 15 degrees of freedom. A similarity of space does not change the conditions, and it has 7. So the problem has $15 - 7 = 8$ essential unknowns: the 3 of the plane at infinity and the 5 of $K_1$. With the plane at infinity written as $\pi_\infty = (p, 1)$ in the projective frame where $P_1 = [I \mid 0]$, one can take
$$H = \begin{pmatrix} K_1 & 0 \\ -p^{\mathsf T} K_1 & 1 \end{pmatrix}.$$

**Equivalent form.** The absolute dual quadric is the $4 \times 4$ matrix $Q_\infty^\ast = \operatorname{diag}(1, 1, 1, 0)$ in a metric frame, and $H \operatorname{diag}(1, 1, 1, 0) H^{\mathsf T}$ in the projective frame. It is symmetric, of rank 3, and has 8 degrees of freedom. In each view it projects to the dual [image of the absolute conic](/image-of-the-absolute-conic/):
$$\omega_i^\ast = K_i K_i^{\mathsf T} \sim P_i \, Q_\infty^\ast \, P_i^{\mathsf T}.$$
In a metric frame this is direct: $K [R \mid t] \operatorname{diag}(1, 1, 1, 0) [R \mid t]^{\mathsf T} K^{\mathsf T} = K R R^{\mathsf T} K^{\mathsf T} = K K^{\mathsf T}$. Self-calibration is the search for a $Q_\infty^\ast$ for which every $P_i Q_\infty^\ast P_i^{\mathsf T}$ satisfies the assumptions on $K_i$ (Triggs 1997, HZ Section 19.3).

## Variants

- **Constant intrinsics.** One unknown $K$ for all views. This is the classic case of Maybank and Faugeras (1992).
- **Varying intrinsics.** A zoom or focus change changes $f$, and sometimes the principal point. Pollefeys, Koch and Van Gool (1999) showed that zero skew alone is enough in theory, with enough views.
- **Rotating camera.** All views share one center. There is no 3D reconstruction, but the views are related by homographies $H_i = K R_i K^{-1}$, and $\omega = H_i^{-\mathsf T} \omega H_i^{-1}$ gives linear equations on $\omega$ (HZ Section 19.6). This is how a panorama tool such as [image stitching](/image-stitching/) finds the focal length.
- **Restricted motion.** Planar motion and turntable motion have special methods with fewer unknowns (HZ Sections 19.8 and 19.9).
- **Stereo rigs.** A rig that moves rigidly gives two cameras with a fixed relation, which adds constraints (HZ Section 19.10).

## Examples

**Counting views.** Pollefeys, Koch and Van Gool (1999) count as follows. Let $n_k$ be the number of known intrinsic parameters per view and $n_f$ the number of unknown but fixed ones. Each known parameter gives one constraint in each of the $N$ views. Each fixed parameter gives one constraint in each view after the first, because its value in the first view is one of the unknowns. The constraints must at least match the 8 essential unknowns, so a necessary condition is
$$N n_k + (N - 1) n_f \ge 8.$$

| assumption | $n_k$ | $n_f$ | views needed |
|---|---|---|---|
| all 5 intrinsics constant and unknown | 0 | 5 | $5 (N - 1) \ge 8$, so $N \ge 3$ |
| zero skew known, other 4 constant | 1 | 4 | $N + 4 (N - 1) \ge 8$, so $N \ge 3$ |
| zero skew known, all others varying | 1 | 0 | $N \ge 8$ |
| zero skew and aspect ratio known, others varying | 2 | 0 | $N \ge 4$ |
| only the focal length unknown and varying | 4 | 0 | $N \ge 2$ |

This count is necessary, not sufficient: the motion must also not be critical.

**Kruppa count for a constant camera.** With constant $K$, each pair of views gives 2 Kruppa equations on the 5 unknowns of $\omega^\ast$. Three views give 3 pairs and 6 equations, which agrees with $N \ge 3$ above.

**A motion that fails.** Let a camera with $f = 800$ and $c = (320, 240)$ only translate. Then the fundamental matrix is $F = [e']_\times / \det K$, with $\det K = 640000$, and the Kruppa equations hold for every $\omega^\ast$. More generally, under pure translation the infinite homography between any two views is the identity, so $\omega = H^{-\mathsf T} \omega H^{-1}$ says nothing. The reconstruction is affine and stays affine: the scene can be stretched in any direction without breaking any assumption on $K$.

## Known algorithms

- **Kruppa equations.** Estimate the [fundamental matrix](/fundamental-matrix/) of each pair, write the 2 equations per pair, and solve the quadratic system for $\omega^\ast$, for example by [polynomial system solving](/polynomial-system-solving/) or by local optimization. It needs no consistent projective frame, but it is weaker than the methods below for some motions (Sturm 2000).
- **Absolute dual quadric.** From a projective reconstruction, solve for $Q_\infty^\ast$. If the constraints are linear in $\omega_i^\ast$, for example a known principal point moved to the origin and zero skew, then each view gives linear equations in the 10 entries of $Q_\infty^\ast$, and a linear least squares step gives it. Then enforce rank 3, get $H$ by an eigendecomposition, and refine (Triggs 1997, Pollefeys et al. 1999, HZ Section 19.3).
- **Stratified methods.** First find the plane at infinity, which upgrades the projective reconstruction to an affine one. With constant $K$, the modulus constraint says that the infinite homographies $K R_i K^{-1}$ have eigenvalues of equal modulus, which gives a quartic equation per view pair in the 3 unknowns of the plane. Then $\omega$ follows linearly from $\omega = H_\infty^{-\mathsf T} \omega H_\infty^{-1}$ (HZ Section 19.5). See [stratified reconstruction](/stratified-reconstruction/).
- **Rotating cameras.** Compute the homographies between the views and solve the linear equations on $\omega$, then get $K$ by the Cholesky factorization (HZ Section 19.6).
- **Bundle adjustment.** Every method above gives a start value. The final answer comes from a [bundle adjustment](/bundle-adjustment/) with the intrinsics as unknowns and the assumptions as constraints, which minimizes the reprojection error. This is the standard practice in structure from motion systems.

## Bounds

- **Unknowns and equations.** A projective to metric upgrade has 8 essential unknowns. Each pair of views gives at most 2 independent constraints of the Kruppa type, because a fundamental matrix has 7 degrees of freedom and a calibrated relative pose has 5.
- **Number of solutions.** For a constant camera and three views, 5 of the 6 Kruppa equations are quadrics in the 5 unknowns of $\omega^\ast$ up to scale, so the Bezout bound gives at most 32 isolated complex solutions. Only real solutions with a positive definite $\omega^\ast$ are valid.
- **Critical motions.** For a constant camera, Sturm (1997) classified the motion sequences for which the solution is not unique, whatever the method. They include pure translations (an affine ambiguity remains), pure rotations (the calibration can be found, but no reconstruction), and motions in which all the rotations have parallel axes, such as planar motion and orbital motion around an object. Real sequences close to these are badly conditioned.
- **Noise.** No accuracy bound holds without a noise model. In practice, self-calibration is much less accurate than calibration with a target, and errors in the principal point are large. This is an observation from experiments, not a theorem.

## Reductions

- **From projective reconstruction.** Self-calibration takes the output of a projective [structure from motion](/structure-from-motion-problem/) pipeline, for example [Sturm-Triggs factorization](/sturm-triggs-factorization/), and turns it into a metric one.
- **To affine plus metric upgrade.** Finding the plane at infinity reduces the problem to the affine case, where $\omega$ comes from linear equations.
- **To the calibrated case.** Once $K$ is known, every pair becomes a [relative pose problem](/relative-pose-problem/) of calibrated cameras.

## Applications

- 3D models from photos of unknown cameras, for example from the internet or from old footage, where no calibration is possible.
- Cameras whose zoom changes during a sequence, as in broadcast video and handheld recordings.
- Focal length estimation for panoramas from a rotating camera.
- A check of a target calibration: a self-calibration result that disagrees strongly with the target result points to an error in one of them.
