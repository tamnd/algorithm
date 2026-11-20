---
tag: 6EZVM9
kind: algorithm
slug: maccormack-method
name: MacCormack method
aliases:
- MacCormack scheme
area: scientific-computing/conservation-laws-and-shock-capturing
level: intro
summary: A two-step predictor-corrector with forward then backward differences, second order and equal to Lax-Wendroff on linear problems.
solves: [euler-equations-of-gas-dynamics, burgers-equation]
model: real-ram
complexity:
  vars: {M: "the number of grid points", K: "the number of time steps"}
  time: {worst: "O(K M)"}
  space: {extra: "O(M)"}
  evaluations: {worst: "2 K (M + 2)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "2", monotone: false, tvd: false}
history:
  year: 1969
  people: [R. W. MacCormack]
  note: MacCormack (1969) introduced the scheme in a paper on hypervelocity impact cratering. It became a standard method for the compressible Navier-Stokes equations in the 1970s and 1980s.
prereqs: [hyperbolic-conservation-law, lax-wendroff-method, finite-difference-method]
see_also: [unconditionally-stable-maccormack, lax-wendroff-theorem, godunov-order-barrier, total-variation-diminishing, flux-limiter-methods, courant-friedrichs-lewy-condition, euler-equations-of-gas-dynamics, von-neumann-stability-analysis]
sources:
  - paper: doi:10.2514/2.6901
    title: R. W. MacCormack, The effect of viscosity in hypervelocity impact cratering, Journal of Spacecraft and Rockets 40 (2003) 757-763, a reprint of AIAA Paper 69-354 (1969)
    locator: the predictor-corrector difference scheme
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 6.1 (the Lax-Wendroff method), Section 12.9 (the importance of conservation form), Section 12.10 (the Lax-Wendroff theorem)
  - paper: doi:10.1002/cpa.3160130205
    title: P. D. Lax and B. Wendroff, Systems of conservation laws, Communications on Pure and Applied Mathematics 13 (1960) 217-237
    locator: the limit of a convergent conservative scheme is a weak solution
---

The MacCormack method moves a quantity such as density, momentum or energy along a 1D grid by one time step in two passes. The predictor pass makes a first guess from the flux differences to the right of each point. The corrector pass uses the flux differences of that guess to the left, and averages the result with the old value. It is a finite difference scheme for a conservation law $U_t + F(U)_x = 0$, second order in space and time, and for a linear flux it gives the same numbers as the [Lax-Wendroff method](/lax-wendroff-method/). The [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/) of fluid animation has the same name but is a different scheme: it traces semi-Lagrangian advection forward and back and corrects with half the error. Compared with that graphics scheme, this one is written in conservation form, so it keeps the total mass, momentum and energy exactly and moves shocks at the correct speed, but it is explicit and is stable only when the Courant number is at most 1. It is not TVD, and without added viscosity it oscillates at shocks.

## In plain words

Think of a row of points along a tube, each with an amount of gas. To advance one time step, first look to the right of each point: compare what flows through the right neighbour with what flows through the point itself, and make a first guess of the new amount. Then look to the left: do the same comparison on the guesses, against the left neighbour. The new amount is the average of the old amount and the corrected guess. Each pass alone is crude and leans to one side. Together the two leanings cancel, and the result is accurate for smooth flow. All the changes are written as flows through the gaps between points, so nothing is lost or created. At a sudden jump the method makes small ripples, so it needs some extra smoothing there.

## The problem

Given a flux $F$ with Jacobian $A(U) = F'(U)$, grid values $U_j$ at $M$ points $x_j$ with spacing $\Delta x$, a time step $\Delta t$ and a number of steps $K$, approximate the solution of the [hyperbolic conservation law](/hyperbolic-conservation-law/) $U_t + F(U)_x = 0$ at time $K\Delta t$. The Courant number is $\nu = \frac{\Delta t}{\Delta x}\max|\lambda_p(U)|$, with $\lambda_p$ the eigenvalues of $A$. The boundary gives one ghost value on each side: periodic, or transmissive (a copy of the end value).

## The algorithm

```pseudo id=main
MACCORMACK(U, Δx, Δt, K, F)
L1  for n ← 1 to K do
L2      for j ← 1 to M do U*_j ← U_j - (Δt/Δx)(F(U_(j+1)) - F(U_j))                  ▷ predictor: forward difference
L3      for j ← 1 to M do U_j ← (U_j + U*_j)/2 - (Δt/(2Δx))(F(U*_j) - F(U*_(j-1)))   ▷ corrector: backward difference
L4  return U
```

Line L2 also computes the predictor at the left ghost point, because line L3 needs $U^*_0$. Line L3 can overwrite $U_j$ in place, because it reads only its own old value $U_j$. The two lines together are a conservative scheme with the face flux

$$H_{j+1/2} = \tfrac12\big(F(U_{j+1}) + F(U^*_j)\big), \qquad U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}\big(H_{j+1/2} - H_{j-1/2}\big).$$

The order of the two differences can be swapped (backward then forward). Many codes alternate the order from step to step, so that the one-sided bias does not build up.

## Example

**One step by hand.** Take $u_t + u_x = 0$ on 6 periodic points with $\Delta x = 1$, $\Delta t = \frac12$ (Courant number $\frac12$) and $u = (1, 1, 1, 0, 0, 0)$. The predictor is $u^*_j = u_j - \frac12(u_{j+1} - u_j)$, which gives $u^* = (1, 1, \frac32, 0, 0, -\frac12)$. The corrector gives

$$u^{\text{new}} = \big(\tfrac58,\ 1,\ \tfrac98,\ \tfrac38,\ 0,\ -\tfrac18\big).$$

For example $u^{\text{new}}_3 = \frac12(1 + \frac32) - \frac14(\frac32 - 1) = \frac98$. The Lax-Wendroff formula $u_j - \frac{\nu}{2}(u_{j+1} - u_{j-1}) + \frac{\nu^2}{2}(u_{j+1} - 2u_j + u_{j-1})$ gives the same six numbers. The sum is still 3, so the scheme conserves. But $\frac98 > 1$ and $-\frac18 < 0$, and the total variation grows from 2 to $\frac52$. This is the overshoot at a jump.

**Second order on smooth data** (measurement, with the code on this page). $L^1$ errors at $t = 0.3$ for [Burgers' equation](/burgers-equation/) with $u_0 = 0.5 + 0.25\sin 2\pi x$ (smooth until $t = 2/\pi \approx 0.64$), and at $t = 0.25$ for an Euler density wave $\rho = 1 + 0.2\sin 2\pi(x - t)$, $u = 1$, $p = 1$:

| $M$ | Burgers error | ratio | Euler density error | ratio |
|---|---|---|---|---|
| 40 | 9.861e-4 | | 7.939e-4 | |
| 80 | 2.517e-4 | 3.92 | 1.987e-4 | 3.99 |
| 160 | 6.326e-5 | 3.98 | 4.970e-5 | 4.00 |
| 320 | 1.586e-5 | 3.99 | 1.243e-5 | 4.00 |

A ratio of 4 per halving of $\Delta x$ is order 2.

**Sod's shock tube** (measurement). On 100 points in $[0, 1]$ with transmissive ends, the plain scheme with $\Delta t/\Delta x = 0.2$ gives a negative pressure next to the initial jump after 10 steps, and the run fails. With $\Delta t/\Delta x = 0.45$ (Courant number about 0.99 for the fastest wave) it reaches $t = 0.2$, but the pressure falls to 0.0871 below the right state 0.1, and the velocity overshoots to 0.9405 against the exact $u^* = 0.92745$. With the constant artificial viscosity $0.05\,(U_{j+1} - 2U_j + U_{j-1})$ added after each step and $\Delta t/\Delta x = 0.4$, the pressure stays positive, and the shock is at $x = 0.845$ against the exact $0.5 + 1.75216 \times 0.2 = 0.8504$, within one grid spacing.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the scheme has the conservative form above with a consistent face flux, so with periodic boundaries the sum of the values does not change. For $F(U) = AU$ with a constant matrix, one step equals the Lax-Wendroff method. A Taylor expansion shows that the local truncation error is $O(\Delta x^2)$ for smooth solutions at a fixed ratio $\Delta t/\Delta x$. For linear advection, the amplification factor is $g(\theta) = 1 - i\nu\sin\theta - \nu^2(1 - \cos\theta)$ with $|g|^2 = 1 - \nu^2(1 - \nu^2)(1 - \cos\theta)^2$, so the scheme is stable exactly when $|\nu| \le 1$. The coefficient of $u_{j+1}$ is negative for $0 < \nu < 1$, so the scheme is not monotone. By the [Lax-Wendroff theorem](/lax-wendroff-theorem/), if the scheme converges, the limit is a weak solution. Nothing guarantees that it converges at shocks, or that the limit is the entropy solution.

## Complexity

Theorem: each step evaluates the flux at the $M$ grid values and at the $M$ predicted values, plus the ghost points, and does $O(M)$ further arithmetic. So $K$ steps cost $O(KM)$ time. The memory is the solution and one predictor array, $O(M)$. For a fixed final time $T$, the CFL condition gives $K \ge T\max|\lambda_p|/\Delta x$, so $K = \Theta(M)$ and the total cost is $\Theta(M^2)$ in 1D.

## Properties

- **Conservative and consistent.** Shocks, if they are captured, move at the Rankine-Hugoniot speed.
- **Second order** in space and time for smooth solutions.
- **Equal to Lax-Wendroff** for linear constant-coefficient systems. For a nonlinear flux it is a different scheme, and it needs no Jacobian matrix.
- **Stable for $|\nu| \le 1$** in the linear analysis.
- **Not monotone and not TVD.** By [Godunov's order barrier](/godunov-order-barrier/), a linear second-order scheme cannot be monotone.
- **Not symmetric.** The forward predictor and the backward corrector give a one-sided bias; the results depend on the direction of the waves.

## Variants and improvements

- **Swapped or alternating order.** Backward predictor and forward corrector, or an alternation from step to step.
- **Artificial viscosity.** A second-difference term, often scaled by a pressure switch, damps the oscillations at shocks. A constant coefficient makes the scheme first order.
- **TVD and flux-corrected forms.** Adding a limited dissipation term gives a TVD MacCormack scheme. See [flux limiter methods](/flux-limiter-methods/) and [total variation diminishing](/total-variation-diminishing/).
- **Multidimensional and viscous flows.** Directional splitting, or the unsplit form with predictor and corrector in each direction. MacCormack's later implicit and hybrid versions are for the compressible Navier-Stokes equations.
- **Graphics.** The [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/) is a semi-Lagrangian advection scheme, not this one.

## When to use it

Use it for smooth compressible flows, for teaching, and for problems where shocks are weak and a little artificial viscosity is acceptable. It is simple, it needs only flux evaluations, and it is second order. For strong shocks use a Godunov-type scheme with a limiter, such as the [MUSCL scheme](/muscl-scheme/) or a [WENO scheme](/weno-scheme/) with [SSP Runge-Kutta](/strong-stability-preserving-runge-kutta/) time steps.

## Pitfalls

- **No dissipation at shocks.** The plain scheme oscillates at shocks and can give negative pressure or density. Add artificial viscosity or a limiter.
- **The time step.** The Courant number uses the fastest wave speed $|u| + c$, which can grow during the run. Compute it at every step.
- **Point values, not cell averages.** The scheme is written for point values on a grid. As a finite volume scheme it has the same form, but the initial data and the errors must then use cell averages.
- **The boundary.** The predictor at the last point uses a neighbour outside the grid, and the corrector at the first point uses a predictor outside it. Both need ghost values.
- **The graphics name.** Do not confuse it with the unconditionally stable MacCormack method of fluid animation.

## Implementations

## History

MacCormack (1969) introduced the predictor-corrector scheme in an AIAA paper on hypervelocity impact cratering; the Journal of Spacecraft and Rockets reprinted the paper in 2003. The scheme is a variant of the two-step Lax-Wendroff schemes of the 1960s that needs no Jacobian. It was a standard method for compressible flow computation in aerodynamics in the 1970s and 1980s, before Godunov-type upwind schemes replaced it for flows with strong shocks.

## References
