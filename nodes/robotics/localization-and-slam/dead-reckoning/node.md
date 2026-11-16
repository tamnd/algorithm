---
tag: TXG0WX
kind: technique
slug: dead-reckoning
name: Dead reckoning
aliases:
- wheel odometry
- deduced reckoning
area: robotics/localization-and-slam
level: intro
summary: "Estimates position and heading by integrating measured speed and turn rate from a known start. With no outside fix, the position error grows with time, often faster than linearly."
prereqs: [robot-pose, unicycle-model, euler-method]
see_also: [odometry-motion-model, velocity-motion-model, differential-drive-model, ekf-localization, visual-odometry, pose-compounding-operators, attitude-estimation, mobile-robot-localization]
sources:
  - paper: doi:10.1177/0278364904041326
    title: "Alonzo Kelly, Linearized error propagation in odometry, The International Journal of Robotics Research 23(2), 2004, pages 179 to 218"
    locator: "the linearized error dynamics of odometry and the integral solutions for systematic and random errors"
  - paper: "Oliver J. Woodman, An introduction to inertial navigation, Technical Report UCAM-CL-TR-696, University of Cambridge Computer Laboratory, 2007"
    locator: "Sections 3.2.1 and 3.2.2 (gyro bias and white noise) and Sections 4.2.1 and 4.2.2 (accelerometer bias and white noise, and the position errors they cause)"
---

Dead reckoning estimates where a vehicle is by starting from a known pose and adding up measured motion: distance and turn from wheel encoders, speed and heading from a log and a compass, or acceleration and rate from an inertial unit. It needs no outside reference, so it works everywhere and at a high rate. Its weakness is that each step adds a small error and nothing removes it, so the pose error grows with time or distance. On robots it is the prediction step of every localization filter: the [odometry motion model](/odometry-motion-model/) and the [velocity motion model](/velocity-motion-model/) add a noise model to it, and [EKF localization](/ekf-localization/) or a particle filter corrects it with landmarks or maps. The rotational half, integrating a gyro, is the drift problem of [attitude estimation](/attitude-estimation/).

## In plain words

If you know where you started, how far you went and which way you turned, you can work out where you are now. A robot does this by counting the turns of its wheels. A ship did it with a compass and a measure of speed. The method is simple and needs no map or signal from outside. But every reading is a little wrong: a wheel slips, the wheel size is not quite what you think, the compass is off a bit. These small errors add up, and an error in direction is the worst, because every later step then goes off at a slight angle. After a long trip the estimate can be far from the truth, so it must be corrected now and then.

## When it applies

- The start pose is known, or only the motion relative to the start matters.
- A sensor measures motion in the body frame: wheel encoders, a gyro, an accelerometer, a speed log or a camera used for [visual odometry](/visual-odometry/).
- The trip is short, or outside fixes arrive often enough to bound the error. Between fixes, dead reckoning fills the gaps.

## The template

The pose is $x_k = (p_x, p_y, \theta)$, a planar [robot pose](/robot-pose/). Over a short step, the sensors give a distance $\Delta s_k$ and a heading change $\Delta\theta_k$. For a [differential drive](/differential-drive-model/) robot with wheel distances $\Delta s_r$ and $\Delta s_l$ and track width $w$, these are $\Delta s = (\Delta s_r + \Delta s_l) / 2$ and $\Delta\theta = (\Delta s_r - \Delta s_l) / w$.

1. **Integrate.** Update the pose with the midpoint heading:
   $$\theta_{k+1} = \theta_k + \Delta\theta_k, \qquad p_{k+1} = p_k + \Delta s_k \begin{pmatrix} \cos(\theta_k + \Delta\theta_k / 2) \\ \sin(\theta_k + \Delta\theta_k / 2) \end{pmatrix}.$$
   The plain [Euler method](/euler-method/) uses $\theta_k$ in place of the midpoint, with a larger error per step on curves. In general, compose the body motion with the pose by the [pose compounding operator](/pose-compounding-operators/) $x_{k+1} = x_k \oplus u_k$.
2. **Propagate the uncertainty.** Linearize the update to get $F_k = \partial x_{k+1} / \partial x_k$ and $G_k = \partial x_{k+1} / \partial u_k$, and update the covariance as $P_{k+1} = F_k P_k F_k^T + G_k Q_k G_k^T$, with $Q_k$ the covariance of the measured motion. Kelly (2004) gives the integral form of this recursion.
3. **Reset.** When an outside fix arrives, correct the pose and the covariance with a filter, and continue from there.

## Classic examples

- **Wheel odometry.** A differential drive robot integrates its encoder counts at $50$ to $1000$ Hz with the template above. The main errors are unequal wheel radii, an error in the track width and slip.
- **Heading random walk.** A robot drives straight at speed $v$, and its heading error is a random walk with variance $\sigma^2 t$. To first order the lateral position error is $v \int_0^t \delta\theta(s) \, ds$, whose standard deviation is $v \sigma t^{3/2} / \sqrt{3}$ (theorem, for small angles and a Brownian heading error). With $v = 1$ m/s and $\sigma = 0.01$ rad per square root of a second, a Monte Carlo run with 2000 paths gave $2.03$ m at $t = 50$ s, against $2.04$ m from the formula, and $5.66$ m at $t = 100$ s, against $5.77$ m (measurement).
- **Inertial dead reckoning.** A strapdown inertial unit integrates the gyro once for attitude and the accelerometer twice for position. White accelerometer noise of standard deviation $\sigma$ per sample of length $\delta t$ gives a position error with standard deviation $\sigma t^{3/2} \sqrt{\delta t / 3}$, and a constant bias $\varepsilon$ gives $\varepsilon t^2 / 2$ (Woodman, 2007, Sections 4.2.1 and 4.2.2). A tilt error leaks gravity into the horizontal acceleration, which makes the error grow faster still.
- **Ship navigation.** A compass gives the heading directly and a log gives the speed. The heading error is then bounded, and the position error grows about linearly with the distance for a fixed compass error.

## Variations

- **Compass or magnetometer heading.** Measuring heading directly, rather than integrating a turn rate, stops the heading error from growing. It trades drift for local magnetic disturbances.
- **Exact arcs.** For a constant speed and turn rate over a step, the robot moves on a circular arc, and the [velocity motion model](/velocity-motion-model/) integrates it exactly.
- **Pedestrian dead reckoning.** A phone detects steps from the accelerometer, estimates a step length and adds it along the current heading.
- **Fused odometry.** Wheel distance with a gyro heading is a common mix: the gyro is better for turns, the wheels for distance.
- **Visual and lidar odometry.** Motion from consecutive camera or lidar frames is still dead reckoning, with smaller and different errors.

## Pitfalls

- **Heading errors dominate (heuristic).** A small heading error makes every later step go the wrong way, so the position error grows faster than the heading error. Spend sensor effort on heading first.
- **Systematic errors.** Unequal wheel radii and a wrong track width give a steady turn error, and the lateral error then grows with the square of the distance. Calibrate them; a random noise model does not cover them.
- **Slip and skid.** On loose ground or during hard turns, the wheels do not roll without slipping, and the encoder counts overstate the motion.
- **Angle wrap.** Keep $\theta$ in a fixed interval, or differences of headings near $\pm\pi$ become wrong by $2\pi$.
- **Over-confidence.** A covariance from the linearized recursion assumes white, independent errors. Real errors are often correlated in time, and the true spread is then larger.

## Exercises

1. A robot starts at $(0, 0, 0)$, drives $1$ m forward, turns in place by $+\pi/2$ and drives $1$ m forward. Where is it? *Answer:* At $(1, 1, \pi/2)$. The first leg ends at $(1, 0, 0)$, the turn gives $(1, 0, \pi/2)$, and the second leg goes along $(\cos \pi/2, \sin \pi/2) = (0, 1)$.
2. Show that a Brownian heading error with variance $\sigma^2 t$ gives a lateral error with variance $v^2 \sigma^2 t^3 / 3$ for a robot that drives straight at speed $v$. *Answer:* The lateral error is $y(t) = v \int_0^t \delta\theta(s) \, ds$ to first order. Its variance is $v^2 \int_0^t \int_0^t \operatorname{E}[\delta\theta(s) \delta\theta(u)] \, ds \, du = v^2 \sigma^2 \int_0^t \int_0^t \min(s, u) \, ds \, du = v^2 \sigma^2 t^3 / 3$.
3. A differential drive robot has track width $w = 0.5$ m, and its right wheel radius is $1\%$ larger than the value in the software. It drives straight for $s = 10$ m. What heading error and lateral error does dead reckoning report? *Answer:* The software reads the right wheel distance as $s / 1.01$, so $\Delta\theta \approx -0.01 s / w = -0.2$ rad in total. The heading error grows linearly with the distance, so the lateral error is about $0.01 s^2 / (2 w) = 1$ m.

## References
