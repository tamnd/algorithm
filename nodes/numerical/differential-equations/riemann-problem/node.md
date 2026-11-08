---
tag: CTARDX
kind: problem
slug: riemann-problem
name: Riemann problem
aliases:
- Riemann initial value problem
- shock tube problem
area: numerical/differential-equations
level: advanced
summary: "A conservation law u_t + f(u)_x = 0 with data equal to u_L for x < 0 and u_R for x > 0. The solution depends on x/t only and is a fan of shocks, rarefactions and contact waves."
model: real-ram
prereqs: [advection-equation, burgers-equation, method-of-characteristics]
see_also: [godunov-method, finite-volume-method, upwind-scheme, total-variation-diminishing, weno-scheme, courant-friedrichs-lewy-condition, wave-equation]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 3 (the Riemann problem for linear systems), Chapter 11 (scalar nonlinear conservation laws, shocks, rarefactions, entropy conditions), Chapter 13 (nonlinear systems, the shallow water Riemann problem, Hugoniot loci and integral curves), Chapter 16 (nonconvex flux and the convex hull construction)
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, American Mathematical Society, 2010
    locator: Section 3.4 (scalar conservation laws, Rankine-Hugoniot, entropy solutions, the Riemann problem), Chapter 11 (systems of conservation laws, Lax's solution of the Riemann problem)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 4 (the exact Riemann solver for the Euler equations), Chapters 9 to 11 (approximate Riemann solvers of Roe, Osher and HLL type)
  - paper: "Peter D. Lax, Hyperbolic systems of conservation laws II, Communications on Pure and Applied Mathematics 10 (1957) 537-566"
    locator: solution of the Riemann problem for small data; Lax entropy condition; doi:10.1002/cpa.3160100406
  - paper: "Bernhard Riemann, Über die Fortpflanzung ebener Luftwellen von endlicher Schwingungsweite, Abhandlungen der Königlichen Gesellschaft der Wissenschaften zu Göttingen 8 (1860)"
    locator: the original problem for gas dynamics
---

The Riemann problem is the initial value problem for a hyperbolic conservation law $u_t + f(u)_x = 0$, $u(x, t) \in \mathbb{R}^m$, with piecewise constant data that jump once: $u(x, 0) = u_L$ for $x < 0$ and $u(x, 0) = u_R$ for $x > 0$. Since both the equation and the data are unchanged by the scaling $(x, t) \to (\alpha x, \alpha t)$, the solution is self-similar, $u(x, t) = w(x/t)$. It consists of at most $m$ waves, each a shock, a rarefaction fan or a contact discontinuity, separating constant states. The Riemann problem is the building block of the [Godunov method](/godunov-method/) and of most [finite volume methods](/finite-volume-method/) for gas dynamics, shallow water and other hyperbolic systems.

## In plain words

Put a wall in a tube, with gas at high pressure on one side and low pressure on the other, and remove the wall at once. What happens next is a Riemann problem. A pressure jump runs into the quiet gas, a smooth expansion runs back into the dense gas, and the boundary between the two original gases drifts in between.

The striking fact is that the pattern only stretches with time: a picture at one second and a picture at two seconds look the same after rescaling. So the whole answer is a short list of waves and their speeds. Many computer methods for flows cut space into cells and solve exactly this small problem at every cell boundary.

## Definition

**Notation.** $u(x, t) \in \mathbb{R}^m$, flux $f : \mathbb{R}^m \to \mathbb{R}^m$ smooth, Jacobian $f'(u)$ with real eigenvalues $\lambda_1(u) \le \dots \le \lambda_m(u)$ and eigenvectors $r_p(u)$ (hyperbolicity). Numerical experiments use cells of width $\Delta x$, a step $\Delta t$ and the Courant number $\nu = \Delta t \max|\lambda| / \Delta x$; errors are measured in the $L^1$ norm in $x$ at a fixed time.

**Weak solutions.** Discontinuous solutions are understood in the weak sense: $\int\!\!\int (u \phi_t + f(u) \phi_x)\,dx\,dt + \int u(x, 0)\phi(x, 0)\,dx = 0$ for all smooth test functions $\phi$ with compact support. A discontinuity moving with speed $s$ is admissible in this sense exactly when the **Rankine-Hugoniot condition** $s\,(u_+ - u_-) = f(u_+) - f(u_-)$ holds.

**Entropy condition.** Weak solutions are not unique, so a selection rule is added. For a $p$-shock, **Lax's condition** asks $\lambda_p(u_-) > s > \lambda_p(u_+)$: characteristics run into the shock from both sides. For scalar equations the equivalent general form is Oleinik's chord condition, and Kruzhkov's entropy inequalities $|u - k|_t + (\operatorname{sgn}(u - k)(f(u) - f(k)))_x \le 0$ for every constant $k$ single out a unique solution (Kruzhkov 1970).

**The task.** Given $f$, $u_L$ and $u_R$, find the entropy solution $w(\xi)$, $\xi = x/t$, as a list of waves with their speeds and the intermediate states. A numerical method often only needs the value $w(0)$ on the line $x = 0$, or the flux $f(w(0))$ there.

## Variants

- **Scalar convex flux** ($m = 1$, $f'' > 0$, for example Burgers' $f(u) = u^2/2$). If $u_L > u_R$ the solution is a shock with speed $s = (f(u_L) - f(u_R))/(u_L - u_R)$. If $u_L < u_R$ it is a rarefaction fan: $w(\xi) = u_L$ for $\xi \le f'(u_L)$, $w(\xi) = (f')^{-1}(\xi)$ in between, $w(\xi) = u_R$ for $\xi \ge f'(u_R)$.
- **Scalar nonconvex flux** (for example the Buckley-Leverett flux in oil reservoir models). The solution comes from the convex hull of $f$ on $[u_L, u_R]$ when $u_L < u_R$ (concave hull when $u_L > u_R$): linear parts of the hull are shocks, curved parts are rarefactions, and compound waves (a shock attached to a fan) appear.
- **Linear systems** $u_t + A u_x = 0$. Expand $u_R - u_L = \sum_p \alpha_p r_p$ in eigenvectors of $A$. Then $w(\xi) = u_L + \sum_{\lambda_p < \xi} \alpha_p r_p$: $m$ jumps moving with speeds $\lambda_p$. This is exact and costs one eigen-decomposition.
- **Nonlinear systems** such as the Euler equations of gas dynamics ($m = 3$) and the shallow water equations ($m = 2$). Each wave family is either genuinely nonlinear (shocks or rarefactions) or linearly degenerate (contact discontinuities). The intermediate states solve a nonlinear equation, usually for the pressure or the depth.
- **Generalized Riemann problems** take piecewise smooth (for example linear) data on each side, as needed by higher-order ADER schemes; and multidimensional Riemann problems take four constant states in the quadrants.

## Examples

**Burgers shock.** $u_L = 1$, $u_R = 0$: a shock with speed $s = \frac12$, so $w(\xi) = 1$ for $\xi < \frac12$ and $0$ after.

**Burgers rarefaction and an entropy violating solution.** $u_L = -1$, $u_R = 1$: the entropy solution is the fan $w(\xi) = \xi$ for $|\xi| \le 1$. The stationary jump $u = -1$ for $x < 0$, $u = 1$ for $x > 0$ satisfies Rankine-Hugoniot with $s = 0$, so it is also a weak solution, but it violates Lax's condition ($\lambda(u_-) = -1 < 0 < 1 = \lambda(u_+)$) and is unstable. Numerical schemes can pick the wrong one. On $[-1, 1]$ at $t = 0.5$ with Courant number 0.9, Godunov's scheme gives $L^1$ errors $0.053$, $0.033$, $0.020$, $0.012$ for $M = 50, 100, 200, 400$ cells, converging to the fan; a Roe-flux upwind scheme keeps the initial jump exactly, with error $0.500$ for every $M$ (observed). On the shock data both schemes give the same errors, $0.016$ to $0.0016$.

**Dam break in shallow water.** $h_t + (hu)_x = 0$, $(hu)_t + (hu^2 + \frac12 g h^2)_x = 0$ with $g = 1$, $h_L = 2$, $h_R = 1$, $u_L = u_R = 0$. The middle state solves $u_L + 2(\sqrt{g h_L} - \sqrt{g h_m}) = u_R + (h_m - h_R)\sqrt{\frac g2(\frac1{h_m} + \frac1{h_R})}$, giving $h_m = 1.45384$ and $u_m = 0.41692$. The solution is a rarefaction moving left between speeds $-\sqrt{2} = -1.41421$ and $u_m - \sqrt{g h_m} = -0.78883$, and a shock moving right with speed $(h_m u_m)/(h_m - h_R) = 1.33557$.

**Sod's shock tube.** For the Euler equations with $(\rho, v, p) = (1, 0, 1)$ on the left and $(0.125, 0, 0.1)$ on the right, $\gamma = 1.4$, the solution is a left rarefaction, a contact discontinuity and a right shock; it is the standard test for gas dynamics codes (Sod 1978; Toro, Chapter 4).

## Known algorithms

- **Exact solution for scalar laws.** Closed form for convex $f$ (shock speed or inverse of $f'$); for nonconvex $f$, the convex hull construction, computable in $O(n)$ time for $f$ sampled at $n$ points.
- **Exact solution for linear systems.** Eigen-decomposition of $A$ and the formula above.
- **Exact iterative solvers for nonlinear systems.** For gas dynamics and shallow water, solve one scalar equation for the middle pressure or depth by Newton's method or bisection, then fill in the waves (Godunov 1959; Toro, Chapter 4).
- **Approximate Riemann solvers.** The Roe solver solves a linearized problem $u_t + \hat A(u_L, u_R) u_x = 0$; the HLL and HLLC solvers keep only two or three waves with estimated speeds; the Rusanov (local Lax-Friedrichs) flux keeps one speed. They cost $O(m^2)$ or $O(m)$ per interface instead of an iteration, and some need an entropy fix at transonic rarefactions.
- **Front tracking and Glimm's random choice method** assemble solutions of general data from Riemann solutions; Glimm (1968) used this to prove existence for systems with small total variation.

## Bounds

- **Existence and uniqueness, scalar case (proved).** For any $u_L$, $u_R$ and any smooth $f$, there is a unique entropy solution in Kruzhkov's sense, and it is self-similar.
- **Systems, small data (proved).** If the system is strictly hyperbolic and each field is genuinely nonlinear or linearly degenerate, then for $|u_R - u_L|$ small enough the Riemann problem has a unique solution made of $m$ elementary waves satisfying Lax's condition (Lax 1957).
- **Large data.** Existence can fail or need extra conditions: for the Euler equations the solution exists unless the data generate vacuum, which happens when $v_R - v_L \ge \frac{2}{\gamma - 1}(c_L + c_R)$ with sound speeds $c_L, c_R$ (Toro, Section 4.3).
- **Finite speed.** All waves lie in the cone $\min_u \lambda_1 \le x/t \le \max_u \lambda_m$; this bounds the time step of Godunov-type schemes by the [CFL condition](/courant-friedrichs-lewy-condition/) $\nu \le 1$.
- **No growth of variation (scalar).** The total variation of the entropy solution never exceeds $|u_R - u_L|$, and values stay between $u_L$ and $u_R$; schemes built on exact scalar Riemann solutions inherit these properties ([TVD](/total-variation-diminishing/)).

## Reductions

- **Conservation law to Riemann problems.** The Godunov method replaces the solution in each cell by its average, solves a Riemann problem at every interface, and averages again; higher-order methods ([MUSCL, WENO](/weno-scheme/)) do the same with reconstructed interface values.
- **Linear system to scalar advection.** In the eigenbasis, $u_t + Au_x = 0$ splits into $m$ independent [advection equations](/advection-equation/), each with a two-state Riemann problem solved by the [upwind scheme](/upwind-scheme/).
- **Second-order wave equation to a linear system.** The [wave equation](/wave-equation/) in first-order form has the two speeds $\pm c$, so its Riemann problem has two jumps.

## Applications

- **Computational fluid dynamics.** Godunov-type codes for compressible flow, astrophysics, and combustion solve millions of Riemann problems per time step.
- **Shallow water and flood modeling.** Dam breaks, tsunamis and river flows with hydraulic jumps.
- **Traffic flow.** The Lighthill-Whitham-Richards model is a scalar conservation law; queues are shocks and the dissolution of a queue at a green light is a rarefaction.
- **Multiphase flow in porous media.** Buckley-Leverett displacement with a nonconvex flux.
- **Analysis.** Existence theory for systems with small total variation (Glimm, Bressan) is built from Riemann solutions.

## References
