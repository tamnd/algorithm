---
tag: HQEZ7E
kind: algorithm
slug: hllc-riemann-solver
name: HLLC Riemann solver
aliases:
- HLLC flux
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: Restores the contact wave in the HLL solver with two intermediate states, giving sharp contacts and shear layers.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1 on smooth solutions", keeps_stationary_contact: true, exact_isolated_contact: true}
history:
  year: 1994
  people: [Eleuterio F. Toro, M. Spruce, W. Speares]
  note: Toro, Spruce and Speares (1994) added the contact wave to the HLL solver. Batten, Clarke, Lambert and Causon (1997) studied the choice of the speeds and positivity.
prereqs: [hll-riemann-solver, exact-riemann-solver]
see_also: [hll-riemann-solver, roe-solver, rusanov-flux, exact-riemann-solver, euler-equations-of-gas-dynamics, muscl-scheme, rankine-hugoniot-conditions, ausm-scheme]
sources:
  - paper: "E. F. Toro, M. Spruce and W. Speares, Restoration of the contact surface in the HLL-Riemann solver, Shock Waves 4(1) (1994) 25-34"
    locator: the two middle states, the contact speed and the flux; doi:10.1007/BF01414629
  - paper: "P. Batten, N. Clarke, C. Lambert and D. M. Causon, On the choice of wavespeeds for the HLLC Riemann solver, SIAM Journal on Scientific Computing 18(6) (1997) 1553-1570"
    locator: the speed estimates, the contact speed and positivity of HLLC; doi:10.1137/S1064827593260140
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 10 (the HLLC solver for the Euler equations, the middle states and the wave speed estimates)
  - paper: "Amiram Harten, Peter D. Lax and Bram van Leer, On upstream differencing and Godunov-type schemes for hyperbolic conservation laws, SIAM Review 25(1) (1983) 35-61"
    locator: approximate Riemann solvers consistent with the integral form of the conservation law; doi:10.1137/1025002
  - paper: "Bernd Einfeldt, On Godunov-type methods for gas dynamics, SIAM Journal on Numerical Analysis 25(2) (1988) 294-318"
    locator: the outer speed estimates with Roe averages; doi:10.1137/0725021
---

The HLLC solver is the [HLL solver](/hll-riemann-solver/) with the contact wave put back. HLL replaces the fan of the [Riemann problem](/riemann-problem/) by one constant state between a left speed $S_L$ and a right speed $S_R$. That state cannot hold a contact discontinuity, so HLL smears contacts. HLLC (the C is for contact) splits the middle into two states $U^*_L$ and $U^*_R$ at a contact speed $S^*$. The two states have the same velocity $S^*$ and the same pressure $p^*$, but different densities. The jump conditions across the three waves then fix everything. Toro, Spruce and Speares (1994) introduced it. It keeps an isolated contact exactly, like the [Roe solver](/roe-solver/), and it keeps most of the robustness of HLL, so it is a default solver in many gas dynamics codes.

## In plain words

HLL treats everything between the fastest left wave and the fastest right wave as one blended state. For gas this blends hot and cold gas at a contact, so the contact spreads out over time. HLLC adds one more wave in the middle that moves with the gas. Gas to the left of this wave keeps its own density, gas to the right keeps its own, and only the pressure and the velocity are shared. If the data are already just a contact, the method sees that and moves it without any smearing at the face.

## The problem

Given cell averages $U_j^n$ of the [Euler equations](/euler-equations-of-gas-dynamics/) $U_t + F(U)_x = 0$ with $U = (\rho, \rho u, E)$, $F = (\rho u, \rho u^2 + p, u(E + p))$, $E = p/(\gamma - 1) + \rho u^2/2$, $c = \sqrt{\gamma p/\rho}$ and $\gamma = 1.4$, compute a face flux $F_{j+1/2}$ from $U_L = U_j$ and $U_R = U_{j+1}$ for the conservative update $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$. The flux should be exact for an isolated contact.

## The algorithm

```pseudo id=main
HLLC-FLUX(U_L, U_R)
L1  (S_L, S_R) <- WAVE-SPEEDS(U_L, U_R)            ▷ Einfeldt estimates
L2  if S_L >= 0: return F(U_L)
L3  if S_R <= 0: return F(U_R)
L4  S* <- (p_R - p_L + ρ_L u_L (S_L - u_L) - ρ_R u_R (S_R - u_R)) / (ρ_L (S_L - u_L) - ρ_R (S_R - u_R))
L5  if S* >= 0: K <- L else K <- R
L6  U*_K <- ρ_K (S_K - u_K)/(S_K - S*) · (1, S*, E_K/ρ_K + (S* - u_K)(S* + p_K/(ρ_K (S_K - u_K))))
L7  return F(U_K) + S_K (U*_K - U_K)

FV-STEP(U, Δt, Δx)
L8  add one ghost cell on each side (copy for outflow, wrap for periodic)
L9  for each face j+1/2: F_{j+1/2} <- HLLC-FLUX(U_j, U_{j+1})
L10 for each cell j: U_j <- U_j - (Δt/Δx)(F_{j+1/2} - F_{j-1/2})
```

The speeds of line L1 are $S_L = \min(u_L - c_L, \tilde u - \tilde c)$ and $S_R = \max(u_R + c_R, \tilde u + \tilde c)$ with the Roe averages $\tilde u$, $\tilde H$ and $\tilde c^2 = (\gamma - 1)(\tilde H - \tilde u^2/2)$. The time step is $\Delta t = 0.9\,\Delta x/\max_j(|u_j| + c_j)$ with forward Euler. The middle pressure is $p^* = p_K + \rho_K(S_K - u_K)(S^* - u_K)$, the same for $K = L$ and $K = R$; line L4 is the condition that the two are equal.

## Example

**The flux by hand.** Take Sod's states $W_L = (\rho, u, p) = (1, 0, 1)$ and $W_R = (0.125, 0, 0.1)$. The Einfeldt speeds are $S_L = -1.18322$ and $S_R = 1.15190$ (computed on the [HLL](/hll-riemann-solver/) page). Both velocities are zero, so line L4 is

$$S^* = \frac{0.1 - 1}{S_L - 0.125\,S_R} = \frac{-0.9}{-1.32721} = 0.678118.$$

Since $S^* > 0$, $K = L$. Line L6 gives $\rho^*_L = S_L/(S_L - S^*) = 0.635682$, so the middle state is $U^*_L = (0.635682, 0.431067, 1.517200)$. The middle pressure is $p^* = 1 + (-1.18322)(0.678118) = 0.197640$. Line L7 gives the flux

$$F = (\rho^*_L S^*,\ \rho^*_L S^{*2} + p^*,\ S^*(E^*_L + p^*)) = (0.431067, 0.489954, 1.162864).$$

The exact solution has $u^* = 0.92745$ and $p^* = 0.30313$ and the exact Godunov flux is $(0.395391, 0.669837, 1.154038)$. The HLL flux with the same speeds is $(0.510714, 0.543964, 1.313264)$. The HLLC mass flux is closer to the exact one.

**Sod's tube.** On $[0, 1]$, outflow boundaries, Courant number 0.9, $t = 0.2$, the $L^1$ density errors against exact cell averages, measured with the code on this page, are:

| cells $M$ | steps | HLLC | HLL (Einfeldt) |
|---|---|---|---|
| 100 | 48 | 0.01387 | 0.01505 |
| 200 | 97 | 0.00919 | 0.00994 |
| 400 | 194 | 0.00581 | 0.00629 |

The observed orders are 0.59 and 0.66. The gain over HLL comes from the contact.

**A moving contact.** On a periodic grid of 100 cells, put $\rho = 1$ for $0.25 < x < 0.75$ and $\rho = 0.5$ elsewhere, with $u = 1$ and $p = 1$. After 149 steps ($t = 0.5$) the $L^1$ density error is 0.0459 for HLLC and 0.0578 for HLL. In both, $u$ and $p$ stay exact to $10^{-15}$. A moving contact is still smeared by HLLC, because the scheme averages over a cell each step. Only the face flux is exact.

**A contact at rest.** With $\rho = 1$ on the left half and $0.5$ on the right half, $u = 0$ and $p = 1$, every face flux is $(0, 1, 0)$ and the solution does not change at all. HLL, on the same data, gives $0.968, 0.927, \ldots, 0.539$ around the contact after 8 steps.

**A smooth wave.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid, the $L^1$ density errors at $t = 0.1$ for $M = 25, 50, 100, 200$ are $0.006143$, $0.003056$, $0.001536$ and $0.000770$, with orders 1.01, 0.99 and 1.00. The HLL errors are $0.008008, \ldots, 0.001010$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: with $S_L < u_L$, $u_R < S_R$ and $S_L < S^* < S_R$, the middle states of lines L4 and L6 are the unique states with a common velocity $S^*$ and a common pressure $p^*$ that satisfy the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) across $S_L$ and $S_R$. The jump across $S^*$ also satisfies them, so the average of the two middle states over the fan is the HLL state: the solver is consistent with the integral form of the law. The flux is consistent, $F(U, U) = F(U)$, it is continuous across the switch $S^* = 0$, and the scheme is conservative. For data with $u_L = u_R$ and $p_L = p_R$, the solver returns the exact flux, and a contact at rest is a steady solution of the scheme. The middle densities are positive. Positivity of the middle pressures is shown by Batten et al. (1997) for these speeds and is not proved on this page.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: one HLLC flux costs $O(m)$ operations and a constant number of square roots for the speeds, a few more operations than HLL. One step costs $O(mM)$ and the memory is $O(mM)$. A fixed end time at a fixed Courant number takes $O(M)$ steps, so the total is $O(mM^2)$.

## Properties

- **Keeps contacts and shear waves.** A contact at rest is exact. In 2D and 3D the transverse velocity is carried by the two middle states like the density, so a shear layer at rest is also kept.
- **Upwind for supersonic flow.** For $S_L \ge 0$ or $S_R \le 0$ it returns $F(U_L)$ or $F(U_R)$.
- **Positive in practice.** On the 123 problem ($W_L = (1, -2, 0.4)$, $W_R = (1, 2, 0.4)$, $M = 100$, $t = 0.15$) the smallest density is 0.0186 and the smallest pressure is 0.0069. The exact density at the center is 0.0219.
- **First order.** The measured order on the smooth wave is 0.99 to 1.01.
- **Not entropy stable by proof.** The middle states are not averages of the exact solution, so the entropy argument of HLL does not apply.

## Variants and improvements

- **Other speed estimates.** Davis speeds or pressure-based speeds (Toro 2009, Chapter 10) can replace the Einfeldt speeds of line L1.
- **Low Mach corrections.** At low Mach number the dissipation on the acoustic waves is too large. Rescaled forms reduce it.
- **Hybrids for the carbuncle.** HLLC, like Roe, can give the carbuncle at strong shocks aligned with the grid. Codes switch to HLL in the direction normal to such a shock.
- **HLLD and multi-state solvers.** For magnetohydrodynamics, more middle states give the HLLD solver.
- **High order.** Use the flux on [MUSCL](/muscl-scheme/) or WENO values with a Runge-Kutta method.

## When to use it

Use HLLC as the default flux for compressible gas dynamics: it keeps contacts and shear layers like Roe, it needs no eigenvectors and no entropy fix, and it is robust near vacuum. Use HLL instead at strong grid-aligned shocks where the carbuncle appears, or for systems where the middle wave structure is not known.

## Pitfalls

- **The pressure of the middle state.** The pressure $p^*$ in the flux is not the pressure that the equation of state gives for $U^*_K$. Do not recompute it from $U^*_K$.
- **The sign of the denominator.** The denominator of $S^*$ is negative when $S_L < u_L$ and $S_R > u_R$. Estimates that break these conditions can make it zero.
- **Choosing $K$.** At $S^* = 0$ both choices give the same flux (Lemma 3 of the proof), so the switch $S^* \ge 0$ is safe. A test on $u_L$ or $u_R$ in place of $S^*$ is wrong.
- **Expecting a sharp moving contact.** The face flux of an isolated contact is exact, but a moving contact still smears at first order because of the cell averages. Only a contact at rest stays sharp.

## Implementations

## History

Harten, Lax and van Leer (1983) noted that a solver with one middle state loses the contact and suggested that more states would help. Toro, Spruce and Speares (1994) built the solver with two middle states for the Euler equations and named it HLLC. Batten, Clarke, Lambert and Causon (1997) studied the choice of the outer speeds and of $S^*$, and showed positivity with the Einfeldt speeds. The solver is described in detail in Toro (2009, Chapter 10).

## References
