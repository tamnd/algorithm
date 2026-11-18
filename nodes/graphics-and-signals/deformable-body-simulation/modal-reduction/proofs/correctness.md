---
title: The modal basis diagonalizes the linear system, the modal steps equal the full steps, and a truncated basis keeps its modes exactly
proves: [correctness]
status: full
---

The code works on a triangle mesh in the plane with linear elasticity, Lamé parameters $\mu > 0$ and $\lambda > 0$, and a lumped mass matrix $M = \operatorname{diag}(m_1, \ldots, m_n)$ with every $m_i > 0$.
$K$ is the stiffness matrix after the fixed degrees of freedom are removed.
All claims are about exact arithmetic, except Step 2, which also bounds the error of the eigensolver.

## Step 1: $K$ is the Hessian of the linear energy

For one triangle with rest edge matrix $D_m$ and area $A$, the code forms $H = D_sD_m^{-1}$ from the vertex displacements, $P = \mu(H + H^T) + \lambda(\operatorname{tr}H)I$, and the forces as the columns of $-AP D_m^{-T}$, with vertex 0 getting minus their sum.
$P$ is the gradient of $\psi(H) = \mu\lvert\operatorname{sym}H\rvert^2 + \frac\lambda2(\operatorname{tr}H)^2$, so these forces are $-\partial(A\psi)/\partial u$, by the same chain rule as for every energy density of $F$.
The forces are linear in $u$, so the column of the element force for a unit displacement $e_b$ is $-K_e e_b$, and the code stores $K_e$ column by column.
The sum over triangles gives $K$ with $\frac12u^TKu = \sum A\psi$, so $K$ is symmetric.
$\psi \ge 0$ for $\mu > 0$ and $\lambda > 0$, so $K$ is positive semidefinite, and removing degrees of freedom takes a principal submatrix, which keeps both properties. $\square$

## Step 2: the generalized eigenpairs

Let $S = M^{-1/2}$ and $L = SKS$, which is symmetric.
Each Jacobi rotation $G$ replaces $L$ by $G^TLG$ and $V$ by $VG$, so after the loop $V$ is orthogonal and $L' = V^TLV$.
Let $D$ be the diagonal of $L'$ and $\delta$ the Frobenius norm of its off-diagonal part, which the stop test bounds.
Then $LV - VD = V(L' - D)$, whose norm is $\delta$, so each column $y_k$ of $V$ satisfies $\lvert Ly_k - D_{kk}y_k\rvert \le \delta$.
For $\phi_k = Sy_k$, $K\phi_k - D_{kk}M\phi_k = S^{-1}(Ly_k - D_{kk}y_k)$, so the pairs $(D_{kk}, \phi_k)$ solve $K\phi = \lambda M\phi$ up to this residual, and exactly when $\delta = 0$.
$\phi_j^TM\phi_k = y_j^Ty_k$, so the $\phi_k$ are $M$-orthonormal exactly, up to rounding, whatever $\delta$ is.
The cyclic Jacobi method makes $\delta$ go to zero (a known result), and the stop test checks it.
By Step 1, every eigenvalue is at least 0. $\square$

## Step 3: the full basis diagonalizes the system

Let $U$ be the square matrix with columns $\phi_1, \ldots, \phi_n$ and $\Omega^2 = \operatorname{diag}(\lambda_1, \ldots, \lambda_n)$.
By Step 2, $U^TMU = I$ and $KU = MU\Omega^2$, so $U^TKU = \Omega^2$.
$U$ is invertible with $U^{-1} = U^TM$, so $M^{-1} = UU^T$.
For $u = Uq$, the equation $M\ddot u = -Ku + f$ becomes $\ddot q = -\Omega^2q + U^Tf$: $n$ oscillators that do not interact. $\square$

## Step 4: the modal steps equal the full steps

The full code does $v \leftarrow v + hM^{-1}(f - Ku)$, then $u \leftarrow u + hv$.
Let $u = Uq$ and $v = Uw$, with $q_0 = U^TMu_0$ and $w_0 = U^TMv_0$, so that $Uq_0 = u_0$ and $Uw_0 = v_0$.
By Step 3, $M^{-1}(f - KUq) = UU^Tf - UU^TMU\Omega^2q = U(g - \Omega^2q)$ with $g = U^Tf$.
So the full velocity step is $U$ times the modal step $w_i \leftarrow w_i + h(g_i - \lambda_iq_i)$, and the position step is $U$ times $q_i \leftarrow q_i + hw_i$.
By induction on the number of steps, the full shape is $Uq$ after every step, which is what L6 returns. $\square$

## Step 5: a truncated basis keeps its modes exactly

The modal updates of Step 4 for mode $i$ use only $q_i$, $w_i$ and $g_i$.
So the code with the first $r$ modes computes the same $q_1, \ldots, q_r$ as the full basis, and these are $q_i = \phi_i^TMu$ of the full solution $u$.
The error $u - U_rq_r$ is $\sum_{i > r}q_i\phi_i$, the part of $u$ in the dropped modes.
For a static load, $q_i = g_i/\lambda_i$ for $\lambda_i > 0$, so the error in the norm $\lvert x\rvert_M = \sqrt{x^TMx}$ is $\bigl(\sum_{i > r}(g_i/\lambda_i)^2\bigr)^{1/2}$, which does not increase with $r$ and is zero for $r = n$. $\square$

## Step 6: the zero modes are the rigid motions

$\psi(H) = 0$ for $\mu > 0$ and $\lambda > 0$ exactly when $\operatorname{sym}H = 0$, so $Ku = 0$ exactly when $u$ on each triangle is $c + \omega Jx$ with $J$ the rotation by a right angle.
If two triangles share an edge with the distinct end points $x_1$, $x_2$, two such fields that agree at both points have $(\omega - \omega')J(x_1 - x_2) = 0$, so $\omega = \omega'$ and then $c = c'$.
The grid is connected through edges, so the null space of the full $K$ is the 3-dimensional space of the two translations and the field $(-y, x)$, and a free body has exactly 3 zero eigenvalues.
If two distinct nodes are fixed, a field $c + \omega Jx$ that is zero at both is zero, so $K$ is positive definite and every $\lambda_i > 0$. $\square$

## Step 7: the rotation mode at finite amplitude

The field $u = \theta(-y, x)$ gives $F = I + \theta J$ on every triangle.
$\det F = 1 + \theta^2$, so each triangle, and the mesh, has its area times $1 + \theta^2$.
$F^TF = (1 + \theta^2)I$, so the Green strain is $E = \frac{\theta^2}2I$, and the St. Venant-Kirchhoff energy density $\mu\lvert E\rvert^2 + \frac\lambda2(\operatorname{tr}E)^2$ is $(\mu + \lambda)\frac{\theta^4}2$.
So a mesh of area $A$ has the energy $A(\mu + \lambda)\theta^4/2$, while the linear energy $\frac12u^TKu$ is 0 by Step 6. $\blacksquare$
