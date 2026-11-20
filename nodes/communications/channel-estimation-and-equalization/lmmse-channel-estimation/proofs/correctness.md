---
title: The LMMSE channel estimate minimizes the mean squared error over all linear estimators, and its two forms and its error covariance agree
proves: [correctness]
status: full
---

Write $X$ for the $m \times L$ pilot matrix of line L1 and $v$ for the samples of line L2. The model is

$$v = X h + w, \tag{1}$$

where $h$ has mean zero and covariance $R = R_h = E[h h^H]$, which is Hermitian and positive semidefinite, and $w$ has mean zero and covariance $N_0 I$ with $N_0 > 0$, and is uncorrelated with $h$. Let $G = X^H X$ and

$$K = E[v v^H] = X R X^H + N_0 I.$$

$K$ is Hermitian and positive definite, because $z^H K z = (X^H z)^H R (X^H z) + N_0 \|z\|^2 \ge N_0 \|z\|^2$. We also need $E[h v^H] = E[h (X h + w)^H] = R X^H$.

**Lemma 1 (the error of a linear estimator).** For any $L \times m$ matrix $W$, the estimate $W v$ has the mean squared error

$$J(W) = E\|W v - h\|^2 = \operatorname{tr}(W K W^H) - 2 \operatorname{Re} \operatorname{tr}(W X R) + \operatorname{tr}(R).$$

*Proof.* $E\|W v - h\|^2 = \operatorname{tr} E[(W v - h)(W v - h)^H] = \operatorname{tr}(W K W^H - W X R - R X^H W^H + R)$, and $\operatorname{tr}(R X^H W^H) = \overline{\operatorname{tr}(W X R)}$, because $R$ is Hermitian. $\square$

**Theorem 1 (the best linear estimator).** Let $W_\ast = R X^H K^{-1}$. Then

$$J(W) = J(W_\ast) + \operatorname{tr}\big((W - W_\ast) K (W - W_\ast)^H\big)$$

for every $W$. So $W_\ast$ is the unique linear estimator with the smallest mean squared error, and the error $W_\ast v - h$ is uncorrelated with $v$ (the orthogonality principle).

*Proof.* Put $D = W - W_\ast$ in Lemma 1. Since $W_\ast K = R X^H$, the cross terms are $\operatorname{tr}(D K W_\ast^H) = \operatorname{tr}(D X R)$ and its conjugate, so

$$J(W) = J(W_\ast) + \operatorname{tr}(D K D^H) + 2 \operatorname{Re} \operatorname{tr}(D X R) - 2 \operatorname{Re} \operatorname{tr}(D X R).$$

The last two terms cancel. $K$ is positive definite, so $\operatorname{tr}(D K D^H) = \sum_i d_i^H K d_i \ge 0$ over the rows $d_i^H$ of $D$, with equality if and only if $D = 0$. Finally, $E[(W_\ast v - h) v^H] = W_\ast K - R X^H = 0$. $\square$

**Lemma 2 (the form of lines L3 to L6).** $A = R G + N_0 I$ is invertible, and $W_\ast = A^{-1} R X^H$. So line L6 returns $\hat h = A^{-1} R X^H v = W_\ast v$.

*Proof.* Let $\mu$ be an eigenvalue of $R G$ with eigenvector $z \ne 0$. Then $G z \ne 0$ when $\mu \ne 0$, and $(G z)^H R G z = \mu\, z^H G z$, which shows $\mu \ge 0$ because both quadratic forms are real and nonnegative and $z^H G z > 0$ if $G z \ne 0$. So every eigenvalue of $A$ is at least $N_0 > 0$, and $A$ is invertible. Next,

$$A R X^H = R X^H X R X^H + N_0 R X^H = R X^H (X R X^H + N_0 I) = R X^H K.$$

Multiply on the left by $A^{-1}$ and on the right by $K^{-1}$: $R X^H K^{-1} = A^{-1} R X^H$. $\square$

This form needs an $L \times L$ solve instead of an $m \times m$ inverse, and it does not need $R^{-1}$, so a singular $R$ is allowed. A zero row of $R$ gives a zero row of $R X^H$, and so the estimate of a tap that is known to be zero is exactly zero.

**Theorem 2 (the error covariance).** The error $e = \hat h - h$ has mean zero and covariance

$$C_e = N_0 (R G + N_0 I)^{-1} R,$$

which equals $(R^{-1} + G/N_0)^{-1}$ when $R$ is invertible. The mean squared error is $\operatorname{tr}(C_e)$.

*Proof.* $E[e] = W_\ast X E[h] + W_\ast E[w] - E[h] = 0$. By the orthogonality of Theorem 1, $E[e v^H] = 0$, so $C_e = E[e (W_\ast v - h)^H] = -E[e h^H] = R - W_\ast X R$. With Lemma 2,

$$C_e = R - A^{-1} R G R = A^{-1}(A R - R G R) = A^{-1} (R G R + N_0 R - R G R) = N_0 A^{-1} R.$$

If $R$ is invertible, $N_0 A^{-1} R = N_0 (R^{-1} A)^{-1} = N_0 (G + N_0 R^{-1})^{-1} = (R^{-1} + G/N_0)^{-1}$. $\square$

**Corollary 1 (LMMSE is at least as good as LS).** If $G$ is invertible, $\operatorname{tr}(C_e) \le N_0 \operatorname{tr}(G^{-1})$, the error of the LS estimate.

*Proof.* The LS estimate $G^{-1} X^H v$ is a linear estimator $W_{LS} v$. It is unbiased for every fixed $h$, with error covariance $N_0 G^{-1}$, so its mean squared error averaged over $h$ is also $N_0 \operatorname{tr}(G^{-1})$. By Theorem 1 this is at least $J(W_\ast) = \operatorname{tr}(C_e)$. $\square$

**Corollary 2 (the limits).** If $R$ and $G$ are invertible, then $W_\ast \to G^{-1} X^H$, the LS estimator, as $N_0 \to 0$. As $N_0 \to \infty$, $W_\ast \to 0$ and the estimate falls back to the prior mean.

*Proof.* $W_\ast = (R G + N_0 I)^{-1} R X^H$ is continuous in $N_0$ near $0$ because $R G$ is invertible, and at $N_0 = 0$ it is $(R G)^{-1} R X^H = G^{-1} X^H$. For large $N_0$, $W_\ast = N_0^{-1} (R G / N_0 + I)^{-1} R X^H \to 0$. $\square$

**Theorem 3 (Gaussian channel and noise).** If $h$ and $w$ are jointly Gaussian and independent, then $\hat h = E[h \mid v]$, so the LMMSE estimate has the smallest mean squared error among all estimators, linear or not.

*Proof.* The pair $(e, v)$ is a linear function of the Gaussian vector $(h, w)$, so it is jointly Gaussian. By Theorem 1, $e$ and $v$ are uncorrelated, and uncorrelated jointly Gaussian vectors are independent. So $E[e \mid v] = E[e] = 0$, and $E[h \mid v] = E[W_\ast v - e \mid v] = W_\ast v$. The conditional mean minimizes the mean squared error over all functions of $v$. $\square$

**Remark (nonzero mean).** If $E[h] = \bar h$, apply the result to $h - \bar h$ and $v - X \bar h$: $\hat h = \bar h + W_\ast (v - X \bar h)$, with the same error covariance.

**Remark (the cost).** Lines L1 and L2 copy $O(m L)$ numbers. Line L3 costs $m L^2 + m L$ multiplications, line L4 costs $L^3$, line L5 costs $L^2$ and the solve of line L6 costs $O(L^3)$. The total is $O(m L^2 + L^3)$ per pilot block. If $X$, $R$ and $N_0$ do not change, $W_\ast$ is computed once, and each estimate costs $m L$ multiplications, the same as LS.
