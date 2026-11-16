---
tag: 8W9F6Q
kind: problem
slug: nonlinear-least-squares
name: Nonlinear least squares
aliases:
- NLLS
- nonlinear least squares problem
area: computer-vision/structure-from-motion
level: core
summary: Minimize a sum of squared nonlinear residuals of the parameters, the form of bundle adjustment, calibration and most refinement steps in vision.
prereqs: [least-squares-problem]
see_also: [gauss-newton-algorithm, levenberg-marquardt, powell-dogleg, bundle-adjustment, curve-fitting, maximum-likelihood-estimation, m-estimator, systems-of-nonlinear-equations]
sources:
  - book: isbn:9780387303031
    title: "Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006"
    locator: "Chapter 10, Least-squares problems (the structure of the gradient and the Hessian, the Gauss-Newton and Levenberg-Marquardt methods, large residual problems)"
  - book: isbn:9780898713640
    title: "J. E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996"
    locator: "Chapter 10, Nonlinear least squares (the problem, the Gauss-Newton and Levenberg-Marquardt methods and the methods for large residuals)"
  - paper: "Kaj Madsen, Hans Bruun Nielsen and Ole Tingleff, Methods for Non-Linear Least Squares Problems, second edition, Informatics and Mathematical Modelling, Technical University of Denmark, 2004"
    locator: "Chapter 1 (the problem and the conditions for a local minimizer) and Chapter 3 (the Gauss-Newton, Levenberg-Marquardt and dog leg methods)"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Appendix 6, Iterative estimation methods (the iterative minimization of geometric cost functions, robust cost functions and the choice of parametrization)"
---

Nonlinear least squares is the problem of finding the parameters $x \in \mathbb{R}^n$ that minimize $F(x) = \tfrac12 \sum_{i=1}^m r_i(x)^2$, where each residual $r_i$ is a smooth but nonlinear function of $x$. It is the standard way to fit a model to data when the model is not linear in its parameters: the residuals are the differences between predicted and measured values. When the measurement errors are independent Gaussian with equal variance, its solution is the [maximum likelihood estimate](/maximum-likelihood-estimation/). Unlike the linear [least squares problem](/least-squares-problem/), it has no closed form, it can have many local minimizers, and it is solved by iteration from a start. The main iterative methods are pages of their own: the [Gauss-Newton algorithm](/gauss-newton-algorithm/) linearizes the residuals and solves the normal equations, [Levenberg-Marquardt](/levenberg-marquardt/) adds damping to keep the cost decreasing, and [Powell's dog leg method](/powell-dogleg/) uses a trust region. In computer vision almost every refinement step has this form, and the largest instance is [bundle adjustment](/bundle-adjustment/), which minimizes the reprojection error over all cameras and points.

## In plain words

You have a model with some unknown numbers and many measurements. For each measurement you can compute how far the model is from it. You want the unknown numbers that make the total of the squared distances as small as possible. If the model were a straight line, one formula would give the answer. Here the model bends, for example through an exponential or a rotation, so there is no single formula. You start from a guess and improve it step by step. There can be several "best" spots in different places, and which one you reach depends on where you start.

## Definition

**Input.** A residual function $r: \mathbb{R}^n \to \mathbb{R}^m$, usually with $m \ge n$, that is at least once continuously differentiable. In practice also its Jacobian $J(x) = \partial r / \partial x$ and a start $x_0$.

**Output.** A local minimizer $x^*$ of $F(x) = \tfrac12 \|r(x)\|^2$, or in practice a point where the gradient $g(x) = J(x)^{\mathsf T} r(x)$ is small. The global minimizer is wanted but is not guaranteed by any of the standard methods.

**Structure.** The gradient and the Hessian have a special form:
$$\nabla F = J^{\mathsf T} r, \qquad \nabla^2 F = J^{\mathsf T} J + \sum_{i=1}^m r_i \nabla^2 r_i.$$
The first term of the Hessian needs only first derivatives. The second term is small when the residuals are small or nearly linear. All the methods of this group use this fact.

**Optimality.** At a local minimizer, $J^{\mathsf T} r = 0$ (the residual is orthogonal to the columns of $J$) and $\nabla^2 F$ is positive semidefinite. If $J^{\mathsf T} r = 0$ and $\nabla^2 F$ is positive definite, the point is a strict local minimizer.

**Residual size.** A problem is a zero residual problem if $r(x^*) = 0$, a small residual problem if the second term of the Hessian is small compared with $J^{\mathsf T} J$ at $x^*$, and a large residual problem otherwise. The local rate of Gauss-Newton depends on this class.

## Variants

- **Weighted.** Minimize $\tfrac12 r^{\mathsf T} W r$ with a positive definite $W$, the inverse covariance of the measurements. With $W = C^{\mathsf T} C$, replace $r$ by $C r$ to get the plain form.
- **Robust.** Minimize $\sum_i \rho(r_i)$ with an [M-estimator](/m-estimator/) $\rho$ that grows slower than the square, such as the [Huber function](/huber-m-estimator/). This is solved by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).
- **Regularized.** Add a term $\tfrac12 \lambda \|x - x_p\|^2$ for a prior $x_p$, as in [Tikhonov regularization](/tikhonov-regularization/). This is again a least squares problem, with $n$ extra residuals.
- **On a manifold.** Some parameters are rotations or unit vectors. The step is computed in a local parametrization, for example the axis-angle update $R \leftarrow \exp([\omega]_\times) R$ for a rotation, and the result is mapped back.
- **Bound constrained.** Simple bounds on $x$, handled by projected or active set versions of the same methods.
- **Separable.** If some parameters enter linearly, they can be eliminated in closed form (variable projection), which leaves a smaller nonlinear problem.
- **Errors in variables.** When both the inputs and the outputs of the model are noisy, the residuals are orthogonal distances, and the unknown true inputs become extra parameters. Bundle adjustment and [optimal triangulation](/optimal-triangulation/) have this form.

## Examples

- **Exponential fit.** $r_i(x) = x_1 e^{x_2 t_i} - y_i$. With $y_i = 2 e^{-0.5 t_i}$ at $t = 0, 1, 2, 3$ the solution is $(2, -0.5)$ with zero residual; Gauss-Newton from $(1, 0)$ reaches it to 12 digits in 4 steps (see the Gauss-Newton page).
- **The Rosenbrock function.** $r(x) = (10(x_2 - x_1^2), 1 - x_1)$, a zero residual problem with a curved valley. The standard start is $(-1.2, 1)$, and the minimizer is $(1, 1)$.
- **A one-parameter problem with a nonzero residual.** $r(x) = (x + 1, \lambda x^2 + x - 1)$ has its minimizer at $0$ for $\lambda < 1$, with $F(0) = 1$. Gauss-Newton converges linearly for $|\lambda| < 1$ and does not converge for $\lambda < -1$ (Madsen, Nielsen and Tingleff 2004).
- **Point triangulation.** Find the 3D point that minimizes the [reprojection error](/reprojection-error/) in two or more images: $r_{i} = \pi(P_i X) - x_i$ with 3 parameters.
- **Homography refinement.** Minimize the transfer error of point matches over the 8 degrees of freedom of a [homography](/homography-estimation/), from a linear estimate.
- **Camera calibration.** Fit the intrinsics, the lens distortion and one pose per image to the observed corners of a target, as in [Zhang's method](/zhang-calibration-method/).
- **Bundle adjustment.** All cameras and all 3D points at once. Here $n$ can be in the millions, and the Jacobian is very sparse.

## Known algorithms

| method | step | per iteration | local rate | global safeguard |
|---|---|---|---|---|
| [Gauss-Newton](/gauss-newton-algorithm/) | solve $J^{\mathsf T} J h = -J^{\mathsf T} r$ | $\Theta(m n^2 + n^3)$ | quadratic for zero residual, else linear or none | none |
| Gauss-Newton with a line search | the same, then a [backtracking line search](/backtracking-line-search/) | the same plus extra evaluations | as Gauss-Newton | line search |
| [Levenberg-Marquardt](/levenberg-marquardt/) | solve $(J^{\mathsf T} J + \mu D) h = -J^{\mathsf T} r$ | $\Theta(m n^2 + n^3)$ per try | as Gauss-Newton when $\mu \to 0$ | damping |
| [Powell's dog leg](/powell-dogleg/) | dog leg path in a trust region | $\Theta(m n^2 + n^3)$ per accepted step | as Gauss-Newton near the solution | trust region |
| Newton's method | solve $\nabla^2 F\, h = -g$ | needs the second derivatives of all $r_i$ | quadratic | needs a line search or trust region |
| Structured [quasi-Newton](/quasi-newton-method/) | Gauss-Newton matrix plus an update for the second term | $\Theta(m n^2 + n^3)$ | superlinear, also for large residuals | line search |
| Inexact Newton | solve the Gauss-Newton system by [CG](/conjugate-gradient-method/) | a few products with $J$ and $J^{\mathsf T}$ | linear to superlinear, by the forcing term | trust region or damping |

The costs are for dense $J$ in the real RAM model; a dense factorization is counted as $\Theta(n^3)$. For bundle adjustment, the [reduced camera system](/reduced-camera-system/), [sparse bundle adjustment](/sparse-bundle-adjustment/) and [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/) use the sparsity to do much better.

## Bounds

**Global minimization is NP-hard (theorem).** Given integers $a_1, \dots, a_n$, take the $n + 1$ residuals $r_i(x) = x_i^2 - 1$ for $i \le n$ and $r_{n+1}(x) = \sum_i a_i x_i$. Then $\min F = 0$ exactly when there are signs $x_i = \pm 1$ with $\sum_i a_i x_i = 0$, which is the partition problem. So deciding whether the global minimum of a nonlinear least squares problem with quadratic residuals is zero is NP-hard, and no method of this group can promise the global minimizer in polynomial time unless P = NP. The standard methods are local methods.

**Statistical accuracy (theorem).** If $y_i = f_i(x_{\text{true}}) + \epsilon_i$ with independent $\epsilon_i \sim N(0, \sigma^2)$, then the minimizer is the maximum likelihood estimate. When $J$ has full column rank at the solution, its covariance is approximately $\sigma^2 (J^{\mathsf T} J)^{-1}$ to first order, which matches the [Cramer-Rao bound](/cramer-rao-bound/) for this model to first order. When $J$ is rank deficient, as with a [gauge freedom](/gauge-freedom/), some directions are not determined by the data at all.

**Local rate (theorem).** Near a minimizer where $J$ has full column rank, Gauss-Newton converges quadratically if the residual is zero, linearly with factor $\|(J^{\mathsf T} J)^{-1} \sum_i r_i \nabla^2 r_i\|$ if that norm is below 1, and may not converge otherwise (Dennis and Schnabel, chapter 10; Madsen, Nielsen and Tingleff, section 3.1).

## Reductions

- **Linear least squares** is the case where $r(x) = A x - b$; then $J = A$, the Hessian is $A^{\mathsf T} A$ exactly, and one Gauss-Newton step solves the problem. Each step of the nonlinear methods solves a linear least squares problem, by the [normal equations](/normal-equations/) or by [QR](/qr-decomposition/).
- **Systems of nonlinear equations.** A square or overdetermined system $r(x) = 0$ has a solution exactly when $\min F = 0$, so the [systems of nonlinear equations](/systems-of-nonlinear-equations/) problem reduces to nonlinear least squares. Powell's dog leg was first written for this case.
- **Maximum likelihood with Gaussian noise.** The negative log likelihood is $F$ plus a constant, so this estimation problem is nonlinear least squares.
- **Robust estimation** reduces to a sequence of weighted nonlinear least squares problems through iteratively reweighted least squares.
- **Bundle adjustment, calibration, triangulation and image alignment** are instances, with residuals given by the [reprojection error](/reprojection-error/) or by intensity differences.

## Applications

- Curve and surface fitting in science and engineering, the classic use since Gauss.
- Camera calibration, pose estimation, homography and fundamental matrix refinement, and triangulation in computer vision.
- Bundle adjustment in [structure from motion](/structure-from-motion-problem/) and photogrammetry, and pose graph optimization in SLAM.
- Image alignment, such as the [Lucas-Kanade method](/lucas-kanade-method/), where the residuals are intensity differences.
- Geodesy and surveying, where networks of distance and angle measurements are adjusted.
- System identification and kinetics, where model parameters are fitted to measured time series.

## References
