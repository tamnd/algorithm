---
tag: P133N7
kind: model
slug: odometry-motion-model
name: Odometry motion model
aliases:
- odometry-based motion model
area: robotics/localization-and-slam
level: core
summary: "A probabilistic model of motion as a rotation, a translation and a rotation read from wheel odometry, each with noise."
history:
  year: 2005
  people: [Sebastian Thrun, Wolfram Burgard, Dieter Fox]
  note: Probabilistic Robotics gives the model as a rotation, a translation and a second rotation computed from two odometry readings, with an algorithm for its density and an algorithm that draws samples from it.
prereqs: [bayes-filter]
see_also: [velocity-motion-model, dead-reckoning, differential-drive-model, monte-carlo-localization, ekf-localization, particle-filter, beam-range-finder-model, unicycle-model]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 5, Section 5.4 (the odometry motion model: the closed form density in Section 5.4.1, sampling in Section 5.4.2 and the derivation in Section 5.4.3), and Chapter 2, Section 2.4 (the place of the motion model in the Bayes filter)"
---

The odometry motion model gives the probability that a planar robot moves from one pose to another, given what its wheel encoders report. A pose is a position $(x, y)$ and a heading $\theta$. The encoders do not measure the true motion: wheels slip, the floor is uneven, and the wheel radius is not known exactly. The model treats the reported motion as a measurement of the true motion. It splits each motion into three steps, a rotation, a straight translation and a second rotation, and adds independent zero-mean Gaussian noise to each step. The result is the motion model $p(x_t \mid u_t, x_{t-1})$ of the [Bayes filter](/bayes-filter/), where the control $u_t$ is a pair of odometry readings. [Monte Carlo localization](/monte-carlo-localization/) draws samples from it, and [EKF localization](/ekf-localization/) uses a linearized form of it. The notation is the one of Thrun, Burgard and Fox (2005).

## The machine

**State.** The pose $x_t = (x, y, \theta)$ of the robot in the world frame, in meters and radians. The pose before the motion is $x_{t-1}$ and the pose after it is $x_t = (x', y', \theta')$.

**Input.** Two readings of the internal odometry of the robot, $u_t = (\bar x_{t-1}, \bar x_t)$, with $\bar x_{t-1} = (\bar x, \bar y, \bar\theta)$ and $\bar x_t = (\bar x', \bar y', \bar\theta')$. The odometry frame drifts against the world frame, so only the relative motion between the two readings is used. It is the motion that the encoders report:

$$\delta_{\mathrm{rot1}} = \operatorname{atan2}(\bar y' - \bar y,\ \bar x' - \bar x) - \bar\theta, \qquad \delta_{\mathrm{trans}} = \sqrt{(\bar x' - \bar x)^2 + (\bar y' - \bar y)^2}, \qquad \delta_{\mathrm{rot2}} = \bar\theta' - \bar\theta - \delta_{\mathrm{rot1}}.$$

The first rotation turns the robot towards the end point, the translation drives it there, and the second rotation turns it to the final heading.

**Noise.** The true motion is the reported motion minus independent Gaussian errors. In the variance form used on this page,

$$\hat\delta_{\mathrm{rot1}} = \delta_{\mathrm{rot1}} - \varepsilon_1, \quad \varepsilon_1 \sim \mathcal N(0,\ \alpha_1 \delta_{\mathrm{rot1}}^2 + \alpha_2 \delta_{\mathrm{trans}}^2),$$

$$\hat\delta_{\mathrm{trans}} = \delta_{\mathrm{trans}} - \varepsilon_2, \quad \varepsilon_2 \sim \mathcal N(0,\ \alpha_3 \delta_{\mathrm{trans}}^2 + \alpha_4 (\delta_{\mathrm{rot1}}^2 + \delta_{\mathrm{rot2}}^2)),$$

$$\hat\delta_{\mathrm{rot2}} = \delta_{\mathrm{rot2}} - \varepsilon_3, \quad \varepsilon_3 \sim \mathcal N(0,\ \alpha_1 \delta_{\mathrm{rot2}}^2 + \alpha_2 \delta_{\mathrm{trans}}^2).$$

The second argument of $\mathcal N$ is a variance. The printings of the source and many course notes differ here: some use the standard deviation $\alpha_1 |\delta_{\mathrm{rot1}}| + \alpha_2 \delta_{\mathrm{trans}}$ instead. The two forms are different models, and alpha values fitted for one do not carry over to the other.

**Parameters.** Four dimensionless numbers $\alpha_1, \ldots, \alpha_4 \ge 0$. $\alpha_1$ scales rotation noise from rotation, $\alpha_2$ rotation noise from translation, $\alpha_3$ translation noise from translation, and $\alpha_4$ translation noise from rotation. They depend on the robot and the floor, and they are fitted to data; there are no correct default values.

**Output.** The new pose is the old pose moved by the true motion:

$$x' = x + \hat\delta_{\mathrm{trans}} \cos(\theta + \hat\delta_{\mathrm{rot1}}), \qquad y' = y + \hat\delta_{\mathrm{trans}} \sin(\theta + \hat\delta_{\mathrm{rot1}}), \qquad \theta' = \theta + \hat\delta_{\mathrm{rot1}} + \hat\delta_{\mathrm{rot2}}.$$

**Standing assumptions.** The robot moves in a plane. The three errors are independent of each other, of the pose and of the errors of earlier steps; this independence is what makes the motion a Markov process, and it is an approximation (slip on a wet patch persists over several steps). Odometry is treated as a measurement and not as a control, so the model can be used only after the motion, not to plan it.

**Two algorithms.** Sampling draws $\varepsilon_1, \varepsilon_2, \varepsilon_3$ and applies the output equations. The closed form takes a hypothesized pair $(x_{t-1}, x_t)$, computes the motion $(\hat\delta_{\mathrm{rot1}}, \hat\delta_{\mathrm{trans}}, \hat\delta_{\mathrm{rot2}})$ that would produce it with the same three equations as for $u_t$, and returns $p_1 p_2 p_3$, the product of the three Gaussian densities of the differences $\delta - \hat\delta$. Angle differences must be wrapped into $(-\pi, \pi]$ before the Gaussian is evaluated. Implementations differ in where they take the variances from: from the reported motion $\delta$, as the sampler does, or from the hypothesized motion $\hat\delta$.

**Example.** The odometry reports $\bar x_{t-1} = (0, 0, 0)$ and $\bar x_t = (1, 1, \pi/2)$, so $\delta_{\mathrm{rot1}} = \pi/4 \approx 0.7854$, $\delta_{\mathrm{trans}} = \sqrt 2 \approx 1.4142$ and $\delta_{\mathrm{rot2}} = \pi/4$. Take $\alpha = (0.05, 0.01, 0.02, 0.005)$. The variances are $0.05 (\pi/4)^2 + 0.01 \cdot 2 \approx 0.050843$ for each rotation (standard deviation $0.2255$ rad) and $0.02 \cdot 2 + 0.005 \cdot 2 (\pi/4)^2 \approx 0.046169$ for the translation (standard deviation $0.2149$ m). A robot at $x_{t-1} = (2, 3, \pi/2)$ ends at $(1, 4, \pi)$ if there is no noise. At that pose the closed form returns $p_1 p_2 p_3 = (2\pi \cdot 0.050843)^{-1} (2\pi \cdot 0.046169)^{-1/2} \approx 5.8121$.

## What it counts

The model assigns a probability to a motion. It gives two things:

- the density $p(x_t \mid u_t, x_{t-1})$ for a hypothesized end pose, which the [Bayes filter](/bayes-filter/) needs in its prediction step on a grid ([histogram filter](/histogram-filter/), [Markov localization](/markov-localization/));
- samples of $x_t$ given $x_{t-1}$ and $u_t$, which a [particle filter](/particle-filter/) needs.

Both take $O(1)$ arithmetic operations and calls to $\sin$, $\cos$ and $\operatorname{atan2}$ for one pose. The prediction step of a particle filter with $N$ particles therefore costs $O(N)$, and the prediction step on a grid of $g$ poses costs $O(g^2)$ if every pair of cells is evaluated. The model does not predict where the robot is in the world; it predicts how far the robot is from where the odometry says it moved, relative to the last pose.

## Relation to other models

- **[Velocity motion model](/velocity-motion-model/).** Uses the commanded linear and angular velocities instead of odometry readings, and moves the robot on an arc instead of along a rotation, a translation and a rotation. Thrun, Burgard and Fox (2005) note that odometry is usually more accurate than the commands, so the odometry model is the common choice when encoders exist. The velocity model is needed for planning and control, before the motion has happened.
- **[Dead reckoning](/dead-reckoning/).** Dead reckoning integrates the same odometry with no noise and no correction; it is the mean path of this model, up to the shrinking effect below. The errors grow without bound over time, which is why the noise model is used inside a filter that also has a measurement model, such as the [beam range finder model](/beam-range-finder-model/).
- **[Differential drive model](/differential-drive-model/) and [unicycle model](/unicycle-model/).** These are the kinematic models that turn wheel rotations into the odometry pose $\bar x_t$. The odometry model sits on top of them and adds noise to their output.
- **[EKF localization](/ekf-localization/).** Linearizes the output equations around the mean motion. The noise is Gaussian in $(\hat\delta_{\mathrm{rot1}}, \hat\delta_{\mathrm{trans}}, \hat\delta_{\mathrm{rot2}})$ and is mapped into the pose space by the Jacobian of the output equations, so the pose noise in the filter is only approximately Gaussian.

## Known results in the model

- **Theorem (change of variables).** The output map $(\hat\delta_{\mathrm{rot1}}, \hat\delta_{\mathrm{trans}}, \hat\delta_{\mathrm{rot2}}) \mapsto (x', y', \theta')$ for a fixed $x_{t-1}$ has a Jacobian with determinant $-\hat\delta_{\mathrm{trans}}$. Proof: the derivatives of $(x', y')$ with respect to $(\hat\delta_{\mathrm{rot1}}, \hat\delta_{\mathrm{trans}})$ form the matrix $\begin{pmatrix} -t s & c \\ t c & s \end{pmatrix}$ with $t = \hat\delta_{\mathrm{trans}}$, $c = \cos(\theta + \hat\delta_{\mathrm{rot1}})$, $s = \sin(\theta + \hat\delta_{\mathrm{rot1}})$, whose determinant is $-t(s^2 + c^2) = -t$; the third output adds a row $(1, 0, 1)$, and $(x', y')$ does not depend on $\hat\delta_{\mathrm{rot2}}$, so expanding along the last column gives $-t$. Hence, when the variances are taken from the reported motion, $p_1 p_2 p_3$ is the density of the motion parameters, and the density of the pose is $p_1 p_2 p_3 / \hat\delta_{\mathrm{trans}}$ (summed over every parameter triple that gives the same pose, which matters only when the noise can make the translation negative). The closed form that returns $p_1 p_2 p_3$ is therefore not a density over poses. In a particle filter this does not matter, since the sampler is exact. On a grid it adds a weight that favors poses far from $x_{t-1}$.
- **Measurement (the size of the factor).** For the example above, a numerical integral of $p_1 p_2 p_3$ over a fine grid of end poses gives about $1.413$, close to $\delta_{\mathrm{trans}} = \sqrt 2$, and the integral of $p_1 p_2 p_3 / \hat\delta_{\mathrm{trans}}$ gives about $0.999$. The pose density at the noise-free end pose is $5.8121 / \sqrt 2 \approx 4.1098$. With the variances taken from the hypothesized motion instead, the integral after the division is about $1.08$, so that variant is not exactly a density in any coordinates.
- **Theorem (the mean falls short).** If $\varepsilon \sim \mathcal N(0, v)$, then $\mathbb E[\cos(a + \varepsilon)] = e^{-v/2} \cos a$, and the same holds for $\sin$. Since $\hat\delta_{\mathrm{trans}}$ and $\hat\delta_{\mathrm{rot1}}$ are independent, $\mathbb E[x'] = x + \delta_{\mathrm{trans}}\, e^{-v_1/2} \cos(\theta + \delta_{\mathrm{rot1}})$ and $\mathbb E[y'] = y + \delta_{\mathrm{trans}}\, e^{-v_1/2} \sin(\theta + \delta_{\mathrm{rot1}})$, where $v_1$ is the variance of $\varepsilon_1$, and $\mathbb E[\theta'] = \theta + \delta_{\mathrm{rot1}} + \delta_{\mathrm{rot2}}$ when the heading is not wrapped. So the mean position is not the noise-free position: it lies on the same line, closer to the start. In the example $e^{-v_1/2} \approx 0.974899$, and the mean is $(1.025101, 3.974899, \pi)$; a Monte Carlo run with 200000 samples gave $(1.02500, 3.97494, 3.14164)$. The samples form a curved, banana-shaped cloud around the arc of radius $\delta_{\mathrm{trans}}$, so a single Gaussian in $(x, y, \theta)$ fits them badly when the rotation noise is large.
- **Pure rotation.** When $\delta_{\mathrm{trans}} = 0$, the direction $\delta_{\mathrm{rot1}}$ is not defined, and a tiny translation makes it jump. Implementations set $\delta_{\mathrm{rot1}} = 0$ below a small threshold on $\delta_{\mathrm{trans}}$ and put the whole rotation into $\delta_{\mathrm{rot2}}$. The same issue appears in the closed form for hypothesized poses with $x' = x$ and $y' = y$.
- **Heuristic (fitting the alphas).** The alphas are fitted to data, for example by driving known paths and matching the spread of the end poses, or by maximum likelihood inside a localization run. The Gaussian shape and the independence of the three errors are modeling choices, not facts about wheels. Since the true errors are correlated in time, alphas fitted to single steps can make the predicted spread over many steps too small.

## References
