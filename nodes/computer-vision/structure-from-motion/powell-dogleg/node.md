---
tag: GQ5JQ6
kind: algorithm
slug: powell-dogleg
name: Powell's dog leg method
aliases:
- dog leg trust region
area: computer-vision/structure-from-motion
level: advanced
summary: A trust region method for least squares whose step follows the path from the steepest descent point to the Gauss-Newton point, cut at the region boundary.
solves: [nonlinear-least-squares]
model: real-ram
complexity:
  vars: {m: "the number of residuals", n: "the number of parameters", k: "the number of steps tried, accepted or rejected"}
  time: {per_iteration: "Θ(m n^2 + n^3)"}
  space: {extra: "Θ(m n)"}
  evaluations: {per_iteration: "1"}
properties: {deterministic: true, iterative: true, local: true, recursive: false, monotone: true}
history:
  year: 1970
  people: [M. J. D. Powell]
  note: Powell introduced the hybrid step for nonlinear equations in 1970. Madsen, Nielsen and Tingleff gave the least squares form used here, and Lourakis and Argyros (2005) showed that a sparse dog leg can beat Levenberg-Marquardt in bundle adjustment.
prereqs: [gauss-newton-algorithm, gradient-descent]
see_also: [levenberg-marquardt, nonlinear-least-squares, sparse-bundle-adjustment, bundle-adjustment, newton-method-for-systems, backtracking-line-search, conjugate-gradient-method, cholesky-decomposition]
sources:
  - paper: "M. J. D. Powell, A hybrid method for nonlinear equations, in P. Rabinowitz (ed.), Numerical Methods for Nonlinear Algebraic Equations, Gordon and Breach, London, 1970"
    locator: "the whole chapter (the step that combines the steepest descent and the Newton step inside a region of fixed radius)"
  - paper: "Kaj Madsen, Hans Bruun Nielsen and Ole Tingleff, Methods for Non-Linear Least Squares Problems, second edition, Informatics and Mathematical Modelling, Technical University of Denmark, 2004"
    locator: "Section 3.3, Powell's dog leg method (the formula (3.20b) for the step on the second leg and Algorithm 3.21 with its radius update)"
  - book: isbn:9780387303031
    title: "Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006"
    locator: "Chapter 4, Trust-region methods (Section 4.1, the Cauchy point and the dogleg method; Lemma 4.3, the Cauchy decrease; Section 4.2, Theorems 4.5 and 4.6 on global convergence)"
  - paper: doi:10.1109/ICCV.2005.128
    title: "Manolis I. A. Lourakis and Antonis A. Argyros, Is Levenberg-Marquardt the most efficient optimization algorithm for implementing bundle adjustment?, Tenth IEEE International Conference on Computer Vision (ICCV 2005), vol. 2, 1526-1531"
    locator: "the whole paper (a sparse dog leg for bundle adjustment and its comparison with sparse Levenberg-Marquardt)"
---

Powell's dog leg method minimizes a sum of squares $F(x) = \tfrac12 \|r(x)\|^2$ by a trust region strategy. At each step it trusts the linear model $L(h) = \tfrac12 \|r + J h\|^2$ only inside a ball of radius $\Delta$. It computes two steps: the Gauss-Newton step $b$, which minimizes the model, and the steepest descent step $a$, which minimizes it along the negative gradient. If $b$ fits in the ball it takes $b$. If even $a$ does not fit, it takes the steepest descent direction cut at the boundary. Otherwise it follows the bent path from $0$ to $a$ to $b$, the "dog leg", and stops where the path leaves the ball. The radius grows after good steps and shrinks after bad ones, and a step is kept only if it lowers $F$. The [nonlinear least squares](/nonlinear-least-squares/) page states the problem. Compared with the close methods: [Gauss-Newton](/gauss-newton-algorithm/) always takes $b$, with no safeguard. [Levenberg-Marquardt](/levenberg-marquardt/) also moves between the two steps, but through a damping parameter, and it must solve a new linear system after each rejected step. The dog leg method keeps $a$ and $b$ when a step is rejected and only shrinks the radius, so a rejection costs no new factorization. This is why Lourakis and Argyros proposed it for [bundle adjustment](/bundle-adjustment/).

## In plain words

You are walking downhill in fog and can only trust your map for a short distance around you. The map shows two useful targets: the very bottom of the valley as the map draws it, and the best point if you walk straight downhill. If the bottom is within your trusted distance, you go there. If even the straight-downhill point is too far, you walk straight downhill until you reach the edge of the trusted area. Otherwise you walk to the downhill point and then turn toward the bottom, and stop at the edge. After the step you compare the real height with the map. If they agree well, you trust the map farther next time; if they disagree, you trust it less. The bent path looks like a dog's hind leg, which is where the name comes from.

## The problem

**Input.** A residual function $r: \mathbb{R}^n \to \mathbb{R}^m$, its Jacobian $J(x)$, a start $x_0$, a start radius $\Delta_0 > 0$, tolerances $\varepsilon_1$ and $\varepsilon_2$, and an iteration limit $k_{\max}$. The method as written needs $J$ of full column rank at every iterate.

**Output.** A point $x$ with $F(x) \le F(x_0)$ at which $g = J^{\mathsf T} r$ is small, or the last iterate when a limit is reached.

## The algorithm

The version below is Algorithm 3.21 of Madsen, Nielsen and Tingleff (2004).

```pseudo id=main
DOG-LEG(r, J, x_0, Δ_0, ε_1, ε_2, k_max)
L1  x <- x_0 ; Δ <- Δ_0 ; r <- r(x) ; J <- J(x)
L2  for k <- 1 to k_max
L3      g <- J^T r
L4      if ||g||_∞ <= ε_1 then return x
L5      α <- ||g||^2 / ||J g||^2
L6      a <- -α g ; solve (J^T J) b = -g
L7      if ||b|| <= Δ then h <- b
L8      else if ||a|| >= Δ then h <- -(Δ / ||g||) g
L9      else h <- a + β (b - a), with β in (0, 1) such that ||h|| = Δ
L10     if ||h|| <= ε_2 (||x|| + ε_2) then return x
L11     ρ <- (F(x) - F(x + h)) / (L(0) - L(h))
L12     if ρ > 0 then x <- x + h ; r <- r(x) ; J <- J(x)
L13     if ρ > 0.75 then Δ <- max(Δ, 3 ||h||)
L14     else if ρ < 0.25 then Δ <- Δ / 2
L15 return x
```

Line L5 is the exact minimizer of the model along $-g$, so $a$ in line L6 is the steepest descent point of the model; $b$ is the Gauss-Newton step. Lines L7 to L9 choose the step: $b$ inside the region, the cut steepest descent step if $a$ is outside, and otherwise the point where the segment from $a$ to $b$ crosses the boundary. Line L9 solves a scalar quadratic for $\beta$; there is exactly one root in $(0, 1)$. Line L11 compares the actual decrease with the decrease of the model, $L(0) - L(h) = -g^{\mathsf T} h - \tfrac12 \|J h\|^2$. Line L12 keeps the step if $F$ went down. Lines L13 and L14 update the radius. When a step is rejected, $x$, $a$ and $b$ do not change, so the next try needs only a new cut of the same path; the reference code recomputes them for simplicity.

## Example

Take the Rosenbrock residuals $r(x) = (10 (x_2 - x_1^2), 1 - x_1)$ at $x_0 = (-1.2, 1)$. Then $r = (-4.4, 2.2)$, $J = \begin{pmatrix} 24 & 10 \\ -1 & 0 \end{pmatrix}$, $g = (-107.8, -44)$ and $F = 12.1$. Line L5 gives $\alpha = 0.0014775$, so $a = (0.15927, 0.06501)$ with $\|a\| = 0.17203$, and $b = (2.2, -4.84)$ with $\|b\| = 5.31654$. The step for four radii:

| $\Delta$ | line | $h$ | $L(h)$ | $F(x_0 + h)$ | $\rho$ | next $\Delta$ |
|---|---|---|---|---|---|---|
| $0.1$ | L8 | $(0.0926, 0.0378)$ | $3.8407$ | $3.9987$ | $0.981$, accepted | $0.3$ |
| $1$ | L9 | $(0.5372, -0.8434)$ | $1.3842$ | $5.3783$ | $0.627$, accepted | $1$ |
| $5$ | L9 | $(2.0783, -4.5476)$ | $0.0074$ | $932.72$ | $-76.1$, rejected | $2.5$ |
| $6$ | L7 | $(2.2, -4.84)$ | $0$ | $1171.28$ | $-95.8$, rejected | $3$ |

The Gauss-Newton step zeroes the model but raises $F$ almost a hundredfold: the linear model is good only near $x_0$. The radius keeps the step where the model holds. From $\Delta_0 = 1$ the reference code reaches $(1, 1)$ to machine precision after 21 tries, 12 of them accepted. On the one-parameter example $r(x) = (x + 1, -2x^2 + x - 1)$, where plain Gauss-Newton does not converge, it converges to $0$, slowly: about 90 tries to reach $1.5 \cdot 10^{-9}$, since the radius keeps cutting the Gauss-Newton step that overshoots. These counts are measurements on these examples only.

## Correctness

The step of lines L7 to L9 lies in the region, and on its boundary unless it is the Gauss-Newton step (theorem). Along the dog leg path the model decreases and the distance from $x$ increases (theorem), so the step is at least as good for the model as the Cauchy point, the best point along $-g$ inside the region. This gives the Cauchy decrease $L(0) - L(h) \ge \tfrac12 \|g\| \min(\Delta, \|g\| / \|J^{\mathsf T} J\|)$ (theorem), so the model decrease is positive and every accepted step lowers $F$ (theorem). The proof file below proves these facts. From the Cauchy decrease, the general trust region theory gives $\liminf \|g_k\| = 0$ when $F$ is bounded below and has a Lipschitz gradient, for a radius rule with an upper bound (Nocedal and Wright, Theorem 4.5; theorem, not proved here). The rule of lines L13 and L14 has no upper bound; add one if you need the theorem. Near a minimizer with zero residual and full rank $J$, the radius stops binding and the method takes Gauss-Newton steps, with their quadratic rate.

## Complexity

In the real RAM model, one try costs one evaluation of $r$, $\Theta(m n)$ for $g$ and $J g$, $\Theta(m n^2)$ to form $J^{\mathsf T} J$ and $\Theta(n^3)$ for its dense Cholesky factorization, so $\Theta(m n^2 + n^3)$ plus the evaluation. An implementation that caches $a$ and $b$ pays the $\Theta(m n^2 + n^3)$ part only once per accepted step; a rejected try then costs $\Theta(m + n)$ plus one evaluation of $r$. The extra space is $\Theta(m n)$. The number of tries has no useful general bound. In bundle adjustment, the Gauss-Newton step is computed with the [reduced camera system](/reduced-camera-system/), and the caching matters because that solve is the most expensive part of a step.

## Properties

- **Monotone (theorem).** Accepted costs decrease strictly.
- **Cheap rejections.** After a rejected step only the radius changes, and the same $a$ and $b$ give the next step. In Levenberg-Marquardt a rejection needs a new factorization.
- **Needs full rank.** The Gauss-Newton step of line L6 needs $J$ of full column rank. With a [gauge freedom](/gauge-freedom/), fix the gauge or add a tiny damping.
- **Scale dependence.** The region is a ball, so the step depends on the units of the parameters. A scaled norm $\|D h\| \le \Delta$ removes this.
- **Steps on a piecewise linear path.** The dog leg only approximates the exact trust region step, which lies on a curved path; the approximation is good when $J^{\mathsf T} J$ is well conditioned.

## Variants and improvements

- **Double dog leg.** Dennis and Mei move the turning point from $a$ toward $b$, so the path bends less and the steps are closer to the Gauss-Newton step.
- **Exact trust region step.** Solve $\min L(h)$ subject to $\|h\| \le \Delta$ exactly by finding the $\mu$ for which the Levenberg-Marquardt step has length $\Delta$ (Moré 1978). This is more accurate per step and more expensive.
- **Two-dimensional subspace minimization.** Minimize the model exactly over the span of $g$ and $b$ inside the region.
- **Steihaug's truncated CG.** For large problems, run the [conjugate gradient method](/conjugate-gradient-method/) on the normal equations from $0$ and stop at the boundary. The first CG iterate is the Cauchy point, so the Cauchy decrease still holds.
- **Sparse dog leg for bundle adjustment.** Lourakis and Argyros (2005) compute $b$ with the sparse block structure and report that, on their tests, the dog leg method was faster than sparse Levenberg-Marquardt for the same accuracy (a benchmark result).

## When to use it

Use the dog leg method when one solve of the Gauss-Newton system is expensive compared with an evaluation of the residuals, so that cheap rejections pay off, as in bundle adjustment. Use it also when you want an explicit trust radius, for example to limit the step in a robot or a tracker. When $J$ can be rank deficient, Levenberg-Marquardt is simpler, since its damping makes every system solvable. When the start is good and the residuals are small, plain Gauss-Newton is enough.

## Pitfalls

- **A wrong model decrease.** Line L11 must use $L(0) - L(h)$ for the step actually taken. Using the decrease of the Gauss-Newton step for a cut step gives a wrong $\rho$.
- **Rounding in line L9.** The textbook root $(-c + \sqrt{c^2 + \|d\|^2 \rho_0}) / \|d\|^2$ cancels badly when $c > 0$; use the second form. The reference code does both cases.
- **Zero model decrease near convergence.** Near the solution, $L(0) - L(h)$ can round to $0$, and line L11 divides by zero. The reference code stops when it is not positive.
- **Rank deficient $J$.** Line L6 fails without a gauge fix. Do not silently replace $b$ by a pseudoinverse step without checking the length.
- **A start radius far off.** A $\Delta_0$ that is much too small wastes many accepted but tiny steps, because line L13 at most triples the radius per step. Scale $\Delta_0$ to the size of $x_0$.

## Implementations

## History

M. J. D. Powell introduced the hybrid step in 1970 for systems of nonlinear equations: inside a region of trusted radius, combine the steepest descent step and the Newton step, and change the radius by comparing actual and predicted reductions. This is one of the first trust region methods. The same idea applies to least squares with the Gauss-Newton step in place of the Newton step, as in the lecture notes of Madsen, Nielsen and Tingleff (2004), who remark that the name comes from golf, a game Powell played. Dennis and Mei proposed the double dog leg. In computer vision, Lourakis and Argyros (2005) asked whether Levenberg-Marquardt was the most efficient method for bundle adjustment and showed that a sparse dog leg method was faster on their tests.

## References
