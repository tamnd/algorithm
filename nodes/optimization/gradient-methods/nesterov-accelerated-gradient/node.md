---
tag: FR184S
kind: algorithm
slug: nesterov-accelerated-gradient
name: Nesterov accelerated gradient
aliases:
- Nesterov's accelerated gradient
- Nesterov momentum
- accelerated gradient method
- Nesterov's optimal method
area: optimization/gradient-methods
level: advanced
summary: A gradient step from an extrapolated point. On L_f-smooth convex f the error is at most 2L_f R^2/(k+1)^2, and the strongly convex form has the factor 1 - 1/√κ; both are optimal.
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, D: "L_f R^2 (the smoothness constant times the squared distance from x_0 to x*)", ε: the target accuracy, κ: the condition number L_f/μ}
  time: {worst: O(k n)}
  space: {extra: O(n)}
  gradients: {convex: O(√(D/ε)), strongly_convex: O(√κ log(1/ε)), step: "1"}
properties: {deterministic: true, iterative: true, descent_method: false, first_order: true, optimal: true}
history:
  year: 1983
  people: [Yurii Nesterov]
  note: Nesterov published the method in 1983 and showed the rate O(1/k^2), which matches the lower bound for first-order methods on smooth convex functions.
prereqs: [gradient-descent, momentum-method, first-order-lower-bound]
see_also: [momentum-method, fista, gradient-descent, first-order-lower-bound, linear-convergence-strongly-convex, proximal-gradient-method, condition-number-of-an-optimization-problem, convergence-rate]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 2.2, Optimal methods (estimating sequences and the constant step schemes for smooth convex and strongly convex functions)
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009
    locator: pages 183 to 202 (the sequence t_k and the proof of the rate 2L R^2/(k+1)^2, Theorem 4.4)
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.7, Nesterov's accelerated gradient descent (the strongly convex and the convex cases)
  - paper: doi:10.1561/2400000036
    title: Alexandre d'Aspremont, Damien Scieur and Adrien Taylor, Acceleration methods, Foundations and Trends in Optimization 5(1-2), 2021
    locator: Chapter 4, Nesterov acceleration (potential function proofs)
  - paper: doi:10.1007/s10208-013-9150-3
    title: Brendan O'Donoghue and Emmanuel Candès, Adaptive restart for accelerated gradient schemes, Foundations of Computational Mathematics 15(3), 2015
    locator: pages 715 to 732 (the ripples of the convex scheme on strongly convex functions and restart rules)
  - paper: doi:10.1007/s10107-015-0949-3
    title: Donghwan Kim and Jeffrey A. Fessler, Optimized first-order methods for smooth convex minimization, Mathematical Programming 159, 2016
    locator: pages 81 to 107 (the optimized gradient method)
  - paper: doi:10.1016/j.jco.2016.11.001
    title: Yoel Drori, The exact information-based complexity of smooth convex minimization, Journal of Complexity 39, 2017
    locator: pages 1 to 16 (the lower bound that the optimized gradient method attains)
  - paper: doi:10.1007/s10107-013-0677-5
    title: Olivier Devolder, François Glineur and Yurii Nesterov, First-order methods of smooth convex optimization with inexact oracle, Mathematical Programming 146, 2014
    locator: pages 37 to 75 (fast methods accumulate the errors of an inexact oracle)
---

Nesterov's accelerated gradient method takes a [gradient descent](/gradient-descent/) step from an extrapolated point: $x_k = y_k - \frac{1}{L_f}\nabla f(y_k)$ and $y_{k+1} = x_k + \beta_k(x_k - x_{k-1})$. With the momentum $\beta_k = (t_k - 1)/t_{k+1}$ of a simple scalar sequence, it reaches $f(x_k) - f^* \le 2L_f\|x_0 - x^*\|^2/(k+1)^2$ on every convex $L_f$-[smooth](/smoothness/) function, against $L_f\|x_0 - x^*\|^2/(2k)$ for gradient descent. With the constant momentum $(\sqrt\kappa - 1)/(\sqrt\kappa + 1)$, the error of a $\mu$-strongly convex function shrinks by $1 - 1/\sqrt\kappa$ per step. Both rates match the [first-order lower bound](/first-order-lower-bound/) up to constants, so the method is optimal among methods that only use gradients. Unlike the [heavy ball method](/momentum-method/), these guarantees hold for every smooth convex function, not only for quadratics.

## In plain words

Gradient descent looks at the slope where it stands and steps downhill. The accelerated method first coasts a little further in the direction it was already moving, then looks at the slope at that look-ahead point and steps downhill from there.

Looking ahead makes the difference. If the coasting has carried the point too far, the slope at the look-ahead point already shows it, and the gradient step pulls back before the overshoot grows. This keeps the speed that momentum builds up, without the wild swings.

The amount of coasting grows slowly over time in the general case, and it stays fixed when the bowl is known to be curved enough.

## The problem

The input is the gradient $\nabla f$ of a convex $L_f$-smooth $f : \mathbb{R}^n \to \mathbb{R}$, the constant $L_f$ (or an upper bound), optionally a strong convexity constant $\mu > 0$, a start $x_0$ and a number of iterations $K$. The output is the last iterate $x_K$. All arithmetic is in floating point; the tests compare with a relative tolerance of $10^{-9}$.

## The algorithm

```pseudo id=main
NESTEROV-AGD(∇f, x₀, L, K, μ = 0)
L1  x_prev ← x₀;  y ← x₀;  t ← 1
L2  for k ← 1 to K do
L3      x ← y − ∇f(y)/L                                  ▷ gradient step from the look-ahead point
L4      t_next ← (1 + √(1 + 4t²))/2
L5      β ← (t − 1)/t_next,  or β ← (√κ − 1)/(√κ + 1) if μ > 0
L6      y ← x + β (x − x_prev)                            ▷ extrapolate
L7      (x_prev, t) ← (x, t_next)
L8  return x
```

Line L3 is a gradient step with step $1/L_f$, taken from $y_k$ in place of $x_{k-1}$. Lines L4 and L5 compute the momentum. In the convex case, $t_1 = 1$ and $t_{k+1} = (1 + \sqrt{1 + 4t_k^2})/2$, so $t_{k+1}^2 - t_{k+1} = t_k^2$ and $t_k \ge (k + 1)/2$; the momentum $\beta_k = (t_k - 1)/t_{k+1}$ starts at $0$ and tends to $1$ like $1 - 3/k$. In the strongly convex case it is fixed. Line L6 extrapolates past $x_k$ along the last step.

## Example

Take $f(x) = \frac12(x_1^2 + 10x_2^2)$, so $L_f = 10$, $\mu = 1$, and start at $x_0 = (10, 1)$. The first gradient step with step $1/10$ gives $x_1 = (9, 0)$: it solves the steep coordinate at once, and the rest of the run is about $x_1$ alone. The table gives the first $k$ with $\|\nabla f(x_k)\| \le 10^{-6}$, and the same for $f(x) = \frac12(x_1^2 + 1000x_2^2)$ with $L_f = 1000$.

| method | $\kappa = 10$ | $\kappa = 1000$ |
|---|---|---|
| gradient descent, step $1/L_f$ | 153 | 16111 |
| accelerated, convex momentum $(t_k - 1)/t_{k+1}$ | 148 | 6479 |
| accelerated, constant momentum $(\sqrt\kappa - 1)/(\sqrt\kappa + 1)$ | 50 | 595 |

With the convex momentum, $f(x_k)$ is not monotone: on the first function it increases at steps $11$ to $14$, $21$ to $24$, and so on. The momentum grows towards $1$ and the iterate overshoots the minimizer, with a period of about $10$ steps here. The constant momentum, tuned to $\kappa$, has no such ripples on this run.

**The lower bound function.** On Nesterov's worst-case quadratic in $\mathbb{R}^{2k+1}$ from the [first-order lower bound](/first-order-lower-bound/), started at $0$ with $L_f = 1$, the gap after $k = 100$ steps is $0.00198$. The lower bound $3L_fR^2/(32(k+1)^2)$ is $0.00061$ and the upper bound $2L_fR^2/(k+1)^2$ is $0.0131$, so the method is within a factor of about $3.2$ of the best possible on this function.

## Correctness

The proofs are in the correctness proof of this page. Let $x^*$ be a minimizer, $f^* = f(x^*)$ and $R = \|x_0 - x^*\|$.

1. **Key inequality.** For every $y$ and $z$, with $x^+ = y - \nabla f(y)/L_f$,
   $$f(x^+) \le f(z) + \frac{L_f}{2}\left(\|y - z\|^2 - \|x^+ - z\|^2\right).$$
   It follows from the descent lemma and convexity.
2. **Convex case.** With $u_k = t_kx_k - (t_k - 1)x_{k-1} - x^*$, the potential $E_k = t_k^2(f(x_k) - f^*) + \frac{L_f}{2}\|u_k\|^2$ does not increase, and $E_1 \le \frac{L_f}{2}R^2$. Hence for every $k \ge 1$
   $$f(x_k) - f^* \le \frac{L_fR^2}{2t_k^2} \le \frac{2L_fR^2}{(k + 1)^2}.$$
   *Reason:* apply the key inequality at $y = y_k$ with $z = (1 - 1/t_k)x_{k-1} + (1/t_k)x^*$ and multiply by $t_k^2$; the identity $t_k^2 - t_k = t_{k-1}^2$ makes the terms telescope.
3. **Strongly convex case.** With constant momentum, $s = 1/\sqrt\kappa$ and $z_k = x_k + (\sqrt\kappa - 1)(x_k - x_{k-1})$ ($x_{-1} = x_0$), the potential $\Phi_k = f(x_k) - f^* + \frac{\mu}{2}\|z_k - x^*\|^2$ satisfies $\Phi_{k+1} \le (1 - s)\Phi_k$. Hence
   $$f(x_k) - f^* \le \left(1 - \frac{1}{\sqrt\kappa}\right)^k\left(f(x_0) - f^* + \frac{\mu}{2}R^2\right) \le \left(1 - \frac{1}{\sqrt\kappa}\right)^k\frac{L_f + \mu}{2}R^2.$$

## Complexity

Each iteration costs one gradient and $O(n)$ arithmetic, and the method stores $x$, $x_{\text{prev}}$ and $y$, so the extra space is $O(n)$.

**Convex.** By claim 2, $f(x_k) - f^* \le \varepsilon$ once $k + 1 \ge \sqrt{2L_fR^2/\varepsilon}$, so $O(\sqrt{L_fR^2/\varepsilon})$ gradients suffice. The [first-order lower bound](/first-order-lower-bound/) shows that no method that moves in the span of the gradients can do better than $\Omega(\sqrt{L_fR^2/\varepsilon})$ for $k$ below about $n/2$.

**Strongly convex.** By claim 3, $O(\sqrt\kappa\log(L_fR^2/\varepsilon))$ gradients suffice, against $O(\kappa\log(1/\varepsilon))$ for gradient descent. The lower bound for this class is also of order $\sqrt\kappa\log(1/\varepsilon)$.

| setting | gradients to accuracy $\varepsilon$ | gradient descent |
|---|---|---|
| convex, $L_f$-smooth | $O(\sqrt{L_fR^2/\varepsilon})$ | $O(L_fR^2/\varepsilon)$ |
| $\mu$-strongly convex, $L_f$-smooth | $O(\sqrt\kappa\log(L_fR^2/\varepsilon))$ | $O(\kappa\log(L_fR^2/\varepsilon))$ |

## Properties

- **Optimal.** Both rates match the lower bounds for first-order methods up to constant factors.
- **Not a descent method.** $f(x_k)$ can increase, as in the example. The potentials $E_k$ and $\Phi_k$ decrease, not $f$.
- **Gradient at the look-ahead point.** The only change from the [heavy ball method](/momentum-method/) is that the gradient is computed at $y_k$, not at $x_k$. This is what makes the proof work for every smooth convex function.
- **Needs $L_f$.** The step is $1/L_f$. A backtracking version that increases an estimate of $L_f$ until the quadratic upper bound holds keeps the rate up to a constant factor.
- **Proximal form.** Replacing the gradient step by a proximal gradient step gives [FISTA](/fista/) for composite problems, with the same rate and the same proof.

## Variants and improvements

- **[FISTA](/fista/).** The same scheme with a [proximal gradient](/proximal-gradient-method/) step, for $f + h$ with $h$ convex and possibly nonsmooth.
- **Adaptive restart.** O'Donoghue and Candès reset $t \leftarrow 1$ (and $x_{\text{prev}} \leftarrow x$) when $f$ increases or when the step and the gradient point the same way. This removes the ripples and recovers a linear rate on strongly convex functions without knowing $\mu$.
- **Constant momentum without $\mu$.** If $\mu$ is unknown, restarting every $O(\sqrt\kappa)$ steps gives the accelerated linear rate when $\kappa$ is known up to a constant, and adaptive restart works well in practice.
- **Optimized gradient method.** Kim and Fessler (2016) give a method of the same form whose worst-case bound is about half of Nesterov's, and Drori (2017) showed that no method of this class has a smaller worst-case bound.
- **Stochastic "Nesterov momentum".** Deep learning libraries implement the look-ahead gradient with a stochastic gradient and a fixed $\beta$; it keeps the form but not the guarantee.

## When to use it

Use the accelerated method for smooth convex problems when gradients are expensive and the condition number is large, for example regularized regression, logistic regression and image reconstruction. With a known strong convexity constant, use the constant momentum; without it, use the convex momentum with adaptive restart. For nonsmooth terms, use [FISTA](/fista/). For problems that are cheap per iteration and have some curvature structure, [L-BFGS](/limited-memory-bfgs/) is often faster in practice, though without the worst-case guarantee.

## Pitfalls

- **Monitoring $f$.** The values go up and down. Do not stop or reject steps because $f$ increased, unless you restart.
- **A wrong $L_f$.** With $L$ below the true smoothness constant the method can diverge; with $L$ much larger it is slow. Use backtracking on $L$ when in doubt.
- **The convex momentum on a strongly convex problem.** It still converges, at the rate $O(1/k^2)$ guaranteed by claim 2, but it does not use the strong convexity, and the ripples of the example appear. Use the constant momentum or restart.
- **The wrong point for the gradient.** Computing the gradient at $x_k$ in place of $y_k$ gives the heavy ball method, which has no global accelerated guarantee.
- **Errors in the gradient.** Devolder, Glineur and Nesterov show that with an inexact gradient oracle, fast methods accumulate the errors while gradient descent does not, so with inexact or stochastic gradients the advantage can disappear.

## Implementations

The Python function runs the method with the convex momentum, or with the constant momentum when $\mu > 0$ is given, and returns all the gradient-step points $x_0, \ldots, x_K$.

## History

Yurii Nesterov published the method in 1983 in Soviet Mathematics Doklady, with the rate $O(1/k^2)$, which matched the lower bound of Nemirovski and Yudin for smooth convex functions. He later developed the method of estimating sequences, which gives the strongly convex scheme, in his books. Beck and Teboulle extended the method to composite problems in 2009 under the name FISTA, with the short proof through the sequence $t_k$ that is given here.

## References
