---
tag: WSD57B
kind: technique
slug: method-of-characteristics
name: Method of characteristics
aliases:
- characteristics method
- semi-Lagrangian method
area: numerical/differential-equations
level: advanced
summary: "Solve a first-order PDE by following characteristic curves, along which it reduces to ODEs; numerically, integrate those ODEs or trace them back from grid points and interpolate (semi-Lagrangian)."
prereqs: [pde-classification, ode-initial-value-problem]
see_also: [advection-equation, burgers-equation, wave-equation, eikonal-equation, riemann-problem, upwind-scheme, courant-friedrichs-lewy-condition, level-set-method]
sources:
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, American Mathematical Society, 2010
    locator: Chapter 3, Section 3.2 (characteristics for nonlinear first-order PDE) and Section 3.4 (conservation laws, crossing characteristics)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 2 (characteristics and Riemann invariants for linear systems), Chapter 3 (characteristics and the Riemann problem) and Chapter 11 (nonlinear scalar conservation laws, wave breaking)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 10 (the advection equation, characteristics and the domain of dependence)
  - paper: "Andrew Staniforth and Jean Côté, Semi-Lagrangian integration schemes for atmospheric models, a review, Monthly Weather Review 119 (1991) 2206-2223"
    locator: semi-Lagrangian advection, back trajectories and interpolation, stability beyond the CFL limit
---

The method of characteristics solves a first-order partial differential equation by finding curves in the $(x, t)$ plane, the characteristics, along which the PDE becomes a system of [ordinary differential equations](/ode-initial-value-problem/). For $u_t + a(x, t)\,u_x = c(x, t, u)$ the characteristics solve $\frac{dx}{dt} = a(x, t)$, and along each of them $\frac{du}{dt} = c$. Solving these ODEs from the initial line gives the solution exactly where characteristics do not cross, shows where shocks must form when they do, and is the basis of numerical methods: ray tracing, characteristic grids for hyperbolic systems, and the semi-Lagrangian schemes of weather prediction, which trace characteristics back from grid points and interpolate.

## In plain words

Imagine smoke carried by a wind. Each puff of smoke moves with the wind and, apart from fading, keeps its strength. So to know how much smoke is at a place now, follow the wind backward from that place to where it was at the start, and read off the starting amount. The path a puff takes is a characteristic.

This replaces a problem about how a whole field changes in space and time with many separate problems about single paths, each easy to solve. Trouble starts when paths cross: then two different starting amounts arrive at the same place, and the smooth solution breaks into a jump, a shock wave.

## When it applies

- **First-order equations.** Linear $u_t + a(x, t)u_x = c(x, t)u + d(x, t)$, quasilinear $u_t + a(x, t, u)u_x = c(x, t, u)$ such as [Burgers' equation](/burgers-equation/), and, with characteristic strips, fully nonlinear $F(x, u, \nabla u) = 0$ such as the [eikonal equation](/eikonal-equation/). In several space dimensions, $\frac{dx}{dt} = a(x, t)$ is a system.
- **Hyperbolic systems.** For $q_t + Aq_x = 0$ with $A$ diagonalisable with real eigenvalues ([hyperbolic](/pde-classification/)), the characteristic variables $w = R^{-1}q$ each satisfy a scalar advection equation with speed $\lambda_p$. For nonlinear $2 \times 2$ systems, Riemann invariants are constant along characteristics.
- **Smooth solutions up to a time.** The classical method works until characteristics cross. After that the solution is defined as a weak solution with shocks, and a [Riemann problem](/riemann-problem/) or a conservative scheme is needed.
- **Not for elliptic or parabolic equations.** They have no real characteristics carrying information at finite speed; diffusion terms are added by [operator splitting](/operator-splitting/) when a characteristic method is used for the transport part.

## The template

**Notation.** The PDE is $u_t + a(x, t, u)u_x = c(x, t, u)$ with $u(x, 0) = u_0(x)$. A characteristic starts at $\xi$ and is written $X(t; \xi)$; $Z(t; \xi)$ is the value of $u$ on it.

```pseudo id=main
CHARACTERISTICS(a, c, u0, T, starting points ξ_1, …, ξ_m)
L1  for each starting point ξ do
L2      X(0) ← ξ, Z(0) ← u0(ξ)
L3      solve dX/dt = a(X, t, Z), dZ/dt = c(X, t, Z) on [0, T]   ▷ hole: ODE solver
L4      record the curve (X(t), Z(t))
L5  check that X(t; ξ) is increasing in ξ for each t           ▷ else characteristics cross: shock
L6  u(x, t) ← Z(t; ξ) where ξ solves X(t; ξ) = x               ▷ hole: inversion or interpolation
```

**Why it works.** If $u$ is a $C^1$ solution and $X' = a(X, t, u(X, t))$, then by the chain rule

$$\frac{d}{dt}u(X(t), t) = u_t + X'u_x = u_t + a u_x = c,$$

so $Z(t) = u(X(t), t)$ satisfies the second ODE. Conversely, if the map $\xi \mapsto X(t; \xi)$ is a $C^1$ bijection with positive derivative for $t \le T$, then $u(x, t) = Z(t; \xi(x, t))$ is a $C^1$ solution (Evans, Section 3.2). Since the ODEs have a unique solution when $a$ and $c$ are [Lipschitz](/lipschitz-condition/), so does the PDE, and the domain of dependence of $(x, t)$ is the single point $\xi$.

**The semi-Lagrangian scheme.** For a solution on a grid $x_j$ with step $\Delta t$: for each $j$, integrate $\frac{dX}{dt} = a$ backward over one step from $(x_j, t_{n+1})$ to the foot $X_j^*$ at time $t_n$, interpolate $U^n$ at $X_j^*$, and add the source integrated along the path. Each step costs an ODE step and an interpolation per grid point. With interpolation of degree $r$ and a foot computed with error $O(\Delta t^{q+1})$, the error after $T/\Delta t$ steps is $O(\Delta x^{r+1}/\Delta t + \Delta t^q)$ for smooth solutions (asymptotic).

## Classic examples

**Linear advection.** For $u_t + au_x = 0$ the characteristics are the lines $x = \xi + at$ and $u(x, t) = u_0(x - at)$: the profile moves unchanged with speed $a$. The [CFL condition](/courant-friedrichs-lewy-condition/) says that an explicit grid scheme must contain this foot in its stencil, and the [upwind scheme](/upwind-scheme/) at $\nu \le 1$ is exactly linear interpolation at the foot.

**Variable speed, semi-Lagrangian.** $u_t + a(x)u_x = 0$ with $a(x) = 1 + \frac12\sin 2\pi x$ on $[0, 1]$ periodic, $u_0(x) = e^{-100(x - 0.5)^2}$, $T = 1$. Feet by one RK4 step, cubic Lagrange interpolation, reference solution by tracing back with 2000 RK4 steps. Max errors:

| $\Delta x$ | 1/50 | 1/100 | 1/200 | 1/400 |
|---|---|---|---|---|
| $\Delta t = 0.5\Delta x$ | $1.28 \cdot 10^{-1}$ | $3.11 \cdot 10^{-2}$ | $5.11 \cdot 10^{-3}$ | $6.81 \cdot 10^{-4}$ |
| $\Delta t = 5\Delta x$ | $2.56 \cdot 10^{-2}$ | $4.02 \cdot 10^{-3}$ | $5.48 \cdot 10^{-4}$ | $6.97 \cdot 10^{-5}$ |

The ratios approach $8$, order 3, as $\Delta x^4/\Delta t$ predicts with $\Delta t \propto \Delta x$. With Courant numbers up to $7.5$ the scheme is stable and ten times more accurate, because it interpolates ten times less often. An explicit Eulerian scheme would be unstable there.

**Burgers' equation and wave breaking.** For $u_t + uu_x = 0$, $u$ is constant along characteristics and they are straight lines $x = \xi + u_0(\xi)t$. With $u_0(x) = e^{-x^2}$, solving $\xi + tu_0(\xi) = x$ by bisection gives at $t = 1$: $u(0, 1) = 0.652919$ (from $\xi = -0.652919$), $u(1, 1) = 1$ (the peak, from $\xi = 0$), $u(1.5, 1) = 0.170953$. Two characteristics meet first at $t^* = 1/\max_\xi(-u_0'(\xi)) = e^{1/2}/\sqrt2 = 1.16582$, where $u_x$ becomes infinite; after that the method of characteristics gives a multivalued profile and the physical solution has a shock.

**The wave equation.** $u_{tt} = c^2u_{xx}$ as a first-order system for $(u_t, u_x)$ has the characteristic variables $u_t \mp cu_x$, constant along $x \pm ct = $ const. This gives d'Alembert's formula $u = F(x - ct) + G(x + ct)$.

**Rays for the eikonal equation.** For $|\nabla T| = 1/c(x)$, the characteristic strips are the rays of geometric optics, $\dot x = c^2 p$, $\dot p = -\nabla c / c$ with $p = \nabla T$. Ray tracing is used in seismology; grid methods such as the [fast marching method](/fast-marching-method/) avoid the caustics where rays cross.

## Variations

- **Characteristic grids (Hartree, Courant-Isaacson-Rees).** For a hyperbolic $2 \times 2$ system, build the grid from intersecting characteristics of both families and step along them; accurate but awkward with shocks and in several dimensions.
- **Semi-Lagrangian methods.** Fixed grid, backward trajectories, interpolation; the standard transport scheme in many weather and climate models, often with semi-implicit treatment of the fast gravity waves. Monotone variants use limited or shape-preserving interpolation.
- **Eulerian-Lagrangian localized adjoint methods and characteristic Galerkin.** Finite element versions that integrate along characteristics in space-time and can be made mass conservative.
- **Godunov and upwind schemes.** Use the characteristic decomposition locally at each cell face, via the solution of a Riemann problem, without tracing characteristics over long times.
- **Lagrangian particle methods.** Move particles with the flow and never interpolate back to a fixed grid, as in [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/).

## Pitfalls

- **Crossing characteristics.** After $t^*$ the formula $u = Z(t; \xi(x, t))$ is multivalued. The weak solution has a shock whose speed comes from the Rankine-Hugoniot condition, not from the characteristics.
- **Gaps.** At a jump in increasing data, characteristics fan out and leave a wedge with no characteristic; the solution there is a rarefaction wave, which a code that only follows characteristics from grid points misses.
- **Conservation.** A semi-Lagrangian scheme with ordinary interpolation does not conserve $\int u\,dx$ exactly; conservative remapping variants are needed for tracers in long simulations.
- **Interpolation overshoots.** Cubic interpolation produces new maxima and minima near steep gradients, like any linear scheme of order above 1; use limited interpolation when positivity matters.
- **Small Courant numbers hurt.** The interpolation error is made once per step, so taking smaller steps makes a semi-Lagrangian scheme less accurate, as the table shows.

## Exercises

1. Solve $u_t + xu_x = -u$, $u(x, 0) = u_0(x)$ by characteristics.
2. Show that for $u_t + uu_x = 0$ the first crossing time is $t^* = 1/\max(-u_0')$ when $u_0'$ takes negative values, and is infinite otherwise.
3. Show that the semi-Lagrangian scheme with linear interpolation and exact feet is the upwind scheme when $0 \le \nu \le 1$, and is a shifted upwind scheme for larger $\nu$. Show it is stable in the max norm for all $\nu$.
4. For the shallow water equations $h_t + (hu)_x = 0$, $(hu)_t + (hu^2 + \frac12gh^2)_x = 0$, find the Riemann invariants $u \pm 2\sqrt{gh}$ and their characteristic speeds $u \pm \sqrt{gh}$.

## References
