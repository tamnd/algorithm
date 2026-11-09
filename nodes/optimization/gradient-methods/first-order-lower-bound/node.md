---
tag: 0CXN65
kind: theorem
slug: first-order-lower-bound
name: First-order lower bound for smooth convex optimization
aliases:
- Nesterov lower bound
- Nemirovski-Yudin lower bound
- lower complexity bound for smooth convex minimization
area: optimization/gradient-methods
level: research
summary: For k ≤ (n-1)/2, a convex quadratic makes every method with iterates in the span of past gradients have f(x_k) - f* ≥ 3 L_f R^2/(32(k+1)^2). So the 1/k^2 rate of Nesterov's method is optimal.
prereqs: [gradient-descent-convergence-theorem, krylov-subspace]
see_also: [nesterov-accelerated-gradient, gradient-descent-convergence-theorem, conjugate-gradient-method, unconstrained-smooth-minimization, condition-number-of-an-optimization-problem, query-model, linear-convergence-strongly-convex, convergence-rate]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 2.1.2, Lower complexity bounds for smooth convex functions (the worst function and the bound), and Section 2.1.4, the lower bounds for smooth strongly convex functions
  - book: isbn:9780471103455
    title: A. S. Nemirovsky and D. B. Yudin, Problem Complexity and Method Efficiency in Optimization, Wiley, 1983
    locator: the lower bounds on the information-based complexity of smooth convex minimization
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.5, Lower bounds
  - paper: doi:10.1016/j.jco.2016.11.001
    title: Yoel Drori, The exact information-based complexity of smooth convex minimization, Journal of Complexity 39, 2017
    locator: pages 1 to 16 (the lower bound that matches the optimized gradient method exactly)
  - paper: doi:10.1007/s10107-015-0949-3
    title: Donghwan Kim and Jeffrey A. Fessler, Optimized first-order methods for smooth convex minimization, Mathematical Programming 159, 2016
    locator: pages 81 to 107 (the optimized gradient method and its worst-case bound)
  - paper: doi:10.1007/s10107-019-01406-y
    title: Yair Carmon, John C. Duchi, Oliver Hinder and Aaron Sidford, Lower bounds for finding stationary points I, Mathematical Programming 184, 2020
    locator: pages 71 to 120 (the analogous lower bound for stationary points of nonconvex smooth functions)
---

The first-order lower bound says that no method that sees only gradients can minimize every convex $L_f$-[smooth](/smoothness/) function faster than at the rate $L_f R^2/k^2$. For each $k \le (n-1)/2$ there is a convex quadratic on $\mathbb{R}^n$ on which every method whose iterates lie in the span of the past gradients has $f(x_k) - f^* \ge \frac{3L_f R^2}{32(k+1)^2}$, where $R = \|x_0 - x^*\|$. [Nesterov's accelerated gradient method](/nesterov-accelerated-gradient/) reaches $2L_f R^2/(k+1)^2$, so it is optimal up to a constant factor, while [gradient descent](/gradient-descent/), with its rate $L_f R^2/(2k)$, is not. The analogous bound for $\mu$-strongly convex functions is a factor $\left(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\right)^{2}$ per step.

## Statement

**The class of methods.** A *first-order span method* is a method that starts at $x_0$ and picks each iterate in the affine span of the start and the gradients it has seen:

$$x_k \in x_0 + \operatorname{span}\{\nabla f(x_0), \nabla f(x_1), \ldots, \nabla f(x_{k-1})\}.$$

Gradient descent with any step sizes, heavy ball momentum, Nesterov's method, the [conjugate gradient method](/conjugate-gradient-method/) and nonlinear conjugate gradient methods are span methods. Quasi-Newton methods such as BFGS with the initial matrix $I$ are span methods too, since each search direction is a combination of the past gradients.

**Theorem (Nesterov).** Let $L_f > 0$, $n \ge 3$ and $1 \le k \le (n - 1)/2$, and let $x_0 \in \mathbb{R}^n$. There is a convex quadratic $f : \mathbb{R}^n \to \mathbb{R}$ with an $L_f$-Lipschitz gradient and a minimizer $x^*$ such that every first-order span method has

$$f(x_k) - f^* \ge \frac{3L_f\|x_0 - x^*\|^2}{32(k+1)^2} \qquad\text{and}\qquad \|x_k - x^*\|^2 \ge \frac18\|x_0 - x^*\|^2.$$

**Strongly convex case (Nesterov, Section 2.1.4).** On the Hilbert space $\ell_2$ of square-summable sequences, for each $\mu > 0$ and $\kappa = L_f/\mu > 1$, there is a $\mu$-strongly convex $L_f$-smooth quadratic on which every span method has $\|x_k - x^*\| \ge \left(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\right)^k\|x_0 - x^*\|$ and $f(x_k) - f^* \ge \frac{\mu}{2}\left(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\right)^{2k}\|x_0 - x^*\|^2$. This case is stated with its source and is not proved on this page.

## In plain words

A method that only asks for slopes learns about the landscape one direction at a time. The bad landscape here is a long chain: the slope at the start shows only the first link, and each new question can reveal at most one more link of the chain.

So after some number of questions, the method still knows nothing about the far half of the chain, and its guess must be wrong there. That leaves a gap that shrinks only like one over the square of the number of questions. A known method shrinks the gap at this speed, so it is the best possible up to a fixed factor. Plain downhill steps are slower, so they are not the best.

## Proof

Translating the variable by $x_0$ maps span methods to span methods, so assume $x_0 = 0$. Write $\mathbb{R}^{i, n}$ for the vectors of $\mathbb{R}^n$ whose coordinates after the $i$-th are $0$.

**The worst functions.** For $1 \le p \le n$ let

$$f_p(x) = \frac{L_f}{4}\left(\frac12\left(x_1^2 + \sum_{i=1}^{p-1}(x_i - x_{i+1})^2 + x_p^2\right) - x_1\right) = \frac{L_f}{4}\left(\frac12 x^\top A_p x - e_1^\top x\right),$$

where $A_p$ is the $n \times n$ matrix with the tridiagonal block $\operatorname{tridiag}(-1, 2, -1)$ of size $p$ in its upper left corner and zeros elsewhere.

**Step 1 (convex and $L_f$-smooth).** For each $x$, $x^\top A_p x = x_1^2 + \sum_{i<p}(x_i - x_{i+1})^2 + x_p^2 \ge 0$, so $f_p$ is convex. With $(a - b)^2 \le 2a^2 + 2b^2$, $x^\top A_p x \le x_1^2 + 2\sum_{i<p}(x_i^2 + x_{i+1}^2) + x_p^2 \le 4\|x\|^2$. So $0 \preceq \nabla^2 f_p = \frac{L_f}{4}A_p \preceq L_f I$, and the [eigenvalues](/eigenvalue/) of the Hessian lie in $[0, L_f]$.

**Step 2 (the minimizer).** The gradient is $\nabla f_p(x) = \frac{L_f}{4}(A_p x - e_1)$. The vector $\bar{x}^{(p)}$ with $\bar{x}^{(p)}_i = 1 - \frac{i}{p+1}$ for $i \le p$ and $0$ for $i > p$ solves $A_p x = e_1$: for $2 \le i \le p - 1$, $-\bar{x}_{i-1} + 2\bar{x}_i - \bar{x}_{i+1} = 0$ because the entries are linear in $i$; the first row gives $2(1 - \frac{1}{p+1}) - (1 - \frac{2}{p+1}) = 1$; the last row gives $-\frac{2}{p+1} + \frac{2}{p+1} = 0$. At a solution of $A_p x = e_1$, $\frac12 x^\top A_p x - e_1^\top x = -\frac12 x_1$, so

$$f_p^* = -\frac{L_f}{8}\left(1 - \frac{1}{p+1}\right).$$

Its squared norm is $\|\bar{x}^{(p)}\|^2 = \sum_{j=1}^{p}\left(\frac{j}{p+1}\right)^2 = \frac{p(2p+1)}{6(p+1)} \le \frac{p+1}{3}$.

**Step 3 (one new coordinate per gradient).** Since $A_p$ is tridiagonal, it maps $\mathbb{R}^{i, n}$ into $\mathbb{R}^{i+1, n}$, and $e_1 \in \mathbb{R}^{1, n}$. So if $x \in \mathbb{R}^{i, n}$, then $\nabla f_p(x) \in \mathbb{R}^{i+1, n}$. By induction on $k$, every span method run on $f_p$ from $x_0 = 0$ has $x_k \in \mathbb{R}^{k, n}$: $x_0 = 0 \in \mathbb{R}^{0,n}$, and if $x_0, \ldots, x_{k-1}$ lie in $\mathbb{R}^{k-1, n}$, their gradients lie in $\mathbb{R}^{k, n}$, and so does their span.

**Step 4 (on the first $k$ coordinates, $f_p$ is $f_k$).** Let $k \le p$ and $x \in \mathbb{R}^{k, n}$. In $f_p(x)$, the terms $(x_i - x_{i+1})^2$ with $i > k$ and the term $x_p^2$ (if $p > k$) are $0$, and the term $(x_k - x_{k+1})^2$ equals $x_k^2$. So $f_p(x) = f_k(x) \ge f_k^*$.

**Step 5 (the bound).** Take $p = 2k + 1 \le n$ and $f = f_{2k+1}$, with $x^* = \bar{x}^{(2k+1)}$. By steps 3 and 4,

$$f(x_k) - f^* \ge f_k^* - f_{2k+1}^* = \frac{L_f}{8}\left(\frac{1}{k+1} - \frac{1}{2k+2}\right) = \frac{L_f}{16(k+1)}.$$

By step 2, $R^2 = \|x^*\|^2 \le \frac{2k+2}{3}$, so $\frac{L_f}{16(k+1)} \ge \frac{L_f}{16(k+1)} \cdot \frac{3R^2}{2(k+1)} = \frac{3L_f R^2}{32(k+1)^2}$.

**Step 6 (the distance).** Since $x_k \in \mathbb{R}^{k, n}$, $\|x_k - x^*\|^2 \ge \sum_{i=k+1}^{2k+1}(x^*_i)^2 = \sum_{j=1}^{k+1}\left(\frac{j}{2k+2}\right)^2 = \frac{(k+2)(2k+3)}{24(k+1)}$, while $\|x^*\|^2 = \frac{(2k+1)(4k+3)}{12(k+1)}$. The ratio is $\frac{(k+2)(2k+3)}{2(2k+1)(4k+3)}$, and it is at least $\frac18$ because $4(k+2)(2k+3) = 8k^2 + 28k + 24 \ge 8k^2 + 10k + 3 = (2k+1)(4k+3)$. $\blacksquare$

## Consequences

- **Optimality of acceleration.** Nesterov's method has $f(x_k) - f^* \le 2L_f R^2/(k+1)^2$, which is at most $\frac{64}{3} \approx 21.3$ times the lower bound. So the complexity of the class is $\Theta(\sqrt{L_f R^2/\varepsilon})$ gradient calls while $k \le (n-1)/2$.
- **Gradient descent is not optimal.** Its worst case $L_f R^2/(4k + 2)$ ([convergence theorem](/gradient-descent-convergence-theorem/)) is of order $1/k$, against the possible $1/k^2$.
- **The iterates may not converge fast.** The distance bound says that no span method gets closer to $x^*$ than $\frac{1}{\sqrt{8}}R$ during the first $(n-1)/2$ steps, on this function. In high dimension, convergence of the values does not give convergence of the iterates at any rate.
- **The bound is dimension-free.** It holds for every $n \ge 2k + 1$, so it governs large-scale problems, where $n$ is much larger than the number of steps.
- **Conjugate gradient is optimal on quadratics.** It minimizes $f$ over the same [Krylov subspace](/krylov-subspace/) $x_0 + \operatorname{span}\{g_0, A g_0, \ldots, A^{k-1}g_0\}$ that contains the iterates of every span method on a quadratic, so on the worst function it attains the value $f_k^*$ exactly.
- **Strongly convex problems.** The strongly convex bound gives $\Omega(\sqrt{\kappa}\ln(1/\varepsilon))$ steps, matched by Nesterov's method with constant momentum.

## Tightness

- **In the number of steps.** The restriction $k \le (n-1)/2$ is needed for a bound of this kind: on a quadratic in $\mathbb{R}^n$ the conjugate gradient method finds the exact minimizer in at most $n$ steps.
- **In the constant.** Nesterov's method is within the factor $64/3$. Kim and Fessler (2016) found the optimized gradient method, with a smaller worst-case bound, about $L_f R^2/(k+1)^2$, and Drori (2017) proved a lower bound for large dimension that equals the bound of that method. So the optimal worst-case constant for this class is known exactly.
- **The span assumption.** Nemirovski and Yudin proved lower bounds of the same order for all deterministic first-order methods, without the span assumption, with a larger dimension. Nesterov's simpler quadratic proof above uses the span assumption.

## History

Nemirovski and Yudin founded the theory of information-based complexity of convex optimization in their 1983 book, with lower bounds on the number of oracle calls for convex classes, including smooth ones. Nesterov's 1983 method reached the rate $O(1/k^2)$ for smooth convex functions and so matched the bound. The tridiagonal quadratic and the proof above are from Nesterov's lectures. Drori's 2017 lower bound closed the gap in the constant. Carmon, Duchi, Hinder and Sidford proved the analogous lower bound of order $\varepsilon^{-2}$ for finding stationary points of smooth nonconvex functions.

## References
