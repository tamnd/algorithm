---
title: For the exact covariance of d tones in white noise, the MUSIC null spectrum vanishes exactly at the d frequencies
proves: [correctness]
status: full
---

The notation is that of the page. $a(\omega) = (1, e^{i\omega}, \dots, e^{i(m-1)\omega})^T$ is the steering vector, and the exact covariance is

$$R = A P A^H + \sigma^2 I, \qquad A = \big(a(\omega_1), \dots, a(\omega_d)\big),$$

with distinct $\omega_1, \dots, \omega_d$ in $[-\pi, \pi)$, $d < m$, a $d \times d$ positive definite source covariance $P$ (diagonal, with the powers, for uncorrelated tones) and $\sigma^2 > 0$.

**Lemma 1 (Vandermonde rank).** For $k \le m$ distinct frequencies $\theta_1, \dots, \theta_k$, the $m \times k$ matrix $(a(\theta_1), \dots, a(\theta_k))$ has rank $k$.

*Proof.* Its first $k$ rows form the Vandermonde matrix in the distinct numbers $e^{i\theta_j}$, whose determinant $\prod_{j < l}(e^{i\theta_l} - e^{i\theta_j})$ is not zero. $\square$

**Lemma 2 (the eigenstructure of $R$).** The $m - d$ smallest eigenvalues of $R$ are all equal to $\sigma^2$, the $d$ largest are strictly larger, and the eigenspace of $\sigma^2$ is the orthogonal complement of the range of $A$.

*Proof.* $APA^H$ is Hermitian and positive semidefinite. For $v$ in the range of $A$, $v = Au$ with $u \ne 0$ when $v \ne 0$ (Lemma 1), and $v^H APA^H v = (A^H A u)^H P (A^H A u) > 0$ because $A^H A$ is nonsingular and $P$ is positive definite. So $APA^H$ is positive definite on the $d$-dimensional range of $A$ and zero on its orthogonal complement, which is $\ker A^H$, of dimension $m - d$. By the spectral theorem, $APA^H$ has $d$ positive eigenvalues $\mu_1 \ge \dots \ge \mu_d > 0$ with eigenvectors spanning the range of $A$ and the eigenvalue $0$ on $\ker A^H$. Adding $\sigma^2 I$ adds $\sigma^2$ to every eigenvalue and keeps the eigenvectors. $\square$

**Lemma 3 (the zeros of the null spectrum).** Let $E$ be any $m \times (m - d)$ matrix whose columns are orthonormal eigenvectors for the $m - d$ smallest eigenvalues, as chosen by lines L1 and L2. Then $D(\omega) = \|E^H a(\omega)\|^2$ is zero if and only if $\omega \in \{\omega_1, \dots, \omega_d\}$.

*Proof.* By Lemma 2 the columns of $E$ form an orthonormal basis of $\ker A^H$, so $EE^H$ is the orthogonal projector onto it and $D(\omega)$ is the squared distance from $a(\omega)$ to the range of $A$. For $\omega = \omega_k$, $a(\omega)$ is a column of $A$ and the distance is zero. For any other $\omega$, the $d + 1 \le m$ vectors $a(\omega_1), \dots, a(\omega_d), a(\omega)$ are linearly independent by Lemma 1, so $a(\omega)$ is not in the range of $A$ and $D(\omega) > 0$. Because the eigenvalue gap of Lemma 2 is strict, sorting the eigenvalues selects this subspace, and any orthonormal basis of it gives the same projector, so the choice of eigenvectors within the repeated eigenvalue $\sigma^2$ does not matter. $\square$

**Theorem.** With the exact covariance $R$, the function $D$ of line L3 is continuous, nonnegative and has exactly $d$ zeros in $[-\pi, \pi)$, at the true frequencies. Hence the pseudospectrum $1/D$ has $d$ infinite peaks there. If the grid of line L3 is fine enough that each zero is the unique minimum of $D$ in the bracket of two grid steps around its grid minimum, and the $d$ deepest grid minima are the brackets of the $d$ zeros, then lines L4 and L5 return the $d$ frequencies to within the tolerance of the golden-section search.

*Proof.* Continuity: $D$ is a trigonometric polynomial, $D(\omega) = q_0 + 2\operatorname{Re}\sum_{k=1}^{m-1} q_k e^{i\omega k}$ with $q_k$ the sums of the $k$th superdiagonal of $EE^H$. Its zeros are given by Lemma 3. On a bracket where $D$ has a unique minimum, the golden-section search of line L5 keeps the minimum inside the bracket at every step, and the bracket shrinks by the factor $(\sqrt 5 - 1)/2$ per step. $\blacksquare$

**Remark (estimated covariance).** For a sample covariance $\hat R$ the conclusions hold in the limit: $\hat R \to R$ almost surely as the number of snapshots grows, the eigenvalues and the projector $EE^H$ are continuous functions of the matrix where the gap of Lemma 2 is strict, and so the minima of $\hat D$ converge to the true frequencies. This is the consistency of MUSIC; its variance was derived by Stoica and Nehorai (1989).
