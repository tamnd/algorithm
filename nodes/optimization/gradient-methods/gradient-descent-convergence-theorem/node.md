---
tag: NDY404
kind: theorem
slug: gradient-descent-convergence-theorem
name: Convergence of gradient descent for smooth convex functions
aliases:
- O(1/k) rate for gradient descent
- sublinear rate of gradient descent
area: optimization/gradient-methods
level: advanced
summary: For a convex L_f-smooth f, gradient descent with step 1/L_f has f(x_k) - f* ≤ L_f R^2/(2k) and never moves away from a minimizer. The order 1/k cannot be improved for this method.
prereqs: [gradient-descent, convex-function, smoothness]
see_also: [linear-convergence-strongly-convex, first-order-lower-bound, nesterov-accelerated-gradient, backtracking-line-search, convergence-rate, polyak-lojasiewicz-condition, projected-gradient-descent]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 2.1.5, The gradient method (the rate of the gradient method on smooth convex functions)
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.2, Gradient descent for smooth functions
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 10, The proximal gradient method (the sublinear rate in the convex case, which contains gradient descent as the case h = 0)
  - paper: doi:10.1007/s10107-013-0653-0
    title: Yoel Drori and Marc Teboulle, Performance of first-order methods for smooth convex minimization, a novel approach, Mathematical Programming 145, 2014
    locator: pages 451 to 482 (the exact worst case L_f R^2/(4k + 2) of gradient descent with step 1/L_f, and the function that attains it)
  - paper: doi:10.4171/dms/6/27
    title: Claude Lemaréchal, Cauchy and the gradient method, Documenta Mathematica, Extra Volume Optimization Stories, 2012
    locator: pages 251 to 254
---

Let $f$ be [convex](/convex-function/) and $L_f$-[smooth](/smoothness/) with a minimizer. Then [gradient descent](/gradient-descent/) with a constant step $\alpha \in (0, 1/L_f]$ satisfies $f(x_k) - f^* \le \|x_0 - x^*\|^2 / (2\alpha k)$, which is $L_f R^2/(2k)$ for $\alpha = 1/L_f$. The distance to every minimizer does not increase, and the iterates converge to a minimizer. The rate $1/k$ is the right order for this method: a one-dimensional Huber function makes the error exactly $L_f R^2/(4k + 2)$. It is slower than the rate $1/k^2$ of [Nesterov's method](/nesterov-accelerated-gradient/), which the [first-order lower bound](/first-order-lower-bound/) shows to be optimal.

## Statement

**Theorem.** Let $f : \mathbb{R}^n \to \mathbb{R}$ be convex and differentiable, with $\|\nabla f(x) - \nabla f(y)\| \le L_f \|x - y\|$ for all $x, y$, and let the set $X^*$ of minimizers be nonempty, with $f^* = \min f$. Let $x_0 \in \mathbb{R}^n$, $0 < \alpha \le 1/L_f$, and $x_{k+1} = x_k - \alpha \nabla f(x_k)$. Then for every $x^* \in X^*$ and every $k \ge 1$:

1. $f(x_{k+1}) \le f(x_k) - \frac{\alpha}{2}\|\nabla f(x_k)\|^2$;
2. $\|x_{k+1} - x^*\| \le \|x_k - x^*\|$;
3. $f(x_k) - f^* \le \dfrac{\|x_0 - x^*\|^2}{2 \alpha k}$, in particular $f(x_k) - f^* \le \dfrac{L_f R^2}{2k}$ for $\alpha = 1/L_f$ and $R = \operatorname{dist}(x_0, X^*)$;
4. $x_k$ converges to a point of $X^*$.

## In plain words

Take a bowl-shaped landscape whose slope does not change too fast, and walk downhill with short fixed steps. Then each step takes you lower, and no step takes you farther from the bottom.

After some number of steps, the remaining height above the bottom is at most the starting distance squared, divided by a number that grows in proportion to the step count. So twice as many steps halve the guaranteed remaining height. This is a slow rate: each extra correct digit costs ten times as many steps. Some flat-bottomed bowls show that the method cannot do better than this, so a faster method needs a new idea, such as momentum.

## Proof

**Lemma (descent lemma).** For all $x, y$, $f(y) \le f(x) + \nabla f(x)^\top (y - x) + \frac{L_f}{2}\|y - x\|^2$.

*Proof.* With $h = y - x$, the fundamental theorem of calculus gives $f(y) - f(x) - \nabla f(x)^\top h = \int_0^1 (\nabla f(x + th) - \nabla f(x))^\top h\,dt$. By the Cauchy-Schwarz inequality and the Lipschitz bound, the integrand is at most $L_f t\|h\|^2$, and $\int_0^1 L_f t\,dt = L_f/2$. $\square$

Write $g_k = \nabla f(x_k)$.

*Claim 1.* Put $y = x_{k+1} = x_k - \alpha g_k$ in the lemma: $f(x_{k+1}) \le f(x_k) - \alpha\left(1 - \frac{L_f \alpha}{2}\right)\|g_k\|^2$. Since $L_f \alpha \le 1$, the factor $1 - L_f\alpha/2$ is at least $1/2$.

*A one-step inequality.* Convexity gives $f^* = f(x^*) \ge f(x_k) + g_k^\top (x^* - x_k)$. With claim 1,

$$f(x_{k+1}) - f^* \le g_k^\top (x_k - x^*) - \frac{\alpha}{2}\|g_k\|^2.$$

Expand $\|x_{k+1} - x^*\|^2 = \|x_k - x^*\|^2 - 2\alpha g_k^\top (x_k - x^*) + \alpha^2\|g_k\|^2$. Solve it for $g_k^\top(x_k - x^*) - \frac{\alpha}{2}\|g_k\|^2$ and substitute:

$$f(x_{k+1}) - f^* \le \frac{1}{2\alpha}\left(\|x_k - x^*\|^2 - \|x_{k+1} - x^*\|^2\right). \tag{$*$}$$

*Claim 2.* The left side of $(*)$ is at least $0$.

*Claim 3.* Add $(*)$ for $k = 0, \ldots, K - 1$. The right side telescopes:

$$\sum_{i=1}^{K}\left(f(x_i) - f^*\right) \le \frac{1}{2\alpha}\left(\|x_0 - x^*\|^2 - \|x_K - x^*\|^2\right) \le \frac{\|x_0 - x^*\|^2}{2\alpha}.$$

By claim 1 the values $f(x_i)$ do not increase, so each term of the sum is at least $f(x_K) - f^*$. Hence $K(f(x_K) - f^*) \le \|x_0 - x^*\|^2/(2\alpha)$. Take $x^*$ as the minimizer nearest to $x_0$ for the form with $R$; $X^*$ is closed and convex, so this point exists.

*Claim 4.* By claim 2 the sequence stays in the ball of radius $\|x_0 - x^*\|$ around $x^*$, so it has a convergent subsequence $x_{k_j} \to \bar{x}$. By claim 3 and continuity, $f(\bar{x}) = f^*$, so $\bar{x} \in X^*$. Apply claim 2 with $x^* = \bar{x}$: the distances $\|x_k - \bar{x}\|$ do not increase, and a subsequence of them tends to $0$. So the whole sequence tends to $0$, and $x_k \to \bar{x}$. $\blacksquare$

## Consequences

- **Iteration count.** With $\alpha = 1/L_f$, $f(x_k) - f^* \le \varepsilon$ for all $k \ge L_f R^2/(2\varepsilon)$.
- **Gradient norm.** Claim 1 and $f(x_{k+1}) \ge f^*$ give $\|\nabla f(x_k)\|^2 \le 2L_f(f(x_k) - f^*) \le L_f^2 R^2/k$, so $\|\nabla f(x_k)\| \le L_f R/\sqrt{k}$.
- **Unknown $L_f$.** With [backtracking line search](/backtracking-line-search/) and the Armijo constant $c = 1/2$, each step satisfies claim 1 with its own step $\alpha_i$, and the proof gives $f(x_k) - f^* \le R^2/(2k\alpha_{\min})$, with $\alpha_{\min} = \min(\alpha_0, \rho/L_f)$ for the initial trial step $\alpha_0$ and the shrink factor $\rho$.
- **Constraints.** The same proof with the gradient mapping in place of the gradient gives the bound $L_f R^2/(2k)$ for [projected gradient descent](/projected-gradient-descent/) and the [proximal gradient method](/proximal-gradient-method/) (Beck, Chapter 10).
- **Stronger assumptions give linear rates.** Under [strong convexity](/strong-convexity/) or the [Polyak-Lojasiewicz condition](/polyak-lojasiewicz-condition/), the error falls by a constant factor per step ([linear convergence theorem](/linear-convergence-strongly-convex/)).
- **Not optimal.** The [first-order lower bound](/first-order-lower-bound/) is of order $L_f R^2/k^2$, and Nesterov's method reaches it. So gradient descent needs the square of the number of steps of an optimal method, up to constants.

## Tightness

**The order $1/k$ is attained.** Fix $k \ge 1$, $L_f > 0$ and $R > 0$, and let $\delta = R/(2k + 1)$. Take the Huber-type function on $\mathbb{R}$

$$f(x) = \begin{cases} \frac{L_f}{2}x^2 & |x| \le \delta, \\ L_f\delta|x| - \frac{L_f}{2}\delta^2 & |x| \ge \delta. \end{cases}$$

It is convex, its derivative $f'(x) = L_f \max(-\delta, \min(\delta, x))$ is $L_f$-Lipschitz, $x^* = 0$ and $f^* = 0$. Start at $x_0 = R$ with $\alpha = 1/L_f$. While $x_i \ge \delta$, each step subtracts exactly $\delta$, so $x_k = R - k\delta = (k + 1)\delta \ge \delta$, and

$$f(x_k) = L_f\delta(k + 1)\delta - \frac{L_f}{2}\delta^2 = \frac{L_f\delta^2(2k + 1)}{2} = \frac{L_f R^2}{2(2k + 1)} = \frac{L_f R^2}{4k + 2}.$$

So no bound of the form $o(1/k)$ holds for gradient descent with step $1/L_f$ on this class, and the constant $1/2$ of the theorem is within a factor of about $2$ of the truth. Drori and Teboulle proved that $L_f R^2/(4k + 2)$ is the exact worst case for step $1/L_f$, so this function is a worst case.

**Quadratics are not the worst case.** On a convex quadratic with Hessian eigenvalues in $[0, L_f]$, gradient descent with step $1/L_f$ multiplies the eigencomponent for $\lambda$ by $1 - \lambda/L_f$, so $f(x_k) - f^* \le R^2 \max_{\lambda \in [0, L_f]}\frac{\lambda}{2}(1 - \lambda/L_f)^{2k}$. The maximum is at $\lambda = L_f/(2k + 1)$, and the bound is $\frac{L_f R^2}{2(2k + 1)}\left(\frac{2k}{2k + 1}\right)^{2k}$, about $L_f R^2/(4ek)$ for large $k$. This is smaller than the Huber value, so the bound of the theorem cannot be shown tight with quadratics alone.

**The step size range.** For $\alpha > 2/L_f$ the method diverges on $\frac{L_f}{2}x^2$, since $x_{k+1} = (1 - \alpha L_f)x_k$ with $|1 - \alpha L_f| > 1$. Steps in $(1/L_f, 2/L_f)$ still converge at the rate $O(1/k)$ with a different constant (Nesterov, Section 2.1.5); the theorem above covers only $\alpha \le 1/L_f$.

## History

Cauchy proposed the gradient method in 1847, as Lemaréchal recounts. Bounds of the form $O(L_f R^2/k)$ for convex smooth functions are standard in the textbooks of Nesterov (Section 2.1.5) and of Beck. Drori and Teboulle introduced the performance estimation approach in 2014, which computes the exact worst case of a first-order method by a semidefinite program, and they found the exact value $L_f R^2/(4k + 2)$ for step $1/L_f$.

## References
