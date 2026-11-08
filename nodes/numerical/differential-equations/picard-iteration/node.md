---
tag: 56X5PF
kind: algorithm
slug: picard-iteration
name: Picard iteration
aliases:
- Picard-Lindelöf iteration
- method of successive approximations
- waveform relaxation
area: numerical/differential-equations
level: advanced
summary: "Solve y' = f(t, y) by y^(k+1)(t) = y_0 + integral of f(s, y^(k)(s)). Converges like (L t)^k / k! when f is Lipschitz; on a grid with the trapezoidal rule its fixed point is the trapezoidal method."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {W: "the number of windows", m: "the number of sub-intervals per window", K: "the number of iterations per window", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(W K m (C + d))"}
  space: {extra: "Θ(m d)"}
  evaluations: {worst: "W K (m + 1)"}
properties: {deterministic: true, implicit: false, iterative: true, order: "2 in the grid spacing (trapezoidal fixed point)", converges_if: "L Δτ / 2 < 1 on the grid", parallel_across_nodes: true}
history:
  year: 1890
  people: [Émile Picard, Ernst Lindelöf, Joseph Liouville]
  note: Liouville used successive approximations for linear equations in 1838; Picard made them a general existence proof in 1890, and Lindelöf gave the sharp Lipschitz form in 1894.
prereqs: [ode-initial-value-problem, lipschitz-condition, banach-fixed-point-theorem]
see_also: [picard-lindelof-theorem, gronwall-inequality, fixed-point-iteration, taylor-series-method, parareal-algorithm, collocation-method, implicit-runge-kutta-methods, stiff-ode-problem]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section I.7 (existence theory, the method of successive approximations and its error bound) and Section II.7 (fixed point iteration for the stages of implicit methods)
  - book: isbn:9780898715101
    title: Philip Hartman, Ordinary Differential Equations, second edition, SIAM Classics in Applied Mathematics, 2002
    locator: Chapter II, Section 1 (the Picard-Lindelöf theorem by successive approximations)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1, Section 1.1 (the Lipschitz condition and existence) and Chapter 7 (functional iteration and Newton iteration for implicit methods)
  - paper: "Émile Picard, Mémoire sur la théorie des équations aux dérivées partielles et la méthode des approximations successives, Journal de Mathématiques Pures et Appliquées (4) 6 (1890) 145-210"
  - paper: "Ekachai Lelarasmee, Albert E. Ruehli and Alberto L. Sangiovanni-Vincentelli, The waveform relaxation method for time-domain analysis of large scale integrated circuits, IEEE Transactions on Computer-Aided Design 1 (1982) 131-145"
---

Picard iteration solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, by rewriting it as the integral equation $y(t) = y_0 + \int_{t_0}^t f(s, y(s))\,ds$ and iterating

$$y^{(k+1)}(t) = y_0 + \int_{t_0}^{t} f\bigl(s, y^{(k)}(s)\bigr)\,ds, \qquad y^{(0)}(t) = y_0.$$

When $f$ is [Lipschitz](/lipschitz-condition/) in $y$ with constant $L$, the iterates converge uniformly on any bounded interval, with error at most $\frac{M}{L}\frac{(L(t - t_0))^{k+1}}{(k+1)!}e^{L(t - t_0)}$; this is the proof of the [Picard-Lindelöf theorem](/picard-lindelof-theorem/). As a numerical method the integral is replaced by a quadrature on a grid and the whole trajectory is updated at once. With the cumulative trapezoidal rule the fixed point is the solution of the implicit trapezoidal method, so the result has order 2 in the grid spacing, and the iteration converges when $L\Delta\tau/2 < 1$ for the grid spacing $\Delta\tau$. Cutting the interval into windows makes the convergence fast in practice.

## In plain words

Start with a rough guess for the whole path, say that nothing moves at all. Using that guess, work out how fast things would change at every moment, and add up those changes from the start. This gives a new path, better than the guess. Repeat with the new path.

Each round fixes the path a bit further out in time, so after enough rounds it is right everywhere. Unlike step-by-step methods, every round updates all moments at once, which suits parallel computers. Over a long time span many rounds are needed, so in practice the time span is cut into pieces and the rounds are done piece by piece.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, continuous and Lipschitz in $y$ with constant $L$, a start value $y_0$, the number of windows $W$, the number of sub-intervals $m$ per window, a tolerance and an iteration limit $K$, compute $y_N \approx y(T)$ and the grid values. The cost is counted in evaluations of $f$.

## The algorithm

On each window $[a, b]$, with nodes $\tau_i = a + i\Delta\tau$, $\Delta\tau = (b - a)/m$:

```pseudo id=main
PICARD-ITERATION(f, t0, y0, T, m, W, tol, K)
L1  ℓ ← (T − t0)/W
L2  for w ← 0 to W − 1 do                       ▷ window [a, b] = [t0 + wℓ, t0 + (w+1)ℓ]
L3      Y_i ← y_start for i = 0..m              ▷ y_start = y0 in the first window
L4      repeat at most K times
L5          F_i ← f(τ_i, Y_i) for i = 0..m       ▷ all nodes at once
L6          Z_0 ← y_start; Z_i ← Z_{i−1} + (Δτ/2)(F_{i−1} + F_i) for i = 1..m
L7          δ ← max_i ‖Z_i − Y_i‖; s ← max(1, max_i ‖Z_i‖, (b − a) max_i ‖F_i‖)
L8          Y ← Z
L9          if δ ≤ tol · s then leave the loop
L10     y_start ← Y_m                           ▷ report failure if the loop did not converge
L11 return y_start
```

Line L6 is the cumulative trapezoidal rule for $\int_a^{\tau_i} f(s, Y(s))\,ds$. The stopping test in line L9 is relative to the size of the terms: an absolute test fails in floating point when $(b - a)\max\|f\|$ is large, because the iterates stall at a rounding level proportional to it. The exact iterates of the continuous iteration for polynomial $f$ can be computed in rational arithmetic; the implementation does both.

## Example

$y' = -2ty^2$, $y(0) = 1$, exact solution $1/(1 + t^2)$.

**Exact iterates.** $y^{(1)} = 1 - t^2$, $y^{(2)} = 1 - t^2 + t^4 - \frac13 t^6$, $y^{(3)} = 1 - t^2 + t^4 - t^6 + \frac23 t^8 - \frac13 t^{10} + \frac19 t^{12} - \frac{1}{63}t^{14}$. Each agrees with $1 - t^2 + t^4 - \cdots$ one degree further. At $t = 1$ the values are $0$, $0.6667$, $0.4286$ against $0.5$.

**On a grid**, $m = 10$, one window: values at $t = 0, 0.2, \dots, 1$ after $k$ sweeps:

| $k$ | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|---|
| 1 | 1 | 0.96 | 0.84 | 0.64 | 0.36 | 0 |
| 2 | 1 | 0.9620 | 0.8656 | 0.7566 | 0.6852 | 0.6684 |
| 3 | 1 | 0.9619 | 0.8628 | 0.7330 | 0.5897 | 0.4263 |
| 4 | 1 | 0.9619 | 0.8630 | 0.7370 | 0.6154 | 0.5223 |
| 19 (converged) | 1 | 0.9619 | 0.8631 | 0.7363 | 0.6110 | 0.5008 |
| exact | 1 | 0.9615 | 0.8621 | 0.7353 | 0.6098 | 0.5 |

The early nodes settle first. The first sweep reproduces $y^{(1)} = 1 - t^2$ exactly at the nodes, because the trapezoidal rule integrates $-2t$ exactly. The converged values differ from the exact ones by the trapezoidal error: at $t = 1$ the errors for $m = 10, 20, 40, 80$ are $7.70 \cdot 10^{-4}$, $1.92 \cdot 10^{-4}$, $4.80 \cdot 10^{-5}$, $1.20 \cdot 10^{-5}$, order 2. The number of sweeps, 17 to 19, does not grow with $m$.

**Fixed point.** For $y' = y$ on $[0, 1]$ the converged value differs from the trapezoidal value $\bigl(\frac{1 + 1/(2m)}{1 - 1/(2m)}\bigr)^m$ by less than $1.4 \cdot 10^{-13}$ for $m = 16, \dots, 128$, after 15 sweeps each.

**Windows.** $y' = -y$ on $[0, 10]$ with 400 sub-intervals in total: with $W = 1, 2, 5, 10, 20$ windows the total number of sweeps is $45$, $58$, $91$, $137$, $216$, but the number of $f$ evaluations falls, $18045$, $11658$, $7371$, $5617$, $4536$, because each sweep of a short window is cheap and few are needed. The final error is $2.36 \cdot 10^{-8}$ in each case.

**Stiff problem.** $y' = -1000y$ on $[0, 1]$, $m = 10$: $L\Delta\tau/2 = 50$ and the iterates overflow; the run reports failure. With $W = 100$ windows of 10 sub-intervals, $L\Delta\tau/2 = \frac12$, the iteration converges (87 sweeps in the first window, 3815 in all) to $|y| < 10^{-12}$. Picard iteration is an explicit process and pays for stiffness like an explicit method.

## Correctness

Proved in the correctness file:

- **Continuous iteration.** If $f$ is continuous on $[t_0, T] \times \mathbb{R}^d$ and Lipschitz in $y$ with constant $L$, and $M = \max_t \|f(t, y_0)\|$, the iterates converge uniformly to the unique solution, with $\|y(t) - y^{(k)}(t)\| \le \frac{M}{L}\frac{(L(t - t_0))^{k+1}}{(k+1)!}e^{L(t - t_0)}$.
- **Discrete iteration.** If $L\Delta\tau/2 < 1$, the map of lines L5 and L6 is a contraction in a weighted max norm, for any window length. So it has a unique fixed point, the trapezoidal solution on the window, and the sweeps converge to it geometrically, with rate as close to $L\Delta\tau/2$ as desired, after a transient that can grow like $(L(b - a))^k/k!$.
- **Order.** The trapezoidal method has global error $O(\Delta\tau^2)$ for $C^3$ solutions (cited, HNW I, Section II.3 and II.7), so the converged result has order 2 in $\Delta\tau$.
- **Termination.** At most $K$ sweeps per window, $W$ windows.

## Complexity

Each sweep evaluates $f$ at the $m + 1$ nodes and does $O(md)$ arithmetic: $\Theta(m(C + d))$. With at most $K$ sweeps per window, the time is $\Theta(WKm(C + d))$ in the [real RAM](/real-ram/) model and the evaluations $WK(m + 1)$; the extra space is $\Theta(md)$ for one window. A step-by-step trapezoidal solver with Newton iteration costs about $Wm$ evaluations plus Jacobians and linear solves, so Picard iteration does more work in total. Its advantage is that the $m + 1$ evaluations of a sweep are independent: with $m + 1$ processors a sweep takes time $\Theta(C + \log m)$ (the cumulative sum is a [parallel prefix](/parallel-prefix/) computation).

## Properties

- **Converges for any window when $L\Delta\tau/2 < 1$**, but the number of sweeps grows with $L(b - a)$: the bound $(L(b - a))^k/k!$ only drops below 1 after about $eL(b - a)$ sweeps, since each sweep fixes the solution roughly over one more interval of length $1/L$.
- **Order 2** at the fixed point with the trapezoidal rule; order up to $2m'$ with Gauss quadrature on $m'$ nodes per sub-interval (spectral deferred correction and collocation variants).
- **Each sweep gains one order** in the continuous iteration: $y^{(k)}$ agrees with the Taylor polynomial of $y$ up to degree $k$ when $f$ is analytic and $y^{(0)} = y_0$.
- **Not suited to stiff problems**, since convergence needs $L\Delta\tau = O(1)$, as for explicit methods.
- **Parallel across the time nodes and across components** (waveform relaxation splits the components as well).

## Variants and improvements

- **Waveform relaxation.** For large coupled systems, iterate each subsystem over a whole time window with the other subsystems' waveforms from the last sweep (Jacobi or Gauss-Seidel style); used for circuit simulation since Lelarasmee, Ruehli and Sangiovanni-Vincentelli (1982). Its convergence theory is the same weighted-norm argument.
- **Spectral and Chebyshev Picard methods.** Represent the iterate by Chebyshev polynomials and integrate exactly; used in orbit propagation (modified Chebyshev-Picard iteration).
- **Spectral deferred correction.** Iterate on the error equation with a low-order sweep; each sweep raises the order by one up to the collocation order.
- **Newton-type waveform relaxation.** Linearise around the last iterate to handle stiffness, at the cost of linear solves.
- **The stage iteration of implicit methods.** For an [implicit Runge-Kutta method](/implicit-runge-kutta-methods/) the fixed point iteration $Z \leftarrow h(A \otimes I)F(Z)$ for the stages is Picard iteration on one step; it converges when $hL\|A\| < 1$.
- **Parareal.** The [parareal algorithm](/parareal-algorithm/) also iterates on whole trajectories, but corrects with a coarse sequential solver, which makes it converge in fewer sweeps.

## When to use it

Use it to prove existence and to get series solutions by hand or in exact arithmetic; numerically, when a whole trajectory is wanted, $f$ is cheap to evaluate in parallel, and the problem is not stiff; and as the inner solver of collocation and waveform relaxation schemes. For a single serial run of a nonstiff problem, a Runge-Kutta method is cheaper; for stiff problems use an implicit method with Newton iteration.

## Pitfalls

- **Long windows.** The continuous error bound $\frac{(L(t - t_0))^{k+1}}{(k+1)!}$ is tiny only after $k \gg L(t - t_0)$ sweeps, and intermediate iterates can be huge (differences between sweeps near 4700 for $y' = -1000y$, $y_0 = 1$, on a window of length 0.01). Choose windows with $L(b - a)$ of order 1 to 10.
- **Absolute stopping tests.** They can fail to be met in floating point; scale the tolerance with the size of the terms.
- **Accuracy is set by the quadrature**, not by the number of sweeps: once converged, extra sweeps do not reduce the error below the trapezoidal error.
- **Stiffness.** $L\Delta\tau/2 \ge 1$ makes the discrete iteration diverge no matter how many sweeps are made.

## Implementations

## History

Liouville used successive approximations for second order linear equations in 1838, and Peano and others used them for linear systems. Picard made the method a general tool in 1890, in a memoir on partial differential equations, and Lindelöf in 1894 gave the version for Lipschitz $f$ that is now the textbook proof of existence and uniqueness. Numerical use followed with computers: functional iteration for implicit methods, Clenshaw and Norton's Chebyshev series (1963), and waveform relaxation for circuits (1982), which made the method a parallel-in-time technique.

## References
