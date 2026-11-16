---
tag: 70HXEB
kind: model
slug: landmark-measurement-model
name: Landmark measurement model
aliases:
- range-bearing model
area: robotics/localization-and-slam
level: core
summary: "Gives the range and bearing of a known landmark from the robot pose, with Gaussian noise, for feature-based maps."
history:
  year: 2005
  people: [Sebastian Thrun, Wolfram Burgard, Dieter Fox]
  note: Probabilistic Robotics gives the range and bearing model with a signature for each landmark, with algorithms for its density with known correspondence and for sampling poses from one feature.
prereqs: [bayes-filter]
see_also: [ekf-localization, ekf-slam, fastslam, data-association-slam, joint-compatibility-branch-and-bound, extended-kalman-filter, beam-range-finder-model, perspective-n-point]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 6, Section 6.6 (feature-based measurement models: range and bearing with a signature, known correspondence, and sampling poses), and Chapter 7 (EKF localization, which linearizes this model)"
---

The landmark measurement model gives the probability of a measurement of a known landmark, given the pose of the robot. A landmark is a distinct point in the world, such as a pole, a door corner or a visual marker, whose position is in the map. The sensor reports two numbers for it: the range, the distance from the robot to the landmark, and the bearing, the angle of the landmark as seen from the robot's heading. The model says that each number is the true geometric value plus independent Gaussian noise. Optionally the sensor also reports a signature, such as a color, that helps to tell landmarks apart. This model is the measurement model $p(z_t \mid x_t, m)$ of [EKF localization](/ekf-localization/), [EKF SLAM](/ekf-slam/) and [FastSLAM](/fastslam/). The notation is the one of Thrun, Burgard and Fox (2005).

## The machine

**State.** The pose $x_t = (x, y, \theta)$ of the robot in meters and radians, and a feature-based map $m = \{m_1, \ldots, m_M\}$. Landmark $j$ has a position $(m_{j,x}, m_{j,y})$ and a signature $s_j$.

**Measurement.** A set of features $z_t = \{f_t^1, f_t^2, \ldots\}$. Each feature $f_t^i = (r_t^i, \phi_t^i, s_t^i)$ has a range in meters, a bearing in radians relative to the heading, and a signature.

**Correspondence.** The variable $c_t^i = j$ says that feature $i$ comes from landmark $j$. The basic model assumes that it is known. When it is not, it must be estimated; this is [data association](/data-association-slam/).

**The model.** For $c_t^i = j$,

$$r_t^i = \sqrt{(m_{j,x} - x)^2 + (m_{j,y} - y)^2} + \varepsilon_r, \qquad \phi_t^i = \operatorname{atan2}(m_{j,y} - y,\ m_{j,x} - x) - \theta + \varepsilon_\phi, \qquad s_t^i = s_j + \varepsilon_s,$$

with independent $\varepsilon_r \sim \mathcal N(0, \sigma_r^2)$, $\varepsilon_\phi \sim \mathcal N(0, \sigma_\phi^2)$ and $\varepsilon_s \sim \mathcal N(0, \sigma_s^2)$. Write $\hat r$ and $\hat\phi$ for the noise-free values. The density of one feature is

$$p(f_t^i \mid c_t^i, x_t, m) = \mathcal N(r_t^i - \hat r;\ 0, \sigma_r^2)\ \mathcal N(\phi_t^i - \hat\phi;\ 0, \sigma_\phi^2)\ \mathcal N(s_t^i - s_j;\ 0, \sigma_s^2),$$

with the bearing difference wrapped into $(-\pi, \pi]$, and the density of a scan is the product over its features.

**Parameters.** $\sigma_r$ in meters, $\sigma_\phi$ in radians and $\sigma_s$ in the unit of the signature. They are fitted to data. Real range noise often grows with the range; a constant $\sigma_r$ is a simplification.

**Standing assumptions.** The features are independent of each other given the pose and the map, which is an approximation (they come from the same image or scan). The landmarks are points that do not move. The feature extractor finds each landmark at most once per scan.

**Example.** The robot is at $(2, 1, \pi/2)$ and landmark $j$ is at $(5, 5)$. Then $\hat r = \sqrt{3^2 + 4^2} = 5$ and $\hat\phi = \operatorname{atan2}(4, 3) - \pi/2 \approx 0.92730 - 1.57080 = -0.64350$: the landmark is ahead and to the right. With $\sigma_r = 0.1$ m and $\sigma_\phi = 0.05$ rad and no signature, the reading $(5.1, -0.6)$ has the density $\mathcal N(0.1; 0, 0.01)\, \mathcal N(0.04350; 0, 0.0025) \approx 2.41971 \times 5.46478 \approx 13.2232$.

## What it counts

The model assigns a likelihood to a set of features at a hypothesized pose, and it predicts the expected range and bearing of each landmark. One feature costs $O(1)$ time. A scan with $k$ features and known correspondences costs $O(k)$; with unknown correspondences, the maximum likelihood choice for each feature compares it with all $m$ landmarks, $O(k m)$, and joint choices can cost exponential time in $k$. In an EKF the model enters through its mean and its Jacobian; in a particle filter through its density.

## Relation to other models

- **[Beam range finder model](/beam-range-finder-model/) and [likelihood field model](/likelihood-field-model/).** Use every raw beam of a dense scan against a dense map. The landmark model first reduces the data to a few features, which is much cheaper and fits sparse maps, but it loses the information in the rest of the scan and depends on the feature extractor.
- **Range-only and bearing-only models.** Keep one of the two numbers. Radio beacons give range only; a single camera gives bearing only. Each needs more measurements to fix a pose than the full model.
- **Camera projection.** A camera measures the direction of a 3D point through a projection, the 3D cousin of the bearing. [Perspective-n-point](/perspective-n-point/) recovers a camera pose from several such measurements of known points.
- **[Extended Kalman filter](/extended-kalman-filter/).** EKF localization and EKF SLAM use this model, linearized with the Jacobian below.

## Known results in the model

- **Theorem (Jacobian).** With $\delta_x = m_{j,x} - x$, $\delta_y = m_{j,y} - y$ and $q = \delta_x^2 + \delta_y^2$, the Jacobian of $(\hat r, \hat\phi)$ with respect to the pose $(x, y, \theta)$ is

  $$H = \begin{pmatrix} -\delta_x / \sqrt q & -\delta_y / \sqrt q & 0 \\ \delta_y / q & -\delta_x / q & -1 \end{pmatrix},$$

  and the Jacobian with respect to the landmark position is the negative of the first two columns. In the example, $H = \begin{pmatrix} -0.6 & -0.8 & 0 \\ 0.16 & -0.12 & -1 \end{pmatrix}$. $H$ is not defined at $q = 0$, and the bearing row grows like $1/\sqrt q$ near the landmark, so the linearization is poor for close landmarks.
- **Theorem (one landmark fixes a curve).** The poses that give a noise-free reading $(r, \phi)$ of landmark $j$ are exactly the poses $(m_{j,x} + r\cos\gamma,\ m_{j,y} + r\sin\gamma,\ \gamma - \pi - \phi)$ for $\gamma \in [0, 2\pi)$: the robot stands on the circle of radius $r$ around the landmark and faces so that the landmark has bearing $\phi$. Sampling $\gamma$ uniformly and adding noise to $r$ and $\phi$ gives samples of poses from one feature, which can seed particles for global localization. In the example, $\gamma = \operatorname{atan2}(-4, -3) \approx -2.21430$ gives back $(2, 1)$ and the heading $\gamma - \pi - \hat\phi \equiv \pi/2$.
- **Theorem (two landmarks fix the pose).** Two noise-free readings of two distinct landmarks with known correspondence determine the pose uniquely. Let $b_i = r_i (\cos\phi_i, \sin\phi_i)$ be landmark $i$ in the robot frame and $R(\theta)$ the rotation by $\theta$. Then $m_2 - m_1 = R(\theta)(b_2 - b_1)$, and since $m_2 \ne m_1$ this fixes $\theta$ modulo $2\pi$; then the position is $m_1 - R(\theta) b_1$.
- **Data association.** With unknown correspondences, choosing for each feature the landmark of maximum likelihood is fast but can make wrong choices that an EKF cannot undo. [Joint compatibility branch and bound](/joint-compatibility-branch-and-bound/) tests the choices for all features together, at a cost that is exponential in the number of features in the worst case.
- **Heuristic (Gaussian in polar coordinates).** The noise is Gaussian in range and bearing, so in Cartesian coordinates the uncertainty of a landmark seen from far away is a curved, banana-shaped region. EKF SLAM approximates it with a Gaussian in Cartesian coordinates, which is accurate only when $\sigma_\phi$ is small.

## References
