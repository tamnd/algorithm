---
tag: MA9G95
kind: algorithm
slug: hll-riemann-solver
name: HLL Riemann solver
aliases:
- Harten-Lax-van Leer solver
- HLLE solver
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Approximates the Riemann fan by one intermediate state between the slowest and fastest wave estimates; robust and positive but diffusive at contacts.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1 on smooth solutions", positive: "when the speeds bound the waves and dt max|S| / dx <= 1/2", keeps_stationary_contact: false}
history:
  year: 1983
  people: [Amiram Harten, Peter D. Lax, Bram van Leer, Bernd Einfeldt, S. F. Davis]
  note: Harten, Lax and van Leer (1983) defined the solver with one intermediate state. Davis (1988) and Einfeldt (1988) gave the speed estimates used in practice.
prereqs: [riemann-problem, godunov-method, euler-equations-of-gas-dynamics]
see_also: [hllc-riemann-solver, rusanov-flux, roe-solver, exact-riemann-solver, muscl-scheme, positivity-preserving-limiter, lax-wendroff-theorem, entropy-stable-scheme]
sources:
  - paper: "Amiram Harten, Peter D. Lax and Bram van Leer, On upstream differencing and Godunov-type schemes for hyperbolic conservation laws, SIAM Review 25(1) (1983) 35-61"
    locator: the approximate Riemann solver with one intermediate state, its consistency with the integral form of the conservation law and of the entropy condition; doi:10.1137/1025002
  - paper: "Bernd Einfeldt, On Godunov-type methods for gas dynamics, SIAM Journal on Numerical Analysis 25(2) (1988) 294-318"
    locator: the speed estimates with Roe averages (HLLE) and positivity; doi:10.1137/0725021
  - paper: "S. F. Davis, Simplified second-order Godunov-type methods, SIAM Journal on Scientific and Statistical Computing 9(3) (1988) 445-473"
    locator: the simple speed estimates from the two states; doi:10.1137/0909030
  - paper: "Bernd Einfeldt, Claus-Dieter Munz, Philip L. Roe and Björn Sjögreen, On Godunov-type methods near low densities, Journal of Computational Physics 92 (1991) 273-295"
    locator: positively conservative schemes; the HLLE scheme is positive and linearized solvers are not; doi:10.1016/0021-9991(91)90211-3
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 10 (the HLL and HLLC solvers and the wave speed estimates)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 15.3 (approximate Riemann solvers, including the HLL solver), Section 12.10 (the Lax-Wendroff theorem)
---

The HLL solver replaces the full solution of the [Riemann problem](/riemann-problem/) at a cell face by a simpler one: a single constant state $U^*$ between a left speed $S_L$ and a right speed $S_R$. If these speeds bound all waves of the exact solution, the integral form of the conservation law fixes $U^*$ and the flux with no further assumption. The solver needs no eigenvectors and no iteration, only two speed estimates. Harten, Lax and van Leer (1983) defined it. With the speed estimates of Einfeldt (1988) it is often called HLLE. It is the standard robust solver of [Godunov type](/godunov-method/): it keeps density and pressure positive and gives entropy solutions. Its weakness is that the one middle state averages away a contact discontinuity, which [HLLC](/hllc-riemann-solver/) restores.

## In plain words

At each face between two cells, gas from the left meets gas from the right, and a set of waves goes out. The exact answer has several waves and needs an iteration. HLL keeps only the fastest wave to the left and the fastest wave to the right and puts one averaged state between them. The conservation law tells you exactly what that averaged state must be, once you know the two speeds. So the method is simple and it never makes negative density, but anything inside the fan, such as a contact between hot and cold gas, is blurred into the average.

## The problem

Given cell averages $U_j^n$ of a [hyperbolic conservation law](/hyperbolic-conservation-law/) $U_t + F(U)_x = 0$, compute a face flux $F_{j+1/2}$ from $U_L = U_j$ and $U_R = U_{j+1}$ for the conservative update $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$. The page uses the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$, $F(U) = (\rho u, \rho u^2 + p, u(E + p))$, $E = p/(\gamma - 1) + \rho u^2/2$, $c = \sqrt{\gamma p/\rho}$ and $\gamma = 1.4$, and a scalar law $u_t + f(u)_x = 0$.

## The algorithm

```pseudo id=main
HLL-FLUX(U_L, U_R)
L1  (S_L, S_R) <- WAVE-SPEEDS(U_L, U_R)
L2  if S_L >= 0: return F(U_L)                    ▷ all waves go right
L3  if S_R <= 0: return F(U_R)                    ▷ all waves go left
L4  return (S_R F(U_L) - S_L F(U_R) + S_L S_R (U_R - U_L)) / (S_R - S_L)

FV-STEP(U, Δt, Δx)
L5  add one ghost cell on each side (copy for outflow, wrap for periodic)
L6  for each face j+1/2: F_{j+1/2} <- HLL-FLUX(U_j, U_{j+1})
L7  for each cell j: U_j <- U_j - (Δt/Δx)(F_{j+1/2} - F_{j-1/2})
```

The code gives two choices for line L1.

- **Davis:** $S_L = \min(u_L - c_L, u_R - c_R)$ and $S_R = \max(u_L + c_L, u_R + c_R)$.
- **Einfeldt (the default):** $S_L = \min(u_L - c_L, \tilde u - \tilde c)$ and $S_R = \max(u_R + c_R, \tilde u + \tilde c)$, where $\tilde u$, $\tilde H$ are the Roe averages, weighted by $\sqrt\rho$, and $\tilde c^2 = (\gamma - 1)(\tilde H - \tilde u^2/2)$ with $H = (E + p)/\rho$.

For a scalar law the code takes $S_L = \min(f'(u_L), f'(u_R))$ and $S_R = \max(f'(u_L), f'(u_R))$. The time step is $\Delta t = 0.9\,\Delta x/\max_j(|u_j| + c_j)$ with forward Euler.

The flux of line L4 comes from the HLL state

$$U^* = \frac{S_R U_R - S_L U_L - (F_R - F_L)}{S_R - S_L}, \qquad F^{hll} = F_L + S_L(U^* - U_L),$$

which are the integral form of the law over the fan and the jump condition across the left wave.

## Example

**The flux by hand.** Take Sod's states $W_L = (\rho, u, p) = (1, 0, 1)$ and $W_R = (0.125, 0, 0.1)$, so $U_L = (1, 0, 2.5)$, $U_R = (0.125, 0, 0.25)$, $F_L = (0, 1, 0)$ and $F_R = (0, 0.1, 0)$. The enthalpies are $H_L = 3.5$ and $H_R = 2.8$. With weights $1$ and $\sqrt{0.125} = 0.353553$, the Roe averages are $\tilde u = 0$ and $\tilde H = 4.48995/1.353553 = 3.31715$, so $\tilde c = \sqrt{0.4 \times 3.31715} = 1.15190$. The Einfeldt speeds are $S_L = \min(-1.18322, -1.15190) = -1.18322$ and $S_R = \max(1.05830, 1.15190) = 1.15190$. Then $S_R - S_L = 2.33512$, $S_L S_R = -1.36294$, and line L4 gives

$$F = \Big(\frac{1.36294 \times 0.875}{2.33512},\ \frac{1.15190 + 0.118322}{2.33512},\ \frac{1.36294 \times 2.25}{2.33512}\Big) = (0.510714, 0.543964, 1.313264).$$

The exact Godunov flux is $(0.395391, 0.669837, 1.154038)$, and the Rusanov flux is $(0.517657, 0.55, 1.331118)$. With the Davis speeds, $S_L = -S_R = -1.18322$, and the HLL flux is exactly the Rusanov flux.

**The HLL state is an average.** With $S_L = -2$ and $S_R = 2$, which bound all Sod waves (the shock moves at 1.75216), the HLL state is $U^* = (0.5625, 0.225, 1.375)$. The test computes the average of the exact solution over $-2 \le x/t \le 2$ with 4000 midpoints and finds the same state to $2 \times 10^{-3}$, the error of the midpoint rule at the three jumps.

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$, outflow boundaries and Courant number 0.9, the scheme runs to $t = 0.2$. The $L^1$ errors of the density against exact cell averages are measurements made with the code on this page.

| cells $M$ | steps | Einfeldt | Davis |
|---|---|---|---|
| 100 | 48 | 0.01505 | 0.01522 |
| 200 | 96 | 0.00994 | 0.01008 |
| 400 | 194 | 0.00629 | 0.00634 |

The observed orders with the Einfeldt speeds are 0.60 and 0.66. The Rusanov errors on the same grids are 0.02148, 0.01515 and 0.00998.

**A smooth wave.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid, the $L^1$ density errors at $t = 0.1$ for $M = 25, 50, 100, 200$ are $0.008008$, $0.004010$, $0.002016$ and $0.001010$, with orders 1.00, 0.99 and 1.00. They are half of the Rusanov errors, because here $S_L = u - c$ is much smaller in size than $|u| + c$.

**A contact at rest.** With $\rho = 1$ on the left half and $0.5$ on the right half, $u = 0$ and $p = 1$, after 8 steps on 40 cells the velocity and the pressure are exact to rounding, but the density around the contact is $0.968, 0.927, 0.863, 0.783, 0.702, 0.630, 0.576, 0.539$. HLL averages the contact into the middle state.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the flux is consistent and the scheme is conservative. If the speeds bound the waves of each local Riemann problem and $\frac{\Delta t}{\Delta x}\max|S| \le \frac12$, then (1) $U^*$ is the average of the exact Riemann solution over the fan, (2) for the Euler equations, positive density and pressure are kept, because the admissible set is convex and the new cell average is an average of admissible states, and (3) for any convex entropy pair $(\eta, q)$ the scheme satisfies the cell entropy inequality $\eta(U_j^{n+1}) \le \eta(U_j^n) - \lambda(Q_{j+1/2} - Q_{j-1/2})$ with a consistent numerical entropy flux $Q$. With the [Lax-Wendroff theorem](/lax-wendroff-theorem/), bounded $L^1$ limits are entropy weak solutions. For a convex scalar law the scheme is TVD for $\lambda\max|S| \le 1$.

The estimates of Davis and Einfeldt are not proven bounds: for Sod's data they give $S_R = 1.18322$ and $1.15190$, below the shock speed 1.75216. The positivity of HLLE with the Einfeldt speeds rests on the analysis of Einfeldt, Munz, Roe and Sjögreen (1991), which the proof here does not repeat.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: one HLL flux costs $O(m)$ operations, plus a constant number of square roots for the speeds. One step costs $O(mM)$ and the memory is $O(mM)$. A fixed end time at a fixed Courant number needs $O(M)$ steps, so the total cost is $O(mM^2)$. The cost per flux is close to that of the Rusanov flux and below that of the Roe flux, which needs the eigenvectors.

## Properties

- **First order and upwind.** For supersonic flow, $S_L \ge 0$ or $S_R \le 0$, and the flux is the upwind flux $F_L$ or $F_R$ exactly. The measured order on the smooth wave is 0.99 to 1.00.
- **Positive.** On the 123 problem ($W_L = (1, -2, 0.4)$, $W_R = (1, 2, 0.4)$, $M = 100$, $t = 0.15$), the smallest density is 0.0228 and the smallest pressure is 0.0070. The exact density at the center is 0.0219. Linearized solvers such as Roe's can give negative density on data of this kind (Einfeldt et al. 1991).
- **Entropy satisfying.** A transonic rarefaction is opened: for Burgers' equation with $u_L = -1$ and $u_R = 1$ the flux is $-\frac12$, not $f(\pm1) = \frac12$, so the jump spreads. No entropy fix is needed.
- **Smears contacts and shear waves.** The middle state has no structure, so a contact, at rest or moving, is smeared like in the Rusanov scheme.

## Variants and improvements

- **HLLC.** Restore the contact with two middle states separated by a contact speed $S^*$. See [HLLC](/hllc-riemann-solver/).
- **Rusanov.** Use one speed $S_R = -S_L = s$. See the [Rusanov flux](/rusanov-flux/).
- **Pressure-based speeds.** Estimate the middle pressure first, then set the speeds from the shock or rarefaction relations; this gives better bounds (Toro 2009, Chapter 10).
- **HLLEM and other one-state solvers with anti-diffusion.** Add back a part of the contact wave with an estimate of its strength (Einfeldt et al. 1991).
- **High order.** Use the flux on reconstructed values from [MUSCL](/muscl-scheme/) or WENO with a Runge-Kutta method. Positivity of the reconstruction then needs a [positivity-preserving limiter](/positivity-preserving-limiter/).

## When to use it

Use HLL or HLLE when robustness matters more than sharpness: near vacuum, strong rarefactions, strong shocks and for systems whose eigenstructure is costly. It is a good fallback in a code whose main solver is Roe or HLLC. Avoid it at first order when contacts, shear layers or boundary layers must stay sharp, because it smears them like the Rusanov flux.

## Pitfalls

- **Speeds that do not bound the waves.** The simple estimates can be too small for a strong shock (Sod's shock moves faster than both estimates). The scheme usually still works, but the proven properties then do not apply. Use pressure-based estimates when this matters.
- **The Roe average near vacuum.** The Einfeldt speeds need $\tilde c^2 > 0$. With extreme data, check it before the square root.
- **Dividing by $S_R - S_L$.** Lines L2 and L3 handle the supersonic cases first, so line L4 has $S_L < 0 < S_R$ and the divisor is positive. Do not reorder the tests.
- **Time step.** The theorems need $\lambda\max|S| \le \frac12$, a stricter bound than the usual Courant condition. The code uses $\nu = 0.9$ with $\max(|u| + c)$, which is a common choice that the tests show to work, not a proven bound.

## Implementations

## History

Harten, Lax and van Leer (1983) set up the theory of approximate Riemann solvers that are consistent with the integral form of the conservation law and of the entropy condition, and gave the solver with one middle state as the simplest example. Davis (1988) and Einfeldt (1988) proposed the speed estimates. Einfeldt showed that the choice with Roe averages keeps the density and the internal energy positive, and Einfeldt, Munz, Roe and Sjögreen (1991) showed that linearized solvers such as Roe's cannot have this property. Toro, Spruce and Speares (1994) added the contact wave to get HLLC.

## References
