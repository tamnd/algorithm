---
tag: RC03NN
kind: algorithm
slug: pure-pursuit
name: Pure pursuit
aliases:
- pure pursuit path tracking
area: robotics/mobile-and-legged-robots
level: intro
summary: Steers along the circular arc that meets the path at a lookahead distance ahead of the vehicle.
model: real-ram
complexity:
  vars: {n: "the number of vertices of the path polyline; the bounds are for one control step"}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {deterministic: true, randomized: false, online: true, exact: false}
history:
  year: 1992
  people: [R. Craig Coulter]
  note: Pure pursuit came from the road-following work at Carnegie Mellon in the 1980s; Coulter's report of 1992 gave the derivation of the arc and the implementation steps that most later code follows.
prereqs: [kinematic-bicycle-model]
see_also: [stanley-controller, kinematic-bicycle-model, unicycle-model, model-predictive-control, pid-controller, jacobian-linearization, exponential-stability, dynamic-window-approach]
sources:
  - paper: "R. Craig Coulter, Carnegie Mellon University Robotics Institute, report CMU-RI-TR-92-01, 1992"
    title: Implementation of the Pure Pursuit Path Tracking Algorithm
    locator: the whole report (the curvature of the arc through the goal point and the steps of the implementation)
  - paper: "Jarrod M. Snider, Carnegie Mellon University Robotics Institute, report CMU-RI-TR-09-08, 2009"
    title: Automatic Steering Methods for Autonomous Automobile Path Tracking
    locator: the section on pure pursuit (the law kappa = 2 sin(alpha) / ld, the steering angle of the bicycle model, and a lookahead proportional to speed with a lower and an upper limit)
---

Pure pursuit is a steering law for a wheeled vehicle that follows a given path. At each control step it picks a goal point on the path, at a fixed distance $\ell_d$ (the lookahead) ahead of the vehicle. It then computes the circle arc that starts at the rear axle, is tangent to the current heading and passes through the goal point, and it steers the wheels to drive on that arc. The curvature of the arc is $\kappa = 2\sin\alpha/\ell_d$, where $\alpha$ is the angle of the goal point seen from the heading, and the steering angle of a car with wheelbase $L$ is $\delta = \arctan(\kappa L)$. The law is a heuristic: it has one tuning parameter, needs no model of the dynamics, and is used on many robots and autonomous cars at low and medium speed.

## In plain words

Look at a point on the road some meters ahead of you. Turn the wheel so that, if you kept it still, the car would drive a smooth curve that hits that point. A moment later, look again at a point the same distance ahead, and correct the wheel. Repeat.

If you look far ahead, the car turns gently and smoothly, but it cuts corners. If you look close, the car follows the road more tightly, but it can weave from side to side. The look-ahead distance is the only knob.

## The problem

**The model.** The vehicle is the [kinematic bicycle model](/kinematic-bicycle-model/) with the reference point at the center of the rear axle: $x' = v\cos\theta$, $y' = v\sin\theta$, $\theta' = (v/L)\tan\delta$, with the speed $v > 0$ given by another loop and the steering angle $\delta$ in $[-\delta_{max}, \delta_{max}]$. A [unicycle](/unicycle-model/) or a differential drive robot uses the same law with $\omega = v\kappa$ in place of the steering angle. The path is a polyline in the plane. Arithmetic, square roots and trigonometric functions cost one step each, as in the [real RAM](/real-ram/).

**Input.** The path as a list of points in meters, the current pose $(x, y, \theta)$ of the rear axle, the lookahead $\ell_d > 0$ in meters and the wheelbase $L$ in meters.

**Output.** A steering angle $\delta$ in radians for the next control period.

**How it differs from close pages.** The [Stanley controller](/stanley-controller/) uses the front axle, the closest point instead of a point ahead, and the heading error of the path; it reacts more directly to the cross-track error and needs a positive speed. [Model predictive control](/model-predictive-control/) optimizes the steering over a horizon with a model and constraints, at a much higher cost per step. A [PID controller](/pid-controller/) on the cross-track error has no geometry and needs tuning of three gains. The [dynamic window approach](/dynamic-window-approach/) chooses velocities to avoid obstacles and does not follow a given path.

## The algorithm

```pseudo id=main
PURE-PURSUIT(path, (x, y, θ), ℓd, L, δmax)
L1  (i, u) ← the point of the path closest to (x, y), searching from the last index onward
L2  g ← the first point of the path after (i, u) at distance ℓd from (x, y), or the last point of the path
L3  (xg, yg) ← g in the vehicle frame: xg = cos θ (gx - x) + sin θ (gy - y), yg = -sin θ (gx - x) + cos θ (gy - y)
L4  κ ← 2 yg / (xg^2 + yg^2)
L5  δ ← clamp(arctan(κ L), -δmax, δmax)
L6  apply δ for one control period dt
L7  the vehicle moves; repeat from L1 at the next period
```

Line L2 intersects the circle of radius $\ell_d$ around the rear axle with each segment, from the closest point onward, and takes the exit point of the circle on the first segment that has one. Searching only from the last closest index stops the vehicle from jumping back to an earlier part of a path that crosses itself. Line L4 is the curvature of the arc of Lemma 1 of the proof; when the goal point is at distance $\ell_d$, it equals $2\sin\alpha/\ell_d$. In the implementation, line L7 integrates the model with the classical [Runge-Kutta method](/runge-kutta-methods/) and $\delta$ held constant, so the simulation is exact to about $10^{-9}$ m and the only error is the zero-order hold of the controller.

## Example

Let $L = 2.5$ m, $v = 5$ m/s and $\ell_d = 5$ m. The path is the $x$ axis, and the car starts at $(0, 1, 0)$: 1 m to the left of the path, with the heading of the path.

Line L1 gives the closest point $(0, 0)$. Line L2 gives the goal point $(\sqrt{5^2 - 1^2}, 0) = (4.8990, 0)$. In the vehicle frame it is $(4.8990, -1)$, so line L4 gives $\kappa = 2 \cdot (-1)/25 = -0.08$ 1/m, a right turn of radius 12.5 m. Line L5 gives $\delta = \arctan(-0.2) = -0.1974$ rad, which is $-11.3$ degrees.

For a small error, the linear analysis of the proof gives $e(t) = e_0 e^{-at}(\cos at + \sin at)$ with $a = v/\ell_d = 1$ 1/s. The error crosses zero at $t = 3\pi/(4a) = 2.356$ s and reaches its least value $-e_0 e^{-\pi} = -0.0432$ m at $t = \pi/a = 3.14$ s, an overshoot of $4.3\%$. Measured: the simulation with $e_0 = 1$ m and a step of 1 ms crosses zero at 2.352 s, reaches $-0.0434$ m at 3.137 s, and stays within 0.001 m of the linear formula for 6 s. Even at $e_0 = 1$ m, the error is small compared with $\ell_d$.

The lookahead sets the trade-off. Measured with the same start and a step of 10 ms:

| $\ell_d$ (m) | Largest steering (rad) | Time until the error stays within 5 cm (s) | Overshoot (m) |
|---|---|---|---|
| 2 | 0.896 | 0.81 | 0.044 |
| 5 | 0.197 | 2.05 | 0.043 |
| 10 | 0.050 | 4.13 | 0.043 |

The time scales with $\ell_d/v$ and the overshoot does not change, as the theorem says: the damping ratio is $1/\sqrt{2}$ for every $\ell_d$.

## Correctness

Pure pursuit is a heuristic, so its correctness is a set of narrower claims, proved in the [proof](proofs/correctness/). Lemma 1 is geometric: among circles tangent to the heading at the rear axle, exactly one passes through the goal point, and its curvature is $2y_g/(x_g^2 + y_g^2)$. Lemma 2: the steering angle $\arctan(\kappa L)$ makes the rear axle of the kinematic bicycle drive on that circle. Theorem 1 (local): on a straight path, the linearized closed loop is $\ddot e + (2v/\ell_d)\dot e + (2v^2/\ell_d^2)e = 0$, with damping ratio $1/\sqrt{2}$, so the path is locally [exponentially stable](/exponential-stability/) with rate $v/\ell_d$. Theorem 2: on a circle of radius $R > \ell_d/2$, a car that starts on the circle stays on it with $\delta = \arctan(L/R)$. There is no global guarantee.

## Complexity

- **Time per step.** Line L1 and line L2 scan the segments from the last closest index, so a step costs $O(n)$ in the worst case for a path of $n$ vertices. A search window of a few segments around the last index makes it $O(1)$ when the vehicle moves less than a segment per step. The rest is $O(1)$. Measured: one call to the steering function takes 2 to 4 microseconds in CPython on a laptop, for a path of two points.
- **Space.** $O(1)$ beyond the path.

## Properties

- **Geometric and model-light.** The law uses only the geometry of the path and the wheelbase. It does not use the speed, the mass or the tires.
- **Corner cutting.** On a curve, the goal point is inside the curve, and the vehicle cuts it. On a circle the cut is zero only when the vehicle is already on the circle (Theorem 2); at a corner of the path, the vehicle starts to turn up to $\ell_d$ before the corner.
- **Smooth steering.** The steering angle changes continuously with the pose when the goal point moves continuously along the path.
- **Speed scaling.** With a fixed $\ell_d$, the closed loop gets faster with $v$ (rate $v/\ell_d$), and at high speed the steering becomes too aggressive for the real tires. A lookahead proportional to the speed, $\ell_d = k v$, keeps the response in distance the same.
- **Not exact.** The vehicle does not converge to the path in finite time, and on a curved path with a varying curvature there is a steady error.

## Variants and improvements

- **Speed-dependent lookahead.** $\ell_d = k v$, clamped to a range. Snider's report uses this form with a lower and an upper limit, and tunes $k$ on the vehicle. The value of $k$ is chosen by experiment, not derived.
- **Adaptive pure pursuit.** Change $\ell_d$ with the curvature of the path ahead: shorter on tight curves, longer on straight parts.
- **Regulated pure pursuit.** Reduce the speed when the curvature of the arc is large or an obstacle is near. The ROS 2 Nav2 stack uses a variant of this kind.
- **Vector pursuit.** Also matches the heading of the path at the goal point, with screw theory.
- **Front-axle or center reference.** Using another reference point changes the arc and the steering formula; the rear axle is the point where the kinematic bicycle has no side slip.

## When to use it

Use it to follow a path at low or moderate speed, when the path is smooth and a simple, robust law is enough: field robots, warehouse vehicles, small cars and course tracking in research. It handles noisy poses well, because a long lookahead averages them. For high speed or tight tracking, use a controller with a dynamic model, such as the [Stanley controller](/stanley-controller/) at moderate speed or [model predictive control](/model-predictive-control/). For reverse motion, run the law on the mirrored vehicle.

## Pitfalls

- **Lookahead tuning.** Too short gives oscillation and, with a time delay in the steering actuator, instability. Too long cuts corners and reacts late. The theorem on the page assumes no delay and no steering limit.
- **The goal point jumps.** When the vehicle is far from the path, the circle of radius $\ell_d$ may not meet the path ahead, or may meet a later part of a path that loops. Searching only forward from the last closest index, and taking the end of the path as a fallback, are the usual fixes.
- **End of the path.** Near the end, the goal point is the last point, closer than $\ell_d$. Use the actual distance in line L4, not $\ell_d$, or the curvature is wrong.
- **Wrong reference point.** The formula $\delta = \arctan(\kappa L)$ holds for the rear axle. Measuring the pose at the center of mass or the front axle and using the same formula gives a biased steering.
- **Sign conventions.** Left turns must have positive $y_g$, positive $\kappa$ and positive $\delta$ in the same frame; a sign error makes the vehicle turn away from the path.

## Implementations

## History

Pure pursuit came from the road-following work at Carnegie Mellon University in the 1980s. Wallace, Stentz, Thorpe, Moravec, Whittaker and Kanade described an early form in 1985, and Amidi compared it with other path trackers in his report of 1990. Coulter's report of 1992 wrote down the geometry of the arc and the implementation steps, and most later code follows it. Snider's report of 2009 described pure pursuit, the Stanley controller and other steering laws for cars side by side, with their tuning.

## References
