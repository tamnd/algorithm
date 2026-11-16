---
tag: 0W0KC6
kind: algorithm
slug: articulated-body-algorithm
name: Articulated-body algorithm
aliases:
- Featherstone's algorithm
- ABA
area: robotics/robot-dynamics
level: advanced
summary: Forward dynamics of a kinematic tree in O(n) time by three passes that compute articulated-body inertias and then accelerations.
model: real-ram
complexity:
  vars: {n: "the number of joints, one degree of freedom each, in a serial chain or a tree"}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1983
  people: [Roy Featherstone]
  note: Featherstone introduced articulated-body inertias and computed the forward dynamics of a robot in time linear in the number of links.
prereqs: [forward-dynamics, articulated-body-inertia, recursive-newton-euler-algorithm]
see_also: [composite-rigid-body-algorithm, spatial-vector-algebra, spatial-inertia, manipulator-equation, rigid-body-dynamics-derivatives, floating-base-dynamics, gauss-principle-of-least-constraint, schur-complement]
sources:
  - paper: doi:10.1177/027836498300200102
    title: Roy Featherstone, The calculation of robot dynamics using articulated-body inertias, The International Journal of Robotics Research 2(1), 1983
    locator: pages 13 to 30
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 7 (forward dynamics by propagation methods): the articulated-body inertia, its calculation and the articulated-body algorithm; Chapter 10 (accuracy and efficiency) for the operation counts"
  - book: doi:10.1007/978-0-387-74315-8
    title: Roy Featherstone, Robot Dynamics Algorithms, Kluwer Academic Publishers, 1987
    locator: the chapter on the articulated-body method and its comparison with the composite-rigid-body method
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 3, Dynamics, by Roy Featherstone and David E. Orin"
---

The articulated-body algorithm (ABA) solves the [forward dynamics](/forward-dynamics/) problem of a robot made of rigid bodies in a serial chain or a tree: given the joint positions $q$, velocities $\dot q$ and forces $\tau$, it returns the joint accelerations $\ddot q$. It never forms the [joint-space inertia matrix](/joint-space-inertia-matrix/). Instead, it computes for each body its [articulated-body inertia](/articulated-body-inertia/), the inertia that the body seems to have when the joints beyond it are free to move, and with these it finds the accelerations one joint at a time. It makes three passes over the bodies, so the cost is $\Theta(n)$ for $n$ joints. The [composite rigid body algorithm](/composite-rigid-body-algorithm/) solves the same problem by forming $M(q)$ and solving a linear system, which costs $\Theta(n^3)$ for a serial chain. The ABA inverts the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/), which solves the reverse problem in $\Theta(n)$.

## In plain words

When you push the first link of a robot arm whose joints are all free, the arm does not resist like one solid piece, because the outer links swing away instead of following. The algorithm finds how heavy each link feels with everything beyond it hanging free. It starts at the tips: the last link feels like itself. The link before it feels like itself plus the part of the last link that a free joint cannot let swing away. Going inward, each link gets the felt weight of its outer part. On the way back out, the first joint now knows exactly how hard its load resists, so its acceleration follows from its motor effort. With that acceleration known, the next joint is like a first joint, and so on to the tips.

## The problem

The robot is a tree of $n$ rigid bodies with the notation of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/): body $i$ has the parent $\lambda(i) < i$ ($\lambda(i) = 0$ for the base), joint $i$ has the screw axis $S_i$ in the frame $\{i\}$ of body $i$, $X_i = \mathrm{Ad}(T_{\lambda(i),i}(q_i)^{-1})$ maps motion vectors from $\{\lambda(i)\}$ to $\{i\}$ coordinates, and $I_i$ is the [spatial inertia](/spatial-inertia/) of body $i$ about the origin of $\{i\}$. Spatial vectors have the angular part first, and $\mathrm{crm}$ and $\mathrm{crf}$ are the spatial cross products for motion and force vectors (see [spatial vector algebra](/spatial-vector-algebra/)). Gravity is $a_g = (0, g)$ with $g = (0, 0, -9.81)$ m/s$^2$ in base coordinates, and $f^{\mathrm{ext}}_i$ is an optional wrench of the outside world on body $i$ in $\{i\}$ coordinates.

Input: the model, $q$, $\dot q$, $\tau \in \mathbb{R}^n$, $a_g$ and $f^{\mathrm{ext}}$. Output: the vector $\ddot q$ with
$$M(q)\ddot q = \tau - C(q, \dot q)\dot q - g(q) + \textstyle\sum_i J_i(q)^T f^{\mathrm{ext}}_i ,$$
the [manipulator equation](/manipulator-equation/) solved for $\ddot q$. Equivalently, $\ddot q$ is the unique vector with $\mathrm{RNEA}(q, \dot q, \ddot q) = \tau$.

## The algorithm

```pseudo id=main
ABA(model, q, q̇, τ, a_g, f_ext)
L1  for i ← 1 to n do                                  ▷ pass 1: velocities
L2      X_i ← Ad(T_{λ(i),i}(q_i)^-1)
L3      v_i ← X_i v_λ(i) + S_i q̇_i                     ▷ v_0 = 0
L4      c_i ← crm(v_i) S_i q̇_i
L5      I^A_i ← I_i ; p^A_i ← crf(v_i) I_i v_i - f_ext,i
L6  for i ← n downto 1 do                              ▷ pass 2: articulated inertias
L7      U_i ← I^A_i S_i ; D_i ← S_i^T U_i ; u_i ← τ_i - S_i^T p^A_i
L8      if λ(i) ≠ 0 then
L9          I^a ← I^A_i - U_i U_i^T / D_i
L10         p^a ← p^A_i + I^a c_i + U_i u_i / D_i
L11         I^A_λ(i) ← I^A_λ(i) + X_i^T I^a X_i ; p^A_λ(i) ← p^A_λ(i) + X_i^T p^a
L12 a_0 ← -a_g                                         ▷ gravity as a base acceleration
L13 for i ← 1 to n do                                  ▷ pass 3: accelerations
L14     a'_i ← X_i a_λ(i) + c_i
L15     q̈_i ← (u_i - U_i^T a'_i) / D_i
L16     a_i ← a'_i + S_i q̈_i
L17 return q̈
```

The second pass keeps the invariant $f_i = I^A_i a_i + p^A_i$: the wrench that joint $i$ transmits to body $i$ is an affine function of the acceleration of body $i$, when the joints beyond it obey their own equations. $I^A_i$ is the articulated-body inertia and $p^A_i$ is the bias force: the wrench needed when $a_i = 0$, which holds the velocity product terms, the external forces and the joint forces of the subtree. Line L7 solves the joint equation $\tau_i = S_i^T f_i$ for $\ddot q_i$ in terms of the parent acceleration. Lines L9 and L10 put that solution back into $f_i$, which gives the inertia $I^a$ and the bias $p^a$ that the parent feels through joint $i$. Line L11 adds them to the parent. The third pass uses line L15, the joint equation solved for $\ddot q_i$, once the acceleration of the parent is known.

## Example

Take the planar arm with two revolute joints about $z$, links of 1 m, point masses of 1 kg at the link ends and no gravity. Frame $\{2\}$ is 1 m along link 1, both screw axes are $S = (0, 0, 1, 0, 0, 0)$, and each point mass is at $(1, 0, 0)$ in its own frame. Take $q = (0, \pi/2)$, $\dot q = (1, 1)$ rad/s and $\tau = 0$.

Pass 1 gives $v_1 = (0, 0, 1,\ 0, 0, 0)$, $v_2 = (0, 0, 2,\ 1, 0, 0)$, $c_1 = 0$ and $c_2 = (0, 0, 0,\ 0, -1, 0)$. The bias forces are $p^A_1 = (0, 0, 0,\ -1, 0, 0)$, the centripetal force on mass 1, and $p^A_2 = (0, 0, 2,\ -4, 2, 0)$.

Pass 2, body 2: $U_2 = I_2 S_2 = (0, 0, 1,\ 0, 1, 0)$, $D_2 = 1$ and $u_2 = 0 - S_2^T p^A_2 = -2$. Line L9 removes from $I_2$ the part that joint 2 lets swing, and line L10 gives $p^a = (0, 0, 0,\ -4, 0, 0)$. After line L11,
$$I^A_1 = \begin{pmatrix} 1 & -1 & 0 & 0 & 0 & 1 \\ -1 & 2 & 0 & 0 & 0 & -2 \\ 0 & 0 & 2 & 0 & 2 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 2 & 0 & 2 & 0 \\ 1 & -2 & 0 & 0 & 0 & 2 \end{pmatrix}, \qquad p^A_1 = (0, 0, -4,\ -1, -4, 0).$$
Body 1: $U_1 = (0, 0, 2,\ 0, 2, 0)$, $D_1 = 2$ and $u_1 = 4$.

$D_1 = 2$ is the inertia that joint 1 feels with joint 2 free. With joint 2 locked, the whole arm is one rigid body and joint 1 feels $M_{11} = 3$ kg m$^2$. With joint 2 free, it feels only $M_{11} - M_{12}^2/M_{22} = 3 - 1 = 2$ kg m$^2$.

Pass 3: $a'_1 = 0$, so $\ddot q_1 = 4/2 = 2$ rad/s$^2$ and $a_1 = (0, 0, 2,\ 0, 0, 0)$. Then $a'_2 = X_2 a_1 + c_2 = (0, 0, 2,\ 2, -1, 0)$ and $\ddot q_2 = (-2 - U_2^T a'_2)/1 = (-2 - 1)/1 = -3$ rad/s$^2$.

So $\ddot q = (2, -3)$ rad/s$^2$. As a check, with $M = \begin{pmatrix} 3 & 1 \\ 1 & 1 \end{pmatrix}$ and the velocity terms $C\dot q = (-3, 1)$ N m from the RNEA example, $M\ddot q = (3, -1) = -C\dot q$.

## Correctness

The second pass proves $f_i = I^A_i a_i + p^A_i$ by backward induction. For a leaf, $f_i$ is the Newton-Euler wrench $I_i a_i + \mathrm{crf}(v_i) I_i v_i - f^{\mathrm{ext}}_i$. For an inner body, each child $c$ adds $X_c^T f_c$, with $f_c = I^A_c a_c + p^A_c$ by induction and $a_c = X_c a_i + c_c + S_c \ddot q_c$. The joint equation $\tau_c = S_c^T f_c$ fixes $\ddot q_c$, and the result is affine in $a_i$ with the matrix $X_c^T I^a_c X_c$, which is lines L9 to L11. Each $D_i$ is positive, because $I^A_i$ is the positive definite $I_i$ plus positive semidefinite terms. The forward pass then evaluates the joint equations in the order from the base, and it gives the unique solution of $\mathrm{RNEA}(q, \dot q, \ddot q) = \tau$. The full proof is in the correctness proof of this page.

## Complexity

In the [real RAM](/real-ram/), each step of each pass does a fixed number of operations on $6 \times 6$ matrices and 6-vectors, so the time is $\Theta(n)$ for any tree, and the extra space is $\Theta(n)$. This is optimal in order, because the output has $n$ entries.

The constant is larger than that of the RNEA, mainly because line L11 moves a $6 \times 6$ matrix through a transform for each body. Featherstone (2008, Chapter 10) gives exact operation counts for the ABA, the CRBA and the RNEA. Featherstone (1987) reports that the articulated-body method becomes faster than the composite rigid body method with a Cholesky solve for chains of about nine or more bodies. The crossover depends on the implementation and on the shape of the tree: for robots with short branches, the CRBA with a sparse factorization is often as fast.

## Properties

- **No mass matrix.** The ABA never forms or factors $M(q)$; it solves $M\ddot q = \tau - b$ implicitly by a recursive factorization along the tree.
- **Exact.** The only errors are floating-point rounding. Featherstone (2008, Chapter 10) discusses the accuracy and the efficiency of the dynamics algorithms.
- **Linear in $\tau$ and $f^{\mathrm{ext}}$.** For fixed $q$ and $\dot q$, $\ddot q$ is affine in $\tau$ and in the external wrenches, with the matrix $M^{-1}$.
- **Inverse of the RNEA.** $\mathrm{RNEA}(q, \dot q, \mathrm{ABA}(q, \dot q, \tau)) = \tau$ for every $\tau$.
- **Articulated inertia bounds.** $I^A_i$ lies between the inertia $I_i$ of body $i$ alone and the composite inertia of the subtree of $i$, in the order of positive semidefinite matrices; see [articulated-body inertia](/articulated-body-inertia/).
- **The transmitted inertia is singular.** $I^a S_i = 0$: a free joint transmits no inertia along its own axis.

## Variants and improvements

- **Floating base.** With a free base, the base is body 1 with a six degree of freedom joint; the ABA handles it with $6 \times 6$ matrices $U$ and $D$, and $D$ is the articulated inertia of the whole robot. See [floating-base dynamics](/floating-base-dynamics/).
- **Multi-degree-of-freedom joints.** For a joint with $k$ degrees of freedom, $S_i$ is $6 \times k$, $D_i$ is a $k \times k$ matrix and line L15 solves a small linear system.
- **Hybrid dynamics.** Some joints may have a given acceleration and others a given force; the passes then mix the RNEA and the ABA. Featherstone (2008, Chapter 9) treats this as hybrid dynamics, together with floating bases.
- **Inverse of the mass matrix.** With $\dot q = 0$, no gravity and $\tau = e_j$, the ABA returns column $j$ of $M(q)^{-1}$. So $n$ calls give $M^{-1}$ in $\Theta(n^2)$ without forming $M$; the second pass does not depend on $\tau$ except through $u_i$ and can be shared.
- **Derivatives.** The partial derivatives of $\ddot q$ by $q$, $\dot q$ and $\tau$ come from the derivatives of the RNEA and $M^{-1}$; see [analytical derivatives of rigid body dynamics](/rigid-body-dynamics-derivatives/).

## When to use it

Use the ABA to simulate a robot: for long serial chains, for robots with many bodies, and in any loop that only needs $\ddot q$. If you also need $M(q)$, for example for a controller, the [composite rigid body algorithm](/composite-rigid-body-algorithm/) gives it, and a Cholesky solve is then almost free. For two or three joints, both methods are fast, and the simpler one is fine.

## Pitfalls

- **Bodies without mass.** A body with $I_i = 0$, and no subtree with mass, gives $D_i = 0$ and a division by zero. A floating base modelled as six joints has five massless bodies; it works only because the last body of the base carries mass. The implementation raises an error if $D_i \le 0$.
- **The sign of gravity.** Line L12 sets $a_0 = -a_g$, as in the RNEA.
- **Dropping $I^a c_i$ in line L10.** The velocity product term of the child must enter the bias force of the parent; without it, the result is right only at zero velocity.
- **Using $I^A_i$ in place of $I^a$.** The parent receives $I^a$, the inertia with the free joint removed, not $I^A_i$. With $I^A_i$, the result is the dynamics of the robot with the joint locked.
- **Comparing against a dense solve.** For checks, compare with $\mathrm{RNEA}(q, \dot q, \ddot q) = \tau$, which tests the result without a second solver and its own rounding.

## Implementations

## History

Featherstone (1983) introduced articulated-body inertias and the $O(n)$ algorithm for the forward dynamics of a serial robot. His 1987 book extended it, compared it with the composite rigid body method of Walker and Orin, and gave the crossover in efficiency. His 2008 book gives the algorithm for kinematic trees in the spatial notation that this page uses, and the chapter by Featherstone and Orin in the Springer Handbook of Robotics gives a short form. The name Featherstone's algorithm refers to the 1983 paper.

## References
