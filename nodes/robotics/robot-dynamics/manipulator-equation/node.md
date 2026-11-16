---
tag: P9VBJE
kind: definition
slug: manipulator-equation
name: Manipulator equation
aliases:
- robot equations of motion
area: robotics/robot-dynamics
level: core
summary: "The standard form of the equations of motion of a robot arm: M(q) q'' + C(q, q') q' + g(q) = tau + J(q)^T F_ext, with M symmetric positive definite."
prereqs: [euler-lagrange-manipulator-dynamics, joint-space-inertia-matrix]
see_also: [forward-dynamics, inverse-dynamics, skew-symmetry-of-manipulator-dynamics, linearity-in-dynamic-parameters, operational-space-formulation, floating-base-dynamics, computed-torque-control, flexible-joint-model]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.1.2 (general formulation), Section 8.5 (forward dynamics of open chains), Section 8.6 (dynamics in the task space) and Section 8.7 (constrained dynamics)"
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: "Chapter 6, Section 6.3 (equations of motion) and Section 6.5 (properties of robot dynamic equations)"
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7 (dynamics; the equation B(q) q'' + C(q, q') q' + F_v q' + F_s sgn(q') + g(q) = tau - J^T(q) h_e)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 4 (robot dynamics and control)
---

The manipulator equation is the standard form of the equations of motion of a robot arm with $n$ joints. It says that the joint torques, plus the torques that external forces cause, equal an inertia term, a velocity term and a gravity term: $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau + J(q)^T F_{\text{ext}}$. Almost every result in robot control is stated for this form. This page defines the form and its terms. [Euler-Lagrange manipulator dynamics](/euler-lagrange-manipulator-dynamics/) shows how to derive it, and the [joint-space inertia matrix](/joint-space-inertia-matrix/) page treats $M$ alone.

## Definition

A robot is a set of rigid links joined by $n$ one-degree-of-freedom joints into a serial chain or a tree with a fixed base. Its configuration is $q \in \mathbb{R}^n$. Its equation of motion is in manipulator form if

$$M(q)\,\ddot q + C(q, \dot q)\,\dot q + g(q) = \tau + J(q)^T F_{\text{ext}},$$

with these terms:

- $M(q) \in \mathbb{R}^{n \times n}$ is the [joint-space inertia matrix](/joint-space-inertia-matrix/), symmetric and positive definite, with kinetic energy $K = \tfrac12\dot q^T M(q)\dot q$.
- $C(q, \dot q)\dot q \in \mathbb{R}^n$ holds the Coriolis and centripetal torques. Each entry is a quadratic form in $\dot q$: $(C\dot q)_k = \sum_{i,j} c_{ijk}(q)\dot q_i\dot q_j$. The vector is unique; the matrix $C$ is not. The usual choice is $C_{kj} = \sum_i c_{ijk}\dot q_i$ with the Christoffel symbols $c_{ijk} = \tfrac12(\partial M_{kj}/\partial q_i + \partial M_{ki}/\partial q_j - \partial M_{ij}/\partial q_k)$.
- $g(q) = \partial P/\partial q$ is the gravity torque, the gradient of the potential energy $P(q)$. Gravity is $(0, 0, -9.81)$ m/s$^2$ in the space frame $\{s\}$.
- $\tau \in \mathbb{R}^n$ is the vector of joint torques (N m for a revolute joint) and forces (N for a prismatic joint).
- $F_{\text{ext}}$ is the wrench (moment first, then force) that the environment applies to the robot at a contact frame, and $J(q)$ is the Jacobian of that frame, in the same coordinates as $F_{\text{ext}}$. Lynch and Park use the opposite sign: they write $\tau = M\ddot q + h + J^T\mathcal{F}_{\text{tip}}$, where $\mathcal{F}_{\text{tip}} = -F_{\text{ext}}$ is the wrench that the robot applies to the environment.

Lynch and Park write $c(q, \dot q) = C(q, \dot q)\dot q$ and $h(q, \dot q) = c(q, \dot q) + g(q)$, so the equation becomes $M(q)\ddot q + h(q, \dot q) = \tau$ when there is no contact. Friction, if it is modeled, adds a term $\tau_f(\dot q)$ on the left side, for example $F_v\dot q + F_s\,\mathrm{sgn}(\dot q)$ in Siciliano et al.

Because $M(q)$ is invertible, the equation is a second-order ordinary differential equation. With the state $x = (q, \dot q)$,

$$\dot x = \begin{bmatrix}\dot q \\ M(q)^{-1}\big(\tau + J^T F_{\text{ext}} - C(q, \dot q)\dot q - g(q)\big)\end{bmatrix},$$

which is an [ODE initial value problem](/ode-initial-value-problem/) once $\tau(t)$ and the initial state are given. Solving the equation for $\ddot q$ is the [forward dynamics](/forward-dynamics/) problem; solving it for $\tau$ is the [inverse dynamics](/inverse-dynamics/) problem.

Four structural properties follow from the form, each with its own page:
1. $M(q)$ is symmetric positive definite, and bounded above and below for an arm with revolute joints only.
2. With the Christoffel choice of $C$, the matrix $\dot M - 2C$ is skew-symmetric; for every valid choice, $\dot q^T(\dot M - 2C)\dot q = 0$. See [skew symmetry of manipulator dynamics](/skew-symmetry-of-manipulator-dynamics/).
3. The left side is linear in the masses, first moments and inertias of the links: $M\ddot q + C\dot q + g = Y(q, \dot q, \ddot q)\pi$. See [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/).
4. Energy balance: $\frac{d}{dt}(K + P) = \dot q^T(\tau + J^T F_{\text{ext}})$. The arm is passive from $\tau$ to $\dot q$; see [passivity](/passivity/).

## Examples and non-examples

The planar 2R arm. Take $L_1 = L_2 = 1$ m, point masses of 1 kg at the link ends, a vertical plane, and $q_1$ measured from the horizontal. With $s_2 = \sin q_2$, $c_2 = \cos q_2$, $c_1 = \cos q_1$ and $c_{12} = \cos(q_1 + q_2)$:

$$\begin{bmatrix} 3 + 2c_2 & 1 + c_2 \\ 1 + c_2 & 1\end{bmatrix}\ddot q + \begin{bmatrix} -s_2\dot q_2 & -s_2(\dot q_1 + \dot q_2) \\ s_2\dot q_1 & 0\end{bmatrix}\dot q + 9.81\begin{bmatrix} 2c_1 + c_{12} \\ c_{12}\end{bmatrix} = \tau.$$

At rest at $q = (0, 0)$ with $\tau = 0$, $M = [[5, 2], [2, 1]]$, $M^{-1} = [[1, -2], [-2, 5]]$ and $g = (29.43, 9.81)$ N m, so $\ddot q = -M^{-1}g = (-9.81, 9.81)$ rad/s$^2$. Both masses start to fall with the acceleration $9.81$ m/s$^2$, and link 2 keeps its absolute angle ($\ddot q_1 + \ddot q_2 = 0$), which is what free fall of two point masses on massless links should give.

A load at the tip. Put the same arm at $q = (0, \pi/2)$, at rest, so that the tip is at $(1, 1)$ m and the linear Jacobian of the tip is $[[-1, -1], [1, 0]]$. A weight hangs on the tip and pulls with the force $F_{\text{ext}} = (0, -10)$ N. Then $J^T F_{\text{ext}} = (-10, 0)$ N m, and the static equation $g(q) = \tau + J^T F_{\text{ext}}$ gives $\tau = (19.62, 0) + (10, 0) = (29.62, 0)$ N m. Joint 2 needs no torque, because the tip is straight above it.

A Cartesian gantry. Three prismatic joints along $x$, $y$ and $z$ give $M = \mathrm{diag}(m_1 + m_2 + m_3, m_2 + m_3, m_3)$, $C = 0$ and $g = (0, 0, 9.81\,m_3)$ N. The equation is three decoupled masses.

Non-example: a robot with elastic joints. If a spring connects each motor to its link, the motor angles $\theta$ and the link angles $q$ are separate coordinates. The model has two coupled equations, $M(q)\ddot q + C\dot q + g = K(\theta - q)$ for the links and $B\ddot\theta + K(\theta - q) = \tau$ for the motors. The torque does not act on $q$ directly, so this is not the manipulator form in $q$; see [flexible joint model](/flexible-joint-model/).

Non-example: a robot in contact with a constraint. If the tip must stay on a surface, $J^T F_{\text{ext}}$ is not a given input but an unknown constraint force, and the model is a differential-algebraic system with multipliers. See [rigid contact complementarity](/rigid-contact-complementarity/) and the [Gauss principle of least constraint](/gauss-principle-of-least-constraint/).

Non-example: a wheeled robot with rolling constraints. A [nonholonomic constraint](/nonholonomic-constraint/) cannot be removed by a choice of independent coordinates, so the equation carries a constraint force term $A(q)^T\lambda$ with $A(q)\dot q = 0$.

## Related definitions

- [Joint-space inertia matrix](/joint-space-inertia-matrix/): the matrix $M(q)$.
- [Forward dynamics](/forward-dynamics/) and [inverse dynamics](/inverse-dynamics/): the two computational problems posed by this equation.
- [Operational space formulation](/operational-space-formulation/): the same dynamics written for the end-effector, $\Lambda(q)\dot{\mathcal{V}} + \eta(q, \mathcal{V}) = \mathcal{F}$ with $\Lambda = (JM^{-1}J^T)^{-1}$ (Lynch and Park, Section 8.6).
- [Floating-base dynamics](/floating-base-dynamics/): the same form for a robot whose base is free, with $n + 6$ coordinates and no actuation on the first six.
- [Centroidal dynamics](/centroidal-dynamics/): the six rows of a floating-base equation that give the rate of the total momentum.
- [Newton-Euler equations](/newton-euler-equations/): the equations of one rigid body, which the manipulator equation combines for all links.
- [Computed-torque control](/computed-torque-control/) and [PD control with gravity compensation](/pd-control-with-gravity-compensation/): two control laws built on this form.

## References
