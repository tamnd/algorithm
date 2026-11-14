---
title: Given the discordant total the count b is Binomial(m, 1/2), so the exact p-value is valid and the statistic tends to chi-square with 1 degree of freedom
proves: [correctness]
status: full
---

**Model.** $N$ independent pairs, each with a binary outcome before and after (or for the two members of a matched pair). Each pair falls in one of four cells with probabilities $\pi_{11}$ (yes, yes), $\pi_{12}$ (yes, no), $\pi_{21}$ (no, yes) and $\pi_{22}$ (no, no). The counts $(a, b, c, d)$ are multinomial. The null hypothesis of marginal homogeneity is $P(\text{yes first}) = P(\text{yes second})$, that is $\pi_{11} + \pi_{12} = \pi_{11} + \pi_{21}$, which is $\pi_{12} = \pi_{21}$. Write $m = b + c$.

**Claim 1 (the conditional null law).** If $\pi_{12} + \pi_{21} > 0$, then given $m$, $b \sim \text{Binomial}(m, \theta)$ with $\theta = \pi_{12}/(\pi_{12} + \pi_{21})$, whatever $a$, $d$, $\pi_{11}$ and $\pi_{22}$ are. Under $H_0$, $\theta = 1/2$.

*Proof.* Classify each pair as concordant, (yes, no) or (no, yes). The pairs are independent, so the number of discordant pairs $m$ is binomial, and given which pairs are discordant, each of them is (yes, no) with probability $\pi_{12}/(\pi_{12} + \pi_{21})$, independently of the others. So given $m$, $b$ is a sum of $m$ independent Bernoulli($\theta$) variables. The concordant pairs do not enter. $\square$

**Claim 2 (lines L1 to L4 return the exact two-sided p-value).** Let $B \sim \text{Binomial}(m, 1/2)$ and $T(k) = \lvert 2k - m \rvert = \lvert k - (m - k) \rvert$. The exact p-value is $p(b) = P(T(B) \ge T(b))$, and

$$p(b) = \min\Big\{1,\; 2 \sum_{k = 0}^{\min(b, c)} \binom{m}{k} 2^{-m}\Big\}.$$

*Proof.* Let $s = \min(b, c)$. Then $T(k) \ge T(b) = m - 2s$ if and only if $k \le s$ or $k \ge m - s$. If $b \ne c$ then $s < m/2 < m - s$, the two sets are disjoint, and by the symmetry $\binom{m}{k} = \binom{m}{m - k}$ they have the same probability, so $p(b) = 2P(B \le s)$, which is at most 1 since the two disjoint events have total probability at most 1. If $b = c$ then $T(b) = 0$, every $k$ qualifies, and $p(b) = 1$; the formula gives $2P(B \le m/2) \ge 1$, which the minimum cuts to 1. Line L3 sums the integers $\binom{m}{k}$ exactly (see Cost for how it finds them), and line L4 forms the fraction exactly. When $m = 0$ there is no information and the code returns 1. $\square$

**Claim 3 (validity).** Under $H_0$, $P(p \le \alpha) \le \alpha$ for every $\alpha$, both given $m$ and without conditioning.

*Proof.* Given $m$, $p(b)$ is a tail $P(T(B) \ge T(b))$ of a finite law, so the lemma on the [binomial test](/binomial-test/) correctness page gives $P(p \le \alpha \mid m) \le \alpha$. Averaging over $m$ gives the unconditional bound. $\square$

**Claim 4 (the asymptotic statistic).** $X^2 = (b - c)^2/(b + c) = Z^2$ with $Z = (b - m/2)/\sqrt{m/4}$, the standardized count of a Binomial($m$, 1/2) variable. Under $H_0$ with $\pi_{12} = \pi_{21} > 0$ fixed, $X^2$ converges in distribution to the chi-square law with 1 degree of freedom as $N \to \infty$, and the size of the asymptotic test tends to $\alpha$.

*Proof.* $b - m/2 = (b - c)/2$ and $\sqrt{m/4} = \sqrt m/2$, so $Z = (b - c)/\sqrt m$ and $Z^2 = X^2$. Given $m$, $Z$ is a standardized sum of $m$ iid Bernoulli(1/2) variables, so by the [central limit theorem](/central-limit-theorem/), $\sup_x \lvert P(Z \le x \mid m) - \Phi(x) \rvert \to 0$ as $m \to \infty$ (Pólya's theorem turns pointwise convergence to a continuous limit into uniform convergence). Since $m \sim \text{Binomial}(N, \pi_{12} + \pi_{21})$, $m \to \infty$ in probability as $N \to \infty$. So $P(\lvert Z \rvert \le x) = \mathbb{E}[P(\lvert Z \rvert \le x \mid m)] \to 2\Phi(x) - 1$ by bounded convergence, and $Z^2$ tends to the square of a standard normal, which is chi-square with 1 degree of freedom. The law is continuous, so the size at the quantile tends to $\alpha$. $\square$

The convergence is not uniform in the parameters: for small $\pi_{12} + \pi_{21}$, $m$ stays small and the conditional size of the asymptotic test can be far from $\alpha$. The page and the tests compute it exactly for each $m$. Edwards's corrected statistic has the same limit, because $(\lvert b - c \rvert - 1)^2/m - (b - c)^2/m = (1 - 2\lvert b - c \rvert)/m \to 0$ in probability (as $\lvert b - c \rvert/\sqrt m$ stays bounded in probability). That the corrected test keeps its size below $\alpha$ is measured, not proved: the tests check it for $m \le 100$.

**Lines L5 and L6.** Line L5 computes $X^2$ or the corrected statistic, and line L6 returns $P(\chi^2_1 > X^2)$ from the regularized incomplete gamma function of the helper module. With 1 degree of freedom this equals $\operatorname{erfc}(\sqrt{X^2/2})$, which the tests use as an independent check.

**Cost.** The exact method sums $\min(b, c) + 1 \le m/2 + 1$ binomial coefficients. Line L3 finds each from the one before by $\binom{m}{k + 1} = \binom{m}{k}(m - k)/(k + 1)$, an exact integer division because $\binom{m}{k}(m - k) = \binom{m}{k + 1}(k + 1)$. So the sum takes $\Theta(\min(b, c) + 1)$ operations on integers of at most $m$ bits, and $O(m^2)$ bit operations. The asymptotic methods take $\Theta(1)$ operations plus one incomplete gamma evaluation. $\square$
