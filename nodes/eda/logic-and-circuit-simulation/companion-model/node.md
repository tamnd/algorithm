---
tag: JH4KPG
kind: technique
slug: companion-model
name: Companion model
aliases:
- discretized companion model
- associated discrete circuit
area: eda/logic-and-circuit-simulation
level: core
summary: Replace each capacitor or inductor, at one step of an implicit integration formula, by a conductance and a current source, so a transient step becomes a resistive circuit solve.
prereqs: [modified-nodal-analysis, backward-euler-method, trapezoidal-rule]
see_also: [transient-circuit-analysis, crank-nicolson-method, backward-differentiation-formulas, local-truncation-error, a-stability, l-stability, stiff-ode-problem, tellegen-theorem]
sources:
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 2, Section 2.5.1 (dynamic element stamps), and Chapter 5 (solution of differential circuit equations)
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the chapter on transient analysis (implicit integration of capacitors and inductors, trapezoidal and Gear formulas, truncation error and time step control)
  - book: "Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits: Algorithms and Computational Techniques, Prentice-Hall, 1975"
    title: Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits, Prentice-Hall, 1975
    locator: the chapters on numerical integration of circuit equations (associated discrete circuit models of capacitors and inductors)
  - book: isbn:9780070501690
    title: Lawrence T. Pillage, Ronald A. Rohrer and Chandramouli Visweswariah, Electronic Circuit and System Simulation Methods, McGraw-Hill, 1994
    locator: the chapters on numerical integration and companion models
---

A companion model replaces a capacitor or an inductor, for one time step of an implicit integration formula, by a conductance $G$ in parallel with a current source $J$, so that the element current at the new time point is $i_{n+1} = G\, v_{n+1} + J$. With every dynamic element replaced, one step of transient simulation becomes one solve of a resistive circuit by [modified nodal analysis](/modified-nodal-analysis/), with $G$ depending on the step $h$ and $J$ on the past values. The technique belongs to the circuit simulation half of the logic and circuit simulation sub-area. For a capacitor $C$, [backward Euler](/backward-euler-method/) gives $G = C/h$ and the [trapezoidal rule](/trapezoidal-rule/) gives $G = 2C/h$.

## In plain words

A capacitor's current depends on how fast its voltage changes, so a circuit with capacitors gives differential equations, not plain equations. A simulator walks through time in small steps instead.

Over one short step, the capacitor behaves like a resistor plus a small battery-like source. The resistor part says that a larger jump in voltage needs a larger current. The source part remembers where the voltage was at the end of the last step. An inductor gets the same treatment with the roles of voltage and current swapped.

Swap every capacitor and inductor for its stand-in, and the circuit at the end of the step has only resistors and sources. The simulator solves it like a DC circuit, updates what each stand-in remembers, and moves on to the next step.

## When it applies

The technique applies to any lumped circuit with capacitors and inductors, integrated by an implicit linear multistep formula: backward Euler, the trapezoidal rule, [backward differentiation formulas](/backward-differentiation-formulas/) (Gear's methods, as in SPICE2) and the two stages of [TR-BDF2](/tr-bdf2/). Each formula gives its own $G$ and $J$. Circuit equations are stiff, with time constants that differ by many orders of magnitude, so explicit formulas would need tiny steps; this is why simulators use implicit ones and need companion models ([stiff ODE problem](/stiff-ode-problem/)). Nonlinear capacitors use the same idea on the charge $q(v)$, inside each Newton iteration of the step. The full time loop with step control and Newton iterations is [transient circuit analysis](/transient-circuit-analysis/).

## The template

**Convention.** An element from node $p$ to node $q$ has the voltage $v = e_p - e_q$ and the current $i$ counted from $p$ through the element to $q$. A companion model $(G, J)$ is a conductance $G$ from $p$ to $q$ in parallel with a current source $J$ from $p$ through it to $q$, so the stamps of MNA apply: $G$ in the matrix, $-J$ at row $p$ and $+J$ at row $q$ of the right side.

```pseudo id=main
TRANSIENT(netlist, e_0, h, K, method)
L1  for each capacitor and inductor el do set (v_el, i_el) from e_0 and the initial currents
L2  for k ← 1 to K do
L3      for each capacitor and inductor el do (G_el, J_el) ← COMPANION(el, method, h, v_el, i_el)
L4      M ← stamps of the resistors and of every G_el; factor M once for each (h, method)
L5      z ← stamps of the sources at t_k = k h and of every J_el
L6      e_k ← SOLVE(M, z)
L7      for each capacitor and inductor el do v_el ← e_p − e_q; i_el ← G_el v_el + J_el
L8  return e_0, e_1, ..., e_K
```

The holes are COMPANION, which holds the integration formula, and SOLVE. Line L4 factors $M$ only when $h$ or the method changes, because for a linear circuit the conductances depend on nothing else; then each step costs one forward and one back substitution. A production simulator adds a Newton loop around lines L3 to L7 for nonlinear devices and a step size control after line L7.

**The models and why they are exact.** A capacitor obeys $i = C\, dv/dt$ and an inductor $v = L\, di/dt$. Apply each formula to these laws and solve for $i_{n+1}$:

| Element and formula | Discrete law | $G$ | $J$ |
|---|---|---|---|
| capacitor, backward Euler | $C (v_{n+1} - v_n)/h = i_{n+1}$ | $C/h$ | $-(C/h)\, v_n$ |
| capacitor, trapezoidal | $C (v_{n+1} - v_n)/h = (i_{n+1} + i_n)/2$ | $2C/h$ | $-(2C/h)\, v_n - i_n$ |
| inductor, backward Euler | $L (i_{n+1} - i_n)/h = v_{n+1}$ | $h/L$ | $i_n$ |
| inductor, trapezoidal | $L (i_{n+1} - i_n)/h = (v_{n+1} + v_n)/2$ | $h/(2L)$ | $i_n + (h/2L)\, v_n$ |

Each row is the discrete law rearranged, for example $C(v_{n+1} - v_n)/h = i_{n+1}$ is $i_{n+1} = (C/h) v_{n+1} - (C/h) v_n$. So a source $J = -(C/h) v_n$ from $p$ to $q$ is a source of $C v_n / h$ that drives current into node $p$, in parallel with $G = C/h$. Every other element keeps its law, and KCL and KVL are unchanged, so the solution of the resistive circuit at step $n + 1$ is exactly the solution of the circuit equations discretized by the formula. The companion model adds no error of its own; all the error is the error of the integration formula.

**Exact solution of the RC circuit.** Let a source $E$ with a series resistor $R$ charge a capacitor $C$ from $v_0 = 0$, and let $\tau = RC$ and $w_k = E - v_k$. The exact solution is $v(t) = E(1 - e^{-t/\tau})$. With backward Euler, KCL at the capacitor node is $C(v_{k+1} - v_k)/h = (E - v_{k+1})/R$, that is $(w_k - w_{k+1})\tau/h = w_{k+1}$, so $w_{k+1} = \rho\, w_k$ with $\rho = 1/(1 + h/\tau)$. With the trapezoidal rule and the consistent start $i_0 = E/R$, $(w_k - w_{k+1})\tau/h = (w_{k+1} + w_k)/2$, so $\rho = (1 - h/2\tau)/(1 + h/2\tau)$. In both cases $v_k = E(1 - \rho^k)$ exactly.

**The order of the error.** At a fixed time $t = kh$ the error is $v_k - v(t) = E(e^{-t/\tau} - \rho^k)$ with $\rho^k = e^{k \ln \rho}$. For backward Euler $\ln \rho = -\ln(1 + h/\tau) = -h/\tau + h^2/(2\tau^2) + O(h^3)$, so $k \ln \rho = -t/\tau + t h/(2\tau^2) + O(h^2)$ and the error is $-E e^{-t/\tau}\, t h / (2\tau^2) + O(h^2)$: first order in $h$. For the trapezoidal rule, with $x = h/(2\tau)$, $\ln\rho = \ln(1 - x) - \ln(1 + x) = -2x - 2x^3/3 + O(x^5) = -h/\tau - h^3/(12\tau^3) + O(h^5)$, so the error is $E e^{-t/\tau}\, t h^2 / (12\tau^3) + O(h^4)$: second order. These match the local truncation errors of the two formulas, $-\tfrac{h^2}{2} x''$ for backward Euler and $-\tfrac{h^3}{12} x'''$ for the trapezoidal rule per step ([local truncation error](/local-truncation-error/)).

**Worked example.** Take $E = 1$ V, $R = 1\ \Omega$, $C = 1$ F and $h = 0.1$ s, with the source in Norton form, 1 A into the node in parallel with $1\ \Omega$. Backward Euler: $G = 10$, $J = 0$, so $(1 + 10)\, v_1 = 1$ and $v_1 = 1/11 \approx 0.09091$. Trapezoidal with $i_0 = 1$ A: $G = 20$, $J = -20 \cdot 0 - 1 = -1$, so the source drives 1 A into the node and $(1 + 20)\, v_1 = 1 + 1$, $v_1 = 2/21 \approx 0.09524$. The exact value is $1 - e^{-0.1} \approx 0.09516$. Over $0 \le t \le 1$ the largest errors are:

| steps in $[0, 1]$ | 10 | 20 | 40 | 80 |
|---|---|---|---|---|
| backward Euler | $1.766 \times 10^{-2}$ | $9.010 \times 10^{-3}$ | $4.551 \times 10^{-3}$ | $2.287 \times 10^{-3}$ |
| trapezoidal | $3.069 \times 10^{-4}$ | $7.666 \times 10^{-5}$ | $1.916 \times 10^{-5}$ | $4.790 \times 10^{-6}$ |

Halving $h$ halves the backward Euler error and divides the trapezoidal error by 4. The leading term $e^{-1} h^2/12$ of the formula above gives $3.066 \times 10^{-4}$ for $h = 0.1$.

**Energy of a lossless network.** For a network of capacitors and inductors only, the trapezoidal rule keeps the stored energy $\sum \tfrac12 C v^2 + \sum \tfrac12 L i^2$ exactly, and backward Euler lowers it at every step that changes the state. *Proof.* With the trapezoidal rule, the averages $\bar v = (v_{n+1} + v_n)/2$ and $\bar i = (i_{n+1} + i_n)/2$ satisfy KVL and KCL, because both laws are linear. By [Tellegen's theorem](/tellegen-theorem/), $\sum_j \bar v_j \bar i_j = 0$. For a capacitor, $\bar i = C(v_{n+1} - v_n)/h$, so $\bar v \bar i = C(v_{n+1}^2 - v_n^2)/(2h)$; for an inductor, $\bar v = L(i_{n+1} - i_n)/h$, so $\bar v \bar i = L(i_{n+1}^2 - i_n^2)/(2h)$. The sum of these terms is the change of energy divided by $h$, so the change is zero. With backward Euler, Tellegen's theorem on $(v_{n+1}, i_{n+1})$ gives $\sum C v_{n+1}(v_{n+1} - v_n) + \sum L i_{n+1}(i_{n+1} - i_n) = 0$, and $a(a - b) = \tfrac12(a^2 - b^2) + \tfrac12(a - b)^2$ turns this into: the energy drops by $\tfrac12 \sum C (v_{n+1} - v_n)^2 + \tfrac12 \sum L (i_{n+1} - i_n)^2$. $\blacksquare$

**Cost.** For a linear circuit with $N$ MNA unknowns, $K$ steps and a fixed $h$, the run costs one LU factorization plus $K$ pairs of triangular solves, $\Theta(N^3 + K N^2)$ with dense LU, and lines L3, L5 and L7 cost time linear in the number of elements per step. The code of this page does exactly this, with exact fractions or floats.

## Classic examples

- [Transient circuit analysis](/transient-circuit-analysis/) in SPICE: trapezoidal and Gear companion models with a step chosen from the truncation error estimate.
- [TR-BDF2](/tr-bdf2/): a trapezoidal stage followed by a second-order BDF stage, each a companion model solve, which damps the ringing of the plain trapezoidal rule.
- [Power grid analysis](/power-grid-analysis/) in time: with a fixed step, the grid matrix with its companion conductances is factored once and reused for thousands of steps.
- The [Crank-Nicolson method](/crank-nicolson-method/) for a discretized heat equation is the trapezoidal rule on an RC network, and its matrix is the MNA matrix with the companion conductances $2C/h$.

## Variations

- **Gear (BDF) models.** The second-order backward differentiation formula $\tfrac{3}{2} v_{n+1} - 2 v_n + \tfrac12 v_{n-1} = h\, i_{n+1}/C$ gives $G = 3C/(2h)$ and $J = -(C/h)(2 v_n - \tfrac12 v_{n-1})$. Higher orders use more past points.
- **Charge form.** For a nonlinear capacitor with charge $q(v)$, the discrete law $i_{n+1} = (q(v_{n+1}) - q(v_n))/h$ is linearized at each Newton iterate $v^{(m)}$, which gives $G = q'(v^{(m)})/h$. Writing the law in charge conserves charge exactly, while a law in $C(v)\, dv/dt$ does not.
- **Thevenin form.** A voltage source in series with a resistance gives the same model and suits inductors in a formulation that keeps their currents as unknowns.
- **Variable step.** When $h$ changes, $G$ changes and $M$ must be factored again. The step is chosen so that an estimate of the local truncation error, for example from divided differences of the last few solutions as in SPICE2, stays below a tolerance ([adaptive step size control](/adaptive-step-size-control/)).

## Pitfalls

- **Trapezoidal ringing.** For a fast mode with $h \gg \tau$, the trapezoidal factor $\rho = (1 - h/2\tau)/(1 + h/2\tau)$ is close to $-1$, so the error flips sign at every step and decays very slowly. The rule is [A-stable](/a-stability/) but not [L-stable](/l-stability/). Backward Euler has $\rho \to 0$ and damps such modes, which is why simulators take a backward Euler step after a breakpoint or switch to Gear's methods.
- **The trapezoidal rule needs the current.** The companion source of the trapezoidal rule uses $i_n$, so the run needs consistent initial capacitor currents. SPICE avoids the problem by taking the first step with backward Euler, which keeps the global order 2, since one step of local error $O(h^2)$ adds only $O(h^2)$.
- **Backward Euler adds loss.** In a lossless LC circuit it lowers the energy at every step, as proved above, so an oscillator simulated with backward Euler decays although the real one does not.
- **Breakpoints.** A source with a corner, such as a pulse edge, breaks the smoothness that the error order needs. Simulators place a time point at each corner.
- **Refactoring.** A change of $h$ changes every companion conductance, so the matrix must be factored again; changing the step on every step loses the saving of a fixed step.

## Exercises

1. Derive the BDF2 capacitor model of the Variations section, and check that it reduces the RC recurrence to a two-term linear recurrence whose roots give a global error of order $h^2$.
2. Show that backward Euler with the companion model of a capacitor gives $|\rho| < 1$ for every $h > 0$ on the RC circuit, and that $\rho \to 0$ as $h \to \infty$.
3. A capacitor and an inductor in parallel start with $v_0 = 1$ V and $i_0 = 0$. With $C = 1/2$ F, $L = 2$ H and $h = 1/5$ s, compute three trapezoidal steps exactly and check that the energy stays $1/4$ J.
4. Write the trapezoidal model of a capacitor in Thevenin form, and show that it gives the same node voltages as the Norton form.

## References
