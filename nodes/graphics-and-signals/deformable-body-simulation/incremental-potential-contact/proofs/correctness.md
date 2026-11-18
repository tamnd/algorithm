---
title: The barrier is smooth, the projected Newton step is a descent step, the step bound keeps every distance positive, and stationary points carry nonnegative contact forces
proves: [correctness]
status: full
---

We use the notation of the page for the 2D code. The free vertices have masses $m_i > 0$ and positions $\mathbf x_i \in \mathbb R^2$; pinned vertices are fixed. Springs $s = (a, b)$ have rest length $r_s > 0$, stiffness $k_s > 0$ and energy $E_s = \frac{k_s}{2}(|\mathbf x_a - \mathbf x_b| - r_s)^2$, and $\Psi = \sum_s E_s$. The obstacles are fixed segments $S_1, \dots, S_c$ of positive length, and $d_{ik}(\mathbf x) = \operatorname{dist}(\mathbf x_i, S_k)$. With $\hat{\mathbf x} = \mathbf x^n + \Delta t\mathbf v^n + \Delta t^2\mathbf g$ on the free vertices, the barrier augmented incremental potential is

$$B(\mathbf x) = \tfrac12(\mathbf x - \hat{\mathbf x})^T M(\mathbf x - \hat{\mathbf x}) + \Delta t^2\Psi(\mathbf x) + \kappa\sum_{i,k} b(d_{ik}(\mathbf x)),$$

with $\kappa > 0$, $\hat d > 0$ and $b(d) = -(d - \hat d)^2\ln(d/\hat d)$ for $0 < d < \hat d$ and $b(d) = 0$ for $d \ge \hat d$. The feasible set is $\mathcal A = \{\mathbf x : d_{ik}(\mathbf x) > 0 \text{ for all } i, k\}$, and $B = +\infty$ outside it. All statements are for exact arithmetic.

## The barrier

**Lemma 1.** On $(0, \infty)$, $b$ is $C^2$, $b \ge 0$, $b' \le 0$ and $b'' \ge 0$, with $b > 0$, $b' < 0$ and $b'' > 0$ on $(0, \hat d)$. Also $b(d) \to +\infty$ as $d \to 0^+$, and $b$, $b'$ and $b''$ tend to $0$ as $d \to \hat d^-$.

*Proof.* Let $t = d - \hat d < 0$ and $\ell = \ln(d/\hat d) < 0$ on $(0, \hat d)$. Then $b = -t^2\ell > 0$, $b' = -2t\ell - t^2/d$ and $b'' = -2\ell - 4t/d + t^2/d^2$. In $b'$, $-2t\ell < 0$ since $t < 0$ and $\ell < 0$, and $-t^2/d < 0$. In $b''$ all three terms are positive. As $d \to \hat d$, $t \to 0$ and $\ell \to 0$, so all three tend to $0$, which matches the zero function on $[\hat d, \infty)$ to second order; so $b$ is $C^2$ at $\hat d$. As $d \to 0$, $t^2 \to \hat d^2$ and $-\ell \to +\infty$. $\square$

**Lemma 2.** On $\mathcal A$, each $d_{ik}$ is $C^1$ with $|\nabla d_{ik}| = 1$. Where the closest point of $S_k$ is inside the segment, $\nabla d = \mathbf n$ (the unit normal toward $\mathbf x_i$) and $\nabla^2 d = 0$; where it is an end point $\mathbf c$, $\nabla d = \mathbf u = (\mathbf x_i - \mathbf c)/d$ and $\nabla^2 d = (I - \mathbf u\mathbf u^T)/d$, which is positive semidefinite.

*Proof.* The distance to a closed convex set is $C^1$ off the set, with gradient the unit vector from the closest point. In the two regions the formulas are the derivatives of $\mathbf n\cdot(\mathbf x - \mathbf a)$ and $|\mathbf x - \mathbf c|$. On the border of the regions the closest point is the end point and $\mathbf u = \mathbf n$, so the gradients agree. The Hessian of $|\mathbf x - \mathbf c|$ has eigenvalues $0$ (along $\mathbf u$) and $1/d$. $\square$

So $B$ is $C^1$ on $\mathcal A$ and $C^2$ away from the region borders, and $B(\mathbf x) \to +\infty$ when $\mathbf x$ approaches the boundary of $\mathcal A$ (Lemma 1, since all other terms are bounded on bounded sets). $B \ge 0$ because every term is nonnegative.

## The projected Hessian

**Lemma 3.** The matrix $H$ built by the code with `project=True` is the sum of $M$ and, for each stencil, the projection to positive semidefinite matrices of the stencil Hessian (the negative eigenvalues set to zero). So $H$ is symmetric positive definite on the free coordinates.

*Proof.* For a spring with length $\ell$ and direction $\mathbf n$, the Hessian of $\Delta t^2 E_s$ in $(\mathbf x_a, \mathbf x_b)$ is $\begin{pmatrix} K & -K \\ -K & K\end{pmatrix}$ with $K = \Delta t^2 k_s(\mathbf n\mathbf n^T + \sigma(I - \mathbf n\mathbf n^T))$ and $\sigma = 1 - r_s/\ell$. Its eigenvalues are $0, 0, 2\Delta t^2 k_s, 2\Delta t^2 k_s\sigma$, with eigenvectors $(\mathbf w, \mathbf w)$ and $(\mathbf w, -\mathbf w)$ for $\mathbf w$ an eigenvector of $K$. Replacing $\sigma$ by $\max(\sigma, 0)$ sets the one possibly negative eigenvalue to zero and keeps the eigenvectors, which is the projection. Dropping a pinned end removes rows and columns, which keeps the matrix positive semidefinite.

For a contact pair, the Hessian of $\kappa b(d)$ in $\mathbf x_i$ is $\kappa(b''\nabla d\nabla d^T + b'\nabla^2 d)$ (equation (7) of the paper). In the interior region $\nabla^2 d = 0$ and the matrix is $\kappa b''\mathbf n\mathbf n^T \succeq 0$. In the end point region it is $\kappa b''\mathbf u\mathbf u^T + \kappa(b'/d)(I - \mathbf u\mathbf u^T)$ by Lemma 2, with eigenvalues $\kappa b'' \ge 0$ along $\mathbf u$ and $\kappa b'/d \le 0$ across it (Lemma 1). The projection keeps $\kappa b''\mathbf u\mathbf u^T$, which is what the code assembles. The sum of $M \succ 0$ and positive semidefinite matrices is positive definite. $\square$

**Lemma 4 (descent direction).** If $\mathbf g = \nabla B(\mathbf z) \ne 0$, the Newton direction $\mathbf p = -H^{-1}\mathbf g$ satisfies $\mathbf g^T\mathbf p < 0$. If $\mathbf p = 0$, then $\nabla B(\mathbf z) = 0$.

*Proof.* $\mathbf g^T\mathbf p = -\mathbf g^T H^{-1}\mathbf g < 0$ since $H^{-1}$ is positive definite (Lemma 3). If $\mathbf p = 0$ then $\mathbf g = -H\mathbf p = 0$. $\square$

## The step bound

**Lemma 5.** Let $\mathbf q \notin S$ and let $\mathbf q(t) = \mathbf q + t\,\Delta\mathbf q$. `segment_toi` returns the smallest $t \in [0, 1]$ with $\mathbf q(t) \in S$, or none if there is no such $t$.

*Proof.* Let $S$ have ends $\mathbf a$ and $\mathbf b$ and $\mathbf e = \mathbf b - \mathbf a$. The point $\mathbf q(t)$ is in $S$ exactly when $\mathbf q(t) = \mathbf a + s\mathbf e$ for some $s \in [0, 1]$. If $\Delta\mathbf q \times \mathbf e \ne 0$, this linear system in $(t, s)$ has the one solution of Cramer's rule used by the code, so there is at most one touching time, and the code returns it when $t, s \in [0, 1]$. If $\Delta\mathbf q \times \mathbf e = 0$ and $\mathbf q$ is not on the line of $S$, the path is parallel to the line and never meets it. If $\mathbf q$ is on the line, the path stays on the line; since $\mathbf q \notin S$ it is outside the segment, and it enters $S$ first at an end point, at the smaller of the times at which it passes $\mathbf a$ and $\mathbf b$, which the code computes. $\square$

**Theorem 6 (no crossing).** Let $\mathbf z \in \mathcal A$ and let $\alpha$ be the value of L6. Then $\mathbf z + \tau\mathbf p \in \mathcal A$ for all $\tau \in [0, \alpha]$. Hence every iterate of the step and the result are in $\mathcal A$: no free vertex touches or crosses a segment at any iterate, nor on the straight path between consecutive iterates.

*Proof.* Each free vertex moves on the line $\mathbf z_i + \tau\mathbf p_i$. If it would touch $S_k$ for some $\tau \in [0, 1]$, Lemma 5 gives the first such time $t_{ik} > 0$ (positive because $\mathbf z_i \notin S_k$), and the code sets $\alpha \le 0.8\,t_{ik} < t_{ik}$. If it touches no segment for $\tau \in [0, 1]$, then $\alpha \le 1$ is enough. So for $\tau \le \alpha$ no vertex is on a segment, and all distances are positive. The line search only shrinks $\alpha$, so the accepted point is on this safe path. The start $\mathbf z = \mathbf x^n$ is in $\mathcal A$ by assumption, and induction over the iterations and the steps gives the claim. $\square$

The factor $0.8$ keeps the vertex away from the segment, so that the barrier stays finite and the next step does not begin at a touching point. In floating point arithmetic the theorem needs a collision check that does not report a later time than the true one; that is the conservative hypothesis under which the paper states its guarantee. The test checks the time of impact against sampling of the path and fixes a point at 1000 m/s that the plain Newton step would carry through a thin segment.

## The line search

**Lemma 7 (monotone).** If $\nabla B(\mathbf z) \ne 0$, the halving loop of L7 stops with $B(\mathbf z + \alpha\mathbf p) \le B(\mathbf z)$ after a finite number of halvings. So the potential never increases over the iterations of a step.

*Proof.* By Theorem 6, $\phi(\tau) = B(\mathbf z + \tau\mathbf p)$ is finite on $[0, \alpha_0]$, and it is $C^1$ there with $\phi'(0) = \mathbf g^T\mathbf p < 0$ (Lemmas 2 and 4). So $\phi(\tau) < \phi(0)$ for all small $\tau > 0$, and halving reaches such a $\tau$. $\square$

The code also stops the halving when $\alpha < 10^{-12}$, as a guard against rounding. Then it accepts the point even if $B$ rose, but by Theorem 6 that point is still in $\mathcal A$. The test records $B$ at every iteration of 30 steps of a box drop and finds no increase. Lemma 7 says that $B$ decreases; it does not prove that the iterates converge to a stationary point, since the simple decrease test is weaker than an Armijo condition.

## Stationary points

**Theorem 8 (contact forces).** If the loop stops with $\mathbf p = 0$ at $\mathbf x^{n+1}$, then on the free vertices

$$M\frac{\mathbf x^{n+1} - \hat{\mathbf x}}{\Delta t^2} = -\nabla\Psi(\mathbf x^{n+1}) + \sum_{i,k}\lambda_{ik}\nabla d_{ik}, \qquad \lambda_{ik} = -\frac{\kappa}{\Delta t^2}b'(d_{ik}) \ge 0,$$

and $\lambda_{ik} > 0$ only when $d_{ik} < \hat d$. This is the backward Euler equation with contact forces along the distance gradients (equations (8) and (9) of the paper).

*Proof.* By Lemma 4, $\nabla B = 0$. Write out $\nabla B = M(\mathbf x - \hat{\mathbf x}) + \Delta t^2\nabla\Psi + \kappa\sum b'(d_{ik})\nabla d_{ik}$ and divide by $\Delta t^2$. The sign and support of $\lambda_{ik}$ follow from Lemma 1. $\square$

The forces are compressive and vanish beyond $\hat d$, and the gap of an active contact is positive, so this is a relaxed form of the complementarity conditions $\lambda \ge 0$, $d \ge 0$, $\lambda d = 0$, with the product small when $\hat d$ is small. For a body at rest on flat ground the sum of the $\lambda_{ik}$ equals the weight, $\sum m_i g$; the test checks this to $10^{-4}$ N.

**Corollary 9 (no contact is backward Euler).** If no pair is within $\hat d$ along the whole solve, the step is a Newton solve of the variational backward Euler step. For one spring along its axis, with one end pinned and no gravity, one Newton step reaches the closed form $x = (m y + \Delta t^2 k r)/(m + \Delta t^2 k)$; for free fall, one step gives $\mathbf x^{n+1} = \hat{\mathbf x}$, the symplectic Euler update.

*Proof.* Without active pairs the barrier terms are zero. For the spring along its axis, with the vertex at $y > r$, the energy restricted to the axis is the quadratic $\frac m2(x - y)^2 + \frac{\Delta t^2k}{2}(x - r)^2$, and the gradient across the axis is zero, so the Newton step is exact. For free fall $B = \frac12|\mathbf x - \hat{\mathbf x}|^2_M$ and the step from any point lands on $\hat{\mathbf x}$. With $\mathbf v^{n+1} = (\mathbf x^{n+1} - \mathbf x^n)/\Delta t$ this is $\mathbf v^{n+1} = \mathbf v^n + \Delta t\mathbf g$, $\mathbf x^{n+1} = \mathbf x^n + \Delta t\mathbf v^{n+1}$. $\square$

## Cost

**Lemma 10.** With $n$ free vertices, $s$ springs and $c$ segments, one Newton iteration of the code costs $O(n^3 + s + nc)$ time and $\Theta(n^2 + s + c)$ memory, plus $O(s + nc)$ for each halving of the line search.

*Proof.* The assembly visits every spring and every vertex and segment pair once, with $O(1)$ work each. The dense LU solve of the $2n \times 2n$ system costs $O(n^3)$ and stores $\Theta(n^2)$ numbers. The step bound visits every vertex and segment pair once. One evaluation of $B$ costs $O(n + s + nc)$. $\square$

The paper uses a sparse solver and a spatial culling of the pairs (Section 4.6), which replace the $n^3$ and $nc$ terms in practice.
