---
title: The MMSE detector minimizes the mean square error, maximizes the SINR among linear detectors, and lies between the matched filter and the decorrelator
proves: [correctness]
status: full
---

The model is $y = S A b + w$ for one symbol interval. The matrix $S$ is $N \times K$, its column $s_k$ is the signature of user $k$ with $\|s_k\| = 1$, $A = \mathrm{diag}(A_1, \ldots, A_K)$ with $A_k > 0$, the bits $b_k \in \{-1, +1\}$ are independent and equally likely, and $w \sim \mathcal{N}(0, \sigma^2 I_N)$ with $\sigma > 0$. Let $R = S^\top S$ and $z = S^\top y = R A b + n$, with $n \sim \mathcal{N}(0, \sigma^2 R)$. Line L3 forms $G = R + \sigma^2 A^{-2}$, line L4 computes $x = G^{-1} z$, and line L5 decides $\hat b_k = \mathrm{sgn}(x_k)$.

**Lemma 1 (line L4 always succeeds).** For $\sigma > 0$, $G$ is symmetric positive definite, even when $R$ is singular.

*Proof.* $v^\top G v = \|S v\|^2 + \sigma^2 \sum_k v_k^2 / A_k^2$. The first term is at least 0 and the second is positive for $v \ne 0$. $\square$

**Theorem 1 (minimum mean square error).** For each user $k$, the linear filter $w_k = G^{-1} e_k / A_k$ on $z$ minimizes $E[(b_k - w^\top z)^2]$ over all $w \in \mathbb{R}^K$. The decision $\mathrm{sgn}(w_k^\top z)$ equals $\mathrm{sgn}(x_k)$.

*Proof.* The bits have $E[b b^\top] = I$ and are independent of $n$, so $E[z z^\top] = R A^2 R + \sigma^2 R$ and $E[z\, b_k] = R A e_k = A_k R e_k$. The mean square error $1 - 2 w^\top E[z b_k] + w^\top E[z z^\top] w$ is a convex quadratic in $w$, so $w$ is a minimizer if and only if it solves the normal equations $(R A^2 R + \sigma^2 R) w = A_k R e_k$. Note that $R A^2 R + \sigma^2 R = R A^2 (R + \sigma^2 A^{-2}) = R A^2 G$. For $w_k = G^{-1} e_k / A_k$,

$$R A^2 G\, G^{-1} e_k / A_k = R A^2 e_k / A_k = A_k R e_k,$$

so $w_k$ solves the normal equations. Since $G^{-1}$ is symmetric, $w_k^\top z = (G^{-1} z)_k / A_k = x_k / A_k$, and $A_k > 0$, so the signs agree. $\square$

**Theorem 2 (maximum SINR).** For a filter $w$ on $z$, the output for user $k$ is $w^\top z = (w^\top R e_k) A_k b_k + \sum_{j \ne k} (w^\top R e_j) A_j b_j + w^\top n$. Define its SINR as the ratio of the signal power to the power of the other two terms,

$$\mathrm{SINR}_k(w) = \frac{A_k^2 (w^\top R e_k)^2}{\sum_{j \ne k} A_j^2 (w^\top R e_j)^2 + \sigma^2 w^\top R w}.$$

Then $\mathrm{SINR}_k(w) \le A_k^2\, s_k^\top C_k^{-1} s_k$ for every $w$, where $C_k = \sigma^2 I + \sum_{j \ne k} A_j^2 s_j s_j^\top$, and $w_k$ attains the bound.

*Proof.* Put $v = S w$, so that $w^\top z = v^\top y$, $w^\top R e_j = v^\top s_j$ and $w^\top R w = \|v\|^2$. The denominator becomes $v^\top C_k v$ and the numerator $A_k^2 (v^\top s_k)^2$. The matrix $C_k$ is positive definite, so by the Cauchy-Schwarz inequality in the inner product of $C_k$,

$$(v^\top s_k)^2 = \big( (C_k^{1/2} v)^\top (C_k^{-1/2} s_k) \big)^2 \le (v^\top C_k v)(s_k^\top C_k^{-1} s_k),$$

with equality if and only if $v$ is a multiple of $C_k^{-1} s_k$. This proves the bound. For $w_k$, let $C = \sigma^2 I + S A^2 S^\top = C_k + A_k^2 s_k s_k^\top$. Then

$$C\, S w_k = (\sigma^2 S + S A^2 R)\, G^{-1} e_k / A_k = S A^2 (\sigma^2 A^{-2} + R)\, G^{-1} e_k / A_k = A_k s_k,$$

so $S w_k = A_k C^{-1} s_k$. By the [Sherman-Morrison formula](/sherman-morrison-formula/), $C^{-1} s_k = C_k^{-1} s_k / (1 + A_k^2 s_k^\top C_k^{-1} s_k)$, a positive multiple of $C_k^{-1} s_k$. So $v = S w_k$ attains equality. $\square$

**Theorem 3 (the two limits).** If $R$ is invertible, then $G^{-1} \to R^{-1}$ as $\sigma \to 0$, so the MMSE detector tends to the [decorrelating detector](/decorrelating-detector/). For any $R$, $\sigma^2 G^{-1} \to A^2$ as $\sigma \to \infty$. So, for a fixed $z$ with no zero entry, the MMSE decisions equal the matched filter decisions $\mathrm{sgn}(z_k)$ once $\sigma$ is large enough.

*Proof.* Matrix inversion is continuous on the invertible matrices. $G = R + \sigma^2 A^{-2} \to R$ as $\sigma \to 0$. For the second limit, $\sigma^2 G^{-1} = (\sigma^{-2} R + A^{-2})^{-1} \to (A^{-2})^{-1} = A^2$. Then $\sigma^2 x = \sigma^2 G^{-1} z \to A^2 z$, whose entries $A_k^2 z_k$ have the signs of $z_k$. Each entry of $\sigma^2 x$ converges, so its sign is that of the limit once $\sigma$ is large enough. $\square$

**Theorem 4 (the exact error rate).** With $u = R w$, the error probability of user $k$ under the decision $\mathrm{sgn}(w^\top z)$ is

$$P_k = 2^{-(K-1)} \sum_{b:\, b_k = +1} Q\Big( \frac{\sum_j u_j A_j b_j}{\sigma \sqrt{w^\top R w}} \Big),$$

the sum running over the $2^{K-1}$ choices of the other bits.

*Proof.* Given $b$, $w^\top z$ is Gaussian with mean $u^\top A b$ and variance $\sigma^2 w^\top R w$. By symmetry under $b \to -b$, the error probability for $b_k = -1$ equals that for $b_k = +1$, and given $b_k = +1$ the decision errs when $w^\top z < 0$. Average over the other bits. $\square$

Unlike the decorrelator, the MMSE output still holds some interference, so its error rate depends on the other amplitudes. Theorem 2 is a statement about SINR, not about the error rate: the residual interference is not Gaussian, and the MMSE detector does not minimize the error probability in general.

**Remark (the cost).** Line L1 costs $O(K N)$, line L2 costs $O(K^2 N)$ and line L4 costs $O(K^3)$. When the signatures, the amplitudes and $\sigma$ do not change, $G^{-1}$ is computed once and each interval costs $O(K N + K^2)$.
