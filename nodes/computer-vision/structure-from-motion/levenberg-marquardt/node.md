---
tag: MSS87Z
kind: algorithm
slug: levenberg-marquardt
name: Levenberg-Marquardt algorithm
aliases:
- Levenberg-Marquardt
- damped least squares method
area: computer-vision/structure-from-motion
level: core
summary: Gauss-Newton with a damping term added to J^T J, raised when a step fails and lowered when it succeeds, moving between Gauss-Newton and gradient descent.
solves: [nonlinear-least-squares]
model: real-ram
complexity:
  vars: {m: "the number of residuals", n: "the number of parameters", k: "the number of steps tried, accepted or rejected"}
  time: {per_iteration: "Θ(m n^2 + n^3)"}
  space: {extra: "Θ(m n)"}
  evaluations: {per_iteration: "1"}
properties: {deterministic: true, iterative: true, local: true, recursive: false, monotone: true}
history:
  year: 1944
  people: [Kenneth Levenberg, Donald W. Marquardt, Jorge J. Moré]
  note: Levenberg proposed damped least squares in 1944. Marquardt (1963) rediscovered it, scaled the damping by the diagonal of J^T J and gave a rule to adapt it. Moré (1978) recast it as a trust region method and proved convergence.
prereqs: [gauss-newton-algorithm]
see_also: [powell-dogleg, nonlinear-least-squares, gradient-descent, tikhonov-regularization, sparse-bundle-adjustment, bundle-adjustment, damped-least-squares-inverse-kinematics, iteratively-reweighted-least-squares]
sources:
  - paper: doi:10.1090/qam/10666
    title: "Kenneth Levenberg, A method for the solution of certain non-linear problems in least squares, Quarterly of Applied Mathematics 2(2), 1944, 164-168"
    locator: "the whole note (the damped least squares step and its relation to the Taylor series method)"
  - paper: doi:10.1137/0111030
    title: "Donald W. Marquardt, An algorithm for least-squares estimation of nonlinear parameters, Journal of the Society for Industrial and Applied Mathematics 11(2), 1963, 431-441"
    locator: "the whole paper (the interpolation between the Gauss-Newton and the gradient step, the scaling by the diagonal of J^T J and the rule for the damping)"
  - paper: doi:10.1007/BFb0067700
    title: "Jorge J. Moré, The Levenberg-Marquardt algorithm, implementation and theory, in G. A. Watson (ed.), Numerical Analysis, Lecture Notes in Mathematics 630, Springer, 1978, 105-116"
    locator: "the whole paper (the trust region form, the computation of the damping from the radius and the convergence theorem)"
  - paper: "Kaj Madsen, Hans Bruun Nielsen and Ole Tingleff, Methods for Non-Linear Least Squares Problems, second edition, Informatics and Mathematical Modelling, Technical University of Denmark, 2004"
    locator: "Section 3.2, The Levenberg-Marquardt method (Algorithm 3.16, the start value of the damping, the update rule and the stopping rules)"
  - book: isbn:9780387303031
    title: "Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006"
    locator: "Chapter 10, Least-squares problems (Section 10.3, the Levenberg-Marquardt method as a trust region method, its implementation and its convergence)"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Appendix 6, Iterative estimation methods (the Levenberg-Marquardt iteration, its sparse form and its application to bundle adjustment)"
---

The Levenberg-Marquardt algorithm (LM) minimizes a sum of squares $F(x) = \tfrac12 \|r(x)\|^2$ of smooth residuals. Like the [Gauss-Newton algorithm](/gauss-newton-algorithm/), it linearizes the residuals at each step, but it solves the damped system $(J^{\mathsf T} J + \mu D) h = -J^{\mathsf T} r$ with a damping $\mu > 0$ and $D = I$ or $D = \operatorname{diag}(J^{\mathsf T} J)$. A step is accepted only if the cost goes down. After a failure $\mu$ grows, which makes the step shorter and turns it toward the steepest descent direction $-J^{\mathsf T} r$. After a success $\mu$ shrinks, so near a good solution the method becomes Gauss-Newton and inherits its fast local rate. The damping also makes the system solvable when $J$ is rank deficient. The [nonlinear least squares](/nonlinear-least-squares/) page states the problem. Plain Gauss-Newton has no safeguard, and [Powell's dog leg method](/powell-dogleg/) controls a trust region radius directly and, after a rejected step, reuses the Gauss-Newton step it already has, where LM must factor a new damped matrix. LM is the standard solver for small and medium nonlinear least squares problems in computer vision, such as camera calibration, homography and pose refinement, and, in its sparse form, [bundle adjustment](/bundle-adjustment/).

## In plain words

You want the best values of some unknown numbers, where "best" means the sum of the squared errors is smallest. The fast method (Gauss-Newton) jumps to where a straight line approximation says the best values are, but if you start far away, that jump can make things worse. Levenberg-Marquardt adds a brake. It tries a jump, and if the error goes down, it keeps the jump and loosens the brake a little. If the error goes up, it throws the jump away, tightens the brake and tries a shorter, more careful jump in the downhill direction. So it is careful when things go badly and fast when they go well.

## The problem

**Input.** A residual function $r: \mathbb{R}^n \to \mathbb{R}^m$, its Jacobian $J(x)$, a start $x_0$, a damping factor $\tau$ for the first $\mu$, tolerances $\varepsilon_1$ and $\varepsilon_2$, and an iteration limit $k_{\max}$.

**Output.** A point $x$ with $F(x) \le F(x_0)$ at which the gradient $g = J^{\mathsf T} r$ is small, or the last iterate when a limit is reached.

**Notation.** $A = J^{\mathsf T} J$, $g = J^{\mathsf T} r$, $L(h) = \tfrac12 \|r + J h\|^2$ is the linear model of the residuals, and $D$ is $I$ (Levenberg) or $\operatorname{diag}(A)$ (Marquardt).

## The algorithm

The version below is Algorithm 3.16 of Madsen, Nielsen and Tingleff (2004), with an option for the scaling $D$.

```pseudo id=main
LEVENBERG-MARQUARDT(r, J, x_0, τ, ε_1, ε_2, k_max)
L1  x <- x_0 ; ν <- 2
L2  A <- J(x)^T J(x) ; g <- J(x)^T r(x)
L3  μ <- τ · max_i A_ii
L4  for k <- 1 to k_max
L5      if ||g||_∞ <= ε_1 then return x
L6      solve (A + μ D) h = -g by Cholesky
L7      if ||h|| <= ε_2 (||x|| + ε_2) then return x
L8      ρ <- (F(x) - F(x + h)) / (½ h^T (μ D h - g))
L9      if ρ > 0 then
L10         x <- x + h ; A <- J(x)^T J(x) ; g <- J(x)^T r(x)
L11         μ <- μ · max(1/3, 1 - (2ρ - 1)^3) ; ν <- 2
L12     else μ <- μ ν ; ν <- 2 ν
L13 return x
```

Line L3 scales the first damping to the size of $A$; $\tau = 10^{-6}$ suits a start close to the answer and $\tau = 10^{-3}$ or $1$ a start that is not (a rule of thumb of Madsen, Nielsen and Tingleff). Line L6 computes the damped step, which minimizes $L(h) + \tfrac12 \mu h^{\mathsf T} D h$. Line L8 compares the actual decrease of $F$ with the decrease that the linear model predicts; the denominator is $L(0) - L(h)$, which is positive. Line L9 accepts any step that lowers $F$. Line L11 lowers $\mu$ by up to a factor 3 when the model is good ($\rho$ near 1) and raises it a little when $\rho$ is small. Line L12 raises $\mu$ after a failure by a factor that doubles with each failure in a row, so a run of failures quickly gives a short steepest descent step. Lines L5 and L7 are the stopping rules for a small gradient and a small step.

The two limits of line L6 explain the method. As $\mu \to 0$, $h$ tends to the Gauss-Newton step. As $\mu \to \infty$, $h \approx -D^{-1} g / \mu$, a short step along the scaled steepest descent direction.

## Example

The one-parameter example of Madsen, Nielsen and Tingleff is $r(x) = (x + 1, \lambda x^2 + x - 1)$. For $\lambda = -2$ the only minimizer is $x^* = 0$ with $F(0) = 1$, and plain Gauss-Newton does not converge to it (see the [Gauss-Newton](/gauss-newton-algorithm/) page). Run LM from $x_0 = 0.1$ with $\tau = 1$ and $D = I$. At $x_0$, $r = (1.1, -0.92)$, $J = (1, 0.6)^{\mathsf T}$, $A = 1.36$, $g = 0.548$ and $F = 1.0282$, so line L3 gives $\mu = 1.36$.

| try | $x$ | $\mu$ | $h$ | $F(x + h)$ | predicted | $\rho$ | result |
|---|---|---|---|---|---|---|---|
| 1 | $0.1$ | $1.3600$ | $-0.201471$ | $1.033190$ | $0.082804$ | $-0.0603$ | rejected, $\mu \leftarrow 2\mu$ |
| 2 | $0.1$ | $2.7200$ | $-0.134314$ | $1.003616$ | $0.061337$ | $0.4008$ | accepted |
| 3 | $-0.034314$ | $2.7412$ | $0.042361$ | $1.000193$ | $0.006977$ | $0.4906$ | accepted |
| 4 | $0.008047$ | $2.7413$ | $-0.010239$ | $1.000014$ | $0.000389$ | $0.4597$ | accepted |
| 5 | $-0.002192$ | $2.7427$ | $0.002769$ | $1.000001$ | $0.000029$ | $0.4672$ | accepted |

The first try is the step that Gauss-Newton would almost take, and it raises $F$. Doubling $\mu$ gives a shorter step that lowers $F$. After that, $\mu$ stays near $2.74$ and the error shrinks by a factor of about $-0.266$ per step: linear convergence, as expected with a nonzero residual. The run stops at $x \approx -7 \cdot 10^{-10}$ after 27 tries, 14 of them accepted. On the Rosenbrock residuals $r = (10(x_2 - x_1^2), 1 - x_1)$ from $(-1.2, 1)$, the reference code reaches $(1, 1)$ in 18 tries (15 accepted) with $\tau = 10^{-3}$ and in 25 tries (22 accepted) with $\tau = 1$. These counts are measurements on this example only.

## Correctness

For every $\mu > 0$ the matrix of line L6 is positive definite, so the step exists, also for a rank deficient $J$ (theorem). The predicted reduction of line L8 is $\tfrac12 h^{\mathsf T} (\mu D h - g) > 0$ whenever $g \ne 0$, so an accepted step lowers $F$ strictly and the costs of the accepted iterates decrease (theorem). At a point with $g \ne 0$, enough rejections make $\rho$ tend to 1, so a step is accepted after finitely many tries (theorem). The proof file below proves these three facts. They do not by themselves show convergence of the iterates. For a version that controls a trust region radius and derives $\mu$ from it, Moré (1978) proves that the gradients tend to zero along a subsequence, and convergence to a stationary point under further conditions (theorem, not proved here). Near a minimizer where $J$ has full column rank and $\mu \to 0$, the steps approach Gauss-Newton steps, so the method inherits the quadratic rate for zero residual problems (a standard result when $\mu_k = O(\|g_k\|)$; the update of line L11 is a heuristic that usually achieves it).

## Complexity

In the real RAM model, a try costs one evaluation of $r$, $\Theta(n^3)$ for the dense Cholesky factorization of line L6, and $\Theta(n)$ for the test of line L8. An accepted step also costs one evaluation of $J$ and $\Theta(m n^2)$ to form $A$ in line L10. So each try costs $\Theta(m n^2 + n^3)$ plus one evaluation, and the extra space is $\Theta(m n)$ for $J$ and $\Theta(n^2)$ for $A$. A rejected step costs a new factorization but no new Jacobian. The number of tries has no useful general bound; it depends on the problem and on $x_0$. In bundle adjustment the dense factorization is replaced by the [reduced camera system](/reduced-camera-system/), which brings the cost of a try down to that of [sparse bundle adjustment](/sparse-bundle-adjustment/).

## Properties

- **Monotone (theorem).** The accepted costs decrease strictly.
- **Defined for rank deficient $J$ (theorem).** For $\mu > 0$ and $D = I$ the damped matrix is positive definite for every $J$. This matters in bundle adjustment, where the [gauge freedom](/gauge-freedom/) makes $J^{\mathsf T} J$ singular.
- **A trust region method (theorem).** The step of line L6 minimizes $L$ over the ellipsoid $h^{\mathsf T} D h \le \|h\|_D^2$, so $\mu$ controls the radius indirectly.
- **Scale dependence.** With $D = I$ the step depends on the units of the parameters. With $D = \operatorname{diag}(A)$ it does not change when a parameter is rescaled.
- **Same weakness against outliers as Gauss-Newton.** The cost is a plain sum of squares.

## Variants and improvements

- **Marquardt scaling.** $D = \operatorname{diag}(A)$ makes the method invariant to a diagonal rescaling of the parameters. On the Rosenbrock example the reference code needs 35 tries with it, against 18 without, which shows that the scaling is not always better.
- **Nielsen's update.** Lines L11 and L12 are the update of Nielsen, used by Madsen, Nielsen and Tingleff. The older rule multiplies $\mu$ by a fixed factor, for example 10, after a failure and divides by it after a success.
- **Trust region form.** Moré (1978) controls a radius $\Delta$ and finds the $\mu$ for which $\|D h\| = \Delta$ by a scalar iteration. This is the form in MINPACK and the one with the convergence proof.
- **Geodesic acceleration.** A second order correction along the step, computed from a directional second derivative of $r$, helps on problems with long curved valleys.
- **Sparse LM.** For bundle adjustment, the damped normal equations have the same block structure as the undamped ones, and the points can be eliminated by the Schur complement. See [sparse bundle adjustment](/sparse-bundle-adjustment/), and [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/) for the iterative solve.
- **Robust costs.** With an [M-estimator](/m-estimator/) the residuals and the Jacobian are reweighted at each step, as in [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).

## When to use it

Use LM for small and medium nonlinear least squares problems when the start may be poor or some directions are poorly determined, which is the usual case in calibration, pose estimation, homography refinement and small bundle adjustments. It is a safe default: it never raises the cost, and near a good solution it is as fast as Gauss-Newton. For problems where one factorization is expensive and many steps are rejected, the dog leg method can be cheaper, since it can shrink the radius without a new factorization (Lourakis and Argyros 2005 report this for bundle adjustment). For very large problems, solve the damped system iteratively.

## Pitfalls

- **Wrong predicted reduction.** Line L8 must divide by $L(0) - L(h)$, not by $F(x)$ or by $\|g\|$. With the wrong value, $\rho$ has the wrong scale and line L11 adapts $\mu$ badly.
- **$\mu$ that only grows.** If line L11 is left out, $\mu$ never falls and the method becomes slow gradient descent. Check that $\mu$ decreases near the solution.
- **Rounding near convergence.** Close to the minimum, $F(x) - F(x + h)$ is a difference of nearly equal numbers and $\rho$ is noisy. Rely on the stopping rules of lines L5 and L7.
- **Scaling.** With $D = I$, parameters in very different units, such as a focal length in pixels and a rotation in radians, get the same damping. Normalize the parameters or use the Marquardt scaling.
- **Rank deficiency hidden by damping.** With $D = I$ a gauge freedom no longer breaks line L6, but the iterates can drift along the gauge directions. Fix the gauge when you need a unique answer.

## Implementations

## History

Kenneth Levenberg published damped least squares in 1944: add a multiple of the identity, or of a diagonal matrix, to the normal equations so that the step stays in the region where the linear approximation holds. Donald Marquardt, at DuPont, published the same idea in 1963, with a geometric argument that the damped step interpolates between the Gauss-Newton step and the gradient step, the scaling by the diagonal of $J^{\mathsf T} J$, and a simple rule for $\mu$. His paper made the method widely used. Jorge Moré (1978) described it as a trust region method, gave a robust implementation, which became part of MINPACK, and proved its convergence. In computer vision, Hartley and Zisserman made LM the standard refinement step, and Lourakis and Argyros built their sparse bundle adjustment package on it.

## References
