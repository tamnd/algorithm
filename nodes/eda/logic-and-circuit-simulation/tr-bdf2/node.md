---
tag: W1B2JC
kind: algorithm
slug: tr-bdf2
name: TR-BDF2
aliases:
- Bank-Coughran TR-BDF2
- trapezoidal BDF2 method
area: eda/logic-and-circuit-simulation
level: advanced
summary: An L-stable second-order one-step integrator that does a trapezoidal stage to t + gamma h and a BDF2 stage to t + h, with gamma = 2 - sqrt(2) so both stages share one matrix.
model: real-ram
complexity:
  vars: {n: "the number of MNA unknowns", N: "the number of time steps", K: "the Newton iterations per stage", T: "the cost of one sparse LU solve of the MNA matrix"}
  time: {worst: "O(N K T)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1985
  people: [Randolph E. Bank, William M. Coughran Jr., Wolfgang Fichtner, Eric H. Grosse, Donald J. Rose, R. Kent Smith]
  note: Bank, Coughran, Fichtner, Grosse, Rose and Smith proposed the method in 1985 for transient simulation of devices and circuits. Hosea and Shampine analysed it in 1996.
prereqs: [trapezoidal-rule, backward-differentiation-formulas, l-stability, companion-model, differential-algebraic-equations, transient-circuit-analysis]
see_also: [stiff-ode-problem, a-stability, adaptive-step-size-control, local-truncation-error, backward-euler-method, implicit-runge-kutta-methods, radau-iia-methods, klu-solver]
sources:
  - paper: doi:10.1109/TCAD.1985.1270142
    title: Randolph E. Bank, William M. Coughran Jr., Wolfgang Fichtner, Eric H. Grosse, Donald J. Rose and R. Kent Smith, Transient simulation of silicon devices and circuits, IEEE Transactions on Computer-Aided Design 4(4), 436 to 451, 1985
    locator: the composite trapezoidal and BDF2 step, the choice of gamma, and the error estimate for step control
  - paper: "M. E. Hosea and L. F. Shampine, Analysis and implementation of TR-BDF2, Applied Numerical Mathematics 20, 1996"
    title: M. E. Hosea and L. F. Shampine, Analysis and implementation of TR-BDF2, Applied Numerical Mathematics 20, 1996
    locator: the analysis as a one-step method, the error constant, the error estimate and the interpolant
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 5, Sections 5.5 (trapezoidal ringing) and 5.6 (variable time-step methods)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second edition, Springer, 1996
    locator: the chapter on stability of implicit Runge-Kutta methods (A-stability, L-stability and the stability function)
---

TR-BDF2 is an implicit one-step method for stiff differential equations and for the [differential-algebraic equations](/differential-algebraic-equations/) of circuits. Each step of size $h$ does a [trapezoidal](/trapezoidal-rule/) stage from $t_n$ to $t_n + \gamma h$ and then a second-order [backward differentiation](/backward-differentiation-formulas/) stage (BDF2) through $t_n$, $t_n + \gamma h$ and $t_n + h$. With $\gamma = 2 - \sqrt 2$ both stages solve linear systems with the same matrix, and the method is second order and [L-stable](/l-stability/), so it does not ring on stiff components as the trapezoidal rule does. It is a general method of numerical analysis; this page frames it for [transient circuit analysis](/transient-circuit-analysis/) in the circuit simulation half of the logic and circuit simulation sub-area.

## In plain words

A circuit simulator computes voltages and currents at a sequence of time points. Each new point comes from the previous one by a formula that is solved like a resistive circuit. The trapezoidal formula is accurate, but when a part of the circuit reacts much faster than the time step, its answer flips sign from step to step and dies out slowly. The waveform then shows a false oscillation.

TR-BDF2 splits each step in two. The first part uses the trapezoidal formula for a fraction of the step. The second part uses a formula that looks back at both earlier points and damps the fast parts strongly. The fraction is chosen so that both parts need the same matrix, so the extra part costs little. The method stays as accurate as the trapezoidal formula, and fast parts die out at once instead of ringing.

## The problem

Integrate the circuit equations of [modified nodal analysis](/modified-nodal-analysis/) in charge form,

$$f(x) + \frac{d}{dt} q(x) = u(t), \qquad x(t_0) = x_0,$$

from $t_0$ to $t_{\text{end}}$, where $x$ holds node voltages and branch currents, $f$ the resistive currents and branch laws, $q$ the charges and fluxes, and $u$ the sources. Write $G(x) = \partial f/\partial x$ and $C(x) = \partial q/\partial x$. $C$ is usually singular, so the system is a DAE, and the time constants differ by many orders of magnitude, so it is a [stiff problem](/stiff-ode-problem/). The output is a sequence of time points and solution values whose local error is below a tolerance at each step.

## The algorithm

Let $\gamma = 2 - \sqrt 2$, $c = \gamma/2$, $F(t, x) = u(t) - f(x)$ (which is $\dot q$ on a solution), and $k = (-3\gamma^2 + 4\gamma - 2)/(12(2 - \gamma)) \approx -0.0404$.

```pseudo id=main
TR-BDF2(f, q, u, x0, t0, t_end, h, rtol, atol)
L1  t ← t0; x ← x0
L2  while t < t_end do
L3      x_γ ← solve q(x_γ) + c·h·(f(x_γ) − u(t + γh)) = q(x) + c·h·F(t, x) by Newton        ▷ trapezoidal stage
L4      x_new ← solve q(x_new) + c·h·(f(x_new) − u(t + h)) = (q(x_γ) − (1 − γ)²·q(x)) / (γ(2 − γ)) by Newton   ▷ BDF2 stage
L5      E ← 2kh·(F(t, x)/γ − F(t + γh, x_γ)/(γ(1 − γ)) + F(t + h, x_new)/(1 − γ))
L6      r ← max_i |E_i| / (rtol·|q_i(x_new)| + atol)
L7      if r ≤ 1 then t ← t + h; x ← x_new; record (t, x)
L8      h ← h · min(2, max(1/5, 0.9 · r^(−1/3))); h ← min(h, t_end − t)
L9  return the recorded points
```

Lines L3 and L4 each run [Newton's method](/newton-method-for-systems/) with the Jacobian $C(x) + c h\, G(x)$, the same form in both stages. In [companion model](/companion-model/) terms, a capacitor $C$ becomes a conductance $2C/(\gamma h)$ in both stages, with a different current source; for a linear circuit one LU factorization serves both stages and all steps of the same size. Line L5 estimates the local error from the second divided difference of $F$, line L6 scales it, and line L8 picks the next step from the third-order behavior of the local error. When Newton fails to converge, a code cuts $h$ (by 4 in the code of this page) and retries the step. The initial $x_0$ must be consistent, for example the result of a [DC operating point](/dc-operating-point-analysis/), so that the algebraic rows hold at $t_0$.

## Example

**One step on an RC circuit.** A 1 V source charges $C = 1$ F through $R = 1\ \Omega$ from $v = 0$, so $\dot v = 1 - v$, and we take $h = 0.5$. The stage point is $\gamma h = 0.2929$.

| quantity | TR-BDF2 | exact |
|---|---|---|
| $v$ at $t = 0.2929$ (line L3) | $0.29289 / 1.14645 = 0.25548$ | $1 - e^{-0.2929} = 0.25390$ |
| $v$ at $t = 0.5$ (line L4) | $(1.20711 \cdot 0.25548 + 0.14645)/1.14645 = 0.39674$ | $1 - e^{-0.5} = 0.39347$ |
| error estimate $E$ (line L5) | $-0.00385$ | true error, exact minus numerical: $-0.00327$ |

The estimate has the right sign and size at this large step; on $\dot y = -y$ its ratio to the true error is within 10 percent of 1 for $h \le 0.1$, measured by the test of this page.

**Stiff decay.** Let the capacitor start at 1 V and discharge with $RC = 1$ ms, sampled with $h = 10$ ms, so $h\lambda = -10$. The exact value after one step is $e^{-10} \approx 4.5 \times 10^{-5}$.

| step | trapezoidal | TR-BDF2 | backward Euler |
|---|---|---|---|
| 1 | $-0.6667$ | $-0.2036$ | $0.0909$ |
| 2 | $0.4444$ | $0.0414$ | $0.0083$ |
| 3 | $-0.2963$ | $-0.0084$ | $7.5 \times 10^{-4}$ |
| 5 | $-0.1317$ | $-3.5 \times 10^{-4}$ | $6.2 \times 10^{-6}$ |

The trapezoidal values are $(-2/3)^n$: they change sign at each step and are still 13 percent of the start after five steps. TR-BDF2 multiplies by $R(-10) = -0.2036$ per step, and its factor goes to 0 as $h\lambda \to -\infty$. Backward Euler damps even more but is only first order.

## Correctness

TR-BDF2 is a consistent one-step method, so it converges with the order of its local error. With $\gamma = 2 - \sqrt 2$ the stability function is

$$R(z) = \frac{1 + (\sqrt 2 - 1) z}{\left(1 - \tfrac{2 - \sqrt 2}{2} z\right)^2},$$

whose Taylor series agrees with $e^z$ up to $z^2$, with the $z^3$ term off by $(3\sqrt 2 - 4)/6 \approx 0.0404$; so the method is second order. On the imaginary axis $|R(iy)|^2 = (1 + s)/(1 + s/2)^2 \le 1$ with $s = (3 - 2\sqrt 2) y^2$, its only pole is on the positive real axis, and $R(z) \to 0$ at infinity; so it is A-stable and L-stable. The trapezoidal rule has $R_T(z) = (1 + z/2)/(1 - z/2) \to -1$, so it is [A-stable](/a-stability/) but not L-stable. The derivations, the second order on smooth ODEs and the error estimate are in [the correctness proof](proofs/correctness.md). Second order for index-1 DAEs is shown by Bank et al. and Hosea and Shampine, and is cited, not proved there.

## Complexity

Each accepted step costs two nonlinear solves, each with $K$ Newton iterations, and each iteration costs one evaluation of the device models and one sparse LU solve, for example with [KLU](/klu-solver/). The total is $O(N K T)$ for $N$ steps, where $T$ is the cost of one factor and solve; rejected steps add to $N$. For a linear circuit with a fixed step, one factorization serves the whole run, and each stage costs only a forward and back substitution. The number of steps for a given tolerance grows like $\text{tol}^{-1/3}$, the rate of a method whose local error is $O(h^3)$. Measured on $\dot v = \sin 3t - v$ over $[0, 4]$ (atol $10^{-8}$, the code of this page):

| rtol | accepted steps | rejected steps | max error |
|---|---|---|---|
| $10^{-3}$ | 68 | 23 | $9.2 \times 10^{-4}$ |
| $10^{-4}$ | 131 | 31 | $2.1 \times 10^{-4}$ |
| $10^{-5}$ | 261 | 23 | $4.9 \times 10^{-5}$ |
| $10^{-6}$ | 512 | 8 | $1.1 \times 10^{-5}$ |

The step count roughly doubles per decade of tolerance, close to $10^{1/3} \approx 2.15$. The error is a global error, so it is larger than the per-step tolerance. These are toy measurements, not benchmark results.

## Properties

- **Second order and L-stable.** No method of the BDF family above order 2 is A-stable, and the trapezoidal rule is not L-stable; TR-BDF2 has both properties at order 2.
- **One-step.** It needs only $x_n$ to start a step, so a change of step size or a restart after a breakpoint (a corner of a source waveform) costs nothing extra, unlike variable-step BDF2.
- **One matrix per step.** With $\gamma = 2 - \sqrt 2$ the stages share the Newton matrix form $C + (\gamma h/2) G$.
- **Measured order.** With fixed steps, the error at $t = 1$ on the RC circuit above falls from $1.50 \times 10^{-4}$ ($h = 0.1$) to $3.74 \times 10^{-5}$, $9.32 \times 10^{-6}$ and $2.33 \times 10^{-6}$ as $h$ halves: ratios 4.02, 4.01, 4.00. On a series RLC circuit ($R = 1\ \Omega$, $L = 1$ H, $C = 1$ F, a 1 V step, full MNA with a singular $C$ matrix, max error of the capacitor voltage over $[0, 5]$) the ratios are 4.02, 4.01, 4.00 from $h = 0.1$. These are measurements of the code of this page against the closed-form solutions.
- **Smaller error constant than the trapezoidal rule per step of size h.** On the RC circuit at $h = 0.1$ the error is $1.50 \times 10^{-4}$, about half that of the trapezoidal rule at the same $h$ reported on the [companion model](/companion-model/) page, but TR-BDF2 does two stage solves per step.

## Variants and improvements

- **Other values of $\gamma$.** Any $\gamma \in (0, 1)$ gives a second-order method, and the stability function still tends to 0 at infinity; only $\gamma = 2 - \sqrt 2$ makes the two matrices equal, which is why it is the standard choice.
- **As a Runge-Kutta method.** TR-BDF2 is a three-stage [implicit Runge-Kutta method](/implicit-runge-kutta-methods/) with an explicit first stage and equal diagonal entries (an ESDIRK). This view gives a cheap embedded error estimate and a smooth interpolant between points, both used by Hosea and Shampine, and their method is the solver ode23tb of MATLAB.
- **Other L-stable methods.** [Radau IIA](/radau-iia-methods/) methods are L-stable of order 3 and above but need larger linear systems; [backward Euler](/backward-euler-method/) is L-stable of order 1.

## When to use it

Use TR-BDF2 for transient simulation of stiff circuits where trapezoidal ringing would show, such as circuits with switches, ideal sources driving capacitors, or very fast parasitic time constants, and where second order is accurate enough. Use the trapezoidal rule when the circuit is not stiff relative to the step and the lack of numerical damping is wanted, for example for oscillators, where the damping of BDF methods reduces the amplitude. Use higher-order BDF or Radau methods for very tight tolerances.

## Pitfalls

- **Inconsistent start.** The trapezoidal stage carries the residual of the algebraic rows at $t_n$ into the next stage. Start from a consistent DC operating point, or after a breakpoint take a backward Euler step first.
- **Error control on algebraic variables.** The estimate of line L5 is for $q$, which is zero for purely algebraic rows. The node voltages without capacitance are controlled only through the rows they couple to; check the result on those nodes.
- **Damping of true oscillations.** L-stability damps components with $|h\lambda| \gg 1$, including real fast oscillations sampled with too large a step. The method then reports a smooth waveform that is wrong.
- **Absolute tolerance in the wrong units.** The estimate is in charge and flux units. An absolute tolerance chosen for volts can be orders of magnitude too loose, as with an $\text{atol}$ of $10^{-6}$ C on a $100\ \mu$F node, which allows 10 mV per step.

## Implementations

## History

Bank, Coughran, Fichtner, Grosse, Rose and Smith introduced TR-BDF2 in 1985, in a paper on the transient simulation of silicon devices and circuits, to remove the ringing of the trapezoidal rule while keeping one matrix per step. Hosea and Shampine (1996) analysed it as a one-step Runge-Kutta method, and derived its error constant, an embedded error estimate and an interpolant. Najm's textbook presents trapezoidal ringing and variable-step methods in the circuit setting.

## References
