---
tag: 8QP9X9
kind: algorithm
slug: stanley-controller
name: Stanley controller
aliases:
- Stanley steering control
area: robotics/mobile-and-legged-robots
level: core
summary: Steers by the heading error plus the arctangent of gain times cross-track error over speed at the front axle. Locally exponentially stable for the kinematic bicycle at positive speed.
model: real-ram
complexity:
  vars: {n: "the number of vertices of the path polyline; the bounds are for one control step"}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {deterministic: true, randomized: false, online: true, exact: false}
history:
  year: 2006
  people: [Sebastian Thrun, Michael Montemerlo, Gabriel M. Hoffmann, Claire J. Tomlin]
  note: The law steered Stanley, the Stanford car that won the DARPA Grand Challenge of 2005; Thrun et al. published it in 2006, and Hoffmann et al. analyzed and extended it in 2007.
prereqs: [kinematic-bicycle-model, exponential-stability]
see_also: [pure-pursuit, kinematic-bicycle-model, model-predictive-control, pid-controller, exponential-stability, lyapunov-function, jacobian-linearization, asymptotic-stability]
sources:
  - paper: doi:10.1002/rob.20147
    title: Sebastian Thrun et al., Stanley, the robot that won the DARPA Grand Challenge, Journal of Field Robotics 23(9), 2006
    locator: pages 661 to 692; Section 9.2 (the steering law, equation (7), the error equation (8) and the exponential convergence for small errors, equation (9))
  - paper: doi:10.1109/ACC.2007.4282788
    title: Gabriel M. Hoffmann, Claire J. Tomlin, Michael Montemerlo and Sebastian Thrun, Autonomous automobile trajectory tracking for off-road driving, controller design, experimental validation and racing, American Control Conference, 2007
    locator: pages 2296 to 2301 (the analysis of the law for positive speed and the extensions of the law for a real vehicle)
  - paper: "Jarrod M. Snider, Carnegie Mellon University Robotics Institute, report CMU-RI-TR-09-08, 2009"
    title: Automatic Steering Methods for Autonomous Automobile Path Tracking
    locator: Section 2.3 (the Stanley method, its geometry and its tuning, next to pure pursuit)
---

The Stanley controller is a steering law for a car that follows a path. It looks at the front axle. It measures the heading error $\psi$, the angle between the path and the car, and the cross-track error $e$, the signed distance from the center of the front axle to the closest point of the path. It steers with $\delta = \psi + \arctan(ke/u)$, where $u$ is the speed of the front wheels and $k$ is a gain. The first term aligns the wheels with the path, and the second turns them toward the path, more strongly when the error is large or the car is slow. For the kinematic bicycle model at a constant positive speed and without saturation, the cross-track error on a straight path converges to zero for every start, and the path is locally exponentially stable. The law steered Stanley, the car that won the DARPA Grand Challenge of 2005.

## In plain words

Look at the road at your front wheels, not far ahead. Two things are wrong: the car points in a slightly wrong direction, and the front wheels are a bit to the side of the line. Turn the wheels to fix the direction, and turn them a bit more toward the line. If you are far from the line, turn toward it hard. If you are close, turn toward it gently.

At high speed, the same distance from the line asks for a smaller correction, because the car covers ground fast. That is why the speed is in the formula.

## The problem

**The model.** The car is the [kinematic bicycle model](/kinematic-bicycle-model/) with the reference point at the center of the front axle: $x_f' = u\cos(\theta + \delta)$, $y_f' = u\sin(\theta + \delta)$, $\theta' = (u/L)\sin\delta$, with wheelbase $L$, speed $u > 0$ of the front wheels, and steering angle $|\delta| \le \delta_{max}$. The speed comes from another loop. The path is a polyline in the plane. The machine model is the [real RAM](/real-ram/).

**Input.** The path, the pose $(x_f, y_f, \theta)$ of the front axle, the speed $u$, the gain $k > 0$ in 1/s and the steering limit $\delta_{max}$.

**Output.** A steering angle $\delta$ in radians for the next control period.

**How it differs from close pages.** [Pure pursuit](/pure-pursuit/) uses the rear axle and a goal point at a lookahead distance, and ignores the heading of the path; it is smoother but cuts corners, and it has no proof of convergence for large errors. The Stanley law uses the closest point at the front axle and the path heading, so it reacts at once to errors, and it needs a positive speed. [Model predictive control](/model-predictive-control/) uses a dynamic model and a horizon. A [PID controller](/pid-controller/) on the cross-track error is the usual baseline, with three gains and no geometry.

## The algorithm

```pseudo id=main
STANLEY(path, (xf, yf, θ), u, k, δmax)
L1  (i, s) ← the point of the path closest to (xf, yf), searching from the last index onward
L2  e ← signed distance from (xf, yf) to that point, positive when the path is to the left of the front axle
L3  ψ ← wrap(heading of segment i - θ)
L4  δ ← ψ + arctan(k e / u)
L5  δ ← clamp(δ, -δmax, δmax)
L6  apply δ for one control period
L7  the vehicle moves; repeat from L1 at the next period
```

With this sign convention, a positive $\delta$ is a left turn and reduces a positive $e$. Line L4 uses the two-argument arctangent of $(ke, u)$ in the code. Thrun et al. write the law with the cross-track error $x(t)$ and the speed $u(t)$, as $\delta(t) = \psi(t) + \arctan(k\,x(t)/u(t))$. The implementation integrates the model with the classical [Runge-Kutta method](/runge-kutta-methods/), either with $\delta$ held for a step, like a digital controller, or with $\delta$ recomputed in each stage, which integrates the continuous closed loop of the proof.

## Example

Let $L = 2.85$ m, $k = 1$ 1/s and $u = 5$ m/s; the wheelbase and the gain are the values in Thrun et al. (2006). The path is the $x$ axis, and the front axle starts at $(0, 1)$ with heading 0, so it is 1 m to the left of the path. Line L2 gives $e = -1$ m and line L3 gives $\psi = 0$. Line L4 gives $\delta = \arctan(-1/5) = -0.1974$ rad, a right turn of 11.3 degrees.

From then on, the proof shows that $\dot e = -ke/\sqrt{1 + (ke/u)^2}$, whatever the heading, as long as the steering does not saturate. With $s = ke/u$, the time to go from $e_0$ to $e$ is $(F(s_0) - F(s))/k$ with $F(s) = \sqrt{1 + s^2} + \ln(|s|/(1 + \sqrt{1 + s^2}))$. The table gives the time to reach 1 cm for $k = 1$:

| $u$ (m/s) | From 1 m (s) | From 10 m (s) |
|---|---|---|
| 1 | 4.831 | 14.248 |
| 5 | 4.615 | 7.663 |
| 20 | 4.606 | 6.968 |
| pure exponential $e^{-kt}$ | 4.605 | 6.908 |

For a small $ke/u$, the error decays like $e^{-kt}$ and the speed does not matter. For a large one, the front axle drives straight at the path, and the time is about the distance over the speed. Measured: with a steering limit of 24 degrees, $u = 5$ m/s and $e_0 = 10$ m, the steering saturates for the first 0.79 s, and the error reaches 1 cm at 7.873 s instead of 7.663 s.

## Correctness

The [proof](proofs/correctness/) works under three hypotheses: the kinematic bicycle model at the front axle, a constant speed $u > 0$, and no saturation of line L5. Lemma 1 shows that on a straight path the law gives $\dot e = -ke/\sqrt{1 + (ke/u)^2}$ for every heading. Theorem 1 solves this equation: the error keeps its sign, decreases strictly to zero from every start, and decays like $e^{-kt}$ once it is small. Theorem 2 shows that the heading also converges and that the path is locally [exponentially stable](/exponential-stability/), with the eigenvalues $-k$ and $-u/L$. Theorem 3 shows that a circle of radius $R > L$ is an equilibrium, with $\delta = \arcsin(L/R)$. The behavior under saturation, with dynamics or on general curved paths is not proved; Hoffmann et al. (2007) give an analysis for positive speed, and the tests measure convergence with a 24 degree limit.

## Complexity

- **Time per step.** Finding the closest point costs $O(n)$ for a path of $n$ vertices in the worst case, and $O(1)$ with a search window of a few segments near the last index, which the implementation offers. The law itself is $O(1)$. Measured: one call takes about 1.5 microseconds in CPython on a laptop for a path of two points.
- **Space.** $O(1)$ beyond the path.

## Properties

- **Global on a straight path.** Without saturation, the cross-track error converges from any start, monotonically, without overshoot. This is a theorem for the kinematic model, not a measurement.
- **Speed scaling.** For small errors, the decay rate is $k$ in time, not in distance, so the car covers about $u/k$ m per e-fold of the error. At high speed the correction stretches over a long distance.
- **Low speed.** As $u \to 0$, the term $\arctan(ke/u)$ goes to $\pm\pi/2$ for any nonzero error, and the law becomes very sensitive to noise in $e$. The softening constant below fixes this.
- **Front axle reference.** The law needs the pose of the front axle. A pose estimate at the rear axle or the center of mass must be moved to the front axle first.
- **Curved paths.** On a circle, the equilibrium heading lags the path by $\arcsin(L/R)$, and the rear axle runs inside the path, on the circle of radius $\sqrt{R^2 - L^2}$.

## Variants and improvements

- **Softening constant.** Use $\arctan(ke/(k_s + u))$ with a small $k_s > 0$, so the law stays bounded at low speed. Hoffmann et al. (2007) and Snider (2009) use this form; the implementation has it as the parameter `soft`.
- **Damping terms.** Hoffmann et al. add terms on the yaw rate and on the steering rate for a real car at speed, where the kinematic model no longer holds.
- **Feedforward of the curvature.** Add the steering angle that the curvature of the path needs, so that the heading error does not have to build up on curves.
- **Reverse driving.** In reverse, the rear axle leads. Apply the law at the rear axle with the speed and the heading reversed; the proof of the page does not cover this case.

## When to use it

Use it for path tracking at low to moderate speed when the path has a heading at every point and the pose of the front axle is known well: autonomous cars, off-road vehicles, and course tracking in research and teaching. It needs a path that is smooth enough for the heading error to make sense, and a positive speed. The gain $k$ is a tuning parameter; it is not derived from the model, and in practice it is set by tests on the vehicle. For high speed, combine it with a dynamic model, or use [model predictive control](/model-predictive-control/).

## Pitfalls

- **Wrong reference point.** The analysis holds at the front axle. Using the rear axle with the same law changes the error equation and can oscillate.
- **Sign conventions.** The signs of $e$, $\psi$ and $\delta$ must agree; with this page's convention, a positive $e$ means that the path is to the left and a positive $\delta$ turns left.
- **Angle wrapping.** The heading error must be wrapped to $[-\pi, \pi)$, or a path heading near $\pm\pi$ makes the car turn the long way.
- **Noisy cross-track error at low speed.** Without the softening constant, a few centimeters of noise in $e$ at $u \approx 0$ give a full steering swing.
- **Polyline headings.** The heading of a polyline jumps at each vertex, and so does $\psi$, which gives a jump in the steering. Use dense points, or interpolate the heading.

## Implementations

## History

The Stanford Racing Team, led by Sebastian Thrun, built Stanley for the DARPA Grand Challenge of 2005, a race of autonomous cars through the desert, and won it. The steering law was one part of the system. Thrun et al. (2006) described the whole car, and wrote the law and its error equation in the section on control. Hoffmann, Tomlin, Montemerlo and Thrun (2007) gave the analysis for positive speed and the extensions for a real car at speed. Snider's report of 2009 placed the law next to pure pursuit and other steering methods, and it became a standard method in teaching.

## References
