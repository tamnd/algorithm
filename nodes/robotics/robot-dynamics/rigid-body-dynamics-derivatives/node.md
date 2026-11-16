---
tag: M6C9BY
kind: algorithm
slug: rigid-body-dynamics-derivatives
name: Analytical derivatives of rigid body dynamics
aliases:
- RNEA derivatives
area: robotics/robot-dynamics
level: research
summary: "Carpentier and Mansard's recursion for the partial derivatives of inverse dynamics in O(n d) time for a tree of depth d (O(n^2) for a serial chain), and of forward dynamics through M^-1."
model: real-ram
complexity:
  vars: {n: "the number of joints, one degree of freedom each", d: "the depth of the tree, the largest number of joints on a path from the base (d = n for a serial chain)"}
  time: {inverse: Θ(n d), forward: O(n^3)}
  space: {extra: Θ(n d)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 2018
  people: [Justin Carpentier, Nicolas Mansard]
  note: Carpentier and Mansard differentiated the recursive Newton-Euler algorithm in closed form with spatial algebra and made the derivatives several times faster than finite differences.
prereqs: [recursive-newton-euler-algorithm, composite-rigid-body-algorithm]
see_also: [automatic-differentiation, trajectory-optimization, control-limited-ddp, nonlinear-mpc, articulated-body-algorithm, jacobian-linearization, contact-implicit-trajectory-optimization, forward-dynamics]
sources:
  - paper: doi:10.15607/RSS.2018.XIV.038
    title: Justin Carpentier and Nicolas Mansard, Analytical derivatives of rigid body dynamics algorithms, Robotics, Science and Systems XIV, 2018
    locator: "Sections II to V (spatial algebra, the derivatives of the recursive Newton-Euler algorithm, the derivatives of forward dynamics, and the benchmarks)"
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 2 (spatial vector algebra, the cross products and the derivatives of spatial vectors) and Chapter 5 (inverse dynamics)"
  - paper: doi:10.1115/1.3149599
    title: J. Y. S. Luh, M. W. Walker and R. P. C. Paul, On-line computational scheme for mechanical manipulators, Journal of Dynamic Systems, Measurement, and Control 102(2), 1980
    locator: pages 69 to 76 (the recursion that is differentiated)
---

The analytical derivatives of rigid body dynamics are the partial derivatives of the joint forces $\tau = \mathrm{ID}(q, \dot q, \ddot q)$ by the joint positions $q$ and velocities $\dot q$, and the partial derivatives of the accelerations $\ddot q = \mathrm{FD}(q, \dot q, \tau)$ by $q$, $\dot q$ and $\tau$. Carpentier and Mansard (2018) computed the derivatives of the inverse dynamics by differentiating each line of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) (RNEA) with spatial algebra, and they obtained the derivatives of the [forward dynamics](/forward-dynamics/) from them with the inverse of the [joint-space inertia matrix](/joint-space-inertia-matrix/). The result is exact up to rounding, unlike finite differences, and much faster than finite differences or general [automatic differentiation](/automatic-differentiation/) of the RNEA. The derivatives are what [trajectory optimization](/trajectory-optimization/), [DDP](/control-limited-ddp/) and [nonlinear MPC](/nonlinear-mpc/) need at every step. The cost is $O(n d)$ for a tree of depth $d$, which is $\Theta(n^2)$ for a serial chain. It cannot be $O(n)$, because the output of a serial chain has $\Theta(n^2)$ nonzero entries.

## In plain words

An optimizer that plans the motion of a robot must know how a small change of a joint angle or speed changes the forces at all the joints. The simple way is to nudge each joint a little, run the force computation again, and compare. That needs many runs, and the nudge spoils the digits. This method works out the change directly. It follows the same two walks over the robot as the force computation, out to the tips and back to the base. Next to each link's motion it also carries how that motion changes with each joint above it. On the way back, it carries how each joint push changes. A link far out on a long arm depends on every joint before it, so the total work grows with the length of the arm times the number of links.

## The problem

The robot is a tree of $n$ rigid bodies with the notation of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/): body $i$ has the parent $\lambda(i) < i$ ($\lambda(i) = 0$ for the base), joint $i$ has the screw axis $S_i$ in the frame $\{i\}$, $X_i = \mathrm{Ad}(T_{\lambda(i),i}(q_i)^{-1})$ with $T_{\lambda(i),i}(q_i) = T^{\mathrm{tree}}_i e^{[S_i] q_i}$, and $I_i$ is the [spatial inertia](/spatial-inertia/) of body $i$. Spatial vectors have the angular part first, and $\mathrm{crm}$ and $\mathrm{crf}$ are the spatial cross products of [spatial vector algebra](/spatial-vector-algebra/). $\mathrm{anc}(i)$ is the set of body $i$ and its ancestors.

Input: the model, $q, \dot q, \ddot q \in \mathbb{R}^n$ and gravity $a_g$. Output: $\tau = \mathrm{ID}(q, \dot q, \ddot q)$ and the three $n \times n$ matrices $\partial \tau/\partial q$, $\partial \tau/\partial \dot q$ and $\partial \tau/\partial \ddot q = M(q)$.

For the forward dynamics, the input is $q, \dot q, \tau$ and the output is $\ddot q = \mathrm{FD}(q, \dot q, \tau)$ with $\partial \ddot q/\partial q$, $\partial \ddot q/\partial \dot q$ and $\partial \ddot q/\partial \tau$.

## The algorithm

The algorithm rests on two identities for the derivative of a joint transform. Since $X_i(q_i + h) = \mathrm{Ad}(e^{-[S_i]h}) X_i(q_i)$, for a motion vector $m$ and a force vector $f$ that do not depend on $q_i$,
$$\frac{\partial (X_i m)}{\partial q_i} = \mathrm{crm}(X_i m)\, S_i, \qquad \frac{\partial (X_i^T f)}{\partial q_i} = X_i^T\, \mathrm{crf}(S_i)\, f .$$
For each body, the algorithm stores the derivatives of $v_i$, $a_i$ and $f_i$ by the coordinates of the joints in $\mathrm{anc}(i)$; all other derivatives are 0. In the pseudocode, $\partial_k$ is the derivative by $q_k$, by $\dot q_k$ or by $\ddot q_k$, and a line with $\partial_k$ runs for each of the three.

```pseudo id=main
RNEA-DERIVATIVES(model, q, q̇, q̈, a_g)
L1  for i ← 1 to n do                                ▷ forward pass, with the RNEA
L2      X_i ← Ad(T_{λ(i),i}(q_i)^-1) ; v_i, a_i, f_i as in the RNEA
L3      for k in anc(λ(i)): ∂_k v_i ← X_i ∂_k v_λ(i) ; ∂_k a_i ← X_i ∂_k a_λ(i)
L4      ∂v_i/∂q_i ← crm(X_i v_λ(i)) S_i ; ∂a_i/∂q_i ← crm(X_i a_λ(i)) S_i
L5      ∂v_i/∂q̇_i ← S_i ; ∂a_i/∂q̇_i ← crm(v_i) S_i ; ∂a_i/∂q̈_i ← S_i
L6      for k in anc(i), by q and by q̇: ∂_k a_i ← ∂_k a_i + crm(∂_k v_i) S_i q̇_i
L7      for k in anc(i): ∂_k f_i ← I_i ∂_k a_i + crf(∂_k v_i) I_i v_i + crf(v_i) I_i ∂_k v_i
L8  for i ← n downto 1 do                            ▷ backward pass
L9      τ_i ← S_i^T f_i ; for each stored k: ∂τ_i/∂u_k ← S_i^T ∂_k f_i
L10     if λ(i) ≠ 0 then
L11         for each stored k: ∂_k f_λ(i) ← ∂_k f_λ(i) + X_i^T ∂_k f_i
L12         ∂f_λ(i)/∂q_i ← ∂f_λ(i)/∂q_i + X_i^T crf(S_i) f_i
L13         f_λ(i) ← f_λ(i) + X_i^T f_i
L14 return τ, ∂τ/∂q, ∂τ/∂q̇, ∂τ/∂q̈
```

Line L3 carries the derivatives of the parent through $X_i$; it is the first part of the product rule, for the joints above $i$. Line L4 is the first identity, the derivative of $X_i$ itself by $q_i$. Line L5 is the direct effect of $\dot q_i$ and $\ddot q_i$. Line L6 differentiates the velocity product $\mathrm{crm}(v_i) S_i \dot q_i$ through $v_i$. Line L7 is the product rule on the Newton-Euler wrench $I_i a_i + \mathrm{crf}(v_i) I_i v_i$; for the derivatives by $\ddot q$, the velocity does not change and only $I_i\, \partial_k a_i$ is left. In the backward pass, the derivatives of $f_i$ by the joints below $i$ arrive from the children through line L11, and line L12 is the second identity, the derivative of $X_i^T$ by $q_i$.

The forward dynamics derivatives follow from the identity $\mathrm{ID}(q, \dot q, \mathrm{FD}(q, \dot q, \tau)) = \tau$. Differentiate it:
$$\frac{\partial \mathrm{FD}}{\partial q} = -M^{-1} \frac{\partial \mathrm{ID}}{\partial q}, \qquad \frac{\partial \mathrm{FD}}{\partial \dot q} = -M^{-1} \frac{\partial \mathrm{ID}}{\partial \dot q}, \qquad \frac{\partial \mathrm{FD}}{\partial \tau} = M^{-1},$$
where the derivatives of $\mathrm{ID}$ are evaluated at $\ddot q = \mathrm{FD}(q, \dot q, \tau)$, not at $\ddot q = 0$. So the forward derivatives cost one forward dynamics, one call of RNEA-DERIVATIVES, which also returns $M$, and a product with $M^{-1}$.

## Example

Take the planar arm with two revolute joints about $z$, links of 1 m and point masses of 1 kg at the link ends. Its inverse dynamics in closed form, with $c_2 = \cos q_2$ and $s_2 = \sin q_2$ and without gravity, is
$$\tau_1 = (3 + 2c_2)\ddot q_1 + (1 + c_2)\ddot q_2 - s_2(2\dot q_1\dot q_2 + \dot q_2^2), \qquad \tau_2 = (1 + c_2)\ddot q_1 + \ddot q_2 + s_2 \dot q_1^2 .$$
At $q = (0, \pi/2)$, $\dot q = (1, 1)$ rad/s and $\ddot q = 0$, the algorithm returns $\tau = (-3, 1)$ N m and
$$\frac{\partial \tau}{\partial \dot q} = \begin{pmatrix} -2 & -4 \\ 2 & 0 \end{pmatrix}, \qquad \frac{\partial \tau}{\partial q} = 0, \qquad \frac{\partial \tau}{\partial \ddot q} = M = \begin{pmatrix} 3 & 1 \\ 1 & 1 \end{pmatrix}.$$
The closed form gives the same: $\partial\tau_1/\partial\dot q_1 = -2 s_2 \dot q_2 = -2$, $\partial\tau_1/\partial\dot q_2 = -2 s_2(\dot q_1 + \dot q_2) = -4$, $\partial\tau_2/\partial\dot q_1 = 2 s_2 \dot q_1 = 2$, and $\tau_2$ does not depend on $\dot q_2$. The derivative by $q$ is 0 here, because $\tau$ does not depend on $q_1$ without gravity, and $\partial\tau/\partial q_2$ has the factors $s_2 \ddot q$ and $c_2 \dot q^2$, which are both 0 at this state.

For the forward dynamics at the same $q$ and $\dot q$ with $\tau = 0$, the [articulated-body algorithm](/articulated-body-algorithm/) gives $\ddot q = (2, -3)$ rad/s$^2$. At this $\ddot q$, the inverse dynamics derivative by $q$ is no longer 0: $\partial \mathrm{ID}/\partial q = \begin{pmatrix} 0 & -1 \\ 0 & -2 \end{pmatrix}$. With $M^{-1} = \tfrac12 \begin{pmatrix} 1 & -1 \\ -1 & 3 \end{pmatrix}$,
$$\frac{\partial \ddot q}{\partial q} = \begin{pmatrix} 0 & -0.5 \\ 0 & 2.5 \end{pmatrix}, \qquad \frac{\partial \ddot q}{\partial \dot q} = \begin{pmatrix} 2 & 2 \\ -4 & -2 \end{pmatrix}, \qquad \frac{\partial \ddot q}{\partial \tau} = \begin{pmatrix} 0.5 & -0.5 \\ -0.5 & 1.5 \end{pmatrix}.$$
The tests check the inverse dynamics values above, and they compare the inverse and forward derivatives on random trees of up to 7 joints with central finite differences ($h = 10^{-6}$, tolerance $10^{-6}$).

With gravity $9.81$ m/s$^2$ along $-y$ in the plane, at $q = (0.3, 0.7)$, $\dot q = (0.5, -1.2)$ and $\ddot q = (2, -1)$, the algorithm gives $\partial\tau/\partial q = \begin{pmatrix} -14.052936816 & -10.371045548 \\ -8.254830361 & -9.352055189 \end{pmatrix}$ and $\partial\tau/\partial\dot q = \begin{pmatrix} 1.546122449 & 0.901904762 \\ 0.644217687 & 0 \end{pmatrix}$.

## Correctness

The derivative of a composition is the composition of the derivatives, so it is enough to differentiate each line of the RNEA in order. Two facts make this simple. First, $X_i$ depends only on $q_i$, and the two identities above give its derivative in closed form. Second, $v_i$ and $a_i$ depend only on the joints in $\mathrm{anc}(i)$, and $f_i$ depends only on the joints that are on a common path with $i$, so all other derivatives are 0 and need no storage. By induction over the forward pass, the stored derivatives of $v_i$, $a_i$ and the body wrench are exact; by backward induction, the derivatives of the transmitted wrench $f_i$ are complete when the loop reaches $i$, because all children have larger indices. The derivative of $\tau_i = S_i^T f_i$ is $S_i^T \partial f_i$, since $S_i$ is constant. The forward dynamics formulas follow from the chain rule applied to $\mathrm{ID}(q, \dot q, \mathrm{FD}(q, \dot q, \tau)) = \tau$. The correctness proof of this page gives each step.

## Complexity

In the [real RAM](/real-ram/), body $i$ stores $\mathrm{depth}(i)$ derivatives of each of $v_i$ and $a_i$ for each of $q$, $\dot q$ and $\ddot q$, and each costs a fixed number of $6 \times 6$ products. In the backward pass, the derivatives of $f_i$ cover the joints on a common path with $i$, and each one is moved to the parent once. The number of such pairs $(i, k)$ is at most $2\sum_i \mathrm{depth}(i)$, so the time is $O(n d)$ for a tree of depth $d$ and $\Theta(n^2)$ for a serial chain. This is the order of the number of nonzero entries of the output, so it is optimal in order. The extra space is $\Theta(n d)$ for the stored derivatives. An implementation that stores the output as dense matrices also spends $\Theta(n^2)$ to set them to zero.

Finite differences need $2n + 1$ or $4n + 1$ calls of the RNEA for the two derivatives, which is also $\Theta(n^2)$, but with a much larger constant, and they lose about half of the digits. The forward dynamics derivatives add a forward dynamics in $\Theta(n)$, the inverse $M^{-1}$ and two products of $n \times n$ matrices, which is $O(n^3)$ when done densely.

Carpentier and Mansard (2018) report measurements in their library Pinocchio on a 2.2 GHz Intel Core i7. For a KUKA arm, the HyQ quadruped and the Atlas humanoid, the inverse dynamics took 1.20, 2.14 and 5.51 µs, its analytical derivatives 3.34, 7.01 and 16.72 µs, and finite differences of the inverse dynamics 21.26, 88.52 and 452.46 µs. The analytical derivatives of the forward dynamics took 5.78, 14.24 and 45.20 µs. These are measurements on one machine, not bounds.

## Properties

- **Exact.** The derivatives are exact up to floating-point rounding. Central finite differences with a step $h$ have an error of order $h^2$ plus a rounding error of order $\varepsilon/h$.
- **$\partial\tau/\partial\ddot q = M(q)$.** The algorithm returns the joint-space inertia matrix as a side product, the same matrix that the [composite rigid body algorithm](/composite-rigid-body-algorithm/) computes.
- **Sparsity follows the tree.** $\partial\tau_i/\partial q_k$ and $\partial\tau_i/\partial\dot q_k$ are 0 when joints $i$ and $k$ are on different branches, the same pattern as the branch-induced sparsity of $M$.
- **Gravity enters only $\partial\tau/\partial q$.** Gravity is a base acceleration that does not depend on $\dot q$, so it changes $\partial\tau/\partial q$ only.
- **Linear in $\ddot q$.** $\partial\tau/\partial q$ is affine in $\ddot q$, and $\partial\tau/\partial\dot q$ does not depend on $\ddot q$.

## Variants and improvements

- **Matrix form.** Carpentier and Mansard (2018) write the same recursion with $6 \times n$ matrices per body in place of one derivative per joint, which suits vectorized linear algebra.
- **Automatic differentiation.** Forward or reverse mode [automatic differentiation](/automatic-differentiation/) of an RNEA code gives the same numbers, and it works for any code, but it has a larger constant.
- **Contact dynamics.** The same idea extends to constrained and contact dynamics, where the derivatives of the contact forces are needed for [contact-implicit trajectory optimization](/contact-implicit-trajectory-optimization/).
- **Floating base.** For a free base, the configuration lies on a Lie group, and the derivative by $q$ is taken in the tangent space; see [floating-base dynamics](/floating-base-dynamics/).
- **Second order.** Some optimizers need the second derivatives of the dynamics; they can be obtained by differentiating the recursion again, at a higher cost.

## When to use it

Use these derivatives inside gradient-based [trajectory optimization](/trajectory-optimization/), [control-limited DDP](/control-limited-ddp/), [nonlinear MPC](/nonlinear-mpc/) and [linearization](/jacobian-linearization/) of a robot model around a trajectory. They also give the Jacobians of the dynamics for an extended Kalman filter that estimates joint states. For one-time checks or very small arms, finite differences are fine. For a robot with a floating base and many joints, the analytical derivatives are the fastest exact choice.

## Pitfalls

- **Forward derivatives at the wrong acceleration.** $\partial\mathrm{FD}/\partial q = -M^{-1}\, \partial\mathrm{ID}/\partial q$ needs $\partial\mathrm{ID}/\partial q$ at $\ddot q = \mathrm{FD}(q, \dot q, \tau)$, not at $\ddot q = 0$. The example above shows the difference.
- **The derivative of $X_i^T$.** Forgetting line L12 drops the term $X_i^T \mathrm{crf}(S_i) f_i$ and gives wrong entries $\partial\tau_j/\partial q_i$ for the ancestors $j$ of $i$, but correct diagonal entries.
- **The sign convention of the joint transform.** The identities hold for $T = T^{\mathrm{tree}} e^{[S_i]q_i}$ with $S_i$ in the child frame. With the exponential on the left, $S_i$ is in the parent frame, and the identities change.
- **Finite differences as the reference.** They agree only to about $10^{-6}$ to $10^{-8}$ in double precision. A test needs a tolerance to match.
- **A claim of $O(n)$.** The derivatives of a serial chain have $\Theta(n^2)$ nonzero entries, so no algorithm can output them in $O(n)$ time.

## Implementations

## History

Before 2018, robot software computed the derivatives of the dynamics by finite differences or by automatic differentiation of the RNEA, and the Euler-Lagrange form gave symbolic derivatives for small arms. Carpentier and Mansard (2018) differentiated the RNEA in closed form with spatial algebra, derived the forward dynamics derivatives from it, and released the method in the open-source library Pinocchio. Their measurements showed the analytical derivatives several times faster than finite differences, with the gap growing with the size of the robot.

## References
