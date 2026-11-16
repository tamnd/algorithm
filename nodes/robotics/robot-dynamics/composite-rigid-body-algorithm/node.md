---
tag: 7BWY71
kind: algorithm
slug: composite-rigid-body-algorithm
name: Composite rigid body algorithm
aliases:
- CRBA
- Walker-Orin method
area: robotics/robot-dynamics
level: core
summary: "Builds the joint-space inertia matrix from the inertias of the subtrees beyond each joint, in O(n d) time for a tree of depth d, which is O(n^2) for a serial chain."
model: real-ram
complexity:
  vars: {n: "the number of joints, one degree of freedom each", d: "the depth of the tree, the largest number of joints on a path from the base (d = n for a serial chain)"}
  time: {worst: Θ(n d)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1982
  people: [Michael W. Walker, David E. Orin]
  note: "Walker and Orin compared four methods for the simulation of robot arms; their third method, the composite rigid body method, was the fastest of them."
prereqs: [joint-space-inertia-matrix, recursive-newton-euler-algorithm, cholesky-decomposition]
see_also: [articulated-body-algorithm, forward-dynamics, spatial-inertia, articulated-body-inertia, centroidal-momentum-matrix, manipulator-equation, sparse-matrix, rigid-body-dynamics-derivatives]
sources:
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 6 (forward dynamics by inertia matrix methods): Section 6.2 (the composite-rigid-body algorithm) and Section 6.4 (branch-induced sparsity); Chapter 10 (accuracy and efficiency) for the operation counts"
  - paper: doi:10.1115/1.3139699
    title: M. W. Walker and D. E. Orin, Efficient dynamic computer simulation of robotic mechanisms, Journal of Dynamic Systems, Measurement, and Control 104(3), 1982
    locator: pages 205 to 211 (method 3)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 3, Dynamics, by Roy Featherstone and David E. Orin"
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 8, Section 8.5 (forward dynamics of open chains)
---

The composite rigid body algorithm (CRBA) computes the [joint-space inertia matrix](/joint-space-inertia-matrix/) $M(q)$ of a robot that is a serial chain or a tree of rigid bodies. It uses one idea: when only joint $j$ accelerates, everything beyond joint $j$ moves as one rigid body, the composite body of that subtree. The algorithm sums the [spatial inertias](/spatial-inertia/) of each subtree from the tips inward, and then reads each entry of $M$ as a product of a composite inertia with two joint axes. Together with one call of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) for the bias forces and a [Cholesky factorization](/cholesky-decomposition/), it solves the [forward dynamics](/forward-dynamics/) problem. The [articulated-body algorithm](/articulated-body-algorithm/) solves the same problem in $\Theta(n)$ without forming $M$; the CRBA costs more for long chains but is often faster for the small trees of real robots.

## In plain words

Picture a robot arm with all its joints locked except one. If you push that one joint, the part of the arm beyond it swings as one stiff piece. How hard that piece resists the push depends on its total mass and how far the mass is from the joint. The algorithm finds this resistance for every joint. It starts at the tip, where the stiff piece is only the last link. Moving inward, each piece is the next link plus the piece that hangs on it, so the work done for one joint is reused for the next. The resistance felt at a joint when another joint moves is found from the same stiff pieces. The result is a table of numbers that tells how the motion of every joint couples to every other joint.

## The problem

The robot is a tree of $n$ rigid bodies with the notation of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/): body $i$ has the parent $\lambda(i) < i$ ($\lambda(i) = 0$ for the base), joint $i$ has the screw axis $S_i$ in the frame $\{i\}$ of body $i$, $X_i = \mathrm{Ad}(T_{\lambda(i),i}(q_i)^{-1})$ maps motion vectors from $\{\lambda(i)\}$ to $\{i\}$ coordinates, and $I_i$ is the spatial inertia of body $i$ about the origin of $\{i\}$. Spatial vectors have the angular part first, as in Featherstone (2008).

Input: the model and $q \in \mathbb{R}^n$. Output: the symmetric matrix $H = M(q) \in \mathbb{R}^{n \times n}$ of the [manipulator equation](/manipulator-equation/) $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$. Featherstone writes $H$ for this matrix; here $H$ and $M$ are the same.

For the [forward dynamics](/forward-dynamics/) problem, the CRBA is one step: compute the bias $b = C(q, \dot q)\dot q + g(q)$ as $\mathrm{RNEA}(q, \dot q, 0)$, compute $H$ by the CRBA, and solve $H \ddot q = \tau - b$.

## The algorithm

```pseudo id=main
CRBA(model, q)
L1  for i ← 1 to n do X_i ← Ad(T_{λ(i),i}(q_i)^-1) ; I^c_i ← I_i ; H ← 0
L2  for i ← n downto 1 do
L3      if λ(i) ≠ 0 then I^c_λ(i) ← I^c_λ(i) + X_i^T I^c_i X_i
L4      F ← I^c_i S_i                      ▷ the wrench to accelerate the subtree of i
L5      H_ii ← S_i^T F
L6      j ← i
L7      while λ(j) ≠ 0 do                   ▷ climb to the base
L8          F ← X_j^T F ; j ← λ(j)
L9          H_ij ← S_j^T F ; H_ji ← H_ij
L10 return H
```

$I^c_i$ is the composite inertia of the subtree of body $i$, in the coordinates of $\{i\}$. Line L3 moves it into the frame of the parent and adds it to the parent's composite inertia. Because every child has a larger index than its parent, the loop of line L2 completes $I^c_i$ before it uses it.

Line L4 has a physical meaning. If only joint $i$ accelerates, at unit rate, with no velocity and no gravity, the subtree of $i$ moves as one rigid body with the acceleration $S_i$, and $F = I^c_i S_i$ is the wrench that joint $i$ must transmit. Joint $i$ feels $S_i^T F$ of it (line L5). Every joint $j$ between $i$ and the base must transmit the same wrench, moved into its own frame (line L8), and feels $S_j^T F$ of it (line L9). So $H_{ji}$ is the force at joint $j$ per unit acceleration of joint $i$. Entries for pairs of joints on different branches are never written and stay 0.

## Example

Take the planar arm with two revolute joints, links of 1 m, and point masses of 1 kg at the link ends. Frame $\{2\}$ is 1 m along link 1, both screw axes are $S = (0, 0, 1, 0, 0, 0)$, and each point mass is at $(1, 0, 0)$ in its own frame. Take $q = (0, \pi/2)$.

- $i = 2$: $I^c_2 = I_2$. Line L4 gives $F = I_2 S_2 = (0, 0, 1,\ 0, 1, 0)$: an angular momentum of 1 about the joint and a linear part of 1 N along $y$ of $\{2\}$. Line L5 gives $H_{22} = 1$.
- Line L8 moves $F$ into $\{1\}$: $X_2^T F = (0, 0, 1,\ -1, 0, 0)$. Line L9 gives $H_{12} = H_{21} = 1$.
- Line L3 for $i = 2$ also made $I^c_1 = I_1 + X_2^T I_2 X_2$, the inertia of both masses about joint 1. Its third column is $(0, 0, 3,\ -1, 2, 0)$: the two masses at $(1, 0)$ and $(1, 1)$ m have a moment of inertia $1 + 2 = 3$ kg m$^2$ about the $z$ axis through joint 1.
- $i = 1$: line L4 gives $F = I^c_1 S_1 = (0, 0, 3,\ -1, 2, 0)$ and line L5 gives $H_{11} = 3$.

So $M = \begin{pmatrix} 3 & 1 \\ 1 & 1 \end{pmatrix}$, which is the closed form $\begin{pmatrix} 3 + 2c_2 & 1 + c_2 \\ 1 + c_2 & 1 \end{pmatrix}$ at $c_2 = 0$.

For forward dynamics, take $q = (0.3, 0.7)$, $\dot q = (0.5, -1.2)$ rad/s, gravity $9.81$ m/s$^2$ along $-y$ in the plane, and $\tau = (31.183981854, 7.991104417)$ N m. The RNEA gives the bias $b$, and the Cholesky solve of $M\ddot q = \tau - b$ gives $\ddot q = (2, -1)$ rad/s$^2$ to rounding, which is the motion that the RNEA example produced this $\tau$ from.

## Correctness

With $\dot q = 0$ and no gravity, the RNEA gives $\tau = M(q)\ddot q$, and it shows that $\tau_i$ collects the wrenches $I_l a_l$ of the bodies $l$ in the subtree of $i$, where $a_l$ sums the accelerations $S_k \ddot q_k$ of the joints $k$ on the path from $l$ to the base. The coefficient of $\ddot q_j$ in $\tau_i$ is then a sum over the bodies that are beyond both $i$ and $j$. If $j$ is on the path from $i$ to the base, this set is the subtree of $i$, and the sum is $S_i^T I^c_i X_{i \leftarrow j} S_j$, where $X_{i \leftarrow j}$ is the product of the joint transforms from $j$ to $i$. If $i$ and $j$ are on different branches, the set is empty and the entry is 0. Lines L4 to L9 compute the first case for every pair, and the climb of line L8 builds $X_{i \leftarrow j}^T F$ one joint at a time. The same sum shows $\dot q^T M \dot q = \sum_l v_l^T I_l v_l$, which is twice the kinetic energy, so $M$ is symmetric positive definite when every body has positive mass and inertia. The correctness proof of this page gives the details.

## Complexity

In the [real RAM](/real-ram/), line L3 costs a fixed number of $6 \times 6$ products per body, and the climb from body $i$ costs one transform and one dot product per ancestor of $i$. The time is $\Theta(n + \sum_i \mathrm{depth}(i))$. For a tree of depth $d$ this is $O(n d)$; for a serial chain, $d = n$ and the time is $\Theta(n^2)$; for a robot with short branches, such as a legged robot with a floating base, it is much less. These counts do not include the factorization. The extra space is $\Theta(n)$ besides the output matrix. A dense output matrix also costs $\Theta(n^2)$ to set to zero; a sparse storage of only the nonzero entries avoids this.

The forward dynamics also needs the factorization. A dense Cholesky factorization costs $\Theta(n^3)$, and the two triangular solves cost $\Theta(n^2)$. Featherstone (2008, Chapter 6) shows that the factorization in the order $L^T L$ keeps the zeros of branch-induced sparsity, and then costs $O(n d^2)$. Exact operation counts of the CRBA and of its use for forward dynamics are in Featherstone (2008, Chapter 10).

## Properties

- **Exact.** No approximation, only floating-point rounding.
- **Symmetric by construction.** Line L9 writes each pair once and copies it, so the output is exactly symmetric, also in floating point.
- **Branch-induced sparsity.** $H_{ij} = 0$ when joints $i$ and $j$ are on different branches. The zeros do not depend on $q$.
- **Positive definite.** $M(q)$ is symmetric positive definite when every body has positive mass and positive definite rotational inertia, as the proof shows.
- **Independent of $\dot q$ and $g$.** $M$ depends only on $q$. One evaluation can serve several right sides, for example in an implicit integrator or for the operational space quantities.
- **Kinetic energy.** $\tfrac12 \dot q^T M(q) \dot q$ is the kinetic energy of the robot, a cheap check of an implementation.

## Variants and improvements

- **Column by column.** The simplest way to build $M$ calls the RNEA $n$ times, with $\ddot q = e_j$, no velocity and no gravity, to get column $j$. This costs $\Theta(n^2)$ for any tree, with a larger constant than the CRBA, and it ignores the sparsity. The tests of this page use it as the reference.
- **Sparse factorization.** Featherstone (2008, Chapter 6) factors $H = L^T L$ in an order that creates no fill-in, so the cost of the factorization and of the solves follows the shape of the tree.
- **Centroidal momentum.** The composite inertias $I^c_i$ also give the [centroidal momentum matrix](/centroidal-momentum-matrix/) at almost no extra cost.
- **Derivatives.** The [derivatives of rigid body dynamics](/rigid-body-dynamics-derivatives/) give $M$ as $\partial\tau/\partial\ddot q$ as a side product.
- **Floating base.** With a free-floating base, the first $6 \times 6$ block of $M$ is the composite inertia of the whole robot, $I^c_1$; see [floating-base dynamics](/floating-base-dynamics/).

## When to use it

Use the CRBA when you need $M(q)$ itself: for the [operational space formulation](/operational-space-formulation/), for a quadratic program of a whole-body controller, to compute the kinetic energy, or for a forward dynamics with a few joints. For forward dynamics of a long serial chain, the [articulated-body algorithm](/articulated-body-algorithm/) is faster; Featherstone (1987) reports that it becomes faster than the composite rigid body method for chains of about nine bodies or more. For robots with short branches, such as legged robots and humanoids, the CRBA with a sparse factorization is competitive.

## Pitfalls

- **Missing bias forces.** Forward dynamics needs $\tau - C\dot q - g$ on the right side; the CRBA gives only the matrix.
- **The order of the bodies.** Line L3 must run for a child before its parent uses $I^c$. With $\lambda(i) < i$ and a loop from $n$ down, this holds.
- **The transform direction.** Line L8 needs $X_j^T$, the force transform from $\{j\}$ to $\{\lambda(j)\}$. Using $X_j$ gives wrong off-diagonal entries but correct diagonal entries, so a test of the diagonal alone does not catch it.
- **Cholesky on a matrix that is not positive definite.** With massless bodies, such as the first five bodies of a floating base modelled by six joints, $M$ is still positive definite only if the masses beyond them make it so. Check the pivots.
- **Dense storage for a tree.** Storing and factoring $M$ as a dense matrix throws away the sparsity of a branched robot.

## Implementations

## History

Walker and Orin (1982) compared four methods for the dynamic simulation of robot arms. Their third method computes the inertia matrix from composite rigid bodies, and it was the fastest of the four in their comparison. Featherstone (1987, 2008) rewrote the method with spatial vectors as the composite-rigid-body algorithm, extended it to trees, and showed how branch-induced sparsity makes the factorization cheaper. The name Walker-Orin method refers to the 1982 paper.

## References
