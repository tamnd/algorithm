---
tag: YR61S6
kind: concept
slug: uncertainty-on-lie-groups
name: Uncertainty on Lie groups
aliases:
- concentrated Gaussian on SE(3)
area: robotics/rigid-body-motion
level: research
summary: A random pose as a mean in SE(3) times the exponential of a Gaussian twist, so covariances live in the Lie algebra.
prereqs: [se3-exponential-map, adjoint-map-se3, pose-compounding-operators]
see_also: [invariant-extended-kalman-filter, error-state-kalman-filter, pose-graph-optimization, bundle-adjustment, unscented-kalman-filter, ekf-slam, robot-pose, so3-logarithm-map]
sources:
  - paper: doi:10.1109/TRO.2014.2298059
    title: "Timothy D. Barfoot and Paul T. Furgale, Associating uncertainty with three-dimensional poses for use in estimation problems, IEEE Transactions on Robotics 30(3), 679 to 693, 2014"
    locator: the whole paper (perturbations of 4x4 transforms by the exponential map, compounding of uncertain poses to second and fourth order, and fusion of pose measurements)
  - book: isbn:9781107159396
    title: Timothy D. Barfoot, State Estimation for Robotics, Cambridge University Press, 2017
    locator: Chapter 7, Section 7.3 (uncertainty on SO(3) and SE(3), with 7.3.3 compounding poses and 7.3.4 fusing poses)
  - paper: arxiv:1812.01537
    title: Joan Solà, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the sections on right and left perturbations, the adjoint, uncertainty in the tangent space and covariance propagation
  - paper: doi:10.15607/RSS.2012.VIII.034
    title: "Andrew W. Long, Kevin C. Wolfe, Michael J. Mashner and Gregory S. Chirikjian, The banana distribution is Gaussian: a localization study with exponential coordinates, Robotics: Science and Systems VIII, 2012"
    locator: the whole paper (the pose distribution of a noisy planar robot as a Gaussian in exponential coordinates)
  - paper: "Yunfeng Wang and Gregory S. Chirikjian, Error propagation on the Euclidean group with applications to manipulator kinematics, IEEE Transactions on Robotics 22(4), 591 to 602, 2006"
    title: Error propagation on the Euclidean group with applications to manipulator kinematics
    locator: the whole paper (covariances defined on the Lie algebra and their propagation through chains of uncertain motions)
---

Uncertainty on a Lie group is the practice of describing a random rotation or pose by a mean element of the group and a small random perturbation in its tangent space.
For a pose, the model is $T = \bar T \operatorname{Exp}(\xi)$ with $\xi \sim \mathcal N(0, \Sigma)$, where $\bar T$ is in the [special Euclidean group](/special-euclidean-group/) SE(3), $\xi$ is a 6-vector twist and $\operatorname{Exp}$ is the [SE(3) exponential](/se3-exponential-map/).
Every sample is a valid pose, the covariance $\Sigma$ is a 6 by 6 matrix with one row for each degree of freedom, and there is no singularity as there is with Euler angles.
When $\Sigma$ is small, the distribution is called a concentrated Gaussian, and the usual rules for means and covariances carry over with the [adjoint](/adjoint-map-se3/) in place of a rotation of axes.

## In plain words

A pose has a position and a direction, and the set of all poses is curved.
You cannot just add a small random number to each entry of a rotation, because the result is no longer a rotation.
Instead, you take a best guess of the pose and then apply a small random motion to it.
The small motion is a list of six numbers, three for turning and three for sliding, and these six numbers have the usual bell-shaped spread.
So the spread lives in a flat space of small motions, and every sample is still a real pose.
You must say whether the small motion is applied in the robot's own frame or in the fixed frame, because the two give different numbers.
With this model, you can chain, invert, average and combine uncertain poses with simple matrix rules.

## The idea

This page writes a twist as $\xi = (\omega, v)$, angular part first, and $\operatorname{Exp}(\xi) = e^{[\xi]}$ as in Lynch and Park.
It uses the right perturbation $\bar T \operatorname{Exp}(\xi)$ unless it says otherwise.
Barfoot and Furgale, and Barfoot's book, use the left perturbation $\operatorname{Exp}(\xi)\bar T$ and order the twist as $(\rho, \phi)$, translation first, so their adjoint has its blocks in the other order.

**A Gaussian in the tangent space.**
A random pose with mean $\bar T$ and covariance $\Sigma$ is

$$T = \bar T \operatorname{Exp}(\xi), \qquad \xi \sim \mathcal N(0, \Sigma).$$

The vector $\xi$ is in the body frame of $\bar T$.
The mean $\bar T$ is the pose with $\mathbb E[\operatorname{Log}(\bar T^{-1} T)] = 0$, and $\Sigma = \mathbb E[\xi \xi^T]$.
For small $\Sigma$ the density on the group is close to $\exp\!\big(-\tfrac12 \operatorname{Log}(\bar T^{-1}T)^T \Sigma^{-1} \operatorname{Log}(\bar T^{-1}T)\big)$ up to a constant.
The same construction with $\operatorname{Exp}$ of SO(3) and a 3 by 3 covariance gives uncertain rotations.

**Left and right.**
Because $\bar T \operatorname{Exp}(\xi) \bar T^{-1} = \operatorname{Exp}(\mathrm{Ad}_{\bar T}\, \xi)$, the same random pose has the two forms

$$\operatorname{Exp}(\xi_L)\, \bar T = \bar T \operatorname{Exp}(\xi_R), \qquad \xi_L = \mathrm{Ad}_{\bar T}\, \xi_R, \qquad \Sigma_L = \mathrm{Ad}_{\bar T}\, \Sigma_R\, \mathrm{Ad}_{\bar T}^T .$$

The left form puts the noise in the fixed frame, and the right form puts it in the body frame.
A covariance without a statement of its side has no meaning.

**Inverse.**
$T^{-1} = \operatorname{Exp}(-\xi)\, \bar T^{-1} = \bar T^{-1} \operatorname{Exp}(-\mathrm{Ad}_{\bar T}\, \xi)$.
So the inverse has the mean $\bar T^{-1}$ and, in the right perturbation, the covariance $\mathrm{Ad}_{\bar T}\, \Sigma\, \mathrm{Ad}_{\bar T}^T$.
This is exact, because the new perturbation is a linear function of $\xi$.

**Compounding.**
For independent $T_1 = \bar T_1 \operatorname{Exp}(\xi_1)$ and $T_2 = \bar T_2 \operatorname{Exp}(\xi_2)$,

$$T_1 T_2 = \bar T_1 \bar T_2 \operatorname{Exp}(\mathrm{Ad}_{\bar T_2^{-1}}\, \xi_1) \operatorname{Exp}(\xi_2).$$

To first order in the Baker-Campbell-Hausdorff formula, $\operatorname{Exp}(a)\operatorname{Exp}(b) \approx \operatorname{Exp}(a + b)$, so the mean is $\bar T_1 \bar T_2$ and

$$\Sigma \approx \mathrm{Ad}_{\bar T_2^{-1}}\, \Sigma_1\, \mathrm{Ad}_{\bar T_2^{-1}}^T + \Sigma_2 \quad\text{(right)}, \qquad \Sigma \approx \Sigma_1 + \mathrm{Ad}_{\bar T_1}\, \Sigma_2\, \mathrm{Ad}_{\bar T_1}^T \quad\text{(left)}.$$

If $\xi_1$ and $\xi_2$ are correlated, add the cross terms $A \Sigma_{12} + \Sigma_{12}^T A^T$ with $A = \mathrm{Ad}_{\bar T_2^{-1}}$ in the right form.
This is a linearization, like the [pose compounding operators](/pose-compounding-operators/) of Smith, Self and Cheeseman, but the mean stays exactly on the group, and the frames of the noise are explicit.
Barfoot and Furgale also give a fourth-order expression, which they compare with a second-order one, sigma points and Monte Carlo; it matters when the input covariances are large.

**Mean of samples.**
For poses $T_1, \dots, T_N$, iterate

$$\bar T \leftarrow \bar T \operatorname{Exp}\Big(\frac1N \sum_{i=1}^N \operatorname{Log}(\bar T^{-1} T_i)\Big)$$

until the step is small, and take $\Sigma = \frac1N \sum_i \xi_i \xi_i^T$ with $\xi_i = \operatorname{Log}(\bar T^{-1} T_i)$.
This is a Gauss-Newton step for the sum of the squared lengths of the $\xi_i$, and it converges when the samples are concentrated, with rotation angles well below $\pi$ from the mean.

**Fusion and functions.**
To fuse $K$ estimates $(\bar T_k, \Sigma_k)$ of one pose, minimize $\sum_k e_k^T \Sigma_k^{-1} e_k$ with $e_k = \operatorname{Log}(\bar T_k^{-1} T)$ over $T$, by Gauss-Newton with updates $T \leftarrow T \operatorname{Exp}(\delta)$.
To push the uncertainty through a function $y = f(T)$, take $J = \partial f(\bar T \operatorname{Exp}(\xi)) / \partial \xi$ at $\xi = 0$ and $\Sigma_y \approx J \Sigma J^T$.
Filters and smoothers on groups use these two steps again and again.

**Limits.**
The model is good when the rotational standard deviations are small compared with $\pi$.
For larger spreads, $\operatorname{Log}$ wraps at an angle of $\pi$, the mean found by iteration can depend on the start, and the first-order compounding underestimates or overestimates the spread.

## Examples

**The banana is a Gaussian (planar, exact).**
In SE(2) write $\xi = (\omega, v_x, v_y)$.
A robot at the origin gets a heading error $\varphi \sim \mathcal N(0, \sigma^2)$ and then drives 1 m along its own $x$ axis.
The end pose is $(\cos\varphi, \sin\varphi, \varphi)$, a rotation by $\varphi$ about the start point applied to $\bar T = (1, 0, 0)$, so

$$T = \operatorname{Exp}\big((\varphi, 0, 0)\big)\, \bar T \quad\text{exactly}, \qquad \Sigma_L = \operatorname{diag}(\sigma^2, 0, 0).$$

The planar adjoint of a pose with translation $p$ and no rotation is $\begin{pmatrix} 1 & 0 & 0 \\ p_y & 1 & 0 \\ -p_x & 0 & 1 \end{pmatrix}$.
With $\bar T^{-1} = (-1, 0, 0)$, the right perturbation is $\xi_R = \mathrm{Ad}_{\bar T^{-1}} \xi_L = (\varphi, 0, \varphi)$: a turn and a slide to the left, both proportional to $\varphi$.
In both forms the distribution is a Gaussian in the twist, with no approximation.
In the coordinates $(x, y, \theta)$ it is not: the samples lie on an arc.
For $\sigma = 0.5$, $\mathbb E[x] = e^{-\sigma^2/2} = 0.8825$, $\operatorname{var} x = (1 + e^{-2\sigma^2})/2 - e^{-\sigma^2} = 0.0245$ and $\operatorname{var} y = (1 - e^{-2\sigma^2})/2 = 0.1967$.
A Gaussian in $(x, y, \theta)$ from a linearization has the mean $(1, 0, 0)$, $\operatorname{var} x = 0$ and $\operatorname{var} y = 0.25$, and its samples leave the arc.
Long, Wolfe, Mashner and Chirikjian show that the banana-shaped pose cloud of a noisy two-wheeled robot is close to a Gaussian in exponential coordinates.

**Compounding turns the axes.**
Let $T_1$ have a right covariance with the single entry $0.01$ at $v_x$: an error of standard deviation 0.1 m along the $x$ axis of frame 1.
Let $T_2 = \bar T_2$ be exact, a rotation $R_z(\pi/2)$ with no translation.
Then $\mathrm{Ad}_{\bar T_2^{-1}}$ has the diagonal blocks $R_z(-\pi/2)$, which maps $(1, 0, 0)$ to $(0, -1, 0)$.
The composite has the single entry $0.01$ at $v_y$: in the body frame of $T_1 T_2$, which is frame 1 turned by a quarter turn, the old $x$ axis is the $-y$ axis.
Here the formula is exact, because $T_2$ has no noise.
In the left form, the covariance of the composite is $\Sigma_{1,L}$ without change, because the noise stays in the fixed frame.

**Inverse moves heading error into position.**
Let $\bar T$ be a translation by $(2, 0, 0)$ with no rotation, and let the right covariance have only a heading variance $\sigma^2 = 0.01$ (about $z$).
For a heading error $\delta$, $\xi = (0, 0, \delta, 0, 0, 0)$ and $\mathrm{Ad}_{\bar T}\, \xi = (0, 0, \delta, 0, -2\delta, 0)$, because $[p]\omega = (2, 0, 0) \times (0, 0, \delta) = (0, -2\delta, 0)$.
So $T^{-1}$ has the right perturbation $(0, 0, -\delta, 0, 2\delta, 0)$, with $\operatorname{var}\omega_z = 0.01$, $\operatorname{var} v_y = 0.04$ and $\operatorname{cov}(\omega_z, v_y) = -0.02$.
In words: seen from the robot, the world origin is 2 m behind it, and a heading error of $\delta$ moves the origin sideways by $2\delta$.

## Where it is used

- Filters that keep the state on a group: the [error-state Kalman filter](/error-state-kalman-filter/) and the [invariant extended Kalman filter](/invariant-extended-kalman-filter/) hold a covariance of the tangent perturbation, and the [unscented Kalman filter](/unscented-kalman-filter/) on a group maps its sigma points through $\operatorname{Exp}$.
- [Pose graph optimization](/pose-graph-optimization/) writes each edge error as $\operatorname{Log}(Z_{ij}^{-1} X_i^{-1} X_j)$ with an information matrix in the tangent space, and updates each pose by $X \leftarrow X \operatorname{Exp}(\delta)$.
- [Bundle adjustment](/bundle-adjustment/) perturbs camera poses in the same way, so the normal equations have 6 unknowns per camera.
- [EKF SLAM](/ekf-slam/) and the [pose compounding operators](/pose-compounding-operators/) chain uncertain [robot poses](/robot-pose/); the group form keeps each mean a valid pose.
- Uncertain rotations alone use the same model on SO(3), with the [SO(3) logarithm](/so3-logarithm-map/) in place of the SE(3) one; Wang and Chirikjian use covariances on the Lie algebra to propagate errors through the joints of a manipulator.

## References
