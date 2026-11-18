---
title: The condition forces are exact gradients, modified-pcg is preconditioned CG on the free directions, and the step keeps momentum up to the residual
proves: [correctness]
status: full
---

We use the notation of the page.
The state has $n$ particles in 3D. A condition $C(\mathbf x)$ with stiffness $k$ has the energy $E_C = \frac k2 C^2$ (Baraff and Witkin 1998, Section 4.1).
$\mathbf x$, $\mathbf v$ and the other state vectors have $3n$ entries, in blocks of 3 per particle.

## Forces and Jacobians

**Lemma 1 (equations (7) and (8)).** $\mathbf f_i = -\partial E_C / \partial \mathbf x_i = -k\, C\, \partial C/\partial \mathbf x_i$, and $K_{ij} = \partial \mathbf f_i / \partial \mathbf x_j = -k \big( \frac{\partial C}{\partial \mathbf x_i} \frac{\partial C}{\partial \mathbf x_j}^{\!\top} + \frac{\partial^2 C}{\partial \mathbf x_i \partial \mathbf x_j} C \big)$. The matrix $K$ is symmetric.

*Proof.* The chain rule for $\frac k2 C^2$ gives the force, and the product rule gives $K$. Both terms of $K_{ij}$ change into those of $K_{ji}^\top$ when $i$ and $j$ change places, because second derivatives commute. $\square$

**The stretch condition.** For a triangle with vertices $\mathbf x_0, \mathbf x_1, \mathbf x_2$ and rest coordinates $(u_i, v_i)$, equation (9) of the paper is $(\mathbf w_u\ \mathbf w_v) = (\Delta \mathbf x_1\ \Delta \mathbf x_2) D^{-1}$ with $D = \begin{pmatrix} \Delta u_1 & \Delta u_2 \\ \Delta v_1 & \Delta v_2 \end{pmatrix}$. With $\det D = \Delta u_1 \Delta v_2 - \Delta u_2 \Delta v_1$, this is
$\mathbf w_u = \sum_i c^u_i \mathbf x_i$ and $\mathbf w_v = \sum_i c^v_i \mathbf x_i$, with $c^u_1 = \Delta v_2/\det D$, $c^u_2 = -\Delta v_1/\det D$, $c^v_1 = -\Delta u_2/\det D$, $c^v_2 = \Delta u_1/\det D$ and $c_0 = -c_1 - c_2$ for both.
The coefficients do not depend on $\mathbf x$, so $\partial \mathbf w_u / \partial \mathbf x_i = c^u_i I$.
For $C_u = a(|\mathbf w_u| - b_u)$, with $\hat{\mathbf w} = \mathbf w_u / |\mathbf w_u|$,

$$\frac{\partial C_u}{\partial \mathbf x_i} = a\, c^u_i\, \hat{\mathbf w}, \qquad \frac{\partial^2 C_u}{\partial \mathbf x_i \partial \mathbf x_j} = \frac{a\, c^u_i c^u_j}{|\mathbf w_u|} \big(I - \hat{\mathbf w} \hat{\mathbf w}^\top\big),$$

because the derivative of $\mathbf w \mapsto \mathbf w/|\mathbf w|$ is $(I - \hat{\mathbf w}\hat{\mathbf w}^\top)/|\mathbf w|$. The same holds for $C_v$ with $c^v$.

**The shear condition.** For $C = a\, \mathbf w_u \cdot \mathbf w_v$ (Section 4.3), $\partial C / \partial \mathbf x_i = a (c^u_i \mathbf w_v + c^v_i \mathbf w_u)$ and $\partial^2 C / \partial \mathbf x_i \partial \mathbf x_j = a (c^u_i c^v_j + c^v_i c^u_j) I$.

**The bend condition.** $C = \theta$, the signed angle of the code. Its gradient is the formula of Bridson, Marino and Fedkiw; this note does not prove it, and the tests check it against central differences at ten random configurations. The code uses only the term $-k \frac{\partial C}{\partial \mathbf x_i}\frac{\partial C}{\partial \mathbf x_j}^{\!\top}$ of the bend Jacobian. The dropped term has the factor $C = \theta$, so it is zero at every configuration with $\theta = 0$, and the Jacobian is exact there.

**Lemma 2 (invariance).** Every condition of the page has $\sum_i \partial C/\partial \mathbf x_i = 0$ and $\sum_i \partial^2 C / \partial \mathbf x_i \partial \mathbf x_j = 0$ for each $j$. Hence the internal forces sum to zero and every block column of $K$ and of the damping Jacobians sums to zero. Every condition is zero at the rest state ($\mathbf x_i = (u_i, -v_i, 0)$, $b_u = b_v = 1$) and keeps its value under a rigid motion, so all internal forces are zero there.

*Proof.* A translation of all particles by $\mathbf t$ does not change $\mathbf w_u$, $\mathbf w_v$ (the coefficients sum to zero) or $\theta$. So $C(\mathbf x + \mathbf 1 \otimes \mathbf t) = C(\mathbf x)$ for all $\mathbf t$, and the derivative in $\mathbf t$ is $\sum_i \partial C / \partial \mathbf x_i = 0$. Differentiating this identity in $\mathbf x_j$ gives the second claim. A rotation $R$ maps $\mathbf w_u, \mathbf w_v$ to $R\mathbf w_u, R \mathbf w_v$ and keeps lengths, dot products and the angle between normals. At rest, $\mathbf w_u = (1, 0, 0)$ and $\mathbf w_v = (0, -1, 0)$, so the stretch and shear conditions are zero, and the sheet is flat, so $\theta = 0$. Each force is a multiple of $C$ or of $\dot C$, and $\dot C = 0$ when $\mathbf v = 0$. $\square$

## Damping

**Lemma 3.** For $\mathbf d_i = -k_d\, \dot C\, \partial C / \partial \mathbf x_i$ with $\dot C = \sum_j \frac{\partial C}{\partial \mathbf x_j} \cdot \mathbf v_j$ (equation (11)):
(a) $\partial \mathbf d_i / \partial \mathbf v_j = -k_d \frac{\partial C}{\partial \mathbf x_i} \frac{\partial C}{\partial \mathbf x_j}^{\!\top}$, which is symmetric;
(b) $\partial \mathbf d_i / \partial \mathbf x_j = -k_d \big( \frac{\partial C}{\partial \mathbf x_i} \frac{\partial \dot C}{\partial \mathbf x_j}^{\!\top} + \frac{\partial^2 C}{\partial \mathbf x_i \partial \mathbf x_j} \dot C \big)$ (equation (12)), and the code keeps only the second term, as the paper does;
(c) $\sum_i \mathbf d_i \cdot \mathbf v_i = -k_d \dot C^2 \le 0$.

*Proof.* $\dot C$ is linear in $\mathbf v$ with the gradient $\partial C / \partial \mathbf x_j$, which gives (a). The product rule gives (b). For (c), $\sum_i \mathbf d_i \cdot \mathbf v_i = -k_d \dot C \sum_i \frac{\partial C}{\partial \mathbf x_i} \cdot \mathbf v_i = -k_d \dot C^2$. $\square$

The term that the code drops makes $\partial \mathbf d / \partial \mathbf x$ asymmetric. Without it the matrix $A$ below is symmetric. The paper calls the omission "not physically justifiable" and reports no ill effects; this is a model choice, not a theorem. The test checks that the code's $\partial \mathbf d / \partial \mathbf x$ plus the dropped term equals central differences of $\mathbf d$.

## The linear system

Linearize $\mathbf f(\mathbf x_0 + \Delta \mathbf x, \mathbf v_0 + \Delta \mathbf v)$ at $(\mathbf x_0, \mathbf v_0)$ and put $\Delta \mathbf x = h(\mathbf v_0 + \Delta \mathbf v)$ into backward Euler $M \Delta \mathbf v = h \mathbf f(\mathbf x_1, \mathbf v_1)$. This gives equation (15):

$$A\, \Delta \mathbf v = \mathbf b, \qquad A = M - h \frac{\partial \mathbf f}{\partial \mathbf v} - h^2 \frac{\partial \mathbf f}{\partial \mathbf x}, \qquad \mathbf b = h\Big(\mathbf f_0 + h \frac{\partial \mathbf f}{\partial \mathbf x} \mathbf v_0\Big).$$

By Lemmas 1 and 3, $A$ is symmetric. The paper calls $A$ positive definite. That holds when $-\partial \mathbf f / \partial \mathbf x$ is positive semidefinite, for example near the rest state, but a compressed stretch condition or a sheared triangle adds terms $-k\, \partial^2 C\, C$ of either sign, and a large $h$ can then make $A$ indefinite. This note assumes that $A$ is positive definite, as the paper does (model assumption).

## modified-pcg

Let $S_i$ be the filter of particle $i$ (equation (13)): $I$, $I - \mathbf p \mathbf p^\top$, $I - \mathbf p \mathbf p^\top - \mathbf q \mathbf q^\top$ with orthonormal $\mathbf p, \mathbf q$, or $0$. Each $S_i$ is an orthogonal projection. Let $W$ be the block diagonal matrix of the $S_i$, so $\text{filter}(\mathbf a) = W \mathbf a$. Choose a matrix $B$ with orthonormal columns that span the range of $W$; then $W = B B^\top$ and $B^\top B = I$. The value $z_i$ lies in the range of $I - S_i$, so $W \mathbf z = 0$.

The code applies one diagonal matrix $Q$, with $Q_{ii} = 1/A_{ii}$ for each of the $3n$ components, wherever the paper writes $P$ or $P^{-1}$. The paper defines $P_{ii} = 1/A_{ii}$, uses $P$ in $\delta_0$ and $P^{-1}$ in the products $P^{-1}\mathbf r$; read literally, $\delta_0$ and $\delta_{\text{new}}$ would then be in different norms. Using $Q$ in all three places is the standard preconditioned conjugate gradient method with the preconditioner $\text{diag}(A)$. The value $\delta_0$ only sets the scale of the stopping test, so this choice does not change the iterates.

**Theorem 4.** Let $\hat A = B^\top A B$, $\hat{\mathbf b} = B^\top (\mathbf b - A \mathbf z)$ and $\hat Q = B^\top Q B$. If $A$ is symmetric positive definite, then $\hat A$ and $\hat Q$ are symmetric positive definite, and the iterates of modified-pcg are
$\Delta \mathbf v_k = \mathbf z + B \boldsymbol\alpha_k$, $\mathbf r_k = B \boldsymbol\rho_k$ and $\mathbf c_k = B \boldsymbol\gamma_k$, where $\boldsymbol\alpha_k$, $\boldsymbol\rho_k$ and $\boldsymbol\gamma_k$ are the iterates of the standard preconditioned conjugate gradient method for $\hat A \boldsymbol\alpha = \hat{\mathbf b}$ with the preconditioner $\hat Q$, started at $\boldsymbol\alpha_0 = 0$. The scalars $\delta$ and $\alpha$ of the two methods are equal.

*Proof.* $\hat A$ is symmetric, and for $\boldsymbol\alpha \ne 0$, $B \boldsymbol\alpha \ne 0$, so $\boldsymbol\alpha^\top \hat A \boldsymbol\alpha = (B\boldsymbol\alpha)^\top A (B\boldsymbol\alpha) > 0$. The same argument works for $\hat Q$, since $Q$ is diagonal with positive entries ($A_{ii} > 0$ for a positive definite $A$).
Induction on $k$. At the start (lines L3 to L5), $\Delta \mathbf v_0 = \mathbf z$, $\mathbf r_0 = W(\mathbf b - A \mathbf z) = B \hat{\mathbf b}$, so $\boldsymbol\rho_0 = \hat{\mathbf b} - \hat A \cdot 0$. Then $\mathbf c_0 = W Q \mathbf r_0 = B (B^\top Q B) \boldsymbol\rho_0 = B \hat Q \boldsymbol\rho_0$, and $\delta_{\text{new}} = \mathbf r_0^\top \mathbf c_0 = \boldsymbol\rho_0^\top \hat Q \boldsymbol\rho_0$, using $B^\top B = I$.
At an iteration (lines L7 to L10), $\mathbf q = W A \mathbf c = B (B^\top A B) \boldsymbol\gamma = B \hat A \boldsymbol\gamma$, and $\mathbf c^\top \mathbf q = \boldsymbol\gamma^\top \hat A \boldsymbol\gamma$, so $\alpha$ is the same. The updates of $\Delta \mathbf v$ and $\mathbf r$ are the images under $B$ of the updates of $\boldsymbol\alpha$ and $\boldsymbol\rho$. The vector $\mathbf s = Q \mathbf r$ is not filtered, but it enters only through $\mathbf r^\top \mathbf s = \boldsymbol\rho^\top \hat Q \boldsymbol\rho$ and through $\mathbf c = W(\mathbf s + \beta \mathbf c) = B(\hat Q \boldsymbol\rho + \beta \boldsymbol\gamma)$. These are the formulas of the standard method. $\square$

**Corollary 5.** (a) After any number of iterations, $(I - S_i) \Delta \mathbf v_i = \mathbf z_i$ for every constrained particle. (b) In exact arithmetic, the method stops after at most $\dim(\text{range } W)$ iterations with the unique solution of $W(A \Delta \mathbf v - \mathbf b) = 0$ with $(I - W)\Delta \mathbf v = \mathbf z$, which is equation (14) of the paper.
(c) Without constraints this is the standard preconditioned conjugate gradient method for $A \Delta \mathbf v = \mathbf b$.

*Proof.* (a) $(I - W)(\mathbf z + B\boldsymbol\alpha) = \mathbf z$, because $W\mathbf z = 0$ and $W B = B$. (b) The standard method on an SPD system of dimension $m$ reaches the exact solution in at most $m$ steps, and $\hat A \boldsymbol\alpha = \hat{\mathbf b}$ is $B^\top (A\Delta \mathbf v - \mathbf b) = 0$, which is $W(A \Delta \mathbf v - \mathbf b) = 0$. (c) Take $W = I$, $B = I$ and $\mathbf z = 0$. $\square$

The tests check (a) after 0, 1, 2 and 5 iterations, and the final $\Delta \mathbf v$ against a dense solve of the reduced system $\hat A \boldsymbol\alpha = \hat{\mathbf b}$, with two pinned particles and two particles on planes.

## Momentum

**Theorem 6.** With no constraints, $\sum_i m_i \Delta \mathbf v_i - h \sum_i \mathbf f_{\text{ext}, i} = \sum_i (A \Delta \mathbf v - \mathbf b)_i$, the sum of the blocks of the residual. So the exact solve changes the linear momentum by $h \sum \mathbf f_{\text{ext}}$ exactly, and an inexact solve is off by the sum of its residual blocks.

*Proof.* By Lemma 2, every block column of $\partial \mathbf f / \partial \mathbf x$ and $\partial \mathbf f / \partial \mathbf v$ sums to zero, so $\sum_i (A \Delta \mathbf v)_i = \sum_i m_i \Delta \mathbf v_i$. Also by Lemma 2, $\sum_i (\mathbf f_0)_i = \sum_i \mathbf f_{\text{ext}, i}$ and $\sum_i \big(\frac{\partial \mathbf f}{\partial \mathbf x} \mathbf v_0\big)_i = 0$, so $\sum_i \mathbf b_i = h \sum_i \mathbf f_{\text{ext}, i}$. Subtract. $\square$

The test runs five steps with the tolerance $\varepsilon = 10^{-14}$ and checks the momentum to $10^{-10}$ relative.

## Stable is not accurate

For a linear force $\mathbf f = -K\mathbf x$, the linearization is exact, and one step is backward Euler. For one mass on one spring, the energy is then multiplied by $1/(1 + \omega^2 h^2)$ at each step (the same computation as in the proof of the fast mass-spring page). So the step damps stiff motion strongly. For the nonlinear conditions of cloth, the page claims no stability theorem: the step is one Newton iteration of backward Euler, and the bounded run at a large step is a measurement.
