---
tag: 0QMSQD
kind: technique
slug: flux-limiter-methods
name: Flux limiter methods
aliases:
- slope limiters
- flux limiters
- high-resolution schemes
- TVD limiters
area: numerical/differential-equations
level: research
summary: "Conservative schemes that add to a first-order flux a correction toward a second-order flux, scaled by a limiter φ(r) of a smoothness ratio, so they stay TVD and do not oscillate at shocks."
prereqs: [finite-volume-method, upwind-scheme, lax-wendroff-method]
see_also: [total-variation-diminishing, godunov-method, weno-scheme, riemann-problem, burgers-equation, advection-equation, courant-friedrichs-lewy-condition, method-of-lines]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 6 (high-resolution methods; slope limiters and flux limiters, the TVD condition, Harten's theorem, the Sweby region, clipping at extrema)
  - paper: doi:10.1137/0721062
    title: P. K. Sweby, High resolution schemes using flux limiters for hyperbolic conservation laws, SIAM Journal on Numerical Analysis 21(5) (1984) 995-1011
    locator: the flux-limited Lax-Wendroff scheme, the TVD region 0 ≤ φ(r) ≤ min(2r, 2), the second-order region, the minmod and superbee limiters
  - paper: doi:10.1016/0021-9991(83)90136-5
    title: Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49(3) (1983) 357-393
    locator: the definition of TVD schemes, the incremental form and the sufficient condition for the TVD property
  - paper: doi:10.1016/0021-9991(74)90019-9
    title: Bram van Leer, Towards the ultimate conservative difference scheme II. Monotonicity and conservation combined in a second-order scheme, Journal of Computational Physics 14(4) (1974) 361-370
    locator: the smooth limiter φ(r) = (r + |r|)/(1 + |r|) applied to the Lax-Wendroff correction
  - paper: doi:10.1016/0021-9991(79)90145-1
    title: Bram van Leer, Towards the ultimate conservative difference scheme V. A second-order sequel to Godunov's method, Journal of Computational Physics 32(1) (1979) 101-136
    locator: the MUSCL approach, piecewise linear reconstruction with limited slopes
  - paper: "S. K. Godunov, A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics, Matematicheskii Sbornik 47(89) (1959) 271-306"
    locator: the proof that monotonicity-preserving linear schemes are at most first order accurate
---

A flux limiter method is a conservative [finite volume](/finite-volume-method/) scheme for a hyperbolic conservation law $u_t + f(u)_x = 0$ whose numerical flux is a low-order monotone flux plus a correction toward a high-order flux, scaled by a limiter $\varphi(r) \ge 0$. The ratio $r$ of consecutive differences measures local smoothness: where the data are smooth, $\varphi \approx 1$ and the scheme is second order, like the [Lax-Wendroff method](/lax-wendroff-method/); near a jump or an extremum, $\varphi$ falls to 0 and the scheme becomes the first-order [upwind scheme](/upwind-scheme/), which does not oscillate. With a limiter in Sweby's region the scheme is [total variation diminishing](/total-variation-diminishing/) under the CFL condition $0 \le \nu \le 1$.

## In plain words

Simple schemes for moving waves come in two kinds. Low-order schemes never create wiggles, but they smear sharp fronts over many cells. High-order schemes keep smooth waves crisp, but they create wiggles next to every sharp front. A flux limiter uses both. In each cell it compares the slope on one side with the slope on the other. If the two agree, the data are smooth there, and the scheme uses the accurate correction. If they disagree or point in opposite directions, there is a front or a peak, and the scheme drops the correction and falls back to the safe low-order rule. The rule that decides how much of the correction to keep is the limiter. A good limiter gives sharp fronts without wiggles and high accuracy on smooth parts.

## When it applies

- The equation is a hyperbolic conservation law, scalar or a system, and the solution has shocks, contact discontinuities or steep fronts next to smooth regions.
- The scheme is explicit and conservative, $u_j^{n+1} = u_j^n - \frac{\Delta t}{\Delta x}(F_{j+1/2} - F_{j-1/2})$, so that it inherits conservation and, if it converges, converges to a weak solution.
- There is a monotone (or at least TVD) low-order flux $F^L$, such as upwind or Godunov, and a higher-order flux $F^H$, such as Lax-Wendroff.
- The time step satisfies a [CFL condition](/courant-friedrichs-lewy-condition/); for the scheme below, $0 \le \nu \le 1$.

The reason a nonlinear device is needed: a linear scheme that preserves monotone data is at most first order accurate (Godunov 1959), so a second-order scheme without oscillations must let its coefficients depend on the data.

## The template

**Notation.** Linear [advection](/advection-equation/) $u_t + au_x = 0$ with $a > 0$ on a uniform grid, cell averages $u_j$, Courant number $\nu = a\Delta t/\Delta x \in [0, 1]$, periodic or extended boundary values. The smoothness ratio at interface $j + \tfrac12$ is $r_j = (u_j - u_{j-1})/(u_{j+1} - u_j)$, the upwind difference over the local one. A limiter is a function $\varphi : \mathbb{R} \to [0, \infty)$.

```pseudo id=main
FLUX-LIMITED-STEP(u, a, ν, φ)
L1  for each interface j + 1/2 do
L2      Δ ← u_(j+1) − u_j
L3      if Δ = 0 then C ← 0
L4      else r ← (u_j − u_(j−1))/Δ; C ← φ(r) Δ                 ▷ limited correction
L5      F_(j+1/2) ← a (u_j + ½ (1 − ν) C)                        ▷ upwind flux + limited antidiffusion
L6  for each cell j do
L7      u_j ← u_j − (ν/a)(F_(j+1/2) − F_(j−1/2))
L8  return u
```

**Walk-through.** Line L5 is $F^L + \varphi(r)(F^H - F^L)$ with the upwind flux $F^L = au_j$ and the Lax-Wendroff flux $F^H = au_j + \tfrac12a(1 - \nu)(u_{j+1} - u_j)$. The choice $\varphi \equiv 0$ gives upwind, $\varphi \equiv 1$ gives Lax-Wendroff, and $\varphi(r) = r$ gives Beam-Warming. Line L3 handles flat data, where the correction vanishes for any bounded $\varphi$. For $a < 0$ the roles of left and right are mirrored, and for a nonlinear flux $f$ one takes $F^L$ from a monotone flux (for example the [Godunov flux](/godunov-method/)), $F^H$ from a second-order flux, and $r$ in the upwind direction of the local wave speed.

**Why it is TVD (Sweby's condition).** Write $\Delta_{j-1/2} = u_j - u_{j-1}$. If $0 \le \varphi(r) \le 2r$ and $\varphi(r) \le 2$ for $r > 0$, and $\varphi(r) = 0$ for $r \le 0$, then line L7 can be written as

$$u_j^{n+1} = u_j - C_{j-1/2}\Delta_{j-1/2}, \qquad C_{j-1/2} = \nu\Big(1 + \frac{1 - \nu}{2}\Big(\frac{\varphi(r_j)}{r_j} - \varphi(r_{j-1})\Big)\Big),$$

using $\varphi(r_j)\Delta_{j+1/2} = \frac{\varphi(r_j)}{r_j}\Delta_{j-1/2}$ (with the term read as 0 when $\varphi(r_j) = 0$). Both $\varphi(r_j)/r_j$ and $\varphi(r_{j-1})$ lie in $[0, 2]$, so the bracket lies in $[\nu, 2 - \nu]$ and $0 \le \nu^2 \le C_{j-1/2} \le \nu(2 - \nu) \le 1$. Harten's lemma (Harten 1983) states that a scheme $u_j^{n+1} = u_j - C_{j-1/2}\Delta_{j-1/2} + D_{j+1/2}\Delta_{j+1/2}$ with $C_{j-1/2} \ge 0$, $D_{j+1/2} \ge 0$ and $C_{j+1/2} + D_{j+1/2} \le 1$ for all $j$ does not increase $\sum_j|\Delta_{j-1/2}|$; here $D = 0$. So the total variation does not increase, and no new extrema appear.

**Second order.** If in addition $\varphi$ is Lipschitz near $r = 1$ with $\varphi(1) = 1$, the scheme is second order accurate wherever the solution is smooth and $u_x \ne 0$, because there $r_j = 1 + O(\Delta x)$ and the flux differs from the Lax-Wendroff flux by $O(\Delta x^2)$ (Sweby 1984). Sweby recommends limiters between $\varphi = 1$ and $\varphi = r$ in the TVD region for $r$ near 1.

## Classic examples

**Common limiters.** All are 0 for $r \le 0$, satisfy $\varphi(1) = 1$ and lie in Sweby's region.

| limiter | $\varphi(r)$ for $r > 0$ | behaviour |
|---|---|---|
| minmod | $\min(1, r)$ | lower edge of the second-order region; most diffusive |
| superbee (Roe) | $\max(\min(2r, 1), \min(r, 2))$ | upper edge of the TVD region; most compressive |
| van Leer | $\dfrac{2r}{1 + r}$ | smooth (from $(r + \lvert r\rvert)/(1 + \lvert r\rvert)$); $\varphi(\infty) = 2$ |
| monotonized central (MC) | $\min\big(2r, \tfrac{1 + r}{2}, 2\big)$ | central slope where it is admissible |

**One step by hand.** Take $u = (0, 0, 0, \tfrac12, 1, 1, 1)$, $\nu = \tfrac12$, so $\tfrac12(1 - \nu) = \tfrac14$, with constant extension at the ends. With minmod: at the interface between the cells $0$ and $\tfrac12$, $r = 0/\tfrac12 = 0$, so $\varphi = 0$ and $F/a = 0$; between $\tfrac12$ and $1$, $r = \tfrac12/\tfrac12 = 1$, $\varphi = 1$ and $F/a = \tfrac12 + \tfrac14 \cdot \tfrac12 = \tfrac58$; between $1$ and $1$, $F/a = 1$. The new values are

| scheme | new $u$ |
|---|---|
| upwind ($\varphi = 0$) | $0, 0, 0, \tfrac14, \tfrac34, 1, 1$ |
| Lax-Wendroff ($\varphi = 1$) | $0, 0, -\tfrac1{16}, \tfrac14, \tfrac{13}{16}, 1, 1$ |
| minmod or superbee | $0, 0, 0, \tfrac3{16}, \tfrac{13}{16}, 1, 1$ |

Lax-Wendroff creates the new minimum $-\tfrac1{16}$; the limited scheme does not, and its front is steeper than upwind's.

**A square wave.** Advection of the indicator of $[0.3, 0.6)$ on $[0, 1]$, periodic, 100 cells, $\nu = 0.5$, one full period (200 steps). The exact total variation is 2.

| scheme | $L^1$ error | min | max | total variation |
|---|---|---|---|---|
| upwind | 0.1127 | 0.0000 | 0.9659 | 1.9318 |
| Lax-Wendroff | 0.0779 | $-0.2244$ | 1.2232 | 3.6158 |
| minmod | 0.0493 | 0.0000 | 0.9997 | 1.9995 |
| van Leer | 0.0339 | 0.0000 | 1.0000 | 2.0000 |
| MC | 0.0286 | 0.0000 | 1.0000 | 2.0000 |
| superbee | 0.0175 | 0.0000 | 1.0000 | 2.0000 |

**A smooth wave.** Cell averages of $\sin 2\pi x$, same setup, $m = 50, 100, 200, 400$ cells. Observed orders between $m = 200$ and $m = 400$:

| scheme | $L^1$ error, $m = 400$ | order in $L^1$ | order in max norm |
|---|---|---|---|
| upwind | $1.55 \times 10^{-2}$ | 0.98 | 0.98 |
| Lax-Wendroff | $1.23 \times 10^{-4}$ | 2.00 | 2.00 |
| minmod | $3.38 \times 10^{-4}$ | 1.89 | 1.30 |
| superbee | $2.41 \times 10^{-4}$ | 1.95 | 1.31 |
| van Leer | $7.33 \times 10^{-5}$ | 2.15 | 1.43 |
| MC | $2.90 \times 10^{-5}$ | 2.33 | 1.54 |

The limiters keep nearly second order in $L^1$ but lose it in the maximum norm, because at the two extrema of the sine $r \le 0$ and the scheme falls back to first order there (clipping).

## Variations

- **Slope limiters (MUSCL).** Reconstruct a piecewise linear function in each cell with a limited slope, for example $\sigma_j = \operatorname{minmod}(\Delta_{j-1/2}, \Delta_{j+1/2})/\Delta x$, then solve Riemann problems at the interfaces (van Leer 1979). For linear advection each slope limiter corresponds to a flux limiter; for nonlinear systems the slope form extends more naturally to Godunov and approximate Riemann solvers.
- **Systems.** Apply the limiter to each characteristic field, using the eigenvectors of a local Roe matrix (wave limiters in LeVeque's wave propagation form). Limiting the conserved variables componentwise is cheaper but can leave oscillations.
- **Method of lines.** Use the limited flux in a semidiscretization $u_j' = -(F_{j+1/2} - F_{j-1/2})/\Delta x$ and integrate in time with a strong stability preserving Runge-Kutta method; the TVD condition then becomes a bound on $\nu$ that depends on the time integrator.
- **Flux-corrected transport (FCT).** Compute the full antidiffusive flux, then scale it down so that no cell exceeds bounds taken from its neighbours after the low-order step; this form extends directly to several dimensions and unstructured grids.
- **TVB and extremum-preserving limiters** relax the TVD condition near smooth extrema to avoid clipping. [WENO schemes](/weno-scheme/) avoid limiters altogether by weighting several stencils.

## Pitfalls

- **Clipping of smooth extrema.** TVD schemes degenerate to first order at smooth extrema (LeVeque 2002, Chapter 6), which shows in the maximum norm; the table above shows max-norm orders between 1.3 and 1.5. Use TVB, extremum-preserving or WENO methods when peaks matter.
- **Compressive limiters on smooth data.** Superbee steepens smooth profiles and can turn a sine wave toward a square wave over long times; it is suited to contact discontinuities, not to smooth flow.
- **Limiters outside the TVD region.** For example $\varphi(r) = r$ (Beam-Warming) or $\varphi \equiv 1$ (Lax-Wendroff) are not bounded by $2r$ and 2, and they oscillate at jumps.
- **Courant number.** The proof needs $0 \le \nu \le 1$; for $\nu > 1$ even the upwind part is unstable.
- **Division by zero in $r$.** When $u_{j+1} = u_j$, $r$ is undefined; set the correction to 0 (line L3) or add a tiny number to the denominator with the right sign.
- **Upwind direction for nonlinear and system problems.** The ratio must be taken in the upwind direction of the local wave; using the wrong side lets oscillations through at sonic points and in systems with waves in both directions.
- **TVD is not entropy.** A TVD scheme for a nonlinear law can still converge to an entropy-violating shock if the underlying low-order flux does; use an entropy-satisfying monotone flux.

## Exercises

1. Show that line L5 with $\varphi \equiv 1$ is the Lax-Wendroff scheme $u_j^{n+1} = u_j - \tfrac\nu2(u_{j+1} - u_{j-1}) + \tfrac{\nu^2}2(u_{j+1} - 2u_j + u_{j-1})$, and that with $\varphi(r) = r$ it is the Beam-Warming scheme.
2. Check that minmod, superbee, van Leer and MC satisfy $0 \le \varphi(r) \le \min(2r, 2)$ for $r > 0$ and $\varphi(1) = 1$. Which of them are Lipschitz near $r = 1$, and which are differentiable there?
3. Apply one step of Lax-Wendroff with $\nu = \tfrac12$ to the step data $(0, 0, 1, 1)$ and show that it creates a value below 0. Explain how this fits Godunov's theorem.
4. Prove Harten's lemma: if $u_j^{n+1} = u_j - C_{j-1/2}\Delta_{j-1/2} + D_{j+1/2}\Delta_{j+1/2}$ with $C_{j-1/2}, D_{j+1/2} \ge 0$ and $C_{j+1/2} + D_{j+1/2} \le 1$ for all $j$, then $\sum_j|u_{j+1}^{n+1} - u_j^{n+1}| \le \sum_j|\Delta_{j+1/2}|$ (periodic data).
5. Show that at a strict local maximum of smooth data, $r_j \le 0$ for an interface next to it, so every limiter in this page uses $\varphi = 0$ there. Deduce that the local truncation error at that cell is $O(\Delta x)$ rather than $O(\Delta x^2)$.

## References
