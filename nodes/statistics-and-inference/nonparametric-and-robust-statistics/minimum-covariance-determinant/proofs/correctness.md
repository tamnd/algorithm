---
title: A C-step never increases the determinant, and the concentration loop stops
proves: [correctness]
status: full
---

This proof covers the C-step and the loop of FAST-MCD. It does not prove that FAST-MCD finds the MCD subset: it does not always find it. The breakdown point, the consistency and the efficiency of the MCD are cited on the main page and are not proved here.

**Notation.** The points are $x_1, \ldots, x_n \in \mathbb R^p$ and $p < h \le n$. For a set $H$ of $h$ indices put
$$T(H) = \frac1h\sum_{i \in H} x_i, \qquad S(H) = \frac1h\sum_{i \in H}(x_i - T(H))(x_i - T(H))^{\mathsf T}.$$
If $S(H)$ is nonsingular, put $d_H(i)^2 = (x_i - T(H))^{\mathsf T}S(H)^{-1}(x_i - T(H))$. A C-step from $H_1$ returns a set $H_2$ of $h$ indices with the $h$ least values of $d_{H_1}(i)^2$, with ties broken in any way. Write $T_k = T(H_k)$ and $S_k = S(H_k)$.

**Lemma 1 (the distances inside $H$ add up to $hp$).** If $S(H)$ is nonsingular, then $\sum_{i \in H} d_H(i)^2 = hp$.

*Proof.* A scalar equals its trace, and $\operatorname{tr}(AB) = \operatorname{tr}(BA)$. So
$$\sum_{i \in H} d_H(i)^2 = \operatorname{tr}\Bigl(S(H)^{-1}\sum_{i \in H}(x_i - T(H))(x_i - T(H))^{\mathsf T}\Bigr) = \operatorname{tr}\bigl(S(H)^{-1}\,h\,S(H)\bigr) = hp. \qquad \square$$

**Lemma 2 (moving the center).** For every $m \in \mathbb R^p$,
$$\frac1h\sum_{i \in H}(x_i - m)(x_i - m)^{\mathsf T} = S(H) + (T(H) - m)(T(H) - m)^{\mathsf T}.$$

*Proof.* Write $x_i - m = (x_i - T(H)) + (T(H) - m)$ and expand. The two cross terms contain $\sum_{i \in H}(x_i - T(H)) = 0$, so they vanish. $\square$

**Lemma 3 (eigenvalues of $A^{-1}B$).** Let $A$ be symmetric positive definite and $B$ symmetric positive semidefinite. Then $A^{-1}B$ has real eigenvalues $\lambda_1, \ldots, \lambda_p \ge 0$, with $\sum_j\lambda_j = \operatorname{tr}(A^{-1}B)$ and $\prod_j\lambda_j = \det B/\det A$. If every $\lambda_j$ equals 1, then $B = A$.

*Proof.* Let $A^{1/2}$ be the symmetric positive definite square root of $A$. Then $A^{-1}B = A^{-1/2}\,(A^{-1/2}BA^{-1/2})\,A^{1/2}$, so $A^{-1}B$ is similar to $C = A^{-1/2}BA^{-1/2}$. $C$ is symmetric, and $z^{\mathsf T}Cz = (A^{-1/2}z)^{\mathsf T}B(A^{-1/2}z) \ge 0$, so its eigenvalues are real and nonnegative. Similar matrices have the same trace, determinant and eigenvalues, and $\det C = \det B/\det A$. If every eigenvalue of the symmetric matrix $C$ is 1, then $C = I$, so $B = A^{1/2}A^{1/2} = A$. $\square$

**Theorem (the C-step).** Let $\det S_1 > 0$ and let $H_2$ be the result of a C-step from $H_1$. Then
$$\operatorname{tr}(S_1^{-1}S_2) + (T_2 - T_1)^{\mathsf T}S_1^{-1}(T_2 - T_1) \le p \quad\text{and}\quad \det S_2 \le \det S_1,$$
and $\det S_2 = \det S_1$ holds only if $T_2 = T_1$ and $S_2 = S_1$.

*Proof.* $H_2$ holds the $h$ least values of $d_{H_1}(i)^2$, and $H_1$ is one set of $h$ indices, so by Lemma 1
$$\sum_{i \in H_2} d_{H_1}(i)^2 \le \sum_{i \in H_1} d_{H_1}(i)^2 = hp.$$
Use the trace as in Lemma 1 and then Lemma 2 with $H = H_2$ and $m = T_1$. With $\delta = T_2 - T_1$,
$$\frac1h\sum_{i \in H_2} d_{H_1}(i)^2 = \operatorname{tr}\Bigl(S_1^{-1}\,\frac1h\sum_{i \in H_2}(x_i - T_1)(x_i - T_1)^{\mathsf T}\Bigr) = \operatorname{tr}(S_1^{-1}S_2) + \delta^{\mathsf T}S_1^{-1}\delta.$$
This gives the first inequality. Since $S_1^{-1}$ is positive definite, $\delta^{\mathsf T}S_1^{-1}\delta \ge 0$, so $\operatorname{tr}(S_1^{-1}S_2) \le p$. Let $\lambda_1, \ldots, \lambda_p \ge 0$ be the eigenvalues of $S_1^{-1}S_2$ (Lemma 3 with $A = S_1$ and $B = S_2$). The inequality of the arithmetic and geometric means gives
$$\frac{\det S_2}{\det S_1} = \prod_j\lambda_j \le \Bigl(\frac1p\sum_j\lambda_j\Bigr)^p = \Bigl(\frac{\operatorname{tr}(S_1^{-1}S_2)}{p}\Bigr)^p \le 1.$$
Now suppose $\det S_2 = \det S_1$. Then every inequality in the chain is an equality. So $\frac1p\sum_j\lambda_j = 1$, which forces $\delta^{\mathsf T}S_1^{-1}\delta = 0$, so $\delta = 0$ and $T_2 = T_1$. Equality in the inequality of the means holds only if all $\lambda_j$ are equal, and their mean is 1, so every $\lambda_j = 1$, and Lemma 3 gives $S_2 = S_1$. $\square$

**Corollary 1 (the loop stops).** In exact arithmetic, the loop of lines L5 to L9 stops after at most $\binom nh$ passes. When it stops at a set $H$ with $\det S(H) > 0$, the C-step from $H$ gives the same mean and the same covariance matrix as $H$.

*Proof.* Line L9 accepts $H'$ only if $\det S(H') < \det S(H)$. So the determinants of the accepted sets strictly decrease, no set is accepted twice, and there are $\binom nh$ sets. If an accepted set has determinant 0, line L7 stops. Otherwise line L9 stops when $H' = H$ or $\det S(H') \ge \det S(H)$. In the first case the claim is clear. In the second case the theorem gives $\det S(H') \le \det S(H)$, so the two are equal, and the theorem gives $T(H') = T(H)$ and $S(H') = S(H)$. $\square$

**Corollary 2 (the MCD subset is a fixed point).** Let $H^*$ minimize $\det S(H)$ over all sets of $h$ indices, with $\det S(H^*) > 0$. Then every C-step from $H^*$ gives the mean $T(H^*)$ and the covariance matrix $S(H^*)$.

*Proof.* By the theorem the C-step gives a set $H'$ with $\det S(H') \le \det S(H^*)$, and by the minimality of $H^*$ the two are equal. The equality case of the theorem completes the proof. $\square$

So FAST-MCD returns the MCD subset if the C-steps from at least one start reach it. Corollary 2 shows that the MCD subset is among the stopping points, but other sets can be stopping points too, and a random start does not always lead to the best one.

**Lemma 4 (the form of the consistency factor).** Let $X \sim N(0, I_p)$, $0 < \alpha < 1$, and let $q_\alpha$ be the $\alpha$-quantile of the chi-squared distribution with $p$ degrees of freedom. Then
$$\mathbb E\bigl[XX^{\mathsf T} \mid \|X\|^2 \le q_\alpha\bigr] = \frac{F_{p+2}(q_\alpha)}{\alpha}\,I_p,$$
where $F_k$ is the chi-squared distribution function with $k$ degrees of freedom.

*Proof.* The law of $X$ and the event are invariant under orthogonal maps, so the conditional covariance is a multiple $\kappa I_p$, and $p\kappa = \mathbb E[\|X\|^2 \mid \|X\|^2 \le q_\alpha]$. $\|X\|^2$ has the chi-squared density $f_p(u) = u^{p/2 - 1}e^{-u/2}/(2^{p/2}\Gamma(p/2))$. Since $\Gamma(p/2 + 1) = \frac p2\Gamma(p/2)$, $u f_p(u) = p f_{p+2}(u)$. So
$$p\kappa = \frac1\alpha\int_0^{q_\alpha} u f_p(u)\,du = \frac{p\,F_{p+2}(q_\alpha)}{\alpha}. \qquad \square$$

At the normal model $N(\mu, \Sigma)$, the population MCD region is the ellipsoid $\{(x - \mu)^{\mathsf T}\Sigma^{-1}(x - \mu) \le q_\alpha\}$. This fact is cited, not proved here (see Hubert, Debruyne and Rousseeuw 2018). Lemma 4, applied to $\Sigma^{-1/2}(X - \mu)$, then shows that the raw scatter estimates $\frac{F_{p+2}(q_\alpha)}{\alpha}\Sigma$. Line L11 divides by this factor. The same computation with $1 - \delta$ in place of $\alpha$ gives the factor of line L13.
