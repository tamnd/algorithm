---
tag: DS2ESK
kind: definition
slug: consistency
name: Consistency of a numerical method
aliases:
- consistent method
- consistency condition
area: numerical/differential-equations
level: core
summary: A method is consistent when its local truncation error, the defect left when the exact solution is put into one step, is o(h). For multistep methods this means rho(1) = 0 and rho'(1) = sigma(1).
prereqs: [ode-initial-value-problem, local-truncation-error]
see_also: [zero-stability, order-of-accuracy, dahlquist-equivalence-theorem, lax-equivalence-theorem, global-error, linear-multistep-methods, butcher-tableau, butcher-order-conditions]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.3 (local error and convergence of one-step methods), Section III.2 (order of multistep methods, the conditions on rho and sigma), Sections III.3 and III.4 (stability and convergence)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 2, Section 2.2 (order and convergence of multistep methods)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (local truncation error of methods for initial value problems, defined with a division by the time step) and Chapter 6 (zero-stability and convergence)
  - paper: "Germund Dahlquist, Convergence and stability in the numerical integration of ordinary differential equations, Mathematica Scandinavica 4 (1956) 33-53"
    locator: consistency, stability and the equivalence with convergence for linear multistep methods
---

A numerical method for $y' = f(t, y)$ is consistent when the exact solution satisfies the method up to a defect that is small compared with the step size $h$: the [local truncation error](/local-truncation-error/) of one step is $o(h)$ as $h \to 0$. Consistency says that the method approximates the right differential equation. It does not by itself make the method converge: a consistent method must also be [zero-stable](/zero-stability/), and the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/) (for multistep methods) and the [Lax equivalence theorem](/lax-equivalence-theorem/) (for linear PDE schemes) say that the two together are exactly what convergence needs.

## Definition

**Notation.** The problem is the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, on $[t_0, T]$, with a solution $y \in C^1$. The step is $h$, the grid is $t_n = t_0 + nh$, and $y_n \approx y(t_n)$.

**One-step methods.** A one-step method has the form $y_{n+1} = y_n + h\,\Phi(t_n, y_n, h)$ with an increment function $\Phi$. Its local truncation error at $t_{n+1}$ is
$$\tau_{n+1} = y(t_{n+1}) - y(t_n) - h\,\Phi(t_n, y(t_n), h).$$
The method is **consistent** if $\max_n \|\tau_{n+1}\| / h \to 0$ as $h \to 0$ for each problem with $f$ continuous and Lipschitz in $y$. It has **order** $p$ if $\tau_{n+1} = O(h^{p+1})$ for each $f$ smooth enough. When $\Phi$ is continuous in all its arguments, consistency is equivalent to
$$\Phi(t, y, 0) = f(t, y) \quad \text{for all } t, y.$$
For a [Runge-Kutta method](/runge-kutta-methods/) with [Butcher tableau](/butcher-tableau/) $(A, b, c)$, $\Phi(t, y, 0) = (\sum_i b_i) f(t, y)$, so it is consistent if and only if $\sum_{i=1}^s b_i = 1$.

**Linear multistep methods.** A $k$-step method $\sum_{j=0}^{k} \alpha_j y_{n+j} = h \sum_{j=0}^{k} \beta_j f(t_{n+j}, y_{n+j})$, with $\alpha_k \ne 0$, has the characteristic polynomials $\rho(\zeta) = \sum_j \alpha_j \zeta^j$ and $\sigma(\zeta) = \sum_j \beta_j \zeta^j$. Its local truncation error is $\tau_{n+k} = \sum_j \alpha_j y(t_{n+j}) - h\sum_j \beta_j y'(t_{n+j})$. It is consistent if
$$\rho(1) = 0 \quad \text{and} \quad \rho'(1) = \sigma(1).$$

*Why these two conditions.* Expand each term at $t_n$ for $y \in C^{2}$: $\tau_{n+k} = C_0\, y(t_n) + C_1\, h\, y'(t_n) + O(h^2)$, with $C_0 = \sum_j \alpha_j = \rho(1)$ and $C_1 = \sum_j j\alpha_j - \sum_j \beta_j = \rho'(1) - \sigma(1)$. If $C_0 = C_1 = 0$ then $\tau = O(h^2)$. Conversely, the problem $y' = 0$, $y = 1$ gives $\tau = C_0$, which is not $o(h)$ unless $C_0 = 0$; and then $y' = 1$, $y = t$ gives $\tau = C_1 h$, which is not $o(h)$ unless $C_1 = 0$. More generally, with $C_q = \sum_j \frac{j^q}{q!}\alpha_j - \sum_j \frac{j^{q-1}}{(q-1)!}\beta_j$, the method has order $p$ if and only if $C_0 = \dots = C_p = 0$ (Hairer, Nørsett and Wanner, Section III.2).

**Conventions.** These pages use the defect of one step, as above. LeVeque divides it by $h$, so his $\tau$ is $O(h^p)$ for a method of order $p$ and consistency reads $\tau \to 0$. The two definitions give the same notion of consistency and order.

**PDE schemes.** A finite difference scheme for a PDE in $u(x, t)$ is consistent if its truncation error, the defect when the exact solution is put into the scheme and divided by $\Delta t$, tends to 0 in the chosen norm as $\Delta x, \Delta t \to 0$ along the refinement path (for example with the [Courant number](/courant-friedrichs-lewy-condition/) fixed).

## Examples and non-examples

- **Euler method.** $\Phi = f(t, y)$, so $\Phi(t, y, 0) = f$. Consistent, with $\tau = \tfrac{h^2}{2}y'' + O(h^3)$, order 1.
- **[Classical Runge-Kutta](/classical-runge-kutta-4/).** $b = (1/6, 1/3, 1/3, 1/6)$ sums to 1. Consistent, order 4.
- **Two-step Adams-Bashforth.** $\rho(\zeta) = \zeta^2 - \zeta$, $\sigma(\zeta) = \tfrac{3}{2}\zeta - \tfrac{1}{2}$. Then $\rho(1) = 0$ and $\rho'(1) = 1 = \sigma(1)$. Consistent, order 2.
- **Non-example: wrong scaling.** $y_{n+1} = y_n + 2h f(t_n, y_n)$ has $\Phi(t, y, 0) = 2f$. On $y' = y$, $y(0) = 1$, it gives $y_N(1) = (1 + 2h)^{1/h}$, which is $6.1917$, $7.2446$ and $7.3743$ for $h = 0.1, 0.01, 0.001$. It converges, but to $e^2 = 7.3891$, the solution of $y' = 2y$, not to $e = 2.71828$.
- **Consistent but not convergent.** The explicit two-step method $y_{n+2} + 4y_{n+1} - 5y_n = h(4f_{n+1} + 2f_n)$ has $\rho(\zeta) = \zeta^2 + 4\zeta - 5$ and $\sigma(\zeta) = 4\zeta + 2$. Here $\rho(1) = 0$ and $\rho'(1) = 6 = \sigma(1)$. Its constants are $C_0 = \dots = C_3 = 0$ and $C_4 = 1/6$, so it is consistent of order 3, the highest order of any explicit two-step method. But $\rho$ has the root $-5$, so the method is not zero-stable. On $y' = -y$, $y(0) = 1$, with the exact value at $t_1$, the error at $t = 1$ is $7.05$ for $h = 0.1$, $4.65 \cdot 10^6$ for $h = 0.05$, $2.88 \cdot 10^{19}$ for $h = 0.025$ and $1.67 \cdot 10^{46}$ for $h = 0.0125$. Smaller steps make it worse.
- **Non-example: consistency in the wrong sense.** A method whose defect is $O(h)$ but not $o(h)$ is not consistent, even though its defect tends to 0. Over the $N = (T - t_0)/h$ steps these defects add up to a quantity of order 1.

## Related definitions

- **[Local truncation error](/local-truncation-error/)** and **[order of accuracy](/order-of-accuracy/).** Consistency is order at least 1. The order is the largest $p$ with $\tau = O(h^{p+1})$.
- **[Zero-stability](/zero-stability/).** All roots of $\rho$ lie in the closed unit disc, and those on the circle are simple. Every one-step method satisfies it when $\Phi$ is Lipschitz in $y$.
- **Convergence and the [global error](/global-error/).** A method converges if $\max_n \|y(t_n) - y_n\| \to 0$ as $h \to 0$, whenever the starting values converge. For a one-step method with $\Phi$ Lipschitz in $y$, consistency implies convergence, and order $p$ gives a global error $O(h^p)$ (Hairer, Nørsett and Wanner, Section II.3). For a linear multistep method, convergence holds if and only if the method is consistent and zero-stable (Dahlquist 1956).
- **[Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/)** and **[Lax equivalence theorem](/lax-equivalence-theorem/).** Consistency plus stability is equivalent to convergence, for multistep methods and for linear well-posed PDE problems respectively.
- **[Butcher order conditions](/butcher-order-conditions/).** The conditions on a Runge-Kutta tableau for order $p$. Consistency is the first of them, $\sum_i b_i = 1$.

## References
