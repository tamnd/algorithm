---
tag: 8QXENF
kind: algorithm
slug: recursive-newton-euler-algorithm
name: Recursive Newton-Euler algorithm
aliases:
- RNEA
- Luh-Walker-Paul algorithm
area: robotics/robot-dynamics
level: core
summary: Inverse dynamics in O(n) time by an outward pass of link velocities and accelerations and an inward pass of forces.
model: real-ram
complexity:
  vars: {n: "the number of joints, one degree of freedom each, in a serial chain or a tree"}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1980
  people: [J. Y. S. Luh, M. W. Walker, R. P. C. Paul]
  note: Luh, Walker and Paul computed the joint torques of an arm by recursive Newton-Euler equations fast enough for control in real time.
prereqs: [inverse-dynamics, spatial-inertia, kinematic-chain]
see_also: [composite-rigid-body-algorithm, articulated-body-algorithm, rigid-body-dynamics-derivatives, manipulator-equation, euler-lagrange-manipulator-dynamics, computed-torque-control, floating-base-dynamics, spatial-vector-algebra]
sources:
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 5 (inverse dynamics), Section 5.3 (the recursive Newton-Euler algorithm); Chapter 10 (accuracy and efficiency) for the operation counts"
  - paper: doi:10.1115/1.3149599
    title: J. Y. S. Luh, M. W. Walker and R. P. C. Paul, On-line computational scheme for mechanical manipulators, Journal of Dynamic Systems, Measurement, and Control 102(2), 1980
    locator: pages 69 to 76
  - paper: doi:10.1109/TSMC.1980.4308393
    title: John M. Hollerbach, A recursive Lagrangian formulation of manipulator dynamics and a comparative study of dynamics formulation complexity, IEEE Transactions on Systems, Man, and Cybernetics 10(11), 1980
    locator: pages 730 to 736
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 8, Section 8.2 (dynamics of a single rigid body) and Section 8.3 (Newton-Euler inverse dynamics)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 3, Dynamics, by Roy Featherstone and David E. Orin"
---

The recursive Newton-Euler algorithm (RNEA) solves the [inverse dynamics](/inverse-dynamics/) problem of a robot made of rigid links: given the joint positions $q$, velocities $\dot q$ and accelerations $\ddot q$, it returns the joint forces $\tau$ that produce this motion. It goes out from the base to the tips and computes the velocity and the acceleration of every link, and then it comes back from the tips to the base and adds up the forces that each joint must transmit. Both passes visit each link once, so the cost is $\Theta(n)$ for $n$ joints, for a serial chain and for a branched tree. The [inverse dynamics](/inverse-dynamics/) page states the problem, the [Euler-Lagrange form](/euler-lagrange-manipulator-dynamics/) gives the same $\tau$ by symbolic differentiation, and the [articulated-body algorithm](/articulated-body-algorithm/) solves the reverse problem, [forward dynamics](/forward-dynamics/), in the same $\Theta(n)$ time. This page writes the algorithm with [spatial vectors](/spatial-vector-algebra/), as Featherstone does.

## In plain words

Imagine a robot arm that must follow a planned motion. To know how hard each motor must push, start at the base and walk out along the arm. Each link moves like the link before it, plus the turn of its own joint, so you know how every link moves and how fast that motion changes. From that, each link tells you the push it needs to move that way. Now walk back from the tips. The last link gets its push only from its own joint. The link before it must push its own mass and also carry the push of every link that hangs on it. At each joint, the part of the push that turns the joint is the motor effort. Each link is visited twice, so a long arm costs a little more, never much more.

## The problem

The robot is a tree of $n$ rigid bodies on a fixed base, numbered so that the parent $\lambda(i)$ of body $i$ has $\lambda(i) < i$, with $\lambda(i) = 0$ for the base. A serial chain is the case $\lambda(i) = i - 1$. Joint $i$ connects body $\lambda(i)$ to body $i$ and has one degree of freedom with the screw axis $S_i \in \mathbb{R}^6$, given in the coordinates of a frame $\{i\}$ fixed to body $i$. The pose of $\{i\}$ in $\{\lambda(i)\}$ is $T_{\lambda(i),i}(q_i) = T^{\mathrm{tree}}_i e^{[S_i] q_i}$, where $T^{\mathrm{tree}}_i$ is the pose at $q_i = 0$ and $e^{[S]q}$ is the [exponential map](/se3-exponential-map/).

Spatial vectors follow Featherstone (2008) with the angular part first. A motion vector, such as a [twist](/rigid-body-twist/), is $v = (\omega, v_O)$, and a force vector, such as a [wrench](/wrench/), is $f = (n_O, f)$. $X_i = \mathrm{Ad}(T_{\lambda(i),i}^{-1})$ is the $6 \times 6$ [adjoint matrix](/adjoint-map-se3/) that maps motion vectors from $\{\lambda(i)\}$ coordinates to $\{i\}$ coordinates, and $X_i^T$ maps force vectors from $\{i\}$ to $\{\lambda(i)\}$. The spatial cross products are
$$\mathrm{crm}(v)\, m = (\omega \times m_\omega,\ v_O \times m_\omega + \omega \times m_v), \qquad \mathrm{crf}(v)\, f = (\omega \times n + v_O \times f,\ \omega \times f),$$
with $\mathrm{crf}(v) = -\mathrm{crm}(v)^T$. Body $i$ has the [spatial inertia](/spatial-inertia/) $I_i$ about the origin of $\{i\}$. Gravity is the spatial acceleration $a_g = (0, g)$ with $g = (0, 0, -9.81)$ m/s$^2$ in base coordinates, and $f^{\mathrm{ext}}_i$ is an optional wrench of the outside world on body $i$, in $\{i\}$ coordinates.

Input: the model, $q, \dot q, \ddot q \in \mathbb{R}^n$, $a_g$ and $f^{\mathrm{ext}}$. Output: $\tau \in \mathbb{R}^n$ with
$$\tau = M(q)\ddot q + C(q, \dot q)\dot q + g(q) - \textstyle\sum_i J_i(q)^T f^{\mathrm{ext}}_i ,$$
the [manipulator equation](/manipulator-equation/), where $J_i$ is the Jacobian of the twist of body $i$ in $\{i\}$ coordinates.

## The algorithm

```pseudo id=main
RNEA(model, q, q̇, q̈, a_g, f_ext)
L1  a_0 ← -a_g ; v_0 ← 0                         ▷ gravity as a base acceleration
L2  for i ← 1 to n do                            ▷ outward pass
L3      X_i ← Ad(T_{λ(i),i}(q_i)^-1)
L4      v_i ← X_i v_λ(i) + S_i q̇_i
L5      a_i ← X_i a_λ(i) + S_i q̈_i + crm(v_i) S_i q̇_i
L6      f_i ← I_i a_i + crf(v_i) I_i v_i - f_ext,i  ▷ Newton-Euler for body i
L7  for i ← n downto 1 do                        ▷ inward pass
L8      τ_i ← S_i^T f_i
L9      if λ(i) ≠ 0 then f_λ(i) ← f_λ(i) + X_i^T f_i
L10 return τ
```

Line L4 adds the joint twist to the twist of the parent. Line L5 is its time derivative; the last term, $\mathrm{crm}(v_i) S_i \dot q_i$, is the velocity product term, which holds the Coriolis and centripetal accelerations. Line L6 is the [Newton-Euler equation](/newton-euler-equations/) of body $i$: the wrench needed to give it the acceleration $a_i$. Line L1 is a standard trick: if the base accelerates upward at $-g$, every body feels the same apparent force as gravity, so no gravity term is needed in line L6. After line L1, the variables $a_i$ are the true accelerations minus the gravity field, not the true accelerations.

In the inward pass, $f_i$ starts as the wrench of body $i$ alone. Line L9 adds it to the parent, so when the loop reaches body $i$, $f_i$ is the wrench that joint $i$ must transmit to the whole subtree that hangs on it. Line L8 takes the component of this wrench along the joint axis: the joint torque for a revolute joint, the force for a prismatic joint. The other five components are carried by the bearings.

## Example

Take a planar arm with two revolute joints about $z$, two links of 1 m, and a point mass of 1 kg at the end of each link, with no gravity. Frame $\{1\}$ is at joint 1 and frame $\{2\}$ is at joint 2, 1 m along link 1, so $T^{\mathrm{tree}}_2$ is a translation by $(1, 0, 0)$ and both screw axes are $S = (0, 0, 1, 0, 0, 0)$. Each point mass is at $(1, 0, 0)$ in its own frame. Take $q = (0, \pi/2)$, $\dot q = (1, 1)$ rad/s and $\ddot q = 0$.

- Lines L4 and L5 for body 1: $v_1 = (0, 0, 1,\ 0, 0, 0)$ and $a_1 = 0$, because $S_1$ is parallel to $v_1$.
- Line L6 for body 1: $I_1 v_1 = (0, 0, 1,\ 0, 1, 0)$, and $f_1 = \mathrm{crf}(v_1) I_1 v_1 = (0, 0, 0,\ -1, 0, 0)$. This is the centripetal force of 1 N that pulls the mass toward joint 1.
- Line L4 for body 2: $v_2 = (0, 0, 2,\ 1, 0, 0)$. The angular velocity is the sum of the two joint rates, and $(1, 0, 0)$ is the velocity of the origin of $\{2\}$ in $\{2\}$ coordinates.
- Line L5 for body 2: $a_2 = \mathrm{crm}(v_2) S_2 \dot q_2 = (0, 0, 0,\ 0, -1, 0)$.
- Line L6 for body 2: $f_2 = (0, 0, 1,\ -4, 1, 0)$.
- Lines L8 and L9 for body 2: $\tau_2 = S_2^T f_2 = 1$ N m, and $X_2^T f_2 = (0, 0, -3,\ -1, -4, 0)$ is added to $f_1$.
- Line L8 for body 1: $f_1 = (0, 0, -3,\ -2, -4, 0)$, and $\tau_1 = -3$ N m.

So $\tau = (-3, 1)$ N m. The closed form of the Euler-Lagrange equations for this arm, $\tau_1 = (3 + 2c_2)\ddot q_1 + (1 + c_2)\ddot q_2 - s_2(2\dot q_1 \dot q_2 + \dot q_2^2)$ and $\tau_2 = (1 + c_2)\ddot q_1 + \ddot q_2 + s_2 \dot q_1^2$ without gravity, gives the same values at $c_2 = 0$ and $s_2 = 1$. With gravity $g = 9.81$ m/s$^2$ along $-y$ in the plane of the arm, $q = (0.3, 0.7)$, $\dot q = (0.5, -1.2)$ and $\ddot q = (2, -1)$, the implementation and the closed form both give $\tau = (31.183981854, 7.991104417)$ N m.

## Correctness

The outward pass computes the true twist of every body. The twist of body $i$ is the twist of its parent, moved into the frame of $i$, plus the twist $S_i \dot q_i$ of the joint (line L4). The acceleration (line L5) is the time derivative of line L4, where the derivative of $X_i$ gives the velocity product term. Line L6 is the Newton-Euler equation of one body. The inward pass is Newton's third law: the joint of body $i$ must supply the wrench of body $i$ and the wrenches that body $i$ passes to its children. Because every child has a larger index than its parent, the loop of line L7 finishes all children before their parent. The full proof, with the gravity trick and the lemma on the derivative of $X_i$, is in the correctness proof of this page.

## Complexity

In the [real RAM](/real-ram/), each step of each loop does a fixed number of products of $6 \times 6$ matrices and 6-vectors, so the time is $\Theta(n)$ for any tree with $n$ joints. The extra space is $\Theta(n)$ for the transforms and the vectors $v_i$, $a_i$ and $f_i$. Featherstone (2008, Chapter 10) gives exact counts of multiplications and additions for several versions of the algorithm; a careful version does not form the $6 \times 6$ matrices and uses the special structure of $X_i$ and $I_i$.

Hollerbach (1980) compared the operation counts of the formulations of manipulator dynamics. The Lagrangian equations in the form of Uicker and Kahn need $O(n^4)$ operations, a recursive Lagrangian form that Hollerbach gives needs $O(n)$, and the recursive Newton-Euler form needs fewer operations than both. Luh, Walker and Paul (1980) report about 4.5 ms for the Stanford arm on a PDP 11/45 computer; this is a measurement on that machine.

## Properties

- **Linear in the accelerations.** For fixed $q$ and $\dot q$, $\tau$ is an affine function of $\ddot q$. So $\mathrm{RNEA}(q, 0, e_j) $ with no gravity is column $j$ of $M(q)$, and $\mathrm{RNEA}(q, \dot q, 0)$ is the bias $C(q, \dot q)\dot q + g(q)$.
- **Linear in the inertial parameters.** $\tau$ is linear in the ten parameters of each spatial inertia. This gives the regressor form of [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/).
- **Exact.** The algorithm uses no approximation. The only errors are floating-point rounding.
- **Coordinates.** All the work of body $i$ happens in its own frame $\{i\}$, where $S_i$ and $I_i$ are constant. Other versions use base coordinates for every body; they give the same $\tau$.
- **No mass matrix.** The algorithm never forms $M(q)$, which is why it costs $\Theta(n)$ and not $\Theta(n^2)$.

## Variants and improvements

- **Base coordinates.** All vectors can be kept in base coordinates. Then the inertias change with $q$ and must be moved at each step, but the joint axes come straight from the [product of exponentials](/product-of-exponentials-formula/). Both versions give the same $\tau$ and the same order of cost.
- **Floating base.** For a humanoid or a legged robot the base is a free body. The inverse dynamics then needs the base acceleration and contact forces as well; see [floating-base dynamics](/floating-base-dynamics/).
- **Bias forces only.** The call $\mathrm{RNEA}(q, \dot q, 0)$ gives $C\dot q + g$ in $\Theta(n)$, which the [composite rigid body algorithm](/composite-rigid-body-algorithm/) uses for forward dynamics.
- **Multi-degree-of-freedom joints.** A spherical joint has a $6 \times 3$ matrix $S_i$, and lines L4, L5 and L8 use the matrix in place of the vector.
- **Derivatives.** [Analytical derivatives of rigid body dynamics](/rigid-body-dynamics-derivatives/) differentiate each line of the algorithm and give $\partial\tau/\partial q$ and $\partial\tau/\partial\dot q$ for optimization and control.
- **Closed loops.** A mechanism with kinematic loops is cut into a spanning tree plus loop constraints, and the loop forces are found from the constraints. Featherstone (2008) treats closed loop systems in a chapter of their own.

## When to use it

Use the RNEA wherever the joint forces of a known motion are needed: in [computed torque control](/computed-torque-control/) and other model-based controllers, in the feedforward of a planned trajectory, to identify the inertial parameters from measured torques, and to check a simulation. It is also the fastest way to get the bias forces $C\dot q + g$. If you need $M(q)$ itself, use the [composite rigid body algorithm](/composite-rigid-body-algorithm/); if you need $\ddot q$ from $\tau$, use the [articulated-body algorithm](/articulated-body-algorithm/). For a 2 or 3 joint arm, a closed form from the Euler-Lagrange equations is also fine.

## Pitfalls

- **The order of the bodies.** The loops need $\lambda(i) < i$. With another numbering the forward pass reads a parent that is not yet computed.
- **Angular part first or last.** Featherstone and Lynch and Park put the angular part first, but some texts and libraries put the linear part first. Mixing the two gives wrong forces without an error.
- **The sign of gravity.** Line L1 sets $a_0 = -a_g$, not $+a_g$. With $g = (0, 0, -9.81)$ m/s$^2$, $a_0 = (0, 0, 0,\ 0, 0, 9.81)$: the base accelerates upward.
- **The variables $a_i$.** Because of the trick of line L1, the variables $a_i$ are not the true accelerations of the bodies. Do not use them as the output of a forward kinematics of accelerations.
- **The spatial acceleration is not the classical one.** $a_i$ is the derivative of the twist. The classical acceleration of the origin of $\{i\}$ is the linear part of $a_i$ plus $\omega_i \times v_{O,i}$. See [spatial vector algebra](/spatial-vector-algebra/).
- **External wrenches.** $f^{\mathrm{ext}}_i$ must be in the coordinates of $\{i\}$ and taken about the origin of $\{i\}$. A force measured at a sensor needs a change of coordinates first.

## Implementations

## History

Luh, Walker and Paul (1980) gave the recursive Newton-Euler scheme in link coordinates and showed that it could run on-line for control, at a time when the Lagrangian equations were too slow. Hollerbach (1980) made the Lagrangian equations recursive and compared the costs of the formulations. Featherstone (1983, 1987) wrote the dynamics with spatial vectors, and his 2008 book gives the spatial form of the RNEA that this page uses. The name RNEA and the name Luh-Walker-Paul algorithm both refer to this recursion.

## References
