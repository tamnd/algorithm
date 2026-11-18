---
title: The goals are the best rigid or linear fit of the rest shape, and the step keeps linear and angular momentum exactly
proves: [correctness]
status: full
---

We use the notation of the page, in 2D. A body has $n$ particles with masses $m_i > 0$, total mass $M = \sum m_i$, rest positions $\mathbf x^0_i$ and current positions $\mathbf x_i$. Let $\mathbf x_{cm}$ and $\mathbf x^0_{cm}$ be the centers of mass, $\mathbf q_i = \mathbf x^0_i - \mathbf x^0_{cm}$ and $\mathbf p_i = \mathbf x_i - \mathbf x_{cm}$, so $\sum m_i \mathbf q_i = \sum m_i \mathbf p_i = 0$. Let $A_{pq} = \sum m_i \mathbf p_i \mathbf q_i^T$ and $S_0 = \sum m_i \mathbf q_i \mathbf q_i^T$, which we assume invertible (the rest shape does not lie on a line). The goal positions are $\mathbf g_i = G \mathbf q_i + \mathbf x_{cm}$ for a $2 \times 2$ matrix $G$, and the step of lines L6 and L7 is

$$\mathbf v_i' = \mathbf v_i + \frac{\alpha}{\Delta t}(\mathbf g_i - \mathbf x_i) + \Delta t\, \frac{\mathbf f_i}{m_i}, \qquad \mathbf x_i' = \mathbf x_i + \Delta t\, \mathbf v_i' ,$$

equation (9) of Müller et al. (2005). The cross product of two vectors in the plane is the number $\mathbf a \times \mathbf b = a_x b_y - a_y b_x$.

## The goals are best fits

**Lemma 1 (rigid fit).** Among all rotations $R$ and translations $\mathbf t$, the sum $\sum m_i |R\mathbf q_i + \mathbf t - \mathbf x_i|^2$ is smallest for $\mathbf t = \mathbf x_{cm}$ and for the rotation $R(\theta)$ with $\theta = \operatorname{atan2}\big((A_{pq})_{10} - (A_{pq})_{01},\ (A_{pq})_{00} + (A_{pq})_{11}\big)$, which line L3 computes. The rotation is unique unless both arguments of atan2 are zero.

*Proof.* The sum is a convex quadratic in $\mathbf t$ with gradient $2\sum m_i(R\mathbf q_i + \mathbf t - \mathbf x_i) = 2M(\mathbf t - \mathbf x_{cm})$, because $\sum m_i \mathbf q_i = 0$. So $\mathbf t = \mathbf x_{cm}$ for every $R$. Then the sum is $\sum m_i |R\mathbf q_i - \mathbf p_i|^2 = \sum m_i |\mathbf q_i|^2 + \sum m_i |\mathbf p_i|^2 - 2\sum m_i \mathbf p_i \cdot R\mathbf q_i$, and $\sum m_i \mathbf p_i \cdot R\mathbf q_i = \operatorname{tr}(R^T A_{pq})$. For $R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$, $\operatorname{tr}(R^T A_{pq}) = \cos\theta\,(a_{00} + a_{11}) + \sin\theta\,(a_{10} - a_{01})$. This is $\rho\cos(\theta - \theta^*)$ with $\rho = |(a_{00} + a_{11}, a_{10} - a_{01})|$ and $\theta^*$ the angle of the formula, so it is largest exactly at $\theta^*$ when $\rho > 0$. $\square$

When $\det A_{pq} > 0$ this is the rotation factor $R$ of the polar decomposition $A_{pq} = RS$ with $S$ symmetric positive definite, the formula of Section 3.3 of the paper. When $\det A_{pq} < 0$ the paper's formula $A_{pq}(A_{pq}^T A_{pq})^{-1/2}$ would be a reflection, while the formula above is still the best rotation. In both cases $R^T A_{pq}$ is symmetric: with $c = \cos\theta^*$ and $s = \sin\theta^*$, $(R^T A_{pq})_{01} - (R^T A_{pq})_{10} = c\,a_{01} + s\,a_{11} - (c\,a_{10} - s\,a_{00}) = s(a_{00} + a_{11}) - c(a_{10} - a_{01}) = \rho(\sin\theta^*\cos\theta^* - \cos\theta^*\sin\theta^*) = 0$. We write $S = R^T A_{pq}$ for this symmetric matrix.

**Lemma 2 (linear fit).** The matrix $A = A_{pq} S_0^{-1}$ minimizes $\sum m_i |A\mathbf q_i - \mathbf p_i|^2$ over all $2 \times 2$ matrices. If $\mathbf x_i = F\mathbf x^0_i + \mathbf t$ for all $i$, then $A = F$.

*Proof.* The sum is a convex quadratic in $A$ with gradient $2\sum m_i (A\mathbf q_i - \mathbf p_i)\mathbf q_i^T = 2(A S_0 - A_{pq})$, which is zero exactly at $A = A_{pq} S_0^{-1}$. If $\mathbf x_i = F\mathbf x^0_i + \mathbf t$, then $\mathbf x_{cm} = F\mathbf x^0_{cm} + \mathbf t$, so $\mathbf p_i = F\mathbf q_i$, $A_{pq} = F S_0$ and $A = F$. $\square$

The volume preserving matrix of line L4 is $\tilde A = A/\sqrt{\det A}$ when $\det A > 0$, with $\det \tilde A = 1$ in 2D; the code uses $R$ when $\det A \le 0$. Line L4 uses $G = \beta\tilde A + (1 - \beta)R$ (Section 4.2 of the paper).

**Lemma 3 (no pull at a rigid pose).** If $\mathbf x_i = Q\mathbf x^0_i + \mathbf t$ for a rotation $Q$, then $\mathbf g_i = \mathbf x_i$ for all $i$, in the rigid mode and in the linear mode for every $\beta$.

*Proof.* Here $\mathbf p_i = Q\mathbf q_i$ and $A_{pq} = Q S_0$. For any rotation $R$, $\operatorname{tr}(R^T Q S_0) = \operatorname{tr}(U S_0)$ with the rotation $U = R^T Q$, and $\operatorname{tr}(U S_0) \le \operatorname{tr}(S_0)$ because $S_0$ is symmetric positive definite and the diagonal entries of $U$ in the eigenbasis of $S_0$ are at most 1. Equality holds for $U = I$, and by Lemma 1 the maximizer is unique since $\rho = \operatorname{tr} S_0 > 0$. So $R = Q$. By Lemma 2, $A = Q$, which has determinant 1, so $\tilde A = Q$ and $G = Q$ in every mode. Then $\mathbf g_i = Q\mathbf q_i + \mathbf x_{cm} = \mathbf p_i + \mathbf x_{cm} = \mathbf x_i$. $\square$

## Momentum

**Lemma 4.** For every $G$, $\sum m_i (\mathbf g_i - \mathbf x_i) = 0$.

*Proof.* $\sum m_i (G\mathbf q_i + \mathbf x_{cm} - \mathbf x_{cm} - \mathbf p_i) = G\sum m_i\mathbf q_i - \sum m_i \mathbf p_i = 0$. $\square$

**Lemma 5.** If $G A_{pq}^T$ is symmetric, then $\sum m_i \mathbf x_i \times (\mathbf g_i - \mathbf x_i) = 0$. This holds for $G = R$, $G = A$, $G = \tilde A$ and every $G = \beta\tilde A + (1 - \beta)R$.

*Proof.* Write $\mathbf x_i = \mathbf x_{cm} + \mathbf p_i$ and $\mathbf g_i - \mathbf x_i = G\mathbf q_i - \mathbf p_i$. Then the sum is $\mathbf x_{cm} \times \sum m_i (G\mathbf q_i - \mathbf p_i) + \sum m_i \mathbf p_i \times G\mathbf q_i - \sum m_i \mathbf p_i \times \mathbf p_i$. The first term is zero by Lemma 4 and the last term is zero. For the middle term, $\mathbf p \times G\mathbf q = (G\mathbf q\,\mathbf p^T)_{10} - (G\mathbf q\,\mathbf p^T)_{01}$, and $\sum m_i G\mathbf q_i \mathbf p_i^T = G A_{pq}^T$. So the middle term is the difference of the off-diagonal entries of $G A_{pq}^T$, which is zero when this matrix is symmetric. Now $R A_{pq}^T = R S^T R^T = R S R^T$ is symmetric because $S = R^T A_{pq}$ is (Lemma 1). $A A_{pq}^T = A_{pq} S_0^{-1} A_{pq}^T$ is symmetric because $S_0^{-1}$ is. $\tilde A$ is a multiple of $A$, and a combination of matrices with the property has it. $\square$

**Theorem 6.** With no external forces, one step keeps $\mathbf P = \sum m_i \mathbf v_i$ and $L = \sum m_i \mathbf x_i \times \mathbf v_i$ exactly, in the rigid and in the linear mode, for every $\alpha$ and $\Delta t$.

*Proof.* By Lemma 4, $\mathbf P' = \mathbf P + \frac{\alpha}{\Delta t}\sum m_i (\mathbf g_i - \mathbf x_i) = \mathbf P$. For $L$, $\mathbf x_i' \times \mathbf v_i' = (\mathbf x_i + \Delta t\mathbf v_i') \times \mathbf v_i' = \mathbf x_i \times \mathbf v_i'$, so $L' = \sum m_i \mathbf x_i \times \mathbf v_i + \frac{\alpha}{\Delta t}\sum m_i \mathbf x_i \times (\mathbf g_i - \mathbf x_i) = L$ by Lemma 5. $\square$

**Corollary 7.** Under uniform gravity, $\mathbf f_i = m_i\mathbf g$, the center of mass moves by symplectic Euler: $\mathbf v_{cm}' = \mathbf v_{cm} + \Delta t\,\mathbf g$ and $\mathbf x_{cm}' = \mathbf x_{cm} + \Delta t\,\mathbf v_{cm}'$.

*Proof.* Multiply the step by $m_i$, sum and divide by $M$; the goal terms cancel by Lemma 4. $\square$

## Stability with a fixed goal

**Lemma 8.** For one particle with a fixed goal $\mathbf g$ and no external force, the pair $(\mathbf v, \mathbf e)$ with $\mathbf e = \mathbf x - \mathbf g$ evolves by the matrix $E = \begin{pmatrix} 1 & -\alpha/\Delta t \\ \Delta t & 1 - \alpha \end{pmatrix}$ in each coordinate (equation (11) of the paper). For $0 < \alpha < 4$ its eigenvalues are $e^{\pm i\theta}$ with $\cos\theta = 1 - \alpha/2$, so they have magnitude 1, and the motion is a rotation of $(\mathbf v, \mathbf e)$ in a fixed elliptic norm: it neither grows nor decays.

*Proof.* The step gives $\mathbf v' = \mathbf v - \frac{\alpha}{\Delta t}\mathbf e$ and $\mathbf e' = \mathbf e + \Delta t\mathbf v' = \Delta t\mathbf v + (1 - \alpha)\mathbf e$, which is $E$. Its determinant is $(1 - \alpha) + \alpha = 1$ and its trace is $2 - \alpha$. The eigenvalues solve $\lambda^2 - (2 - \alpha)\lambda + 1 = 0$. For $|2 - \alpha| < 2$ the discriminant is negative, so the two roots are complex conjugates whose product is 1, hence both have magnitude 1, and $\operatorname{Re}\lambda = 1 - \alpha/2 = \cos\theta$. The roots are distinct, so $E$ is diagonalizable over $\mathbb C$ and is similar to a rotation by $\theta$. $\square$

The paper calls this unconditionally stable. It is a statement about the model with a fixed goal; the real goals move with the particles. The period is $2\pi/\theta$ steps for every $\Delta t$, so the stiffness that $\alpha$ gives depends on $\Delta t$: a spring with the same period has $\omega\Delta t = \theta$.

**Lemma 9.** If $\alpha = 1$, $\mathbf v_i = 0$ and $\mathbf f_i = 0$, one step gives $\mathbf x_i' = \mathbf g_i$.

*Proof.* $\mathbf v_i' = (\mathbf g_i - \mathbf x_i)/\Delta t$, so $\mathbf x_i' = \mathbf x_i + (\mathbf g_i - \mathbf x_i) = \mathbf g_i$. $\square$

## Cost

**Lemma 10.** A step costs $\Theta(n)$ time and memory, after a $\Theta(n)$ precomputation of $\mathbf x^0_{cm}$, the $\mathbf q_i$ and $S_0^{-1}$.

*Proof.* Lines L1, L2, L5, L6 and L7 are sums or maps over the particles with $O(1)$ work each. Lines L3 and L4 work on $2 \times 2$ matrices in $O(1)$. $\square$
