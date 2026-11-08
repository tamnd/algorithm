---
tag: 4ZKPAC
kind: concept
slug: total-variation-diminishing
name: Total variation diminishing schemes
aliases:
- TVD schemes
- TVD property
area: numerical/differential-equations
level: advanced
summary: "A scheme for a scalar conservation law is TVD if the discrete total variation sum of |U_(j+1) - U_j| never increases. TVD schemes cannot create new oscillations."
prereqs: [finite-volume-method, upwind-scheme, lax-wendroff-method]
see_also: [flux-limiter-methods, godunov-method, weno-scheme, burgers-equation, riemann-problem, courant-friedrichs-lewy-condition, lax-equivalence-theorem, von-neumann-stability-analysis]
sources:
  - paper: "Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49 (1983) 357-393"
    locator: definition of TVD schemes, the incremental-form lemma (Harten's lemma), TVD implies monotonicity preserving; doi:10.1016/0021-9991(83)90136-5
  - paper: "Peter K. Sweby, High resolution schemes using flux limiters for hyperbolic conservation laws, SIAM Journal on Numerical Analysis 21 (1984) 995-1011"
    locator: the TVD region 0 <= φ(r) <= min(2r, 2) for flux limiters and the second-order subregion; doi:10.1137/0721062
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 6 (high-resolution methods; total variation, TVD methods, Harten's theorem, TVD limiters), Chapter 12 (nonlinear stability, total variation stability and convergence)
  - paper: "Sergei K. Godunov, A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics, Matematicheskii Sbornik 47 (1959) 271-306"
    locator: the order barrier for monotone linear schemes
---

A numerical scheme for a scalar conservation law $u_t + f(u)_x = 0$ is **total variation diminishing (TVD)** if, for every grid function $U^n$,

$$TV(U^{n+1}) \le TV(U^n), \qquad TV(U) = \sum_j |U_{j+1} - U_j|.$$

Exact solutions of scalar conservation laws have this property, even after shocks form. A scheme that copies it cannot create new local maxima or minima, so it does not ring next to a discontinuity the way the [Lax-Wendroff method](/lax-wendroff-method/) does. Harten introduced the notion in 1983 and gave a simple sufficient condition; [flux limiters](/flux-limiter-methods/) are the standard way to build TVD schemes that are second order away from extrema.

## In plain words

Total variation measures how far a pen moves up and down as it traces the solution from left to right. A single step up of height 1 has total variation 1; the same step with a wiggle of height 0.2 on each side has total variation 1.8. A TVD scheme promises that this up-and-down distance never grows.

That promise is exactly what is needed near a shock or a contact. A high-order linear scheme overshoots a jump, and the overshoots add variation, so it is not TVD. The cheapest TVD scheme, [upwind](/upwind-scheme/), never overshoots but smears the jump over many cells. TVD schemes in practice switch between the two: they use the high-order flux where the solution is smooth and fall back towards upwind next to jumps and extrema.

## The idea

**The setting.** A conservative scheme on cells of width $\Delta x$ with time step $\Delta t$ updates $U_j^{n+1} = U_j^n - \frac{\Delta t}{\Delta x}\big(F_{j+1/2} - F_{j-1/2}\big)$. Total variation is the discrete $\ell^1$ norm of the differences, either on $\mathbb{Z}$ with $U$ of bounded variation or on a periodic grid. For a function, $TV(u) = \sup\sum|u(x_{k+1}) - u(x_k)|$ over partitions; the entropy solution of a scalar conservation law satisfies $TV(u(\cdot, t)) \le TV(u(\cdot, 0))$ (proved; see Chapter 12 of LeVeque's book).

**Harten's lemma (proved).** Write the scheme in incremental form

$$U_j^{n+1} = U_j^n - C_{j-1/2}(U_j^n - U_{j-1}^n) + D_{j+1/2}(U_{j+1}^n - U_j^n),$$

where the coefficients may depend on $U^n$. If $C_{j+1/2} \ge 0$, $D_{j+1/2} \ge 0$ and $C_{j+1/2} + D_{j+1/2} \le 1$ for all $j$, the scheme is TVD. The proof subtracts the formula at $j + 1$ and $j$, takes absolute values, and sums by parts; the three conditions make every coefficient nonnegative and the sum telescope.

**A hierarchy (proved).** Monotone schemes (the new value is a nondecreasing function of every old value) are TVD, and TVD schemes are monotonicity preserving: monotone data stay monotone. Neither converse holds.

**Order barriers.** Godunov's theorem: a *linear* monotonicity-preserving scheme is at most first order accurate. So a second-order TVD scheme must be nonlinear, with coefficients that depend on the data. Further, Osher and Chakravarthy showed that TVD schemes degenerate to first order at smooth extrema in the max norm; the clipping of peaks is visible in the example below.

**Flux limiters (Sweby).** For the advection equation $u_t + au_x = 0$ with $a > 0$ and Courant number $\nu = a\Delta t/\Delta x$, use the flux

$$F_{j+1/2} = a\Big(U_j + \tfrac{1}{2}(1 - \nu)\,\varphi(r_j)\,(U_{j+1} - U_j)\Big), \qquad r_j = \frac{U_j - U_{j-1}}{U_{j+1} - U_j}.$$

$\varphi = 0$ is upwind and $\varphi = 1$ is Lax-Wendroff. Harten's lemma shows the scheme is TVD for $0 \le \nu \le 1$ when $\varphi(r) = 0$ for $r \le 0$ and $0 \le \varphi(r) \le \min(2r, 2)$. Second order in smooth monotone regions needs $\varphi(1) = 1$ and a smooth $\varphi$ there; the second-order TVD limiters lie between minmod $\max(0, \min(1, r))$ and superbee $\max(0, \min(2r, 1), \min(r, 2))$.

**Why it matters for convergence.** A conservative, consistent scheme with a uniform TV bound has, by Helly's compactness theorem, subsequences that converge in $L^1_{loc}$, and by the Lax-Wendroff theorem the limits are weak solutions. TV stability plays for nonlinear conservation laws the role that $\ell^2$ stability plays in the [Lax equivalence theorem](/lax-equivalence-theorem/). It does not by itself select the entropy solution; that needs an entropy condition on the scheme.

## Examples

**Square wave, one period.** Advect a unit square pulse on $[0, 1)$ with $M = 100$ cells, periodic boundaries and $\nu = 0.5$ for 200 steps, so the exact solution returns to the initial data with $TV = 2$. Observed:

| scheme | final $TV$ | max | min | $L^1$ error |
|---|---|---|---|---|
| upwind | 1.846 | 0.923 | 0.000 | 0.113 |
| Lax-Wendroff | 3.576 | 1.223 | -0.223 | 0.077 |
| Beam-Warming | 3.467 | 1.213 | -0.213 | 0.075 |
| minmod | 1.997 | 0.998 | 0.000 | 0.049 |
| van Leer | 2.000 | 1.000 | 0.000 | 0.034 |
| MC | 2.000 | 1.000 | 0.000 | 0.029 |
| superbee | 2.000 | 1.000 | 0.000 | 0.018 |

The two linear second-order schemes raise the total variation by 79% and 73% and overshoot by 22%; the limited schemes keep $TV \le 2$ at every step, as Harten's lemma predicts, and are more accurate than upwind by a factor of 2 to 6. Superbee is the most compressive and keeps the edges sharpest; it also tends to square off smooth profiles.

**Smooth data and clipping.** For $u_0 = \sin 2\pi x$ over one period, the $L^1$ errors with $M = 50, 100, 200, 400$ give observed orders 0.93 to 0.98 for upwind, 2.00 for Lax-Wendroff, 1.82 to 1.89 for minmod and 2.11 to 2.17 for van Leer. In the max norm the limited schemes drop to about 1.3 (minmod) and 1.4 (van Leer), because the limiter switches to first order at the two extrema of the sine and clips the peaks.

**Violating the hypothesis.** Harten's conditions need $\nu \le 1$. The minmod scheme run with $\nu = 1.2$ on the square wave reaches $TV \approx 9000$ after 25 steps: the TVD property is gone along with ordinary stability.

## Where it is used

- **High-resolution finite volume methods.** Limited slopes in [MUSCL-type](/finite-volume-method/) reconstruction and limited fluxes on top of [Godunov's method](/godunov-method/) are designed to be TVD for scalar problems, and applied componentwise or in characteristic variables for systems such as the Euler equations, where TVD is no longer a theorem.
- **Time stepping.** Strong-stability-preserving (TVD) Runge-Kutta methods keep the TVD property of a forward Euler step under a Courant number restriction; they are the standard time integrators for [WENO](/weno-scheme/) and limited schemes.
- **Design criterion.** The TVD region is the yardstick for flux limiters, and the related notions (TVB, ENO, monotonicity preserving and maximum principle preserving schemes) all relax it to escape the clipping at extrema.
- **Convergence proofs** for scalar conservation laws in one space dimension, through total variation bounds.

## References
