---
tag: 7X2N83
kind: theorem
slug: linearity-in-dynamic-parameters
name: Linearity in the dynamic parameters
aliases:
- dynamic regressor form
area: robotics/robot-dynamics
level: core
summary: The joint torques are linear in the masses, first moments and inertias of the links, tau = Y(q, q', q'') pi, with 10 parameters per link and a regressor Y that depends only on the motion.
prereqs: [manipulator-equation, least-squares-problem]
see_also: [base-inertial-parameters, dynamic-parameter-identification, slotine-li-adaptive-control, spatial-inertia, euler-lagrange-manipulator-dynamics, skew-symmetry-of-manipulator-dynamics, recursive-newton-euler-algorithm, adaptive-control]
sources:
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 6, Section 6.5 (properties of robot dynamic equations)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7, Section 7.2.2 (linearity in the dynamic parameters)
  - paper: "Pradeep K. Khosla and Takeo Kanade, Parameter identification of robot dynamics, Proceedings of the 24th IEEE Conference on Decision and Control, 1985"
    locator: the linear form of the Newton-Euler equations in the inertial parameters and its use for identification (general locator)
  - paper: doi:10.1177/027836498600500306
    title: Christopher G. Atkeson, Chae H. An and John M. Hollerbach, Estimation of inertial parameters of manipulator loads and links, International Journal of Robotics Research 5(3), 101-119, 1986
    locator: the whole paper (the Newton-Euler equations written linearly in the ten inertial parameters of each link, least squares estimation, and the unidentifiable parameters)
  - paper: doi:10.1177/027836498700600303
    title: Jean-Jacques E. Slotine and Weiping Li, On the adaptive control of robot manipulators, International Journal of Robotics Research 6(3), 49-59, 1987
    locator: the adaptive law built on the regressor form
---

Linearity in the dynamic parameters says that the joint torques of a rigid robot arm are a linear function of the inertial parameters of its links: the masses, the first moments of mass and the entries of the rotational inertias. The motion enters only through a known matrix, the regressor $Y(q, \dot q, \ddot q)$, so that $\tau = Y(q, \dot q, \ddot q)\,\pi$. This turns the estimation of unknown inertias into a linear least squares problem, and it is the basis of adaptive control of robot arms. The equation is not linear in the link lengths or in the joint angles.

## Statement

Take a robot of $N$ rigid links joined by $n$ revolute or prismatic joints into a serial chain or a tree with a fixed base, with the [manipulator equation](/manipulator-equation/) $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$ and no contact. Fix a frame $\{i\}$ to each link $i$. For link $i$ let $m_i$ be its mass, $c_i$ its center of mass in $\{i\}$, $h_i = m_i c_i$ its first moment of mass, and $\mathcal{I}_i^O = \mathcal{I}_{ci} + m_i[c_i]^T[c_i]$ its rotational inertia about the origin of $\{i\}$, in $\{i\}$ coordinates. Collect the ten numbers

$$\pi_i = \big(m_i,\ h_{ix}, h_{iy}, h_{iz},\ I^O_{ixx}, I^O_{ixy}, I^O_{ixz}, I^O_{iyy}, I^O_{iyz}, I^O_{izz}\big) \in \mathbb{R}^{10}$$

and stack them as $\pi = (\pi_1, \dots, \pi_N) \in \mathbb{R}^{10N}$. Then there is a matrix $Y(q, \dot q, \ddot q) \in \mathbb{R}^{n \times 10N}$ that depends only on the joint types, the geometry of the frames and the gravity vector, and not on $\pi$, such that for all $q$, $\dot q$ and $\ddot q$

$$M(q)\ddot q + C(q, \dot q)\dot q + g(q) = Y(q, \dot q, \ddot q)\,\pi.$$

Each entry of $Y$ is a sum of terms that are linear in $\ddot q$, quadratic in $\dot q$ or free of $\dot q$ and $\ddot q$, with coefficients that are smooth functions of $q$.

## In plain words

To know which torques move an arm in a given way, you need two kinds of facts. Some describe the shape: link lengths and joint axes. Others describe the mass: how heavy each link is and how its mass is spread. The theorem says that the second kind enters in the simplest possible way. If you double every mass and inertia, the torques double. If you add two arms that have the same shape, their torques add. So you can write the torque as a fixed table of numbers that depends on the motion, times a list of unknown mass numbers. Finding that list from measured torques is then a plain fitting problem.

## Proof

The proof uses energy. Let $\mathcal{V}_i = (\omega_i, v_i)$ be the twist of frame $\{i\}$ in $\{i\}$ coordinates. It depends only on $q$, $\dot q$ and the geometry. The spatial inertia of link $i$ about the origin of $\{i\}$ is

$$\mathcal{G}_i = \begin{bmatrix} \mathcal{I}_i^O & [h_i] \\ [h_i]^T & m_i I\end{bmatrix},$$

which is the spatial inertia of Featherstone (2008, Chapter 2) written with $h_i = m_i c_i$ and $\mathcal{I}_i^O = \mathcal{I}_{ci} + m_i[c_i][c_i]^T$. Every entry of $\mathcal{G}_i$ is one of the ten numbers in $\pi_i$, up to sign. So the kinetic energy $K_i = \tfrac12\mathcal{V}_i^T\mathcal{G}_i\mathcal{V}_i$ is linear in $\pi_i$.

Let $p_i(q)$ and $R_i(q)$ be the position and orientation of $\{i\}$ in the space frame. The center of mass is at $p_i + R_ic_i$, so the potential energy is

$$P_i = -m_i\,\mathrm{g}^T(p_i + R_ic_i) = -\mathrm{g}^T\big(m_ip_i + R_ih_i\big),$$

with $\mathrm{g} = (0, 0, -9.81)$ m/s$^2$. This is linear in $(m_i, h_i)$.

So the Lagrangian $\mathcal{L} = \sum_i (K_i - P_i)$ has the form $\mathcal{L} = \phi(q, \dot q)^T\pi$, where $\phi$ does not depend on $\pi$. The Euler-Lagrange operator is linear in $\mathcal{L}$, so

$$\tau_k = \frac{d}{dt}\frac{\partial\mathcal{L}}{\partial\dot q_k} - \frac{\partial\mathcal{L}}{\partial q_k} = \Big(\frac{d}{dt}\frac{\partial\phi}{\partial\dot q_k} - \frac{\partial\phi}{\partial q_k}\Big)^T\pi.$$

The total time derivative brings in $\ddot q$ linearly. Row $k$ of $Y$ is the vector in parentheses. $\square$

The same result follows from the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/): the wrench of link $i$ is $\mathcal{G}_i\dot{\mathcal{V}}_i - [\mathrm{ad}_{\mathcal{V}_i}]^T\mathcal{G}_i\mathcal{V}_i$, which is linear in $\mathcal{G}_i$, gravity enters as an acceleration of the base, and the joint torques are sums of link wrenches mapped by matrices that depend only on $q$. This is how Khosla and Kanade (1985) and Atkeson, An and Hollerbach (1986) wrote it.

## Consequences

A worked example. Take the planar 2R arm in a vertical plane, with $q_1$ from the horizontal, link lengths $L_1$ and $L_2$, and the center of mass of link $i$ on the line of the link at distance $r_i$ from joint $i$, with inertia $I_i$ about it. With $c_1 = \cos q_1$, $c_{12} = \cos(q_1 + q_2)$, $c_2 = \cos q_2$ and $s_2 = \sin q_2$, the [Euler-Lagrange derivation](/euler-lagrange-manipulator-dynamics/) gives $\tau = Y a$ with

$$Y = \begin{bmatrix} \ddot q_1 & \ddot q_1 + \ddot q_2 & c_2(2\ddot q_1 + \ddot q_2) - s_2(2\dot q_1\dot q_2 + \dot q_2^2) & c_1 & c_{12} \\ 0 & \ddot q_1 + \ddot q_2 & c_2\ddot q_1 + s_2\dot q_1^2 & 0 & c_{12}\end{bmatrix},$$

$$a_1 = I_1 + m_1r_1^2 + m_2L_1^2,\quad a_2 = I_2 + m_2r_2^2,\quad a_3 = m_2L_1r_2,\quad a_4 = 9.81(m_1r_1 + m_2L_1),\quad a_5 = 9.81\,m_2r_2.$$

For $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, $a = (2, 1, 1, 19.62, 9.81)$. At $q = (0, \pi/2)$, $\dot q = (1, 1)$ rad/s and $\ddot q = 0$, the rows of $Y$ are $(0, 0, -3, 1, 0)$ and $(0, 0, 1, 0, 0)$, so $\tau = (-3 + 19.62, 1) = (16.62, 1)$ N m, the same as the Euler-Lagrange torque.

Base parameters. The 2R example has 20 inertial parameters (10 per link), but the torque depends on them only through the five numbers $a_1, \dots, a_5$. In general $Y$ has fewer independent columns than $10N$. The independent linear combinations of $\pi$ that the torques determine are the [base inertial parameters](/base-inertial-parameters/), and only they can be found from motion data.

Identification. If you record $\tau$ along a motion, stack the rows $Y(q(t_k), \dot q(t_k), \ddot q(t_k))$, and solve the [least squares problem](/least-squares-problem/) for the base parameters, you get a model of the arm; see [dynamic parameter identification](/dynamic-parameter-identification/). The motion must excite all base parameters. In the 2R example, static poses give only $a_4$ and $a_5$: at $q = (0, 0)$ at rest, $\tau = (a_4 + a_5, a_5)$, which for the point-mass arm is $(29.43, 9.81)$ N m and gives $a_5 = 9.81$ and $a_4 = 19.62$. The arm must move to reveal $a_1$, $a_2$ and $a_3$.

Adaptive control. The [Slotine-Li controller](/slotine-li-adaptive-control/) updates an estimate $\hat\pi$ with a law of the form $\dot{\hat\pi} = -\Gamma Y(q, \dot q, \dot q_r, \ddot q_r)^Ts$. The regressor form makes the parameter error enter the Lyapunov derivative linearly, so it can be cancelled.

Friction and motors. Viscous friction $f_{v,j}\dot q_j$ and Coulomb friction $f_{c,j}\,\mathrm{sgn}(\dot q_j)$ are linear in $f_{v,j}$ and $f_{c,j}$, and the reflected rotor inertia of a geared motor adds a term linear in the rotor inertia. All of them can be appended to $\pi$ with extra columns in $Y$.

## Tightness

The choice of parameters matters. If you use the mass $m_i$, the center of mass $c_i$ and the inertia $\mathcal{I}_{ci}$ about the center of mass as parameters, the torque is not linear in them: $\mathcal{I}_i^O$ contains the product $m_i[c_i][c_i]^T$, and the gravity torque contains $m_ic_i$. The first moment $h_i = m_ic_i$ and the inertia about a fixed point of the link remove both products.

The torque is not linear in the kinematic parameters. In the 2R example, $a_3 = m_2L_1r_2$ is a product of a link length and an inertial parameter, and $Y$ contains $\cos q_2$ and $\sin q_2$. A change in a link length changes $Y$ itself.

Linearity does not give physical consistency. Every $\pi$ in $\mathbb{R}^{10N}$ gives some torque, but only those with $m_i > 0$ and a rotational inertia about the center of mass that is positive definite and satisfies the triangle inequalities of its principal moments describe a real body. A least squares estimate can violate these conditions.

Some friction laws are not linear in their parameters. A Stribeck model with an exponential decay in the velocity has a parameter inside the exponential, and elastic links or joints add states that the regressor of the rigid model does not cover.

## History

Several groups found the linear form in the mid-1980s and used it for identification. Khosla and Kanade (1985) wrote the Newton-Euler equations linearly in the inertial parameters of the links and used the form to estimate them. Atkeson, An and Hollerbach (1986) gave the same form with ten parameters per link, estimated the inertial parameters of loads and links, and pointed out the parameters that cannot be found from joint torques. Slotine and Li (1987) used the regressor form to build an adaptive controller with a global stability proof. Textbooks now list the property beside skew symmetry: Spong et al. (Section 6.5) and Siciliano et al. (Section 7.2.2).

## References
