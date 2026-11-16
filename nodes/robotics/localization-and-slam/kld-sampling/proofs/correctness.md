---
title: KLD-sampling stops at its bound, and the bound gives the coverage 1 - delta asymptotically
proves: [correctness]
status: full
---

**Setting.** One call of KLD-MCL with $\varepsilon > 0$, $\delta \in (0, 1)$ and integers $1 \le n_\text{min} \le n_\text{max}$. After $n$ draws, $k_n$ is the number of occupied bins and $n_\chi(k)$ is the value of line L8, with $n_\chi(k) = 0$ for $k \le 1$. For Part 3, $p = (p_1, \dots, p_k)$ is a distribution over $k \ge 2$ bins with all $p_j > 0$, $X_1, X_2, \dots$ are independent draws of $p$, $N_j$ is the number of the first $n$ draws in bin $j$, $\hat p_j = N_j / n$ and $K_n = \sum_j \hat p_j \log(\hat p_j / p_j)$, with $0 \log 0 = 0$. Let $q = \chi^2_{k-1, 1-\delta}$ and $n(\varepsilon) = \lceil q / (2\varepsilon) \rceil$.

**Assumptions.**

- (A1) The previous weights are $\ge 0$ with a positive sum, so line L3 is defined.
- (A2) For Part 3 only: the draws are independent and identically distributed with the distribution $p$ over the bins. This is an assumption about the samples, not something that the particle filter guarantees.

**Claim.**

1. The loop ends after at most $n_\text{max}$ iterations.
2. If it ends with $n < n_\text{max}$ draws, then $n \ge n_\text{min}$, $n \ge n_\chi(k_n)$, and the loop did not end after any earlier draw $n' < n$, that is, $n' < n_\text{min}$ or $n' < n_\chi(k_{n'})$.
3. Under (A2), $2 n K_n$ converges in distribution to the chi-square distribution with $k - 1$ degrees of freedom as $n \to \infty$, and $P(K_{n(\varepsilon)} \le \varepsilon) \to 1 - \delta$ as $\varepsilon \to 0$.

*Proof.*

*Claim 1.* Each iteration increases $n$ by 1 (line L9), starting from 0. The test of line L10 is true when $n \ge n_\text{max}$, so the loop ends at the latest after iteration $n_\text{max}$.

*Claim 2.* The loop tests line L10 after each draw, with the current values of $n$ and $n_\chi$. Line L8 sets $n_\chi$ to $n_\chi(k)$ each time $k$ grows past 1, and $n_\chi$ stays $0 = n_\chi(k)$ while $k \le 1$, so at each test $n_\chi = n_\chi(k_n)$. The loop ends at draw $n$ for the first $n$ where $(n \ge n_\chi(k_n)$ and $n \ge n_\text{min})$ or $n \ge n_\text{max}$. If $n < n_\text{max}$, the first part holds; the condition was false at each earlier $n'$, which gives the last statement.

*Claim 3.* Let $d_j = \hat p_j - p_j$, so $\sum_j d_j = 0$.

Step 1: Pearson's statistic. The vector $Y_n = \sqrt{n}\,(\hat p - p)$ is a normalized sum of $n$ independent copies of $e_{X} - p$, where $e_X$ is the unit vector of the bin of $X$. Its mean is 0 and its covariance is $\Sigma = \mathrm{diag}(p) - p p^\top$. By the multivariate [central limit theorem](/central-limit-theorem/), $Y_n \to Y \sim N(0, \Sigma)$ in distribution. Pearson's statistic is $X_n^2 = \sum_j n d_j^2 / p_j = Y_n^\top D Y_n$ with $D = \mathrm{diag}(1/p)$. The map $y \mapsto y^\top D y$ is continuous, so $X_n^2 \to Y^\top D Y$ in distribution. The vector $Y$ has the same distribution as $D^{-1/2} (I - s s^\top) G$ with $s = (\sqrt{p_1}, \dots, \sqrt{p_k})$ and $G \sim N(0, I)$: indeed $D^{-1/2}(I - s s^\top)(I - s s^\top)D^{-1/2} = D^{-1/2}(I - s s^\top) D^{-1/2} = \mathrm{diag}(p) - p p^\top$, because $s^\top s = 1$ makes $I - s s^\top$ a projection and $D^{-1/2} s = p$. Then $Y^\top D Y = G^\top (I - s s^\top) G$, the squared length of the projection of a standard normal vector onto a subspace of dimension $k - 1$. This has the chi-square distribution with $k - 1$ degrees of freedom.

Step 2: $2 n K_n - X_n^2 \to 0$ in probability. For $|t| \le 1/2$, Taylor's theorem gives $(1 + t)\log(1 + t) = t + t^2/2 + r(t)$ with $|r(t)| \le |t|^3$. (The third derivative of $(1+t)\log(1+t)$ is $-1/(1+t)^2$, of absolute value at most 4 on $|t| \le 1/2$, so $|r(t)| \le 4 |t|^3 / 6 \le |t|^3$.) With $t_j = d_j / p_j$,

$$K_n = \sum_j p_j (1 + t_j) \log(1 + t_j) = \sum_j d_j + \sum_j \frac{d_j^2}{2 p_j} + \sum_j p_j r(t_j) = \frac{X_n^2}{2n} + \sum_j p_j r(t_j)$$

on the event $E_n = \{\max_j |t_j| \le 1/2\}$. On $E_n$, $|2 n K_n - X_n^2| \le 2 n \sum_j p_j |t_j|^3 = 2 \sum_j |Y_{n,j}|^3 / (\sqrt{n}\, p_j^2)$. Since $Y_n$ converges in distribution, it is bounded in probability, so this tends to 0 in probability. By the law of large numbers $\hat p \to p$ almost surely, so $P(E_n) \to 1$. Hence $2 n K_n - X_n^2 \to 0$ in probability, and by Slutsky's theorem $2 n K_n \to \chi^2_{k-1}$ in distribution.

Step 3: the coverage. Let $F_n$ be the distribution function of $2 n K_n$ and $F$ that of $\chi^2_{k-1}$. $F$ is continuous, so by Pólya's theorem $\sup_x |F_n(x) - F(x)| \to 0$. As $\varepsilon \to 0$, $n = n(\varepsilon) \to \infty$, and $x_\varepsilon = 2 n(\varepsilon)\, \varepsilon$ lies in $[q, q + 2\varepsilon)$, so $x_\varepsilon \to q$. Then

$$|P(K_n \le \varepsilon) - (1 - \delta)| = |F_n(x_\varepsilon) - F(q)| \le \sup_x |F_n(x) - F(x)| + |F(x_\varepsilon) - F(q)| \to 0,$$

since $F(q) = 1 - \delta$ by the definition of $q$ and $F$ is continuous. $\blacksquare$

**What this does not show.** Claim 3 is a limit; it gives no error bound for a fixed $n$. The code uses the Wilson-Hilferty approximation of $q$, which the tests compare with the exact quantile. In the particle filter, the samples are drawn from the predicted belief and weighted afterwards, the number of bins $k$ is counted from the samples, and the errors of successive steps add up, so the claim does not bound the error of the filter. That use is a heuristic.
