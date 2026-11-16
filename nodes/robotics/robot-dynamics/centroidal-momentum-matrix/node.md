---
tag: M8T9ZN
kind: definition
slug: centroidal-momentum-matrix
name: Centroidal momentum matrix
aliases:
- CMM
area: robotics/robot-dynamics
level: advanced
summary: The matrix that maps joint and base velocities to the linear and angular momentum of the whole robot about its center of mass.
prereqs: [spatial-inertia, composite-rigid-body-algorithm]
see_also: [centroidal-dynamics, floating-base-dynamics, whole-body-control, joint-space-inertia-matrix, geometric-jacobian, spatial-vector-algebra, zero-moment-point, convex-mpc-legged-locomotion]
sources:
  - paper: doi:10.1109/IROS.2008.4650772
    title: "David E. Orin and Ambarish Goswami, Centroidal momentum matrix of a humanoid robot: structure and properties, IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2008"
    locator: pages 653 to 659
  - paper: doi:10.1007/s10514-013-9341-4
    title: David E. Orin, Ambarish Goswami and Sung-Hee Lee, Centroidal dynamics of a humanoid robot, Autonomous Robots 35(2-3), 2013
    locator: pages 161 to 176
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 2 (spatial inertia and momentum) and Chapter 6 (composite-rigid-body inertias)"
---

The centroidal momentum matrix (CMM) of a robot is the $6 \times n$ matrix $A_G(q)$ that turns the velocities of all its joints, and of its base if the base is free, into the total momentum of the robot about its center of mass. The top three rows give the angular momentum about the center of mass and the bottom three rows give the linear momentum. Orin and Goswami (2008) named and studied the matrix for humanoid robots. It is the main tool of balance control and [whole-body control](/whole-body-control/) of legged robots, because the rate of the centroidal momentum is set by the contact forces alone; see [centroidal dynamics](/centroidal-dynamics/).

## Definition

Take a robot of rigid bodies in a kinematic tree with $n$ one-degree-of-freedom joints, in the notation of [spatial vector algebra](/spatial-vector-algebra/) with the angular part first. A floating base counts as six joints, three prismatic along the axes of the fixed frame $\{s\}$ and three revolute, with the first five bodies massless. Body $i$ has the [spatial inertia](/spatial-inertia/) $I_i$ in its frame $\{i\}$, the pose $T_{si}(q)$ and the twist $v_i$ in $\{i\}$, and joint $i$ has the screw axis $S_i$ in $\{i\}$. Let $m$ be the total mass and $c(q)$ the center of mass. Let $\{G\}$ be the frame with its origin at $c$ and its axes parallel to $\{s\}$, and let $T_{iG} = T_{si}^{-1} T_{sG}$.

The **centroidal momentum** is the sum of the momenta of the bodies, moved to $\{G\}$:
$$h_G = \begin{pmatrix} k_G \\ l_G \end{pmatrix} = \sum_i \mathrm{Ad}(T_{iG})^T\, I_i\, v_i ,$$
where $k_G$ is the angular momentum about the center of mass and $l_G$ is the linear momentum. Each $v_i$ is linear in $\dot q$, so $h_G$ is linear in $\dot q$. The **centroidal momentum matrix** is the $6 \times n$ matrix $A_G(q)$ with
$$h_G = A_G(q)\, \dot q \quad \text{for all } \dot q .$$

**The columns.** A unit rate of joint $j$, with all other joints still, moves the subtree of $j$ as one rigid body with the twist $S_j$ in $\{j\}$, and moves nothing else. So column $j$ is the momentum of that subtree about $G$:
$$A_G[:, j] = \mathrm{Ad}(T_{jG})^T\, I^c_j\, S_j ,$$
where $I^c_j$ is the composite inertia of the subtree of $j$, as in the [composite rigid body algorithm](/composite-rigid-body-algorithm/). This gives the matrix in $\Theta(n)$ time:

```pseudo id=main
CENTROIDAL-MOMENTUM-MATRIX(model, q)
C1  compute T_si for every body, and X_i ← Ad(T_{λ(i),i}^-1)
C2  for i ← 1 to n do I^c_i ← I_i
C3  for i ← n downto 1 do if λ(i) ≠ 0 then I^c_λ(i) ← I^c_λ(i) + X_i^T I^c_i X_i
C4  m ← Σ_i m_i ; c ← (Σ_i m_i c_i) / m ; T_sG ← (1, c)
C5  for j ← 1 to n do
C6      A_G[:, j] ← Ad(T_sj^-1 T_sG)^T I^c_j S_j
C7  return A_G, m, c
```

**Properties.**

- **The linear rows.** The bottom three rows are $m J_c(q)$, the mass times the Jacobian of the center of mass, because the linear momentum of the robot is $m \dot c$.
- **The base columns.** For a floating base, the columns of the three prismatic base joints are $(0, m e_k)$: moving the whole robot along an axis adds only linear momentum.
- **The locked robot.** If all joints but the base are still, the robot moves as one rigid body with some twist $v_G$ at $G$, and $h_G = I_G v_G$, where $I_G$ is the inertia of the locked robot about $G$. Orin and Goswami call $I_G$ the centroidal composite rigid body inertia.
- **The rate.** $\dot h_G = A_G \ddot q + \dot A_G \dot q$, and by the Newton-Euler equations for the whole robot this equals the sum of the external wrenches about $G$, including gravity. This is the [centroidal dynamics](/centroidal-dynamics/) of the robot.
- **Not integrable.** The angular part $k_G = A_k(q) \dot q$ is not the time derivative of any function of $q$ in general. So a robot can change its orientation with zero angular momentum, as a falling cat does.
- **Relation to the inertia matrix.** If the base is a free 6-dimensional joint with its velocity in the base frame $\{b\}$, the first six rows of the [joint-space inertia matrix](/joint-space-inertia-matrix/) give the momentum of the robot in $\{b\}$. Moving that momentum to $\{G\}$ by $\mathrm{Ad}(T_{bG})^T$ gives $A_G$ for these velocity coordinates.

## Examples and non-examples

**The planar arm with two links.** Take two revolute joints about $z$ at a fixed base, links of 1 m and point masses of 1 kg at the link ends. At $q = (0, \pi/2)$, the masses are at $(1, 0, 0)$ and $(1, 1, 0)$ m, so $m = 2$ kg and $c = (1, 0.5, 0)$ m. The nonzero rows of $A_G$ are
$$k_z: \ (0.5,\ 0.5), \qquad l_x: \ (-1,\ -1), \qquad l_y: \ (2,\ 0),$$
and the rows of $k_x$, $k_y$ and $l_z$ are zero. As a check by hand, joint 1 moves the first mass with the velocity $(0, 1, 0)$ and the second with $(-1, 1, 0)$, so the linear momentum is $(-1, 2, 0)$, and the angular momentum about $c$ is $(0, -0.5) \times (0, 1) + (0, 0.5) \times (-1, 1) = 0 + 0.5$. Joint 2 moves only the second mass, with the velocity $(-1, 0, 0)$, which gives $(-1, 0, 0)$ and $(0, 0.5) \times (-1, 0) = 0.5$. At $\dot q = (1, 1)$ rad/s, $h_G = (0, 0, 1,\ -2, 2, 0)$.

**Non-example: the momentum about a fixed point.** The angular momentum about the base origin is not $k_G$. At the same state it is $k_O = k_G + c \times l_G = 1 + (1 \cdot 2 - 0.5 \cdot (-2)) = 4$ kg m$^2$/s, which is also $\sum_i p_i \times \dot p_i = 1 + 3$. Its rate contains the moment of gravity about $O$, which is why the CMM uses the center of mass.

**Non-example: the Jacobian of the center of mass.** $m J_c$ is only the bottom half of $A_G$. It says nothing about the angular momentum, which matters for balance when the arms or the legs swing.

**Non-example: the composite inertia.** The $6 \times 6$ inertia $I_G$ of the locked robot maps the twist of a rigid body to its momentum. It does not see the joint motions, so it gives $h_G$ only when the joints are still.

## Related definitions

- [Centroidal dynamics](/centroidal-dynamics/): the equation $\dot h_G = $ the sum of the external wrenches about $G$, written with $A_G$.
- [Spatial inertia](/spatial-inertia/): the inertia of one body; $A_G$ sums them, moved to $G$.
- [Composite rigid body algorithm](/composite-rigid-body-algorithm/): computes the subtree inertias $I^c_j$ that give the columns.
- [Joint-space inertia matrix](/joint-space-inertia-matrix/): its base rows, moved to $G$, are $A_G$ for a floating base.
- [Geometric Jacobian](/geometric-jacobian/): the bottom rows of $A_G$ are the mass times the Jacobian of the center of mass.
- [Floating-base dynamics](/floating-base-dynamics/): the setting where the base columns of $A_G$ appear.

## References
