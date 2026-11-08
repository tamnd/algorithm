---
tag: X5DDNH
kind: technique
slug: finite-difference-method
name: Finite difference method
aliases:
- finite differences
- finite difference scheme
- FDM
- difference method
area: numerical/differential-equations
level: core
summary: "Put a grid on the domain, replace each derivative by a difference quotient of grid values, and solve the resulting algebraic equations. Consistency plus stability gives convergence."
prereqs: [pde-classification, boundary-conditions, finite-differences]
see_also: [ftcs-method, crank-nicolson-method, upwind-scheme, lax-wendroff-method, von-neumann-stability-analysis, lax-equivalence-theorem, method-of-lines, finite-volume-method]
sources:
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 1 (finite difference approximations, truncation errors, deriving formulas by the method of undetermined coefficients), Chapter 2 (steady states and boundary value problems, local truncation error, stability and convergence in the max-norm), Chapter 3 (elliptic equations, the five-point Laplacian)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 1 (finite difference schemes for hyperbolic equations, consistency and stability), Chapter 10 (convergence and the Lax-Richtmyer equivalence theorem)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 2 (parabolic equations in one space variable, explicit and implicit schemes), Chapter 6 (consistency, convergence and stability)
  - paper: doi:10.1007/BF01448839
    title: Richard Courant, Kurt Friedrichs and Hans Lewy, Über die partiellen Differenzengleichungen der mathematischen Physik, Mathematische Annalen 100 (1928) 32-74
    locator: difference equations on grids as approximations of elliptic, parabolic and hyperbolic problems; the domain of dependence condition
---

The finite difference method solves a differential equation approximately by putting a grid on the domain and replacing each derivative by a difference quotient of the unknown values at nearby grid points. The equation, written at each grid point, becomes a system of algebraic equations: a linear system for a linear [boundary value problem](/bvp-boundary-value-problem/), or a time-stepping rule for an evolution equation such as the [heat equation](/heat-equation/). The error at a grid point depends on two properties: consistency (the difference equation approximates the differential equation) and stability (the discrete problem does not amplify small errors). For linear problems, the two together give convergence, which is the content of the [Lax equivalence theorem](/lax-equivalence-theorem/).

## In plain words

A derivative is a slope: how fast a quantity changes as you move a little. A computer cannot move "a little" in the limit, but it can look at values a short, fixed distance apart and divide their difference by that distance. The finite difference method does this everywhere at once. It lays a regular grid of points over the region, keeps one unknown number at each point, and rewrites the equation at each point using only its neighbours. What comes out is a large but simple set of equations, which a computer can solve. A finer grid gives smaller errors, at a rate fixed by the formulas chosen. But a fine grid does not help on its own: the scheme must also keep small errors from growing, and for time-dependent problems this often limits how large a time step may be.

## When it applies

- The domain is an interval, a rectangle, or another shape that a regular or mapped grid fits well. Curved boundaries and local refinement are awkward; there the [finite element method](/finite-element-method/) or [finite volume method](/finite-volume-method/) is usually easier.
- The solution is smooth enough for the Taylor expansions behind the difference formulas: a formula of order $q$ for a derivative of order $m$ needs about $m + q$ bounded derivatives. Near shocks, kinks and corners the observed order drops.
- The problem is posed with [boundary conditions](/boundary-conditions/) (and initial data, for evolution problems) that can be written as equations at or near the grid ends.
- The cost model is grid points: the work is the cost of solving the discrete system, counted in arithmetic operations per grid point and per time step.

## The template

**Notation.** One space variable $x \in [a, b]$, grid $x_j = a + j\Delta x$ for $j = 0, \ldots, J$ with $\Delta x = (b - a)/J$, and for evolution problems time levels $t^n = n\Delta t$. The unknowns are $U_j \approx u(x_j)$ or $U_j^n \approx u(x_j, t^n)$. The local truncation error $\tau_j$ is the residual left when the exact solution is put into the difference equation, divided so that it is comparable with the differential equation. The global error is $e_j = u(x_j) - U_j$, measured in the max-norm $\|e\|_\infty = \max_j |e_j|$ unless stated otherwise.

```pseudo id=main
FINITE-DIFFERENCE(PDE, domain, data)
L1  choose grid points x_j (and time levels t^n); Δx, Δt are the spacings
L2  for each derivative in PDE choose a stencil D of order q    ▷ hole: the difference formulas
L3  at each interior grid point write PDE with each derivative replaced by its stencil
L4  write each boundary condition as an equation in grid values  ▷ hole: boundary closure
L5  if the problem is steady then
L6      solve the algebraic system A U = F                       ▷ hole: linear or nonlinear solver
L7  else
L8      for n ← 0 to N − 1 do
L9          compute U^(n+1) from U^n by the time-stepping rule    ▷ hole: explicit or implicit in time
L10 return U
```

There are four holes: the stencils (line L2), the boundary closure (L4), the solver for the steady system (L6), and the time discretization (L9). Lines L3 and L4 together define the discrete problem. The analysis has the same three steps every time. First, compute $\tau$ by Taylor expansion of the exact solution (consistency, order $q$). Second, bound the inverse of the discrete operator, or the growth of the time-stepping rule, independently of $\Delta x$ (stability). Third, combine them: the error satisfies the discrete equations with $\tau$ as right-hand side, so $\|e\| \le C\|\tau\|$.

**The basic stencils.** For $u$ smooth, Taylor expansion about $x$ gives, with $h = \Delta x$:

| stencil | formula | leading error term | order |
|---|---|---|---|
| forward difference | $\dfrac{u(x + h) - u(x)}{h}$ | $\tfrac{h}{2}u''(x)$ | 1 |
| backward difference | $\dfrac{u(x) - u(x - h)}{h}$ | $-\tfrac{h}{2}u''(x)$ | 1 |
| centred difference | $\dfrac{u(x + h) - u(x - h)}{2h}$ | $\tfrac{h^2}{6}u'''(x)$ | 2 |
| second difference | $\dfrac{u(x + h) - 2u(x) + u(x - h)}{h^2}$ | $\tfrac{h^2}{12}u''''(x)$ | 2 |
| five-point Laplacian | $\dfrac{U_{i+1,j} + U_{i-1,j} + U_{i,j+1} + U_{i,j-1} - 4U_{i,j}}{h^2}$ | $\tfrac{h^2}{12}(u_{xxxx} + u_{yyyy})$ | 2 |

Each row is "formula = derivative + leading term + higher order terms". Formulas of any order on any set of points follow from the method of undetermined coefficients: ask the weights to make the formula exact on $1, x, \ldots, x^{k}$, which is a small Vandermonde system. Fornberg's algorithm computes the weights stably for arbitrary points.

**Walk-through on a model problem.** Take $-u'' = f$ on $(0, 1)$ with $u(0) = u(1) = 0$. With the second difference at $x_1, \ldots, x_{J-1}$ (lines L2, L3) and $U_0 = U_J = 0$ (line L4), the system (line L6) is

$$\frac{-U_{j-1} + 2U_j - U_{j+1}}{\Delta x^2} = f(x_j), \qquad j = 1, \ldots, J - 1.$$

The matrix $A$ is tridiagonal, symmetric and positive definite, and the [Thomas algorithm](/thomas-algorithm/) solves it in $\Theta(J)$ operations. *Consistency:* $|\tau_j| \le \tfrac{\Delta x^2}{12}M_4$ with $M_4 = \max|u''''|$. *Stability:* $A$ has non-negative inverse entries, and $A^{-1}\mathbf 1 = w$ with $w_j = \tfrac12 x_j(1 - x_j)$, because the second difference of a quadratic is exact. So $\|A^{-1}\|_\infty = \max_j w_j \le \tfrac18$. *Convergence:* the error satisfies $Ae = \tau$, so

$$\|e\|_\infty \le \tfrac18\|\tau\|_\infty \le \frac{M_4}{96}\Delta x^2.$$

This is a proved bound, for $u \in C^4[0, 1]$.

## Classic examples

**Two-point boundary value problem.** For $f(x) = \pi^2\sin(\pi x)$ the exact solution is $u = \sin(\pi x)$ and $M_4 = \pi^4$. With $J = 4$ the computed values at $x = \tfrac14, \tfrac12, \tfrac34$ are $0.744604, 1.053029, 0.744604$, against $0.707107, 1, 0.707107$. Halving $\Delta x$:

| $J$ | $\|e\|_\infty$ | bound $\pi^4/(96J^2)$ | observed order $\log_2(e_{J/2}/e_J)$ |
|---|---|---|---|
| 4 | $5.303 \cdot 10^{-2}$ | $6.342 \cdot 10^{-2}$ | |
| 8 | $1.295 \cdot 10^{-2}$ | $1.585 \cdot 10^{-2}$ | 2.034 |
| 16 | $3.219 \cdot 10^{-3}$ | $3.964 \cdot 10^{-3}$ | 2.008 |
| 32 | $8.036 \cdot 10^{-4}$ | $9.909 \cdot 10^{-4}$ | 2.002 |
| 64 | $2.008 \cdot 10^{-4}$ | $2.477 \cdot 10^{-4}$ | 2.001 |

The observed order tends to 2 and the error stays below the proved bound.

**The heat equation.** For $u_t = \kappa u_{xx}$, the forward difference in time and the second difference in space give the [FTCS method](/ftcs-method/), which is stable in the max-norm iff $r = \kappa\Delta t/\Delta x^2 \le \tfrac12$. The average of the explicit and implicit space differences gives the [Crank-Nicolson method](/crank-nicolson-method/), second order in time and unconditionally stable in the $\ell^2$ norm, at the price of one tridiagonal solve per step.

**Advection.** For $u_t + a u_x = 0$, the one-sided difference against the flow gives the [upwind scheme](/upwind-scheme/), first order and stable for Courant number $|a|\Delta t/\Delta x \le 1$. Centred differences with a second-order Taylor step in time give the [Lax-Wendroff method](/lax-wendroff-method/). Forward time with centred space is unstable for every $\Delta t > 0$, a standard result of [von Neumann analysis](/von-neumann-stability-analysis/).

**Poisson's equation.** The five-point Laplacian on a square grid turns the [Poisson equation](/poisson-equation/) into a sparse system with $(J - 1)^2$ unknowns, solved by [Gauss-Seidel](/gauss-seidel-method/), [successive over-relaxation](/successive-over-relaxation/), the [conjugate gradient method](/conjugate-gradient-method/) or the [multigrid method](/multigrid-method/).

**Numerical differentiation and rounding.** For $u = e^x$ at $x = 1$ in double precision, the forward difference error is $1.36 \cdot 10^{-1}$ at $h = 10^{-1}$, falls to $6.6 \cdot 10^{-9}$ at $h = 10^{-8}$, and rises again to $4.3 \cdot 10^{-4}$ at $h = 10^{-12}$. The centred difference falls from $4.53 \cdot 10^{-3}$ at $h = 10^{-1}$ to about $6 \cdot 10^{-11}$ at $h = 10^{-5}$ and then rises. The truncation error falls like $h^q$, but the rounding error in the numerator, divided by $h$, grows like $\varepsilon/h$ with [machine epsilon](/machine-epsilon/) $\varepsilon$, so the best $h$ is near $\sqrt{\varepsilon}$ for order 1 and near $\varepsilon^{1/3}$ for order 2.

## Variations

- **Method of lines.** Discretize only in space, which gives a system of ODEs $U'(t) = F(U)$, and hand it to an ODE solver ([method of lines](/method-of-lines/)). Stiffness of the space-discretized heat equation (eigenvalues down to about $-4\kappa/\Delta x^2$) then calls for an implicit solver such as [backward Euler](/backward-euler-method/) or the [BDF methods](/backward-differentiation-formulas/).
- **Higher-order and compact stencils.** Wider stencils raise the order; compact (Padé) schemes reach order 4 or 6 on three points by coupling neighbouring derivative values in a tridiagonal system. [Richardson extrapolation](/richardson-extrapolation/) on two grids raises the order of a scheme with an expansion in even powers of $\Delta x$.
- **Nonuniform and mapped grids.** Difference formulas on unequal spacings lose an order unless the spacing varies smoothly; a smooth map from a uniform grid keeps the order.
- **Conservation form.** Writing the scheme as differences of numerical fluxes makes it conservative, the starting point of the [finite volume method](/finite-volume-method/) and of shock-capturing schemes such as [Godunov's method](/godunov-method/).
- **Alternating direction implicit.** In two or more space dimensions, the [ADI method](/adi-method/) splits an implicit step into one-dimensional tridiagonal solves.

## Pitfalls

- **Consistency without stability.** A consistent scheme can diverge: FTCS for the heat equation with $r$ just above $\tfrac12$, or forward-time centred-space for advection at any step. Check stability before trusting the truncation error.
- **Boundary closure of lower order.** A first-order approximation of a Neumann condition can reduce the global order of a second-order interior scheme. It does not always do so, because a boundary truncation error of order $\Delta x$ at one point may contribute only $O(\Delta x^2)$ to the solution, but this must be checked for the scheme at hand.
- **Measuring the order on rough data.** Observed orders on a solution with a kink or a discontinuity are lower than the formal order; choose a smooth test solution.
- **Too small a step in differentiation.** As the table above shows, shrinking $h$ below about $\sqrt\varepsilon$ makes a difference quotient worse.
- **The norm matters.** Stability in $\ell^2$ (von Neumann analysis) does not give stability in the max-norm, and the convergence statement must name its norm.

## Exercises

1. Derive the coefficients and the leading error term of the one-sided formula $u'(x) \approx (-3u(x) + 4u(x + h) - u(x + 2h))/(2h)$.
2. For the model problem, show that $A^{-1}$ has non-negative entries by writing it as a discrete Green's function, and show that $\|A^{-1}\|_\infty \le \tfrac18$.
3. Replace $u(0) = 0$ in the model problem by $u'(0) = 0$ written as $(U_1 - U_0)/\Delta x = 0$, solve $-u'' = \cos(\pi x/2)\pi^2/4$ with $u(1) = 0$, and measure the observed order. Then use a ghost point and the centred difference, and measure it again.
4. Show by Taylor expansion that the forward-time centred-space scheme for $u_t + a u_x = 0$ is consistent of order 1 in time and 2 in space, and find its amplification factor.

## References
