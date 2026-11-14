---
tag: 9D84DK
kind: problem
slug: transient-circuit-analysis
name: Transient circuit analysis
aliases:
- transient analysis
- time-domain circuit simulation
area: eda/logic-and-circuit-simulation
level: intro
summary: Compute the waveforms of a nonlinear circuit over time by integrating its differential-algebraic MNA equations with an implicit method and adaptive steps.
prereqs: [modified-nodal-analysis, companion-model, dc-operating-point-analysis, differential-algebraic-equations, stiff-ode-problem]
see_also: [tr-bdf2, trapezoidal-rule, backward-differentiation-formulas, adaptive-step-size-control, iterated-timing-analysis, klu-solver, shooting-newton-steady-state, timing-simulation]
sources:
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the transient analysis of SPICE2 (implicit integration, Newton iteration at each time point, truncation error and time step control)
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 5, solution of differential circuit equations (linear multistep methods, stability, Section 5.5 trapezoidal ringing, Section 5.6 variable time-step methods)
  - book: isbn:9780442011949
    title: Jiri Vlach and Kishore Singhal, Computer Methods for Circuit Analysis and Design, second edition, Van Nostrand Reinhold, 1994
    locator: the chapters on numerical integration and on time-domain analysis of nonlinear networks
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second edition, Springer, 1996
    locator: the chapters on A-stability of multistep methods (the second Dahlquist barrier) and on index-1 and index-2 problems
  - paper: doi:10.1109/TCAD.1985.1270142
    title: Randolph E. Bank, William M. Coughran Jr., Wolfgang Fichtner, Eric H. Grosse, Donald J. Rose and R. Kent Smith, Transient simulation of silicon devices and circuits, IEEE Transactions on Computer-Aided Design 4(4), 436 to 451, 1985
    locator: the TR-BDF2 method, introduced to remove the ringing of the trapezoidal rule
---

Transient circuit analysis is the problem of computing the voltages and currents of a circuit as functions of time, from a known starting state and for given source waveforms. In the circuit simulation half of the logic and circuit simulation sub-area it is the main analysis of a SPICE-type simulator: the circuit is written as the [modified nodal analysis](/modified-nodal-analysis/) system $f(x) + \frac{d}{dt} q(x) = u(t)$, a stiff system of [differential-algebraic equations](/differential-algebraic-equations/), and integrated with an implicit method, a Newton solve at each time point and an adaptive step. The other circuit analyses are defined relative to it: [DC operating point](/dc-operating-point-analysis/) analysis gives its start, [AC analysis](/ac-small-signal-analysis/) is its small-signal limit, and periodic steady state analyses look for its periodic solutions directly.

## In plain words

A circuit with capacitors and inductors does not jump to its final state; its voltages change over time as the capacitors charge and the currents in the inductors build up. Transient analysis asks how. You give it the circuit, the signals at the inputs over time, and the state at the start. It gives back the waveform of every node voltage and every source current over the time you asked for.

The simulator gets there by taking small steps in time. At each step it solves a circuit without capacitors or inductors, in which each of them is replaced by a resistor and a source that remember the past. It makes the step shorter when the waveforms change fast and longer when they change slowly, so that the error at each step stays below a limit you set.

## Definition

**Input.** A circuit, given as a netlist of elements with their models; source waveforms $u(t)$ for $t \in [t_0, t_{\text{end}}]$; a consistent initial state $x_0$; and tolerances (relative, absolute in volts and amperes, and in charge).

**Equations.** With the MNA unknowns $x = (e_1, \ldots, e_n, j_1, \ldots, j_m)$, node voltages first and then the currents of voltage sources and inductors,

$$f(x) + \frac{d}{dt} q(x) = u(t), \qquad x(t_0) = x_0,$$

where $f$ holds the currents of resistive elements and the branch laws, $q$ the capacitor charges and inductor fluxes, and $u$ the independent sources. For a linear circuit this is $Gx + C\dot x = u(t)$. The matrix $C = \partial q/\partial x$ is usually singular: rows of nodes without a capacitance and rows of voltage sources have no derivative. So the system is a DAE, not an ODE.

**Consistency.** The algebraic rows must hold at $t_0$. The usual $x_0$ is the DC operating point at $t = t_0$, which solves $f(x) = u(t_0)$ and so makes all derivatives zero; a simulator option can instead start from given capacitor voltages and inductor currents and solve only the algebraic rows.

**Output.** Time points $t_0 < t_1 < \cdots < t_N = t_{\text{end}}$ and values $x_k \approx x(t_k)$ such that the estimated local error of each step is below the tolerance, plus the waveforms obtained by interpolation.

**Well-posedness.** For a circuit with positive resistances, capacitances and inductances and no degenerate loops or cutsets, the DAE has differentiation index 1 and a unique solution for consistent initial values. A loop made only of capacitors and voltage sources, or a cutset made only of inductors and current sources, raises the [index](/differentiation-index/) to 2; then some variables depend on derivatives of the sources, and some integration methods lose order or fail on the corresponding components. The MNA page notes that the index is 1 or 2 for the usual elements; Hairer and Wanner treat the numerical consequences of index 2.

## Variants

- **Linear transient analysis.** RC and RLC networks, for example interconnect and power grids. Each step solves a linear system, and with a fixed step one LU factorization serves the whole run.
- **Nonlinear transient analysis.** Transistors and diodes make $f$ and $q$ nonlinear. Each step solves a nonlinear system by Newton's method, often with [junction voltage limiting](/junction-voltage-limiting/).
- **Timing simulation.** Digital circuits analysed with simplified device models and relaxation methods that exploit latency and one-way coupling: [timing simulation](/timing-simulation/), [iterated timing analysis](/iterated-timing-analysis/) and waveform relaxation, which is the [Picard iteration](/picard-iteration/) on subcircuits.
- **Mixed-mode simulation.** Some blocks at the transistor level and others at the logic level, coupled by events: [mixed-mode simulation](/mixed-mode-simulation/).
- **Periodic steady state.** For a circuit driven by a periodic source, find the periodic solution without integrating through the start-up transient: [shooting Newton](/shooting-newton-steady-state/) and [harmonic balance](/harmonic-balance-analysis/).

## Examples

**RC charging.** A source $E$ charges a capacitor $C$ through a resistor $R$ from $v(0) = 0$. With $\tau = RC$ the equation is $C\dot v + v/R = E/R$ and the solution is $v(t) = E(1 - e^{-t/\tau})$. The [companion model](/companion-model/) page traces backward Euler and the trapezoidal rule on this circuit and measures first and second order.

**Trapezoidal ringing on one pole.** Let the capacitor start at $v_0$ with $E = 0$, so $\dot v = \lambda v$ with $\lambda = -1/\tau$. One step of size $h$ of the [trapezoidal rule](/trapezoidal-rule/) gives $v_{k+1} = R_T(h\lambda)\, v_k$ with

$$R_T(z) = \frac{1 + z/2}{1 - z/2}.$$

*The rule is A-stable.* For $\operatorname{Re} z \le 0$, with $w = z/2$, $|1 + w|^2 - |1 - w|^2 = 4\operatorname{Re} w \le 0$, so $|R_T(z)| \le 1$: no decaying circuit gives a growing numerical solution.

*The rule is not L-stable.* As $z \to -\infty$, $R_T(z) \to -1$. Take $\tau = 1$ ms and $h = 10$ ms, so $z = -10$: $R_T = (1 - 5)/(1 + 5) = -2/3$. The numerical values are $v_k = (-2/3)^k v_0$, that is $-0.667, 0.444, -0.296, 0.198, -0.132$ times $v_0$, while the exact values are $e^{-10k} v_0$, below $5 \times 10^{-5} v_0$ after one step. The computed voltage changes sign at every step and decays slowly. This is trapezoidal ringing. It appears whenever a time constant of the circuit is much smaller than the step, which happens all the time in circuits with parasitic capacitances, because the step follows the slow waveforms. [Backward Euler](/backward-euler-method/) gives $1/(1 - z) = 1/11$ per step and [TR-BDF2](/tr-bdf2/) gives $-0.2036$ per step, and both factors go to 0 as $z \to -\infty$.

**A series RLC step.** A 1 V step drives $R = 1\ \Omega$, $L = 1$ H and $C = 1$ F in series. With $\alpha = R/(2L) = 1/2$ and $\omega_d = \sqrt{1/(LC) - \alpha^2} = \sqrt{3}/2$, the capacitor voltage is $1 - e^{-\alpha t}(\cos \omega_d t + (\alpha/\omega_d) \sin \omega_d t)$. The MNA unknowns are three node voltages, the source current and the inductor current; $C$ has rank 2 of 5. The TR-BDF2 page measures second-order convergence of the capacitor voltage on this circuit.

## Known algorithms

- **The SPICE direct method.** At each time point, replace each capacitor and inductor by its companion model for an implicit linear multistep formula, solve the resulting nonlinear resistive circuit by [Newton's method](/newton-method-for-systems/) with a sparse LU solver ([Markowitz pivoting](/markowitz-pivoting/), [KLU](/klu-solver/)), estimate the local truncation error from divided differences, and accept or reject the step. SPICE2 offered the trapezoidal rule and Gear's [backward differentiation formulas](/backward-differentiation-formulas/) (Nagel 1975).
- **TR-BDF2.** A one-step method that pairs a trapezoidal stage with a BDF2 stage; second order and L-stable: [TR-BDF2](/tr-bdf2/).
- **Relaxation methods.** [Iterated timing analysis](/iterated-timing-analysis/) solves the nonlinear system at each time point node by node with Gauss-Seidel-Newton sweeps and skips inactive nodes. Waveform relaxation iterates whole waveforms of subcircuits.
- **Model order reduction of linear parts.** Large linear subnetworks, such as interconnect, are replaced by small models with the same low-order moments: [Padé via Lanczos](/pade-via-lanczos/) and [PRIMA](/prima/).
- **Steady-state methods.** For periodic inputs, [shooting Newton](/shooting-newton-steady-state/) and [harmonic balance](/harmonic-balance-analysis/) compute the periodic solution directly.

## Bounds

- **Stiffness rules out explicit methods.** Forward Euler on $\dot v = \lambda v$ is stable only for $|1 + h\lambda| \le 1$, so the step must stay below $2\tau_{\min}$, the smallest time constant of the circuit, even when the waveforms of interest change on a much slower scale. This is why circuit simulators use implicit methods ([stiff ODE problem](/stiff-ode-problem/)).
- **The second Dahlquist barrier.** An A-stable linear multistep method has order at most 2, and the trapezoidal rule has the smallest error constant among them. So any method of higher order is either not A-stable (BDF3 to BDF6, which are stable only in a region that excludes part of the left half plane near the imaginary axis) or not a linear multistep method (implicit Runge-Kutta methods). Hairer and Wanner give the proof.
- **Step count.** For a method of order $p$ with local error control at tolerance $\varepsilon$, the step size near a smooth part of the solution is proportional to $\varepsilon^{1/(p+1)}$, so the number of steps grows like $\varepsilon^{-1/(p+1)}$; the TR-BDF2 page measures this growth for $p = 2$.
- **Cost per step.** Each accepted step costs one or more Newton iterations, each with an evaluation of all device models and a sparse LU factorization and solve. For circuits of practical size the device evaluation often dominates; this is an observation from practice, not a bound.

## Reductions

- **To a sequence of DC problems.** With companion models, each time step is a DC operating point problem of a resistive circuit; Newton's method reduces it in turn to a sequence of sparse linear systems.
- **From DC to transient.** Conversely, [pseudo-transient analysis](/pseudo-transient-analysis/) finds a hard DC operating point by integrating a transient problem with added capacitors until it settles.
- **Periodic steady state to a boundary value problem.** A periodic solution of period $T$ solves $x(T) = x(0)$, which [shooting Newton](/shooting-newton-steady-state/) treats with transient integration and the [shooting method](/shooting-method/).
- **Small-signal limit.** Linearizing around a DC operating point and taking a sinusoidal input of small amplitude gives [AC analysis](/ac-small-signal-analysis/), which solves the linear transient problem in the frequency domain.

## Applications

- **Digital cell characterization.** The delay and output slope tables of a standard cell library come from transient simulations of each cell over a grid of input slopes and output loads; [static timing analysis](/static-timing-analysis/) then uses the tables.
- **Analog and mixed-signal design.** Settling time, overshoot, slew rate and the start-up of oscillators are transient properties.
- **Signal and power integrity.** Ringing on interconnect, crosstalk, and voltage drop on the [power grid](/power-grid-analysis/) during switching.
- **Device and circuit co-simulation.** Bank et al. (1985) introduced TR-BDF2 to simulate semiconductor devices together with their circuits.

## References
