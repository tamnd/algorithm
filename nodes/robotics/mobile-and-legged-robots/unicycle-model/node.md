---
tag: HFTPYZ
kind: model
slug: unicycle-model
name: Unicycle model
aliases:
- unicycle kinematics
area: robotics/mobile-and-legged-robots
level: intro
summary: A planar robot with pose x, y, theta that moves forward at speed v along its heading and turns at rate w. It is the simplest nonholonomic system and the base of most wheeled-robot models.
prereqs: [configuration-space]
see_also: [differential-drive-model, kinematic-bicycle-model, nonholonomic-constraint, brockett-condition, lie-algebra-rank-condition, differential-flatness, velocity-motion-model, dubins-path]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 13.3.1 (the unicycle and the canonical model of nonholonomic wheeled robots), Section 13.3.2 (controllability), Section 13.3.3 (motion planning) and Section 13.3.4 (feedback control)"
  - book: isbn:9780521862059
    title: "Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006"
    locator: "Section 13.1.2 (kinematics of the simple car, the differential drive and the unicycle) and Sections 15.3 to 15.5 (optimal paths, nonholonomic system theory and steering methods)"
  - book: isbn:9783540762195
    title: "Jean-Paul Laumond (editor), Robot Motion Planning and Control, Lecture Notes in Control and Information Sciences 229, Springer, 1998"
    locator: "the chapters on nonholonomic motion planning and on feedback control of a nonholonomic car-like robot"
---

The unicycle model is the kinematic model of a body that moves in the plane, can only go forward or backward along its heading, and can turn. Its state is the pose $(x, y, \theta)$, and its inputs are the forward speed $v$ and the turning rate $\omega$: $\dot x = v\cos\theta$, $\dot y = v\sin\theta$, $\dot\theta = \omega$. For a control reader, it is the standard example of a driftless [control-affine system](/control-affine-system/) with two inputs and three states. It is [controllable](/controllability/) by the [Lie algebra rank condition](/lie-algebra-rank-condition/), its Jacobian linearization at rest is not controllable, it fails [Brockett's condition](/brockett-condition/), so no continuous time-invariant feedback stabilizes a pose, and it is [differentially flat](/differential-flatness/) with the position as flat output. The no-sideways-slip condition behind it is a [nonholonomic constraint](/nonholonomic-constraint/). The [differential-drive model](/differential-drive-model/) is the same motion written with the two wheel speeds as inputs; the unicycle uses $v$ and $\omega$ directly.

## The machine

**State.** The pose $q = (x, y, \theta) \in \mathbb{R}^2 \times S^1$: the position of a reference point in meters and the heading in radians, measured from the $x$ axis and wrapped to $[-\pi, \pi)$. For a wheeled robot the reference point is on the wheel axle, for example the midpoint between two drive wheels.

**Inputs.** The forward speed $v$ in m/s and the turning rate $\omega$ in rad/s. Either can be negative.

**Equations.**

$$\dot q = \begin{bmatrix} \cos\theta \\ \sin\theta \\ 0 \end{bmatrix} v + \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \omega = g_1(q)\, v + g_2(q)\, \omega.$$

**Constraint.** The velocity of the reference point has no component along the axle: $\dot x\sin\theta - \dot y\cos\theta = 0$. This is a [Pfaffian constraint](/pfaffian-constraint/), and $g_1$, $g_2$ span its null space.

**Output.** Usually the full pose, or the position $(x, y)$.

**Standing assumptions.** Rigid body on a flat plane. The wheels roll without slipping in any direction, so there is no sideways motion and the forward speed is the rolling speed. The velocities are inputs: mass, inertia, motor torques and friction limits are not in the model. The heading is the direction of motion, so the reference point must be on the axle; a point ahead of the axle moves sideways during a turn.

**Bounds.** A real robot adds bounds such as $|v| \le v_{\max}$ and $|\omega| \le \omega_{\max}$, or a bound on the curvature $|\omega| \le |v| / R_{\min}$. The second bound turns the unicycle into a car: the Dubins car ($v$ = 1, forward only) or the Reeds-Shepp car ($v = \pm 1$).

## What it counts

The model predicts the path of the pose for a given input signal. For constant inputs on an interval of length $t$, the solution is exact. With $\omega \ne 0$, the reference point moves on a circle of radius $v / \omega$ about the instantaneous center:

$$x(t) = x_0 + \frac{v}{\omega}\bigl(\sin(\theta_0 + \omega t) - \sin\theta_0\bigr), \quad y(t) = y_0 - \frac{v}{\omega}\bigl(\cos(\theta_0 + \omega t) - \cos\theta_0\bigr), \quad \theta(t) = \theta_0 + \omega t.$$

With $\omega = 0$ it moves on a line: $x(t) = x_0 + v t\cos\theta_0$ and $y(t) = y_0 + v t\sin\theta_0$. Inputs that are constant over each sample period, as a digital controller gives, therefore produce a path of arcs and lines, and this formula updates the pose exactly.

**Worked example.** From $(0, 0, 0)$ with $v = 1$ m/s and $\omega = 0.5$ rad/s, the radius is 2 m. After $t = 2$ s the pose is $(2\sin 1,\ 2(1 - \cos 1),\ 1) = (1.6829, 0.9194, 1)$. After $t = \pi$ s it is exactly $(2, 2, \pi/2)$, a quarter circle. The forward Euler method with step 0.1 s gives $(1.7056, 0.8771)$ at $t = 2$ s, 4.8 cm from the exact point; with step 0.01 s the error is 0.48 cm. This error is a measurement of the integration method, and it shrinks in proportion to the step. The exact arc has no such error.

The model does not predict slip, skid, tip-over, or the time that motors need to reach a commanded speed. A probabilistic version, which adds noise to $v$ and $\omega$, is the [velocity motion model](/velocity-motion-model/).

## Relation to other models

- **[Differential-drive model](/differential-drive-model/).** Two wheels on one axle. The map $(\omega_R, \omega_L) \mapsto (v, \omega)$ is linear and invertible, so the two models have the same paths. The differential drive adds the wheel geometry and the wheel speed limits.
- **[Kinematic bicycle model](/kinematic-bicycle-model/).** A car with steered front wheels. At the rear axle it is the unicycle with $\omega = v\tan\delta / L$, so the turning rate is tied to the speed and $|\omega| \le |v| / R_{\min}$. It cannot turn on the spot.
- **Dubins and Reeds-Shepp cars.** The unicycle with a fixed speed and a bound on curvature. Their shortest paths are the [Dubins path](/dubins-path/) and the [Reeds-Shepp path](/reeds-shepp-path/).
- **[Omnidirectional robot](/omnidirectional-robot-kinematics/).** Three independent velocity inputs and no nonholonomic constraint. It can move sideways.
- **[Odometry motion model](/odometry-motion-model/)** and **[dead reckoning](/dead-reckoning/).** They integrate measured wheel motion through the same kinematics.
- **Point mass.** The model $\dot x = u_1$, $\dot y = u_2$ ignores the heading. Planners often plan for it and then track the plan with a unicycle controller.

## Known results in the model

All of these are theorems about the equations above.

- **Controllability.** The bracket $[g_1, g_2] = (\sin\theta, -\cos\theta, 0)$ and the fields $g_1$, $g_2$ span $\mathbb{R}^3$ at every pose (the determinant is 1). By the [Lie algebra rank condition](/lie-algebra-rank-condition/) and the Chow-Rashevskii theorem, any pose can reach any other pose, in any time, with unbounded inputs. With $|v| \le v_{\max}$ and $|\omega| \le \omega_{\max}$ the system is still controllable, because it has no drift.
- **The linearization is not controllable.** At a rest pose $(x_0, y_0, \theta_0)$ with $v = \omega = 0$, the [Jacobian linearization](/jacobian-linearization/) is $\dot{\tilde q} = B u$ with $A = 0$ and $B = [g_1(q_0), g_2(q_0)]$, of rank 2. The sideways direction is lost, so linear methods such as LQR cannot park the unicycle.
- **No continuous stabilizing feedback.** The map $(q, v, \omega) \mapsto (v\cos\theta, v\sin\theta, \omega)$ near $(q_0, 0, 0)$ does not reach the velocity $(-\varepsilon\sin\theta_0, \varepsilon\cos\theta_0, 0)$, the sideways direction, for small $\varepsilon \ne 0$: that needs $\omega = 0$ and a heading $\theta_0 \pm \pi/2$, far from $\theta_0$. So [Brockett's condition](/brockett-condition/) fails, and no continuous feedback $u = k(q)$ makes a pose asymptotically stable. Time-varying feedback and discontinuous feedback can.
- **Tracking is easier.** Along a reference path with a forward speed that does not go to zero, the error dynamics have a controllable linearization, and smooth feedback gives local [exponential stability](/exponential-stability/). Path trackers such as [pure pursuit](/pure-pursuit/) and the [Stanley controller](/stanley-controller/) use this, the latter in the bicycle form.
- **Flatness.** The position $(x, y)$ is a flat output: where $v \ne 0$, $\theta = \operatorname{atan2}(\dot y, \dot x)$, $v = \pm\sqrt{\dot x^2 + \dot y^2}$ and $\omega = (\dot x\ddot y - \dot y\ddot x) / (\dot x^2 + \dot y^2)$. A smooth curve in the plane fixes the inputs; see [differential flatness](/differential-flatness/).
- **Shortest paths.** With a bound on curvature and forward motion only, the shortest path between two poses is a Dubins path of at most three arcs and lines (Dubins 1957); with reverse allowed, a Reeds-Shepp path (Reeds and Shepp 1990). Without a bound on curvature, the shortest path in length is turn, line, turn, but the infimum of time with bounded $v$ and $\omega$ is a different problem.
- **Chained form.** For $|\theta| < \pi/2$, a change of coordinates and inputs puts the unicycle into the chained form $\dot z_1 = u_1$, $\dot z_2 = u_2$, $\dot z_3 = z_2 u_1$, which is equivalent to Brockett's nonholonomic integrator. Steering methods with sinusoids and piecewise constant inputs work in that form (LaValle, Section 15.5).

## References
