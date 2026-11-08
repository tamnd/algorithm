---
title: The Monte Carlo estimate is unbiased with variance V^2 σ^2/N, and the reported standard error is consistent
proves: [correctness]
status: full
---

Let $B = \prod_{k=1}^{s} [a_k, b_k]$ with $a_k < b_k$, volume $V = \prod_k (b_k - a_k)$, and let $f : B \to \mathbb{R}$ be measurable with $\int_B |f| < \infty$. Write $I = \int_B f$. The points $X_1, \ldots, X_N$ of line L4 are independent and uniform on $B$ (we treat the generator as producing independent uniform variates; see the remark at the end). Put $Y_j = f(X_j)$. The $Y_j$ are independent and identically distributed with

$$\mathbb{E}[Y_j] = \int_B f(x)\,\frac{dx}{V} = \frac{I}{V}, \qquad \sigma^2 = \operatorname{Var}(Y_j) = \frac{1}{V} \int_B f^2 - \frac{I^2}{V^2},$$

where $\sigma^2$ may be $+\infty$.

**Lemma 1 (the one-pass update).** After step $j$ of the loop, $\mu_j = \frac{1}{j} \sum_{i \le j} Y_i$ and $q_j = \sum_{i \le j} (Y_i - \mu_j)^2$.

*Proof.* By induction; for $j = 1$, $\delta = Y_1$, $\mu_1 = Y_1$ and $q_1 = Y_1 \cdot 0 = 0$. For $j \ge 2$, let $\delta = Y_j - \mu_{j-1}$. Then $\mu_j = \mu_{j-1} + \delta/j$ is the new mean. Split $q_j$:

$$\sum_{i \le j} (Y_i - \mu_j)^2 = \sum_{i < j} (Y_i - \mu_{j-1})^2 + (j - 1)(\mu_{j-1} - \mu_j)^2 + (Y_j - \mu_j)^2,$$

because the cross term $2(\mu_{j-1} - \mu_j) \sum_{i<j} (Y_i - \mu_{j-1})$ vanishes. With $\mu_j - \mu_{j-1} = \delta/j$ and $Y_j - \mu_j = \delta (j - 1)/j$, the last two terms add to $\frac{(j-1)\delta^2}{j^2} + \frac{(j-1)^2 \delta^2}{j^2} = \frac{(j - 1)\delta^2}{j} = \delta\,(Y_j - \mu_j)$, which is what line L6 adds. $\square$

So line L8 returns $\hat I_N = V \bar Y$ with $\bar Y = \frac1N \sum_j Y_j$, and $\widehat{\mathrm{se}} = V \sqrt{S^2/N}$ with the sample variance $S^2 = \frac{1}{N - 1} \sum_j (Y_j - \bar Y)^2$.

**Theorem 1 (unbiased, with known variance).** $\mathbb{E}[\hat I_N] = I$. If $\sigma^2 < \infty$, then $\operatorname{Var}(\hat I_N) = V^2 \sigma^2/N$, so the root mean square error is exactly $V \sigma/\sqrt{N}$.

*Proof.* Linearity of expectation gives $\mathbb{E}[\hat I_N] = V \cdot \frac{1}{N} \cdot N \cdot \frac{I}{V} = I$. Variances of independent variables add, so $\operatorname{Var}(\bar Y) = \sigma^2/N$ and $\operatorname{Var}(V \bar Y) = V^2 \sigma^2/N$. $\square$

**Theorem 2 (convergence).** (a) $\hat I_N \to I$ almost surely as $N \to \infty$, for every integrable $f$, even with $\sigma^2 = \infty$. (b) If $\sigma^2 < \infty$, then for every $t > 0$, $\Pr(|\hat I_N - I| \ge t) \le V^2 \sigma^2/(N t^2)$. (c) If $0 < \sigma^2 < \infty$, then $\sqrt{N}(\hat I_N - I)/(V \sigma)$ converges in distribution to a standard normal variable.

*Proof.* (a) is the strong [law of large numbers](/law-of-large-numbers/) for the i.i.d. integrable $Y_j$. (b) is the [Chebyshev inequality](/chebyshev-inequality/) applied with Theorem 1. (c) is the [central limit theorem](/central-limit-theorem/). $\square$

**Theorem 3 (the standard error).** $\mathbb{E}[S^2] = \sigma^2$ when $\sigma^2 < \infty$, and $S^2 \to \sigma^2$ almost surely. Hence $\widehat{\mathrm{se}} \sqrt{N} \to V\sigma$ almost surely, and by Slutsky's lemma, $(\hat I_N - I)/\widehat{\mathrm{se}}$ converges in distribution to a standard normal variable when $0 < \sigma^2 < \infty$. So $\hat I_N \pm 1.96\,\widehat{\mathrm{se}}$ is an asymptotic 95 percent confidence interval.

*Proof.* $\sum_j (Y_j - \bar Y)^2 = \sum_j (Y_j - \nu)^2 - N(\bar Y - \nu)^2$ with $\nu = I/V$. Taking expectations, $N\sigma^2 - N \cdot \sigma^2/N = (N - 1)\sigma^2$. For the almost sure limit, $\frac1N \sum_j Y_j^2 \to \mathbb{E}[Y^2]$ and $\bar Y \to \nu$ by the strong law, so $S^2 = \frac{N}{N - 1}\big(\frac1N \sum Y_j^2 - \bar Y^2\big) \to \sigma^2$. $\square$

**Orientation and degenerate boxes.** If some $b_k < a_k$, line L1 gives a signed volume $V$, and the points of line L4 are still uniform on the box with corners $a$ and $b$; the result is the oriented integral, with the sign of $V$, as in one dimension. If some $b_k = a_k$, then $V = 0$ and the algorithm returns $(0, 0)$, the integral over a set of measure zero. $\blacksquare$

**Termination and cost.** The loop runs $N$ times, with $s$ uniform variates and one evaluation of $f$ per pass, and keeps only $\mu$, $q$ and the current point.

**Remark on pseudorandom numbers.** The theorems hold for independent uniform variates. A program uses a [pseudorandom number generator](/pseudorandom-number-generator/), here the [Mersenne Twister](/mersenne-twister/) of Python's `random` module, whose output is deterministic. The theorems then describe the behaviour to the extent that the generator passes the relevant statistical tests, which is an empirical, not a proved, property. The tests check the predicted variance and coverage on fixed seeds.
