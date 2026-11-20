---
title: Right decisions are a fixed point of parallel cancellation, the stages can oscillate, and the linear form is Jacobi iteration toward the decorrelator
proves: [correctness]
status: full
---

The model is $y = S A b + w$ for one symbol interval, with unit-norm signatures $s_k$, known amplitudes $A_k > 0$, bits $b_k \in \{-1, +1\}$ and $w \sim \mathcal{N}(0, \sigma^2 I_N)$. Let $R = S^\top S$ and $z = S^\top y = R A b + n$, with $n \sim \mathcal{N}(0, \sigma^2 R)$. Line L1 sets the stage 0 decisions $\hat b^{(0)}$. Lines L3 to L5 compute, for every user $k$ at the same time,

$$x_k^{(m)} = z_k - \sum_{j \ne k} R_{kj} A_j \hat b_j^{(m-1)}, \qquad \hat b_k^{(m)} = \mathrm{sgn}(x_k^{(m)}). \tag{1}$$

**Lemma 1 (what stage m sees).** For every stage $m \ge 1$,

$$x_k^{(m)} = A_k b_k + \sum_{j \ne k} R_{kj} A_j \big( b_j - \hat b_j^{(m-1)} \big) + n_k. \tag{2}$$

*Proof.* Substitute $z_k = A_k b_k + \sum_{j \ne k} R_{kj} A_j b_j + n_k$ into (1). $\square$

Each term $b_j - \hat b_j^{(m-1)}$ is 0 for a right decision and $2 b_j$ for a wrong one. So a stage removes the interference of the users that the previous stage decided right, and doubles the interference of the users it decided wrong.

**Theorem 1 (right decisions are a fixed point).** If $\hat b^{(m-1)} = b$, then $x_k^{(m)} = A_k b_k + n_k$ for every $k$, with $n_k \sim \mathcal{N}(0, \sigma^2)$. Without noise, $\hat b^{(m)} = b$, and all later stages stay at $b$. With noise, each user then errs with probability $Q(A_k / \sigma)$, the single-user error rate.

*Proof.* All terms of the sum in (2) vanish. $R_{kk} = 1$, so $n_k$ has variance $\sigma^2$. Without noise, $\mathrm{sgn}(A_k b_k) = b_k$, and induction on $m$ gives the rest. $\square$

**Corollary (decorrelator start).** If the signatures are linearly independent and $w = 0$, the [decorrelating detector](/decorrelating-detector/) decides $b$ exactly, so a PIC that starts from it stays at $b$ for every stage.

**Theorem 2 (two users without noise).** Let $K = 2$, $w = 0$, $|R_{12}| = |\rho| < 1$, and label the users so that $A_1 \ge A_2$. If $A_1 > 2 |\rho| A_2$, then stage 1 is right for both users, and so is every later stage.

*Proof.* At stage 0, $z_1 = A_1 b_1 + \rho A_2 b_2$ and $|\rho| A_2 < A_2 \le A_1$, so $\hat b_1^{(0)} = b_1$. By (2), $x_2^{(1)} = A_2 b_2 + \rho A_1 (b_1 - \hat b_1^{(0)}) = A_2 b_2$, so $\hat b_2^{(1)} = b_2$. Also $x_1^{(1)} = A_1 b_1 + \rho A_2 (b_2 - \hat b_2^{(0)})$, and the second term has absolute value at most $2 |\rho| A_2 < A_1$, so $\hat b_1^{(1)} = b_1$. Theorem 1 does the rest. $\square$

**Theorem 3 (the stages can oscillate, even without noise).** Take $K = 2$, $\rho = 0.9$, $A = (1, 0.8)$, $b = (+1, -1)$ and $w = 0$. Then the stages alternate between $(+1, +1)$ and $(-1, -1)$ and never reach $b$.

*Proof.* $z = (1 - 0.72,\ -0.8 + 0.9) = (0.28, 0.1)$, so $\hat b^{(0)} = (+1, +1)$. From $(+1, +1)$, (1) gives $x^{(m)} = (0.28 - 0.72,\ 0.1 - 0.9) = (-0.44, -0.8)$, so the next stage is $(-1, -1)$. From $(-1, -1)$, (1) gives $(0.28 + 0.72,\ 0.1 + 0.9) = (1, 1)$, so the next stage is $(+1, +1)$ again. $\square$

Here $A_1 = 1 < 2 \cdot 0.9 \cdot 0.8 = 1.44$, so Theorem 2 does not apply. The stage 0 error on the weak user doubles its interference on the strong user, and each user's error then flips the other.

**Theorem 4 (linear PIC is Jacobi iteration).** Remove the sign: let $x^{(0)} = z$ and $x^{(m)} = z - (R - I)\, x^{(m-1)}$. If $R$ is invertible, then

$$x^{(m)} - R^{-1} z = (I - R)^{m+1} \big( - R^{-1} z \big) \quad \text{and} \quad x^{(m)} = \sum_{i=0}^{m} (I - R)^i z. \tag{3}$$

So $x^{(m)} \to R^{-1} z$, the decorrelator output, for every $z$ if and only if the spectral radius of $R - I$ is less than 1, that is, if and only if every eigenvalue of $R$ lies in the open interval $(0, 2)$.

*Proof.* The update is the Jacobi method for $R x = z$, because the diagonal of $R$ is the identity. Let $e^{(m)} = x^{(m)} - R^{-1} z$. Since $R^{-1} z = z - (R - I) R^{-1} z$, subtracting gives $e^{(m)} = (I - R)\, e^{(m-1)}$, and $e^{(0)} = z - R^{-1} z = (I - R)(-R^{-1} z)$ gives the first formula. The second follows by unrolling the update. $R - I$ is symmetric, so $\|(I - R)^m v\|$ tends to 0 for every $v$ if and only if all its eigenvalues $\lambda_i(R) - 1$ have absolute value less than 1. $\square$

For the three users of the page, $R - I$ has the eigenvalues $0.5$ and $(-1 \pm \sqrt{3})/4$, so its spectral radius is $(1 + \sqrt 3)/4 \approx 0.683$, and the error shrinks by that factor at each stage. For three users with all correlations $0.6$, $R$ has the eigenvalue $2.2$, and linear PIC diverges.

**Remark (the cost).** Each stage computes $K$ sums of $K - 1$ terms, so $J$ stages cost $O(J K^2)$ after $z$ and $R$, which cost $O(K N)$ and $O(K^2 N)$. Done on $y$, a stage rebuilds the sum of the $K$ signals once and subtracts it, at $O(K N)$ per stage.
