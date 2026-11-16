---
tag: PCHM7K
kind: definition
slug: base-inertial-parameters
name: Base inertial parameters
aliases:
- minimal dynamic parameters
area: robotics/robot-dynamics
level: advanced
summary: The smallest set of combinations of the link masses, first moments and inertias that determines the joint torques of a robot for every motion; only these can be identified.
prereqs: [spatial-inertia, linearity-in-dynamic-parameters]
see_also: [dynamic-parameter-identification, joint-space-inertia-matrix, qr-decomposition, singular-value-decomposition, condition-number, kinematic-calibration, least-squares-problem, linear-matrix-inequality]
sources:
  - paper: doi:10.1109/70.56655
    title: Maxime Gautier and Wisama Khalil, Direct calculation of minimum set of inertial parameters of serial robots, IEEE Transactions on Robotics and Automation 6(3), 1990
    locator: pages 368 to 373
  - paper: doi:10.1109/70.56663
    title: Hirokazu Mayeda, Koji Yoshida and Koichi Osuka, Base parameters of manipulator dynamic models, IEEE Transactions on Robotics and Automation 6(3), 1990
    locator: pages 312 to 321
  - paper: doi:10.1002/rob.4620080405
    title: Maxime Gautier, Numerical calculation of the base inertial parameters of robots, Journal of Robotic Systems 8(4), 1991
    locator: pages 485 to 506
  - paper: doi:10.1177/0278364913514870
    title: "Cristóvão D. Sousa and Rui Cortesão, Physical feasibility of robot base inertial parameter identification: a linear matrix inequality approach, The International Journal of Robotics Research 33(6), 2014"
    locator: pages 931 to 944
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 6, Model Identification, by John Hollerbach, Wisama Khalil and Maxime Gautier, pages 113 to 138"
---

The base inertial parameters of a robot are a minimal set of linear combinations of its standard inertial parameters (the mass, the first moment of mass and the six entries of the inertia matrix of each link) that fixes the joint torques for every motion. Some standard parameters have no effect on the torques at all, and others act only in fixed combinations, so torque measurements can never separate them. The base parameters are what is left: the combinations that the data can determine.

## Definition

By [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/), the inverse dynamics of a rigid robot with $N$ links is
$$\tau = Y(q, \dot q, \ddot q)\, \pi ,$$
with the regressor $Y$ of size $n \times 10N$ and the standard parameter vector $\pi \in \mathbb{R}^{10N}$, ten numbers per link from its [spatial inertia](/spatial-inertia/). Let $r$ be the largest rank of the matrix formed by stacking $Y(q_k, \dot q_k, \ddot q_k)$ for any finite set of motion samples $k$. Generically $r < 10N$.

A vector $\pi_B = K \pi \in \mathbb{R}^r$, with a constant matrix $K$ of size $r \times 10N$, is a set of **base inertial parameters** if there is a regressor $Y_B$ of size $n \times r$ with
$$Y(q, \dot q, \ddot q)\, \pi = Y_B(q, \dot q, \ddot q)\, \pi_B \quad \text{for all } q, \dot q, \ddot q \text{ and all } \pi .$$
Two parameter vectors $\pi$ and $\pi'$ then give the same torques for every motion if and only if $K\pi = K\pi'$. So $\pi_B$ is exactly the identifiable part of $\pi$, and $r$ is the number of base parameters.

A standard construction (Gautier 1991) stacks the regressor at many random samples and finds, by a [QR decomposition](/qr-decomposition/) with column pivoting or by the [SVD](/singular-value-decomposition/), $r$ independent columns $Y_1$ and the constant matrix $\beta$ with $Y_2 = Y_1 \beta$ for the other columns $Y_2$. Then $\pi_B = \pi_1 + \beta \pi_2$ and $Y_B = Y_1$. The choice of the independent columns is not unique, so the base parameters are not unique either; they are unique up to an invertible linear map. Gautier and Khalil (1990) gave closed-form rules that group the parameters of a serial robot link by link, and Mayeda, Yoshida and Osuka (1990), in the same issue of the same journal, derived the base parameters of manipulator dynamic models.

## Examples and non-examples

**A planar arm in a vertical plane.** Take the planar arm with two revolute joints, link 1 of length $l_1$, and per link the four parameters that act in the plane: the inertia $I_i$ about the joint axis, the first moments $m x_i$ and $m y_i$ in the link frame, and the mass $m_i$. That is 8 standard parameters. The rank of the stacked regressor is 6, and a set of base parameters is
$$\pi_B = \big(I_1 + m_2 l_1^2,\ \ m x_1 + l_1 m_2,\ \ m y_1,\ \ I_2,\ \ m x_2,\ \ m y_2\big).$$
The mass $m_1$ has no effect, because link 1 turns about a fixed axis, and $m_2$ acts only through the two combinations with $I_1$ and $m x_1$: link 2 appears to link 1 as a point mass $m_2$ at the distance $l_1$ plus a body that turns about joint 2.

**The same arm in a horizontal plane.** Without gravity in the plane of motion, $m x_1$ and $m y_1$ have no effect either, and the rank is 4: $\pi_B = (I_1 + m_2 l_1^2, I_2, m x_2, m y_2)$.

**Non-example: the standard parameters.** The full vector $\pi$ is not a set of base parameters when $r < 10N$: there are vectors $\pi \ne \pi'$ with the same torques for all motions, so no experiment can give $\pi$.

**Non-example: separate masses.** In the vertical arm, $(I_1, m_2)$ cannot be part of a set of base parameters, because the torques depend on them only through $I_1 + m_2 l_1^2$. Adding 1 kg m$^2$ to $I_1$ and removing $1 / l_1^2$ kg from $m_2$ (with the matching change of $m x_1$) gives the same torques.

**Non-example: a physical robot.** A value of $\pi_B$ that fits the data may not come from any physical $\pi$, that is from links with positive masses and inertia matrices that satisfy the triangle inequalities. Physical consistency is a separate condition on $\pi$; Sousa and Cortesão (2014) state the condition for base parameters as a [linear matrix inequality](/linear-matrix-inequality/).

## Related definitions

- The regressor and the parameter vector: [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/).
- The estimation of $\pi_B$ from torque data: [dynamic parameter identification](/dynamic-parameter-identification/). Its least squares problem has a full rank regressor only after the reduction to base parameters.
- The [joint-space inertia matrix](/joint-space-inertia-matrix/) depends on $\pi$ only through the base parameters, as every other term of the dynamics does.
- The same idea in kinematics: the identifiable combinations of the geometric errors in [kinematic calibration](/kinematic-calibration/).
- The numerical rank of the stacked regressor is a question of the [condition number](/condition-number/) and of a threshold on the singular values.

## References
