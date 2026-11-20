---
title: RZF meets the power constraint, minimizes the sum MSE with a common receive scale, and tends to zero forcing and to matched beams at its two limits
proves: [correctness]
status: full
---

The model is $y_k = h_k^H x + w_k$ for $k = 1, \ldots, K$, with $H = [h_1, \ldots, h_K]^H \in \mathbb{C}^{K \times M}$, $w \sim \mathcal{CN}(0, N_0 I_K)$, $x = W s$ and $E[s s^H] = I_K$. Lines L1 to L5 compute $\alpha = K N_0 / P$, $F = H^H (H H^H + \alpha I)^{-1}$, $\beta = \sqrt{P / \|F\|_F^2}$ and $W = \beta F$. Each user scales its sample by $1/\beta$.

**Lemma 1 (push-through identity).** For $\alpha > 0$, both $H H^H + \alpha I_K$ and $H^H H + \alpha I_M$ are positive definite, and $H^H (H H^H + \alpha I_K)^{-1} = (H^H H + \alpha I_M)^{-1} H^H$.

*Proof.* For $u \ne 0$, $u^H (H H^H + \alpha I) u = \|H^H u\|^2 + \alpha \|u\|^2 > 0$, and the same holds for the other matrix. Then $(H^H H + \alpha I) H^H = H^H H H^H + \alpha H^H = H^H (H H^H + \alpha I)$. Multiply on the left by $(H^H H + \alpha I)^{-1}$ and on the right by $(H H^H + \alpha I)^{-1}$. $\square$

**Theorem 1 (power).** $\mathrm{tr}(W^H W) = P$.

*Proof.* $\mathrm{tr}(W^H W) = \beta^2 \|F\|_F^2 = P$. Here $F \ne 0$ if $H \ne 0$, because $H F = H H^H (H H^H + \alpha I)^{-1}$ has the positive eigenvalues $\lambda_i / (\lambda_i + \alpha)$ for the positive eigenvalues $\lambda_i$ of $H H^H$. $\square$

**Lemma 2 (the MSE of a scaled precoder).** For $W = \beta F$ with $\beta = \sqrt{P / \|F\|_F^2}$, the sum MSE with the common receive scale $1/\beta$ is

$$E\|s - \beta^{-1} y\|^2 = \|I_K - H F\|_F^2 + \frac{K N_0}{P} \|F\|_F^2.$$

*Proof.* $\beta^{-1} y = H F s + \beta^{-1} w$, so $s - \beta^{-1} y = (I - H F) s - \beta^{-1} w$. The two terms are independent with zero mean, so the MSE is $\mathrm{tr}((I - H F)(I - H F)^H) + \beta^{-2} K N_0$, and $\beta^{-2} = \|F\|_F^2 / P$. $\square$

The right side does not change when $F$ is multiplied by a positive scalar together with the matching $\beta$. So minimizing it over $F$ is the same as minimizing the MSE over all pairs $(W, \beta)$ with $\mathrm{tr}(W^H W) = P$.

**Theorem 2 (the transmit Wiener filter).** The function $J(F) = \|I - H F\|_F^2 + \alpha \|F\|_F^2$ with $\alpha = K N_0 / P$ has the unique minimizer $F^\star = H^H (H H^H + \alpha I)^{-1}$, and the minimum is $J(F^\star) = \alpha\, \mathrm{tr}\bigl((H H^H + \alpha I)^{-1}\bigr)$.

*Proof.* $J$ is a sum of $K$ independent problems, one for each column $f_k$ of $F$: $J = \sum_k \bigl(\|e_k - H f_k\|^2 + \alpha \|f_k\|^2\bigr)$. Each is a [Tikhonov regularization](/tikhonov-regularization/) problem. Expand it as $f_k^H (H^H H + \alpha I) f_k - 2 \mathrm{Re}(f_k^H H^H e_k) + 1$. The quadratic form is positive definite by Lemma 1, so the function is strictly convex, and its unique minimizer is the zero of the gradient, $(H^H H + \alpha I) f_k = H^H e_k$. So $F^\star = (H^H H + \alpha I)^{-1} H^H$, which is $H^H (H H^H + \alpha I)^{-1}$ by Lemma 1. For the value, let $A = H H^H + \alpha I$. Then $I - H F^\star = I - H H^H A^{-1} = \alpha A^{-1}$, and

$$J(F^\star) = \alpha^2 \mathrm{tr}(A^{-2}) + \alpha\, \mathrm{tr}(A^{-1} H H^H A^{-1}) = \alpha\, \mathrm{tr}\bigl(A^{-1} (\alpha I + H H^H) A^{-1}\bigr) = \alpha\, \mathrm{tr}(A^{-1}). \ \square$$

So, by Lemma 2 and the remark after it, the RZF precoder of lines L1 to L6 minimizes the sum MSE over all linear precoders with power $P$ and a common receive scale. This is the transmit Wiener filter of Joham, Utschick and Nossek (2005).

**Theorem 3 (the two limits).** Let $H$ have full row rank. As $\alpha \to 0$, $W$ tends to $\sqrt{P / \mathrm{tr}((H H^H)^{-1})}\, H^H (H H^H)^{-1}$, the zero-forcing precoder with the channel inversion power rule, so $H W$ tends to a multiple of $I$. As $\alpha \to \infty$, $W$ tends to $\sqrt{P / \|H\|_F^2}\, H^H$, a matched beam $h_k$ for each user with the power share $\|h_k\|^2 / \|H\|_F^2$.

*Proof.* $W$ does not change when $F$ is multiplied by a positive scalar. As $\alpha \to 0$, $F \to H^H (H H^H)^{-1}$ by continuity of the inverse at the invertible matrix $H H^H$. As $\alpha \to \infty$, $\alpha F = H^H (H H^H / \alpha + I)^{-1} \to H^H$. In both cases the normalization by $\beta$ gives the stated limits. $\square$

The tests check Theorem 1 within $10^{-9}$, Theorem 2 by the zero gradient (the KKT condition of the unconstrained problem), by random perturbations of $F$, by a grid search over each column of $F$ for real $2 \times 2$ channels and by the closed form of the minimum, Theorem 3 at $\alpha = 10^{-10}$ and $\alpha = 10^{10}$, and the example values of the page.
