---
title: The normal equations give the unique least-squares fit, the fit is exact on the span, and the hat matrix gives the leave-one-out residuals
proves: [correctness, termination]
status: full
---

We assume exact arithmetic. Let $A$ be the $N \times P$ design matrix of line L4, with rows $A_i = (\Psi_\alpha(x_i))_{\alpha \in \Lambda}$, and let $y = (y_1, \ldots, y_N)^{\mathsf T}$. Write $G = A^{\mathsf T} A$ and $r(c) = y - A c$.

**Lemma 1 (Cholesky succeeds exactly when $A$ has full column rank).** $G$ is symmetric positive semidefinite, and it is positive definite if and only if the columns of $A$ are linearly independent.

*Proof.* $G^{\mathsf T} = G$, and $v^{\mathsf T} G v = \|A v\|^2 \ge 0$, with equality if and only if $A v = 0$. So $G$ is positive definite if and only if $A v = 0$ only for $v = 0$. The Cholesky algorithm on a symmetric matrix finds a positive pivot at every step if and only if the matrix is positive definite, so line L5 succeeds exactly in this case. $\square$

**Lemma 2 (the normal equations give the unique minimizer).** If $A$ has full column rank, the solution $c$ of $G c = A^{\mathsf T} y$ satisfies $\|r(c')\|^2 = \|r(c)\|^2 + \|A (c' - c)\|^2$ for every $c'$, so $c$ is the unique minimizer of $\|y - A c'\|$.

*Proof.* $A^{\mathsf T} r(c) = A^{\mathsf T} y - G c = 0$, so the residual is orthogonal to every column of $A$. Then $r(c') = r(c) - A (c' - c)$, and the cross term $2 (c' - c)^{\mathsf T} A^{\mathsf T} r(c)$ vanishes. The last term is positive for $c' \ne c$ by full rank. $\square$

**Lemma 3 (exact on the span).** If $q = \sum_{\alpha \in \Lambda} c^*_\alpha \Psi_\alpha$ and $A$ has full column rank, then line L5 returns $c = c^*$.

*Proof.* Then $y = A c^*$, so $\|r(c^*)\| = 0$, which is the smallest possible value, and Lemma 2 says the minimizer is unique. $\square$

**Lemma 4 (the leverages).** Let $L$ be the Cholesky factor, $G = L L^{\mathsf T}$, and $h_i = A_i G^{-1} A_i^{\mathsf T}$. Then $h_i = \|L^{-1} A_i^{\mathsf T}\|^2$, $0 \le h_i \le 1$, and $\sum_i h_i = P$.

*Proof.* $G^{-1} = L^{-\mathsf T} L^{-1}$, so $h_i = (L^{-1} A_i^{\mathsf T})^{\mathsf T} (L^{-1} A_i^{\mathsf T})$. The hat matrix $H = A G^{-1} A^{\mathsf T}$ satisfies $H^{\mathsf T} = H$ and $H^2 = A G^{-1} G G^{-1} A^{\mathsf T} = H$, so it is an orthogonal projection, and $h_i = e_i^{\mathsf T} H e_i = \|H e_i\|^2 \le \|e_i\|^2 = 1$. Finally $\sum_i h_i = \operatorname{tr} H = \operatorname{tr}(G^{-1} A^{\mathsf T} A) = \operatorname{tr} I_P = P$. $\square$

**Lemma 5 (leave-one-out residuals).** Suppose $A$ with row $i$ removed, $A_{(i)}$, still has full column rank, and let $c_{(i)}$ be its least-squares fit to $y$ with entry $i$ removed. Then $h_i < 1$ and

$$y_i - A_i c_{(i)} = \frac{y_i - A_i c}{1 - h_i}.$$

*Proof.* $G_{(i)} = A_{(i)}^{\mathsf T} A_{(i)} = G - A_i^{\mathsf T} A_i$ is positive definite by Lemma 1. By the matrix determinant lemma, $\det G_{(i)} = (1 - A_i G^{-1} A_i^{\mathsf T}) \det G = (1 - h_i) \det G$, so $h_i < 1$. The Sherman-Morrison formula gives

$$G_{(i)}^{-1} = G^{-1} + \frac{G^{-1} A_i^{\mathsf T} A_i G^{-1}}{1 - h_i}.$$

Also $A_{(i)}^{\mathsf T} y_{(i)} = A^{\mathsf T} y - A_i^{\mathsf T} y_i$. Multiply: $c_{(i)} = G_{(i)}^{-1} (A^{\mathsf T} y - A_i^{\mathsf T} y_i)$. Apply $A_i$ on the left and use $A_i G^{-1} A^{\mathsf T} y = A_i c$ and $A_i G^{-1} A_i^{\mathsf T} = h_i$:

$$A_i c_{(i)} = A_i c - h_i y_i + \frac{h_i (A_i c - h_i y_i)}{1 - h_i} = \frac{A_i c - h_i y_i}{1 - h_i}.$$

Then $y_i - A_i c_{(i)} = \frac{(1 - h_i) y_i - A_i c + h_i y_i}{1 - h_i} = \frac{y_i - A_i c}{1 - h_i}$. $\square$

**Lemma 6 (unbiased Gram matrix).** If the points are drawn independently from the input law, then $\mathbb{E}[\frac{1}{N} G] = I_P$.

*Proof.* $\frac{1}{N} G_{\alpha\beta} = \frac{1}{N} \sum_i \Psi_\alpha(x_i) \Psi_\beta(x_i)$, and each term has expectation $\mathbb{E}[\Psi_\alpha \Psi_\beta] = \delta_{\alpha\beta}$ by orthonormality. $\square$

**Theorem.** REGRESSION-PCE stops after $N$ model runs. If $A$ has full column rank, it returns the unique least-squares coefficients; they equal the true coefficients when $q$ lies in the span of the basis. If also every $A_{(i)}$ has full column rank, the value $\varepsilon_{\mathrm{LOO}}$ of line L6 equals $\frac{1}{N} \sum_i (y_i - A_i c_{(i)})^2$ divided by the sample variance of $y$, the leave-one-out mean squared error of $N$ separate refits.

*Proof.* Termination: lines L2 to L4 are loops of length $N$ and $N P$, line L5 is a Cholesky factorization of a $P \times P$ matrix and two triangular solves, and line L6 is $N$ triangular solves; all are finite. The coefficients are Lemmas 1 to 3, and the leave-one-out value is Lemmas 4 and 5. $\blacksquare$

The theorem makes no claim about the accuracy of the fit on new inputs for a $q$ outside the span. That claim needs the probabilistic stability theorem of Cohen, Davenport and Leviatan, which holds when $N / \log N$ is large compared with $\sup_\xi \sum_\alpha \Psi_\alpha(\xi)^2$, and which is quoted on the page but not proved here.
