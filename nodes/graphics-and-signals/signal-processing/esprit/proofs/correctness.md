---
title: For the exact covariance of d tones in white noise, the ESPRIT rotation operator has the eigenvalues e^{iω_k}
proves: [correctness]
status: full
---

The notation is that of the page. $a(\omega) = (1, e^{i\omega}, \dots, e^{i(m-1)\omega})^T$, $A = (a(\omega_1), \dots, a(\omega_d))$ with distinct $\omega_k$ in $[-\pi, \pi)$ and $d < m$, and $R = APA^H + \sigma^2 I$ with $P$ a positive definite $d \times d$ source covariance and $\sigma^2 > 0$. For an $m$-row matrix $X$, $X_1$ is $X$ without its last row and $X_2$ is $X$ without its first row.

**Lemma 1 (the signal subspace).** The eigenvectors $u_1, \dots, u_d$ of the $d$ largest eigenvalues of $R$ span the range of $A$, so $S = (u_1, \dots, u_d) = AT$ for a nonsingular $d \times d$ matrix $T$.

*Proof.* $A$ has rank $d$, because its first $d$ rows form a Vandermonde matrix in the distinct points $e^{i\omega_k}$. Then $APA^H$ is positive definite on the range of $A$ and zero on its orthogonal complement, so $R$ has $d$ eigenvalues larger than $\sigma^2$, with eigenvectors in the range of $A$, and the eigenvalue $\sigma^2$ on the complement. Because the $d$ large eigenvalues are strictly larger than the others, line L1 sorts them first. The columns of $S$ are $d$ orthonormal vectors in the $d$-dimensional range of $A$, so $S = AT$ with $T = (A^H A)^{-1} A^H S$, and $T$ is nonsingular because $S$ has rank $d$. $\square$

**Lemma 2 (shift invariance).** $A_2 = A_1 D$ with $D = \operatorname{diag}(e^{i\omega_1}, \dots, e^{i\omega_d})$.

*Proof.* Entry $(r, k)$ of $A_2$ is $e^{i(r+1)\omega_k} = e^{ir\omega_k}\, e^{i\omega_k}$, which is entry $(r, k)$ of $A_1$ times $D_{kk}$. $\square$

**Lemma 3 (line L4).** $S_1$ has full column rank, and the least-squares problem $\min_\Phi \|S_1 \Phi - S_2\|_F$ of line L4 has the unique solution $\Phi = T^{-1} D T$, with residual zero.

*Proof.* By Lemma 1, $S_1 = A_1 T$ and $S_2 = A_2 T$. $A_1$ is an $(m - 1) \times d$ Vandermonde matrix with $d \le m - 1$ distinct points, so it has rank $d$, and $S_1$ has rank $d$ because $T$ is nonsingular. By Lemma 2, $S_2 = A_1 D T = A_1 T\,(T^{-1} D T) = S_1 (T^{-1} D T)$, so $\Phi = T^{-1}DT$ gives residual zero. Full column rank of $S_1$ makes $S_1^H S_1$ nonsingular, and the normal equations $S_1^H S_1 \Phi = S_1^H S_2$ that line L4 solves have only this solution. $\square$

**Theorem.** With the exact covariance, the eigenvalues of the $\Phi$ of line L4 are $e^{i\omega_1}, \dots, e^{i\omega_d}$, and line L6 returns $\omega_1, \dots, \omega_d$.

*Proof.* By Lemma 3, $\Phi$ is similar to $D$, so it has the same eigenvalues, the diagonal entries of $D$. They lie on the unit circle, and the argument of $e^{i\omega_k}$ in $[-\pi, \pi)$ is $\omega_k$. The result does not depend on which orthonormal basis of the signal subspace line L1 returns, because a change of basis replaces $T$ by $TQ$ and $\Phi$ by the similar matrix $Q^{-1}\Phi Q$. $\blacksquare$

**Remark (estimated covariance).** With a sample covariance, $\hat S$ spans a perturbed subspace and the eigenvalues of $\hat\Phi$ are off the unit circle by a small amount. Because the signal subspace and the least-squares solution are continuous functions of $R$ when the eigenvalue gap of Lemma 1 is strict, the estimates converge to the true frequencies as the covariance estimate converges.
