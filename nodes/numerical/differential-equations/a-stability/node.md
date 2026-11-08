---
tag: QV5S89
kind: definition
slug: a-stability
name: A-stability
aliases:
- A-stable
- A-stable method
area: numerical/differential-equations
level: core
summary: A method is A-stable if its stability region contains the whole closed left half-plane, so that it is stable on y' = lambda y with Re lambda <= 0 for every step size h > 0.
prereqs: [absolute-stability]
see_also: [stability-region, l-stability, dahlquist-barrier, stiff-ode-problem, backward-euler-method, crank-nicolson-method, backward-differentiation-formulas, gauss-legendre-runge-kutta]
sources:
  - paper: doi:10.1007/BF01963532
    title: Germund Dahlquist, A special stability problem for linear multistep methods, BIT 3 (1963) 27-43
    locator: the definition of A-stability and the order barrier for A-stable linear multistep methods
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.3 (A-stability of implicit Runge-Kutta methods, the criterion on the imaginary axis, the E-polynomial, L-stability) and Section V.1 (A-stability and A(alpha)-stability of multistep methods)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 4, Section 4.2 (A-stability), Section 4.3 (A-stability of Runge-Kutta methods) and Section 4.4 (A-stability of multistep methods)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 3, Section 3.5 (A-stability and stiff decay)
  - paper: "Olof B. Widlund, A note on unconditionally stable linear multistep methods, BIT 7 (1967) 65-70"
    locator: the definition of A(alpha)-stability
---

A numerical method for ODEs is A-stable if its [stability region](/stability-region/) contains the closed left half-plane $\mathbb{C}^- = \{z : \operatorname{Re} z \le 0\}$. Then the method, applied to the [test equation](/dahlquist-test-equation/) $y' = \lambda y$ with $\operatorname{Re} \lambda \le 0$, gives a bounded sequence for every step size $h > 0$. Dahlquist introduced the notion in 1963 as the property that a method for [stiff problems](/stiff-ode-problem/) should have: the step size is then limited by accuracy alone, not by [absolute stability](/absolute-stability/). No explicit method is A-stable, and no linear multistep method of order above 2 is (the [Dahlquist barrier](/dahlquist-barrier/)).

## Definition

**Notation.** $z = h\lambda$, $R(z)$ is the stability function of a one-step method, and $\pi(\zeta; z) = \rho(\zeta) - z\sigma(\zeta)$ is the stability polynomial of a linear multistep method with characteristic polynomials $\rho$ and $\sigma$.

A method is **A-stable** if it is absolutely stable at every $z$ with $\operatorname{Re} z \le 0$:

- for a Runge-Kutta method, $|R(z)| \le 1$ for all $z \in \mathbb{C}^-$;
- for a linear multistep method, for each $z \in \mathbb{C}^-$ all roots of $\pi(\cdot\,; z)$ satisfy $|\zeta| \le 1$, and those of modulus 1 are simple.

For a Runge-Kutta method, $R = P/Q$ is a rational function. The following test reduces A-stability to a check on the imaginary axis.

**Proposition (Hairer and Wanner, Section IV.3).** A rational function $R$ satisfies $|R(z)| \le 1$ on $\mathbb{C}^-$ if and only if $R$ has no pole in $\operatorname{Re} z < 0$ and $|R(iy)| \le 1$ for all real $y$.

*Proof.* If $|R| \le 1$ on $\mathbb{C}^-$, then $R$ is bounded there, so it has no pole there, and in particular $|R(iy)| \le 1$. Conversely, assume the two conditions. A pole at a point $iy_0$ would make $|R(iy)|$ unbounded as $y \to y_0$, so $R$ has no pole in the closed half-plane and is analytic on an open set that contains it. Since $|R(iy)| \le 1$ as $y \to \infty$, the degree of $P$ is at most that of $Q$, so $R(z)$ has a finite limit $R(\infty)$ as $|z| \to \infty$ in any direction, and $|R(\infty)| = \lim_{y \to \infty} |R(iy)| \le 1$. Fix $\varepsilon > 0$ and choose $r$ with $|R(z)| \le 1 + \varepsilon$ for $|z| \ge r$. On the half disc $\{|z| \le r, \operatorname{Re} z \le 0\}$, the maximum modulus principle bounds $|R|$ by its maximum on the boundary, which is the segment of the imaginary axis (where $|R| \le 1$) and the half circle (where $|R| \le 1 + \varepsilon$). So $|R| \le 1 + \varepsilon$ on all of $\mathbb{C}^-$. Since $\varepsilon$ is arbitrary, $|R| \le 1$ on $\mathbb{C}^-$. $\square$

With $R = P/Q$ and real coefficients, the condition on the axis is that the **E-polynomial** $E(y) = |Q(iy)|^2 - |P(iy)|^2$ is nonnegative for all real $y$. $E$ is an even polynomial in $y$ with real coefficients, so this is a finite check.

**No explicit Runge-Kutta method is A-stable.** For an explicit method $R$ is a nonconstant polynomial (see [absolute stability](/absolute-stability/)), so $|R(z)| \to \infty$ along the negative real axis.

## Examples and non-examples

**The theta method.** $y_{n+1} = y_n + h[(1 - \theta) f_n + \theta f_{n+1}]$ has $R(z) = (1 + (1 - \theta)z)/(1 - \theta z)$. For $\theta > 0$ its only pole $1/\theta$ lies in the right half-plane, and
$$|R(iy)|^2 = \frac{1 + (1 - \theta)^2 y^2}{1 + \theta^2 y^2},$$
which is at most 1 for all $y$ if and only if $(1 - \theta)^2 \le \theta^2$, that is $\theta \ge 1/2$. So the method is A-stable exactly for $\theta \ge 1/2$: [backward Euler](/backward-euler-method/) ($\theta = 1$) and the trapezoidal rule ($\theta = 1/2$, the time step of [Crank-Nicolson](/crank-nicolson-method/)) are A-stable, and explicit Euler ($\theta = 0$) is not. At $\theta = 1/2$, $E(y) = 0$ for all $y$, so $|R(iy)| = 1$ exactly.

**Other A-stable methods.** The implicit midpoint rule ($R$ the same as the trapezoidal rule); the $s$-stage [Gauss methods](/gauss-legendre-runge-kutta/) of order $2s$, whose $R$ is the diagonal Padé approximant of $e^z$; the [Radau IIA](/radau-iia-methods/) methods of order $2s - 1$; and [BDF2](/backward-differentiation-formulas/), $\tfrac{3}{2}y_{n+2} - 2y_{n+1} + \tfrac{1}{2}y_n = hf_{n+2}$.

**Non-example: BDF3.** BDF3 has $\rho(\zeta) = \tfrac{11}{6}\zeta^3 - 3\zeta^2 + \tfrac{3}{2}\zeta - \tfrac{1}{3}$ and $\sigma(\zeta) = \zeta^3$. Its boundary locus $z(\theta) = \rho(e^{i\theta})/\sigma(e^{i\theta}) = \sum_{j=1}^{3} \tfrac{1}{j}(1 - e^{-i\theta})^j$ passes through $z = -\tfrac{1}{12} + \tfrac{3\sqrt{3}}{4} i$ at $\theta = \pi/3$, a point of the left half-plane. At the nearby point $z = -0.04 + 1.3i$ the stability polynomial has a root of modulus $1.0221$, so BDF3 is not A-stable. It is A($\alpha$)-stable with $\alpha \approx 86°$, which suffices when the stiff eigenvalues are near the negative real axis.

**Non-example: the leapfrog (explicit midpoint two-step) rule.** $y_{n+2} = y_n + 2hf_{n+1}$ has $\pi(\zeta; z) = \zeta^2 - 2z\zeta - 1$. For real $z < 0$ the roots are $z \pm \sqrt{z^2 + 1}$, and $|z - \sqrt{z^2+1}| > 1$. So it is unstable on the whole negative real axis, though it has order 2.

**A-stable but not damping.** For the trapezoidal rule at $z = -100$, $R = (1 - 50)/(1 + 50) = -0.9608$, while $e^{-100} \approx 3.7 \cdot 10^{-44}$. A stiff component of the error flips its sign in each step and decays very slowly. A-stability allows this; [L-stability](/l-stability/), which adds $R(\infty) = 0$, does not.

## Related definitions

- **[L-stability](/l-stability/).** A-stable and $\lim_{z \to \infty} R(z) = 0$. Backward Euler and Radau IIA are L-stable; the trapezoidal rule and the Gauss methods are not ($|R(\infty)| = 1$).
- **A($\alpha$)-stability** (Widlund, 1967). The stability region contains the sector $|\arg(-z)| \le \alpha$. BDF3 to BDF6 are A($\alpha$)-stable with $\alpha$ decreasing from about $86°$ to about $18°$.
- **[Dahlquist's second barrier](/dahlquist-barrier/).** An A-stable linear multistep method has order at most 2, and the trapezoidal rule has the smallest error constant among those of order 2.
- **B-stability and algebraic stability.** Nonlinear extensions: contractivity for problems with $\langle f(t,u) - f(t,v), u - v\rangle \le 0$. B-stability implies A-stability.
- **[Absolute stability](/absolute-stability/) and [stability region](/stability-region/).** A-stability is a condition on the shape of the region.

## References
