---
tag: F8CA3J
kind: definition
slug: grasp-matrix
name: Grasp matrix
aliases:
- grasp map
area: robotics/grasping-and-manipulation
level: core
summary: "The matrix G that maps the contact force components of a grasp to the net wrench on the object; its transpose maps the object twist to the contact velocities."
prereqs: [grasp-contact-models, adjoint-map-se3, rigid-body-twist]
see_also: [force-closure, grasp-wrench-space, grasp-quality-measures, jacobian-statics-duality, adjoint-map-se3, cooperative-manipulation, in-hand-manipulation, null-space-projection]
sources:
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.1.1 (Velocity Kinematics, the grasp matrix and the hand Jacobian) and Section 38.1.2 (Dynamics and Equilibrium); Section 38.2.1 (Grasp Classifications, Table 38.5); the chapter is pages 955 to 988"
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (grasp statics, the grasp map and internal forces); the book writes wrenches force first
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 12, Section 12.2.3 (Force Closure), where the contact wrenches form the columns of a matrix F; Chapter 3 for the adjoint map of wrenches"
  - paper: "J. Kenneth Salisbury and Bernard Roth, Kinematic and force analysis of articulated mechanical hands, Journal of Mechanisms, Transmissions, and Automation in Design 105(1), 35-41, 1983"
    locator: the force and velocity analysis of a grasp through its contacts
---

The grasp matrix of a grasp is the linear map from the forces that the fingers apply at the contacts to the net force and moment (the wrench) that they apply to the object. Its transpose goes the other way in velocity: it maps the motion of the object to the velocities of the object at the contact points. It depends only on where the contacts are, on the directions of their normals, and on the [contact model](/grasp-contact-models/), not on the hand that makes the contacts. Force closure, internal forces and many grasp quality scores are properties of this matrix.

## Definition

A rigid object with body frame $\{b\}$ is touched at $c$ contacts. Contact $i$ has the contact frame $\{C_i\}$ with origin $p_i$ (in $\{b\}$), rotation $R_i$ (in $\{b\}$), and $z$ axis along the inward normal. Its contact model gives $m_i$ force components $\lambda_i$ and a wrench basis $B_i$ ($6 \times m_i$), so the contact applies the wrench $B_i \lambda_i$ in $\{C_i\}$. Wrenches are written moment first, $\mathcal{F} = (m, f)$.

A wrench changes frame by the transpose of the adjoint map, $\mathcal{F}_b = \mathrm{Ad}_{T_{C_i b}}^T \mathcal{F}_{C_i}$, with

$$\mathrm{Ad}_{T_{C_i b}}^T = \begin{pmatrix} R_i & [p_i] R_i \\ 0 & R_i \end{pmatrix},$$

where $[p_i]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $p_i$. The contact block of the grasp matrix is $G_i = \mathrm{Ad}_{T_{C_i b}}^T B_i$, and the **grasp matrix** is

$$G = \begin{pmatrix} G_1 & G_2 & \cdots & G_c \end{pmatrix} \in \mathbb{R}^{6 \times m}, \qquad m = \sum_i m_i.$$

The net wrench that the contacts apply to the object is $\mathcal{F}_c = G \lambda$, where $\lambda$ stacks the $\lambda_i$. For a hard finger, $B_i = (0; I_3)$ and

$$G_i = \begin{pmatrix} [p_i] R_i \\ R_i \end{pmatrix},$$

so the column of each force component is the wrench $(p_i \times r, r)$ of the unit force $r$ along that axis of the contact frame. In the plane, a wrench is $(m_z, f_x, f_y)$ and $G$ has 3 rows.

**The velocity side.** If the object moves with the twist $\mathcal{V} = (\omega, v)$ in $\{b\}$, then $G_i^T \mathcal{V}$ is the velocity of the object point at $p_i$, in the axes of $\{C_i\}$, restricted to the components that the contact transmits. For a hard finger, $G_i^T \mathcal{V} = R_i^T (v + \omega \times p_i)$. The two sides agree on power: $\lambda^T (G^T \mathcal{V}) = (G\lambda)^T \mathcal{V}$. This is the same duality as between a robot Jacobian and joint torques ([Jacobian statics duality](/jacobian-statics-duality/)).

**Equilibrium and internal forces.** With an external wrench $\mathcal{F}_{ext}$ on the object, quasi-static balance is $G\lambda + \mathcal{F}_{ext} = 0$. If $\lambda_p$ is one solution, all solutions are $\lambda_p + \lambda_N$ with $\lambda_N$ in the null space of $G$. The vectors of $\mathcal{N}(G)$ are the **internal forces**: they squeeze the object and leave the net wrench zero. Friction needs them, because a finger can only push sideways as hard as it pushes in.

Properties that follow from the definition:

- $G$ depends on the reference point. Moving the reference point of $\{b\}$ multiplies $G$ on the left by an invertible adjoint transpose, so the rank and the null space do not change.
- If $\operatorname{rank} G < 6$ (or $< 3$ in the plane), some external wrench cannot be balanced by any contact forces, so the grasp is not in [force closure](/force-closure/).
- $\mathcal{N}(G^T)$ is the set of object twists that no contact constraint sees. If it is not $\{0\}$, the object can move while every transmitted contact velocity stays zero.
- The Handbook classifies grasps by the null spaces of $G$, of $G^T$ and of the hand Jacobian, the map from the joint velocities of the hand to the contact velocities. In its Table 38.5, a grasp with $\mathcal{N}(G^T) \ne \{0\}$ is indeterminate, and a grasp with $\mathcal{N}(G) \ne \{0\}$ is graspable (it has internal forces).

## Examples and non-examples

**Two fingers on a box (planar).** A box has its center at the origin and its sides at $x = \pm 1$. Finger 1 touches at $p_1 = (-1, 0)$ with $n_1 = (1, 0)$; finger 2 touches at $p_2 = (1, 0)$ with $n_2 = (-1, 0)$. Both are hard fingers. Take the tangent $t_i$ as $n_i$ turned by +90 degrees, so $t_1 = (0, 1)$ and $t_2 = (0, -1)$, and order the components as $\lambda = (f_{t1}, f_{n1}, f_{t2}, f_{n2})$. The planar moment of a force $f$ at $p$ is $p_x f_y - p_y f_x$. The columns are the wrenches $(m_z, f_x, f_y)$ of $t_1$ and $n_1$ at $p_1$ and of $t_2$ and $n_2$ at $p_2$:

$$G = \begin{pmatrix} -1 & 0 & -1 & 0 \\ 0 & 1 & 0 & -1 \\ 1 & 0 & -1 & 0 \end{pmatrix}.$$

The rank is 3. The null space is spanned by $(0, 1, 0, 1)$: equal normal forces, a pure squeeze. The transpose gives the contact velocities: for $\mathcal{V} = (\omega, v_x, v_y)$, the first row of $G^T \mathcal{V}$ is $v_y - \omega$, which is the velocity of the box at $p_1$ along $t_1$, since the point $(-1, 0)$ moves with $(v_x, v_y - \omega)$.

**Holding the box against gravity.** Let the box have a mass of 1 kg and let gravity act along $-y$, so $\mathcal{F}_{ext} = (0, 0, -9.81)$ N. The balance $G\lambda = (0, 0, 9.81)$ gives $f_{t1} - f_{t2} = 9.81$ and $f_{t1} + f_{t2} = 0$, so $f_{t1} = 4.905$ and $f_{t2} = -4.905$ N, and $f_{n1} = f_{n2} = s$. Each finger carries 4.905 N of friction. With $\mu = 0.5$ the [friction cone](/friction-cone/) needs $4.905 \le 0.5\, s$, so the squeeze must be at least $s = 9.81$ N. The internal force is what makes the grasp work.

**Two hard fingers in space.** Put the same box in space, with contacts at $(\pm 1, 0, 0)$. Every column of $G$ is a wrench $(p_i \times r, r)$ with $p_i$ on the $x$ axis, and $p_i \times r$ has no $x$ component. So the row of $m_x$ is zero and $\operatorname{rank} G = 5$. No contact forces resist a twist of the box about the line through the fingers.

**The dependence on units.** If the half-width of the box is $L$ meters instead of 1, the moment row of the planar example is multiplied by $L$, and $G G^T = \operatorname{diag}(2L^2, 2, 2)$. The singular values of $G$ are $\sqrt{2} L$, $\sqrt{2}$ and $\sqrt{2}$. A measure such as the smallest singular value then changes with the length unit: it is $\sqrt{2}$ for $L = 1$ and $0.1414$ for $L = 0.1$. See [grasp quality measures](/grasp-quality-measures/).

**Non-example: the hand Jacobian.** The hand Jacobian maps joint velocities of the fingers to contact velocities. It describes the hand, while $G$ describes only the contacts on the object. A grasp can have a good $G$ and a hand that cannot apply the needed forces.

**Non-example: the matrix of normals only.** The frictionless matrix $G_n$, whose columns are the wrenches $(p_i \times n_i, n_i)$ of the normals, is the grasp matrix of the frictionless model. It is a different matrix from the hard finger $G$ of the same contacts, and form closure is a property of $G_n$.

## Related definitions

- [Grasp contact models](/grasp-contact-models/): they give the blocks $B_i$ and the cones of allowed $\lambda_i$.
- [Force closure](/force-closure/): every wrench is $G\lambda$ for some $\lambda$ inside the friction cones.
- [Grasp wrench space](/grasp-wrench-space/): the image under $G$ of a set of bounded contact forces.
- [Adjoint map of SE(3)](/adjoint-map-se3/): the change of frame that builds each block.
- [Jacobian statics duality](/jacobian-statics-duality/): the same force and velocity duality for a robot arm.
- [Cooperative manipulation](/cooperative-manipulation/): several arms on one object, where the grasp matrix splits the load and the internal forces.
- [Null space projection](/null-space-projection/): the tool that adds internal forces without changing the net wrench.

## References
