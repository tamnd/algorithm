---
tag: 40T9VJ
kind: algorithm
slug: nessyahu-tadmor-scheme
name: Nessyahu-Tadmor central scheme
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: A second order central scheme on staggered cells that needs no Riemann solver and no characteristic decomposition.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, riemann-solver-free: true, order: "2 on smooth solutions away from extrema", tvd: "for linear advection with Courant number at most 1/2", positive: "not guaranteed"}
history:
  year: 1990
  people: [Haim Nessyahu, Eitan Tadmor]
  note: Nessyahu and Tadmor (1990) extended the staggered Lax-Friedrichs scheme to second order with limited piecewise linear data and a midpoint rule in time.
prereqs: [lax-friedrichs-scheme, muscl-scheme, total-variation-diminishing]
see_also: [kurganov-tadmor-scheme, rusanov-flux, godunov-method, finite-volume-method, courant-friedrichs-lewy-condition, eno-scheme]
sources:
  - paper: "Haim Nessyahu and Eitan Tadmor, Non-oscillatory central differencing for hyperbolic conservation laws, Journal of Computational Physics 87(2) (1990) 408-463"
    locator: the staggered second order central scheme with limited slopes and the midpoint rule for the flux; doi:10.1016/0021-9991(90)90260-8
  - paper: "Alexander Kurganov and Eitan Tadmor, New high-resolution central schemes for nonlinear conservation laws and convection-diffusion equations, Journal of Computational Physics 160(1) (2000) 241-282"
    locator: the numerical viscosity of the staggered scheme at small time steps and the semi-discrete scheme that removes this limit; doi:10.1006/jcph.2000.6459
---

The Nessyahu-Tadmor scheme is a second order finite volume scheme for [hyperbolic conservation laws](/hyperbolic-conservation-law/) that needs no Riemann solver, no eigenvectors and no flux Jacobian. It works on two grids. Each step takes the averages over the cells of one grid and computes averages over the cells of a grid shifted by half a cell, whose cells straddle the faces of the old grid. The flux is needed only at the old cell centers, where the solution is smooth for a short time, so no Riemann problem appears. With constant data in each cell it is the staggered [Lax-Friedrichs scheme](/lax-friedrichs-scheme/); with limited straight lines, as in [MUSCL](/muscl-scheme/), it is second order.

## In plain words

Upwind schemes put a cell face at each jump and ask a Riemann solver what happens there. This scheme moves the cell instead: the new cell runs from the center of one old cell to the center of the next, so the jump between the old cells sits in the middle of the new cell. The new average is the mass already in that range, plus the flux in at the left center, minus the flux out at the right center. Near the old centers the solution stays smooth during one step if the time step is short enough, so these fluxes are easy to get from a Taylor step. The next step moves back to the old grid.

## The problem

Given cell averages $U_j$ of $U_t + F(U)_x = 0$ on a uniform grid with width $\Delta x$, compute averages at $t + \Delta t$ that are second order where the solution is smooth and free of oscillations at shocks, using only the flux $F$. The page uses scalar laws and the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$ and $\gamma = 1.4$. The values are cell averages, so errors are measured against exact cell averages.

## The algorithm

```pseudo id=main
NT-STAGGERED-STEP(U, λ = Δt/Δx, F, θ)
L1  add two ghost cells on each side (copy for outflow, wrap for periodic)
L2  for each cell j: U'_j <- S(U_{j-1}, U_j, U_{j+1});  F'_j <- S(F(U_{j-1}), F(U_j), F(U_{j+1}))
L3      U_j^{n+1/2} <- U_j - (λ/2) F'_j                                    ▷ Taylor step to the midpoint in time
L4  for each j: W_{j+1/2} <- (U_j + U_{j+1})/2 + (U'_j - U'_{j+1})/8 - λ(F(U_{j+1}^{n+1/2}) - F(U_j^{n+1/2}))
L5  the next step applies lines L1 to L4 to W, which gives averages over the original cells
```

$S(a, b, c) = \mathrm{minmod}(\theta(b - a), (c - a)/2, \theta(c - b))$ is the limited slope, computed per component, with $1 \le \theta \le 2$. The value $W_{j+1/2}$ is the average over $[x_j, x_{j+1}]$, the interval between two old cell centers. The first two terms of line L4 are the exact average of the old piecewise linear data over this interval. The last term is the midpoint rule in time for the fluxes at $x_j$ and $x_{j+1}$. Line L2 applies the limiter to the flux values, so no Jacobian is needed. The code takes two staggered steps with the same $\Delta t = 0.4\,\Delta x/\max_j(|u_j| + c_j)$, so that the result is on the original grid, and uses $\theta = 1.5$ by default.

## Example

**One step by hand.** Take $u_t + u_x = 0$, $\theta = \frac32$, $\lambda = \frac14$, outflow boundaries and $u = (0, 0, 1, 3, 4, 4)$. For $f(u) = cu$, line L4 becomes

$$W_{j+1/2} = \big(\tfrac12 + \nu\big)u_j + \big(\tfrac12 - \nu\big)u_{j+1} + \kappa(u'_j - u'_{j+1}), \qquad \nu = \lambda c, \quad \kappa = \tfrac{1 - 4\nu^2}{8}.$$

Here $\nu = \frac14$ and $\kappa = \frac3{32}$. The slopes are $u'_3 = u'_4 = \frac32$ and zero elsewhere. For the interval between cells 2 and 3, $W = \frac34\cdot 0 + \frac14\cdot 1 + \frac3{32}(0 - \frac32) = \frac7{64}$. All the values are $(0, \frac7{64}, \frac32, \frac{217}{64}, 4, 4)$, and the step back gives $(0, \frac{49}{4096}, \frac{1305}{4096}, \frac{8359}{4096}, \frac{14863}{4096}, 4)$. The test checks both lists exactly in `Fraction` arithmetic. At $\nu = \frac12$, $\kappa = 0$ and $W_{j+1/2} = u_j$: the scheme moves the data exactly by half a cell.

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$, outflow boundaries and Courant number 0.4, the scheme runs to $t = 0.2$. These $L^1$ density errors against exact cell averages are measurements made with the code on this page.

| cells $M$ | staggered steps | $\theta = 1$ | $\theta = 1.5$ | $\theta = 2$ |
|---|---|---|---|---|
| 100 | 108 to 110 | 0.007331 | 0.005485 | 0.005456 |
| 200 | 218 to 220 | 0.004301 | 0.002955 | 0.002956 |
| 400 | 438 to 440 | 0.002405 | 0.001447 | 0.001446 |

At this Courant number the errors are lower than those of the [Kurganov-Tadmor scheme](/kurganov-tadmor-scheme/) with Heun's method (0.007000 at $M = 100$, $\theta = 1.5$), and close to [MUSCL-Hancock](/muscl-scheme/) with HLLC and minmod (0.00585).

**A smooth wave.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid to $t = 0.1$, the $L^1$ density errors at $M = 25, 50, 100$ are 0.0017865, 0.0004384 and 0.0001011, so the observed orders are 2.03 and 2.12. For $u_t + u_x = 0$ with the averages of $\sin(2\pi x)$, $\nu = 0.4$, $\theta = 1.5$ and one period, the $L^1$ errors at $M = 20, 40, 80, 160$ are 0.022273, 0.005769, 0.001386 and 0.000327 (orders 1.95, 2.06, 2.08).

**Small time steps add viscosity.** In the same advection problem with $M = 40$, the $L^1$ errors at the Courant numbers 0.4, 0.2, 0.1 and 0.05 are 0.005769, 0.017103, 0.029484 and 0.046198. Each step averages neighbors through the term $\frac12(u_j + u_{j+1})$, and more steps mean more averaging. The Kurganov-Tadmor scheme removes this: its error changes by about 1 percent over the same range.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the scheme is conservative and consistent, so by the [Lax-Wendroff theorem](/lax-wendroff-theorem/) bounded $L^1$ limits are weak solutions. For linear advection with $|\nu| \le \frac12$ and $1 \le \theta \le 2$, each staggered value is a convex combination of two values that both lie between $u_j$ and $u_{j+1}$, and each of the two sequences of such values has total variation at most $TV(u)$. So the scheme is [TVD](/total-variation-diminishing/) and makes no new extrema.

TVD for nonlinear laws and positivity for the Euler equations are not proved here. The tests check TVD for Burgers' equation on one step problem, which is a measurement.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: one staggered step costs $O(mM)$ operations: two limiter calls per component and cell, one flux evaluation per cell at the old data and one at the midpoint value. It keeps $O(mM)$ numbers. A fixed end time at a fixed Courant number needs $K = O(M)$ steps, so the total is $O(mM^2)$. The code evaluates the flux at each midpoint value twice, once for each staggered cell that uses it, which costs a constant factor only.

## Properties

- **No Riemann solver and no Jacobian.** Only $F$ is needed. The time step needs an upper bound for the wave speeds.
- **Second order on smooth solutions.** Measured above: orders about 2 on smooth advection and on the Euler wave.
- **Conservative.** Exact in rational arithmetic; the test checks it in `Fraction` for Burgers' equation.
- **TVD for linear advection** with $|\nu| \le \frac12$. Proved.
- **Viscosity grows as $\Delta t$ falls.** Measured above. This rules out a semi-discrete form and makes the scheme poor for problems that force small time steps, such as stiff source terms or diffusion.
- **Two grids.** The averages alternate between the original grid and the staggered grid, so boundary conditions and output need care.

## Variants and improvements

- **Kurganov-Tadmor scheme.** Uses local wave speeds to make the staggered cells narrow, then lets $\Delta t \to 0$, which gives a semi-discrete non-staggered scheme without the $1/\Delta t$ viscosity.
- **Higher order central schemes.** Piecewise quadratic or [ENO](/eno-scheme/) reconstructions on the staggered grid give third order and higher central schemes.
- **Multi-dimensional staggered schemes.** The same idea works on two staggered grids in two dimensions, with averages over cells centered at the old cell corners.

## When to use it

Use it for a simple second order shock capturing scheme when a Riemann solver is not available, the time step is limited only by the Courant condition, and staggered output is acceptable. If small time steps are needed, or the code is built around the method of lines, use the Kurganov-Tadmor scheme instead.

## Pitfalls

- **Courant number above one half.** The fluxes at the old cell centers stay smooth only if waves from the neighbor faces do not reach the centers during the step, which needs $\lambda\max|f'| \le \frac12$. The test of TVD uses this bound.
- **Mixing up the grids.** After an odd number of steps the values are averages over the staggered cells. Taking two steps per call, as the code does, keeps the output on the original grid.
- **Very small time steps.** The error grows as the Courant number falls, by a factor of 8 between 0.4 and 0.05 in the test above.

## Implementations

## History

The first order Lax-Friedrichs scheme, in its staggered form, averages two neighbor cells and differences their fluxes. Nessyahu and Tadmor (1990) replaced the constant data by limited piecewise linear data and the fluxes by a midpoint rule with a Taylor step. This gave a second order non-oscillatory central scheme without Riemann solvers, which led to many central schemes in the 1990s. Kurganov and Tadmor (2000) showed how to remove its $1/\Delta t$ viscosity with local speeds, which gave the [Kurganov-Tadmor scheme](/kurganov-tadmor-scheme/).

## References
