---
title: The Kalman filter is the best linear estimator, and the exact posterior for Gaussian noise
proves: [correctness]
status: full
---

**Model.** For $t \ge 1$, $x_t = A x_{t-1} + q_t$ and $y_t = C x_t + r_t$, where $x_0, q_1, q_2, \ldots, r_1, r_2, \ldots$ are random vectors with finite second moments, $E[x_0] = m_0$, $\operatorname{Cov}(x_0) = P_0$, $E[q_t] = 0$, $\operatorname{Cov}(q_t) = Q$, $E[r_t] = 0$, $\operatorname{Cov}(r_t) = R$ positive definite, and all of them are mutually uncorrelated. We work in exact real arithmetic, as in the real RAM.

**Notation.** Let $H_s$ be the set of random variables of the form $b + \sum_{i=1}^{s} B_i y_i$ with constant $b$ and $B_i$, the affine functions of the data $y_1, \ldots, y_s$; $H_0$ is the constants. For a random vector $z$, let $\hat E[z \mid H_s]$ be its orthogonal projection onto $H_s$, entry by entry, in the inner product $\langle a, b \rangle = E[a b]$. It is the affine function of the data with the least mean-square error, and it is characterized by: $\hat z \in H_s$ and $E[(z - \hat z)\, h] = 0$ for every scalar $h \in H_s$. Let $m_t$ and $P_t$ be the values of lines L8 and L9 at time $t$, with $m$ read as the same affine function of the data; $m_0$ and $P_0$ are the values of line L1.

**Lemma 1 (adding an orthogonal piece).** Let $v$ be a random vector with zero mean, positive definite covariance $S$, and $E[v\, h] = 0$ for every $h \in H_{t-1}$, such that $H_t$ is spanned by $H_{t-1}$ and the entries of $v$. Then for any $z$, $\hat E[z \mid H_t] = \hat E[z \mid H_{t-1}] + E[z v^T] S^{-1} v$.

*Proof.* Call the right side $\hat z$; it lies in $H_t$. For $h \in H_{t-1}$, $E[(z - \hat z) h] = E[(z - \hat E[z \mid H_{t-1}]) h] - E[z v^T] S^{-1} E[v h] = 0 - 0$. For the entries of $v$, $E[(z - \hat z) v^T] = E[z v^T] - E[\hat E[z \mid H_{t-1}]\, v^T] - E[z v^T] S^{-1} E[v v^T] = E[z v^T] - 0 - E[z v^T] = 0$, because $\hat E[z \mid H_{t-1}] \in H_{t-1}$. The error is orthogonal to a spanning set of $H_t$, so $\hat z$ is the projection. $\square$

**Theorem 1 (best linear estimator).** For every $t \ge 0$, $m_t = \hat E[x_t \mid H_t]$ and $P_t = E[(x_t - m_t)(x_t - m_t)^T]$.

*Proof.* By induction on $t$. For $t = 0$, the projection onto the constants is $E[x_0] = m_0$, with error covariance $P_0$. Assume the claim for $t - 1$, and write $e = x_{t-1} - m_{t-1}$.

*Prediction (lines L3 and L4).* The data $y_1, \ldots, y_{t-1}$ and $x_{t-1}$ are affine functions of $x_0, q_1, \ldots, q_{t-1}, r_1, \ldots, r_{t-1}$, so $q_t$ is uncorrelated with them and with every element of $H_{t-1}$, and it has zero mean. Hence $\hat E[q_t \mid H_{t-1}] = 0$ and, by linearity of the projection, $m^- := \hat E[x_t \mid H_{t-1}] = A m_{t-1}$, line L3. The error is $x_t - m^- = A e + q_t$, and $E[e\, q_t^T] = 0$, so its covariance is $A P_{t-1} A^T + Q = P^-$, line L4.

*Innovation (lines L5 and L6).* In the same way $r_t$ is uncorrelated with $x_t$ and with $H_{t-1}$, so $\hat E[y_t \mid H_{t-1}] = C m^-$ and $v = y_t - C m^- = C (x_t - m^-) + r_t$, line L5. It has zero mean, it is orthogonal to $H_{t-1}$ by the property of projections, and $H_t$ is spanned by $H_{t-1}$ and the entries of $v$, since $y_t = v + C m^-$ with $C m^- \in H_{t-1}$. Its covariance is $S = C P^- C^T + R$, line L6, because $x_t - m^-$ and $r_t$ are uncorrelated. $S$ is positive definite since $R$ is.

*Update (lines L7 to L9).* By Lemma 1, $m_t = m^- + E[x_t v^T] S^{-1} v$. Since $m^- \in H_{t-1}$ is orthogonal to $v$, $E[x_t v^T] = E[(x_t - m^-) v^T] = E[(x_t - m^-)(x_t - m^-)^T] C^T + E[(x_t - m^-) r_t^T] = P^- C^T$. So $m_t = m^- + K v$ with $K = P^- C^T S^{-1}$, lines L7 and L8. The new error is $x_t - m_t = (x_t - m^-) - K v$, and with $E[(x_t - m^-) v^T] = P^- C^T = K S$,

$$E[(x_t - m_t)(x_t - m_t)^T] = P^- - K S K^T - K S K^T + K S K^T = P^- - K S K^T,$$

which is line L9. $\square$

**Theorem 2 (exact posterior).** If moreover $x_0, q_1, \ldots, q_t, r_1, \ldots, r_t$ are independent Gaussian vectors, then the conditional law of $x_t$ given $y_1, \ldots, y_t$ is $\mathcal N(m_t, P_t)$.

*Proof.* Then $(x_t, y_1, \ldots, y_t)$ is a linear function of a Gaussian vector, so the error $x_t - m_t$ and the data are jointly Gaussian. By Theorem 1 the error is uncorrelated with every $y_i$ and has zero mean, as $1 \in H_t$; uncorrelated jointly Gaussian vectors are independent. So given the data, $x_t = m_t + (x_t - m_t)$ is the constant $m_t$ plus an independent $\mathcal N(0, P_t)$ vector. $\blacksquare$

**Remarks.** Theorem 1 does not use Gaussianity: for any noise with these first and second moments, $m_t$ is the affine estimate of least mean-square error, and $P_t$ is its exact error covariance, but a nonlinear function of the data can do better. The matrices $P^-$, $S$, $K$ and $P_t$ do not depend on the data, so they can be computed in advance. Theorem 2 is the same statement as direct conditioning of the joint Gaussian of $(x_t, y_1, \ldots, y_t)$ by the [Schur complement](/schur-complement/), and the tests check this equality exactly in fractions.
