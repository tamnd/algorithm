---
tag: A4VA83
kind: problem
slug: heat-equation
name: Heat equation
aliases:
- diffusion equation
- heat conduction equation
area: numerical/differential-equations
level: intro
summary: "The parabolic PDE u_t = alpha u_xx with initial and boundary data. Solutions smooth out and decay. The model problem for the explicit stability limit dt <= dx^2/(2 alpha)."
model: real-ram
prereqs: [pde-classification]
see_also: [ftcs-method, crank-nicolson-method, method-of-lines, von-neumann-stability-analysis, lax-equivalence-theorem, stiff-ode-problem, poisson-equation, finite-difference-method]
sources:
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 9 (diffusion equations and parabolic problems)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 16 (the diffusion equation)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 2 (parabolic equations in one space variable)
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, American Mathematical Society, 2010
    locator: Section 2.3 (the heat equation, fundamental solution, maximum principle, energy methods)
---

The heat equation $u_t = \alpha u_{xx}$ describes how a temperature or a concentration $u(x, t)$ spreads out by diffusion, with a diffusion coefficient $\alpha > 0$. It is the model [parabolic](/pde-classification/) equation: its solutions become smooth at once, they decay, and they obey a maximum principle. For numerical methods it is the model problem that shows why explicit time steps must satisfy $\Delta t \le \Delta x^2 / (2\alpha)$, and why implicit schemes such as [Crank-Nicolson](/crank-nicolson-method/) are used instead.

## In plain words

Heat a metal rod in the middle and leave it alone. The hot part cools, the cool parts warm up, and after a while the temperature is even along the rod. The heat equation says that the temperature at a point rises when its neighbours are warmer than it on average, and falls when they are cooler.

Sharp corners in the temperature profile disappear at once, and the fast wiggles fade much faster than the slow waves. A computer stores the temperature at points of a grid and moves forward in small time steps. The simplest method is only correct when each time step is small compared to the square of the grid spacing. If the step is a little too large, the fast wiggles grow instead of fading, and the numbers explode.

## Definition

**Notation.** The unknown is $u(x, t)$. The mesh widths are $\Delta x = \ell / M$ and $\Delta t$, the grid points are $x_j = j \Delta x$ and $t_n = n \Delta t$, and $U_j^n \approx u(x_j, t_n)$. The mesh ratio is $r = \alpha \Delta t / \Delta x^2$. It plays for the heat equation the part that the Courant number plays for the [advection equation](/advection-equation/). Errors are measured in the max norm $\max_j |U_j^n - u(x_j, t_n)|$ unless the text says otherwise.

**The initial-boundary value problem.** Given $\alpha > 0$, a length $\ell > 0$, a final time $T > 0$ and initial data $u_0$ with $u_0(0) = u_0(\ell) = 0$, find $u$ with

$$u_t = \alpha\, u_{xx} \quad (0 < x < \ell,\ 0 < t \le T), \qquad u(x, 0) = u_0(x), \qquad u(0, t) = u(\ell, t) = 0.$$

The [boundary conditions](/boundary-conditions/) here are homogeneous Dirichlet conditions. Neumann conditions $u_x = 0$ describe an insulated end.

**Fourier series solution.** If $u_0(x) = \sum_{k \ge 1} b_k \sin(k \pi x / \ell)$ with $\sum |b_k| < \infty$, the solution is

$$u(x, t) = \sum_{k \ge 1} b_k\, e^{-\alpha (k\pi/\ell)^2 t} \sin(k \pi x / \ell).$$

Each sine mode decays at its own rate $\alpha (k\pi/\ell)^2$, and the high modes decay fastest. This is the smoothing property: for each $t > 0$ the series converges with all its derivatives, so $u(\cdot, t)$ is $C^\infty$ even when $u_0$ has corners.

**Energy decay.** For a smooth solution, $E(t) = \int_0^\ell u^2\, dx$ does not increase. *Proof.* $E'(t) = 2\int_0^\ell u\, u_t\, dx = 2\alpha \int_0^\ell u\, u_{xx}\, dx = -2\alpha \int_0^\ell u_x^2\, dx \le 0$, by integration by parts, where the boundary term $2\alpha [u\, u_x]_0^\ell$ is zero because $u = 0$ at both ends. $\square$ The same argument applied to the difference of two solutions gives uniqueness and stability in the $L^2$ norm.

**Maximum principle.** A classical solution on $[0, \ell] \times [0, T]$ takes its maximum and its minimum on the parabolic boundary $\{t = 0\} \cup \{x = 0\} \cup \{x = \ell\}$ (Evans, Section 2.3). With zero boundary values this gives $\min(0, \min u_0) \le u \le \max(0, \max u_0)$, so the problem is stable in the max norm.

**The whole line.** On $x \in \mathbb{R}$ with bounded continuous $u_0$, the solution is the convolution with the heat kernel, $u(x, t) = (4\pi\alpha t)^{-1/2} \int_{\mathbb{R}} e^{-(x - s)^2/(4\alpha t)}\, u_0(s)\, ds$. A positive $u_0$ with compact support gives $u > 0$ everywhere for $t > 0$: the speed of propagation is infinite.

**The computational task.** Given $u_0$, $\alpha$, $\ell$, $T$ and a mesh, compute $U_j^N$ with $t_N = T$, and report the error in a stated norm.

## Variants

- **Several space dimensions.** $u_t = \alpha \Delta u$ on a domain $\Omega \subset \mathbb{R}^m$. The steady state $\Delta u = 0$, or $-\Delta u = g$ with a source, is the [Poisson equation](/poisson-equation/).
- **Variable coefficients.** $u_t = (\kappa(x) u_x)_x$, with a conductivity $\kappa(x) \ge \kappa_0 > 0$.
- **Sources and reactions.** $u_t = \alpha u_{xx} + g(x, t, u)$. With a nonlinear $g$ these are reaction-diffusion equations, a standard use of [operator splitting](/operator-splitting/).
- **Advection-diffusion.** $u_t + a u_x = \alpha u_{xx}$, which moves to the hyperbolic regime as $\alpha \to 0$.
- **Backward heat equation.** Find $u_0$ from $u(\cdot, T)$. This is ill posed: the mode $k$ is multiplied by $e^{\alpha (k\pi/\ell)^2 T}$, so arbitrarily small changes of the data change $u_0$ by arbitrarily large amounts.

## Examples

**One mode.** With $\alpha = 1$, $\ell = 1$ and $u_0 = \sin \pi x$, the solution is $u = e^{-\pi^2 t} \sin \pi x$. At $t = 0.1$ the amplitude is $e^{-0.1\pi^2} = 0.372708$.

**A parabola.** For $u_0(x) = x(1 - x)$ on $[0, 1]$, $b_k = 8/(k\pi)^3$ for odd $k$ and $b_k = 0$ for even $k$. At $t = 0.1$, $u(0.5, 0.1) = 0.0961619$.

**Convergence of FTCS.** The explicit [FTCS scheme](/ftcs-method/) is $U_j^{n+1} = U_j^n + r\,(U_{j-1}^n - 2U_j^n + U_{j+1}^n)$. With $u_0 = x(1 - x)$, $\alpha = 1$, $r = 0.4$ fixed and $T = 0.1$, the max-norm errors are:

| $\Delta x$ | steps | max error at $T = 0.1$ |
|---|---|---|
| 1/10 | 25 | $1.111 \cdot 10^{-3}$ |
| 1/20 | 100 | $2.741 \cdot 10^{-4}$ |
| 1/40 | 400 | $6.830 \cdot 10^{-5}$ |
| 1/80 | 1600 | $1.706 \cdot 10^{-5}$ |

The error falls by a factor of about 4 when $\Delta x$ is halved. Since $\Delta t = r \Delta x^2$, this is the expected $O(\Delta t + \Delta x^2) = O(\Delta x^2)$.

**Just below and just above the limit.** Same data, $\Delta x = 1/20$, 400 steps. With $r = 0.48$ (so $T = 0.48$) the max error is $4.13 \cdot 10^{-5}$. With $r = 0.5$ it is $3.76 \cdot 10^{-5}$. With $r = 0.52$ (so $T = 0.52$) the largest value $|U_j^{400}|$ is $1.96 \cdot 10^6$, while the exact solution is at most $0.0015$. The highest grid mode is multiplied in each step by $1 - 4r \sin^2(19\pi/40)$, which is less than $-1$ when $r > 0.5$ by a small margin.

## Known algorithms

- **[FTCS](/ftcs-method/).** Forward Euler in time, central differences in space. Order $O(\Delta t + \Delta x^2)$, stable in the max norm and the 2-norm if and only if $r \le 1/2$. For $r \le 1/2$ each new value $r U_{j-1}^n + (1 - 2r) U_j^n + r U_{j+1}^n$ is a convex combination of old values, which gives a discrete maximum principle.
- **Backward Euler in time.** Unconditionally stable, order $O(\Delta t + \Delta x^2)$, one [tridiagonal solve](/thomas-algorithm/) of cost $O(M)$ per step.
- **[Crank-Nicolson](/crank-nicolson-method/).** The trapezoidal rule in time: order $O(\Delta t^2 + \Delta x^2)$, unconditionally stable in the 2-norm, but its amplification factor tends to $-1$ for high modes, so rough data give slowly decaying oscillations.
- **[Method of lines](/method-of-lines/).** Discretize $u_{xx}$ by central differences and solve the ODE system $U' = \alpha A U$ with a stiff solver such as the [backward differentiation formulas](/backward-differentiation-formulas/) or an [L-stable](/l-stability/) Runge-Kutta method.
- **Other space discretizations.** [Finite elements](/finite-element-method/) on general domains, [spectral methods](/spectral-methods/) for smooth periodic problems, and the [ADI method](/adi-method/) in two dimensions, which needs only tridiagonal solves.

## Bounds

- **Stiffness of the semi-discrete problem.** The central difference matrix $\alpha A$ with $M - 1$ interior points has the eigenvalues $-\frac{4\alpha}{\Delta x^2} \sin^2\frac{k \pi \Delta x}{2\ell}$, $k = 1, \dots, M - 1$. They lie between about $-\alpha\pi^2/\ell^2$ and $-4\alpha/\Delta x^2$, so their ratio grows like $\Delta x^{-2}$.
- **Explicit methods need $\Delta t = O(\Delta x^2)$.** An explicit Runge-Kutta method has a bounded stability interval $[-\beta, 0]$ on the negative real axis, so the method of lines with it is stable only if $\Delta t \le \beta \Delta x^2 / (4\alpha)$. For forward Euler $\beta = 2$, which gives $r \le 1/2$. This is proved by the eigenvalue argument above. To reach a fixed $T$ an explicit method takes $\Theta(\Delta x^{-2})$ steps of cost $\Theta(\Delta x^{-1})$ each in one dimension.
- **Implicit methods.** Backward Euler and Crank-Nicolson are stable for each $r$. In one dimension a step costs $\Theta(M)$ with the tridiagonal solver, so a run to a fixed $T$ with $\Delta t \sim \Delta x$ costs $\Theta(M^2)$ for Crank-Nicolson.
- **Convergence.** By the [Lax equivalence theorem](/lax-equivalence-theorem/), a consistent linear scheme converges if and only if it is stable. The orders above hold when $u$ is smooth enough, for example $u_{tt}$ and $u_{xxxx}$ bounded for FTCS.

## Reductions

- **To an ODE system.** The [method of lines](/method-of-lines/) turns the heat equation into the linear [initial value problem](/ode-initial-value-problem/) $U' = \alpha A U$, a standard [stiff problem](/stiff-ode-problem/).
- **To linear systems.** Each step of an implicit scheme is a [tridiagonal system](/tridiagonal-system-solving/) in one dimension and a [sparse linear system](/sparse-linear-systems/) in higher dimensions, often solved by [multigrid](/multigrid-method/) or the [conjugate gradient method](/conjugate-gradient-method/).
- **To the eigenproblem.** Separation of variables reduces the problem to the eigenfunctions of $-d^2/dx^2$ with the boundary conditions, a [Sturm-Liouville problem](/sturm-liouville-problem/). On a uniform grid the discrete eigenvectors are sine vectors, so the [discrete sine transform](/discrete-sine-transform/) diagonalizes the scheme.
- **Steady state.** As $t \to \infty$ with time-independent sources, the solution tends to the solution of the [Poisson equation](/poisson-equation/).

## Applications

Heat conduction in solids, diffusion of chemicals and pollutants, the Black-Scholes equation of option pricing (which becomes the heat equation after a change of variables), image smoothing (Gaussian blur is the heat kernel), and the viscous part of the [Navier-Stokes equations](/navier-stokes-equations/).

## References
