---
tag: 4DWMHX
kind: concept
slug: local-truncation-error
name: Local truncation error
aliases:
- local discretization error
- local error
- truncation error
area: numerical/differential-equations
level: core
summary: "The error of one step started on the exact solution: delta_(n+1) = y(t_(n+1)) - Phi_h(t_n, y(t_n)). A method of order p has delta = O(h^(p+1)); stability turns this into a global error O(h^p)."
prereqs: [ode-initial-value-problem]
see_also: [global-error, order-of-accuracy, consistency, euler-method, heuns-method, linear-multistep-methods, butcher-order-conditions, adaptive-step-size-control]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.2 (order of Runge-Kutta methods and the local error), Section II.3 (error estimation and convergence, Lady Windermere's fan), Section III.2 (local error and order conditions of multistep methods)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (local truncation errors of one-step and multistep methods) and Chapter 9 (truncation error of schemes for the heat equation)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1 (order of a method) and Chapter 2 (order of multistep methods)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 3 (local truncation error, consistency, 0-stability and convergence)
---

The local truncation error of a method for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$ is the error that one step makes when it starts on the exact solution. It is the defect left when the exact solution is put into the formula of the method. A method has [order](/order-of-accuracy/) $p$ when this defect is $O(h^{p+1})$ for smooth problems, and a stable method then has a [global error](/global-error/) of $O(h^p)$. The local error is what order conditions are built from and what [step size control](/adaptive-step-size-control/) estimates.

## In plain words

Imagine that you stand exactly on the true path and take one step with the method. You land close to the path, but not on it. The distance between where you land and where the path really is after that step is the local error. It measures how good the rule for one step is, without the errors of earlier steps.

To reach a fixed end time you take many steps, so many small local errors add up to the error at the end. The number of steps grows as the steps get shorter, so the error at the end is about one power of the step length larger than one local error. A method whose local error shrinks fast when the step gets shorter is a method of high order.

## The idea

**Notation.** As on all pages of this sub-area: step size $h$, grid $t_n = t_0 + nh$, approximations $y_n \approx y(t_n)$, global error $e_n = y(t_n) - y_n$, Lipschitz constant $L$ of $f$ in $y$.

**One-step methods.** Write the method as $y_{n+1} = \Phi_h(t_n, y_n)$. Its local truncation error at $t_{n+1}$ is

$$\delta_{n+1} = y(t_{n+1}) - \Phi_h\bigl(t_n, y(t_n)\bigr),$$

where $y$ is the exact solution. The method is [consistent](/consistency/) when $\delta_{n+1} = o(h)$ uniformly in $n$, and it has order $p$ when $\|\delta_{n+1}\| \le C h^{p+1}$ for all sufficiently smooth $f$, with $C$ independent of $h$ and $n$. For a [Runge-Kutta method](/runge-kutta-methods/) the expansion of $\delta$ in powers of $h$ leads to the [Butcher order conditions](/butcher-order-conditions/). The smoothness needed is that $y \in C^{p+1}$, which holds when $f \in C^p$.

**Linear multistep methods.** For a [linear multistep method](/linear-multistep-methods/) $\sum_{j=0}^{k} \alpha_j y_{n+j} = h \sum_{j=0}^{k} \beta_j f_{n+j}$ with $\alpha_k = 1$, the local truncation error is the residual of the exact solution,

$$\delta_{n+k} = \sum_{j=0}^{k} \alpha_j\, y(t_{n+j}) - h \sum_{j=0}^{k} \beta_j\, y'(t_{n+j}).$$

Expanding each term about $t_n$ by Taylor's formula gives $\delta_{n+k} = \sum_{q \ge 0} C_q h^q y^{(q)}(t_n)$ with

$$C_0 = \sum_j \alpha_j, \qquad C_q = \sum_j \frac{j^q}{q!}\,\alpha_j - \sum_j \frac{j^{q-1}}{(q-1)!}\,\beta_j \quad (q \ge 1).$$

The method has order $p$ exactly when $C_0 = \dots = C_p = 0$ and $C_{p+1} \ne 0$. Then $\delta_{n+k} = C_{p+1} h^{p+1} y^{(p+1)}(t_n) + O(h^{p+2})$, and $C_{p+1}$ is the error constant. For an implicit method the error $y(t_{n+k}) - y_{n+k}$ of one step from exact past values differs from $\delta_{n+k}$ only by the factor $(I - h\beta_k f_y)^{-1}$, so the two agree up to $O(h^{p+2})$ (HNW I, Section III.2).

**Two conventions.** Some books, LeVeque among them, divide the residual by $h$ and call $\tau = \delta / h$ the local truncation error. Then order $p$ means $\tau = O(h^p)$, the same exponent as the global error. The two definitions describe the same thing; this site uses $\delta$, of size $O(h^{p+1})$.

**From local to global error.** The global error at $t_N$ is the sum of all local errors, each carried forward by the method to $t_N$ (the picture called Lady Windermere's fan in HNW I, Section II.3). If the step map satisfies $\|\Phi_h(t, u) - \Phi_h(t, v)\| \le (1 + h\Lambda) \|u - v\|$ and $\|\delta_{n+1}\| \le C h^{p+1}$, then induction gives

$$\|e_n\| \le C h^{p+1} \sum_{m=0}^{n-1} (1 + h\Lambda)^m \le C h^p\, \frac{e^{\Lambda (t_n - t_0)} - 1}{\Lambda}.$$

One power of $h$ is lost because about $(t_n - t_0)/h$ local errors are added. For linear multistep methods the same step needs [zero-stability](/zero-stability/), as the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/) shows.

**Partial differential equations.** For a finite difference scheme, the truncation error is the residual left when the exact solution $u(x, t)$ is put into the scheme, usually written in the form that approximates the PDE, so divided by $\Delta t$. For the [FTCS scheme](/ftcs-method/) for $u_t = \alpha u_{xx}$ it is $\tau = \frac{\Delta t}{2} u_{tt} - \frac{\alpha \Delta x^2}{12} u_{xxxx} + \ldots = O(\Delta t + \Delta x^2)$. Together with stability this gives convergence by the [Lax equivalence theorem](/lax-equivalence-theorem/).

## Examples

**Euler's method.** $\Phi_h(t, u) = u + h f(t, u)$, so Taylor's formula gives $\delta_{n+1} = y(t_n + h) - y(t_n) - h y'(t_n) = \frac{h^2}{2} y''(t_n) + O(h^3)$. Order 1. For $y' = -2ty^2$, $y(0) = 1$ and $h = 0.2$, the first step gives $y_1 = 1$ while $y(0.2) = 1/1.04$, so $\delta_1 = -0.038462$.

**Three one-step methods on $y' = -y$.** One step from $y(0) = 1$ gives $R(-h)$, and the local error is $e^{-h} - R(-h)$:

| $h$ | [Euler](/euler-method/), $1 - h$ | [Heun](/heuns-method/), $1 - h + h^2/2$ | [RK4](/classical-runge-kutta-4/) |
|---|---|---|---|
| 0.2 | $1.8731 \cdot 10^{-2}$ | $-1.2692 \cdot 10^{-3}$ | $-2.5803 \cdot 10^{-6}$ |
| 0.1 | $4.8374 \cdot 10^{-3}$ | $-1.6258 \cdot 10^{-4}$ | $-8.1964 \cdot 10^{-8}$ |
| 0.05 | $1.2294 \cdot 10^{-3}$ | $-2.0575 \cdot 10^{-5}$ | $-2.5826 \cdot 10^{-9}$ |
| 0.025 | $3.0991 \cdot 10^{-4}$ | $-2.5880 \cdot 10^{-6}$ | $-8.1042 \cdot 10^{-11}$ |

Halving $h$ divides the local errors by $3.97$, $7.95$ and $31.87$ in the last row, close to $2^2$, $2^3$ and $2^5$: local errors $O(h^{p+1})$ for $p = 1, 2, 4$. The leading terms are $h^2/2$, $-h^3/6$ and $-h^5/120$, the first omitted terms of the series of $e^{-h}$.

**Error constants of multistep methods.** With exact fractions, the formula for $C_q$ gives:

| method | $\rho(\zeta)$, $\sigma(\zeta)$ | $C_0, C_1, C_2$ | $C_3$ |
|---|---|---|---|
| [Adams-Bashforth](/adams-bashforth-methods/) 2 | $\zeta^2 - \zeta$, $\frac32\zeta - \frac12$ | $0, 0, 0$ | $\frac{5}{12}$ |
| trapezoidal ([Adams-Moulton](/adams-moulton-methods/) 1) | $\zeta - 1$, $\frac12 \zeta + \frac12$ | $0, 0, 0$ | $-\frac{1}{12}$ |
| [BDF2](/backward-differentiation-formulas/) | $\zeta^2 - \frac43 \zeta + \frac13$, $\frac23 \zeta^2$ | $0, 0, 0$ | $-\frac{2}{9}$ |
| explicit midpoint (leapfrog) | $\zeta^2 - 1$, $2\zeta$ | $0, 0, 0$ | $\frac13$ |

All four have order 2. The trapezoidal rule has the smallest error constant.

**A small local error is not enough.** The two-step method $y_{n+2} + 4y_{n+1} - 5y_n = h(4 f_{n+1} + 2 f_n)$ has order 3, the highest possible for an explicit two-step method, but $\rho(\zeta) = \zeta^2 + 4\zeta - 5$ has the root $-5$. It is not zero-stable, and its errors grow like $5^n$ (Iserles, Chapter 2; HNW I, Section III.3).

## Where it is used

- **Order conditions.** Order is defined through the local truncation error, and the [Butcher order conditions](/butcher-order-conditions/) and the conditions $C_q = 0$ above come from its Taylor expansion.
- **Convergence proofs.** Local error $O(h^{p+1})$ plus a stability property gives global error $O(h^p)$: for one-step methods by the summation above, for multistep methods by the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/), for linear PDE schemes by the [Lax equivalence theorem](/lax-equivalence-theorem/).
- **Step size control.** [Embedded Runge-Kutta pairs](/embedded-runge-kutta-pairs/) and Milne's device for predictor-corrector pairs estimate the local error of each step and choose the next $h$ from it, as in [adaptive step size control](/adaptive-step-size-control/). They control the local error per step, not the global error.
- **Modified equations.** The leading term of the truncation error of a PDE scheme gives its modified equation, which explains numerical diffusion in the [upwind scheme](/upwind-scheme/) and dispersion in the [Lax-Wendroff method](/lax-wendroff-method/).
- **Comparing methods of the same order.** The error constant, such as $|C_3|$ for the methods above, predicts which method is more accurate at the same step size.

## References
