---
title: The SISO MMSE equalizer computes the linear MMSE estimate under the prior model, its output is extrinsic, and its LLR is exact for the Gaussian model of the estimate
proves: [correctness]
status: full
---

**Setting.** For symbol $n$, the window is $Y = H X + w$, with $H$ of size $W \times (W + L - 1)$, $w \sim N(0, \sigma^2 I)$ independent of $X$, and $\sigma^2 > 0$. Column $j_0 = N_2 + L - 1$ of $H$ is $s$, and $X_{j_0} = x_n$. The **prior model** $\mathcal M$ says: the entries of $X$ are independent; $x_n$ has mean 0 and variance 1; every other entry $X_j$ has mean $\bar X_j$ and variance $V_{jj}$, from line L1, or mean 0 and variance 0 if it lies outside the block. Let $\bar X'$ be $\bar X$ with entry $j_0$ set to 0, and $V'$ be $V$ with entry $j_0$ set to 1.

**Lemma 1 (the moments of the window).** Under $\mathcal M$, $E[Y] = H \bar X' = H \bar X - \bar x_n s$, $\mathrm{Cov}(Y) = H V' H^T + \sigma^2 I$, which is the matrix $C$ of line L4, and $\mathrm{Cov}(Y, x_n) = s$.

*Proof.* $E[Y] = H E[X] = H \bar X'$, and $H \bar X' = H \bar X - \bar x_n H e_{j_0} = H \bar X - \bar x_n s$. The entries of $X$ are independent, so $\mathrm{Cov}(X) = V'$, and $w$ is independent of $X$, so $\mathrm{Cov}(Y) = H V' H^T + \sigma^2 I$. Now $V' = V + (1 - v_n) e_{j_0} e_{j_0}^T$, so $H V' H^T = H V H^T + (1 - v_n) s s^T$, which is line L4. Last, $\mathrm{Cov}(Y, x_n) = H\, \mathrm{Cov}(X, x_n) = H e_{j_0} \cdot 1 = s$. $\square$

**Theorem 1 (linear MMSE).** Among all estimates $a + g^T Y$, the one with the least $E_{\mathcal M}(x_n - a - g^T Y)^2$ is $\hat x = f^T (Y - E Y)$ with $f = C^{-1} s$, which is line L6.

*Proof.* $C \succeq \sigma^2 I \succ 0$, so $C$ is invertible. Write the error as $x_n - a - g^T Y$. Its mean square is $(E x_n - a - g^T E Y)^2 + \mathrm{Var}(x_n - g^T Y)$. The first term is 0 for $a = -g^T E Y$, since $E x_n = 0$. The second is $1 - 2 g^T s + g^T C g$, a strictly convex quadratic in $g$ with gradient $2(C g - s)$, which is zero only at $g = C^{-1} s = f$. So $\hat x = f^T (Y - E Y)$, and by Lemma 1, $Y - E Y = Y - H \bar X + \bar x_n s$. $\square$

**Theorem 2 (extrinsic).** $L_e(x_n)$ does not depend on $L_a(x_n)$.

*Proof.* $L_a(x_n)$ enters only through $\bar x_n$ and $v_n$. By Lemma 1, $C = H V' H^T + \sigma^2 I$, and $V'$ does not contain $v_n$. The vector $Y - H \bar X + \bar x_n s = Y - H \bar X'$, and $\bar X'$ does not contain $\bar x_n$. So $f$, $\hat x$, $\mu$ and $L_e(x_n)$ do not depend on $L_a(x_n)$. $\square$

**Lemma 2 ($0 \le \mu < 1$).** Let $D = C - s s^T = H V'' H^T + \sigma^2 I$, where $V''$ is $V'$ with entry $j_0$ set to 0. Then $D \succ 0$, and with $\alpha = s^T D^{-1} s \ge 0$, $\mu = s^T C^{-1} s = \alpha / (1 + \alpha)$.

*Proof.* $D \succeq \sigma^2 I \succ 0$. By the Sherman-Morrison formula, $C^{-1} s = (D + s s^T)^{-1} s = D^{-1} s / (1 + \alpha)$, so $\mu = s^T C^{-1} s = \alpha / (1 + \alpha) \in [0, 1)$. $\square$

**Theorem 3 (the conditional moments).** Under $\mathcal M$ and given $x_n = b \in \{+1, -1\}$, $E[\hat x \mid x_n = b] = \mu b$ and $\mathrm{Var}[\hat x \mid x_n = b] = \mu - \mu^2$.

*Proof.* Given $x_n = b$, $Y - E Y = b s + H (X' - \bar X') + w$, where $X'$ is $X$ with entry $j_0$ set to 0. The last two terms have mean 0 and covariance $H V'' H^T + \sigma^2 I = D$. So $E[\hat x \mid b] = b f^T s = \mu b$ and $\mathrm{Var}[\hat x \mid b] = f^T D f = f^T (C - s s^T) f = f^T s - (f^T s)^2 = \mu - \mu^2$, using $C f = s$. $\square$

**Theorem 4 (the LLR of the Gaussian model).** If $\hat x \mid x_n = b$ is modeled as $N(\mu b, \mu - \mu^2)$ and $0 < \mu < 1$, then $\ln p(\hat x \mid b = +1) / p(\hat x \mid b = -1) = 2 \hat x / (1 - \mu)$, which is line L8.

*Proof.* The two Gaussians have the same variance $\tau^2 = \mu (1 - \mu)$, so the log ratio is $((\hat x + \mu)^2 - (\hat x - \mu)^2) / (2 \tau^2) = 4 \mu \hat x / (2 \mu (1 - \mu)) = 2 \hat x / (1 - \mu)$. With $x = 1 - 2b$, $x_n = +1$ is $b = 0$, so this is the LLR in the sign convention $\ln P(b = 0) / P(b = 1)$. $\square$

**What is not proved.** Theorem 3 gives the true first two moments under $\mathcal M$, but $\hat x$ given $x_n$ is a mixture over the other symbols plus Gaussian noise. It is Gaussian only when no residual symbol variance reaches the output, that is, when $H V'' H^T = 0$ on the support of $f$. Then $L_e$ is the true extrinsic LLR of $\hat x$. Otherwise the Gaussian model is a heuristic. The prior model $\mathcal M$ is also a heuristic inside a turbo loop: the decoder outputs are not independent, and they are not exact. So the equalizer is not the MAP equalizer.

**Two closed forms.** If every prior is 0, then $\bar X = 0$, $V' = I$ and $f = (H H^T + \sigma^2 I)^{-1} s$, the MMSE linear equalizer for the delay $N_2$. If every prior is perfect, then $V'' = 0$, $D = \sigma^2 I$, $\alpha = \|s\|^2 / \sigma^2$, $f = s / (\sigma^2 + \|s\|^2)$, $1 - \mu = \sigma^2 / (\sigma^2 + \|s\|^2)$ and $L_e(x_n) = 2 s^T (Y - H \bar X') / \sigma^2$. Here $\hat x$ given $x_n$ is exactly Gaussian, so this is the true LLR. The tests check both forms and an enumeration of Theorem 1 and Theorem 3 to $10^{-9}$.
