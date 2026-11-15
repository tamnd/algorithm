---
tag: 64C4HP
kind: model
slug: switched-system
name: Switched system
aliases:
- switched linear system
area: control/discrete-event-and-hybrid-systems
level: core
summary: A system whose vector field is chosen at each time from a finite family by a switching signal.
prereqs: [state-space-representation, lyapunov-stability]
see_also: [common-lyapunov-function, joint-spectral-radius, dwell-time-theorem, hybrid-automata, piecewise-affine-system, zeno-behavior, linear-time-varying-system, sliding-mode-control]
sources:
  - book: isbn:9780817642976
    title: Daniel Liberzon, Switching in Systems and Control, Birkhäuser, 2003
    locator: the chapters on stability under arbitrary switching and on stability under constrained switching (dwell time, multiple Lyapunov functions)
  - paper: doi:10.1109/37.793443
    title: Daniel Liberzon and A. Stephen Morse, Basic problems in stability and design of switched systems, IEEE Control Systems Magazine 19(5), 59-70, 1999
    locator: the three basic problems (stability under arbitrary switching, under slow switching, and the design of a stabilizing switching signal)
  - paper: "Kumpati S. Narendra and Jeyendran Balakrishnan, A common Lyapunov function for stable LTI systems with commuting A-matrices, IEEE Transactions on Automatic Control 39(12), 2469-2471, 1994"
    locator: the main theorem (commuting Hurwitz matrices have a common quadratic Lyapunov function)
  - paper: "Wijesuriya P. Dayawansa and Clyde F. Martin, A converse Lyapunov theorem for a class of dynamical systems which undergo switching, IEEE Transactions on Automatic Control 44(4), 751-760, 1999"
    locator: the converse theorem (uniform asymptotic stability under arbitrary switching gives a common Lyapunov function) and the example with no common quadratic Lyapunov function
  - paper: "A. Stephen Morse, Supervisory control of families of linear set-point controllers, Part 1, Exact matching, IEEE Transactions on Automatic Control 41(10), 1413-1431, 1996"
    locator: the dwell-time switching logic and its stability argument
---

A switched system is a dynamical system with several modes. Each mode has its own vector field, and a piecewise constant switching signal says which mode is active at each time. The continuous state moves along the active vector field and does not jump when the mode changes. The model describes a plant with gear changes or with valves that open and close, a power converter, a controller that a supervisor replaces with another one, and a nonlinear system that is approximated by a different linear model in each region. It is the simplest class of hybrid systems: the discrete part is reduced to the switching signal, and the questions are about the continuous state. The main surprise is that switching between modes that are each globally exponentially stable can make the state grow without bound, and that switching between unstable modes can make it converge.

## The machine

**Modes.** A finite index set $\mathcal{P}$ and a family of vector fields $f_p : \mathbb{R}^n \to \mathbb{R}^n$, $p \in \mathcal{P}$, each locally Lipschitz with $f_p(0) = 0$. In a **switched linear system**, $f_p(x) = A_p x$.

**Switching signal.** A piecewise constant function $\sigma : [0, \infty) \to \mathcal{P}$, continuous from the right, with a finite number of discontinuities, the switching times, on every bounded interval. This excludes infinitely many switches in finite time ([Zeno behavior](/zeno-behavior/)).

**Dynamics.**

$$\dot x(t) = f_{\sigma(t)}(x(t)).$$

Between two switching times the solution follows one vector field; at a switching time it is continuous and only its derivative jumps. The discrete-time version is $x(t+1) = A_{\sigma(t)} x(t)$, with $\sigma$ any sequence in $\mathcal{P}$.

**Kinds of switching.** The signal can be:

- time dependent: an external signal, known or unknown, on which the analysis puts no condition (arbitrary switching) or a condition on how often it switches (constrained switching);
- state dependent: $\sigma$ is a function of $x$, with the modes assigned to regions of the state space, as in a [piecewise affine system](/piecewise-affine-system/). Near a boundary between regions the solution can chatter, and then a sliding motion along the boundary must be defined;
- controlled: the designer chooses $\sigma$, as a control input.

**Example.** Take

$$A_1 = \begin{bmatrix} -0.1 & 1 \\ -10 & -0.1 \end{bmatrix}, \qquad A_2 = \begin{bmatrix} -0.1 & 10 \\ -1 & -0.1 \end{bmatrix}.$$

Both have eigenvalues $-0.1 \pm j\sqrt{10}$, so each mode alone is globally exponentially stable. The orbits of mode 1 are spirals stretched along the $x_2$ axis, and those of mode 2 are stretched along the $x_1$ axis. Use the switching rule: mode 1 when $x_1 x_2 \le 0$, mode 2 when $x_1 x_2 > 0$. From $x(0) = (1, 0)$, each quarter turn takes $\tau = \pi / (2\sqrt{10}) \approx 0.4967$ and is made on the stretched side, which multiplies the distance from the origin by $\sqrt{10}\, e^{-0.1\tau}$. Each half turn multiplies it by $10\, e^{-0.2\tau} \approx 9.054$:

| $t$ | 0 | 0.9935 | 1.9869 | 2.9804 |
|---|---|---|---|---|
| $\lvert x(t) \rvert$ | 1 | 9.054 | 81.98 | 742.3 |

Each mode alone, for the same time $0.9935$, takes $(1, 0)$ to about $(-0.905, 0)$. The reverse rule, mode 2 when $x_1 x_2 \le 0$, makes each half turn multiply the distance by $e^{-0.2\tau}/10 \approx 0.0905$, a much faster decay than either mode gives. From this initial state the first rule produces the same signal as a timer that switches every $\tau \approx 0.4967$ s, so a time-dependent signal with that period also makes the state grow.

## What it counts

The model predicts the trajectory for a given switching signal. The analysis asks questions over a class of signals:

- **Stability under arbitrary switching.** Is the origin globally uniformly asymptotically stable (GUAS), or globally uniformly exponentially stable (GUES), for every switching signal, with constants that do not depend on the signal?
- **Stability under constrained switching.** For which classes of slow signals, such as a minimum time between switches, is the origin GUES?
- **Stabilization by switching.** Is there a switching signal or rule that drives the state to the origin, even when no mode is stable by itself?

The model does not include jumps of the state, guards and resets in general, or the timing of the discrete logic itself. For those, use [hybrid automata](/hybrid-automata/).

## Relation to other models

- A [hybrid automaton](/hybrid-automata/) with one location per mode, no reset maps and switching on guards is a switched system with state-dependent switching. A switched system with time-dependent switching hides the discrete dynamics inside $\sigma$.
- A [piecewise affine system](/piecewise-affine-system/) is a switched affine system whose switching is fixed by a polyhedral partition of the state space. A [mixed logical dynamical system](/mixed-logical-dynamical-system/) is an equivalent discrete-time form used for optimization.
- For one fixed signal $\sigma$, a switched linear system is a [linear time-varying system](/linear-time-varying-system/) with a piecewise constant $A(t)$. Its [state transition matrix](/state-transition-matrix/) is a product of matrix exponentials $e^{A_p \Delta t}$.
- [Gain scheduling](/gain-scheduling/) and the supervisors of adaptive control switch between controllers, and the closed loop is a switched system. [Sliding mode control](/sliding-mode-control/) switches the control law on a surface and uses the sliding motion on it.
- [Sampled-data](/sampled-data-system/) and [event-triggered](/event-triggered-control/) control loops become switched or hybrid systems when the sampling times vary.

## Known results in the model

- **Stability of each mode is not enough.** The example above has two Hurwitz modes and an unstable switched system.
- **Common Lyapunov functions.** If the modes share one [common Lyapunov function](/common-lyapunov-function/), the switched system is GUAS under arbitrary switching. The converse holds for a compact set of modes: GUAS under arbitrary switching gives a common Lyapunov function (Dayawansa and Martin 1999). For switched linear systems, GUAS under arbitrary switching is the same as GUES.
- **Commuting matrices.** If the matrices $A_p$ are Hurwitz and commute pairwise, they have a common quadratic Lyapunov function, and the system is GUES under arbitrary switching (Narendra and Balakrishnan 1994). The result extends to sets of Hurwitz matrices that generate a solvable Lie algebra, a condition stated with the [Lie bracket](/lie-bracket/) (Liberzon 2003, the chapter on stability under arbitrary switching).
- **Quadratic functions are not always enough.** Some switched linear systems are GUES under arbitrary switching but have no common quadratic Lyapunov function (Dayawansa and Martin 1999).
- **Discrete time.** The system $x(t+1) = A_{\sigma(t)} x(t)$ is GUES under arbitrary switching if and only if the [joint spectral radius](/joint-spectral-radius/) of $\{A_p\}$ is below 1.
- **Slow switching.** If every mode is globally exponentially stable and the time between switches is at least a large enough dwell time, the switched system is GUES. The bound depends only on the modes ([dwell-time theorem](/dwell-time-theorem/), Morse 1996), and an average dwell time is enough.

## References
