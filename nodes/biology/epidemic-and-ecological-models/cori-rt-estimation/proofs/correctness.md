---
title: The window likelihood, the gamma posterior and its summaries
proves: [correctness]
status: full
---

**Setting.** Days are $1, \ldots, T$, with incidence $I_1, \ldots, I_T$. The weights $w_1, \ldots, w_{s_{\max}}$ are non-negative, and $w_0 = 0$. Cases before day 1 are taken as 0, so $\Lambda_t = \sum_{s=1}^{\min(t - 1, s_{\max})} w_s I_{t-s}$. Fix a window $W = \{s_0, \ldots, t\}$ of $\tau$ days with $s_0 \ge 2$. The model is: given $I_1, \ldots, I_{u-1}$, the count $I_u$ is Poisson($R_u \Lambda_u$), and $R_u = R$ for every $u \in W$. The days before $s_0$ have their own reproduction numbers, which do not involve $R$. The prior on $R$ is a gamma law with shape $a > 0$ and scale $b > 0$, with density $\pi(R) \propto R^{a - 1} e^{-R/b}$ on $R > 0$.

**Claim 1 (line L1).** The list `lam` holds $\Lambda_1, \ldots, \Lambda_T$.

*Proof.* For the day with index $t$ (0-based, day $t + 1$), the loop adds $w_s I$ for the day $s$ steps before, for $s = 1, \ldots, \min(t, s_{\max})$. These are exactly the terms of $\Lambda_{t+1}$ whose day is 1 or later; the terms for earlier days are 0 by the convention. The check $w_0 = 0$ makes sure that $I_u$ never enters its own $\Lambda_u$. $\square$

**Claim 2 (the window likelihood).** As a function of $R$,
$$P(I_{s_0}, \ldots, I_t \mid I_1, \ldots, I_{s_0 - 1}, R) = \prod_{u \in W} \frac{(R \Lambda_u)^{I_u} e^{-R \Lambda_u}}{I_u!} \propto R^{\sum_{u \in W} I_u} \exp\Big(-R \sum_{u \in W} \Lambda_u\Big).$$

*Proof.* By the chain rule, the joint probability of the window counts given the earlier counts is the product over $u \in W$ of $P(I_u \mid I_1, \ldots, I_{u-1}, R)$. Each factor is the Poisson($R \Lambda_u$) mass at $I_u$, and $\Lambda_u$ is a fixed number given $I_1, \ldots, I_{u-1}$, because $w_0 = 0$. The factors $\Lambda_u^{I_u} / I_u!$ do not depend on $R$. If $\Lambda_u = 0$ the model forces $I_u = 0$, and the factor is 1 for every $R$, which agrees with the formula. $\square$

**Claim 3 (the posterior).** The posterior of $R$ given $I_1, \ldots, I_t$ is the gamma law with shape $A = a + \sum_{u \in W} I_u$ and rate $B = 1/b + \sum_{u \in W} \Lambda_u$.

*Proof.* The probability of the days before $s_0$ does not depend on $R$, by the setting. So by [Bayes' theorem](/bayes-theorem/), the posterior density is proportional to the prior times the window likelihood of Claim 2:
$$R^{a - 1} e^{-R / b} \cdot R^{\sum I_u} e^{-R \sum \Lambda_u} = R^{A - 1} e^{-B R}.$$
Since $A \ge a > 0$ and $B \ge 1/b > 0$, this is integrable on $(0, \infty)$, with integral $\Gamma(A) / B^A$, and the normalized density is the gamma density with shape $A$ and rate $B$. This is the [conjugate](/conjugate-prior/) update of a gamma prior by Poisson counts. $\square$

**Claim 4 (lines L2 to L4).** For each $t$ from $\text{first\_day} + \tau - 1$ to $T$, the code sets $s = t - \tau + 1$ and computes $A$ and $B$ of Claim 3 for the window $\{s, \ldots, t\}$.

*Proof.* The prefix sums satisfy $c_I[k] = \sum_{u=1}^{k} I_u$ and $c_\Lambda[k] = \sum_{u=1}^{k} \Lambda_u$, by induction on $k$, since each step adds the next term. So $c_I[t] - c_I[s - 1] = \sum_{u=s}^{t} I_u$, and the same for $\Lambda$. The loop starts at $t = \text{first\_day} + \tau - 1$, so $s \ge \text{first\_day} \ge 2$ for every window, and the window has $\tau$ days. $\square$

**Claim 5 (line L5).** The mean is $A / B$, the standard deviation is $\sqrt A / B$, and the coefficient of variation is $1 / \sqrt A$.

*Proof.* For a gamma law with shape $A$ and rate $B$, $E[R] = \int_0^\infty R \cdot \frac{B^A}{\Gamma(A)} R^{A-1} e^{-BR}\, dR = \frac{B^A}{\Gamma(A)} \cdot \frac{\Gamma(A+1)}{B^{A+1}} = \frac{A}{B}$, and in the same way $E[R^2] = A(A+1)/B^2$, so the variance is $A / B^2$. The ratio of the standard deviation to the mean is $1/\sqrt A$. $\square$

**Claim 6 (line L6).** `gamma_quantile(p, A, B)` returns the $p$-quantile of the posterior to within the tolerance.

*Proof.* If $R$ has the gamma law with shape $A$ and rate $B$, then $X = 2BR$ has density proportional to $x^{A-1} e^{-x/2}$, which is the chi-squared law with $2A$ degrees of freedom. So $P(R \le x) = 1 - P(X > 2Bx)$, which is what `gamma_cdf` computes with `chi2_sf`. This function $F$ is continuous and strictly increasing on $(0, \infty)$, with $F(0) = 0$ and $F(x) \to 1$. The first loop doubles `hi` until $F(\text{hi}) \ge p$, which happens after finitely many steps. Then the invariant $F(\text{lo}) < p \le F(\text{hi})$ holds, since $F(0) = 0 < p$. Each bisection step keeps it, as it moves `lo` up only when $F(\text{mid}) < p$ and moves `hi` down otherwise. So the unique $x^*$ with $F(x^*) = p$ stays in $[\text{lo}, \text{hi}]$, and the returned midpoint is within the final interval length of $x^*$. $\square$

**Conclusion.** Each `WindowEstimate` holds the exact gamma posterior of $R$ for its window under the model, and its mean, standard deviation, coefficient of variation and quantiles. The test of simulation-based calibration checks Claim 3 as a whole: when $R$ is drawn from the prior and the data from the model, the posterior distribution function at the true $R$ is uniform.
