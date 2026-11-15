---
tag: M6YPVK
kind: concept
slug: adaptive-control
name: Adaptive control
aliases:
- adaptive controller
area: control/robust-and-adaptive-control
level: intro
summary: Control that adjusts its parameters online from data, for plants whose parameters are unknown or change slowly.
prereqs: [feedback-control-loop]
see_also: [model-reference-adaptive-control, self-tuning-regulator, certainty-equivalence, gain-scheduling, mit-rule, rohrs-counterexample, system-identification, model-uncertainty]
sources:
  - book: isbn:9780486462783
    title: "Karl Johan Åström and Björn Wittenmark, Adaptive Control, second edition, Addison-Wesley 1995 (Dover reprint 2008)"
    locator: "Chapter 1, What is adaptive control (the definition, the two loops, direct and indirect schemes, and the relation to gain scheduling and robust control)"
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Chapter 1, Introduction (adaptive control, direct and indirect schemes, certainty equivalence and a brief history)"
  - book: isbn:9780486442266
    title: "Kumpati S. Narendra and Anuradha M. Annaswamy, Stable Adaptive Systems, Prentice Hall 1989 (Dover reprint 2005)"
    locator: "Chapter 1, Introduction (the classes of adaptive systems and the history of the stability problem)"
---

Adaptive control is control that adjusts the parameters of the controller while the system runs, from measured data, for a plant whose parameters are unknown or change slowly. An adaptive controller has two loops: an ordinary feedback loop with adjustable parameters, and an outer loop that changes these parameters. It differs from robust control, which uses one fixed controller for a whole set of possible plants, and from [gain scheduling](/gain-scheduling/), which changes the parameters from a measured operating condition by a fixed table and does not learn from the response.

## In plain words

A normal controller is tuned once, for one version of the machine. If the machine changes, for example an aircraft that burns fuel or a ship with a different load, the tuning is no longer right. An adaptive controller watches how the machine responds and changes its own tuning while it works. One kind first estimates a model of the machine and then tunes itself for that model. Another kind compares the machine with an ideal response and changes the tuning to make the difference small. Both kinds must learn fast enough to follow the changes, but not so fast that they react to noise or to effects that the model does not include.

## The idea

The plant has a known structure and unknown parameters $\theta^*$, for example a [transfer function](/transfer-function/) of known order with unknown coefficients. The controller $C(\vartheta)$ has adjustable parameters $\vartheta$. The adjustment mechanism updates $\vartheta(t)$ from the signals $u$, $y$ and the command $r$.

There are two classic structures.

- **Indirect (explicit) scheme.** An estimator computes $\hat\theta(t)$, for example with the [recursive least squares algorithm](/rls-algorithm/). A design rule $F$ then gives $\vartheta = F(\hat\theta)$, for example pole placement or minimum variance. Using the estimate as if it were the true value is the [certainty equivalence principle](/certainty-equivalence/). The [self-tuning regulator](/self-tuning-regulator/) and [adaptive pole placement](/adaptive-pole-placement/) are of this type.
- **Direct (implicit) scheme.** The plant model is written in terms of the controller parameters, and these are estimated directly, with no design step. [Model reference adaptive control](/model-reference-adaptive-control/) is of this type: the error $e = y - y_m$ to a reference model drives the update of the gains.

Even for a linear time-invariant plant the adaptive loop is nonlinear and time varying, because the parameters multiply the signals. So linear tools do not prove its properties. The main tools are a [Lyapunov function](/lyapunov-function/) of the tracking error and the parameter error, which gives bounded signals and $e \to 0$ (theorems on the MRAC page); averaging, which describes slow adaptation; and the [persistent excitation](/persistent-excitation/) condition, which decides whether the parameters converge to the true values.

Three questions recur in the field.

- **Convergence of the parameters.** The error can go to zero while the parameters stop at wrong values, if the command does not excite the plant enough.
- **Robustness.** The ideal theorems assume the plant has exactly the assumed structure. Small unmodeled dynamics and bounded disturbances can make the parameters drift and the loop lose stability; see the [Rohrs counterexample](/rohrs-counterexample/). Modifications such as [parameter projection](/parameter-projection/) and [sigma modification](/sigma-modification/) keep the parameters bounded.
- **Design at each instant.** An indirect scheme must avoid estimates for which the design does not exist, for example a model with a common factor of the numerator and the denominator.

## Examples

- **The MIT rule.** For the plant $kG(s)$ with $G(s) = 1/(s^2 + s + 1)$, $k = 1$, the model gain $k_0 = 2$ and a constant command $u_0$, the gradient law converges if and only if $\gamma u_0^2 < 1/2$ (a theorem on the [MIT rule](/mit-rule/) page). The safe gain depends on the size of the command, which is why the Lyapunov designs replaced this law.
- **Model reference control of an unstable plant.** For $\dot y = y + 2u$ and the model $\dot y_m = -2y_m + 2r$, the Lyapunov law drives the gains to the ideal values $(-1.5, 1)$ when $r = \sin t$. With $r = 1$ the error still goes to zero, but the gains stop on the line $k + l = -0.5$ (measurements on the [MRAC](/model-reference-adaptive-control/) page).
- **A self-tuning regulator.** For $y_{t+1} = 0.9y_t + 0.5u_t + e_{t+1} + 0.5e_t$ with unit noise variance, the open loop output has the variance 11.3. The self-tuner, which knows only the structure, reaches a variance between 0.97 and 1.04 after 5000 samples, close to the minimum 1 (measurements on the [self-tuning regulator](/self-tuning-regulator/) page).

## Where it is used

Adaptive control began with aircraft autopilots in the 1950s, where the dynamics change with speed and altitude. It is used in ship steering and autopilots, process control (pH, chemical reactors, paper machines), automatic tuning of [PID controllers](/pid-controller/) by [relay auto-tuning](/relay-autotuning/) followed by adaptation, active noise and vibration control with adaptive filters, robot manipulators with unknown loads, and power electronics. In many industrial products the adaptation runs only on demand (auto-tuning) or is combined with gain scheduling, because a loop that adapts all the time needs supervision to stay safe. Related learning methods are [iterative learning control](/iterative-learning-control/) for repeated tasks, [extremum seeking control](/extremum-seeking-control/) for the optimum of an unknown map, and [model-based reinforcement learning](/model-based-reinforcement-learning/).

## References
