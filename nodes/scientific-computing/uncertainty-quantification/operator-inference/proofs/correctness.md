---
title: With re-projected data and a data matrix of full column rank, operator inference returns the intrusive POD-Galerkin reduced model
proves: [correctness]
status: full
---

We assume exact arithmetic. The full step is $f(x) = A x + H(x \otimes x)$ with $x \in \mathbb{R}^n$, $V \in \mathbb{R}^{n \times r}$ has orthonormal columns, and $s(a) = (a_i a_j)_{i \le j}$ has $q = r(r+1)/2$ entries. Let $p = r + q$.

**Lemma 1 (the intrusive model has the assumed form).** There are unique matrices $\hat{A}_{int} \in \mathbb{R}^{r \times r}$ and $\hat{H}_{int} \in \mathbb{R}^{r \times q}$ with $V^T f(V a) = \hat{A}_{int} a + \hat{H}_{int} s(a)$ for all $a \in \mathbb{R}^r$.

*Proof.* $V^T f(V a) = V^T A V a + V^T H (V a \otimes V a)$. The first part is linear in $a$. Each entry of $V a \otimes V a$ is $\sum_{i, j} V_{ki} V_{lj} a_i a_j$, a quadratic form in $a$; collect the terms $a_i a_j$ and $a_j a_i$ for $i < j$ into one coefficient. This gives the form with $\hat{A}_{int} = V^T A V$. For uniqueness, a polynomial $B a + C s(a)$ that is 0 for all $a$ has all coefficients 0, because the monomials $a_i$ and $a_i a_j$ with $i \le j$ are linearly independent functions. $\square$

The implementation reads off the same matrices with $f$ only. Since $f(-x) = -A x + H(x \otimes x)$, the odd part $(f(x) - f(-x))/2$ is $A x$ and the even part $(f(x) + f(-x))/2$ is $H(x \otimes x)$. The column $j$ of $\hat{A}_{int}$ is $V^T$ times the odd part at $v_j$. For $i < j$ the even part $Q$ gives $Q(v_i + v_j) - Q(v_i) - Q(v_j) = H(v_i \otimes v_j + v_j \otimes v_i)$, which is the coefficient of $a_i a_j$ after the projection by $V^T$, and $Q(v_i)$ gives the coefficient of $a_i^2$.

**Lemma 2 (least squares by QR).** Let $D \in \mathbb{R}^{K \times p}$ have full column rank and $R \in \mathbb{R}^{K \times r}$. Then $\|D O - R\|_F$ has a unique minimizer $O^*$, the solution of $D^T D O = D^T R$. If $D = Q_1 T$ with $Q_1^T Q_1 = I$ and $T$ upper triangular with a positive diagonal, then $O^* = T^{-1} Q_1^T R$, which line L5 computes.

*Proof.* $\|D O - R\|_F^2 = \sum_c \|D o_c - r_c\|_2^2$ over the columns, so each column is a separate problem. For one column, $g(o) = \|D o - r\|_2^2$ is a quadratic with the Hessian $2 D^T D$, which is positive definite since $D$ has full column rank. So $g$ has a unique minimizer, where the gradient $2 D^T (D o - r)$ is 0. Gram-Schmidt on independent columns does not divide by 0 and gives $D = Q_1 T$ as stated. Then $D^T D = T^T T$ and $D^T r = T^T Q_1^T r$, and since $T^T$ is invertible, the normal equations become $T o = Q_1^T r$, which back substitution solves. $\square$

**Theorem (exact recovery with re-projection).** Let the reduced states be re-projected, $\hat{a}_0 = V^T x_0$ and $\hat{a}_{k+1} = V^T f(V \hat{a}_k)$ for each trajectory, and let the data matrix $D$ of lines L3 and L4 have full column rank. Then line L6 returns $\hat{A} = \hat{A}_{int}$ and $\hat{H} = \hat{H}_{int}$.

*Proof.* Let $O_{int} = [\hat{A}_{int}, \hat{H}_{int}]^T \in \mathbb{R}^{p \times r}$. The row of $D$ for the state $\hat{a}_k$ is $d_k^T = [\hat{a}_k^T, s(\hat{a}_k)^T]$, and the matching row of $R$ is $\hat{a}_{k+1}^T$. By Lemma 1, $\hat{a}_{k+1} = V^T f(V \hat{a}_k) = \hat{A}_{int} \hat{a}_k + \hat{H}_{int} s(\hat{a}_k) = O_{int}^T d_k$. So $R = D O_{int}$, and $\|D O_{int} - R\|_F = 0$. Then $O_{int}$ is a minimizer, and by Lemma 2 it is the only one, so $O^* = O_{int}$. Line L6 takes the first $r$ rows of $O^*$ as $\hat{A}^T$ and the remaining $q$ rows as $\hat{H}^T$. $\blacksquare$

**The closure error with projected data.** If instead $\hat{a}_k = V^T x_k$ with $x_{k+1} = f(x_k)$, then $\hat{a}_{k+1} = V^T f(x_k)$, while the intrusive model predicts $V^T f(V V^T x_k)$. So $R = D O_{int} + E$, where the row $k$ of $E$ is $(V^T f(x_k) - V^T f(V V^T x_k))^T$, and by Lemma 2 the learned operator is $O^* = O_{int} + (D^T D)^{-1} D^T E$. $E = 0$ if every $x_k$ is in the range of $V$, and then plain projection also recovers the intrusive model. In general $E \ne 0$ when the snapshots have a component outside the range of $V$, and the learned model differs from the intrusive one. The example on the page measures this difference.

**Termination.** Every line runs a fixed number of steps: $K$ calls of $f$ per trajectory for line L2, $p$ Gram-Schmidt columns with two passes each, and $r$ back substitutions of length $p$. Lemma 2 shows that no division by 0 occurs when $D$ has full column rank; the implementation raises an error if a column norm is exactly 0.
