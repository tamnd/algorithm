---
tag: Z1EVBP
kind: technique
slug: method-of-lines
name: Method of lines
aliases:
- MOL
- semi-discretization
area: numerical/differential-equations
level: core
summary: "Discretize a time-dependent PDE in space only, which gives a large ODE system U' = F(t, U), then solve it with an ODE integrator whose stability region holds dt times the spectrum of F."
prereqs: [ode-initial-value-problem, finite-difference-method, heat-equation]
see_also: [stiff-ode-problem, absolute-stability, crank-nicolson-method, backward-differentiation-formulas, classical-runge-kutta-4, advection-equation, courant-friedrichs-lewy-condition, operator-splitting]
sources:
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 9 (method of lines discretizations of the heat equation, stiffness) and Chapter 10 (method of lines for the advection equation, stability regions and the spectrum)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.1 (stiff equations, the method of lines for the heat equation as a source of stiffness)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 16 (the diffusion equation, semi-discretization and the method of lines) and Chapter 17 (hyperbolic equations)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 1 (ODE systems from the method of lines) and Chapter 3 (stiffness)
---

The method of lines solves a time-dependent partial differential equation in two stages: it first discretizes the space variables only, which turns the PDE into a large system of ordinary differential equations $U'(t) = F(t, U(t))$, and then it solves that [initial value problem](/ode-initial-value-problem/) with an ODE method. The space discretization can be a [finite difference](/finite-difference-method/), [finite volume](/finite-volume-method/), [finite element](/finite-element-method/) or [spectral](/spectral-methods/) method. The time step is then chosen so that $\Delta t$ times the eigenvalues of the Jacobian of $F$ lie in the [stability region](/absolute-stability/) of the ODE method, which for diffusion makes the system a [stiff problem](/stiff-ode-problem/).

## In plain words

A PDE describes a quantity that changes in space and in time, such as the temperature along a rod. The method of lines first picks a row of points along the rod and keeps one unknown temperature at each point. The PDE then says how fast each of these temperatures changes, given its neighbours. That is a system of ordinary differential equations, one for each point, all coupled together.

Now any good solver for ordinary differential equations can do the time stepping. The name comes from the picture: in a plane with space across and time upward, the unknowns live on vertical lines, one line for each grid point. The hard part is the time step. Fine grids create very fast modes, and an explicit solver must take tiny steps to follow them without blowing up.

## When it applies

- The PDE is an evolution equation $u_t = \mathcal{L}(u)$ with initial data, where $\mathcal{L}$ contains only space derivatives: parabolic equations such as the [heat equation](/heat-equation/), hyperbolic equations such as the [advection equation](/advection-equation/), and mixed ones such as advection-diffusion-reaction equations.
- A good ODE solver with error control is available, and you want to reuse it. Stiff solvers based on the [BDF](/backward-differentiation-formulas/) or on [Radau IIA](/radau-iia-methods/) methods are the usual choice for diffusion.
- The space and time errors can be treated separately. The total error is the space error of the semi-discrete system plus the time error of the ODE solver.
- It applies less well when space and time accuracy are tightly coupled, as in the [Lax-Wendroff method](/lax-wendroff-method/), whose second-order accuracy comes from a Taylor expansion in space and time together, with a compact three-point stencil for the correction term; central differences followed by a two-stage Runge-Kutta method give a different scheme with a wider stencil.

## The template

**Notation.** The PDE is $u_t = \mathcal{L}(u)$ for $u(x, t)$ on a space domain with [boundary conditions](/boundary-conditions/). The mesh width is $\Delta x$, the semi-discrete unknowns are $U_j(t) \approx u(x_j, t)$, and $\Delta t$ is the time step of the ODE method. The norm is stated with each result.

```pseudo id=main
METHOD-OF-LINES(PDE, u0, T, Δx, ODE-SOLVER)
L1  choose space grid points x_1, …, x_m with spacing Δx
L2  build F with F_j(t, U) ≈ L(u)(x_j, t) from the U_i near x_j     ▷ hole: space discretization of order q
L3  put the boundary conditions into F (or as algebraic equations)  ▷ hole: boundary closure
L4  U(0) ← (u0(x_1), …, u0(x_m))
L5  estimate the spectrum of ∂F/∂U                                   ▷ decides stiff or nonstiff
L6  choose ODE-SOLVER whose stability region holds Δt · spectrum     ▷ hole: time integrator of order p
L7  U(T) ← ODE-SOLVER(F, 0, U(0), T, Δt)
L8  return U(T)
```

**Error.** Let $u$ be the exact solution and $\bar U(t)$ the exact solution of the semi-discrete system. Then $u(x_j, T) - U_j^N = (u(x_j, T) - \bar U_j(T)) + (\bar U_j(T) - U_j^N)$. The first part is the space error, $O(\Delta x^q)$ when the semi-discretization is consistent of order $q$ and stable uniformly in $\Delta x$. The second part is the global error of the ODE method on the semi-discrete system, $O(\Delta t^p)$, but with a constant that must not grow as $\Delta x \to 0$. For a linear system $U' = AU$ with a normal matrix $A$, this holds when $\Delta t \lambda$ lies in the stability region for each eigenvalue $\lambda$ of $A$ (in the 2-norm). For non-normal $A$ the eigenvalue condition is necessary but not always sufficient, and one needs bounds on the pseudospectra or on the norms of the powers of the step matrix.

**Stability limits from the spectrum.** For $u_t = \alpha u_{xx}$ with central differences and Dirichlet data on $[0, 1]$, the eigenvalues of $A$ are $-\frac{4\alpha}{\Delta x^2}\sin^2\frac{k\pi\Delta x}{2}$, $k = 1, \dots, m$, so they fill $[-4\alpha/\Delta x^2, 0)$. For $u_t + a u_x = 0$ with periodic central differences, the eigenvalues are $-\frac{ia}{\Delta x}\sin(k\Delta x)$, on the imaginary axis between $\pm i|a|/\Delta x$. For first-order upwind differences they lie on a circle of radius $|a|/\Delta x$ through 0 in the left half-plane. An explicit method with a stability interval $[-\beta, 0]$ on the real axis therefore needs $\Delta t \le \beta \Delta x^2 / (4\alpha)$ for the heat equation, and a method that contains $[-i\gamma, i\gamma]$ on the imaginary axis needs $|\nu| = |a|\Delta t/\Delta x \le \gamma$ for central advection.

## Classic examples

**FTCS and Crank-Nicolson.** Central differences for $u_{xx}$ followed by [Euler's method](/euler-method/) give the [FTCS scheme](/ftcs-method/). Followed by the trapezoidal rule they give the [Crank-Nicolson method](/crank-nicolson-method/). Followed by [backward Euler](/backward-euler-method/) they give the fully implicit scheme. So these three classic schemes are all methods of lines.

**Space error versus time error.** For $u_t = u_{xx}$ on $[0, 1]$, $u_0 = \sin\pi x$, the semi-discrete solution with central differences is exactly $\bar U_j(t) = e^{\mu t}\sin\pi x_j$ with $\mu = -\frac{4}{\Delta x^2}\sin^2\frac{\pi\Delta x}{2}$, and [classical RK4](/classical-runge-kutta-4/) multiplies it by $R(\mu\Delta t)$ in each step. With $\Delta x = 1/20$ and $T = 0.1$, the max-norm error of the semi-discrete solution is $7.565 \cdot 10^{-4}$. The time errors $|R(\mu\Delta t)^N - e^{\mu T}|$ are $2.26 \cdot 10^{-10}$, $1.40 \cdot 10^{-11}$, $8.68 \cdot 10^{-13}$, $3.66 \cdot 10^{-14}$ for $N = 60, 120, 240, 480$, a factor of about 16 per halving. The total error stays at $7.565 \cdot 10^{-4}$: here the space error dominates, and a smaller $\Delta t$ buys nothing.

**The explicit limit, just below and above.** With $\Delta x = 1/20$ and 19 interior points, the most negative eigenvalue is $-1600\sin^2(19\pi/40) = -1590.15$. The real stability interval of RK4 is $[-2.7853, 0]$, so the limit is $\Delta t \le 2.7853/1590.15 = 0.0017516$. With $u_0 = x(1 - x)$ and 300 steps, $\Delta t = 0.0017$ gives $\max_j |U_j| = 0.00170$ at $T = 0.51$, close to the true solution. $\Delta t = 0.0018$ gives $\max_j |U_j| = 1.1 \cdot 10^{10}$ at $T = 0.54$.

**Advection.** Central differences plus Euler's method is unstable for every $\Delta t > 0$, because $|1 + iy| > 1$ for each real $y \ne 0$. Central differences plus RK4 are stable for $|\nu| \le 2\sqrt2 \approx 2.83$, since RK4 contains the segment $[-2\sqrt2\, i, 2\sqrt2\, i]$ of the imaginary axis. Upwind differences plus Euler's method give the [upwind scheme](/upwind-scheme/), stable for $0 \le \nu \le 1$. Strong-stability-preserving Runge-Kutta methods with [WENO](/weno-scheme/) or [flux-limited](/flux-limiter-methods/) finite volume space discretizations are the standard high-resolution method of lines for conservation laws.

**Reaction-diffusion with a stiff solver.** For $u_t = \alpha u_{xx} + g(u)$, a BDF code with a banded or sparse Jacobian solves the whole system with error control. The tridiagonal Jacobian makes each Newton step cost $O(m)$ in one dimension.

## Variations

- **Implicit-explicit (IMEX) methods.** Treat the stiff linear diffusion implicitly and the nonstiff reaction or advection explicitly, in one Runge-Kutta or multistep method.
- **[Operator splitting](/operator-splitting/).** Solve the semi-discrete diffusion and reaction parts in alternating sub-steps, each with its best solver.
- **[Exponential integrators](/exponential-integrators/).** Integrate the stiff linear part $AU$ exactly through functions of $\Delta t A$, and treat the rest explicitly.
- **Moving meshes.** Let the grid points $x_j(t)$ move with the solution, which adds equations for $x_j$ and makes $F$ depend on the mesh.
- **Transverse method of lines (Rothe's method).** Discretize in time first, which leaves a boundary value problem in space at each time step, solved for example by adaptive finite elements.

## Pitfalls

- **An explicit solver on a diffusion problem.** The step limit $\Delta t = O(\Delta x^2)$ is set by the fastest grid mode, not by the accuracy needed. An adaptive explicit solver does not fail, but it takes a huge number of small steps, all at the stability limit.
- **Balancing the two errors badly.** As in the example above, a time integrator of high order with tiny $\Delta t$ cannot remove the space error. Choose $\Delta t$ so that the time error is about the size of the space error.
- **Trusting eigenvalues for non-normal matrices.** For upwind advection with inflow boundaries the matrix is far from normal, and the eigenvalues alone can predict stability where transient growth is large. Use the pseudospectrum or the energy method.
- **Boundary conditions that are not consistent with the initial data.** A mismatch at $t = 0$ creates a layer of fast transients that an error-controlled solver resolves with many tiny steps.
- **Order reduction at the boundaries.** Runge-Kutta methods applied to semi-discretizations with time-dependent boundary data can lose order, because the stage values do not satisfy the boundary conditions at the stage times.

## Exercises

1. Show that the eigenvectors of the central difference matrix for $u_{xx}$ with Dirichlet conditions are the sine vectors $(\sin k\pi x_j)_j$, and find the eigenvalues.
2. Find the largest $\Delta t$ for which central differences plus Heun's method are stable for $u_t = u_{xx}$ with $\Delta x = 0.01$.
3. Show that upwind differences in space followed by Euler's method in time give exactly the upwind scheme, and find the eigenvalues of the semi-discrete periodic matrix.
4. For $u_t = u_{xx}$ with $u_0 = \sin\pi x$, compare the total error of central differences plus backward Euler for $\Delta t = \Delta x$ and $\Delta t = \Delta x^2$, and explain which error dominates.

## References
