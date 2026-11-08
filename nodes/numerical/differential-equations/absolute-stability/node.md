---
tag: M98H7E
kind: definition
slug: absolute-stability
name: Absolute stability
aliases:
- linear stability
- region of absolute stability
area: numerical/differential-equations
level: core
summary: A method is absolutely stable at z = h lambda if its solution of y' = lambda y stays bounded (|R(z)| <= 1, or the root condition for multistep methods). These z form the stability region.
prereqs: [dahlquist-test-equation, ode-initial-value-problem]
see_also: [stability-region, a-stability, l-stability, zero-stability, stiff-ode-problem, euler-method, classical-runge-kutta-4, von-neumann-stability-analysis]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.2 (stability function and stability domain of explicit Runge-Kutta methods), Section IV.3 (implicit Runge-Kutta methods), Section V.1 (stability domain of multistep methods)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 4, Section 4.2 (the linear stability domain and A-stability), Sections 4.3 and 4.4 (Runge-Kutta and multistep methods)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 7 (absolute stability for ordinary differential equations, stability regions, systems of equations)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 3, Section 3.3 (absolute stability)
  - paper: doi:10.1007/BF01963532
    title: Germund Dahlquist, A special stability problem for linear multistep methods, BIT 3 (1963) 27-43
    locator: the test equation y' = lambda y and the stability of a method for a fixed step
---

Absolute stability is the property that a numerical method, applied with a fixed step $h$ to the [test equation](/dahlquist-test-equation/) $y' = \lambda y$, produces a bounded sequence $y_n$. It depends only on $z = h\lambda$, and the set of $z \in \mathbb{C}$ where it holds is the [stability region](/stability-region/) of the method. For a decaying problem ($\operatorname{Re}\lambda < 0$) a method outside its region amplifies errors from step to step, however accurate it is in theory, and this is what limits the step size of explicit methods on [stiff problems](/stiff-ode-problem/).

## Definition

**Notation.** The test equation is $y' = \lambda y$, $\lambda \in \mathbb{C}$, with step $h > 0$ and $z = h\lambda$.

**One-step methods.** A Runge-Kutta method with [Butcher tableau](/butcher-tableau/) $(A, b, c)$, applied to the test equation, gives $y_{n+1} = R(z)\, y_n$ with the **stability function**
$$R(z) = 1 + z\, b^{T}(I - zA)^{-1}\mathbf{1}, \qquad \mathbf{1} = (1, \dots, 1)^{T},$$
defined where $I - zA$ is invertible. The method is **absolutely stable at $z$** if $|R(z)| \le 1$. The **stability region** is $S = \{z \in \mathbb{C} : |R(z)| \le 1\}$.

**Linear multistep methods.** A $k$-step method with polynomials $\rho$ and $\sigma$ gives the recurrence $\sum_j (\alpha_j - z\beta_j) y_{n+j} = 0$, with the **stability polynomial** $\pi(\zeta; z) = \rho(\zeta) - z\sigma(\zeta)$. The method is absolutely stable at $z$ if every root $\zeta$ of $\pi(\cdot\,; z)$ has $|\zeta| \le 1$, and each root with $|\zeta| = 1$ is simple. This is exactly the condition that every solution of the recurrence is bounded, for every choice of starting values.

**Conventions.** Hairer and Wanner use the closed set $|R(z)| \le 1$, as here. Iserles and LeVeque define the region by $y_n \to 0$ for all starting values, which is $|R(z)| < 1$ for one-step methods. The two sets differ only on the boundary curve. Absolute stability is a statement for a fixed $h$; [zero-stability](/zero-stability/) is the case $z = 0$, the limit $h \to 0$.

**Systems.** For $y' = My$ with a diagonalizable matrix $M = V\Lambda V^{-1}$, a Runge-Kutta step gives $y_{n+1} = R(hM) y_n$, and $R(hM) = V R(h\Lambda) V^{-1}$. If $h\lambda_i \in S$ for each eigenvalue $\lambda_i$, then $\|y_n\| \le \kappa(V)\|y_0\|$ for all $n$, with $\kappa(V) = \|V\|\|V^{-1}\|$. For a strongly non-normal $M$, $\kappa(V)$ can be huge, and transient growth is possible even when all $h\lambda_i \in S$. For a nonlinear problem the eigenvalues of the Jacobian $\partial f/\partial y$ play the role of $\lambda$; this is a local guide, not a theorem.

**Two facts.**

1. *An explicit Runge-Kutta method has a bounded stability region.* If $A$ is strictly lower triangular, $A$ is nilpotent ($A^s = 0$), so $(I - zA)^{-1} = \sum_{k=0}^{s-1} z^k A^k$ and $R$ is a polynomial of degree at most $s$. It is not constant, because consistency gives $R(z) = 1 + z\sum_i b_i + O(z^2) = 1 + z + O(z^2)$. A nonconstant polynomial tends to infinity, so $|R(z)| > 1$ for $|z|$ large and $S$ is bounded.
2. *For $p = s \le 4$, $R$ is the Taylor polynomial of $e^z$.* One step from $y_0 = 1$ on $y' = \lambda y$ gives $R(h\lambda)$, while the exact value is $e^{h\lambda}$. For a method of order $p$ the difference is $O(h^{p+1})$ for each fixed $\lambda$, so $R(z) = e^z + O(z^{p+1})$ as $z \to 0$. A polynomial of degree at most $s = p$ that agrees with $e^z$ to order $p$ is $\sum_{k=0}^{p} z^k/k!$. So every explicit 4-stage method of order 4 has the same region as [RK4](/classical-runge-kutta-4/).

## Examples and non-examples

| method | $R(z)$ or $\pi(\zeta; z)$ | real interval in $S$ | imaginary interval in $S$ |
|---|---|---|---|
| explicit [Euler](/euler-method/) | $1 + z$ | $[-2, 0]$ | $\{0\}$ only |
| 3-stage order 3 | $1 + z + z^2/2 + z^3/6$ | $[-2.5127, 0]$ | $[-\sqrt{3}, \sqrt{3}]i$ |
| [RK4](/classical-runge-kutta-4/) | $1 + z + z^2/2 + z^3/6 + z^4/24$ | $[-2.7853, 0]$ | $[-2\sqrt{2}, 2\sqrt{2}]i$ |
| [backward Euler](/backward-euler-method/) | $1/(1 - z)$ | $(-\infty, 0]$ | all |
| trapezoidal rule | $(1 + z/2)/(1 - z/2)$ | $(-\infty, 0]$ | all |
| [Adams-Bashforth](/adams-bashforth-methods/) 2 | $\zeta^2 - (1 + \tfrac{3}{2}z)\zeta + \tfrac{1}{2}z$ | $[-1, 0]$ | $\{0\}$ only |

For explicit Euler, $S$ is the closed disc of radius 1 centered at $-1$. For the trapezoidal rule, $|R(z)| \le 1$ exactly when $|1 + z/2| \le |1 - z/2|$, which is $\operatorname{Re} z \le 0$; so $S$ is the closed left half-plane and the method is [A-stable](/a-stability/). For AB2 at $z = -1$, $\pi(\zeta; -1) = \zeta^2 + \tfrac{1}{2}\zeta - \tfrac{1}{2} = (\zeta + 1)(\zeta - \tfrac{1}{2})$, so $z = -1$ is on the boundary.

**A step size limit.** For $y' = -100y$, explicit Euler is absolutely stable only for $h \le 0.02$ and RK4 only for $h \le 0.027853$. At $h = 0.03$, $z = -3$: Euler multiplies the error by $-2$ in each step, and RK4 by $R(-3) = 1.375$, so both blow up, while the true solution decays by the factor $e^{-3} = 0.0498$ per step.

**Sample points.** At $z = -1.5$: $|1 + z| = 0.5$ and $|R_{\mathrm{RK4}}(z)| = 0.2734$, both stable. At $z = -0.5 + i$: $|1 + z| = 1.118$, so explicit Euler is unstable there, while $|R_{\mathrm{RK4}}(z)| = 0.6198$. At $z = -2.5$: Euler gives 1.5 (unstable) and RK4 gives 0.6484 (stable). At $z = -2.9$, RK4 gives 1.1872 (unstable).

**Non-example: a stable method that is not accurate.** Backward Euler at $z = -2.5$ has $R = 0.2857$, while $e^{-2.5} = 0.0821$. Absolute stability says nothing about accuracy; it only says that errors do not grow.

**Non-example: growth that is correct.** For $\operatorname{Re}\lambda > 0$ the exact solution grows, and a method that is not absolutely stable there is doing the right thing. Absolute stability is a useful requirement only where the problem itself is stable.

## Related definitions

- **[Stability region](/stability-region/).** The set $S$ itself, usually drawn in the complex plane.
- **[A-stability](/a-stability/).** $S$ contains the whole left half-plane $\operatorname{Re} z \le 0$.
- **[L-stability](/l-stability/).** A-stability and $R(z) \to 0$ as $z \to \infty$.
- **[Zero-stability](/zero-stability/).** Absolute stability at $z = 0$ for a multistep method; it is the root condition on $\rho$.
- **[Stiff problems](/stiff-ode-problem/).** Problems where the absolute stability of explicit methods, not accuracy, decides the step size.
- **[Von Neumann stability analysis](/von-neumann-stability-analysis/).** The same idea for a PDE scheme: each Fourier mode is a test equation, and the amplification factor plays the role of $R(z)$.

## References
