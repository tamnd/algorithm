---
tag: H2DFND
kind: definition
slug: capture-point
name: Capture point
aliases:
- instantaneous capture point
area: robotics/mobile-and-legged-robots
level: advanced
summary: "The ground point where a legged robot must put its center of pressure to come to a stop; for the linear inverted pendulum it is x + x' / omega, exact only for that model."
prereqs: [linear-inverted-pendulum-model]
see_also: [support-polygon, center-of-pressure, zero-moment-point, footstep-planning, zmp-preview-control, convex-mpc-legged-locomotion, region-of-attraction, centroidal-dynamics]
sources:
  - paper: doi:10.1109/ICHR.2006.321385
    title: Jerry Pratt, John Carff, Sergey Drakunov and Ambarish Goswami, Capture point, a step toward humanoid push recovery, IEEE-RAS International Conference on Humanoid Robots, 2006
    locator: pages 200 to 207
  - paper: doi:10.1177/0278364912452673
    title: Twan Koolen, Tomas de Boer, John Rebula, Ambarish Goswami and Jerry Pratt, Capturability-based analysis and control of legged locomotion, Part 1, Theory and application to three simple gait models, International Journal of Robotics Research 31(9), 2012
    locator: pages 1094 to 1113
  - paper: doi:10.1109/TRO.2015.2405592
    title: Johannes Englsberger, Christian Ott and Alin Albu-Schäffer, Three-dimensional bipedal walking control based on divergent component of motion, IEEE Transactions on Robotics 31(2), 2015
    locator: pages 355 to 368
---

The capture point is the point on the ground where a legged robot must put its center of pressure, by a step or by its ankle, so that it comes to a stop. For the [linear inverted pendulum model](/linear-inverted-pendulum-model/), it has the closed form $\xi = x + \dot x / \omega$, where $x$ is the position of the center of mass (CoM), $\dot x$ its velocity and $\omega = \sqrt{g / z_0}$. A robot that is pushed can use it to decide where to step. The formula is exact for that model only; for a real robot it is an estimate.

## Definition

**The general definition.** Koolen et al. (2012) define the terms for any legged model. A *captured state* is a state with zero kinetic energy from which the robot can stay at rest without new steps. A *capture point* is a point on the ground such that, if the robot steps so that its base of support covers that point, it can come to a captured state with no further steps (Pratt et al., 2006, define it as a point where the robot can step to come to a complete stop). A state is *N-step capturable* if the robot can reach a captured state in at most $N$ steps. In general the set of capture points depends on the model, the actuator limits and the step time, and it is a region, not a point.

**The instantaneous capture point of the LIPM.** In the linear inverted pendulum, with CoM position $x \in \mathbb{R}^2$, velocity $\dot x$, height $z_0$, $g = 9.81$ m/s² along $-z$ and $\omega = \sqrt{g / z_0}$, the **instantaneous capture point** is

$$\xi = x + \frac{\dot x}{\omega}.$$

Englsberger et al. (2015) call the same quantity the divergent component of motion. With the foot point, or the center of pressure, at $p$, it moves by

$$\dot \xi = \omega (\xi - p), \qquad \text{so for constant } p: \quad \xi(t) = p + (\xi_0 - p) e^{\omega t}.$$

**Theorem (capture in the LIPM).** Hold the center of pressure at a constant point $p$. The CoM comes to rest over $p$, that is $x(t) \to p$ and $\dot x(t) \to 0$, if and only if $p = \xi_0$.

*Proof.* Write $\zeta = x - \dot x / \omega$. The model $\ddot x = \omega^2 (x - p)$ gives $\dot \zeta = -\omega (\zeta - p)$, so $\zeta(t) \to p$ for every start. Also $x = (\xi + \zeta) / 2$ and $\dot x = \omega (\xi - \zeta) / 2$. If $p = \xi_0$, then $\xi(t) = p$ for all $t$, so $x \to p$ and $\dot x \to 0$. If $p \ne \xi_0$, then $|\xi(t) - p|$ grows as $e^{\omega t}$, so $x$ or $\dot x$ is unbounded. $\square$

So in the LIPM the capture point is a single point, and the CoM converges to it with the time constant $1 / \omega$. The robot is 0-step capturable, which means it can stop with its ankle only, exactly when $\xi$ lies in its [support polygon](/support-polygon/). A capture point that the robot cannot reach in one step means a fall in this model, unless it takes more steps.

**A control law.** Because $\xi$ is the only unstable part of the LIPM, a balance controller can control $\xi$ alone. Setting the center of pressure to

$$p = \xi - \frac{\dot \xi_d}{\omega} + \frac{k}{\omega} (\xi - \xi_d), \qquad k > 0,$$

gives $\dot \xi - \dot \xi_d = -k (\xi - \xi_d)$, so $\xi$ converges to a planned path $\xi_d$. This holds only while the commanded $p$ is in the support polygon. When the command must be clipped to the polygon, the convergence proof no longer holds, and the remedy is a step.

## Examples and non-examples

**The check value.** Take $z_0 = 1$ m, so $\omega = 3.13209$ 1/s. A CoM at $x = 0$ moving at $\dot x = 0.5$ m/s has $\xi = 0.5 / 3.13209 = 0.15964$ m. The robot comes to rest over its foot if it puts the foot 0.15964 m ahead of the CoM.

**Ankle or step.** A robot stands with its CoM over the middle of a sole that reaches $0.1$ m to the front. A push gives it a speed of $0.25$ m/s. Then $\xi = 0.0798$ m, which is in the sole, so the ankle can stop the robot by moving the center of pressure to $\xi$. After a push to $0.5$ m/s, $\xi = 0.15964$ m is outside the sole, and the robot must step.

**A late step.** In the case $\dot x = 0.5$ m/s, if the center of pressure stays at $p = 0$ until the step, the capture point moves away as $\xi(t) = 0.15964\, e^{\omega t}$. It is at $0.2987$ m after $0.2$ s, at $0.4085$ m after $0.3$ s and at $0.5588$ m after $0.4$ s. A slow step needs a much longer step, and if the leg cannot reach that far, one step is not enough. This growth is why the N-step capture regions of Koolen et al. (2012) depend on the minimum step time and the maximum step length.

**Non-example: the CoM projection.** The point under the CoM is the capture point only when the robot does not move. A robot that walks has its capture point ahead of its CoM in the direction of motion.

**Non-example: a robot with a varying height or a moving upper body.** If the CoM height changes or the robot changes its angular momentum, the formula $x + \dot x / \omega$ is an estimate, not the exact capture point. A flywheel or a swinging upper body can shift the effective center of pressure for a short time, and Koolen et al. (2012) treat these models separately. The exact capture region of a full humanoid has no closed form.

## Related definitions

- [Linear inverted pendulum model](/linear-inverted-pendulum-model/): the model in which $\xi$ is exact; $\xi$ is its unstable part.
- [Support polygon](/support-polygon/): the robot can stop without a step exactly when $\xi$ is inside it (in the LIPM).
- [Center of pressure](/center-of-pressure/) and [zero moment point](/zero-moment-point/): the input that moves $\xi$. The ZMP criterion is a condition at one instant; the capture point also says where the next foot must go.
- [Footstep planning](/footstep-planning/): capture point based controllers adjust the next footstep online.
- [Region of attraction](/region-of-attraction/): the set of N-step capturable states is a region of attraction of the captured states, under the stepping rules of the model.

## References
