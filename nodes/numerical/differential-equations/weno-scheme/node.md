---
tag: EF32M5
kind: algorithm
slug: weno-scheme
name: WENO schemes
aliases:
- weighted essentially non-oscillatory schemes
- WENO
- WENO5
- WENO-JS
area: numerical/differential-equations
level: research
summary: "High-order shock-capturing schemes: reconstruct cell edge values as a weighted average of candidate stencils, with weights that switch off any stencil that crosses a discontinuity."
solves: [advection-equation, burgers-equation]
model: real-ram
complexity:
  vars: {m: "the number of cells", N: "the number of time steps, ⌈T/Δt⌉", C: "the cost of one evaluation of the flux f"}
  time: {worst: "Θ(N m (C + 1))"}
  space: {extra: "Θ(m)"}
  evaluations: {worst: "3 N (m + 6)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "5 in space and 3 in time on smooth solutions", tvd: false, stable_for: "observed Courant number up to about 1.6 with SSP-RK3"}
history:
  year: 1994
  people: [Xu-Dong Liu, Stanley Osher, Tony Chan, Guang-Shan Jiang, Chi-Wang Shu]
  note: Liu, Osher and Chan (1994) replaced the stencil choice of ENO by a weighted average; Jiang and Shu (1996) gave the smoothness indicators and the fifth-order scheme now called WENO5.
prereqs: [finite-volume-method, flux-limiter-methods, total-variation-diminishing]
see_also: [godunov-method, riemann-problem, upwind-scheme, lax-wendroff-method, method-of-lines, runge-kutta-methods, spectral-methods, von-neumann-stability-analysis]
sources:
  - paper: "Guang-Shan Jiang and Chi-Wang Shu, Efficient implementation of weighted ENO schemes, Journal of Computational Physics 126 (1996) 202-228"
    locator: the smoothness indicators, the fifth-order WENO scheme, Lax-Friedrichs flux splitting and numerical tests; doi:10.1006/jcph.1996.0130
  - paper: "Xu-Dong Liu, Stanley Osher and Tony Chan, Weighted essentially non-oscillatory schemes, Journal of Computational Physics 115 (1994) 200-212"
    locator: the first WENO schemes (third order); doi:10.1006/jcph.1994.1187
  - paper: "Ami Harten, Björn Engquist, Stanley Osher and Sukumar R. Chakravarthy, Uniformly high order accurate essentially non-oscillatory schemes, III, Journal of Computational Physics 71 (1987) 231-303"
    locator: ENO reconstruction by adaptive stencil choice; doi:10.1016/0021-9991(87)90031-3
  - paper: "Chi-Wang Shu and Stanley Osher, Efficient implementation of essentially non-oscillatory shock-capturing schemes, Journal of Computational Physics 77 (1988) 439-471"
    locator: TVD (SSP) Runge-Kutta time discretizations, the third-order method; doi:10.1016/0021-9991(88)90177-5
  - paper: "Andrew K. Henrick, Tariq D. Aslam and Joseph M. Powers, Mapped weighted essentially non-oscillatory schemes, Journal of Computational Physics 207 (2005) 542-567"
    locator: loss of order at critical points and the mapped weights; doi:10.1016/j.jcp.2005.01.023
  - paper: "Rafael Borges, Monique Carmona, Bruno Costa and Wai Sun Don, An improved weighted essentially non-oscillatory scheme for hyperbolic conservation laws, Journal of Computational Physics 227 (2008) 3191-3211"
    locator: the WENO-Z weights with the global indicator τ5; doi:10.1016/j.jcp.2007.11.038
  - paper: "Chi-Wang Shu, High order weighted essentially nonoscillatory schemes for convection dominated problems, SIAM Review 51 (2009) 82-126"
    locator: survey of WENO reconstruction, finite volume and finite difference forms, time stepping and open problems; doi:10.1137/070679065
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 6 (high-resolution methods and TVD limiters, the setting WENO generalizes), Chapter 10 (other approaches to high resolution, including semidiscrete methods with ENO and WENO reconstruction)
---

WENO schemes are high-order [finite volume](/finite-volume-method/) (or finite difference) methods for conservation laws $u_t + f(u)_x = 0$ that stay sharp and nearly free of oscillations at shocks. To compute the flux through a cell edge they build several low-order reconstructions from overlapping stencils and take a weighted average. In smooth regions the weights are close to fixed optimal weights that combine the candidates into one high-order formula; near a discontinuity the weight of every stencil that crosses it drops to almost zero. The standard WENO5 scheme of Jiang and Shu uses three 3-cell stencils, is fifth order on smooth solutions, and is usually paired with a third-order strong-stability-preserving Runge-Kutta method in time.

## In plain words

To guess the value at the edge of a cell, you can draw a parabola through three neighbouring cells. There are three ways to pick those three cells: shifted left, centered, or shifted right. If the function is smooth, all three guesses are good, and a particular blend of them is much better than any one: it is the same as fitting a degree-4 curve through all five cells.

If there is a jump inside one of the groups, the parabola through it wiggles and gives a bad guess. WENO measures how wiggly each parabola is and gives a group a weight roughly proportional to 1 over its wiggliness squared. Groups that contain the jump become nearly invisible, and the answer comes from the smooth side. No switch or if-statement is needed; the weights change smoothly, which keeps the scheme high order where the data are smooth.

## The problem

Given a flux $f$, a bound $\alpha \ge \max|f'(u)|$ over the data, initial cell averages $U_j^0$ on $m$ cells of width $\Delta x$, a time step $\Delta t$ and an end time $T \ge 0$, compute cell averages $U_j^N \approx \frac{1}{\Delta x}\int_{I_j}u(x, T)\,dx$ of the entropy solution. Boundary conditions are periodic or transmissive. Errors are measured in the max norm or the $L^1$ norm over cell averages; the Courant number is $\alpha\Delta t/\Delta x$. Cost is counted in evaluations of $f$.

## The algorithm

```pseudo id=main
WENO5(U^0, f, α, Δx, Δt, T, ε)          ▷ α ≥ max |f'|, ε = 10^-6
L1  N ← ⌈T/Δt − δ⌉, U ← U^0, t ← 0     ▷ δ: relative slack 10^-9
L2  for n ← 0 to N − 1 do h ← (T if n = N − 1 else (n + 1)Δt) − t
L3      U1 ← U + h L(U)
L4      U2 ← (3/4) U + (1/4)(U1 + h L(U1))
L5      U ← (1/3) U + (2/3)(U2 + h L(U2)), t ← t + h
L6  return U
    L(U):
L7      add 3 ghost cells per side; f± ← (f(U) ± α U)/2
L8      for each edge j+1/2: v ← f+ on cells j−2..j+2, w ← f− on cells j+3..j−1 (mirrored)
L9          F_{j+1/2} ← WENO(v) + WENO(w)
L10     return L_j = −(F_{j+1/2} − F_{j−1/2})/Δx
```

Lines L1 to L6 are the Shu-Osher SSP-RK3 method. Line L7 splits the flux into a right-moving part $f^+$ and a left-moving part $f^-$ (Lax-Friedrichs splitting), and line L8 reconstructs each from its upwind side. For averages $v = (a, b, c, d, e)$ of cells $j - 2, \dots, j + 2$, $\text{WENO}(v)$ at the right edge of cell $j$ is:

- **Candidates:** $q_0 = (2a - 7b + 11c)/6$, $q_1 = (-b + 5c + 2d)/6$, $q_2 = (2c + 5d - e)/6$.
- **Smoothness indicators:** $\beta_0 = \frac{13}{12}(a - 2b + c)^2 + \frac{1}{4}(a - 4b + 3c)^2$, $\beta_1 = \frac{13}{12}(b - 2c + d)^2 + \frac{1}{4}(b - d)^2$, $\beta_2 = \frac{13}{12}(c - 2d + e)^2 + \frac{1}{4}(3c - 4d + e)^2$.
- **Weights:** $\alpha_k = d_k/(\varepsilon + \beta_k)^2$ with $d = (\frac{1}{10}, \frac{3}{5}, \frac{3}{10})$, $\omega_k = \alpha_k/\sum_l\alpha_l$, and $\text{WENO}(v) = \sum_k\omega_k q_k$.

With $\omega = d$ the formula is the linear fifth-order upwind value $(2a - 13b + 47c + 27d - 3e)/60$. The WENO-Z variant uses $\alpha_k = d_k\big(1 + (\tau_5/(\varepsilon + \beta_k))^2\big)$ with $\tau_5 = |\beta_0 - \beta_2|$. As on the other time-stepping pages, $T = 0$ gives zero steps and a $\Delta t$ beyond $T$ gives one short step.

## Example

**Square wave.** Advect a unit pulse on $[0.25, 0.5)$ across the periodic interval $[0, 1)$ with 100 cells, Courant number 0.5 and one full period, as on the [TVD page](/total-variation-diminishing/). Observed:

| scheme | final TV (initial 2) | max | min | $L^1$ error |
|---|---|---|---|---|
| WENO5 (Jiang-Shu) | 2.0027 | 1.0004 | -0.0003 | 0.0315 |
| WENO-Z | 2.0019 | 1.0003 | -0.0003 | 0.0274 |
| linear weights $\omega = d$ | 2.686 | 1.072 | -0.072 | 0.0282 |
| minmod limiter (for comparison) | 1.997 | 0.998 | 0.000 | 0.049 |

The nonlinear weights cut the 7% overshoot of the linear fifth-order scheme to 0.04%; the total variation grows by 0.13%, so WENO is not exactly TVD, but the oscillations are at the level of $10^{-4}$.

**Smooth data.** For $u_0 = \sin 2\pi x$, time $T = 0.5$ and $\Delta t \propto \Delta x^{5/3}$ (Courant number 0.5 at $m = 10$, so that the third-order time error is $O(\Delta x^5)$), the max-norm errors of the cell averages are:

| $m$ | 10 | 20 | 40 | 80 |
|---|---|---|---|---|
| Jiang-Shu | 2.64e-2 | 1.41e-3 | 5.12e-5 | 1.55e-6 |
| WENO-Z | 7.98e-3 | 2.75e-4 | 8.90e-6 | 2.80e-7 |

The observed orders are 4.22, 4.78, 5.05 and 4.86, 4.95, 4.99. With 80 cells the error is $10^{-6}$ to $10^{-7}$, where the second-order van Leer limiter needs far finer grids (its $L^1$ error is $7.3 \times 10^{-5}$ at 400 cells).

**Burgers shock.** For $f(u) = u^2/2$ with the jump from 1 to 0 at $x = 0.3$, 100 cells and $T = 0.4$, the computed profile crosses $\frac12$ between $x = 0.495$ and $0.505$, the exact shock position $0.5$ from the Rankine-Hugoniot speed $\frac12$, with an overshoot of $1.1 \times 10^{-4}$ and the shock spread over about 3 cells. The mass changes by exactly the boundary flux $0.2$ up to $10^{-12}$.

## Correctness

**Theorem (proved in the proof file for the reconstruction).** (1) The candidates are exact for polynomials of degree at most 2 and the linear combination for degree at most 4 (checked exactly in Fractions). (2) The weights are nonnegative and sum to 1, and on smooth data with $v' \ne 0$, $\omega_k - d_k = O(\Delta x^2)$, so the reconstruction error is $O(\Delta x^5)$. (3) If one stencil is smooth and another crosses a jump of fixed size, the weight of the crossing stencil is $O((\varepsilon + \Delta x^2)^2)$. (4) The scheme is conservative, and SSP-RK3 is a convex combination of forward Euler steps, so it keeps any convex bound that forward Euler keeps under the same step restriction; its order is exactly 3 with stability polynomial $R(z) = 1 + z + z^2/2 + z^3/6$.

What is *not* proved: there is no general $\ell^2$ or total variation stability theorem for WENO5 with nonlinear weights, and no general proof of convergence to the entropy solution (Shu 2009). Fifth order of the whole scheme is shown by an asymptotic argument of Henrick, Aslam and Powers under $\omega_k - d_k = O(\Delta x^3)$, and is observed in the example. With $\varepsilon \to 0$ the Jiang-Shu weights lose accuracy at critical points: on $\sin(\pi x - \sin(\pi x)/\pi)$ with $\varepsilon = 10^{-40}$ the observed reconstruction orders fall to 4.29, 4.14, 4.01, while WENO-Z keeps 5.0.

## Complexity

Each right-hand side evaluates $f$ on the $m + 6$ cells including ghosts and does $\Theta(m)$ arithmetic (two reconstructions per edge, each a fixed number of operations). SSP-RK3 needs three evaluations per step, so $N$ steps cost $\Theta(N m (C + 1))$ time and $3N(m + 6)$ flux evaluations, with $\Theta(m)$ extra space for the stages. At a fixed Courant number, $N = \Theta(m)$ and the cost to time $T$ is $\Theta(m^2)$ in one dimension. Per cell and step, WENO5 costs several times a limited second-order scheme (three stages, two reconstructions per edge); this pays off when the solution has smooth structure to resolve.

## Properties

- **Order:** 5 in space for smooth solutions (observed and argued asymptotically), 3 in time with SSP-RK3. Near shocks the error is $O(\Delta x)$ in $L^1$, as for any shock-capturing scheme.
- **Conservative:** fluxes telescope, so the Lax-Wendroff theorem applies to convergent sequences.
- **Essentially non-oscillatory, not TVD:** spurious oscillations are of the size of the truncation error rather than $O(1)$.
- **Smooth in the data:** the weights depend smoothly on $U$, which helps steady-state convergence and analysis, unlike ENO's discrete stencil choice.
- **Explicit**, with an observed Courant limit near 1.6 for SSP-RK3 and linear advection.

## Variants and improvements

- **WENO-Z** (Borges et al. 2008) and **mapped WENO** (Henrick et al. 2005) restore fifth order at critical points and reduce dissipation.
- **Finite difference WENO** (Jiang and Shu) reconstructs point-value fluxes instead of cell averages; it is cheaper in several dimensions because it works dimension by dimension.
- **Characteristic-wise WENO** for systems such as the Euler equations reconstructs in the eigenvector basis of the flux Jacobian, which avoids oscillations from interacting waves.
- **Local Lax-Friedrichs or Roe splitting** with a local $\alpha$ reduces dissipation compared with the global $\alpha$ used here.
- **Higher orders** (WENO7, WENO9), **central WENO** and **WENO for Hamilton-Jacobi equations**; Runge-Kutta discontinuous Galerkin methods use WENO as a limiter.
- **ENO** (Harten, Engquist, Osher and Chakravarthy 1987) chooses the single smoothest stencil instead of averaging; it is order $r$ from $r$-cell stencils, while WENO gets order $2r - 1$.

## When to use it

Use WENO for problems with both shocks and rich smooth structure: compressible turbulence, shock-vortex and shock-entropy wave interaction, detonations, astrophysical flows and level-set advection. For problems that are mostly discontinuities, a second-order [flux-limited](/flux-limiter-methods/) or [Godunov](/godunov-method/) scheme is cheaper and nearly as good. For smooth periodic problems without shocks, [spectral methods](/spectral-methods/) or linear high-order schemes are more efficient.

## Pitfalls

- **Large time steps for accuracy tests.** With a fixed Courant number the third-order time error dominates on fine grids; observe fifth order only with $\Delta t \propto \Delta x^{5/3}$ or a higher-order integrator.
- **The size of $\varepsilon$.** $\varepsilon = 10^{-6}$ hides the loss of order at critical points but makes the weights depend on the scaling of $u$; with $\varepsilon = 10^{-40}$ the Jiang-Shu weights drop to fourth order there. Nondimensionalize the data or use WENO-Z.
- **Courant number too large.** At Courant number 2.0 the smooth advection test grows by $10^{14}$ by $T = 5$, while 1.0 is stable; nonlinear weights give no protection.
- **Componentwise reconstruction of systems** produces oscillations near strong shocks; use characteristic variables.
- **A splitting constant $\alpha$ below $\max|f'|$** breaks the upwinding of $f^\pm$ and can make the scheme unstable.
- **Positivity.** WENO does not by itself keep densities and pressures positive near vacuum; positivity-preserving limiters are needed.

## Implementations

## History

ENO schemes, which choose the smoothest stencil adaptively, were introduced by Harten, Engquist, Osher and Chakravarthy (1987), and Shu and Osher (1988) gave efficient finite difference ENO with the TVD (now SSP) Runge-Kutta methods. Liu, Osher and Chan (1994) replaced the choice by a convex combination, the first WENO scheme. Jiang and Shu (1996) introduced the smoothness indicators used today and the fifth-order scheme. Henrick, Aslam and Powers (2005) found the loss of order at critical points and proposed mapped weights, and Borges, Carmona, Costa and Don (2008) the WENO-Z weights (Shu 2009 surveys the field).

## References
