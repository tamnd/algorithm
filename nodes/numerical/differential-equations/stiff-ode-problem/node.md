---
tag: XBD13R
kind: problem
slug: stiff-ode-problem
name: Stiff ordinary differential equations
aliases:
- stiffness
- stiff problem
- stiff initial value problem
area: numerical/differential-equations
level: core
summary: "Initial value problems with fast decaying components next to a slow solution, so the step of explicit methods is limited by stability rather than accuracy. Implicit A-stable methods remove the limit."
model: real-ram
prereqs: [ode-initial-value-problem, stability-region, dahlquist-test-equation]
see_also: [a-stability, l-stability, backward-euler-method, backward-differentiation-formulas, radau-iia-methods, rosenbrock-methods, differential-algebraic-equations, exponential-integrators]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.1 (examples of stiff equations, the Curtiss-Hirschfelder and Robertson problems), Section IV.2 (stability domains of explicit methods and the bound on the real stability interval), Section IV.3 (A-stability), Section V.1 (Dahlquist's second barrier)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 8 (stiff ordinary differential equations; numerical difficulties, characterizations of stiffness, A- and L-stability, BDF methods)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 4 (stiff equations)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Section 3.4 (stiffness), Chapter 5 (BDF methods for stiff problems)
  - paper: "C. F. Curtiss and J. O. Hirschfelder, Integration of stiff equations, Proceedings of the National Academy of Sciences 38 (1952) 235-243"
    locator: the term stiff and the first backward differentiation methods; doi:10.1073/pnas.38.3.235
  - paper: "Germund Dahlquist, A special stability problem for linear multistep methods, BIT 3 (1963) 27-43"
    locator: A-stability and the order barrier for A-stable multistep methods; doi:10.1007/BF01963532
---

A stiff ordinary differential equation is an [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, whose Jacobian $\partial f / \partial y$ has eigenvalues with large negative real parts while the solution of interest varies slowly. The fast components decay almost at once, but an explicit method must keep resolving them: its step $h$ is bounded by the [stability region](/stability-region/), not by the accuracy wanted. Stiffness is therefore a property of a problem together with an interval, a tolerance and a class of methods. Implicit methods with large stability regions, such as [backward Euler](/backward-euler-method/), the [BDF methods](/backward-differentiation-formulas/) and [Radau IIA](/radau-iia-methods/), take steps set by accuracy alone.

## In plain words

Picture a cup of coffee in a room. The coffee cools over many minutes, but a thin layer of air around it adjusts to the coffee's temperature in a split second. If you only care about the coffee, the fast air layer is not interesting after the first moment. Yet a simple step-by-step method that looks only at the current state must take tiny steps the whole time, or its picture of the air layer starts to swing wildly and blows up.

Problems like this are called stiff. They appear wherever very fast and very slow processes live side by side: chemistry, electrical circuits, heat flow and control. The cure is a method that looks ahead and solves an equation at each step. That costs more per step, but it can take steps that are thousands of times longer.

## Definition

There is no single formal definition; the standard texts give operational ones (HNW II, Section IV.1; LeVeque 2007, Chapter 8). We use the following.

**Linear model.** For $y' = My + g(t)$ with $M$ diagonalizable with eigenvalues $\lambda_1, \ldots, \lambda_d$, all with $\operatorname{Re}\lambda_i < 0$, the problem on $[t_0, T]$ is stiff when
$$\max_i |\lambda_i| \, (T - t_0) \gg 1 \quad\text{while the solution of interest varies on a time scale much longer than } 1 / \max_i |\lambda_i|.$$
The stiffness ratio $\max_i |\operatorname{Re}\lambda_i| / \min_i |\operatorname{Re}\lambda_i|$ is a common rough measure (Lambert), but a large ratio is neither necessary nor sufficient on its own.

**Operational definition.** A problem is stiff on an interval for a given tolerance when an explicit method with step size control needs a step $h_{\text{stab}}$ that is much smaller than the step $h_{\text{acc}}$ that the local error alone would allow. For nonlinear problems the eigenvalues are those of the Jacobian $J(t) = \partial f / \partial y(t, y(t))$ along the solution, which is a heuristic, not a theorem.

## Variants

- **Linear constant-coefficient stiffness:** $y' = My$ with widely separated eigenvalues, the model behind all stability theory.
- **Singular perturbations:** $y' = f(y, z)$, $\varepsilon z' = g(y, z)$ with small $\varepsilon > 0$ and $g_z$ having eigenvalues with negative real parts. As $\varepsilon \to 0$ this becomes a [differential-algebraic equation](/differential-algebraic-equations/).
- **Oscillatory stiffness:** eigenvalues near the imaginary axis with large modulus (mechanics, wave problems), where damping methods destroy the oscillation and symplectic or exponential methods are preferred.
- **Parabolic PDEs** after semi-discretization by the [method of lines](/method-of-lines/).

## Examples

**Curtiss-Hirschfelder equation.** $y' = -50(y - \cos t)$, $y(0) = 0$, with exact solution $y = \frac{2500\cos t + 50\sin t}{2501} - \frac{2500}{2501}e^{-50t}$. The transient dies by $t \approx 0.2$; afterwards $y \approx \cos t$. Errors at $t = 1.2$ (observed):

| method | $h$ | steps | error |
|---|---|---|---|
| explicit Euler | 0.03 | 40 | 1.2e-4 |
| explicit Euler | 0.04 | 30 | 1.0 |
| explicit Euler | 0.05 | 24 | 1.7e4 |
| backward Euler | 0.1 | 12 | 4.3e-4 |
| backward Euler | 0.2 | 6 | 9.2e-4 |
| backward Euler | 0.4 | 3 | 2.2e-3 |

Explicit Euler is stable only for $50h \le 2$; at $h = 0.04$ the transient is multiplied by $-1$ each step and never decays. Backward Euler, with $R(z) = 1/(1 - z)$, is stable for every $h$.

With the adaptive [Runge-Kutta-Fehlberg method](/runge-kutta-fehlberg-method/) on $[0, 10]$, tolerances $10^{-1}$, $10^{-2}$, $10^{-3}$ and $10^{-4}$ give 166, 167, 169 and 180 accepted steps (observed): the step count hardly depends on the tolerance, because it is set by stability ($h \approx 3.0/50$, the real stability limit of the fourth-order formula). This is the practical signature of stiffness.

**Robertson's chemical kinetics.** $y_1' = -0.04y_1 + 10^4 y_2y_3$, $y_2' = 0.04y_1 - 10^4y_2y_3 - 3 \cdot 10^7 y_2^2$, $y_3' = 3 \cdot 10^7 y_2^2$, $y(0) = (1, 0, 0)$. The solution changes slowly after a short initial layer, but RKF45 with $\text{rtol} = 10^{-4}$ needs 724 accepted steps to reach $t = 1$ and 7742 to reach $t = 10$, about 770 per unit time (observed), and would need millions to reach $t = 10^{5}$. Implicit stiff solvers, whose step is limited only by accuracy, can follow it out to $t = 10^{11}$ with steps that grow with $t$ (HNW II, Chapter IV).

**Heat equation.** Central differences for $u_t = u_{xx}$ on $m$ interior points give eigenvalues from about $-\pi^2$ to about $-4/\Delta x^2$. Explicit Euler needs $\Delta t \le \Delta x^2/2$; the stiffness grows as the grid is refined.

**Non-example.** $y' = -y$ on $[0, 1]$ has a decaying solution but no separation of scales: the accuracy-limited step is already smaller than the stability limit, so it is not stiff.

## Known algorithms

- **[Backward Euler](/backward-euler-method/)**: order 1, A-stable and [L-stable](/l-stability/).
- **[BDF methods](/backward-differentiation-formulas/)** (Gear's methods): orders 1 to 6, A-stable for orders 1 and 2, A($\alpha$)-stable up to 6; the basis of most production stiff solvers.
- **[Radau IIA methods](/radau-iia-methods/)**: implicit Runge-Kutta, order $2s - 1$, L-stable.
- **[Rosenbrock methods](/rosenbrock-methods/)**: linearly implicit, one Jacobian and $s$ linear solves per step, no Newton iteration.
- **[Crank-Nicolson / trapezoidal rule](/crank-nicolson-method/)** and **[Gauss-Legendre](/gauss-legendre-runge-kutta/)** methods: A-stable but not L-stable, so very stiff components are damped poorly.
- **[Exponential integrators](/exponential-integrators/)**: treat the stiff linear part exactly with matrix functions.
- **IMEX and [operator splitting](/operator-splitting/)**: implicit for the stiff part, explicit for the rest.
- **Stabilized explicit methods** (Runge-Kutta-Chebyshev): many stages with a long real stability interval, for mildly stiff parabolic problems with eigenvalues near the negative real axis.

All implicit methods solve a nonlinear system per step, usually by a simplified [Newton iteration](/newton-method-for-systems/) with the matrix $I - h\gamma J$.

## Bounds

- **No explicit method is A-stable** (proved on the [stability region](/stability-region/) page): the stability function of an explicit Runge-Kutta method is a polynomial, so the stability region is bounded. Hence every explicit method needs $h|\lambda| \le C$ for the stiff eigenvalues, and the number of steps on $[t_0, T]$ is at least proportional to $(T - t_0)\max_i|\lambda_i|$.
- **Real stability interval.** For an explicit $s$-stage method of order at least 1, the real stability interval $[-\beta, 0]$ satisfies $\beta \le 2s^2$, with equality for shifted Chebyshev polynomials (HNW II, Section IV.2). So even with many stages, the number of evaluations of $f$ grows like $\sqrt{(T - t_0)\max|\lambda|}$ at best for problems with real negative eigenvalues.
- **Dahlquist's second barrier** (1963): an A-stable linear multistep method has order at most 2, and the trapezoidal rule has the smallest error constant among them (see [Dahlquist barrier](/dahlquist-barrier/)).
- **Cost per step of implicit methods.** For a dense Jacobian, one LU factorization of $I - h\gamma J$ costs $\Theta(d^3)$ and each solve $\Theta(d^2)$; in practice the factorization is reused over many steps.

## Reductions

- **From DAEs:** a semi-explicit index-1 DAE is the limit $\varepsilon \to 0$ of the stiff singular perturbation $\varepsilon z' = g(y, z)$; methods that are L-stable and stiffly accurate, such as Radau IIA and BDF, carry over to DAEs.
- **From parabolic PDEs:** the method of lines turns the [heat equation](/heat-equation/) into a stiff system whose stiffness grows like $1/\Delta x^2$.
- **To linear algebra:** each implicit step reduces to linear systems with $I - h\gamma J$, so sparse direct or Krylov solvers decide the cost for large $d$.

## Applications

Chemical kinetics and combustion (reaction rates spanning many orders of magnitude), electrical circuit simulation (SPICE uses BDF and trapezoidal methods), control and multibody systems, atmospheric chemistry, biology (enzyme kinetics, neuron models), and time stepping of diffusion-dominated PDEs.

## References
