---
title: The Guttman transform never increases the raw stress
proves: [correctness]
status: full
---

We take unit weights. Let $A_{ij} = (e_i - e_j)(e_i - e_j)^\top$ for $i < j$, so that $d_{ij}(X)^2 = \operatorname{tr}(X^\top A_{ij} X)$, and let $V = \sum_{i<j} A_{ij} = nI - \mathbf{1}\mathbf{1}^\top$. Write $\eta_\delta^2 = \sum_{i<j}\delta_{ij}^2$ and $\rho(X) = \sum_{i<j}\delta_{ij}d_{ij}(X)$. A matrix is *centered* when its columns sum to zero. For a centered $X$, $VX = nX$.

**Lemma 1 (expansion).** $\sigma(X) = \eta_\delta^2 + \operatorname{tr}(X^\top V X) - 2\rho(X)$.

*Proof.* Expand $(d_{ij} - \delta_{ij})^2 = \delta_{ij}^2 + d_{ij}^2 - 2\delta_{ij}d_{ij}$ and sum over $i < j$, using $\sum_{i<j} d_{ij}^2 = \operatorname{tr}(X^\top V X)$. $\square$

**Lemma 2 (a linear lower bound of $\rho$).** For all $X$ and $Z$, $\rho(X) \ge \operatorname{tr}(X^\top B(Z) Z)$, with equality when $X = Z$.

*Proof.* By the definition of $B(Z)$ in lines L4 and L5, $B(Z) = \sum_{i<j} s_{ij} A_{ij}$ with $s_{ij} = \delta_{ij}/d_{ij}(Z)$ when $d_{ij}(Z) > 0$ and $s_{ij} = 0$ otherwise. So $\operatorname{tr}(X^\top B(Z) Z) = \sum_{i<j} s_{ij}(x_i - x_j)^\top(z_i - z_j)$. For a pair with $d_{ij}(Z) > 0$, the Cauchy-Schwarz inequality gives $(x_i - x_j)^\top(z_i - z_j) \le d_{ij}(X)\,d_{ij}(Z)$, so the term is at most $\delta_{ij}d_{ij}(X)$, because $\delta_{ij} \ge 0$. For a pair with $d_{ij}(Z) = 0$, the term is $0 \le \delta_{ij}d_{ij}(X)$. Summing gives the inequality. If $X = Z$, each term with $d_{ij}(Z) > 0$ equals $\delta_{ij}d_{ij}(Z)$, and each term with $d_{ij}(Z) = 0$ equals $0 = \delta_{ij}d_{ij}(Z)$. $\square$

**Lemma 3 (the majorizer).** Let $\tau(X, Z) = \eta_\delta^2 + \operatorname{tr}(X^\top V X) - 2\operatorname{tr}(X^\top B(Z) Z)$. Then $\sigma(X) \le \tau(X, Z)$ for all $X$, and $\sigma(Z) = \tau(Z, Z)$.

*Proof.* Combine Lemma 1 and Lemma 2. $\square$

**Lemma 4 (the minimum of the majorizer).** Let $Z$ be centered and $X^+ = \frac1n B(Z)Z$. Then $X^+$ is centered, and for each centered $X$,

$$\tau(X, Z) = \eta_\delta^2 + n\|X - X^+\|_F^2 - n\|X^+\|_F^2 .$$

*Proof.* The rows of $B(Z)$ sum to zero by line L5, and $B(Z)$ is symmetric, so $\mathbf{1}^\top B(Z) = 0$ and $\mathbf{1}^\top X^+ = 0$. For a centered $X$, $\operatorname{tr}(X^\top V X) = n\|X\|_F^2$, and $\operatorname{tr}(X^\top B(Z)Z) = n\operatorname{tr}(X^\top X^+)$. So $\tau(X, Z) = \eta_\delta^2 + n\|X\|_F^2 - 2n\operatorname{tr}(X^\top X^+)$, and completing the square gives the claim. $\square$

**Theorem (sandwich inequality).** Let $Z$ be centered and $X^+ = \frac1n B(Z)Z$. Then

$$\sigma(X^+) \le \sigma(Z) - n\|Z - X^+\|_F^2 \le \sigma(Z).$$

*Proof.* By Lemma 3, $\sigma(X^+) \le \tau(X^+, Z)$ and $\sigma(Z) = \tau(Z, Z)$. By Lemma 4 applied to $X = X^+$ and to $X = Z$, $\tau(Z, Z) - \tau(X^+, Z) = n\|Z - X^+\|_F^2$. Combine the two. $\square$

**Corollary.** Line L1 centers $X_0$, and by Lemma 4 each Guttman transform of a centered configuration is centered. So the theorem applies at each iteration, and the stress values $\sigma(X_0) \ge \sigma(X_1) \ge \cdots$ are non-increasing and bounded below by 0, hence convergent. Summing the theorem over the iterations gives $n\sum_{t \ge 0}\|X_t - X_{t+1}\|_F^2 \le \sigma(X_0)$, so the step lengths tend to 0. A strict decrease happens at each step that changes the configuration. The loop of lines L2 to L9 therefore stops for any $\varepsilon > 0$: the decreases are non-negative, and their sum is at most $\sigma(X_0)$, so at most $\sigma(X_0)/\varepsilon$ iterations have a decrease of at least $\varepsilon$, and the first iteration with a smaller decrease returns at line L8.

**Fixed points.** If $d_{ij}(X) = \delta_{ij} > 0$ for all $i \ne j$, then $b_{ij} = -1$ for $i \ne j$ and $b_{ii} = n - 1$, so $B(X) = V$ and $\frac1n B(X) X = \frac1n VX = X$ for a centered $X$. The stress is then 0, its global minimum.

**Relation to the gradient.** Where all $d_{ij}(X) > 0$, the gradient of $\sigma$ is $\nabla\sigma(X) = 2VX - 2B(X)X$, because the gradient of $\operatorname{tr}(X^\top V X)$ is $2VX$ and the gradient of $d_{ij}(X)$ is $A_{ij}X/d_{ij}(X)$, so the gradient of $\rho$ is $\sum_{i<j}\delta_{ij}A_{ij}X/d_{ij}(X) = B(X)X$. For a centered $X$ this is $2nX - 2B(X)X$, so $X^+ = X - \frac{1}{2n}\nabla\sigma(X)$. A fixed point with positive distances is therefore a stationary point of $\sigma$. It can still be a local minimum that is not global, or a saddle point.
