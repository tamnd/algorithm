---
tag: 8RPTER
kind: concept
slug: manipulability-ellipsoid
name: Manipulability ellipsoid
aliases:
- velocity ellipsoid
- force ellipsoid
area: robotics/robot-kinematics
level: core
summary: The image of the unit ball of joint velocities under the Jacobian, an ellipsoid that shows the easy and hard directions of motion.
prereqs: [geometric-jacobian, singular-value-decomposition, kinematic-singularity]
see_also: [yoshikawa-manipulability-measure, jacobian-statics-duality, condition-number, kinematic-redundancy, null-space-projection, joint-space-inertia-matrix, positive-definite-matrix, convex-polytope]
sources:
  - paper: doi:10.1177/027836498500400201
    title: Tsuneo Yoshikawa, Manipulability of robotic mechanisms, The International Journal of Robotics Research 4(2), 3-9, 1985
    locator: the whole paper (the manipulability ellipsoid, its principal axes from the singular value decomposition, and the measure w)
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 5, Section 5.4 (manipulability, the velocity and force ellipsoids, separate angular and linear ellipsoids, and three scalar measures)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.9 (manipulability ellipsoids, velocity and force, and their duality)
---

The manipulability ellipsoid of a robot arm at a configuration $q$ is the set of end effector velocities that the joints can produce with joint velocities of norm at most 1.
It is the image of a ball under the linear map $J(q)$, the [Jacobian](/geometric-jacobian/), so it is an ellipsoid; its long axes point where the arm moves easily, and its short axes where it moves only slowly.
The force ellipsoid is its dual: the set of end effector forces that joint torques of norm at most 1 can hold, with the same axes and the inverse lengths.
Both collapse at a [kinematic singularity](/kinematic-singularity/), and their volume is the [Yoshikawa measure](/yoshikawa-manipulability-measure/).

## In plain words

Imagine every motor of an arm can spin at most a little, and you try all the ways to spin them together.
The tip of the arm then moves in many ways, and the set of all the tip speeds it can reach has the shape of a stretched ball.
Along the long direction of this shape, the tip moves fast with little effort.
Along the short direction, it moves slowly, and if the shape is flat, the tip cannot move that way at all.
Forces work the other way round.
The tip pushes hard in the direction where it moves slowly, and it pushes weakly where it moves fast, like a lever.
So one picture tells you where the arm is quick and where it is strong.

## The idea

Let $J$ be the $m \times n$ Jacobian at $q$, with full row rank $m \le n$, and let $J = U\Sigma V^{\mathsf T}$ be its [singular value decomposition](/singular-value-decomposition/), with the singular values $\sigma_1 \ge \dots \ge \sigma_m > 0$ and the orthonormal left singular vectors $u_1, \dots, u_m$.

**The velocity ellipsoid.** It is the set

$$E_v = \{ J\dot q : |\dot q| \le 1 \} = \{ \dot x : \dot x^{\mathsf T}(J J^{\mathsf T})^{-1}\dot x \le 1 \}.$$

The two descriptions agree because the smallest $\dot q$ with $J\dot q = \dot x$ is $J^{+}\dot x$, with $J^{+} = J^{\mathsf T}(JJ^{\mathsf T})^{-1}$, and $|J^{+}\dot x|^2 = \dot x^{\mathsf T}(JJ^{\mathsf T})^{-1}\dot x$; so $\dot x$ is reachable with $|\dot q| \le 1$ exactly when this number is at most 1.
Since $JJ^{\mathsf T} = U\Sigma^2 U^{\mathsf T}$, the principal axes of $E_v$ are the vectors $u_i$, and the semi-axis along $u_i$ has the length $\sigma_i$.
The volume of $E_v$ is the volume of the unit ball of $\mathbb{R}^m$ times $\sigma_1 \cdots \sigma_m = \sqrt{\det(JJ^{\mathsf T})}$, which is Yoshikawa's measure $w$.

**The force ellipsoid.** By the [statics duality](/jacobian-statics-duality/), a wrench $\mathcal F$ at the end effector needs the joint torques $\tau = J^{\mathsf T}\mathcal F$.
The wrenches that need torques of norm at most 1 form the set

$$E_f = \{ \mathcal F : |J^{\mathsf T}\mathcal F| \le 1 \} = \{ \mathcal F : \mathcal F^{\mathsf T}(JJ^{\mathsf T})\mathcal F \le 1 \}.$$

It has the same principal axes $u_i$, and the semi-axis along $u_i$ has the length $1/\sigma_i$.
So a direction that is good for speed is bad for force, and the reverse: the product of the two semi-axes along each $u_i$ is 1.
This is the transmission ratio of a lever, in every direction at once.

**Scalar summaries.** Three numbers are common.
The ratio $\sigma_1/\sigma_m$ of the longest to the shortest axis is the [condition number](/condition-number/) of $J$; it is 1 for a round, isotropic ellipsoid and infinite at a singularity.
Its square, $\lambda_{max}/\lambda_{min}$ of $JJ^{\mathsf T}$, is also used.
The volume measure $w = \sigma_1\cdots\sigma_m$ is Yoshikawa's measure.
Lynch and Park use all three.
How large a condition number or how small a $w$ counts as "close to singular" is a rule of thumb for each arm, not a derived bound.

**Units and scaling.** If $J$ has both angular rows (rad/s) and linear rows (m/s), the shape of $E_v$ depends on the choice of units, so the axes have no physical meaning.
Lynch and Park draw separate ellipsoids for the angular part $J_\omega$ and the linear part $J_v$.
The unit ball of joint velocities also treats all joints alike; with joints of different speed limits, use the ball $\dot q^{\mathsf T}W\dot q \le 1$ with a [positive definite](/positive-definite-matrix/) weight $W$, which gives the ellipsoid of $JW^{-1/2}$.
With independent box limits on each joint speed, the true set of tip velocities is a [convex polytope](/convex-polytope/), the image of the box, and the ellipsoid is only a smooth stand-in for it.

**A dynamic version.** Replacing the unit ball of joint velocities by the unit ball of joint torques and the map $J$ by $J M(q)^{-1}$, with the [joint space inertia matrix](/joint-space-inertia-matrix/) $M$, gives an ellipsoid of end effector accelerations at zero velocity and without gravity.

## Examples

**The 2R check configuration.** The planar 2R arm with $L_1 = L_2 = 1$ m at $q = (0, \pi/2)$ has the tip at $(1, 1)$ m and

$$J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}, \qquad JJ^{\mathsf T} = \begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix}.$$

The eigenvalues of $JJ^{\mathsf T}$ are $(3 \pm \sqrt 5)/2 = 2.618$ and $0.382$, so $\sigma_1 = 1.618$ and $\sigma_2 = 0.618$, the golden ratio and its inverse.
The major axis is $u_1 = (0.851, -0.526)$, at $-31.7$ degrees from the $x$ axis, and the minor axis is $u_2 = (0.526, 0.851)$, at $58.3$ degrees.
With joint rates of norm 1 rad/s, the tip can move at up to 1.618 m/s along $u_1$, but only 0.618 m/s along $u_2$.
The area of the ellipse is $\pi\sigma_1\sigma_2 = \pi$, since $\sigma_1\sigma_2 = |\det J| = 1$, and the condition number is $2.618$.

The force ellipse has the same axes with the lengths $1/1.618 = 0.618$ N along $u_1$ and $1/0.618 = 1.618$ N along $u_2$, for joint torques of norm 1 N m.
For example, the force $\mathcal F = 1.618\,u_2 = (0.851, 1.377)$ N needs $\tau = J^{\mathsf T}\mathcal F = (-f_x + f_y, -f_x) = (0.526, -0.851)$ N m, whose norm is 1.

**The stretched arm.** At $q = (0, 0)$, $J = \begin{pmatrix} 0 & 0 \\ 2 & 1 \end{pmatrix}$ has the singular values $\sqrt 5$ and 0.
The velocity ellipse becomes a segment of half-length $\sqrt 5 = 2.236$ along the $y$ axis, across the arm, and the force ellipse becomes an infinite strip: the arm holds any pull along its length with no torque.

**Isotropy.** The shape of the ellipse of a 2R arm depends only on $q_2$.
With $L_1 = L_2 = 1$, $J^{\mathsf T}J$ has the trace $3 + 2\cos q_2$ and the determinant $\sin^2 q_2$, and the condition number is smallest at $\cos q_2 = -2/3$, that is $q_2 \approx 131.8$ degrees, where it is $1.618$.
So with equal links the ellipse is never a circle, and the configuration with the largest area, $q_2 = \pi/2$, is not the roundest one.
With $L_2 = L_1/\sqrt 2$ and $q_2 = 3\pi/4$, the two columns of $J$ are orthogonal and have the same length, $JJ^{\mathsf T} = (L_1^2/2)\,I$, and the ellipse is a circle.

## Where it is used

- **Posture choice.** For a task that needs speed in one direction, choose the configuration whose velocity ellipsoid is long in that direction; for a task that pushes, such as drilling or polishing, choose one whose force ellipsoid is long along the push.
- **Redundancy.** For a [redundant](/kinematic-redundancy/) arm, the [null space projection](/null-space-projection/) of the gradient of $w$ moves the arm along its self-motion toward larger ellipsoids, away from singularities; Yoshikawa (1985) proposed this use.
- **Design.** Comparing ellipsoids over the workspace helps to choose link lengths; the isotropic 2R design above is one such result.
- **Monitoring.** A controller can watch the shortest axis or the condition number and slow down or switch to [damped least squares](/damped-least-squares-inverse-kinematics/) near a singularity; the threshold is set by hand.

## References
