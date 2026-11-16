---
tag: VZFKY9
kind: model
slug: linear-inverted-pendulum-model
name: Linear inverted pendulum model
aliases:
- LIPM
- LIP model
area: robotics/mobile-and-legged-robots
level: core
summary: "A point mass at constant height over a massless leg; its horizontal motion is linear, x'' = (g / z0) (x - p), and the ZMP p is the input."
prereqs: [zero-moment-point]
see_also: [capture-point, zmp-preview-control, center-of-pressure, spring-loaded-inverted-pendulum, centroidal-dynamics, footstep-planning, matrix-exponential, hamiltonian-systems]
sources:
  - paper: doi:10.1109/IROS.2001.973365
    title: Shuuji Kajita, Fumio Kanehiro, Kenji Kaneko, Kazuhito Yokoi and Hirohisa Hirukawa, The 3D linear inverted pendulum mode, a simple modeling for a biped walking pattern generation, IEEE/RSJ International Conference on Intelligent Robots and Systems, 2001
    locator: volume 1, pages 239 to 246
  - book: isbn:9783642545351
    title: Shuuji Kajita, Hirohisa Hirukawa, Kensuke Harada and Kazuhito Yokoi, Introduction to Humanoid Robotics, Springer Tracts in Advanced Robotics 101, Springer, 2014
    locator: Chapter 4 (biped walking)
  - paper: doi:10.1109/TRO.2015.2405592
    title: Johannes Englsberger, Christian Ott and Alin Albu-Schäffer, Three-dimensional bipedal walking control based on divergent component of motion, IEEE Transactions on Robotics 31(2), 2015
    locator: pages 355 to 368
  - paper: doi:10.1109/ICHR.2006.321385
    title: Jerry Pratt, John Carff, Sergey Drakunov and Ambarish Goswami, Capture point, a step toward humanoid push recovery, IEEE-RAS International Conference on Humanoid Robots, 2006
    locator: pages 200 to 207
---

The linear inverted pendulum model (LIPM) describes a walking robot as a point mass on a massless leg that can change its length. The leg keeps the mass at a constant height $z_0$, and then the horizontal motion of the mass obeys a linear equation, $\ddot x = \omega^2 (x - p)$ with $\omega = \sqrt{g / z_0}$, where $p$ is the foot point or, for a flat foot, the [zero moment point](/zero-moment-point/). Because it is linear, it has a closed form solution, a conserved energy and a simple split into a stable and an unstable part. Most ZMP based walking pattern generators, including [ZMP preview control](/zmp-preview-control/), and the [capture point](/capture-point/) are built on it.

## The machine

**State.** The position and velocity of the center of mass (CoM) in the horizontal plane, $(x, y, \dot x, \dot y)$, in meters and meters per second. The height is fixed: $z = z_0$ above the ground.

**Input.** The point $p = (p_x, p_y)$ on the ground through which the leg force acts. For a point foot it is the foot; for a flat foot it is the [center of pressure](/center-of-pressure/), which the ankle torque moves. It must stay in the [support polygon](/support-polygon/).

**Parameters.** The height $z_0 > 0$ in meters and gravity $g = 9.81$ m/s² along $-z$. The mass $m$ does not appear in the motion. The time constant is $1 / \omega$ with $\omega = \sqrt{g / z_0}$; for $z_0 = 1$ m, $\omega = 3.13209$ 1/s.

**Equations.** The leg pushes along the line from $p$ to the CoM, with a force $f = \lambda (c - p)$ where $\lambda \ge 0$. A constant height needs $\lambda z_0 = m g$, so $\lambda = m g / z_0$ and the leg force has size $m g \ell / z_0$ for a leg of length $\ell$. The horizontal parts of Newton's law are then

$$\ddot x = \omega^2 (x - p_x), \qquad \ddot y = \omega^2 (y - p_y).$$

The two axes are independent, so most analysis uses one axis.

**Assumptions.** The ground is flat and the foot does not slip. The robot has no angular momentum about its CoM, or its rate of change is zero. The height is constant; Kajita et al. (2001) also allow a sloped constraint plane $z = k_x x + k_y y + z_0$, and the equations stay linear. Real robots match these assumptions only in part: the legs have mass, the CoM height changes during a step, and the upper body rotates. The model is a template, not a description of a particular robot.

## What it counts

The model predicts the CoM motion for a given ZMP path, and the ZMP for a given CoM motion:

$$p = x - \frac{\ddot x}{\omega^2}.$$

This second form is the point mass formula of the [zero moment point](/zero-moment-point/) with $\ddot z = 0$. A walking pattern generator uses it in one of the two directions: it chooses $p(t)$ in the feet and solves for $x(t)$, or it chooses $x(t)$ and checks that $p(t)$ is in the feet.

## Relation to other models

- **The cart-table model** is the same equation written with the CoM jerk as the input and $p$ as the output. [ZMP preview control](/zmp-preview-control/) uses this form.
- **The full inverted pendulum** of fixed length $\ell$ has $\ddot \theta = (g / \ell) \sin \theta$ and a height that changes with the angle. The LIPM replaces the fixed length by a leg that changes its length to keep the height, which makes the equation linear without a small angle assumption.
- **The [spring-loaded inverted pendulum](/spring-loaded-inverted-pendulum/)** has a leg spring and a height that changes. It describes running and the bouncing of the CoM in walking, and its stance phase has no closed form.
- **[Centroidal dynamics](/centroidal-dynamics/)** is the exact model of the total momentum of a robot. The LIPM is the special case with a constant height and no change of angular momentum.
- **Models with a flywheel** add a body inertia with a torque about the CoM. The torque moves the effective $p$ beyond the foot for a short time.

## Known results in the model

**Closed form solution.** For a constant input $p$, with $x(0) = x_0$ and $\dot x(0) = \dot x_0$,

$$x(t) = p + (x_0 - p) \cosh(\omega t) + \frac{\dot x_0}{\omega} \sinh(\omega t), \qquad \dot x(t) = (x_0 - p)\, \omega \sinh(\omega t) + \dot x_0 \cosh(\omega t).$$

This follows from the linear equation, and it is the [matrix exponential](/matrix-exponential/) of $\begin{pmatrix} 0 & 1 \\ \omega^2 & 0 \end{pmatrix}$ applied to the state. A walking gait is a sequence of such pieces, one for each step, joined at the step times.

**Orbital energy.** For a constant $p$, the quantity

$$E = \frac{\dot x^2}{2} - \frac{\omega^2 (x - p)^2}{2}$$

is constant, because $\dot E = \dot x \ddot x - \omega^2 (x - p) \dot x = 0$. Kajita et al. (2001) call it the orbital energy. If $E > 0$, the mass passes over $p$ and goes on. If $E < 0$, it stops before $p$ and falls back. If $E = 0$ and the mass moves toward $p$, it comes to rest over $p$ as $t \to \infty$.

**Stable and unstable parts.** Let $\xi = x + \dot x / \omega$ and $\zeta = x - \dot x / \omega$. Then

$$\dot \xi = \omega (\xi - p), \qquad \dot \zeta = -\omega (\zeta - p).$$

The part $\zeta$ converges to $p$ and $\xi$ moves away from $p$ at the rate $e^{\omega t}$. So the model is a saddle with eigenvalues $\pm \omega$, and only $\xi$ needs control. $\xi$ is the [capture point](/capture-point/) of Pratt et al. (2006), and Englsberger et al. (2015) call it the divergent component of motion. The condition $E = 0$ with motion toward $p$ is the same as $\xi = p$.

**An example.** Take $z_0 = 1$ m, $\omega = 3.13209$ 1/s, $x_0 = 0$ and $\dot x_0 = 0.5$ m/s. Then $\xi = 0 + 0.5 / 3.13209 = 0.15964$ m.

| foot point $p$ | $x(0.2)$ | $\dot x(0.2)$ | $x(0.5)$ | $\dot x(0.5)$ | $x(1.0)$ | $\dot x(1.0)$ |
|---|---|---|---|---|---|---|
| $0$ | 0.1067 | 0.6014 | 0.3655 | 1.2491 | 1.8261 | 5.7414 |
| $0.15964$ (equal to $\xi$) | 0.0743 | 0.2673 | 0.1263 | 0.1044 | 0.1527 | 0.0218 |

With the foot under the CoM, the mass speeds up and falls. With the foot at $\xi$, it slows down and comes to rest over the foot, since $x(t) = p (1 - e^{-\omega t})$. With $p = 0.1$, which is behind $\xi$, $E = 0.125 - 9.81 \cdot 0.01 / 2 = 0.07595$ m²/s², so the mass passes over the foot with speed $\sqrt{2E} = 0.3897$ m/s.

**Linear tools apply.** The model is linear and time invariant, so its exact discretization gives a linear state space model, and linear quadratic control and model predictive control apply to it with no approximation of the model itself. ZMP preview control (Kajita et al., 2003) and the linear MPC of Wieber (2006) are examples. Their optimality holds for the LIPM, not for the robot.

## References
