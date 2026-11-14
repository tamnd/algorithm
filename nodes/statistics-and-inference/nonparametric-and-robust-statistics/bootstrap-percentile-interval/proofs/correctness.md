---
title: The percentile interval computes the bootstrap quantiles and respects monotone transformations
proves: [correctness]
status: full
---

We use the pseudocode of the page. The data $x_1, \ldots, x_n$ are fixed. $G(t) = P^*(\hat\theta^* \le t)$ is the bootstrap distribution function, where $P^*$ is the law of a resample of size $n$ from $\hat F_n$. $\hat G_b(t) = \frac{1}{b} \#\{j : \theta^*_j \le t\}$ is the empirical distribution function of the $b$ replicates. For any distribution function $K$, $K^{-1}(p) = \inf\{t : K(t) \ge p\}$.

This file proves what the algorithm computes and when the ideal interval has exact coverage. It does not prove a coverage level for a general $F$. That coverage is measured on the page.

**Claim 1 (lines L5 and L6 compute the empirical quantiles).** For $0 < p < 1$, $\hat G_b^{-1}(p) = \theta^*_{(k)}$ with $k = \lceil b p \rceil$.

*Proof.* Since $0 < p < 1$, $1 \le k \le b$. At $t = \theta^*_{(k)}$ at least $k$ replicates are $\le t$, so $\hat G_b(t) \ge k/b \ge p$. For $t < \theta^*_{(k)}$ at most $k - 1$ replicates are $\le t$, so $\hat G_b(t) \le (k-1)/b < p$, because $k - 1 < b p$ by the definition of the ceiling. So the infimum is $\theta^*_{(k)}$. With $p = \alpha/2$ and $p = 1 - \alpha/2$ this is lines L5 and L6. The `max(1, ...)` in line L5 changes nothing for $p > 0$; it only keeps the index valid. $\square$

**Claim 2 (the Monte Carlo endpoints converge to the ideal ones).** Let $0 < p < 1$ be a number that $G$ does not take as a value. Then, with probability 1 over the resampling, $\hat G_b^{-1}(p) = G^{-1}(p)$ for all large $b$.

*Proof.* $G$ is a step function with finitely many jumps, at the values $t_1 < \cdots < t_r$ that $s$ takes on the $n^n$ resamples, and every replicate is one of these values. Let $t_i = G^{-1}(p)$. Then $G(t_i) \ge p$, and since $p$ is not a value of $G$, $G(t_i) > p$. If $i > 1$, then $G(t_{i-1}) < p$ by the definition of the infimum. By the strong law of large numbers, $\hat G_b(t_i) \to G(t_i)$ and $\hat G_b(t_{i-1}) \to G(t_{i-1})$ almost surely. So for all large $b$, $\hat G_b(t_i) > p$ and $\hat G_b(t) \le \hat G_b(t_{i-1}) < p$ for every $t < t_i$, because $\hat G_b$ is constant between consecutive $t$ values. So $\hat G_b^{-1}(p) = t_i$. If $i = 1$, no replicate is below $t_1$, and the same argument applies with only the first inequality. $\square$

The values of $G$ are multiples of $n^{-n}$, so the condition excludes only finitely many $p$. The tests compute $G$ exactly over all $n^n$ resamples for $n \le 5$ and check that the ideal interval of the implementation, which weights the $\binom{2n-1}{n}$ multisets of indices, returns $G^{-1}(\alpha/2)$ and $G^{-1}(1 - \alpha/2)$.

**Claim 3 (transformation respecting).** Let $g$ be strictly increasing on a set that contains every value of $s$. Run the algorithm twice with the same random numbers, once with the statistic $s$ and once with $g \circ s$. If the first run returns $[L, U]$, the second returns $[g(L), g(U)]$.

*Proof.* Line L2 draws the resample indices without looking at the statistic, so both runs use the same resamples, and the $j$-th replicate of the second run is $g(\theta^*_j)$. A strictly increasing $g$ keeps the order, so the $k$-th smallest of the $g(\theta^*_j)$ is $g(\theta^*_{(k)})$. Lines L5 and L6 use the same $k$ and $k'$ in both runs. $\square$

For a strictly decreasing $g$ the same argument gives $[g(U), g(L)]$, up to the index of the order statistic: the $k$-th smallest of $g(\theta^*_j)$ is $g(\theta^*_{(b + 1 - k)})$. With $b \alpha / 2$ an integer, $b + 1 - \lceil b \alpha/2 \rceil = \lceil b(1 - \alpha/2) \rceil + 1$, so the two endpoints are adjacent order statistics, not equal ones. The tests use $b = 999$ and $\alpha = 0.1$, where $k = 50$ and $k' = 950 = b + 1 - k$, and there the result is exact.

**Claim 4 (exact coverage under a normalizing transformation).** Suppose there is a continuous, strictly increasing $\phi$ and a continuous, strictly increasing distribution function $H$, symmetric about 0, such that

$$\phi(\hat\theta) - \phi(\theta) \sim H \quad \text{under } F, \qquad \phi(\hat\theta^*) - \phi(\hat\theta) \sim H \quad \text{under } P^*.$$

Then the ideal interval $[G^{-1}(\alpha/2), G^{-1}(1 - \alpha/2)]$ contains $\theta$ with probability exactly $1 - \alpha$.

*Proof.* Write $h_p = H^{-1}(p)$, so $h_{\alpha/2} = -h_{1 - \alpha/2}$ by symmetry. By the second assumption $G(t) = P^*(\phi(\hat\theta^*) \le \phi(t)) = H(\phi(t) - \phi(\hat\theta))$, so $G^{-1}(p) = \phi^{-1}(\phi(\hat\theta) + h_p)$. Because $\phi$ is increasing,

$$G^{-1}(\alpha/2) \le \theta \le G^{-1}(1 - \alpha/2) \iff h_{\alpha/2} \le \phi(\theta) - \phi(\hat\theta) \le h_{1 - \alpha/2} \iff h_{\alpha/2} \le \phi(\hat\theta) - \phi(\theta) \le h_{1-\alpha/2},$$

where the last step uses $-h_{1-\alpha/2} = h_{\alpha/2}$. By the first assumption this event has probability $H(h_{1-\alpha/2}) - H(h_{\alpha/2}) = 1 - \alpha$. $\square$

The algorithm does not need to know $\phi$; this is the reason for the method. The symmetry of $H$ is necessary: without it the correct interval uses $h_{\alpha/2}$ and $h_{1-\alpha/2}$ in the reverse order, which is the basic interval of the page. The BCa interval relaxes both assumptions of Claim 4 by allowing a bias $z_0$ and a standard deviation that changes with $\theta$.

**What is not proved.** For a real $F$ the bootstrap distribution is discrete and no exact $\phi$ exists. Under smoothness conditions, Edgeworth expansions show that each one-sided endpoint has coverage error of order $n^{-1/2}$ (Hall 1988; Hall 1992, Chapter 3). The coverages on the page come from a simulation with a stated seed. They are measurements with a Monte Carlo standard error of about $0.007$, not theorems.

**Cost.** The loop of lines L1 to L3 runs $b$ times. Each pass draws $n$ indices and evaluates $s$ once. Line L4 sorts $b$ numbers in $\Theta(b \log b)$ comparisons, and lines L5 and L6 take constant time. So the time is $\Theta(b \cdot (n + C_s(n)) + b \log b)$, where $C_s(n)$ is the cost of $s$, and the extra space is $\Theta(b + n)$.
