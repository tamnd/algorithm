---
tag: G2C9NX
kind: definition
slug: robot-workspace
name: Robot workspace
aliases:
- reachable workspace
- dexterous workspace
area: robotics/robot-kinematics
level: intro
summary: The set of end effector positions a manipulator can reach over all joint values in range. The dexterous workspace is the part it can reach with every orientation.
prereqs: [forward-kinematics]
see_also: [forward-kinematics, inverse-kinematics, kinematic-singularity, kinematic-redundancy, configuration-space, manipulability-ellipsoid, parallel-manipulator]
sources:
  - paper: doi:10.1115/1.3254968
    title: A. Kumar and K. J. Waldron, The workspaces of a mechanical manipulator, Journal of Mechanical Design 103(3), 1981
    locator: pages 665 to 672, the reachable and the dextrous workspace and how their boundaries are found
  - paper: doi:10.1115/1.3256412
    title: K. C. Gupta and B. Roth, Design considerations for manipulator workspace, Journal of Mechanical Design 104(4), 1982
    locator: pages 704 to 711, the workspace and its dexterous part, and the effect of the link lengths and the hand length
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Section 2.5, Task Space and Workspace (the workspace and the dexterous workspace)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Section 2.10.1, Workspace
---

The workspace of a robot arm is the set of points that its end effector can reach. It is the image of all allowed joint values under the [forward kinematics](/forward-kinematics/) map, so it depends on the link lengths and on the joint limits, and in most uses it ignores obstacles. The **reachable workspace** is the set of points that the end effector can reach with at least one orientation. The **dexterous workspace** is the smaller set of points that it can reach with every orientation. A planar arm with two links of lengths 2 m and 1 m reaches the ring between radii 1 m and 3 m around its base, and no point of it with every heading.

## Definition

Let a manipulator have joint values $q$ in a set $Q \subset \mathbb{R}^n$, usually a box of joint limits. Let its forward kinematics be $T(q) = (R(q), p(q)) \in SE(3)$, where $p(q)$ is the position of a chosen point of the end effector, the tool center point. For a planar arm, replace $SE(3)$ by $SE(2)$ and $SO(3)$ by the circle of headings $\varphi$.

**Reachable workspace.** $W = \{\, p(q) : q \in Q \,\}$.

**Dexterous workspace.** $W_D = \{\, x : \text{for every } R \in SO(3) \text{ there is a } q \in Q \text{ with } T(q) = (R, x) \,\}$.

Clearly $W_D \subseteq W$. Both sets depend on the choice of the tool center point. A longer tool makes $W$ larger and $W_D$ smaller.

**Workspace and task space.** The workspace is a set of positions or poses of the end effector. The task space is the space in which a task is described, for example the plane of a drawing for a pen. The [configuration space](/configuration-space/) is the space of joint values $Q$, not the workspace.

**Where the boundary comes from.** Let $J_p(q) = \partial p / \partial q$ be the $3 \times n$ position Jacobian ($2 \times n$ in the plane). *If $q$ is in the interior of $Q$ and $J_p(q)$ has full row rank, then $p(q)$ is an interior point of $W$.* Proof: then $p$ is a submersion near $q$. By the implicit function theorem, a small ball around $q$ in $Q$ maps onto a neighborhood of $p(q)$. $\blacksquare$ So every boundary point of $W$ is the image of a configuration that is either at a joint limit or where $J_p$ loses rank, a [kinematic singularity](/kinematic-singularity/) of the position map. This is the basis of the methods that trace workspace boundaries.

## Examples and non-examples

**A planar 2R arm.** Links $L_1 = 2$ m and $L_2 = 1$ m, joints without limits. The distance from the base to the tip is $r = \sqrt{L_1^2 + L_2^2 + 2L_1L_2\cos q_2}$, which takes every value from $|L_1 - L_2| = 1$ to $L_1 + L_2 = 3$ as $q_2$ runs over $[0, \pi]$, and $q_1$ turns the arm to any direction. So $W$ is the ring $1 \le r \le 3$, with area $\pi(3^2 - 1^2) = 8\pi \approx 25.1$ m$^2$. The Jacobian determinant is $L_1 L_2 \sin q_2$, zero at $q_2 = 0$ and $q_2 = \pi$, which give $r = 3$ and $r = 1$: the two boundary circles, as the statement above predicts. The heading at the tip is $q_1 + q_2$, which is fixed once the point is fixed up to the two elbow choices, so no point has every heading, and $W_D$ is empty.

**Equal links.** With $L_1 = L_2 = 1$ m the ring becomes the disc $r \le 2$. The base point $r = 0$ is reached with $q_2 = \pi$ and any $q_1$, which is a whole circle of joint values for one point.

**A joint limit that does not shrink the workspace.** Limit the elbow of the arm with $L_1 = 2$, $L_2 = 1$ to $0 \le q_2 \le \pi$. Every radius in $[1, 3]$ is still reached, and $q_1$ still turns the arm freely, so $W$ is still the full ring. The limit removes one of the two inverse kinematic solutions at each point, not any point of the workspace.

**A planar 3R arm and its dexterous workspace.** Links $L_1 = L_2 = 1$ m and $L_3 = 0.5$ m, no limits. For a tip point $x$ and heading $\varphi$, the wrist point is $w = x - L_3(\cos\varphi, \sin\varphi)$, and the first two links reach $w$ if and only if $|w| \le 2$. As $\varphi$ runs over all headings, $w$ runs over the circle of radius 0.5 m around $x$. That circle lies in the disc $|w| \le 2$ if and only if $|x| \le 1.5$. So $W_D$ is the disc of radius $L_1 + L_2 - L_3 = 1.5$ m, while $W$ is the disc of radius $L_1 + L_2 + L_3 = 2.5$ m.

**Non-example: the set of joint values.** The box $Q$ of joint values is the configuration space. Two very different joint vectors can give the same point of $W$, and a straight line in $Q$ is in general a curve in $W$.

**Non-example: points that cannot be joined.** The workspace says which points can be reached, not whether the arm can move between them. With obstacles or with joint limits, two points of $W$ can lie in parts that no path of the arm joins. That question belongs to [motion planning](/motion-planning/).

## Related definitions

- [Forward kinematics](/forward-kinematics/): the workspace is the image of the forward map.
- [Inverse kinematics](/inverse-kinematics/): a point has an inverse kinematic solution if and only if it is in the workspace.
- [Kinematic singularity](/kinematic-singularity/): the boundary of the workspace comes from singular configurations and joint limits.
- [Kinematic redundancy](/kinematic-redundancy/): extra joints can enlarge the dexterous workspace.
- [Manipulability ellipsoid](/manipulability-ellipsoid/): describes how well the arm moves at each point inside the workspace.
- [Parallel manipulator](/parallel-manipulator/): parallel robots have small workspaces for their size, limited by leg lengths, joint ranges and collisions between legs.

### History

Kumar and Waldron (1981) defined the reachable and the dextrous workspace of a manipulator and studied their boundaries. Gupta and Roth (1982) studied how the link lengths and the hand length change the workspace and its dexterous part. Later work traced workspace boundaries from the rank deficiency of the Jacobian and from joint limits.

## References
