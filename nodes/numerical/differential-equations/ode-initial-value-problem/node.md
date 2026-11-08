---
tag: 9Z37FY
kind: problem
slug: ode-initial-value-problem
name: Initial value problem for ODEs
aliases:
- IVP
- Cauchy problem
- initial value problem
area: numerical/differential-equations
level: intro
summary: "Find y(t) with y' = f(t, y) and y(t_0) = y_0 on [t_0, T]. Well posed when f is continuous and Lipschitz in y. Numerically: approximate y(T) with few evaluations of f."
model: real-ram
prereqs: [lipschitz-condition]
see_also: [picard-lindelof-theorem, euler-method, runge-kutta-methods, linear-multistep-methods, stiff-ode-problem, global-error, order-of-accuracy, gronwall-inequality]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Chapter I, Sections I.7 to I.10 (existence theory, Lipschitz condition, differential inequalities and dependence on the initial values)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1, Section 1.1 (ordinary differential equations and the Lipschitz condition)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (the initial value problem for ordinary differential equations, Lipschitz continuity and well-posedness)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 1 (ordinary differential equations) and Chapter 2 (on problem stability)
---

The initial value problem for an ordinary differential equation (ODE) asks for a function $y : [t_0, T] \to \mathbb{R}^d$ with $y'(t) = f(t, y(t))$ and $y(t_0) = y_0$, where the right-hand side $f$ and the start value $y_0$ are given. When $f$ is continuous and [Lipschitz](/lipschitz-condition/) in $y$, the solution exists, is unique, and depends continuously on $y_0$ ([Picard-Lindelöf theorem](/picard-lindelof-theorem/)). The numerical task is to compute approximations $y_n \approx y(t_n)$ on a grid with as few evaluations of $f$ as possible. Almost every method of this sub-area, from [Euler's method](/euler-method/) to [Runge-Kutta](/runge-kutta-methods/) and [linear multistep methods](/linear-multistep-methods/), solves this problem.

## In plain words

You know where something is at the start, and you have a rule that tells you, at each place and each moment, in which direction and how fast it moves. The task is to find the whole path. A planet with a known position and speed, under gravity, is an example. So is a chemical mixture whose concentrations change by known reaction rates.

A computer cannot follow the path at every moment. It takes small time steps, and at each step it asks the rule for the current direction. The quality of a method is how close it stays to the true path for a given number of questions to the rule. Some problems are easy, because nearby paths stay close together. In others, nearby paths move apart quickly, so each small error grows, and no method can do well.

## Definition

**Notation.** This notation is used on all pages of this sub-area. The unknown is $y(t) \in \mathbb{R}^d$. The step size is $h > 0$, the grid is $t_n = t_0 + n h$ (or $t_{n+1} = t_n + h_n$ with variable steps), and $y_n$ is the approximation of $y(t_n)$. The global error is $e_n = y(t_n) - y_n$. A method has order $p$ when $e_n = O(h^p)$ on bounded intervals. $L$ is a Lipschitz constant of $f$ in $y$, and $\|\cdot\|$ is a fixed norm on $\mathbb{R}^d$. The test equation is $y' = \lambda y$ with $z = h\lambda$, and a one-step method maps $y_n$ to $y_{n+1} = R(z) y_n$ on it, with stability function $R$.

**The problem.** Let $D \subseteq \mathbb{R} \times \mathbb{R}^d$ be open, $f : D \to \mathbb{R}^d$ continuous and $(t_0, y_0) \in D$. A solution on an interval $I \ni t_0$ is a differentiable function $y : I \to \mathbb{R}^d$ with $(t, y(t)) \in D$ and

$$y'(t) = f(t, y(t)) \quad (t \in I), \qquad y(t_0) = y_0.$$

Since $f$ is continuous, each solution is $C^1$, and $y$ is a solution if and only if it is continuous and satisfies the integral equation

$$y(t) = y_0 + \int_{t_0}^{t} f(s, y(s))\, ds \qquad (t \in I).$$

**Existence and uniqueness.** If $f$ is continuous on $[t_0, T] \times \mathbb{R}^d$ and satisfies $\|f(t, u) - f(t, v)\| \le L \|u - v\|$ for all $t \in [t_0, T]$ and $u, v \in \mathbb{R}^d$, then the problem has exactly one solution on $[t_0, T]$ (Picard-Lindelöf). Continuity of $f$ alone gives a solution on some interval around $t_0$ (Peano's theorem, HNW I, Section I.7), but it does not give uniqueness, and it does not give a solution up to a prescribed $T$.

**Continuous dependence.** Under the same hypotheses, two solutions $y$ and $z$ with start values $y_0$ and $z_0$ satisfy

$$\|y(t) - z(t)\| \le e^{L (t - t_0)} \|y_0 - z_0\| \qquad (t_0 \le t \le T).$$

*Proof.* Let $w(t) = \|y(t) - z(t)\|$. Subtracting the two integral equations gives $w(t) \le w(t_0) + \int_{t_0}^t L\, w(s)\, ds$, and [Gronwall's inequality](/gronwall-inequality/) turns this into $w(t) \le w(t_0) e^{L(t - t_0)}$. $\square$

So the problem is well posed: a small change in $y_0$ (or, by the same argument, in $f$) changes the solution by a small amount on a bounded interval. The factor $e^{L(t - t_0)}$ is the worst case, and it is attained by $y' = L y$.

**The computational task.** The input is a procedure that returns $f(t, u)$ for given $(t, u)$, the values $t_0$, $y_0$ and $T$, and either a step size $h$ or an error tolerance. The output is $y_N$ with $t_N = T$, often also the values $y_n$ at the grid points or a [dense output](/dense-output/) polynomial. The cost is counted as the number of evaluations of $f$, plus, for implicit methods, the number of Jacobian evaluations $\partial f / \partial y$ and of linear solves. The accuracy is measured by the global error $\|e_N\|$ at the final time, or by $\max_n \|e_n\|$.

## Variants

- **Autonomous problems.** $y' = f(y)$. Each problem becomes autonomous when $t$ is added as an extra component with $t' = 1$.
- **Higher order equations.** $y^{(m)} = g(t, y, y', \dots, y^{(m-1)})$ becomes a first order system for $(y, y', \dots, y^{(m-1)})$. Second order systems $y'' = g(t, y)$ also have special methods, such as [Verlet integration](/verlet-integration/).
- **Stiff problems.** Problems where $f_y$ has eigenvalues with large negative real part, while the solution of interest is smooth. Explicit methods need tiny steps there; see [stiff ODE problem](/stiff-ode-problem/).
- **Hamiltonian problems.** $p' = -\partial H/\partial q$, $q' = \partial H/\partial p$, where long-time behaviour matters more than accuracy at one time; see [Hamiltonian systems](/hamiltonian-systems/).
- **Differential-algebraic equations.** Some components satisfy algebraic constraints instead of ODEs; see [differential-algebraic equations](/differential-algebraic-equations/).
- **Delay equations.** $f$ depends on $y(t - \tau)$; see [delay differential equations](/delay-differential-equations/).
- **Stochastic equations.** A noise term is added; see [stochastic differential equations](/stochastic-differential-equation/).
- **Boundary value problems.** Conditions are given at two ends of the interval instead of at $t_0$ only; see [boundary value problems](/bvp-boundary-value-problem/).

## Examples

**A linear scalar problem.** $y' = \lambda y$, $y(t_0) = y_0$ has the solution $y(t) = y_0 e^{\lambda (t - t_0)}$. Here $L = |\lambda|$.

**A nonlinear problem used for tests.** $y' = -2 t y^2$, $y(0) = 1$ has the solution $y(t) = 1/(1 + t^2)$, so $y(1) = 0.5$.

**The logistic equation.** $y' = y(1 - y)$, $y(0) = y_0$ has the solution $y(t) = y_0 e^t / (1 - y_0 + y_0 e^t)$. For $y_0 = 0.1$, $y(1) = 0.231969316684$. The right-hand side is not globally Lipschitz, but it is Lipschitz with $L = 1$ on the strip $0 \le y \le 1$, and the solution stays in that strip.

**The cost of accuracy.** On the logistic problem above, at $T = 1$, the errors of two methods with $N$ equal steps are:

| method | evaluations of $f$ | $N$ | error at $T = 1$ |
|---|---|---|---|
| [Euler](/euler-method/) | 20 | 20 | $2.98 \cdot 10^{-3}$ |
| Euler | 40 | 40 | $1.51 \cdot 10^{-3}$ |
| [classical RK4](/classical-runge-kutta-4/) | 20 | 5 | $9.15 \cdot 10^{-7}$ |
| RK4 | 40 | 10 | $6.05 \cdot 10^{-8}$ |

The order-4 method is more accurate by a factor of more than 3000 at the same cost, and each doubling of $N$ divides its error by about $2^4 = 16$.

**No solution up to $T$.** $y' = y^2$, $y(0) = 1$ has the solution $y(t) = 1/(1 - t)$, which tends to infinity as $t \to 1$. The right-hand side is smooth but not globally Lipschitz, and no solution exists on $[0, T]$ for $T \ge 1$. A numerical method with a fixed step still returns finite numbers, which are meaningless.

**No uniqueness.** $y' = \sqrt{|y|}$, $y(0) = 0$ has the two solutions $y(t) = 0$ and $y(t) = t^2/4$ for $t \ge 0$ (and infinitely many more, which stay at 0 up to some time $c$ and then follow $(t - c)^2/4$). The right-hand side is continuous but not Lipschitz at $y = 0$. Euler's method started at $y_0 = 0$ returns $y_n = 0$ for all $n$, one solution among many.

**Ill-conditioning.** For $y' = y$ on $[0, 10]$ a change of $y_0$ by $\delta$ changes $y(10)$ by $e^{10}\delta \approx 22026\,\delta$. No method can compute $y(10)$ to a better relative accuracy than the data allow. For $y' = -y$ the same change is damped by $e^{-10}$.

**Stiffness.** $y' = -1000\,(y - \cos t) - \sin t$, $y(0) = 1$ has the smooth solution $y(t) = \cos t$, but $L = 1000$. Euler's method needs $h \le 2/1000$ to stay stable, although $\cos t$ could be followed with much larger steps.

## Known algorithms

- **One-step methods.** [Euler's method](/euler-method/) (order 1), [Heun's method](/heuns-method/) and the [explicit midpoint method](/explicit-midpoint-method/) (order 2), [classical RK4](/classical-runge-kutta-4/), and in general the explicit and [implicit Runge-Kutta methods](/implicit-runge-kutta-methods/), described by a [Butcher tableau](/butcher-tableau/). The [Taylor series method](/taylor-series-method/) uses derivatives of $f$.
- **Multistep methods.** [Linear multistep methods](/linear-multistep-methods/) such as the [Adams-Bashforth](/adams-bashforth-methods/) and [Adams-Moulton methods](/adams-moulton-methods/) reuse earlier values of $f$, so they need only one or two new evaluations per step at any order.
- **Methods for stiff problems.** The [backward Euler method](/backward-euler-method/), [backward differentiation formulas](/backward-differentiation-formulas/), [Radau IIA methods](/radau-iia-methods/) and [Rosenbrock methods](/rosenbrock-methods/). They solve a linear or nonlinear system in each step.
- **Error control.** [Embedded Runge-Kutta pairs](/embedded-runge-kutta-pairs/) such as the [Dormand-Prince method](/dormand-prince-method/) estimate the local error and choose $h$ by [adaptive step size control](/adaptive-step-size-control/). [Extrapolation](/bulirsch-stoer-method/) raises the order by combining runs with several step sizes.
- **Structure-preserving methods.** [Symplectic integrators](/symplectic-integrators/) for Hamiltonian problems.
- **Theory, not a practical solver.** [Picard iteration](/picard-iteration/) proves existence and gives a convergent sequence of functions, but each iterate needs an integral.

## Bounds

- **Convergence.** A one-step method of order $p$ whose increment function is Lipschitz in $y$ has a global error $O(h^p)$ at a fixed $T$, with a constant that contains $e^{L (T - t_0)}$ (HNW I, Section II.3). For a linear multistep method, consistency and [zero-stability](/zero-stability/) together are necessary and sufficient for convergence ([Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/)). These are proved results.
- **Cost for a given accuracy.** A method of order $p$ reaches the error $\varepsilon$ with $N = O(\varepsilon^{-1/p})$ steps, when the solution is smooth enough. This is asymptotic in $\varepsilon \to 0$.
- **Butcher barriers.** An explicit Runge-Kutta method of order $p$ needs at least $p$ stages, and for $p \ge 5$ at least $p + 1$ stages (HNW I, Section II.5). See [Butcher order conditions](/butcher-order-conditions/).
- **Dahlquist barriers.** A zero-stable linear $k$-step method has order at most $k + 1$ for odd $k$ and $k + 2$ for even $k$, and at most $k$ when it is explicit. An A-stable linear multistep method has order at most 2. See [Dahlquist barrier](/dahlquist-barrier/).
- **Stiffness bound.** The stability function of an explicit Runge-Kutta method is a polynomial, so its stability region is bounded, and on $y' = \lambda y$ with $\lambda < 0$ the step must satisfy $h \le c / |\lambda|$ for a constant $c$ that depends on the method only.

## Reductions

- **Quadrature is a special case.** If $f$ does not depend on $y$, then $y(T) = y_0 + \int_{t_0}^T f(t)\, dt$, so each IVP solver is also a [numerical integration](/numerical-integration/) rule. Classical RK4 reduces to [Simpson's rule](/simpsons-rule/) in this case.
- **Order reduction to first order systems.** Each explicit ODE of order $m$ becomes a first order system in $\mathbb{R}^{m d}$, as in the Variants above.
- **Boundary value problems to IVPs.** The [shooting method](/shooting-method/) guesses the missing initial values, solves IVPs, and adjusts the guess by [root finding](/newton-method-for-systems/).
- **PDEs to IVPs.** The [method of lines](/method-of-lines/) discretizes the space variables of a time-dependent PDE and leaves a large IVP in time.
- **IVPs to fixed points.** The integral equation above is a fixed point problem $y = \Phi(y)$, which is the basis of [Picard iteration](/picard-iteration/) and of the existence proof.

## Applications

Initial value problems model orbits in celestial mechanics, molecular dynamics, chemical kinetics, electric circuits, population dynamics and epidemics, control systems and the flight of vehicles. They also appear inside other computations: as the time integration step of PDE solvers, inside shooting methods for boundary value problems, and in continuation and optimization methods that follow a path defined by an ODE.

## References
