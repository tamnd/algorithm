---
tag: N95ZRW
kind: algorithm
slug: lax-wendroff-method
name: Lax-Wendroff method
aliases:
- Lax-Wendroff scheme
- Richtmyer two-step Lax-Wendroff method
area: numerical/differential-equations
level: advanced
summary: "Second order explicit scheme for u_t + f(u)_x = 0 from a Taylor expansion in time. Stable for |nu| <= 1 in L2; dispersive, so it oscillates near shocks and steep fronts."
solves: [advection-equation, burgers-equation]
model: real-ram
complexity:
  vars: {m: "the number of cells", N: "the number of time steps, ⌈T/Δt⌉", C: "the cost of one evaluation of the flux f"}
  time: {worst: "Θ(N m (C + 1))"}
  space: {extra: "Θ(m)"}
  evaluations: {worst: "2 N m"}
properties: {deterministic: true, explicit: true, conservative: true, order: "2 in space and time", stable_for: "|ν| <= 1 in the L2 norm", monotone: false, tvd: false}
history:
  year: 1960
  people: [Peter D. Lax, Burton Wendroff, Robert D. Richtmyer]
  note: Lax and Wendroff published the scheme in 1960 together with the theorem that convergent conservative schemes converge to weak solutions. Richtmyer gave the two-step form in 1963.
prereqs: [advection-equation, courant-friedrichs-lewy-condition, lax-friedrichs-scheme]
see_also: [upwind-scheme, flux-limiter-methods, total-variation-diminishing, von-neumann-stability-analysis, lax-equivalence-theorem, godunov-method, burgers-equation, method-of-lines]
sources:
  - paper: doi:10.1002/cpa.3160130205
    title: Peter Lax and Burton Wendroff, Systems of conservation laws, Communications on Pure and Applied Mathematics 13 (1960) 217-237
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 10 (the Lax-Wendroff method, von Neumann analysis, modified equations, dispersion)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 6 (Lax-Wendroff as a second order method, oscillations, high-resolution methods), Chapter 8 (accuracy, stability, modified equations) and Chapter 12 (the Lax-Wendroff theorem, Richtmyer and MacCormack forms)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 3 (order of accuracy and the Lax-Wendroff scheme) and Chapter 5 (dispersion and group velocity)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 4 (hyperbolic equations in one space dimension, the Lax-Wendroff scheme)
---

The Lax-Wendroff method solves a conservation law $u_t + f(u)_x = 0$, and in particular the [advection equation](/advection-equation/) $u_t + au_x = 0$, with second order accuracy in both space and time, using only three neighbouring values per step. For linear advection with Courant number $\nu = a\Delta t/\Delta x$ and $U_j^n \approx u(x_j, t_n)$ it reads

$$U_j^{n+1} = U_j^n - \frac{\nu}{2}\bigl(U_{j+1}^n - U_{j-1}^n\bigr) + \frac{\nu^2}{2}\bigl(U_{j+1}^n - 2U_j^n + U_{j-1}^n\bigr).$$

It comes from the Taylor series $u(t + \Delta t) = u + \Delta t\, u_t + \frac{\Delta t^2}{2} u_{tt} + \ldots$ with the time derivatives replaced by space derivatives from the equation, $u_t = -au_x$ and $u_{tt} = a^2 u_{xx}$. It is stable in the $L^2$ norm for $|\nu| \le 1$. Its leading error is dispersive, so near jumps it produces oscillations; it is the basis of the high-resolution schemes that add [flux limiters](/flux-limiter-methods/).

## In plain words

To move a profile along a grid, the simplest schemes look at the slope next to each point. Lax-Wendroff also looks at how the slope bends, and uses that to correct its step. This makes it much more accurate on smooth waves: when the grid is twice as fine, the error drops to a quarter.

The same correction misbehaves near a sharp edge. There the bending is huge, and the scheme answers with small ripples next to the edge, values above the top and below the bottom of the jump. So it is excellent for smooth waves and needs help, a limiter that switches to a cautious scheme near edges, for shocks.

## The problem

Given a flux $f \in C^1$, cell values $U_j^0$ ($j = 0, \dots, m - 1$) of $u_0$, periodic or transmissive boundary conditions, $T \ge 0$ and $\Delta x, \Delta t > 0$, compute $U^N$ with $t_N = T$. For linear advection the Courant number is $\nu = a\Delta t/\Delta x$; the error is measured in the discrete $L^1$, $L^2$ or max norm. The cost is counted in flux evaluations and arithmetic per cell and step.

## The algorithm

Richtmyer's two-step form, which works for any flux and needs no derivative of $f$:

```pseudo id=main
LAX-WENDROFF(U^0, f, Δx, Δt, T, bc)
L1  N ← ⌈T/Δt − δ⌉                         ▷ δ: relative slack 10^-9 against rounding
L2  U ← U^0, t ← 0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else (n + 1)Δt
L5      λ ← (t_next − t)/Δx
L6      F_j ← f(U_j) for all j
L7      add ghost values U_m, F_m from bc     ▷ periodic: wrap; transmissive: copy
L8      V_{j+1/2} ← (U_j + U_{j+1})/2 − (λ/2)(F_{j+1} − F_j)   ▷ Lax-Friedrichs half step
L9      G_{j+1/2} ← f(V_{j+1/2}) for all j
L10     U_j ← U_j − λ (G_{j+1/2} − G_{j−1/2}) for all j          ▷ leapfrog-like full step
L11     t ← t_next
L12 return U
```

Line L8 is a [Lax-Friedrichs](/lax-friedrichs-scheme/) step of length $\Delta t/2$ to the cell faces, and line L10 is a conservative update with the midpoint-in-time flux. For $f(u) = au$, substituting L8 into L10 gives exactly the one-step formula above (the tests check this with exact fractions). In the one-step form,

$$U_j^{n+1} = \frac{\nu(1 + \nu)}{2} U_{j-1}^n + (1 - \nu^2) U_j^n - \frac{\nu(1 - \nu)}{2} U_{j+1}^n,$$

which is the value at $x_j - \nu\Delta x$ of the quadratic that interpolates $U^n$ at $x_{j-1}, x_j, x_{j+1}$.

## Example

**Two steps by hand.** With $\nu = \frac12$ the weights are $\frac38$, $\frac34$, $-\frac18$. From $U^0 = (0, 0, 1, 1, 0, 0, 0, 0)$, periodic, $U^1 = (0, -\frac18, \frac58, \frac98, \frac38, 0, 0, 0)$ and $U^2 = (\frac{1}{64}, -\frac{11}{64}, \frac{9}{32}, \frac{33}{32}, \frac{45}{64}, \frac{9}{64}, 0, 0)$. The negative weight creates the value $-\frac18$ ahead of nothing and the overshoot $\frac98$ after one step: the scheme is not monotone.

**Convergence on smooth data.** $u_t + u_x = 0$, $u_0 = \sin 2\pi x$ on $[0, 1]$ periodic, $\nu = 0.5$, $T = 0.5$:

| $\Delta x$ | 1/100 | 1/200 | 1/400 | 1/800 |
|---|---|---|---|---|
| $L^1$ error | $9.8687 \cdot 10^{-4}$ | $2.4673 \cdot 10^{-4}$ | $6.1685 \cdot 10^{-5}$ | $1.5421 \cdot 10^{-5}$ |
| max error | $1.549 \cdot 10^{-3}$ | $3.875 \cdot 10^{-4}$ | $9.689 \cdot 10^{-5}$ | $2.422 \cdot 10^{-5}$ |

The ratios are $4.00$: second order. [Lax-Friedrichs](/lax-friedrichs-scheme/) has error $0.0454$ at $\Delta x = 1/200$, 184 times larger.

**Phase lag.** A Gaussian pulse $e^{-100(x - 0.5)^2}$, $\Delta x = 1/100$, $\nu = 0.5$, after one period $T = 1$: the exact peak is at $x = 0.5$; the computed peak is at $x = 0.49$ with height $0.9908$, and small negative values down to $-5.8 \cdot 10^{-4}$ trail behind. The waves of the scheme are slightly slower than $a$.

**Discontinuous data.** For the step $u_0 = 1$ on $[0.25, 0.5)$ at $T = 0.5$, the $L^1$ errors at $\Delta x = 1/100, 1/200, 1/400, 1/800$ are $0.0594$, $0.0394$, $0.0262$, $0.0173$, an observed order of about $0.6$, and the solution ranges over $[-0.204, 1.204]$, $[-0.223, 1.223]$, $[-0.232, 1.232]$, $[-0.239, 1.239]$. The oscillations do not shrink as the grid is refined; they only get narrower.

**At the stability limit.** Sine data plus random noise of size $10^{-3}$ (seed 1), $\Delta x = 1/100$, $T = 5$: $\max_j |U_j^N|$ is $1.000$ for $\nu = 0.95$, $0.99$ and $1$, but $2.8 \cdot 10^4$ for $\nu = 1.01$ and $1.7 \cdot 10^{34}$ for $\nu = 1.05$. The growth is much faster than for Lax-Friedrichs, whose amplification factor exceeds 1 by less.

**Burgers' equation.** $u_t + (u^2/2)_x = 0$, $u_L = 1$ left of $0.3$, $u_R = 0$, $\Delta x = 1/200$, $\Delta t = 0.8\Delta x$, $T = 0.4$: the shock is between $x = 0.4975$ and $0.5025$ as it should be, the $L^1$ error is $0.0025$ (Lax-Friedrichs: $0.0069$), and the solution overshoots to $1.239$ behind the shock.

## Correctness

For linear advection with periodic boundary conditions, $u_0 \in C^3$ and $0 < |\nu| \le 1$, the scheme converges with order 2 in the discrete $L^2$ norm $\|v\|_{2} = (\Delta x \sum_j v_j^2)^{1/2}$ on a domain of length $\ell$:

$$\|u(\cdot, t_N) - U^N\|_{2} \le \frac{T|a|(1 - \nu^2)}{6}\, M_3 \sqrt{\ell}\; \Delta x^2, \qquad M_3 = \max|u_0'''|.$$

The proof has two parts. The local error is the error of quadratic interpolation at $x_j - \nu\Delta x$, at most $\frac{M_3}{6}|\nu|(1 - \nu^2)\Delta x^3$. The scheme does not increase the $L^2$ norm, because each Fourier mode is multiplied by $g(\theta)$ with $|g(\theta)|^2 = 1 - \nu^2(1 - \nu^2)(1 - \cos\theta)^2 \le 1$; by discrete Parseval this is $L^2$ stability. Adding $N = T|a|/(|\nu|\Delta x)$ local errors gives the bound. It is proved and non-asymptotic; the proof is in the correctness file. The scheme is not stable in the max norm with constant 1, since one weight is negative.

For nonlinear $f$ the scheme is conservative and consistent, so by the Lax-Wendroff theorem any bounded a.e. limit of the computed solutions is a weak solution, with shocks moving at the right speed (cited). It is not monotone, so the entropy condition is not guaranteed.

## Complexity

Each step evaluates the flux at $m$ cells and $m$ faces and does $O(1)$ arithmetic per cell: $\Theta(m(C + 1))$ per step and $\Theta(N m (C + 1))$ in total, with $2Nm$ flux evaluations, in the [real RAM](/real-ram/) model. Extra space $\Theta(m)$. At fixed $\nu$, $N \propto m$, so a fixed $T$ costs $\Theta(m^2)$ in one dimension. Since the error on smooth data is $O(\Delta x^2)$, an error $\varepsilon$ costs $\Theta(\varepsilon^{-1})$ against $\Theta(\varepsilon^{-2})$ for first-order schemes (asymptotic).

## Properties

- **Order 2.** The truncation error is $O(\Delta t^2 + \Delta x^2)$; at fixed $\nu$, $O(\Delta x^2)$.
- **Amplification factor.** $g(\theta) = 1 - i\nu\sin\theta - \nu^2(1 - \cos\theta)$, so $|g| \le 1$ for all $\theta$ exactly when $|\nu| \le 1$ ([von Neumann analysis](/von-neumann-stability-analysis/)). At $\nu = \pm 1$ the scheme is the exact shift by one cell.
- **Modified equation.** To third order the scheme solves $u_t + au_x = -\frac{a\Delta x^2}{6}(1 - \nu^2)u_{xxx}$, a dispersive equation: a Fourier mode with wave number $k$ moves with speed about $a\bigl(1 - \frac{(1 - \nu^2)k^2\Delta x^2}{6}\bigr) < a$. Short waves lag behind, which forms the trailing wiggles behind steep fronts.
- **Not monotone, not TVD.** By Godunov's theorem a linear scheme of second order cannot be monotone. The overshoots near a jump persist under refinement, at about 20 to 24 percent of the jump in the example.
- **Conservative.** With periodic boundary conditions $\sum_j U_j$ is exactly constant (checked with fractions).
- **Symmetric stencil.** Like Lax-Friedrichs it needs no upwind direction and works for systems $u_t + f(u)_x = 0$ unchanged.

## Variants and improvements

- **The original form.** Lax and Wendroff wrote the second derivative with the Jacobian $A = f'(u)$: $U_j^{n+1} = U_j - \frac{\lambda}{2}(F_{j+1} - F_{j-1}) + \frac{\lambda^2}{2}\bigl(A_{j+1/2}(F_{j+1} - F_j) - A_{j-1/2}(F_j - F_{j-1})\bigr)$. The two-step forms avoid the Jacobian.
- **MacCormack's method.** A predictor with forward differences and a corrector with backward differences; the same as Lax-Wendroff for linear problems.
- **Flux-limited schemes.** Write the flux as the [upwind](/upwind-scheme/) flux plus a correction toward the Lax-Wendroff flux, multiplied by a limiter that is near 1 in smooth regions and near 0 at jumps: the [TVD](/total-variation-diminishing/) high-resolution schemes of LeVeque's Chapter 6.
- **Artificial viscosity.** Add a term $\varepsilon\,\Delta x^2 |u_x| u_{xx}$ to damp the oscillations; older but still common in engineering codes.
- **Beam-Warming.** A one-sided second order scheme, stable for $0 \le \nu \le 2$, whose wiggles appear ahead of jumps instead of behind.
- **Lax-Wendroff and the method of lines.** For $u_t = -au_x$ with central differences, the Taylor step is a second order Taylor method in time with an extra space correction; the Cauchy-Kovalevskaya (ADER) schemes extend the idea to high order.

## When to use it

Use Lax-Wendroff for smooth solutions of linear or weakly nonlinear hyperbolic problems, such as acoustics and linear waves, where its second order and low cost per step pay off, and as the high-order part of a flux-limited scheme. Do not use it alone where shocks or steep fronts occur, or where positivity matters, such as densities and concentrations.

## Pitfalls

- **Oscillations near jumps.** They do not go away under refinement, and they can produce negative densities or pressures in gas dynamics.
- **Dispersion at low resolution.** With fewer than about 10 points per wavelength the phase error is large; a pulse arrives late and leaves a wave train behind.
- **The stability limit is sharp.** At $\nu = 1.01$ the solution of the example grows by a factor $10^4$ over about 500 steps. Choose $\Delta t$ from the largest wave speed $\max|f'(u)|$, which can change in time.
- **Boundary conditions.** The transmissive copy is first order and can reflect waves; a true outflow condition for a second order scheme needs extrapolation of higher order.

## Implementations

## History

Lax and Wendroff published the scheme in 1960 in "Systems of conservation laws", together with the theorem that a convergent conservative scheme converges to a weak solution, which makes shock speeds come out right. Richtmyer proposed the two-step form in a 1963 report and MacCormack the predictor-corrector form in 1969. The oscillations of the scheme motivated the flux-corrected transport of Boris and Book (1973), van Leer's MUSCL schemes and Harten's TVD schemes.

## References
