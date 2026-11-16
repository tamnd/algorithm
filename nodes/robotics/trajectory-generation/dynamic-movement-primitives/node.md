---
tag: DHD4FD
kind: model
slug: dynamic-movement-primitives
name: Dynamic movement primitives
aliases:
- DMP
area: robotics/trajectory-generation
level: advanced
summary: "A stable second-order attractor system plus a learned forcing term, which encodes a demonstrated motion and adapts it to new goals."
history:
  year: 2002
  people: [Auke Jan Ijspeert, Jun Nakanishi, Stefan Schaal]
  note: "Ijspeert, Nakanishi and Schaal encoded demonstrated movements of a humanoid robot as nonlinear dynamical systems with learned forcing terms. Ijspeert, Nakanishi, Hoffmann, Pastor and Schaal gave the consolidated form in 2013."
prereqs: [ode-initial-value-problem, imitation-learning]
see_also: [imitation-learning, minimum-jerk-trajectory, runge-kutta-methods, asymptotic-stability, lyapunov-function, least-squares-problem, gaussian-process, trajectory-generation-problem]
sources:
  - paper: doi:10.1109/ROBOT.2002.1014739
    title: "Auke Jan Ijspeert, Jun Nakanishi and Stefan Schaal, Movement imitation with nonlinear dynamical systems in humanoid robots, IEEE International Conference on Robotics and Automation, 2002, 1398-1403"
    locator: "the whole paper (the dynamical system with a learned nonlinear term, and learning it from a demonstration)"
  - paper: doi:10.1162/NECO_a_00393
    title: "Auke Jan Ijspeert, Jun Nakanishi, Heiko Hoffmann, Peter Pastor and Stefan Schaal, Dynamical movement primitives, learning attractor models for motor behaviors, Neural Computation 25(2), 2013, 328-373"
    locator: "the whole paper (the transformation and canonical systems, the forcing term, locally weighted regression, stability, and the invariance properties)"
---

Dynamic movement primitives (DMPs) represent a motion, such as a reach or a stroke, as the solution of a small system of differential equations rather than as a list of points or a polynomial. The core is a damped spring that pulls the position $y$ toward a goal $g$: on its own, it always converges to $g$, smoothly and without overshoot. A learned forcing term pushes the spring along the shape of a demonstrated motion. The forcing term is driven by a phase variable $x$ that decays from 1 to 0, so it fades out and the spring alone finishes the motion at the goal. The weights of the forcing term are fitted to one demonstration by linear regression. After that, the same equations produce the motion again, faster or slower by changing one time constant $\tau$, and toward a different goal or from a different start by changing $g$ or $y_0$. Ijspeert, Nakanishi and Schaal (2002) introduced the model for [imitation learning](/imitation-learning/) on humanoid robots; the 2013 paper of Ijspeert, Nakanishi, Hoffmann, Pastor and Schaal, which spells the name "dynamical movement primitives", is the standard reference. This page covers the discrete (point-to-point) DMP of one coordinate.

## The machine

A discrete DMP for one coordinate has the state $(y, z, x)$: the position $y$, a scaled velocity $z = \tau \dot y$, and the phase $x$. Given a start $y_0$, a goal $g$, a time constant $\tau > 0$, gains $\alpha_z, \beta_z, \alpha_x > 0$, and weights $w_1, \dots, w_N$,

$$\tau \dot z = \alpha_z\big(\beta_z (g - y) - z\big) + f(x), \qquad \tau \dot y = z, \qquad \tau \dot x = -\alpha_x x,$$

with $y(0) = y_0$, $z(0) = 0$ and $x(0) = 1$. The first two equations are the *transformation system*, the third the *canonical system*. The forcing term is

$$f(x) = \frac{\sum_{i} \psi_i(x)\, w_i}{\sum_i \psi_i(x)}\; x\, (g - y_0), \qquad \psi_i(x) = \exp\big(-h_i (x - c_i)^2\big),$$

with centers $c_i$ spread along the decay of $x$ and widths $h_i$. The code uses $N = 20$ basis functions with $c_i = e^{-\alpha_x (i - 1)/(N - 1)}$, $h_i = 1/(c_{i+1} - c_i)^2$, $\alpha_z = 25$, $\beta_z = \alpha_z/4$ and $\alpha_x = 4$. The choice $\beta_z = \alpha_z/4$ makes the spring critically damped; the other values are tuning choices, common in the literature, not derived values.

```pseudo id=main
ROLLOUT(w, y0, g, τ, duration, dt)
L1  (y, z, x) ← (y0, 0, 1)
L2  ψi ← exp(-hi (x - ci)²) for each i
L3  f ← (Σ ψi wi / Σ ψi) · x · (g - y0)
L4  ż ← (αz (βz (g - y) - z) + f) / τ
L5  ẏ ← z / τ
L6  ẋ ← -αx x / τ
L7  repeat duration/dt times: advance (y, z, x) by one classical Runge-Kutta step of size dt, with derivatives from L2 to L6

FIT(t, y, ẏ, ÿ of the demonstration, τ)       ▷ g ← last y, y0 ← first y
L8  f_target ← τ² ÿ - αz (βz (g - y) - τ ẏ) at each sample, and x at each sample from x = exp(-αx t / τ)
L9  wi ← Σ ψi(x) s f_target / Σ ψi(x) s², with s = x (g - y0)
```

Line L8 solves the transformation system for the forcing term that would reproduce the demonstration exactly. Line L9 fits each weight by locally weighted regression, a weighted [least-squares problem](/least-squares-problem/) with one unknown per basis function. Line L7 integrates the [initial value problem](/ode-initial-value-problem/) with the classical fourth-order [Runge-Kutta method](/runge-kutta-methods/).

## What it counts

The model describes a motion by $N$ weights plus the parameters $y_0$, $g$ and $\tau$. It does not count time or cost; what matters is what the motion does when the parameters change.

**A measured example.** The demonstration is the [minimum-jerk](/minimum-jerk-trajectory/) motion from 0 to 1 in 1 s, sampled every millisecond. After FIT with the values above, ROLLOUT with RK4 at $dt = 0.001$ s gives a maximum error of $0.0127$ against the demonstration over $[0, 1]$, and $y(1) = 0.99896$. At $t = 3$ s the state is $(y, z, x) \approx (0.999997,\ 1.25 \times 10^{-5},\ 6.1 \times 10^{-6})$: the motion has settled at the goal. These are measurements with these settings, checked by the tests with the tolerance $0.03$ on the error.

## Relation to other models

- **Polynomial trajectories.** A [minimum-jerk](/minimum-jerk-trajectory/) or [quintic](/quintic-polynomial-trajectory/) motion is fixed by its end states and duration. A DMP can encode any smooth demonstrated shape, at the cost of $N$ weights, and it is defined by a differential equation, so it can react to a changed goal during the motion.
- **Plain spring-damper.** With $f = 0$, the DMP is a critically damped spring that converges to $g$ with no overshoot; the tests check that this motion is monotone. The forcing term is what makes the motion take the demonstrated shape.
- **Imitation learning.** DMPs are a representation for [imitation learning](/imitation-learning/) from one demonstration. Probabilistic movement primitives and [Gaussian process](/gaussian-process/) models represent distributions over motions from many demonstrations instead.
- **Rhythmic DMPs.** Replacing the decaying phase by a phase oscillator and the basis functions by periodic ones gives a model of periodic motions (Ijspeert et al. 2013).
- **Trajectory generation.** A DMP gives positions, velocities and accelerations over time, like any method of the [trajectory generation problem](/trajectory-generation-problem/), but it does not enforce velocity or acceleration limits.

## Known results in the model

**Convergence to the goal (theorem).** The phase is $x(t) = e^{-\alpha_x t/\tau}$, so $|f(x(t))| \le W x(t) |g - y_0|$, where $W$ is the largest $|w_i|$, and the forcing term decays exponentially. The transformation system is a stable linear system driven by this decaying input: with $\beta_z = \alpha_z/4$ both of its eigenvalues equal $-\alpha_z/(2\tau)$. A stable linear system with an input that tends to zero has a state that tends to its equilibrium $(g, 0)$, so $y(t) \to g$ and $z(t) \to 0$ from every start, for any weights. In the terms of [stability theory](/asymptotic-stability/), the equilibrium $(g, 0, 0)$ of the whole system is globally asymptotically stable. Ijspeert et al. (2013) discuss this property; for the unforced part, a quadratic [Lyapunov function](/lyapunov-function/) gives it directly. The tests check convergence at $t = 3$ s for the demonstration, and for a new start and goal.

**Time scaling (theorem).** If $(y, z, x)(t)$ solves the system with time constant 1, then $(y, z, x)(t/\tau)$ solves it with time constant $\tau$, because $\tau$ divides every right-hand side. So changing $\tau$ replays the same motion slower or faster, with the same shape. A discrete version also holds: RK4 with step $\tau\, dt$ for time constant $\tau$ gives the same samples as step $dt$ for time constant 1. The tests check this for $\tau = 2$ and $dt = 0.002$, to $10^{-9}$.

**Goal scaling (theorem, and a known weakness).** Because $f$ contains the factor $g - y_0$, moving the goal scales the forcing term in proportion to the amplitude of the motion, so the shape is stretched along the coordinate. If $g = y_0$, the forcing term vanishes and the motion is a rest. If $g - y_0$ changes sign, the shape is mirrored. Ijspeert et al. (2013) discuss these effects and alternatives for the scaling factor.

**Learning is linear (theorem).** For a fixed phase, $f$ is linear in the weights. Line L9 fits each weight by its own one-dimensional weighted regression, whose solution is unique whenever $\sum \psi_i s^2 > 0$ on the data.

**Other results.** The 2013 paper treats coupling terms that add obstacle avoidance or contact forces, several coordinates sharing one phase, and online changes of the goal; these are beyond this page.

## References
