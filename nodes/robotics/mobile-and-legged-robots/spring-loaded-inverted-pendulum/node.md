---
tag: Y7XKFH
kind: model
slug: spring-loaded-inverted-pendulum
name: Spring-loaded inverted pendulum
aliases:
- SLIP model
area: robotics/mobile-and-legged-robots
level: advanced
summary: "A point mass on a massless spring leg, the template model of running and hopping in animals and robots; its stance phase has no closed form solution in general."
prereqs: [linear-inverted-pendulum-model]
see_also: [raibert-hopping-controller, linear-inverted-pendulum-model, passive-dynamic-walking, hybrid-zero-dynamics, limit-cycle, hybrid-automata, runge-kutta-methods, hamiltonian-systems]
sources:
  - paper: doi:10.1016/0021-9290(89)90224-8
    title: Reinhard Blickhan, The spring-mass model for running and hopping, Journal of Biomechanics 22(11-12), 1989
    locator: pages 1217 to 1227
  - paper: doi:10.1242/jeb.202.23.3325
    title: Robert J. Full and Daniel E. Koditschek, Templates and anchors, neuromechanical hypotheses of legged locomotion on land, Journal of Experimental Biology 202(23), 1999
    locator: pages 3325 to 3332
  - paper: doi:10.1016/S0021-9290(01)00245-7
    title: Andre Seyfarth, Hartmut Geyer, Michael Günther and Reinhard Blickhan, A movement criterion for running, Journal of Biomechanics 35(5), 2002
    locator: pages 649 to 655
  - paper: doi:10.1016/j.jtbi.2004.08.015
    title: Hartmut Geyer, Andre Seyfarth and Reinhard Blickhan, Spring-mass running, simple approximate solution and application to gait stability, Journal of Theoretical Biology 232(3), 2005
    locator: pages 315 to 328
---

The spring-loaded inverted pendulum (SLIP) is a point mass on a massless leg that is a linear spring. In flight the mass moves on a parabola, and in stance the foot is fixed and the spring compresses and extends. With a few parameters it reproduces the center of mass motion and the ground force of running and hopping animals, as Blickhan (1989) showed for running and hopping, and Full and Koditschek (1999) called it a template: the simplest model that captures a behavior, which a more detailed robot model (an anchor) must embed. Its stance phase has no closed form solution in general, so most results are found by numerical integration.

## The machine

The model is planar. Gravity is $g = 9.81$ m/s² along $-y$, and the ground is the line $y = 0$.

**State.** The position and velocity of the mass, $(x, y, \dot x, \dot y)$, and the phase, which is flight or stance. In stance, the foot point $(x_f, 0)$ is also part of the state.

**Parameters.** The mass $m$ in kilograms, the leg stiffness $k$ in newtons per meter, the rest length $\ell_0$ in meters, and the angle of attack $\alpha$: the angle between the leg and the ground at touchdown. A common dimensionless group is the relative stiffness $k \ell_0 / (m g)$.

**Flight.** $\ddot x = 0$ and $\ddot y = -g$. The leg is held at the angle $\alpha$, and its mass is zero, so it does not affect the motion.

**Touchdown.** Stance starts when the foot reaches the ground, at $y = \ell_0 \sin \alpha$ while $\dot y < 0$. The foot is fixed at $x_f = x + \ell_0 \cos \alpha$ for a robot that moves in $+x$.

**Stance.** With $r = (x - x_f, y)$ and leg length $\ell = |r|$,

$$m \ddot r = k (\ell_0 - \ell) \frac{r}{\ell} - m g e_y.$$

The foot does not slip, and the ground can only push, so the leg force $k (\ell_0 - \ell)$ must be positive.

**Lift-off.** Stance ends when the leg returns to its rest length, $\ell = \ell_0$, and the next flight starts.

**Assumptions.** The leg has no mass, so touchdown has no impact loss. The spring has no damping and no actuator, so the model is conservative. There is no body, so there is no pitch. Raibert's hopping robots add a body, a leg actuator and a hip torque to this model; see the [Raibert hopping controller](/raibert-hopping-controller/).

## What it counts

The model predicts the path of the mass, the ground reaction force $k (\ell_0 - \ell)$ along the leg, the stance and flight times, and the apex return map: the map from one apex (the top of a flight, where $\dot y = 0$) to the next. In studies of animals, the parameters are fitted to measured force plate data and to the motion of the center of mass.

## Relation to other models

- **[Linear inverted pendulum model](/linear-inverted-pendulum-model/).** The LIPM keeps the height constant and has no flight phase and no spring. It describes walking with a stiff leg; SLIP describes the bouncing motion of running.
- **The [Raibert hopping controller](/raibert-hopping-controller/)** runs a robot whose leg is close to a SLIP leg, with a thrust added in stance to put back the energy that the robot loses.
- **Bipedal SLIP models** use two spring legs and a double support phase to describe walking with the same template.
- **[Passive dynamic walking](/passive-dynamic-walking/)** and **[hybrid zero dynamics](/hybrid-zero-dynamics/)** study gaits of models that have legs with mass, impacts at touchdown and joints, instead of a massless spring leg.
- **Hybrid systems.** A SLIP is a hybrid system with two modes and guards at touchdown and lift-off, as in [hybrid automata](/hybrid-automata/). A periodic gait is a [limit cycle](/limit-cycle/) of this hybrid system.

## Known results in the model

**Energy is conserved.** The total energy $\frac12 m (\dot x^2 + \dot y^2) + m g y + \frac12 k (\ell_0 - \ell)^2$, with the spring term only in stance, is constant through flight, touchdown, stance and lift-off. At an apex the vertical speed is zero, so for a fixed energy the apex height $y_a$ fixes the forward speed. The apex return map is a map of one number, $y_a \mapsto y_a'$.

**No closed form in stance.** With forward motion, the stance equations couple the leg length and the leg angle through gravity, and no closed form solution is known in general. Two special cases have one. In a vertical hop ($\dot x = 0$), the stance is a harmonic oscillator about the static compression $m g / k$. If gravity is neglected during stance, the leg force is central, the angular momentum about the foot is conserved, and the motion reduces to a quadrature. Geyer, Seyfarth and Blickhan (2005) build an approximate stance solution with small leg compression and small leg sweep, and use it to study the stability of gaits.

**The vertical hop.** Let the mass hit the ground with downward speed $v$ and let $\omega_s = \sqrt{k / m}$. The stance lasts

$$t_s = \frac{2\pi - 2\beta}{\omega_s}, \qquad \beta = \operatorname{atan2}\!\left(\frac{v}{\omega_s}, \frac{m g}{k}\right),$$

which is longer than half the spring period $\pi / \omega_s$ because gravity holds the mass down. With $m = 80$ kg, $k = 20000$ N/m, $\ell_0 = 1$ m and a drop from an apex of $1.1$ m, $v = 1.4007$ m/s, $\omega_s = 15.811$ 1/s, $m g / k = 0.03924$ m and $t_s = 0.2514$ s, against $\pi / \omega_s = 0.1987$ s. The largest compression is $m g / k + \sqrt{(m g / k)^2 + (v / \omega_s)^2} = 0.1361$ m, and the peak force is $2723$ N, about $3.47$ times the body weight.

**Self-stable running (a numerical result).** Seyfarth et al. (2002) found, by numerical simulation, that a SLIP runner with a fixed angle of attack can run in a stable way, without any feedback, for suitable pairs of stiffness and angle. The result is a computation for the stated parameters, not a theorem for all parameters. The table shows the same effect for $m = 80$ kg, $k = 20000$ N/m, $\ell_0 = 1$ m and a total energy equal to that of a speed of $5$ m/s at a height of $1$ m. The stance is integrated with the classical fourth-order [Runge-Kutta method](/runge-kutta-methods/) at a step of $10^{-4}$ s, and the energy error stays below $10^{-6}$ of the total.

| angle of attack | apex heights from $1.0$ m, one per step (m) | outcome |
|---|---|---|
| 66 degrees | 1.0, 1.0149, 1.0283, 1.0411, 1.0539, 1.0672 | the apex rises at each step; no gait near this height |
| 68 degrees | 1.0, 0.9557, 0.9405, 0.9402, 0.9403, 0.9403 | converges to a periodic gait with apex $0.9403$ m |
| 70 degrees | 1.0, 0.9169, then the apex is below the touchdown height | the runner stumbles |

At 68 degrees the fixed point of the apex map has an apex speed of $5.116$ m/s and a stance time of $0.1493$ s, and starts at $0.95$ m and $1.05$ m converge to the same apex. The stable range of the angle is narrow, and it moves with the stiffness and the speed.

## References
