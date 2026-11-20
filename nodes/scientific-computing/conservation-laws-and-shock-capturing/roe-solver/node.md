---
tag: 9FFHHH
kind: algorithm
slug: roe-solver
name: Roe solver
aliases:
- Roe approximate Riemann solver
- Roe linearization
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Approximates the Riemann problem by a linear one with a Roe-averaged Jacobian that resolves single shocks exactly.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m^2 M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1 on smooth solutions", exact_single_discontinuity: true, keeps_stationary_contact: true, entropy_satisfying: false, positive: false}
history:
  year: 1981
  people: [Philip L. Roe]
  note: Roe (1981) built a linearization with property U from a parameter vector, so that every single discontinuity is resolved exactly.
prereqs: [riemann-problem, godunov-method, hyperbolic-conservation-law]
see_also: [harten-hyman-entropy-fix, hll-riemann-solver, hllc-riemann-solver, rusanov-flux, exact-riemann-solver, flux-vector-splitting, rankine-hugoniot-conditions, lax-entropy-condition]
sources:
  - paper: "P. L. Roe, Approximate Riemann solvers, parameter vectors, and difference schemes, Journal of Computational Physics 43(2) (1981) 357-372"
    locator: property U, the parameter vector and the averaged Jacobian for the Euler equations; doi:10.1016/0021-9991(81)90128-5
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 4.14 (Roe's method for linear systems), Section 15.3 (approximate Riemann solvers, the Roe linearization and the entropy fix)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 11 (the Riemann solver of Roe, the Roe averages, the wave strengths and the entropy fix)
  - paper: "Bernd Einfeldt, Claus-Dieter Munz, Philip L. Roe and Björn Sjögreen, On Godunov-type methods near low densities, Journal of Computational Physics 92 (1991) 273-295"
    locator: linearized Riemann solvers are not positively conservative; doi:10.1016/0021-9991(91)90211-3
  - paper: "James J. Quirk, A contribution to the great Riemann solver debate, International Journal for Numerical Methods in Fluids 18(6) (1994) 555-574"
    locator: failures of the Roe solver such as the carbuncle and the odd-even decoupling; doi:10.1002/fld.1650180603
---

The Roe solver replaces the nonlinear [Riemann problem](/riemann-problem/) at a cell face by a linear one, $U_t + \hat A U_x = 0$, with a constant matrix $\hat A$ built from the two neighbor states. Roe (1981) chose $\hat A$ so that $F(U_R) - F(U_L) = \hat A(U_R - U_L)$ holds exactly. This "property U" makes the method conservative and makes it resolve any single shock or contact exactly. For the Euler equations, $\hat A$ is the Jacobian at a special average of the two states, the Roe average, weighted by $\sqrt\rho$. The flux needs the eigenvalues and eigenvectors of $\hat A$ but no iteration. It is one of the sharpest first order fluxes. It has two known flaws: it accepts expansion shocks, so it needs an [entropy fix](/harten-hyman-entropy-fix/), and it can give negative pressure near vacuum.

## In plain words

The exact Riemann problem at a face is nonlinear and needs an iteration. Roe asks a simpler question: which linear problem gives the right answer? A linear problem is a set of waves that each move at one fixed speed. Roe found an average state such that the linear waves at that state add up exactly to the jump between the two cells, and their fluxes add up exactly to the jump in the flux. Then each wave is upwinded by the sign of its own speed. A single shock, or a single contact, is one wave of the linear problem, so it comes out exactly right.

## The problem

Given cell averages $U_j^n$ of a [hyperbolic conservation law](/hyperbolic-conservation-law/) $U_t + F(U)_x = 0$, compute a face flux $F_{j+1/2}$ from $U_L = U_j$ and $U_R = U_{j+1}$ for the update $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$. The flux should be exact for a single discontinuity. The page uses the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$, $F = (\rho u, \rho u^2 + p, \rho u H)$, $H = (E + p)/\rho$, $c^2 = \gamma p/\rho$ and $\gamma = 1.4$, and a scalar law.

## The algorithm

```pseudo id=main
ROE-FLUX(U_L, U_R)
L1  ũ <- (√ρ_L u_L + √ρ_R u_R)/(√ρ_L + √ρ_R);  H̃ <- (√ρ_L H_L + √ρ_R H_R)/(√ρ_L + √ρ_R);  c̃ <- √((γ-1)(H̃ - ũ²/2))
L2  λ <- (ũ - c̃, ũ, ũ + c̃);  r_1 <- (1, ũ - c̃, H̃ - ũc̃);  r_2 <- (1, ũ, ũ²/2);  r_3 <- (1, ũ + c̃, H̃ + ũc̃)
L3  Δ <- U_R - U_L;  α_2 <- (γ-1)/c̃² (Δ_0 (H̃ - ũ²) + ũ Δ_1 - Δ_2);  α_1 <- (Δ_0 (ũ + c̃) - Δ_1 - c̃ α_2)/(2c̃);  α_3 <- Δ_0 - α_1 - α_2
L4  return (F(U_L) + F(U_R))/2 - (1/2) Σ_k |λ_k| α_k r_k

FV-STEP(U, Δt, Δx)
L5  add one ghost cell on each side (copy for outflow, wrap for periodic)
L6  for each face j+1/2: F_{j+1/2} <- ROE-FLUX(U_j, U_{j+1})
L7  for each cell j: U_j <- U_j - (Δt/Δx)(F_{j+1/2} - F_{j-1/2})
```

For a scalar law the code uses the same lines with one wave: $a = (f(u_R) - f(u_L))/(u_R - u_L)$ (or $f'(u_L)$ if the states are equal) and $F = \frac12(f_L + f_R) - \frac12|a|(u_R - u_L)$. This is the Murman-Roe scheme. The time step is $\Delta t = 0.9\,\Delta x/\max_j(|u_j| + c_j)$ with forward Euler. The code has no entropy fix. The [Harten-Hyman entropy fix](/harten-hyman-entropy-fix/) page adds one.

## Example

**The flux by hand.** Take Sod's states $W_L = (\rho, u, p) = (1, 0, 1)$ and $W_R = (0.125, 0, 0.1)$, so $\Delta = (-0.875, 0, -2.25)$. Line L1 gives $\tilde u = 0$, $\tilde H = 3.31716$ and $\tilde c = 1.15190$. Line L3 gives

$$\alpha_2 = \frac{0.4}{1.32686}(-0.875 \times 3.31716 + 2.25) = -0.196708, \qquad \alpha_1 = \alpha_3 = \frac{-0.875 + 0.196708}{2} = -0.339146.$$

The waves $1$ and $3$ have $|\lambda| = \tilde c$, the wave $2$ has $\lambda = 0$. Line L4 gives the mass flux $-\tilde c\,\alpha_1 = 0.390660$, the momentum flux $0.55$ (the two acoustic terms cancel), and the energy flux $-\tilde c\,\alpha_1\tilde H = 1.295882$. The exact Godunov flux is $(0.395391, 0.669837, 1.154038)$. The Roe mass flux is closer to it than the HLL value $0.510714$.

**Sod's tube.** On $[0, 1]$ with outflow boundaries and Courant number 0.9 at $t = 0.2$, the $L^1$ density errors against exact cell averages, measured with the code on this page, are 0.01319 ($M = 100$, 48 steps), 0.00886 ($M = 200$, 97 steps) and 0.00565 ($M = 400$, 194 steps). The observed orders are 0.57 and 0.65. On the same grids HLLC gives 0.01387, 0.00919 and 0.00581. The rarefaction of Sod's problem is not transonic: its head moves at $-1.18322$ and its tail at $u^* - c^*_L = -0.0703$. So the missing entropy fix does no harm here.

**A smooth wave.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid, the $L^1$ density errors at $t = 0.1$ for $M = 25, 50, 100, 200$ are $0.006143$, $0.003056$, $0.001536$ and $0.000770$, with orders 1.01, 0.99 and 1.00. These are the HLLC numbers to all digits shown: with constant $u$ and $p$ the data are pure contact waves, and both solvers give the upwind flux for them.

**Three discontinuities at rest.** Take a Mach 2 shock at rest: $W_L = (1, 2\sqrt{1.4}, 1)$ and $W_R = (8/3, 0.88741, 4.5)$. It satisfies the Rankine-Hugoniot condition with speed 0. On 40 cells, after 30 steps, the solution is unchanged to $10^{-12}$. A contact at rest is also kept. Now swap the two states. The result is a jump from subsonic to supersonic flow at rest, an expansion shock, which violates the [entropy condition](/lax-entropy-condition/). The Roe scheme keeps it too, unchanged. For Burgers' equation the jump from $u = -1$ to $u = 1$ gives $a = 0$, the flux $\frac12 = f(\pm 1)$ on every face, and the same steady expansion shock.

**Negative pressure.** The 123 problem has $W_L = (1, -2, 0.4)$ and $W_R = (1, 2, 0.4)$. At the center face $\tilde u = 0$, $\tilde H = 3.4$ and $\tilde c = 1.16619$, and $\alpha_1 = -\alpha_3 = -1.71499$. The Roe flux is $(0, 2.06762, 0)$: no mass and no energy leaves the center, but the momentum flux is much less than the true $4.4$. On 100 cells with the Courant number 0.9, after one step the two center cells have $\rho = 0.3451$ and $p = -0.5765$. HLL and HLLC run the same problem with positive pressure.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: (1) $\tilde c^2 > 0$ for any two physical states. (2) Property U: with the parameter vector $Z = \sqrt\rho(1, u, H)$, both $U$ and $F$ are quadratic in $Z$, so $F_R - F_L = \hat A(U_R - U_L)$ exactly, where $\hat A$ is the Jacobian at $(\tilde u, \tilde H)$. (3) The $r_k$ are the eigenvectors of $\hat A$ and $\sum_k\alpha_k r_k = U_R - U_L$. (4) The Roe flux is the Godunov flux of the linear problem $V_t + \hat A V_x = 0$. (5) The flux is consistent and the scheme is conservative. (6) If $U_L$ and $U_R$ are joined by a single discontinuity of speed $s$, the flux is $F_L$ for $s \ge 0$ and $F_R$ for $s < 0$, so a single shock or contact is exact, and one at rest is a steady solution. (7) For a scalar law, the Murman-Roe scheme is TVD for $\lambda\max|a| \le 1$. The scheme does not satisfy the entropy condition and is not positive, as the examples show.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: for a system of $m$ equations, the Roe flux costs $O(m^2)$ operations once the eigenvectors are known in closed form, as here, plus a constant number of square roots. One step costs $O(m^2 M)$ and the memory is $O(mM)$. A fixed end time at a fixed Courant number takes $O(M)$ steps, so the total is $O(m^2 M^2)$. For the Euler equations, $m = 3$, and the cost is a few times that of HLL.

## Properties

- **Exact for single waves.** The face flux of a single shock or contact is exact. One at rest stays sharp. A moving one still smears over a few cells, because the scheme averages over each cell every step.
- **Upwind on each field.** Each wave is upwinded by the sign of its own speed, so the dissipation on the contact wave is $\frac12|\tilde u|$, which is zero for a contact at rest.
- **Not entropy satisfying.** A sonic point is where some $\lambda_k$ changes sign. There the dissipation $|\lambda_k|$ is zero and an expansion shock can stay. The Harten-Hyman fix adds dissipation there.
- **Not positive.** Near vacuum and in strong rarefactions it can give negative density or pressure, as on the 123 problem.
- **Carbuncle.** In 2D, a strong shock aligned with the grid can grow a spurious bump, the carbuncle (Quirk 1994).

## Variants and improvements

- **Entropy fixes.** The [Harten-Hyman fix](/harten-hyman-entropy-fix/) replaces $|\lambda_k|$ near a sonic point by a larger value. Harten's earlier fix uses a smooth parabola with a fixed width.
- **Roe-type schemes for other systems.** A matrix with property U exists for every system with a convex entropy (Harten, Lax and van Leer 1983). For shallow water, MHD and real gases, special averages are known.
- **HLLE and HLLC.** These need only speed estimates and are positive. HLLC keeps contacts like Roe.
- **Flux difference splitting.** The Roe flux can be written $F_L + \hat A^-\Delta$, a split of the flux difference into left and right going parts. It contrasts with [flux vector splitting](/flux-vector-splitting/) (LeVeque 2002, Section 4.13).
- **High order.** Use the flux on [MUSCL](/muscl-scheme/) or WENO values with a Runge-Kutta method.

## When to use it

Use the Roe solver when sharp shocks and contacts matter and the flow stays away from vacuum, for example in steady aerodynamics. Always add an entropy fix. Prefer HLLC or HLLE near vacuum, in strong rarefactions and at strong shocks aligned with the grid. For systems with no closed form eigenvectors, the cost of the Roe solver grows, and HLL type solvers are simpler.

## Pitfalls

- **No entropy fix.** Without one, a transonic rarefaction can turn into an expansion shock. This is the most common error with Roe's solver.
- **The arithmetic mean.** Taking $\hat A$ as the Jacobian at $\frac12(U_L + U_R)$ breaks property U. The scheme is then still conservative, but shocks are no longer exact. The weights must be $\sqrt{\rho}$.
- **Negative pressure.** Check density and pressure after each step, and fall back to HLL in cells where they become negative.
- **Dividing by $\tilde c$.** The strengths of line L3 divide by $\tilde c$. Lemma 1 of the proof shows $\tilde c > 0$ for physical states, but a state with $p \le 0$ gives a domain error.

## Implementations

## History

Roe (1981) introduced the linearization with property U and the parameter vector $Z = \sqrt\rho(1, u, H)$ for the Euler equations. The scalar scheme is often called the Murman-Roe scheme, after earlier work of Murman on transonic flow. Harten, Lax and van Leer (1983) proved that a Roe matrix exists for every system with a convex entropy. Harten and Hyman (1983) gave the entropy fix used with the solver. Einfeldt, Munz, Roe and Sjögreen (1991) showed that linearized solvers are not positive, and Quirk (1994) collected the failures of the solver in 2D, among them the carbuncle.

## References
