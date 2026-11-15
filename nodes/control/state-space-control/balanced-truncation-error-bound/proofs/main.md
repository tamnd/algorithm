---
title: Balanced truncation keeps asymptotic stability and has the error bound of twice the sum of the distinct deleted Hankel singular values
proves: [statement]
status: full
---

This file proves both parts of the statement. Part 1 is the stability result of Pernebo and Silverman (1982). Part 2 is the error bound of Enns (1984) and Glover (1984). The argument is the standard one, found for example in Zhou, Doyle and Glover, Chapter 7. It uses only the two Lyapunov equations, a block inverse and one fact about eigenvalues.

## Setting

Let $(A, B, C, D)$ be a minimal balanced realization of $G(s) = C(sI - A)^{-1}B + D$, with $A$ Hurwitz, so that

$$A \Sigma + \Sigma A^T + B B^T = 0, \qquad A^T \Sigma + \Sigma A + C^T C = 0, \qquad \Sigma = \operatorname{diag}(\Sigma_1, \Sigma_2),$$

with $\Sigma_1 = \operatorname{diag}(\sigma_1, \dots, \sigma_r)$, $\Sigma_2 = \operatorname{diag}(\sigma_{r+1}, \dots, \sigma_n)$ and $\sigma_1 \ge \dots \ge \sigma_n > 0$. Partition $A$, $B$ and $C$ to match:

$$A = \begin{bmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{bmatrix}, \qquad B = \begin{bmatrix} B_1 \\ B_2 \end{bmatrix}, \qquad C = \begin{bmatrix} C_1 & C_2 \end{bmatrix}.$$

The truncated model is $G_r(s) = C_1(sI - A_{11})^{-1}B_1 + D$. Assume the gap $\sigma_r > \sigma_{r+1}$, so that no diagonal entry of $\Sigma_2$ equals a diagonal entry of $\Sigma_1$.

The blocks of the two Lyapunov equations give the six equations used below:

$$A_{11}\Sigma_1 + \Sigma_1 A_{11}^T + B_1 B_1^T = 0, \qquad A_{11}^T\Sigma_1 + \Sigma_1 A_{11} + C_1^T C_1 = 0, \tag{1}$$

$$A_{21}\Sigma_1 + \Sigma_2 A_{12}^T + B_2 B_1^T = 0, \qquad A_{12}^T\Sigma_1 + \Sigma_2 A_{21} + C_2^T C_1 = 0, \tag{2}$$

$$A_{22}\Sigma_2 + \Sigma_2 A_{22}^T + B_2 B_2^T = 0, \qquad A_{22}^T\Sigma_2 + \Sigma_2 A_{22} + C_2^T C_2 = 0. \tag{3}$$

The second equation of (2) is the transpose of the $(1,2)$ block of the observability equation, $\Sigma_1 A_{12} + A_{21}^T \Sigma_2 + C_1^T C_2 = 0$.

## Part 1: $A_{11}$ is Hurwitz

**Step 1: no eigenvalue in the open right half plane.** Let $A_{11} v = \lambda v$ with $v \in \mathbb{C}^r$, $v \ne 0$. Since $A_{11}$ is real, $v^* A_{11}^T = \bar\lambda v^*$. Multiply the second equation of (1) by $v^*$ on the left and by $v$ on the right:

$$2 \operatorname{Re}\lambda \; v^* \Sigma_1 v = -\|C_1 v\|^2 \le 0.$$

Since $\Sigma_1$ is positive definite, $\operatorname{Re}\lambda \le 0$.

**Step 2: an eigenvalue on the axis gives a special eigenvector.** Suppose $A_{11}$ has an eigenvalue $j\omega$ with $\omega$ real, and let the columns of $V$ be a basis of $\mathcal{K} = \ker(A_{11} - j\omega I)$. Step 1 with $\operatorname{Re}\lambda = 0$ gives $C_1 v = 0$ for every $v \in \mathcal{K}$, so $C_1 V = 0$. Then the second equation of (1) gives $A_{11}^T \Sigma_1 V = -\Sigma_1 A_{11} V = -j\omega\, \Sigma_1 V$. Put $W = \Sigma_1 V$. Then $A_{11}^T W = -j\omega W$, and, since $A_{11}$ is real, $W^* A_{11} = j\omega W^*$. Multiply the first equation of (1) by $W^*$ on the left and $W$ on the right:

$$j\omega\, W^*\Sigma_1 W - j\omega\, W^* \Sigma_1 W + W^* B_1 B_1^T W = 0,$$

so $B_1^T W = 0$. The first equation of (1) applied to $W$ now gives $A_{11} \Sigma_1 W = -\Sigma_1 A_{11}^T W = j\omega\, \Sigma_1 W$, that is

$$A_{11} \Sigma_1^2 V = j\omega\, \Sigma_1^2 V.$$

So $\Sigma_1^2$ maps $\mathcal{K}$ into $\mathcal{K}$. The restriction of the Hermitian matrix $\Sigma_1^2$ to the invariant subspace $\mathcal{K}$ has an eigenvector: there is $v \in \mathcal{K}$, $v \ne 0$, with $\Sigma_1^2 v = \sigma^2 v$ for some $\sigma > 0$. Since $\Sigma_1$ is diagonal and positive, $\Sigma_1 v = \sigma v$, and $\sigma$ is one of $\sigma_1, \dots, \sigma_r$. This vector satisfies

$$A_{11} v = j\omega v, \qquad C_1 v = 0, \qquad \Sigma_1 v = \sigma v, \qquad B_1^T v = \sigma^{-1} B_1^T \Sigma_1 v = 0,$$

where the last equation uses $B_1^T W = 0$ and $\Sigma_1 v \in \operatorname{im} W$.

**Step 3: the eigenvector extends to one of $A$.** Apply both equations of (2) to $v$, and put $x = A_{21} v$ and $y = A_{12}^T v$:

$$\sigma x + \Sigma_2 y = 0, \qquad \sigma y + \Sigma_2 x = 0.$$

Multiply the second equation by $\Sigma_2$ and use the first: $-\sigma^2 x + \Sigma_2^2 x = 0$, so $(\Sigma_2^2 - \sigma^2 I) x = 0$. Every diagonal entry of $\Sigma_2$ is at most $\sigma_{r+1} < \sigma_r \le \sigma$, so $\Sigma_2^2 - \sigma^2 I$ is invertible and $x = A_{21} v = 0$. Then

$$A \begin{bmatrix} v \\ 0 \end{bmatrix} = \begin{bmatrix} A_{11} v \\ A_{21} v \end{bmatrix} = j\omega \begin{bmatrix} v \\ 0 \end{bmatrix},$$

so $A$ has the eigenvalue $j\omega$. This contradicts the assumption that $A$ is Hurwitz. So $A_{11}$ has no eigenvalue on the imaginary axis, and with Step 1 it is Hurwitz.

**Step 4: the truncated model is balanced and minimal.** Equation (1) says that $\Sigma_1$ is both Gramian of $(A_{11}, B_1, C_1)$. Since $A_{11}$ is Hurwitz, these are the unique solutions of the Lyapunov equations, and since $\Sigma_1$ is positive definite, the truncated model is controllable and observable. Its Hankel singular values are $\sigma_1, \dots, \sigma_r$.

## Part 2: the error bound

**Lemma (one distinct value).** If, in the setting above, $\Sigma_2 = \tau I$ for one number $\tau > 0$, then $\|G - G_r\|_\infty \le 2\tau$.

*Proof of the lemma.* Fix a real $\omega$ and put $s = j\omega$. By Part 1, $A_{11}$ is Hurwitz, so $\Phi = (j\omega I - A_{11})^{-1}$ exists. Put

$$\psi = j\omega I - A_{22} - A_{21}\Phi A_{12}, \qquad \tilde B = A_{21}\Phi B_1 + B_2, \qquad \tilde C = C_1 \Phi A_{12} + C_2.$$

The matrix $\psi$ is the [Schur complement](/schur-complement/) of the block $j\omega I - A_{11}$ in $j\omega I - A$, so $\det(j\omega I - A) = \det(j\omega I - A_{11}) \det \psi$, and $\psi$ is invertible since $A$ is Hurwitz. The block formula for the inverse of $j\omega I - A$ gives

$$G(j\omega) - G_r(j\omega) = \tilde C \psi^{-1} \tilde B. \tag{4}$$

To check (4), write $M_{11} = j\omega I - A_{11}$. The inverse of $j\omega I - A$ has the blocks $\Phi + \Phi A_{12}\psi^{-1}A_{21}\Phi$, $\Phi A_{12} \psi^{-1}$, $\psi^{-1}A_{21}\Phi$ and $\psi^{-1}$, and multiplying out $C (j\omega I - A)^{-1} B$ gives $C_1 \Phi B_1 + \tilde C \psi^{-1} \tilde B$.

Next, the Lyapunov equations give

$$\tilde B \tilde B^* = \tau (\psi + \psi^*), \qquad \tilde C^* \tilde C = \tau (\psi + \psi^*). \tag{5}$$

For the first identity, write $A_{11} = j\omega I - M_{11}$. The first equation of (1) becomes $M_{11}\Sigma_1 + \Sigma_1 M_{11}^* = B_1 B_1^T$, and multiplying by $\Phi$ on the left and $\Phi^*$ on the right gives $\Phi B_1 B_1^T \Phi^* = \Sigma_1 \Phi^* + \Phi \Sigma_1$. The first equation of (3) with $\Sigma_2 = \tau I$ becomes $B_2 B_2^T = \tau (M_{22} + M_{22}^*)$ with $M_{22} = j\omega I - A_{22}$. The first equation of (2) gives $B_2 B_1^T = -A_{21}\Sigma_1 - \tau A_{12}^T$. Expand:

$$\tilde B \tilde B^* = A_{21}\Phi B_1 B_1^T \Phi^* A_{21}^T + A_{21}\Phi B_1 B_2^T + B_2 B_1^T \Phi^* A_{21}^T + B_2 B_2^T.$$

Substituting the three relations, the terms with $A_{21}\Sigma_1\Phi^*A_{21}^T$ and $A_{21}\Phi\Sigma_1A_{21}^T$ cancel, and what remains is

$$\tilde B \tilde B^* = -\tau \left( A_{21}\Phi A_{12} + (A_{21}\Phi A_{12})^* \right) + \tau (M_{22} + M_{22}^*) = \tau (\psi + \psi^*).$$

The second identity of (5) is the first one for the dual system $(A^T, C^T, B^T)$, which is balanced with the same $\Sigma$. Its $\psi$ is $\psi^T$ and its $\tilde B$ is $\tilde C^T$, so $\tilde C^T \bar{\tilde C} = \tau(\psi + \psi^*)^T$, and the transpose of this is the second identity.

Now put $H = \psi + \psi^*$. By (5), $H = \tilde B \tilde B^* / \tau$ is positive semidefinite. With $E = G(j\omega) - G_r(j\omega) = \tilde C \psi^{-1} \tilde B$,

$$E^* E = \tilde B^* \psi^{-*} \tilde C^* \tilde C \psi^{-1} \tilde B = \tau\, \tilde B^* (\psi^{-*} H \psi^{-1}) \tilde B.$$

The nonzero eigenvalues of $X Y$ and $Y X$ agree, so the nonzero eigenvalues of $E^*E$ are those of $\tau\, \psi^{-*} H \psi^{-1} \tilde B \tilde B^* = \tau^2\, \psi^{-*} H \psi^{-1} H$. With $\Delta = \psi^{-*}\psi$,

$$\psi^{-*} H \psi^{-1} H = (\psi^{-*}\psi + I)(I + \psi^{-1}\psi^*) = (\Delta + I)(I + \Delta^{-1}) = \Delta + 2I + \Delta^{-1}.$$

Every eigenvalue $\mu$ of $\Delta$ has $|\mu| = 1$. Indeed, let $\psi v = \mu \psi^* v$ with $v \ne 0$, and put $a = v^*\psi v$. Then $a = \mu \bar a$. If $a \ne 0$, then $|\mu| = 1$. If $a = 0$, then $v^* H v = 2 \operatorname{Re} a = 0$, so $H v = 0$ because $H$ is positive semidefinite, so $\psi^* v = -\psi v$, and $\psi v = -\mu \psi v$ gives $\mu = -1$ because $\psi$ is invertible. Write $\mu = e^{i\theta}$. The eigenvalues of $\Delta + 2I + \Delta^{-1}$ are the numbers $\mu + 2 + \mu^{-1} = 2 + 2\cos\theta \le 4$. So every eigenvalue of $E^*E$ is at most $4\tau^2$, and $\|E\|_2 \le 2\tau$. This holds for every real $\omega$, so $\|G - G_r\|_\infty \le 2\tau$. $\square$

**The general case.** Let $\tau_1 > \tau_2 > \dots > \tau_k$ be the distinct values among $\sigma_{r+1}, \dots, \sigma_n$. For $i = 0, 1, \dots, k$ let $G^{(i)}$ be the truncation of the balanced realization that keeps the states whose value is not among $\tau_{k-i+1}, \dots, \tau_k$, that is, it deletes the $i$ smallest distinct values. So $G^{(0)} = G$ and $G^{(k)} = G_r$. Each $G^{(i)}$ is a leading block of the balanced realization of $G$, and the deleted values are smaller than all the kept ones, so by Part 1 each $G^{(i)}$ has a Hurwitz state matrix and is a minimal balanced realization. The step from $G^{(i-1)}$ to $G^{(i)}$ deletes exactly the states with the value $\tau_{k-i+1}$, a block $\tau_{k-i+1} I$, and keeps only larger values. The lemma applied to $G^{(i-1)}$ gives $\|G^{(i-1)} - G^{(i)}\|_\infty \le 2\tau_{k-i+1}$. By the triangle inequality,

$$\|G - G_r\|_\infty \le \sum_{i=1}^{k} \|G^{(i-1)} - G^{(i)}\|_\infty \le 2 (\tau_1 + \dots + \tau_k).$$

**Realizations that are not minimal.** If the given realization is not minimal, some Hankel singular values are zero. Balanced truncation is then defined on a minimal realization of the same $G$, which has the nonzero values only, and the zero values add nothing to the bound. $\blacksquare$
