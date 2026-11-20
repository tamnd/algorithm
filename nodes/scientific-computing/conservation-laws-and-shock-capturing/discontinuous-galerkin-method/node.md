---
tag: TAT3SX
kind: algorithm
slug: discontinuous-galerkin-method
name: Discontinuous Galerkin method
aliases:
- DG method
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: "Space discretization with a polynomial of degree k in each cell and no continuity between cells, coupled only by numerical fluxes on faces. Conservative; order k + 1 for smooth solutions."
solves: [advection-equation, burgers-equation, linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {M: "the number of cells", k: "the polynomial degree", N: "the number of time steps"}
  time: {worst: "Θ(N M (k+1)^2)"}
  space: {extra: "Θ(M (k+1))"}
properties: {deterministic: true, explicit: true, conservative: true, order: "k + 1 for smooth solutions (measured; k + 1/2 proved in general)", local: true}
history:
  year: 1973
  people: [W. H. Reed, T. R. Hill, P. Lesaint, P.-A. Raviart, B. Cockburn, C.-W. Shu]
  note: Reed and Hill (1973) introduced the method for the steady neutron transport equation. Lesaint and Raviart (1974) gave the first error analysis, and Cockburn and Shu (1989 to 1998) extended it to nonlinear conservation laws.
prereqs: [galerkin-method, finite-volume-method, legendre-polynomials]
see_also: [runge-kutta-discontinuous-galerkin, godunov-method, strong-stability-preserving-runge-kutta, gauss-legendre-quadrature, spectral-element-method, symmetric-interior-penalty-galerkin, hybridizable-discontinuous-galerkin, weno-scheme]
sources:
  - book: isbn:9780387720654
    title: Jan S. Hesthaven and Tim Warburton, Nodal Discontinuous Galerkin Methods, Springer, 2008 (Texts in Applied Mathematics 54)
    locator: Chapters 2 to 5 (the key ideas, the method in one dimension, stability and error estimates, nonlinear problems)
  - paper: doi:10.1023/A:1012873910884
    title: Bernardo Cockburn and Chi-Wang Shu, Runge-Kutta discontinuous Galerkin methods for convection-dominated problems, Journal of Scientific Computing 16(3) (2001) 173-261
    locator: the scalar one-dimensional case, the L2 stability of the semi-discrete method, the error estimates
  - paper: "W. H. Reed and T. R. Hill, Triangular mesh methods for the neutron transport equation, Los Alamos Scientific Laboratory report LA-UR-73-479, 1973"
    locator: the method for the steady neutron transport equation on triangles
  - paper: "P. Lesaint and P.-A. Raviart, On a finite element method for solving the neutron transport equation, in C. de Boor (ed.), Mathematical Aspects of Finite Elements in Partial Differential Equations, Academic Press, 1974, 89-123"
    locator: the first error analysis
  - paper: doi:10.1090/S0025-5718-1986-0815828-4
    title: Claes Johnson and Juhani Pitkäranta, An analysis of the discontinuous Galerkin method for a scalar hyperbolic equation, Mathematics of Computation 46(173) (1986) 1-26
    locator: the L2 error estimate of order k + 1/2
  - paper: doi:10.1137/0728006
    title: Todd E. Peterson, A note on the convergence of the discontinuous Galerkin method for a scalar hyperbolic equation, SIAM Journal on Numerical Analysis 28(1) (1991) 133-140
    locator: a family of meshes on which the order k + 1/2 is sharp
---

The discontinuous Galerkin (DG) method discretizes a conservation law $u_t + f(u)_x = 0$ in space with a polynomial of degree $k$ in each cell and no continuity condition between cells. Each cell does a [Galerkin](/galerkin-method/) projection of the equation onto its own polynomials, and integration by parts puts a flux on each face. Because the two sides of a face have different values there, that flux is a numerical flux $\hat F(u^-, u^+)$, the same as in a [finite volume](/finite-volume-method/) scheme. This is the only coupling between cells. With $k = 0$ the method is the first-order Godunov-type finite volume scheme. With degree $k$ the error for smooth solutions on regular meshes is of order $k + 1$. The mass matrix is block diagonal, the method is conservative, and $hp$ adaptivity and unstructured meshes are natural. This page is about the space discretization. The time stepping and the limiter that make it work for shocks are on [Runge-Kutta discontinuous Galerkin](/runge-kutta-discontinuous-galerkin/).

## In plain words

Cut the line into cells. In each cell, describe the unknown by a short polynomial, such as a line or a parabola, chosen on its own. The polynomial of one cell does not have to meet the polynomial of the next cell, so at each wall there are two values. A rule picks one flow through the wall from those two values, usually the value that comes from upstream. Each cell then changes its polynomial so that, on average against every shape it can represent, the equation holds, with that wall flow as the only input from the neighbours. Higher degree polynomials give much better accuracy for the same number of cells, and each cell only talks to its direct neighbours, which suits parallel computers.

## The problem

Given a flux $f$, periodic initial data $u_0$ on $[x_L, x_R]$ and a final time $T$, approximate the solution of $u_t + f(u)_x = 0$ with $M$ cells $C_j = [x_{j-1/2}, x_{j+1/2}]$ of width $\Delta x$. On $C_j$ write $\xi = 2(x - x_j)/\Delta x \in [-1, 1]$ and

$$u_h(x, t) = \sum_{l=0}^{k} U_{j,l}(t)\, P_l(\xi),$$

with $P_l$ the [Legendre polynomials](/legendre-polynomials/). Then $U_{j,0}$ is the cell average. Multiply the equation by $P_l$, integrate over $C_j$ and integrate by parts. With $\int_{C_j} P_l P_m\,dx = \frac{\Delta x}{2l+1}\delta_{lm}$, $P_l(1) = 1$ and $P_l(-1) = (-1)^l$, the semi-discrete system is

$$\frac{dU_{j,l}}{dt} = \frac{2l+1}{\Delta x}\Big(\int_{-1}^{1} f(u_h)\,P_l'(\xi)\,d\xi - \hat F_{j+1/2} + (-1)^l \hat F_{j-1/2}\Big), \qquad \hat F_{j+1/2} = \hat F(u^-_{j+1/2}, u^+_{j+1/2}).$$

The face traces are $u^-_{j+1/2} = \sum_l U_{j,l}$ and $u^+_{j+1/2} = \sum_l (-1)^l U_{j+1,l}$. The flux must be consistent, $\hat F(u, u) = f(u)$. The usual choices are the upwind flux for $f(u) = au$ and a monotone flux such as Godunov's or [Rusanov's](/rusanov-flux/) for nonlinear $f$.

## The algorithm

```pseudo id=main
DG(U, Δx, Δt, T, f, F̂)
L1  repeat SSP-RK3 steps until t = T, each stage computing R ← DG-OPERATOR(U)
    DG-OPERATOR(U):
L2      for each face j+1/2 do u⁻ ← Σ_l U_(j,l);  u⁺ ← Σ_l (-1)^l U_(j+1,l)
L3          F_(j+1/2) ← F̂(u⁻, u⁺)
L4      for each cell j and each degree l = 0, ..., k do
L5          V ← Σ_q w_q f(u_h(ξ_q)) P_l'(ξ_q)                 ▷ Gauss rule with k+1 points
L6          R_(j,l) ← ((2l+1)/Δx) (V - F_(j+1/2) + (-1)^l F_(j-1/2))
L7      return R
```

Line L1 is the method of lines. Any stable ODE solver works for a smooth solution. The usual choice is the three-stage [SSP Runge-Kutta](/strong-stability-preserving-runge-kutta/) method of Shu and Osher with $a\,\Delta t/\Delta x \le 1/(2k+1)$ (a common rule, not a sharp bound). Lines L2 and L3 do one flux evaluation per face. Lines L4 to L6 are local to each cell: the volume integral $V$ uses a [Gauss-Legendre rule](/gauss-legendre-quadrature/) with $k + 1$ points, which is exact when $f$ is linear and, for $f(u) = u^2/2$, when $k \le 2$. The initial coefficients are the $L^2$ projection $U_{j,l} = \frac{2l+1}{2}\int_{-1}^{1} u_0\,P_l\,d\xi$.

With $k = 0$, L5 gives $V = 0$ and L6 is the finite volume update $-(\hat F_{j+1/2} - \hat F_{j-1/2})/\Delta x$. With the upwind flux this is the [upwind scheme](/upwind-scheme/).

## Example

**One evaluation by hand.** Take $f(u) = u$ (advection with $a = 1$), the upwind flux, $k = 1$, two periodic cells with $\Delta x = \tfrac12$, and $U_0 = (1, \tfrac12)$, $U_1 = (0, \tfrac14)$. So $u_h = 1 + \tfrac12\xi$ on the first cell and $\tfrac14\xi$ on the second.

- Traces: the first cell has $u^- = 1.5$ on its right face, and the second cell has $u^- = 0.25$ on its right face (which is the left face of the first cell, by periodicity). The upwind fluxes are $\hat F_{1/2} = 1.5$ and $\hat F_{3/2} = \hat F_{-1/2} = 0.25$.
- Volume terms: $P_0' = 0$, $P_1' = 1$, so $V = \int_{-1}^{1} u_h\,d\xi$ is $2$ for the first cell and $0$ for the second.
- First cell: $R_{0,0} = 2(0 - 1.5 + 0.25) = -2.5$ and $R_{0,1} = 6(2 - 1.5 - 0.25) = 1.5$.
- Second cell: $R_{1,0} = 2(0 - 0.25 + 1.5) = 2.5$ and $R_{1,1} = 6(0 - 0.25 - 1.5) = -10.5$.

The averages change at rates $-2.5$ and $2.5$, so the total mass is constant. The energy rate is $\sum \frac{\Delta x}{2l+1}U_{j,l}R_{j,l} = -1.25 + 0.125 - 0.4375 = -1.5625$. The jumps $u^- - u^+$ at the two faces are $1.5 - (-0.25) = 1.75$ and $0.25 - 0.5 = -0.25$, and $-\tfrac12(1.75^2 + 0.25^2) = -1.5625$. This is the energy identity of the next section.

**Refinement study (measurement).** $u_0 = \sin 2\pi x$ on $[0, 1]$, $a = 1$, $T = 0.5$, SSP-RK3 with $\Delta t = 0.9\,\Delta x/(2k+1)$, $L^2$ error by an 8-point Gauss rule in each cell:

| $M$ | $k = 0$ | $k = 1$ | $k = 2$ |
|---|---|---|---|
| 8 | 5.232e-1 | 2.883e-2 | 1.702e-3 |
| 16 | 3.349e-1 | 6.808e-3 | 2.118e-4 |
| 32 | 1.918e-1 | 1.671e-3 | 2.645e-5 |
| 64 | 1.030e-1 | 4.155e-4 | 3.305e-6 |
| $p_{\text{obs}}$ (32 to 64) | 0.90 | 2.01 | 3.00 |

The observed order is $k + 1$. With $k = 2$, 16 cells give a smaller error than 64 cells with $k = 1$. For $k = 0$ the rate is still rising toward 1 on these coarse grids.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It derives the cell equations from the weak form, shows that the $l = 0$ equation is a conservative finite volume update so the total mass changes only through the boundary, and proves the energy identity for $f(u) = au$ with the upwind flux: $\frac{d}{dt}\tfrac12\|u_h\|^2 = -\tfrac{|a|}{2}\sum_{\text{faces}}(u^- - u^+)^2$. So the semi-discrete method is $L^2$ stable, and the jumps are the only source of dissipation. The error estimates are cited. Lesaint and Raviart (1974) proved order $k$ on general triangulations. Johnson and Pitkäranta (1986) proved order $k + 1/2$ in $L^2$, and Peterson (1991) gave meshes on which $k + 1/2$ is sharp. On uniform and many other meshes the observed order is $k + 1$, as in the table.

## Complexity

One operator evaluation does $M$ flux evaluations and, per cell, $k + 1$ evaluations of $f$ and $(k + 1)^2$ multiply-adds for the volume terms (with the values of $P_l$ and $P_l'$ at the Gauss points tabulated once). That is $\Theta(M(k+1)^2)$ per stage and $\Theta(NM(k+1)^2)$ for $N$ steps of a three-stage method. The memory is $\Theta(M(k+1))$. The mass matrix is diagonal in the Legendre basis, so no linear system is solved. The time step shrinks like $\Delta x/(2k+1)$, so for a fixed $T$, $N = \Theta(M(2k+1))$.

## Properties

- **Conservative.** The cell averages satisfy a finite volume update with the face fluxes $\hat F$ (theorem).
- **Local.** Each cell needs only the traces of its two neighbours, so the method parallelizes well and handles nonconforming and $hp$ meshes.
- **$L^2$ stable** for linear advection with the upwind flux, in the semi-discrete form (theorem). The fully discrete SSP-RK3 method kept the energy nonincreasing in the tests at $\Delta t = 0.1\,\Delta x$ (measurement).
- **Order $k + 1$** for smooth solutions on regular meshes (measurement here; $k + 1/2$ is the general theorem).
- **Not monotone for $k \ge 1$.** Near shocks the polynomials oscillate, so a limiter is needed for nonlinear problems.
- **Superconvergence.** At the downwind face and at the right Radau points, the DG solution of linear advection is more accurate than order $k + 1$ (the observed rate is up to $2k + 1$ at the faces).

## Variants and improvements

- **[RKDG](/runge-kutta-discontinuous-galerkin/).** SSP Runge-Kutta time stepping with a TVB slope limiter (Cockburn and Shu), for shocks.
- **Nodal DG.** Lagrange basis at Gauss-Lobatto or Gauss points instead of Legendre modes (Hesthaven and Warburton 2008). With Gauss-Lobatto points and a diagonal mass matrix this is the DG spectral element method, which has the [summation-by-parts](/summation-by-parts-operators/) property and admits [entropy stable](/entropy-stable-scheme/) forms.
- **Elliptic and diffusive terms.** The [symmetric interior penalty](/symmetric-interior-penalty-galerkin/) method, the local DG method and the [hybridizable DG](/hybridizable-discontinuous-galerkin/) method.
- **Space-time DG** and ADER-DG, which treat time with the same polynomial idea.
- **Limiting by subcells.** Replace troubled cells by a finite volume scheme on subcells, or use [WENO](/weno-scheme/) reconstruction as a limiter.

## When to use it

Use DG for hyperbolic problems that need high order on unstructured or adaptive meshes: wave propagation in electromagnetics and acoustics, compressible flow with smooth regions, and transport. It is local and explicit, so it scales well on parallel machines and GPUs. For problems that are mostly shocks on a Cartesian grid, a finite volume scheme with [WENO](/weno-scheme/) reconstruction is simpler and cheaper per unknown. For elliptic problems a continuous finite element method has fewer unknowns.

## Pitfalls

- **Time step too large.** Explicit DG is stable only for Courant numbers of about $1/(2k+1)$ with SSP-RK3. Using the finite volume CFL number makes the method blow up for $k \ge 1$.
- **Central flux for advection.** The average $\tfrac12(f(u^-) + f(u^+))$ conserves energy, so it gives no dissipation, and in practice it loses one order of accuracy for odd $k$. Use an upwind or monotone flux.
- **Too few quadrature points.** For nonlinear $f$, an inexact volume integral (aliasing) can make an unlimited DG method unstable. Use more points or a split form.
- **Wrong signs at the left face.** The left face enters equation $l$ with the factor $(-1)^l = P_l(-1)$. Mistakes here keep $k = 0$ correct and break $k \ge 1$.
- **No limiter at shocks.** For $k \ge 1$, an unlimited method produces oscillations near discontinuities that do not decay as $\Delta x \to 0$.
- **Initial data by interpolation.** Interpolating $u_0$ instead of projecting it can lower the observed order and puts a different mass in each cell.

## Implementations

## History

Reed and Hill (1973) introduced the method at Los Alamos for the steady neutron transport equation, a linear hyperbolic problem, where the solution in each triangle can be computed cell by cell in the direction of the flow. Lesaint and Raviart (1974) gave the first analysis. Johnson and Pitkäranta (1986) proved the $L^2$ estimate of order $k + 1/2$, and Peterson (1991) showed that it cannot be improved in general. Cockburn and Shu extended the method to nonlinear conservation laws and systems in a series of papers from 1989 to 1998, with Runge-Kutta time stepping and a limiter. Hesthaven and Warburton (2008) is the standard text on nodal DG methods.

## References
