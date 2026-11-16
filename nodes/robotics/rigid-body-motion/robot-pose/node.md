---
tag: 9204S9
kind: definition
slug: robot-pose
name: Pose
aliases:
- position and orientation
area: robotics/rigid-body-motion
level: intro
summary: The position and orientation of a frame relative to another, an element of SE(2) in the plane or SE(3) in space.
prereqs: [special-euclidean-group, homogeneous-transformation-matrix]
see_also: [pose-compounding-operators, uncertainty-on-lie-groups, pose-graph, configuration-space, odometry-motion-model, dead-reckoning, unit-quaternion-rotation, roll-pitch-yaw-angles]
sources:
  - book: isbn:9780262201629
    title: Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005
    locator: Chapter 5, Section 5.2.1 (kinematic configuration; the pose (x, y, theta) of a mobile robot in the plane)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Sections 3.1 and 3.3.1 (rigid-body motions in the plane, and homogeneous transformation matrices)
---

The pose of a robot, or of any rigid body, is its position together with its orientation, given as the place and the direction of a body frame relative to a reference frame.
In the plane a pose is three numbers $(x, y, \theta)$, an element of SE(2), and in space it is a rotation matrix and a position $(R, p)$, an element of the [special Euclidean group](/special-euclidean-group/) SE(3).
The same object is both a place where the body is and a motion that takes the reference frame to the body frame, which is why poses compose by matrix product and not by vector addition.
Mapping, localization and manipulation all work with poses: the pose of the robot in the map, of a landmark seen by a camera, or of a tool relative to a part.

## Definition

**Pose in the plane.**
Let $\{a\}$ be a reference frame and $\{b\}$ a body frame, both in the plane.
The pose of $\{b\}$ in $\{a\}$ is $x_{ab} = (x, y, \theta)$, where $(x, y)$ are the $\{a\}$ coordinates of the origin of $\{b\}$, and $\theta$ is the angle from the $x$ axis of $\{a\}$ to the $x$ axis of $\{b\}$, counterclockwise, usually wrapped to $[-\pi, \pi)$.
Its matrix in SE(2) is

$$T_{ab} = \begin{pmatrix} \cos\theta & -\sin\theta & x \\ \sin\theta & \cos\theta & y \\ 0 & 0 & 1 \end{pmatrix} .$$

**Pose in space.**
The pose of $\{b\}$ in $\{a\}$ is $T_{ab} = (R_{ab}, p_{ab}) \in SE(3)$, where $p_{ab}$ is the position of the origin of $\{b\}$ in $\{a\}$ coordinates and the columns of $R_{ab} \in SO(3)$ are the axes of $\{b\}$ in $\{a\}$ coordinates.
As a [homogeneous transformation matrix](/homogeneous-transformation-matrix/),

$$T_{ab} = \begin{pmatrix} R_{ab} & p_{ab} \\ 0 & 1 \end{pmatrix} .$$

**The rules of the subscripts.**
A point with coordinates $x_b$ in $\{b\}$ has the coordinates $x_a = R_{ab}x_b + p_{ab}$ in $\{a\}$.
Poses chain by $T_{ac} = T_{ab}T_{bc}$, and the inverse is $T_{ba} = T_{ab}^{-1} = (R_{ab}^{\mathsf T}, -R_{ab}^{\mathsf T}p_{ab})$.
The inner subscripts must match in a product.
In the robotics literature on uncertain poses, the planar product $x_{ab} \oplus x_{bc}$ and the inverse $\ominus x_{ab}$ are the [pose compounding operators](/pose-compounding-operators/).

**Representations in space.**
The group SE(3) has dimension 6, but the 12 numbers of $(R, p)$ are not free.
Common ways to store a pose are the $4 \times 4$ matrix, the position with a [unit quaternion](/unit-quaternion-rotation/) (7 numbers, with $q$ and $-q$ the same), the position with [roll-pitch-yaw angles](/roll-pitch-yaw-angles/) (6 numbers, with [gimbal lock](/gimbal-lock/)), the exponential coordinates of the [exponential map of SE(3)](/se3-exponential-map/) (6 numbers, good near a reference pose), and the [dual quaternion](/dual-quaternion/) (8 numbers).

## Examples and non-examples

**A robot on the floor.**
A robot at $x_{wr} = (2, 1, \pi/2)$ in the world frame $\{w\}$ stands at $(2, 1)$ and faces the $+y$ direction.
Its matrix is $T_{wr} = \begin{pmatrix} 0 & -1 & 2 \\ 1 & 0 & 1 \\ 0 & 0 & 1 \end{pmatrix}$.

- A landmark 1 m straight ahead has robot coordinates $(1, 0)$ and world coordinates $T_{wr}(1, 0, 1)^{\mathsf T} = (2, 2, 1)^{\mathsf T}$, that is $(2, 2)$.
- The inverse pose is $x_{rw} = (-1, 2, -\pi/2)$: the world origin is 1 m behind the robot and 2 m to its left. Check: the vector from the robot to the origin is $(-2, -1)$, and its parts along the robot axes $(0, 1)$ and $(-1, 0)$ are $-1$ and $2$.
- A second robot at $x_{ws} = (3, 3, \pi)$ has the relative pose $x_{rs} = x_{rw} \oplus x_{ws} = (2, -1, \pi/2)$: 2 m ahead of the first robot and 1 m to its right, turned by a quarter turn to the left relative to it.

**A pose in space.**
The pose with $R = R_z(\pi/2)$ and $p = (1, 1, 0)$ is the check value of the [exponential map of SE(3)](/se3-exponential-map/).
As a position and a quaternion it is $((1, 1, 0), (0.70711, 0, 0, 0.70711))$.

**Non-example: the difference of two pose vectors.**
For the two robots above, $x_{ws} - x_{wr} = (1, 2, \pi/2)$, but the pose of the second robot relative to the first is $(2, -1, \pi/2)$.
The difference is in world axes, not in the axes of the first robot, so it is not a relative pose.

**Non-example: the average of two headings.**
The headings $3.1$ and $-3.1$ rad point in nearly the same direction, close to $\pi$.
Their arithmetic mean is $0$, which points the other way.
Means of poses must be taken on the group, as in [uncertainty on Lie groups](/uncertainty-on-lie-groups/), or at least with the angles unwrapped about a reference.

**Non-example: a location.**
A position $(x, y)$ without a heading is a location, not a pose.
Thrun, Burgard and Fox make this distinction for mobile robots.
A heading alone is an orientation, or an attitude in aerospace.

**Non-example: the configuration of an arm.**
The joint angles of an arm are a point in its [configuration space](/configuration-space/), not a pose.
Forward kinematics maps them to the pose of the tool frame, and many joint vectors can give the same pose.

**Non-example: a twist.**
A [twist](/rigid-body-twist/) is a velocity of a body, an element of the Lie algebra, not a place.
Integrating a constant twist for unit time gives a pose, its exponential.

## Related definitions

- [Special Euclidean group](/special-euclidean-group/) and [rigid-body transformation](/rigid-body-transformation/): the set of all poses with its composition.
- [Pose compounding operators](/pose-compounding-operators/): $\oplus$ and $\ominus$ on planar and spatial poses, with the first-order propagation of their covariances.
- [Uncertainty on Lie groups](/uncertainty-on-lie-groups/): a random pose as a mean pose times a small random motion.
- [Pose graph](/pose-graph/): a graph of robot poses with measured relative poses on its edges.
- [Odometry motion model](/odometry-motion-model/) and [dead reckoning](/dead-reckoning/): the pose of a mobile robot from its own motion measurements.
- [Configuration space](/configuration-space/): for a free rigid body, the configuration space is the set of poses, SE(2) or SE(3).

## References
