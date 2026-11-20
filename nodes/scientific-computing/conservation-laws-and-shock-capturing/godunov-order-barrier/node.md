---
tag: GP60PF
kind: theorem
slug: godunov-order-barrier
name: "Godunov's order barrier theorem"
aliases:
- "Godunov's theorem"
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: A linear monotone scheme for the advection equation is at most first order accurate, so high resolution schemes must be nonlinear.
prereqs: [advection-equation, order-of-accuracy, upwind-scheme]
see_also: [total-variation-diminishing, lax-wendroff-method, flux-limiter-methods, muscl-scheme, eno-scheme, weno-scheme, kurganov-tadmor-scheme, godunov-method]
sources:
  - paper: "S. K. Godunov, A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics, Matematicheskii Sbornik 47(89) (1959) 271-306"
    locator: the theorem on monotone linear difference schemes
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 6 (high resolution methods; Section 6.7 total variation, Section 6.12 TVD limiters)
  - paper: doi:10.1016/0021-9991(83)90136-5
    title: A. Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49 (1983) 357-393
    locator: monotone, TVD and monotonicity preserving schemes and the relations between them
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 13 (high resolution and TVD methods)
---

Godunov's order barrier theorem says that a linear scheme for the [advection equation](/advection-equation/) $u_t + au_x = 0$ cannot both keep monotone data monotone and be second order accurate. A linear scheme with this monotonicity property is at most first order, apart from the trivial case where the Courant number is an integer and the scheme is an exact shift. So the [upwind scheme](/upwind-scheme/) does not oscillate but smears shocks, and the [Lax-Wendroff method](/lax-wendroff-method/) is second order but oscillates. The theorem is about linear schemes only. Every high resolution scheme gets around it by being nonlinear: its coefficients depend on the data. This is how [flux limiters](/flux-limiter-methods/), the [MUSCL scheme](/muscl-scheme/), the [ENO](/eno-scheme/) and [WENO](/weno-scheme/) schemes, the [piecewise parabolic method](/piecewise-parabolic-method/), and the central [Nessyahu-Tadmor](/nessyahu-tadmor-scheme/) and [Kurganov-Tadmor](/kurganov-tadmor-scheme/) schemes work. [Total variation diminishing](/total-variation-diminishing/) is a related but different property: for linear schemes it is equivalent to monotonicity, so the barrier holds for linear TVD schemes too, while nonlinear TVD schemes can be second order away from extrema.

## Statement

**Setting.** Consider $u_t + au_x = 0$ on a uniform grid $x_j = j\Delta x$, $t_n = n\Delta t$, with the Courant number $\nu = a\Delta t/\Delta x$ fixed. A **linear scheme** is

$$U_j^{n + 1} = \sum_{k = -l}^{r}c_kU_{j + k}^n,$$

with constants $c_k$ that depend only on $\nu$. It is **monotonicity preserving** if monotone data $U^n$ (nondecreasing or nonincreasing in $j$) always give monotone $U^{n + 1}$ of the same kind. It has **order** $p$ if its local truncation error for smooth solutions is $O(\Delta x^{p + 1})$ per step, see [order of accuracy](/order-of-accuracy/).

**Theorem (Godunov, 1959).** A linear monotonicity preserving scheme for $u_t + au_x = 0$ is at most first order accurate, unless $\nu$ is an integer and the scheme is the exact shift $U_j^{n + 1} = U_{j - \nu}^n$.

**Lemma.** A linear scheme is monotonicity preserving if and only if $c_k \ge 0$ for all $k$. The same holds for monotone in the sense of Harten (1983), and for TVD.

## In plain words

A linear scheme computes each new value as a fixed weighted sum of nearby old values. If all the weights are positive, the new value is an average of old values, and no new peaks or dips can appear. If a weight is negative, a jump in the data produces an overshoot.

Second order accuracy puts three conditions on the weights. These conditions say that the weights act like a probability distribution whose spread is zero. With positive weights that is possible only if all the weight sits on one point, and that is the exact shift. So positive weights and second order cannot go together.

## Proof

**The lemma.** If all $c_k \ge 0$ and $U^n$ is nondecreasing, then $U_{j + 1}^{n + 1} - U_j^{n + 1} = \sum_kc_k(U_{j + 1 + k}^n - U_{j + k}^n) \ge 0$, so $U^{n + 1}$ is nondecreasing. Conversely, let $c_{k_0} < 0$. Take the step data $U_i^n = 0$ for $i \le 0$ and $U_i^n = 1$ for $i \ge 1$, which is nondecreasing. Then $U_{j + 1}^{n + 1} - U_j^{n + 1} = \sum_kc_k(U_{j + 1 + k}^n - U_{j + k}^n) = c_{-j}$, because the difference of the step data is 1 only at $j + k = 0$. With $j = -k_0$ this is $c_{k_0} < 0$, so $U^{n + 1}$ is not monotone. For a linear scheme, monotone in the sense of Harten means that the update is a nondecreasing function of each $U_{j + k}^n$, which is $c_k \ge 0$. A TVD scheme is monotonicity preserving (Harten 1983), and $c_k \ge 0$ gives $\sum_j|U_{j + 1}^{n + 1} - U_j^{n + 1}| \le \sum_kc_k\sum_j|U_{j + 1 + k}^n - U_{j + k}^n| = \sum_j|U_{j + 1}^n - U_j^n|$, so the three properties are the same for linear schemes.

**The moment conditions.** Let $u$ be smooth. The exact solution gives $u(x_j, t_{n + 1}) = u(x_j - \nu\Delta x, t_n)$. Taylor expansion at $x_j$:

$$\sum_kc_ku(x_j + k\Delta x) - u(x_j - \nu\Delta x) = \Big(\sum_kc_k - 1\Big)u + \Delta x\Big(\sum_kkc_k + \nu\Big)u_x + \frac{\Delta x^2}{2}\Big(\sum_kk^2c_k - \nu^2\Big)u_{xx} + O(\Delta x^3).$$

The error is $O(\Delta x^3)$ for every smooth $u$, that is order 2, exactly when

$$\sum_kc_k = 1, \qquad \sum_kkc_k = -\nu, \qquad \sum_kk^2c_k = \nu^2.$$

**The barrier.** Assume order 2 and all $c_k \ge 0$. By the three conditions,

$$\sum_k(k + \nu)^2c_k = \nu^2 - 2\nu^2 + \nu^2 = 0.$$

Every term is nonnegative, so $c_k = 0$ for every $k \ne -\nu$. If $\nu$ is not an integer, all $c_k$ vanish, which contradicts $\sum_kc_k = 1$. If $\nu$ is an integer, then $c_{-\nu} = 1$ and the scheme is the exact shift. In all other cases a scheme with $c_k \ge 0$ is not of order 2, and so not of any order above 1. $\square$

The proof is the statement that a probability distribution with mean $-\nu$ and second moment $\nu^2$ has variance zero.

## Consequences

- **The Lax-Wendroff method has a negative coefficient.** Its coefficients are $c_{-1} = \frac12\nu(1 + \nu)$, $c_0 = 1 - \nu^2$, $c_1 = -\frac12\nu(1 - \nu)$, and $c_1 < 0$ for $0 < \nu < 1$. For $\nu = \frac12$: $c = (\frac38, \frac34, -\frac18)$. Check the moments: the sum is 1, $\sum kc_k = -\frac38 - \frac18 = -\frac12$, $\sum k^2c_k = \frac38 - \frac18 = \frac14$. On the step data $(1, 1, 1, 0, 0, 0)$ it gives $(1, 1, \frac98, \frac38, 0, 0)$ away from the ends: an overshoot of $\frac18$. This is exact arithmetic that the reader can check by hand.
- **First order schemes with positive coefficients.** The upwind scheme for $0 \le \nu \le 1$ has $c_{-1} = \nu$, $c_0 = 1 - \nu$. The Lax-Friedrichs scheme has $c_{\mp 1} = \frac12(1 \pm \nu)$. Both are monotone for $|\nu| \le 1$ and first order, as the theorem says.
- **High resolution needs nonlinear schemes.** Since the barrier holds for all linear schemes, a scheme that is second order in smooth regions and does not oscillate at shocks must have coefficients that depend on the solution. Flux limiters switch between a second order flux and a monotone flux with a limiter function of the ratio of slopes (Harten 1983; LeVeque 2002, Section 6.12). ENO and WENO schemes choose the stencil from the data. These schemes are nonlinear even for the linear advection equation.
- **Nonlinear schemes have their own limits.** TVD schemes drop to first order at smooth extrema of the solution, because the limiter must clip every new extremum. This is the reason for ENO, WENO and relaxed limiters that allow small new extrema.
- **Monotone nonlinear schemes.** A conservative scheme whose update is a nondecreasing function of every argument is called monotone. Harten, Hyman and Lax (1976, CPAM 29, 297-322) proved that such schemes are at most first order too. This is a separate theorem with a different proof.

## Tightness

- **The exact shift.** For integer $\nu$ the shift $U_j^{n + 1} = U_{j - \nu}^n$ is monotone and exact, so the exception in the statement is needed.
- **First order is reached.** The upwind scheme is monotone and first order, so the bound "first order" cannot be lowered.
- **Linearity is needed.** The minmod limited scheme is TVD and second order in smooth monotone regions, which a linear scheme cannot be. So the theorem does not extend to nonlinear schemes in the same form.
- **Monotonicity is needed.** The Lax-Wendroff method is linear and second order, and it has a negative coefficient.

## History

Godunov proved the theorem in his 1959 paper, which also introduced the [Godunov method](/godunov-method/) based on Riemann problems. The theorem explained why the linear schemes of the time either smeared or oscillated at shocks. In the 1970s and 1980s, Boris and Book (flux corrected transport), van Leer (MUSCL) and Harten (TVD schemes, 1983) built nonlinear schemes that get around the barrier. Harten (1983) also set out the relations between monotone, TVD and monotonicity preserving schemes.

## References
