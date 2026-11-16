---
tag: 1MSSP0
kind: model
slug: velocity-motion-model
name: Velocity motion model
aliases:
- velocity-based motion model
area: robotics/localization-and-slam
level: core
summary: A probabilistic model of the next pose of a planar robot given linear and angular velocity commands with noise.
history:
  year: 2005
  people: [Sebastian Thrun, Wolfram Burgard, Dieter Fox]
  note: Probabilistic Robotics gives the model with noisy linear and angular velocities and a third noisy rotation at the end of the motion, so that the end pose has a density in all three coordinates.
prereqs: [bayes-filter]
see_also: [odometry-motion-model, unicycle-model, differential-drive-model, kinematic-bicycle-model, monte-carlo-localization, ekf-localization, particle-filter, dead-reckoning]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 5, Section 5.3 (the velocity motion model: the closed form density, the sampling algorithm and the derivation with the final rotation)"
---

The velocity motion model gives the probability of the next pose of a planar robot, given the linear and angular velocity that it was told to drive with. A pose is a position $(x, y)$ and a heading $\theta$. If the robot followed the command exactly, with constant velocities $v$ and $\omega$ for a time $\Delta t$, it would move on a circular arc. Real robots do not follow commands exactly, so the model adds Gaussian noise to both velocities and also adds a small noisy rotation at the end. The result is the motion model $p(x_t \mid u_t, x_{t-1})$ of the [Bayes filter](/bayes-filter/), with the control $u_t = (v, \omega)$. Since it needs only the command, it can be used before the motion happens, for prediction and planning. The notation is the one of Thrun, Burgard and Fox (2005).

## The machine

**State.** The pose $x_{t-1} = (x, y, \theta)$ before the motion and $x_t = (x', y', \theta')$ after it, in meters and radians.

**Input.** The command $u_t = (v, \omega)$: a linear velocity $v$ in m/s and an angular velocity $\omega$ in rad/s, held constant for the time step $\Delta t$ in seconds.

**Noise.** The robot executes noisy velocities and a final rotation rate:

$$\hat v = v + \varepsilon_1, \quad \varepsilon_1 \sim \mathcal N(0,\ \alpha_1 v^2 + \alpha_2 \omega^2),$$

$$\hat\omega = \omega + \varepsilon_2, \quad \varepsilon_2 \sim \mathcal N(0,\ \alpha_3 v^2 + \alpha_4 \omega^2),$$

$$\hat\gamma = \varepsilon_3, \quad \varepsilon_3 \sim \mathcal N(0,\ \alpha_5 v^2 + \alpha_6 \omega^2).$$

The second argument of $\mathcal N$ is a variance. The printings of the source and many course notes differ: some use the standard deviation $\alpha_1 |v| + \alpha_2 |\omega|$ instead. The two forms are different models, and alpha values fitted for one do not carry over.

**Parameters.** Six numbers $\alpha_1, \ldots, \alpha_6 \ge 0$. They carry units, since each adds a squared linear and a squared angular velocity. They depend on the robot, its controller and the floor, and they are fitted to data.

**Output.** With $r = \hat v / \hat\omega$,

$$x' = x - r \sin\theta + r \sin(\theta + \hat\omega \Delta t), \qquad y' = y + r \cos\theta - r \cos(\theta + \hat\omega \Delta t), \qquad \theta' = \theta + \hat\omega \Delta t + \hat\gamma \Delta t.$$

The robot moves on a circle of signed radius $r$ around the center $(x - r \sin\theta,\ y + r \cos\theta)$. For $\hat\omega = 0$ the arc becomes a straight line, $x' = x + \hat v \Delta t \cos\theta$ and $y' = y + \hat v \Delta t \sin\theta$, and code must treat this case on its own.

**Standing assumptions.** The robot moves in a plane, and the velocities are constant during $\Delta t$; a real controller changes them during the step. The three errors are independent of each other and of the errors of earlier steps, which is an approximation. The model is the [unicycle model](/unicycle-model/) with noise, so it fits robots that can follow any arc, such as a differential drive. It does not fit a car, whose turning radius has a lower bound.

**Two algorithms.** Sampling draws $\varepsilon_1, \varepsilon_2, \varepsilon_3$ and applies the output equations. The closed form inverts the output equations. Given $x_{t-1}$ and $x_t$, the center of the circle through the two positions that is tangent to the start heading is $(x^*, y^*)$ with

$$\mu = \frac{1}{2}\, \frac{(x - x')\cos\theta + (y - y')\sin\theta}{(y - y')\cos\theta - (x - x')\sin\theta}, \qquad x^* = \frac{x + x'}{2} + \mu (y - y'), \qquad y^* = \frac{y + y'}{2} + \mu (x' - x).$$

The turn is $\Delta\theta = \operatorname{atan2}(y' - y^*, x' - x^*) - \operatorname{atan2}(y - y^*, x - x^*)$, wrapped into $(-\pi, \pi]$. Then $\hat\omega = \Delta\theta / \Delta t$, $\hat v = \hat\omega\, r_s$ with the signed radius $r_s = -(x^* - x)\sin\theta + (y^* - y)\cos\theta$, and $\hat\gamma = (\theta' - \theta)/\Delta t - \hat\omega$. The closed form returns the product $p_1 p_2 p_3$ of the Gaussian densities of $v - \hat v$, $\omega - \hat\omega$ and $\hat\gamma$.

**Example.** Start at $(0, 0, 0)$ with $v = 1$ m/s, $\omega = 0.5$ rad/s and $\Delta t = 1$ s. The noise-free end pose is $(\sin 0.5,\ 2(1 - \cos 0.5),\ 0.5) \approx (0.95885, 0.24483, 0.5)$, on the circle of radius 2 around $(0, 2)$. The closed form gives $\mu \approx 1.95816$, the center $(0, 2)$, $\Delta\theta = 0.5$, and so $\hat v = 1$, $\hat\omega = 0.5$ and $\hat\gamma = 0$. With every $\alpha_i = 0.01$, each variance is $0.01 \cdot 1 + 0.01 \cdot 0.25 = 0.0125$, and $p_1 p_2 p_3 = (2\pi \cdot 0.0125)^{-3/2} \approx 45.432$.

## What it counts

The model assigns a probability to a motion under a command. It gives the density $p(x_t \mid u_t, x_{t-1})$ for a hypothesized end pose, which grid filters such as the [histogram filter](/histogram-filter/) need, and samples of $x_t$, which a [particle filter](/particle-filter/) needs. Both take $O(1)$ arithmetic operations and trigonometric calls per pose, so the prediction step of a filter with $N$ particles costs $O(N)$. The model also predicts the mean motion of a command, which a planner can use before the robot moves.

## Relation to other models

- **[Odometry motion model](/odometry-motion-model/).** Uses the motion that the wheel encoders measured, as a rotation, a translation and a rotation, instead of the command. Thrun, Burgard and Fox (2005) note that odometry is usually more accurate than the commanded velocities, so the odometry model is the usual choice for localization when encoders exist. The velocity model is the one available for planning and for robots without encoders.
- **[Unicycle model](/unicycle-model/) and [differential drive model](/differential-drive-model/).** The noise-free output equations are the exact solution of the unicycle equations $\dot x = v\cos\theta$, $\dot y = v\sin\theta$, $\dot\theta = \omega$ with constant $v$ and $\omega$. A differential drive maps its two wheel speeds to $(v, \omega)$.
- **[Kinematic bicycle model](/kinematic-bicycle-model/).** Also moves on arcs under constant inputs, but its curvature is bounded by the steering limit, and its input is a steering angle, not $\omega$.
- **[EKF localization](/ekf-localization/).** Linearizes the output equations around the command. The noise of $(\hat v, \hat\omega)$ is mapped into pose space by the Jacobian of the output equations with respect to the control.
- **[Dead reckoning](/dead-reckoning/).** Integrating the noise-free output equations step by step is dead reckoning from commands.

## Known results in the model

- **Theorem (why the final rotation is needed).** Without $\hat\gamma$, the end pose depends on only two random numbers, $\hat v$ and $\hat\omega$, so it lies on a two-dimensional surface in the three-dimensional pose space. On that surface the heading is fixed by the position: the chord from $(x, y)$ to $(x', y')$ has the direction $\theta + \hat\omega\Delta t / 2$, so $\theta' = 2\varphi - \theta$, where $\varphi$ is the direction of the chord (for $\hat v > 0$, modulo $2\pi$). The distribution of $x_t$ then has no density, and every pose off the surface has probability zero, however close it is to the surface. The term $\hat\gamma$ gives the end pose a density in all three coordinates. In the example the chord direction is $\operatorname{atan2}(0.24483, 0.95885) = 0.25 = \omega\Delta t / 2$.
- **Theorem (change of variables).** For fixed $x_{t-1}$, the map $(\hat v, \hat\omega, \hat\gamma) \mapsto (x', y', \theta')$ has a Jacobian determinant of absolute value $|\hat v|\, \Delta t^2 (1 - \cos \hat\omega\Delta t) / \hat\omega^2$. Proof: $\hat\gamma$ enters only $\theta'$, with coefficient $\Delta t$, so the determinant is $\Delta t$ times the $2 \times 2$ determinant of $(x', y')$ with respect to $(\hat v, \hat\omega)$. After a rotation to $\theta = 0$, with $a = \hat\omega \Delta t$, the position is $(\hat v/\hat\omega)(\sin a,\ 1 - \cos a)$, and a direct computation gives that determinant as $\hat v \Delta t (\sin^2 a + \cos^2 a - \cos a)/\hat\omega^2 = \hat v \Delta t (1 - \cos a)/\hat\omega^2$. Hence $p_1 p_2 p_3$ is a density over the controls, and the density over poses is $p_1 p_2 p_3$ divided by this factor. In the example the factor is $(1 - \cos 0.5)/0.25 \approx 0.12242/0.25 \approx 0.48967$, and the pose density at the noise-free end pose is about $45.432 / 0.48967 \approx 92.78$. The factor tends to $|\hat v| \Delta t^4 / 2$ as $\hat\omega \to 0$ and is zero for $\hat v = 0$, where the position does not depend on $\hat\omega$.
- **The sign of the velocity.** With the unsigned radius $r^* = \sqrt{(x - x^*)^2 + (y - y^*)^2}$, the formula $\hat v = (\Delta\theta / \Delta t)\, r^*$ gives $\hat v$ the sign of $\hat\omega$, which is wrong whenever $v$ and $\omega$ have opposite signs. For example, a robot at $(0, 0, 0)$ that drives forward with $v = 0.8$ and turns right with $\omega = -0.4$ gets $\hat v = -0.8$ from that formula, and one that backs up with $v = -1$, $\omega = 0.5$ ends at $(-0.95885, -0.24483, 0.5)$ and gets $\hat v = 1$. The signed radius $r_s$ above, the position of the center to the left of the start heading, fixes this.
- **Degenerate cases.** The denominator of $\mu$ is zero when the end position lies on the line of the start heading. Then the motion is straight, $\hat\omega = 0$, and $\hat v$ is the signed distance along the heading divided by $\Delta t$. When the end position equals the start position, $\hat v = 0$ and $\hat\omega$ is not determined by the positions. The closed form must handle both cases on their own, and the wrap of $\Delta\theta$ assumes $|\hat\omega \Delta t| < \pi$.
- **Heuristic (fitting the alphas).** The alphas are fitted to data, for example by driving fixed commands and matching the spread of the end poses. The Gaussian shape, the constant velocity over $\Delta t$ and the independence of the errors over time are modeling choices.

## References
