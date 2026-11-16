---
tag: 0XMNG2
kind: theorem
slug: newton-euler-equations
name: Newton-Euler equations of a rigid body
aliases:
- Euler's equations of rigid body motion
area: robotics/robot-dynamics
level: intro
summary: For a rigid body, the net force is mass times the acceleration of the center of mass, and the moment about it is I dw/dt + w x I w in body coordinates.
prereqs: [angular-velocity, wrench]
see_also: [rigid-body-twist, spatial-inertia, spatial-vector-algebra, recursive-newton-euler-algorithm, inverse-dynamics, euler-lagrange-manipulator-dynamics, kanes-method, centroidal-dynamics]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.2 (dynamics of a single rigid body): 8.2.1 classical formulation, 8.2.2 twist-wrench formulation, 8.2.3 dynamics in other frames"
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: Chapter 2 (spatial vector algebra, the spatial equation of motion of a rigid body)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 6, Section 6.6 (Newton-Euler formulation)
  - book: "Isaac Newton, Philosophiae Naturalis Principia Mathematica, London, 1687"
    locator: the axioms or laws of motion at the start of Book I
  - paper: "Leonhard Euler, Nova methodus motum corporum rigidorum determinandi, Novi Commentarii Academiae Scientiarum Petropolitanae 20, 208-238, 1776 (Eneström number E479)"
    locator: the whole paper (the balance of linear momentum and the balance of angular momentum stated as two general laws)
---

The Newton-Euler equations are the laws of motion of one rigid body. The translational part says that the net force on the body equals its mass times the acceleration of its center of mass. The rotational part says that the net moment about the center of mass equals the rate of change of the angular momentum, which in body coordinates is $\mathcal{I}_b \dot\omega_b + \omega_b \times \mathcal{I}_b \omega_b$. Every dynamics algorithm for robot arms, from the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) to [Kane's method](/kanes-method/), applies these two equations to each link.

## Statement

Let a rigid body have mass $m > 0$ and center of mass $c$. Attach a body frame $\{b\}$ at $c$, and let $\mathcal{I}_b \in \mathbb{R}^{3 \times 3}$ be the rotational inertia matrix about $c$ in $\{b\}$ coordinates. $\mathcal{I}_b$ is symmetric positive definite and constant in time. Let $R(t) = R_{sb}(t)$ be the orientation of $\{b\}$ in an inertial frame $\{s\}$, let $\omega_b$ be the [angular velocity](/angular-velocity/) in body coordinates, so that $\dot R = R[\omega_b]$, and let $v_b = R^T \dot p_c$ be the velocity of the center of mass in body coordinates. Let $f_b$ be the net external force and $m_b$ the net external moment about $c$, both in $\{b\}$ coordinates. Then

$$f_b = m\,(\dot v_b + \omega_b \times v_b),$$

$$m_b = \mathcal{I}_b \dot\omega_b + \omega_b \times \mathcal{I}_b \omega_b.$$

The term $\dot v_b + \omega_b \times v_b$ is the acceleration $\ddot p_c$ of the center of mass, written in body coordinates. In space coordinates the first equation is $f_s = m \ddot p_c$.

With the [wrench](/wrench/) $\mathcal{F}_b = (m_b, f_b)$, the twist $\mathcal{V}_b = (\omega_b, v_b)$ and the spatial inertia $\mathcal{G}_b = \mathrm{diag}(\mathcal{I}_b, m I)$ about the center of mass, the two equations are one equation in six dimensions (Lynch and Park, Section 8.2.2):

$$\mathcal{F}_b = \mathcal{G}_b \dot{\mathcal{V}}_b - [\mathrm{ad}_{\mathcal{V}_b}]^T \mathcal{G}_b \mathcal{V}_b, \qquad [\mathrm{ad}_{\mathcal{V}}] = \begin{bmatrix} [\omega] & 0 \\ [v] & [\omega] \end{bmatrix}.$$

## In plain words

Push a body and its center of mass speeds up in the direction of the push. The heavier the body, the less it speeds up. Turning works in a similar way, but with a twist. A body that spins about a tilted axis needs a moment just to keep spinning at a constant rate, because its spin and its angular momentum do not point the same way. The second term of the rotational equation is that extra moment. If the body spins about one of its principal axes, the extra moment is zero.

## Proof

The translational part is Newton's second law, and it is assumed for single particles. The rotational part follows from it with three more assumptions:

1. The frame $\{s\}$ is inertial.
2. The body is a finite set of particles with masses $m_i$ and positions $r_i$, and the distances between them do not change.
3. The force $f_{ij}$ of particle $j$ on particle $i$ satisfies $f_{ji} = -f_{ij}$, and it acts along the line $r_i - r_j$ (the strong form of Newton's third law).

Each particle obeys $m_i \ddot r_i = F_i + \sum_{j \ne i} f_{ij}$, where $F_i$ is the external force on it.

Linear momentum. Sum over $i$. The internal forces cancel in pairs, so $\sum_i m_i \ddot r_i = \sum_i F_i = f$. With $m = \sum_i m_i$ and $p_c = \sum_i m_i r_i / m$, this is $f = m \ddot p_c$. Writing $\ddot p_c$ in body coordinates, $R^T \ddot p_c = R^T \frac{d}{dt}(R v_b) = \dot v_b + \omega_b \times v_b$, which gives the first equation.

Angular momentum about the center of mass. Let $\rho_i = r_i - p_c$, so that $\sum_i m_i \rho_i = 0$. Define $H = \sum_i m_i \rho_i \times \dot\rho_i$. Then

$$\dot H = \sum_i m_i \rho_i \times \ddot\rho_i = \sum_i \rho_i \times m_i \ddot r_i - \Big(\sum_i m_i \rho_i\Big) \times \ddot p_c = \sum_i \rho_i \times F_i + \sum_i \sum_{j \ne i} \rho_i \times f_{ij}.$$

The term $\dot\rho_i \times \dot\rho_i$ is zero, and the second sum in the middle is zero because $\sum_i m_i \rho_i = 0$. In the double sum, the pair $(i, j)$ gives $\rho_i \times f_{ij} + \rho_j \times f_{ji} = (r_i - r_j) \times f_{ij}$, which is zero because $f_{ij}$ is parallel to $r_i - r_j$. So $\dot H = n$, the net external moment about the center of mass.

Rigidity. Because the distances do not change, $\rho_i = R \beta_i$ with constant body vectors $\beta_i$, and $\dot\rho_i = \omega_s \times \rho_i$ with $\omega_s = R\omega_b$. Then

$$H = \sum_i m_i \rho_i \times (\omega_s \times \rho_i) = R \Big(\sum_i m_i [\beta_i]^T [\beta_i]\Big) R^T \omega_s = R\,\mathcal{I}_b\,\omega_b,$$

with $\mathcal{I}_b = \sum_i m_i [\beta_i]^T [\beta_i] = \sum_i m_i (\|\beta_i\|^2 I - \beta_i \beta_i^T)$, which is constant. Differentiate with $\dot R = R[\omega_b]$:

$$\dot H = R\big([\omega_b] \mathcal{I}_b \omega_b + \mathcal{I}_b \dot\omega_b\big).$$

So the moment in body coordinates, $m_b = R^T n$, equals $\mathcal{I}_b \dot\omega_b + \omega_b \times \mathcal{I}_b \omega_b$. For a continuous body, replace the sums by integrals over the mass density. $\square$

The proof needs assumption 3. For a continuum, the balance of angular momentum is usually taken as a separate axiom instead, which is how Euler stated it in 1776. The six-dimensional form follows by stacking the two equations: the moment row of $[\mathrm{ad}_{\mathcal{V}_b}]^T \mathcal{G}_b \mathcal{V}_b$ is $-\omega_b \times \mathcal{I}_b \omega_b - v_b \times m v_b = -\omega_b \times \mathcal{I}_b\omega_b$, and the force row is $-m\,\omega_b \times v_b$.

## Consequences

Torque-free rotation conserves energy and the size of the angular momentum. With $m_b = 0$, $\frac{d}{dt}\big(\tfrac12 \omega_b^T \mathcal{I}_b \omega_b\big) = \omega_b^T \mathcal{I}_b \dot\omega_b = -\omega_b^T(\omega_b \times \mathcal{I}_b\omega_b) = 0$. In the same way $\frac{d}{dt}\|\mathcal{I}_b \omega_b\|^2 = 0$.

Euler's equations in principal axes. If $\{b\}$ is aligned with the principal axes, $\mathcal{I}_b = \mathrm{diag}(I_1, I_2, I_3)$ and

$$m_1 = I_1\dot\omega_1 + (I_3 - I_2)\,\omega_2\omega_3,\quad m_2 = I_2\dot\omega_2 + (I_1 - I_3)\,\omega_3\omega_1,\quad m_3 = I_3\dot\omega_3 + (I_2 - I_1)\,\omega_1\omega_2.$$

A worked example. Take $\mathcal{I}_b = \mathrm{diag}(1, 2, 3)$ kg m$^2$ and $\omega_b = (1, 1, 0)$ rad/s. Then $\mathcal{I}_b\omega_b = (1, 2, 0)$ and $\omega_b \times \mathcal{I}_b\omega_b = (0, 0, 1)$. To hold this spin constant ($\dot\omega_b = 0$), the body needs the moment $m_b = (0, 0, 1)$ N m about its center of mass. With no moment, the body starts to turn away instead: $\dot\omega_b = -\mathcal{I}_b^{-1}(0, 0, 1) = (0, 0, -1/3)$ rad/s$^2$. If the spin is about a principal axis, for example $\omega_b = (2, 0, 0)$ rad/s, then $\mathcal{I}_b\omega_b$ is parallel to $\omega_b$ and no moment is needed.

Robot links. In a serial chain, each link $i$ receives a wrench from link $i - 1$ and gives one to link $i + 1$. Applying the six-dimensional equation to each link, outward for the velocities and accelerations and inward for the wrenches, gives the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/), which solves [inverse dynamics](/inverse-dynamics/) in $O(n)$ for $n$ joints. Featherstone (2008, Chapter 2) writes the same law with spatial vectors as $f = I a + v \times^* I v$, with the inertia about any frame origin; see [spatial vector algebra](/spatial-vector-algebra/) and [spatial inertia](/spatial-inertia/).

## Tightness

Each hypothesis is needed.

- Non-inertial frame. In a frame that accelerates or rotates relative to an inertial frame, the equations hold only after fictitious forces are added.
- Moments about another point. About a point $o$ that is not the center of mass, the moment equation gets the extra term $(p_c - o) \times m \ddot p_c$. The simple form holds about the center of mass, or about a pivot that is fixed both in the body and in space, with the inertia taken about that pivot.
- Space coordinates. The form $n_s = \mathcal{I}_s\dot\omega_s + \omega_s \times \mathcal{I}_s\omega_s$ is also true, but $\mathcal{I}_s = R\,\mathcal{I}_b R^T$ changes with time. Body coordinates are used because $\mathcal{I}_b$ is constant.
- Non-rigid or variable-mass bodies. If the particles move relative to each other, $H$ is not $\mathcal{I}\omega$ with a constant $\mathcal{I}$. A body that loses mass, such as a rocket, needs terms for the momentum that the mass carries away.
- Non-central internal forces. If the internal forces are equal and opposite but not along the line between the particles, the double sum in the proof need not vanish, and the particle argument no longer gives the moment equation.

## History

Newton stated the laws of motion for bodies treated as points in the Principia of 1687. Euler worked on the rotation of rigid bodies over several decades. In his paper Nova methodus motum corporum rigidorum determinandi (presented in 1775, published in 1776) he stated the balance of linear momentum and the balance of angular momentum as two general laws, and took the second as independent of the first. The six-dimensional form with twists and wrenches is newer. Featherstone (2008) gives it in spatial vector notation, and Lynch and Park (2017) give it with the Lie bracket $[\mathrm{ad}_{\mathcal{V}}]$. Luh, Walker and Paul (1980) used the equations link by link in the recursive Newton-Euler algorithm.

## References
