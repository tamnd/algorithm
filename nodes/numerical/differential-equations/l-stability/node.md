---
tag: 430VQD
kind: definition
slug: l-stability
name: L-stability
aliases:
- L-stable
- L-stable method
- stiff decay
area: numerical/differential-equations
level: advanced
summary: "A one-step method is L-stable if it is A-stable and its stability function satisfies R(z) -> 0 as z -> infinity, so very stiff components are damped in one step."
prereqs: [a-stability, dahlquist-test-equation]
see_also: [stiff-ode-problem, backward-euler-method, radau-iia-methods, backward-differentiation-formulas, crank-nicolson-method, gauss-legendre-runge-kutta, implicit-runge-kutta-methods, rosenbrock-methods]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.3 (stability function, A-stability, L-stability, stiffly accurate methods) and Section IV.4 (Padé approximations to the exponential and their A- and L-stability)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 3, Section 3.5 (A-stability and stiff decay)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 8 (stiff ordinary differential equations, A-stability and L-stability)
  - paper: "Byron L. Ehle, On Padé approximations to the exponential function and A-stable methods for the numerical solution of initial value problems, Research Report CSRR 2010, University of Waterloo, 1969"
    locator: the introduction of L-stability
---

L-stability strengthens [A-stability](/a-stability/) for [stiff problems](/stiff-ode-problem/). An A-stable method keeps the numerical solution of $y' = \lambda y$ bounded for every $\operatorname{Re}\lambda \le 0$ and every step size, but it may damp the fast components only very weakly when $h|\lambda|$ is large. An L-stable method damps them almost completely in one step, as the exact solution does. [Backward Euler](/backward-euler-method/) and the [Radau IIA methods](/radau-iia-methods/) are L-stable; the trapezoidal rule and the [Gauss methods](/gauss-legendre-runge-kutta/) are A-stable but not L-stable.

## Definition

**Notation.** A one-step method applied to the [Dahlquist test equation](/dahlquist-test-equation/) $y' = \lambda y$ with step $h$ gives $y_{n+1} = R(z)\, y_n$ with $z = h\lambda$. For a Runge-Kutta method with Butcher tableau $(A, b, c)$ and $s$ stages, $R(z) = 1 + z\, b^{T}(I - zA)^{-1}\mathbb{1}$, a rational function. The method is A-stable if $|R(z)| \le 1$ for all $\operatorname{Re} z \le 0$.

**Definition (L-stability, HW II, Section IV.3).** A one-step method is L-stable if it is A-stable and

$$\lim_{z \to \infty} R(z) = 0.$$

Since $R$ is rational, the limit is the same along every direction, so it is enough to take $z \to -\infty$ along the real axis.

**Why it matters.** For $y' = \lambda (y - g(t)) + g'(t)$ with $\operatorname{Re}\lambda \ll 0$, every solution approaches $g(t)$ within a time of order $1/|\lambda|$. A method with step $h \gg 1/|\lambda|$ multiplies the distance to $g$ by about $R(h\lambda) \approx R(\infty)$ per step. If $|R(\infty)| = 1$, an initial transient that the exact solution kills at once survives for many steps, often with a sign change at each step. If $R(\infty) = 0$, it is gone after one step.

**A sufficient condition (HW II, Section IV.3).** If $A$ is nonsingular, then $R(\infty) = 1 - b^{T}A^{-1}\mathbb{1}$. If the method is stiffly accurate, that is $a_{sj} = b_j$ for all $j$ (the last row of $A$ equals $b^T$), then $b^{T}A^{-1} = e_s^{T}$ and $R(\infty) = 1 - 1 = 0$. So an A-stable, stiffly accurate method with nonsingular $A$ is L-stable.

**Multistep methods.** For a [linear multistep method](/linear-multistep-methods/) with polynomials $\rho$ and $\sigma$, the analogue asks that the method be A-stable and that all roots of $\rho(\zeta) - z\sigma(\zeta)$ tend to $0$ as $z \to \infty$, which means $\sigma(\zeta) = \beta_k \zeta^k$. This is what [BDF](/backward-differentiation-formulas/) methods do. Ascher and Petzold call this property stiff decay and do not require A-stability for it.

## Examples and non-examples

**Values of $R(z)$ on the negative real axis.** Computed in double precision:

| method | $R(z)$ | $z = -1$ | $z = -10$ | $z = -100$ | $z = -10^6$ | L-stable |
|---|---|---|---|---|---|---|
| backward Euler | $\frac{1}{1 - z}$ | $0.5$ | $0.0909$ | $0.0099$ | $1.0 \cdot 10^{-6}$ | yes |
| trapezoidal rule | $\frac{1 + z/2}{1 - z/2}$ | $0.3333$ | $-0.6667$ | $-0.9608$ | $-0.999996$ | no |
| 2-stage Gauss | $\frac{1 + z/2 + z^2/12}{1 - z/2 + z^2/12}$ | $0.3684$ | $0.3023$ | $0.8869$ | $0.999988$ | no |
| 2-stage Radau IIA | $\frac{1 + z/3}{1 - 2z/3 + z^2/6}$ | $0.3636$ | $-0.0959$ | $-0.0186$ | $-2.0 \cdot 10^{-6}$ | yes |
| SDIRK2, $\gamma = 1 - \frac{\sqrt 2}{2}$ | $\frac{1 + (1 - 2\gamma) z}{(1 - \gamma z)^2}$ | $0.3504$ | $-0.2036$ | $-0.0441$ | $-4.8 \cdot 10^{-6}$ | yes |

The exact factor is $e^{z}$, which is $0.3679$ at $z = -1$ and below $10^{-4}$ at $z = -10$. All five methods are A-stable. For the trapezoidal rule and the Gauss methods $|R(\infty)| = 1$; for the other three $R(\infty) = 0$.

- **Backward Euler.** $s = 1$, $A = (1)$, $b = (1)$: stiffly accurate, so $R(\infty) = 0$. L-stable, order 1.
- **Radau IIA.** The $s$-stage Radau IIA method has order $2s - 1$ and is stiffly accurate. For $s = 2$, $A = \begin{pmatrix} 5/12 & -1/12 \\ 3/4 & 1/4 \end{pmatrix}$ and $b = (3/4, 1/4)$; the exact computation $1 - b^{T}A^{-1}\mathbb{1}$ with fractions gives $0$.
- **SDIRK2.** The two-stage singly diagonally implicit method with $A = \begin{pmatrix} \gamma & 0 \\ 1 - \gamma & \gamma \end{pmatrix}$, $b = (1 - \gamma, \gamma)$ is stiffly accurate, so $R(\infty) = 0$, for every $\gamma$. It has order 2 when $\gamma^2 - 2\gamma + \frac12 = 0$, that is $\gamma = 1 \pm \frac{\sqrt 2}{2}$, and both choices are A-stable.
- **Non-example: the trapezoidal rule.** It is A-stable with $R(\infty) = -1$. On $y' = -10^6 (y - \cos t) - \sin t$, $y(0) = 0$, whose solution is $\cos t - e^{-10^6 t}$, the errors at $T = 1$ with $N = 10, 20, 40, 80$ steps are $-0.9996$, $-0.9984$, $-0.9936$, $-0.9747$: the initial jump of size 1 is never damped. Backward Euler on the same problem gives $-2.84 \cdot 10^{-8}$, $-1.39 \cdot 10^{-8}$, $-6.84 \cdot 10^{-9}$, $-3.40 \cdot 10^{-9}$.
- **Non-example: Gauss methods.** Their $R$ is the diagonal Padé approximation of $e^z$, with $|R(iy)| = 1$ and $R(\infty) = (-1)^s$. They are A-stable and of the highest possible order $2s$, but not L-stable.
- **Non-example: explicit methods.** For an explicit Runge-Kutta method $R$ is a polynomial, so $|R(z)| \to \infty$ as $z \to -\infty$. No explicit method is A-stable, let alone L-stable.
- **Padé approximations.** The Padé approximation $R_{k,j}$ to $e^z$ with numerator degree $k$ and denominator degree $j$ is A-stable exactly when $k \le j \le k + 2$, and then it is L-stable exactly when $j = k + 1$ or $j = k + 2$ (HW II, Section IV.4). The Radau IIA functions are $R_{s-1,s}$.
- **BDF.** BDF1 (backward Euler) and BDF2 are A-stable and have stiff decay. BDF3 to BDF6 have stiff decay but are only A($\alpha$)-stable, which is called L($\alpha$)-stability.

## Related definitions

- **[A-stability](/a-stability/).** $|R(z)| \le 1$ on the closed left half-plane. L-stability is A-stability plus $R(\infty) = 0$.
- **Strong A-stability.** A-stable with $|R(\infty)| < 1$. This lies between A- and L-stability; the [Crank-Nicolson method](/crank-nicolson-method/) fails it.
- **L($\alpha$)-stability.** A($\alpha$)-stability, that is stability in the sector $|\arg(-z)| \le \alpha$, plus $R(\infty) = 0$.
- **Stiff accuracy.** $a_{sj} = b_j$: the last stage is the new value. Together with A-stability it gives L-stability, and it also avoids part of the order reduction on stiff problems and on differential-algebraic equations.
- **B-stability and algebraic stability.** Nonlinear analogues of A-stability, defined by contractivity for problems with a one-sided [Lipschitz condition](/lipschitz-condition/) $\langle f(t, u) - f(t, v), u - v \rangle \le 0$.
- **[Stability region](/stability-region/).** The set $\{z : |R(z)| \le 1\}$; A- and L-stability are statements about it and about the behaviour of $R$ at infinity.

## References
