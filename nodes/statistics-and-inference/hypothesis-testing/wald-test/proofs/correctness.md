---
title: The Wald test returns the quadratic form of the estimate error, the closed forms are correct, and its size tends to alpha under the regularity conditions of MLE asymptotics
proves: [correctness, termination]
status: full
---

We prove that WALD-TEST returns $W = d^\top \hat V^{-1} d$ with $d = \hat\theta - \theta_0$, that $W \ge 0$ when $\hat V$ is positive definite, that the closed forms of the table are this quadratic form, and that $W \to \chi^2_r$ under $H_0$ whenever the estimate is asymptotically normal and $\hat V$ is consistent, so the size of the test tends to $\alpha$. The asymptotic normality of the MLE is proved on its own page and is used here as a hypothesis. Finite-sample sizes are not proved; they are computed by enumeration in the tests.

**Lemma 1 (the solve).** If $\hat V$ is nonsingular, Gaussian elimination with partial pivoting in exact arithmetic returns the unique $y$ with $\hat V y = d$. So line L3 returns $W = d^\top \hat V^{-1} d$.

*Proof.* Each elimination step swaps two rows of the augmented matrix $[\hat V \mid d]$ or subtracts a multiple of one row from a later row. Both operations are invertible and keep the solution set of the system. At step $c$, the pivot is the entry of largest absolute value in column $c$ at or below row $c$. If it were 0, the first $c$ columns of the current matrix would have rank below $c$, and $\hat V$ would be singular; so for nonsingular $\hat V$ every pivot is nonzero. After $r$ steps the matrix is upper triangular with nonzero diagonal, and back substitution gives the unique solution. $\square$

With Fraction inputs every operation is exact, so the returned $W$ is exactly $d^\top \hat V^{-1} d$; the tests check this against the inverse by cofactors. With floating point inputs, partial pivoting makes the solve backward stable: the computed $y$ solves $(\hat V + E)y = d$ with $\|E\|$ a small multiple of the unit roundoff times $\|\hat V\|$, for matrices of the sizes used here.

**Lemma 2 (sign).** If $\hat V$ is symmetric positive definite, then $W \ge 0$, with equality only if $d = 0$.

*Proof.* $\hat V^{-1}$ is symmetric positive definite, since its eigenvalues are the reciprocals of those of $\hat V$. So $d^\top \hat V^{-1} d > 0$ for $d \ne 0$. $\square$

So a negative $W$ shows that $\hat V$ is not positive definite, and the implementation raises an error in that case.

**Lemma 3 (closed forms).** The one-parameter formulas of the table equal $(\hat\theta - \theta_0)^2/\widehat{\operatorname{Var}}(\hat\theta)$ with the MLE and the inverse Fisher information evaluated at the MLE.

*Proof.* Binomial: $\ell(p) = k\log p + (n - k)\log(1 - p)$, the MLE is $\hat p = k/n$, and $I_n(p) = n/(p(1 - p))$, so $\widehat{\operatorname{Var}} = \hat p(1 - \hat p)/n$. Log odds: with $\beta = \log(p/(1 - p))$, $dp/d\beta = p(1 - p)$, so $I_n(\beta) = I_n(p)(dp/d\beta)^2 = np(1 - p)$, and the MLE is $\hat\beta = \log(\hat p/(1 - \hat p)) = \log(k/(n - k))$ by invariance of the MLE. Poisson: $\ell(\lambda) = t\log\lambda - n\lambda$, $\hat\lambda = t/n$, $I_n(\lambda) = n/\lambda$. Normal with $\sigma$ known: $\hat\mu = \bar x$ and $I_n = n/\sigma^2$. Normal with $\sigma^2$ unknown: the MLE is $(\bar x, SS/n)$, and the information matrix of $(\mu, \sigma^2)$ is $\operatorname{diag}(n/\sigma^2, n/(2\sigma^4))$, whose inverse has $(1, 1)$ entry $\sigma^2/n$. At the MLE this is $SS/n^2$, so $W = n^2(\bar x - \mu_0)^2/SS$. $\square$

**Lemma 4 (the null distribution).** Suppose that under $H_0$, $\sqrt n(\hat\theta_{(1)} - \theta_0) \to N(0, \Sigma)$ in distribution with $\Sigma$ positive definite, and $n\hat V \to \Sigma$ in probability. Then $W \to \chi^2_r$ in distribution, and $P_{H_0}(Q(r/2, W/2) \le \alpha) \to \alpha$ for every $\alpha \in (0, 1)$.

*Proof.* Write $Z_n = \sqrt n(\hat\theta_{(1)} - \theta_0)$, so $W = Z_n^\top (n\hat V)^{-1} Z_n$. Matrix inversion is continuous at the positive definite $\Sigma$, so $(n\hat V)^{-1} \to \Sigma^{-1}$ in probability, by the continuous mapping theorem. By [Slutsky's theorem](/slutsky-theorem/) and continuous mapping, $W \to Z^\top \Sigma^{-1} Z$ with $Z \sim N(0, \Sigma)$. Let $\Sigma^{1/2}$ be the symmetric square root and $Y = \Sigma^{-1/2}Z \sim N(0, I_r)$. Then $Z^\top \Sigma^{-1} Z = Y^\top Y = \sum_{j=1}^r Y_j^2$, a sum of $r$ independent squared standard normals, which is $\chi^2_r$ by definition. The upper tail $G(c) = Q(r/2, c/2)$ of $\chi^2_r$ is continuous and strictly decreasing, so $\{G(W) \le \alpha\} = \{W \ge G^{-1}(\alpha)\}$, and its probability tends to $G(G^{-1}(\alpha)) = \alpha$ because the limit law is continuous. $\square$

Under the conditions on the page on the [asymptotic normality of the MLE](/asymptotic-normality-of-mle/), $\Sigma$ is the $(1, 1)$ block of $I(\theta)^{-1}$, and $n$ times the corresponding block of $I_n(\hat\theta)^{-1}$ converges to it in probability when $I$ is continuous and $\hat\theta$ is consistent. For the normal mean with known $\sigma$, $W = Z^2$ with $Z \sim N(0, 1)$ exactly, so the size is exactly $\alpha$ for every $n$.

**Lemma 5 (the order for a normal mean).** For iid normal data with $\sigma$ unknown and $u = n(\bar x - \mu_0)^2/SS = T^2/(n - 1)$, the Wald, likelihood ratio and score statistics are $nu$, $n\log(1 + u)$ and $nu/(1 + u)$, and $nu \ge n\log(1 + u) \ge nu/(1 + u)$.

*Proof.* The Wald value is Lemma 3. The likelihood ratio value is proved on the likelihood ratio test page. For the score, the restricted MLE of $\sigma^2$ is $v_0 = (SS + n(\bar x - \mu_0)^2)/n$, the score for $\mu$ at $(\mu_0, v_0)$ is $n(\bar x - \mu_0)/v_0$, the score for $\sigma^2$ is 0 there, and the information is diagonal with $(1, 1)$ entry $n/v_0$; so $S = n(\bar x - \mu_0)^2/v_0 = nu/(1 + u)$. For $u \ge 0$, $\log(1 + u) \le u$ because $\log(1 + u) = \int_0^u dt/(1 + t)$ and the integrand is at most 1, and $\log(1 + u) \ge u/(1 + u)$ because $\log(1 + u) = \int_0^u dt/(1 + t)$ and the integrand is at least $1/(1 + u)$. $\square$

**Termination.** Elimination makes $r$ passes, each over at most $r$ rows of $r + 1$ entries, and back substitution makes $r$ more steps, so line L2 stops after $O(r^3)$ operations. The other lines take $O(r)$ operations, plus one evaluation of the incomplete gamma function, which stops after a bounded number of iterations. The closed forms make one pass over the data.

**Theorem.** For a positive definite $\hat V$, WALD-TEST returns $W = (\hat\theta - \theta_0)^\top \hat V^{-1}(\hat\theta - \theta_0) \ge 0$ and $p = P(\chi^2_r \ge W)$. If $\hat\theta$ is asymptotically normal and $\hat V$ is consistent under $H_0$, rejecting when $p \le \alpha$ has size tending to $\alpha$.

*Proof.* Lemmas 1 to 4. $\blacksquare$
