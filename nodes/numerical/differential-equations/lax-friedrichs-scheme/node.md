---
tag: 5WKGZC
kind: algorithm
slug: lax-friedrichs-scheme
name: Lax-Friedrichs scheme
aliases:
- Lax-Friedrichs method
- Lax method
area: numerical/differential-equations
level: advanced
summary: "U_j^(n+1) = (U_(j-1) + U_(j+1))/2 - (dt/(2dx))(f(U_(j+1)) - f(U_(j-1))). First order, conservative and monotone for |nu| <= 1; very diffusive, more so as nu shrinks."
solves: [advection-equation, burgers-equation]
model: real-ram
complexity:
  vars: {m: "the number of cells", N: "the number of time steps, ⌈T/Δt⌉", C: "the cost of one evaluation of the flux f"}
  time: {worst: "Θ(N m (C + 1))"}
  space: {extra: "Θ(m)"}
  evaluations: {worst: "N m"}
properties: {deterministic: true, explicit: true, conservative: true, order: "1", monotone: "for max |f'(u)| Δt/Δx <= 1", stable_for: "|ν| <= 1", tvd: true}
history:
  year: 1954
  people: [Peter D. Lax, Kurt O. Friedrichs]
  note: Lax used the scheme in 1954 to compute weak solutions of nonlinear conservation laws, including shocks; Friedrichs studied the same averaging for symmetric hyperbolic systems in the same year.
prereqs: [advection-equation, courant-friedrichs-lewy-condition, finite-volume-method]
see_also: [upwind-scheme, lax-wendroff-method, godunov-method, burgers-equation, von-neumann-stability-analysis, total-variation-diminishing, lax-equivalence-theorem, riemann-problem]
sources:
  - paper: doi:10.1002/cpa.3160070112
    title: Peter D. Lax, Weak solutions of nonlinear hyperbolic equations and their numerical computation, Communications on Pure and Applied Mathematics 7 (1954) 159-193
  - paper: doi:10.1002/cpa.3160070206
    title: K. O. Friedrichs, Symmetric hyperbolic linear differential equations, Communications on Pure and Applied Mathematics 7 (1954) 345-392
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 4 (finite volume methods and the Lax-Friedrichs flux), Chapter 8 (convergence, accuracy and stability) and Chapter 12 (monotone methods for nonlinear scalar conservation laws)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 10 (advection equations, the Lax-Friedrichs method, von Neumann analysis and modified equations)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 1 (the one-way wave equation and the Lax-Friedrichs scheme) and Chapter 2 (von Neumann analysis)
  - paper: doi:10.1090/S0025-5718-1980-0551288-3
    title: Michael G. Crandall and Andrew Majda, Monotone difference approximations for scalar conservation laws, Mathematics of Computation 34 (1980) 1-21
---

The Lax-Friedrichs scheme solves a scalar conservation law $u_t + f(u)_x = 0$, and in particular the [advection equation](/advection-equation/) $u_t + a u_x = 0$, on a grid $x_j = j\Delta x$, $t_n = n\Delta t$ with values $U_j^n \approx u(x_j, t_n)$:

$$U_j^{n+1} = \frac{U_{j-1}^n + U_{j+1}^n}{2} - \frac{\Delta t}{2\Delta x}\Bigl(f(U_{j+1}^n) - f(U_{j-1}^n)\Bigr).$$

It is the unstable centred scheme FTCS with $U_j^n$ replaced by the average of its neighbours. That one change makes the scheme stable for Courant numbers $|\nu| \le 1$, $\nu = a\Delta t/\Delta x$, conservative and monotone, so it converges to the physically correct (entropy) solution even through shocks. The price is first order accuracy and strong numerical diffusion, which grows as $\Delta t$ shrinks at fixed $\Delta x$.

## In plain words

Picture a row of cups along a channel, each holding some water that is carried downstream. To find the new level in a cup, the scheme first takes the average of its two neighbours, then corrects it by how much more flows in from one side than out the other. The averaging is what keeps the method calm: no cup can ever get more than the fullest of its neighbours had.

The same averaging also blurs every sharp edge, a little at each step. So the method is safe and simple, and it gets shocks in the right place, but the picture it draws is smeared. It is used where safety matters more than sharpness, and as a building block inside better methods.

## The problem

Given a flux $f \in C^1(\mathbb{R})$, cell values $U_j^0$ ($j = 0, \dots, m - 1$) of the initial data $u_0$, periodic or transmissive boundary conditions, a final time $T \ge 0$ and $\Delta x, \Delta t > 0$, compute $U_j^N$ with $t_N = T$. The error is measured in the discrete $L^1$ norm $\Delta x \sum_j |U_j^N - u(x_j, T)|$ or the max norm. For the linear case the Courant number is $\nu = a\Delta t/\Delta x$; for a nonlinear flux the relevant number is $\max |f'(u)|\,\Delta t/\Delta x$. The cost is counted in flux evaluations and arithmetic per cell and step.

## The algorithm

```pseudo id=main
LAX-FRIEDRICHS(U^0, f, Δx, Δt, T, bc)
L1  N ← ⌈T/Δt − δ⌉                        ▷ δ: relative slack 10^-9 against rounding
L2  U ← U^0, t ← 0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else (n + 1)Δt
L5      λ ← (t_next − t)/Δx                ▷ Δt/Δx, smaller for a shortened last step
L6      F_j ← f(U_j) for all j
L7      add ghost values U_{−1}, U_m, F_{−1}, F_m from bc    ▷ periodic: wrap; transmissive: copy
L8      U_j ← (U_{j−1} + U_{j+1})/2 − (λ/2)(F_{j+1} − F_{j−1}) for all j (from the old values)
L9      t ← t_next
L10 return U
```

**Conservation form.** Line L8 equals $U_j^{n+1} = U_j^n - \lambda(\hat F_{j+1/2} - \hat F_{j-1/2})$ with the numerical flux

$$\hat F_{j+1/2} = \frac{f(U_j) + f(U_{j+1})}{2} - \frac{\Delta x}{2\Delta t}(U_{j+1} - U_j),$$

the central flux plus a diffusion term. In the language of [finite volume methods](/finite-volume-method/) it is the Rusanov flux with the largest possible signal speed $\Delta x/\Delta t$.

**Linear form.** For $f(u) = a u$, line L8 reads $U_j^{n+1} = \frac{1 + \nu}{2} U_{j-1}^n + \frac{1 - \nu}{2} U_{j+1}^n$: a convex combination of the two neighbours when $|\nu| \le 1$.

## Example

**One step by hand.** With $a = 1$, $\nu = 0.5$ and $U^0 = (0, 0, 1, 1, 0, 0, 0, 0)$ periodic, the weights are $0.75$ and $0.25$, and $U^1 = (0, 0.25, 0.25, 0.75, 0.75, 0, 0, 0)$, then $U^2 = (0.0625, 0.0625, 0.375, 0.375, 0.5625, 0.5625, 0, 0)$. The values come in equal pairs: $U_j^{n+1}$ uses only $U_{j\pm1}^n$, so the even and odd points form two decoupled grids, which shows as a staircase.

**Convergence on smooth data.** $u_t + u_x = 0$, $u_0 = \sin 2\pi x$ on $[0, 1]$ periodic, $T = 0.5$, $\nu = 0.5$:

| $\Delta x$ | 1/100 | 1/200 | 1/400 | 1/800 |
|---|---|---|---|---|
| $L^1$ error | 0.087644 | 0.045427 | 0.023132 | 0.011673 |

The ratios $1.93$, $1.96$, $1.98$ tend to 2: first order. On the same problem the [upwind scheme](/upwind-scheme/) has error $0.015515$ at $\Delta x = 1/200$, three times smaller, and [Lax-Wendroff](/lax-wendroff-method/) $0.00024673$ (numbers from the advection page).

**The effect of $\nu$.** At $\Delta x = 1/200$ the $L^1$ errors for $\nu = 0.1, 0.25, 0.5, 0.9, 1$ are $0.2461$, $0.1076$, $0.04543$, $0.006899$ and $7 \cdot 10^{-16}$. At $\nu = 1$ the scheme is the exact shift $U_j^{n+1} = U_{j-1}^n$; for small $\nu$ the many steps each add diffusion.

**Discontinuous data.** For the step $u_0 = 1$ on $[0.25, 0.5)$, with the same settings, the $L^1$ errors at $\Delta x = 1/100, 1/200, 1/400, 1/800$ are $0.1375$, $0.0975$, $0.0690$, $0.0488$: a factor $1.41$ per halving, observed order $1/2$. The solution stays in $[0, 1]$ with no overshoot.

**At the stability limit.** Sine data plus random noise of size $10^{-3}$ (seed 1), $\Delta x = 1/100$, $T = 5$: $\max_j |U_j^N|$ is $0.903$ for $\nu = 0.95$, $0.979$ for $\nu = 0.99$, $1.000$ for $\nu = 1$, $1.019$ for $\nu = 1.01$ and $5.3 \cdot 10^5$ for $\nu = 1.05$.

**Burgers' equation.** For $u_t + (u^2/2)_x = 0$ with $u_L = 1$ left of $x = 0.3$ and $u_R = 0$ right of it, the shock moves with speed $\frac12$. With $\Delta x = 1/200$, $\Delta t = 0.8\Delta x$ and $T = 0.4$, the computed profile crosses $\frac12$ between $x = 0.4975$ and $0.5025$, around the exact position $0.5$, and the $L^1$ error is $0.0069$. With the data swapped ($u_L = 0$, $u_R = 1$) the scheme produces the rarefaction fan, the entropy solution, with $L^1$ error $0.018$, and not the stationary expansion shock that also solves the equation weakly.

## Correctness

For the linear advection equation with periodic boundary conditions, $u_0 \in C^2$ and $0 < |\nu| \le 1$, the scheme converges in the max norm with

$$\max_j |u(x_j, t_N) - U_j^N| \le N \cdot \frac{M_2}{2} \Delta x^2 (1 - \nu^2) = \frac{T |a| (1 - \nu^2)}{2 |\nu|} M_2\, \Delta x, \qquad M_2 = \max |u_0''|,$$

for equal steps. The proof has two parts. The exact solution is a shift, $u(x, t + \Delta t) = u(x - \nu\Delta x, t)$, and the scheme is linear interpolation between $x - \Delta x$ and $x + \Delta x$ evaluated at $x - \nu \Delta x$; so the local error is an interpolation error, at most $\frac{M_2}{2}(1 - \nu)(1 + \nu)\Delta x^2$. The scheme is a convex combination when $|\nu| \le 1$, so it does not increase the max norm, and the errors add up over $N$ steps. This is a proved, non-asymptotic bound; it is the [Lax equivalence theorem](/lax-equivalence-theorem/) at work.

For nonlinear $f$ the scheme is conservative, so when it converges the limit is a weak solution (the Lax-Wendroff theorem), and it is monotone under $\max|f'(u)|\Delta t/\Delta x \le 1$, so it converges to the entropy solution (Crandall and Majda 1980, cited, not proved here). The proofs are in the correctness file.

## Complexity

Each step evaluates the flux once per cell and does $O(1)$ arithmetic per cell: $\Theta(m(C + 1))$ per step and $\Theta(N m (C + 1))$ in total, with $N = \lceil T/\Delta t \rceil$, in the [real RAM](/real-ram/) model. The extra space is $\Theta(m)$ for the flux values and the new layer. At a fixed Courant number $N \propto m$, so reaching a fixed $T$ costs $\Theta(m^2)$ in one space dimension, and $\Theta(m^{k+1})$ on a grid with $m$ cells per direction in $k$ dimensions. Because the error is $O(\Delta x)$ for smooth data, an error $\varepsilon$ costs $\Theta(\varepsilon^{-2})$ in one dimension (asymptotic).

## Properties

- **Stability.** The amplification factor for $u_t + a u_x = 0$ is $g(\theta) = \cos\theta - i\nu\sin\theta$, with $|g|^2 = \cos^2\theta + \nu^2\sin^2\theta$. So $|g| \le 1$ for all $\theta$ exactly when $|\nu| \le 1$ ([von Neumann analysis](/von-neumann-stability-analysis/)), in agreement with the [CFL condition](/courant-friedrichs-lewy-condition/) for a stencil that reaches one cell to each side.
- **Modified equation.** The scheme is closer to $u_t + a u_x = D u_{xx}$ with $D = \frac{\Delta x^2}{2\Delta t}(1 - \nu^2) = \frac{|a|\Delta x}{2|\nu|}(1 - \nu^2)$ than to the advection equation. For $\nu = 0.5$ this is three times the diffusion $\frac{|a| \Delta x}{2}(1 - |\nu|)$ of upwind.
- **Monotone, TVD, maximum principle.** Under the CFL condition $U_j^{n+1}$ is a nondecreasing function of $U_{j-1}^n$ and $U_{j+1}^n$, so the scheme preserves order, does not create new extrema and does not increase the total variation ([TVD](/total-variation-diminishing/)). By Godunov's theorem a linear monotone scheme is at most first order, so this costs accuracy.
- **Conservative.** With periodic boundary conditions $\sum_j U_j^n$ is exactly constant, up to rounding.
- **Odd-even decoupling.** The checkerboard mode $(-1)^j$ has $g(\pi) = -1$: it changes sign at every step and is never damped, for any $\nu$.
- **No need for the sign of $f'$.** The scheme is symmetric in space and needs no upwind direction and no Riemann solver, so it works unchanged for systems.

## Variants and improvements

- **Rusanov (local Lax-Friedrichs) flux.** Replace $\frac{\Delta x}{\Delta t}$ in the numerical flux by the local maximum speed $\max(|f'(U_j)|, |f'(U_{j+1})|)$. Much less diffusive and still monotone; the standard simple flux for systems.
- **Staggered Lax-Friedrichs.** Store values at $x_{j+1/2}$ on alternate steps, which removes the decoupling. With a piecewise linear reconstruction this gives the Nessyahu-Tadmor central scheme of second order.
- **[Lax-Wendroff](/lax-wendroff-method/), Richtmyer two-step form.** Its predictor is a Lax-Friedrichs half-step on the staggered grid.
- **Systems and several dimensions.** For $u_t + f(u)_x + g(u)_y = 0$ average over the four neighbours; the stability condition becomes stricter in two dimensions.

## When to use it

Use Lax-Friedrichs as a robust first try for a new system of conservation laws, as the low-order flux in flux-limited and flux-corrected schemes, as a reference that is known to converge to the entropy solution, and in teaching. For accurate results use upwind-based [Godunov](/godunov-method/) methods with [flux limiters](/flux-limiter-methods/) or [WENO](/weno-scheme/) reconstructions.

## Pitfalls

- **Small time steps make it worse.** At fixed $\Delta x$ the error grows as $\Delta t$ shrinks, because the diffusion $\Delta x^2/(2\Delta t)$ grows. Run it near $|\nu| = 1$, and choose $\Delta t$ from the largest wave speed.
- **Nonlinear CFL.** For a nonlinear flux the limit is $\max|f'(u)|\Delta t/\Delta x \le 1$ over the values that occur, which change in time; check it at every step.
- **The checkerboard mode.** Odd-even oscillations in the data survive forever; do not mistake them for a physical effect.
- **Boundaries.** The transmissive copy of the last cell is a simple outflow condition; it reflects waves partly and is not a physical boundary condition.

## Implementations

## History

Lax introduced the scheme in 1954 as a method for weak solutions of nonlinear hyperbolic conservation laws, showing that a conservative scheme computes shocks with the right speed. Friedrichs used the same averaging in his 1954 work on symmetric hyperbolic systems. Crandall and Majda proved in 1980 that conservative monotone schemes, Lax-Friedrichs among them, converge to the entropy solution of scalar conservation laws.

## References
