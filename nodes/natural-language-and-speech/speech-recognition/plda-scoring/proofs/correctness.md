---
title: The PLDA closed form is the exact log likelihood ratio of the two-covariance model
proves: [correctness]
status: full
---

We use the notation of the page. Embeddings have dimension $d$. In the two-covariance model an embedding of speaker $s$ is $x = m + y_s + e$, with $y_s \sim \mathcal{N}(0, B)$ shared by all embeddings of $s$, and $e \sim \mathcal{N}(0, W)$ new for each embedding. All $y$ and $e$ are independent. $B$ is symmetric positive semidefinite and $W$ is symmetric positive definite. Write $A = B + W$, $u = x_1 - m$, $v = x_2 - m$, and all logs are natural logs.

$H_s$ is the hypothesis that $x_1$ and $x_2$ come from the same speaker, and $H_d$ is the hypothesis that they come from two different speakers.

**Lemma 1 (the two joint densities).** Under $H_d$, $(u, v) \sim \mathcal{N}(0, \operatorname{diag}(A, A))$. Under $H_s$, $(u, v) \sim \mathcal{N}(0, J)$ with
$$J = \begin{pmatrix} A & B \\ B & A \end{pmatrix}.$$
$A$, $J$ and $S = A - B A^{-1} B$ are positive definite.

*Proof.* Under $H_d$, $u = y + e_1$ and $v = y' + e_2$ with independent $y, y'$, so $u$ and $v$ are independent with covariance $B + W = A$. Under $H_s$, $u = y + e_1$ and $v = y + e_2$. Then $\operatorname{Cov}(u) = \operatorname{Cov}(v) = A$ and $\operatorname{Cov}(u, v) = \operatorname{Cov}(y) = B$. Both are linear maps of Gaussian vectors, so both are Gaussian. $J$ is the sum of $\begin{pmatrix} B & B \\ B & B \end{pmatrix}$, which is positive semidefinite because $(a, b)$ gives $(a + b)^\top B (a + b) \ge 0$, and $\operatorname{diag}(W, W)$, which is positive definite. So $J$ is positive definite. $A$ is a diagonal block of $J$, so $A$ is positive definite. $S$ is the Schur complement of the block $A$ in $J$, and $\det J = \det A \det S$. The Schur complement of a positive definite matrix is positive definite. $\square$

**Lemma 2 (the inverse of $J$).** Write $\Lambda = A^{-1}$ and $\Gamma = S^{-1}$. Then
$$J^{-1} = \begin{pmatrix} \Gamma & -\Lambda B \Gamma \\ -\Lambda B \Gamma & \Gamma \end{pmatrix},$$
and $\Lambda B \Gamma$ is symmetric.

*Proof.* The block inverse formula for $\begin{pmatrix} A & B \\ B & A \end{pmatrix}$ gives the lower right block $S^{-1} = \Gamma$ and the upper right block $-A^{-1} B S^{-1} = -\Lambda B \Gamma$. Swap the two halves of the coordinates: the permutation maps $J$ to itself, so it also maps $J^{-1}$ to itself. Thus the upper left block equals the lower right block $\Gamma$, and the lower left block equals the upper right block. $J^{-1}$ is symmetric, so the lower left block is also the transpose of the upper right block. Hence $\Lambda B \Gamma = (\Lambda B \Gamma)^\top$. $\square$

**Theorem 3 (the closed form).** With $Q = \Lambda - \Gamma$, $P = \Lambda B \Gamma$ and $c = \frac12 (\log \det A - \log \det S)$,
$$\log \frac{p(x_1, x_2 \mid H_s)}{p(x_1, x_2 \mid H_d)} = \tfrac12 u^\top Q u + \tfrac12 v^\top Q v + u^\top P v + c.$$
Lines L1 to L6 compute this value.

*Proof.* For a Gaussian $\mathcal{N}(0, K)$ in dimension $k$, $\log p(z) = -\frac12 (k \log 2\pi + \log \det K + z^\top K^{-1} z)$. The two densities have the same dimension $2d$, so the terms $2d \log 2\pi$ cancel. By Lemma 1, $\log \det J = \log \det A + \log \det S$ and $\log \det \operatorname{diag}(A, A) = 2 \log \det A$. The difference of the log determinant terms is $-\frac12(\log \det A + \log \det S) + \log \det A = c$. By Lemma 2 the quadratic form under $H_s$ is $u^\top \Gamma u + v^\top \Gamma v - 2 u^\top \Lambda B \Gamma v$, and under $H_d$ it is $u^\top \Lambda u + v^\top \Lambda v$. Thus the log ratio is
$$-\tfrac12 (u^\top \Gamma u + v^\top \Gamma v - 2 u^\top P v) + \tfrac12 (u^\top \Lambda u + v^\top \Lambda v) + c,$$
which is the stated form. L1 forms $A$, L2 forms $S$ and its inverse, L3 forms $Q$ and $P$, L4 forms $c$, and L5 and L6 evaluate the form. $\square$

**Corollary 4 (properties).** The score is symmetric in $x_1$ and $x_2$. $c \ge 0$, and $Q$ is negative semidefinite. If $B$ is positive definite, $Q$ is negative definite and $c > 0$. If $B = 0$, the score is $0$ for all inputs.

*Proof.* Symmetry follows from $P = P^\top$ (Lemma 2), since then $u^\top P v = v^\top P u$. $S = A - B A^{-1} B$ with $B A^{-1} B$ positive semidefinite, so $S \preceq A$. For positive definite matrices, $S \preceq A$ implies $S^{-1} \succeq A^{-1}$ and $\det S \le \det A$. Thus $Q = A^{-1} - S^{-1} \preceq 0$ and $c \ge 0$. If $B$ is positive definite, $B A^{-1} B$ is positive definite, the inequalities are strict, and so $Q \prec 0$ and $c > 0$. If $B = 0$, then $S = A$, so $Q = 0$, $P = 0$ and $c = 0$. $\square$

**Theorem 5 (several enrollment embeddings).** Let $B$ be positive definite. Suppose $x_1, \ldots, x_n$ are the enrollment embeddings of one speaker and $x_t$ is a test embedding. $H_s$ says that $x_t$ comes from the same speaker. $H_d$ says that it comes from another speaker. Write $C_n = (B^{-1} + n W^{-1})^{-1}$ and $\mu_n = C_n W^{-1} \sum_i (x_i - m)$. Then
$$\log \frac{p(x_1, \ldots, x_n, x_t \mid H_s)}{p(x_1, \ldots, x_n, x_t \mid H_d)} = \log \mathcal{N}(x_t; m + \mu_n, W + C_n) - \log \mathcal{N}(x_t; m, A).$$
For $n = 1$ this equals the value of Theorem 3. Lines L7 to L9 compute it.

*Proof.* Under both hypotheses, the enrollment embeddings have the same density $p(x_1, \ldots, x_n)$. Under $H_d$, $x_t$ is independent of them and has density $\mathcal{N}(m, A)$. Under $H_s$, write the joint density as $p(x_1, \ldots, x_n) \, p(x_t \mid x_1, \ldots, x_n)$. Thus the ratio is $p(x_t \mid x_1, \ldots, x_n, H_s) / \mathcal{N}(x_t; m, A)$. Given $y$, the $x_i - m$ are independent $\mathcal{N}(y, W)$. The prior $\mathcal{N}(0, B)$ is conjugate, and the log posterior of $y$ is, up to a constant, $-\frac12 y^\top (B^{-1} + n W^{-1}) y + y^\top W^{-1} \sum_i (x_i - m)$. So the posterior is $\mathcal{N}(\mu_n, C_n)$. Given the enrollment data, $x_t = m + y + e_t$, with $y$ from this posterior and $e_t \sim \mathcal{N}(0, W)$ independent of it. So $x_t \sim \mathcal{N}(m + \mu_n, C_n + W)$. For $n = 1$, both theorems compute the log of the same ratio of densities, so the values are equal. $\square$

**Proposition 6 (the Prince-Elder parameters).** In the model $x = m + F h + G w + \varepsilon$, with $h \sim \mathcal{N}(0, I)$ shared by a speaker, $w \sim \mathcal{N}(0, I)$ new for each embedding, and $\varepsilon \sim \mathcal{N}(0, \Sigma)$ with diagonal $\Sigma$, the speaker term $y = F h$ has covariance $B = F F^\top$ and the session term $G w + \varepsilon$ has covariance $W = G G^\top + \Sigma$. So the scores of Theorems 3 and 5 apply with these $B$ and $W$.

*Proof.* $\operatorname{Cov}(F h) = F I F^\top$, and the session term is a sum of independent zero mean Gaussians, so its covariance is the sum of $G G^\top$ and $\Sigma$. The scores depend on the model only through the joint distribution of the embeddings, which is the same as that of the two-covariance model with these $B$ and $W$. $\square$

**Remark.** The theorems hold for the model. They do not say that real embeddings are Gaussian. Length normalization and LDA before PLDA are heuristics that make the embeddings closer to Gaussian. The ratio is a calibrated likelihood ratio only to the extent that the model fits.
