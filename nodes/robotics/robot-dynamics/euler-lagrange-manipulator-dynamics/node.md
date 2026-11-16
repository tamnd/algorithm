---
tag: AFJK9B
kind: technique
slug: euler-lagrange-manipulator-dynamics
name: Euler-Lagrange dynamics of a manipulator
aliases:
- Lagrangian dynamics of manipulators
area: robotics/robot-dynamics
level: intro
summary: Derives the manipulator equation from energy. Write the kinetic energy (1/2) q'^T M(q) q' and the potential P(q), then the Euler-Lagrange equations give M, the Coriolis matrix C and gravity g.
prereqs: [euler-lagrange-equation, joint-space-inertia-matrix]
see_also: [manipulator-equation, newton-euler-equations, kanes-method, recursive-newton-euler-algorithm, skew-symmetry-of-manipulator-dynamics, linearity-in-dynamic-parameters, pfaffian-constraint, gauss-principle-of-least-constraint]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.1 (Lagrangian formulation): 8.1.1 basic concepts and motivating examples, 8.1.2 general formulation (the Christoffel symbols and the Coriolis matrix), 8.1.4 Lagrangian versus Newton-Euler dynamics; Section 8.7 (constrained dynamics)"
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: "Chapter 6, Section 6.1 (the Euler-Lagrange equations), Section 6.2 (kinetic and potential energy), Section 6.3 (equations of motion) and Section 6.4 (some common configurations)"
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7 (the Lagrange formulation of manipulator dynamics)
  - paper: doi:10.1109/TSMC.1980.4308393
    title: John M. Hollerbach, A recursive Lagrangian formulation of manipulator dynamics and a comparative study of dynamics formulation complexity, IEEE Transactions on Systems, Man, and Cybernetics 10(11), 730-736, 1980
    locator: the whole paper (the recursive Lagrangian form and the comparison of operation counts)
---

Euler-Lagrange manipulator dynamics is the method that derives the equation of motion of a robot arm from its energy. You write the kinetic energy of the links as $\tfrac12 \dot q^T M(q)\dot q$ and their potential energy $P(q)$, and you apply the [Euler-Lagrange equation](/euler-lagrange-equation/) to each joint. The result is the [manipulator equation](/manipulator-equation/) $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$, with $C$ built from the derivatives of $M$ and $g$ the gradient of $P$. The method needs no internal forces between the links, which is how it differs from the [Newton-Euler equations](/newton-euler-equations/) used link by link.

## In plain words

A robot arm stores energy in two ways. Moving links have kinetic energy, and links that are lifted have potential energy. If you can write both as functions of the joint angles and their rates, one fixed recipe turns them into the torque that each motor must give. The recipe takes derivatives only. You never need the forces that one link puts on the next, because those forces do no net work. The price is algebra: for an arm with many joints, the expressions become long, so the method is best for small arms, for symbolic models and for proofs about the structure of the equations.

## When it applies

- The robot is a set of rigid bodies joined by joints, in a serial chain or a tree, so that the joint variables $q \in \mathbb{R}^n$ are independent generalized coordinates. Closed chains and contacts need extra constraints (see Variations).
- The reference frame $\{s\}$ is inertial. Gravity is $g = (0, 0, -9.81)$ m/s$^2$ in $\{s\}$, with $z$ up.
- The applied forces are gravity, which has a potential, and other forces that enter as generalized forces: the joint torques $\tau$, external wrenches through $J(q)^T F_{\text{ext}}$, and friction.
- It is the method of choice when you want the equation in closed form, for a control proof such as [skew symmetry](/skew-symmetry-of-manipulator-dynamics/) or [linearity in the parameters](/linearity-in-dynamic-parameters/), or for an arm with two or three joints. For numerical work on long chains, the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) is faster.

## The template

1. Choose the joint variables $q = (q_1, \dots, q_n)$ and the forward kinematics of each link: the center of mass $p_{ci}(q)$ in $\{s\}$ and the orientation $R_i(q)$ of a frame $\{i\}$ at the center of mass.
2. Compute the Jacobians $J_{vi}(q)$ with $\dot p_{ci} = J_{vi}\dot q$ and $J_{\omega i}(q)$ with $\omega_i = J_{\omega i}\dot q$, the angular velocity in $\{i\}$ coordinates.
3. Form the [joint-space inertia matrix](/joint-space-inertia-matrix/) $M(q) = \sum_i \big(m_i J_{vi}^T J_{vi} + J_{\omega i}^T \mathcal{I}_i J_{\omega i}\big)$, so that $K = \tfrac12 \dot q^T M(q)\dot q$.
4. Form the potential energy $P(q) = \sum_i m_i\, 9.81\, z_{ci}(q)$, where $z_{ci}$ is the height of the center of mass.
5. Write the Lagrangian $\mathcal{L} = K - P$ and the equations $\frac{d}{dt}\frac{\partial \mathcal{L}}{\partial \dot q_k} - \frac{\partial \mathcal{L}}{\partial q_k} = \tau_k$ for $k = 1, \dots, n$.
6. Expand them into $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$ with

$$c_{ijk}(q) = \frac12\left(\frac{\partial M_{kj}}{\partial q_i} + \frac{\partial M_{ki}}{\partial q_j} - \frac{\partial M_{ij}}{\partial q_k}\right),\qquad C_{kj}(q, \dot q) = \sum_{i=1}^n c_{ijk}(q)\,\dot q_i,\qquad g_k(q) = \frac{\partial P}{\partial q_k}.$$

The numbers $c_{ijk}$ are the Christoffel symbols of the first kind. Lynch and Park write them as $\Gamma_{kij}$ with the row index first (Section 8.1.2); the values are the same.

Why step 6 is right. From $K = \tfrac12 \sum_{i,j} M_{ij}\dot q_i\dot q_j$ we get $\partial \mathcal{L}/\partial \dot q_k = \sum_j M_{kj}\dot q_j$, so

$$\frac{d}{dt}\frac{\partial \mathcal{L}}{\partial \dot q_k} = \sum_j M_{kj}\ddot q_j + \sum_{i,j}\frac{\partial M_{kj}}{\partial q_i}\dot q_i\dot q_j,\qquad \frac{\partial \mathcal{L}}{\partial q_k} = \frac12\sum_{i,j}\frac{\partial M_{ij}}{\partial q_k}\dot q_i\dot q_j - \frac{\partial P}{\partial q_k}.$$

The sum $\sum_{i,j}\frac{\partial M_{kj}}{\partial q_i}\dot q_i\dot q_j$ does not change if $i$ and $j$ swap, so it equals $\frac12\sum_{i,j}\big(\frac{\partial M_{kj}}{\partial q_i} + \frac{\partial M_{ki}}{\partial q_j}\big)\dot q_i\dot q_j$. Subtracting gives $\sum_j M_{kj}\ddot q_j + \sum_{i,j} c_{ijk}\dot q_i\dot q_j + \partial P/\partial q_k = \tau_k$, which is the claimed form.

Terms with $i = j$ in $\sum_{i,j} c_{ijk}\dot q_i\dot q_j$ are centripetal terms, and terms with $i \ne j$ are Coriolis terms.

## Classic examples

A single link. One revolute joint, a link of mass $m$ with its center of mass at distance $r$ and inertia $I$ about it, in a vertical plane, with $q$ measured from the horizontal. Then $K = \tfrac12 (I + m r^2)\dot q^2$ and $P = m\, 9.81\, r\sin q$, so $\tau = (I + m r^2)\ddot q + 9.81\, m r\cos q$. There is no velocity term, because $M$ is constant.

The planar 2R arm with point masses. Take $L_1 = L_2 = 1$ m, point masses of 1 kg at the link ends, in a vertical plane with heights measured upward and $q_1$ from the horizontal. Write $s_2 = \sin q_2$, $c_2 = \cos q_2$, $c_1 = \cos q_1$ and $c_{12} = \cos(q_1 + q_2)$.

Steps 1 to 3. The masses are at $p_1 = (c_1, \sin q_1)$ and $p_2 = p_1 + (c_{12}, \sin(q_1 + q_2))$. Their speeds are $\|\dot p_1\|^2 = \dot q_1^2$ and $\|\dot p_2\|^2 = \dot q_1^2 + (\dot q_1 + \dot q_2)^2 + 2c_2\,\dot q_1(\dot q_1 + \dot q_2)$. Collecting the terms of $K = \tfrac12\|\dot p_1\|^2 + \tfrac12\|\dot p_2\|^2$:

$$M(q) = \begin{bmatrix} 3 + 2c_2 & 1 + c_2 \\ 1 + c_2 & 1\end{bmatrix}.$$

Step 4. $P = 9.81\,(2\sin q_1 + \sin(q_1 + q_2))$.

Step 6. Only $M_{11}$ and $M_{12}$ depend on $q_2$, with $\partial M_{11}/\partial q_2 = -2s_2$ and $\partial M_{12}/\partial q_2 = -s_2$. The nonzero symbols are $c_{121} = c_{211} = c_{221} = -s_2$ and $c_{112} = s_2$. So

$$C(q, \dot q) = \begin{bmatrix} -s_2\dot q_2 & -s_2(\dot q_1 + \dot q_2) \\ s_2\dot q_1 & 0\end{bmatrix},\qquad g(q) = 9.81\begin{bmatrix} 2c_1 + c_{12} \\ c_{12}\end{bmatrix}.$$

The torques are

$$\tau_1 = (3 + 2c_2)\ddot q_1 + (1 + c_2)\ddot q_2 - s_2(2\dot q_1\dot q_2 + \dot q_2^2) + 9.81(2c_1 + c_{12}),$$
$$\tau_2 = (1 + c_2)\ddot q_1 + \ddot q_2 + s_2\dot q_1^2 + 9.81\,c_{12}.$$

Numbers. At $q = (0, \pi/2)$, $\dot q = (1, 1)$ rad/s and $\ddot q = 0$, without gravity, $C\dot q = (-1 - 2, 1) = (-3, 1)$, so $\tau = (-3, 1)$ N m. The arm needs these torques just to keep its joint rates constant. With gravity, $g(q) = (19.62, 0)$ and $\tau = (16.62, 1)$ N m. At rest in the stretched horizontal pose $q = (0, 0)$, $\tau = g(q) = (29.43, 9.81)$ N m: the holding torques are $9.81$ N times the horizontal lever arms, $1 + 2 = 3$ m for joint 1 and $1$ m for joint 2.

The 2R arm with general links. With center-of-mass distances $r_1$, $r_2$ and inertias $I_1$, $I_2$, the same steps give $M$ with the entries $a_1 + a_2 + 2a_3c_2$, $a_2 + a_3c_2$ and $a_2$, where $a_1 = I_1 + m_1r_1^2 + m_2L_1^2$, $a_2 = I_2 + m_2r_2^2$ and $a_3 = m_2L_1r_2$, and $C$ is the matrix above with $s_2$ replaced by $a_3s_2$. Gravity is $g(q) = (a_4c_1 + a_5c_{12},\ a_5c_{12})$ with $a_4 = 9.81(m_1r_1 + m_2L_1)$ and $a_5 = 9.81\,m_2r_2$. The torque is linear in $(a_1, \dots, a_5)$; this is the [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/).

A Cartesian gantry. Three prismatic joints along $x$, $y$ and $z$, each stage carrying the next. $M = \mathrm{diag}(m_1 + m_2 + m_3, m_2 + m_3, m_3)$ is constant, so $C = 0$, and only the vertical joint feels gravity: $g(q) = (0, 0, 9.81\,m_3)$. Each joint is a mass driven by a force.

## Variations

- Closed form with Jacobians. Lynch and Park (Section 8.4) stack the link twists and write $M(q) = \mathcal{A}^T\mathcal{L}^T\mathcal{G}\mathcal{L}\mathcal{A}$ and a matching expression for $c(q, \dot q) = C\dot q$, with block matrices built from the screw axes and the link inertias. This gives the same equation without symbolic differentiation.
- Recursive Lagrangian. Hollerbach (1980) organized the Lagrangian computation recursively along the chain and showed that it can be made to grow linearly in $n$, like the Newton-Euler recursion.
- Constraints. If the robot closes a loop or touches the world, the constraints $A(q)\dot q = 0$ add a force $A(q)^T\lambda$ with multipliers $\lambda$: $M\ddot q + C\dot q + g = \tau + A^T\lambda$ (Lynch and Park, Section 8.7). See [Pfaffian constraint](/pfaffian-constraint/) and the [Gauss principle of least constraint](/gauss-principle-of-least-constraint/).
- Nonconservative forces. Friction torques and external wrenches enter on the right side as generalized forces, $\tau - \tau_f(\dot q) + J(q)^T F_{\text{ext}}$. They do not go into the Lagrangian.
- Motor inertia. A motor with rotor inertia $I_r$ and gear ratio $G_r$ adds about $G_r^2 I_r$ to the diagonal entry of its joint (Lynch and Park, Section 8.9).
- Floating base. A legged robot or a humanoid adds six coordinates for the pose of its base; see [floating-base dynamics](/floating-base-dynamics/).

## Pitfalls

- Velocity of the wrong point. $K$ needs the velocity of the center of mass of each link, not of the origin of the link frame. If you use another point, you must add the cross term of the spatial inertia.
- Frames of $\omega$ and $\mathcal{I}$. The rotational energy $\tfrac12\omega^T\mathcal{I}\omega$ needs both in the same frame. In body coordinates $\mathcal{I}$ is constant; in $\{s\}$ it is $R\,\mathcal{I}R^T$ and changes with $q$.
- Angles. In a planar arm with relative angles, link $i$ turns at $\dot q_1 + \dots + \dot q_i$, not at $\dot q_i$.
- Many matrices $C$. Any $C'$ with $C'\dot q = C\dot q$ gives the same equation of motion. Only the Christoffel choice of step 6 makes $\dot M - 2C$ skew-symmetric, which many control proofs need.
- Signs of gravity. $g(q) = +\partial P/\partial q$ appears on the left side. A sign error here makes gravity compensation push the arm down.
- Cost. Expanding the symbols by hand or with computer algebra grows quickly with $n$. Hollerbach (1980) compared the operation counts of the formulations; the direct Lagrangian evaluation (the Uicker and Kahn form) grows as about $n^4$, and the recursive forms grow as $n$. Use the closed form for analysis and a recursive algorithm for simulation and control.

## Exercises

1. A link of mass 2 kg has its center of mass at $r = 0.5$ m from the joint and $I = 0.1$ kg m$^2$ about it. Find the torque at $q = 0$, $\dot q = 0$ and $\ddot q = 1$ rad/s$^2$. Answer: $(0.1 + 0.5) \cdot 1 + 9.81 \cdot 2 \cdot 0.5 = 10.41$ N m.
2. For the point-mass 2R arm, find $\tau$ at $q = (0.3, 0.7)$ rad, $\dot q = (0.5, -1.2)$ rad/s and $\ddot q = (2, -1)$ rad/s$^2$ with gravity. Answer: $\tau = (31.184, 7.991)$ N m.
3. Show that $C' = \begin{bmatrix} -2s_2\dot q_2 & -s_2\dot q_2 \\ s_2\dot q_1 & 0\end{bmatrix}$ gives $C'\dot q = C\dot q$ for the 2R arm, and that $\dot M - 2C'$ is not skew-symmetric at $q_2 = \pi/2$, $\dot q = (1, 2)$.
4. Show that the gantry has $c_{ijk} = 0$ for all indices, and explain why a constant $M$ always gives $C = 0$.
5. Show that $\dot q^T(\tau - g(q)) = \frac{d}{dt}K$ for any arm. This is the energy balance that the [skew symmetry](/skew-symmetry-of-manipulator-dynamics/) property expresses.

## References
