---
title: The affine map gives a constant mass matrix, the orthogonality energy vanishes exactly on orthogonal maps, the projected Newton step is a descent step, and a convex body never crosses a line
proves: [correctness]
status: full
---

We use the notation of the page for the 2D code. The body has vertices with rest coordinates $\bar{\mathbf x}_v$ and masses $m_v > 0$. The state is $\mathbf q = (\mathbf p, A)$ with $\mathbf p \in \mathbb R^2$ and $A \in \mathbb R^{2 \times 2}$ stored row by row, so $\mathbf q \in \mathbb R^6$. The world position of a vertex is

$$\mathbf x_v = A\bar{\mathbf x}_v + \mathbf p = J_v\mathbf q, \qquad J_v = \begin{pmatrix} 1 & 0 & \bar x_{v,1} & \bar x_{v,2} & 0 & 0 \\ 0 & 1 & 0 & 0 & \bar x_{v,1} & \bar x_{v,2}\end{pmatrix}.$$

The mass matrix is $M = \sum_v m_v J_v^T J_v$, the orthogonality energy is $V(A) = k\,\|AA^T - I\|_F^2$ with $k = \kappa_o \cdot \text{area} > 0$, and the obstacles are half planes $\{\mathbf x : \mathbf n_\ell\cdot\mathbf x \ge h_\ell\}$ with $|\mathbf n_\ell| = 1$. The gap of vertex $v$ to line $\ell$ is $d_{v\ell}(\mathbf q) = \mathbf n_\ell\cdot J_v\mathbf q - h_\ell$. With $\tilde{\mathbf q} = \mathbf q^n + \Delta t\dot{\mathbf q}^n + \Delta t^2 M^{-1}\mathbf f$, $\mathbf f = \sum_v m_v J_v^T\mathbf g$, one step minimizes

$$E(\mathbf q) = \tfrac12(\mathbf q - \tilde{\mathbf q})^T M(\mathbf q - \tilde{\mathbf q}) + \Delta t^2 V(A) + \kappa\sum_{v,\ell} b(d_{v\ell}(\mathbf q)),$$

with the barrier $b(d) = -(d - \hat d)^2\ln(d/\hat d)$ for $0 < d < \hat d$ and $b(d) = 0$ for $d \ge \hat d$ of incremental potential contact (Lemma 1 of the proof on that page): $C^2$ on $(0, \infty)$, zero for $d \ge \hat d$, with $b' < 0 < b''$ on $(0, \hat d)$ and $b \to \infty$ as $d \to 0^+$. All statements are for exact arithmetic.

## The affine model

**Lemma 1 (kinetic energy and mass).** For every $\dot{\mathbf q}$, $\frac12\dot{\mathbf q}^T M\dot{\mathbf q} = \sum_v \frac12 m_v|J_v\dot{\mathbf q}|^2$, the kinetic energy of the vertices, and $M$ does not depend on $\mathbf q$. If $\sum_v m_v\bar{\mathbf x}_v = 0$, then $M = \begin{pmatrix} m_{\text{tot}} I & 0 \\ 0 & M_A\end{pmatrix}$ with $m_{\text{tot}} = \sum_v m_v$. If three of the $\bar{\mathbf x}_v$ are not on one line, $M$ is positive definite.

*Proof.* The velocity of a vertex is $\dot{\mathbf x}_v = J_v\dot{\mathbf q}$ because $J_v$ is constant, so $\sum_v \frac12 m_v|J_v\dot{\mathbf q}|^2 = \frac12\dot{\mathbf q}^T(\sum_v m_v J_v^TJ_v)\dot{\mathbf q}$. The block of $M$ that couples $\mathbf p$ with the entries of $A$ is $\sum_v m_v\bar x_{v,c}$ in the matching places, which is zero when the weighted mean of the rest coordinates is zero. If $\mathbf q^TM\mathbf q = 0$, then $A\bar{\mathbf x}_v + \mathbf p = 0$ for every $v$; three points that are not on one line span the plane affinely, so the affine map $\mathbf x \mapsto A\mathbf x + \mathbf p$ is zero, and $A = 0$, $\mathbf p = 0$. $\square$

This is the 2D form of equations (1) to (4) of the paper: the mass matrix is constant, so there are no Coriolis or centrifugal terms, and the equation of motion is $M\ddot{\mathbf q} = -\nabla V + \mathbf f$ (equation (5)). The code places $\bar{\mathbf x}_v$ on the border of a rectangle centered at its center of mass, with equal masses, so both conditions hold.

## The orthogonality energy

**Lemma 2.** Let $C = AA^T - I$. Then $V \ge 0$, and $V = 0$ exactly when $A$ is orthogonal, that is, a rotation or a reflection. The gradient is $\nabla_A V = 4kCA$, which is zero on orthogonal matrices, and the Hessian acts on a direction $D$ as $\nabla^2 V[D] = 4k\big((DA^T + AD^T)A + CD\big)$.

*Proof.* $V = k\sum_{ij}C_{ij}^2$ is zero exactly when $C = 0$. With $dC = DA^T + AD^T$ and $C$ symmetric, $dV = 2k\operatorname{tr}(C\,dC) = 2k\operatorname{tr}(CDA^T + CAD^T) = 4k\operatorname{tr}((CA)^TD)$, using $\operatorname{tr}(CDA^T) = \operatorname{tr}(A^TCD) = \operatorname{tr}((CA)^TD)$. So $\nabla V = 4kCA$. Differentiating $4kCA$ in the direction $D$ gives $4k(dC\,A + C\,D)$. $\square$

$V$ is not convex: at $A = sI$ with $s^2 < 1/3$ the Hessian has a negative eigenvalue (the test checks $s = 0.3$). The paper uses the same energy with $\kappa_o$ above 100 GPa and reports that it is cheaper than ARAP and neo-Hookean energies (Section 3.2).

**Lemma 3 (projection).** `project_psd` returns $\sum_k \max(\lambda_k, 0)\mathbf v_k\mathbf v_k^T$ for the eigenpairs of the $4 \times 4$ Hessian of $V$. This matrix is positive semidefinite, and it equals the Hessian when the Hessian is positive semidefinite.

*Proof.* The cyclic Jacobi method applies plane rotations that zero one off diagonal entry at a time; the sum of the squares of the off diagonal entries decreases strictly with each nontrivial rotation and tends to zero, and the product of the rotations is an orthogonal $V$ with $V^THV$ diagonal in the limit. The code stops when the off diagonal part is below a relative $10^{-30}$, which the test confirms by rebuilding $H$ from the eigenpairs to $10^{-10}$. Clamping the eigenvalues gives a sum of positive semidefinite rank one matrices, and if no eigenvalue is negative nothing changes. $\square$

## Contact

**Lemma 4.** Each gap $d_{v\ell}$ is affine in $\mathbf q$, with constant gradient $J_v^T\mathbf n_\ell$ and zero Hessian. So the barrier Hessian $\kappa b''(d)\,J_v^T\mathbf n_\ell\mathbf n_\ell^TJ_v$ is positive semidefinite with no projection, and along a straight path $\mathbf q + t\mathbf p$ each gap is $d_{v\ell} + t\,\mathbf n_\ell\cdot J_v\mathbf p$, linear in $t$.

*Proof.* $J_v$ is constant, so $\mathbf n_\ell\cdot J_v\mathbf q - h_\ell$ is affine. The chain rule gives $\nabla^2 b(d) = b''\nabla d\nabla d^T + b'\nabla^2 d = b''\nabla d\nabla d^T$, and $b'' \ge 0$. $\square$

This linearity is why the paper can run continuous collision checks on straight vertex paths (Section 4.1): a straight path in $\mathbf q$ moves every point of the body on a straight line.

**Theorem 5 (no crossing).** Suppose every gap is positive at $\mathbf q$ and let $\alpha$ be the value of `step_bound`. Then every gap is positive at $\mathbf q + \tau\mathbf p$ for $\tau \in [0, \alpha]$. If the rest shape is the convex hull of the $\bar{\mathbf x}_v$, as for the rectangle of the code, then the whole body stays strictly inside every half plane, at every iterate and on the path between iterates.

*Proof.* By Lemma 4 the gap of $(v, \ell)$ is $d + t r$ with $d > 0$ and $r = \mathbf n_\ell\cdot J_v\mathbf p$. If $r \ge 0$ it stays positive for all $t \ge 0$. If $r < 0$ it reaches zero at $t^* = d/(-r)$; the code sets $\alpha \le 0.8\,t^*$ when $0.8\,t^* < 1$, and otherwise $\alpha \le 1 < t^*$. So $\alpha < t^*$ in every case, and the gap is positive on $[0, \alpha]$. For the second claim, the affine map of a convex hull is the convex hull of the images of the vertices, and a half plane that contains all vertex images strictly contains their convex hull. The line search only shrinks the step. $\square$

The theorem covers contact against fixed lines. The paper treats contact between bodies with point and triangle and edge and edge pairs, where the same linearity of the vertex paths holds; the code does not.

## The Newton iteration

**Lemma 6 (descent).** The matrix $H = M + \Delta t^2 P + \sum\kappa b''\nabla d\nabla d^T$ of the code, with $P$ the projected Hessian of $V$ placed in the $A$ block, is positive definite, so $\mathbf p = -H^{-1}\nabla E$ satisfies $\nabla E^T\mathbf p < 0$ whenever $\nabla E \ne 0$, and $\mathbf p = 0$ only if $\nabla E = 0$.

*Proof.* $M$ is positive definite by Lemma 1, and the other terms are positive semidefinite by Lemmas 3 and 4. Then $\nabla E^T\mathbf p = -\nabla E^TH^{-1}\nabla E < 0$. $\square$

**Lemma 7 (monotone).** If $\nabla E(\mathbf z) \ne 0$, the halving loop ends after finitely many halvings with $E(\mathbf z + \alpha\mathbf p) \le E(\mathbf z)$.

*Proof.* By Theorem 5, $\phi(\tau) = E(\mathbf z + \tau\mathbf p)$ is finite and $C^1$ on $[0, \alpha_0]$, and $\phi'(0) < 0$ by Lemma 6. So $\phi < \phi(0)$ on some interval $(0, \tau_0)$, and halving reaches it. $\square$

As in incremental potential contact, the guard $\alpha < 10^{-12}$ accepts a point without decrease only to stop rounding loops, and the decrease test does not prove that the iterates converge to a minimizer. The test checks by sampling 300 nearby states that the result of a converged step is a local minimum.

## Momentum and free fall

**Theorem 8 (linear momentum).** Let $\sum_v m_v\bar{\mathbf x}_v = 0$ and let no gap be below $\hat d$. At a stationary point of $E$, $\mathbf p^{n+1} = \tilde{\mathbf p}$, so the linear momentum $\mathbf P = \sum_v m_v\dot{\mathbf x}_v = m_{\text{tot}}\dot{\mathbf p}$ satisfies $\mathbf P^{n+1} = \mathbf P^n + \Delta t\,m_{\text{tot}}\mathbf g$.

*Proof.* Since $J_v\dot{\mathbf q} = \dot A\bar{\mathbf x}_v + \dot{\mathbf p}$, $\mathbf P = \dot A\sum_v m_v\bar{\mathbf x}_v + m_{\text{tot}}\dot{\mathbf p} = m_{\text{tot}}\dot{\mathbf p}$. With the block form of $M$, $\nabla_{\mathbf p}E = m_{\text{tot}}(\mathbf p - \tilde{\mathbf p})$, since $V$ does not depend on $\mathbf p$ and no barrier is active. So $\mathbf p^{n+1} = \tilde{\mathbf p} = \mathbf p^n + \Delta t\dot{\mathbf p}^n + \Delta t^2\mathbf g$, where $M^{-1}\mathbf f = (\mathbf g, 0)$ by the block form. Then $\dot{\mathbf p}^{n+1} = (\mathbf p^{n+1} - \mathbf p^n)/\Delta t = \dot{\mathbf p}^n + \Delta t\mathbf g$. $\square$

**Corollary 9 (free fall).** A body at rest with $A = I$ and no contact falls as symplectic Euler: $\mathbf p$ after 10 steps of $0.1$ s with $\mathbf g = (0, -9.81)$ is $(0, -5.3955)$.

*Proof.* $A = I$ stays a minimizer of the $A$ part ($\tilde A = I$ and $\nabla V(I) = 0$), and Theorem 8 gives the update of $\mathbf p$. Summing $y_n = -0.0981\,n(n+1)/2$ for $n = 10$ gives $-5.3955$. $\square$

Angular momentum is not kept: the backward Euler step damps rotation. The page measures this; the damping shrinks as $\Delta t$ goes to zero, at first order.

**Theorem 10 (contact forces).** At a stationary point, $M(\mathbf q - \tilde{\mathbf q})/\Delta t^2 = -\nabla V + \sum_{v,\ell}\lambda_{v\ell}J_v^T\mathbf n_\ell$ with $\lambda_{v\ell} = -\kappa b'(d_{v\ell})/\Delta t^2 \ge 0$, nonzero only for $d_{v\ell} < \hat d$. For a body at rest on one line with normal $(0, 1)$, the $\mathbf p$ rows give $\sum_v\lambda_{v\ell} = m_{\text{tot}}|\mathbf g|$.

*Proof.* Set $\nabla E = 0$ and divide by $\Delta t^2$. At rest, $\mathbf q = \mathbf q^n$ and $\dot{\mathbf q}^n = 0$, so $\mathbf q - \tilde{\mathbf q} = -\Delta t^2M^{-1}\mathbf f$ and the left side is $-\mathbf f$. The $\mathbf p$ rows of $J_v^T\mathbf n_\ell$ are $\mathbf n_\ell$, and $\nabla V$ has no $\mathbf p$ rows, so $-m_{\text{tot}}\mathbf g = \sum\lambda_{v\ell}(0, 1)$. $\square$

## Cost

**Lemma 11.** With $V_b$ vertices and $L$ lines, one Newton iteration costs $O(V_b L)$ for the assembly and the step bound, plus a constant for the $4 \times 4$ eigen decomposition and the $6 \times 6$ solve. Each halving costs $O(V_b L)$. The memory is $\Theta(V_b + L)$.

*Proof.* Each vertex and line pair adds $O(1)$ work with $6 \times 6$ matrices. The Jacobi method on a fixed $4 \times 4$ matrix with a fixed sweep limit and the LU solve of a $6 \times 6$ matrix take constant time. $\square$

In 3D the state has 12 numbers, the eigen problem is $9 \times 9$ and the solve is $12 \times 12$ per body. With many bodies the Hessian is block diagonal except for the contact pairs between bodies, which is what the paper exploits (Section 4.3).
