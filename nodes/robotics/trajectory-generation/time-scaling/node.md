---
tag: CHPQG8
kind: definition
slug: time-scaling
name: Time scaling
aliases:
- time parameterization
area: robotics/trajectory-generation
level: intro
summary: "A function s(t) from time to the path parameter that turns a geometric path into a trajectory."
prereqs: [configuration-space]
see_also: [trajectory-generation-problem, time-optimal-path-parameterization, maximum-velocity-curve, feedrate-scheduling, cubic-polynomial-trajectory, trapezoidal-velocity-profile, path-velocity-decomposition, trajectory-optimization]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Chapter 9, Section 9.1 (definitions of path, time scaling and trajectory), Section 9.2.2 (time scaling a straight-line path) and Section 9.4 (time-optimal time scaling)"
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009"
    locator: "the chapter on trajectory planning (operational space trajectories, path and timing law)"
---

A time scaling says how fast a robot moves along a path that is already fixed. A *path* is a purely geometric curve $\theta(s)$ in the [configuration space](/configuration-space/) of the robot, parameterized by a number $s$ from 0 to 1; it says where the robot goes but not when. A time scaling is a function $s(t)$ that gives, for each time $t$ between 0 and the duration $T$, the point on the path where the robot is. Composing the two gives a *trajectory* $\theta(s(t))$, a position for every time. Splitting a motion this way lets a planner choose the geometry first, for example to avoid obstacles, and the timing second, for example to respect the speed and acceleration limits of the motors. The same idea in machine tools is the [feedrate schedule](/feedrate-scheduling/) along a tool path. This page defines the object; the [trajectory generation problem](/trajectory-generation-problem/) asks for a good one, and [trajectory optimization](/trajectory-optimization/) chooses path and timing together instead.

## Definition

Let $\theta : [0, 1] \to \mathcal C$ be a path in the configuration space $\mathcal C \subseteq \mathbb R^n$, at least twice differentiable. A **time scaling** of duration $T > 0$ is a function

$$s : [0, T] \to [0, 1], \qquad s(0) = 0, \quad s(T) = 1,$$

that is continuous and has a piecewise continuous second derivative. Lynch and Park (Section 9.1) define path, time scaling and trajectory in this way. Most uses also ask that $s$ be nondecreasing, so the robot never backs up along the path; this page assumes it. The **trajectory** defined by the pair is $q(t) = \theta(s(t))$. By the chain rule,

$$\dot q = \theta'(s)\, \dot s, \qquad \ddot q = \theta'(s)\, \ddot s + \theta''(s)\, \dot s^2,$$

where the prime is the derivative in $s$ and the dot the derivative in $t$. So the joint velocities depend on the path tangent and the path speed $\dot s$, and the joint accelerations depend on the path acceleration $\ddot s$ and, through the curvature term $\theta''(s)\dot s^2$, on the square of the path speed. A limit on the joints is therefore a limit on the pair $(s, \dot s)$, which is the reason that time-optimal methods work in the plane of $s$ and $\dot s$, the *phase plane*.

A **rest-to-rest** time scaling has $\dot s(0) = \dot s(T) = 0$. Some texts call $s(t)$ a time parameterization, a path parameterization, or the timing law of the path.

## Examples and non-examples

**Example: polynomial time scalings.** With $\tau = t/T$, the cubic $s = 3\tau^2 - 2\tau^3$ and the quintic $s = 10\tau^3 - 15\tau^4 + 6\tau^5$ are rest-to-rest time scalings. Their peak path speeds are $1.5/T$ and $1.875/T$. See the [cubic](/cubic-polynomial-trajectory/) and [quintic](/quintic-polynomial-trajectory/) pages.

**Example: trapezoidal time scaling.** The [trapezoidal velocity profile](/trapezoidal-velocity-profile/) with distance 1, speed limit $v$ and acceleration limit $a$ for $s$ is a rest-to-rest time scaling.

**Worked example: a straight line in joint space.** Let $\theta(s) = \theta_0 + s\, \Delta$ with $\Delta = (1, 2)$ rad for a two-joint arm, and let each joint have the limits $|\dot q_i| \le 1$ rad/s and $|\ddot q_i| \le 2$ rad/s². Here $\theta'' = 0$, so $\dot q = \Delta \dot s$ and $\ddot q = \Delta \ddot s$. Joint 2 binds both limits: $\dot s \le 0.5$ and $|\ddot s| \le 1$. A trapezoid for $s$ with these limits has the time $1/0.5 + 0.5/1 = 2.5$ s, and both joints arrive together because they share $s$. Joint 1 then moves at most at half its speed limit.

**Example: a curved path.** On a circle of radius $R$ in the plane, $\theta(s) = R(\cos 2\pi s, \sin 2\pi s)$, the term $\theta''(s)\dot s^2$ has length $4\pi^2 R \dot s^2$: even at a constant path speed, the acceleration is not zero. A bound $A$ on the acceleration then caps the path speed at $\dot s \le \sqrt{A/(4\pi^2 R)}$ everywhere. This is the simplest case of the [maximum velocity curve](/maximum-velocity-curve/).

**Example, not rest to rest: linear time scaling.** $s(t) = t/T$ is a time scaling, but its path speed jumps from 0 to $1/T$ at the start if the robot was at rest. It is useful only as part of a larger motion.

**Non-example: overshoot.** A cubic in $s$ with large end velocities can leave $[0, 1]$. The function is no longer a time scaling, because $\theta(s)$ is not defined outside $[0, 1]$, or the robot leaves the path.

**Non-example: unsynchronized joints.** If each joint of the straight-line example runs its own fastest trapezoid, joint 1 finishes after $1.5$ s and joint 2 after $2.5$ s. The motion is a trajectory, but it is not $\theta(s(t))$ for the straight line, and the robot leaves the line.

**Non-example: backing up.** A function $s$ that decreases on some interval makes the robot move backward along the path. It is a reparameterization, but not a time scaling in the usual sense.

## Related definitions

- **Path and trajectory.** A path is geometric; a trajectory is a position as a function of time. A time scaling turns one into the other. The [trajectory generation problem](/trajectory-generation-problem/) asks for a trajectory.
- **Phase plane and maximum velocity curve.** Joint limits become limits in the plane of $(s, \dot s)$. The [maximum velocity curve](/maximum-velocity-curve/) is the largest $\dot s$ for which some admissible $\ddot s$ exists.
- **Time-optimal path parameterization.** The fastest time scaling of a fixed path under the joint limits is the subject of [time-optimal path parameterization](/time-optimal-path-parameterization/) (Lynch and Park, Section 9.4).
- **Feedrate.** In machining, the speed of the tool along its path; a feedrate schedule is a time scaling by arc length. See [feedrate scheduling](/feedrate-scheduling/).
- **Path-velocity decomposition.** The same split of geometry and timing, used to avoid moving obstacles: plan the path among static obstacles, then the time scaling among moving ones. See [path-velocity decomposition](/path-velocity-decomposition/).
- **Arc-length parameterization.** A path parameterized by its arc length has $\|\theta'(s)\| = 1$, so $\dot s$ is the actual speed. Many feedrate methods use this form; robot joint paths often do not.

## References
