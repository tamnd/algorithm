---
tag: FE63NV
kind: algorithm
slug: runge-kutta-discontinuous-galerkin
name: Runge-Kutta discontinuous Galerkin method
aliases:
- RKDG
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: "The Cockburn-Shu method for conservation laws: discontinuous Galerkin in space, SSP Runge-Kutta in time and a TVB slope limiter after each stage, so shocks are captured without oscillations."
solves: [burgers-equation, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", k: "the polynomial degree", N: "the number of time steps"}
  time: {worst: "Θ(N M (k+1)^2)"}
  space: {extra: "Θ(M (k+1))"}
properties: {deterministic: true, explicit: true, conservative: true, tvdm: "with TVB constant 0 and a CFL condition", order: "k + 1 for smooth solutions with a large enough TVB constant (measured)"}
history:
  year: 1989
  people: [B. Cockburn, C.-W. Shu]
  note: Cockburn and Shu combined the discontinuous Galerkin space discretization with the SSP Runge-Kutta methods of Shu and Osher and a TVB limiter, in a series of papers from 1989 to 1998.
prereqs: [discontinuous-galerkin-method, strong-stability-preserving-runge-kutta, total-variation-diminishing]
see_also: [flux-limiter-methods, muscl-scheme, weno-scheme, godunov-method, positivity-preserving-limiter, entropy-stable-scheme, burgers-equation, hyperbolic-conservation-law]
sources:
  - paper: doi:10.1090/S0025-5718-1989-0983311-4
    title: "Bernardo Cockburn and Chi-Wang Shu, TVB Runge-Kutta local projection discontinuous Galerkin finite element method for conservation laws II: general framework, Mathematics of Computation 52(186) (1989) 411-435"
    locator: the TVB limiter with the constant M, the TVDM and TVBM properties, convergence for scalar laws
  - paper: doi:10.1023/A:1012873910884
    title: Bernardo Cockburn and Chi-Wang Shu, Runge-Kutta discontinuous Galerkin methods for convection-dominated problems, Journal of Scientific Computing 16(3) (2001) 173-261
    locator: the RKDG method for scalar conservation laws in one dimension, the generalized slope limiter, systems and multidimensional problems
  - paper: "Bernardo Cockburn and Chi-Wang Shu, The Runge-Kutta discontinuous Galerkin method for conservation laws V: multidimensional systems, Journal of Computational Physics 141 (1998) 199-224"
    locator: the limiter for systems in characteristic variables and on general meshes
  - paper: "Chi-Wang Shu and Stanley Osher, Efficient implementation of essentially non-oscillatory shock-capturing schemes, Journal of Computational Physics 77 (1988) 439-471"
    locator: the three-stage TVD (SSP) Runge-Kutta method
  - book: isbn:9780387720654
    title: Jan S. Hesthaven and Tim Warburton, Nodal Discontinuous Galerkin Methods, Springer, 2008
    locator: Chapter 5 (nonlinear problems, filtering and limiting)
---

The Runge-Kutta discontinuous Galerkin (RKDG) method of Cockburn and Shu solves nonlinear conservation laws $u_t + f(u)_x = 0$ with shocks. It has three parts. The [discontinuous Galerkin method](/discontinuous-galerkin-method/) discretizes space with a polynomial of degree $k$ in each cell and a monotone numerical flux on each face. An explicit [SSP Runge-Kutta](/strong-stability-preserving-runge-kutta/) method advances in time. A slope limiter, applied after every stage, compares the polynomial in each cell with the averages of its neighbours and, where they disagree, replaces it by a linear function with a limited slope. With the plain minmod limiter the cell averages are total variation diminishing (TVDM) under a CFL condition. The TVB version, with a constant $M$, leaves the polynomial alone near smooth extrema, so the method keeps order $k + 1$ in smooth regions and still captures shocks within one or two cells without oscillations.

## In plain words

High-degree polynomials in each cell give very accurate answers for smooth flows, but near a shock they wiggle, and the wiggles do not go away when the cells get smaller. RKDG fixes this with a check after every small time step. For each cell it looks at the averages of the cell and its two neighbours. If the polynomial at the cell walls goes above or below what the neighbouring averages allow, the cell is suspect, and its polynomial is replaced by a straight line with a slope that is no steeper than the neighbours permit. Smooth regions pass the check and keep their full polynomials. A tolerance lets small smooth peaks pass the check too, so they are not flattened.

## The problem

Given a flux $f$, periodic initial data $u_0$ on $[x_L, x_R]$ and a final time $T$, approximate the entropy solution of $u_t + f(u)_x = 0$ on $M$ cells of width $\Delta x$, with $u_h = \sum_{l=0}^k U_{j,l}P_l(\xi)$ on cell $C_j$ as on the [DG page](/discontinuous-galerkin-method/) and $\bar u_j = U_{j,0}$ the cell average. The numerical flux $\hat F(a, b)$ is consistent and monotone (nondecreasing in $a$, nonincreasing in $b$), with Lipschitz constants $L_1$ and $L_2$ in its two arguments. Here we use Godunov's flux for [Burgers' equation](/burgers-equation/), $f(u) = u^2/2$. The goal is an approximation that is order $k + 1$ where the solution is smooth and has no growing oscillations at shocks.

## The algorithm

For a cell $j$ let $\Delta^+ = \bar u_{j+1} - \bar u_j$, $\Delta^- = \bar u_j - \bar u_{j-1}$, and let the face deviations be $\tilde u_j = u_h(x_{j+1/2}^-) - \bar u_j$ and $\tilde{\tilde u}_j = \bar u_j - u_h(x_{j-1/2}^+)$. The modified minmod function is

$$\tilde m(a, b, c) = \begin{cases} a & \text{if } |a| \le M\Delta x^2, \\ m(a, b, c) & \text{otherwise,} \end{cases} \qquad m(a, b, c) = \begin{cases} s\min(|a|, |b|, |c|) & \text{if } s = \operatorname{sign} a = \operatorname{sign} b = \operatorname{sign} c, \\ 0 & \text{otherwise.} \end{cases}$$

```pseudo id=main
RKDG(U, Δx, Δt, T, f, F̂, M)
L1  U ← LIMIT(U); repeat until t = T:                     ▷ the last step is shortened
L2      U¹ ← LIMIT(U + Δt L(U))                           ▷ L is the DG operator
L3      U² ← LIMIT(¾ U + ¼ (U¹ + Δt L(U¹)))
L4      U ← LIMIT(⅓ U + ⅔ (U² + Δt L(U²)))
    LIMIT(U): for each cell j do
L5      compute Δ⁺, Δ⁻ from the means and the face deviations ũ, ũ̃
L6      ũ_mod ← m̃(ũ, Δ⁺, Δ⁻);  ũ̃_mod ← m̃(ũ̃, Δ⁺, Δ⁻)
L7      if ũ_mod = ũ and ũ̃_mod = ũ̃ then keep the cell unchanged
L8      else U_(j,1) ← m̃(U_(j,1), Δ⁺, Δ⁻); U_(j,l) ← 0 for l ≥ 2
```

Lines L2 to L4 are the three-stage SSP Runge-Kutta method of Shu and Osher, a convex combination of forward Euler steps, with the limiter after each stage. Lines L5 to L8 are the generalized slope limiter of Cockburn and Shu. The limiter never changes the mean $U_{j,0}$, so it keeps conservation. A cell that fails the test at L7 becomes the linear function $\bar u_j + U_{j,1}\xi$. For $k = 1$ both face deviations equal $U_{j,1}$, so L8 is the same minmod slope limiter as in [MUSCL](/muscl-scheme/), with the half-cell deviation compared to full differences of the means.

The TVB constant $M$ is a choice. $M = 0$ gives the TVDM minmod limiter, which also clips smooth extrema. Cockburn and Shu relate the right size of $M$ to the second derivative of the solution at its extrema, so a larger $M$ is needed for sharper smooth peaks, and a too large $M$ lets oscillations through. The time step used here is $\Delta t\max|f'|/\Delta x \le 0.2$.

## Example

**The limiter on three cells.** Take $k = 1$, $\Delta x = 0.1$ and means $\bar u_{j-1} = 0$, $\bar u_j = 0.5$, $\bar u_{j+1} = 1.5$, with slope coefficient $U_{j,1} = 0.6$. Then $\Delta^- = 0.5$, $\Delta^+ = 1$ and both face deviations are $0.6$.

- With $M = 0$: $m(0.6, 1, 0.5) = 0.5 \ne 0.6$, so the cell is limited to the slope $0.5$. Its face values become $0$ and $1$, which lie between the neighbouring means.
- With $M = 100$: $M\Delta x^2 = 1 \ge 0.6$, so $\tilde m$ returns $0.6$ and the cell is kept.
- At an extremum, with means $0, 1, 0.5$ and slope $0.4$: $\Delta^+ = -0.5$ and $\Delta^- = 1$ have different signs, so with $M = 0$ the slope becomes $0$.

**Refinement study on smooth data (measurement).** Burgers' equation with $u_0 = \tfrac12 + \tfrac14\sin 2\pi x$ on $[0, 1]$ forms a shock at $t = 2/\pi \approx 0.64$. At $T = 0.2$ the solution is smooth and the exact value comes from characteristics, $u = u_0(x - ut)$. $L^2$ errors with $\Delta t = 0.2\,\Delta x$:

| $M$ cells | $k = 1$, $M_{\text{TVB}} = 0$ | $k = 1$, $M_{\text{TVB}} = 50$ | $k = 2$, $M_{\text{TVB}} = 0$ | $k = 2$, $M_{\text{TVB}} = 50$ |
|---|---|---|---|---|
| 10 | 1.242e-2 | 4.680e-3 | 1.254e-2 | 3.575e-4 |
| 20 | 3.425e-3 | 1.232e-3 | 3.447e-3 | 4.959e-5 |
| 40 | 9.304e-4 | 3.155e-4 | 9.145e-4 | 6.400e-6 |
| 80 | 2.419e-4 | 7.975e-5 | 2.410e-4 | 8.126e-7 |
| $p_{\text{obs}}$ (40 to 80) | 1.94 | 1.98 | 1.92 | 2.98 |

With $M_{\text{TVB}} = 0$ the $P^2$ method is limited at the two extrema and falls to the accuracy of $P^1$. With $M_{\text{TVB}} = 50$ it keeps order 3.

**A shock and a rarefaction (measurement).** The square wave $u_0 = 1$ on $[0.25, 0.75)$, $0$ elsewhere, at $T = 0.3$, $\Delta t = 0.15\,\Delta x$, $M_{\text{TVB}} = 0$, $L^1$ error of the cell means:

| $M$ cells | $k = 0$ (Godunov) | $k = 1$ limited | $k = 1$ no limiter | max mean, no limiter |
|---|---|---|---|---|
| 25 | 5.582e-2 | 1.237e-2 | 1.277e-2 | 1.031 |
| 50 | 4.238e-2 | 1.035e-2 | 5.950e-3 | 1.015 |
| 100 | 2.352e-2 | 4.173e-3 | 2.472e-3 | 1.013 |

With the limiter, the means stay in $[0, 1]$ and their total variation stays at its initial value 2. Without it, the means overshoot by more than 1% at the shock at every resolution. The unlimited error is smaller here, but its overshoot does not decrease, and for systems such overshoots can make density or pressure negative.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the limiter keeps every cell mean, so the method is conservative, and that after limiting with $M = 0$ each face deviation is a fraction in $[0, 1]$ of both neighbouring differences of the means. From this it writes one forward Euler step of the means in Harten's incremental form with nonnegative coefficients and proves that, if $\lambda(L_1 + L_2) \le \tfrac12$ with $\lambda = \Delta t/\Delta x$, the means are TVD and satisfy a maximum principle. Because each SSP stage is a convex combination of such steps followed by the limiter, the full Runge-Kutta step keeps both properties. The TVBM bound for $M > 0$ and the convergence to a weak solution are cited from Cockburn and Shu (1989).

## Complexity

The DG operator costs $\Theta(M(k+1)^2)$ per stage and the limiter $\Theta(M(k+1))$, so $N$ steps cost $\Theta(NM(k+1)^2)$ with $\Theta(M(k+1))$ memory. The stable time step is about $\Delta x/(2k+1)$ divided by the wave speed, so a fixed final time needs $N = \Theta(M(2k+1))$ steps. For systems the limiter works in characteristic variables, which adds a $d \times d$ eigenvector transform per cell for $d$ equations.

## Properties

- **Conservative.** The limiter keeps the means, so shocks move at the right speed (theorem).
- **TVDM** with $M = 0$ for one forward Euler step under $\lambda(L_1 + L_2) \le \tfrac12$, and so for SSP-RK3 under the same condition (theorem). With $M > 0$ it is TVBM: the total variation of the means is bounded (Cockburn and Shu 1989).
- **Maximum principle in the means** under the same condition (theorem).
- **Order $k + 1$** in smooth regions with a TVB constant large enough for the extrema (measurement). With $M = 0$ the order drops near smooth extrema.
- **Compact.** The limiter uses only the direct neighbours, so the method stays local.

## Variants and improvements

- **Limiting in characteristic variables** for systems such as the [Euler equations](/euler-equations-of-gas-dynamics/) (Cockburn and Shu 1998). Limiting the conserved variables componentwise gives more oscillations.
- **Troubled-cell indicators** (KXRCF and others), which mark cells first and limit only those.
- **WENO limiters**, which rebuild the polynomial in troubled cells from a WENO reconstruction of the neighbouring data and keep high order.
- **Moment limiters** for $k \ge 2$, which limit the highest modes first and stop when a mode passes.
- **The [positivity-preserving limiter](/positivity-preserving-limiter/)** of Zhang and Shu, a different limiter that keeps density and pressure positive without destroying high order.
- **Subcell finite volume limiting**, which replaces troubled cells by a robust finite volume scheme on subcells.

## When to use it

Use RKDG for conservation laws with shocks when you also want high order in smooth regions and a compact stencil on unstructured meshes, as in compressible aerodynamics and astrophysical flows. For problems dominated by strong shocks on Cartesian grids, finite volume [WENO](/weno-scheme/) schemes are often simpler and more robust. For smooth problems with no shocks, plain DG without a limiter is enough.

## Pitfalls

- **Limiting only once per step.** The TVD argument needs the limiter after every stage, not only after the full step.
- **Mixing up the deviation scale.** The deviations $\tilde u$ are half-cell changes and $\Delta^\pm$ are full-cell differences. Comparing $\tilde u$ with $\Delta^\pm/2$ gives a more dissipative limiter; changing scales by accident changes the method.
- **$M$ in the wrong units.** The threshold is $M\Delta x^2$, not $M$. A fixed threshold independent of $\Delta x$ either limits everything or nothing on fine grids.
- **CFL number of the finite volume scheme.** The DG time step is several times smaller than the finite volume one.
- **Componentwise limiting of systems.** It is cheap but produces oscillations at strong shocks.
- **Limiting does not give positivity.** TVD in the means does not keep the pressure of a gas positive near vacuum; that needs a positivity-preserving limiter.

## Implementations

## History

Cockburn and Shu developed the method in a series of papers from 1989 to 1998, for scalar laws, one-dimensional systems, multidimensional scalar laws and multidimensional systems. They took the DG space discretization of Reed and Hill (1973) and the TVD Runge-Kutta methods of Shu and Osher (1988), and adapted the TVB idea of Shu (1987) to the limiter. Their survey (Cockburn and Shu 2001) is the standard reference. Later work replaced the minmod limiter by WENO and moment limiters and added positivity preservation (Zhang and Shu 2010).

## References
