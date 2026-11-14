---
tag: BP56ZV
kind: technique
slug: pseudo-transient-analysis
name: Pseudo-transient analysis
aliases:
- PTA
- pseudo-transient continuation
area: eda/logic-and-circuit-simulation
level: advanced
summary: Finds a DC operating point by adding artificial capacitors and inductors and running a transient simulation until the circuit settles at a steady state.
prereqs: [dc-operating-point-analysis, companion-model, backward-euler-method]
see_also: [gmin-stepping, source-stepping, junction-voltage-limiting, transient-circuit-analysis, homotopy-continuation, newton-method-for-systems, tellegen-theorem, stiff-ode-problem]
sources:
  - paper: doi:10.1137/S0036142996304796
    title: C. T. Kelley and David E. Keyes, Convergence analysis of pseudo-transient continuation, SIAM Journal on Numerical Analysis 35(2), 508 to 523, 1998
    locator: the method with one Newton step per time step and the switched evolution relaxation rule for the step, and the theorem on its global convergence to a stable steady state and its local quadratic convergence
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 4, Section 4.4.5 (pseudo-transient analysis) and Section 4.4.6 (the justification of the continuation methods)
  - book: isbn:9780898714616
    title: James M. Ortega and Werner C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000 (first published 1970)
    locator: Section 6.4, the uniform monotonicity theorem
---

Pseudo-transient analysis finds the [DC operating point](/dc-operating-point-analysis/) of a circuit by turning it into a time problem. It adds a capacitor from every node to ground and an inductor in series with every voltage source, starts the resulting circuit from a chosen state, and integrates it in time with an implicit method until nothing changes; the state it settles in is an operating point of the original circuit, because the added elements carry no current and drop no voltage at rest. It is a technique of the circuit simulation half of the logic and circuit simulation sub-area, the circuit form of a method for general nonlinear equations that Kelley and Keyes analysed in 1998.

## In plain words

A real circuit always finds its resting state: switch it on and wait. The voltages move, slowly or quickly, and then stop. Pseudo-transient analysis copies this.

It adds small capacitors at every connection point, so that no voltage can jump, and small coils in series with the supplies, so that no supply current can jump. Then it simulates the circuit over time, in steps. Early steps are short and safe. As the circuit calms down, the steps get longer and longer, until one step covers so much time that it lands on the final state.

The added parts change how the circuit moves, but not where it stops, because at rest a capacitor carries no current and a coil has no voltage.

## When it applies

Use it for the DC operating point when Newton, [gmin stepping](/gmin-stepping/) and [source stepping](/source-stepping/) fail, and in particular for circuits whose operating point lies past a turning point of those homotopy paths, which time integration does not see. It needs the circuit with its added elements to settle: the state must converge to a stable equilibrium. Oscillators, and circuits that the added elements turn into oscillators, never settle. It costs more than the stepping methods: Najm reports it as about 2 to 10 times slower than Newton.

## The template

Write the operating point equations as $F(x) = 0$ with $x = (e, j)$. With capacitors $c_k$ from node $k$ to ground and inductors $\ell_m$ in series with voltage source $m$, the circuit is

$$c_k\, \dot e_k = -F_k(x), \qquad \ell_m\, \dot j_m = F_{n+m}(x),$$

KCL with the capacitor current added, and the law of each source with the inductor voltage added (with the sign of the MNA rows). Write this as $M \dot x = -F(x)$ with $M = \operatorname{diag}(c_1, \ldots, c_n, -\ell_1, \ldots, -\ell_m)$. A backward Euler step of length $h$, which is a solve of the circuit with [companion models](/companion-model/), is

$$\frac{1}{h} M (x' - x) + F(x') = 0.$$

```pseudo id=main
PSEUDO-TRANSIENT(F, M, x_0, h_0)
L1  x ← x_0; h ← h_0
L2  repeat
L3      x' ← solution of M (x' − x) / h + F(x') = 0, by Newton started at x    ▷ hole: the corrector
L4      if the corrector failed then h ← h / 4
L5      else
L6          h ← h · ‖F(x)‖ / ‖F(x')‖                                ▷ hole: the step rule
L7          x ← x'
L8  until ‖F(x)‖ ≤ tolerance
L9  return x
```

Line L6 is the switched evolution relaxation rule that Kelley and Keyes analyse: the step grows in proportion to the fall of the residual. In the version they analyse, line L3 takes exactly one Newton iteration; circuit simulators usually iterate to convergence at each time point, as in [transient circuit analysis](/transient-circuit-analysis/).

**The equilibria are the operating points.** $M \dot x = -F(x)$ has $\dot x = 0$ exactly where $F(x) = 0$, since $M$ is nonsingular. So if the run settles, its limit solves the original circuit, whatever capacitors and inductors were added. The added elements change the path and the speed, and they decide which operating point is reached when there are several, but not the set of possible end points.

**One step is a gmin circuit centred at the last state.** At a node, the companion model of $c_k$ is a conductance $c_k/h$ in series with a source equal to the old voltage $e_k$. So a step solves the [gmin](/gmin-stepping/) circuit with conductance $c_k/h$, tied to the previous state instead of to ground. For small $h$ this conductance dominates and the step is easy; as $h \to \infty$ the step becomes a plain Newton solve of $F = 0$. Read this way, the method is a homotopy that moves both the conductance and its centre.

**Theorem (monotone circuits converge from any start, for any steps).** Take a circuit without voltage sources whose devices are two-terminal with laws that are uniformly monotone with constant $\mu > 0$, $(e - e')^{\mathsf T}(F(e) - F(e')) \ge \mu \|e - e'\|^2$, and equal capacitors $c$ at every node. Then each backward Euler step has exactly one solution, and for any sequence of steps $h_k > 0$,

$$\|e_{k+1} - e^\ast\| \le \frac{\|e_k - e^\ast\|}{1 + h_k \mu / c},$$

where $e^\ast$ is the unique operating point.

*Proof.* The step equation $(c/h)(e' - e) + F(e') = 0$ is a uniformly monotone equation in $e'$ with constant $c/h + \mu$, so it has exactly one solution by the uniform monotonicity theorem (Ortega and Rheinboldt, Section 6.4); with $h \to \infty$ the same theorem gives the unique $e^\ast$. Let $w = e_{k+1} - e^\ast$ and $d = e_k - e^\ast$. Subtract $F(e^\ast) = 0$ from the step equation and multiply by $w^{\mathsf T}$: $(c/h_k)\, w^{\mathsf T}(w - d) + w^{\mathsf T}(F(e_{k+1}) - F(e^\ast)) = 0$. The second term is at least $\mu \|w\|^2$, so $(c/h_k + \mu)\|w\|^2 \le (c/h_k)\, w^{\mathsf T} d \le (c/h_k)\|w\|\|d\|$. $\blacksquare$

The same argument with the exact time derivative gives $\tfrac{d}{dt} \tfrac{c}{2}\|e - e^\ast\|^2 \le -\mu\|e - e^\ast\|^2$: the true dynamics converge exponentially. For monotone circuits the method is therefore safe with any step rule, and growing steps make it converge faster than linearly. For circuits that are not monotone nothing like this holds in general.

**What is cited and what is measured.** Kelley and Keyes prove, for the method with one Newton iteration per step and the rule of line L6, that the iterates converge to a steady state if the solution of the differential equation from $x_0$ converges to a stable steady state, $h_0$ is small enough, and the Jacobian satisfies a stability condition along the path; the final convergence is quadratic once $h$ is large. We cite this result and do not prove it. The table below is measured. A source $E$ drives a diode ($I_s = 10^{-14}$ A, $V_t = 25.852$ mV) through $1\ \text{k}\Omega$ with one capacitor at the diode node, one Newton iteration per step, the rule of line L6, and a restart with a 4 times smaller step after an overflow. It counts the steps until the KCL residual is below $10^{-15}$ A, from $e = 0$:

| first companion conductance $c/h_0$ | 1 S | 0.1 S | 0.01 S |
|---|---|---|---|
| $E = 5$ V | 145 | 18 | 16 |
| $E = 20$ V | 42 | 11 | 49 |
| $E = 100$ V | 13 | 15 | 329 |

All runs reach the operating points 0.692544 V, 0.731273 V and 0.773643 V, where plain Newton from zero overflows for 20 V and 100 V. The counts depend strongly on the first step, in both directions: a large first conductance moves slowly at the start, and a small one lets the first step put the diode far up its exponential, from where the iteration needs many steps to come down. Choosing $h_0$ is the hard part of the method in practice.

## Classic examples

- DC operating point analysis in circuit simulators, as a fallback after [gmin stepping](/gmin-stepping/) and [source stepping](/source-stepping/), with the supplies sometimes ramped in time as well.
- Steady flows in computational fluid dynamics, found by marching the flow equations in time with growing steps; this is the setting of Kelley and Keyes's analysis.
- Power-up simulation of a full chip: a [transient analysis](/transient-circuit-analysis/) from zero with ramped supplies, which is the physical form of the same idea and settles memory cells and latches into the states that power-up produces.

## Variations

- **Capacitors only.** Add capacitors at the nodes and leave voltage sources algebraic; the system is then a differential-algebraic equation of index 1 when no voltage-source loop exists.
- **Different element values.** Scale each $c_k$ to the conductance at the node, so that all nodes settle at similar rates.
- **Ramped supplies.** Raise the supplies in time during the run; this combines the method with [source stepping](/source-stepping/).
- **Other integrators.** Backward Euler damps fast modes and suits the method; the trapezoidal rule can ring around the equilibrium, which delays the stop test.
- **One Newton iteration per step.** Take one Newton iteration per step, as Kelley and Keyes do, instead of solving each time point fully; this saves work when the path is followed loosely.

## Pitfalls

- **Oscillation.** A ring oscillator has an operating point, but it is unstable and the transient never settles. The added capacitors and inductors can also create oscillation in a circuit that has none.
- **Unstable operating points.** The true dynamics converge only to stable equilibria, such as the two outer states of a latch. An operating point that is unstable, such as the middle state of the tunnel-diode circuit of [DC operating point analysis](/dc-operating-point-analysis/), is not found except by chance with large steps.
- **The first step.** A first step that is too large lets the method behave like plain Newton, with its overflow; one that is too small wastes steps, as the table shows.
- **Stopping too early.** A slow mode can look settled. The stop test must use the residual $\|F(x)\|$ of the original circuit, not the change between steps alone.

## Exercises

1. For one node with a current source $I$ and a linear resistor $R$, write the backward Euler step with capacitor $c$ and show that the error is multiplied by $1/(1 + h/(Rc))$ at every step.
2. Show that line L6 with one Newton iteration per step and $h \to \infty$ becomes Newton's method on $F$.
3. For the tunnel-diode law $g(v) = v^3 - 6v^2 + 10v$ driven by 6 V through $1\ \Omega$ with a capacitor across the element, find for which starting voltages the transient settles at $v = 1$ and for which at $v = 3$.
4. Give a circuit with a unique operating point in which pseudo-transient analysis cannot converge from any start except the operating point itself.

## References
