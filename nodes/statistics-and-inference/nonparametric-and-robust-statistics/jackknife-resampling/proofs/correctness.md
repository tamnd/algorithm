---
title: Exact identities of the jackknife
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page: $\hat\theta_{(i)}$ is the statistic without $x_i$, $\hat\theta_{(\cdot)}$ their mean, $\hat\theta_{jack} = n\hat\theta - (n - 1)\hat\theta_{(\cdot)}$ and $\widehat{\mathrm{var}}_{jack} = \frac{n-1}{n}\sum_i (\hat\theta_{(i)} - \hat\theta_{(\cdot)})^2$. $\bar x$ is the mean and $S^2 = \frac{1}{n-1}\sum (x_i - \bar x)^2$. Lines L1 to L7 compute these formulas directly, so it remains to prove what the formulas give.

**Claim 1 (the mean).** If $s$ is the mean, the bias estimate is 0, $\hat\theta_{jack} = \bar x$ and $\widehat{\mathrm{var}}_{jack} = S^2/n$.

*Proof.* $\hat\theta_{(i)} = (n\bar x - x_i)/(n - 1)$, so $\hat\theta_{(\cdot)} = (n\bar x - \bar x)/(n - 1) = \bar x$ and the bias estimate $(n - 1)(\bar x - \bar x)$ is 0. Further $\hat\theta_{(i)} - \hat\theta_{(\cdot)} = (\bar x - x_i)/(n - 1)$, so

$$\widehat{\mathrm{var}}_{jack} = \frac{n - 1}{n} \cdot \frac{1}{(n-1)^2}\sum_i (x_i - \bar x)^2 = \frac{1}{n} \cdot \frac{\sum_i (x_i - \bar x)^2}{n - 1} = \frac{S^2}{n}. \qquad \square$$

The same computation with $g(x_i)$ in place of $x_i$ covers every statistic $\frac{1}{n}\sum g(x_i)$.

**Claim 2 (bias reduction).** Suppose that for every sample size $k$, $E\, s(X_1, \ldots, X_k) = \theta + a_1/k + a_2/k^2$ with constants $a_1, a_2$. Then $E\hat\theta_{jack} = \theta - a_2/(n(n-1))$. In particular, if $a_2 = 0$, $\hat\theta_{jack}$ is unbiased.

*Proof.* Each $\hat\theta_{(i)}$ is $s$ on $n - 1$ independent observations, so $E\hat\theta_{(\cdot)} = \theta + a_1/(n-1) + a_2/(n-1)^2$. Then

$$E\hat\theta_{jack} = n\Bigl(\theta + \frac{a_1}{n} + \frac{a_2}{n^2}\Bigr) - (n - 1)\Bigl(\theta + \frac{a_1}{n - 1} + \frac{a_2}{(n - 1)^2}\Bigr) = \theta + \frac{a_2}{n} - \frac{a_2}{n - 1} = \theta - \frac{a_2}{n(n - 1)}. \qquad \square$$

**Claim 3 (V-statistics become U-statistics).** Let $h$ be symmetric, $h(x, y) = h(y, x)$, and let $s$ be the V-statistic $V = \frac{1}{n^2}\sum_{i=1}^n\sum_{j=1}^n h(x_i, x_j)$. Then

$$\hat\theta_{jack} = U = \binom{n}{2}^{-1}\sum_{i < j} h(x_i, x_j).$$

*Proof.* Write $A = \sum_i h(x_i, x_i)$ and $B = \sum_{i<j} h(x_i, x_j)$, so $V = (A + 2B)/n^2$. Leaving out $x_k$ removes $h(x_k, x_k)$ from $A$ and the $n - 1$ terms $h(x_k, x_j)$, $j \ne k$, from $B$:

$$\hat\theta_{(k)} = \frac{A - h(x_k, x_k) + 2\bigl(B - \sum_{j \ne k} h(x_k, x_j)\bigr)}{(n - 1)^2}.$$

Summing over $k$, each diagonal term is removed once and each pair $i < j$ is removed twice, once for $k = i$ and once for $k = j$. So

$$\sum_k \hat\theta_{(k)} = \frac{(n - 1)A + 2(n - 2)B}{(n - 1)^2}, \qquad (n - 1)\hat\theta_{(\cdot)} = \frac{(n - 1)A + 2(n - 2)B}{n(n - 1)}.$$

Then

$$\hat\theta_{jack} = \frac{A + 2B}{n} - \frac{(n - 1)A + 2(n - 2)B}{n(n - 1)} = \frac{(n - 1)(A + 2B) - (n - 1)A - 2(n - 2)B}{n(n - 1)} = \frac{2B}{n(n - 1)} = U. \qquad \square$$

**Corollary (the plug-in variance).** With $h(x, y) = (x - y)^2/2$, $V = \frac{1}{2n^2}\sum_{i,j}(x_i - x_j)^2 = \frac{1}{n}\sum_i (x_i - \bar x)^2$, the plug-in variance, and $U = S^2$. So the jackknife turns the plug-in variance into the unbiased sample variance, and its bias estimate is $V - S^2 = -S^2/n$.

The identity $\frac{1}{2n^2}\sum_{i,j}(x_i - x_j)^2 = \frac{1}{n}\sum_i (x_i - \bar x)^2$ follows by expanding $(x_i - x_j)^2 = x_i^2 - 2x_ix_j + x_j^2$: the double sum is $2n\sum x_i^2 - 2(n\bar x)^2 = 2n\sum (x_i - \bar x)^2$. The identity $U = S^2$ follows in the same way, because $\sum_{i<j}(x_i - x_j)^2$ is half of the double sum.

**Claim 4 (pseudo-values).** With $\tilde\theta_i = n\hat\theta - (n - 1)\hat\theta_{(i)}$, the mean of the $\tilde\theta_i$ is $\hat\theta_{jack}$, and $\frac{1}{n} \cdot \frac{1}{n - 1}\sum_i (\tilde\theta_i - \bar{\tilde\theta})^2 = \widehat{\mathrm{var}}_{jack}$.

*Proof.* Averaging gives $\bar{\tilde\theta} = n\hat\theta - (n - 1)\hat\theta_{(\cdot)} = \hat\theta_{jack}$. Then $\tilde\theta_i - \bar{\tilde\theta} = -(n - 1)(\hat\theta_{(i)} - \hat\theta_{(\cdot)})$, so

$$\frac{1}{n(n - 1)}\sum_i (\tilde\theta_i - \bar{\tilde\theta})^2 = \frac{(n - 1)^2}{n(n - 1)}\sum_i (\hat\theta_{(i)} - \hat\theta_{(\cdot)})^2 = \widehat{\mathrm{var}}_{jack}. \qquad \square$$

For the mean, $\tilde\theta_i = n\bar x - (n\bar x - x_i) = x_i$: the pseudo-values are the data.

**Claim 5 (the median with an even sample size).** Let $n = 2m$, let $s$ be the median, and let $x_{(1)} \le \cdots \le x_{(n)}$ be the order statistics. Then $\widehat{\mathrm{var}}_{jack} = \frac{n - 1}{4}(x_{(m+1)} - x_{(m)})^2$.

*Proof.* Without one observation, $2m - 1$ values remain and the median is the $m$-th smallest of them. If the left-out observation is one of $x_{(1)}, \ldots, x_{(m)}$, the $m$-th smallest of the rest is $x_{(m+1)}$. If it is one of $x_{(m+1)}, \ldots, x_{(n)}$, it is $x_{(m)}$. With ties the same holds for the values, whichever copy is left out. So $m$ of the $\hat\theta_{(i)}$ equal $x_{(m+1)}$ and $m$ equal $x_{(m)}$, their mean is $(x_{(m)} + x_{(m+1)})/2$, and each deviation is $\pm D/2$ with $D = x_{(m+1)} - x_{(m)}$. Hence $\widehat{\mathrm{var}}_{jack} = \frac{n - 1}{n} \cdot n \cdot \frac{D^2}{4} = \frac{n - 1}{4}D^2$. $\square$

So the estimate depends on a single spacing of the sample. For a density $f$ that is positive at the median, $n D$ is asymptotically exponential with mean $1/f(\text{median})$, so $\widehat{\mathrm{var}}_{jack}$ divided by the asymptotic variance $1/(4 n f^2)$ does not converge to 1. This explains the table on the page, which is a measurement.

**Claim 6 (the delete-d jackknife for the mean).** For every $1 \le d < n$, the delete-$d$ variance $\frac{n - d}{d\binom{n}{d}}\sum_S (\bar x_S - \bar m)^2$, where $S$ runs over the subsets of size $r = n - d$ and $\bar m$ is the mean of the $\bar x_S$, equals $S^2/n$.

*Proof.* By symmetry each $x_i$ is in the same number of subsets, so $\bar m = \bar x$. The mean of a random subset of size $r$ drawn without replacement from $x_1, \ldots, x_n$ has variance $\frac{\sigma_0^2}{r}\cdot\frac{n - r}{n - 1}$, where $\sigma_0^2 = \frac{n - 1}{n}S^2$ is the population variance of the $n$ values. This is the variance of the uniform law over the subsets, so

$$\frac{1}{\binom{n}{d}}\sum_S (\bar x_S - \bar x)^2 = \frac{S^2}{n} \cdot \frac{n - r}{r} = \frac{S^2}{n} \cdot \frac{d}{n - d},$$

and multiplying by $\frac{n - d}{d}$ gives $S^2/n$. $\square$

With $d = 1$ the delete-$d$ formula is the formula of line L6, because the subsets are the $n$ leave-one-out samples. The tests check Claims 1 to 6 with exact `Fraction` arithmetic, and Claim 3 against the definition of the U-statistic as a sum over all pairs, for four kernels.

**Cost.** Line L3 runs $n$ times on $n - 1$ values, which costs $\Theta(n^2)$ for a statistic of linear cost. Lines L4 to L6 cost $\Theta(n)$. The $n$ values need $\Theta(n)$ space.
