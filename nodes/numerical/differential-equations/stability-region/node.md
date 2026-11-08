---
tag: JG56PN
kind: concept
slug: stability-region
name: Stability region
aliases:
- absolute stability region
- region of absolute stability
- stability domain
area: numerical/differential-equations
level: core
summary: "The set S of z = hλ in the complex plane for which a method applied to y' = λy gives bounded iterates: |R(z)| <= 1 for one-step methods, the root condition for ρ - zσ for multistep methods."
prereqs: [dahlquist-test-equation, absolute-stability]
see_also: [a-stability, l-stability, stiff-ode-problem, runge-kutta-methods, linear-multistep-methods, backward-differentiation-formulas, zero-stability, von-neumann-stability-analysis]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.2 (stability analysis for explicit Runge-Kutta methods, stability domains), Section IV.3 (stability function of implicit methods, A-stability), Section V.1 (stability of multistep methods, the root locus curve)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 7 (absolute stability for ODEs; regions for one-step and multistep methods, the boundary locus method, stiffness)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 4 (stiff equations; linear stability domains of Runge-Kutta and multistep methods, A-stability)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Section 3.3 (absolute stability), Section 4.4 (absolute stability of Runge-Kutta methods), Section 5.2 (absolute stability of multistep methods)
---

The stability region of a numerical method for $y' = f(t, y)$ is the set $S \subset \mathbb{C}$ of values $z = h\lambda$ for which the method, applied to the [test equation](/dahlquist-test-equation/) $y' = \lambda y$ with step size $h$, produces iterates that do not grow. It turns the question "is this step size small enough?" into the geometric question "do all the scaled eigenvalues $h\lambda$ lie in $S$?". Its shape tells explicit from implicit methods, and it is the tool for choosing a method and a step size for [stiff problems](/stiff-ode-problem/).

## In plain words

Many problems contain parts that die out quickly, like a hot object cooling to room temperature. The exact solution of such a part shrinks. A numerical method should make it shrink too, or at least not make it grow. Whether it does depends only on the product of the step size and the decay rate.

The stability region is the map of all products for which the method behaves. A method with a small region forces small steps whenever some part of the problem decays fast, even if that part has long since vanished and does not matter for accuracy. A method whose region covers the whole left half of the map can take steps as large as accuracy allows.

## The idea

**One-step methods.** A Runge-Kutta method with Butcher tableau $(A, b, c)$, applied to $y' = \lambda y$, gives $y_{n+1} = R(z) y_n$ with $z = h\lambda$ and the stability function
$$R(z) = 1 + z b^T (I - zA)^{-1} \mathbf{1}.$$
The stability region is $S = \{z \in \mathbb{C} : |R(z)| \le 1\}$. For an explicit method $A$ is strictly lower triangular, so $R$ is a polynomial of degree at most $s$; for an implicit method it is a rational function. If the method has order $p$, then $R(z) = e^z + O(z^{p+1})$, so for explicit methods with $p = s \le 4$, $R(z) = \sum_{k=0}^{s} z^k / k!$.

**Linear multistep methods.** A method with characteristic polynomials $\rho$ and $\sigma$, applied to $y' = \lambda y$, gives the linear recurrence $\sum_j (\alpha_j - z\beta_j) y_{n+j} = 0$. Its solutions stay bounded exactly when all roots $\zeta$ of the stability polynomial $\pi(\zeta; z) = \rho(\zeta) - z\sigma(\zeta)$ satisfy $|\zeta| \le 1$, with roots on the unit circle simple. $S$ is the set of $z$ for which this root condition holds. At $z = 0$ it is the [zero-stability](/zero-stability/) condition on $\rho$.

**Why eigenvalues.** For a linear system $y' = My$ with $M = V\Lambda V^{-1}$ diagonalizable, a Runge-Kutta method gives $y_n = V R(h\Lambda)^n V^{-1} y_0$. So $\|y_n\| \le \kappa(V) \max_i |R(h\lambda_i)|^n \|y_0\|$ in the 2-norm, with $\kappa(V) = \|V\|\|V^{-1}\|$. The iterates stay bounded for all $n$ when every $h\lambda_i$ lies in $S$, and grow when some $h\lambda_i$ lies outside. For a nonlinear problem the same test is applied to the eigenvalues of the Jacobian $\partial f / \partial y$ along the solution. This is a heuristic, not a theorem: for strongly non-normal $M$ ($\kappa(V)$ large) transient growth can be large even inside $S$.

**Facts that follow from the definitions.**
1. *Explicit methods have bounded regions.* A nonconstant polynomial satisfies $|R(z)| \to \infty$ as $|z| \to \infty$, so $S$ is bounded for every explicit Runge-Kutta method. The same holds for explicit multistep methods. In particular no explicit method is [A-stable](/a-stability/), that is, has $S \supseteq \{\operatorname{Re} z \le 0\}$.
2. *Near the origin.* Since $R(x) = 1 + x + O(x^2)$ for a consistent one-step method, $|R(x)| < 1$ for small real $x < 0$: every consistent method is stable for small enough $h$ when $\lambda$ is real and negative. Near the imaginary axis this can fail; explicit Euler has $|1 + iy| > 1$ for every real $y \ne 0$.
3. *Boundary locus.* For a multistep method, a root of $\pi$ crosses the unit circle exactly when $z = \rho(e^{i\theta}) / \sigma(e^{i\theta})$ for some $\theta$. Plotting this curve splits the plane into pieces on each of which the number of roots outside the unit disk is constant; testing one point per piece gives $S$.
4. *Maximum principle.* For a rational $R$ with no poles in the left half-plane, $S \supseteq \{\operatorname{Re} z \le 0\}$ holds if and only if $|R(iy)| \le 1$ for all real $y$ (HNW II, Section IV.3). This is how A-stability is checked.

## Examples

Real stability intervals $S \cap \mathbb{R}$ and imaginary-axis intervals of common methods (computed from $R$ and $\pi$):

| method | $R(z)$ or $\pi$ | $S \cap \mathbb{R}$ | $S \cap i\mathbb{R}$ |
|---|---|---|---|
| explicit Euler | $1 + z$ | $[-2, 0]$ | $\{0\}$ |
| Heun, explicit midpoint (order 2) | $1 + z + z^2/2$ | $[-2, 0]$ | $\{0\}$ |
| Kutta order 3 | $1 + z + z^2/2 + z^3/6$ | $[-2.5127, 0]$ | $[-\sqrt3, \sqrt3]$ |
| classical RK4 | $\sum_{k \le 4} z^k/k!$ | $[-2.7853, 0]$ | $[-2\sqrt2, 2\sqrt2]$ |
| Adams-Bashforth 2 | $\zeta^2 - \zeta - z(\frac32\zeta - \frac12)$ | $[-1, 0]$ | $\{0\}$ |
| Adams-Bashforth 3 | $\zeta^3 - \zeta^2 - \frac{z}{12}(23\zeta^2 - 16\zeta + 5)$ | $[-\frac{6}{11}, 0]$ | small interval |
| backward Euler | $1/(1 - z)$ | $(-\infty, 0] \cup [2, \infty)$ | all of $i\mathbb{R}$ |
| trapezoidal rule | $(1 + z/2)/(1 - z/2)$ | $(-\infty, 0]$ | all of $i\mathbb{R}$ |

The explicit Euler region is the disk $|1 + z| \le 1$ of radius 1 around $-1$. Backward Euler is stable outside the disk $|1 - z| < 1$, so it is A-stable and even damps some growing solutions. The trapezoidal rule's region is exactly the closed left half-plane. The [backward differentiation formulas](/backward-differentiation-formulas/) of orders 1 and 2 are A-stable; orders 3 to 6 contain a wedge $|\arg(-z)| \le \alpha$ with $\alpha \approx 86.03°$, $73.35°$, $51.84°$ and $17.84°$ (A($\alpha$)-stability; HNW II, Section V.2).

*A step size limit.* For $y' = -50y$ and explicit Euler, $z = -50h$ must lie in $[-2, 0]$, so $h \le 0.04$. After 20 steps, $(1 - 50h)^{20}$ is $9.5 \times 10^{-7}$ for $h = 0.03$, $1$ for $h = 0.04$, $2.65$ for $h = 0.041$ and $3.3 \times 10^3$ for $h = 0.05$, although the exact solution has decayed to almost nothing in each case.

*Method of lines.* Central differences for the [heat equation](/heat-equation/) $u_t = u_{xx}$ give eigenvalues in $[-4/\Delta x^2, 0]$. Explicit Euler then needs $4\Delta t/\Delta x^2 \le 2$, the familiar limit $\Delta t \le \Delta x^2/2$ of the [FTCS method](/ftcs-method/). Central differences for [advection](/advection-equation/) give imaginary eigenvalues, which explicit Euler cannot handle at any $\Delta t$, while RK4 can for Courant numbers up to $2\sqrt2$.

## Where it is used

- **Choosing the step size** of explicit methods: the largest $h$ with all $h\lambda_i \in S$ (the "stability limit"), often more restrictive than accuracy.
- **Defining stiffness**: a [stiff problem](/stiff-ode-problem/) is one where stability, not accuracy, limits the step of explicit methods.
- **Classifying implicit methods**: [A-stability](/a-stability/), [L-stability](/l-stability/) ($R(z) \to 0$ as $z \to \infty$) and A($\alpha$)-stability are statements about $S$ and $R$.
- **Designing methods**: stabilized explicit methods such as Runge-Kutta-Chebyshev stretch $S$ along the negative real axis to length about $2s^2$ with $s$ stages, for parabolic problems.
- **PDE time stepping** in the [method of lines](/method-of-lines/), where the semi-discrete eigenvalues must fit into $S$; this is a close relative of [von Neumann analysis](/von-neumann-stability-analysis/).

## References
