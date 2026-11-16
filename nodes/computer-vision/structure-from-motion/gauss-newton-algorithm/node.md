---
tag: 77QE67
kind: algorithm
slug: gauss-newton-algorithm
name: Gauss-Newton algorithm
aliases:
- Gauss-Newton method
area: computer-vision/structure-from-motion
level: core
summary: Minimize a sum of squares by linearizing the residuals at each step and solving the normal equations J^T J dx = -J^T r for the update.
solves: [nonlinear-least-squares]
model: real-ram
complexity:
  vars: {m: "the number of residuals", n: "the number of parameters, with m >= n", k: "the number of iterations"}
  time: {per_iteration: "Θ(m n^2 + n^3)"}
  space: {extra: "Θ(m n)"}
  evaluations: {per_iteration: "1"}
properties: {deterministic: true, iterative: true, local: true, recursive: false, globally_convergent: false}
history:
  year: 1809
  people: [Carl Friedrich Gauss]
  note: Gauss used least squares with linearized equations to fit planetary orbits and published the method in 1809. The name joins him with Newton, whose method the iteration approximates. Modern analyses of the local rate are in Dennis and Schnabel (1983) and Nocedal and Wright (1999).
prereqs: [nonlinear-least-squares, normal-equations, cholesky-decomposition]
see_also: [levenberg-marquardt, powell-dogleg, newton-method-for-systems, gradient-descent, quasi-newton-method, quadratic-convergence, iteratively-reweighted-least-squares, bundle-adjustment]
sources:
  - book: isbn:9780387303031
    title: "Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006"
    locator: "Chapter 10, Least-squares problems (the Gauss-Newton method and Theorem 10.1, its global convergence with a Wolfe line search when the singular values of J are bounded away from zero)"
  - book: isbn:9780898713640
    title: "J. E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996"
    locator: "Chapter 10, Nonlinear least squares (Theorem 10.2.1, the local convergence of Gauss-Newton and the role of the second derivative term)"
  - paper: "Kaj Madsen, Hans Bruun Nielsen and Ole Tingleff, Methods for Non-Linear Least Squares Problems, second edition, Informatics and Mathematical Modelling, Technical University of Denmark, 2004"
    locator: "Section 3.1, The Gauss-Newton method (Example 3.3, the residual (x + 1, λx^2 + x - 1), on which the method converges linearly or fails)"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Appendix 6, Iterative estimation methods (Newton iteration and the Gauss-Newton method, and their use for bundle adjustment)"
---

The Gauss-Newton algorithm minimizes a sum of squares $F(x) = \tfrac12 \sum_i r_i(x)^2$ of smooth residuals $r_i$ of a parameter vector $x$. At each step it replaces each residual by its linear approximation $r + J h$, where $J$ is the Jacobian, and moves to the minimizer of that linear least squares model: it solves the [normal equations](/normal-equations/) $J^{\mathsf T} J\, h = -J^{\mathsf T} r$ and sets $x \leftarrow x + h$. It is [Newton's method](/newton-method-for-systems/) on $\nabla F = 0$ with the second derivative term of the Hessian dropped, so it needs only first derivatives. Near a solution where the residuals are zero and $J$ has full column rank it converges quadratically. With nonzero residuals the rate is linear at best, and the method can fail to converge even from a start close to the minimizer. The [nonlinear least squares](/nonlinear-least-squares/) page states the problem. [Levenberg-Marquardt](/levenberg-marquardt/) adds a damping term so that every accepted step lowers the cost, and [Powell's dog leg method](/powell-dogleg/) mixes the Gauss-Newton step with the steepest descent step inside a trust region. Both of those methods reduce to Gauss-Newton near a good solution. In computer vision, Gauss-Newton is the step inside [bundle adjustment](/bundle-adjustment/), camera calibration and image alignment.

## In plain words

You have a model with a few unknown numbers, and many measurements. Each measurement gives an error, and you want to make the sum of the squared errors as small as you can. The errors depend on the unknowns in a curved way, so you cannot solve for the best numbers in one go. Gauss-Newton guesses, then pretends that near the guess every error changes in a straight line. For straight lines, the best change of the numbers is easy to compute. You apply that change and repeat. If the model can fit the data almost exactly, each round roughly doubles the number of correct digits. If the fit stays poor, the rounds can help slowly or not at all.

## The problem

**Input.** A residual function $r: \mathbb{R}^n \to \mathbb{R}^m$ with $m \ge n$, its Jacobian $J(x) = \partial r / \partial x$ (an $m \times n$ matrix), a start $x_0$, a tolerance $\varepsilon$ and an iteration limit $k_{\max}$.

**Output.** A point $x$ that is close to a stationary point of $F(x) = \tfrac12 \|r(x)\|^2$, that is, $g(x) = J(x)^{\mathsf T} r(x) \approx 0$. The method finds a local minimizer only when it converges. It does not find the global one in general.

**Notation.** $A = J^{\mathsf T} J$ and $g = J^{\mathsf T} r$. The Hessian of $F$ is $\nabla^2 F = A + S$ with $S = \sum_i r_i \nabla^2 r_i$. Gauss-Newton uses $A$ in place of $\nabla^2 F$.

## The algorithm

```pseudo id=main
GAUSS-NEWTON(r, J, x_0, ε, k_max)
L1  x <- x_0
L2  for k <- 1 to k_max
L3      r <- r(x) ; J <- J(x)
L4      A <- J^T J ; g <- J^T r
L5      if ||g||_∞ <= ε then return x
L6      solve A h = -g by Cholesky
L7      x <- x + h
L8      if ||h|| <= ε (||x|| + ε) then return x
L9  return x
```

Line L3 evaluates the residual and the Jacobian at the current point. Line L4 forms the normal equations of the linear model $L(h) = \tfrac12 \|r + J h\|^2$, whose gradient is $g + A h$. Line L5 stops at a point where the gradient of $F$ is small. Line L6 finds the minimizer of $L$ by a [Cholesky factorization](/cholesky-decomposition/) of $A$; it fails when $J$ is rank deficient, and then the method is not defined. Line L7 takes the full step, with no line search and no damping. Line L8 stops when the step is small relative to $x$. A numerically safer form of line L6 solves the linear least squares problem $\min \|r + J h\|$ by a [QR decomposition](/qr-decomposition/) of $J$, which does not square the condition number.

## Example

Fit $y = x_1 e^{x_2 t}$ to the four exact values $y = 2 e^{-0.5 t}$ at $t = 0, 1, 2, 3$, so the residuals are $r_i = x_1 e^{x_2 t_i} - y_i$ and the solution is $x^* = (2, -0.5)$ with $F(x^*) = 0$. Start at $x_0 = (1, 0)$. Then $r = (-1, -0.213061, 0.264241, 0.553740)$, $J$ has rows $(1, t_i)$, $A = \begin{pmatrix} 4 & 6 \\ 6 & 14 \end{pmatrix}$ and $g = (-0.395080, 1.976641)$. Line L6 gives $h = (0.869548, -0.513852)$.

| $k$ | $x_k$ | $F(x_k)$ | $\|x_k - x^*\|$ |
|---|---|---|---|
| 0 | $(1, 0)$ | $7.109 \cdot 10^{-1}$ | $1.118$ |
| 1 | $(1.869548, -0.513852)$ | $1.629 \cdot 10^{-2}$ | $1.312 \cdot 10^{-1}$ |
| 2 | $(1.999955, -0.498807)$ | $3.787 \cdot 10^{-6}$ | $1.193 \cdot 10^{-3}$ |
| 3 | $(2.000000, -0.499998)$ | $5.671 \cdot 10^{-12}$ | $1.575 \cdot 10^{-6}$ |
| 4 | $(2.000000, -0.500000)$ | $1.293 \cdot 10^{-23}$ | $2.403 \cdot 10^{-12}$ |

The error is roughly squared at each step, as the theorem for zero residuals says. A nonzero residual changes this. Madsen, Nielsen and Tingleff use $r(x) = (x + 1, \lambda x^2 + x - 1)$ with one parameter. Its minimizer is $x^* = 0$ for every $\lambda < 1$, with $F(0) = 1$, and near it the Gauss-Newton error obeys $e_{k+1} = \lambda e_k + O(e_k^2)$. From $x_0 = 0.1$:

| $\lambda$ | $x_0, x_1, x_2, \dots$ | behavior |
|---|---|---|
| $0.5$ | $0.1, 0.047738, 0.023326, 0.011530, 0.005732, 0.002858$ | linear, the ratio tends to $0.5$ |
| $-2$ | $0.1, -0.302941, 0.136764, -0.467990, 0.066387, -0.176704, 0.153385$ | no convergence |

For $\lambda = -2$, $0$ is the only stationary point and the global minimizer of $F$, yet the iteration jumps around it. Levenberg-Marquardt and the dog leg method converge on the same problem.

## Correctness

Line L6 returns the exact minimizer of the linear model when $J$ has full column rank, and that step is a descent direction for $F$. The local behavior follows from the error recursion $e_{k+1} = -A_*^{-1} S_* e_k + O(\|e_k\|^2)$ at a stationary point $x^*$ with $J(x^*)$ of full column rank and smooth residuals. If $S_* = 0$, which holds when $r(x^*) = 0$, the convergence is quadratic (theorem). If $\|A_*^{-1} S_*\| < 1$ it is linear (theorem). If $|A_*^{-1} S_*| > 1$ in one dimension, the iterates leave every small neighborhood of $x^*$ (theorem, shown on the example above). The proof is in the proof file below. A global result needs a globalization: with a line search that satisfies the [Wolfe conditions](/wolfe-conditions/) and singular values of $J$ bounded away from zero, $J_k^{\mathsf T} r_k \to 0$ (Nocedal and Wright, Theorem 10.1).

## Complexity

In the real RAM model, one iteration costs one evaluation of $r$ and $J$, $\Theta(m n^2)$ to form $A$, $\Theta(m n)$ to form $g$, and $\Theta(n^3)$ for the dense Cholesky factorization. So the cost per iteration is $\Theta(m n^2 + n^3)$ plus the evaluation, and the extra space is $\Theta(m n)$ for $J$. The number of iterations is not bounded in general, since the method can diverge. With zero residual and a start inside the region of quadratic convergence, $O(\log \log (1/\varepsilon))$ iterations reach accuracy $\varepsilon$. When $J$ is sparse, as in bundle adjustment, $A$ is sparse too and a sparse factorization replaces the dense one; see the [reduced camera system](/reduced-camera-system/).

## Properties

- **Only first derivatives.** The method needs $r$ and $J$, not the second derivatives of $r$. The cost is that $A$ only approximates the Hessian.
- **Descent direction (theorem).** If $J$ has full column rank and $g \ne 0$, then $g^{\mathsf T} h = -\|J h\|^2 < 0$. A full step can still increase $F$.
- **Local rate (theorem).** Quadratic for zero residual problems, linear for small residual problems, possibly divergent for large residual problems.
- **Invariance (theorem).** The iterates do not change under an invertible linear change of the parameters $x = B y$, because $h$ is the minimizer of a model that does not depend on the coordinates. Gradient descent does not have this property.
- **Not robust.** Each residual enters squared, so one gross outlier can move the solution far. Use an [M-estimator](/m-estimator/) through [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).

## Variants and improvements

- **Damped Gauss-Newton.** Take $x \leftarrow x + \alpha h$ with $\alpha$ from a line search, for example a [backtracking line search](/backtracking-line-search/) with the [Armijo condition](/armijo-condition/). This gives global convergence to a stationary point under the full rank condition.
- **[Levenberg-Marquardt](/levenberg-marquardt/).** Solve $(A + \mu I) h = -g$ and adapt $\mu$. This handles rank deficient $J$ and keeps the cost decreasing.
- **[Powell's dog leg method](/powell-dogleg/).** Combine the Gauss-Newton step and the steepest descent step inside a trust region.
- **Large residual problems.** Add an approximation of $S$, for example by a [quasi-Newton](/quasi-newton-method/) update of $S$ only (Dennis and Schnabel, chapter 10), or switch to full Newton.
- **Inexact steps.** For very large $n$, solve line L6 approximately by the [conjugate gradient method](/conjugate-gradient-method/). This is the base of [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/).
- **Use in bundle adjustment.** The Jacobian of the [reprojection error](/reprojection-error/) has one block per observation, and the Gauss-Newton matrix $A$ has an arrow structure. Eliminating the points gives the [reduced camera system](/reduced-camera-system/), and [sparse bundle adjustment](/sparse-bundle-adjustment/) wraps it in Levenberg-Marquardt.

## When to use it

Use plain Gauss-Newton when the model fits the data well (small residuals), when $J$ has full rank, and when you start close to the answer, for example when refining a pose or a homography from a good linear estimate. Each step is then cheap and the convergence is fast. When the start may be far, when some directions are poorly determined, or when residuals at the solution are large, use Levenberg-Marquardt or the dog leg method, which keep the cost decreasing. When the residuals are not small and second derivatives are available, Newton's method with a line search can be better.

## Pitfalls

- **Divergence.** Line L7 takes the full step even when it increases $F$. Monitor $F$ and add a line search or switch to Levenberg-Marquardt if it rises.
- **Rank deficient $J$.** Line L6 fails when $J$ does not have full column rank, which happens in bundle adjustment because of the [gauge freedom](/gauge-freedom/). Fix the gauge or add damping.
- **Squaring the condition number.** Forming $A = J^{\mathsf T} J$ in line L4 squares the condition number of $J$. For ill conditioned problems solve the linear least squares problem by QR.
- **Wrong Jacobian.** A Jacobian with a sign or scale error still gives a direction, but the fast rate is lost and line L5 may never be met. Check $J$ against finite differences.
- **Stopping too early.** Line L8 can stop at a point that is not stationary if the steps become small for another reason, such as a very ill conditioned $A$. Check $\|g\|$ at the end.

## Implementations

## History

Gauss used least squares with linearized orbit equations to find the orbits of planets and published the least squares method in his Theoria motus of 1809. The iteration takes its name from him and from Newton's method, of which it is the version without second derivatives. It was used in geodesy and photogrammetry long before the theory of its convergence was written down. Levenberg (1944) and Marquardt (1963) added damping to fix its failures far from the solution. The local analysis with the second derivative term, and the difference between small and large residual problems, is in Dennis and Schnabel (1983) and in Nocedal and Wright (1999). Madsen, Nielsen and Tingleff (2004) give the one-parameter example on which the method fails.

## References
