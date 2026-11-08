---
tag: EY1FXX
kind: definition
slug: dahlquist-test-equation
name: Dahlquist test equation
aliases:
- y' = lambda y test equation
- linear test equation
- scalar test equation
area: numerical/differential-equations
level: core
summary: "The scalar linear problem y' = λ y with complex λ. A method applied to it gives y_(n+1) = R(z) y_n with z = h λ, and R decides the linear stability of the method."
prereqs: [ode-initial-value-problem, euler-method]
see_also: [stability-region, absolute-stability, a-stability, l-stability, stiff-ode-problem, zero-stability, butcher-tableau, linear-multistep-methods]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.2 (stability functions of explicit Runge-Kutta methods), Section IV.3 (stability function of implicit Runge-Kutta methods, A-stability), Section V.1 (stability of multistep methods on the test equation)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 4 (stiff equations; the linear stability domain and A-stability, Section 4.2)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 7 (absolute stability for ordinary differential equations; the test problem, stability regions, systems and the diagonalization argument)
  - paper: doi:10.1007/BF01963532
    title: Germund Dahlquist, A special stability problem for linear multistep methods, BIT 3 (1963) 27-43
    locator: the test equation y' = λ y and the definition of A-stability
---

The Dahlquist test equation is the scalar linear [initial value problem](/ode-initial-value-problem/) $y' = \lambda y$, $y(0) = y_0$, with a complex constant $\lambda$. It is the model on which the linear stability of a numerical method is defined: a one-step method applied to it with step $h$ gives $y_{n+1} = R(z)\, y_n$ with $z = h\lambda$, and the function $R$ is the stability function of the method. Dahlquist used it in 1963 to define [A-stability](/a-stability/).

## Definition

The **test equation** is

$$y' = \lambda y, \qquad y(t_0) = y_0, \qquad \lambda \in \mathbb{C},$$

with exact solution $y(t) = e^{\lambda(t - t_0)} y_0$. Over one step of length $h$ the exact solution is multiplied by $e^{z}$, where $z = h\lambda$. It decays when $\operatorname{Re}\lambda < 0$ and oscillates without growth when $\lambda$ is imaginary.

**Stability function of a one-step method.** A method is applied with a constant step $h$. If for every $\lambda$ and $y_0$ the numbers it produces satisfy $y_{n+1} = R(z)\, y_n$ for a function $R$ that depends only on $z = h\lambda$, then $R$ is the **stability function** of the method. For a Runge-Kutta method with [Butcher tableau](/butcher-tableau/) $(A, b, c)$ and $s$ stages, the stages are $Y = y_n \mathbf{1} + zA Y$, so

$$R(z) = 1 + z\, b^{T}(I - zA)^{-1}\mathbf{1} = \frac{\det(I - zA + z\mathbf{1}b^{T})}{\det(I - zA)},$$

where $\mathbf{1} = (1, \ldots, 1)^T$. $R$ is a rational function, and a polynomial of degree at most $s$ when the method is explicit ($A$ strictly lower triangular). The second form follows from $\det(M + uv^T) = \det(M)(1 + v^T M^{-1} u)$ with $M = I - zA$, $u = z\mathbf{1}$, $v = b$.

**Multistep methods.** A [linear multistep method](/linear-multistep-methods/) $\sum_{j=0}^{k}\alpha_j y_{n+j} = h\sum_{j=0}^{k}\beta_j f_{n+j}$ with $\rho(\zeta) = \sum \alpha_j\zeta^j$ and $\sigma(\zeta) = \sum\beta_j\zeta^j$, applied to the test equation, gives the linear recurrence $\sum_j(\alpha_j - z\beta_j)y_{n+j} = 0$. Its behaviour is governed by the roots $\zeta_1(z), \ldots, \zeta_k(z)$ of the **stability polynomial** $\pi(\zeta; z) = \rho(\zeta) - z\sigma(\zeta)$. All solutions stay bounded iff every root has $|\zeta_i| \le 1$ and the roots with $|\zeta_i| = 1$ are simple.

**Derived notions.** The set $S = \{z \in \mathbb{C} : |R(z)| \le 1\}$ is the [stability region](/stability-region/) (the region of [absolute stability](/absolute-stability/)). The method is A-stable if $S$ contains the closed left half-plane $\operatorname{Re} z \le 0$, and [L-stable](/l-stability/) if moreover $R(z) \to 0$ as $z \to \infty$. Taking $\lambda = 0$ gives $y' = 0$, on which the condition becomes [zero-stability](/zero-stability/) for multistep methods.

**Why one scalar equation is enough for linear systems.** Let $y' = Jy$ with a diagonalizable matrix $J = V\Lambda V^{-1}$, $\Lambda = \operatorname{diag}(\lambda_1, \ldots, \lambda_d)$. A Runge-Kutta method applied to it gives $y_{n+1} = R(hJ)y_n$, with $R(hJ) = V\operatorname{diag}(R(h\lambda_1), \ldots, R(h\lambda_d))V^{-1}$. *Proof.* The stage equations are linear in $y$, so the method commutes with the change of variables $w = V^{-1}y$: in the new variables the system is $w_i' = \lambda_i w_i$ for each $i$ separately, and the same method gives $w_{i, n+1} = R(h\lambda_i)w_{i,n}$. Hence the numerical solution of the system is bounded for all $n$ iff $h\lambda_i \in S$ for each eigenvalue, up to the factor $\|V\|\,\|V^{-1}\|$, the condition number of $V$. $\square$

## Examples and non-examples

**Stability functions of standard methods.** Each line is the factor of one step. A method of order $p$ satisfies $R(z) = e^z + O(z^{p+1})$ as $z \to 0$.

| method | $R(z)$ | $R(-1)$ | $R(-2)$ | $R(-3)$ | $R(-10)$ |
|---|---|---|---|---|---|
| exact, $e^z$ | $e^z$ | 0.3679 | 0.1353 | 0.0498 | $4.5 \cdot 10^{-5}$ |
| [Euler](/euler-method/) | $1 + z$ | 0 | $-1$ | $-2$ | $-9$ |
| [explicit midpoint](/explicit-midpoint-method/) | $1 + z + z^2/2$ | 1/2 | 1 | 5/2 | 41 |
| [classical RK4](/classical-runge-kutta-4/) | $\sum_{k=0}^{4} z^k/k!$ | 3/8 | 1/3 | 11/8 | 291 |
| [backward Euler](/backward-euler-method/) | $1/(1 - z)$ | 1/2 | 1/3 | 1/4 | 1/11 |
| trapezoidal rule | $(1 + z/2)/(1 - z/2)$ | 1/3 | 0 | $-1/5$ | $-2/3$ |

On $y' = -2y$ with $h = 1$ ($z = -2$), Euler's numbers alternate $1, -1, 1, \ldots$, the midpoint method stays at $1$, and RK4 decays like $(1/3)^n$. On $y' = -10y$ with $h = 1$, all three explicit methods blow up while the solution decays to $4.5 \cdot 10^{-5}$ after one unit of time. The real stability interval of RK4 is $[-2.7853, 0]$. Backward Euler damps every decaying mode, and $R(-10) = 1/11$. The trapezoidal rule is A-stable, but $R(-10) = -2/3$ and $R(z) \to -1$ as $z \to -\infty$, so stiff components decay slowly with alternating sign: it is not L-stable.

**A multistep example.** The two-step Adams-Bashforth method has $\rho(\zeta) = \zeta^2 - \zeta$ and $\sigma(\zeta) = \tfrac32\zeta - \tfrac12$. At $z = -1$ the stability polynomial is $\zeta^2 + \tfrac12\zeta - \tfrac12 = (\zeta + 1)(\zeta - \tfrac12)$: one root lies on the unit circle, so $z = -1$ is the left end of its real stability interval $[-1, 0]$.

**Non-example: a non-normal matrix.** For $y' = Jy$ with $J = \begin{pmatrix}-1 & 100 \\ 0 & -2\end{pmatrix}$, both eigenvalues are negative, and $h\lambda_i \in S$ means that $y_n \to 0$. But $V$ is badly conditioned, and the factor $\|V\|\,\|V^{-1}\|$ in the argument above is large: the exact solution and the numbers both grow by a large factor before they decay. The test equation predicts the limit, not the transient size.

**Non-example: a nonlinear problem.** Applying the test equation to $y' = f(t, y)$ with $\lambda$ an eigenvalue of the Jacobian $f_y$ at one point is a heuristic, not a theorem. The Jacobian changes along the solution, and a frozen-coefficient analysis can miss instabilities. Nonlinear stability notions such as B-stability (HW II, Section IV.12) replace it there.

**Non-example: the test equation with variable coefficient.** For $y' = \lambda(t)y$, a Runge-Kutta method still gives $y_{n+1} = r_n y_n$, but $r_n$ depends on $h$, $t_n$ and the values of $\lambda$ at the stage times, not on one number $z$, so it does not define a stability function.

## Related definitions

- [Stability region](/stability-region/): the set where $|R(z)| \le 1$.
- [Absolute stability](/absolute-stability/): $h\lambda$ lies in the stability region.
- [A-stability](/a-stability/) and [L-stability](/l-stability/): the left half-plane lies in the region, and $R(\infty) = 0$.
- [Zero-stability](/zero-stability/): the case $z = 0$ for multistep methods, the root condition on $\rho$.
- [Stiff problems](/stiff-ode-problem/): problems where $h\lambda$ is far out in the left half-plane for some eigenvalue, so that the stability function, not the accuracy, limits the step.
- [Von Neumann stability analysis](/von-neumann-stability-analysis/): the analogue for difference schemes for PDEs, where each Fourier mode plays the role of one eigenvalue.

## References
