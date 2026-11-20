---
tag: 6X7CE5
kind: algorithm
slug: flux-vector-splitting
name: Flux vector splitting
aliases:
- Steger-Warming splitting
- van Leer flux splitting
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Splits the flux into parts with nonnegative and nonpositive eigenvalues and upwinds each part, with no Riemann solver.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1 on smooth solutions", tvd: "for a scalar law split into monotone parts when dt max(f+' - f-') / dx <= 1", keeps_stationary_contact: false}
history:
  year: 1981
  people: [Joseph L. Steger, R. F. Warming, Bram van Leer]
  note: Steger and Warming (1981) split the Euler flux by the signs of the eigenvalues. Van Leer (1982) gave a splitting with parts that are smooth at the sonic points.
prereqs: [godunov-method, upwind-scheme, euler-equations-of-gas-dynamics]
see_also: [ausm-scheme, roe-solver, hll-riemann-solver, rusanov-flux, muscl-scheme, weno-scheme, finite-volume-method, total-variation-diminishing]
sources:
  - paper: "Joseph L. Steger and R. F. Warming, Flux vector splitting of the inviscid gasdynamic equations with application to finite-difference methods, Journal of Computational Physics 40(2) (1981) 263-293"
    locator: the splitting by the signs of the eigenvalues and the homogeneity property F = A U; doi:10.1016/0021-9991(81)90210-2
  - paper: "Bram van Leer, Flux-vector splitting for the Euler equations, in Eighth International Conference on Numerical Methods in Fluid Dynamics, Lecture Notes in Physics 170, Springer, 1982, 507-512"
    locator: the splitting by polynomials in the Mach number, smooth at the sonic points; doi:10.1007/3-540-11948-5_66
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 8 (the flux vector splitting approach, with the Steger-Warming and van Leer splittings)
  - paper: "Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49 (1983) 357-393"
    locator: the incremental form and the lemma on TVD coefficients; doi:10.1016/0021-9991(83)90136-5
  - paper: "Michael G. Crandall and Andrew Majda, Monotone difference approximations for scalar conservation laws, Mathematics of Computation 34 (1980) 1-21"
    locator: convergence of monotone schemes to the entropy solution
---

Flux vector splitting builds an upwind [finite volume](/finite-volume-method/) flux without solving a [Riemann problem](/riemann-problem/). It writes the physical flux as a sum $F(U) = F^+(U) + F^-(U)$, where $F^+$ carries only waves that move right and $F^-$ only waves that move left. At each face it takes the right-moving part from the left cell and the left-moving part from the right cell: $F_{j+1/2} = F^+(U_j) + F^-(U_{j+1})$. Steger and Warming (1981) split by the signs of the eigenvalues. Van Leer (1982) split by polynomials in the Mach number, so that the parts are smooth at the sonic points. Both give first order schemes that are cheap and robust. They smear contacts, even contacts at rest, because the splitting treats each side alone and never sees the jump.

## In plain words

At a cell face, some information flows right and some flows left. Flux vector splitting asks each cell on its own: how much of your flux goes right and how much goes left? The face then takes the right-going part of the left cell and the left-going part of the right cell, and adds them. No cell needs to know about its neighbor, so there is no Riemann problem to solve. When the gas moves faster than sound, everything goes one way and the scheme is plain upwinding. The price is that a jump between two cells is never seen as one wave, so contacts get blurred.

## The problem

Given cell averages $U_j^n$ of the [Euler equations](/euler-equations-of-gas-dynamics/) $U_t + F(U)_x = 0$ with $U = (\rho, \rho u, E)$, $F(U) = (\rho u, \rho u^2 + p, u(E + p))$, $E = p/(\gamma - 1) + \rho u^2/2$, $c = \sqrt{\gamma p/\rho}$, $H = (E + p)/\rho$ and $\gamma = 1.4$, compute face fluxes that make the conservative update $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$ consistent and stable, using only the state of each cell to form its part. The Mach number is $M = u/c$, and $x^\pm = (x \pm |x|)/2$.

## The algorithm

```pseudo id=main
STEGER-WARMING(U)
L1  λ <- (u - c, u, u + c);  r_1 <- (1, u - c, H - uc);  r_2 <- (1, u, u²/2);  r_3 <- (1, u + c, H + uc)
L2  return F^± <- (ρ/(2γ)) (λ_1^± r_1 + 2(γ-1) λ_2^± r_2 + λ_3^± r_3)

VAN-LEER(U)
L3  if M ≥ 1: return (F(U), 0);  if M ≤ -1: return (0, F(U))
L4  m^± <- ± ρc (M ± 1)²/4
L5  return F^± <- m^± (1, ((γ-1)u ± 2c)/γ, ((γ-1)u ± 2c)²/(2(γ²-1)))

FVS-FLUX(U_L, U_R)
L6  return F^+(U_L) + F^-(U_R)

FV-STEP(U, Δt, Δx)
L7  add one ghost cell on each side (copy for outflow, wrap for periodic)
L8  for each face j+1/2: F_{j+1/2} <- FVS-FLUX(U_j, U_{j+1})
L9  for each cell j: U_j <- U_j - (Δt/Δx)(F_{j+1/2} - F_{j-1/2})
```

Lines L1 and L2 use the fact that the Euler flux is homogeneous of degree one, so $F(U) = A(U)U$, and that $U = \frac{\rho}{2\gamma}r_1 + \frac{\rho(\gamma - 1)}{\gamma}r_2 + \frac{\rho}{2\gamma}r_3$. Splitting each eigenvalue into its positive and negative parts splits $F$. Line L3 makes supersonic flow pure upwinding. Lines L4 and L5 are van Leer's quadratic parts, which join the supersonic values with a matching slope at $M = \pm 1$.

## Example

**The flux by hand.** At the face of Sod's shock tube, $W_L = (\rho, u, p) = (1, 0, 1)$ and $W_R = (0.125, 0, 0.1)$, both states are at rest, so $M = 0$ on both sides. With $c_L = 1.18322$ and $c_R = 1.05830$:

- Steger-Warming: $F^\pm = \big(\pm\frac{\rho c}{2\gamma}, \frac{p}{2}, \pm\frac{\rho c^3}{2\gamma(\gamma - 1)}\big)$, so $F^+(U_L) = (0.422577, 0.5, 1.479020)$, $F^-(U_R) = (-0.047246, 0.05, -0.132288)$ and the face flux is $(0.375332, 0.55, 1.346732)$.
- Van Leer: $F^\pm = \big(\pm\frac{\rho c}{4}, \frac{p}{2}, \pm\frac{\rho c^3}{2(\gamma^2 - 1)}\big)$, so $F^+(U_L) = (0.295804, 0.5, 0.862762)$, $F^-(U_R) = (-0.033072, 0.05, -0.077168)$ and the face flux is $(0.262732, 0.55, 0.785594)$.

The exact Godunov flux is $(0.395391, 0.669837, 1.154038)$ (see the [exact Riemann solver](/exact-riemann-solver/)). Both splittings give the momentum flux $(p_L + p_R)/2 = 0.55$, because each side sees only its own pressure.

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$, outflow boundaries and Courant number 0.9, the scheme runs to $t = 0.2$. The table gives the $L^1$ error of the density against the exact cell averages (a 16-point midpoint rule in each cell), measured with the code on this page.

| cells $M$ | steps | Steger-Warming | van Leer |
|---|---|---|---|
| 50 | 24 | 0.02564 | 0.02070 |
| 100 | 48 | 0.01881 | 0.01457 |
| 200 | 97 | 0.01268 | 0.00967 |

For comparison, the [Roe solver](/roe-solver/) gives 0.00886 on 97 steps with 100 cells. The splittings are more diffusive, mostly at the contact.

**A smooth wave.** The density wave $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid is an exact solution. At $t = 0.1$ the van Leer errors for $M = 25, 50, 100, 200$ are $0.005588$, $0.002763$, $0.001385$ and $0.000693$, and the Steger-Warming errors are $0.004071$, $0.001970$, $0.000981$ and $0.000489$. Both have order 1.00 at the finest pair.

**A contact at rest.** Take $\rho = 1$ for $x < 0.5$ and $\rho = 0.125$ for $x > 0.5$, with $u = 0$ and $p = 1$. The van Leer mass flux at the jump is $(\rho_L c_L - \rho_R c_R)/4 = 0.191221$, not zero. With 100 cells, after 47 steps ($t = 0.1$), the densities in cells 47 to 54 are $0.928, 0.836, 0.709, 0.568, 0.440, 0.337, 0.263, 0.212$, and a velocity of up to 0.036 has appeared. Roe and HLLC keep this state exactly.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: both splittings satisfy $F^+(U) + F^-(U) = F(U)$, so the face flux is consistent, and the scheme is conservative; by the [Lax-Wendroff theorem](/lax-wendroff-theorem/), a limit of the scheme is a weak solution. The Steger-Warming parts are $F^\pm = A^\pm U$, where $A^\pm$ has the eigenvalues $\lambda_k^\pm$. The van Leer parts are continuous with continuous first derivatives at $M = \pm 1$, because the subsonic $F^\mp$ has the factor $(M \mp 1)^2$. For a scalar law $f = f^+ + f^-$ with $f^+$ nondecreasing and $f^-$ nonincreasing, the scheme is monotone and [TVD](/total-variation-diminishing/) when $\lambda\sup(f^{+\prime} - f^{-\prime}) \le 1$.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: each split costs $O(m)$ operations and one square root per cell, for $m$ conserved components, and each cell is split once per step, not once per face. One step costs $O(mM)$ and the memory is $O(mM)$. To reach a fixed time at a fixed Courant number takes $O(M)$ steps, so $O(mM^2)$ in all. There is no iteration, no Roe average and no eigenvector of a two-state matrix.

## Properties

- **First order.** The measured order on the smooth wave is 1.00.
- **Upwind for supersonic flow.** If $M \ge 1$ on both sides, the face flux is $F(U_L)$, as in the [upwind scheme](/upwind-scheme/).
- **Smooth parts (van Leer).** The van Leer parts are $C^1$ in $U$. The Jacobian of $F^+$ has the eigenvalue 0 for $|M| < 1$, and the test checks that the other two eigenvalues are not negative by the signs of the characteristic polynomial. Van Leer chose this so that a steady shock has at most two cells inside it.
- **Kinks (Steger-Warming).** The Steger-Warming parts have a kink where an eigenvalue is zero, at $u = 0$ and $u = \pm c$. This can give small glitches at sonic points.
- **Smears contacts and shear.** A contact at rest is not a steady state of the scheme (Proposition 5 in the proof). This is the main weakness, and it is worse for viscous flows, where a boundary layer is a shear layer.
- **One cell at a time.** Each split depends on one state only, which makes the scheme easy to vectorize and easy to make implicit, since $\partial F^\pm/\partial U$ is available in closed form.

## Variants and improvements

- **AUSM.** The [AUSM scheme](/ausm-scheme/) splits the flux into a convective part and a pressure part, and upwinds the convective part with one interface Mach number. It keeps contacts much sharper.
- **Hänel's variant.** Taking the energy part of van Leer's flux with the total enthalpy, $F_E^\pm = m^\pm H$, keeps $H$ constant across a steady flow. It is a common change for steady aerodynamics (Toro 2009, Chapter 8).
- **High order.** Use the split fluxes on reconstructed values from [MUSCL](/muscl-scheme/), or split the flux at each point and reconstruct $F^+$ and $F^-$ separately, as in finite difference [WENO](/weno-scheme/) codes. The local Lax-Friedrichs splitting $F^\pm = \frac12(F \pm sU)$ is the usual choice there.
- **Riemann solvers.** The [Roe](/roe-solver/), [HLL](/hll-riemann-solver/) and HLLC fluxes use both states together. They cost more per face but keep contacts sharper.

## When to use it

Use flux vector splitting when the flux must be cheap and robust, when the scheme is implicit and needs simple flux Jacobians, or as the flux inside a finite difference WENO code. Do not use it at first order for flows where contacts, shear layers or boundary layers must stay sharp. For those, use AUSM, HLLC or Roe.

## Pitfalls

- **Expecting a sharp contact.** Proposition 5 in the proof shows that even a contact at rest moves mass across the face. The smearing is a property of the method.
- **Steger-Warming glitches.** At a sonic point the Steger-Warming parts are not differentiable, and a small kink can appear in a transonic rarefaction. Van Leer's splitting avoids this.
- **Splitting a non-homogeneous flux.** The identity $F = AU$ holds for the ideal gas law. For a general equation of state it can fail, and $\sum_k \lambda_k^\pm w_k r_k$ then does not add up to $F$. Check $F^+ + F^- = F$ before using a splitting.
- **The time step.** The Courant condition must use $\max(|u| + c)$ over all cells. A split with $\lambda\max(f^{+\prime} - f^{-\prime}) > 1$ loses the TVD bound.
- **Mixing up the sides.** The face flux is $F^+(U_L) + F^-(U_R)$. Taking $F^+(U_R)$ gives a downwind scheme that blows up.

## Implementations

## History

Sanders and Prendergast had used a kinetic splitting for astrophysical flows in 1974. Steger and Warming (1981) gave the splitting of the Euler flux by the signs of the eigenvalues, based on the homogeneity of the flux, and used it in implicit finite difference schemes. Van Leer (1982) pointed out the kinks of that splitting at sonic points and gave a splitting by polynomials in the Mach number that is continuously differentiable. Liou and Steffen (1993) later split the convective and pressure parts apart, which led to the AUSM family.

## References
