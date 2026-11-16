---
tag: GMBREF
kind: model
slug: omnidirectional-robot-kinematics
name: Omnidirectional wheeled robot kinematics
aliases:
- mecanum wheel kinematics
- omniwheel kinematics
area: robotics/mobile-and-legged-robots
level: core
summary: The map from the speeds of omni or mecanum wheels to the planar twist of the chassis, which can move in any direction.
prereqs: [rigid-body-twist, unicycle-model]
see_also: [differential-drive-model, unicycle-model, kinematic-bicycle-model, nonholonomic-constraint, instant-center-of-velocity, odometry-motion-model, dead-reckoning, degrees-of-freedom-analysis]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 13.2 (omnidirectional wheeled mobile robots: omniwheels and mecanum wheels, the map from the chassis twist to the wheel speeds) and Section 13.4 (odometry)"
  - paper: doi:10.1109/70.481750
    title: "Guy Campion, Georges Bastin and Brigitte d'Andréa-Novel, Structural properties and classification of kinematic and dynamic models of wheeled mobile robots, IEEE Transactions on Robotics and Automation 12(1), 47-62, 1996"
    locator: "the degree of mobility and the degree of steerability, and the five classes of wheeled robots, with the omnidirectional class (3,0)"
  - book: isbn:9780262015356
    title: "Roland Siegwart, Illah R. Nourbakhsh and Davide Scaramuzza, Introduction to Autonomous Mobile Robots, 2nd edition, MIT Press, 2011"
    locator: "Section 3.2.3 (wheel kinematic constraints, including the Swedish wheel) and Section 3.3 (mobile robot maneuverability)"
  - paper: "Bengt Erland Ilon, US Patent 3,876,255, 1975"
    title: Wheels for a course stable selfpropelling vehicle movable in any desired direction on the ground or some other base
    locator: the mecanum wheel, with free rollers on its rim at 45 degrees to the wheel axis
---

An omnidirectional wheeled robot can move in any direction in the plane and turn at the same time, with no need to turn first. Its wheels have free rollers on the rim. An omniwheel has rollers whose axes are tangent to the rim, so the wheel drives along its own plane and slides freely along its axle. A mecanum wheel, invented by Bengt Ilon in the 1970s, has rollers at 45 degrees, so it drives along one direction and slides freely along another. With three or more such wheels in a suitable layout, the wheel speeds and the planar twist of the chassis, two linear velocities and one angular velocity, are related by a linear map of rank 3. So the chassis has three independent velocity inputs and no [nonholonomic constraint](/nonholonomic-constraint/), unlike the [unicycle](/unicycle-model/) and the [differential drive](/differential-drive-model/), which cannot move along their wheel axle.

## The machine

**State.** The chassis pose $(x, y, \theta)$ in the world frame, in meters and radians. For odometry, add the wheel angles.

**Velocities.** The body twist $\mathcal{V}_b = (\omega, v_x, v_y)$: the turning rate (rad/s) and the velocity of the chassis origin in the chassis frame (m/s). The world velocities are $\dot\theta = \omega$ and $(\dot x, \dot y) = R(\theta)\,(v_x, v_y)$, with $R(\theta)$ the rotation by $\theta$.

**Parameters of wheel $i$.** In the chassis frame: the position $(x_i, y_i)$ of the wheel center (m), the driving direction $\beta_i$ (the direction in which the wheel center moves when the wheel turns and the rollers do not), the radius $r_i$ (m), and the angle $\gamma_i$ between the free sliding direction of the rollers and the wheel axle. For an omniwheel $\gamma_i = 0$; for a mecanum wheel $\gamma_i = \pm 45°$.

**Inputs.** The wheel speeds $u_i$ (rad/s).

**Equations.** The wheel center moves with the chassis at $(v_x - \omega y_i,\ v_y + \omega x_i)$. The rollers absorb any velocity along the free direction. The component along the unit vector at angle $\beta_i + \gamma_i$, which is normal to the free direction, must come from the turning wheel, which gives $r_i u_i \cos\gamma_i$ along it. So

$$u_i = \frac{1}{r_i\cos\gamma_i}\Bigl(\cos(\beta_i + \gamma_i)\,(v_x - \omega y_i) + \sin(\beta_i + \gamma_i)\,(v_y + \omega x_i)\Bigr),$$

and for $m$ wheels $u = H\,\mathcal{V}_b$ with the $m \times 3$ matrix $H$ whose row $i$ is $\frac{1}{r_i\cos\gamma_i}\bigl(x_i\sin(\beta_i + \gamma_i) - y_i\cos(\beta_i + \gamma_i),\ \cos(\beta_i + \gamma_i),\ \sin(\beta_i + \gamma_i)\bigr)$. This is the form of Lynch and Park (Section 13.2), written in this page's notation.

**Standing assumptions.** Flat floor, rigid chassis, point contacts. Each wheel rolls without slip in the direction normal to its free direction, and the rollers turn with no resistance. A mecanum wheel touches the floor through one roller at a time, which makes the contact point move a little; the model ignores this. The wheel speeds are inputs: no motor or chassis dynamics.

## What it counts

**Inverse kinematics.** For a desired twist, $u = H\mathcal{V}_b$ gives the wheel speeds directly. This is the map a controller uses.

**Forward kinematics.** If $H$ has rank 3, the twist is determined by the wheel speeds. With three wheels, $\mathcal{V}_b = H^{-1}u$. With $m > 3$ wheels, only wheel speeds in the column space of $H$ are consistent; other values make wheels slip. Odometry then uses the least squares estimate $\mathcal{V}_b = H^{+}u$, with $H^{+}$ the pseudoinverse.

**Three omniwheels.** Place three omniwheels at distance $D$ from the center, at angles $\alpha_i = 0, 2\pi/3, 4\pi/3$, with driving directions tangent to the circle, $\beta_i = \alpha_i + \pi/2$, and $\gamma_i = 0$. Row $i$ of $H$ is $\frac{1}{r}(D,\ -\sin\alpha_i,\ \cos\alpha_i)$. With $r = 0.05$ m and $D = 0.2$ m: the twist $(\omega, v_x, v_y) = (0, 0.3, 0)$ needs $u = (0, -5.196, 5.196)$ rad/s; $(0, 0, 0.3)$ needs $(6, -3, -3)$; and turning on the spot at 1 rad/s needs $(4, 4, 4)$. The matrix is invertible, so every twist is possible.

**Four mecanum wheels.** Place four mecanum wheels at $(\pm a, \pm b)$, all driving along the chassis $x$ axis, $\beta_i = 0$. With $\gamma = -45°$ on the front left and rear right wheels and $+45°$ on the other two, the rows reduce to the common formulas

$$u_{FL} = \tfrac{1}{r}(v_x - v_y - c\,\omega), \quad u_{FR} = \tfrac{1}{r}(v_x + v_y + c\,\omega), \quad u_{RL} = \tfrac{1}{r}(v_x + v_y - c\,\omega), \quad u_{RR} = \tfrac{1}{r}(v_x - v_y + c\,\omega),$$

with $c = a + b$. With $r = 0.05$ m, $a = 0.2$ m and $b = 0.15$ m:

- Sideways at $v_y = 0.5$ m/s: $u = (-10, 10, 10, -10)$ rad/s. The two diagonals turn in opposite directions.
- The twist $(\omega, v_x, v_y) = (0.5, 0.3, 0.2)$: $u = (-1.5, 13.5, 6.5, 5.5)$ rad/s.
- Back from the wheel speeds: $v_x = r(u_{FL} + u_{FR} + u_{RL} + u_{RR})/4 = 0.3$, $v_y = r(-u_{FL} + u_{FR} + u_{RL} - u_{RR})/4 = 0.2$ and $\omega = r(-u_{FL} + u_{FR} - u_{RL} + u_{RR})/(4c) = 0.5$.
- Consistency: every valid set of wheel speeds has $u_{FL} + u_{FR} - u_{RL} - u_{RR} = 0$. The speeds $(10, 0, 0, 0)$ break it (the sum is 10), so the wheels must slip; the least squares twist is $(\omega, v_x, v_y) = (-0.357, 0.125, -0.125)$.

**Pose.** For a twist that is constant in the chassis frame over a time $t$, the chassis moves on a circular arc about the [instant center](/instant-center-of-velocity/) at $(-v_y/\omega,\ v_x/\omega)$ in the chassis frame, or on a line if $\omega = 0$. The pose update is exact, as for the unicycle. A robot that must move on a straight line while it turns needs a body twist that changes with $\theta$.

## Relation to other models

- **[Differential drive](/differential-drive-model/) and [unicycle](/unicycle-model/).** Their fixed standard wheels forbid motion along the axle. That removes one column of freedom: the chassis twist must satisfy one linear constraint, and the reachable twists form a plane, not all of $\mathbb{R}^3$.
- **[Kinematic bicycle model](/kinematic-bicycle-model/).** Steered standard wheels: the set of twists depends on the steering angle, and changing it takes time.
- **The classification of Campion, Bastin and d'Andréa-Novel.** They describe a wheeled robot by its degree of mobility $\delta_m$, the dimension of the set of allowed twists for fixed steering angles, and its degree of steerability $\delta_s$, the number of steering angles it can set independently. The five classes are $(\delta_m, \delta_s) = (3, 0)$, $(2, 0)$, $(2, 1)$, $(1, 1)$ and $(1, 2)$. Robots with omni or mecanum wheels and no steering are type (3,0), the only class with every twist allowed at every instant. The differential drive is type (2,0) and a car is type (1,1).
- **[Odometry](/odometry-motion-model/).** The forward map gives the twist from wheel encoders. Mecanum wheels slip more than standard wheels, so their odometry drifts faster; this is a heuristic observation, not a property of the model.

## Known results in the model

- **When the robot is omnidirectional (theorem).** The chassis can follow every twist if and only if $H$ has rank 3. This needs at least three wheels, $\cos\gamma_i \ne 0$ for each wheel (a wheel whose free direction is its driving direction cannot drive), and a layout in which the rows of $H$ are independent. For three omniwheels it fails when the three driving lines meet in one point, because a rotation about that point gives every wheel a zero speed, so the wheels can neither produce nor measure it. It also fails when the three driving directions are parallel.
- **A wrong mecanum layout (theorem).** If all four mecanum wheels have the same $\gamma = +45°$, then $\tan\gamma = 1$ for each row, the columns of $v_x$ and $v_y$ in $H$ are equal, and $H$ has rank 2. The robot then cannot separate forward and sideways motion. Mecanum wheels come in left-handed and right-handed versions, and four wheels of the same hand give this case. One wheel of the wrong hand keeps the rank at 3 but changes the map, so the robot moves in unexpected directions.
- **Holonomic chassis, nonholonomic wheels (theorem).** The chassis twist has no constraint, so robots of type (3,0) are often called holonomic. With the wheel angles in the state, the rolling constraints do not integrate in general. For the three-omniwheel robot: drive 1 m along world $x$ at $\theta = 0$, turn by $\pi/2$, drive back 1 m, and turn back. The chassis returns to its start pose, but wheel 1 has turned by $1/r$ rad in total. So the wheel angles are not functions of the pose.
- **Kinematic redundancy.** With $m > 3$ wheels, the null space of $H^T$ has dimension $m - 3$. Wheel speeds in it make the wheels fight each other with no net motion, which a controller must avoid.

## References
