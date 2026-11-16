---
tag: FNGKHS
kind: definition
slug: joint-space-inertia-matrix
name: Joint-space inertia matrix
aliases:
- mass matrix of a robot
- generalized inertia matrix
area: robotics/robot-dynamics
level: core
summary: The symmetric positive definite matrix M(q) with kinetic energy (1/2) q'^T M(q) q'. It is the sum over the links of J^T G J, and it multiplies q'' in the manipulator equation.
prereqs: [forward-kinematics, positive-definite-matrix]
see_also: [manipulator-equation, euler-lagrange-manipulator-dynamics, composite-rigid-body-algorithm, spatial-inertia, articulated-body-inertia, operational-space-formulation, cholesky-decomposition, centroidal-momentum-matrix]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.1.2 (general formulation), Section 8.1.3 (understanding the mass matrix), Section 8.4 (dynamic equations in closed form) and Section 8.9 (actuation, gearing and friction)"
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: "Chapter 6, Section 6.2 (kinetic and potential energy, the inertia tensor), Section 6.3 (equations of motion) and Section 6.5.2 (bounds on the inertia matrix)"
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: Chapter 6 (the joint-space inertia matrix, the composite-rigid-body algorithm and branch-induced sparsity)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7 (the inertia matrix B(q) in the Lagrange formulation)
---

The joint-space inertia matrix $M(q)$ of a robot is the matrix that turns joint velocities into kinetic energy, $K = \tfrac12 \dot q^T M(q) \dot q$. It is the matrix that multiplies the joint accelerations in the [manipulator equation](/manipulator-equation/), and it is symmetric and positive definite for any real arm. This page defines $M$ and its main properties. The [manipulator equation](/manipulator-equation/) page gives the full equation of motion, and [Euler-Lagrange manipulator dynamics](/euler-lagrange-manipulator-dynamics/) shows how $M$ produces the Coriolis and gravity terms.

## Definition

Take a robot of $N$ rigid links, joined by $n$ joints into a serial chain or a tree, with joint variables $q \in \mathbb{R}^n$. Link $i$ has mass $m_i$, center of mass $p_{ci}(q)$, and rotational inertia $\mathcal{I}_i$ about its center of mass in a frame $\{i\}$ fixed to the link at the center of mass. Let $J_{vi}(q)$ be the $3 \times n$ Jacobian with $\dot p_{ci} = J_{vi}(q)\dot q$, and let $J_{\omega i}(q)$ be the $3 \times n$ Jacobian of the angular velocity of link $i$ in $\{i\}$ coordinates. The joint-space inertia matrix is

$$M(q) = \sum_{i=1}^{N} \Big( m_i\, J_{vi}(q)^T J_{vi}(q) + J_{\omega i}(q)^T\, \mathcal{I}_i\, J_{\omega i}(q) \Big).$$

It is the unique symmetric matrix with $K(q, \dot q) = \tfrac12 \dot q^T M(q)\dot q$ for all $\dot q$, where $K$ is the total kinetic energy of the links. In the notation of Lynch and Park, with the body Jacobian $J_{ib}$ of the center-of-mass frame of link $i$ and the $6 \times 6$ spatial inertia $\mathcal{G}_i = \mathrm{diag}(\mathcal{I}_i, m_i I)$, the same matrix is $M(q) = \sum_i J_{ib}(q)^T \mathcal{G}_i J_{ib}(q)$ (Section 8.1.2). Siciliano et al. call it $B(q)$; Spong et al. call it $D(q)$.

Properties.

1. Symmetry. Each term is symmetric.
2. Positive definiteness. $\dot q^T M \dot q = 2K \ge 0$, and $K = 0$ only if every link is at rest. So $M(q)$ is positive definite exactly when every nonzero $\dot q$ moves some mass or turns some link with nonzero inertia. A real link has $\mathcal{I}_i$ positive definite, so for a real arm $M(q)$ is positive definite at every $q$.
3. Column meaning. Column $j$ of $M(q)$ is the vector of joint torques needed to give joint $j$ a unit acceleration from rest, with all other accelerations zero, no gravity and no external force. This is the basis of the [composite-rigid-body algorithm](/composite-rigid-body-algorithm/), which forms $M$ in $O(n^2)$ for a serial chain.
4. The diagonal. For a revolute joint $j$ in a serial chain, $M_{jj}$ is the moment of inertia of all links from $j$ outward, taken as one rigid body, about the axis of joint $j$.
5. Dependence on $q$. $M$ does not depend on $q_1$: moving joint 1 moves the whole arm rigidly along a fixed axis, which does not change the kinetic energy of any motion. In the same way, in a serial chain $M_{jk}$ depends only on the joints $q_l$ with $l > \min(j, k)$.
6. Bounds. For an arm with only revolute joints, there are constants $0 < \lambda_m \le \lambda_M$ with $\lambda_m I \preceq M(q) \preceq \lambda_M I$ for all $q$, because $M$ is continuous and positive definite on a compact set of angles (Spong et al., Section 6.5.2). With prismatic joints, $\lambda_M$ can grow with $q$.
7. Sparsity in trees. In a tree, $M_{jk} = 0$ when neither of the joints $j$ and $k$ lies on the path from the base to the other. Featherstone (2008, Chapter 6) calls this branch-induced sparsity and uses it to factor $M$ faster.

## Examples and non-examples

Planar 2R arm with point masses. Take $L_1 = L_2 = 1$ m, a point mass of 1 kg at each link end, and relative joint angles. Link 1 has $p_{c1} = (\cos q_1, \sin q_1)$, and link 2 has $p_{c2} = (\cos q_1 + \cos(q_1 + q_2), \sin q_1 + \sin(q_1 + q_2))$. The sum $m_1 J_{v1}^T J_{v1} + m_2 J_{v2}^T J_{v2}$ gives

$$M(q) = \begin{bmatrix} 3 + 2\cos q_2 & 1 + \cos q_2 \\ 1 + \cos q_2 & 1 \end{bmatrix} \ \text{kg m}^2.$$

At $q_2 = 0$, $M = [[5, 2], [2, 1]]$, with eigenvalues $3 \pm 2\sqrt2$, that is 0.17157 and 5.82843. At $q_2 = \pi/2$, $M = [[3, 1], [1, 1]]$, with eigenvalues $2 \pm \sqrt2$, that is 0.58579 and 3.41421. At $q_2 = \pi$ the arm is folded back, the outer mass sits on joint 1, and $M = I$. In every case the determinant is $(3 + 2\cos q_2) - (1 + \cos q_2)^2 = 2 - \cos^2 q_2 \ge 1$, so $M$ is positive definite. At $q = (0, \pi/2)$ and $\dot q = (1, 1)$ rad/s, $K = \tfrac12 (3 + 1 + 1 + 1) = 3$ J. A direct check: mass 1 moves at speed 1 m/s and has 0.5 J, and mass 2 has velocity $(-2, 1)$ m/s and 2.5 J. Property 4 gives the same first entry: $M_{11} = 1 \cdot 1^2 + 1 \cdot \|p_{c2}\|^2 = 1 + (2 + 2\cos q_2)$.

The same arm with general links. Let link $i$ have its center of mass at distance $r_i$ from joint $i$ and inertia $I_i$ about it. Then $M_{11} = a_1 + a_2 + 2a_3\cos q_2$, $M_{12} = a_2 + a_3\cos q_2$ and $M_{22} = a_2$, with $a_1 = I_1 + m_1 r_1^2 + m_2 L_1^2$, $a_2 = I_2 + m_2 r_2^2$ and $a_3 = m_2 L_1 r_2$. The point-mass arm is $a = (2, 1, 1)$.

A Cartesian gantry. Three prismatic joints move along $x$, then $y$, then $z$, and each stage carries the next. Joint 1 moves all three stages, joint 2 moves stages 2 and 3, and joint 3 moves stage 3. So $M = \mathrm{diag}(m_1 + m_2 + m_3,\ m_2 + m_3,\ m_3)$, which is constant. The Coriolis term of such a robot is zero.

A single pendulum. One revolute joint and one link with mass $m$, center of mass at distance $r$ and inertia $I$ about it give the $1 \times 1$ matrix $M = I + m r^2$.

Non-example: mass on the joint axis. If the second link of the 2R arm is a point mass placed exactly at joint 2 ($r_2 = 0$ and $I_2 = 0$), then turning joint 2 moves no mass, the second row and column of $M$ are zero, and $M$ is only positive semidefinite. The matrix formula still applies, but the model has lost the dynamics of joint 2. Real links have $I_i > 0$, and a geared motor adds its reflected rotor inertia to the diagonal, which keeps $M$ positive definite.

Non-example: the task-space inertia. The matrix $\Lambda(q) = (J M^{-1} J^T)^{-1}$ of the [operational space formulation](/operational-space-formulation/) gives the kinetic energy in terms of the end-effector twist. It is a different matrix: it depends on the choice of end-effector frame, and it does not exist where $J$ loses rank.

## Related definitions

- [Manipulator equation](/manipulator-equation/): $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau + J^T F_{\text{ext}}$. Its Coriolis matrix $C$ comes from the derivatives of $M$ through the Christoffel symbols.
- [Spatial inertia](/spatial-inertia/): the $6 \times 6$ inertia of one body. $M$ is the sum of the spatial inertias pulled back to joint space by the Jacobians.
- [Articulated-body inertia](/articulated-body-inertia/): the inertia that a body shows when the bodies beyond it are free to move. The [articulated-body algorithm](/articulated-body-algorithm/) uses it to avoid forming $M$.
- [Composite-rigid-body algorithm](/composite-rigid-body-algorithm/): the standard way to compute $M$, in $O(n^2)$ for a serial chain.
- [Cholesky decomposition](/cholesky-decomposition/): $M = L L^T$ exists because $M$ is symmetric positive definite, and it is the usual way to solve $M \ddot q = b$ in [forward dynamics](/forward-dynamics/).
- [Centroidal momentum matrix](/centroidal-momentum-matrix/): the map from $\dot q$ to the momentum of the whole robot about its center of mass, for a floating base.
- [Dynamically consistent generalized inverse](/dynamically-consistent-generalized-inverse/): a pseudoinverse of $J$ weighted by $M^{-1}$.
- In differential geometry, $M(q)$ is a Riemannian metric on the configuration space, and the velocity terms of the equation of motion are the Christoffel symbols of that metric.

## References
