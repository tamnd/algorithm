---
tag: 9TEHQS
kind: problem
slug: online-slam
name: Online SLAM
aliases:
- filtering SLAM
area: robotics/localization-and-slam
level: core
summary: SLAM that estimates only the current pose and the map, marginalizing out past poses as it goes.
prereqs: [slam-problem, bayes-filter, filtering]
see_also: [full-slam, slam-problem, ekf-slam, extended-information-filter, sparse-extended-information-filter, monoslam, schur-complement, ekf-slam-convergence-theorem]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 10 (the online SLAM problem and EKF SLAM) and Chapter 12 (the sparse extended information filter and the effect of marginalizing past poses)"
  - paper: doi:10.1109/MRA.2006.1638022
    title: "Hugh Durrant-Whyte and Tim Bailey, Simultaneous localization and mapping, part I, IEEE Robotics and Automation Magazine 13(2), 2006, from page 99"
    locator: the probabilistic form of SLAM as a recursive estimate of the current pose and the map
---

Online SLAM is the form of the [SLAM problem](/slam-problem/) that asks only for the current pose and the map, $p(x_t, m \mid z_{1:t}, u_{1:t})$, and updates this estimate at every step as new data arrive. It differs from [full SLAM](/full-slam/), which asks for the whole path, $p(x_{1:t}, m \mid z_{1:t}, u_{1:t})$: online SLAM integrates out each past pose as soon as the robot has moved on, so its state does not grow with time, but it cannot correct the past path later. The general problem, with both forms, is on the [SLAM problem](/slam-problem/) page. Online SLAM is a [filtering](/filtering/) problem, and the classical solutions are filters such as [EKF SLAM](/ekf-slam/).

## In plain words

The robot keeps a single best guess of where it is now and where everything on the map is, with a measure of how sure it is. After each move and each reading, it updates this guess and forgets the details of where it was before. This keeps the memory small and steady, and it gives an answer at once, which a moving robot needs. The price is that an old mistake cannot be fixed by going back over the old data, because that data is no longer kept. Everything the past taught is folded into the present guess.

## Definition

**Input.** At each step $t$, a control $u_t$ and a reading $z_t$, a motion model $p(x_t \mid x_{t-1}, u_t)$ and a measurement model $p(z_t \mid x_t, m)$. The map $m$ does not change.

**Output.** At each step, the posterior $p(x_t, m \mid z_{1:t}, u_{1:t})$ over the current pose and the map, or an approximation of it, such as a mean and a covariance.

**The recursion.** Online SLAM is the [Bayes filter](/bayes-filter/) on the state $(x_t, m)$, in which only the pose moves:

$$p(x_t, m \mid z_{1:t}, u_{1:t}) = \eta \, p(z_t \mid x_t, m) \int p(x_t \mid x_{t-1}, u_t) \, p(x_{t-1}, m \mid z_{1:t-1}, u_{1:t-1}) \, \mathrm{d}x_{t-1}.$$

The integral removes the previous pose. Step by step, the online posterior at time $t$ is thus the full posterior with all the past poses $x_{1:t-1}$ integrated out.

## Variants

- **With known or unknown correspondences.** Without them, the filter must also solve [data association](/data-association-slam/) at each step.
- **Gaussian and particle representations.** A Gaussian over $(x_t, m)$ in [EKF SLAM](/ekf-slam/); its inverse, the information form, in the [extended information filter](/extended-information-filter/); particles in [FastSLAM](/fastslam/), which samples whole paths but keeps only what the current step needs.
- **Fixed-lag smoothing.** A middle way keeps the last few poses and integrates out only the older ones. This is fixed-lag [smoothing](/smoothing/).

## Examples

**Why the past poses make the map dense, by hand.** A robot on a line starts at $x_0 = 0$, moves to $x_1$ and then to $x_2$, with odometry of variance 1 each time. From $x_1$ it reads landmark $a$, and from $x_2$ landmark $b$, also with variance 1. In the information form, which is the inverse covariance, each motion step and each reading adds a term that links only the variables it involves. Over $(x_1, x_2, a, b)$ the information matrix is

$$\Omega = \begin{pmatrix} 3 & -1 & -1 & 0 \\ -1 & 2 & 0 & -1 \\ -1 & 0 & 1 & 0 \\ 0 & -1 & 0 & 1 \end{pmatrix}.$$

The entry of $x_1$ is 3: one for the step from $x_0$, one for the step to $x_2$, one for the reading of $a$. The entry of $(a, b)$ is 0: the two landmarks are linked only through the path. This is the matrix of [full SLAM](/full-slam/).

Online SLAM integrates out $x_1$. For a Gaussian this is the [Schur complement](/schur-complement/): subtract $\Omega_{r 1} \Omega_{11}^{-1} \Omega_{1 r}$, where $\Omega_{1 r} = (-1, -1, 0)$ are the links of $x_1$ to $(x_2, a, b)$ and $\Omega_{11} = 3$. Over $(x_2, a, b)$ the result is

$$\Omega' = \begin{pmatrix} 2 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 1 \end{pmatrix} - \frac{1}{3} \begin{pmatrix} 1 & 1 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 0 \end{pmatrix} = \begin{pmatrix} 5/3 & -1/3 & -1 \\ -1/3 & 2/3 & 0 \\ -1 & 0 & 1 \end{pmatrix}.$$

A new link $-1/3$ has appeared between $x_2$ and $a$, which no reading made. Each pose that is integrated out links all its neighbours to each other. Over many steps, every landmark seen from the path gets linked to every other, and the online information matrix, like the covariance, becomes dense. The full SLAM matrix stays sparse because it keeps the poses.

## Known algorithms

- **[EKF SLAM](/ekf-slam/).** One Gaussian over the pose and $m$ landmarks, $O(m^2)$ time per update and $O(m^2)$ memory.
- **[Extended information filter](/extended-information-filter/).** The same Gaussian in information form. A reading is cheap to add, but the motion step and the recovery of the mean are costly.
- **[Sparse extended information filter](/sparse-extended-information-filter/).** It removes weak links of the information matrix to keep it sparse. This sparsification is an approximation, and it makes the estimate overconfident.
- **[MonoSLAM](/monoslam/).** EKF SLAM with one camera as the only sensor.
- **Particle filters.** [FastSLAM](/fastslam/) and [grid-based RBPF SLAM](/grid-based-rbpf-slam/) run online, step by step, but each particle carries a path, so they estimate the full posterior over paths and use it online.

## Bounds

- **Dense state (theorem).** In the linear Gaussian case, the landmarks become fully correlated in the limit, by the [EKF SLAM convergence theorem](/ekf-slam-convergence-theorem/). An exact Gaussian online posterior over $m$ landmarks then needs $\Theta(m^2)$ numbers, and any exact update that touches all correlations costs $\Omega(m^2)$. The example above shows the same effect in the information form: integrating out the poses makes it dense.
- **Same answer as full SLAM in the linear Gaussian case (theorem).** The marginal of a Gaussian keeps the mean and the covariance of the remaining variables. So when the models are linear and the noise is Gaussian, the online estimate of $(x_t, m)$ equals that part of the full SLAM solution. With nonlinear models the two differ: a filter linearizes each step once and cannot go back, while full SLAM can linearize again at better estimates.

## Reductions

- **From full SLAM.** Integrate out $x_{1:t-1}$ from the full posterior.
- **To a Bayes filter.** Online SLAM is a [Bayes filter](/bayes-filter/) whose state is the pose and the static map.
- **Localization.** If the map is known, the online posterior is the localization posterior $p(x_t \mid z_{1:t}, u_{1:t}, m)$, see [mobile robot localization](/mobile-robot-localization/).

## Applications

Online SLAM is the form that a robot needs when it must act on its estimate at once and has a fixed budget of memory and time per step: small indoor robots, drones that track their position against a small map, and camera tracking for augmented reality, as in [MonoSLAM](/monoslam/). Most large systems today solve full SLAM or a fixed-lag form instead, and keep an online estimate only for the newest pose.

## References
