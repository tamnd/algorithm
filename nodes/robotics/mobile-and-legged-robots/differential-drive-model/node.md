---
tag: SNKBY0
kind: model
slug: differential-drive-model
name: Differential-drive model
aliases:
- differential-drive kinematics
area: robotics/mobile-and-legged-robots
level: intro
summary: Two independently driven wheels on one axle, whose wheel speeds map to the forward and turning speeds of a unicycle.
prereqs: [unicycle-model]
see_also: [unicycle-model, nonholonomic-constraint, instant-center-of-velocity, odometry-motion-model, dead-reckoning, kinematic-bicycle-model, omnidirectional-robot-kinematics, dynamic-window-approach]
sources:
  - book: isbn:9780262015356
    title: "Roland Siegwart, Illah R. Nourbakhsh and Davide Scaramuzza, Introduction to Autonomous Mobile Robots, 2nd edition, MIT Press, 2011"
    locator: "Section 3.2 (kinematic models and constraints: forward kinematic models, wheel kinematic constraints and the differential-drive example)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 13.3.1 (the differential-drive robot and its map to the unicycle) and Section 13.4 (odometry)"
  - book: isbn:9780521862059
    title: "Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006"
    locator: "Section 13.1.2 (the differential drive among the kinematic models of wheeled systems)"
---

The differential-drive model gives the motion of a robot with two drive wheels on one axle, each with its own motor, and passive casters for balance. It maps the two wheel speeds to the forward speed and the turning rate of the midpoint of the axle. Equal speeds drive straight, unequal speeds turn, and opposite speeds turn on the spot. Most indoor mobile robots and robot vacuum cleaners use this drive. The map from wheel speeds to $(v, \omega)$ is linear and invertible, so the robot moves exactly as the [unicycle model](/unicycle-model/): the unicycle has $v$ and $\omega$ as inputs, and this page adds the wheel geometry, the wheel speed limits and the wheel angles that encoders measure.

## The machine

**Parameters.** The wheel radius $r$ (m), the same for both wheels, and the half distance $d$ (m) between the wheel contact points, so the wheels are $2d$ apart.

**State.** The pose $(x, y, \theta)$ of the midpoint of the axle. For odometry, add the wheel angles $\varphi_R$ and $\varphi_L$ (rad).

**Inputs.** The wheel angular speeds $\omega_R = \dot\varphi_R$ and $\omega_L = \dot\varphi_L$ (rad/s), positive when the wheel drives the robot forward.

**Equations.**

$$v = \frac{r(\omega_R + \omega_L)}{2}, \qquad \omega = \frac{r(\omega_R - \omega_L)}{2d}, \qquad \dot x = v\cos\theta, \quad \dot y = v\sin\theta, \quad \dot\theta = \omega.$$

The inverse map is $\omega_R = (v + d\omega)/r$ and $\omega_L = (v - d\omega)/r$.

**Constraints.** With the wheel angles in the state, $q = (x, y, \theta, \varphi_R, \varphi_L)$, the model is three [Pfaffian constraints](/pfaffian-constraint/): each wheel rolls without slip along its plane, and neither slips along the axle.

$$\dot x\cos\theta + \dot y\sin\theta + d\dot\theta = r\dot\varphi_R, \qquad \dot x\cos\theta + \dot y\sin\theta - d\dot\theta = r\dot\varphi_L, \qquad \dot x\sin\theta - \dot y\cos\theta = 0.$$

**Standing assumptions.** Rigid body on a flat floor. Coaxial wheels of known, equal radius that roll without slipping in any direction, with a point contact. Casters roll freely and do not resist motion. The wheel speeds are inputs, so motor dynamics, inertia and the friction limit are not in the model.

## What it counts

The model predicts the pose for given wheel speeds, and, from encoder counts, the pose change for given wheel rotations.

**Turning radius.** For $\omega_R \ne \omega_L$, the instantaneous center of rotation is on the line of the axle, at the signed distance $R = v / \omega = d(\omega_R + \omega_L)/(\omega_R - \omega_L)$ from the midpoint, to the left when $R > 0$. It is the [instant center of velocity](/instant-center-of-velocity/) of the chassis. For $\omega_R = -\omega_L$, $R = 0$ and the robot turns on the spot.

**Exact pose update.** For wheel speeds that are constant over a time $t$, the pose moves on an arc of radius $R$ through the angle $\omega t$. The arc formula of the unicycle gives the new pose with no integration error.

**Odometry.** If the encoders report wheel rotations $\Delta\varphi_R$ and $\Delta\varphi_L$ over a sample, the distance traveled by the midpoint is $\Delta s = r(\Delta\varphi_R + \Delta\varphi_L)/2$ and the change of heading is $\Delta\theta = r(\Delta\varphi_R - \Delta\varphi_L)/(2d)$. Under the assumption that each wheel speed was constant during the sample, the motion was an arc of length $\Delta s$, and the pose update is exact. This is [dead reckoning](/dead-reckoning/); the [odometry motion model](/odometry-motion-model/) adds noise to it.

**Worked example.** Take $r = 0.05$ m and $2d = 0.30$ m. With $\omega_R = 12$ rad/s and $\omega_L = 8$ rad/s, $v = 0.05 \cdot 20 / 2 = 0.5$ m/s and $\omega = 0.05 \cdot 4 / 0.30 = 0.6667$ rad/s, so $R = 0.75$ m. After 1 s from $(0, 0, 0)$ the pose is $(0.75\sin\frac23,\ 0.75(1 - \cos\frac23),\ \frac23) = (0.4638, 0.1606, 0.6667)$. To drive at $v = 0.3$ m/s with $\omega = 1$ rad/s, set $\omega_R = (0.3 + 0.15)/0.05 = 9$ rad/s and $\omega_L = 3$ rad/s.

**Speed limits.** If each wheel speed is bounded by $|\omega_{R}|, |\omega_L| \le \Omega$, the reachable pairs are the diamond $|v|/(r\Omega) + d|\omega|/(r\Omega) \le 1$. In the example with $\Omega = 20$ rad/s, the top speed is 1 m/s when driving straight and the top turning rate is 6.667 rad/s when turning on the spot, but not both at once. Planners such as the [dynamic window approach](/dynamic-window-approach/) search inside this region.

**Calibration.** The heading from odometry is inversely proportional to the value of $d$ that the robot uses. If that value is 1% smaller than the true one, a full turn on the spot is measured as $2\pi / 0.99$, an error of 3.6 degrees, and every later position inherits it. Errors in $d$ and in the ratio of the two wheel radii are the usual systematic odometry errors. This is a heuristic statement about real robots; the model itself has no error.

The model does not predict wheel slip, which happens on hard acceleration, on smooth floors and when a caster sticks.

## Relation to other models

- **[Unicycle model](/unicycle-model/).** The same paths, with $(v, \omega)$ as inputs. Every result about the unicycle holds here through the invertible map above.
- **Skid steering.** Tracked vehicles and four-wheel robots with fixed wheels on each side also use left and right speeds. They must slip to turn, so the effective value of $d$ is larger than the geometric one and depends on the floor. The differential-drive equations with a fitted $d$ are a common approximation.
- **[Kinematic bicycle model](/kinematic-bicycle-model/).** A car cannot turn on the spot; its turning radius is bounded below. A differential drive has no such bound.
- **[Omnidirectional robot](/omnidirectional-robot-kinematics/).** Wheels with rollers remove the constraint along the axle, so the chassis can move sideways.
- **Classification.** In the classification of Campion, Bastin and d'Andréa-Novel (1996), the differential drive has degree of mobility 2 and degree of steerability 0, type (2,0), as does the unicycle.

## Known results in the model

- **The wheel angles are partly holonomic (theorem).** Subtract the first two constraints: $2d\dot\theta = r(\dot\varphi_R - \dot\varphi_L)$. This integrates to $\theta - r(\varphi_R - \varphi_L)/(2d) = $ const. So the heading is a function of the wheel angles, and the reachable set in the five variables has dimension 4. The other two constraints are [nonholonomic](/nonholonomic-constraint/): the robot can reach any position and heading, with the wheel angle sum free.
- **Controllability and stabilization (theorems).** As for the unicycle: controllable by the [Lie algebra rank condition](/lie-algebra-rank-condition/), with no continuous time-invariant feedback that stabilizes a pose, by [Brockett's condition](/brockett-condition/).
- **Time-optimal paths (theorem).** With bounded wheel speeds, the fastest paths between two poses are made of turns on the spot and straight lines, with both wheels at full speed, and there is a finite list of their types. Balkcom and Mason found this structure in 2002.
- **Odometry error grows without bound (theorem in the noisy model).** With independent noise on each wheel increment, the variance of the heading grows linearly with the distance, and the position error grows faster. So odometry needs a correction from outside, as in a localization filter.

## References
