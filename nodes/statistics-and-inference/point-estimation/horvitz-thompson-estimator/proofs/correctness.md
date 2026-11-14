---
title: The Horvitz-Thompson estimate and its variance estimates are unbiased
proves: [correctness]
status: full
---

The population is $\{1, \ldots, N\}$ with fixed values $y_1, \ldots, y_N$ and total $Y = \sum_i y_i$. The sample $S$ is drawn from a design $p$; $I_i$ is the indicator of $i \in S$, $\pi_i = \mathbb{E}[I_i]$, $\pi_{ij} = \mathbb{E}[I_iI_j]$ and $\pi_{ii} = \pi_i$. Write $\Delta_{ij} = \pi_{ij} - \pi_i\pi_j = \operatorname{Cov}(I_i, I_j)$ and, for units with $\pi_i > 0$, $\check y_i = y_i/\pi_i$. All expectations are over the design, and the arithmetic is exact.

**Lemma 1 (the loops).** HT-ESTIMATE returns $\hat Y = \sum_{i \in S}\check y_i$. HT-VARIANCE returns $v_{\mathrm{HT}} = \sum_{i \in S}\sum_{j \in S}\frac{\Delta_{ij}}{\pi_{ij}}\check y_i\check y_j$, and SYG-VARIANCE returns $v_{\mathrm{SYG}} = \sum_{i<j;\ i,j \in S}\frac{-\Delta_{ij}}{\pi_{ij}}(\check y_i - \check y_j)^2$.

*Proof.* Lines L2 and L3 add $\check y_i$ once for each $i \in S$ to $T = 0$. In HT-VARIANCE, the diagonal term $i = j$ of the double sum is $\frac{\pi_i - \pi_i^2}{\pi_i}\check y_i^2 = (1 - \pi_i)\check y_i^2$, which is line L7, and an off-diagonal term is $\frac{\pi_{ij} - \pi_i\pi_j}{\pi_{ij}}\check y_i\check y_j = (1 - \pi_i\pi_j/\pi_{ij})\check y_i\check y_j$, which is line L9; lines L6 and L8 visit every ordered pair once. In SYG-VARIANCE, $-\Delta_{ij}/\pi_{ij} = \pi_i\pi_j/\pi_{ij} - 1$, which is line L13, and line L12 visits every unordered pair once. $\square$

**Theorem 1 (unbiased estimate).** If $\pi_i > 0$ for every $i$, then $\mathbb{E}[\hat Y] = Y$. In general, if $\hat Y$ sums over the sampled units with $\pi_i > 0$ (no other units can be sampled), then $\mathbb{E}[\hat Y] = Y - \sum_{i : \pi_i = 0} y_i$.

*Proof.* A unit with $\pi_i = 0$ is in $S$ with probability 0, so with probability 1, $\hat Y = \sum_{i : \pi_i > 0} I_i\check y_i$. By linearity of expectation, $\mathbb{E}[\hat Y] = \sum_{i : \pi_i > 0}\pi_i\,y_i/\pi_i = \sum_{i : \pi_i > 0} y_i$. $\square$

**Theorem 2 (variance).** If $\pi_i > 0$ for every $i$, then
$$\operatorname{Var}[\hat Y] = \sum_{i=1}^N\sum_{j=1}^N \Delta_{ij}\,\check y_i\check y_j.$$

*Proof.* $\hat Y = \sum_i \check y_i I_i$ with constant coefficients, so $\operatorname{Var}[\hat Y] = \sum_i\sum_j \check y_i\check y_j \operatorname{Cov}(I_i, I_j)$, and $\operatorname{Cov}(I_i, I_j) = \mathbb{E}[I_iI_j] - \mathbb{E}[I_i]\mathbb{E}[I_j] = \Delta_{ij}$. For $i = j$, $\mathbb{E}[I_i^2] = \mathbb{E}[I_i] = \pi_i = \pi_{ii}$. $\square$

**Theorem 3 (HT variance estimate).** If $\pi_{ij} > 0$ for all $i, j$, then $\mathbb{E}[v_{\mathrm{HT}}] = \operatorname{Var}[\hat Y]$.

*Proof.* By Lemma 1, $v_{\mathrm{HT}} = \sum_{i}\sum_{j} I_iI_j\frac{\Delta_{ij}}{\pi_{ij}}\check y_i\check y_j$, the sum over all $N^2$ ordered pairs, since $I_iI_j = 1$ exactly when both units are in $S$ (and $I_iI_i = I_i$). Taking expectations term by term, $\mathbb{E}[I_iI_j] = \pi_{ij}$ cancels the denominator, which leaves the sum of Theorem 2. $\square$

**Lemma 4 (fixed size).** If every sample with $p(s) > 0$ has exactly $n$ units, then $\sum_{j=1}^N \Delta_{ij} = 0$ for every $i$.

*Proof.* $\sum_j I_j = n$ with probability 1. Multiply by $I_i$ and take expectations: $\sum_j \pi_{ij} = n\pi_i$. Taking expectations of $\sum_j I_j = n$ gives $\sum_j \pi_j = n$. So $\sum_j \Delta_{ij} = n\pi_i - \pi_i\cdot n = 0$. $\square$

**Theorem 5 (Sen-Yates-Grundy form).** For a fixed-size design with all $\pi_i > 0$,
$$\operatorname{Var}[\hat Y] = \sum_{i<j}(\pi_i\pi_j - \pi_{ij})(\check y_i - \check y_j)^2.$$

*Proof.* Expand the double sum $\sum_i\sum_j \Delta_{ij}(\check y_i - \check y_j)^2 = \sum_i \check y_i^2\sum_j\Delta_{ij} + \sum_j \check y_j^2\sum_i\Delta_{ij} - 2\sum_i\sum_j\Delta_{ij}\check y_i\check y_j$. $\Delta$ is symmetric, so by Lemma 4 both row and column sums vanish, and the double sum is $-2\operatorname{Var}[\hat Y]$ by Theorem 2. The diagonal terms of the double sum are 0 and each unordered pair appears twice, so $\operatorname{Var}[\hat Y] = -\frac12\sum_i\sum_j\Delta_{ij}(\check y_i - \check y_j)^2 = \sum_{i<j}(-\Delta_{ij})(\check y_i - \check y_j)^2$, and $-\Delta_{ij} = \pi_i\pi_j - \pi_{ij}$. $\square$

**Theorem 6 (SYG variance estimate).** For a fixed-size design with $\pi_{ij} > 0$ for all $i \ne j$, $\mathbb{E}[v_{\mathrm{SYG}}] = \operatorname{Var}[\hat Y]$. If moreover $\pi_{ij} \le \pi_i\pi_j$ for all $i \ne j$, then $v_{\mathrm{SYG}} \ge 0$ for every sample.

*Proof.* By Lemma 1, $v_{\mathrm{SYG}} = \sum_{i<j} I_iI_j\frac{\pi_i\pi_j - \pi_{ij}}{\pi_{ij}}(\check y_i - \check y_j)^2$ over all unordered pairs of the population. With $\mathbb{E}[I_iI_j] = \pi_{ij}$, the expectation is the sum of Theorem 5. Under the extra condition every term is a nonnegative number times a square. $\square$

**Corollary 7 (simple random sampling).** For $n$ of $N$ units without replacement, $n \ge 2$, $\hat Y = N\bar y_S$, and $v_{\mathrm{HT}} = v_{\mathrm{SYG}} = N^2(1 - f)s^2/n$ with $f = n/N$ and $s^2 = \frac{1}{n-1}\sum_{i \in S}(y_i - \bar y_S)^2$.

*Proof.* Here $\pi_i = f$ and $\pi_{ij} = \frac{n(n-1)}{N(N-1)}$ for $i \ne j$, so $\hat Y = \sum_{i \in S} y_i/f = N\bar y_S$. Then $1 - f^2/\pi_{ij} = -\frac{1-f}{n-1}$, so by Lemma 1
$$v_{\mathrm{HT}} = \frac{1-f}{f^2}\Big(\sum_{i \in S}y_i^2 - \frac{1}{n-1}\sum_{i \ne j \in S}y_iy_j\Big) = \frac{1-f}{f^2}\cdot\frac{n}{n-1}\Big(\sum_{i \in S}y_i^2 - n\bar y_S^2\Big) = \frac{N^2(1-f)}{n}s^2,$$
using $\sum_{i \ne j}y_iy_j = n^2\bar y_S^2 - \sum_i y_i^2$. For $v_{\mathrm{SYG}}$, the coefficient $\frac{f^2 - \pi_{ij}}{\pi_{ij}f^2}$ equals $\frac{(1-f)N^2}{n^2(n-1)}$, and $\sum_{i<j \in S}(y_i - y_j)^2 = n(n-1)s^2$, which gives the same value. $\square$

**Cost.** HT-ESTIMATE does one division and one addition per sampled unit, $2n$ operations. HT-VARIANCE runs line L7 $n$ times and line L9 $n(n-1)$ times, and SYG-VARIANCE runs line L13 $n(n-1)/2$ times, each a constant number of operations given $\pi_{ij}$; so both take $\Theta(n^2)$ time and $\Theta(1)$ extra space. All loops are over the finite set $S$, so the procedures terminate. $\square$
