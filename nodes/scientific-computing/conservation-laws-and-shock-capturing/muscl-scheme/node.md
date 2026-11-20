---
tag: 7J4C0V
kind: algorithm
slug: muscl-scheme
name: MUSCL scheme
aliases:
- MUSCL-Hancock scheme
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Reconstructs limited linear slopes in each cell and solves Riemann problems between interface values, second order away from shocks.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "2 on smooth solutions away from extrema", tvd: "for linear advection with Courant number at most 1", positive: "not guaranteed"}
history:
  year: 1979
  people: [Bram van Leer, Steve Hancock, Peter K. Sweby]
  note: Van Leer (1979) gave the second order extension of Godunov's method with limited slopes. The predictor step is due to Hancock. Sweby (1984) gave the TVD region for limiters.
prereqs: [godunov-method, flux-limiter-methods, total-variation-diminishing, hllc-riemann-solver]
see_also: [piecewise-parabolic-method, eno-scheme, weno-scheme, kurganov-tadmor-scheme, hll-riemann-solver, godunov-order-barrier, strong-stability-preserving-runge-kutta, positivity-preserving-limiter]
sources:
  - paper: "Bram van Leer, Towards the ultimate conservative difference scheme. V. A second-order sequel to Godunov's method, Journal of Computational Physics 32(1) (1979) 101-136"
    locator: the piecewise linear reconstruction of cell averages with limited slopes and the second order Godunov type scheme; doi:10.1016/0021-9991(79)90145-1
  - paper: "P. K. Sweby, High resolution schemes using flux limiters for hyperbolic conservation laws, SIAM Journal on Numerical Analysis 21(5) (1984) 995-1011"
    locator: the TVD region of flux limiters for linear advection; doi:10.1137/0721062
  - paper: "Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49 (1983) 357-393"
    locator: the incremental form and the lemma on TVD coefficients; doi:10.1016/0021-9991(83)90136-5
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 13 (high order and TVD methods for scalar equations, slope limiters) and Chapter 14 (the MUSCL-Hancock method for nonlinear systems)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 6 (high resolution methods, slope and flux limiters, TVD) and Chapter 10 (other approaches to high resolution)
---

MUSCL (Monotone Upstream-centered Scheme for Conservation Laws) is van Leer's second order extension of [Godunov's method](/godunov-method/). Godunov's method takes the solution in each cell as constant, so it is first order. MUSCL gives each cell a straight line instead, with a slope that a limiter makes smaller near jumps. The values of these lines at the two sides of each face go into a Riemann solver. The result is second order where the solution is smooth and free of oscillations near shocks, which is possible only because the limiter makes the scheme nonlinear (see the [Godunov order barrier](/godunov-order-barrier/)). This page uses the MUSCL-Hancock form: a half time step predictor inside each cell, then one flux evaluation per face, with forward Euler in time.

## In plain words

First order schemes blur everything, because they assume the gas is uniform inside each cell. A better guess is a straight line through the cell average, tilted to match the neighbors. Near a shock, a steep line would overshoot and create a wiggle, so the slope is cut back: if the left and right differences disagree in sign, the slope is zero, and otherwise it is no larger than the limiter allows. Each line gives two edge values per cell. These edge values are pushed forward half a time step, and then each face solves a small Riemann problem between the values on its two sides.

## The problem

Given cell averages $U_j^n$ of a [hyperbolic conservation law](/hyperbolic-conservation-law/) $U_t + F(U)_x = 0$ on a uniform grid with width $\Delta x$, compute $U_j^{n+1}$ at $t^{n+1} = t^n + \Delta t$ with an error of order $\Delta x^2$ in smooth regions and without new oscillations at discontinuities. The page uses scalar laws $u_t + f(u)_x = 0$ and the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$, $E = p/(\gamma - 1) + \rho u^2/2$, $c = \sqrt{\gamma p/\rho}$ and $\gamma = 1.4$. The values are cell averages, so errors are measured against exact cell averages.

## The algorithm

```pseudo id=main
MUSCL-HANCOCK-STEP(U, Δt, Δx, LIM, RIEMANN)
L1  add two ghost cells on each side (copy for outflow, wrap for periodic)
L2  for each cell j: d_j <- LIM(U_j - U_{j-1}, U_{j+1} - U_j) / 2      ▷ half slope, per component
L3      U_j^- <- U_j - d_j;  U_j^+ <- U_j + d_j
L4      Ū_j^± <- U_j^± - (Δt / 2Δx)(F(U_j^+) - F(U_j^-))                ▷ Hancock predictor
L5  for each face j+1/2: F_{j+1/2} <- RIEMANN(Ū_j^+, Ū_{j+1}^-)
L6  for each cell j: U_j <- U_j - (Δt/Δx)(F_{j+1/2} - F_{j-1/2})
```

The limiter of line L2 is a choice. The code has three, all zero when $ab \le 0$:

- **minmod:** the one of $a$, $b$ with the smaller size. It is the most diffusive.
- **van Leer:** $2ab/(a + b)$, the harmonic mean.
- **MC (monotonized central):** $\mathrm{minmod}(2a, (a + b)/2, 2b)$. It is the least diffusive of the three.

For the Euler equations, the code reconstructs the conserved variables componentwise and uses the [HLLC](/hllc-riemann-solver/) flux with the speed estimates of Davis in line L5. The time step is $\Delta t = 0.8\,\Delta x/\max_j(|u_j| + c_j)$. For scalar laws the code uses the exact Riemann flux: the upwind flux $a u_L$ for $u_t + a u_x = 0$ with $a > 0$, and Godunov's flux for Burgers' equation.

## Example

**One step by hand.** Take linear advection with $a = 1$, $\Delta x = 1$, $\Delta t = \frac12$ (so $\nu = \frac12$), outflow boundaries, and $u = (0, 0, 1, 3, 4, 4)$. With minmod, the slopes are $(0, 0, 1, 1, 0, 0)$: in cell 3 the differences are $1$ and $2$, and in cell 4 they are $2$ and $1$. For $a > 0$ the face flux is $a\bar u_j^+ = u_j + \frac{1-\nu}{2}\delta_j$, so the fluxes leaving cells 3 to 6 are $\frac54$, $\frac{13}4$, $4$ and $4$. The update gives

$$u^{n+1} = \Big(0,\ 0,\ 1 - \tfrac12\cdot\tfrac54,\ 3 - \tfrac12\big(\tfrac{13}4 - \tfrac54\big),\ 4 - \tfrac12\big(4 - \tfrac{13}4\big),\ 4\Big) = \Big(0, 0, \tfrac38, 2, \tfrac{29}8, 4\Big).$$

With MC the slopes in cells 3 and 4 are $\frac32$ and the result is $(0, 0, \frac5{16}, 2, \frac{59}{16}, 4)$: the steeper slopes move less mass out of cell 3. The first order upwind scheme gives $(0, 0, \frac12, 2, \frac72, 4)$. The sum falls from 12 to 10 because $\nu \cdot 4 = 2$ leaves through the right boundary. The test checks both results exactly in `Fraction` arithmetic.

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$, outflow boundaries and Courant number 0.8, the scheme runs to $t = 0.2$. These $L^1$ errors of the density against exact cell averages are measurements made with the code on this page.

| cells $M$ | steps | minmod | van Leer | MC |
|---|---|---|---|---|
| 100 | 54 | 0.00585 | 0.00462 | 0.00435 |
| 200 | 109 | 0.00347 | 0.00265 | 0.00247 |
| 400 | 219 | 0.00190 | 0.00138 | 0.00126 |

The first order [HLL](/hll-riemann-solver/) scheme has the error 0.01505 at $M = 100$, more than twice the minmod value. Near the shock and the contact the error is $O(\Delta x)$ in $L^1$ for every scheme, so the observed orders here are 0.76 to 0.97, not 2.

**A smooth wave.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$ and $p = 1$ on a periodic grid, the $L^1$ density errors at $t = 0.1$ for $M = 25, 50, 100, 200$ give these observed orders.

| limiter | error at $M = 25$ | error at $M = 200$ | orders |
|---|---|---|---|
| minmod | 0.0015985 | 0.0000323 | 1.85, 1.88, 1.89 |
| van Leer | 0.0008917 | 0.0000127 | 2.02, 2.06, 2.05 |
| MC | 0.0006558 | 0.0000079 | 2.22, 1.94, 2.23 |

**The limiter at extrema.** For $u_t + u_x = 0$ with the cell averages of $\sin(2\pi x)$, $\nu = 0.8$ and one period ($t = 1$), van Leer gives the $L^1$ errors 0.019367, 0.004899, 0.001225 and 0.000294 for $M = 20, 40, 80, 160$ (orders 1.98, 2.00, 2.06), but the max norm orders are only 1.32, 1.36 and 1.39. The largest errors sit at the crest and the trough, where the limiter sets the slope to zero.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the scheme is conservative and consistent, so by the [Lax-Wendroff theorem](/lax-wendroff-theorem/) bounded $L^1$ limits are weak solutions. For linear advection with the upwind flux, $0 \le \nu \le 1$ and any limiter in Sweby's TVD region ($0 \le \varphi(r) \le \min(2, 2r)$), the update has Harten's incremental form with coefficients in $[\nu^2, \nu(2 - \nu)]$, so the scheme is [TVD](/total-variation-diminishing/) and makes no new extrema. With a contact preserving solver such as HLLC, an isolated stationary contact is kept exactly, because all slopes are zero.

The page does not prove TVD for nonlinear laws or positivity for the Euler equations. The tests check TVD for Burgers' equation on one step problem, which is a measurement.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: one step costs $O(mM)$ operations: $m$ limiter calls per cell, two physical flux evaluations per cell for the predictor, and one Riemann flux per face. The memory is $O(mM)$. A fixed end time at a fixed Courant number needs $K = O(M)$ steps, so the total is $O(mM^2)$. A step costs about three times a first order step with the same solver, but on Sod's problem MUSCL with 100 cells is more accurate than HLL with 400 cells (0.00585 against 0.00629).

## Properties

- **Second order in smooth monotone regions.** The measured $L^1$ order on smooth data is about 2. At smooth extrema the limiter clips the slope, so the max norm order is between 1.3 and 1.5 in the advection test.
- **TVD for linear advection.** Proved for $\nu \le 1$ with the three limiters (see Correctness). The test checks this at $\nu = 0.3$, $0.9$ and $1$.
- **Conservative.** Exact in rational arithmetic; the test checks it in `Fraction` for Burgers' equation.
- **Keeps a stationary contact.** With HLLC, as proved. With HLL or Rusanov in line L5 the contact would smear.
- **Not positivity preserving in general.** The predictor of line L4 can make the density or pressure negative near vacuum. A positivity limiter or a smaller time step is needed there.

## Variants and improvements

- **Primitive or characteristic variables.** Reconstructing $(\rho, u, p)$, or the characteristic variables $L(U_j)U$, gives fewer small oscillations for the Euler equations than the componentwise conserved reconstruction used here (Toro 2009, Chapter 14).
- **Method of lines.** Skip the predictor, use the reconstructed values directly in the [method of lines](/method-of-lines/), and integrate with a second order [SSP Runge-Kutta](/strong-stability-preserving-runge-kutta/) method. With the Rusanov flux this is close to the [Kurganov-Tadmor scheme](/kurganov-tadmor-scheme/).
- **Higher order reconstruction.** The [piecewise parabolic method](/piecewise-parabolic-method/) uses parabolas, and [ENO](/eno-scheme/) and [WENO](/weno-scheme/) use adaptive stencils.
- **Other limiters.** Superbee sits on the upper edge of Sweby's region and steepens contacts; it can square smooth waves.

## When to use it

Use MUSCL-Hancock as the default second order finite volume scheme for gas dynamics and other systems with shocks, when the code already has a Riemann solver. It needs only one flux evaluation per face per step and two ghost cells. For smooth flows with fine structure, use a higher order method such as WENO; for flows near vacuum, add a positivity limiter.

## Pitfalls

- **Limiting the wrong variables.** Componentwise limiting of conserved variables can give small oscillations behind strong shocks in systems. Limit primitive or characteristic variables when they matter.
- **Too few ghost cells.** The slope in the first and last cell needs a second ghost cell on each side. One ghost cell silently gives a first order or wrong boundary.
- **Limiter choice as a tuning knob.** Minmod, van Leer and MC differ by a factor of about 1.3 in the Sod errors above. The choice is a rule of thumb, not a result; MC and superbee steepen contacts but can flatten smooth peaks.
- **Measuring order on a solution with extrema.** In the max norm the order drops to between 1 and 2, which can be mistaken for a bug.
- **Courant number.** The TVD proof needs $\nu \le 1$ for linear advection. The code uses 0.8 for the Euler equations, which the tests show to work; it is not a proven bound.

## Implementations

## History

Van Leer developed MUSCL in a series of papers titled "Towards the ultimate conservative difference scheme" in the 1970s. The fifth paper (1979) applied limited piecewise linear reconstruction to Godunov's method for gas dynamics, with a Lagrangian step and a remap. Hancock's predictor, reported by van Leer in the 1980s and described in Toro's book, gives the simple Eulerian form used here. Harten (1983) defined TVD schemes and gave the incremental form lemma, and Sweby (1984) mapped out the region of limiters that give TVD schemes. Colella and Woodward (1984) extended the idea to parabolas with the [piecewise parabolic method](/piecewise-parabolic-method/).

## References
