---
tag: PDKD22
kind: algorithm
slug: rusanov-flux
name: Rusanov flux
aliases:
- local Lax-Friedrichs flux
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: A numerical flux that averages the two physical fluxes and adds dissipation scaled by the largest local wave speed. Simple, robust and first order.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1 on smooth solutions", tvd: "for a convex scalar law when dt max s / dx <= 1", keeps_stationary_contact: false}
history:
  year: 1961
  people: [V. V. Rusanov]
  note: Rusanov (1961) computed shock waves with a scheme whose dissipation was scaled by the local largest wave speed. The name local Lax-Friedrichs flux came later.
prereqs: [finite-volume-method, godunov-method, lax-friedrichs-scheme]
see_also: [hll-riemann-solver, roe-solver, exact-riemann-solver, kurganov-tadmor-scheme, muscl-scheme, total-variation-diminishing, euler-equations-of-gas-dynamics, positivity-preserving-limiter]
sources:
  - paper: "V. V. Rusanov, The calculation of the interaction of non-stationary shock waves with obstacles, Zhurnal Vychislitel'noi Matematiki i Matematicheskoi Fiziki 1(2) (1961) 267-279; English translation in USSR Computational Mathematics and Mathematical Physics 1(2) (1962) 304-320"
    locator: the scheme with dissipation scaled by the local largest wave speed; the page relies on the English translation; doi:10.1016/0041-5553(62)90062-9
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 12.4 (numerical viscosity), Section 12.5 (the Lax-Friedrichs and local Lax-Friedrichs methods), Section 12.7 (E-schemes), Section 12.12 (nonlinear stability)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 10 (the HLL solver; the Rusanov flux is the HLL flux with one speed)
  - paper: "Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49 (1983) 357-393"
    locator: the incremental form and the lemma on TVD coefficients; doi:10.1016/0021-9991(83)90136-5
  - paper: "Bernd Einfeldt, Claus-Dieter Munz, Philip L. Roe and Björn Sjögreen, On Godunov-type methods near low densities, Journal of Computational Physics 92 (1991) 273-295"
    locator: positivity of HLL type fluxes when the speeds bound the waves; doi:10.1016/0021-9991(91)90211-3
---

The Rusanov flux is the simplest numerical flux for a [finite volume](/finite-volume-method/) scheme. At each cell face it takes the average of the physical fluxes of the two neighbor states and subtracts a dissipation term, $\frac12 s (U_R - U_L)$, where $s$ is the largest wave speed of the two states. It is also called the local Lax-Friedrichs flux, because it is the [Lax-Friedrichs scheme](/lax-friedrichs-scheme/) with the dissipation set by the local speed instead of $\Delta x/\Delta t$. It needs no [Riemann problem](/riemann-problem/) solution and no eigenvectors, only one speed. The price is more dissipation than the [Roe](/roe-solver/), [HLL](/hll-riemann-solver/) and [HLLC](/hllc-riemann-solver/) fluxes: it smears contact discontinuities, and even a contact at rest is not kept.

## In plain words

A finite volume scheme stores the average of the solution in each cell. Each step it moves stuff between neighbor cells through the faces. The amount that crosses a face is the flux. The left cell and the right cell each say what the flux is. The Rusanov flux takes the mean of the two answers. That mean alone gives wild wiggles, so it adds a correction that moves stuff from the larger value to the smaller value, like a small diffusion. The size of the correction is the fastest wave speed near the face. Fast waves get more smoothing, slow waves get less. This is enough to make the scheme stable, and it is very cheap.

## The problem

Given cell averages $U_j^n$ of a [hyperbolic conservation law](/hyperbolic-conservation-law/) $U_t + F(U)_x = 0$, compute a numerical flux $F_{j+1/2} = F(U_j, U_{j+1})$ at each face so that the conservative update $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$ is consistent and stable. The page uses two cases: a scalar law $u_t + f(u)_x = 0$, and the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$, $F(U) = (\rho u, \rho u^2 + p, u(E + p))$, $E = p/(\gamma - 1) + \rho u^2/2$, sound speed $c = \sqrt{\gamma p/\rho}$ and $\gamma = 1.4$. The cells are $C_j = [x_{j-1/2}, x_{j+1/2}]$ with width $\Delta x$, and $U_j^n$ is a cell average.

## The algorithm

```pseudo id=main
RUSANOV-FLUX(U_L, U_R)
L1  s <- max(|u_L| + c_L, |u_R| + c_R)            ▷ scalar law: s <- max(|f'(u_L)|, |f'(u_R)|)
L2  return (F(U_L) + F(U_R))/2 - (s/2)(U_R - U_L)

FV-STEP(U, Δt, Δx)
L3  add one ghost cell on each side (copy for outflow, wrap for periodic)
L4  for each face j+1/2: F_{j+1/2} <- RUSANOV-FLUX(U_j, U_{j+1})
L5  for each cell j: U_j <- U_j - (Δt/Δx)(F_{j+1/2} - F_{j-1/2})
```

The time step is $\Delta t = \nu \Delta x/\max_j(|u_j| + c_j)$ with a Courant number $\nu \le 1$. The code uses $\nu = 0.9$ and forward Euler in time. With [MUSCL](/muscl-scheme/) reconstruction and an [SSP Runge-Kutta](/strong-stability-preserving-runge-kutta/) method, the same flux gives a second order scheme.

## Example

**The flux by hand.** Take the two states of Sod's shock tube: $W_L = (\rho, u, p) = (1, 0, 1)$ and $W_R = (0.125, 0, 0.1)$. The conserved states are $U_L = (1, 0, 2.5)$ and $U_R = (0.125, 0, 0.25)$. The fluxes are $F(U_L) = (0, 1, 0)$ and $F(U_R) = (0, 0.1, 0)$. The sound speeds are $c_L = \sqrt{1.4} = 1.18322$ and $c_R = \sqrt{1.12} = 1.05830$, so $s = 1.18322$. Line L2 gives

$$F = \big(0 - 0.59161 \times (-0.875),\ 0.55 - 0,\ 0 - 0.59161 \times (-2.25)\big) = (0.517657, 0.55, 1.331118).$$

The exact Godunov flux at this face is $(0.395391, 0.669837, 1.154038)$ (see the [exact Riemann solver](/exact-riemann-solver/)). The Rusanov flux moves too much mass and energy, which is the extra dissipation.

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$, outflow boundaries and $\nu = 0.9$, the scheme runs to $t = 0.2$. The table gives the $L^1$ error of the density against the exact cell averages (a 16-point midpoint rule in each cell). These numbers are measurements made with the code on this page.

| cells $M$ | steps | $\lVert e_\rho \rVert_1$ |
|---|---|---|
| 100 | 47 | 0.02148 |
| 200 | 96 | 0.01515 |
| 400 | 193 | 0.00998 |

The observed orders are 0.50 and 0.60. The solution has a shock and a contact, so the order is far below 1, as expected for a first order scheme near discontinuities.

**A smooth wave.** The density wave $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid is an exact solution. At $t = 0.1$ the $L^1$ density errors for $M = 25, 50, 100, 200$ are $0.017181$, $0.008784$, $0.004459$ and $0.002246$, with observed orders 0.97, 0.98 and 0.99. This is the combined order in space and time, at a fixed Courant number.

**A contact at rest.** Take $\rho = 1$ on the left half and $\rho = 0.5$ on the right half, with $u = 0$ and $p = 1$ everywhere. This is an exact steady solution. With 40 cells, after 8 steps ($t = 0.1$) the velocity and the pressure are still exact to rounding, but the density in the 8 cells around the contact is $0.967, 0.924, 0.861, 0.782, 0.703, 0.632, 0.579, 0.540$. The term $\frac12 s(\rho_R - \rho_L)$ is a mass flux even though the gas does not move.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the flux is consistent, $F(U, U) = F(U)$, and the scheme is conservative, so the [Lax-Wendroff theorem](/lax-wendroff-theorem/) applies: if the scheme converges boundedly in $L^1_{loc}$, the limit is a weak solution. For a convex scalar law, the scheme is in Harten's incremental form with coefficients $C_{j+1/2} = \frac{\lambda}{2}(s - a)_{j+1/2}$ and $D_{j+1/2} = \frac{\lambda}{2}(s + a)_{j+1/2}$, where $a$ is the slope of $f$ between the two states. These are nonnegative because $|a| \le s$, and their sum is $\lambda s$. So the scheme is [TVD](/total-variation-diminishing/) for $\lambda \max s \le 1$, and each new value is a convex combination of its three old neighbors for $\lambda \max s \le 1/2$. For the Euler equations, positivity of density and pressure holds when $s$ bounds the true wave speeds and $\lambda s \le 1/2$ (Einfeldt, Munz, Roe and Sjögreen 1991). The simple speed estimate of line L1 is not a proven bound in every case.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: one flux costs $O(m)$ operations and one square root per state, for $m$ conserved components. One step costs $O(mM)$ for $M$ cells, and the memory is $O(mM)$. To reach a fixed time $T$ at a fixed Courant number, the scheme needs $O(M)$ steps, so the total cost is $O(mM^2)$. The flux has no iteration and no eigenvector, so it is the cheapest flux on the pages of this group.

## Properties

- **First order.** The dissipation coefficient $s/2$ does not go to zero where the solution is smooth. The measured order on the smooth wave is 0.97 to 0.99.
- **Monotone character for scalar laws.** For a convex $f$, the scheme is TVD under the stated Courant condition (Theorem above). It is an E-scheme (LeVeque 2002, Section 12.7), so its limits satisfy the entropy condition for scalar laws.
- **Robust.** It needs only a bound on the wave speeds. It works for any hyperbolic system for which one can bound the eigenvalues of the Jacobian, even when the eigenvectors are unknown or hard to compute.
- **Smears contacts.** A contact, at rest or moving, is smeared, because the dissipation acts on all fields with the same coefficient $s$. Roe and HLLC keep a contact at rest exactly.
- **Positive under a condition.** With true wave speed bounds and $\lambda s \le 1/2$, density and pressure stay positive. On the 123 problem ($W_L = (1, -2, 0.4)$, $W_R = (1, 2, 0.4)$, $M = 100$, $t = 0.15$) the smallest density is 0.0299 and the smallest pressure is 0.0081. The exact density at the center is 0.0219.

## Variants and improvements

- **Global Lax-Friedrichs.** Use one speed $s = \max_j(|u_j| + c_j)$ for all faces. This is the flux splitting used by [WENO](/weno-scheme/) finite difference codes. It is more dissipative.
- **HLL.** Replace the one speed by two speeds, $S_L < 0 < S_R$ estimated from each side. The result is the [HLL flux](/hll-riemann-solver/), which is less dissipative when the flow is fast in one direction.
- **Kurganov-Tadmor.** The semi-discrete central scheme of [Kurganov and Tadmor](/kurganov-tadmor-scheme/) uses the Rusanov flux on reconstructed interface values. At first order the two schemes are the same.
- **High order.** Use the flux on reconstructed values $U_{j+1/2}^-$ and $U_{j+1/2}^+$ from [MUSCL](/muscl-scheme/), [ENO](/eno-scheme/) or WENO. The dissipation is then $O(\Delta x^{k})$ times the jump, small where the solution is smooth.
- **Discontinuous Galerkin.** The Rusanov flux is a common face flux of [discontinuous Galerkin](/discontinuous-galerkin-method/) methods.

## When to use it

Use the Rusanov flux to start a new code, for a system whose eigenvectors are hard to compute (magnetohydrodynamics, relativistic flows, many coupled equations), and as a robust fallback where a sharper flux fails. With a high order reconstruction the extra dissipation matters less. Do not use it at first order when contacts or shear layers must stay sharp; use HLLC or Roe there.

## Pitfalls

- **Speed of one state only.** Taking $s$ from $U_L$ or from $U_R$ alone can give $s$ smaller than $|f'|$ on the other side. The scheme then loses its TVD bound and can oscillate.
- **A non-convex flux.** For a scalar law with a non-convex $f$, the endpoint speeds do not bound $|f'|$ between them. Take the maximum of $|f'|$ over the interval between $u_L$ and $u_R$.
- **Time step from the old speeds.** The Courant condition must use the largest speed over all cells, including the ghost cells. A step chosen from the interior only can be too large at a boundary.
- **Expecting a sharp contact.** The smeared contact is a property of the flux, not a bug. Do not try to fix it with a smaller $s$, which breaks stability.

## Implementations

## History

Rusanov (1961) published a scheme for the interaction of shock waves with obstacles in which the artificial dissipation was proportional to the local value of $|u| + c$. Lax (1954) had used the global form, now called the Lax-Friedrichs scheme. The flux with the maximum of the speeds of the two neighbor states is the form in modern books (LeVeque 2002, Section 12.5; Toro 2009, Chapter 10), where it appears as the local Lax-Friedrichs flux and as the HLL flux with the single speed $s$.

## References
