---
tag: YWSH80
kind: concept
slug: pde-classification
name: Classification of PDEs
aliases:
- elliptic, parabolic, hyperbolic
- type of a partial differential equation
area: numerical/differential-equations
level: intro
summary: "A second-order PDE a u_xx + 2b u_xy + c u_yy + ... = 0 is elliptic, parabolic or hyperbolic as b^2 - ac is negative, zero or positive. The type decides the data and the method."
prereqs: []
see_also: [heat-equation, poisson-equation, wave-equation, advection-equation, method-of-characteristics, boundary-conditions, courant-friedrichs-lewy-condition, finite-difference-method]
sources:
  - book: isbn:9780470054567
    title: Walter A. Strauss, Partial Differential Equations, An Introduction, second edition, Wiley, 2008
    locator: Section 1.6 (types of second order equations)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Appendix E (partial differential equations, classification of differential equations)
  - book: isbn:9780471504399
    title: Richard Courant and David Hilbert, Methods of Mathematical Physics, Volume II, Partial Differential Equations, Wiley Classics edition, 1989
    locator: Chapter III (classification of second order equations, normal forms and characteristics)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 1 (introduction, the three model equations)
---

The classification of partial differential equations sorts linear second-order equations into three types, elliptic, parabolic and hyperbolic, by the sign of a discriminant of their highest-order coefficients. The three model equations are the [Poisson equation](/poisson-equation/) (elliptic), the [heat equation](/heat-equation/) (parabolic) and the [wave equation](/wave-equation/) (hyperbolic). The type decides which data give a well-posed problem, how information travels, and which numerical methods work, so it is the first thing to find out about a new PDE.

## In plain words

Three kinds of physical laws behave in three different ways. In a stretched sheet at rest, each point feels all edges of the sheet at once: change one edge and every point moves a little. In a rod that conducts heat, the state moves forward in time, and sharp features smooth out. In a vibrating string, waves travel at a fixed speed: a pluck at one end reaches the other end only after some time, and sharp features stay sharp.

Equations of the first kind need data on the whole boundary and lead to one large system of equations. Equations of the second kind are solved step by step in time, and the steps must be small or the method implicit. Equations of the third kind are also solved step by step, and the step must not let a wave jump over a grid cell.

## The idea

**Two variables.** Consider the linear equation

$$a\, u_{xx} + 2b\, u_{xy} + c\, u_{yy} + d\, u_x + e\, u_y + g\, u = q,$$

where the coefficients are real functions of $(x, y)$ and $a$, $b$, $c$ do not all vanish at the point considered. At a point, the equation is

- **elliptic** if $b^2 - ac < 0$,
- **parabolic** if $b^2 - ac = 0$,
- **hyperbolic** if $b^2 - ac > 0$.

Only the principal part $a u_{xx} + 2b u_{xy} + c u_{yy}$ matters. It corresponds to the symmetric matrix $P = \begin{pmatrix} a & b \\ b & c \end{pmatrix}$, and $b^2 - ac = -\det P$. So the equation is elliptic when $P$ is definite, parabolic when $P$ is singular, and hyperbolic when $P$ has one positive and one negative eigenvalue.

**The type does not depend on the coordinates.** Let $\xi = \xi(x, y)$, $\eta = \eta(x, y)$ be a smooth change of variables with Jacobian matrix $Q$ and $\det Q \ne 0$ at the point. By the chain rule, the second derivatives of $u$ in the new variables have the principal coefficient matrix $Q P Q^T$, and the first-order terms do not change it. So the new discriminant is $-\det(Q P Q^T) = -(\det Q)^2 \det P$, which has the same sign as $b^2 - ac$. The type is a property of the equation, not of the coordinates.

**Characteristics.** A curve $y = y(x)$ is characteristic when its slope $m = dy/dx$ satisfies $a m^2 - 2b m + c = 0$. Along such a curve the equation does not determine all second derivatives of $u$ from the values of $u$ and $u_n$ on the curve, so data given on it are not free. A hyperbolic equation has two real families of characteristics, a parabolic equation has one, and an elliptic equation has none. By a change of variables along the characteristics, each equation takes a canonical form at a point: $u_{\xi\xi} + u_{\eta\eta} + \ldots = 0$ (elliptic), $u_{\xi\xi} + \ldots = 0$ (parabolic) or $u_{\xi\eta} + \ldots = 0$ (hyperbolic), where the dots stand for terms of lower order.

**More variables.** For $\sum_{i, j} a_{ij}\, u_{x_i x_j} + \text{lower order} = 0$ with a symmetric matrix $A = (a_{ij})$ of size $n$, the equation is elliptic when $A$ is definite, and hyperbolic (in the normal sense) when $A$ is nonsingular with $n - 1$ eigenvalues of one sign and one of the other. An equation $u_t = \sum a_{ij} u_{x_i x_j} + \ldots$ with a positive definite $(a_{ij})$ in the space variables is parabolic. Some equations fit none of these classes.

**First-order systems.** A system $u_t + B u_x = 0$, $u \in \mathbb{R}^m$, is hyperbolic when $B$ is diagonalizable with real eigenvalues. The eigenvalues are the speeds of the waves. This is the form in which conservation laws are studied, and the scalar case is the [advection equation](/advection-equation/).

**What the type means.**

| | elliptic | parabolic | hyperbolic |
|---|---|---|---|
| model | $u_{xx} + u_{yy} = q$ | $u_t = \alpha u_{xx}$ | $u_{tt} = c^2 u_{xx}$ |
| data | boundary values on a closed curve | initial values and boundary values | initial values $u$, $u_t$ and inflow boundary values |
| smoothness | solution smooth inside | smooth for $t > 0$ | jumps travel along characteristics |
| speed of information | everywhere at once | infinite, but damped | finite, at most $c$ |
| typical numerics | one large sparse linear system | implicit time steps, $\Delta t$ limit $O(\Delta x^2)$ if explicit | explicit time steps with a [CFL limit](/courant-friedrichs-lewy-condition/) $\Delta t = O(\Delta x)$ |

A problem of the wrong kind is ill posed. The initial value problem for the Laplace equation (Hadamard's example) is the classic case: $u(x, 0) = 0$, $u_y(x, 0) = \sin(kx)/k$ has the solution $u = \sin(kx) \sinh(ky)/k^2$, so data that tend to 0 as $k \to \infty$ give solutions that grow without bound at each fixed $y > 0$. The [backward heat equation](/heat-equation/) is another one.

## Examples

- **Laplace and Poisson.** $u_{xx} + u_{yy} = q$: $a = c = 1$, $b = 0$, so $b^2 - ac = -1$, elliptic.
- **Heat.** $u_t = \alpha u_{xx}$ in the variables $(x, t)$: $a = \alpha$, $b = 0$, $c = 0$, so $b^2 - ac = 0$, parabolic. The only characteristic direction is $t = $ const.
- **Wave.** $c^2 u_{xx} - u_{tt} = 0$ in $(x, t)$: the discriminant is $0 - c^2 \cdot (-1) = c^2 > 0$, hyperbolic, with the characteristics $x \pm c t = $ const.
- **A constant-coefficient example.** $u_{xx} + 4 u_{xy} + 3 u_{yy} = 0$ has $a = 1$, $b = 2$, $c = 3$ and $b^2 - ac = 1$, hyperbolic. The slopes solve $m^2 - 4m + 3 = 0$, so $m = 1$ and $m = 3$, and the characteristics are $y - x = $ const and $y - 3x = $ const. Each $u = F(y - x) + G(y - 3x)$ with $F, G \in C^2$ is a solution: $F(y - x)$ gives $F'' - 4F'' + 3F'' = 0$, and $G(y - 3x)$ gives $9G'' - 12G'' + 3G'' = 0$.
- **Mixed type.** The Tricomi equation $y\, u_{xx} + u_{yy} = 0$ has $b^2 - ac = -y$. It is elliptic for $y > 0$, parabolic on $y = 0$ and hyperbolic for $y < 0$. It models flow around a body near the speed of sound.
- **Advection-diffusion.** $u_t + a u_x = \kappa u_{xx}$ is parabolic for each $\kappa > 0$, but for small $\kappa$ its solutions behave like those of the hyperbolic limit $\kappa = 0$ on the scales a grid can resolve. The type is a statement about the highest derivatives, and the behaviour of a computation also depends on the size of the terms.
- **Not of second order.** The [eikonal equation](/eikonal-equation/) $|\nabla u| = 1$ is a nonlinear first-order equation. It is treated by the [method of characteristics](/method-of-characteristics/) and by upwind schemes, as hyperbolic equations are.

## Where it is used

- **Choice of the method.** Elliptic problems are discretized into one sparse linear system, solved by [multigrid](/multigrid-method/), the [conjugate gradient method](/conjugate-gradient-method/) or fast Poisson solvers. Parabolic problems are solved by the [method of lines](/method-of-lines/) with stiff, often implicit, time integrators such as [Crank-Nicolson](/crank-nicolson-method/). Hyperbolic problems use explicit schemes such as the [upwind scheme](/upwind-scheme/), [Lax-Friedrichs](/lax-friedrichs-scheme/) and [Lax-Wendroff](/lax-wendroff-method/), or [finite volume methods](/finite-volume-method/), under a CFL condition.
- **Choice of the data.** The type tells which [boundary conditions](/boundary-conditions/) make the problem well posed: values on the whole boundary for elliptic problems, initial values plus boundary values for parabolic problems, and initial values plus inflow values for hyperbolic problems.
- **Stability analysis.** [Von Neumann analysis](/von-neumann-stability-analysis/) gives the explicit limits $r = \alpha\Delta t/\Delta x^2 \le 1/2$ for the heat equation and $|\nu| = |a|\Delta t/\Delta x \le 1$ for the advection equation, which come from the parabolic and the hyperbolic scaling.
- **Systems from physics.** The [Navier-Stokes equations](/navier-stokes-equations/) mix the types: the momentum equations are parabolic through viscosity, the incompressibility constraint leads to an elliptic equation for the pressure, and the inviscid limit is hyperbolic.

## References
