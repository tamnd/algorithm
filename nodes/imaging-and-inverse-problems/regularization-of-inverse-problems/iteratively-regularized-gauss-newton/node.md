---
tag: KK6851
kind: algorithm
slug: iteratively-regularized-gauss-newton
name: Iteratively regularized Gauss-Newton method
aliases:
- IRGNM
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: Solve a nonlinear ill-posed equation by Gauss-Newton steps, each one regularized toward an initial guess with a weight that decreases geometrically.
solves: [nonlinear-least-squares]
model: real-ram
complexity:
  vars: {m: "the number of data values", n: "the number of unknowns", k: "the number of Gauss-Newton steps", f: "the cost of one evaluation of F", j: "the cost of one evaluation of the Jacobian"}
  time: {per_iteration: "O(f + j + m n^2 + n^3)", total: "O(k (f + j + m n^2 + n^3))"}
  space: {extra: "O(m n + n^2)"}
properties: {deterministic: true, iterative: true, matrix_free: false, linear_in_data: false, inner_solver: "dense Gaussian elimination", stopping_rule: "discrepancy principle"}
history:
  year: 1992
  people: [A. B. Bakushinskii]
  note: Bakushinskii proposed the method for nonlinear ill-posed problems and proved its convergence under a source condition with an a priori stopping rule.
prereqs: [gauss-newton-algorithm, tikhonov-regularization, morozov-discrepancy-principle]
see_also: [levenberg-marquardt, landweber-iteration, source-condition, tikhonov-convergence-rates, semi-convergence, full-waveform-inversion, adjoint-state-method, calderon-problem]
sources:
  - paper: "A. B. Bakushinskii, The problem of the convergence of the iteratively regularized Gauss-Newton method, Computational Mathematics and Mathematical Physics 32(9), 1992, 1353 to 1359"
    locator: the method and its convergence with an a priori stopping rule (general locator)
  - paper: "B. Blaschke, A. Neubauer and O. Scherzer, On convergence rates for the iteratively regularized Gauss-Newton method, IMA Journal of Numerical Analysis 17(3), 1997, 421 to 436"
    locator: convergence and rates with the discrepancy principle under conditions on the nonlinearity (general locator)
  - book: "B. Kaltenbacher, A. Neubauer and O. Scherzer, Iterative Regularization Methods for Nonlinear Ill-Posed Problems, de Gruyter, Berlin, 2008"
    locator: Chapter 4, Newton type methods (the IRGNM, its convergence and rates) (general locator)
---

The iteratively regularized Gauss-Newton method (IRGNM) solves a nonlinear ill-posed equation $F(x) = y$ from noisy data $y^\delta$ with $\|y^\delta - y\| \le \delta$. At the current iterate $x_k$ it replaces $F$ by its linearization and solves a [Tikhonov](/tikhonov-regularization/) problem for the update. The penalty pulls toward the initial guess $x_0$, not toward $x_k$:
$$x_{k+1} = x_k + \big(F'(x_k)^* F'(x_k) + \alpha_k I\big)^{-1} \big[F'(x_k)^*(y^\delta - F(x_k)) + \alpha_k (x_0 - x_k)\big], \qquad \alpha_k = \alpha_0 q^k .$$
The weights $\alpha_k$ fall geometrically, so the iteration fits the data more and more closely. With noisy data it must be stopped, usually by the [discrepancy principle](/morozov-discrepancy-principle/): at the first $k$ with $\|y^\delta - F(x_k)\| \le \tau\delta$. For a linear $F(x) = A x$, the iterate $x_{k+1}$ is exactly the Tikhonov solution with parameter $\alpha_k$ centered at $x_0$, so the method is a nonlinear version of Tikhonov regularization with a decreasing parameter. It is a standard method for parameter identification, inverse scattering and impedance tomography.

## In plain words

Gauss-Newton solves a nonlinear equation by repeatedly replacing it with a straight-line approximation and solving that. For an ill-posed problem each of these linear problems is unstable, so each one is solved with a Tikhonov penalty. The penalty asks the answer to stay near a fixed first guess. At first the penalty is strong, so the method makes only careful, smooth changes. Each step weakens the penalty by a fixed factor, so the method trusts the data more and more. When the predicted data match the measured data to within the noise, the method stops, because a closer fit would only fit the noise.

## The problem

Given a differentiable map $F: D(F) \subseteq X \to Y$ between Hilbert spaces ($\mathbb{R}^n \to \mathbb{R}^m$ in the code) with derivative $F'(x)$, data $y^\delta$ with $\|y^\delta - F(x^\dagger)\| \le \delta$, the noise level $\delta$, and an initial guess $x_0$ (which carries the prior knowledge), find an approximation of a solution $x^\dagger$ of $F(x) = y$ near $x_0$ whose error tends to 0 as $\delta \to 0$.

## The algorithm

```pseudo id=main
IRGNM(F, F', y, x₀, α₀, q, K, δ, τ)           ▷ α₀ > 0, 0 < q < 1, τ > 1
L1  x ← x₀;  α ← α₀
L2  for k ← 0 to K - 1 do
L3      if ‖y - F(x)‖ ≤ τ δ then return (x, k)
L4      J ← F'(x)
L5      solve (JᵀJ + α I) h = Jᵀ (y - F(x)) + α (x₀ - x)
L6      x ← x + h
L7      α ← q α
L8  return (x, K)
```

Line L1 starts at the initial guess, which is also the center of the penalty in every step. Line L3 is the discrepancy principle. Line L4 evaluates the Jacobian at the current iterate. Line L5 is the normal equation of the linearized Tikhonov problem
$$\min_h \ \|y - F(x) - J h\|^2 + \alpha \|x + h - x_0\|^2,$$
whose matrix is symmetric positive definite for $\alpha > 0$; the code solves it by Gaussian elimination. Line L6 takes the full step, with no line search. Line L7 lowers the weight, so that after $k$ steps $\alpha_k = \alpha_0 q^k$. Line L8 returns after $K$ steps if the residual never reached $\tau\delta$.

The difference from the [Levenberg-Marquardt](/levenberg-marquardt/) method is the center of the penalty. Levenberg-Marquardt penalizes the step $\|h\|$, which pulls toward $x_k$. IRGNM penalizes $\|x_{k+1} - x_0\|$, which keeps every iterate tied to the prior guess. This is what makes the convergence theory under a [source condition](/source-condition/) on $x^\dagger - x_0$ work.

## Example

**A scalar trace.** Take $F(x) = e^x$, $y = e$ (so $x^\dagger = 1$), exact data, $x_0 = 0$, $\alpha_0 = 1$ and $q = 0.5$. With $J = e^{x_k}$, the step is $x_{k+1} = x_k + \big(J(y - e^{x_k}) - \alpha_k x_k\big)/(J^2 + \alpha_k)$.

| $k$ | $\alpha_k$ | $x_k$ | $\lvert y - F(x_k)\rvert$ |
|---|---|---|---|
| 0 | 1 | 0 | 1.71828 |
| 1 | 0.5 | 0.85914 | 0.35715 |
| 2 | 0.25 | 0.92724 | 0.19075 |
| 3 | 0.125 | 0.96495 | 0.09362 |
| 4 | 0.0625 | 0.98279 | 0.04639 |
| 7 | 0.00781 | 0.99788 | 0.00575 |

For example, $x_1 = 0 + (1 \cdot 1.71828 - 0)/(1 + 1) = 0.85914$. After the first step the residual halves with each step, as $\alpha_k$ does: the pull toward $x_0 = 0$ holds the iterate back by an amount proportional to $\alpha_k$. Plain Gauss-Newton would converge quadratically here, because this scalar problem is well posed; the regularization costs speed and buys stability.

**A nonlinear integral equation.** The test problem of the code is a discrete form of $F(x)(s) = \int_0^s e^{x(t)}\,dt$ on $[0, 1]$ with $n = 32$ cells, the truth $x^\dagger(t) = 0.5\sin(\pi t)$, $x_0 = 0$, $\alpha_0 = 1$, $q = 0.5$, $\tau = 2$, and Gaussian noise drawn with `random.Random(2)` and scaled to norm $\delta$. The error is the discrete $L^2$ norm $\|x_k - x^\dagger\|/\sqrt n$ (a measurement).

| $k$ | $\alpha_k$ | residual, $\delta = 10^{-2}$ | error, $\delta = 10^{-2}$ | residual, $\delta = 10^{-3}$ | error, $\delta = 10^{-3}$ |
|---|---|---|---|---|---|
| 0 | 1 | 1.387 | 0.3536 | 1.389 | 0.3536 |
| 4 | 0.0625 | 0.2877 | 0.1219 | 0.2869 | 0.1223 |
| 8 | 0.0039 | 0.02766 | 0.0236 | 0.02664 | 0.0217 |
| 9 | 0.0020 | **0.01550** (stop) | **0.0196** | 0.01396 | 0.0139 |
| 12 | 0.00024 | 0.003811 | 0.0392 | **0.001917** (stop) | **0.0055** |
| 16 | 0.000015 | 0.0004085 | 0.0624 | 0.0001253 | 0.0063 |
| 21 | $4.8 \cdot 10^{-7}$ | 0.00001365 | 0.0655 | 0.000003936 | 0.0065 |

The discrepancy rule stops at $k = 9$ for $\delta = 10^{-2}$ and at $k = 12$ for $\delta = 10^{-3}$. In both cases the stopped iterate has the smallest error of the whole run. Running on shows [semi-convergence](/semi-convergence/): for $\delta = 10^{-2}$ the error grows by a factor of $3.3$ while the residual falls far below the noise level. With exact data the error falls at every step, to below $0.00005$ at $k = 19$.

## Correctness

The proofs are in proofs/correctness.md, in exact arithmetic.

- **The step is well defined and optimal (theorem).** For $\alpha > 0$ the matrix of line L5 is symmetric positive definite, and $x + h$ is the unique minimizer of the linearized Tikhonov functional $\|y - F(x) - J(z - x)\|^2 + \alpha\|z - x_0\|^2$ over $z$.
- **Linear case (theorem).** If $F(x) = A x$, then $x_{k+1} = x_0 + (A^* A + \alpha_k I)^{-1} A^*(y - A x_0)$ for every $k$, whatever $x_k$ is. So IRGNM is Tikhonov regularization centered at $x_0$, evaluated along the sequence $\alpha_0, \alpha_0 q, \alpha_0 q^2, \dots$, and the rates and the saturation of Tikhonov regularization carry over (see [Tikhonov convergence rates](/tikhonov-convergence-rates/)).
- **Termination (theorem).** The loop ends after at most $K$ steps. In the linear case with $\tau > 1$, the test of line L3 passes after finitely many steps for every $\delta > 0$.

For nonlinear $F$, convergence as $\delta \to 0$ and the rates $O(\delta^{2\nu/(2\nu+1)})$ under a source condition $x^\dagger - x_0 = (F'(x^\dagger)^* F'(x^\dagger))^\nu w$ need extra conditions on how nonlinear $F$ is near $x^\dagger$ (Bakushinskii 1992 for an a priori stopping index; Blaschke, Neubauer and Scherzer 1997 for the discrepancy principle; Kaltenbacher, Neubauer and Scherzer 2008, Chapter 4). They are cited, not proved here.

## Complexity

- **Per step.** One evaluation of $F$ at line L3, one Jacobian at line L4, forming $J^T J$ in $O(m n^2)$, and solving the $n \times n$ system in $O(n^3)$. With $f$ and $j$ the costs of $F$ and $F'$, that is $O(f + j + m n^2 + n^3)$.
- **Steps.** Each step multiplies $\alpha$ by $q$. The rule stops once $\alpha_k$ is small enough for the data error to reach the noise level, so the number of steps grows like $\log(1/\delta)$ when the a priori analysis applies; in the example it went from $9$ to $12$ when $\delta$ fell by a factor of $10$.
- **Space.** $O(m n + n^2)$ for the Jacobian and the normal matrix.
- **Large problems.** For images and wave fields, $J$ is never formed. Line L5 is solved approximately by [conjugate gradients](/conjugate-gradient-method/) on $J^* J + \alpha I$, with products $J h$ and $J^* r$ computed by linearized and [adjoint](/adjoint-state-method/) solves. Then a step costs a few tens of forward and adjoint solves.

## Properties

- **Prior-centered.** Every iterate is the minimizer of a Tikhonov functional centered at $x_0$, so the iterates do not drift away from the prior as Gauss-Newton iterates can.
- **Nonlinear in the data.** Both the linearization points and the stopping index depend on $y^\delta$.
- **Finite qualification.** In the linear case it is Tikhonov regularization, so with an a priori stopping index its rate saturates at $\nu = 1$ (in the convention $x^\dagger - x_0 = (A^* A)^\nu w$).
- **Monotone weights.** The sequence $\alpha_k$ must not fall too fast: the theory asks for $1 \le \alpha_k/\alpha_{k+1} \le r$ for some fixed $r$, which $q \in (0, 1)$ gives with $r = 1/q$.

## Variants and improvements

- **Inexact inner solves.** Solve line L5 by conjugate gradients with a tolerance that tightens with $k$ (truncated Newton-CG methods).
- **Other inner regularizations.** Replace Tikhonov in line L5 by a few Landweber or CG steps, or by iterated Tikhonov to raise the qualification.
- **Regularizing Levenberg-Marquardt.** Center the penalty at $x_k$ and choose $\alpha_k$ by an inner discrepancy rule (Hanke's method).
- **Constraints and Banach spaces.** Add bounds on $x$, or replace $\|x - x_0\|^2$ by a convex penalty such as total variation (Kaltenbacher, Neubauer and Scherzer 2008).
- **Nonlinear Landweber.** $x_{k+1} = x_k + \omega F'(x_k)^*(y^\delta - F(x_k))$ is cheaper per step but needs many more steps (see [Landweber iteration](/landweber-iteration/)).

## When to use it

Use IRGNM for a nonlinear inverse problem with a moderate number of unknowns, a Jacobian (or its products) that you can compute, a reasonable first guess, and a known noise level. Examples are coefficient identification in differential equations, inverse scattering, and electrical impedance tomography (see the [Calderon problem](/calderon-problem/)). It needs far fewer steps than nonlinear Landweber. For very large problems where only a gradient is affordable, as in [full waveform inversion](/full-waveform-inversion/), quasi-Newton methods with a fixed penalty are more common. For a well-posed nonlinear least squares problem, plain [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) is faster.

## Pitfalls

- **No stopping rule.** If line L3 is left out, the method keeps lowering $\alpha$ and fits the noise; the error grows again, as in the table.
- **$q$ too small.** If $\alpha$ drops too fast, the linearization is used far from where it is valid, and the iteration can diverge. Values from $0.5$ to $0.9$ are common.
- **$\alpha_0$ too small.** The first step is then a nearly unregularized Gauss-Newton step from $x_0$, which can be wild. Start with $\alpha_0$ of the order of $\|F'(x_0)\|^2$.
- **A poor initial guess.** The convergence theory is local: $x^\dagger - x_0$ must be small and satisfy a source condition. The method converges to a solution near $x_0$, and the result can depend on $x_0$.
- **A wrong Jacobian at line L4.** An inaccurate $F'$ slows convergence and breaks the theory. Check it against finite differences, and check the adjoint code if $J^*$ is applied matrix-free.

## Implementations

## History

A. B. Bakushinskii proposed the method in 1992 and proved convergence with an a priori stopping index under a source condition. B. Blaschke (later Kaltenbacher), A. Neubauer and O. Scherzer proved convergence and rates with the discrepancy principle in 1997. The book of Kaltenbacher, Neubauer and Scherzer (2008) presents the theory of this and related Newton type methods, including inexact inner solves and Banach space versions.

## References
