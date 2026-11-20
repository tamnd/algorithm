---
tag: H6NW64
kind: algorithm
slug: ausm-scheme
name: AUSM scheme
aliases:
- advection upstream splitting method
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: Splits the flux into a convective part upwinded by an interface Mach number and a pressure part, and keeps contacts at rest exactly.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1 on smooth solutions", keeps_stationary_contact: true, keeps_moving_contact: false, positive: "not guaranteed; on a shock tube the first step needs a Courant number bound"}
history:
  year: 1993
  people: [Meng-Sing Liou, Christopher J. Steffen]
  note: Liou and Steffen (1993) split the Euler flux into a convective part and a pressure part and upwinded the convective part with one interface Mach number built from van Leer's Mach number split.
prereqs: [flux-vector-splitting, godunov-method, euler-equations-of-gas-dynamics]
see_also: [roe-solver, hllc-riemann-solver, hll-riemann-solver, rusanov-flux, muscl-scheme, exact-riemann-solver, lax-wendroff-theorem, positivity-preserving-limiter]
sources:
  - paper: "Meng-Sing Liou and Christopher J. Steffen, A new flux splitting scheme, Journal of Computational Physics 107(1) (1993) 23-39"
    locator: the split into convective and pressure parts, the interface Mach number from the Mach number split, and the pressure split; doi:10.1006/jcph.1993.1122
  - paper: "Bram van Leer, Flux-vector splitting for the Euler equations, in Eighth International Conference on Numerical Methods in Fluid Dynamics, Lecture Notes in Physics 170, Springer, 1982, 507-512"
    locator: the split of the Mach number into the parts (M + 1)^2/4 and -(M - 1)^2/4; doi:10.1007/3-540-11948-5_66
  - paper: "Meng-Sing Liou, A sequel to AUSM: AUSM+, Journal of Computational Physics 129(2) (1996) 364-382"
    locator: the AUSM+ scheme, with a common interface sound speed and split polynomials of higher degree; doi:10.1006/jcph.1996.0256
---

The AUSM scheme (advection upstream splitting method) of Liou and Steffen (1993) is a face flux for the Euler equations that sits between [flux vector splitting](/flux-vector-splitting/) and Riemann solvers. It writes the Euler flux as a convective part, the velocity times $(\rho, \rho u, \rho H)$, plus a pressure part $(0, p, 0)$. The convective part is upwinded with one interface Mach number, made from the right-going Mach part of the left state and the left-going Mach part of the right state. The pressure is split in the same way. The flux costs about as much as flux vector splitting and needs no Riemann solver. Unlike van Leer's splitting, it keeps a contact at rest exactly. The price is that no mass and no energy cross a face between two states at rest, which limits the time step on shock tubes.

## In plain words

Gas carries mass, momentum and energy along with it, and pressure pushes on it. AUSM treats these two effects apart. For the carried part, it asks how fast the gas crosses the face, in units of the speed of sound. Each side gives its share of that Mach number, the two shares are added, and the sign of the sum says which side the carried values come from. For the push, each side gives its share of the pressure. When the gas is faster than sound, everything comes from upstream. When the gas is at rest on both sides, the two Mach shares cancel, so nothing is carried, and the pressure is the mean of the two sides.

## The problem

Given cell averages $U_j^n$ of the [Euler equations](/euler-equations-of-gas-dynamics/) $U_t + F(U)_x = 0$ with $U = (\rho, \rho u, E)$, $F(U) = (\rho u, \rho u^2 + p, u(E + p))$, $E = p/(\gamma - 1) + \rho u^2/2$, $c = \sqrt{\gamma p/\rho}$, $H = (E + p)/\rho$, $M = u/c$ and $\gamma = 1.4$, compute face fluxes from the two neighbor states that make the conservative update $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$ consistent and upwind, and that keep contacts sharp.

## The algorithm

```pseudo id=main
AUSM-FLUX(U_L, U_R)
L1  M^± <- ±(M ± 1)²/4 if |M| ≤ 1, else (M ± |M|)/2
L2  p^± <- p (M ± 1)² (2 ∓ M)/4 if |M| ≤ 1, else p (M ± |M|)/(2M)
L3  M_{1/2} <- M_L^+ + M_R^-
L4  p_{1/2} <- p_L^+ + p_R^-
L5  Φ <- c(ρ, ρu, ρH) of U_L if M_{1/2} ≥ 0, else of U_R
L6  return M_{1/2} Φ + (0, p_{1/2}, 0)

FV-STEP(U, Δt, Δx)
L7  add one ghost cell on each side (copy for outflow, wrap for periodic); F_{j+1/2} <- AUSM-FLUX(U_j, U_{j+1})
L8  for each cell j: U_j <- U_j - (Δt/Δx)(F_{j+1/2} - F_{j-1/2})
```

Line L1 is van Leer's Mach number split. Line L2 splits the pressure with weights that are 1 and 0 for supersonic flow and that join those values with matching slopes at $M = \pm 1$. Since $Mc(\rho, \rho u, \rho H) = (\rho u, \rho u^2, u(E + p))$, lines L5 and L6 give the Euler flux when both states are equal. Liou and Steffen write line L5 as $\frac12 M_{1/2}(\Phi_L + \Phi_R) - \frac12|M_{1/2}|(\Phi_R - \Phi_L)$, which is the same thing. The code uses the time step $\Delta t = 0.5\,\Delta x/\max(|u| + c)$.

## Example

**Split values by hand.** At $M = \frac12$, line L1 gives $M^+ = \frac9{16}$ and $M^- = -\frac1{16}$, and line L2 with $p = 1$ gives $p^+ = \frac{27}{32}$ and $p^- = \frac5{32}$. The sums are $\frac12$ and 1. The test checks these values exactly in `Fraction` arithmetic.

**Sod's face.** For $W_L = (\rho, u, p) = (1, 0, 1)$ and $W_R = (0.125, 0, 0.1)$, both states are at rest, so $M_{1/2} = \frac14 - \frac14 = 0$, $p_{1/2} = 0.55$, and the flux is $(0, 0.55, 0)$. The exact Godunov flux is $(0.395391, 0.669837, 1.154038)$ (see the [exact Riemann solver](/exact-riemann-solver/)). AUSM moves momentum but no mass and no energy across this face in the first step.

**A moving contact.** For $W_L = (1, 0.5, 1)$ and $W_R = (0.5, 0.5, 1)$, the sound speeds are $c_L = 1.183216$ and $c_R = 1.673320$, so $M_L = 0.422577$ and $M_R = 0.298807$. Then $M_L^+ = 0.505931$, $M_R^- = -0.122918$ and $M_{1/2} = 0.383013$. The pressure is $p_L^+ + p_R^- = 0.798068 + 0.282564 = 1.080632$. With $\Phi_L = c_L(1, 0.5, 3.625)$, the flux is $(0.453188, 1.307226, 1.642806)$. The exact flux of this contact is $F(U_L) = (0.5, 1.25, 1.8125)$, which the [Roe solver](/roe-solver/) gets. So AUSM keeps contacts at rest but not moving contacts.

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$, outflow boundaries and Courant number 0.5, the scheme runs to $t = 0.2$. The table gives the $L^1$ error of the density against exact cell averages (a 16-point midpoint rule in each cell), measured with the code on this page and with the codes of the Roe and flux vector splitting pages at the same Courant number.

| cells $M$ | AUSM | steps | Roe | van Leer splitting |
|---|---|---|---|---|
| 50 | 0.02250 | 43 | 0.02362 | 0.02506 |
| 100 | 0.01484 | 87 | 0.01626 | 0.01748 |
| 200 | 0.00952 | 174 | 0.01077 | 0.01151 |

The [Rusanov flux](/rusanov-flux/) gives 0.02350 with 100 cells. At 100 cells the velocity in the first cell right of the initial jump is 1.010, against the exact value 0.9274 behind the rarefaction. The largest velocity of the Roe run is 0.932. The other cells near the jump are close to the Roe values.

**A smooth wave.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid to $t = 0.1$, the $L^1$ density errors at $M = 25, 50, 100, 200$ are 0.007065, 0.003573, 0.001797 and 0.000901 (orders 0.98, 0.99 and 1.00).

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the Mach and pressure splits add up to $M$ and $p$ and have continuous first derivatives at $M = \pm 1$, so the face flux is consistent and continuous, and the scheme is conservative; by the [Lax-Wendroff theorem](/lax-wendroff-theorem/) a limit of the scheme is a weak solution. For supersonic flow on both sides the flux is $F(U_L)$ or $F(U_R)$. Between states at rest the flux is $(0, \frac12(p_L + p_R), 0)$, so a contact at rest is kept exactly, also in floating point arithmetic. The same fact gives a bound for the first step of a shock tube: the low pressure cell keeps its density and energy but gains the momentum $\frac12\lambda(p_L - p_R)$, and its pressure stays positive only if $\lambda < \frac{2}{p_L - p_R}\sqrt{2\rho_R p_R/(\gamma - 1)}$.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: each face flux costs $O(m)$ operations and two square roots, for $m = 3$ conserved components. One step costs $O(mM)$ and the memory is $O(mM)$. To reach a fixed time at a fixed Courant number takes $O(M)$ steps, so $O(mM^2)$ in all. There is no iteration, no average state and no eigenvector.

## Properties

- **First order.** The measured order on the smooth wave is 1.00. For higher order, put reconstructed face values into the flux.
- **Upwind for supersonic flow.** If $M \ge 1$ on both sides, the face flux is $F(U_L)$.
- **Keeps contacts at rest.** Proved and tested exactly. Van Leer's flux vector splitting moves mass across such a contact.
- **Does not keep moving contacts.** The two sides use their own sound speeds, so a contact moving at $u = 0.5$ gets a mass flux of 0.453 instead of 0.5 in the example. After the contact has moved 0.2 on 100 cells, $u$ and $p$ are off by about 0.03.
- **Not positivity preserving.** On Sod's tube the first step gives a negative pressure for Courant numbers above 0.6574 (proved). The code fails at 0.7 to 0.9 and runs at 0.5 and 0.6.

## Variants and improvements

- **AUSM+.** Liou (1996) uses one common sound speed at the face for both Mach numbers and split polynomials of higher degree.
- **High order.** Use the flux with [MUSCL](/muscl-scheme/) or WENO face values and a Runge-Kutta time step, as with any face flux.
- **Riemann solvers.** [HLLC](/hllc-riemann-solver/) and Roe keep both contacts at rest and moving contacts, at the cost of more work per face.

## When to use it

Use AUSM as a cheap face flux for steady and unsteady gas dynamics when contacts at rest must stay sharp and flux vector splitting smears them too much. For shock tubes with large pressure ratios, use a smaller time step, a variant from the AUSM family, or a Riemann solver such as HLLC. If moving contacts must stay sharp, use HLLC or Roe.

## Pitfalls

- **The time step on shock tubes.** Between states at rest no mass and no energy cross a face. A Courant number that is safe for Roe or HLLC can give a negative pressure in the first step. For the data $(1, 0, 1000)$ and $(1, 0, 0.01)$ the bound is 0.0167.
- **A glitch near the initial jump.** The code shows a velocity overshoot of about 9 percent in one cell next to the initial jump on Sod's tube.
- **Expecting a sharp moving contact.** Only contacts at rest are kept exactly.
- **Mixing up the sides.** The interface Mach number is $M_L^+ + M_R^-$. Taking $M_R^+$ gives a downwind flux.
- **Mixing AUSM and AUSM+.** The original scheme uses $c_L$ for $M_L$ and $c_R$ for $M_R$; AUSM+ uses one common value and other polynomials. The results differ.

## Implementations

## History

Van Leer (1982) split the Euler flux by polynomials in the Mach number. Liou and Steffen (1993) took his Mach number split and used it only for the interface Mach number that carries the convective part, with the pressure split apart. They called the result the advection upstream splitting method. Liou (1996) gave AUSM+, with a common sound speed at the face, and the scheme grew into a family of fluxes.

## References
