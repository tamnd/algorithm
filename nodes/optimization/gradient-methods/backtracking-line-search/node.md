---
tag: G81MN3
kind: algorithm
slug: backtracking-line-search
name: Backtracking line search
aliases:
- Armijo backtracking
- Armijo line search
- backtracking Armijo rule
area: optimization/gradient-methods
level: core
summary: Try a step α_0, then shrink it by a factor ρ until the Armijo condition holds. It needs no smoothness constant and gives gradient descent the same rates as the step 1/L_f, up to constants.
solves: [step-size-selection]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of trial steps in one call}
  time: {worst: O(m n)}
  space: {extra: O(n)}
properties: {deterministic: true, iterative: true, needs_smoothness_constant: false}
history:
  year: 1966
  people: [Larry Armijo]
  note: Armijo's 1966 paper gave the rule with the factor 1/2, trial steps halved from a fixed start, and a convergence proof for functions with Lipschitz gradients.
prereqs: [armijo-condition]
see_also: [armijo-condition, wolfe-conditions, exact-line-search, gradient-descent, step-size-selection, gradient-descent-convergence-theorem, proximal-gradient-method, polyak-step-size]
sources:
  - paper: doi:10.2140/pjm.1966.16.1
    title: Larry Armijo, Minimization of functions having Lipschitz continuous first partial derivatives, Pacific Journal of Mathematics 16(1), 1966
    locator: pages 1 to 3
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 3.1, Step length (Algorithm 3.1, Backtracking line search)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.2, Descent methods (Algorithm 9.2, Backtracking line search), Section 9.3.1, Convergence analysis (gradient descent with backtracking line search on strongly convex functions), and Section 9.5.3 (the unit Newton step passes the backtracking test near the minimizer)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 10, The proximal gradient method (the backtracking procedure for an unknown smoothness constant)
---

Backtracking line search chooses a step along a descent direction $d$ by trial and error: it tries $\alpha_0$, then $\rho\alpha_0$, $\rho^2\alpha_0$, and so on, and it returns the first step that meets the [Armijo condition](/armijo-condition/) $f(x + \alpha d) \le f(x) + c\,\alpha\,\nabla f(x)^\top d$. It needs only values of $f$ and one gradient, and no knowledge of the [smoothness](/smoothness/) constant $L_f$. For an $L_f$-smooth $f$ it stops after at most about $\log_{1/\rho}(\alpha_0 L_f)$ trials, and the step it returns is at least $\min(\alpha_0, 2\rho(1 - c)/L_f)$ along $-\nabla f(x)$. So [gradient descent](/gradient-descent/) with backtracking keeps the rates of the fixed step $1/L_f$, with $L_f$ replaced by a constant of the same size.

## In plain words

You want to walk downhill, but you do not know how far is safe. So you try a long step first. If the new spot is not clearly lower than where you stand, the step was too long: you go back and try a step half as long, then half again, until the new spot is low enough.

"Low enough" means the drop is at least a small fixed part of the drop you would expect if the hill kept the slope it has under your feet. Because the trial steps start long and shrink by a fixed factor, the step you accept is never much shorter than the longest safe step.

## The problem

The input is a function $f : \mathbb{R}^n \to \mathbb{R}$, a point $x$ with the value $f(x)$ and the gradient $g = \nabla f(x)$, a descent direction $d$ with $g^\top d < 0$, a first trial step $\alpha_0 > 0$, a shrink factor $\rho \in (0, 1)$ and the Armijo constant $c \in (0, 1)$. The output is a step $\alpha > 0$ with $f(x + \alpha d) \le f(x) + c\alpha g^\top d$. When the method is used inside gradient descent, $d = -g$. All arithmetic is in floating point; the tests compare with a relative tolerance of $10^{-9}$.

## The algorithm

```pseudo id=main
BACKTRACKING(f, x, f(x), g, d, α₀, ρ, c)
L1  s ← gᵀd                                   ▷ the slope of φ(α) = f(x + αd) at 0
L2  if s ≥ 0 then error "d is not a descent direction"
L3  α ← α₀
L4  while f(x + α d) > f(x) + c · α · s do     ▷ the Armijo test
L5      α ← ρ α
L6  return α
```

Line L1 computes the slope $\varphi'(0) = g^\top d$ once. Line L2 rejects a direction that does not go downhill, because then the loop of L4 need not stop. Line L4 evaluates $f$ at the trial point and compares it with the line of slope $cs$ through $(0, f(x))$. Line L5 shrinks the step by the factor $\rho$. Common values are $\rho = \frac12$ and $c = 10^{-4}$; Boyd and Vandenberghe suggest $c$ between $0.01$ and $0.3$ and $\rho$ between $0.1$ and $0.8$. For Newton and quasi-Newton directions $\alpha_0 = 1$, so that the full step is taken when it is good; for gradient descent a common choice is the last accepted step times a factor above $1$.

## Example

Take $f(x) = \frac12(x_1^2 + 10x_2^2)$, $x = (10, 1)$, $g = (10, 10)$, $d = -g$, so $f(x) = 55$, $s = -200$ and $\varphi(\alpha) = 55 - 200\alpha + 550\alpha^2$. With $\alpha_0 = 1$, $\rho = \frac12$ and $c = 10^{-4}$:

| trial | $\alpha$ | $f(x + \alpha d)$ | Armijo bound $55 - 0.02\alpha$ | result |
|---|---|---|---|---|
| 1 | $1$ | $405$ | $54.98$ | reject |
| 2 | $0.5$ | $92.5$ | $54.99$ | reject |
| 3 | $0.25$ | $39.375$ | $54.995$ | accept |

With $c = \frac12$ the bound is $55 - 100\alpha$, the trial $0.25$ is rejected ($39.375 > 30$), and the search accepts $0.125$ after four trials, with $f = 38.59 \le 42.5$.

Gradient descent from $(10, 1)$ with backtracking from $\alpha_0 = 1$ at each step and $\rho = \frac12$ reaches $\|\nabla f\| \le 10^{-6}$ after $65$ steps with $c = 10^{-4}$ (217 values of $f$) and after $55$ steps with $c = \frac12$ (195 values of $f$). The fixed step $1/L_f = 0.1$ needs $153$ steps. The accepted steps change from one iteration to the next (with $c = 10^{-4}$ the first four are $0.25$, $0.125$, $0.5$ and $0.125$), so backtracking can be faster than the fixed step on this function, where $1/L_f$ is set by the steep direction alone.

## Correctness

Let $f$ be continuously differentiable and $g^\top d < 0$.

1. **Termination.** The loop stops after finitely many trials.
2. **The Armijo condition holds** for the returned $\alpha$: the loop of L4 exits only when the test fails, that is, when $f(x + \alpha d) \le f(x) + c\alpha s$.
3. **The step is not too short.** If $\nabla f$ is $L_f$-Lipschitz, then every $\alpha \le \bar{\alpha} = 2(1 - c)|s|/(L_f\|d\|^2)$ passes the Armijo test ([Armijo condition](/armijo-condition/)). The returned step is $\alpha_0$, or it is $\rho$ times a rejected step, which exceeds $\bar{\alpha}$. So $\alpha \ge \min(\alpha_0, \rho\bar{\alpha})$, and along $d = -g$ this is $\min(\alpha_0, 2\rho(1 - c)/L_f)$.
4. **Number of trials.** At most $1 + \max\left(0, \lceil\log_{1/\rho}(\alpha_0/\bar{\alpha})\rceil\right)$ trials.

For gradient descent with backtracking along $d_k = -\nabla f(x_k)$ and the bound $\alpha_k \ge \alpha_{\min} = \min(\alpha_0, 2\rho(1 - c)/L_f)$:

- **Nonconvex:** $\min_{i < k}\|\nabla f(x_i)\|^2 \le (f(x_0) - f^*)/(c\sum_{i<k}\alpha_i) \le (f(x_0) - f^*)/(c k \alpha_{\min})$.
- **Convex, with $c \ge \frac12$:** $f(x_k) - f^* \le R^2/(2\sum_{i<k}\alpha_i) \le R^2/(2k\alpha_{\min})$, and the distance to the set of minimizers does not increase.
- **$\mu$-strongly convex, any $c$:** $f(x_{k+1}) - f^* \le (1 - 2\mu c\alpha_k)(f(x_k) - f^*)$, so the rate is linear with the factor $1 - 2\mu c\alpha_{\min}$.

The proofs are in the correctness proof of this page.

## Complexity

**One call.** Each trial is one evaluation of $f$ and $O(n)$ arithmetic for $x + \alpha d$, so $m$ trials cost $m$ values of $f$ and $O(mn)$ operations, plus $O(n)$ for the slope. The extra space is $O(n)$. For an $L_f$-smooth $f$ and $d = -g$, claim 4 gives $m \le 1 + \max(0, \lceil\log_{1/\rho}(\alpha_0 L_f/(2(1 - c)))\rceil)$, independent of $n$.

**Inside gradient descent.** The number of iterations is the number for the fixed step $\alpha_{\min}$: about $R^2/(2\alpha_{\min}\varepsilon)$ for convex $f$ (with $c \ge \frac12$) and about $\ln(1/\varepsilon)/(2\mu c\alpha_{\min})$ for strongly convex $f$. If $\alpha_0$ is fixed at each iteration, the total number of values of $f$ is the number of iterations times $m$.

| claim | value |
|---|---|
| time of one call | $O(mn)$ plus $m$ values of $f$ |
| extra space | $O(n)$ |
| trials, $L_f$-smooth $f$, $d = -g$ | $O(1 + \log(\alpha_0 L_f))$ |

## Properties

- **No constant needed.** It adapts to the local curvature, so on functions where $L_f$ is much larger than the curvature along the path it takes longer steps than $1/L_f$.
- **Monotone.** Each accepted step lowers $f$ by at least $c\alpha|g^\top d|$.
- **Accepts the full step when it is good.** With $\alpha_0 = 1$ and $c < \frac12$, the unit step of Newton's method passes near a minimizer with a positive definite Hessian, so backtracking keeps the local quadratic rate of Newton's method.
- **No curvature condition.** The step satisfies the Armijo condition but not the [Wolfe](/wolfe-conditions/) curvature condition in general, so it does not ensure $y^\top s > 0$ for quasi-Newton updates.

## Variants and improvements

- **Interpolation.** In place of the fixed factor $\rho$, fit a quadratic or cubic to $\varphi(0)$, $\varphi'(0)$ and the last trial values and take its minimizer, kept in $[0.1\alpha, 0.5\alpha]$ (Nocedal and Wright, Section 3.5).
- **Goldstein and Wolfe line searches.** Add a condition that excludes short steps, with a bracketing phase that can also increase $\alpha$. Quasi-Newton methods use the strong [Wolfe conditions](/wolfe-conditions/).
- **Backtracking on $L_f$.** Proximal and accelerated methods keep an estimate $L$ of the smoothness constant and multiply it by $\eta > 1$ until the quadratic upper bound $f(x^+) \le f(x) + \nabla f(x)^\top(x^+ - x) + \frac{L}{2}\|x^+ - x\|^2$ holds (Beck, Chapter 10). This is the same idea with a different test.
- **Nonmonotone line search.** Compare with the largest of the last few values of $f$ in place of $f(x)$, which lets methods such as the Barzilai-Borwein step keep their long steps.
- **Warm start.** Start each search from the last accepted step times a factor such as $2$, so that the search can also grow the step.

## When to use it

Use backtracking when $L_f$ is unknown or the local curvature varies much, and when $f$ is cheap compared with $\nabla f$. It is the standard step rule for gradient descent and for damped Newton methods. Use a strong Wolfe line search for [BFGS](/bfgs/), [L-BFGS](/limited-memory-bfgs/) and [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/), because they need the curvature condition. For stochastic gradients, backtracking on a noisy $f$ is unreliable; [stochastic gradient descent](/stochastic-gradient-descent/) uses step schedules.

## Pitfalls

- **A direction that is not a descent direction.** If $g^\top d \ge 0$, the loop need not stop, or it stops with a tiny useless step. Line L2 checks this.
- **Starting too small.** Backtracking can only shrink the step. With $\alpha_0$ far below $1/L_f$, every step is $\alpha_0$, and the method is as slow as a fixed small step. Start large, or grow the start between iterations.
- **The wrong constant for the convex rate.** The bound $R^2/(2\sum\alpha_i)$ uses $c \ge \frac12$. With a smaller $c$ the proof of that bound fails. If the level set $\{x : f(x) \le f(x_0)\}$ has a finite diameter $D_0$, a rate of order $D_0^2/(c\,k\,\alpha_{\min})$ still follows from $f(x_k) - f^* \le \|\nabla f(x_k)\|D_0$ and the decrease $c\alpha_k\|\nabla f(x_k)\|^2$ at each step.
- **Rounding near the minimum.** When $f(x + \alpha d) - f(x)$ is at the level of rounding errors, the Armijo test compares noise, and the accepted steps are arbitrary. Stop on a small gradient norm, such as $10^{-6}$, before this happens.
- **A wrong gradient.** If $g$ is not the gradient at $x$, the slope $s$ is wrong and the Armijo test can accept steps that increase $f$ less than predicted or reject all reasonable steps.

## Implementations

The Python version returns the accepted step and the number of trials, and the module also has a gradient descent driver that records the accepted steps.

## History

Larry Armijo published the rule in 1966 in a three-page paper in the Pacific Journal of Mathematics, with the constant $\frac12$, trial steps halved from a fixed start, and a proof of convergence for functions with Lipschitz continuous gradients. Goldstein had proposed a two-sided test in 1965, and Wolfe added the curvature condition in 1969. The general constants $c$ and $\rho$ and the name "backtracking" are standard in textbooks such as Nocedal and Wright and Boyd and Vandenberghe.

## References
