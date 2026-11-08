---
tag: DVG38P
kind: concept
slug: order-of-accuracy
name: Order of accuracy
aliases:
- order of convergence
- order of a method
- convergence order
area: numerical/differential-equations
level: core
summary: "A method has order p when its global error is O(h^p) on bounded intervals for smooth problems. Measured in experiments by halving h and taking log2 of the error ratio."
prereqs: [local-truncation-error, global-error]
see_also: [consistency, butcher-order-conditions, dahlquist-barrier, richardson-extrapolation, adaptive-step-size-control, stiff-ode-problem, order-of-convergence, lax-equivalence-theorem]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.2 (order conditions), Section II.3 (convergence of one-step methods) and Section II.8 (asymptotic expansion of the global error)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.15 (B-convergence, order reduction on the Prothero-Robinson problem)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Appendix A (measuring errors, estimating the order of accuracy from computed results)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1 (order and convergence of one-step methods)
---

The order of accuracy of a method for differential equations is the exponent $p$ in the bound $\|e_n\| \le C h^p$ on its [global error](/global-error/), for all sufficiently smooth problems and all small step sizes $h$. Halving $h$ then divides the error by about $2^p$. A stable method has order $p$ when its [local truncation error](/local-truncation-error/) is $O(h^{p+1})$, which is how the order is proved; in experiments it is measured by halving $h$ and fitting the logarithm of the error ratio. The order says how fast the error falls, not how large it is.

## In plain words

The order tells you what you gain when you make the steps smaller. With a method of order one, steps half as long give about half the error. With order two, a quarter of the error. With order four, one sixteenth. So a method of higher order needs far fewer steps to reach a small error.

The promise holds only when the solution is smooth and the steps are already small. A method of high order can lose its advantage when the solution has a kink, when the problem is stiff, or when the steps are so small that rounding errors win. You check the order of a program by running it with several step sizes and comparing the errors.

## The idea

**Notation.** As on all pages of this sub-area: the problem $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$; step size $h$; grid $t_n = t_0 + nh$; approximations $y_n$; global error $e_n = y(t_n) - y_n$; Lipschitz constant $L$.

**Definition.** A method has order $p$ if for each problem with $f$ smooth enough (for one-step methods $f \in C^p$ suffices for most classical methods) and each $T > t_0$, there are $C$ and $h_0 > 0$ with

$$\max_{t_0 \le t_n \le T} \|e_n\| \le C h^p \qquad (0 < h \le h_0).$$

For multistep methods the starting values $y_1, \dots, y_{k-1}$ must also have errors $O(h^p)$. For PDE schemes one states the orders in $\Delta t$ and $\Delta x$ separately, for example $O(\Delta t + \Delta x^2)$, and names the norm.

**Local order gives global order.** In the classical (consistency) sense, a method has order $p$ when its local truncation error is $O(h^{p+1})$. For a one-step method whose step map is Lipschitz in $y$, this local order implies the global bound above (HNW I, Section II.3). For a linear multistep method the same holds if and only if the method is also [zero-stable](/zero-stability/) ([Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/)). For linear PDE schemes, stability plays the same role ([Lax equivalence theorem](/lax-equivalence-theorem/)). These are proved results.

**The asymptotic expansion.** For a one-step method of order $p$ and smooth $f$, the global error has the form

$$e_n = h^p\, E_p(t_n) + O(h^{p+1}),$$

where $E_p$ solves a linear differential equation $E_p' = f_y(t, y(t))\, E_p + d_{p+1}(t)$, $E_p(t_0) = 0$, driven by the principal local error term $d_{p+1}$ (HNW I, Section II.8). So, for small $h$ and $E_p(T) \ne 0$, $\|e_N^{(h)}\| / \|e_N^{(h/2)}\| \to 2^p$. This is an asymptotic statement, and it is the reason why measured ratios approach $2^p$.

**Measuring the order.** With a known exact solution, compute the errors $E(h)$ at a fixed time for $h, h/2, h/4, \dots$ and form

$$p_{\text{obs}} = \log_2 \frac{E(h)}{E(h/2)}.$$

Without an exact solution, use three runs: $p_{\text{obs}} = \log_2 \frac{\|y^{(h)} - y^{(h/2)}\|}{\|y^{(h/2)} - y^{(h/4)}\|}$, which has the same limit because the leading error term cancels in each difference. With more data, fit a line to $\log E$ against $\log h$ by least squares. The observed order is a measurement, not a proof.

**Order and cost.** To reach an error $\varepsilon$ at a fixed $T$, a method of order $p$ needs about $N \approx (C/\varepsilon)^{1/p}$ steps. If a step costs $s$ evaluations of $f$, the work is $s N$. For tight tolerances higher order wins; for loose ones a cheap low-order method can be faster, because the constants matter. In floating point with unit roundoff $u$, the total error behaves like $C h^p + c\, u / h$, so below some $h$ the error grows again.

**Order barriers.** The order is limited by the structure of a method: an explicit Runge-Kutta method with $s$ stages has $p \le s$, with $p \le s - 1$ for $s \ge 5$; a zero-stable linear $k$-step method has $p \le k + 2$; an A-stable linear multistep method has $p \le 2$ ([Dahlquist barrier](/dahlquist-barrier/)).

**Other kinds of order.** The stage order of an implicit Runge-Kutta method is the order of its internal stages; it governs [order reduction](/stiff-ode-problem/) on stiff problems. For [stochastic differential equations](/stochastic-differential-equation/) one distinguishes the strong order (pathwise error) and the weak order (error of expectations): [Euler-Maruyama](/euler-maruyama-method/) has strong order $1/2$ and weak order 1, and the [Milstein method](/milstein-method/) has strong order 1. The [order of convergence](/order-of-convergence/) of an iteration such as Newton's method is a different idea: there the error at step $k + 1$ is compared with a power of the error at step $k$.

## Examples

**Three methods on one problem.** For $y' = -2ty^2$, $y(0) = 1$, the exact value is $y(1) = 0.5$. The errors at $T = 1$ with $N$ equal steps are:

| $N$ | [Euler](/euler-method/) | [Heun](/heuns-method/) | [RK4](/classical-runge-kutta-4/) |
|---|---|---|---|
| 10 | $3.642 \cdot 10^{-3}$ | $9.186 \cdot 10^{-4}$ | $6.022 \cdot 10^{-7}$ |
| 20 | $1.805 \cdot 10^{-3}$ | $2.363 \cdot 10^{-4}$ | $4.093 \cdot 10^{-8}$ |
| 40 | $8.949 \cdot 10^{-4}$ | $5.976 \cdot 10^{-5}$ | $2.641 \cdot 10^{-9}$ |
| 80 | $4.451 \cdot 10^{-4}$ | $1.502 \cdot 10^{-5}$ | $1.674 \cdot 10^{-10}$ |
| $p_{\text{obs}}$ (last pair) | $1.008$ | $1.993$ | $3.980$ |

**Without the exact solution.** From the RK4 values $y^{(h)}$ for $N = 10, 20, 40, 80$ alone, the three-run formula gives $3.874$ and $3.952$, close to the values above.

**Order reduction by a non-smooth solution.** The problem $y' = \sqrt{t}$, $y(0) = 0$ has $y(1) = 2/3$. RK4 reduces to [Simpson's rule](/simpsons-rule/) here. With $N = 10, 20, 40, 80, 160$ the errors are $9.077 \cdot 10^{-4}$, $3.209 \cdot 10^{-4}$, $1.135 \cdot 10^{-4}$, $4.011 \cdot 10^{-5}$, $1.418 \cdot 10^{-5}$, and $p_{\text{obs}} = 1.500$ for each pair. The solution $\frac23 t^{3/2}$ is not $C^2$ at $t = 0$, and the first step alone has an error of order $h^{3/2}$.

**The rounding floor.** For RK4 on $y' = -2ty^2$ in double precision, $N = 16, 64, 256, 1024$ give errors $9.81 \cdot 10^{-8}$, $4.07 \cdot 10^{-10}$, $1.61 \cdot 10^{-12}$, $6.55 \cdot 10^{-15}$. After that the error stays between $0$ and $5 \cdot 10^{-15}$ (at $N = 65536$ it is $3.9 \cdot 10^{-15}$, at $N = 262144$ it is $4.8 \cdot 10^{-15}$): rounding, not truncation, decides it.

**Stiff order reduction.** On the Prothero-Robinson problem $y' = \lambda (y - g(t)) + g'(t)$ with $\operatorname{Re} \lambda \ll 0$, implicit Runge-Kutta methods converge with an order close to their stage order, not their classical order, when $h|\lambda|$ is large (HW II, Section IV.15). For the two-stage Gauss method, of classical order 4 and stage order 2, with $\lambda = -10^6$, $g(t) = \sin t$, $y(0) = 0$ and $T = 1$, the errors for $N = 10, 20, 40, 80$ are $2.336 \cdot 10^{-4}$, $5.829 \cdot 10^{-5}$, $1.446 \cdot 10^{-5}$, $3.503 \cdot 10^{-6}$: the observed order is 2, not 4.

## Where it is used

- **Choosing a method.** The order, together with the cost per step and the stability region, decides which method is cheapest for a given accuracy.
- **Testing code.** A convergence test that shows $p_{\text{obs}} \to p$ is the standard check that an implementation is right. A wrong coefficient in a Butcher tableau often drops the observed order to 1 or 2.
- **Step size control.** [Adaptive step size control](/adaptive-step-size-control/) uses the order to predict the next step: if the local error estimate is $\text{err}$ and the tolerance is $\text{tol}$, the new step is $h (\text{tol}/\text{err})^{1/(q+1)}$, where $q$ is the order of the lower-order method of the pair.
- **Extrapolation.** [Richardson extrapolation](/richardson-extrapolation/) uses the known exponent $p$ of the leading error term to remove it, which raises the order, as in the [Bulirsch-Stoer method](/bulirsch-stoer-method/).
- **PDE schemes.** The orders in space and time decide how to couple $\Delta t$ to $\Delta x$; for example the [Crank-Nicolson method](/crank-nicolson-method/) has order $O(\Delta t^2 + \Delta x^2)$, so $\Delta t$ can be of the same size as $\Delta x$.

## References
