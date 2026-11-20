---
tag: WYYX6A
kind: algorithm
slug: kurganov-tadmor-scheme
name: Kurganov-Tadmor scheme
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: A semi-discrete central scheme that uses local wave speeds to shrink the numerical viscosity, giving an ODE system for the method of lines.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", s: "the number of Runge-Kutta stages", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(s m M K)"}
  space: {extra: "O(s m M)"}
properties: {deterministic: true, explicit: true, conservative: true, riemann-solver-free: true, order: "2 on smooth solutions away from extrema", tvd: "for a scalar law with one global speed under a Courant condition", positive: "not guaranteed"}
history:
  year: 2000
  people: [Alexander Kurganov, Eitan Tadmor]
  note: Kurganov and Tadmor (2000) used local wave speeds in the central scheme of Nessyahu and Tadmor (1990). This made the numerical viscosity independent of the time step and gave a semi-discrete form.
prereqs: [nessyahu-tadmor-scheme, rusanov-flux, method-of-lines, strong-stability-preserving-runge-kutta]
see_also: [muscl-scheme, lax-friedrichs-scheme, hll-riemann-solver, total-variation-diminishing, eno-scheme, weno-scheme, positivity-preserving-limiter]
sources:
  - paper: "Alexander Kurganov and Eitan Tadmor, New high-resolution central schemes for nonlinear conservation laws and convection-diffusion equations, Journal of Computational Physics 160(1) (2000) 241-282"
    locator: the second order central scheme with local speeds, its semi-discrete form and the minmod-theta reconstruction; doi:10.1006/jcph.2000.6459
  - paper: "Haim Nessyahu and Eitan Tadmor, Non-oscillatory central differencing for hyperbolic conservation laws, Journal of Computational Physics 87(2) (1990) 408-463"
    locator: the staggered second order central scheme that the Kurganov-Tadmor scheme improves; doi:10.1016/0021-9991(90)90260-8
  - paper: "Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49 (1983) 357-393"
    locator: the incremental form and the lemma on TVD coefficients; doi:10.1016/0021-9991(83)90136-5
  - paper: "Chi-Wang Shu and Stanley Osher, Efficient implementation of essentially non-oscillatory shock-capturing schemes, Journal of Computational Physics 77(2) (1988) 439-471"
    locator: the TVD (SSP) Runge-Kutta methods built from convex combinations of forward Euler steps; doi:10.1016/0021-9991(88)90177-5
  - paper: "Alexander Kurganov, Sebastian Noelle and Guergana Petrova, Semidiscrete central-upwind schemes for hyperbolic conservation laws and Hamilton-Jacobi equations, SIAM Journal on Scientific Computing 23(3) (2001) 707-740"
    locator: the central-upwind variant with one-sided local speeds; doi:10.1137/S1064827500373413
---

The Kurganov-Tadmor scheme is a second order finite volume scheme for [hyperbolic conservation laws](/hyperbolic-conservation-law/) that needs no Riemann solver and no eigenvectors. It reconstructs a limited straight line in each cell, takes the two values at each face, and combines them with the [Rusanov flux](/rusanov-flux/), using the largest local wave speed at that face. The result is a system of ordinary differential equations for the cell averages, which a [strong stability preserving Runge-Kutta method](/strong-stability-preserving-runge-kutta/) integrates in the [method of lines](/method-of-lines/). Its numerical viscosity does not grow when the time step is small, which the older staggered [Nessyahu-Tadmor scheme](/nessyahu-tadmor-scheme/) cannot claim.

## In plain words

A central scheme does not ask which way the waves go. It takes the average of the fluxes on the two sides of a face and adds a damping term that is proportional to the jump at the face. The damping term is what keeps the scheme stable. If the damping uses one global speed, it smears everything, so this scheme uses the fastest wave speed near each face only. If the data in each cell is a limited straight line instead of a constant, the jump at a face is small where the solution is smooth, so the damping is small there too. Only the flux of the equation and its largest wave speed are needed, so the same code works for any system.

## The problem

Given cell averages $U_j$ of $U_t + F(U)_x = 0$ on a uniform grid with width $\Delta x$, find a conservative semi-discrete scheme $dU_j/dt = L_j(U)$ that is second order where the solution is smooth and free of oscillations at shocks, using only $F$ and the spectral radius $\rho(\partial F/\partial U)$. The page uses scalar laws and the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$, $\gamma = 1.4$, and the spectral radius $|u| + c$. The values are cell averages, so errors are measured against exact cell averages.

## The algorithm

```pseudo id=main
KT-RATE(U, Δx, F, SPEED, θ)
L1  add two ghost cells on each side (copy for outflow, wrap for periodic)
L2  for each cell j: s_j <- MINMOD(θ(U_j - U_{j-1}), (U_{j+1} - U_{j-1}) / 2, θ(U_{j+1} - U_j))   ▷ per component
L3  for each face j+1/2: U^- <- U_j + s_j / 2;  U^+ <- U_{j+1} - s_{j+1} / 2
L4      a_{j+1/2} <- max(SPEED(U^-), SPEED(U^+))
L5      H_{j+1/2} <- (F(U^+) + F(U^-)) / 2 - (a_{j+1/2} / 2)(U^+ - U^-)
L6  return L_j = -(H_{j+1/2} - H_{j-1/2}) / Δx for each cell j
L7  advance dU/dt = L(U) by forward Euler, Heun's SSP RK2 or the SSP RK3 of Shu and Osher
```

MINMOD of three numbers is the smallest one when all three are positive, the largest one when all three are negative, and zero otherwise. The parameter $\theta \in [1, 2]$ sets how steep the slopes may be: $\theta = 1$ is the minmod limiter, and $\theta = 2$ is the MC limiter. The code uses $\theta = 1.5$, Heun's method and $\Delta t = 0.4\,\Delta x/\max_j(|u_j| + c_j)$ by default. With $s_j = 0$, lines L3 to L5 are the first order Rusanov scheme.

## Example

**One rate by hand.** Take $u_t + u_x = 0$, so $F(u) = u$ and the speed is 1, with $\Delta x = 1$, $\theta = \frac32$, outflow boundaries and $u = (0, 0, 1, 3, 4, 4)$. The differences around cell 3 are $1$ and $2$, so $s_3 = \mathrm{minmod}(\frac32, \frac32, 3) = \frac32$. Cell 4 also has $s_4 = \frac32$, and the other slopes are zero. With speed 1 the flux of line L5 is $\frac12(u^+ + u^-) - \frac12(u^+ - u^-) = u^-$, the upwind value. The face fluxes from the left boundary are $(0, 0, 0, \frac74, \frac{15}4, 4, 4)$, for example $H_{3+1/2} = 1 + \frac34$. The rates are $L = (0, 0, -\frac74, -2, -\frac14, 0)$, and one forward Euler step with $\Delta t = \frac14$ gives $(0, 0, \frac9{16}, \frac52, \frac{63}{16}, 4)$. The test checks all three lists exactly in `Fraction` arithmetic.

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$, outflow boundaries, Heun's method and Courant number 0.4, the scheme runs to $t = 0.2$. These $L^1$ density errors against exact cell averages are measurements made with the code on this page.

| cells $M$ | steps | $\theta = 1$ | $\theta = 1.5$ | $\theta = 2$ |
|---|---|---|---|---|
| 100 | 107 to 109 | 0.009727 | 0.007000 | 0.006920 |
| 200 | 217 to 219 | 0.005528 | 0.003832 | 0.003884 |
| 400 | 436 to 440 | 0.003048 | 0.001944 | 0.001988 |

The [MUSCL-Hancock](/muscl-scheme/) scheme with HLLC and minmod has 0.00585 at $M = 100$ with half as many steps. The central flux smears the contact more, because it does not know that a contact exists.

**A smooth wave.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid to $t = 0.1$, the $L^1$ density errors at $M = 25, 50, 100$ are 0.0019461, 0.0005171 and 0.0001268, so the observed orders are 1.91 and 2.03.

**The time step does not add viscosity.** For $u_t + u_x = 0$ with the averages of $\sin(2\pi x)$, $M = 40$, SSP RK3 and one period, the $L^1$ errors at the Courant numbers 0.05, 0.1, 0.2 and 0.4 are 0.019294, 0.019292, 0.019272 and 0.019093. Eight times more steps change the error by about 1 percent. The Nessyahu-Tadmor scheme on the same problem gets worse as the Courant number falls.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the scheme is conservative and consistent, so by the [Lax-Wendroff theorem](/lax-wendroff-theorem/) bounded $L^1$ limits are weak solutions. For a scalar law with one global speed $a \ge |f'|$ and $1 \le \theta \le 2$, the forward Euler step has Harten's incremental form with nonnegative coefficients. It is [TVD](/total-variation-diminishing/) and makes no new extrema when $\lambda a \le 1/(2 + \theta)$, and for linear advection when $\lambda a \le 2/(2 + \theta)$. Heun's method and SSP RK3 are convex combinations of forward Euler steps, so they keep these properties.

With local speeds that differ from face to face, TVD is not proved here. The tests check it for Burgers' equation on one step problem, which is a measurement.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: one evaluation of the rate costs $O(mM)$ operations: $m$ minmod calls per cell, and per face two flux evaluations and two speed evaluations. A step with $s$ stages costs $O(smM)$ and keeps $O(smM)$ numbers. A fixed end time at a fixed Courant number needs $K = O(M)$ steps, so the total is $O(smM^2)$. With Heun's method each step evaluates the rate twice, and the Courant number 0.4 is half the 0.8 that MUSCL-Hancock uses on this site, so a Sod run takes about twice as many steps (108 against 54 at $M = 100$).

## Properties

- **No Riemann solver.** Only $F$ and the spectral radius are needed, so the scheme works for systems whose eigenvectors are costly or unknown.
- **Second order on smooth solutions.** Measured: orders 1.91 and 2.03 on the Euler wave. On a sine wave for advection the $L^1$ order is 1.66 and then 1.93, because the limiter clips the extrema on coarse grids.
- **Conservative.** Exact in rational arithmetic; the test checks it in `Fraction` for Burgers' equation.
- **Viscosity independent of the time step.** Measured above. This is what allows the semi-discrete form.
- **TVD for scalar laws with one global speed.** Proved under the Courant conditions above.
- **Contacts smear.** The diffusion term acts on every jump, so a stationary contact is not kept.

## Variants and improvements

- **Central-upwind schemes.** Kurganov, Noelle and Petrova (2001) use the one-sided local speeds $a^+ \ge 0 \ge a^-$, as in [HLL](/hll-riemann-solver/). This reduces the diffusion further when the waves move to one side.
- **Higher order reconstruction.** Replacing line L2 with [ENO](/eno-scheme/) or [WENO](/weno-scheme/) values gives higher order central schemes; the time stepper must then be of matching order.
- **Characteristic or primitive reconstruction.** Limiting $(\rho, u, p)$ instead of the conserved variables often gives cleaner results for gas dynamics.
- **Convection-diffusion.** The semi-discrete form allows a diffusion term to be added to $L_j$ directly, which Kurganov and Tadmor also treat.

## When to use it

Use it when a robust second order shock capturing scheme is needed and a Riemann solver is not available or not wanted: new systems of equations, systems with complex eigenstructure, or prototypes. Use an upwind scheme such as MUSCL with HLLC when contacts and shear layers must be sharp, and add a positivity limiter for flows near vacuum.

## Pitfalls

- **The alias "central-upwind scheme".** That name belongs to the 2001 scheme of Kurganov, Noelle and Petrova, which uses one-sided speeds. This page is the 2000 scheme with symmetric local speeds.
- **A Courant number that is too large.** The proved bound is $\lambda a \le 1/(2 + \theta)$ for general scalar laws. The code uses 0.4, which the tests show to work, but it is not a proven bound for systems.
- **Forward Euler in time.** It is only first order in time and is TVD only under the stricter bound. Use an SSP Runge-Kutta method of the same order as the reconstruction.
- **Speed estimates that are too small.** If $a_{j+1/2}$ is less than the true largest speed at the face, the scheme can oscillate or blow up. Take the maximum over both face values.
- **One ghost cell.** The slope in the boundary cells needs two ghost cells on each side.

## Implementations

## History

Nessyahu and Tadmor (1990) gave a second order central scheme on a staggered grid, using cell averages over a cell that straddles two cells of the old grid, so no Riemann problem is solved. Its numerical viscosity grows like $1/\Delta t$, so it cannot be used with a very small time step and has no semi-discrete form. Kurganov and Tadmor (2000) replaced the staggered cells with nonuniform cells whose width depends on the local wave speeds, then let the time step go to zero to get the semi-discrete scheme of this page. Kurganov, Noelle and Petrova (2001) added one-sided speeds to get the central-upwind schemes.

## References
