---
tag: Z8QZF9
kind: technique
slug: pose-compounding-operators
name: Pose compounding operators
aliases:
- Smith-Self-Cheeseman compounding
- head-to-tail composition
area: robotics/rigid-body-motion
level: core
summary: The oplus and ominus operators that compose and invert uncertain relative poses and carry their covariances to first order.
model: real-ram
complexity:
  vars: {p: the number of relative poses in a chain}
  time: {worst: Θ(p)}
  space: {extra: Θ(1)}
prereqs: [robot-pose, covariance-matrix]
see_also: [uncertainty-on-lie-groups, ekf-slam, pose-graph, dead-reckoning, odometry-motion-model, extended-kalman-filter, delta-method, unscented-kalman-filter]
sources:
  - paper: doi:10.1007/978-1-4613-8997-2_14
    title: "Randall Smith, Matthew Self and Peter Cheeseman, Estimating uncertain spatial relationships in robotics, in I. J. Cox and G. T. Wilfong (eds.), Autonomous Robot Vehicles, Springer, 1990, 167 to 193"
    locator: the whole chapter (the compounding and inverse operations, their Jacobians and the first-order covariance)
  - paper: arxiv:1304.3111
    title: "Randall Smith, Matthew Self and Peter Cheeseman, Estimating uncertain spatial relationships in robotics, Uncertainty in Artificial Intelligence 2, 1988, 435 to 461"
    locator: Section 3.2 (3.2.1 compounding, 3.2.2 the inverse relationship, 3.2.3 composite relationships) and Appendix A (the six degree of freedom case)
  - paper: doi:10.1177/027836498600500404
    title: Randall C. Smith and Peter Cheeseman, On the representation and estimation of spatial uncertainty, The International Journal of Robotics Research 5(4), 56 to 68, 1986
    locator: the whole paper (approximate transformations, their compounding and merging)
---

The pose compounding operators of Smith, Self and Cheeseman are two operations on relative [poses](/robot-pose/) with uncertainty: $\oplus$ chains two relative poses head to tail, and $\ominus$ reverses one.
Each operator returns a mean pose and a [covariance matrix](/covariance-matrix/), which it gets by a first-order Taylor expansion of the exact pose formula, so the covariance is a linearization and not the exact spread.
With these two operators and the rule for correlated inputs, every relation between frames in a network of uncertain poses can be computed step by step.
They are the basis of stochastic maps, [EKF SLAM](/ekf-slam/) and the edges of a [pose graph](/pose-graph/).

## In plain words

A robot knows where it is only roughly.
It drives a short way, and it knows that step only roughly too.
To find where it is now, you add the step to the old place, but the step is measured in the robot's own direction, so you must first turn it by the robot's heading.
The doubt in the new place comes from the doubt in the old place and the doubt in the step.
A doubt in the heading swings the step to the side, so it adds doubt across the path, more for a longer step.
The operators do this sum and this turn, and they spread the doubts with straight-line rules.
The straight-line rules are good for small doubts and wrong for large heading doubts.

## When it applies

- Poses are planar, $x_{ij} = (x, y, \phi)$, the pose of frame $j$ in frame $i$, or spatial with a fixed parametrization (Appendix A of Smith, Self and Cheeseman uses Euler angles and roll-pitch-yaw angles).
- Each uncertain pose is summarized by a mean and a covariance, and the covariance of $x_{ij}$ is written in the axes of frame $i$.
- The uncertainty is small compared with the curvature of the pose formula, mainly the heading standard deviation times the distance that it swings. Then the first-order answer is close, as the examples show.
- The cross-covariances between inputs are known. If two poses share an error source, the cross term must be carried.

## The template

Let $x_1 = x_{ij} = (x_1, y_1, \phi_1)$ and $x_2 = x_{jk} = (x_2, y_2, \phi_2)$.
The **compound** $x_3 = x_{ik} = x_{ij} \oplus x_{jk}$ is the product of the two planar transforms:

$$x_{ij} \oplus x_{jk} = \begin{pmatrix} x_1 + x_2\cos\phi_1 - y_2\sin\phi_1 \\ y_1 + x_2\sin\phi_1 + y_2\cos\phi_1 \\ \phi_1 + \phi_2 \end{pmatrix} .$$

Its Jacobian $J_\oplus = \partial x_{ik}/\partial(x_{ij}, x_{jk}) = [J_{1\oplus}\ J_{2\oplus}]$, written with the result as in the paper, is

$$J_{1\oplus} = \begin{pmatrix} 1 & 0 & -(y_3 - y_1) \\ 0 & 1 & x_3 - x_1 \\ 0 & 0 & 1 \end{pmatrix}, \qquad J_{2\oplus} = \begin{pmatrix} \cos\phi_1 & -\sin\phi_1 & 0 \\ \sin\phi_1 & \cos\phi_1 & 0 \\ 0 & 0 & 1 \end{pmatrix} .$$

```pseudo id=main
COMPOUND(x1, C1, x2, C2, C12)            ▷ x1 = x_ij, x2 = x_jk, C12 = cov(x1, x2)
L1  (x1, y1, φ1) ← x1 ; c ← cos φ1 ; s ← sin φ1
L2  x3 ← (x1 + c x2 - s y2, y1 + s x2 + c y2, wrap(φ1 + φ2))
L3  J1 ← [[1, 0, -(y3 - y1)], [0, 1, x3 - x1], [0, 0, 1]]
L4  J2 ← [[c, -s, 0], [s, c, 0], [0, 0, 1]]
L5  C3 ← J1 C1 J1ᵀ + J2 C2 J2ᵀ + J1 C12 J2ᵀ + J2 C12ᵀ J1ᵀ
L6  return (x3, C3)
```

Line L5 is $J_\oplus \begin{pmatrix} C_1 & C_{12} \\ C_{12}^{\mathsf T} & C_2 \end{pmatrix} J_\oplus^{\mathsf T}$, the first-order covariance of a function of a random vector, the multivariate [delta method](/delta-method/).
For independent inputs, $C_{12} = 0$, and only the first two terms remain.

The **inverse** $x_{ji} = \ominus x_{ij}$ is the pose of frame $i$ in frame $j$:

$$\ominus x_{ij} = \begin{pmatrix} -x\cos\phi - y\sin\phi \\ x\sin\phi - y\cos\phi \\ -\phi \end{pmatrix}, \qquad J_\ominus = \begin{pmatrix} -\cos\phi & -\sin\phi & y_{ji} \\ \sin\phi & -\cos\phi & -x_{ji} \\ 0 & 0 & -1 \end{pmatrix} .$$

```pseudo id=inverse
INVERT(x1, C1)
I1  (x, y, φ) ← x1 ; c ← cos φ ; s ← sin φ
I2  x' ← (-c x - s y, s x - c y, wrap(-φ))
I3  J ← [[-c, -s, y'], [s, -c, -x'], [0, 0, -1]]
I4  return (x', J C1 Jᵀ)
```

In the words of the paper, the uncertainty is not inverted, but expressed from the opposite point of view.

**Composite relations.**
Two poses that share their head frame give $x_{ik} = x_{ij} \ominus x_{kj} = x_{ij} \oplus (\ominus x_{kj})$ (head to head).
Two poses that share their tail frame give $x_{jk} = \ominus x_{ij} \oplus x_{ik}$ (tail to tail), with the Jacobian $[J_{1\oplus}J_\ominus,\ J_{2\oplus}]$.
Applying the operators step by step along a chain gives the same answer as the first-order expansion of the whole chain at once, because the chain rule of derivatives composes the Jacobians in the same way.

**Cost.**
Each operator is a fixed number of operations on $3 \times 3$ matrices, so a chain of $p$ relative poses costs $\Theta(p)$ time and $\Theta(1)$ extra space in the real RAM, if the inputs are independent.

## Classic examples

**A hand example.**
Let $x_{ij} = (2, 1, \pi/2)$ and $x_{jk} = (1, 0, 0)$, both with covariance $C = \operatorname{diag}(0.01, 0.01, 0.0025)$, that is 0.1 m in position and 0.05 rad in heading, independent.

- Mean: $x_{ik} = (2 + 1 \cdot 0 - 0, 1 + 1 \cdot 1 + 0, \pi/2) = (2, 2, \pi/2)$.
- Jacobians: $J_1 = \begin{pmatrix} 1 & 0 & -1 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$, since $y_3 - y_1 = 1$ and $x_3 - x_1 = 0$, and $J_2$ is the quarter-turn rotation.
- $J_1CJ_1^{\mathsf T} = \begin{pmatrix} 0.0125 & 0 & -0.0025 \\ 0 & 0.01 & 0 \\ -0.0025 & 0 & 0.0025 \end{pmatrix}$, and $J_2CJ_2^{\mathsf T} = C$ because $C$ is the same in all directions of the plane.
- Sum: $C_{ik} = \begin{pmatrix} 0.0225 & 0 & -0.0025 \\ 0 & 0.02 & 0 \\ -0.0025 & 0 & 0.005 \end{pmatrix}$.

The heading error of $x_{ij}$ swings the 1 m step, which points along $+y$ in frame $i$, so it adds variance along $x$ and a negative correlation between $x$ and $\phi$.
A Monte Carlo run with 100000 samples (seed 5) gives the sample mean $(2.0003, 1.9991, 1.571)$ and the sample covariance $\begin{pmatrix} 0.02243 & 0.00006 & -0.00249 \\ 0.00006 & 0.02011 & -0.00007 \\ -0.00249 & -0.00007 & 0.00501 \end{pmatrix}$, within the sampling error of the first-order answer.

**The inverse.**
$\ominus(2, 1, \pi/2) = (-1, 2, -\pi/2)$: the frame $i$ origin is 1 m behind frame $j$ and 2 m to its left.
With the same $C$, $J_\ominus = \begin{pmatrix} 0 & -1 & 2 \\ 1 & 0 & 1 \\ 0 & 0 & -1 \end{pmatrix}$, and the covariance is $\begin{pmatrix} 0.02 & 0.005 & -0.005 \\ 0.005 & 0.0125 & -0.0025 \\ -0.005 & -0.0025 & 0.0025 \end{pmatrix}$.

**Order matters.**
$(1, 0, 0) \oplus (2, 1, \pi/2) = (3, 1, \pi/2)$, not $(2, 2, \pi/2)$.
The operator is associative but not commutative, like the matrix product it comes from.

**Where the linearization fails.**
Start at $(0, 0, 0)$ with heading variance $0.25$ (0.5 rad) and drive $x_{jk} = (10, 0, 0)$ with no error.
The true end point is $(10\cos\phi, 10\sin\phi)$ with $\phi \sim N(0, 0.25)$, on an arc.
Its exact moments are $E[x] = 10e^{-0.125} \approx 8.825$, $\operatorname{var} x = 100\big(\tfrac{1 + e^{-0.5}}{2} - e^{-0.25}\big) \approx 2.446$ and $\operatorname{var} y = 50(1 - e^{-0.5}) \approx 19.67$.
The first-order answer is the mean $(10, 0)$, $\operatorname{var} x = 0$ and $\operatorname{var} y = 100 \cdot 0.25 = 25$.
It misses the mean by more than 1 m, and its ellipse is a flat bar where the samples form a curved banana.
[Uncertainty on Lie groups](/uncertainty-on-lie-groups/) fixes much of this by putting the Gaussian in exponential coordinates.

**Dead reckoning.**
A robot compounds its odometry steps, $x_{0,t} = x_{0,t-1} \oplus u_t$, as in [dead reckoning](/dead-reckoning/) and the [odometry motion model](/odometry-motion-model/).
The steps are independent, so each step adds $J_2 C_u J_2^{\mathsf T}$ and swings the old heading variance through $J_1$, and the position covariance grows without bound.

**Landmarks and loop closures.**
In a stochastic map or [EKF SLAM](/ekf-slam/), a landmark seen from the robot is placed by $x_{wl} = x_{wr} \oplus x_{rl}$, with the cross-covariance between robot and landmark kept in the joint state.
The relative pose of two robot poses that are both in the map is the tail-to-tail relation $\ominus x_{wa} \oplus x_{wb}$, which is the prediction of a [pose graph](/pose-graph/) edge.

## Variations

- **Six degrees of freedom.** Appendix A of the paper gives the same operators for poses with Euler angles or roll-pitch-yaw angles. These angles have a singular set ([gimbal lock](/gimbal-lock/)), where the Jacobians blow up.
- **Lie group form.** With a pose as a mean in SE(3) times the exponential of a small Gaussian twist, compounding becomes $\Sigma \approx \mathrm{Ad}_{\bar T_2^{-1}}\Sigma_1\mathrm{Ad}_{\bar T_2^{-1}}^{\mathsf T} + \Sigma_2$ for the right perturbation, with no singular set. See [uncertainty on Lie groups](/uncertainty-on-lie-groups/) and the [adjoint map](/adjoint-map-se3/).
- **Higher order and sampling.** Barfoot and Furgale (2014) add fourth-order terms on SE(3). The [unscented transform](/unscented-kalman-filter/) and plain Monte Carlo avoid derivatives, at the cost of more evaluations.
- **Merging.** Smith and Cheeseman (1986) also merge two estimates of the same relation with the Kalman update, the step that a [Kalman filter](/extended-kalman-filter/) makes.

## Pitfalls

- **Dropped correlations.** $x_{ij} \oplus (\ominus x_{ij})$ is the identity pose and has no uncertainty. With the full correlation, the operators return the zero covariance. If the two inputs are treated as independent, the same example gives $\begin{pmatrix} 0.025 & -0.01 & 0.005 \\ -0.01 & 0.04 & -0.01 \\ 0.005 & -0.01 & 0.005 \end{pmatrix}$, which is pure error. Keep the cross-covariance whenever two poses share an error source.
- **The linearization.** The covariance is first order. With a heading standard deviation of tenths of a radian over meters of travel, the mean moves inside the arc and the true spread is curved, as the example shows. Check the result with samples when the heading is uncertain.
- **Angle wrapping.** Wrap $\phi$ after each operation, and compute means of angles and residuals with wrapped differences. A naive mean of $3.1$ and $-3.1$ rad is 0.
- **The frame of the covariance.** The covariance of $x_{ij}$ is in the axes of frame $i$. A covariance in the robot's own axes must be turned first, which is exactly what $J_{2\oplus}$ does.
- **The order of the arguments.** $J_{1\oplus}$ uses the result $x_3$ and the first pose. Swapping the arguments of $\oplus$ gives a different pose and different Jacobians.

## Exercises

1. Show that $\ominus(\ominus x) = x$, and that $J_\ominus(\ominus x)\,J_\ominus(x) = I$.
2. For $x_{ij} = (0, 0, 0)$, show that $J_{1\oplus}$ has the entries $-y_2$ and $x_2$ in its last column, and explain them as the motion of the end point when the start frame turns by a small angle.
3. Compute the first-order covariance of $x_{ik} = x_{ij} \oplus x_{jk}$ for $x_{ij} = (0, 0, 0)$ with $C_1 = \operatorname{diag}(0, 0, \sigma^2)$ and $x_{jk} = (d, 0, 0)$ with $C_2 = 0$, and compare it with the exact covariance of $(d\cos\phi, d\sin\phi)$. For which $d\sigma$ is the difference in $\operatorname{var} y$ below 10 percent?
4. Use the chain rule to show that compounding a chain $x_{01} \oplus x_{12} \oplus x_{23}$ in either grouping gives the same first-order covariance.

## References
