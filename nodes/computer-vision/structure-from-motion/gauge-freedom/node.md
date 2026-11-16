---
tag: GBXBCP
kind: concept
slug: gauge-freedom
name: Gauge freedom
aliases:
- gauge ambiguity
- datum problem
area: computer-vision/structure-from-motion
level: advanced
summary: The directions in which a reconstruction can move, such as a global similarity, without changing the cost, which make the normal equations singular until fixed.
prereqs: [bundle-adjustment]
see_also: [reduced-camera-system, sparse-bundle-adjustment, similarity-transformation, projective-reconstruction-theorem, pseudoinverse, cramer-rao-bound, fisher-information-matrix, tikhonov-regularization]
sources:
  - paper: doi:10.1007/3-540-44480-7_21
    title: "Bill Triggs, Philip F. McLauchlan, Richard I. Hartley and Andrew W. Fitzgibbon, Bundle adjustment, a modern synthesis, in Vision Algorithms, Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 298-372"
    locator: "Section 9, Gauge freedom (the gauge group, gauge constraints, inner constraints and gauge invariant covariances)"
  - paper: doi:10.1007/3-540-44480-7_12
    title: "Philip F. McLauchlan, Gauge independence in optimization algorithms for 3D vision, in Vision Algorithms, Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 183-199"
    locator: "the whole paper (how the choice of gauge affects the iterations, and gauge independent algorithms)"
  - paper: doi:10.1109/18.930934
    title: "Kenichi Kanatani and Daniel D. Morris, Gauges and gauge transformations for uncertainty description of geometric structure with indeterminacy, IEEE Transactions on Information Theory 47(5), 2001, 2017-2028"
    locator: "the whole paper (gauges, gauge transformations of the covariance and the normal form of the covariance)"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 10, 3D reconstruction of cameras and structure (the projective, affine and metric ambiguity of a reconstruction) and Appendix 6, Iterative estimation methods (parametrization and the singular normal equations)"
---

Gauge freedom is the set of transformations of the parameters of a problem that leave its cost exactly unchanged, because they change only the coordinate frame and not the thing being measured. In [bundle adjustment](/bundle-adjustment/) with calibrated cameras, the images say nothing about where the world origin is, which way its axes point, or how large the scene is. Any [similarity transformation](/similarity-transformation/) of all points and cameras, 3 for rotation, 3 for translation and 1 for scale, gives the same reprojection errors. So the cost is constant along a 7-dimensional family of solutions through every point, the Jacobian has a 7-dimensional null space, and the normal matrix $J^{\mathsf T} J$ is singular. For uncalibrated projective cameras, the family is the 15-dimensional group of 3D projective transformations, as the [projective reconstruction theorem](/projective-reconstruction-theorem/) states. In photogrammetry this is called the datum problem. A gauge is a rule that picks one solution from each family, such as fixing the first camera and the distance to the second. The choice of gauge does not change the reconstruction up to the transformation, but it changes the numbers, the covariance matrices and, in floating point, the behavior of the solver.

## In plain words

Suppose you measure the distances between three towns and draw a map. The distances fix the shape of the map, but not where it sits on the paper or which way it points. You may slide it or turn it, and every distance stays right. To draw one definite map you must decide, for example, that the first town is at the center and the second is straight up from it. Bundle adjustment has the same problem in 3D, with one more freedom: photos do not show how big the scene is, so the map can also grow or shrink. These free moves are the gauge freedom. Before solving, or while solving, you must pin them down somehow.

## The idea

**The gauge group.** Let $x$ hold all parameters and $F(x) = \tfrac12 \|r(x)\|^2$. A group $G$ acts on the parameters, $x \mapsto g \cdot x$, with $r(g \cdot x) = r(x)$ for all $g$. For calibrated bundle adjustment, $g = (s, Q, c)$ acts by
$$X_j \mapsto s Q X_j + c, \qquad R_i \mapsto R_i Q^{\mathsf T}, \qquad t_i \mapsto s t_i - R_i Q^{\mathsf T} c,$$
and then $R_i X_j + t_i$ is multiplied by $s$, so its projection does not change. $G$ is the similarity group, of dimension 7. If the scale is known, for example from a stereo rig with a known baseline or from an inertial sensor, $G$ is the 6-dimensional group of rigid motions. For projective cameras $P_i \mapsto P_i H^{-1}$, $X_j \mapsto H X_j$ with $H$ a $4 \times 4$ nonsingular matrix up to scale, which has 15 degrees of freedom. A residual that measures the cameras directly, such as a GPS position, removes freedoms.

**The null space (theorem).** Differentiating $r(g(\epsilon) \cdot x) = r(x)$ with respect to a one-parameter family $g(\epsilon)$ through the identity gives $J(x) \, v = 0$ with $v = \tfrac{d}{d\epsilon} g(\epsilon) \cdot x$ at $\epsilon = 0$. The tangent vectors of the orbit $G \cdot x$ are in the null space of $J$. So $J^{\mathsf T} J$ has at least $\dim G$ zero eigenvalues. For a generic scene with enough views and points, the null space is exactly the tangent space of the orbit; any further null direction is a real ambiguity of the scene, not a gauge.

**Fixing the gauge.** There are four common ways.

1. *Fix parameters.* Remove parameters from the unknowns: fix the pose of camera 0 (6 freedoms) and one more number, such as the distance between camera 0 and camera 1, or one coordinate of a point (scale). This is simple and keeps the sparse structure.
2. *Add constraints.* Require, for example, that the centroid of the points is $0$ and their mean distance from it is $1$. These are 4 of the 7 conditions; the rotation needs 3 more. Constraints are handled by Lagrange multipliers or by a projection.
3. *Inner constraints, or free network adjustment.* Choose the update orthogonal to the gauge directions, which gives the minimum norm solution, as with the [pseudoinverse](/pseudoinverse/) of $J^{\mathsf T} J$. In photogrammetry this is the free network adjustment; its covariance is the pseudoinverse of the information matrix.
4. *Let the damping handle it.* Levenberg-Marquardt adds $\mu I$, which makes the matrix positive definite and suppresses the step along the gauge directions. The solution then drifts slowly along the orbit, which is harmless as long as only gauge invariant results are used.

**Covariance depends on the gauge (theorem).** The covariance of the estimate is only defined after a gauge is chosen, and different gauges give different covariance matrices. For example, with camera 0 fixed, the reported uncertainty of a point tends to grow with its distance from camera 0, while with a centroid gauge it is spread more evenly. Quantities that do not change under $G$, such as angles, ratios of distances and reprojected positions, have the same covariance in every gauge. Kanatani and Morris (2001) give the transformation rules for covariances between gauges and a normal form; Triggs et al. (2000) treat gauge invariant covariances in Section 9. The [Cramér-Rao bound](/cramer-rao-bound/) must also be stated for a fixed gauge or for invariant quantities, since the [Fisher information matrix](/fisher-information-matrix/) is singular.

**The effect on the solver.** McLauchlan (2000) studied how the gauge choice affects the iterations of the optimization and described algorithms whose results do not depend on it. In practice, the gauge also changes the conditioning of the matrices that the solver factors, so two gauges can need different numbers of iterations to reach the same reconstruction.

## Examples

**The null space of a small scene.** Take the test scene of [sparse bundle adjustment](/sparse-bundle-adjustment/): 4 calibrated cameras, 20 points, 80 observations, at the true parameters. With all cameras free there are $24 + 60 = 84$ unknowns. The 84 eigenvalues of $J^{\mathsf T} J$, computed with the Jacobi method, are: seven with absolute value at most $1.5 \cdot 10^{-10}$, then $41.6$, $695$ and so on up to $1.41 \cdot 10^{7}$. The seven are the similarity gauge, zero up to rounding. With camera 0 fixed (78 unknowns), one eigenvalue $9.6 \cdot 10^{-13}$ remains, the scale, and the next is $36.1$. Fixing also the scale would make the matrix nonsingular. Running sparse bundle adjustment with only camera 0 fixed, the result on exact data equals the truth multiplied by a scale of $0.99695$: the iterations moved along the remaining gauge direction.

**Points on a line.** Measure the differences $x_2 - x_1$ and $x_3 - x_2$ of three numbers. The Jacobian of the residuals $(x_2 - x_1 - d_1, x_3 - x_2 - d_2)$ has the null vector $(1, 1, 1)$: adding the same number to all three changes nothing. Fixing $x_1 = 0$, or requiring $x_1 + x_2 + x_3 = 0$, picks one solution. With $x_1 = 0$, the variance of $x_3$ is twice that of $x_2$ when both measurements have equal variance; with the centroid gauge, $x_1$ and $x_3$ have equal variance. The distances themselves have the same variance in both gauges.

**Two views.** Two calibrated views determine the relative pose only up to the scale of the translation; this is why the [essential matrix](/essential-matrix/) has 5 degrees of freedom while the relative pose has 6.

**Projective reconstruction.** Without calibration, a reconstruction from any number of views is determined only up to a $4 \times 4$ projective transformation; the gauge has 15 dimensions, and metric information is needed to reduce it to 7.

## Where it is used

- Every bundle adjustment implementation fixes the gauge in one of the ways above, usually by fixing the first camera and letting the damping, or one extra constraint, handle the scale. See [sparse bundle adjustment](/sparse-bundle-adjustment/) and the [reduced camera system](/reduced-camera-system/), whose matrix $S$ is singular without it.
- Uncertainty estimates of reconstructions, where the reported covariance must state its gauge.
- Pose graph optimization and SLAM, where the first pose is fixed, and visual-inertial systems, where gravity makes two rotation angles observable and the gauge has 4 dimensions: yaw and the 3 translations.
- Photogrammetry, as the datum definition by control points or by free network adjustment.
- Outside vision, the same idea appears in network adjustment in geodesy, in [Tikhonov regularization](/tikhonov-regularization/) of rank deficient problems, and in physics, where the name comes from.

## References
