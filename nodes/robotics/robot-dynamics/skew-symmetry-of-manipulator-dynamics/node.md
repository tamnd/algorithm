---
tag: 42QX2A
kind: theorem
slug: skew-symmetry-of-manipulator-dynamics
name: Skew symmetry of manipulator dynamics
aliases:
- passivity property of robot dynamics
area: robotics/robot-dynamics
level: core
summary: "With C built from the Christoffel symbols of M, the matrix M' - 2C is skew-symmetric. For any other valid C, only the weaker identity q'^T (M' - 2C) q' = 0 holds."
prereqs: [manipulator-equation, passivity]
see_also: [pd-control-with-gravity-compensation, slotine-li-adaptive-control, passivity-based-control, euler-lagrange-manipulator-dynamics, joint-space-inertia-matrix, linearity-in-dynamic-parameters, lyapunov-function, computed-torque-control]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.1.2 (the Christoffel symbols, the Coriolis matrix and Proposition 8.1, the skew symmetry of the mass matrix derivative minus twice the Coriolis matrix); the property is used in Section 11.4.2"
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 6, Section 6.5.1 (skew symmetry and passivity)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7, Section 7.2.1 (skew-symmetry of the matrix B' - 2C)
  - paper: doi:10.1115/1.3139651
    title: Morikazu Takegaki and Suguru Arimoto, A new feedback method for dynamic control of manipulators, Journal of Dynamic Systems, Measurement, and Control 103(2), 1981
    locator: the energy argument for PD control with gravity compensation
  - paper: doi:10.1177/027836498700600303
    title: Jean-Jacques E. Slotine and Weiping Li, On the adaptive control of robot manipulators, International Journal of Robotics Research 6(3), 49-59, 1987
    locator: the stability proof of the adaptive controller, which uses the skew symmetry of the full matrix
---

The skew symmetry property says that, for a robot arm in manipulator form, the matrix $\dot M(q) - 2C(q, \dot q)$ is skew-symmetric when the Coriolis matrix $C$ is built from the Christoffel symbols of the inertia matrix $M$. It is the matrix form of energy conservation: the Coriolis and centripetal forces do no work. Lyapunov proofs for robot control use it to cancel the velocity terms. The trap is that $C$ is not unique, and only the Christoffel choice gives the matrix property; every valid choice gives the weaker scalar identity.

## Statement

Let a robot obey the [manipulator equation](/manipulator-equation/) $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$ with $q \in \mathbb{R}^n$, where the [joint-space inertia matrix](/joint-space-inertia-matrix/) $M(q)$ is symmetric and continuously differentiable in $q$, and does not depend on time except through $q$. Let $\dot M = \sum_i (\partial M/\partial q_i)\dot q_i$.

(a) If $C_{kj} = \sum_i c_{ijk}(q)\dot q_i$ with the Christoffel symbols of the first kind

$$c_{ijk} = \frac12\left(\frac{\partial M_{kj}}{\partial q_i} + \frac{\partial M_{ki}}{\partial q_j} - \frac{\partial M_{ij}}{\partial q_k}\right),$$

then $N(q, \dot q) = \dot M(q, \dot q) - 2C(q, \dot q)$ is skew-symmetric for all $q$ and $\dot q$: $x^T N x = 0$ for every $x \in \mathbb{R}^n$.

(b) If $C'$ is any matrix function with $C'(q, \dot q)\dot q = C(q, \dot q)\dot q$ for all $q$ and $\dot q$, then $\dot q^T\big(\dot M - 2C'\big)\dot q = 0$ for all $q$ and $\dot q$. The matrix $\dot M - 2C'$ need not be skew-symmetric.

This is Proposition 8.1 of Lynch and Park and the property of Section 6.5.1 of Spong et al. Positive definiteness of $M$ is not needed, and gravity plays no part.

## In plain words

The velocity terms of a robot arm come from the way its inertia changes as it moves. These terms push the joints around, but they never add or remove energy. The theorem writes this fact as a property of one matrix. If you build the velocity matrix in the standard way, that matrix acts like a pure rotation in joint-velocity space: whatever vector you feed it, the output is at right angles to the input. If you build the velocity matrix in another valid way, this only stays true for the actual joint velocity.

## Proof

(a) Write $\dot M_{kj} = \sum_i \frac{\partial M_{kj}}{\partial q_i}\dot q_i$ and expand $2C_{kj}$:

$$N_{kj} = \dot M_{kj} - 2C_{kj} = \sum_i\left(\frac{\partial M_{kj}}{\partial q_i} - \frac{\partial M_{kj}}{\partial q_i} - \frac{\partial M_{ki}}{\partial q_j} + \frac{\partial M_{ij}}{\partial q_k}\right)\dot q_i = \sum_i\left(\frac{\partial M_{ij}}{\partial q_k} - \frac{\partial M_{ki}}{\partial q_j}\right)\dot q_i.$$

Swap $k$ and $j$:

$$N_{jk} = \sum_i\left(\frac{\partial M_{ik}}{\partial q_j} - \frac{\partial M_{ji}}{\partial q_k}\right)\dot q_i.$$

Because $M$ is symmetric, $M_{ik} = M_{ki}$ and $M_{ji} = M_{ij}$, so $N_{jk} = -N_{kj}$. So $N^T = -N$, and $x^T N x = 0$ for every $x$.

(b) $\dot q^T(\dot M - 2C')\dot q = \dot q^T\dot M\dot q - 2\dot q^T(C'\dot q) = \dot q^T\dot M\dot q - 2\dot q^T(C\dot q) = \dot q^T N\dot q = 0$ by (a). $\square$

A second proof of (b) uses energy. Let $K = \tfrac12\dot q^T M\dot q$. Then $\dot K = \dot q^T M\ddot q + \tfrac12\dot q^T\dot M\dot q = \dot q^T(\tau - g - C'\dot q) + \tfrac12\dot q^T\dot M\dot q$. The work-energy principle gives $\dot K = \dot q^T(\tau - g)$ for any motion, so $\tfrac12\dot q^T(\dot M - 2C')\dot q = 0$.

## Consequences

Energy balance and passivity. With $P(q)$ the potential energy and $H = K + P$, the equation gives $\dot H = \dot q^T\tau$. The arm is a [passive](/passivity/) system from the input $\tau$ to the output $\dot q$, with the total energy $H$ as the storage function, provided $P$ is bounded below. This is why the alias "passivity property" is used for the theorem.

PD control with gravity compensation. For $\tau = -K_p(q - q_d) - K_d\dot q + g(q)$ with a constant goal $q_d$, the function $V = \tfrac12\dot q^T M\dot q + \tfrac12(q - q_d)^T K_p(q - q_d)$ has $\dot V = -\dot q^T K_d\dot q \le 0$. Only part (b) is used, because the vector that multiplies $C$ is $\dot q$ itself. This is the argument of Takegaki and Arimoto (1981); see [PD control with gravity compensation](/pd-control-with-gravity-compensation/).

Adaptive and passivity-based control. The [Slotine-Li adaptive controller](/slotine-li-adaptive-control/) uses the sliding variable $s = \dot q - \dot q_r$ and the function $V = \tfrac12 s^T M s + \dots$. Its derivative contains $\tfrac12 s^T(\dot M - 2C)s$, with $C$ evaluated at the true $\dot q$ and multiplied by $s \ne \dot q$. Here part (a), the full matrix property, is needed, so the controller must use the Christoffel $C$. The same holds for [passivity-based control](/passivity-based-control/) of manipulators.

A worked example. For the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, $M = [[3 + 2c_2, 1 + c_2], [1 + c_2, 1]]$ and the Christoffel matrix is $C = [[-s_2\dot q_2, -s_2(\dot q_1 + \dot q_2)], [s_2\dot q_1, 0]]$. At $q_2 = \pi/2$ and $\dot q = (1, 2)$ rad/s:

$$\dot M = \begin{bmatrix} -2s_2\dot q_2 & -s_2\dot q_2 \\ -s_2\dot q_2 & 0\end{bmatrix} = \begin{bmatrix} -4 & -2 \\ -2 & 0\end{bmatrix},\quad C = \begin{bmatrix} -2 & -3 \\ 1 & 0\end{bmatrix},\quad \dot M - 2C = \begin{bmatrix} 0 & 4 \\ -4 & 0\end{bmatrix},$$

which is skew-symmetric.

## Tightness

The matrix property needs the Christoffel choice. For the same 2R arm, $C' = [[-2s_2\dot q_2, -s_2\dot q_2], [s_2\dot q_1, 0]]$ gives the same vector $C'\dot q = (-s_2(2\dot q_1\dot q_2 + \dot q_2^2),\ s_2\dot q_1^2) = C\dot q$, so it is a valid Coriolis matrix. At $q_2 = \pi/2$ and $\dot q = (1, 2)$ it is $[[-4, -2], [1, 0]]$, and

$$\dot M - 2C' = \begin{bmatrix} 4 & 2 \\ -4 & 0\end{bmatrix}.$$

This is not skew-symmetric: for $x = (1, 0)$, $x^T(\dot M - 2C')x = 4$. But $\dot q^T(\dot M - 2C')\dot q = 4 + 2 \cdot 2 - 4 \cdot 2 = 0$, as part (b) says. With this $C'$, the Slotine-Li proof fails.

The Christoffel choice is not the only one that gives a skew matrix when $n \ge 3$. If $D(q, \dot q)$ is skew-symmetric and $D\dot q = 0$, for example $D = [\dot q]$ when $n = 3$, then $C + D$ gives the same vector and $\dot M - 2(C + D)$ is still skew-symmetric. For $n = 2$, a skew-symmetric $D$ with $D\dot q = 0$ and $\dot q \ne 0$ must be zero, so the skew choice is unique where $\dot q \ne 0$.

Explicit time dependence. If $M$ depends on time directly, for example through a payload that changes during the motion, then $\dot M$ has a term $\partial M/\partial t$, the Lagrangian equations gain a matching term, and neither (a) nor (b) holds in the form above.

## History

Takegaki and Arimoto (1981) used the energy balance of the arm to show that PD control with gravity compensation is globally stable, which uses the scalar identity (b). Slotine and Li (1987) built an adaptive controller whose proof needs the full skew symmetry (a). Textbooks now state the property as a basic fact of robot dynamics: Spong et al. (Section 6.5.1), Siciliano et al. (Section 7.2.1) and Lynch and Park (Proposition 8.1). The underlying fact is older: for any mechanical system with kinetic energy $\tfrac12\dot q^T M\dot q$, the gyroscopic part of the Euler-Lagrange equations does no work.

## References
